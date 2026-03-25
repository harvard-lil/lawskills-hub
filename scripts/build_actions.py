"""Render skills as GPT Actions: static JSON endpoints + OpenAPI spec.

Produces a set of pre-rendered JSON files under _site/actions/ that a
ChatGPT Custom GPT can call via GPT Actions. The accompanying OpenAPI
schema describes the endpoints so the GPT knows how to progressively
discover and load skills.

Endpoint design (mirrors the meta-skill "action pack" progressive-load
pattern, but expressed as static files behind an OpenAPI spec):

  GET /actions/personas
      Lightweight index: id, label, headline, skill_count for each persona.

  GET /actions/personas/{persona_id}
      Full persona detail: design principles, tone, objective, plus a
      skills array with name + description (enough for the GPT to decide
      which skill to fetch).

  GET /actions/skills/{persona_id}/{skill_name}
      The complete SKILL.md body for one skill, plus metadata and a list
      of available reference documents.

  GET /actions/skills/{persona_id}/{skill_name}/references/{ref_name}
      A single reference markdown document shipped alongside a skill.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _parse_skill_md(path: Path) -> dict[str, Any]:
    """Parse a SKILL.md into frontmatter dict + body text."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", text, re.DOTALL)
    if not m:
        raise ValueError(f"No YAML frontmatter in {path}")
    fm: dict[str, Any] = {}
    for line in m.group(1).strip().splitlines():
        key, sep, val = line.partition(":")
        if sep:
            k = key.strip()
            v = val.strip()
            if k == "metadata":
                continue
            if k == "version":
                fm.setdefault("metadata", {})["version"] = v
            else:
                fm[k] = v
    return {"frontmatter": fm, "body": m.group(2).strip()}


def _discover_references(skill_dir: Path) -> list[dict[str, str]]:
    """List reference .md files in a skill's references/ subdirectory."""
    refs_dir = skill_dir / "references"
    if not refs_dir.is_dir():
        return []
    refs = []
    for f in sorted(refs_dir.iterdir()):
        if f.suffix == ".md" and f.is_file():
            refs.append(
                {
                    "name": f.stem,
                    "filename": f.name,
                }
            )
    return refs


