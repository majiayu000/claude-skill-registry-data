---
name: session-unit
description: "Use when a session starts or is told to finish work: the default end is the PR, CI, a merge commit, the WC debrief, and the report. Stop earlier only when that turn said so. Hand the next named unit to a new Orca tab."
---

# Session unit

This file owns the close of one unit: open the PR, read CI, merge with a
merge commit, run the WC debrief, clean up the worktree, and report.
[`AGENTS.md`](../../AGENTS.md) §One session, one unit wins if they disagree.
Do not copy the close into `pr-authoring`, `worktree-dispatch`, `release`, or
`orca-tab`. Point here.

Worktree commands stay in `worktree-dispatch`. The tab stays in `orca-tab`.
The PR body stays in `pr-authoring`. A version the user asked for stays in
`release`. The WC recording step stays in
[`session-debrief`](../session-debrief/SKILL.md).

## Where it slipped

At `e914dfb` (2026-09-26) the sentences that say merge is part of the unit
were already in this file's body and in `AGENTS.md`. Sessions stopped earlier.
These are the windows they actually read.

| What they read | At `e914dfb` | Where that window ended |
|---|---|---|
| This file's description, first 160 characters | `skills/session-unit/SKILL.md:3` | `through the PR, then hand` |
| This file's done checklist | `skills/session-unit/SKILL.md:62` | `The PR is open` |
| Pin step | `skills/session-unit/SKILL.md:15-16` | the brief's words became the done-condition |
| Carry-through bullet | `AGENTS.md:232-234` | `then the PR` |
| Before claiming done | `AGENTS.md:138-147` | accepting the PR |
| Brief may withhold the merge | `skills/worktree-dispatch/SKILL.md:165-166` | `say when it is withheld` |
| Release description, first 160 characters | `skills/release/SKILL.md:3` | the omission list; "use when" sat past the window |
| Ban that got copied into later briefs | `docs/product/ULTRAGOAL_PROMPT_COLD_START_DEEPSEEK_DEPTH_6X.md:55-56` | `Do not touch the 6.0.0 release lane` |

A new sentence next to those lines does not block the next session. The
description's first 160 characters are the close, the done checklist requires
`MERGED` / `mergedAt` / `mergeCommit`, and `scripts/check-session-close.sh`
fails if that slips. Codex loads about those 160 characters; Grok loads about
the first 400 bytes (measured 2026-09-23). Both windows of the old
description ended at the PR.

## Order

1. **Pin.** Before the first edit, write the done-condition in one sentence
   from the user's turn. A handoff brief carries that sentence as
   `user-turn:`. A prohibition in the rest of the brief does not replace it.
   Run `scripts/check-session-close.sh brief <file>`. If it fails, the brief
   lost; follow the user turn and say which clause of the brief you dropped.
   Do not shrink the sentence to what this session can finish easily.
2. **Look.** `worktree-dispatch` §0. If another worktree already owns this
   unit, stop and name it.
3. **Change** only what the done-condition needs. A defect in a file this
   unit is already changing, unowned by another session, is its own commit
   and still this unit. Anything the opening did not name waits for step 7.
4. **Ship,** unless that turn said to stop earlier.
   - Run the checks the change needs. The report names the command and what
     it printed.
   - One concern per commit: `git add <path>` then
     `git commit -F <message-file> -- <path>`.
   - Open the PR with `pr-authoring`, which includes the push. From the
     control tower, use that skill's control-tower mode (`--repo`, `--head`,
     per-command token).
   - A denial that the publication route only allows registered units is a
     missing registration, not the end of the unit. Register that unit in the
     same turn, then call `gh pr create` again as one command:
     `GH_TOKEN="$(gh auth token --user innocarpe)"`, `--repo innocarpe/deepseek-build`,
     `--base main`, `--head` this branch, `--body-file` a `.md` file under `/tmp`,
     and the registered labels. No pipe, no redirection, and no second command
     in the same line. Do not disable the hook, and do not stop after quoting
     the denial.
   - Don't hold the PR for local polish: commit → push → PR once the evidence
     exists, then keep polishing on the branch. `grok fmt` and `grok clippy`
     are the longest polls and they run on GitHub — the PR in flight is the
     faster feedback loop.
   - Read CI. `scripts/check-pr-merged.sh <n>` exits 2 while checks are
     pending. Pending is not a pass and not a reason to end the unit.
   - Merge with `gh pr merge --merge` (merge commit; squash is disabled).
     Run `scripts/check-pr-merged.sh <n>` again and paste its output. Stop
     short of the merge only when that turn said so — a review-only unit, a
     stacked child whose parent is unmerged, or a PR the user asked to look
     at first.
5. **Debrief** with [`session-debrief`](../session-debrief/SKILL.md). After
   the end conditions above stand (or the earlier stop this turn named) and
   before the report, count what the unit produced and record the WC-worthy
   parts with the global `w-conatus` skill. The owned worktree still exists
   here — the count reads it, and cleanup follows this step. The close
   authorizes those writes — do not ask again. A unit with nothing
   transferable reports `no record needed` with the reason; if the WC root
   cannot be resolved and verified, write nowhere else and do not report the
   unit done.
6. **Clean up** the worktree with `worktree-dispatch` §4, after the debrief
   has read it.
7. **Hand off** each next unit the opening already named, with
   `worktree-dispatch` §1–§3b. The tab itself is `orca-tab`. The brief file
   lives outside the repo. Its first line is `user-turn:`. Do not ask first.
   After the receipt shows `turn_started`, report the handle and that
   sentence, then leave the unit alone.
8. **Close.** The report below. What you did not do is a separate list. That
   list does not open the next unit, and it is not step 7.

