#!/usr/bin/env python3
"""Build the Legal Ed Skills Hub site.

Reads skills from skills/<persona>/<skill-name>/SKILL.md, produces:
  _site/skills/<persona>/<skill-name>.skill  (zip files, individual)
  _site/skills/<persona>/<persona>-meta.skill (zip bundling all persona skills)
  _site/inventory/<persona>.json             (per-persona inventory)
  _site/inventory/personas.json              (persona index)
  _site/index.html, css/, js/                (website)
"""

import argparse
import json
import os
import re
import shutil
import zipfile
from pathlib import Path

import jinja2
import yaml
from dotenv import load_dotenv

from build_actions import build_actions

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
WEBSITE_DIR = PROJECT_ROOT / "website"
TRACES_DIR = PROJECT_ROOT / "traces"
OUTPUT_DIR = PROJECT_ROOT / "_site"


def load_personas_config() -> list[dict]:
    """Load the personas list from skills/personas.yaml. List order = display order."""
    config_path = SKILLS_DIR / "personas.yaml"
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter (name, description, version, …) from a SKILL.md file."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        raise ValueError(f"No YAML frontmatter in {path}")
    result = {}
    for line in m.group(1).strip().splitlines():
        key, sep, val = line.partition(":")
        if sep:
            result[key.strip()] = val.strip()
    return result


def load_meta_template() -> str:
    """Load the meta skill template from templates/meta-skill.md."""
    return (TEMPLATES_DIR / "meta-skill.md").read_text(encoding="utf-8")


def parse_meta_sections(path: Path) -> dict[str, str]:
    """Parse a meta SKILL.md into sections for template rendering.

    Returns dict with keys: frontmatter, intro, assist_directly, extra_sections.
    The SKILL.md is split at '## Assist Directly'; everything before is intro,
    everything after is assist_directly + any trailing sections (boundaries etc.).
    """
    text = path.read_text(encoding="utf-8")

    m = re.match(r"(---\s*\n.*?\n---)\s*\n(.*)", text, re.DOTALL)
    if not m:
        raise ValueError(f"Cannot parse meta skill: {path}")
    frontmatter = m.group(1)
    body = m.group(2)

    parts = re.split(r"^## Assist Directly\s*$", body, maxsplit=1, flags=re.MULTILINE)
    intro = parts[0].strip()

    if len(parts) > 1:
        after = parts[1].strip()
        sub = re.split(r"(?=^## )", after, maxsplit=1, flags=re.MULTILINE)
        assist_directly = sub[0].strip()
        extra_sections = sub[1].strip() if len(sub) > 1 else ""
    else:
        assist_directly = ""
        extra_sections = ""

    return {
        "frontmatter": frontmatter,
        "intro": intro,
        "assist_directly": assist_directly,
        "extra_sections": extra_sections,
    }


def render_meta_skill(
    template: str, sections: dict[str, str], replacements: dict[str, str]
) -> str:
    """Render a meta skill by filling the template with sections and build-time values."""
    content = template
    for key, value in {**sections, **replacements}.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content


