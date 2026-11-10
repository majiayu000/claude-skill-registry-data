---
name: pr
description: Open a pull request for the current branch after scripts/verify.sh is green. Use when the user says "open a PR", "/pr", or a spec's work is ready to ship.
---

# /pr — open a pull request for Iron Pipeline

Trunk (`main`) is always green. Agents open PRs; they never merge, tag, or publish (ADR 0003, Agentic CD constraint 7).

## Steps

1. **Branch check.** Refuse if on `main`; work happens on a spec branch (`NNNN-<name>`) or worktree.
2. **Verify locally** — leave `.claude/CLAUDE.md` (repowise block) unstaged during the work. Run the same command CI runs:
   ```bash
   scripts/verify.sh
   ```
   It runs `dotnet format --verify-no-changes`, `dotnet build -c Release` (warnings as errors), `dotnet test`, the engine-boundary, dependencies, spec-id, determinism, asset-manifest and stale-reference checks, and `scripts/check-budget.sh`. If it fails, fix and re-run; do not open the PR red.
   Then, if `.claude/CLAUDE.md` is modified, stage it by name and commit it alone: `git add .claude/CLAUDE.md && git commit -m "chore(repowise): refresh index"` (`check-budget.sh` does not count it).
3. **Code review — a separate step before `gh pr create`.** Run `/dev-team:code-review` once all scenarios are green, before cleanup commits, not after the budget is spent. The PR gate file (`.claude/memory/.pr-review-passed`) is written in its own Bash call, because `pre_pr_review.py` runs before the command executes. Fix errors in their own commit (amend only unpushed commits). Planned-size PRs: run the project review agents on the diff: `review-determinism`, `review-engine-boundary`, plus `review-content-schema` / `review-save-and-replay-compat` / `review-sim-performance` / `review-asset-pipeline` as the diff warrants. Small-size specs skip these agents (root `CLAUDE.md`, "Size the task"). Any PR touching CLAUDE.md, ADRs, skills, agents or templates also runs `review-process-drift`.
3b. **Status.** In the PR's final commit, set `Status: implemented` in `docs/specs/NNNN-*.md` and `features/NNNN-*.feature`.
4. **Playtest checklist** for planned-size, player-facing PRs: `/playtest-checklist NNNN` once reviews pass.
5. **Push and open:**
   ```bash
   git push -u origin HEAD
   gh pr create --fill --base main
   ```
   PR body: follow `.github/PULL_REQUEST_TEMPLATE.md` — link the Spec (`docs/specs/NNNN-*.md`) and Features (`features/NNNN-*.feature`), list the scenarios covered (`S<NN>_...` tests), budget used, Decisions made at the build gate, Deferred (as issue links) and Not covered; note any save/replay version bump. End the body with the attribution line required by the session.
5a. **Done-when gate.** The body's "Done-when criteria from the brief/Spec" section lists every item of the brief's "Done when" list (or the Spec's ACs), each checked only if it was met and verified. Refuse to open the PR with any unchecked item unless the title starts with `[incomplete]` and the body says which items are open and why, and asks the human to decide. Never check an item you did not verify.
5b. **Fix PRs.** If the title or labels say fix / bug / incident, the body's "If this fixes something that went wrong" section must have Symptom, Cause, Cause fix and Check/Verified filled (`root-cause-fix` skill). Refuse to open the PR otherwise.
6. Report the PR URL. Do not merge.
