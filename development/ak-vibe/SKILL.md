---
name: ak-vibe
description: "Run the vibe pipeline to PR readiness: worktree, plan, cook/fix, code-review, ship, review-pr; --both ships beta then stable, --ultra verifies, --advice uses kongming."
when_to_use: "Invoke to take a GitHub issue or request through shipping, merge and CI convergence."
category: workflow
keywords: [vibe, pipeline, autonomous, ship, worktree, plan, cook, fix, review-pr, ci, advice, kongming, ultra, debug, research, test, docs]
argument-hint: "[--ship] [--beta] [--both] [--advice] [--ultra] <github-issue-url | feature request>"
license: Proprietary
metadata:
  author: agentkit
  version: "1.5.0"
---

# Vibe Pipeline

Run a full autonomous product-development pipeline from request intake to PR
readiness, with optional merge and post-merge CI convergence.

This skill orchestrates across `/ak-worktree`, `/ak-plan`, `/ak-cook`, `/ak-fix`,
`/ak-code-review`, `/ak-ship`, and `/ak-review-pr`, integrating `/ak-debug`,
`/ak-research`, `/ak-test`, and `/ak-docs` as needed. It does NOT bypass those
skills' approval gates, tests, code-review blockers, branch protections, or
security policies.

## Inputs

Flags:

| Flag | Effect |
| --- | --- |
| `--beta` | Ship to beta/dev target via `/ak-ship beta`; final ready label is `ready to ship beta`. |
| `--ship` | After review/fix/reply, merge the PR and watch/fix CI until success or true external blocker. |
| `--both` | Dual-stage ship: run the full beta stage first (ship, review, merge, watch CI until green), then the stable stage (ship official, review, merge, watch CI until green). Implies `--ship` for both stages; supersedes `--beta`. |
| `--advice` | Run the whole pipeline under `kongming` advisory supervision, authoring plans formatted for handover to lower-capability executor models with verify-fail escalation (see Advisory supervision). Composes with any ship mode. |
| `--ultra` | Run `/ak-plan` and `/ak-code-review` in ultra verifier mode (best-of-5 candidate pass; opt-in only, significantly increases run cost/time). |
| no `--beta` | Ship stable via `/ak-ship official`; final ready label is `ready to ship stable`. |
| no `--ship` | Stop after PR is reviewed, fixed, replied, and labeled ready. |

Rows describe individual flags in isolation; when `--both` is present, mode
resolution below wins. Mode resolution: `--both` > `--beta` > default stable.
If `--both` and `--beta` are given together, warn once and proceed in `both`
mode. `--advice` and `--ultra` are orthogonal to ship mode and compose with all of them.
`--ultra` activates ultra verifier mode for `/ak-plan` and `/ak-code-review` only (vibe deliberately scopes `--ultra` to plan and code-review).
When `--advice` is present, forward `--advice` to all supporting skills that accept it (`/ak-plan`, `/ak-cook`, `/ak-fix`, `/ak-code-review`, `/ak-ship`, `/ak-review-pr`, `/ak-test`; forward to `/ak-docs` only when its installed mode supports the accepted advisory contract).

## Evidence and continuation

Maintain one controller ledger of accepted scope, source/plan/diff revision, completed checks, findings, authority and outstanding decisions. Pass downstream only its needed context plus evidence pointers. Reuse valid results for unchanged inputs; invalidate them after relevant edits or runtime changes. Continue authorized work through inspection, repairs and PR readiness. Keep exact-head and optional merge/CI gates.

## Batch-landing repositories

When the repository's own instructions (`CLAUDE.md`, `AGENTS.md`, or its
contributing or workflow docs) declare a batch-landing owner (a merge train,
landing bot, or scheduled routine) that lands PRs instead of per-PR CI and
author merges, `/ak-ship` opens the PR ready for review with the local
verification evidence those instructions name, then stops. Vibe follows the
same boundary:

- Step 11 still reviews, fixes, and replies on the diff, but local verification
  evidence replaces PR checks; do not wait for checks that will not run.
- Step 12 applies the ready label as usual.
- Step 13 does not run, even with `--ship` or `--both`: do not enable
  auto-merge, merge, or watch target-branch CI. Report merge as delegated to
  the landing owner, and with `--both` report the stable stage as
  `pending beta merge`.

## Subagent orchestration

