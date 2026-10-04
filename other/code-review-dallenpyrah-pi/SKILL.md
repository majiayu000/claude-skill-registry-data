---
name: code-review
description: "Fan out six focused reviewer personas against the current PR — correctness, testing, maintainability, project-standards, security, and previous-findings. Each reviewer applies first-principles and game-theoretic pressure: invariants, incentives, information asymmetry, local shortcuts, repeated-game health, and adversarial behavior. Dedupe, validate, verify diff-line commentability, then post one GitHub review with summary plus inline comments where possible. No autofix, no approval, no request-changes. Hands off to /address."
---

# /code-review

Before rendering user-facing output, read `../_shared/plain-output.md`.

Run a multi-agent code review and post the validated findings to the current pull request.

This is a review skill, not an autofix skill. It should produce high-signal review comments that improve code health without flooding the PR.

## Preconditions

- You are inside a git repository.
- `gh` is authenticated.
- A PR exists for the current branch. Find it with:

```bash
gh pr view --json number,url,title,body,headRefName,baseRefName,headRefOid,baseRefOid
```

If no PR exists, tell the user to run `/pr` first and stop.

- The working tree is clean:

```bash
git status --porcelain
```

If uncommitted changes exist, stop. Do not review a moving target.

- `REVIEWERS.md` must be present. If it is missing, use the reviewer prompts embedded in this skill package. Do not invent new personas.

## Review standard

Review for durable code health, not perfection.

Block or flag issues that harm correctness, invariant protection, maintainability, architecture, security, test confidence, repo standards, repeated-game code health, or incentive alignment.

Do not flood the PR with cosmetic comments. Nits are allowed only when they are low-cost and clearly marked as non-blocking.

Never fabricate findings to look thorough.

## Game-theoretic review frame

For each potential finding, ask:

- What invariant is at risk?
- Who is the player?
- What local move did this code make easy?
- Who pays the cost later?
- What information is hidden from callers, reviewers, or maintainers?
- Does the code create a bad equilibrium over repeated changes?
- Would a tired engineer under deadline pressure misuse this?
- Would an attacker, malformed input, flaky service, or retry exploit this?
- Can the type/interface/test/port make the good move cheaper?

## Context to gather first

### 1. Repository identity

```bash
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
OWNER="${REPO%/*}"
NAME="${REPO#*/}"
```

### 2. PR metadata

```bash
gh pr view --json number,url,title,body,headRefName,baseRefName,headRefOid,baseRefOid,files,commits,reviews
```

Hold PR number, URL, title, body, base/head branches, head/base SHAs, changed files, commits, and existing reviews.

### 3. Diff and line map

Collect both human-readable diff and machine-usable changed-file patches:

```bash
gh pr diff <n>
gh pr view <n> --json files
```

Build a commentability map:

- `RIGHT` lines are new-file line numbers that appear in the PR diff as added or context lines.
- `LEFT` lines are old-file line numbers that appear in the PR diff as deleted or context lines.
- Inline comments require `(file, side, line)` present in this map.
- Non-commentable findings become summary findings.

Do not guess line positions.

### 4. Linked issue and architecture source of truth

Parse the PR body for closing keywords. If a linked issue exists, read it:

```bash
gh issue view <issue> --json number,title,body,state,url
```

The issue’s Architecture and Modules sections are the source of truth for what this PR was supposed to implement. If no linked issue exists, do not stop; treat the PR body as intent and add a summary-only `major` finding if the PR contains architectural change but no linked issue or architectural intent.

### 5. Prior PR comments

Collect both review comments and issue timeline comments:

```bash
gh api repos/{owner}/{repo}/pulls/<n>/comments --paginate
gh api repos/{owner}/{repo}/issues/<n>/comments --paginate
```

Also collect unresolved review threads through GraphQL when available.

### 6. Repo standards and learnings

Read root/repo/nested `AGENTS.md`, repo `CLAUDE.md`, `docs/learnings/`, `skills/`, relevant package scripts, and relevant test config when present.

## Finding schema

Every reviewer returns JSON only:

```json
[
  {
    "reviewer": "correctness | testing | maintainability | project-standards | security | previous-findings",
    "severity": "blocker | major | minor | nit",
    "category": "correctness | testing | maintainability | standards | security | recurring-pattern",
    "file": "<path or null>",
    "line": <int or null>,
    "side": "RIGHT | LEFT | SUMMARY",
    "finding": "<one-sentence problem statement>",
    "evidence": "<specific code, diff, issue, comment, doc, or repo-standard evidence>",
    "first_principles_issue": "<broken invariant/assumption/source-of-truth issue>",
    "game_theory_issue": "<bad incentive/information asymmetry/bad equilibrium/adversarial move>",
    "suggested_fix": "<concrete suggestion>",
    "confidence": <number between 0 and 1>
  }
]
```

Rules:

- `file`, `line`, and `side` are required for inline findings.
- Use `side: "SUMMARY"` when the finding is architectural, repo-wide, missing-test, missing-issue, or otherwise not tied to a changed diff line.
- `evidence` must name the exact source of the claim.
- `confidence < 0.70` should usually become `[]` unless the risk is severe.
- Return `[]` if there are no findings.

## The six reviewers

Use the prompts in `REVIEWERS.md`.

Always run all six:

