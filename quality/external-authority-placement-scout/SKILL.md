---
name: external-authority-placement-scout
description: Find and score legitimate external authority and backlink opportunities as a dry-run register, using relevance, platform rules, risk, target-page fit, and explicit user approval gates. Use this skill when the user asks where links to a target site could be placed effectively, but never post, submit, DM, email, open PRs, or edit external accounts without separate explicit approval.
---

# External Authority Placement Scout

Use this skill only after the white-hat authority policy exists.

Read `./plans/seo-llm-skill-cluster/authority/white-hat-authority-policy.md`
before creating an opportunity register.

Read [references/scouting-workflow.md](references/scouting-workflow.md) for candidate sources,
required register fields, and draft rules.

## Owns

- dry-run opportunity discovery;
- opportunity register rows;
- relevance and target-fit scoring;
- platform-rule checklist;
- approval-gated outreach or submission drafts;
- handoff to backlink-quality-validator.

## Does Not Own

- external posting;
- account edits;
- PR creation;
- email/DM sending;
- buying links;
- spam automation;
- final quality validation after a link exists.

## Workflow

1. Define target site, target pages, audience, and allowed opportunity categories.
2. Collect candidate opportunities from user-provided platforms or approved public research.
3. Check relevance, user value, target fit, and policy risk.
4. Record platform-rule status and whether current official/public rules must be rechecked.
5. Create register rows matching the opportunity schema.
6. Draft optional human-review text only when useful.
7. Require explicit user approval before any external action.
8. Hand off existing or proposed placements to `backlink-quality-validator`.

## Non-Negotiables

- Dry-run by default.
- Do not post links anywhere.
- Do not open PRs.
- Do not send outreach.
- Do not create accounts.
- Do not recommend PBNs, link farms, fake reviews, fake accounts, mass profile creation, hidden links, or irrelevant directories.
- Do not use exact-match anchor stuffing.
- Do not claim authority impact without evidence.

## Safety And Privacy Boundaries

- Do not store platform credentials, private messages, contact lists, cookies, or tokens.
- Do not scrape platforms against their rules.
- Do not include private account data in reports.
- If the user approves a future external action, create a separate task with platform, draft, approval, rollback/removal path, and monitoring plan.

## Output Shape

Return:

1. Scope and target pages.
2. Opportunity register table.
3. Scoring rationale.
4. Platform-rule status and verification needs.
5. Draft text if requested, clearly marked as draft only.
6. Blocked opportunities and reasons.
7. Approval required before action.

## Validation

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/external-authority-placement-scout
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).
