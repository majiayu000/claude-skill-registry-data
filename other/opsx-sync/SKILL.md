---
name: opsx-sync
description: Sync delta specs from a change to main specs. Use when user wants to apply delta specs from a change to the main specs directory.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
---

Sync delta specs from a change to the main specs directory.

**Input**: Change name (required).

**Steps**

1. **Select the change**
   Use provided name or prompt via `openspec list --json`.

2. **Check for delta specs**
   Look for `openspec/changes/<name>/specs/` directory.

3. **Sync each delta spec**
   Compare delta spec with corresponding main spec at `openspec/specs/<capability>/spec.md`.
   Apply changes (adds, modifications, removals).

4. **Show summary**

**Output**

```
## Spec Sync Complete

**Change:** <name>
**Synced specs:** [list]

Delta specs have been applied to main specs.
```