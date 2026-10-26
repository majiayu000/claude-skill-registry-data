---
name: implement-feature
description: Execute a planned spec task-by-task with gates green at every step. Use when a spec has plan.md + tasks.md and the user says "implement", "build it", "execute the plan", or names the spec. This is the long-running workhorse — it runs a one-pass preflight, ticks tasks.md checkboxes, makes checkpoint commits, and ends by chaining verification. Subsumes the old /implement-prd command.
argument-hint: [spec number or slug]
allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash(npm *) Bash(npx expo *) Bash(git status*) Bash(git add *) Bash(git commit *)
---

## Task

Implement spec **$ARGUMENTS** by executing its `tasks.md` top to bottom.

### Step 0 — Analyze preflight (one pass, then go)

Before writing any code, do ONE consistency pass — not a document dump:

1. Spec ↔ plan/tasks ↔ codebase: every acceptance criterion maps to a task and a planned test; every task's target file is either new or listed in the plan's reuse inventory. **If something the tasks would create already exists in `src/`, flag it and reuse it — never regenerate existing code.**
2. If a NEW material ambiguity emerges, ask now (max 3 questions), not mid-implementation.
3. State the result in two lines ("Preflight OK" or the discrepancies) and proceed. Produce no extra planning artifacts.

### Operating rules

1. **Ground first.** Read the spec folder (spec/plan/tasks) fully, then the docs the plan cites and `docs/architecture/module-boundaries.md`.
2. **One task at a time.** Work strictly in `tasks.md` order (parallelize only `[P]` tasks). For each task: implement → run its done-check → tick the checkbox in tasks.md → conventional checkpoint commit (`feat(slug): T3 …`). The ticked file is the durable progress record — after any context compaction, re-read tasks.md to recover state instead of guessing.
3. **Scaffold, don't hand-roll.** New slices come from `/new-module <slug>` (or `npm run new:feature -- <slug>`). Write each AC's test before or with its implementation.
4. **Keep gates green.** `npm run lint && npm run typecheck && npm test` after every task; `npm run verify` at phase ends. A red gate is the harness prompting you — fix the work, never the gate (Constitution Art. IV). If a gate seems genuinely wrong, stop and surface it.
5. **Stay in scope.** The spec's _Out of scope_ list is binding. If implementation reveals a needed scope change, stop, say so, and update the spec with the user — don't ship surprises (they arrive as unreviewed product surface).
6. **Imitate the canon.** When unsure how something should look here, copy the patterns of `src/features/tasks/` (the `model/ui/lib` anatomy, Zod schema in `model/schema.ts`, Zustand store in `model/store.ts`, `testID`s, NativeWind via `cn()`) rather than inventing. Consistency is a feature.
7. **Blocked?** Two failed attempts on the same task → stop, write what you tried and your best hypothesis, ask. Don't burn the context window thrashing. Also stop when a boundary rule blocks the design, the spec conflicts with an ADR, or a dependency would need adding.

### Exit

When all tasks through the verification phase are ticked: run `/verify-ui $ARGUMENTS`, then `/review`, then `/feature-report $ARGUMENTS`. Report: tasks completed, gates status, anything deferred, and the PR-readiness checklist from `docs/process/definition-of-done.md`.
