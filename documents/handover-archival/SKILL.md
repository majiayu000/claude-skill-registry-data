---
name: handover-archival
description: Use when finishing a handover document or searching for past work context - marks handovers complete and knows where archived handovers live
---

# Handover Archival

## Overview

Handovers are **permanent historical artifacts**, not temporary files. When work completes, mark the status and let CI archive it.

## When Work is Complete

Add this marker near the top of the handover (within first 20 lines):

```markdown
## Status: Complete
```

**Do NOT:**
- Delete handover documents (history is valuable)
- Manually move files (CI script handles this)

## Finding Past Context

| Location | Contents |
|----------|----------|
| `ai_docs/Handovers/` | Active, in-progress handovers |
| `ai_docs/Handovers/Completed/` | **68+ archived handovers** - search here for past work |

## Archival Script

```bash
# Dry run - see what would be archived
python scripts/archive_completed_handovers.py

# Actually move completed handovers
python scripts/archive_completed_handovers.py --apply
```

The script scans for `## Status: Complete` (case-insensitive) and uses `git mv` to archive.