The vibe controller owns interpretation, taste, and every gate. Delegate to
subagents to accelerate work and provide fresh, unbiased context (planning fanout,
code-review fanout, testing, advisory reviews).

For parallel implementation:
- **Disjoint file ownership:** partition files strictly before fanning out; concurrent subagents in the same worktree MUST NOT touch the same file, because overlapping writes clobber each other. For multi-file writes, prefer worktree-isolated subagents via `ak-orchestrate`.
- **Serialize shared files:** name one owner for shared schemas, exports, or configs.
- **Contracts up front:** freeze interfaces before fanout; delegates run independent focused checks within their owned scope; serialize shared build outputs and expensive whole-worktree suites at integration.
- **Fresh context:** use subagents for evaluation, review, and verification to eliminate self-grading bias.

Full orchestration protocol: `references/subagent-orchestration.md`.

## Advisory supervision (`--advice`)

When `--advice` is present, run the whole pipeline under `kongming`
supervision (`../ak-brainstorm/references/advisory-supervision.md` for identity
and model routing). Kongming returns counsel, never code; the main agent stays
responsible for every decision, edit, and gate. Plans created in step 4 follow
the handover contract in `../ak-plan/references/advice-handover-plan.md` (phases
decompose into step-by-step tasks with explicit success criteria and mechanical
verification for lower-capability models like Sonnet or Gemini Flash).

Spawn `kongming` at these checkpoints. A downstream advisory review can satisfy the same checkpoint when it covers the same scope, revision and question; record its receipt rather than repeating it. New failures or materially changed evidence require fresh counsel:

- **After each pipeline phase completes** — after investigation, after the plan gates, after
  implementation, after local code review, and after testing/docs. Pass the
  phase goal, what changed, and the evidence; ask for a go/no-go and the next
  risk to watch before continuing.
- **When stuck** — repeated failures, a blocked step, or contradictory evidence;
  pass everything already tried and the exact obstacle.
- **Before a high-stakes decision** — a design fork, a public-contract or
  security-sensitive change, or an irreversible action (including a promotion
  merge that sweeps unrelated work); get counsel first.
- **On verification failure** — if any verification step, test gate, or sanity
  check fails during implementation, STOP immediately. Do not self-reason or
  guess; spawn `kongming` with the exact command, output, and context before
  touching code again (see `../ak-plan/references/advice-handover-plan.md`).
- **After the PR is opened and CI is green** — this is the mandatory review
  gate described below.

**Mandatory post-PR review gate:** once the PR is opened and CI is green (after
PR review and final CI convergence), spawn `kongming` to review the
implementation and comment assessment plus next steps on the PR and source issue
(in `--both` mode, runs after both beta and stable PRs).

`--advice` adds supervision; it never bypasses approval gates, tests, review blockers, branch protections, or security policy.

## Pipeline

1. **Parse and analyze request**
   - Strip `--ship`, `--beta`, `--both`, `--advice`, and `--ultra` from arguments, then resolve ship mode (`both` > `beta` > stable). `--both` implies `--ship`.
   - If remaining input is a GitHub issue URL/number, treat that issue as the source of truth. Do not create a duplicate.
   - If remaining input is natural language, treat it as the feature request and create the GitHub issue after plan validation/red-team.
   - Resolve repo with `gh repo view --json nameWithOwner,defaultBranchRef`.
   - For GitHub issue URLs, parse `OWNER/REPO` from the URL and compare it with the current repo. If it differs, stop and ask the user to switch to the matching repo/worktree or provide an issue from the current repo.
   - For issue inputs, read the title, body, and comments with `gh issue view`. For natural-language inputs, use the text directly.
   - Extract concrete outcome, acceptance criteria, scope boundary, non-negotiable constraints, blockers, and likely touched surfaces.
   - Classify implementation route:
     - **Bugfix route** when the issue/request is a bug, regression, broken behavior, failing test/CI, production/staging incident, error log, or explicitly says fix/debug/repair.
     - **Feature route** for net-new capability, enhancement, refactor, or ambiguous product work.
   - **Technology detection:** if the request or issue mentions a specific library, framework, plugin, SDK, API, or service, mark for research in step 3.
   - Detect an existing plan in this order, verifying the resolved `plan.md` exists on disk before treating it as reusable: (1) a user-provided plan path; (2) for an issue input, the linked plan in the local index via `ak plan search --issue <n>` (plan state is files-first — the index resolves a plan by issue number without a GitHub link); (3) the current-plan pointer, then `ak plan resolve` (repo + branch); (4) an issue body/comment linking a `plans/.../plan.md`, or a matching plan already in the current worktree. Detection runs before worktree creation, so the pointer and `ak plan resolve` are often unset here — that is expected, not a failure. If `ak` is missing/errors, or `resolve` reports an ambiguity, present the candidates and fall through to the file/issue scan rather than treating it as "no plan". The issue-link/worktree scan stays first-class: a teammate-created plan may exist only as repo files plus an issue link, because the index is per-machine.
   - If any of those are ambiguous enough to change implementation, ask before worktree creation. Otherwise proceed and carry the extracted requirements into planning and issue updates.

