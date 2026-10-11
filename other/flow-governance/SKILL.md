---
name: flow-governance
description: "Use when establishing operational standards for a Salesforce Flow portfolio, including naming conventions, ownership, version discipline, retirement of stale flows, and release readiness checks. Triggers: 'flow naming convention', 'too many old flows', 'who owns this flow', 'flow version governance'. NOT for element-by-element flow logic design or dedicated fault-handling review."
category: flow
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - Operational Excellence
tags:
  - flow-governance
  - naming-conventions
  - version-management
  - ownership
  - flow-standards
triggers:
  - "how should we govern flows in the org"
  - "flow naming convention and ownership"
  - "too many stale flow versions"
  - "who owns this automation"
  - "flow release readiness checklist"
inputs:
  - "how many flows exist, which teams own them, and where operational confusion appears today"
  - "current naming, documentation, and activation practices"
  - "how releases, testing, and retirement decisions are currently made"
outputs:
  - "governance standard for naming, ownership, and lifecycle management"
  - "review findings for stale, weakly named, or undocumented flows"
  - "release checklist for safe activation and retirement decisions"
dependencies: []
version: 2.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

Use this skill when the problem is no longer one flow, but the portfolio of flows in the org. Governance matters once teams start asking which flow is active, who owns it, why two versions exist, or whether a copied automation can be retired safely. Good governance turns Flow from a sprawl risk into an operable platform capability.

