---
name: release-management
description: "Use when planning, coordinating, or governing Salesforce releases: version numbering, rollback strategy, release notes, go/no-go criteria, release calendar, and sandbox preview alignment. NOT for deployment mechanics (use devops/post-deployment-validation or devops/change-set-deployment)."
category: devops
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
triggers:
  - "how do I plan a Salesforce release and define go/no-go criteria"
  - "what is the rollback strategy if a production deployment fails"
  - "how do I version Salesforce metadata in an org-based project"
  - "how do I use quick deploy to speed up deployment night"
  - "our deployment is happening near the Salesforce seasonal release upgrade"
tags:
  - release-management
  - release-planning
  - rollback
  - versioning
  - devops
inputs:
  - "Deployment target (production, partial sandbox, scratch org)"
  - "List of changes in the release (components, Apex, config)"
  - "Salesforce edition and Dev Hub availability"
  - "Release calendar constraints (freeze windows, go-live date)"
outputs:
  - "Release plan document with version number, go/no-go criteria, rollback trigger definition, and smoke test checklist"
  - "Release notes template populated with changes"
  - "Post-release validation checklist"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Release Management

This skill activates when a practitioner needs to plan, coordinate, or govern a Salesforce release cycle — covering version numbering schemes, rollback strategy, release notes generation, go/no-go criteria, and release calendar alignment with Salesforce's three seasonal platform releases per year.

---

## Before Starting

Gather this context before working on anything in this domain:

- Determine whether the project is org-based (change sets, SFDX org-deploy) or artifact-based (unlocked packages, 2GP managed packages). Version numbering and rollback differ fundamentally between the two.
- Confirm the Salesforce seasonal release schedule. Salesforce releases three times per year (Spring, Summer, Winter). Sandbox preview opens approximately 4–6 weeks before the production release weekend. Changes deployed just before preview may be disrupted by platform changes.
- Identify which environments are in scope: production org, Full/Partial/Developer sandboxes, scratch orgs. Each has different data and metadata state implications for rollback.

---

## Core Concepts

### Seasonal Platform Releases and Sandbox Preview

