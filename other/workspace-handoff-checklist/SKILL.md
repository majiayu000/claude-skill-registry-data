---
name: workspace-handoff-checklist
description: "Use this skill when a Mission Control work item is complete or awaiting review and an operator needs a factual handoff draft with outcome, evidence, unresolved risk, next owner, and next action."
version: 0.1.0
owner: software-factory
risk: low
capabilities:
  - agent-operations
  - handoff
---

# Workspace Handoff Checklist

## Purpose

Produce a concise, factual operator handoff for a completed or review-ready Mission Control work item. Preserve uncertainty rather than filling gaps with assumptions.

## Required inputs

Collect the following before drafting:

1. Work-item identifier and current state.
2. Confirmed outcome or current decision.
3. Evidence references, such as a task, run, test output, document, or PR.
4. Unresolved risk, blocker, or explicit confirmation that none is known.
5. Named next owner and the single next action.

When an input is absent, write `Needs confirmation` for that field. Do not infer a status, URL, owner, approval, or completed action.

## Workflow

1. Confirm whether the work item is complete, awaiting review, or otherwise active.
2. Extract only facts supported by the provided work-item context and evidence.
3. Identify gaps, contradictions, or unverified claims and label them `Needs confirmation`.
4. Draft the handoff using the required format.
5. Self-check that all five required sections are present and that the draft does not change task state, request approval, send a message, create a commit, or deploy anything.

## Required output format

```markdown
## Handoff — <work-item identifier>

**State:** <complete | awaiting review | active | Needs confirmation>

**Outcome:** <confirmed result or Needs confirmation>

**Evidence:**
- <verified reference>

**Unresolved risk:** <known risk, blocker, or No known unresolved risk>

**Next owner:** <named person or role, or Needs confirmation>

**Next action:** <one explicit action, or Needs confirmation>
```

## Examples

### Complete evidence

Input: `SFRL-073 is awaiting review. The local lint passed at 92/100. Draft import created version 0.1.0. Product Owner must decide whether to publish.`

Output:

```markdown
## Handoff — SFRL-073

**State:** awaiting review

**Outcome:** The candidate skill passed local structural lint and was imported as draft version 0.1.0.

**Evidence:**
- Local `skill-lint` result: 92/100
- Registry draft: `software-factory/workspace-handoff-checklist` v0.1.0

**Unresolved risk:** Registry evaluation is a structural proxy until an external agent runner is connected.

**Next owner:** Product Owner

**Next action:** Review the evaluation evidence and decide whether to publish the draft.
```

### Missing evidence

Input: `The task may be done, but no test output or owner was supplied.`

Output:

```markdown
## Handoff — Needs confirmation

**State:** Needs confirmation

**Outcome:** Needs confirmation

**Evidence:**
- Needs confirmation: no test output or source reference was provided.

**Unresolved risk:** Completion cannot be verified from the supplied context.

**Next owner:** Needs confirmation

**Next action:** Attach the relevant task and test evidence before review.
```