def build_actions(
    personas: dict[str, dict],
    personas_config: list[dict],
    base_url: str,
    output_dir: Path,
    skills_dir: Path,
):
    """Render all GPT Actions static files and the OpenAPI spec.

    Parameters
    ----------
    personas : dict
        The discover_personas() result from build.py.
    personas_config : list[dict]
        Raw personas.yaml entries (for design metadata).
    base_url : str
        Deployed site base URL (used in OpenAPI `servers`).
    output_dir : Path
        The _site root.
    skills_dir : Path
        The source skills/ directory.
    """
    actions_dir = output_dir / "actions"
    actions_dir.mkdir(parents=True, exist_ok=True)

    config_by_id = {e["id"]: e for e in personas_config}

    # ------------------------------------------------------------------
    # 1. Personas index
    # ------------------------------------------------------------------
    persona_index: list[dict[str, Any]] = []
    for persona_id, pdata in personas.items():
        pm = pdata["meta"]
        design = pm.get("design", {})
        regular = [s for s in pdata["skills"] if not s["is_meta"]]
        meta_skills = [s for s in pdata["skills"] if s["is_meta"]]
        meta_description = meta_skills[0]["description"] if meta_skills else ""
        persona_index.append(
            {
                "id": persona_id,
                "label": pm.get("label", persona_id.replace("-", " ").title()),
                "description": meta_description,
                "objective": design.get("objective", ""),
                "skill_count": len(regular),
            }
        )

    _write_json(
        actions_dir / "personas.json",
        {
            "personas": persona_index,
            "description": (
                "Legal Ed Skills Hub persona index. Each persona targets a specific "
                "type of user and educational objective. Read the description and "
                "objective fields to decide which persona matches the user's needs, "
                "then fetch full detail at /actions/personas/{id}.json."
            ),
        },
    )

    # ------------------------------------------------------------------
    # 2. Per-persona detail
    # ------------------------------------------------------------------
    personas_out = actions_dir / "personas"
    personas_out.mkdir(parents=True, exist_ok=True)

    for persona_id, pdata in personas.items():
        pm = pdata["meta"]
        design = pm.get("design", {})
        regular = [s for s in pdata["skills"] if not s["is_meta"]]

        skills_summary = []
        for s in regular:
            skill_dir = s["dir"]
            refs = _discover_references(skill_dir)
            skills_summary.append(
                {
                    "name": s["name"],
                    "description": s["description"],
                    "version": s["version"],
                    "status": s["status"],
                    "has_references": len(refs) > 0,
                    "reference_count": len(refs),
                }
            )

        _write_json(
            personas_out / f"{persona_id}.json",
            {
                "id": persona_id,
                "label": pm.get("label", persona_id.replace("-", " ").title()),
                "headline": pm.get("headline", ""),
                "pitch": pm.get("pitch", ""),
                "design": design,
                "skills": skills_summary,
                "usage_hint": (
                    "Pick a skill by name, then fetch its full instructions at "
                    f"/actions/skills/{persona_id}/{{skill_name}}."
                ),
            },
        )

    # ------------------------------------------------------------------
    # 3. Per-skill full content
    # ------------------------------------------------------------------
    skills_out = actions_dir / "skills"

    for persona_id, pdata in personas.items():
        persona_skills_out = skills_out / persona_id
        persona_skills_out.mkdir(parents=True, exist_ok=True)

        for s in pdata["skills"]:
            if s["is_meta"]:
                continue
            skill_dir = s["dir"]
            parsed = _parse_skill_md(skill_dir / "SKILL.md")
            refs = _discover_references(skill_dir)

            ref_entries = []
            for r in refs:
                ref_entries.append(
                    {
                        "name": r["name"],
                        "fetch_path": f"/actions/skills/{persona_id}/{s['name']}/references/{r['name']}",
                    }
                )

            _write_json(
                persona_skills_out / f"{s['name']}.json",
                {
                    "name": s["name"],
                    "description": s["description"],
                    "version": s["version"],
                    "status": s["status"],
                    "persona": persona_id,
                    "skill_body": parsed["body"],
                    "references": ref_entries,
                    "usage_hint": (
                        "The skill_body field contains the full skill instructions. "
                        "Follow them to assist the user. "
                        "If references are listed, fetch them as needed for additional context."
                    )
                    if ref_entries
                    else (
                        "The skill_body field contains the full skill instructions. "
                        "Follow them to assist the user."
                    ),
                },
            )

    # ------------------------------------------------------------------
    # 4. Reference documents (nested under skills/, mirroring on-disk layout)
    # ------------------------------------------------------------------
    for persona_id, pdata in personas.items():
        for s in pdata["skills"]:
            if s["is_meta"]:
                continue
            skill_dir = s["dir"]
            refs = _discover_references(skill_dir)
            if not refs:
                continue

            ref_dir_out = skills_out / persona_id / s["name"] / "references"
            ref_dir_out.mkdir(parents=True, exist_ok=True)

            for r in refs:
                content = (skill_dir / "references" / r["filename"]).read_text(
                    encoding="utf-8"
                )
                _write_json(
                    ref_dir_out / f"{r['name']}.json",
                    {
                        "name": r["name"],
                        "skill": s["name"],
                        "persona": persona_id,
                        "content": content,
                    },
                )

    # ------------------------------------------------------------------
    # 5. OpenAPI spec
    # ------------------------------------------------------------------
    spec = _build_openapi_spec(personas, base_url)
    _write_json(actions_dir / "openapi.json", spec)

    # Also write YAML for human readability
    _write_openapi_yaml(actions_dir / "openapi.yaml", spec)

    skill_count = sum(
        len([s for s in p["skills"] if not s["is_meta"]]) for p in personas.values()
    )
    print(f"Built GPT Actions: {len(personas)} personas, {skill_count} skills")
    print(f"OpenAPI spec: {actions_dir / 'openapi.json'}")


