---
name: assembling-release-readiness-bundles
description: Use when organizing a release-readiness checklist, signoff bundle, or launch review from a sanitized local file and a reviewable status summary is needed.
---

# Assembling Release Readiness Bundles

Build a local, review-only readiness bundle from normalized checklist records. Keep external-system reads and writes in a separately configured adapter.

1. Run `python scripts/check_prereqs.py`.
2. Provide synthetic or sanitized records with `name`, `owner`, and `status` (`ready` or `attention`).
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Review the generated Markdown bundle before any signoff or publication action.

Never put names, ticket references, URLs, approvals, or captured meeting data in public fixtures.
