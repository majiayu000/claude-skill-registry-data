---
name: change-backport
description: >-
  Ports a change already merged on one version line of a package to another (`vN/dev` or
  `support/N.x`). Checks it belongs there, applies it in a worktree, builds, tests and
  reviews it, and opens a draft PR. Use when asked to port, backport or forward-port a fix
  or feature, or apply a change to the other version.
user-invocable: true
argument-hint: <commit SHA | PR number | branch> [target line, e.g. v17]
---

# change-backport

Take one change that already exists on one line and land it on another, as its own reviewed
PR. A port is a small, known change, so this skill makes the edit itself, the way `quick-fix`
does, and still sends the result through the `reviewer`.

## Scope

- IN: a change with a concrete source (a commit, a merged PR, or a branch) moving to one other
  line. Ports in either direction.
- OUT: deciding the branch model or which lines exist. That's `git-workflow`'s "Umbraco
  packages and version tracking" section. Writing the change in the first place: that's
  `quick-fix` or the `feature-*` pipeline on the source line. A change that has to be
  redesigned for the target line (a different extension point, an API that doesn't exist
  there) is a new change: stop and suggest `feature-explore` on the target line. Moving the
  whole package to a new CMS major is `major-upgrade`.

## Argument

`$ARGUMENTS` names the source change and, optionally, the target line. If the source is only
a description ("the null check fix from last week"), find the commit or PR and confirm it with
the user. Don't re-derive a fix from a description when a real commit exists. If no target is
given and the project supports exactly two lines, the target is the other one; otherwise ask.

## Preflight

1. **Find the lines.** Read `CLAUDE.md` for the lines the project supports, each line's
   integration branch, and each line's phase (active, security fixes only, or end of life). If
   `CLAUDE.md` doesn't say, list the remote branches and ask; don't infer a phase from a
   branch name.
2. **Check the target should get it.**
   - Active: features and fixes.
   - Security fixes only: a security fix, nothing else.
   - End of life: nothing, unless the user asks for it anyway.

   Then check for a reason not to port: the source commit body or PR saying the change only
   applies to one major (as `git-workflow` asks commits to say), or a project memory note. If
   the change touches something that differs between the lines and you can't tell whether it
   applies, ask.
3. **Check it isn't already there.** Search the target line's history for the source PR
   number, the commit subject, and the changed lines. A partial earlier port means you port
   only the rest.
4. **Read the whole change.** For a PR, list every commit in it, not only the last one. Note
   any database migration and any public signature change.

## Steps

1. **Cut a fresh worktree on the target line.** Create it from the main checkout, never from
   inside another worktree. Use the same mechanism `feature-build` uses (the project's
   `WorktreeCreate` hook or Claude Code's native worktree), named for the change and the
   target line, following `git-workflow`'s branch naming. Then confirm `pwd`, the branch, and
   that its base is the target line's integration branch (`git log --oneline -3`). If the base
   is wrong, stop and fix it before applying anything. Porting onto the wrong base is worse
   than not porting.
2. **Apply the change.**
   - Clean commits: `git cherry-pick -x <sha>...` in their original order. `-x` records the
     source SHA in each message.
   - Conflicts: read each one and resolve it by hand. Never take a side wholesale with
     `--ours` or `--theirs`.
   - Code that differs on the target line (a renamed type, an API the older CMS major doesn't
     have): apply the diff by hand and adapt it to the target line's code. Load the stack
     skills the change touches (`umbraco-package-conventions`, `ef-core-data`,
     `umbraco-backoffice-conventions`, and so on), the same way `quick-fix` does.
   - **A database migration:** copy the migration files, never generate them again on the
     target line. See `ef-core-data`'s "Porting a migration to another version line".
   - **An `[Obsolete]` member:** keep the same removal version as the source line, per
     `umbraco-package-conventions`.
3. **Verify on the target line.** Run the build, the tests, and the lint/format check from
   `CLAUDE.md` for the products the change touches. Then smoke it through the real entry point
   on the target line's demo site, in the order `feature-build`'s "Smoke the real entry point"
   step gives. Passing on the source line proves nothing here. If the site can't run, say "not
   verified end to end" and why in the hand-off.
4. **Review.** Dispatch one `reviewer` subagent (Agent tool, `subagent_type: reviewer`)
   against the port's diff. Give it the source change as the task, and say what you adapted
   and why, so it can check the adaptation and not only the code. Fix Critical and Important
   findings and review again until `PASS`, giving each re-review the round's diff and
   previous findings, as in `feature-build`'s "Recurse" step. If it still fails after three
   rounds, stop and report the findings.
5. **Commit.** Keep the source commit's Conventional Commits type and scope, and its message
   where it still describes the change. Add `Port of <source PR or SHA> to <target line>.` to
   the body.
6. **Open a draft PR.** Ask before pushing. Then open the PR as a draft against the target
   line's integration branch, with `pr-describe` writing the body, per `git-workflow`. The body
   links the source PR, and says what was adapted. Draft the matching one-line link for the
   source PR ("Ported to <target line> in #<n>"). Never merge, however green the checks are.

## Hand off

The port PR's link, what was verified (build, tests, end-to-end smoke, or "not verified end to
end" and why), the review verdict, what was adapted, and the drafted link for the source PR.

- **If another skill started this one**, return those and stop. That skill decides what runs
  next.
- **Otherwise**, post the source PR link on the user's yes, and offer to remove the worktree
  once the port PR merges.

## Rules

- One target line per run, one worktree per target line. Porting to two lines is two runs.
- Never merge, and never push to an integration branch directly.
- Never skip a line's phase rule without the user asking.
- Never port a change whose source PR is still open. Its review may still change it.
