---
name: address-pr-feedback
description: >-
  One-shot pass to address PR review comments: fetch threads, apply validated
  fixes, lint/test affected files, commit, push, reply, and offer to resolve.
  Use when the user asks to address review comments on a PR or points to a PR
  link/number. For continuous monitoring until merge-ready, use pr-babysitter
  instead.
---

# Address PR Feedback

A single pass over a PR's review comments: fix what's valid, reply to everything, push.

## 1. Get PR context

Derive the repo and PR number at runtime — never hard-code them:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
gh pr view --json number -q .number   # PR from current branch, if not given explicitly
```

- Fetch review comments: `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments --paginate`
- Fetch PR details: `gh pr view <PR_NUMBER> --json title,body,files`
- Summarise for the user: which comments need code changes, which are discussion-only.

## 2. Apply code changes

- Address each comment that requires a code change — validate first (see the `pr-babysitter` validation gate: confirmed defect vs preference; behavior impact understood).
- Remove unused components or exports flagged by reviewers.
- When a reviewer asks "do we have a component for this?", search the codebase for an existing shared component before writing a new one.
- If a comment touches an externally consumed surface, apply the `contract-guard` skill before changing it.

## 3. Lint

Run lint only on the **changed files**, the way the repo's pre-commit hook would. Check `package.json` scripts or the pre-commit config (e.g. `lefthook.yml`, `.husky/`) for the right command. Fix errors before proceeding.

## 4. Run affected tests

Find the test command in the repo's package scripts. Run only the tests affected by the changes — not the full suite — following the repo's test conventions.

## 5. Commit and push

Stage only the files you changed. Commit with a clear message in the repo's convention. Push. If asked to rebase: `git fetch origin main`, `git rebase origin/main`, then `git push --force-with-lease`.

## 6. Reply to PR comments

Post a reply to each addressed comment:

```bash
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
  -X POST -f body="<message>"
```

Thank reviewers, confirm what was done ("Done — switched to the shared component. Thanks!"), keep the tone friendly. For declined suggestions, explain the reasoning with evidence.

## 7. Offer to resolve threads

Ask the user whether addressed comments should be marked resolved. If yes:

1. Fetch review thread node IDs (variableized GraphQL):

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        reviewThreads(first: 100) {
          nodes { id isResolved comments(first: 1) { nodes { databaseId body } } }
        }
      }
    }
  }' -f owner="<OWNER>" -f repo="<REPO>" -F pr=<PR_NUMBER>
```

2. Match threads to the comments replied to by `databaseId`, then resolve each:

```bash
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: { threadId: $threadId }) { thread { isResolved } }
  }' -f threadId="<THREAD_NODE_ID>"
```

## Notes

- Always derive `OWNER`, `REPO`, `PR_NUMBER` at runtime from `gh`.
- Don't run the full test suite for a small change — affected files only.
- Never resolve a thread whose fix wasn't validated; reply with analysis instead.