def _build_openapi_spec(personas: dict[str, dict], base_url: str) -> dict[str, Any]:
    """Build the OpenAPI 3.1 spec describing all action endpoints."""
    persona_ids = list(personas.keys())
    all_skills: dict[str, list[str]] = {}
    all_refs: dict[str, dict[str, list[str]]] = {}

    for pid, pdata in personas.items():
        regular = [s for s in pdata["skills"] if not s["is_meta"]]
        all_skills[pid] = [s["name"] for s in regular]
        all_refs[pid] = {}
        for s in regular:
            refs = _discover_references(s["dir"])
            if refs:
                all_refs[pid][s["name"]] = [r["name"] for r in refs]

    server_url = (
        base_url.rstrip("/")
        if base_url
        else "https://example.github.io/skills-hub-demo"
    )

    return {
        "openapi": "3.1.0",
        "info": {
            "title": "Legal Ed Skills Hub",
            "description": (
                "Progressively discover and load pedagogical AI skills for legal education. "
                "Start with the personas list, drill into a persona for its skill inventory, "
                "then fetch individual skill instructions and reference materials as needed."
            ),
            "version": "1.0.0",
        },
        "servers": [{"url": server_url}],
        "paths": {
            "/actions/personas.json": {
                "get": {
                    "operationId": "listPersonas",
                    "summary": "List all available personas",
                    "description": (
                        "Returns a lightweight index of all personas in the Legal Ed Skills Hub. "
                        "Each entry includes the persona id, display label, headline, and number of skills. "
                        "Use a persona id to fetch its full detail."
                    ),
                    "responses": {
                        "200": {
                            "description": "Persona index",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/PersonaIndex",
                                    }
                                }
                            },
                        },
                    },
                },
            },
            "/actions/personas/{persona_id}.json": {
                "get": {
                    "operationId": "getPersona",
                    "summary": "Get full detail for one persona",
                    "description": (
                        "Returns a persona's design principles, pedagogical objective, tone, "
                        "and a list of available skills with descriptions. Use a skill name "
                        "to fetch its full instructions."
                    ),
                    "parameters": [_persona_id_param(persona_ids)],
                    "responses": {
                        "200": {
                            "description": "Persona detail with skill listing",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/PersonaDetail",
                                    }
                                }
                            },
                        },
                    },
                },
            },
            "/actions/skills/{persona_id}/{skill_name}.json": {
                "get": {
                    "operationId": "getSkill",
                    "summary": "Get full skill instructions",
                    "description": (
                        "Returns the complete skill instructions (the SKILL.md body) for one skill, "
                        "plus metadata and a list of available reference documents. "
                        "Follow the skill_body instructions to assist the user."
                    ),
                    "parameters": [
                        _persona_id_param(persona_ids),
                        _skill_name_param(all_skills),
                    ],
                    "responses": {
                        "200": {
                            "description": "Full skill content",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/SkillDetail",
                                    }
                                }
                            },
                        },
                    },
                },
            },
            "/actions/skills/{persona_id}/{skill_name}/references/{ref_name}.json": {
                "get": {
                    "operationId": "getReference",
                    "summary": "Get a skill's reference document",
                    "description": (
                        "Returns the content of a reference markdown document that accompanies a skill. "
                        "Only fetch when the skill instructions direct you to."
                    ),
                    "parameters": [
                        _persona_id_param(persona_ids),
                        _skill_name_param(all_skills),
                        _ref_name_param(all_refs),
                    ],
                    "responses": {
                        "200": {
                            "description": "Reference document content",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ReferenceDetail",
                                    }
                                }
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "PersonaIndex": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "personas": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "string",
                                        "description": "Persona identifier",
                                    },
                                    "label": {
                                        "type": "string",
                                        "description": "Display name",
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": (
                                            "When this persona applies: describes the type of user and "
                                            "tasks this persona handles. Use this to match against the "
                                            "user's question."
                                        ),
                                    },
                                    "objective": {
                                        "type": "string",
                                        "description": "The persona's core pedagogical objective and constraint",
                                    },
                                    "skill_count": {
                                        "type": "integer",
                                        "description": "Number of available skills",
                                    },
                                },
                            },
                        },
                    },
                },
                "PersonaDetail": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "label": {"type": "string"},
                        "headline": {"type": "string"},
                        "pitch": {"type": "string"},
                        "design": {
                            "type": "object",
                            "description": "Pedagogical design: objective, principles, tone, success criteria",
                            "properties": {
                                "objective": {"type": "string"},
                                "principles": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "tone": {"type": "string"},
                                "success": {"type": "string"},
                            },
                        },
                        "skills": {
                            "type": "array",
                            "description": "Available skills — fetch one by name to get full instructions",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "version": {"type": "string"},
                                    "status": {
                                        "type": "string",
                                        "enum": ["preview", "official"],
                                        "description": "Release status of the skill",
                                    },
                                    "has_references": {"type": "boolean"},
                                    "reference_count": {"type": "integer"},
                                },
                            },
                        },
                        "usage_hint": {"type": "string"},
                    },
                },
                "SkillDetail": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "version": {"type": "string"},
                        "status": {
                            "type": "string",
                            "enum": ["preview", "official"],
                            "description": "Release status of the skill",
                        },
                        "persona": {"type": "string"},
                        "skill_body": {
                            "type": "string",
                            "description": "Complete skill instructions in markdown. Follow these to assist the user.",
                        },
                        "references": {
                            "type": "array",
                            "description": "Reference documents available for this skill",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "fetch_path": {
                                        "type": "string",
                                        "description": "Path to fetch reference content",
                                    },
                                },
                            },
                        },
                        "usage_hint": {"type": "string"},
                    },
                },
                "ReferenceDetail": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "skill": {"type": "string"},
                        "persona": {"type": "string"},
                        "content": {
                            "type": "string",
                            "description": "Full markdown content of the reference document",
                        },
                    },
                },
            },
        },
    }


