---
name: pr
description: "Opens or updates a pull request with a Conventional Commits title, a body in What, Why, Verification and Risk, issue link and labels. Use when a branch is ready for review or an existing pull request's description no longer matches the work."
---

# Pull request

Open a pull request a reviewer can judge without reading the whole diff first.

## When to use

- A branch is ready for review, or ready as a draft.
- An existing pull request's description no longer matches the work.

## Steps

1. Read the state: current branch, upstream, `git log <base>..HEAD`, `git status`. Nothing
   uncommitted stays behind unexplained.
2. Push the branch if it is not yet on the remote.
3. Run the repository's verify command and report the real result. Never claim a green check
   that was not seen.
4. Derive the title from the commits as one Conventional Commits line, the summary a reviewer
   reads before the diff. The merge is a merge commit by default, so the atomic commits
   underneath stay in history on their own.
5. Write the body in four sections: What, Why, Verification, Risk, each a short list of bullets.
   The Verification section opens with `Verified on <short sha>.`, then lists every verify
   target on its own line, passed or not. Link an issue with `Closes #123`.
6. Set labels: the type label matching the linked issue's type, and a stack label for every
   config `stacks` glob the changed files match.
7. Create it with `gh pr create`, or update an existing one with `gh pr edit`. Open as draft
   unless config `pr.draft` is `false`. Request no human reviewer unless config says otherwise.
   A stacked pull request has another branch as base. GitHub links `Closes #123` only against
   the default branch, so comment the pull request number on the issue, and edit the body once
   the base has moved to the default branch.
8. Mark it ready once the ready condition in Guardrails holds, or the user asks for it
   directly.
9. Report the URL, the merge strategy and what a reviewer should look at first.

## Guardrails

- The body never carries an attribution footer or a session link.
- Never claim a check ran green without having seen it run.
- A target that did not run is named in the Verification list with its reason, in the same
  list as the targets that passed. Never only in prose after the list.
- After a rework round moves the head commit, update the Verification section's SHA and
  claims to match, or delete the section. A stale section is worse than none.
- A label missing on the tracker is reported, never created.
- Opening a draft or ready pull request needs no confirmation. Merging it does, and belongs to
  a different skill.
- Ready condition: every blocker and should finding resolved, the verify command and the
  pipeline green, the body matching the diff. Holds with or without an `approve` verdict.
- A pull request already ready never goes back to draft.
- A review fix goes into the commit it corrects when that commit is unambiguous: `git commit
  --fixup <sha>`, `git rebase --autosquash` onto the base, push with `--force-with-lease`. Only
  on the own branch, only before the merge.
- The target commit is not clear, or the fix changes something of its own: a new commit instead.
  Never fold a fix into the last commit or an arbitrary one.
- An unfixed security vulnerability in a public repository gets no exploit detail in a pull
  request description: see the baseline's security vulnerability rule.

## Config

- `pr.base`: base branch. Default: the repository default branch.
- `pr.draft`: open as draft. Default: `true`.
- `stacks`: map of label to path globs, used to set a stack label. Default: none.
- `types`: type labels an issue may carry, one of which is copied onto the pull request. Default:
  `bug`, `feature`, `improvement`, `documentation`, `security`.
- `verify`: command that proves the change is good. Default: `task check`.

## References

- `git-conventions` for title, body and draft conventions.
- `review` for reviewing a pull request once it is open.
