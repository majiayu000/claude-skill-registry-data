---
name: orchestrating-cross-tool-rollouts
description: Use when coordinating a multi-system launch, announcement, or operational rollout and a dependency-ordered, review-gated runbook is needed before any external action.
---

# Orchestrating Cross-Tool Rollouts

Produce a deterministic rollout runbook from generic dependency records. The skill plans local work only: configure each external-system adapter separately and obtain approval before any write or send.

1. Run `python scripts/check_prereqs.py`.
2. Provide step IDs and explicit dependencies in a sanitized JSON file.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Review the ordered runbook and approve each external action independently.

Do not put user lists, channels, message contents, credentials, or source URLs in public fixtures.
