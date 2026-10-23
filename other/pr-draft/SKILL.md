---
name: pr-draft
description: Publish confirmed local changes as a monitored GitHub draft pull request. Use only when the user authorizes branch creation, scoped staging, commit, push, draft PR creation, and CI follow-up.
---

# Draft PR

Own end-to-end draft-PR publication after implementation, validation, and review are complete.

## Workflow

1. Confirm shipping authority, repository rules, remotes, current branch, exact scope, and completed validation and review evidence. Resolve the base branch from live remote evidence, such as `git ls-remote --symref <remote> HEAD`, unless the user names it.
2. Preserve unrelated staged, unstaged, and untracked work. Stop only when safe isolation is impossible or a scoped path is sensitive or unexpectedly generated.
3. Create a short branch when needed, stage explicit paths with `git add -- <paths>`, and review the staged path list and diff.
4. Run required checks when existing evidence does not cover the exact staged content.
5. Follow repository PR templates, title conventions, and required fields. Otherwise write concise evidence-based `Problem`, `Change`, `Tests`, and only necessary `Notes` sections.
6. Use `text-improve` on the completed title and body without changing verified facts, required template wording, or technical terms.
7. Use `change-cleanup-review` on the complete staged change and proposed PR presentation. Stop and report material cleanup findings unless the parent request separately authorizes repair. After an authorized repair, restage the exact scope and rerun invalidated checks and prose improvement.
8. Commit using repository conventions and push with an upstream when needed.
9. Check whether a pull request already exists for the branch with `gh pr view --json url,isDraft`; if one exists, update it instead of opening another. Otherwise run `gh pr create --draft --base <base> --title <title> --body-file <file>`. Monitor the checks for the pushed commit with `gh pr checks <number> --watch --fail-fast` under the host's command timeout.
10. Diagnose failures from logs. Route behavior changes through `behavior-implement` and `test-design`, and specialist failures through their owning workflow; verify, rerun `change-cleanup-review` when corrections materially move the change, then commit and push only scoped corrections.
11. Stop when checks pass, the user permits cancellation, a concrete external blocker prevents progress, or three fix cycles for the same failing check have not fixed it.

Do not rewrite history, force-push, merge, mark ready, release, weaken tests, disable validation, expose secrets, or override repository PR conventions.

Finish with the draft PR URL, commits, checks, final CI state, and blockers.
