---
name: reconciling-portfolio-classifications
description: Use when comparing proposed portfolio classifications against existing records and a non-destructive review export is needed before changing any system of record.
---

# Reconciling Portfolio Classifications

Evaluate proposed classifications locally. The workflow returns `update`, `retain`, or `review`; it never overwrites an existing value automatically.

1. Run `python scripts/check_prereqs.py`.
2. Supply sanitized records with `key`, `current`, and `candidates`.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Review every `review` result before configuring an external write adapter.

Public fixtures must use generic values and synthetic keys only.
