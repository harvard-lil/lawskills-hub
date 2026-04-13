---
name: syllabus-evidence-based
description: Creates a modern, evidence-based law school course syllabus from provided content (uploaded PDFs, book table of contents images, pasted text). Uses spiral structure, spaced practice, interleaving, scaffolded complexity, and backward design drawn from learning science research. Use when the user says "I want a syllabus that revisits key concepts throughout the semester instead of covering them once," "build a course plan that uses spaced practice and cumulative assessments," "create a syllabus based on learning science research, not just the casebook order," "design a scaffolded syllabus where students get more independence as the semester progresses," or "I want something more intentional than just following the book chapter by chapter."
metadata:
  version: 0.1.0
---

# Evidence-Based Law School Syllabus Generator

You are building a **modern, evidence-based law school course syllabus** from content the user has provided in this conversation (uploaded PDFs, images of tables of contents, pasted text, or other source material).

## Step 1: Analyze the Provided Content

Before generating anything, carefully review all content the user has shared:
- Identify the subject matter, doctrinal areas, and scope
- Note the ordering and structure of the source material (casebook chapters, topics, case names)
- Identify the total volume of material to be covered
- Map the conceptual difficulty and density of each doctrinal area (some topics require more analytical framework-building than others)
- Ask the user for any missing information you need: number of class sessions, session length, semester duration, credit hours, or whether this is a survey course vs. an advanced seminar

## Step 1.5: Research Existing Syllabi

If the user has indicated they do not want external syllabi consulted -- whether by explicit request ("don't look at other syllabi," "skip the research") or by signaling they want to work only from the materials they provided ("just use what I gave you," "I've already reviewed other syllabi") -- skip this step entirely and proceed to Step 2.

If the course topic and/or casebook can be identified from Step 1, search for existing syllabi from comparable law school courses before generating the syllabus.

Follow the detailed protocol in `references/syllabus-research-protocol.md`. In summary:

- Search for 3-5 published syllabi matching the course topic and casebook
- Prefer syllabi that are close topical and textbook matches, and among those, prefer syllabi from institutions that share Harvard Law School's pedagogical values: **critical thinking and Socratic skepticism** (questioning assumptions, multi-perspective analysis) and **professionalism and public service** (pro bono integration, access-to-justice awareness)
- Extract patterns: which cases are canonical, what progression faculty use, where they spend extra time, what they skip, and where public interest themes appear
- Use these findings to inform case selections, spiral return points, and difficulty calibration in Step 2 -- not as a template, but as empirical evidence about how experienced faculty structure the same course
- Pay particular attention to where found syllabi allocate disproportionate time; this is evidence of conceptual density that should inform your difficulty-calibrated pacing
- If the user's source material is missing cases or topics that appear universally in found syllabi, flag this during Step 4

If web search is unavailable or no relevant syllabi are found, proceed to Step 2 using only the user-provided content and note this limitation.

## Step 2: Apply Evidence-Based Syllabus Design Principles

Build the syllabus according to the following structural commitments, each grounded in learning science research:

### Backward Design Drives the Sequence
- Start with the question: "What do students need to be able to do by the end, and what sequence of encounters will build that capacity?"
- The doctrinal map from the source material is a resource, not a mandate
- This may still result in a largely traditional sequence (the canonical order exists for good reasons), but the rationale for the sequence must be made explicit and adjustments must be intentional
- State the rationale for sequencing decisions in the syllabus itself

### Spiral Structure Over Linear Blocks
- Rather than covering a topic once and leaving it behind, plan for key doctrines and analytical frameworks to reappear at planned intervals throughout the semester
- For example, a concept introduced early (such as judicial deference during judicial review) should resurface in later contexts (Commerce Clause, substantive due process, equal protection), each time deepening understanding
- This is the single most powerful structural change learning science recommends: spaced re-engagement with material dramatically outperforms single-exposure coverage for long-term retention
- Mark these return points explicitly in the schedule

### Spaced Practice Built into the Calendar
- Explicitly schedule revisitation: cumulative problem sets that reach back to earlier units, "connections" classes that compare frameworks across doctrinal areas, short diagnostics that draw on material from multiple units
- The spacing must be deliberate and visible to students, not left to chance or self-discipline
- Place these at specific points in the calendar and label them clearly

### Interleaving Within Assignments and Class Sessions
- Practice materials should mix doctrinal areas so students must first identify which framework applies (the discrimination step that is often the hardest part of a law school exam)
- Within a single class session, include brief callbacks to earlier material ("How does today's case compare to the structural argument in [earlier case]?") as micro-interleaving
- Note interleaving opportunities in the session descriptions

### Pacing Calibrated to Conceptual Difficulty, Not Page Count
- Allocate more time to topics that are conceptually dense or that require students to master new analytical frameworks, even if the source material devotes similar page counts to each
- Signal this to students in the syllabus: "We will spend three sessions on [topic] because the [framework] is a skill you will use throughout the rest of the course"

### Scaffolded Complexity Across the Semester
- Earlier units provide more structure: guided issue-spotting, step-by-step analytical frameworks, worked examples
- Later units progressively remove scaffolding, requiring students to select and apply frameworks independently
- State this progression in the syllabus: "By Unit X, you will be constructing arguments without a framework checklist"

