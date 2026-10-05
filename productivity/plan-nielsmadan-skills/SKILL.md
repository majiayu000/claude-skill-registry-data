---
name: plan
description: Lightweight planning workflow — delegate read-only planning to an Opus subagent, then implement in auto mode after a single go-ahead gate. The middle tier between "just do it" (tiny tasks) and heavyweight superpowers planning (big features). Never enters plan mode, so it sidesteps the plan-mode permission prompts. Use when the user invokes /plan, or wants a plan for a medium-sized task before implementing.
argument-hint: '[--review] <task, or blank to infer from conversation>'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Plan (middle tier)

Produce a concrete implementation plan for a medium-sized task, then implement it
after one approval gate. Deliberately lighter than `superpowers:brainstorming` /
`writing-plans` (no spec files, no per-task checkpoints, no multi-agent fan-out) and
heavier than just editing — the space where a plan helps but full ceremony is overkill.

**This skill IS the planning workflow for this task.** Do not also invoke
`brainstorming` — that is the heavyweight path this skill exists to avoid.

Two design choices make it work:
- **Never enter plan mode / never call `ExitPlanMode`.** Everything runs in the
  session's normal (auto) mode. This is intentional: it avoids plan mode's read-only
  permission prompts entirely, and a subagent's own tool calls never prompt you.
- **A subagent plans, the main session implements.** A single read-only subagent
  pinned to Opus does the exploring and drafts the plan; the main session implements it.

The argument is the task. If blank, infer the task from the current conversation.

## Usage

```
/plan add a --json flag to the export command    # plan a stated task
/plan                                            # plan the task from context
/plan --review <task>                            # plan, then multi-agent review before the gate
```

## Flags

- `--review` — after the plan is drafted, run `review-plan` (multi-agent) on it and
  fold the findings in before presenting for go-ahead. `review-plan` is already
  multi-agent; there is no separate `--multi`.

## Instructions

### Step 1: Scope check (early exit)

Judge the task's size first.

- **Trivial** (one-liner, obvious fix, rename, config flip): planning is overhead.
  Say so in one line and offer to just do it directly — do not spend a planning
  round-trip. Respect the user if they still want a plan.
- **Too big** (multi-subsystem, architectural, multi-session): this is above the
  middle tier. Point at `superpowers:brainstorming` and stop.
- **Middle** (a few files, a new endpoint/component, a contained refactor): proceed.

### Step 2: Dispatch the planning agent

Dispatch **one** subagent via the `Agent` tool:
- `subagent_type: Plan` — read-only by construction (no Edit/Write/NotebookEdit).
- `model: opus`.

The `Plan` agent starts **fresh** (it is not a fork),
so brief it fully. Its prompt MUST contain:
- The task statement (from the argument or inferred from the conversation).
- Relevant context from this conversation and pointers to the files/dirs to start from.
- These directives: explore **read-only** — Read/Grep/Glob and read-only shell only,
  run **no** mutating commands; ground every claim in **real file paths / line ranges**
  it actually read; be **concrete — no placeholders** ("TBD", "add error handling").
- The required output skeleton below.

**Required plan skeleton (the agent returns exactly this):**
```
## Approach
2–3 sentences. Name approach A (recommended) vs B in one line, with why.

## Files to touch
- path/to/file — what changes and why

## Ordered steps
1. …

## Risks / edge-cases
- …

## Assumptions & open questions
- Assumption: …
- Open question: … (blocking? y/n)
```

### Step 3: Review (only if `--review`)

Invoke the `review-plan` skill (via the Skill tool) against the plan in current
context. Fold its findings into the plan — apply clear improvements directly, and
surface unresolved disagreements as open questions for the gate.

### Step 4: Present and STOP

Print the plan inline, cleanly formatted, with the **Assumptions & open questions**
called out so the user can resolve them.

**Hard gate:** do NOT begin implementing. Wait for an explicit go-ahead ("go", "yes",
"proceed", or edits). This stop is load-bearing — in auto mode nothing else prevents
you from barreling into implementation.

### Step 5: Implement on go-ahead

Once the user approves, implement the plan directly in the main session (auto mode),
incorporating any answers they gave to the open questions. Do not enter plan mode and
do not re-dispatch to a subagent — the main session does the implementation.

## Notes

- Read-only precision: the `Plan` agent has no Edit/Write/NotebookEdit tools, so it
  cannot modify files — but it retains Bash, so "no mutating commands" is an
  instruction, not a hard block. Still far safer than plan mode.
- `--review` runs the full `review-plan` fan-out (including a `second-opinion` codex
  agent and a `research-tech` agent); it costs more, which is why it is opt-in.