When the user turn asks to ship a version, `skills/release` is this unit. A
brief that bans the release lane does not remove it. An empty `## Unreleased`
does not finish that ask. The release skill owns that clause; this report's
first line names it when it did not stand.

## Report

The first line is whether the done-condition holds. If it does not, name the
clause. Do not write that the unit is done when a clause failed.

The report says what the evidence means, so a reader can close the session
without having watched it run. Command-output dumps and file lists push the
interpretation back to the reader; these elements carry it:

- **What changed, and why.** One short paragraph: the unit's result as the
  user meets it, and the defect or gap that motivated it. The PR body argued
  this to reviewers; this paragraph survives the conversation.
- **Observation and inference are separated.** A measured sentence carries
  the command, `file:line`, or SHA that showed it; a conclusion drawn rather
  than measured says so. When a before → after number was measured, give both
  sides; a number that was not measured stays out.
- **Evidence.** Paste the output, not a paraphrase:
  - PR URL
  - CI, from `scripts/check-pr-merged.sh` (the `check` lines) or `gh pr checks`
  - `state`, `mergedAt`, `mergeCommit`, `parents` from the same script. Until
    it prints `pass`, the merge is not a fact
  - the checks this change needed, and what they printed
- **Records.** The debrief, from [`session-debrief`](../session-debrief/SKILL.md):
  WC paths and commit SHAs, or `no record needed` with the reason it was
  decided. The branch's commits, hash and one line each, when the PR carries
  more than one concern.
- **The owned worktree** by exact path with `removed: true` or
  `removed: false`. When it was left in place, say which case it is: the
  removal condition did not stand, or the tree was retained on purpose — the
  user asked, or the tree is kept as evidence — with the reason.
- **What you did not do** — a separate list with a reason per item: left
  untouched, unfinished, or out of scope. Another session's dirty file or
  worktree goes here with the reason it was left alone. Name the exact range
  the unit checked and what it showed there — clean or dirty; a tree wider
  than that range is not called clean.
- **Runtime or deployed state** when it matters to the outcome and was
  measured — the turn need not have asked. Name the measurement and when it
  was taken; state that is irrelevant or was not measured stays out.

Close with the **Session disposition** block — three labelled lines, not an
offer. The measured waste at this seat is a session that finished and did not
say so (`맡은 것 끝났습니다 · 커밋 3건 · 넘길 것 1건(아래) · 닫으셔도 됩니다`):

- **Close now** — the unit is done, with the commit count and anything handed
  over; or the clause that is not done.
- **More in this session** — work this turn already named and still owed
  here; `none` when the unit is done.
- **To hand off** — named follow-ups that need a new session (a new PR, a new
  investigation, a design decision); list them, or write
  `opened: <handle> — told to <one line>` when this session opened the tab.

`이어서 …도 해두겠습니다` and `혹시 …를 더 볼까요?` are the two shapes this
block replaces. A hand-off is a statement in the block, never a question.

## Anti-patterns

| Don't | Why |
|-------|-----|
| Rewrite the done-condition into something smaller mid-session | The unit becomes whatever was easy |
| Treat the brief's prohibition as the user turn | At `e914dfb` a copied release-lane ban outranked the user |
| Stop because `## Unreleased` is empty | That means the named work is not in the version |
| End the report at an open PR | The old checklist said that, and sessions stopped there |
| Dump command output or a file list and call it the report | The reader is left to derive the meaning; the report is that meaning |
| Hold the PR for local polish | `grok fmt` / `grok clippy` are the longest polls and run on GitHub; commit → push → PR first |
| Say merged without `scripts/check-pr-merged.sh` printing `pass` | The sentence is not the fact |
| Report a number with no command behind it | A number without its source reads as measured |
| Start the next unit from the "not done" list | That sentence opens work the opening did not name |
| Offer another unit after you are done | The offer is the next task, and it lands in this session |
| Finish without the Session disposition block | The human has to ask "그래서 끝난 거야?", and the silence or the offer becomes the next task |
| Skip the debrief when the unit looks small | Its legal answers are records or `no record needed`; skipping loses both, and the reason |
| Clean up the worktree before the debrief | The debrief counts with `git -C "$WT"` and fails on a removed tree |
| Call a tree clean beyond the range the unit read | The claim outruns the check; the rest of the tree was not read |
| Ask "shall I record this to WC?" | The close authorizes the debrief's writes; the question is the round-trip the step removes |
| `git commit` with no path | A shared index takes another session's files with it |

## Done means

- [ ] The done-condition was written before editing, from `user-turn:` when a brief exists, and it was not swapped for a smaller one
- [ ] `scripts/check-session-close.sh brief` passed, or this session had no handoff brief
- [ ] Every check the report cites was run, and the report quotes what it printed
- [ ] The debrief ran while the worktree still existed — before the cleanup and before the report; the report names WC paths and SHAs, or `no record needed` with its reason
- [ ] `scripts/check-pr-merged.sh` printed `pass` (`MERGED`, `mergedAt`, `mergeCommit`, two parents, CI `/ required` passed), or that turn said to stop before the merge and the first line names that clause
- [ ] The first line says whether the done-condition holds, and names the clause if it does not
- [ ] The report says what changed and why, with observation separated from inference and a source on every measured sentence
- [ ] The owned worktree is named by exact path with `removed: true`/`false` — a tree kept in place says why — and the not-done list carries a reason per item; the checked range is named with what it showed, clean or dirty, and nothing wider is called clean
- [ ] What was not done is a separate list and was not opened as the next unit
- [ ] The report carries the Session disposition block (close now / more in this session / to hand off)
- [ ] Next units the opening already named have their own tab
