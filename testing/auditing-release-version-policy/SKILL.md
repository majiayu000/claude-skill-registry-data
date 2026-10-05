---
name: auditing-release-version-policy
description: Use when checking a generic issue snapshot against a release-version policy and producing reviewable, local-only findings.
---

# Auditing Release-Version Policy

Audit a normalized issue snapshot against a version-format policy, then create local Markdown, HTML, JSON, and draft-message artifacts for human review.

## What this skill does

- Loads a version policy from TOML and issues from a local JSON adapter.
- Identifies missing or noncompliant version values.
- Produces deterministic findings sorted by generic issue key.
- Creates draft remediation messages without contacting any external service.

## Adapter boundary

Supply an array of records with `key`, `status`, and `fix_versions`. Keep connector authentication, URLs, queries, raw responses, page identifiers, and user data outside this public skill. A production integration should map its data into this small generic contract before calling the audit.

## Workflow

1. Run `python scripts/check_prereqs.py`.
2. Review or replace the synthetic TOML policy and JSON snapshot with sanitized input.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Review the local reports and draft messages before taking any action in another system.
5. Run the repository leakage scan before packaging or sharing the skill.

## Safety rules

- Use synthetic issue keys such as `DEMO-200` in examples.
- Keep each output local and treat drafts as review artifacts, never as send instructions.
- Do not add private workflow names, release labels, URLs, email addresses, screenshots, or credentials to fixtures.

## Validation

```powershell
python -m unittest discover -s skills/auditing-release-version-policy/tests -t skills/auditing-release-version-policy -v
```
