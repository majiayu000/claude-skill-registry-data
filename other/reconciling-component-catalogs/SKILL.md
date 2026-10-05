---
name: reconciling-component-catalogs
description: Use when comparing canonical and observed component catalogs, including casing or spacing differences, and reviewable add, remove, and normalization recommendations are needed.
---

# Reconciling Component Catalogs

Create a local component-catalog reconciliation. Results are recommendations only: no ticket, component, or message changes occur in this skill.

1. Run `python scripts/check_prereqs.py`.
2. Provide sanitized `canonical` and `observed` lists from a file adapter.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Review additions, removals, and normalization candidates before any external update.

Use generic labels and synthetic records in public examples.
