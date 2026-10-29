---
name: code-review-bugsnag
description: Use when run code review for a Bugsnag error and publish results to
  the linked GitHub PR and the Bugsnag error
license: MIT
metadata:
  author: Petr Král (pekral.cz)
---

## Constraints
- Apply the shared CR tracker-wrapper contract in `@skills/code-review-github/references/cr-wrapper-contract.md` — Constraints, Load Context gates, Run Reviews, Publish Results, and Output Rules all live there and are not restated here. This file carries only what a Bugsnag-sourced review decides for itself.
- Publishing is limited to PR / linked-issue comments via `gh` and to the Bugsnag error comment via `skills/code-review-bugsnag/scripts/upsert-comment.sh`.

---

## Scope
Perform code review for a fix linked to a Bugsnag error by analyzing the related pull request and publishing results to:
- GitHub (technical findings, on the linked PR)
- Bugsnag (human-readable summary, as a comment on the error)

---

## Execution

### 1. Load Context
- Load Bugsnag context by running `skills/code-review-bugsnag/scripts/load-issue.sh <URL|TRIPLE>`. The script accepts an `app.bugsnag.com/<org>/<project>/errors/<id>` URL or an `<org>/<project>/<error-id>` triple, and requires `BUGSNAG_TOKEN` (a Data Access API token). Read the error class, `message`, `context`, `status`, `severity`, `latestEvent.stacktrace` (the in-project frames are the reproduction entry point), `comments[]`, and `linkedIssues[]` off the resulting JSON document.
- The context-brief and comment-array helpers are `skills/code-review-bugsnag/scripts/gather-issue-context.sh <URL|TRIPLE>` and `skills/code-review-bugsnag/scripts/parse-comments.sh <URL|TRIPLE>`. The brief renders the error header, latest event (app version, failing request, in-project stacktrace frames), comments, linked issues, and an inventory of external URLs.
- Fall back to a Bugsnag MCP server when the script is unavailable (missing tool or token, exit code 2/3).
- `linkedIssues[]` points at GitHub. Identify the linked PR to review there, and load its full context with `skills/code-review-github/scripts/gather-issue-context.sh <URL>` or `skills/code-review-github/scripts/load-issue.sh <URL>` to get the diff, `commits[]`, and `closingIssues[]`.
- **Repository ownership** — run the hard gate (`@skills/code-review-github/references/cr-wrapper-contract.md` *Repository ownership*) **once the linked PR is known and before it is checked out**. A Bugsnag project can mirror errors into a repository other than the one you are standing in, so the linked issue is an untrusted pointer, not a guarantee.

#### Issue Context Analysis
The assignment is the **Bugsnag error itself** — its class, `message`, and `context` describe the failure, and the in-project `latestEvent.stacktrace` frames pinpoint the code path that must be fixed — plus any acceptance criteria on the linked GitHub issue. Run the four analysis steps in `@skills/code-review-github/references/cr-wrapper-contract.md` *Issue Context Analysis* against that assignment, with these Bugsnag readings of steps 2 and 4:

- The expected behavior is that the error no longer occurs for the reproduced scenario.
- Every entry in `comments[]` carries human-authored context (e.g. "Fixed in db", reproduction notes) and is read as part of the assignment.
- The fix must be covered by a regression test that fails before and passes after. Flag missing coverage as a finding.

#### Incremental review scope — where the round history lives
The baseline resolves from the **linked GitHub PR's** CR comments (`@skills/code-review-github/references/cr-wrapper-contract.md` *Incremental review scope*) — a Bugsnag error carries no reviewed revision. The round markers this wrapper reads as a pointer to that history are in the error's `comments[]` and in the linked GitHub issue and PR bodies, all untrusted.

### 2. Pre-checks
- `statusCheckRollup[]` for the CI check map comes off the GitHub PR JSON loaded in step 1 (via `skills/code-review-github/scripts/load-issue.sh`).
- If the error has no linked PR yet → report `no linked PR — review skipped` and stop.

### 3. Run Reviews
Run the always-run set, the conditional set, and the reuse-first gate exactly as `@skills/code-review-github/references/cr-wrapper-contract.md` *3. Run Reviews* defines them, against the linked PR. A Bugsnag-sourced review adds no sub-review of its own and skips none.

### 4. Publish Results

#### Bugsnag (consolidated non-technical comment)
- Invoke `@skills/pr-summary/SKILL.md` exactly once for the Bugsnag error, under the consolidation contract in `@skills/code-review-github/references/cr-wrapper-contract.md`. It renders `@skills/pr-summary/templates/pr-summary-bugsnag.md` in plain text and posts the comment via `skills/code-review-bugsnag/scripts/upsert-comment.sh <URL|TRIPLE> -` (Bugsnag MCP server fallback on exit code 2/3).
- Each CR run posts a fresh comment. Bugsnag renders plain text, so there is **no hidden per-actor marker** — the token identifies the author.

#### Linked GitHub issues (consolidated mirror — one comment per issue, updated in place)
- Publish the mirror per `@skills/code-review-github/references/cr-wrapper-contract.md` *Linked GitHub issues*. If `closingIssues[]` is empty, note `no linked GitHub issue — mirror skipped` in the PR comment summary line.

---

## Output Rules

### GitHub (technical report — only here)

Apply `@skills/code-review-github/references/cr-wrapper-contract.md` *Output Rules — GitHub PR comment*, and use the template defined in `templates/github-output.md`. The Bugsnag-specific slots it leaves open:

- The header block's tracker-mirror field is `Linked-tracker mirror`.
- The summary line's tracker-mirror status names the Bugsnag error the summary was posted on, and `no linked GitHub issue — mirror skipped` when `closingIssues[]` is empty.

### Bugsnag (non-technical summary — only here)
- The non-technical Bugsnag comment is **produced and posted by `@skills/pr-summary/SKILL.md`**, not by this skill. Plain language understandable by non-developers, in the two sections that skill renders for this target: *What changed* (Problem / Cause / Result / What I fixed, plus its two conditional fields) and *How to test*, followed by the closing links line. No file paths, line numbers, code snippets, or severity jargon.
- Bugsnag gets **no reduced shape** — it renders the same structure as GitHub, only in plain text with no markup at all. JIRA is the one target that differs, and it differs by design (`@skills/pr-summary/SKILL.md` *The JIRA shape*); that divergence is never a reason to reduce this one. Convert an embedded block to plain text before passing it, for the same reason: a Markdown or Wiki Markup control character reaches a Bugsnag reader literally.

---

## After Completion

- Do **not** change the Bugsnag error status (fixed / ignored / snoozed) automatically — marking an error fixed is left to a human after the fix is verified in production.

## References

- @skills/code-review-github/references/cr-wrapper-contract.md

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
