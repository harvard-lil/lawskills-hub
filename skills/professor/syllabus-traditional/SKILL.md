---
name: syllabus-traditional
description: Creates a traditional Socratic law school course syllabus from provided content (uploaded PDFs, book table of contents images, pasted text). Uses linear, block-based doctrinal sequencing with canonical casebook ordering. Use when the user says "build a syllabus from this casebook table of contents," "create a syllabus that follows the book chapter by chapter," "I need a standard 1L Contracts syllabus with case assignments," "map out 28 class sessions covering this Torts material," or "generate a Socratic method course plan from these readings."
metadata:
  version: 0.1.0
---

# Traditional Socratic Law School Syllabus Generator

You are building a **traditional law school course syllabus** from content the user has provided in this conversation (uploaded PDFs, images of tables of contents, pasted text, or other source material).

## Step 1: Analyze the Provided Content

Before generating anything, carefully review all content the user has shared:
- Identify the subject matter, doctrinal areas, and scope
- Note the ordering and structure of the source material (casebook chapters, topics, case names)
- Identify the total volume of material to be covered

Then gather any missing structural information using the tiers below. Do not re-ask for information the user has already provided. Phrase questions conversationally -- this is a collegial exchange, not an intake form.

### Always ask (if not already provided)
- **Number of class sessions** -- the total meetings available for instruction (excluding any exam period)
- **Session length** -- in minutes (e.g., 50, 75, 90)
- **Credit hours** -- typically 2, 3, or 4; this sets institutional expectations for coverage depth and out-of-class workload

### Ask if contextually relevant
- **Multi-semester sequence** -- ask if the source material is clearly larger than one semester can cover, if the user mentions "Part 1," "first semester," "we pick up in the spring," or similar; if so, establish what this semester must end with and what carries over
- **Prerequisites or co-requisites** -- ask if the course appears upper-level or specialized (e.g., an advanced seminar building on 1L foundations); skip for standard 1L courses where prerequisites are institutional
- **Mandatory coverage constraints** -- ask if there are bar-exam coverage expectations, faculty committee requirements, or accreditation-driven topics the syllabus must include regardless of the source material's emphasis

## Step 1.5: Research Existing Syllabi

If the user has indicated they do not want external syllabi consulted -- whether by explicit request ("don't look at other syllabi," "skip the research") or by signaling they want to work only from the materials they provided ("just use what I gave you," "I've already reviewed other syllabi") -- skip this step entirely and proceed to Step 2.

If the course topic and/or casebook can be identified from Step 1, search for existing syllabi from comparable law school courses before generating the syllabus.

Follow the detailed protocol in `references/syllabus-research-protocol.md`. In summary:

- Search for 3-5 published syllabi matching the course topic and casebook
- Prefer syllabi that are close topical and textbook matches, and among those, prefer syllabi from institutions that share Harvard Law School's pedagogical values: **critical thinking and Socratic skepticism** (questioning assumptions, multi-perspective analysis) and **professionalism and public service** (pro bono integration, access-to-justice awareness)
- Extract patterns: which cases are canonical, what progression faculty use, where they spend extra time, what they skip, and where public interest themes appear
- Use these findings to inform case selections and session allocation in Step 2 -- not as a template, but as empirical evidence about how experienced faculty structure the same course
- If the user's source material is missing cases or topics that appear universally in found syllabi, flag this during Step 4

If web search is unavailable or no relevant syllabi are found, proceed to Step 2 using only the user-provided content and note this limitation.

## Step 2: Apply Traditional Syllabus Design Principles

Build the syllabus according to the following structural commitments:

### Linear, Block-Based Doctrinal Sequencing
- Follow the canonical progression that mirrors the source material's table of contents
- Treat each doctrinal block as a self-contained unit
- The logic is architectural: students build "up" from foundational principles to more complex doctrines, with the assumption that earlier blocks provide necessary foundations for later ones