2. **Create or reuse isolated worktree and branch**
   - If the current environment is already an isolated git worktree (`git rev-parse --git-common-dir` != `git rev-parse --git-dir`) on a dedicated feature branch (not on `main`, `master`, `dev`, `beta`, or `develop`), skip `/ak-worktree` and reuse the current worktree directly.
   - Otherwise, activate `/ak-worktree` to create an isolated worktree and branch.
   - Use a descriptive branch name derived from the issue/request.
   - If an existing clean feature worktree/branch already matches the request, reuse it and record why.
   - Never work directly on `main`, `master`, `dev`, `beta`, or `develop`.

3. **Pre-plan investigation (conditional)**
   - **Research (`/ak-research`):** if technology was detected in step 1, run `/ak-research "<tech topics>"` for latest docs, updates, best practices, and common issues; feed findings into planning.
   - **Debug (`/ak-debug`):** if on the bugfix route, run `/ak-debug "<error/failure + evidence>"` to prove root cause with concrete evidence (repro command, logs, call stack) — no guessing, no symptom patching. Feed confirmed root cause into `/ak-plan` and `/ak-fix`.
   - Evaluated deterministically; skip if predicate does not hold (see `references/pipeline-skill-integration.md`).

4. **Plan intake and gates**
   - If a valid existing `plan.md` was detected, set `plan.md` to its absolute path, reuse it, and skip `/ak-plan --tdd`.
   - If no valid plan exists, in the active worktree activate:
     ```bash
     /ak-plan --tdd "<source issue or feature request>" [--ultra] [--advice]
     ```
     Pass `--ultra` if set on vibe; pass `--advice` if set on vibe (authors the plan under `../ak-plan/references/advice-handover-plan.md`).
   - For newly created plans, capture the absolute `plan.md` path from `/ak-plan`.
   - Require evidence for both gates, even when the plan already existed:
     ```bash
     /ak-plan validate <plan.md>
     /ak-plan red-team <plan.md>
     ```
   - Before implementation, perform the whole-plan consistency sweep required by `/ak-plan`.
   - Do not proceed to implementation while validation failures, accepted red-team findings, or unresolved contradictions remain.

5. **Create or update GitHub issue**
   - Ensure labels exist:
     ```bash
     gh label list --json name --jq '.[].name' | grep -Fx "ready to cook" >/dev/null \
       || gh label create "ready to cook" --color "0E8A16" --description "Plan validated; ready for ak-cook or ak-fix"
     gh label list --json name --jq '.[].name' | grep -Fx "in progress" >/dev/null \
       || gh label create "in progress" --color "FBCA04" --description "Implementation is in progress"
     gh label list --json name --jq '.[].name' | grep -Fx "ready to ship stable" >/dev/null \
       || gh label create "ready to ship stable" --color "5319E7" --description "PR reviewed and ready for stable merge"
     gh label list --json name --jq '.[].name' | grep -Fx "ready to ship beta" >/dev/null \
       || gh label create "ready to ship beta" --color "1D76DB" --description "PR reviewed and ready for beta merge"
     ```
   - If label creation fails for anything other than an existing label, stop and report the exact `gh` error.
   - Compute relative plan link from repo root.
   - If source issue exists, update/comment on it. If input was natural language, create a new issue.
   - Issue update must include:
     - branch name
     - implementation route (`feature` via `/ak-cook` or `bugfix` via `/ak-fix`)
     - implementation summary
     - relative plan link
     - ship mode (`official`, `beta`, or `both`)
     - acceptance criteria from the plan
   - Add `ready to cook`; remove stale `ready to ship stable` and `ready to ship beta`.
   - Record the linkage in the plan index so later runs resolve this plan by issue number: `ak plan update --issue <issue-number>` (add `--root-comment-id <id>` when a tracking comment was posted). Follow the publish-safety protocol in the shared files-first plan-state reference for author-verification and idempotent projection.

