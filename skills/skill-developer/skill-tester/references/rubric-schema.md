# Rubric Schema Reference

A rubric file (`_hub/rubric.yaml`) lives in a `_hub/` directory beside a skill's `SKILL.md` and defines how to evaluate
whether the skill is working well. Rubrics support both automated evaluation (via the test harness)
and manual evaluation (via the skill-tester skill).

## Schema

```yaml
# Required: identifies which skill this rubric evaluates
persona: <string>        # persona id (e.g., "student", "professor", "cle", "pro-se")
skill: <string>          # skill name matching the SKILL.md frontmatter name field

criteria:
  # Structural criteria: concrete, observable behaviors that can be checked
  # deterministically from a conversation trace.
  structural:
    - id: <string>           # kebab-case identifier, unique within the rubric
      description: <string>  # what the agent should do
      check: <string>        # how to verify it -- describe the observable behavior
                             # in plain language (the test harness translates this
                             # into a deterministic or LLM-assisted check)

  # Pedagogical criteria: subjective quality judgments that require human or
  # LLM evaluation. These capture "how well" rather than "whether."
  pedagogical:
    - id: <string>           # kebab-case identifier, unique within the rubric
      description: <string>  # what quality looks like for this dimension
      weight: <string>       # "low", "medium", or "high" -- relative importance

# Anti-patterns: behaviors that are automatic failures. A single violation
# means the skill is not performing acceptably, regardless of other scores.
anti_patterns:
  - id: <string>             # kebab-case identifier, unique within the rubric
    description: <string>    # what the agent must never do
    check: <string>          # how to detect a violation in the conversation trace

# Test scenarios: scripted interactions for evaluating the skill. Each scenario
# simulates a user with a specific situation and sends a sequence of messages.
test_scenarios:
  - id: <string>             # kebab-case identifier, unique within the rubric
    setup: <string>          # description of the simulated user's situation --
                             # provides context for whoever is role-playing the user
                             # or for the test harness runner
    messages:                # sequence of user messages to send to the agent
      - role: user
        content: <string>    # what the user says
      # Additional messages can be included. All messages have role: user.
      # The agent's responses are captured during the test run, not scripted here.
    expected:                # list of expected agent behaviors (not exact text)
      - <string>             # each entry describes an observable behavior the
                             # agent should exhibit during this scenario
```

## Design Principles

### Structural vs. Pedagogical

The split between structural and pedagogical criteria reflects a practical distinction:

- **Structural criteria** answer "did the agent do X?" They can be evaluated by checking
  whether a behavior occurred in the conversation trace. The test harness can often check
  these deterministically (e.g., "first agent turn contains a question").

- **Pedagogical criteria** answer "how well did the agent do X?" They require judgment
  about quality, nuance, and pedagogical effectiveness. The test harness evaluates these
  using a tightly scoped LLM-as-judge call for each criterion individually.

When writing criteria, prefer structural over pedagogical where possible. A criterion like
"agent asks questions before giving answers" is structural (checkable). "Agent asks
*good* questions" is pedagogical (requires judgment).

### Anti-Patterns

Anti-patterns derive from three sources:

1. **Persona constraints**: Every persona has non-negotiable boundaries (e.g., student
   skills must never produce finished work product). These should always appear as
   anti-patterns.

2. **Skill-specific boundaries**: The skill's own Boundaries section defines what the
   agent must not do.

3. **Common AI failure modes**: Patterns like making up legal citations, giving legal
   advice when the persona forbids it, or producing overly generic responses.

### Test Scenarios

Good test scenarios cover:

- **Happy path**: A straightforward use case.
- **Edge case**: A situation that tests boundaries (e.g., user asks the agent to violate
  a constraint).
- **Minimal input**: User provides little context -- does the skill gather what it needs?
- **Scope boundary**: A request adjacent to but outside the skill's scope.

The `expected` list describes behaviors, not exact text. "Agent asks about which course"
is good; "Agent says 'What course are you taking?'" is too brittle.

### Scoring

When evaluating a conversation against a rubric:

- **Structural criteria**: Pass/fail. Count passes vs. total.
- **Pedagogical criteria**: Rate as strong/adequate/weak. Weight by importance.
- **Anti-patterns**: Clear/violation. Any violation is an overall failure.

The test harness computes a numeric score (0-100) for trending over time:

- Structural score: (criteria passed / total structural criteria) * 40
- Pedagogical score: (weighted sum of ratings, strong=1, adequate=0.6, weak=0.2) * 40
- Anti-pattern penalty: -20 per violation (capped at -100)
- Final score: max(0, structural + pedagogical + 20 base - penalties)

The base 20 points ensure a skill that passes all structural checks and has adequate
pedagogy with no violations scores around 72, leaving room for the "strong" ratings
to push toward 100.
