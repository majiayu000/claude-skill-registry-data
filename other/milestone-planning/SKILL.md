---
name: milestone-planning
description: Structures multi-week work as a milestone with a roadmap, a short always-read STATE digest, phased executable PLAN files with YAML frontmatter and XML task bodies, wave-based parallel execution by fresh subagents, deviation rules, checkpoints, and SUMMARY files for cheap history. Use when scope exceeds about one week or eight tasks, or when starting a greenfield project.
---

# Milestone Planning

`opm:writing-plans` handles a task list that fits in one head and one context window.
When the work is bigger than that (weeks, many tasks, several subsystems, or a blank repo) you
need a structure that survives context resets, lets independent work run in parallel, and leaves
a history the next session can read in under a minute. That structure is a milestone.

## When to use

- Estimated scope is more than about one week or more than about eight tasks.
- Greenfield project, or a feature that touches three or more subsystems.
- The work will span several sessions and someone (or some agent) will need to pick it up cold.

If in doubt, start with `opm:writing-plans`; promote to a milestone when the task list stops fitting.

## Artefacts

```
docs/milestones/<milestone>/
  ROADMAP.md                 phases, goals, status  (written once, updated at phase boundaries)
  STATE.md                   under 100 lines, ALWAYS read first, updated after every plan
  ISSUES.md                  deferred enhancements and known gaps, numbered ISS-NNN
  phases/
    01-<name>/
      PLAN-01-01.md          executable plan (frontmatter + XML body)
      PLAN-01-02.md
      SUMMARY-01-01.md       what actually shipped, with requires/provides/affects
      SUMMARY-01-02.md
    02-<name>/
      ...
```

Templates live in this skill's `templates/` directory: `plan.md`, `state.md`, `summary.md`.

### ROADMAP.md

One section per phase: number, name, one-line goal, the plans it contains with checkboxes,
and a status line. Phases are vertical slices (a user-visible capability end to end), not
horizontal layers (all models, then all APIs, then all UI). A roadmap of four to eight phases
is typical; if you have more than ten, the milestone is too big.

### STATE.md

The project's short-term memory. Every session that touches the milestone reads it first and
updates it after each plan completes. Contents: current position (phase X of Y, plan A of B,
status), the last three to five decisions, open blockers, a pointer to ISSUES.md with a count,
and "stopped at" for session continuity. Under 100 lines, always. It is a digest, not a log;
history lives in the SUMMARY files.

### ISSUES.md

Numbered list of deferred work discovered during execution: `ISS-007: add rate limiting to
login (found in 02-01, Task 2)`. Reviewed when planning each new phase.

## Plan format

A PLAN file is the executable prompt for one subagent. It must be specific enough that the
executor never has to guess. Two or three tasks per plan; if you need more, split the plan.

### Frontmatter

```yaml
---
phase: 02-auth
plan: 01
wave: 1                       # computed at planning time from depends_on and files_modified
depends_on: []                # plan ids, e.g. ["01-02"]; only real dependencies
files_modified: [src/lib/auth.ts, src/middleware/auth.ts]
autonomous: true              # false if any task is a checkpoint
---
```

### Body

```xml
<objective>
What this plan delivers and why it matters for the milestone. Two or three sentences.
</objective>

<context>
Files the executor must read before starting: STATE.md, the relevant source files, and prior
SUMMARY files only when this plan actually consumes what they built.
</context>

<tasks>
<task type="auto">
  <name>Task 1: Create session helper with signed cookie</name>
  <files>src/lib/auth.ts</files>
  <action>Export createSession(userId) and readSession(req). Use jose (not jsonwebtoken: CommonJS
  breaks under the Edge runtime). 15-minute expiry, httpOnly, sameSite=lax.</action>
  <verify>npx vitest run src/lib/auth.test.ts passes; npx tsc --noEmit is clean</verify>
  <done>Round trip create -> read returns the same userId; expired token returns null</done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Login form wired to the session helper</what-built>
  <how-to-verify>1. pnpm dev  2. visit /login  3. sign in with the seed user  4. confirm redirect to /app and the cookie in devtools</how-to-verify>
  <resume-signal>Reply "approved" or describe what is wrong</resume-signal>
</task>
</tasks>

<verification>
Plan-level checks beyond individual tasks: full test suite green, build passes, no new lint errors.
</verification>

<success_criteria>
Measurable statements: "unauthenticated request to /app redirects to /login", not "auth works".
</success_criteria>
```

Every `auto` task has all five children. `files` are exact paths. `action` says what to do, what
to avoid, and why. `verify` is a command or an observable behaviour. `done` is testable without
judgement.

Before writing any plan, run the retrieval half of `opm:compound-learnings` against
`docs/solutions/` for the phase's keywords; prior learnings become constraints in `<context>`.

## Checkpoint types

| Type | Share | Use for |
|---|---|---|
| `checkpoint:human-verify` | most | Visual or interactive confirmation of something already built |
| `checkpoint:decision` | some | A choice that sets direction: present options with pros and cons, wait |
| `checkpoint:human-action` | rare | Steps with no CLI or API: email verification links, 2FA codes, manual approvals |

