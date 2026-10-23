---
name: changes-explain
description: Explain a pull request, commit range, branch, or local diff from a system-design perspective. Use for practical understanding of changed behavior, boundaries, flow, ownership, operations, risks, and verification rather than defect review.
---

# Explain Changes

Translate one code comparison into its effects on the system, without inventing intent or exposing sensitive content.

## Workflow

1. Fix the comparison. For a branch or pull request, compare against the merge base (`git diff <base>...<head>`, or `gh pr diff`), not the current tip of the base branch. For local work, include staged, unstaged, and untracked files. If the scope cannot be isolated, say so and qualify the explanation.
2. Read the diff, the full changed files, the surrounding code they depend on, the tests, the configuration, and any linked brief that is in scope.
3. Group the edits by changed behavior or responsibility, not by file.
4. For each group, explain the previous and new behavior, the affected owner or boundary, the data and control flow, the external interactions, and the effects on users, developers, runtime, or operations.
5. Describe changed failure handling, compatibility, rollout, CI, verification, and remaining risk where the change alters them.
6. Mark what you observed in code, what the documentation or pull request says was intended, and what you infer.

Keep the task read-only. Redact secrets and sensitive diff content. Use `code-review` for defect findings and `rollout-readiness-review` for an operational-readiness judgment.

## Result

Start with a short summary of the overall change, then explain each group. Omit syntax trivia and empty sections. Finish when every material group is explained and the evidence limits are stated.
