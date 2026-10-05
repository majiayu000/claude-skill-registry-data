---
name: pick
description: Fetch open todo issues from a repo, analyze them, and pick the best one to work on next. Prefers PRs with review feedback over new issues.
---

# Pick Work Item

You are selecting the next work item from a GitHub repository. PRs with review feedback take priority over new issues.

## Environment

- The target repo is set via the `WORK_REPO` environment variable. All tools read it automatically.

## Instructions

1. Run `ensure_labels` (no arguments needed — reads repo from environment).
2. Run `get_prs_with_feedback` (no arguments needed).
3. If there are PRs needing attention (changes requested, failing CI checks, or merge conflicts):
   a. Pick the PR with the oldest `updatedAt` (longest waiting for attention).
   b. Write your output with `type` set to `"pr"` and the PR details. Include the `reason` field from the tool result.
   c. Skip the remaining steps.
4. Run `count_open_prs` (no arguments needed). If more than 4, write `o/pick/issue.json` with `{"error": "pr_limit"}` and stop.
5. Run `list_issues` (no arguments needed) to get open issues (returns issues labeled `todo` plus issues filed by repo collaborators).
6. Analyze the issues. Prefer issues labeled `todo` — collaborator-filed issues without `todo` are lower priority candidates. For each, assess:
   - **priority**: p0 > p1 > p2 > unlabeled (check labels array)
   - **age**: older issues first (createdAt)
   - **clarity**: is the issue specific enough to plan and execute?
   - **size**: can it be done in a short session (~50 tool calls)?
7. Pick the single best issue: highest priority, then oldest, then clearest.
8. Transition the issue: run `set_issue_labels` with `issue_number` set to the issue number, `add` set to `["doing"]`, `remove` set to `["todo"]`.
9. Write your output.

## Output

Write `o/pick/issue.json`:

For a PR with feedback:

```json
{
  "type": "pr",
  "number": 123,
  "title": "...",
  "body": "...",
  "url": "https://github.com/owner/repo/pull/123",
  "branch": "<headRefName from PR>",
  "reason": "<changes_requested|checks_failing|merge_conflict|changes_requested,checks_failing|...>",
  "reviews": [
    {
      "author": "username",
      "body": "review body text",
      "state": "CHANGES_REQUESTED",
      "submittedAt": "2026-01-01T00:00:00Z",
      "comments": [
        {
          "path": "file.tl",
          "line": 42,
          "body": "inline comment text",
          "createdAt": "2026-01-01T00:00:00Z"
        }
      ]
    }
  ],
  "comments": [...]
}
```

Copy the `reviews` array exactly as returned by `get_prs_with_feedback`, including each review's nested `comments` array (inline review comments). These inline comments contain file-specific feedback that downstream phases need to address.

For an issue:

```json
{
  "type": "issue",
  "number": 123,
  "title": "...",
  "body": "...",
  "url": "https://github.com/owner/repo/issues/123",
  "branch": "work/<number>-<8 random hex chars>"
}
```

The branch name for issues must be `work/<number>-<8 random hex chars>`.

Write `o/pick/reasoning.md`: brief explanation of why this work item was picked over others.

If there are no PRs with feedback and no open todo issues, write `o/pick/issue.json` containing `{"error": "no_issues"}` and explain in reasoning.md.

## Error Handling

When any tool call fails, classify the error and write `o/pick/issue.json` with exactly `{"error": "<code>"}` (no other fields). Use one of these codes:

| code | when to use |
|---|---|
| `no_issues` | no PRs with feedback and no open todo issues found |
| `pr_limit` | more than 4 open PRs |
| `auth_failure` | tool returns 401, 403, "not accessible", "bad credentials", or other authentication/permission errors |
| `api_failure` | tool returns gh CLI or GraphQL errors that are not auth-related (network errors, 5xx, malformed responses) |
| `label_failure` | `ensure_labels` fails (prevents safe pick) |

Classification rules:

- If the error message contains "401", "403", "authentication", "credentials", "not accessible", "permission", or "SAML" → `auth_failure`.
- If `ensure_labels` fails → `label_failure`.
- Any other tool error (gh exit codes, GraphQL errors, timeouts) → `api_failure`.
- Do not invent new error codes. Every failure must map to one of the five codes above.