This skill is the companion to technical-depth skills like `flow/fault-handling` and `flow/flow-bulkification` — those make individual flows good; this one makes the portfolio operable. Portfolio-level failures (no owner, 47 versions of the same flow, nobody knows what's active) produce the incidents that technical-depth skills can't prevent.

---

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- How many flows exist today? (Rough count; exact via `list_flows_on_object` or tooling query.)
- How are flows named today, and do labels, API names, descriptions, and interview labels help or confuse operators?
- Who owns activation, deactivation, and release approval for production flows?
- Which pain is most acute right now: duplicate automations, stale versions, weak documentation, unclear support ownership?
- Does the org have a change-management process (CAB, release train)? If yes, Flow governance plugs into it.

---

## Core Concepts

Flow governance is about operational clarity. A well-built flow that nobody can identify, safely activate, or retire is still a platform liability. Naming, ownership, description quality, and version discipline are not paperwork. They are what allow admins, support teams, and delivery teams to understand the automation surface they are changing.

### Names Need To Describe Purpose, Not History

Labels like `New Flow`, `Copy of Case Process`, or `Test Version 7` tell the next maintainer almost nothing. Strong naming conventions encode domain, business purpose, and trigger type well enough that an operator can tell what the flow is for before opening it.

**Recommended naming pattern (per `templates/admin/naming-conventions.md`):**

```
<Object>_<TriggerType>_<PurposeVerbPhrase>_v<N>
```

Examples:
- `Opportunity_BeforeSave_SetDefaultOwner_v1`
- `Case_AfterSave_CreateSLAMilestone_v3`
- `Lead_Scheduled_AgeOutCleanup_v1`
- `Global_Autolaunched_EmailDomainCheck_v2`

Parts:
- **Object** — the sObject the flow fires on (or `Global` if object-agnostic).
- **TriggerType** — `BeforeSave` / `AfterSave` / `Scheduled` / `Autolaunched` / `Screen` / `Orchestration`.
- **PurposeVerbPhrase** — what the flow DOES, in UpperCamelCase.
- **Version suffix (optional)** — explicit version when the flow has iterated.

### Ownership Must Be Visible

Every production flow should have an accountable owner or owning team, even if several contributors edit it over time. When a failure, deployment question, or retirement opportunity appears, support should not need archaeology to find the right decision-maker.

**Ownership metadata surfaces:**
- **Description field** — "Owner: sales-ops team. Escalate to: @alice.johnson. Purpose: …"
- **Custom metadata type** — `Flow_Ownership__mdt` keyed by flow DeveloperName; supports bulk reporting.
- **Git commit history** — LastModifiedBy surfaces the latest editor, not the long-term owner.
- **Team's team-by-team wiki** — external to Salesforce but often the pragmatic answer.

Pick ONE canonical source and enforce it. Multiple sources of truth = no source of truth.

### Version Discipline Prevents Automation Drift

Flow versions accumulate easily. Without activation standards and retirement reviews, old inactive versions and copied replacements obscure the true production path. Governance is what turns versioning from a safety feature into a manageable lifecycle.

**Version retention standard:**
- Keep current active version + 1 previous (for emergency rollback).
- After 2 releases since a version was active, delete it.
- Inactive versions > 90 days old and > 2 versions behind are retirement candidates.

### Documentation Should Support Operations

Descriptions, interview labels, release notes, and test intent should make logs and deployment review more understandable. Operational documentation is not a separate project from the flow. It is part of the flow's maintainability.

Required documentation per flow:
- **Description** — 2-3 sentences on purpose, owner, escalation.
- **Element labels** — readable enough to make Flow Interview Log entries interpretable.
- **Fault-path routing** — documented via `flow/fault-handling`.
- **Version-change notes** — when bumping the `_vN` suffix, explain why in the description.

---

## Common Patterns

### Pattern 1: Domain-Purpose Naming Standard

**When to use:** The org has enough flows that labels and API names are becoming ambiguous.

**Structure:** Define naming rules per the recommended pattern above. Apply to new and revised flows. For existing drift, run a rename cleanup during the next deploy window.

### Pattern 2: Activation Gate With Named Owner

**When to use:** Teams frequently activate flows without clear support responsibility or regression review.

**Structure:** Required before activating any production flow:
1. Named owner (in description + custom metadata).
2. Summary of change (in change-management ticket + flow description update).
3. Test evidence (Flow Tests passing + sandbox smoke screenshot).
4. Rollback approach (previous active version preserved, or documented disable/revert plan).

### Pattern 3: Periodic Retirement Review

**When to use:** The org has many inactive copies, superseded automations, or uncertainty about what is still in use.

**Structure:**
1. Quarterly inventory: `tooling_query` on `Flow` + `FlowDefinition` to list all flows with activation state + last modified.
2. Classify: `active_production`, `active_sandbox_only`, `deprecated_keep_for_reference`, `retire_now`.
3. For `retire_now`: delete the metadata in the next deploy.
4. For `active_sandbox_only`: verify sandbox is still in use; delete if not.
5. Emit portfolio metrics: total flows, active production count, per-team distribution, age distribution.

### Pattern 4: Flow Ownership Custom Metadata Type

**When to use:** Org has > 50 flows and the description-field approach is getting unwieldy.

**Structure:** Custom Metadata type `Flow_Ownership__mdt` with fields:
- `Flow_Developer_Name__c` (match to `FlowDefinition.DeveloperName`)
- `Owning_Team__c`
- `Escalation_Contact__c`
- `Business_Purpose__c`
- `Deprecated__c` (boolean)
- `Retirement_Target_Date__c`

Enables: dashboard-driven governance, cross-flow owner lookup, bulk-retirement planning.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| New production flow being introduced | Apply naming, owner, description, activation standards immediately | Governance easiest at creation time |
| Existing portfolio has many ambiguous labels | Run a focused inventory and rename plan (Pattern 1) | Operators need a readable automation map |
| Multiple inactive copies exist, unclear active path | Retirement review (Pattern 3) before more changes land | Flow sprawl compounds quickly |
| Teams activate flows ad hoc | Activation gate (Pattern 2) | Reduces support surprises |
| A flow is technically correct but poorly documented | Treat documentation as part of the fix | Operational clarity is a functional requirement |
| Org has > 50 flows and per-flow description isn't scaling | Custom Metadata governance (Pattern 4) | Structured governance data for dashboards |

---

## Well-Architected Pillar Mapping

This skill is wholly in the **Operational Excellence** pillar. Governance findings are OpsEx findings; governance wins are OpsEx wins. No Reliability/Security/Scalability overlap — those concerns belong to other flow/* skills.

## Review Checklist

- [ ] Flow label and API name describe purpose clearly.
- [ ] A support or product owner is identified (in description, custom metadata, or wiki).
- [ ] Flow description explains business purpose and notable dependencies.
- [ ] Activation and rollback expectations documented.
- [ ] Superseded or duplicate flows reviewed for retirement.
- [ ] Logs and interview labels readable enough for support use.
- [ ] Version count is bounded (≤ 2 historical inactive versions per flow).
- [ ] Periodic retirement review (Pattern 3) cadence established.
- [ ] Ownership source-of-truth is ONE system, not several.


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org's current Flow count, naming state, governance maturity
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Common Patterns above; prefer Pattern 1 + 2 for greenfield, Pattern 3 + 4 for cleanup
4. Validate — run the skill's checker script and verify against the Review Checklist above
5. Document — record the governance standard in a team wiki + flow descriptions; make it discoverable

---

## Salesforce-Specific Gotchas

1. **Copied flows keep confusing names longer than teams expect** — naming debt compounds every time a flow is cloned instead of redesigned cleanly.
2. **Inactive versions still create cognitive load** — even when they are not live, they make support and release review harder.
3. **Interview labels matter operationally** — weak labels make logs and diagnostics harder to interpret.
4. **No visible owner means production changes stall or become risky** — governance gaps surface most clearly during incidents.
5. **"LastModifiedBy" is not "Owner"** — the last editor isn't necessarily the accountable owner; explicit ownership metadata needed.
6. **Flows deployed via change sets don't preserve all Flow Builder context** — some metadata (like interview labels) can get mangled in cross-org deploys; check after migration.
7. **Managed-package flows have their own naming rules** — you can't rename them; their governance is the vendor's problem.
8. **Flow Trigger Explorer shows ordering but doesn't tell you owners** — the Setup view is diagnostic, not governance. Combine with Pattern 4 for the full picture.
9. **Deleted flows are hard-deleted immediately from Setup** — no soft-delete / recycle bin for Flow metadata. Confirm retirement carefully.
10. **Flow version numbers restart when a flow is deleted + recreated** — which confuses audit trails; prefer explicit `_vN` in the DeveloperName.

## Proactive Triggers

Surface these WITHOUT being asked:

- **Flow named `New Flow`, `Copy of X`, `Test`, `Untitled`** → Flag as High. Immediate rename needed.
- **> 5 inactive versions of a single Flow** → Flag as High. Version debt; retire the oldest.
- **Flow with empty description field** → Flag as Medium. Missing governance metadata.
- **Flow owned by inactive user (last modified by deactivated admin)** → Flag as High. Stranded governance.
- **Duplicate flows (same object + same trigger type + similar DeveloperName) both active** → Flag as Critical. Unspecified ordering, production risk.
- **Flow activated in production without change-management ticket reference** → Flag as High. Audit-trail gap.
- **Flow Ownership custom metadata missing for a production flow** → Flag as Medium (if org uses Pattern 4).
- **Flow inventory > 6 months since last retirement review** → Flag as Medium. Cadence slipping.

## Output Artifacts

| Artifact | Description |
|---|---|
| Governance standard | Naming, ownership, version, activation rules for flows |
| Portfolio findings | Concrete risks such as generic names, missing owners, stale copies |
| Release checklist | Minimum metadata and review expectations before activation |
| Retirement inventory | Per-flow classification: active / deprecated / retire-now |
| Ownership registry | Custom metadata records (Pattern 4) mapping each flow to its owning team + escalation path |

## Related Skills

- **flow/fault-handling** — when the operational pain is primarily failure behavior rather than portfolio discipline.
- **flow/flow-bulkification** — governance ≠ performance; this skill won't fix a bulkification bug.
- **flow/record-triggered-flow-patterns** — governance depends on consistent pattern discipline here.
- **admin/change-management-and-deployment** — when the release process itself is the harder systems problem.
- **devops/release-management** — complementary deploy-discipline skill.
- **standards/decision-trees/automation-selection.md** — governance starts with the right-tool choice.
