---
name: pr-demo
description: >-
  Starts a pull request's branch on the project's demo site, in its own worktree with its own
  copy of the demo data, and hands over the address, where the login lives, and a short
  click-through list of what to try. Use when someone wants to try a PR or branch in the
  backoffice themselves before approving or merging it.
user-invocable: true
argument-hint: [PR number, PR URL, or branch | leave blank for the current branch]
---

# Try a pull request on the demo site

A good PR description and screenshots show what changed. Clicking through it yourself shows
how it feels: the empty states, the odd input, the screen next door. This skill gets the
branch running on the demo site with data in it, then gets out of the way.

It never changes code, commits, pushes, or comments on the PR.

## Scope

- IN: one PR or branch, started on the project's demo site, with a click-through list.
- OUT: reviewing the code (`pr-review` for an outside PR, `reviewer` for your own task);
  fixing what you find (`quick-fix`, or the plan's `feature-build`); a project with no demo
  site (say so, and point at `project-init`).

## Argument

`$ARGUMENTS` is a PR number or URL, or a branch name. Empty means the current branch.

## Workflow

1. **Find the branch.** For a PR, `gh pr view <number> --json
   title,body,author,headRefName,baseRefName,files`. Note whether the author is on the core
   team: an outside PR gets step 3 before anything builds.

2. **Find or make a worktree for it.** `git worktree list` shows whether the branch is
   already checked out somewhere.
   - In a linked worktree: use it as it is, with the demo data already in it.
   - Not checked out anywhere: make a worktree for it, named after the branch, and let the
     project's `WorktreeCreate` hook copy in what it copies (`git-workflow` owns that rule).
     For a PR from a fork, fetch it first (`gh pr checkout <number>` inside the new
     worktree). Remember you made it: step 7 removes it.
   - In the main checkout: the demo data there is the original, not a copy. Any migration on
     the branch, and anything clicked during the demo, changes it for every branch after.
     Ask before starting the site there, and offer a worktree with a copy instead.

3. **For an outside PR, read what would run before building it.** Do `pr-review`'s step 2
   scan (build scripts, package sources, `postinstall` entries, workflows, binaries) on the
   diff before `dotnet build` or `npm install` touch the branch. Flag anything it finds and
   wait for a yes.

4. **Check the demo data belongs to this worktree.** The site's database must live inside
   the worktree (such as SQLite under the site folder), as must its media. A connection
   string to a shared server means the demo writes to data other branches use: ask first.
   No demo data at all: the site's own install runs on first start, which is fine.

5. **Start the site.** Use the start command in `CLAUDE.md`'s "Build & test", run in the
   background from the worktree. The port comes from `git wdp-port`, never a fixed one.
   Wait until the backoffice answers, then log in once to check it works. If the build or
   start fails, stop and report it: a demo that won't start is a finding about the PR.

6. **Make sure the change has something to show.** With a plan folder, start from the
   "Demo setup" notes in `BUILD-LOG.md`. Set up what a note names exactly as written (the
   same tags, values and settings) so the result it describes still holds; anything you add
   goes beside it, never into it. Otherwise read the diff for what it needs in the
   site: a document type using a new property editor, content for a new dashboard to list,
   a setting turned on. If the demo data doesn't have it, add what shows the change, through
   the backoffice or the Management API, in this worktree's copy only. List what you added.

   **Make it look like a real site.** Write what an editor of this site would really write:
   real-sounding titles, names and text that match the demo's existing content and
   languages; a mix of lengths, including one long enough to wrap; the characters real
   content has (an accent, an ampersand, quotes); an optional field left empty. Add enough of
   it to reach paging, sorting or an empty state when the change has one, and write out every
   item: never "add more until there are 12" for the user to finish. Never "Test 1",
   "foo" or lorem ipsum: placeholder data hides the layout and edge-case problems a
   click-through is meant to find.

7. **Hand over.** Give:
   - The backoffice address, with the worktree's port.
   - Where the login lives (the file or environment variable), not the password itself.
   - What you added in step 6.
   - The click-through list: each item a click path and what should happen
     ("Settings › Tag filters › add `internal-` as a prefix › the cloud on the home page drops
     the "internal-notes" tag"). Take it from the plan folder when the branch has one (`SPEC.md`,
     `STORIES.md`, and the click paths in `BUILD-LOG.md`), otherwise from the PR's
     description (its "Where to find it" or "How to verify", when `pr-describe` wrote it). Include the edge cases the spec or PR names, and the screens next to the
     change that it could have broken.

   When the user says they're done: stop the site. Remove a worktree this skill made, unless
   it has changes the user made in it; then ask. Leave a worktree that already existed.

## Hand off

One line: the address, the branch, and whether the worktree was made for this demo. If
another skill started this one, return that line and stop. That skill decides what runs next.
Otherwise, if the user found a problem, offer the fix route that fits its size.