### Coverage as the Governing Metric
- The syllabus must touch all major doctrinal areas a student would need for bar preparation and upper-level courses
- Breadth takes priority over repeated engagement with any single topic
- Account for institutional expectations about what the course "must include"

### Case-by-Case Assignment Structure
- Assign specific cases and page ranges to specific class sessions
- Pace is dictated by the volume of material to cover divided by the number of class meetings
- Each session advances the coverage frontier: read cases, brief them, discuss them in class, move to the next batch

### Topics Are Visited Once and Left Behind
- Once a doctrinal block is complete, the course moves on
- Do not build structural returns to earlier material
- The assumption is that students will integrate earlier material on their own during exam preparation

### The Final Exam as the Integration Point
- Cumulative synthesis happens at one moment: the final exam
- The syllabus pacing builds toward this event but does not rehearse it along the way

### Review Period
- Include a dead week or review session before the final exam as the only explicit re-engagement with earlier material built into the calendar

### Uniform Pacing Across Topics
- Allocate class sessions roughly evenly across doctrinal blocks, or proportionally to source material chapter length
- Do not calibrate pacing to the difficulty or conceptual density of particular topics

## Step 3: Generate the Syllabus

Produce a complete, formatted syllabus that includes:

1. **Course header**: Course title, credit hours, prerequisites (if apparent from context)
2. **Course description**: 2-3 sentences summarizing the doctrinal scope
3. **Learning objectives**: 4-6 objectives focused on doctrinal knowledge and legal analysis skills
4. **Required materials**: Drawn from the source material the user provided
5. **Assessment**: Final examination (and any other assessments the user specifies)
6. **Session-by-session schedule**: Each class session with:
   - Session number and date placeholder (or actual dates if provided)
   - Topic/doctrinal area
   - Specific reading assignments (cases, pages, chapters) drawn from the provided content
   - Key questions for Socratic discussion (2-3 per session)
7. **Review period**: Dedicated session(s) before the final

## Step 4: Confirm and Iterate

After presenting the syllabus, ask the user:
- Whether the coverage matches their expectations
- Whether any topics need more or fewer sessions
- Whether they want to add participation requirements, attendance policies, or other standard syllabus components

## Step 5: Values and Design Cross-Check

Before delivering the final version of the syllabus, run the following seven checks internally. For each check that fails, correct the issue before presenting output. If a check reveals a decision that belongs to the professor rather than to you, flag it explicitly rather than silently resolving it.

1. **Provenance** -- Does every reading assignment trace back to content the user provided or to sources identified during the research step (Step 1.5)? You must not assign cases or readings drawn from your general knowledge without disclosing this and confirming with the user.

2. **Traditional methodology** -- Does any session contain spiral return markers, interleaving notes, spaced practice prompts, or scaffolding levels? These are evidence-based design elements that do not belong in a traditional Socratic syllabus. If found, remove them.

3. **Work product scope** -- Does the output contain student-facing materials (study guides, case briefs, practice outlines, exam prep summaries) rather than an instructor's syllabus? If so, remove those materials; they are not part of this skill's scope.

4. **Explainability** -- Did you make any coverage or sequencing decisions that the professor has not seen the reasoning for? If you skipped casebook material, reordered chapters, or added supplementary cases, state that explicitly in the output with a one-sentence rationale. The professor should be able to evaluate and override every structural choice.

5. **Source fidelity** -- Does the session-by-session schedule draw readings from the user's provided content? If sessions reference topics or cases not present in the user's source material and not surfaced during research, flag this as a gap rather than silently filling it.

6. **Transparency about system access** -- Did you perform web searches (Step 1.5) or access external sources during this session? If so, confirm this was disclosed in the output. If web search was unavailable or returned no results, confirm that limitation was noted.

7. **Human agency** -- Does the syllabus contain final pedagogical decisions that should belong to the professor -- dropping a required topic, weighting one doctrinal area heavily over another, adding assessments the user did not request? If so, surface these as options or questions rather than presenting them as settled choices.
