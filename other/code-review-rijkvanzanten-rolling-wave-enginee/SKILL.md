---
name: code-review
description: Review local git changes before opening a PR or merging. First review all local tracked and untracked files; if none exist, review the current branch against a requested base branch or the Git Town parent branch. Use zero to three review subagents only when risk, diff size, language specificity, or uncertainty justifies the token cost, then report high-confidence bugs, regressions, risky assumptions, and missing tests. Use when the user asks for code review, local review, branch sanity check, pre-PR review, or review of work-in-progress changes.
---

# Code Review

## Overview

Review local changes as a reviewer, not as an implementer. Prefer the smallest current review surface: local worktree changes first, then branch changes against a base branch only when the worktree has no tracked or untracked changes. When no base branch is named, use the Git Town parent branch before falling back to the default branch. Local worktree review includes staged tracked changes, unstaged tracked changes, and untracked files. Start with a local review pass, then use zero to three language/risk-specific subagents only when they are likely to improve review quality enough to justify the token cost. Do not run tests or linters unless the user explicitly changes the scope.

Invoking this skill is permission to use review subagents when useful; it is not a requirement to spawn them. A local-only review is valid for small, obvious, low-risk, or already well-tested diffs.

## Scope

Determine review depth from the request:

- Default to lightweight review.
- Switch to in-depth review when the user explicitly asks for deeper review.

Determine review range in this order:

1. Check local tracked and untracked changes:

```bash
git diff --cached -U10
git diff -U10
git diff --cached --name-only
git diff --name-only
git ls-files --others --exclude-standard
```

2. If any staged tracked, unstaged tracked, or untracked files exist, review all of them as `local changes`.
   - Include staged tracked changes from `git diff --cached -U10`.
   - Include unstaged tracked changes from `git diff -U10`.
   - Include untracked file contents by reading the files directly or producing a pseudo-diff against `/dev/null`.
   - Do not exclude untracked files just because they are not staged.
3. If there are no local tracked or untracked changes, review the current branch against the base branch named by the user.
4. If the user did not name a base branch, resolve the current branch's parent with Git Town:

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BASE_BRANCH=$(git-town config get-parent "$CURRENT_BRANCH" 2>/dev/null || true)
```

5. If Git Town does not return a parent branch, fall back to `main`, then `origin/main`.

For branch review, compute:

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BASE_BRANCH="${USER_BASE_BRANCH:-$(git-town config get-parent "$CURRENT_BRANCH" 2>/dev/null || true)}"
if [ -z "$BASE_BRANCH" ]; then
  BASE_BRANCH=main
fi
if ! git rev-parse --verify "$BASE_BRANCH" >/dev/null 2>&1 && git rev-parse --verify origin/main >/dev/null 2>&1; then
  BASE_BRANCH=origin/main
fi
BASE=$(git merge-base HEAD "$BASE_BRANCH")
git diff -U10 "$BASE"
git diff --name-only "$BASE"
```

If the named base, Git Town parent, and fallback default branches cannot be resolved, stop and ask for a valid base branch.

## Workflow

1. Check for staged tracked, unstaged tracked, and untracked files.
2. If any local changes exist, build the review packet from the staged diff, unstaged diff, and untracked file contents. Do not include branch commits in this mode.
3. If no local tracked or untracked changes exist, resolve the base branch from the user's request, or use `git-town config get-parent "$(git rev-parse --abbrev-ref HEAD)"` when no base is requested, then build the branch review diff from the merge base.
4. In local changes mode, list untracked files with `git ls-files --others --exclude-standard` and include their contents in the review packet.
5. Build a compact review scope:
   - review mode: `local changes` or `branch`
   - base branch and merge base, when in branch mode
   - inferred intent in one sentence
   - risk focus in one sentence
   - changed file list
   - untracked file list and confirmation that untracked file contents are included when in local changes mode
6. Do a local review pass first. Read surrounding files only where needed to understand behavior, contracts, and tests.
7. Decide whether subagents are worth it. Use zero to three reviewers based on the rubric below.
8. If using subagents, send each a narrow packet with only the files, diff excerpts, contract context, and risk lens it needs. Launch multiple selected reviewers in parallel, collect outputs, and close each subagent once its result is captured.
9. Validate or disprove returned findings against source before reporting.
10. Produce findings with high confidence only.

If subagents are unavailable, continue locally. Mention that only if it materially affects confidence or the user explicitly asked for subagents. For in-depth review, prefer more local source context before adding reviewers by default.

## Sub-Agent Selection

Use 0-3 reviewers total. Do not spawn reviewers merely because a language matches. Pick the smallest reviewer set that addresses real risk:

