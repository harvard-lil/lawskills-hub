# Contributing to the LIL Skills Hub

We welcome contributions from experienced practitioners, clinical faculty, academic labs, and law firms. If you have pedagogical expertise you want to encode into a skill -- or if you see room to improve an existing one -- this guide is for you.

Because skills are markdown files, **you do not need to be a software engineer to contribute.** Writing a skill is closer to writing a lesson plan than writing code. The sections below walk through everything you need to get started.

## Table of Contents

- [LIL values](#lil-values)
- [What we are looking for](#what-we-are-looking-for)
- [Before you start](#before-you-start)
- [How to create a new skill](#how-to-create-a-new-skill)
- [How to improve an existing skill](#how-to-improve-an-existing-skill)
- [How to test your skill](#how-to-test-your-skill)
- [Submitting a pull request](#submitting-a-pull-request)
- [Personas and their constraints](#personas-and-their-constraints)
- [Design principles](#design-principles)

---

## LIL values

Every skill in this collection should reflect the Library Innovation Lab's core commitments. These are not checklists -- they are design sensibilities that should be visible in the choices you make about what a skill does, what it refuses to do, and how it communicates.

**Empower human agency.** Skills should build the user's own capacity, not substitute for it. A student skill that produces a finished exam answer has failed. A student skill that coaches the student to articulate their own reasoning has succeeded.

**Be transparent about local and remote system access.** If a skill invokes external services, fetches remote content, or accesses local files, the skill's instructions should make that visible to the user. Do not design skills that silently reach out to external resources.

**Prioritize provenance and explainability.** When a skill draws on external sources -- existing syllabi, legal databases, reference documents -- it should surface where that information came from and why it was used. Users should be able to trace the skill's reasoning, not just accept its output.

**Design for accessibility and interoperability.** Skills follow an open standard ([agentskills.io](https://agentskills.io/)) and are designed to work across Claude, ChatGPT, Gemini CLI, and other agentic tools. Write skills that do not assume a particular platform, interface, or level of technical sophistication in the user.

**Target meaningful, repeatable friction.** Not all friction is bad. A skill that forces a student to articulate their reasoning before getting feedback is introducing friction on purpose -- because the friction is where the learning happens. Design friction deliberately, not as a side effect of unclear instructions.

---

## What we are looking for

**New skills** -- A new `SKILL.md` covering an educational task not already in the collection. Examples: a moot court prep skill for students, a client counseling coach for CLE, a course assessment design tool for professors.

**Improvements to existing skills** -- Refined instructions, better step sequences, corrected pedagogical guidance, or additional reference materials for a skill already in the collection.

**New rubrics or test scenarios** -- Even if you don't change a skill's instructions, adding a `rubric.yaml` or new scenarios to an existing one helps us evaluate quality over time.

**New personas** -- If you represent a practitioner type not covered (e.g., legal clinic supervisors, law librarians), propose a new persona with a clearly articulated pedagogical objective. Open an issue first to discuss scope before building.

What we are _not_ looking for: general-purpose AI assistants, skills that produce finished legal work product for users, or skills that give legal advice to non-lawyers. See [Design principles](#design-principles) below.

---

## Before you start

1. **Read the existing skills** in `skills/` to get a feel for the format, tone, and depth expected. A few good starting points:
   - `skills/professor/syllabus-traditional/SKILL.md` -- a well-structured skill with clear steps
   - `skills/student/socratic-tutor/SKILL.md` -- a skill with a coaching constraint
   - `skills/skill-developer/skill-creator/SKILL.md` -- a skill for building other skills

---

## How to create a new skill

### 1. Choose a persona

Each skill belongs to exactly one persona. The persona's pedagogical objective is a hard constraint -- every instruction in your skill must be consistent with it. See [Personas and their constraints](#personas-and-their-constraints) for the full list.

If you are unsure which persona fits, ask yourself: who is holding the conversation? A student studying alone, a professor designing a course, an attorney in active practice? That person is the persona.

### 2. Create the skill folder

Skills follow the [Agent Skills](https://agentskills.io/) open standard. The folder structure for this project is:

```
skills/<persona>/<skill-name>/
├── SKILL.md          # Required: the SOP the agent follows
├── scripts/          # Optional: executable scripts the agent runs
├── references/       # Optional: documents the agent reads when needed
├── assets/           # Optional: templates and data files consumed by scripts
└── rubric.yaml       # Optional: test criteria and scenarios
```

Use lowercase, hyphenated names for the skill folder:

```
skills/professor/assessment-design/
skills/student/case-brief-coach/
skills/cle/deposition-prep/
```

Do not use the suffix `-meta` -- that is reserved for persona meta skills maintained by the LIL team.

**A note on `references/` vs. other assets.** Put content in `references/` only when the agent needs to _read_ it to make a decision -- for example, a rubric schema the agent uses to validate output, or a research protocol it follows during execution. Reference files are loaded into the agent's context window on demand and count against its token budget. If a document is for human contributors to read (background reading, inspiration, prior art), keep it out of `references/` or link to it externally.

### 3. Write the SKILL.md file

Every skill has a single `SKILL.md` file. It acts as a Standard Operating Procedure (SOP) for the agent: imperative, step-by-step instructions for what to do after the skill is activated.

#### Frontmatter (required)

```yaml
---
name: skill-name
description: >
  Coaches a law student through briefing a case using the IRAC framework,
  asking questions rather than producing the brief for them. Use when the
  student wants help understanding a case, writing a brief, or preparing
  to discuss a case in class.
metadata:
  version: 0.1.0
---
```

**The `description` field is the single most important element of a skill.** It is the agent's only signal for whether to load the full skill. Agents use progressive disclosure -- they read only the name and description initially, and only inject the full `SKILL.md` body when they determine the skill is relevant. If the description is vague or incomplete, the skill will be ignored.

Write descriptions in the **third person** ("Coaches a student..." not "I coach a student..."). Use the formula **[what it does] + [when to use it]**, and include 3--5 natural trigger phrases a user might actually say. The description in the example above would activate on "help me brief this case," "I need to understand this case for class," and "how do I write a case brief."

#### Body (the instructions)

The body is what the agent follows after activation. A few conventions:

- **Use numbered steps or named phases** so the agent has an unambiguous sequence to follow.
- **Be explicit about what to do first.** Agents without explicit direction will jump to output immediately. If you want the agent to ask questions before generating anything, say so in Step 1.
- **State the persona's constraint explicitly.** Do not assume the agent will infer it. If the skill is for students, write: "Do not produce finished work product the student would submit." If it is for pro se users, write: "Do not give legal advice."
- **Calibrate degrees of freedom to task fragility.** Match instruction specificity to how much variation is acceptable:
  - _High freedom:_ "Review the draft. Identify any gaps in the legal analysis." (Multiple valid approaches are fine.)
  - _Medium freedom:_ "Generate feedback using the criteria below. Customize the order as needed."
  - _Low freedom:_ "Ask these three questions in this order before proceeding." (Sequence matters; be prescriptive.)
- **Implement a validate-and-fix loop for complex outputs.** If the skill produces a structured document, have the agent check its own output against stated criteria and revise before presenting it to the user. Specify a maximum number of revision rounds.
- **Cite reference materials with relative paths** when the agent needs to consult them: `references/filename.md`.
- **Specify output format** if it matters. Describe sections, headers, or response length.

A minimal SKILL.md:

```markdown
---
name: case-brief-coach
description: >
  Coaches a law student through briefing a case using the IRAC framework,
  asking questions rather than producing the brief for them. Use when the
  student wants help understanding a case, writing a brief, or preparing
  to discuss a case in class.
metadata:
  version: 0.1.0
---

# Case Brief Coach

You are coaching a law student through briefing a case.

**Constraint:** Do not write the brief for the student. Your job is to ask
questions that help them identify the elements themselves.

## Step 1: Identify the case

Ask the student which case they are working on and what course it is for.
Do not proceed until you have this information.

## Step 2: Walk through the brief elements

For each IRAC element (Issue, Rule, Application, Conclusion), ask the student
to articulate it first. Give targeted feedback on their answer before moving
to the next element. Do not move forward until the student has attempted each
element themselves.

## Step 3: Wrap up

Ask the student to summarize the case's significance in one sentence.
Then tell them what they did well and what to watch for in similar cases.
```

### 4. Optionally add a rubric

A `rubric.yaml` lets you define what good performance looks like and write test scenarios. This is optional but strongly encouraged -- it helps reviewers understand your intent and lets the test harness evaluate the skill over time.

See the [rubric schema reference](skills/skill-developer/skill-tester/references/rubric-schema.md) and look at existing rubrics in the collection (e.g., `skills/professor/syllabus-traditional/rubric.yaml`) for the expected format.

A rubric has three sections:

- **`criteria.structural`** -- concrete, checkable behaviors ("agent asks for the case name before proceeding")
- **`criteria.pedagogical`** -- subjective quality dimensions rated strong/adequate/weak ("agent coaches rather than tells")
- **`anti_patterns`** -- things that should never happen ("agent produces a complete brief without prompting")
- **`test_scenarios`** -- scripted multi-turn conversations with expected behaviors

### 5. Optionally add reference materials

If your skill needs external knowledge (research protocols, schema definitions, style guides), add plain markdown files to a `references/` subfolder. Keep them focused -- one topic per file. Cite them in the skill body with a relative path: `references/filename.md`.

Remember: reference files are loaded into the agent's context window and cost tokens. Include only what the agent needs to read at runtime to make a decision, not background reading for human contributors.

### 6. Optionally add scripts

Some skills benefit from a script the agent can execute -- for example, to fetch and parse structured data, validate output against a schema, or process a file the user has provided. Scripts go in a `scripts/` subfolder and are bundled into the `.skill` zip automatically by the build system.

**Scripts are not loaded at startup.** The agent reads `SKILL.md` and `references/` files on activation. Scripts only enter the picture when `SKILL.md` explicitly tells the agent to run one. They cost no context window tokens until their output is read back.

**Prefer scripts over asking the agent to reason about raw data.** If a task requires counting, sorting, parsing, or transforming structured data, a script will be faster and more reliable than asking the agent to do it in-context. Reserve agent reasoning for tasks that require judgment.

#### Languages

We accept **Python** and **Node.js** scripts. Use the approach that makes the script fully self-contained so no separate install step is needed.

**Python -- use PEP 723 inline metadata and `uv run`:**

Declare dependencies directly inside the script using the standard `# /// script` block. The `uv run` command creates an isolated environment and installs them automatically.

```python
# /// script
# dependencies = [
#   "requests>=2.32,<3",
# ]
# ///

import sys, json, requests

url = sys.argv[1]
data = requests.get(url).json()
print(json.dumps(data, indent=2))
```

Run with:

```bash
uv run scripts/fetch_data.py "https://example.com/api"
```

If a script genuinely needs only the standard library, omit the `# /// script` block and invoke with `python3`.

**Node.js -- use `npx` for packages, or plain `node` for built-ins:**

For a one-off package, reference it directly without a bundled script:

```bash
npx prettier@3 --write report.md
```

For reusable logic using only Node.js built-ins (`fs`, `path`, `https`, `crypto`, etc.), write a plain `.js` file and run with `node`:

```bash
node scripts/validate_schema.js input.json
```

If a Node.js script needs third-party packages, use `npx` to invoke the package directly rather than bundling a `node_modules` folder.

#### Declaring environment requirements

If a script requires specific tools (e.g., `uv`, `node`, network access), declare this in the skill's frontmatter using the `compatibility` field:

```yaml
---
name: transcript-parser
description: Parses hearing transcripts into structured JSON. Use when the user provides a court transcript or deposition to analyze.
compatibility: Requires Python 3.12+ and uv (https://docs.astral.sh/uv/)
metadata:
  version: 0.1.0
---
```

#### Referencing scripts from SKILL.md

List available scripts near the top of the `SKILL.md` body so the agent knows they exist, then instruct the agent to run them using relative paths from the skill root:

````markdown
## Available scripts

- **`scripts/parse_transcript.py`** — Parses a transcript file into structured JSON

## Step 2: Parse the transcript

Run:

```bash
uv run scripts/parse_transcript.py "path/to/transcript.txt"
```

The script writes JSON to stdout with keys `speaker`, `timestamp`, and `text` for each turn.
Read the output and use it to identify the issues raised in Step 3.
````

#### Designing scripts for agentic use

Agents run scripts in non-interactive, headless environments. Follow these rules:

- **No interactive prompts.** Accept all input as command-line arguments, flags, or stdin. A script that waits for keyboard input will hang indefinitely.
- **Structured output to stdout.** Prefer JSON or plain markdown. This keeps output parseable by the agent and composable with other tools.
- **Diagnostics to stderr.** Send progress messages, warnings, and debug output to stderr so stdout stays clean.
- **Clear error messages.** When something goes wrong, say what failed, what was expected, and what to try. An opaque error wastes a conversation turn.
- **Implement `--help`.** The `--help` output is the primary way an agent learns a script's interface. Include a brief description, all flags, and at least one usage example.
- **Use meaningful exit codes.** Exit 0 on success, non-zero on failure. Use distinct codes for distinct failure types and document them in `--help`.
- **Design for idempotency.** Agents may retry a command. "Create if not exists" is safer than "create and fail on duplicate."
- **Support `--dry-run` for destructive operations.** A dry-run flag lets the agent preview what will happen before committing.
- **Control output size.** Many agent harnesses truncate tool output beyond 10--30K characters. If a script might produce large output, default to a summary and support a flag like `--output FILE` to write the full result to disk instead.

#### Static files for scripts

If a script needs static data -- templates, lookup tables, schemas -- put those files in `assets/`. The `assets/` directory is for files that scripts consume at runtime; it is not read directly by the agent. Reference assets from your script using relative paths.

---

## How to improve an existing skill

If you want to refine an existing skill:

1. Read the current `SKILL.md` and `rubric.yaml` carefully.
2. Run the existing test scenarios locally (see [How to test your skill](#how-to-test-your-skill)) to understand current behavior before making changes.
3. Make your edits. If you change behavior significantly, bump the version in the frontmatter (e.g., `0.1.0` → `0.2.0`).
4. Update the rubric if your changes affect what the skill should or should not do.
5. Submit a PR with a brief explanation of the pedagogical motivation for your changes.

---

## How to test your skill

### Using the LIL test harness

The test harness runs your skill against a live language model and evaluates the conversation using an LLM judge. It is not a deterministic pass/fail system -- results vary across runs -- but it builds a record of scored conversations that lets you see whether quality is stable or improving.

**Requires:** An `OPENROUTER_API_KEY` set in `.env`.

```bash
# Run all tests
uv run pytest tests/ -v -s

# Run only tests for your skill
uv run pytest tests/ -v -s -k "your-skill-name"

# Run in parallel (much faster)
uv run pytest tests/ -v -n auto

# Force a re-run of scenarios that already have traces
uv run pytest tests/ -v -s --rerun
```

Trace results are saved to `traces/` as JSON files. To browse them:

```bash
uv run python -m http.server -d traces
# Open http://localhost:8000/
```

The viewer shows scored conversations and per-criterion evaluations. Compare your skill's runs against the null baseline (no skill installed) to see where the skill is adding value. If the skill does not improve quality or consistency over the bare model, revise the instructions before submitting.

**Before submitting a PR:** Run at least one scenario for your skill and include the trace output in `traces/`. Traces are checked into version control as a quality record.

### Manual A/B testing

The LLM harness is a formal record, but informal A/B testing is often faster for iterating on instructions. Use two separate agent sessions:

1. **Designer session:** Use one agent instance to help you draft and refine the `SKILL.md` body.
2. **Tester session:** Open a fresh session with no conversation history. Install the skill and run it against natural-language requests. Note where it under-triggers (description too narrow), over-triggers (description too broad), or produces inconsistent output (instructions have too much freedom).
3. Bring failures from the Tester back to the Designer to tighten the instructions. Repeat.

Three specific tests to run:

- **Trigger test:** In a fresh session, try 3--5 natural phrases a user might say. Confirm the skill activates for all of them and does not activate for unrelated requests.
- **Functional test:** Run the skill 4--5 times with different inputs. If output varies significantly, the instructions need tighter degrees of freedom.
- **Value benchmark:** Compare output with the skill versus without it (bare model). If the skill does not improve quality, consistency, or pedagogical soundness, revise before submitting.

---

## Submitting a pull request

1. **Fork the repository** and create a branch: `git checkout -b add-case-brief-coach`
2. **Make your changes** following the conventions above.
3. **Build the site locally** to confirm the skill is discovered correctly:

   ```bash
   uv run scripts/build.py
   uv run python -m http.server -d _site
   # Open http://localhost:8000/ and verify your skill appears
   ```

4. **Run at least one test scenario** and commit the trace output in `traces/`.
5. **Commit and push** your branch.
6. **Open a pull request** against the `main` branch of this repository.

In your PR description, please include:

- **Persona:** Which persona this skill is for.
- **Task:** What educational task the skill handles.
- **Pedagogical rationale:** Why the instructional approach is appropriate for this persona and task. If you are drawing on research or established practice, cite it briefly.
- **LIL values:** Which of the [LIL values](#lil-values) this skill advances and how.
- **What you tested:** Which scenarios you ran and any notable results from comparing the skilled vs. null traces.

PRs that change existing skills should explain the motivation for the change and describe how behavior before and after differs.

We genuinely appreciate every contribution and will do our best to give thoughtful feedback and work with you through revisions. That said, we may decline contributions that don't align with LIL's values, don't meet our pedagogical quality bar, or aren't a good fit for the collection at this time. If we close a PR, we will explain why and, where possible, suggest a path forward.

---

## Personas and their constraints

Each persona has a core pedagogical objective that is a hard constraint for every skill in that group. Skills that violate the persona's objective will not be accepted.

| Persona | Objective | Key constraint |
|---------|-----------|----------------|
| **Professor** | Improve the quality of legal education | Help design learning experiences; do not produce student-facing work product |
| **Student** | Coach, encourage, and check understanding | Never produce finished work product the student would submit |
| **Pro Se** | Orient and connect | Never give legal advice; teach, orient, and empower |
| **CLE** | Coach and build skills | Build the attorney's own capabilities; do not do work for them |
| **Skill Developer** | Help SMEs create effective pedagogical AI skills | Honor domain expertise; handle format and conventions |

The full persona definitions -- including design principles, tone guidance, and success criteria -- are in [`skills/personas.yaml`](skills/personas.yaml).

---

## Design principles

These principles apply across all personas and complement the [LIL values](#lil-values) above.

**Skills encode pedagogy, not just instructions.** The goal is not to automate a task but to support learning. The difference between a skill that does the work for the user and one that coaches the user through doing it themselves is the difference between dependency and capability. Prefer the latter.

**The description is the skill's front door.** Write it so the agent activates on the right requests and ignores the wrong ones. Too broad and the skill triggers constantly; too narrow and it never fires. Include specific trigger phrases users would naturally say. See [Writing the SKILL.md file](#3-write-the-skillmd-file) for the formula.

**Be explicit about constraints.** Agents need explicit direction. Do not assume the agent will infer that a student skill should not produce finished work product. Say it in the skill body.

**Friction is a design tool.** Skills should introduce friction where the friction serves the learning objective -- forcing the user to articulate reasoning, make a decision, or engage with material before getting a response. Smooth, effortless output is often the wrong goal.

**Skills should be testable.** If you cannot write a rubric criterion for a behavior your skill is supposed to exhibit, the skill probably needs to be more specific. Vague aspirations ("be helpful") do not lead to reliable behavior.

**Keep skills focused.** A skill that tries to handle ten different tasks will handle none of them well. It is better to have two focused skills than one sprawling one.

**Tone follows the persona.** A professor skill is collegial and direct. A student skill is encouraging but honest. A pro se skill is calm and plain-spoken. A CLE skill is candid and practical. Match the tone guidance in `skills/personas.yaml`.

**Design for the platform-agnostic case.** Skills follow the [Agent Skills](https://agentskills.io/) open standard and should work across Claude, ChatGPT, Gemini CLI, and other tools. Avoid instructions that assume a specific interface or platform capability.

---

Questions? Open a GitHub issue and we will respond.
