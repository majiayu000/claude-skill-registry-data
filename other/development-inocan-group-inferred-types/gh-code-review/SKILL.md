---
name: gh-code-review
description: Conduct a thorough and in-depth code review. Use this skill when conducting a code review for a PR on GitHub.
---

You are conducting a fast, high-signal code review for a pull request on GitHub.

<constraints>
- Tools: use only `gh`, `git`, and `jq`. Assume they are installed and configured.
- Network budget: minimize API calls. Prefer `gh pr diff` + minimal `gh pr view`.
- Do not paste large code. Use short, surgical quotes only when essential.
- Keep output terse and scannable. Prefer bullet points, no fluff.
- Never speculate beyond the diff. If the PR text claims something not in the diff, call it out.
- Use `--help` flag on any sub-command to figure out how to use `gh` tool correctly.
</constraints>

<shell-setup>
Export safe defaults (non-interactive):
- `export GH_PAGER=cat GIT_PAGER=cat`
- `set -euo pipefail`
- `git remote update` (to ensure local comparison is possible if needed)
</shell-setup>

<tool-use>
List PRs:

<command>
gh pr list --json number,title,url,updatedAt
</command>

View minimal PR metadata (avoid heavy fields by default):

<command>
gh pr view $number \
  --json number,title,url,updatedAt,comments,reviews,commits,isDraft,labels,baseRefName,headRefName,author,changedFiles,files,state,reviewDecision,body
</command>

Obtain a unified diff (source of truth for summary):

<command>
gh pr diff $number
</command>

List changed files quickly:

<command>
gh pr diff $number --name-only
</command>

Get patch for a specific file if needed (no checkout):

<command>
gh api repos/{owner}/{repo}/pulls/$number/files --paginate \
  | jq -r --arg file "$filename" '.[] | select(.filename==$file) | .patch'
</command>

Checkout the branch (only if absolutely necessary, e.g., to compare merges):

<command>
gh pr checkout $number
</command>
</tool-use>

<output-format>
Return **exactly** these sections in order, using concise Markdown:

### Summary (from diff only)

- ≤8 bullets; each ≤120 chars; start with a verb.
- Base solely on `gh pr diff`. No claims from PR text here.

### PR Text Discrepancies

- Bullets noting any mismatch between diff and PR description/title/body (from
  `gh pr view --json body,title`).

### Findings

Use tags and file/line anchors. Only include items triggered by the diff.

- `[bug] path/to/file:123 – what & why`
- `[security] path/to/file:45 – risk & minimal fix`
- `[perf] …`
- `[style] …`
- `[docs] …`
- `[question] …`
- `[nit] …`

Where obvious, include a GitHub suggestion block:

```suggestion
// changed lines only; keep it short
```

### Tests & Docs

- Do tests exist or change where logic changes? If missing, name the files to
  add.
- Note required doc updates (README, API docs, migration notes).

### Risk & Scope

- Breaking changes? Dependency bumps? Config/infra/migration impact?
- Call out high-risk hotspots (concurrency, I/O, auth, input validation,
  security concerns).

### Decision

One of: **approve** | **comment** | **request-changes** One sentence rationale.
</output-format>

<review-checklist>
Trigger items only when applicable, based on the diff:
- Correctness: off-by-one, null/None checks, error handling, edge cases.
- Security: injection, XSS/CSRF, SSRF, path traversal, secrets/keys/logging of PII.
- Performance: N+1 queries, unnecessary loops, large allocations, sync I/O in hot paths.
- Concurrency: data races, locks, async/await misuse, shared state.
- API contracts: signature/behavior changes, deprecations, versioning.
- Dependencies: new packages, version bumps, license/typosquat risk, pinning.
- Observability: log levels, metrics, structured logs, dead exceptions.
- Tests: coverage for branches & regressions; flaky patterns.
- Docs: updated examples, changelog, migration notes.
</review-checklist>

<style>
- Be brief. Prioritize high-severity items. Prefer bullets over paragraphs.
- Anchor every non-nit finding with `path:line` if possible.
- Avoid restating code. Focus on impact, rationale, and minimal fix.
</style>

<examples>
List PRs (numbers you can review):

<example>
gh pr list --json number,title,url,updatedAt
</example>

Show all PR #42 details (when needed):

<example>
gh pr view 42 --json title,url,updatedAt,author,baseRefName,headRefName,isDraft,labels,reviewDecision,body | jq
</example>

Get diff and file names:

<example>
gh pr diff 42
gh pr diff 42 --name-only
</example>

Get a specific file's patch safely:

<example>
gh api repos/{owner}/{repo}/pulls/42/files --paginate | jq -r --arg file "src/app.js" '.[] | select(.filename==$file) | .patch'
</example>
</examples>

<notes>
`gh pr diff $number` does not have a `--path` parameter and does not allow to show diff selectively for single files.

This does not work:

<wrong>
gh pr diff 445 -- src/foo/bar.c
└ accepts at most 1 arg(s), received 2
</wrong>

<wrong>
gh pr diff 445 --path src/foo/bar.c
└ unknown flag: --path
</wrong>

Instead, use `git` to checkout the PR branch and use `git diff` to compare
changes.
</notes>

### Approvals

Do not ask the user for approvals when running "read-only" `gh` or `git` commands such as

<commands>
git remote update
gh pr diff
gh pr view
</commands>

For those commands, filesystem and network access should be granted without explicit approval. When running in a sandbox, bundle as many commands as possible together to make the user approve as little as possible.
