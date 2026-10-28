---
name: ship
disable-model-invocation: true
description: "Takes work that is already implemented and committed on a branch and ships it: runs the repo's ship gates off receipts, pushes, opens a draft pull request, moves the board to in review, and removes the worktree. Use when the code exists and the task is to get it reviewable, or on /ship, and not when anything still needs writing."
---

# ship: committed work to a draft pull request

The tail of the funnel, on its own. Use it when the work already exists: you implemented
by hand, or a task run stopped after the gate, or a branch has been sitting for a day.

If anything still needs writing, this is the wrong skill. Use the task funnel, which has
triage, a spec and a review in front of this.

Input: nothing, or an issue number. Empty means the current branch.

If `kit` is not on PATH or cannot run, every `kit` below means
`${CLAUDE_PLUGIN_ROOT}/scripts/kit`, written out in each command.

## Stage 0 · Is this shippable

```
kit doctor
git status --short
git log --oneline <base>..HEAD
```

Stop and report, without shipping, on any of:

- **Uncommitted changes.** The review diffs commits, so uncommitted work is invisible.
  Commit it or say why it is excluded.
- **No commits ahead of the base.** There is nothing to ship.
- **A commit that does not follow the repo's convention.** `kit config get .docs.commits`
  names the document. Fix the message before the pull request quotes it.
- **A comment in the diff that is not a why.** At most two lines, and no ticket key,
  pull request number, date or count. `kit comments` finds them in the lines the branch
  adds; fix them before the pull request quotes the diff.
- **No review has happened.** Ask before shipping unreviewed work; `kit review`
  is minutes and a defect found here costs a round instead of a revert. If the user says
  ship anyway, say in the pull request body that it went out unreviewed.

## Stage 1 · Gates, off receipts

```
kit gate ship
```

Gates whose receipt already covers this exact tree are skipped and say so. The tree SHA
includes untracked files, so any edit at all invalidates it. That is the difference
between skipping a check and proving it was already paid.

A red gate stops here. `kit gate` prints a `flake` line when the failing file is on the
repo's quarantine list and whether this branch's diff can even reach it; a red gate in a
file the diff never touched is not a reason to stop, and it is not a reason to change code
either. Re-run that file alone.

## Stage 2 · Push

The repo's pre-push hook runs its own checks. The fix for a red hook is the failing check,
never `--no-verify`, and the plugin's `protect-tests` hook refuses it anyway.

## Stage 3 · The pull request

Open it exactly as the repo's pipeline document says. That document, not this skill, owns
the base branch, the draft state and the issue reference.

Fill the repo's template honestly, which means four specific things:

1. **A check is ticked only if it ran.** An unticked box is information; a ticked box that
   did not run is a lie with a green mark next to it.
2. **Answer the surfaces question in prose**, even when the answer is nothing. A sentence
   beats a box, because the box is what gets ticked without being read.
3. **Review findings go in the body as a table**, one row each with what the verifier
   said and the decision: fixed with the sha, dropped, or the issue that owns it. A
   finding nobody verified is a row marked so, not a blocker and not nothing.
4. **The body has a budget, and it is measured.** Write it to a file and run
   `kit pr-body <file>` before `gh pr create`: at most **2000 characters of prose** and
   **600 per section**, counting what you added rather than the template, its tables, its
   checkboxes or a fenced block. Over budget it exits 3 and prints the sections by size.

Cut, do not relocate. The body is the only thing a human reads before deciding whether to
review the diff, so length there is spent out of the reviewer's attention rather than out
of nothing. What does not fit is left out, not moved into a pull request comment: a comment
under the body is a second body, read by the same person, after they already decided. A
product decision goes in the issue, and why a non-obvious line exists goes in the code
beside it. Measured on 2026-08-17: one body ran to 11902 characters of prose across 9
sections, 7 of them over the cap, in front of a 163-line source diff.

What the body owes the reader and nothing more: what changed and why, what to check, and
what is knowingly left out and who owns it. One body per pull request: to change it later,
rewrite the file and `gh api repos/{owner}/{repo}/pulls/<n> -X PATCH -F body=@<file>`,
which the hook measures, rather than adding a comment that amends it.

## Stage 4 · Board and teardown

```
kit board in_review --issue <issue>
kit worktree gc --yes
```

The board move goes after the pull request URL exists. Never `done`: this does not merge,
and the tracker's own automation owns that column.

`gc` removes only what it can prove is finished, which now includes an open pull request
sitting at exactly this head, since everything is then on the remote and the branch
survives removal. It keeps the rest and prints why, including a worktree with nothing of
its own on it, which cannot be told apart from one another session just created.
`rm <issue>` was the step here until 0.3.0 and could not succeed once the pull request
existed.
`gc --dry-run` first if you want to see the verdicts without acting.

## Stage 5 · Report

At most 600 characters of prose, roughly 95 words: what shipped, the gate result including
what was skipped by receipt, the pull request link, and what was left out. Never declare
done without the numbers, and name a gate that stopped you as such.

Then `kit context`, because a ship is a boundary. It prints HOLD, AT THE NEXT BOUNDARY,
NOW or LATE off how full the window is, and anything but HOLD belongs in the report as
one clause. Measured across 16 sessions: 16% of the spend went to requests that reread
nothing from cache and wrote a whole prefix back, at US$ 2.62 each against US$ 0.20 for
a normal one, so a boundary passed without compacting is the cheapest saving there is
to skip. And whatever it says, compact before a long pause.

Characters, not lines, because a paragraph counts as one line in the source and four in the
terminal. 100 characters is about one rendered line.
