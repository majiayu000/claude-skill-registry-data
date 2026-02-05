---
name: embedding-repair
description: Diagnose and repair embedding model availability and MSHR index health; use when embedding errors, dimension mismatches, or rebuild failures appear.
---

# Embedding Repair

Use this skill to diagnose missing embedding backends and rebuild MSHR indexes safely.

## Workflow

1) Run the repair script:

```bash
python skills/conscience/embedding-repair/scripts/repair_embeddings.py
```

2) If models are missing, report the failure and recommend installing the required embedding backend.
3) The script stores a semantic memory entry with results and errors.