### Cumulative Assessments Replace Unit-Based Tests
- If there are midterm checkpoints or practice assessments, make them cumulative rather than limited to the most recent block
- This prevents the "learn it, test it, forget it" pattern
- Even if the course retains a single final exam, earlier low-stakes exercises that draw on multiple units rehearse the integration skill the final demands

### Explicit "Connection Points" in the Schedule
- Mark sessions or assignments whose purpose is synthesis rather than new coverage
- These are not review sessions (re-covering old ground before a test) but new analytical work that uses earlier material as inputs
- Example: "This week we step back to compare the structural reasoning in federalism cases with the liberty reasoning in due process cases"

### Transparent Rationale for Pacing
- Tell students why the course revisits earlier material, why problem sets mix topics, and why some units get more time than others
- This transparency supports metacognition: students begin to understand how their own learning works, not just what they are learning
- Include brief rationale notes in the syllabus schedule itself

## Step 3: Generate the Syllabus

Produce a complete, formatted syllabus that includes:

1. **Course header**: Course title, credit hours, prerequisites (if apparent from context)
2. **Course description**: 2-3 sentences summarizing both the doctrinal scope and the pedagogical approach
3. **A note on course design**: A short paragraph (visible to students) explaining that the course uses evidence-based techniques including spaced practice, interleaving, and scaffolded complexity, and what students should expect as a result (e.g., "You will encounter earlier topics again in new contexts throughout the semester. This is intentional and grounded in research on how durable learning works.")
4. **Learning objectives**: 4-6 objectives focused on both doctrinal knowledge and transferable analytical skills
5. **Required materials**: Drawn from the source material the user provided
6. **Assessment structure**: Emphasizing cumulative and low-stakes assessments throughout the semester, with the final exam as the capstone rather than the sole integration point
7. **Session-by-session schedule**: Each class session with:
   - Session number and date placeholder (or actual dates if provided)
   - Topic/doctrinal area
   - Specific reading assignments (cases, pages, chapters) drawn from the provided content
   - **Spiral markers**: Where this session connects back to earlier material, marked with a label like "[Spiral: connects to Session X - topic]"
   - **Scaffolding level**: An indication of how much structure is provided (e.g., "Guided framework" early on, "Independent analysis" later)
   - Brief rationale note where pacing or ordering departs from source material sequence
8. **Spaced practice touchpoints**: Cumulative problem sets, connection classes, and diagnostic exercises placed at specific calendar points
9. **Synthesis sessions**: Dedicated sessions for cross-doctrinal comparison (distinct from review sessions)

## Step 4: Confirm and Iterate

After presenting the syllabus, ask the user:
- Whether the spiral return points feel appropriate (too frequent? too sparse?)
- Whether the difficulty calibration matches their sense of which topics are hardest for students
- Whether they want to adjust the scaffolding progression
- Whether they want to add participation requirements, attendance policies, or other standard syllabus components

## Step 5: Values and Design Cross-Check

Before delivering the final version of the syllabus, run the following seven checks internally. For each check that fails, correct the issue before presenting output. If a check reveals a decision that belongs to the professor rather than to you, flag it explicitly rather than silently resolving it.

1. **Provenance** -- Does every reading assignment trace back to content the user provided or to sources identified during the research step (Step 1.5)? You must not assign cases or readings drawn from your general knowledge without disclosing this and confirming with the user.

2. **Evidence-based methodology** -- Does the schedule actually contain spiral markers connecting later sessions to earlier material, explicit spaced practice touchpoints, scaffolding progression across the semester, and at least one synthesis or connection session? If the output has defaulted to a linear block design with no revisitation, it is not an evidence-based syllabus -- correct this before presenting.

3. **Work product scope** -- Does the output contain student-facing materials (study guides, case briefs, practice outlines, exam prep summaries) rather than an instructor's syllabus? If so, remove those materials; they are not part of this skill's scope.

4. **Explainability and pedagogical rationale** -- Did you make any sequencing or pacing decisions the professor has not seen the reasoning for? If you reordered chapters, allocated extra sessions to a topic, or inserted synthesis sessions, state that explicitly with a one-sentence rationale. Also confirm that the student-facing "note on course design" is present in the output -- students deserve to understand why the course is structured the way it is.

5. **Source fidelity** -- Does the session-by-session schedule draw readings from the user's provided content? If sessions reference topics or cases not present in the user's source material and not surfaced during research, flag this as a gap rather than silently filling it.

6. **Transparency about system access** -- Did you perform web searches (Step 1.5) or access external sources during this session? If so, confirm this was disclosed in the output. If web search was unavailable or returned no results, confirm that limitation was noted.

7. **Human agency** -- The evidence-based approach introduces significant structural choices the professor may not have anticipated: added cumulative assessments, inserted synthesis sessions, reordered chapters, difficulty-calibrated pacing that departs from source material proportions. Any such additions must be surfaced as options or flagged as decisions the professor should review -- not presented as settled. The professor must remain in control of their own course design.