6. **Implement or fix**
   - Before activating `/ak-cook` or `/ak-fix`, update the pipeline GitHub issue:
     ```bash
     gh issue edit <issue-number-or-url> --add-label "in progress" --remove-label "ready to cook"
     ```
   - If `ready to cook` is not currently on the issue, use `--add-label "in progress"` without `--remove-label`.
   - If the label update fails for any other reason, stop and report the exact `gh` error. Do not start implementation while the issue state still says `ready to cook`.
   - If the request is on the bugfix route, activate:
     ```bash
     /ak-fix --auto <plan.md> [--advice]
     ```
   - Pass the source issue/request, failure evidence, validated plan path, scope boundary, and acceptance criteria into `/ak-fix`.
   - If the request is on the feature route, activate:
     ```bash
     /ak-cook --tdd --auto <plan.md> [--advice]
     ```
   - Honor every hard gate in `/ak-cook`.
   - Honor every hard gate in `/ak-fix` on the bugfix route.
   - If implementation stops for user/business decision, update the GitHub issue with blocker details and stop.

7. **Review local implementation**
   - Activate:
     ```bash
     /ak-code-review --pending [--ultra] [--advice]
     ```
   - Fix Critical and Important findings before shipping. Re-run relevant validation after fixes.

8. **Quality and testing (conditional)**
   - Conditionally activate `/ak-test create|audit|optimize [--advice]` when observable behavior, boundaries, or invariants changed.
   - Skip when coverage from `/ak-cook --tdd` or `/ak-fix` is already honest and adequate. Strictly forbid valueless pass-only or tautological tests.
   - See `references/pipeline-skill-integration.md` for decision rules and anti-cheat constraints.

9. **Documentation sync (conditional & mode-aware)**
   - In `official` mode: skip in-repo `/ak-docs update` (owned by `/ak-ship official` in background to prevent write races); record docs impact in the PR.
   - In `beta` mode: run `/ak-docs update` when public contracts, APIs, or agent context changed (reuse accepted authorization and valid advisory evidence).
   - For official docs in an external repo (e.g. `bestagentkits/agentkit-docs`): search existing issues, then file or link a follow-up issue with the `ai-handle` label.
   - See `references/pipeline-skill-integration.md`.

10. **Ship PR**
    - Pass `--advice` if set on vibe.
    - If `--both` is present, start with the beta stage:
      ```bash
      /ak-ship beta
      ```
      The stable stage runs later, in step 13, only after beta merge and beta CI success.
    - Else if `--beta` is present:
      ```bash
      /ak-ship beta
      ```
    - Otherwise:
      ```bash
      /ak-ship official
      ```
    - Capture PR URL/number from `/ak-ship` output.
    - The ship skill finalizes a plan-backed change as part of its pipeline: it writes `status: completed` to the plan files before committing (so the finalized files ride the ship commit) and records `--linked-pr` after PR creation. The index `close` is deferred to merge (step 13) — no extra action here.

11. **Review/fix/reply PR**
    - Pass `--advice` if set on vibe.
    - Activate:
      ```bash
      /ak-review-pr <pr-url-or-number> --fix --reply
      ```
    - Do not continue until actionable findings are resolved or an external blocker is documented.
    - PR checks must be terminal and green unless the blocker is external and recorded. In a batch-landing repository, local verification evidence replaces PR checks (see Batch-landing repositories).
    - When `--advice` is present, after CI is terminal and green (in a batch-landing repository, after review/fix converges), run the mandatory post-PR review gate: spawn `kongming` to review the whole implementation and post its assessment plus concrete next steps as a comment on the PR and the source issue (see Advisory supervision).

12. **Apply ready label**
    - If beta mode: add `ready to ship beta`.
    - If both mode: add `ready to ship beta` now; `ready to ship stable` is added in step 13 when the stable-stage PR passes review.
    - Otherwise: add `ready to ship stable`.
    - Add the label to both the source issue and PR when possible.
    - Remove `ready to cook` and `in progress` after PR review/fix succeeds.

