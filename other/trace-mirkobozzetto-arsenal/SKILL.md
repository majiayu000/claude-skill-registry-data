---
name: trace
description: Save where the session stands before ending it, so next can resume it in a clean context. Also reads or records project progress.
argument-hint: "[save] | [done <what> --files a,b --id id --status shipped] | [--read n]"
---

# Trace

Run at the end of a session the user wants to close, before `/clear`. It
leaves a dated save that `next` offers to resume. Trace never resumes work
itself. Resolve `scripts/trace.cjs` from this skill's directory.

## Save (no argument, or `save`)

1. Gather, without asking: this conversation; `git log` since the last save
   (`node scripts/trace.cjs saves --all` gives its date); `git status
   --short`; planned work: briefs (`docs/brief/*/brief.md`) and proposals
   (`docs/proposals/*/PROPOSAL.md`) not shipped or superseded, review reports
   (`docs/review/*/report.md`) with unchecked points, and open issues from
   `gh issue list --label arsenal --state open` when `gh` answers.
2. Show at most five lines: done, not finished, planned.
3. Ask only what the context cannot answer, one question per message, in
   plain text and the conversation language, then wait:
   - what to continue next session, with your suggestion;
   - anything to remember that you may have missed: a decision, an approach
     that failed.
   Skip a question the conversation already answers. Usually none is needed.
4. Write it: `node scripts/trace.cjs save --done "…" --left "…" --next "a ;
   b" --remember "…" --planned "…"`. One line per field, in the conversation
   language, specific: paths, branch, task ids, issue numbers, commands.
   Omit an empty field.
5. End with « Tu peux /clear. » in the conversation language, then the
   resume command as the last line: `next` in the harness syntax
   (`/next:next` in Claude Code, `/skill:next` in OMP and Pi, `$next` in
   Codex).

The save is private: the script adds the ledger to `.git/info/exclude` and
it never enters a commit.

## Other modes

- `done "<what>" [--files a,b] [--id id] [--status shipped]`: one intent
  entry. `shipped` only with evidence.
- `--read n`: print the last entries, then stop. Do not reopen the work
  they describe.

The Stop hook logs files moved and commits made each turn, with no model
call. It records activity, not delivery: never upgrade wip to shipped
without evidence. Keep this cross-session ledger distinct from a ship run's
`trace.md`; do not copy events between them.

## Execution policy

Work solo. Ask before any subagent or reviewer, even in auto mode. No
hidden advisor, nested delegation, model retuning, repeated successful
checks, or progress spam. Stop when the save is written. User stops and
scope changes override pending steps.
