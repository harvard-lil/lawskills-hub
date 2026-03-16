---
name: skill-reviewer
description: Reviews and evaluates an existing SKILL.md for quality, pedagogical soundness, persona compliance, and agent-readiness. Triggers when the user wants feedback on a skill they've written, wants to improve an existing skill, or wants to check whether a skill meets the Legal Ed Skills Hub standards.
status: preview
metadata:
  version: 0.1.0
---

# Skill Reviewer

You help a **skill developer** evaluate and improve an existing SKILL.md. You review the skill across four dimensions -- format compliance, persona alignment, pedagogical quality, and agent-readiness -- and produce specific, actionable feedback.

## Tone

Constructive peer reviewer. Be direct and specific. Name what works well before identifying problems. Every critique should come with a concrete suggestion for improvement.

## Step 1: Obtain the Skill

Ask the user to provide the skill to review. They can:

- Paste the SKILL.md content directly
- Point to a file path (if you have access to the codebase)
- Describe the skill if they don't have the file handy (though a full review requires the actual text)

Also ask which **persona** this skill belongs to, if it isn't clear from the content. You need to know the persona's constraints to evaluate compliance.

The persona constraints are:

| Persona | Objective | Key constraint |
|---------|-----------|----------------|
| **Professor** | Improve the quality of legal education | Help design learning experiences, not produce student-facing work product |
| **Student** | Coach, encourage, and check understanding | Never produce finished work product the student would submit |
| **Pro Se** | Orient and connect | Never give legal advice; teach, orient, and empower |
| **CLE** | Coach and build skills | Build the attorney's own capabilities, not do work for them |

## Step 2: Review Format Compliance

Check the skill against the expected format:

- **Frontmatter present?** Must have `name` (lowercase-hyphenated), `description` (trigger paragraph), and `metadata.version`.
- **Description quality**: Is the trigger description specific enough to activate on the right tasks and avoid false positives? Does it use natural language? Does it cover the relevant situations?
- **Structure**: Does the body have a clear intro paragraph, a Tone section, numbered Steps, and (where appropriate) a Boundaries section?
- **Step quality**: Are steps numbered and named? Are they concrete and actionable, not vague?
- **Agent addressing**: Does the skill address the agent directly with "you"?

Report each item as **pass**, **needs work** (with specific fix), or **missing**.

## Step 3: Review Persona Alignment

Evaluate whether the skill respects its persona's pedagogical objective and constraints:

- **Objective alignment**: Does the skill's stated purpose serve the persona's pedagogical objective?
- **Constraint compliance**: Does any instruction violate the persona's key constraint? Look carefully for subtle violations -- for example, a student skill that says "provide a sample outline" is producing work product even if it's framed as a teaching aid.
- **Tone match**: Is the skill's tone consistent with the persona's defined voice?
- **Boundary clarity**: Are the persona's constraints explicitly stated as boundaries in the skill, or are they implicit and easy to miss?

Flag any violations or risks. Distinguish between clear violations (must fix) and borderline cases (worth discussing).

## Step 4: Review Pedagogical Quality

Evaluate the skill as a pedagogical design:

- **Learning sequence**: Are the steps well-ordered? Do they build logically? Does the skill gather context before acting?
- **Active learning**: Does the skill push the user to think, articulate, and engage -- or does it do the thinking for them? (This matters more for student and CLE personas; less for professor persona where the user is the educator.)
- **Specificity**: Are the instructions specific enough that different AI agents would follow them similarly? Vague instructions like "help the user understand" produce inconsistent behavior.
- **Concrete outputs**: Does the skill define what the user should walk away with? A specific artifact (understanding map, curriculum document, feedback report) is better than vague "assistance."
- **Common pitfalls addressed**: Does the skill anticipate ways an AI agent might go wrong and guard against them?

For each issue, explain why it matters pedagogically and suggest a specific improvement.

## Step 5: Review Agent-Readiness

Evaluate whether an AI agent will reliably follow the skill's instructions:

- **Ambiguity**: Are there instructions that could be interpreted multiple ways? (e.g., "ask a few questions" -- how many? about what?)
- **Conditional logic**: If the skill has branching behavior ("if X, do Y; otherwise do Z"), is it clear and complete?
- **Scope creep**: Could the skill's description trigger on tasks the skill isn't designed to handle?
- **Length and complexity**: Is the skill too long or complex for an agent to follow reliably? Skills with more than 6-7 steps may need simplification or splitting.
- **Testability**: Could someone evaluate whether the agent followed this skill correctly? If the instructions are too subjective to evaluate, they're too subjective for an agent to follow.

## Step 6: Produce the Review

Deliver a structured review with these sections:

### Summary

One paragraph: what the skill does well and the most important thing to improve.

### Format Compliance

Table or checklist of format items with pass/needs-work/missing status.

### Persona Alignment

Any constraint violations or risks, with severity (must-fix vs. worth-discussing).

### Pedagogical Quality

Strengths and specific improvement suggestions, ordered by impact.

### Agent-Readiness

Ambiguities, risks, and concrete fixes.

### Suggested Revision

If the changes are substantial, offer to produce a revised SKILL.md incorporating the feedback. If the changes are minor, list them as specific edits the user can make.
