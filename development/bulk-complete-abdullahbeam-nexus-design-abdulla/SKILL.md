---
name: bulk-complete
description: Bulk-complete tasks/steps in a project. Load when user says "bulk complete [project]", "mark all done", "complete phase X", or needs to finish project tasks efficiently. Works with both steps.md and tasks.md formats.
---

# Bulk Complete

Efficiently mark tasks complete in project steps.md files.

## When to Use

- User says "bulk complete [project]" or "mark all tasks done"
- User says "complete Phase 2" or "finish Section 3"
- Project work is done, need to mark all steps [x]
- During close-session if project complete (auto-triggered)

## Quick Start

**Auto-detect and run**:
```bash
python scripts/bulk-complete.py --project [ID] --all --no-confirm
```

## Usage Patterns

**Complete all tasks** (project finished):
```bash
python scripts/bulk-complete.py --project 01 --all --no-confirm
```

**Complete specific phase** (phase done):
```bash
python scripts/bulk-complete.py --project 01 --section "Phase 2"
```

**Complete task range** (selective):
```bash
python scripts/bulk-complete.py --project 01 --tasks 1-5,7,10-15
```

**Interactive mode** (pick tasks):
```bash
python scripts/bulk-complete.py --project 01
```

## Script Details

- **Auto-detects**: steps.md (new) OR tasks.md (legacy)
- **Validates**: Re-reads file to confirm completion
- **Cross-platform**: Works on Windows, Mac, Linux
- **Tested**: 27 unit tests, 100% passing

Run `python scripts/bulk-complete.py --help` for all options.

---

**Integration**: Used by close-session skill (Step 2 auto-complete)
