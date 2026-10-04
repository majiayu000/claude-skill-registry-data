---
name: delivery
description: "ADLC delivery loop: Plan -> Breakdown -> Validate -> Finalize, then per slice: Implement (TDD) -> Review (unbounded until a zero-finding round) -> Commit slice. Routes to the rule and role files."
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

# Delivery (loop)

This skill is the loop, not the work. It tells the orchestrator the
shape of a delivery and points at the canonical sources for each step.
It does not write code, does not produce a plan file, and does not
spawn agents - the orchestrator does that, in order.

## Canonical sources (do not duplicate here)

- ADLC rule: `.agents/rules/05-adlc-agentic-development-lifecycle.md`.
  This is the canonical definition. If this skill disagrees with the
  rule, the rule wins.
- Role definitions: `.agents/agents/{planner,plan-reviewer,builder,reviewer}.md`.
  `planner`/`plan-reviewer` are standalone, manually-selectable roles for
  ad-hoc plan work; the rule's own Step 0 dispatches the generic
  `reviewer` + `auditor` roles instead, and the compiled workflow engine
  (below) uses a different role set entirely. Do not assume `planner`/
  `plan-reviewer` are on either automated critical path.
- Subagent dispatch contract: `.agents/agents/*.md` (binary's
  workflow engine) or the Markdown set above (human/ADLC). Use one,
  not both, per dispatch.
- Workflow templates: `.mivia/workflows/templates/` (plan, plan-review,
  plan-tests, implement, review, repair, decompose, bugfix-*, e2e-*,
  review-panel-*). These are the runtime templates the binary reads.
  The compiled engine's shape varies by workflow: `feature-delivery.toml`
  dispatches `workflow-engineer` for plan/implement/repair steps and a
  `panel-reviewer`/`review-synthesizer` panel for review; `bug-fix.toml`
  and `bug-fix-fast.toml` instead gate review with an active
  `agent = "reviewer"` triage step (their panel/review layers are
  commented out in the checked-in workflow TOMLs as a temporary debug cut).
  None of the three
  dispatch `planner`/`plan-reviewer`/`builder` by name.

## The loop (verbatim from ADLC)

1. **Plan** - `.agents/agents/planner.md` produces an in-context plan.
   No on-disk plan file; ADLC rule 05 forbids it.
2. **Breakdown** - planner subdivides the plan into chunks and groups
   the chunks into slices/phases. Each slice is an independently
   reviewable and independently committable unit (rule 05, Step 1).
3. **Validate** - `.agents/agents/plan-reviewer.md` runs
   `architecture-review` against the plan and returns `approved` /
   `changes_requested` (the latter optionally flagged `Reject: true` for a
   wrong-shape plan that needs a redo, not a patch).
4. **Finalize** - on `approved`, the orchestrator captures the plan in
   context and routes to the builder.
5. **Implement (TDD, per slice)** - `.agents/agents/builder.md` writes
   that slice's code and tests, runs `make verify-fast`, returns chunk
   logs.
6. **Review (per slice, unbounded)** - `.agents/agents/reviewer.md`
   re-runs `make verify`, dispatches the right per-lens skill via
   `.agents/skills/review/`, returns `approved` / `changes_requested`.
   Any round with findings goes back to the builder (step 5) for fixes
   and then into another review round. There is **no round cap**: rounds
   repeat until one reports **zero findings**, and that clean round is
   the only review verdict that unblocks the commit. Exits other than a
   clean round (rule 05, Step 5): the same root-cause bug surviving 3
   fix attempts, or a revealed plan flaw - both go back to Step 0.
7. **Commit (per slice)** - only after step 6's zero-finding round does
   the reviewer commit that slice itself (the zero-finding round's
   concluding act): it stages exactly the slice's reviewed files by path
   and commits with the conventional `type(scope): subject` format from
   `.mivia/policy/commit-message.json`, hooks running normally. The
   orchestrator records the SHA the reviewer reports and never commits.
   The loop then returns to step 5 for the next slice.

Steps 5-7 repeat once per slice, in slice order. A slice whose latest
review round still has findings - of any severity - is never committed;
only a zero-finding round gates the commit.

## Output (exact shape)

```text
Loop start: <one-line task description>
Step 1: <status> - <planner verdict or "skipped">
Step 2: <status> - <chunk count>, <slice count> slices
Step 3: <status> - <plan-reviewer verdict: approved | changes_requested (+ reject flag)>
Step 4: <status> - <builder dispatch or "skipped">
Steps 5-7 repeat per slice, in slice order:
Step 5: <status> - <slice id>: <builder output>
Step 6: <status> - <slice id>: round <N> - <findings: fixed, re-review | zero findings: approved>
Step 7: <status> - <slice id>: <commit landed | blocked | abandoned> (only after a zero-finding round)
```

## Disallowed operations

- Writing a plan file. ADLC forbids it.
- Running any step's work directly. The orchestrator dispatches; this
  skill narrates.
- Committing. The reviewer commits each slice at the end of its own
  zero-finding round (`.agents/agents/reviewer.md` "Commit on approval"),
  and only after that slice's review round reported zero findings. The
  orchestrator never commits. A slice whose latest review round still
  has findings is never committed.
- Skipping a step because the previous one "felt good." Each step's
  verdict is the only thing that lets the next step start - and a slice's
  commit is admitted by nothing except its own zero-finding review round.

## Escalation

- **No cap on the per-slice review loop.** Rounds repeat until one
  reports zero findings; do not escalate merely because rounds keep
  finding bugs. Escalate to Step 0 with the full round log attached only
  when the same root-cause bug survives 3 fix attempts, or when a round
  reveals a plan flaw (rule 05, Step 5 and Rejection & Rollback table).
- **A step finds a deviation between this skill and the ADLC rule.**
  Trust the rule; this skill is a router, not the source of truth.

## Report shape

`.agents/skills/delivery/report-template.md` holds the long form of the output
above: the same steps with 5-7 expanded per slice, plus timestamps,
per-step sub-fields and per-slice round counts. Read it with `read_file`
before the first step when the run needs that detail. The verdicts are then
recorded as the loop runs, not reconstructed at the end. The short shape
above stays the default.