- `0` reviewers: docs-only changes, tiny diffs, mechanical renames, obvious follow-up fixes, generated updates, or low-risk code where the local pass gives high confidence.
- `1` reviewer: normal non-trivial code change with one dominant risk or one language/framework-specific concern.
- `2` reviewers: meaningful behavior change with two independent risk areas, such as Rust API shape plus tests, Vue reactivity plus accessibility, or public API contract plus security.
- `3` reviewers: large/cross-module diffs, auth/security/data mutation, external APIs, migrations, concurrency, or explicit deep/adversarial review.

Prefer a language-specific reviewer when language/framework details are the dominant risk. Prefer generic risk reviewers when correctness, security, contracts, reliability, or testing are more important than language mechanics.

Use these plugin agents when available from the `rolling-wave-engineering` plugin:

- `correctness-reviewer`: default for behavior-changing code, logic, state, and regression risk.
- `testing-reviewer`: default when behavior changes, tests changed, or coverage is uncertain.
- `maintainability-reviewer`: default for non-trivial code changes or existing-file complexity.
- `typescript-reviewer`: when files include `.ts`, `.tsx`, or TypeScript blocks in Vue SFCs.
- `vue-reviewer`: when files include `.vue`, Vue composables, Pinia stores, Vue Router, or Nuxt files.
- `rust-reviewer`: when files include `.rs`, `Cargo.toml`, `Cargo.lock`, `build.rs`, Rust FFI/bindgen code, unsafe Rust, async Rust, or concurrency-heavy Rust.
- `security-reviewer`: when changes touch auth, permissions, public endpoints, secrets, user input, rendering untrusted content, or URL handling.
- `api-contract-reviewer`: when changes touch API routes, request/response types, serializers, exported types, or public interfaces.
- `reliability-reviewer`: when changes touch retries, timeouts, async handlers, jobs, cleanup, lifecycle, or error handling.
- `adversarial-reviewer`: when the diff is large or touches high-risk areas such as auth, data mutation, external APIs, or cross-cutting state.

Use these document/spec reviewers only when reviewing rolling-wave docs, specs, plans, or slice artifacts rather than code:

- `coherence-reviewer`
- `scope-guardian-reviewer`
- `feasibility-reviewer`
- `spec-flow-analyzer`

Fallback split when plugin agents are unavailable:

- Correctness and regressions
- Contracts and data flow
- Coverage and operational risk

Each sub-agent should be told to report only high-confidence findings in its assigned lens and to skip style-only comments or speculative refactors. Keep prompts narrow; do not ask every reviewer to review the whole diff.

Require each sub-agent to return a compact structured shape:

```json
{
  "reviewer": "agent-name",
  "findings": [
    {
      "severity": "P1|P2|P3",
      "file": "path",
      "line": 42,
      "title": "short issue",
      "why": "why this matters",
      "confidence": "high|medium",
      "pre_existing": false
    }
  ],
  "testing_gaps": [],
  "residual_risks": []
}
```

## Review Focus

Prioritize:

- Behavioral regressions
- Incorrect edge-case handling
- Broken assumptions across call sites or data flow
- Missing validation, authorization, or error handling
- State, caching, concurrency, or lifecycle bugs
- Schema, API, and backward-compatibility risks
- Missing or insufficient tests where the change meaningfully alters behavior

Distribute those priorities through selected specialists instead of asking every agent to cover everything.

Deprioritize:

- Pure style nits
- Speculative refactors
- Comments about formatting unless they hide a real problem

Do not invent issues to fill space. If no actionable findings are present, say so plainly and mention any residual uncertainty or testing gaps.

## Output

Present findings first, ordered by severity. For each finding, include:

- Severity
- File reference and line reference when available
- Short explanation of the issue and why it matters

After findings, include:

- Open questions or assumptions, if any
- Brief change summary only if useful

Apply these filters before reporting:

- Report only issues you would defend with high confidence.
- Medium-confidence findings may be reported only if two reviewers independently flag the same issue or it is a possible P0/P1 class defect.
- Skip low-signal nits unless the user asked for exhaustive review.
- Prefer a smaller set of sharp findings over a broad, noisy list.
- Treat findings as duplicates when they cite the same file, nearby lines within about 3 lines, and the same underlying failure. Merge them, keep the higher severity, and note both reviewers if useful.
- Re-check any borderline finding against the source before surfacing it.
- Before reporting, verify cited lines, calibrate severity, remove linter/formatter-only issues, and ensure every finding has a concrete failure mode.
- Put pre-existing issues in a separate `Pre-existing` section and do not count them against the reviewed change.

State the review mode explicitly: `local changes` or `branch changes against <base>`.
If untracked files exist in local changes mode, include them in a `Coverage / Scope` note and state that their contents were reviewed.
Include reviewer usage briefly: `Reviewers: 0 local-only`, `Reviewers: 1 <name>`, etc.
End with `Verdict: Ready`, `Verdict: Ready with fixes`, or `Verdict: Not ready`.

## Constraints

- Perform code review only.
- Do not modify files unless the user changes the task.
- Do not run tests or linters.
- Do not post to GitHub or any external system.