13. **Optional merge and CI convergence**
    - Only run this step when `--ship` or `--both` is present, and never in a batch-landing repository (see Batch-landing repositories).
    - Merge via GitHub using repository convention and branch protection. Prefer `gh pr merge --auto` when required checks are still pending; otherwise use the repo's allowed merge method.
    - Never force push. Never direct-push to protected target branches.
    - After merge, watch target-branch CI/deploy workflows for the merge commit.
    - On merge success, finalize the plan index: match the merged PR to its plan (recorded `--linked-pr`, or plan branch == PR head branch) and run `ak plan close <id>`; optionally append a completion comment to a linked issue per the shared reference's "Delivery finalization" section. A resolve/match miss means already closed or no plan — skip silently. Never delete plan files.
    - If CI fails with a deterministic repo-fixable error:
      1. Inspect the failed run/job logs with `gh run view`.
      2. Create a follow-up fix branch/worktree from the target branch.
      3. Activate `/ak-fix --auto` with exact failing command/error evidence.
      4. Ship the follow-up in the same mode (during `--both`, the current stage's mode: beta stage → beta, stable stage → official), run `/ak-review-pr --fix --reply`, merge, and watch again.
    - Stop only when target-branch CI succeeds, an external blocker remains, or the same blocker survives 3 fix attempts.
    - **Dual-stage (`--both`) sequence:**
      1. **Beta stage:** merge the beta PR and watch beta/dev-branch CI to green using the merge and fix loop above.
      2. Do not start the stable stage while beta CI is red, pending, or blocked. If the beta stage ends on an external blocker or exhausts fix attempts, stop, report, and mark the stable stage as skipped.
      3. **Stable stage:** after beta CI is green, ship stable. Pick the path from how the beta merge landed:
         - If the feature is already merged into the beta/dev branch and the repository promotes beta/dev into stable by convention (release/promotion PR from dev to main), follow that convention. Before merging a promotion PR, list the commits it carries; if it sweeps unrelated work beyond this issue, stop and ask the user instead of merging silently.
         - If the feature branch is still independent of the stable target (no promotion convention; stable receives feature PRs directly), activate `/ak-ship official` from the feature branch.
      4. Capture the stable PR, then activate `/ak-review-pr <stable-pr> --fix --reply`, apply `ready to ship stable` to the source issue and stable PR, and remove `ready to ship beta`. When `--advice` is present, run the mandatory post-PR review gate for the stable PR too: after its CI is terminal and green, spawn `kongming` to review the whole implementation and comment its assessment plus next steps on the stable PR and the source issue (see Advisory supervision).
      5. Merge the stable PR and watch stable-branch CI to green with the same merge and fix loop. The run is complete only when stable CI succeeds or a documented external blocker remains.

## GitHub Issue Body

When creating or updating a pipeline issue, include:
- **Outcome:** user-visible outcome.
- **How It Works:** 3 operational bullets (mechanism, data flow, boundaries).
- **Architecture / Flow:** Mermaid flowchart (`flowchart TD`) of components.
- **Advisor Scope Lock:** locked boundaries and non-goals (when `--advice` active).
- **Implementation metadata:** branch, plan path, mode, route, PR link(s).
- **Acceptance Criteria:** checklist from plan.
- **Pipeline State:** checklist tracking phases (worktree, investigate, plan, cook/fix, review, test, docs, ship, PR review, merge/CI).

Full template: `references/report-templates.md`.

## Security

- Never write secrets, tokens, customer data, or private env values into issues, PRs, comments, plans, or logs.
- Redact sensitive command output before posting to GitHub.
- If `gh` auth lacks permission to create labels, issues, PRs, reviews, or merges, stop and report the exact missing capability.
- If CI fails because of missing secrets, unavailable services, or required human approval, record it as an external blocker. Do not weaken tests or hide failures.

## Completion Report

End every vibe run with a structured report containing:
- **Vibe Result:** source, branch/worktree, plan, issue, PR(s), mode, route, review, merge, CI status, and disposition lines for all conditional steps (`Research`, `Debug`, `Test`, `Docs`: run or skipped + reason).
- **Journey Diagram:** Mermaid flowchart (`flowchart LR`) showing pipeline execution path.
- **Implementation Summary:** concrete changes shipped across components.
- **Plan Deviations:** differences from original plan with rationale, or `None`.
- **Subagent Quality Assessment:** grounded code-review verdict and severity counts (`0 Critical / 0 Important / N Minor — resolved X/Y`), never fabricated scores.
- **Human Next Steps:** concrete follow-up tasks for human reviewers/operators.
- **Unresolved questions:** any remaining open issues or `None`.

Full template: `references/report-templates.md`.
