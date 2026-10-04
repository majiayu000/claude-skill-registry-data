---
name: daily-okr
description: Use when planning or closing a daily knowledge-compounding cycle across input, cognition, wiki, behavior, creativity, output, and feedback.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "stateful"
  assumes: "A daily note or equivalent state record is writable and the user can choose one priority."
  conflicts_with: "Invented completion, seven unrelated priorities, or activity counts without evidence."
---

# Daily OKR

<skill_contract>
  <input>Date, one priority objective, available time, active project, current inputs, and prior-day evidence.</input>
  <output>A seven-KR daily cycle linking input, cognition, wiki, behavior, creativity, output, and feedback.</output>
  <done>Each claimed KR has a durable receipt, and today's feedback changes one explicit next-day action or knowledge state.</done>
  <non_goals>Seven unrelated priorities, invented completion, activity counting without evidence, or treating scheduled notes as execution.</non_goals>

Run one daily objective through seven linked Key Results. The cycle compounds only when evidence from today changes tomorrow's behavior or knowledge state.

## Usage Template

Provide: date, one objective, available time, active project, knowledge inputs, and yesterday's evidence. Optional: a scheduled knowledge-loop note; treat it as input, not proof of execution.

## Workflow

<intake>

1. Load the current daily state and any scheduled-loop proposal.
2. Choose one objective tied to an active project or explicit learning goal.
3. Set a total time budget and a minimum viable day.
4. Carry forward only unresolved items with an owner or decision value.

</intake>

<unknowns_gate>

If priority, available time, or completion evidence is missing, return `NEEDS_INPUT` with one narrow probe. If the day is constrained, select the minimum cycle rather than fabricating seven completed results.

</unknowns_gate>

<execute>

Create seven causally linked KRs:

1. **Input:** capture one high-value source or observation.
2. **Cognition:** extract one mechanism, contradiction, or decision implication.
3. **Wiki:** write or improve one durable note with provenance.
4. **Behavior:** execute one minimum behavior linked to the objective.
5. **Creativity:** produce one alternative or falsifiable experiment.
6. **Output:** ship one reviewable artifact or project increment.
7. **Feedback:** record evidence, error, and tomorrow's adjustment.

Each KR needs an artifact or receipt. Keep unfinished work visible; do not convert a scheduled trigger into a success claim.

</execute>

<evaluate>

At close, mark each KR `done`, `partial`, `blocked`, or `skipped` from evidence. Check that at least one input became a durable wiki change and one observation changed a future action. Remove vanity metrics and report the bottleneck.

</evaluate>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus date, objective, seven KR statuses, artifact links, bottleneck, and tomorrow adjustment. Append receipts; never rewrite historical completion evidence.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: no daily objective or time budget can be inferred safely.
- `BLOCKED_DEPENDENCY`: a required source, project, or tool is unavailable; complete independent KRs and record the blocker.
- `VERIFY_FAILED`: a KR has no artifact or receipt; mark it partial or skipped.
- `BUDGET_STOP`: time is exhausted; close the state and select one next action.

## Output Contract

Return `status`, `result` (objective plus seven KR states), `evidence` (artifact links or receipts), `unknowns`, and `next_action` for the next cycle.

## Edge Cases

- Only 15 minutes remain: perform Input -> Cognition -> Wiki as one atomic note, then record feedback; mark other KRs skipped.
- A scheduled loop note exists but no command ran: record the trigger as proposed work, not execution evidence.

## Success Metrics

- One objective governs all seven KRs.
- At least one source becomes a verified durable note.
- The closing feedback changes a named next action.

## Quality Gates

- [ ] Every completed KR has evidence.
- [ ] Scheduled and executed states are distinct.
- [ ] Carry-forward work has decision value and an owner.
- [ ] The minimum day respects the declared budget.

</skill_contract>