The rule: if it has a CLI or API, the executor does it. Checkpoints are for confirmation and
decisions, never for delegating automatable work to a human. Batch verification into one
checkpoint at the end of a plan rather than one after every task. An authentication error
during execution is not a failure; it becomes a dynamic `human-action` checkpoint ("run
`vercel login`, then reply done") followed by a retry.

Any plan containing a checkpoint sets `autonomous: false`.

## Wave algorithm

Waves are computed when the phase is planned and written into each plan's frontmatter, so the
executor does no dependency analysis at run time.

1. Start with all plans in the phase, wave unassigned.
2. A plan is eligible for wave N when every id in its `depends_on` is in a wave lower than N.
3. Among eligible plans, two can share a wave only if their `files_modified` sets do not overlap.
4. Assign the lowest wave that satisfies both rules. Repeat until every plan has a wave.
5. Plans with `autonomous: false` stay in their computed wave; they simply pause at their checkpoint.

Do not add `depends_on` because a plan is numerically earlier. Only a real consumption
relationship (types, exports, decisions, data) is a dependency. Reflexive chaining serialises
work that could have run in parallel.

## Executing a phase

The orchestrator stays small: it reads STATE.md and the phase's plans, groups them by wave, and
for each wave spawns one fresh subagent per plan, all in a single message so they run in parallel.
It waits for the wave to finish, confirms each SUMMARY exists, then starts the next wave.

Each subagent receives the plan path and STATE.md, and executes the plan using the task discipline
of `opm:executing-plans`: read the task, do exactly it, run `verify`, confirm `done`, commit that
task's files individually (`feat(02-01): task name`), move on. TDD-shaped tasks use
`opm:tdd-workflow`. At the end the subagent runs `opm:verification-loop`, writes the SUMMARY,
and updates STATE.md. When it hits a checkpoint, it stops and returns the checkpoint content plus
a table of completed tasks; after the human responds, a fresh subagent continues from the next
task. Agents are not resumed; state lives in files and commits, not in context.

### Deviation rules

Plans are guides, not straitjackets. During execution:

1. **Bug found in scope** - fix it now, note it in the SUMMARY under Deviations.
2. **Security or correctness gap** - add the fix now, note it.
3. **Blocker** (missing dependency, broken config) - fix it now, note it.
4. **Architecture change** - stop and ask. Do not refactor structure on your own initiative.
5. **Enhancement or polish** - log to ISSUES.md as `ISS-NNN` with the plan and task, continue.

Only rule 4 needs the human. Everything else is recorded, not asked.

### Commit rules

One commit per task, staging only that task's files (never `git add .` or `-A`). Format
`<type>(<phase>-<plan>): <task name>` with type in feat, fix, test, refactor, perf, chore.
After the last task, one metadata commit for PLAN, SUMMARY, STATE: `docs(02-01): complete plan`.

## SUMMARY files

Written by the executing subagent when a plan finishes. The frontmatter is what makes history
cheap: future planning scans only these ~20 lines across all SUMMARY files to assemble context.

```yaml
---
phase: 02-auth
plan: 01
requires:
  - { phase: 01-foundation, provides: prisma User model }
provides:
  - createSession / readSession helpers in src/lib/auth.ts
  - auth middleware protecting /app/*
affects: [03-dashboard, 04-billing]
key_files: [src/lib/auth.ts, src/middleware/auth.ts]
key_decisions:
  - "jose over jsonwebtoken: ESM and Edge compatible"
issues_created: [ISS-004]
completed: 2026-09-12
---
```

The body opens with a substantive one-liner ("Signed-cookie sessions with 15-minute expiry and
protected /app routes", never "auth done"), then accomplishments, task commits with hashes,
decisions, deviations (auto-fixed and deferred), and readiness notes for the next phase.

## Continuation closer

Every planning or execution turn that ends a unit of work closes with the same block, so the
human can copy one line and keep going in a fresh context:

```
---
## Next up

**02-02: Refresh token rotation** - sliding expiry on /api/auth/refresh

Execute: docs/milestones/v1/phases/02-auth/PLAN-02-02.md

Run /clear first (fresh context window; STATE.md carries everything needed).

Also available:
- Review the plan before executing
- Plan phase 3 instead
---
```

Always name what the next thing is, not just its path. Pull the description from ROADMAP.md or
the plan's `<objective>`.

## Lifecycle in one screen

1. **Start**: write ROADMAP.md (phases as vertical slices), an empty STATE.md, an empty ISSUES.md.
2. **Plan a phase**: read STATE.md, ROADMAP.md, ISSUES.md, prior SUMMARY frontmatter, and
   `docs/solutions/`. Use `opm:brainstorming` if the approach is unclear. Write two to five
   PLAN files, compute waves, commit them. Close with the continuation block.
3. **Execute the phase**: wave by wave, fresh subagent per plan, checkpoints surface to the human.
4. **Close the phase**: confirm every plan has a SUMMARY, tick the roadmap, refresh STATE.md,
   run `opm:compound-learnings` for anything non-obvious that happened. Close with the continuation block.
5. **Close the milestone**: when the last phase closes, write a short retrospective at the top of
   ROADMAP.md and reset STATE.md for the next milestone.
   Optional: `/opm:explainer-video <path>` turns this into a narrated explainer.

## Anti-patterns

- A STATE.md over 100 lines (it stopped being a digest).
- Plans with one huge task or more than three tasks.
- Horizontal phases (all models, then all APIs).
- `depends_on` set by numbering rather than by consumption.
- A checkpoint after every task.
- Asking the human to do something a CLI can do.
- Resuming an old subagent instead of spawning a fresh one from files.

<!-- Adapted from gsd-build/get-shit-done (MIT) -->
