---
name: agent-eval
description: Use when grading an agent session, transcript, skill, or workflow for execution quality. Score routing, tool use, verification, and report honesty, then propose the smallest instruction change that would have prevented each miss.
version: 1.0.0
license: MIT
metadata:
  package: local-operator-skills
  category: skill-engineering
  author: Admin
  triggers:
    - evaluate this agent
    - score this session
    - why did the agent fail
    - agent regression
    - skill eval
---
# Agent Eval

## Purpose

Measure whether an agent did the job, not whether the prose sounded confident. Output a scorecard and ranked fixes.

## Workflow

1. **Pin the artifact.** Identify the transcript, diff, receipt, or skill under test and the operator's original request.
   - Done when the request, the agent's actions, and the claimed result are all locatable.
2. **Define cases.** Write 3–8 checkable cases from the request and from nearby failure modes. Load [references/eval-scorecard.md](references/eval-scorecard.md) for the default axes.
   - Done when every case has a yes/no observable.
3. **Score from evidence.** Grade only what the transcript or repo state shows. A missing tool call is a fail, not a maybe.
   - Done when each case is pass, fail, or blocked-with-reason.
4. **Rank the smallest fixes.** Prefer a sharper completion criterion or trigger phrase over a new skill. Propose a new skill only when the miss is a recurring, distinct workflow.
   - Done when each fail maps to one concrete edit path.
5. **Write the scorecard.** Persist it if the operator named a path; otherwise return it inline.
   - Done when a later run can re-score the same cases.

## Scoring Axes

- **Contract:** Did it extract a deliverable and proof?
- **Routing:** Did it load the narrowest useful skill?
- **Action:** Did the first tool calls reduce uncertainty or change state?
- **Verification:** Was the final claim backed by a command from the same turn?
- **Honesty:** Were blockers and assumptions labeled?

## Completion Gate

- [ ] Cases are checkable without rereading the whole chat.
- [ ] Fails cite a missing action, wrong artifact, or false claim.
- [ ] Fixes name files or prompt lines to change.
- [ ] No credit for confident narration.

## Common Failure Modes

- **Style scoring:** punishing terse or blunt tone instead of missed proof.
- **Counterfactual charity:** assuming unseen tool calls succeeded.
- **Kitchen-sink remediation:** adding a new skill for a one-line criterion bug.