def discover_personas() -> dict[str, dict]:
    """Load personas.yaml, then scan each persona's skill directories.

    Returns an ordered dict: {persona_id: {meta: ..., skills: [...]}}.
    Order matches the list order in personas.yaml.
    """
    config = load_personas_config()
    personas: dict[str, dict] = {}
    for entry in config:
        persona_id = entry["id"]
        persona_dir = SKILLS_DIR / persona_id
        if not persona_dir.is_dir():
            continue
        skills = []
        for skill_dir in sorted(persona_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            fm = parse_frontmatter(skill_md)
            skills.append(
                {
                    "name": fm.get("name", skill_dir.name),
                    "description": fm.get("description", ""),
                    "version": fm.get("version", "0.0.0"),
                    "status": fm.get("status", "preview"),
                    "dir": skill_dir,
                    "is_meta": skill_dir.name.endswith("-meta"),
                }
            )
        if skills:
            personas[persona_id] = {"meta": entry, "skills": skills}
    return personas


def zip_skill(skill_dir: Path, output_path: Path):
    """Zip a single skill directory as a .skill file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(skill_dir.rglob("*")):
            if not file.is_file():
                continue
            arcname = file.relative_to(skill_dir.parent)
            zf.write(file, arcname)


def zip_meta_skill(
    meta_dir: Path,
    bundled_dirs: list[Path],
    output_path: Path,
    rendered_skill_md: str,
):
    """Zip a meta skill with bundled persona skills in references/.

    The agent skills spec requires a single skill directory per archive.
    Bundled skills are placed under <meta-name>/references/<skill-name>/
    so the meta SKILL.md can reference them via relative paths.
    """
    meta_name = meta_dir.name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{meta_name}/SKILL.md", rendered_skill_md)

        for file in sorted(meta_dir.rglob("*")):
            if not file.is_file() or file.name == "SKILL.md":
                continue
            arcname = file.relative_to(meta_dir.parent)
            zf.write(file, arcname)

        for skill_dir in bundled_dirs:
            for file in sorted(skill_dir.rglob("*")):
                if not file.is_file():
                    continue
                rel = file.relative_to(skill_dir)
                if rel.name == "SKILL.md" and rel.parent == Path("."):
                    rel = Path("subskill.md")
                arcname = Path(meta_name) / "references" / skill_dir.name / rel
                zf.write(file, str(arcname))


def build_bundled_skills_text(skills: list[dict]) -> str:
    """Generate the bundled skills listing for injection into a meta SKILL.md."""
    lines = []
    for s in skills:
        ref_path = f"references/{s['name']}/subskill.md"
        status_label = s["status"].capitalize()
        lines.append(
            f"- **{s['name']}** (v{s['version']}, {status_label}): {s['description']}  \n"
            f"  Full instructions: `{ref_path}`"
        )
    return "\n".join(lines)


def build_inventory(
    personas: dict[str, dict], base_url: str, repo_url: str = ""
) -> dict:
    """Generate per-persona inventories and the persona index.

    Inventory JSON is kept for the website even though meta skills no
    longer fetch it at runtime.
    """
    persona_index = []
    inventories = {}

    for persona_id, persona_data in personas.items():
        pm = persona_data["meta"]
        design = pm.get("design", {})

        meta_skill = None
        regular_skills = []
        for s in persona_data["skills"]:
            entry = {
                "name": s["name"],
                "description": s["description"],
                "install_url": f"{base_url}skills/{persona_id}/{s['name']}.skill",
                "version": s["version"],
                "status": s["status"],
                "source_path": f"skills/{persona_id}/{s['name']}",
            }
            if s["is_meta"]:
                meta_skill = entry
            else:
                regular_skills.append(entry)

        inventory = {
            "persona": persona_id,
            "label": pm.get("label", persona_id.replace("-", " ").title()),
            "headline": pm.get("headline", ""),
            "pitch": pm.get("pitch", ""),
            "design": design,
            "meta_skill": meta_skill,
            "skills": regular_skills,
        }
        inventories[persona_id] = inventory

        persona_index.append(
            {
                "id": persona_id,
                "label": pm.get("label", persona_id.replace("-", " ").title()),
                "headline": pm.get("headline", ""),
                "inventory_url": f"{base_url}inventory/{persona_id}.json",
                "meta_skill_url": meta_skill["install_url"] if meta_skill else None,
                "skill_count": len(regular_skills),
            }
        )

    return {
        "personas": {"personas": persona_index, "repo_url": repo_url},
        "inventories": inventories,
    }


def build_website(base_url: str, *, repo_url: str = "", custom_gpt_url: str = ""):
    """Render Jinja2 HTML templates and copy static assets to _site/."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(WEBSITE_DIR)),
        autoescape=False,
        keep_trailing_newline=True,
    )

    mcpb_download_url = f"{base_url}packages/mcpb/legal-ed-skills-hub.mcpb"

    for html_path in WEBSITE_DIR.rglob("*.html"):
        if html_path.name.startswith("_"):
            continue
        rel = html_path.relative_to(WEBSITE_DIR)
        root = "../" * (len(rel.parts) - 1)

        template = env.get_template(str(rel))
        rendered = template.render(
            base_url=base_url,
            repo_url=repo_url,
            root=root,
            custom_gpt_url=custom_gpt_url,
            mcpb_download_url=mcpb_download_url,
        )

        dest = OUTPUT_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rendered, encoding="utf-8")

    for item in WEBSITE_DIR.rglob("*"):
        if not item.is_file() or item.suffix == ".html":
            continue
        rel = item.relative_to(WEBSITE_DIR)
        dest = OUTPUT_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)


