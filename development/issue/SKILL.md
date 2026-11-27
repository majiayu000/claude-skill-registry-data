---
name: issue
description: Take a bug report (a Discord screenshot, a user's message, a GitHub issue) from a reproduction to a GitHub issue, a fix on its own branch, and a ship to main once the user says to ship. Use whenever the user hands over a bug report or asks to work on an issue.
---

A bug goes from a report to `main` in four steps, in the session's own
worktree. Arguments: `$ARGUMENTS` (an issue number, or nothing for a report
in the conversation). Pass `gh` the `origin` repository (`--repo
<owner>/<repo>`, from `git remote get-url origin`): the checkout has more
than one remote.

## 1. Reproduce, then file the issue

Skip the filing when the issue exists: read it (`gh issue view <n>`) and
check that its reproduction still fails.

1. Get the case down to data. For a game, fetch its PGN
   (`/game/export/<id>`, with a browser's user agent: see "Crawlers get a
   404" in `AGENTS.md`) and play it to the position, including the moves
   played after the game if the report shows a variation. Read the board in
   the screenshot to tell which moves they were.
2. Compute what you need (FENs, the move's UCI) with the project's own code,
   in a throwaway test beside the module (`zz-*.test.ts`, deleted right
   after), and run the function at fault on it. The bug is confirmed when
   its output is wrong: say so to the user before filing.
3. Find the cause in the code, not only the case: which helper gets it
   wrong, and who else calls it.
4. File it (T3's `create_issue`, else `gh issue create`), in English, with
   the `🐞 Bug` label:
   - what goes wrong, in a sentence or two, and a link to the game or page;
   - steps to reproduce on lichess.org, then the data (FEN before, the move,
     FEN after);
   - expected and actual;
   - the cause, with the files and functions;
   - a vitest case that fails on `main` today, ready to paste;
   - how to fix it, and what it may change (legacy fixtures, other callers).

   Leave out the reporter's personal details; a public game's link is fine.

5. Link it to the thread (T3's `link_issue`) and give the user its URL.

## 2. A branch for the fix

Rename the worktree's branch after the issue:
`git branch -m t3/issue-<n>-<what>` (`t3/issue-39-pinned-sacrifice`). The
fix lives there until it ships; nothing is committed before the user says to
ship.

## 3. Fix, as a draft

1. Fix the cause where it lives, for the whole family of cases, to the
   quality bar of `AGENTS.md`. Prefer a fix in the shared helper over a patch
   in one caller, then go over the other callers.
2. Run the area's tests. A legacy fixture (`fixtures/legacy*.json`) that
   changes is never regenerated: look at each changed entry, and edit by hand
   only the ones the old code got wrong, naming each in the commit.
3. `pnpm check:fast`, rebase onto `origin/main`, then `pnpm preview` with a
   `--url` to the page that shows the case (see "How a change goes").
4. Tell the user exactly how to reproduce it in Chrome: the page, the moves
   to play from where it opens, what they saw before and should see now.
5. If they want to compare with `main`, build it from a throwaway worktree
   and leave yours alone:

   ```sh
   git worktree add --detach /tmp/ln-issue<n>-main origin/main
   cd /tmp/ln-issue<n>-main && pnpm install --frozen-lockfile
   pnpm preview --take --name "<n>, sans le fix" --url <page> --thread <id>
   git worktree remove --force /tmp/ln-issue<n>-main
   ```

   Then preview the fix again from your worktree when they come back to it.

## 4. Ship, when the user says so ("livre", "ship")

1. Write the tests: the issue's case first, then the rest of the family
   (each way the fix changes the answer, and a case it must leave alone).
2. See them fail without the fix, without touching the stash the worktrees
   share:

   ```sh
   git diff <fixed files> > /tmp/ln-issue<n>.patch && git checkout <fixed files>
   pnpm vitest run <test files>   # they fail
   git apply /tmp/ln-issue<n>.patch && rm /tmp/ln-issue<n>.patch
   ```

3. `pnpm check`, then ship as `AGENTS.md`'s "Before shipping" and
   "Shipping" say: the other sessions, `pnpm turn take ship`, the commit, a
   rebase onto `origin/main`, `git push origin HEAD:main` (a fast-forward:
   no PR, no merge commit), the main checkout pulled and previewed,
   `pnpm turn release ship`.
4. The commit's body explains the cause, names any legacy entry it changes,
   and ends with `Fixes #<n>`: the push to `main` closes the issue. Check
   that it did (`gh issue view <n> --json state`).
5. Remove the throwaway files and worktrees, then tell the user what
   shipped, the tests, and any step skipped and why.
