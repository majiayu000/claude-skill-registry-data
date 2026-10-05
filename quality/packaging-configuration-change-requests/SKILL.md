---
name: packaging-configuration-change-requests
description: Use when converting a configuration change into a complete, reviewable request package with explicit scope and acceptance criteria before any environment change is made.
---

# Packaging Configuration Change Requests

Validate a local request package before sending it to an independently configured change-management system. This skill creates drafts only and never changes configuration.

1. Run `python scripts/check_prereqs.py`.
2. Provide a sanitized request with `id`, `title`, `scope`, and `acceptance`.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Resolve missing fields and obtain change approval before using another system.

Do not include real service names, tenant details, field identifiers, screenshots, tickets, or credentials in public examples.