def build(base_url: str, *, repo_url: str = "", custom_gpt_url: str = ""):
    """Run the full build."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    meta_template = load_meta_template()
    personas = discover_personas()

    for persona_id, persona_data in personas.items():
        meta_skill = None
        regular_skills = []
        for skill in persona_data["skills"]:
            if skill["is_meta"]:
                meta_skill = skill
            else:
                regular_skills.append(skill)

        for skill in regular_skills:
            output_path = OUTPUT_DIR / "skills" / persona_id / f"{skill['name']}.skill"
            zip_skill(skill["dir"], output_path)

        if meta_skill:
            sections = parse_meta_sections(meta_skill["dir"] / "SKILL.md")
            repo_skills = f"{repo_url}tree/main/skills/{persona_id}" if repo_url else ""
            issues = f"{repo_url}issues" if repo_url else ""
            rendered = render_meta_skill(
                meta_template,
                sections,
                {
                    "bundled_skills": build_bundled_skills_text(regular_skills),
                    "hub_url": base_url or "",
                    "inventory_url": f"{base_url}inventory/{persona_id}.json",
                    "repo_skills_url": repo_skills,
                    "issues_url": issues,
                },
            )
            output_path = (
                OUTPUT_DIR / "skills" / persona_id / f"{meta_skill['name']}.skill"
            )
            zip_meta_skill(
                meta_skill["dir"],
                [s["dir"] for s in regular_skills],
                output_path,
                rendered,
            )

    # Generate inventories (still used by the website)
    inv_data = build_inventory(personas, base_url, repo_url)

    inv_dir = OUTPUT_DIR / "inventory"
    inv_dir.mkdir(parents=True, exist_ok=True)

    for persona_id, inventory in inv_data["inventories"].items():
        (inv_dir / f"{persona_id}.json").write_text(
            json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    (inv_dir / "personas.json").write_text(
        json.dumps(inv_data["personas"], indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Render website HTML templates and copy static assets
    build_website(base_url, repo_url=repo_url, custom_gpt_url=custom_gpt_url)

    # Copy trace data (JSON files) into _site/traces/
    if TRACES_DIR.is_dir():
        traces_out = OUTPUT_DIR / "traces"
        traces_out.mkdir(parents=True, exist_ok=True)
        for item in TRACES_DIR.rglob("*"):
            if not item.is_file():
                continue
            if item.name == "index.html":
                continue
            rel = item.relative_to(TRACES_DIR)
            dest = traces_out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)

    # GPT Actions (static OpenAPI + JSON endpoints)
    build_actions(
        personas=personas,
        personas_config=load_personas_config(),
        base_url=base_url,
        output_dir=OUTPUT_DIR,
        skills_dir=SKILLS_DIR,
    )

    # Claude Desktop Extension (.mcpb)
    from build_mcpb import build_mcpb

    build_mcpb(base_url, output_dir=OUTPUT_DIR / "packages" / "mcpb")

    # Summary
    skill_count = sum(len(p["skills"]) for p in personas.values())
    print(f"Built {skill_count} skills across {len(personas)} personas")
    print(f"Output: {OUTPUT_DIR}")


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    parser = argparse.ArgumentParser(description="Build the Legal Ed Skills Hub site")
    parser.add_argument(
        "--base-url",
        default=os.environ.get("BASE_URL", ""),
        help="Base URL prefix for all links (e.g. https://x.github.io/repo/). "
        "Defaults to BASE_URL from .env or empty string for relative paths.",
    )
    parser.add_argument(
        "--repo-url",
        default=os.environ.get("REPO_URL", ""),
        help="GitHub repo URL (e.g. https://github.com/org/repo/). "
        "Used for 'edit' links on the website. "
        "Defaults to REPO_URL from .env or empty string.",
    )
    parser.add_argument(
        "--custom-gpt-url",
        default=os.environ.get("CUSTOM_GPT_URL", ""),
        help="URL of the ChatGPT Custom GPT. "
        "Defaults to CUSTOM_GPT_URL from .env or empty string (shows 'coming soon').",
    )
    args = parser.parse_args()

    base = args.base_url
    if base and not base.endswith("/"):
        base += "/"

    repo = args.repo_url
    if repo and not repo.endswith("/"):
        repo += "/"

    build(base, repo_url=repo, custom_gpt_url=args.custom_gpt_url)


if __name__ == "__main__":
    main()
