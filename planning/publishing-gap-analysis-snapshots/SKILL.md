---
name: publishing-gap-analysis-snapshots
description: Use when comparing two sanitized catalogs or planning snapshots and a reviewable, static gap report is needed before updating any source system or publication.
---

# Publishing Gap Analysis Snapshots

Compare two local catalogs and render a static report of values unique to each side. This skill intentionally separates analysis from any external update or publishing action.

1. Run `python scripts/check_prereqs.py`.
2. Provide two sanitized catalog lists through a local adapter.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Review add/remove candidates before configuring an external writer.

Do not include live exports, organization labels, product codes, URLs, issue IDs, or credentials in public artifacts.
