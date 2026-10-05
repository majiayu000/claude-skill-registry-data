---
name: building-static-status-snapshots
description: Use when a live status view is slow, unstable, or unavailable and a dated static snapshot from sanitized local records is needed for review.
---

# Building Static Status Snapshots

Render a local HTML status snapshot from normalized records. This skill creates a review artifact; it does not refresh a remote dashboard or publish a page.

1. Run `python scripts/check_prereqs.py`.
2. Provide `key`, `status`, and ISO `updated` fields through a file adapter.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Review stale entries and the generated snapshot before choosing any follow-up action.

Use synthetic keys and dates in all public examples.
