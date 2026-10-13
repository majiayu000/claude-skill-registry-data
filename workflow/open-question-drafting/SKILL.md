---
name: open-question-drafting
description: Draft the open-question punch list + rule-implication checklist for an upcoming requirement step, before any implementation begins. Surfaces questions; never answers or codes. Used by the workflow-step-planner agent at /workflow:step-start.
---

# Open-question drafting skill

## Mission
Draft the open questions for an upcoming implementation step, so the user resolves them before coding starts. Surface questions — never answer them, never write code.

## Inputs
- Feature name and step name (e.g. "Step C - Application layer wiring").
- The relevant section of `docs/<feature>/<feature>.plan.md`.
- `docs/<feature>/<feature>.status.md` for resolved-questions history.

If any input is missing, read the files directly.

## Read scope
- The plan section for the step.
- The prior step's "Resolved questions" in `status.md` (these often constrain the new step).
- `docs/<feature>/<feature>.analyzed.md` "Project-Specific Rule Overrides", if present — an override may already supersede a rule for this feature.
- Project `architecture-rules` / `coding-rules` via `project-seams` — skim the ones governing this step's kind of work.

## Procedure
1. Read the plan section, prior resolved questions, analyzed overrides, and relevant rule skills.
2. Draft a numbered list of open questions (typically 3-5). For each: state it concisely; mark `[Waiting for Answer]`; identify which rule section / prior decision / analyzed override forces it; state the **default** you'd pick if unanswered; state the **alternatives** worth considering.
3. Suggest a resolution order (which answer unblocks others).
4. Return only the punch list — no narrative, no implementation suggestions.

## Output shape
```
## Open questions for <feature> / <step>

1. **<Q1 short title>** [Waiting for Answer]
   - Forced by: <rule section, prior decision, or analyzed.md override>
   - Default: <one line>
   - Alternatives: <one line>

2. ...

## Suggested resolution order
1. Q<n> first - unblocks Q<m>
2. ...
```

## Boundary
Writes no code, modifies no files, answers no questions itself, and uses only read tools (`Read`, `Glob`, `Grep`). Full contract: `pipeline-protocol`.
