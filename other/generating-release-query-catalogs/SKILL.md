---
name: generating-release-query-catalogs
description: Use when generating a release-scoped query catalog from reusable, sanitized query templates and a local review artifact is needed before creating saved queries in any external system.
---

# Generating Release Query Catalogs

Render a local catalog from approved query templates. This skill does not authenticate to, create, or share external saved queries.

1. Run `python scripts/check_prereqs.py`.
2. Provide generic query templates that use only the `{{release}}` placeholder.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Review rendered query text before an independently configured external adapter creates anything.

Do not include project names, field identifiers, URLs, user groups, or authorization configuration in public templates.