def _persona_id_param(persona_ids: list[str]) -> dict[str, Any]:
    return {
        "name": "persona_id",
        "in": "path",
        "required": True,
        "schema": {"type": "string", "enum": persona_ids},
        "description": "Persona identifier",
    }


def _skill_name_param(all_skills: dict[str, list[str]]) -> dict[str, Any]:
    flat = sorted({name for names in all_skills.values() for name in names})
    return {
        "name": "skill_name",
        "in": "path",
        "required": True,
        "schema": {"type": "string", "enum": flat},
        "description": "Skill name (unique within a persona)",
    }


def _ref_name_param(all_refs: dict[str, dict[str, list[str]]]) -> dict[str, Any]:
    flat = sorted(
        {
            name
            for skills in all_refs.values()
            for names in skills.values()
            for name in names
        }
    )
    return {
        "name": "ref_name",
        "in": "path",
        "required": True,
        "schema": {"type": "string", "enum": flat} if flat else {"type": "string"},
        "description": "Reference document name (without .md extension)",
    }


def _write_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _write_openapi_yaml(path: Path, spec: dict[str, Any]):
    """Write OpenAPI spec as YAML for human readability.

    Uses a minimal YAML emitter to avoid adding a PyYAML dependency
    just for this one output file. Falls back to JSON-in-YAML if the
    structure gets surprising.
    """
    try:
        import yaml as _yaml

        path.write_text(
            _yaml.dump(
                spec, default_flow_style=False, sort_keys=False, allow_unicode=True
            ),
            encoding="utf-8",
        )
    except ImportError:
        path.write_text(
            json.dumps(spec, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
