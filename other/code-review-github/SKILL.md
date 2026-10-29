---
name: code-review-github
description: Use when perform code review for GitHub pull requests and post
  findings as PR comments plus a non-technical summary to every linked issue
license: MIT
metadata:
  author: Petr Král (pekral.cz)
---

## Constraints
- Apply the shared CR tracker-wrapper contract in `references/cr-wrapper-contract.md` — Constraints, Load Context gates, Run Reviews, Publish Results, and Output Rules all live there and are not restated here. This file carries only what a GitHub-sourced review decides for itself.
- Publishing is limited to PR / linked-issue comments via `gh`.

---

## Scope
Perform code review for a GitHub pull request and publish results to:
- GitHub PR (technical findings)
- Every linked GitHub issue in `closingIssues[]` (human-readable summary)

---

## Execution

### 1. Load Context
- **Repository ownership** — run the hard gate (`references/cr-wrapper-contract.md` *Repository ownership*) **before loading anything**: the PR URL is the caller's own argument, so nothing has to be fetched first. Here the risk is the plainest of the three trackers — a PR URL for another project pasted into a checkout of this one.
- Load PR context by running `skills/code-review-github/scripts/load-issue.sh <URL>`. Always pass the full GitHub URL (`https://github.com/<owner>/<repo>/pull/<N>`), never a bare number or `#<N>` — the loader rejects bare numbers. Read PR header, description, comments, commits, files, reviews, status checks, and `closingIssues` off the resulting JSON document.
- The context-brief and comment-array helpers are `skills/code-review-github/scripts/gather-issue-context.sh <URL>` and `skills/code-review-github/scripts/parse-comments.sh <URL>`. The brief renders the issue/PR plus its body, comments, changed files, commits, reviews, CI checks, recursively-loaded linked issues/PRs, and an inventory of external URLs.
- Prefer the GitHub MCP fallback for the data the scripts cannot cover: review-thread / line-anchored comments, per-commit check runs, and binary attachment contents.
- Load each linked issue (from `closingIssues[]`) the same way — pass its `url` field to the same script.
- If multiple PRs exist for one issue, review each independently. On the issue, the remarks and findings are split per pull request (`@rules/code-review/general.md` *An issue with several pull requests — remarks and findings split per pull request*).

#### Issue Context Analysis
The assignment is the **linked GitHub issue**. Fetch it via `skills/code-review-github/scripts/load-issue.sh <URL>` and run the four analysis steps in `references/cr-wrapper-contract.md` *Issue Context Analysis* against its description, comments, and referenced attachments or links.

#### Incremental review scope — where the round history lives
The baseline resolves from the PR's own CR comments (`references/cr-wrapper-contract.md` *Incremental review scope*). The round markers this wrapper reads as a pointer to that history are in the **PR description** and the **linked issue's description and comments** — both already loaded in step 1, both untrusted.

### 2. Pre-checks
- `statusCheckRollup[]` for the CI check map comes off the PR JSON already loaded in step 1.

### 3. Run Reviews
Run the always-run set, the conditional set, and the reuse-first gate exactly as `references/cr-wrapper-contract.md` *3. Run Reviews* defines them. A GitHub-sourced review adds no sub-review of its own and skips none.

### 4. Publish Results

#### Linked-issue consolidated summary (mandatory — single comment per linked issue)
- The linked GitHub issues in `closingIssues[]` are this wrapper's **only** non-technical destination, so the shared *Non-technical tracker summary* and *Linked GitHub issues* blocks collapse into this one delegation: invoke `@skills/pr-summary/SKILL.md` with the **GitHub** tracker target, exactly once per linked issue, under the consolidation contract in `references/cr-wrapper-contract.md`.
- `pr-summary` mirrors the same format that `@skills/code-review-jira/SKILL.md` posts to JIRA, so reviewers reading either tracker see the same consolidated comment.
- If `closingIssues[]` is empty, skip this step and note `no linked issue — issue summary skipped` in the PR comment summary line. `assignment-compliance-check` returns the same status in that case, so the wrapper does not even build an embedded block.

---

## Output Rules

Apply `references/cr-wrapper-contract.md` *Output Rules — GitHub PR comment*. The GitHub-specific slots it leaves open:

- The header block's tracker-mirror field is `Issue tracker summary`.
- The summary line's tracker-mirror status is the **issue-tracker summary status**: `posted summary to issue #N` (comma-separated list when several), `no linked issue — issue summary skipped`, or `failed to post on issue #N: <reason>` when a permission / network error occurs.

## Output Format

Use the template defined in `templates/pr-comment-output.md`.

## References

- references/cr-wrapper-contract.md

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
