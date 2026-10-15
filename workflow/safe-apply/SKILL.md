---
name: safe-apply
description: "Sort a change proposal into safe mechanical items and items needing human judgment. Do NOT use to apply the changes."
---

# safe-apply

Cross-cutting approval-workflow atom: takes a change proposal and categorization rules, returns two lists — safe changes (mechanical, auto-appliable) and risky changes (judgment, human-review-required). Reduces duplication across feed-curator, skill-repair, and standards-updater.

## Input

```json
{
  "change_proposal": [
    {"action": "remove", "target": "dead-feed-url", "reason": "HTTP 404", "evidence": {"http_code": 404}},
    {"action": "add", "target": "new-feed-url", "reason": "discovered via autodiscovery"},
    {"action": "update_label", "target": "existing-feed", "old_value": "secondary", "new_value": "primary"}
  ],
  "safe_rules": {
    "remove": {"if_evidence_http_code": [404, 410]},
    "add": {"if_source": "verified_discovery"},
    "update_label": "never_auto_apply"
  }
}
```

## Output

```json
{
  "tool": "safe-apply",
  "safe_changes": [
    {"action": "remove", "target": "dead-feed-url", "reason": "confirmed 404", "rule_matched": "remove.if_evidence_http_code"}
  ],
  "risky_changes": [
    {"action": "add", "target": "new-feed-url", "reason": "needs human verification", "why_risky": "source not in verified_discovery"},
    {"action": "update_label", "target": "existing-feed", "why_risky": "label changes are never auto-applied"}
  ],
  "summary": "1 safe (auto-apply), 2 risky (human review)",
  "human_review_required": true
}
```

## Do NOT use this atom for
- Actually applying changes (this atom classifies, the orchestrator applies)
- Content generation or editing
- Security scanning (use tools/security_scan.py)

## Pipeline note
Follows `references/method.md` at the Validation step (change categorization). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — even mechanical changes should be reviewed in aggregate before commit.
