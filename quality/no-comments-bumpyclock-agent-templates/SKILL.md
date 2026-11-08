---
name: no-comments
description: Review and remove unnecessary comments while preserving unresolved constraints.
disable-model-invocation: true
---

# No comments

Use the caller's files or diff. Otherwise review the current branch diff, including the worktree.
Keep unrelated code and user edits outside the scope.

Use Comment Sicko for a bounded read-only review when that role is available and an independent perspective helps.
Otherwise inspect directly.
Treat the review as evidence to assess, not permission to accept every deletion.

Use the [shared comment policy](../../../defaults/AGENTS.md#code-clarity-and-comments) to assess each candidate deletion.
Keep an ambiguous comment until evidence resolves its purpose.
Do not treat uncertainty as a reason to delete.

When a constraint can use a type, runtime check, test, or lint, propose the smallest in-scope enforcement.
If the user approves that implementation, validate the enforcement before removing the redundant comment.
If approval is absent or the root cause is outside scope, retain the comment and report the unresolved constraint.

Do not turn a comment cleanup into an architecture exercise or unrelated code repair.
Use additional investigation only to resolve a consequential uncertainty.
Validate affected contracts when a change can affect behavior or tool directives.
Report accepted deletions, retained constraints, and validation limits.
