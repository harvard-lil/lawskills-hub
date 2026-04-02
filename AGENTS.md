# AGENTS.md

## Project Description
This repository contains the source code for the **Harvard Law School Library Innovation Lab (LIL) Agent Skills Hub**. It is a build-pipeline-backed website and distribution system for modular pedagogical "skills" for AI agents, organized around personas (law professor, law student, pro se litigant, CLE attorney, skill developer). The project includes a Python build system, an LLM-based test harness, a GPT Actions API, and a Claude Desktop Extension (.mcpb).

Skills in this project follow the open [Agent Skills](https://agentskills.io) standard (`SKILL.md` with YAML frontmatter + markdown body), ensuring portability across Claude Code, OpenAI Codex, Gemini CLI, Cursor, and other compatible agents.

## LIL Values

Every skill in this repository must embody these values. They are non-negotiable design constraints, not aspirational suggestions.

1. **Empower Human Agency.** Skills coach, orient, and build capability. They never replace the user's judgment or produce finished work product the user should create themselves. The user must remain the decision-maker.
2. **Be Transparent About Local/Remote System Access.** If a skill triggers web searches, API calls, or file system operations, it must say so explicitly in its instructions. No silent side effects.
3. **Prioritize Provenance and Explainability.** Skills should surface where information comes from. When a skill references research, existing syllabi, legal resources, or external data, it must attribute sources and explain its reasoning so the user can evaluate and verify.
4. **Design for Accessibility and Interoperability.** Skills must work across platforms (not just one agent product). Use plain language. Avoid jargon in user-facing output. Structure output for screen readers and assistive technology where feasible.
5. **Target Meaningful, Repeatable Friction.** Skills exist to solve tasks that are genuinely difficult, time-consuming, or error-prone when done manually -- and that recur often enough to justify encoding. Do not create skills for trivial or one-off tasks.

## Core Mandates
1.  **LIL Aesthetic:** High-contrast, bold typography, specific pastel accents (Green #8AAFBA, Blue #A7E2FF, Purple #F0D0FF, Yellow #FFF069).
2.  **Persona-Driven Architecture:** Skills are grouped by persona. Each persona has a meta skill that bundles and routes to specialized sub-skills. See `skills/personas.yaml` for the full persona list with design principles, tone, and success criteria.
3.  **Functionality:**
    *   **Filterable Skills Grid:** Users can filter skills by persona (Professor, Student, Pro Se, CLE, Skill Developer).
    *   **Video Training:** Embeds YouTube tutorials.
    *   **Install Page:** Tiered install options -- Custom GPT, Claude Desktop Extension (.mcpb), direct skill download, and developer API/source access.
    *   **Traces Viewer:** Browse evaluation traces from the test harness at `/traces/`.
    *   **GPT Actions API:** Static JSON endpoints with an OpenAPI spec (`/actions/`) for ChatGPT Custom GPT integration.
    *   **Claude Desktop Extension:** A `.mcpb` package (Node.js MCP server) built from `templates/mcpb/`.

## Skill Authoring Standards

Skills in this repository follow the [Agent Skills specification](https://agentskills.io/specification) and the best practices below. These standards apply to anyone creating or modifying skills.

### SKILL.md Structure

Every skill lives in `skills/<persona>/<skill-name>/SKILL.md` and contains:

```yaml
---
name: skill-name          # Required. Lowercase, hyphens only. Max 64 chars. Must match directory name.
description: ...          # Required. Max 1024 chars. What it does + when to use it.
metadata:
  version: "0.1.0"        # Semver string.
---
```

The markdown body is the Standard Operating Procedure (SOP) -- imperative, step-by-step instructions the agent follows. Keep it under 500 lines.

### Directory Layout Per Skill

```
skills/<persona>/<skill-name>/
├── SKILL.md              # Required: metadata + step-by-step instructions
├── references/           # Optional: documents the agent reads when needed (style guides, protocols, schemas)
├── rubric.yaml           # Optional: test scenarios, criteria, and anti-patterns for the test harness
└── assets/               # Optional: raw materials consumed by scripts, NOT loaded by the agent
```

**Progressive disclosure governs what goes where:**
- `SKILL.md` body: Instructions the agent always needs when the skill is active (~100-5000 tokens).
- `references/`: Material the agent loads on demand (e.g., `syllabus-research-protocol.md`). Keep references one level deep from SKILL.md -- no nested reference chains.
- `assets/`: Files consumed by scripts during execution. The agent should never read these directly.

### Writing the `description` Field

The description is the single most important element. Agents read only `name` and `description` at startup to decide whether to load a skill. The full SKILL.md body is only injected when the agent decides the skill is relevant.

**Formula:** `[What it does in third person] + Use when [3-5 natural-language trigger phrases the user might actually say].`

**Rules:**
- Write in **third person only** ("Creates a syllabus..." not "I create a syllabus..." or "Use this to create...").
- Answer **WHAT** (what the skill does) and **WHEN** (specific trigger phrases).
- Include **3-5 concrete trigger phrases** -- real sentences a user would type, not category labels.
- Trigger phrases must **disambiguate from sibling skills**. If two skills handle related tasks (e.g., `syllabus-traditional` vs. `syllabus-evidence-based`), the trigger phrases must route cleanly to the correct one.
- Include **input types** the skill handles (uploaded PDFs, pasted text, images of tables of contents, etc.).
- Stay under **1024 characters** (agentskills.io spec limit).

**Good example:**
```yaml
description: >-
  Creates a traditional Socratic law school course syllabus from provided content
  (uploaded PDFs, book table of contents images, pasted text). Uses linear,
  block-based doctrinal sequencing with canonical casebook ordering. Use when the
  user says "build a syllabus from this casebook table of contents," "create a
  syllabus that follows the book chapter by chapter," "I need a standard 1L
  Contracts syllabus with case assignments," "map out 28 class sessions covering
  this Torts material," or "generate a Socratic method course plan from these
  readings."
```

**Poor example:**
```yaml
description: Helps with syllabi.
```

### Writing the SKILL.md Body

- **Address the agent directly** using "you."
- **Be imperative and concrete.** "Ask the user for the number of class sessions" is good. "Help the user" is too vague.
- **State boundaries explicitly.** If the agent must never do something, say so in a dedicated section or inline.
- **Match instruction specificity to task fragility:**
  - High freedom: "Review the syllabus and suggest improvements." (Multiple valid approaches.)
  - Medium freedom: "Generate a syllabus using this structure. Customize section lengths as needed."
  - Low freedom: "Follow the exact steps below in order. Do not skip any." (Fragile, strict sequence.)
- **Assume the agent is already knowledgeable.** Only add context the agent doesn't already have. Do not explain what a PDF is or how law school works.
- **Use consistent terminology.** Pick one term and stick with it throughout (e.g., always "session" not sometimes "class" and sometimes "meeting").
- **Reference files with relative paths** using forward slashes: `references/syllabus-research-protocol.md`, not backslashes.

### Persona Compliance

Every skill must respect its persona's constraints defined in `skills/personas.yaml`:

| Persona | Objective | Key Constraint |
|---------|-----------|----------------|
| **Professor** | Improve the quality of legal education | Help design learning experiences, not produce student-facing work product |
| **Student** | Coach, encourage, and check understanding | Never produce finished work product the student would submit |
| **Pro Se** | Orient and connect | Never give legal advice; teach, orient, and empower |
| **CLE** | Coach and build skills | Build the attorney's own capabilities, not do work for them |
| **Skill Developer** | Help create effective pedagogical AI skills | Honor subject matter expertise; handle format and conventions |

A skill that violates its persona's constraints is broken regardless of how well it performs the task.

## Testing and Quality

### Rubric Files

Each skill can include a `rubric.yaml` defining test scenarios, criteria, and anti-patterns. The test harness (`tests/test_skills.py`) discovers these automatically.

A rubric contains:
- **`criteria.structural`**: Binary pass/fail checks (e.g., "Agent asks for missing information").
- **`criteria.pedagogical`**: Qualitative assessments weighted high/medium/low (e.g., "Follows source ordering").
- **`anti_patterns`**: Things the skill must NOT do (e.g., "Injects evidence-based techniques into a traditional syllabus").
- **`test_scenarios`**: Scripted multi-turn conversations with expected behaviors.

### Running Tests

```bash
uv run pytest tests/ -v -s          # Requires OPENROUTER_API_KEY in .env
uv run pytest tests/ -v -s --rerun  # Re-run scenarios that already have traces
```

### The A/B Testing Method

When iterating on a skill:

1. **Trigger test:** In a fresh agent session, use natural language matching your trigger phrases. If the skill under-triggers (doesn't activate when it should), broaden the description. If it over-triggers (activates on unrelated tasks), narrow it.
2. **Functional test:** Run the skill 4-5 times with different inputs. If output varies wildly, tighten the instructions (reduce degrees of freedom).
3. **Value benchmark:** Compare the agent's output with the skill vs. without it. If the skill does not improve quality, speed, or consistency, reconsider whether it should exist.
4. **Cross-model test:** If feasible, test with multiple models. What works for a powerful model may need more detail for a smaller one.

### Evaluation-Driven Development

Build evaluations before writing extensive instructions:
1. Run the agent on representative tasks without the skill. Document specific failures.
2. Create 3+ test scenarios that target those failures.
3. Establish a baseline score.
4. Write minimal instructions to address the gaps.
5. Iterate: run evaluations, compare against baseline, refine.

## Build System
The site requires a Python build step. **No raw HTML is served directly from the repo.**

*   **Toolchain:** Python 3.12+, managed with `uv`. Dependencies in `pyproject.toml` (jinja2, pyyaml, python-dotenv, openai, pytest).
*   **Build command:** `uv run scripts/build.py --base-url <URL>` (reads `.env` for defaults).
*   **Output:** Everything is rendered into `_site/` (gitignored), which is the deploy artifact.
*   **Configuration:** `.env` (from `.env.example`) sets `BASE_URL` and `REPO_URL`. The build also accepts `--repo-url` and `--custom-gpt-url` flags.

## File Structure
*   `skills/` -- Skill source files, organized by persona.
    *   `skills/personas.yaml` -- Defines the persona list, display order, labels, design principles, and tone.
    *   `skills/<persona>/<skill-name>/SKILL.md` -- Each skill's instructions (YAML frontmatter + markdown body). Frontmatter fields: `name`, `description`, `status` (`preview` or `official`; defaults to `preview`), `metadata.version`.
    *   `skills/<persona>/<skill-name>/rubric.yaml` -- Test rubric with scenarios, criteria, and anti-patterns.
    *   `skills/<persona>/<skill-name>/references/` -- Optional reference markdown documents shipped with the skill.
    *   `skills/<persona>/<persona>-meta/SKILL.md` -- The meta skill that bundles all sub-skills for a persona.
*   `website/` -- Jinja2 HTML templates and static assets for the site.
    *   `website/_base.html` -- Base template (header, footer, nav).
    *   `website/index.html` -- Homepage (hero, training videos, persona-filterable skills grid).
    *   `website/install.html` -- Tiered install guide (Custom GPT, Claude Desktop, direct download, developer).
    *   `website/traces/index.html` -- Trace viewer UI.
    *   `website/css/styles.css` -- CSS variables for colors/fonts. Responsive grid layout.
    *   `website/css/traces.css` -- Styles for the trace viewer.
    *   `website/js/app.js` -- Fetches inventory JSON at runtime, builds filter buttons and persona sections dynamically.
    *   `website/js/traces.js` -- Trace viewer logic.
*   `scripts/` -- Python build scripts.
    *   `scripts/build.py` -- Main build: discovers skills, zips `.skill` files, generates inventory JSON, renders HTML, builds GPT Actions and .mcpb.
    *   `scripts/build_actions.py` -- Generates the GPT Actions static JSON endpoints and OpenAPI spec.
    *   `scripts/build_mcpb.py` -- Builds the Claude Desktop Extension `.mcpb` zip from `templates/mcpb/`.
*   `templates/` -- Build-time templates.
    *   `templates/meta-skill.md` -- Template for rendering meta skill SKILL.md files with bundled skill listings.
    *   `templates/mcpb/` -- Source for the Claude Desktop Extension (manifest.json, Node.js MCP server).
*   `tests/` -- LLM-based test harness for evaluating skill quality.
    *   `tests/test_config.yaml` -- Configures models under test and judge models (uses OpenRouter API).
    *   `tests/test_skills.py` -- Discovers `rubric.yaml` files, runs scenarios against models, evaluates with judge LLMs.
    *   `tests/conftest.py` -- Pytest fixtures, rubric discovery, and trace index rebuild on session finish.
    *   `tests/harness/runner.py` -- Runs multi-turn conversations between a model (with skill as system prompt) and scripted user messages.
    *   `tests/harness/evaluator.py` -- Evaluates traces against rubric criteria (structural pass/fail, pedagogical strong/adequate/weak, anti-pattern violation detection). Scores 0-100.
    *   `tests/harness/trace_writer.py` -- Saves trace JSON to `traces/` and rebuilds `traces/index.json`.
*   `traces/` -- Evaluation trace data (JSON files), organized by `<persona>/<skill>/<version>/`. Includes `index.json` for the web viewer.
*   `.github/workflows/deploy.yml` -- CI/CD: installs uv, runs the build, deploys `_site/` to GitHub Pages.
*   `assets/` -- Static assets (currently empty).

## How to Modify
*   **Add a skill:** Create `skills/<persona>/<skill-name>/SKILL.md` with YAML frontmatter (name, description, version) and markdown body. Optionally add a `rubric.yaml` for testing and a `references/` directory. The build script discovers it automatically. Follow the Skill Authoring Standards above.
*   **Add a persona:** Add an entry to `skills/personas.yaml` (with id, label, headline, pitch, design objective, principles, tone, and success criteria) and create the persona directory with a meta skill (`<persona>-meta/SKILL.md`).
*   **Change styles:** Edit CSS variables in `website/css/styles.css`.
*   **Update videos:** Change iframe src in `website/index.html`.
*   **Update install options:** Edit `website/install.html` (Jinja2 template).
*   **Test skills:** Run `uv run pytest tests/ -v -s` (requires `OPENROUTER_API_KEY` in `.env`). Use `--rerun` to re-run scenarios that already have traces.

## Deployment
This project is deployed via GitHub Pages from the `main` branch using a GitHub Actions workflow (`.github/workflows/deploy.yml`). The workflow runs `uv run scripts/build.py` to produce the `_site/` artifact, which is then deployed. A `CUSTOM_GPT_URL` repository variable can be set to enable the ChatGPT install option.
