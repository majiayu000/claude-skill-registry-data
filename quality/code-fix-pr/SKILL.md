---
name: code-fix-pr
description: Evaluate PR review comments with parallel analysis across correctness, security, and convention lenses.
---

Evaluate and address PR review comments.

## Prerequisites

Reference these skills first:

- Read `jujutsu` skill to understand change context.
- Read `github-cli` skill to fetch PR comments.

## Process

### Step 1 - Gather PR Data

- Get PR number: ask the user or infer from the current branch.
- Determine repository: `gh repo view` or `jj git remote list`.
- Fetch PR comments: `gh api repos/owner/repo/pulls/<number>/comments -X GET --paginate`.
- Fetch reviews: `gh api repos/owner/repo/pulls/<number>/reviews -X GET --paginate`.
- Get PR diff: `gh pr diff <number> -R owner/repo`.
- Check PR status: `gh pr checks <number> -R owner/repo`.
- Fetch failure logs: `gh run view <run-id> -R owner/repo --log-failed`.
- Capture CI failure context: summarize failed checks, error messages, and stack traces for later analysis.
- View working copy changes: `jj diff -s`.

**Important**: Always use `-X GET` to be explicit about read-only access.

### Step 2 - Analyze Comments and CI

Apply a reviewer lens to review comments across all relevant perspectives:

- Ground findings in file paths and line numbers.
- Prioritize the requested lens.
- Distinguish confirmed findings from speculative risks.
- Explain why each issue matters.

Review across these perspectives:

- **Correctness and quality**: Classify each comment as already-addressed, valid-fix-needed, invalid, or needs-discussion.
- **Security**: Identify valid security concerns vs false positives; assess severity.
- **Simplicity and convention**: Prefer the simplest change satisfying valid feedback; distinguish valid simplifications from over-engineering.
- **CI correlation**: Check whether each comment relates to an observed CI failure and whether addressing it would resolve the failure; incorporate available CI failure context.

Apply a researcher lens to validate APIs and research best practices for the fixes suggested in the PR comments:

- Prefer official documentation over blog posts.
- Cite sources with URLs.
- Separate confirmed facts from plausible interpretations.
- Note version requirements.
- Lead with the single most actionable recommendation.

- If CI failure logs are included, apply a researcher lens to research the specific error messages, stack traces, or test failures to identify root causes and known solutions:
  - Prefer official documentation over blog posts; cite sources with URLs.
  - Separate confirmed facts from plausible interpretations; note version requirements.
  - Lead with the single most actionable recommendation.

- If checks failed, apply a reviewer lens to analyze the GitHub Actions CI failure logs:
  - Ground findings in file paths and line numbers.
  - Distinguish confirmed findings from speculative risks.
  - Explain why each issue matters.

For each failure:

- **Failure classification**: test flake, code regression, env/infra issue, dependency problem, or timeout.
- **Root cause**: most likely root cause with supporting evidence from logs.
- **Diff relationship**: whether failures occur in code touched by this PR's diff or unrelated code.
- **Fix suggestion**: minimal fixes for code-regression failures; mitigation steps (retry, env fixes) for flakes/infra.

### Step 3 - Adjudicate Disputes

- For disputes or conflicting recommendations, apply an oracle lens to decide which feedback should be fixed, discussed, or rejected:
  - Identify the decision.
  - State assumptions and constraints.
  - Pick the smallest safe path that preserves future options.
  - Note what evidence would change the recommendation.
  - Explain the reasoning clearly.

### Step 4 - Synthesize Findings

Synthesize into a unified report:

1. **PR Summary**: PR number, title, state; total comments analyzed.
2. **Comment Classification**:
   - **Already Addressed**: list with resolution evidence.
   - **Valid - Should Fix**: list with severity and location.
   - **Not Valid - Won't Fix**: list with reasoning.
   - **Needs Discussion**: list with questions.
3. **Fix Plan**: numbered steps with file:line targets; best-practice references; estimated effort.
4. **CI Failure Analysis** (only if checks failed):
   - **Failing Checks**: each failed check with run ID and error summary.
   - **Failure Classification**: test flake / code regression / env-infra / dependency / timeout.
   - **Root Causes**: per-failure analysis with log evidence.
   - **PR Relationship**: in PR-touched code or unrelated.
   - **Recommendations**: fix suggestions for regressions; mitigation steps for flakes/infra.
5. **Next Steps**: immediate actions; questions for reviewer.
