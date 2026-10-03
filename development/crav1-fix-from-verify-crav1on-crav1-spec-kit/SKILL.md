---
name: crav1-fix-from-verify
description: After /crav1-verify-spec, walk inner-loop gaps one by one (verify failed, then unverified, then G#). Fix in-spec and re-run that evidence. Omit Gap to take the next. Do not edit spec.md. Do not auto-pick unimplemented tasks.
disable-model-invocation: true
icon: bug
color: red
---

# Fix from verify

You run this **after `/crav1-verify-spec`**. Walk the **inner-loop queue** one item at a time: failed evidence, then unverified/could-not-run, then leftover `G#` wiring gaps. Omit `Gap` to take the next. Unimplemented tasks are **not** this skill (`/crav1-implement-task`).

Do not change `spec.md`. Do not invent product behavior to get a green matrix.

## Find the work

Spec folder: user @-mention, else most recently edited `docs/specs/` tree excluding `_template/`.

Read, in order:

1. `verify.md` (required if it exists). Chat TL;DR from the last `/crav1-verify-spec` in this thread counts as the same source.
2. `spec.md`, `tasks.md`, `plan.md` — spec wins.
3. Report shape: this skill’s `assets/fix-log.md`.

If `verify.md` is missing and they did not paste a verify TL;DR, **stop**. Next: `/crav1-verify-spec`. Do not guess gaps from vibes.

## Pick one gap (no edits yet)

This skill is the **inner-loop queue**: something is *supposed* to already work (or already be checked off) but verify could not prove it. It is not a backlog burn-down.

**In the queue** (walk in this order; skip empty buckets):

1. **Implemented, verify failed** — evidence ran and contradicted (`T#` then `A#` as listed in `verify.md`)
2. **Claimed done, unverified** — `[x]` but evidence could not run (no host, port, browser, SQL)
3. **`G#` in verify.md Gaps** — only if it is the same kind of problem (fail, untested, live/wiring) **and** it is not a duplicate of a `T#`/`A#` already in (1) or (2)

**Not in this queue** (do not auto-pick; say so and point elsewhere):

| Verify says | Use instead |
| --- | --- |
| **Not implemented** | `/crav1-implement-task T#` |
| **Acceptance with no task** | `/crav1-plan-from-spec` or `/crav1-tighten-spec` — this skill does not grow the spec |

If they named `T#` / `A#` / `G#`:

- Inner-loop (failed, unverified, or a wiring `G#`) → that is the current item
- Not implemented / no-task → **stop**, send them to the table above. Do not implement a new `T#` here just because they typed the id

If they **omitted Gap**: take the **first remaining** item in the queue above. List the rest as `F2`, `F3`, … so the next `/crav1-fix-from-verify` with no Gap continues the walk.

Build the queue fresh from `verify.md` each turn (minus what `fix-log.md` already marked fixed **and** whose evidence you re-ran green). Deduplicate: one live SQL proxy failure that explains three unverified rows is still **one** current item — after the fix, re-run **each** of those rows’ evidence.

**Stop** (no fix) if:

- Closing the gap needs behavior **not** in the spec
- It would implement a **non-goal** or reopen a rejected ADR
- Playbook-only workspace and they did not ask to change an app here
- The inner-loop queue is **empty** (only unimplemented / no-task left, or everything verified) — tell them `/crav1-implement-task` or `/crav1-verify-spec` / ship

Confirm the before-state: re-run that row’s evidence once. Quote the failure. Do not skip.

## Fix (in spec)

Smallest change that makes **this** verify row pass:

- Product code only if this row is **verify failed** (already implemented, evidence red) — not to start an unimplemented `T#`
- Tests or UI checks that **cover existing** acceptance (new test OK; new acceptance not OK)
- Inner-loop wiring when evidence could not run or failed for connectivity: publish/ports, Aspire/SQL proxy, env, compose waits, operator health probes — not a new public API unless the spec already has it

Do **not**:

- Edit `spec.md`, exports, or acceptance text
- Delete or weaken the failing check to go green
- Refactor unrelated files
- Add endpoints, fields, or actors the spec does not require

## Verify the fix (required, same turn)

If this gap’s evidence is **live**, follow `crav1-verify-spec` `references/live-host.md` (drop-in: `.cursor/skills/crav1/crav1-verify-spec/references/live-host.md`; plugin: sibling `skills/crav1-verify-spec/references/live-host.md`) **before** re-running it (especially after you changed API/service code).

1. Re-run **the same evidence** for this gap (test name, UI path, or live HTTP/DB command from verify.md / the user). Fail → pass, or report still failing.
2. If you changed app or config, re-run the repo test command. Must still pass.
3. Extra probes (SQL ready, etc.) are optional **add-ons**. They do not replace the verify row.

Passing tests alone is not enough when the gap was live/untested. The **row’s evidence** is enough when the gap was a failing test.

Update `tasks.md` `[x]` only if that task’s stated verify now passes.

## Write `docs/specs/<slug>/fix-log.md`

Follow this skill’s `assets/fix-log.md` (TL;DR first). **Append** a dated entry if the file exists.

Optionally patch **only this row** in `verify.md` if that file exists (status/evidence). Do not restage the whole matrix — tell them to run `/crav1-verify-spec` for a fresh full report.

Do not rewrite `spec.md`.

If an older `live-fix.md` exists, you may append a one-line pointer to the new `fix-log.md` entry. Prefer `fix-log.md` going forward.

## After (chat)

TL;DR first:

- Which verify bucket / id you fixed
- Before → after (the **same** evidence)
- Tests still pass? (if you ran them)
- Files changed
- Remaining **inner-loop** ids (`F2`…) — not unimplemented tasks
- Next: `/crav1-fix-from-verify` with **no Gap** to continue the walk, or `/crav1-verify-spec` when the inner-loop queue is empty

## Hard rules

- **Spec is frozen.** Disagreement with the spec → stop, do not patch the spec.
- One inner-loop item per turn unless they named a shared cause and listed the ids. Omit Gap = next in queue.
- Do not mark success without re-running that gap’s evidence.