1. **correctness** — conformance to issue architecture, behavior, edge cases, race conditions, error paths, contracts.
2. **testing** — coverage, test level, regression tests, error-path tests, false-confidence tests.
3. **maintainability** — architecture principles, deep modules, no complecting, lifecycle state, ports/adapters, names, abstraction quality.
4. **project-standards** — `AGENTS.md`, local conventions, Effect discipline, grounding, verification loop, swallowed errors.
5. **security** — trust boundaries, validation, secrets, auth/authz, injection, SSRF, unsafe deserialization, XSS, crypto, logs.
6. **previous-findings** — recurring review issues, `docs/learnings/`, prior comments, previously corrected patterns.

## Orchestration

Before spawning subagents, read `../_shared/subagents.md` and `../_shared/evidence-quality.md`.

### 1. Fan out

Use host-neutral reviewer subagents. Spawn all six reviewer agents in parallel when the host supports subagents. If subagents are unavailable, run the six reviewer lanes locally and state that parallel review was unavailable.

Pass the same context bundle to each reviewer: PR metadata, diff, changed files, linked issue if any, PR body, prior comments, repo standards, relevant files, line commentability map, relevant learnings, first-principles/game-theory review frame.

### 2. Collect and parse

Parse reviewer JSON into one flat list. Reject malformed findings unless the problem is obvious and can be normalized without changing meaning.

### 3. Normalize

Trim vague language, convert unsupported claims to invalid, convert non-diff-line findings to `side: "SUMMARY"`, attach reviewer/category if missing, ensure severity is valid, and ensure first-principles/game-theory fields are present or explicitly `not applicable`.

### 4. Dedupe

Two findings are duplicates when they share same file or both summary-level, line within 5 lines or same missing concern, same category, same root cause, and same bad incentive when applicable. Keep highest severity and merge evidence/suggested fixes.

### 5. Validate

For each deduped finding, spawn one validator subagent in parallel when the host supports subagents. If subagents are unavailable, validate locally and state that parallel validation was unavailable.

Validator input: finding JSON, relevant file contents, PR diff, line commentability map, linked issue/architecture, relevant repo standard, relevant prior comments or learning files.

Validator returns JSON only:

```json
{
  "valid": true,
  "posting_mode": "inline | summary",
  "reason": "<short reason>",
  "normalized_file": "<path or null>",
  "normalized_line": 1,
  "normalized_side": "RIGHT | LEFT | SUMMARY"
}
```

Drop invalid findings. Keep valid but non-commentable findings summary-only. Do not invent a line.

### 6. Group and cap noise

Post all blockers and majors. Post minors only when actionable. Post nits only in the summary unless they prevent confusion in a public API or architectural interface. If more than 12 validated findings survive, post all blockers/majors and summarize the rest by category.

## Posting to GitHub

Post one GitHub review with a summary body and inline comments when available.

### Build summary body

Use:

```markdown
## Review summary

<X> blockers, <Y> majors, <Z> minors, <W> nits.
<D> findings dropped by validator pass.
<S> findings kept summary-only because they were not commentable diff lines.

### Blockers
- <file:line or summary> — <finding>

### Majors
- ...

### Minors
- ...

### Nits
- ...

### Mechanism notes
- <recurring incentive or bad equilibrium found, if any>

Posted by `/code-review` — inline comments contain details for diff-line findings.
```

Omit empty severity sections. If zero validated findings, post `No findings.`.

### Inline comment body

Each inline comment body:

```markdown
**<Severity> — <category>**

<finding>

Evidence: <evidence>

First-principles issue: <first_principles_issue>

Game-theory issue: <game_theory_issue>

Suggested fix: <suggested_fix>
```

For nits, prefix: `Nit — I would not block on this.`

### Preferred post path — single review

Create a JSON payload with commit_id, event `COMMENT`, body, and comments. Post:

```bash
gh api -X POST "repos/${OWNER}/${NAME}/pulls/${PR_NUMBER}/reviews" --input "$PAYLOAD_FILE"
```

Do not use `APPROVE`. Do not use `REQUEST_CHANGES`.

### Summary-only path

If there are no inline comments:

```bash
gh pr review <n> --comment --body-file "$SUMMARY_FILE"
```

### Posting failure

If GitHub returns a validation error, print the exact error, do not post a partial review, re-check the line commentability map, convert invalid inline comments to summary-only only when the map proves they are not commentable, retry once with summary-only, and stop if retry fails.

## What NOT to do

- Do not approve the PR.
- Do not request changes.
- Do not autofix.
- Do not post an empty review except the explicit `No findings.` summary.
- Do not post comments on unchanged lines unless they are present as context lines in the PR diff.
- Do not comment on generated files unless the generated output is the reviewed artifact.
- Do not duplicate prior comments unless the current PR reintroduces the same problem.
- Do not bury blockers under nits.
- Do not treat “works once” as enough if the design creates bad repeated-game incentives.

## Output

Use Plain Senior output:

````markdown
## Decision
Review posted to <PR URL>.

## Why
blockers=<n> majors=<n> minors=<n> nits=<n>
dropped_by_validator=<n> summary_only=<n> inline_comments=<n>

## Example
```bash
gh pr view --json number,url,title
```

## Risk
<validator drops, summary-only comments, or "None known">

## Next
Run `/address` to work through the comments.
````

Then end with exactly this line and stop:

> Review posted to PR <url>. Run `/address` to work through the comments.
