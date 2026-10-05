---
name: opsx-continue
description: Continue implementing tasks from an OpenSpec change. Use when user wants to resume work on an existing change.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
---

Continue implementing tasks from an OpenSpec change.

**Input**: Optionally specify a change name. If omitted, check for active changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Check conversation context for mentioned change
   - Auto-select if only one active change exists
   - If ambiguous, run `openspec list --json` and use **AskUserQuestion tool** to select

   Announce: "Continuing with change: <name>"

2. **Check current status**
   ```bash
   openspec status --change "<name>" --json
   ```

3. **Get apply instructions**
   ```bash
   openspec instructions apply --change "<name>" --json
   ```

4. **Read context files** (from contextFiles in instructions)

5. **Show progress** and continue implementing remaining tasks

**Output**

```
## Continuing: <change-name>

Progress: N/M tasks complete
Working on: <current task>
...
```

If all done: "All tasks complete! Use `/opsx:archive` to close this change."