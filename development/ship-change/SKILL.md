---
name: ship-change
description: Take a finished Lodestone change from a branch to main - review, commit, push, open a pull request, get CI green and squash-merge. Use whenever work is ready to land.
---

# Ship a Change

main is protected and keeps a linear history: every change lands through a pull request, after CI passes, as a squash merge - the only merge method the repository allows (see `AGENTS.md` and `docs/Testing.md#ci`).

1. **Branch** - work on a descriptive branch (`milestone-2-window`, `fix-log-flush`), never on main.
2. **Verify locally** - follow the `build-and-test` skill: the debug, release and dist workflows, the format check and clang-tidy all pass.
3. **Update the docs** - `docs/Milestones.md` (tick finished items, update Current State), any new decision in `docs/Decisions/` (and its index), `AGENTS.md` and the skills if commands or layout changed, and `THIRD_PARTY_LICENSES.md` for new dependencies.
4. **Review** - review the full diff (`git diff main...HEAD`, plus uncommitted changes) with `/code-review`. Fix every real finding, and check the change against `docs/CodeStyle.md`.
5. **Commit** - a clear message explaining what changed and why. No AI attribution lines (no `Co-Authored-By: Claude`, no "Generated with Claude Code").
6. **Push and open the pull request** - `git push -u origin <branch>`, then `gh pr create --base main` with a summary of the change and how it was tested.
7. **CI** - wait for every job. The `CI passed` job sums them up. If a job fails, read its log (`gh run view <id> --log-failed`), fix the cause, and push again. A failed rendering test uploads its images as an artifact (`gh run download <id>`). Never weaken a test or a check to get green.
8. **Merge** - once CI is green: `gh pr merge <number> --squash --delete-branch`. Then update the local main: `git switch main && git pull`.
