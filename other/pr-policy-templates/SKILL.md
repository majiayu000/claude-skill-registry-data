---
name: pr-policy-templates
description: "Enforce change quality via PR templates, required reviews, metadata ownership, and automated checks. NOT for branching model selection."
category: devops
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
triggers:
  - "pr template salesforce"
  - "codeowners metadata"
  - "required pr checks salesforce"
  - "enforce test coverage pr"
tags:
  - pr
  - github
  - codeowners
  - governance
inputs:
  - "team topology"
  - "coverage SLA"
outputs:
  - "PR template, CODEOWNERS, branch protection config"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# Pull Request Policy Templates

A consistent PR template + CODEOWNERS + required checks shifts quality left. This skill defines a template with sections for scope, test evidence, deploy plan, and risk; a CODEOWNERS matching metadata types to owning teams; and branch-protection rules requiring status checks (validation deploy, test run, scan).

## When to Use

Teams >3 people; regulated or production-critical repos.

Typical trigger phrases that should route to this skill: `pr template salesforce`, `codeowners metadata`, `required pr checks salesforce`, `enforce test coverage pr`.

## Recommended Workflow

1. Write `.github/pull_request_template.md` with Scope, Test Evidence, Deploy Plan, Rollback, and Risk sections.
2. Create `.github/CODEOWNERS` mapping `force-app/main/default/flows/` to @flow-team, `classes/` to @apex-team, etc.
3. Enable branch protection: require PR + 1 review + all required checks green + CODEOWNERS approval.
4. Wire required status checks: validation deploy, Apex test run ≥75%, PMD/Checkmarx scan.
5. Quarterly: audit merged PRs; measure cycle time and revert rate; tune policy.

## Key Considerations

- CODEOWNERS with @team handles scales better than individual usernames.
- Coverage can be blocker or soft warning — pick one and enforce consistently.
- Squash-merge keeps history clean; but preserve deploy traceability with merge commits.
- Template must be ≤1 screen — long templates get ignored.

## Worked Examples (see `references/examples.md`)

- *CODEOWNERS mapping* — Flow changes route to flow team
- *Required check: validation deploy* — Prevent 'works in dev' surprises

## Common Gotchas (see `references/gotchas.md`)

- **CODEOWNERS without team** — User leaves; PRs stuck.
- **Template too long** — Authors delete it.
- **Coverage check both warn+block inconsistent** — Confusion.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- Optional PR template (unused)
- CODEOWNERS with personal accounts
- No validation deploy gate

## Official Sources Used

- Salesforce DX Developer Guide — https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/
- Unlocked Packaging — https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_dev2gp.htm
- SF CLI — https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/
- DevOps Center — https://help.salesforce.com/s/articleView?id=sf.devops_center_overview.htm
- Scratch Org Snapshots — https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_scratch_orgs_snapshots.htm
- sfdx-hardis — https://sfdx-hardis.cloudity.com/
