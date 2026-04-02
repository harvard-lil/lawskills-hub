# Legal Ed Agent Skills Hub

A collection of AI agent skills for legal education, built by the [Harvard Law School Library Innovation Lab](https://lil.law.harvard.edu/).

## Why This Exists

People are already using AI to teach and learn the law -- to prepare for class, study for exams, understand legal issues, build professional skills. Much of that use, especially for students, happens without pedagogical guidance: the AI helps, but we need to think about *how* it should help for a given educational context.

This project explores what it looks like to bring sound pedagogy to AI-assisted legal education. The vehicle is **agent skills** -- modular capabilities you install into an AI coding or writing assistant. Each skill encodes a pedagogical approach: not just "help me with X," but "help me with X in a way that builds understanding / develops capability / orients me toward the right resources."

### Skills as markdown, not software

A skill is a markdown file. It contains instructions that shape how an AI agent approaches a task -- what questions to ask, what steps to follow, what tone to use, what to avoid. Writing a skill is closer to writing a lesson plan than writing code.

This matters because the people who know how law should be taught -- professors, clinical faculty, librarians, practitioners -- are mostly not software developers. By structuring legal edtech as markdown files with clear conventions, subject matter experts can create, review, and iterate on AI-assisted educational tools directly, without writing code or depending on engineers.

### Rapid exploration

Each skill is a self-contained experiment in AI-assisted pedagogy. You can write one in an afternoon, test it immediately, and iterate based on what works. The collection can grow to dozens of skills across different educational contexts without any of them depending on each other. This makes it practical to explore a wide range of approaches quickly -- traditional Socratic methods alongside evidence-based designs, student coaching alongside professional development, legal information alongside legal research training.

## How It Works

### Personas

Skills are organized by **persona** -- the role someone occupies when using them. Each persona is associated with a **pedagogical objective** that shapes every skill in the collection: not just what the skills do, but how they do it.

| Persona | Skill Objective | Key constraint |
|---------|-----------|----------------|
| **Instructor** | Improve the quality of legal education | Help design learning experiences, not produce student-facing work product |
| **Student** | Coach, encourage, and check understanding | Never produce finished work product the student would submit |
| **Pro Se** | Orient and connect | Never give legal advice; teach, orient, and empower |
| **CLE** | Coach and build skills | Build the attorney's own capabilities, not do work for them |
| **Skill Developer** | Help SMEs create effective pedagogical AI skills | Honor domain expertise; handle format and conventions |

The pedagogical objectives are design constraints, not labels. A pro-se skill should never do legal research *for* the user; it should teach them how to find relevant information and connect them with professional help. A student skill should coach rather than produce finished answers. These constraints are defined in `skills/personas.yaml` alongside design principles, tone guidance, and success criteria for each persona.

### Meta skills: making the collection sticky

Individual skills do one job well, but they're forgettable -- you have to remember they exist and go find them. A **meta skill** solves this by acting as an ambient capability layer for an entire persona.

You install one meta skill for your role. From that point on:

1. You describe tasks normally ("I need to build a syllabus," "check if I understand this case").
2. The meta skill triggers on any task within the persona's domain.
3. It checks whether a specialized skill is already installed that handles the task.
4. If yes: it defers to that skill.
5. If no: it fetches the persona's inventory from a live JSON endpoint and recommends relevant skills with install links.
6. If nothing matches: it assists directly, guided by the persona's pedagogical objective.

The user never has to remember skill names or revisit the website. The meta skill handles discovery, making the collection feel like an always-available set of competencies rather than a catalog you visit once.

### Skill format

Each skill is a folder with a `SKILL.md` file and optional reference material. The SKILL.md has YAML frontmatter (`name` and `description` -- the trigger that tells the agent when to activate the skill) and a markdown body (the instructions the agent follows after activation). No code required.

## Skills in This Collection

Skills are labeled **Official** (tested and stable) or **Preview** (experimental/in development, may change).

### Instructor

- **Syllabus Traditional** `Official` -- Creates a conventional Socratic law school syllabus from provided course materials, using linear doctrinal sequencing and casebook ordering.
- **Syllabus Evidence-Based** `Preview` -- Creates a modern syllabus using evidence-supported pedagogical techniques and learning strategies such as the spiral approach, spaced practice, interleaving, and backward design.

### Student

- **Understanding Check** `Preview` -- Conducts a structured diagnostic to identify gaps and misconceptions halfway through a course.
- **Exam Answer Eval** `Preview` -- Evaluates a practice exam answer along standard law school dimensions (issue-spotting, analysis, counterarguments) with specific, actionable feedback.
- **Socratic Tutor** `Preview` -- Conducts a Socratic dialogue on assigned readings to prepare for class.

### Pro Se

- **Issue Interview** `Preview` -- A structured intake interview that helps someone understand their legal issue in plain language and prepare to seek help.
- **Research Coach** `Preview` -- Teaches how to find and read relevant law, rather than doing the research for them.

### CLE

- **Development Plan** `Preview` -- Creates a structured professional development plan with quarterly milestones.
- **Topic Curriculum** `Preview` -- Builds a self-study curriculum for transitioning into a new practice area.
- **Client Email Coach** `Preview` -- Reviews draft client emails with specific feedback on clarity, tone, and risk management.

### Skill Developer

- **Skill Creator** `Preview` -- Walks a subject matter expert through authoring a new SKILL.md, handling format and conventions while the user supplies the educational judgment.
- **Skill Reviewer** `Preview` -- Evaluates an existing skill for format compliance, persona alignment, pedagogical quality, and agent-readiness.
- **Skill Tester** `Preview` -- Helps define rubrics and test scenarios for a skill, and evaluates conversation traces against those rubrics.

## Delivery

The core of this project is the `skills/` directory: markdown files in the [Agent Skills](https://agentskills.org/) format. But not every chat client makes agent skills easy or convenient to install, and keeping a full collection up to date is harder still. Skills are a simple concept -- progressive context management (load a list of descriptions, load a SKILL.md, load references) -- and that's easy to replicate in lots of ways.

So we use a flexible build approach that meets people where they're at:

- **ChatGPT**: We build a static JSON API with an [OpenAPI spec](https://developers.openai.com/docs/actions/introduction) that a Custom GPT can use as an Action. The GPT calls the API to discover and load skills on demand.
- **Claude Desktop**: We build a `.mcpb` [Desktop Extension](https://www.anthropic.com/engineering/desktop-extensions) that packages a lightweight MCP server. Double-click to install; the server fetches skills from the same static API.
- **Raw skills**: The `.skill` zip files and JSON inventories are available for any agent that supports the Agent Skills format directly.
- **API**: Any tool-calling agent can point at the OpenAPI spec and use the API without a wrapper.

We intend to keep iterating on this to address more clients and offer a smoother experience. The install page on the website guides users to the right option for their setup.

## Development

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
# Build the site locally (relative URLs)
uv run scripts/build.py

# Build for deployment (absolute URLs)
uv run scripts/build.py --base-url https://example.github.io/skills-hub-demo/

# Preview
uv run python -m http.server -d _site
```

The build script reads `skills/` and produces `_site/` containing `.skill` zip files, JSON inventories, the Claude Desktop extension (`.mcpb`), GPT Actions API, and the static website. HTML pages use Jinja2 templates (in `website/`) with a shared `_base.html` layout. The website is deployed to GitHub Pages automatically on push to `main`.

### Testing skills

Skills are hard to evaluate with certainty -- the same skill, model, and prompt can produce different results on different runs, and "good pedagogy" is partly subjective. The test harness doesn't try to produce a definitive pass/fail. Instead, it builds up a log of scored conversations over time so you can see whether quality is roughly stable, improving, or regressing. Think of it as a progress log, not a gate.

Each skill can include a `rubric.yaml` alongside its `SKILL.md` that defines:

- **Structural criteria** -- concrete, checkable behaviors ("agent asks about context before diving in")
- **Pedagogical criteria** -- subjective quality dimensions rated strong/adequate/weak ("agent coaches rather than tells")
- **Anti-patterns** -- things that should never happen ("agent produces finished work product")
- **Test scenarios** -- scripted user messages with expected behaviors

The harness plays out each scenario against a model, then evaluates the conversation using an LLM judge that scores each criterion independently. Results are saved as JSON trace files in `traces/`, checked into version control as a quality record.

```bash
# Configure API access (edit .env with your key)
echo "OPENROUTER_API_KEY=your-key-here" > .env

# Run skill tests (with real-time logging)
uv run pytest tests/ -v -s

# Run in parallel (much faster — each scenario runs in its own worker)
uv run pytest tests/ -v -n auto
```

Criterion evaluations within each scenario also run concurrently (each is an independent judge API call), so even a single-worker run is faster than fully sequential.

**Traces are write-once by default.** If a trace already exists for a given (skill, version, scenario, model) combination, the test skips it. This keeps test runs cheap -- you only pay API costs for new scenarios or new skill versions. To force a fresh run of everything (e.g., to add another data point), pass `--rerun`:

```bash
uv run pytest tests/ -v -s --rerun
```

**Null baselines.** Every scenario also runs with no skill installed -- just a bare "You are a helpful assistant." prompt. These null traces (stored at version `_null`) show what the model does on its own, so you can see what value the skill is actually adding. Null baselines never fail the test suite; they're purely for comparison.

Test configuration (models, API endpoint) is in `tests/test_config.yaml`.

### Viewing traces

Trace files accumulate in `traces/` with a `traces/index.json` manifest that the viewer reads. To browse them:

```bash
uv run python -m http.server -d traces
# Open http://localhost:8000/
```

The viewer groups traces by skill and scenario, shows sparkline score trends over time, and lets you click into any run to see the full conversation and per-criterion evaluations. Compare skilled vs. null runs to see where the skill is making a difference and where the bare model already does fine.

## Contributing

We welcome contributions from experienced practitioners, clinical faculty, academic labs, and law firms. Skills are markdown files -- writing one is closer to writing a lesson plan than writing code -- so you do not need to be a software engineer to contribute.

See [CONTRIBUTING.md](CONTRIBUTING.md) for a full guide: how to create or improve a skill, how to write a rubric and run the test harness locally, and how to submit a pull request.

## License

TBD
