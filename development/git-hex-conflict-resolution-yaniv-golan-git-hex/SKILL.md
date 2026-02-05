---
name: git-hex-conflict-resolution
description: >
  This skill should be used when the user is stuck in a git-hex-driven rebase,
  merge, or cherry-pick due to conflicts and wants the agent to inspect, resolve,
  and then continue or abort safely. Trigger phrases include: "resolve conflicts",
  "rebase is stuck", "conflict markers", "continue the rebase", "abort the rebase".
---

# Git-hex Conflict Resolution

## When to use this Skill

This skill should be used when:

- A git-hex tool reports that an operation is paused because of conflicts.
- The user says a rebase or cherry-pick is "stuck", "paused", or "in conflict".
- You need to see which files conflict and decide whether to continue or abort.

Trigger phrases include: "rebase conflict", "cherry-pick conflict", "merge conflict",
"stuck on conflicts", "continue the rebase", "abort the cherry-pick".

## Workflow

1. **Inspect conflict state**
   - Call `git-hex-getConflictStatus` to determine:
     - Whether a rebase/merge/cherry-pick/revert is in progress.
     - Which files are conflicting and the overall operation type (`rebase`,
       `merge`, `cherry-pick`, or `revert`).
   - Use `includeContent: true` only when necessary to inspect base/ours/theirs
     content for specific text files.

2. **Resolve conflicts per file**
   - For text files:
     - Propose or apply edits based on `base`, `ours`, and `theirs`.
     - Ensure conflict markers are removed before resolving.
     - Call `git-hex-resolveConflict` with the file path (and `resolution: "delete"`
       for delete conflicts when appropriate).
  - For delete conflicts, use the `resolution` parameter to choose whether
     to keep or remove the file.

3. **Continue or abort the operation**
   - When all conflicts are resolved (or `getConflictStatus` shows no remaining
     conflicting files but the operation is still paused), call `git-hex-continueOperation`.
   - If the user decides to give up on the rebase or cherry-pick, call
     `git-hex-abortOperation` to restore the pre-operation state.

4. **Escalate if needed**
   - If the final result after continuing is not what the user wanted, suggest
     using `git-hex-undoLast` from the branch cleanup Skill to revert.

## Tools to prefer

- Inspection: `git-hex-getConflictStatus`
- Resolution: `git-hex-resolveConflict`
- Control: `git-hex-continueOperation`, `git-hex-abortOperation`
- Recovery: `git-hex-undoLast` (via the branch cleanup Skill)

## Conflict types

### Operation-level
- `"rebase"` - Interactive rebase paused
- `"merge"` - Merge in progress
- `"cherry-pick"` - Cherry-pick paused
- `"revert"` - Revert paused (detected but `continueOperation`/`abortOperation` are not supported; use `git revert --continue` or `--abort` directly)

### File-level
- `"both_modified"` - Both sides modified the file
- `"deleted_by_us"` - We deleted, they modified
- `"deleted_by_them"` - We modified, they deleted
- `"added_by_both"` - Both sides added different versions

## Delete conflict handling

```json
// To keep the file (must exist on disk):
{ "file": "path/to/file", "resolution": "keep" }

// To accept deletion:
{ "file": "path/to/file", "resolution": "delete" }
```
