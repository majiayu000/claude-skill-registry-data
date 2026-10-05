---
name: opsx-verify
description: Verify an OpenSpec change is complete and ready. Use when user wants to check if a change is ready for archive or implementation.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
---

Verify an OpenSpec change is complete and ready.

**Input**: Optionally specify a change name. If omitted, prompt for selection.

**Steps**

1. **Select the change**
   Run `openspec list --json` and let user select if not provided.

2. **Run validation**
   ```bash
   openspec validate <change-name> --json
   ```

3. **Check artifact status**
   ```bash
   openspec status --change "<name>" --json
   ```

4. **Show verification results**

**Output**

```
## Verification Results

**Change:** <name>
**Status:** ✓ Valid / ✗ Invalid

Artifacts: N/M complete
Tasks: N/M complete

[Details if issues found]
```