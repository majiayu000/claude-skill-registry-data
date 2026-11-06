---
name: software-dev-loop
description: "General software development only (no game engine, no game design). The complete software-development loop — persist the goal → write a plan doc and harden it with the source-anchored-design critic loop → implement and critic-harden → red-green test + benchmark → dump JOURNEY in between → write durable long-term memory. Use when starting or running a real software build, when a task needs goal, docs, testing, and memory chained in order, or when the user asks for the \"holy grail\" dev workflow. Not for games - use game-dev-loop."

version: 1.3.1
metadata:
  category: software-development
  created_by: agent
---

# Software Dev Loop — goal → docs → test → memory

One loop that chains the vault's dev skills into a single build process. It does not replace any of them — it is the sequence and the handoff between them.

```
goal → plan doc → implement → test → journey → long-term memory
  └──────────────← bug or goal unmet ←──────────────┘
```

## When to Use

- Starting or running a real software build where goal, docs, tests, and memory should chain in order.
- A task large enough that "just write code" would drift — you need a persisted goal and a plan on paper first.
- The user asks for the "holy grail" dev workflow.

## The loop

1. **Persist the goal.** Capture the objective once; keep it intact for the whole run. (`goal-persistence`)
2. **Write a plan doc, then harden it.** Decide on paper before code; run the `source-anchored-design` critic loop on the plan once and improve it before implementing.
3. **Implement the plan, then critic-harden the implementation.** Send the diff to ONE critic subagent (fresh context — never self-review), re-verify the critic's load-bearing claims against source, apply minimal fixes, repeat until blocking = 0.
4. **Test.** Red-green TDD for behavior, plus a benchmark that measures how good the result is. (`tdd`)
5. **Dump a JOURNEY in between.** Record the human/AI back-and-forth and lessons at checkpoints, not only at the end. (`journey`)
6. **Write long-term memory.** Persist durable facts, decisions, and lessons so the next session resumes instead of re-discovering.

**Loop back:** a failing test or an unmet goal returns to step 2 (plan), not straight to more code.

## Pillars → skills

| Pillar | Skill | Contribution |
|---|---|---|
| Goal | `goal-persistence` | durable objective, anti-drift steering, completion audit |
| Documentation — plan/design | `content-craft`, `technical-research-analysis-doc`, `source-anchored-design` | 结论先行, 说人话, code anchors, impact chain, critic-hardened |
| Documentation — journey | `journey` | ME/YOU two-column history, risks/TODO up top, vibe-coding lessons |
| Testing | `tdd` | red-green loop, seams, vertical slices, anti-patterns |
| Benchmark | (this skill) | a numeric baseline so "better" is measured, not felt |
| Long-term memory | (this skill) | durable memory file + optional MCP knowledge graph |
| etc | `code-review`, `diagnosing-bugs`, `debugger-persona`, `implement` | review, root-cause, minimal fix, build |

## Rules

1. **Goal first, never narrowed.** Re-inject the objective every turn; audit completion against real state, never self-declared.
2. **Plan before code.** A plan doc names the approach, the seams, and the success criteria. Harden it with the `source-anchored-design` critic loop once before implementing — a fresh-context critic, never self-review.
3. **Vertical slices.** One test → one implementation → repeat. Don't write all tests then all code.
4. **Measure goodness.** "It works" is not a result; a benchmark number against a baseline is.
5. **Write memory as you go.** Decisions and gotchas land in the durable store the same turn they happen.
6. **Journey in between.** Dump `JOURNEY.md` at checkpoints, not only at the finish.
7. **Loop back on failure.** Return to the plan, not to more code.

## Stage handoff

Each stage hands a written artifact to the next:

- **goal** → objective + status + completion evidence
- **plan doc** → approach + seams + success criteria
- **implement** → code + what changed
- **test** → red-green results + benchmark vs baseline
- **journey** → `JOURNEY.md` (ME/YOU table + risks + lessons)
- **memory** → durable facts / decisions / lessons appended to the store

## Long-term memory (pillar 4)

A fresh session must resume without re-discovering what this one learned.

- **Durable memory file** — one project memory doc (default `<project>/KNOWLEDGE.md`, or a `.memory/` directory). Read it at session start; append decisions (why), facts (numbers with baselines), gotchas (error signature + fix), and next steps as they happen.
- **MCP knowledge graph (optional)** — if memory tools (`memory_create_entities` / `memory_add_observations`) are available, mirror the same facts as entities + observations.

Either way the contract is the same: read first, append as you learn, never let a discovered fact live only in the chat.

## Per-round gate (answer at the end of EVERY round)

A round does not close until all four questions are answered explicitly. Do not
advance to the next step — or repeat — on an unanswered gate.

1. **Success / fail criteria?** State the acceptance bar for THIS round — write
   it down verbatim so it can be restated in the report. What must be true (tests
   green? benchmark met? blocking issues = 0?) for the round to count as success
   vs failure. No criteria = drift, not a round.
2. **What should touch / not touch?** State the scope boundary: which files /
   areas / behaviors this round may modify, and which are off-limits. Anything
   outside the boundary is a scope violation, not a fix.
3. **Report criteria?** State what the end-of-round report must contain — use the
   fixed report format below, nothing else as the round summary.
4. **Self-review rounds + next step?** State how many critic rounds you will run
   before accepting (`source-anchored-design`: repeat until blocking = 0; set a
   hard cap if the round has a budget), and whether the next step auto-starts and
   repeats.

## Round report (fixed format)

At the end of every round, emit exactly this block — nothing else as the round's
summary. The agent does NOT judge success/failure itself; it restates the
original criteria, reports each one's current status, and gives only a
confidence score so the human can judge:

```
success criteria: <restate this round's original criteria verbatim>
criteria status: <one line per criterion: met / not met / partial, with evidence>
success confidence: <0-10>, <why>
failure confidence: <0-10>, <why>
goal sticked: <what subparts of goal done so far>
touched: <files/areas modified>
not touched: <files/areas deliberately left alone>
test ran: <results> <wall clock time spent>
journey: <what has been updated in short>
next: <single next action>
self review status: <critic rounds run, blocking issues remaining>
next step status: <auto-start | wait-for-user | done>
```

The two confidence scores (0–10) are the agent's own estimate of how likely the
round succeeded and how likely it failed — they are NOT a verdict. The human
decides success/failure from the criteria status, not from the scores.

## Termination

The loop ends when the goal's completion audit passes against real state — tests
green, benchmark meets baseline, memory and journey written — and the final round
report shows all criteria `met` with `next step status: done`. The agent never
declares the loop a success itself; the human does, from the criteria status. A
failing test or unmet goal is not termination; it is a return to step 2 (plan).

## When NOT to use

- Trivial one-shot edits — a one-line change does not need the whole loop.
- Pure research or content with no code — use `research` or the writing skills directly.
- A single skill already covers the task — don't compose for the sake of composing.