Salesforce delivers three named releases per year (e.g., Spring '25, Summer '25, Winter '26). Each release upgrades all production orgs on a staggered weekend schedule (NA pods first, then EMEA, then APAC). Before production upgrade, Salesforce opens a sandbox preview window — typically 4–6 weeks before the production weekend. Orgs opted into preview receive the new release early.

Practical impact: any release you plan to deploy to production in the 2-week window immediately preceding the production upgrade weekend is high risk. Test in a preview sandbox if your deployment overlaps with a platform upgrade.

### Versioning Schemes by Deployment Model

**Org-based projects** (change sets, `sf project deploy start`): The platform has no native version number for org metadata. Teams must define their own convention. Common approaches:
- Git tag with `vYYYY.MM.DD-N` (date + sequence)
- Jira/Linear release milestone label
- Custom object to track deployed versions

**Unlocked packages**: Version numbers are `Major.Minor.Patch.Build`. Only Major.Minor.Patch are user-controlled; Build auto-increments. The `sf package version create` command creates a new immutable version. The version ancestry is linear — you cannot branch and merge package versions.

**2GP managed packages**: Same `Major.Minor.Patch.Build` scheme. Patch versions require a patch org created from the specific version being patched (`sf package version create --package-id 04t...`).

### Rollback Strategy

Salesforce has no native undo button for metadata deployments. Rollback means:
1. Pre-deploy: retrieve and archive the current state of every component you are deploying.
2. Post-deploy failure: redeploy the archived version.
3. For org-based: run `sf project deploy start --manifest pre-release-backup.xml` pointing at your archived source.
4. For unlocked packages: install the prior qualified package version with `sf package install --package 04t<prior-version-id>`.

Data changes made by the released code cannot be rolled back by redeploying metadata. Identify data mutations in your release notes and plan compensating data fixes if rollback is needed.

### Go/No-Go Criteria

A go/no-go gate blocks deployment unless defined criteria pass. Typical criteria:
- All Apex tests pass with ≥75% org-wide coverage (RunLocalTests) or ≥75% per-class/trigger coverage (RunSpecifiedTests).
- Smoke test checklist passes in a Full sandbox that mirrors production.
- Zero open Severity 1 defects from UAT.
- Deployment validation (`sf project deploy validate`) completed successfully within the last 10 days (enables Quick Deploy).
- Release notes reviewed and signed off by product owner.

---

## Common Patterns

### Validation Deploy + Quick Deploy

**When to use:** Large orgs where running full Apex test suite takes 30–90 minutes. You want deployment weekend to be fast.

**How it works:**
1. Run `sf project deploy validate --source-dir force-app --test-level RunLocalTests --async` against production before the go-live window (within 10 days).
2. Save the returned deploy ID.
3. On deployment night, run `sf project deploy quick --job-id <validatedDeployID>` — this skips the full test run and completes in minutes.

**Why not just deploy directly:** Validation gives you a rehearsal. If it fails, you have days to fix. If you deploy directly and it fails at 2am, you are in a crisis.

### Freeze Window Coordination

**When to use:** Shared production org with multiple teams and competing deployment schedules.

**How it works:**
1. Publish a release calendar with named code freeze dates. Code freeze = no new feature branch merges to main/release.
2. Only hotfixes (P1/P2) are allowed after code freeze.
3. Define the freeze period: typically 3–5 business days before deployment weekend.
4. Use a shared DevOps Center pipeline or a Jira board column to signal freeze status.

**Rollback trigger:** Define trigger conditions in writing before deployment begins — for example: "If any Apex test fails in production post-deploy, or if >3 Sev-1 defects are raised within 2 hours, rollback is initiated."

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Org-based project, versioning needed | Git tag + internal version custom object | No native version support; git tag provides retrieval anchor for rollback |
| Unlocked package, need to patch a GA version | Create patch org from prior version ID, increment Patch number | 2GP patch orgs are immutable snapshots; cannot merge changes into old version |
| Release overlaps with Salesforce upgrade weekend | Test in preview sandbox first, consider delaying by 1 week | Platform changes may break your code or reveal regressions |
| Need fast deployment night with large test suite | Validation deploy 3–7 days early, Quick Deploy on the night | Quick Deploy skips tests, uses 10-day validated ID |
| Multiple teams sharing one production org | Coordinated release train with shared freeze calendar | Competing deploys cause cross-reference errors and test failures |

---

## Recommended Workflow

1. Confirm deployment model (org-based vs package-based) and define the versioning convention for this project before any release is cut.
2. Check the Salesforce release calendar at trust.salesforce.com and flag any overlap between your planned deployment date and the seasonal upgrade weekend.
3. Build the release notes from the component list: list each component changed, the reason for the change, and any data migration steps.
4. Run a validation deploy (`sf project deploy validate`) against production at least 3 days before go-live. Resolve all failures.
5. Conduct UAT sign-off in a Full sandbox with the exact build being deployed. Close Sev-1 and Sev-2 defects before proceeding.
6. Execute deployment using Quick Deploy if within 10-day window; otherwise re-run full deploy.
7. Execute the post-deploy smoke test checklist and confirm all go/no-go criteria pass. If a rollback trigger fires, redeploy the pre-release archived version immediately.

---

## Review Checklist

- [ ] Version number is defined and recorded in git tag / release notes / version tracking object
- [ ] Salesforce upgrade weekend checked against planned deployment date
- [ ] Validation deploy passed against production within the last 10 days
- [ ] UAT completed with full sign-off; zero open Sev-1 defects
- [ ] Rollback archive retrieved and stored before deployment begins
- [ ] Post-deploy smoke test checklist executed and all checks pass
- [ ] Release notes distributed to stakeholders before go-live

---

## Salesforce-Specific Gotchas

1. **Quick Deploy uses a new deploy ID** — the `sf project deploy quick` command returns a NEW deploy request ID, not the validation ID. Monitor the new ID for status. Teams that poll the old validation ID will see it as Succeeded (it was) while the actual quick deploy is running.
2. **RunSpecifiedTests is stricter than RunLocalTests** — when you specify individual test classes, Salesforce requires 75% coverage per class AND per trigger in the deployed package, not just org-wide. This catches coverage gaps that RunLocalTests would miss.
3. **Sandbox preview opt-in is per-sandbox** — only sandboxes explicitly opted into the preview release receive it early. Your development sandbox may be on the new release while production is still on the prior one, causing metadata shape mismatches if you deploy preview-era metadata to a non-preview production.
4. **Rollback cannot undo data changes** — redeploying previous metadata does not reverse DML executed by the released code. Document every data mutation in release notes and prepare compensating scripts.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Release plan document | Version number, scope, deployment date, rollback trigger definition, go/no-go criteria sign-off |
| Release notes | Component change log, data migration steps, known issues, stakeholder communication |
| Pre-release backup manifest | package.xml listing every component being changed; used as rollback input |
| Post-deploy smoke test checklist | Ordered list of manual verifications to execute immediately after deployment |

---

## Related Skills

- devops/post-deployment-validation — validation deploy mechanics and Quick Deploy commands
- devops/change-set-deployment — org-based deployment when SFDX is not in use
- devops/continuous-integration-testing — automated test execution in CI, coverage gates
- devops/environment-strategy — sandbox strategy and environment topology decisions
