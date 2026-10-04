---
name: flow-governance
description: "Use when establishing operational standards for a Salesforce Flow portfolio, including naming conventions, ownership, version discipline, retirement of stale flows, and release readiness checks. Triggers: 'flow naming convention', 'too many old flows', 'who owns this flow', 'flow version governance', 'flow deployed but not active', 'two flows on the same object', 'triggerOrder', 'Flow.settings', 'deploy processes and flows as active', 'paused flow interviews', 'cannot delete flow version', 'flow inventory query'. NOT for element-by-element flow logic design or dedicated fault-handling review - use flow/fault-handling."
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
  - "flow governance isn't working"
  - "audit every active flow in the org"
  - "find flows deployed as inactive after a release"
  - "enforce a naming convention across the flow portfolio"
  - "set triggerOrder for two flows on the same object"
  - "query FlowDefinitionView for the flow inventory"
  - "delete a flow version blocked by paused interviews"
  - "decide whether to deploy processes and flows as active"
  - "write a flow governance policy the pipeline can check"
inputs:
  - "how many flows exist, which teams own them, and where operational confusion appears today"
  - "current naming, documentation, and activation practices"
  - "how releases, testing, and retirement decisions are currently made"
outputs:
  - "governance standard for naming, ownership, and lifecycle management"
  - "review findings for stale, weakly named, or undocumented flows"
  - "release checklist for safe activation and retirement decisions"
  - "deployable Flow.settings, PermissionSet and FlowDefinition governance metadata"
  - "flow-governance-policy.yaml that scripts/check_flow_governance.py enforces"
dependencies: []
version: 2.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when the problem is no longer one flow, but the portfolio of flows in the org. Governance matters once teams start asking which flow is active, who owns it, why two versions exist, or whether a copied automation can be retired safely. Good governance turns Flow from a sprawl risk into an operable platform capability.

