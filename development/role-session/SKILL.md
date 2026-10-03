---
name: role-session
description: Parallel-session lane protocol — role charters, file-lock claims, git token queue, per-role handover; sequential fallback without handover/ folder. Trigger when the user assigns a role ("you are the tester", "frontend session") or a handover/ board/locks structure exists.
---

# Role Session — One Lane of the GPU

The user runs multiple parallel Claude sessions, each a job role with one task, human-in-the-loop (the dev watches, reviews, and pushes/pulls git manually). This skill is the lane protocol: stay in your charter, claim files before editing, never touch git without the token, hand over on completion.

**Sequential fallback:** if the project has no `handover/` folder (just a classic `handover.md`, or nothing), this machinery is off — work normally, use the `handover` skill's classic mode. Never create the parallel structure unprompted; the user activates it.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a coordination failure seen, a rule that saved a conflict, friction worth removing. Merge instead of duplicating; delete disproven bullets.

## The coordination files (in `handover/`)
```
handover/
  PROTOCOL.md    ← cross-tool coordination protocol (see protocol.md in this skill's folder)
  board.md       ← lane dashboard: one row per active task (role, task, files, status)
  locks.md       ← file claims + git token/queue (formats below)
  roles/<role>.md← charter: mission, owned paths, forbidden paths, definition of done
  <role>.md      ← per-role handover (state, next steps) — replaces single handover.md
```
`PROTOCOL.md` is the tool-agnostic layer for repos shared with other AI tools (OpenCode, Codex, …): session-start modes (new claim vs. resume), incremental handover writing, stale-lock recovery, graceful handoff. Follow it alongside the lane rules below.
`locks.md` format:
```
git: free                      ← or: held by <role> (<task>)
git-queue: <role>, <role>      ← approved work waiting to commit, FIFO

| File | Role | Task | Status | Claimed |
| src/x.ts | frontend | venus counters | editing | 2026-07-12 14:30 |
```
Statuses: `editing` → `awaiting-review` → (rows deleted on completion).

## Session lifecycle

**1. Boot.** Confirm your role with the user if not stated. Read: your charter (`roles/<role>.md`), `board.md`, your `<role>.md` handover, `locks.md`. Add/update your board row (`role | task | files | in-progress`) — the `Files` column lists every path the task will touch; before a **new** claim, verify every listed file is free in `locks.md` (per `handover/PROTOCOL.md`). Stay strictly inside charter-owned paths; needing a forbidden path = stop and ask the dev, never trespass.

**2. Claim before edit — never before.** At the moment you are about to make your first edit (NOT during plan mode / analysis / discussion — reading anything, including locked files, is always free):
- Add a row per file you'll edit, status `editing`, timestamped.
- Re-read `locks.md` to verify your rows are the only claims on those files (claim-verify-proceed).
- If a file is already claimed by another role: do not edit. Inform the dev — who holds it, their task and status — and wait for the dev's call. The dev may override stale rows (a dead session's leftovers); that's the dev's decision, never yours.
- **Scope growth:** any file entering edit scope mid-task gets claimed the same way before it is touched. No exceptions — unclaimed edits are the one thing that breaks the whole system.

**3. Work.** Normal discipline (standards chain, session-budget, debug-protocol all apply). Edits only within charter paths + claimed files.

**4. Handoff for review.** Work complete and self-verified — run `pre-merge-gate` scoped to your own claimed files — then flip your lock rows to `awaiting-review`, update board row to `awaiting-review`, tell the dev what to look at. Keep all locks — they protect the work through the review wait. If the dev requests changes, flip touched rows back to `editing` and continue.

**5. Commit — only with the token.** After dev approval:
- Append your role to `git-queue` in `locks.md`.
- Take the token only when `git:` is `free` AND you are first in queue. Set `git: held by <role> (<task>)`, remove yourself from the queue.
- Stage **only the files in your lock rows** — your lock rows are the commit manifest. Never `git add .` — other lanes' work-in-progress shares the tree.
- Commit per the project's git standard (pre-commit skill applies). No push/pull — that is the dev's, always manual.
- Release: set `git: free` immediately after committing. Holding the token is a seconds-long act; never work while holding it.

**6. Complete.** Delete your lock rows, update your `<role>.md` handover (outcome, decisions, next steps for this role), clear your board row, capture any memory-bank-worthy knowledge. Session's job is finished.

Three boundedness rules apply here. Each exists because these files are read at every session start, so anything parked in them is charged to every future session:
- **Your `<role>.md` obeys the `handover` skill's 120-line ceiling and its routing table** (current state → handover · decisions and solved mysteries → `memory-bank/` · what happened → git, never copied). The ceiling is per role file, since each session reads only its own. Over it, run `memory-gardener`.
- **Clear your own `done` board row as part of completing** — don't leave it for the dev. A board that accumulates finished rows is the same unbounded-growth bug in a different file.
- **`memory-bank/` is shared and owned by no role.** Claim `memory-bank/INDEX.md` in `locks.md` before demoting into it, and release in the same step — concurrent demotions from two roles otherwise collide on the index.

## Session-mode notes
- **Plan mode:** planning is read-only — no lock claims, no board writes until the plan is approved and execution starts. Claims happen at first edit (rule 2 already enforces this).
- **Auto-accept / autonomous:** all rules above hold without the dev prompting them — especially claim-before-edit and stage-only-locked-files, which are what make autonomy safe in a shared tree.
- **Manual-approve:** identical behavior; lock-file writes are just edits the dev approves like any other.

## Shared-runtime awareness
One dev server / build / test run exists for all lanes. Before verifying against the running app, note that other lanes may be mid-edit; prefer verifying `awaiting-review` (stable) states, and tell the dev when a check needs the tree quiet. Tester role: prefer reviewing lanes' `awaiting-review` work over live-edited code.

## Hard rules (the ones that must never bend)
1. No edit to an unclaimed file.
2. No edit outside charter paths without dev approval.
3. No git command without holding the token; never `git add .`; never push/pull.
4. Locks live until completion — through review waits.
5. Another role's rows are read-only — only the dev overrides them.
