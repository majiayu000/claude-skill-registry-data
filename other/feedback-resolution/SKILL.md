---
name: feedback-resolution
description: "Address PR review feedback through surgical fixes traceable to specific comments, apply the Boy Scout Rule only to already-modified files (separate `improve:` commits), recover context by code snippet rather than line number, and enforce pushback only when factually incorrect, test-breaking, or CLAUDE.md-violating. Use when resolving reviewer comments on a pull request. This skill MUST be consulted because every untraceable change is out-of-context, and pushback without evidence is just disagreement."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
context: fork
agent: general-purpose
---

# Feedback Resolution

## Contract

Iron law: **every change traces to a specific review comment or passes the Boy Scout proximity test; anything else is out-of-context and does not belong in this round.** Invoked by `/flow:address` Phase 1 (collect and categorize feedback) through Phase 4 (verify, post the resolution comment, re-request review). Returns one commit per feedback item (`fix(scope): address review — {summary}`), separate `improve:` commits for Boy Scout fixes, a response for every Question or Pushback item, and the resolution comment from `templates/resolution-comment.md` posted before review is re-requested. Permitted skips: none — pushback replaces a fix only with `file:line` evidence, a named breaking test, or a quoted CLAUDE.md rule.

## Collect

```bash
PR_NUM="${PR_NUM:?pass the PR number from the invoking command}"
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
gh api repos/$REPO/pulls/$PR_NUM/comments --jq '.[] | {id: .id, path: .path, line: .line, body: .body, author: .user.login}'
gh pr view $PR_NUM --json reviews --jq '.reviews[] | {state: .state, body: .body, author: .author.login}'
```

## Categorize

| Category | Meaning |
|----------|---------|
| **P1 — Must fix** | Code bug, security issue, logic error |
| **P2 — Should fix** | Convention violation, missing test, unclear code |
| **P3 — Consider** | Style preference, optimization suggestion |
| **Question** | Needs a response, not necessarily a code change |
| **Resolved** | Already fixed or no longer relevant |

## Fix Each Item (one task per item)

1. Read the comment. Do not trust its line number — locate by the quoted snippet (`grep -n "quoted_code" $FILE`) and path, then read the current file.
2. Implement the minimal fix to the literal comment. If intent is unclear, check follow-up comments and codebase patterns, take the most conservative interpretation, and state it in the response.
3. Write or update a test that would have caught the issue, following existing test patterns; test the specific edge case, not just the happy path. Touch only the fix target and its test file.
4. Verify the fix addresses that comment and tests pass.
5. Commit `fix(scope): address review — {summary}` — one commit per item, never batched.

No new features; no formatting changes in files the feedback did not mention.

## Boy Scout Rule

Cleanup is allowed only in files already modified for feedback and only if it passes the `code-quality-principles` proximity test. Boy Scout fixes get separate `improve:` commits, never mixed with feedback fixes. A finding in a touched file is never out-of-scope. P1/P2 anywhere: fix in this PR. Cosmetic P3 in an untouched file: fix if bounded (<10 lines) or document inline under `### Known cosmetic notes`; a follow-up issue only under `minimalScope` mode.

## Pushback

Valid only when one of these holds, with the evidence in the response:

- **Factually incorrect** — cite `file:line` showing the current state and why the feedback does not apply.
- **Would break existing tests** — name the test and its `file:line`.
- **Contradicts CLAUDE.md** — quote the rule and its location.

"I disagree" is not pushback; preferences resolve in the reviewer's favor. Never ignore feedback silently. A genuine product/architecture judgment beyond these three categories is a six-field escalation per `references/escalation-format.md`; finding triage (P1/P2/P3 disposition) is never an escalation trigger (`skills/llm-operator-principles/SKILL.md`).

## Verify and Re-Request

Before re-requesting: all quality commands pass; every item has a commit or response; change-classification shows no out-of-context files; push (Tier 2). Then, as one atomic sequence: post the resolution comment (`gh pr comment $PR_NUM --body "$BODY"`, structure from `templates/resolution-comment.md`) and re-request (`gh pr edit $PR_NUM --add-reviewer @{reviewer}`). Push without the comment is incomplete — the reviewer cannot see what was addressed.
