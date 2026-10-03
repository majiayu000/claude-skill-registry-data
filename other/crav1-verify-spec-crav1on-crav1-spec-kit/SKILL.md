---
name: crav1-verify-spec
description: Map every v0 acceptance line to tests or UI checks and report pass, fail, or missing. Lead with a TL;DR of which tasks are implemented vs not. Use after implementation or when the user wants proof against spec.md. Do not add product features.
disable-model-invocation: true
icon: beaker
color: orange
---

# Verify spec

You prove the **running system** (or current tree) against `spec.md`. You do not add features. You do not “fix” the spec to match the code.

Lead with a **TL;DR**: which tasks are implemented and verified, which are not. Same facts as today — **overview first, details below**.

## Find the spec

User @-mention, else the most recently edited tree under `docs/specs/` excluding `_template/`.

Read `spec.md` acceptance (and EARS/BDD export if present — spec.md still wins). Read `tasks.md` if it exists. Skim tests and the files `plan.md` said would be touched.

## Classify each task (before writing)

For every `T#` in `tasks.md`:

| Status | Meaning |
| --- | --- |
| **Implemented, verified** | Row is `[x]` **and** its verify evidence ran and passed |
| **Implemented, verify failed** | `[x]` or code exists for this `T#`, but verify ran and failed |
| **Not implemented** | Still `- [ ]` (or no code for this `T#`) |
| **Claimed done, unverified** | `[x]` but evidence could not be run (no command, no browser) |

Acceptance lines with **no** `T#` stay in the detail matrix as **missing** coverage — also list their ids in the TL;DR.

## Results (unchanged meanings)

- **pass** — evidence ran and matched the acceptance line
- **fail** — evidence ran and contradicted it
- **untested** — could not run (no command, no browser)
- **missing** — no test, no task, no UI path covers it

**Evidence** must be something a stranger could rerun. “Looks fine” is not evidence.

Then:

1. If any acceptance or task verify is **live** (running Aspire/compose/dev host, published URL, browser against localhost), follow this skill’s [references/live-host.md](references/live-host.md) **before** that evidence. Record refresh/health in **Commands run**.
2. Run the documented test/lint commands from `AGENTS.md` or the repo README when they exist. Record the command and outcome.
3. For UI acceptance, use the browser if available; otherwise mark **untested** and say why.
4. Map `tasks.md` rows: checked but failing verify → **Implemented, verify failed**; unchecked → **Not implemented**.

## Write `docs/specs/<slug>/verify.md`

Follow this skill’s `assets/verify.md` **section order**. Do not put the long acceptance table first.

1. **TL;DR** — counts + id lists. Then one line: next command (`/crav1-fix-from-verify` if failed/unverified/`G#` remain, else `/crav1-implement-task` or ship).
2. **Tasks — overview** — one short table: `T#` | title | status | verify result. Group or sort: verified first, then failed, then not implemented.
3. **Acceptance — details** — the full A# matrix (quote, evidence, result).
4. **Commands run**
5. **Gaps** (`G1`, `G2`, …)

Do not rewrite `spec.md`.

## After the report (chat)

Same order as the file. Do **not** open with the full acceptance matrix.

1. Path to `verify.md`
2. **TL;DR** (copy the id lists; they should be scannable in a few seconds)
3. Point at the Tasks overview in the file
4. Next:
   - Inner-loop (**verify failed**, **claimed done, unverified**, wiring **`G#`**) → `/crav1-fix-from-verify` (omit Gap to walk them in order)
   - **Not implemented** → `/crav1-implement-task T#`
   - acceptance with no task → `/crav1-plan-from-spec` or `/crav1-tighten-spec` if the line should die
   - all **Implemented, verified** and no missing acceptance → spec is demoable; they can ship / PR

Do not start implementing in this turn unless they already named a `T#` to fix.

## Hard rules

- Do not invent new acceptance. Do not expand v0.
- Do not mark pass without a command, test name, or exercised UI path.
- If the code is right and the spec is wrong, say so and send `/crav1-tighten-spec` — do not silently edit the spec.
- If this workspace has no application to run, report **untested** / **claimed done, unverified** with that reason; do not scaffold an app to get a green matrix.
- Do not bury task implementation status inside the acceptance table. Overview is task-first; details are acceptance-first.
