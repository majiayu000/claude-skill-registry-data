---
name: opsx-bulk-archive
description: Archive multiple completed changes at once. Use when user wants to archive several changes in one operation.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
---

Archive multiple completed changes at once.

**Input**: Optionally specify change names. If omitted, prompt for selection.

**Steps**

1. **Get active changes**
   ```bash
   openspec list --json
   ```

2. **Select changes to archive**
   Use **AskUserQuestion tool** with multiSelect for multiple selections.

3. **For each selected change:**
   - Verify all tasks complete
   - Check delta specs sync status
   - Move to archive: `openspec/changes/<name>` → `openspec/changes/archive/YYYY-MM-DD-<name>`

4. **Show summary**

**Output**

```
## Bulk Archive Complete

**Archived:** [list of change names]

All changes have been moved to the archive.
```