This skill is the companion to technical-depth skills like `flow/fault-handling` and `flow/flow-bulkification` — those make individual flows good; this one makes the portfolio operable. Portfolio-level failures (no owner, 47 versions of the same flow, nobody knows what's active) produce the incidents that technical-depth skills can't prevent.

---

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- How many flows exist today, and how many are Active? (Exact answer: the `FlowDefinitionView` query in `references/metadata-examples.md` §5(a) — run it with and without the `InstalledPackageName = null` filter.)
- How are flows named today, and do labels, API names, descriptions, and interview labels help or confuse operators?
- Who owns activation, deactivation, and release approval for production flows?
- Which pain is most acute right now: duplicate automations, stale versions, weak documentation, unclear support ownership?
- Does the org have a change-management process (CAB, release train)? If yes, Flow governance plugs into it.

---

## Questions to Ask Before Configuring

Ask these before writing a standard. Each one traces to a platform behaviour in `references/gotchas.md` — an LLM that skips them produces a naming convention and calls it governance.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "In production, is **Deploy processes and flows as active** on or off?" | `enableFlowDeployAsActiveEnabled` defaults `false` in production and `true` in every sandbox, so a rehearsed deploy exercises the opposite behaviour from the real one (`api_meta.txt` L116877) | Whether "deploy" and "activate" are one reviewable event or a pipeline step plus an unrecorded Setup click |
| "Does the repo carry a `flowDefinitions/` directory?" | If it does, `activeVersionNumber` overrides every `<status>` in the diff (L73929–73932) | The `activation_control` value, and a deletion if the answer is "yes, but nobody meant to keep it" |
| "Which objects already have more than one Active record-triggered flow, and do those flows declare `triggerOrder`?" | The save order treats before-save and after-save flows as single steps and does not rank flows inside them (`apexdev.txt` L15440, L15466) | The list of undeclared ties — the defects that are invisible in Setup and unreachable by per-flow review |
| "Is Pause enabled, and does anyone inventory paused interviews?" | A version with paused interviews cannot be deleted (`api_meta.txt` L68041), so retirement stalls silently | Whether the retirement cadence is a calendar entry or a query, and who owns the abandoned interviews |
| "Where do flow error emails go today?" | With `enableFlowUseApexExceptionEmail` false they go to the last modifier — often someone who left (L116961) | The concrete fix for "no visible owner", rather than a wiki page asserting one |
| "What is the oldest `apiVersion` among Active flows, and is anyone tracking `ApiVersionRuntime`?" | Two flows on one object at different API versions adopt different versioned run-time behaviour in the same save (`object_reference.txt` L144985–145008) | The `min_api_version` floor and the size of the remediation behind it |
| "Which flows run as `SystemModeWithoutSharing`, and who approved that?" | It means "the flow can access all data" (`api_meta.txt` L68382); it is one line in a large XML file and no release review reads it | The run-mode allow-list, and the named exceptions that get a security review instead of a config ticket |

What a proper configuration adds over just writing a naming convention: the standard becomes a `flow-governance-policy.yaml` that `scripts/check_flow_governance.py` fails a merge on, the portfolio becomes a set of SOQL assertions a pipeline can run, and the two failures that no per-flow review can catch — an undeclared `triggerOrder` tie and a flow that deployed as Draft — become build errors instead of incident reports.

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

| Part | Meaning |
|---|---|
| Object | The sObject the flow fires on (or `Global` if object-agnostic). |
| TriggerType | `BeforeSave` / `AfterSave` / `Scheduled` / `Autolaunched` / `Screen` / `Orchestration`. |
| PurposeVerbPhrase | What the flow DOES, in UpperCamelCase. |
| Version suffix (optional) | Explicit version when the flow has iterated. |

### Ownership Must Be Visible

Every production flow should have an accountable owner or owning team, even if several contributors edit it over time. When a failure, deployment question, or retirement opportunity appears, support should not need archaeology to find the right decision-maker.

**Ownership metadata surfaces:**

| Surface | Notes |
|---|---|
| Description field | "Owner: sales-ops team. Escalate to: @alice.johnson. Purpose: …" |
| Custom metadata type | `Flow_Ownership__mdt` keyed by flow DeveloperName; supports bulk reporting. |
| Git commit history | LastModifiedBy surfaces the latest editor, not the long-term owner. |
| Team-by-team wiki | External to Salesforce but often the pragmatic answer. |

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

| Item | Standard |
|---|---|
| Description | 2-3 sentences on purpose, owner, escalation. |
| Element labels | Readable enough to make Flow Interview Log entries interpretable. |
| Fault-path routing | Documented via `flow/fault-handling`. |
| Version-change notes | When bumping the `_vN` suffix, explain why in the description. |

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

1. **Inventory before opining.** Run the five queries in `references/metadata-examples.md` §5 against the target org: active flows per object and save context, version-level drift, paused interviews, what those interviews hold, and flows below the API floor. Run §5(a) twice — once including managed-package rows, once excluding them — because those flows run in the same save and are unreachable through Metadata API (`api_meta.txt` L68035).
2. **Read the org's switchboard.** Retrieve `settings/Flow.settings` and diff it against the annotated field table in `references/metadata-examples.md` §1. Six of those booleans decide what every flow in the portfolio is permitted to do; three of them (`enableFlowDeployAsActiveEnabled`, `enableFlowFieldFilterEnabled`, `enableFlowInterviewSharingEnabled`) change the meaning of findings you are about to write.
3. **Write the standard as a file, not a page.** Fill in `flow-governance-policy.yaml` (`references/metadata-examples.md` §6): `activation_control`, the naming regex, `min_api_version`, the `runInMode` allow-list, the co-residency rule, the documentation and test gates, and the review gates. Declare one activation authority — `flow_status` or `flow_definition`, never both.
4. **Lint the retrieved tree.** `python3 scripts/check_flow_governance.py --manifest-dir force-app/main/default`. It lints the policy itself, then every flow, `FlowDefinition` and `Flow.settings` against it. It does not judge fault paths: run `flow/fault-handling` `scripts/check_flow_faults.py` over the same directory, and `flow/flow-element-naming-conventions` for element-level names.
5. **Deploy in the order in §8.** Settings before flows, dry-run before deploy, FlowTests with the flows, permission set after the flows, retirement last. Deploying `Flow.settings` after the flows changes what the flow deploy meant.
6. **Verify with the assertion, not the deploy result.** Run the aggregate query in `references/metadata-examples.md` §9 and require zero rows, then confirm `FlowDefinitionView.IsActive` and `IsOutOfDate` for each governed flow. A green deploy with `enableFlowDeployAsActiveEnabled` false activates nothing.
7. **Set the retirement cadence as a query.** Schedule §5(c) and §5(d); a version with paused interviews cannot be deleted (`api_meta.txt` L68041), so the blocker has to be found before the deploy window, not during it.

---

## Salesforce-Specific Gotchas

1. **Copied flows keep confusing names longer than teams expect** — naming debt compounds every time a flow is cloned instead of redesigned cleanly.
2. **Inactive versions still create cognitive load** — even when they are not live, they make support and release review harder.
3. **Interview labels matter operationally** — weak labels make logs and diagnostics harder to interpret.
4. **No visible owner means production changes stall or become risky** — governance gaps surface most clearly during incidents.
5. **"LastModifiedBy" is not "Owner"** — the last editor isn't necessarily the accountable owner; explicit ownership metadata needed.
6. **A flow with no `<status>` element deploys as Draft, not "unchanged"** — "any flow without a `status` value is deployed or retrieved with a `status` value of `Draft`" (`api_meta.txt` L73187). Absence is a decision the platform makes for you, and it makes the quiet one.
7. **Managed-package flows are unreachable through Metadata API** — "you can't use Metadata API to access a flow installed from a managed package unless the flow is a template" (`api_meta.txt` L68035). Inventory them from `FlowDefinitionView.InstalledPackageName` / `NamespacePrefix` / `ManageableState` instead; their governance is the vendor's problem but their save-order position is yours.
8. **Flow Trigger Explorer shows ordering but doesn't tell you owners** — the Setup view is diagnostic, not governance. The machine-readable form is `FlowDefinitionView` (`object_reference.txt` L139267); combine with Pattern 4 for ownership.
9. **A version with paused interviews cannot be deleted** — "you can delete a flow version if it isn't active and doesn't have any paused interviews… wait for those interviews to resume and finish, or delete them" (`api_meta.txt` L68041–68042). Retirement is gated on a query, not on a calendar.
10. **Spaces in a flow file name break the deploy** — "spaces in a flow file name can lead to errors when you deploy the flow. You can include spaces at the beginning or end of a name, but these spaces are removed when you deploy" (`api_meta.txt` L68036–68037). The naming regex in the policy file is where that is caught.
11. **A `flowDefinitions/` directory silently overrides every `<status>` in the diff** — `activeVersionNumber` wins (`api_meta.txt` L73929–73932). Declare one activation authority in the policy and let the checker fail the build when the tree contradicts it.
12. **Editing retrieved Process Builder metadata makes it unopenable** — "if you deploy process metadata that you edited, you can't open the process in the target org" (`api_meta.txt` L68044–68046). Exclude `processType` `Workflow` and `InvocableProcess` from any bulk rename or description backfill.

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

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | You are about to write anything deployable: the annotated `Flow.settings` field table, the flow-access `PermissionSet`, `FlowDefinition` activation control, the five inventory SOQL queries, the governance policy YAML, `package.xml`, deploy order and verification. |
| `references/gotchas.md` | A governance rule is being argued about, a deploy activated nothing, a retirement will not ship, or two flows on one object behave inconsistently. Every entry carries the guide line it rests on. |
| `references/examples.md` | You want the two worked diagnoses end to end — the undeclared `triggerOrder` tie on `Case`, and a retirement blocked by paused interviews — plus the naming and activation-gate patterns. |
| `references/llm-anti-patterns.md` | You are reviewing governance advice an assistant produced, or checking your own output for the six failure shapes (generic naming, no version cleanup, single-owner bottleneck, no retirement process, ignoring co-resident automation, no testing requirement). |
| `references/well-architected.md` | You need the Operational Excellence and Security framing, the activation-control tradeoff, or the sourced claim list. |
| `scripts/check_flow_governance.py` | Every time the source tree changes. `--manifest-dir <tree>`, optional `--policy <file>`; exit 1 on any ERROR. |
| `templates/flow-governance-template.md` | You are reviewing one flow by hand rather than linting a tree. |

## Related Skills

- **flow/fault-handling** — when the operational pain is primarily failure behavior rather than portfolio discipline.
- **flow/flow-bulkification** — governance ≠ performance; this skill won't fix a bulkification bug.
- **flow/record-triggered-flow-patterns** — governance depends on consistent pattern discipline here.
- **admin/change-management-and-deployment** — when the release process itself is the harder systems problem.
- **devops/release-management** — complementary deploy-discipline skill.
- **flow/flow-element-naming-conventions** — element-level names inside a flow; this skill governs the flow's own API name.
- **flow/subflows-and-reusability** — when the portfolio problem is duplication rather than ambiguity.
- **admin/change-advisory-board-process** — when activation needs an approval record, not just an owner.
- **admin/devops-process-documentation** — where the standard written here gets published and kept current.
- **standards/decision-trees/automation-selection.md** — governance starts with the right-tool choice.
