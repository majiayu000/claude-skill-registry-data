---
name: resolving-merge-conflicts
description: Resolve an in-progress git merge or rebase conflict. Use when a merge, rebase, or cherry-pick stops on conflicts.
---

1. **See the current state** of the merge/rebase. Check `git status`, the git history of both sides, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs (`gh pr view`), check the original issues/tickets (PR bodies reference them with the `TRACKER_ISSUE_PREFIX` from `.env`).

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

4. **Regenerate, don't hand-merge.** Conflict markers in generated files are never resolved by hand:
   - Lockfiles (`package-lock.json`, `yarn.lock`, `poetry.lock`, `uv.lock`, `Cargo.lock`, `go.sum`, ...): merge the manifest first, take either side of the lockfile wholesale, then regenerate it with the project's package manager (`INSTALL_CMD` in `.claude/project.env` usually does it).
   - Generated migrations and their metadata (journals, snapshots): drop this branch's generated migration, re-run the migration generator against the merged schema, then format the output with `FORMAT_FIX_CMD`.
   - Any other generated artifact (paths matching `GENERATED_PATHS_REGEX` in `.claude/project.env`: codegen stubs, generated API references, schema diagrams): re-run its generator against the merged sources; never edit the output.

5. **Run the automated checks** and fix anything the merge broke. Formatting, lint, and typechecking run automatically via the Stop hook; run the tests yourself (`TEST_CMD` in `.claude/project.env`, scoped to the affected area when the runner allows). The pre-commit hook (`scripts/pre-commit`) runs the project's checks and tests; failures that already exist on the base branch are not the merge's fault, and `--no-verify` is acceptable only for those.

6. **Finish the merge/rebase.** Stage everything and commit. If rebasing, continue the rebase process (`git rebase --continue`) until all commits are rebased.
