---
name: mine-learnings
description: Mine project history (commits, docs, logs) for durable learnings and write them to LEARNINGS.md and CLAUDE.md, idempotently. Use when the user asks to "extract learnings", "mine learnings from history" or "update CLAUDE.md from project history".
---

# mine-learnings

Turn project history into durable, reusable knowledge: a `LEARNINGS.md` file
of dated entries, with the highest-value ones folded as short rules into
`CLAUDE.md`. Idempotent — safe to run repeatedly; only genuinely new material
produces new entries.

## Process

1. **Locate repo root and existing files.** `git rev-parse --show-toplevel`,
   then check for an existing `CLAUDE.md` and `LEARNINGS.md` at that root. If
   `LEARNINGS.md` doesn't exist, it will be created in step 6 — don't create
   an empty stub up front.

2. **Read the hash ledger.** If `LEARNINGS.md` exists, parse its hidden
   ledger comments (see `sections/learnings-format.md`) for both accepted
   hashes (entries already written) and rejected hashes (candidates the user
   declined on a previous run). Both sets are things to never re-propose.

3. **Gather history sources:**
   Sources and caps: `sections/history-sources.md`.

4. **Extract candidates.** Look for:
   Signals to look for: `sections/extraction-signals.md`.

   For each candidate, compute a content hash of the normalized learning
   text. Drop any candidate whose hash is already in the accepted or
   rejected ledger before it goes any further — this is what makes reruns
   idempotent.

5. **Confirm with the user before writing anything.** Present the remaining
   new candidates via `AskUserQuestion`, batched a few at a time (approve /
   edit / reject each). Never write a candidate straight to disk without
   this step — `CLAUDE.md` and `LEARNINGS.md` are checked-in files the user
   reads and re-reads; unwanted entries are expensive to notice and remove.

6. **Write approved entries to `LEARNINGS.md`** — dated section, category,
   source reference (commit SHA or file path), the learning itself (what
   happened, why it matters, how to apply it), and its content hash so
   future runs recognize it. Create the file with a short header if it
   doesn't exist yet.

7. **Fold only the most durable/actionable approved learnings into
   `CLAUDE.md`** as short rules, each pointing back to its `LEARNINGS.md`
   entry (e.g. `- Never do X — see LEARNINGS.md#short-title.`). Leave
   situational entries only in `LEARNINGS.md`.

   Model-routing learnings: `sections/model-routing.md`.
   Procedural: tank `evolve` may draft a skill (never auto-wired).

8. **Record rejected candidates' hashes** in `LEARNINGS.md`'s rejected
   ledger so they aren't re-proposed on the next run.

9. **Report a short summary**: N new entries written, M folded into
   `CLAUDE.md`, K rejected, L already-seen (no-op, skipped before the user
   ever saw them).

## Idempotency contract

Every run rescans full history — there's no watermark file to go stale or
drift from reality — but nothing is ever duplicated: a candidate's hash
being present in either ledger short-circuits it before it reaches the user.
Running the skill twice with no new history in between must report "0 new
candidates" and touch neither file.

## Notes

- If a repo has no docs/logs beyond git history, mine commits alone — don't
  treat a missing `LOGS/`/`docs/` as an error.
- If `LEARNINGS.md` would grow past a few hundred lines, suggest splitting
  by category or year to the user — don't do this unprompted.
- This skill never runs `git push`; writing local files is as far as it
  goes. Committing/pushing the result is a separate, explicit step.

## Sections
Read a section only when its condition applies; do not preload them.
- sections/history-sources.md: read at step 3
- sections/extraction-signals.md: read at step 4
- sections/model-routing.md: read at step 7 for model-choice learnings
- sections/learnings-format.md: read at steps 2, 6 and 8
