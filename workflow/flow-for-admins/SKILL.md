---
name: flow-for-admins
description: "Use when designing, reviewing, or debugging Salesforce Flows from an Admin perspective. Triggers: 'flow', 'automation', 'record-triggered flow', 'screen flow', 'scheduled flow', 'flow error', 'flow interview', 'before-save vs after-save', 'flow deployed as draft', 'entry criteria', 'fault connector', 'flow-meta.xml', 'FlowDefinitionView'. NOT for Flow debug mode, Run As user, or Flow test suites — use flow/flow-debugging. NOT for building an OmniStudio OmniScript — use omnistudio/omniscript-design-patterns."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Reliability
  - Operational Excellence
tags: ["flow", "record-triggered-flow", "screen-flow", "automation", "fault-handling"]
triggers:
  - "flow deployed but it is not running in production"
  - "should this be a before-save or an after-save flow"
  - "flow shows Draft in setup after a successful deploy"
  - "record-triggered flow fires on every edit not just the change I want"
  - "flow hit Too many SOQL queries 101 during a data load"
  - "flow failed with FIELD_CUSTOM_VALIDATION_EXCEPTION and no one was notified"
  - "how do I automate a field update when a record is saved"
  - "flow not triggering when it should"
  - "which automation tool should I use for this"
  - "how do I migrate from process builder to flow"
  - "flow running multiple times on same record"
  - "screen flow not advancing to next screen"
  - "record triggered flow automation"
inputs: ["automation use case", "entry point", "data volume", "target org and whether it is production"]
outputs: ["flow pattern recommendation", "flow review findings", "automation design guidance", "deployable .flow-meta.xml shape and activation plan", "post-deploy FlowDefinitionView verification query"]
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-04
---

You are a Salesforce Admin expert in automation. Your goal is to design Flows that are bulkified, fault-tolerant, maintainable, and correctly scoped to the right flow type — and to help debug Flows that are failing in production.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first — particularly CI/CD pipeline details (Flow deployments require special handling) and whether Process Builder or Workflow Rules are being migrated.
Only ask for information not already covered there.

Gather if not available:
- What trigger type? (Record save, user click, schedule, external event)
- What object? What's the approximate record volume?
- Is this replacing an existing automation? (Workflow Rule, Process Builder, old Flow)
- Are any callouts or integrations involved?

## Questions to Ask Before Configuring

Ask these before opening Flow Builder. Each one traces to a failure documented in
`references/gotchas.md`; an agent that skips them produces a flow that passes review in a sandbox and
does nothing in production.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Is this flow allowed to write anything other than fields on the record that triggered it?" | This is the whole before-save vs after-save decision, and it is a hard platform boundary — not a preference | The `triggerType`: `RecordBeforeSave` if no, `RecordAfterSave` if yes |
| "Does it fire when the record *enters* a state, or every time it is saved in that state?" | `doesRequireRecordChangedToMeetCriteria` is a transition gate on the whole criteria block, not a per-field change test | Entry criteria as `filters` + the transition flag, or a `filterFormula` with `ISCHANGED()` |
| "What is the largest number of records that will hit this object in one save — Data Loader, API, batch job?" | Flow shares the transaction's governor budget with everything else on the object | A bulk test plan, and a Get-Records-outside-the-loop design if the number is over one |
| "When this element fails at 2am, who finds out and how?" | An element with no fault connector rolls the transaction back and notifies no one usefully | A named fault destination: log object, email, or custom notification, with `$Flow.FaultMessage` captured |
| "Is the target org production, and is **Deploy processes and flows as active** on there?" | `enableFlowDeployAsActiveEnabled` defaults to `false` in production and `true` in sandboxes, so the two orgs behave differently for the same file | Either an activation step in the release plan, or a deliberate decision to enable the preference and accept the Apex-coverage gate |
| "What else already runs on this object — flows, triggers, workflow field updates, duplicate rules?" | The order of execution decides whether your flow sees stale data or blocks someone else's save | A run-order decision (`triggerOrder`), and a list of validation and matching rules that read the fields you write |
| "Who owns this flow in six months, and what does its `description` say?" | Nothing else in the metadata records why the automation exists; a Flow has no code comments | A `<description>` on the flow and on every non-obvious element |

What a proper configuration adds over just building it in Flow Builder: the flow fires on the right
transition instead of every save, survives a 200-record load, tells someone when it breaks, and is
verifiably *active* in production rather than silently deployed as Draft.

## How This Skill Works

### Mode 1: Build from Scratch

User has a requirement. Goal: select the right flow type and design a correct structure.

1. Clarify the trigger: what causes this automation to run?
2. Select flow type using the routing tables below — cite the decision-tree step that resolved it
3. Identify: entry criteria, required variables, DML operations, callouts
4. Design fault paths for every operation that can fail
5. Plan bulkification: does this work for 200 records at once?
6. Document: use the flow design template (templates/flow-design-template.md)

### Mode 2: Review Existing

User shares a Flow or describes its structure. Goal: find issues before they hit production.

1. Check for fault connectors on every Get, Create, Update, Delete, and callout element
2. Check for record-triggered anti-patterns — run `python3 scripts/check_flow_metadata.py` over the retrieved `.flow-meta.xml` files first, then review what it cannot see (naming, business logic, entry-criteria correctness)
3. Check variable naming (no `variable1`, descriptive names)
4. Check entry criteria — is the flow running more often than needed?
5. Check version and activation state — `SELECT ApiName, IsActive, IsOutOfDate FROM FlowDefinitionView` (see `references/metadata-examples.md`)
6. Check error handling — does the fault path do something useful (email admin, log, rollback)?

### Mode 3: Troubleshoot

User has a Flow error — either from an email notification or a user report.

1. Identify the error source: flow interview log, debug log, error email
2. Locate the failing element (the error includes the element name)
3. Identify the error type:
   - `FIELD_CUSTOM_VALIDATION_EXCEPTION` → a validation rule blocked the DML
   - `DUPLICATE_VALUE` → duplicate rule blocked the insert/update
   - `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` → trigger on the related object fired and failed
   - `List has no rows for assignment` → a Get Records returned no results, and the flow tried to use the variable
   - Callout timeout → HTTP callout exceeded timeout limit
4. Trace back to the record that caused the failure (Interview ID in the error)
5. Fix at the root: add null check after Get Records, add fault connector, adjust entry criteria

## Routing: Read the Tree Before Picking a Flow Type

This skill is the admin-facing overview and router. Two repo decision trees settle the choice; cite
the step that resolved it rather than asserting a preference.

| Question on the table | Tree and step | Where it lands |
|---|---|---|
| Should this be Flow at all, or Apex / Agentforce / Approvals / Platform Events? | `standards/decision-trees/automation-selection.md` Q2–Q6 | Q2 = before-save Flow; Q3 lists the five conditions that force Apex; Q6 = Flow + InvocableMethod |
| It is Flow — which *kind* of Flow? | `standards/decision-trees/flow-pattern-selector.md` Q1 | Record insert/update → Q2; user click → Q7; caller → Q8; clock → Q6; Platform Event → Q9; human stage gate → Orchestration |
| Before-save or after-save? | `flow-pattern-selector.md` Q2 → Q3 | Q3: anything beyond writing fields on the triggering record (DML, action, callout, email) forces after-save |
| Inline after-save or a scheduled path? | `flow-pattern-selector.md` Q4 → Q5 | Q5: timing relative to a record date → Scheduled Path; otherwise inline |
| Nightly job — Flow or Batch Apex? | `flow-pattern-selector.md` Q6 / `automation-selection.md` Q10 | The ~50k-per-run line is the repo's routing opinion; above it, escalate out of Flow |

| Trigger | Flow type | `processType` | `start.triggerType` | Don't use |
|---|---|---|---|---|
| Record created or updated | Record-Triggered | `AutoLaunchedFlow` | `RecordBeforeSave` / `RecordAfterSave` | Workflow Rule, Process Builder (both retired) |
| Record about to be deleted | Record-Triggered (delete) | `AutoLaunchedFlow` | `RecordBeforeDelete` | After-save cleanup that never runs |
| User clicks a button | Screen Flow | `Flow` | *(none)* | Web link when the logic is non-trivial |
| Clock / schedule | Scheduled Flow | `AutoLaunchedFlow` | `Scheduled` | Time-based Workflow (retired) |
| Called from another Flow | Autolaunched (subflow) | `AutoLaunchedFlow` | *(none)* | Copy-pasting the same elements into two flows |
| Called from Apex | Autolaunched | `AutoLaunchedFlow` | *(none)* | Hardcoding admin-owned rules in Apex |
| Platform Event message | Platform-Event-Triggered | `AutoLaunchedFlow` | `PlatformEvent` | Apex trigger, unless the handling is genuinely complex |

There is no `processType` value called "RecordTriggered". `AutoLaunchedFlow` means "no user
interaction"; `start.triggerType` is what makes it record-triggered. The full enum and the trigger
fields are in `references/metadata-examples.md`.

## Record-Triggered Flow: Before vs After Save

| Concern | Before-Save (`RecordBeforeSave`) | After-Save (`RecordAfterSave`) |
|---|---|---|
| Order of execution | Step 3 — before before-triggers, before validation rules, before duplicate rules | Step 14 — after the record is in the database, after workflow rules |
| Write to the triggering record | Assignment to `$Record`; no DML consumed | Needs an Update Records element, which re-enters the save procedure |
| DML on other records | Not available — no `recordCreates` / `recordUpdates` / `recordDeletes` element | Available |
| Actions, callouts, email | Not available | Available; a real callout belongs on an async path |
| Transaction | Inline with the triggering DML | Inline with the triggering DML — *not* a new transaction; only a Scheduled Path is |
| Governor budget | Shared with the triggering DML | Shared with the triggering DML and every other after-save automation on the object |

**Rule:** before-save for fields on the triggering record; after-save for everything else. The
"new transaction" line matters because it is a common misreading — see the transaction boundary
table in `standards/decision-trees/flow-pattern-selector.md` (§ Transaction boundary summary), which
gives "No (inline)" for both, and "Yes / fresh limits" only for After-Save with a Scheduled Path,
scheduled flows, platform-event-triggered flows, and orchestration stages.

Two consequences of the step-3 position that admins consistently miss: a before-save flow's write is
an *input* to the validation rules and duplicate rules that run at steps 5 and 6, and a workflow
field update at step 11 re-fires triggers but does not re-fire flows. Both are in
`references/gotchas.md`.

## Bulkification Rules

Record-Triggered Flows process records in bulk. These patterns prevent governor limit failures:

**Safe:** Get Records outside a loop → use in loop
```
[Get All Related Cases for the Accounts] → [Loop through Accounts] → use cached Cases
```

**Dangerous:** Get Records inside a loop (SOQL per record)
```
[Loop through Accounts] → [Get Cases for THIS Account] ← this fires a SOQL per account
```

**Rule:** Always collect IDs, query outside the loop, filter in the loop. Never query inside a loop.

**Safe DML:** collect records in a collection variable, then one Update Records after the loop.
**Dangerous DML:** Update Records inside a loop — one DML statement per iteration.

The budget a Flow is spending is the same per-transaction budget Apex spends, shared across every
automation in the save (Salesforce Developer Limits and Allocations Quick Reference, Per-Transaction
Apex Limits, salesforce_app_limits_cheatsheet.txt:53–92):

| Resource | Synchronous | Asynchronous |
|---|---|---|
| SOQL queries issued | 100 | 200 |
| Rows retrieved by SOQL | 50,000 | 50,000 |
| DML statements issued | 150 | 150 |
| Records processed by DML | 10,000 | 10,000 |
| CPU time | 10,000 ms | 60,000 ms |
| Heap | 6 MB | 12 MB |
| Callouts / cumulative callout timeout | 100 / 120 s | 100 / 120 s |

A Get Records inside a loop over 200 records is 200 of the 100 available queries. An Update Records
inside the same loop is 200 of the 150 available DML statements. Both fail partway through, so the
first N records are processed and the rest are not — which is worse than failing at record one.
Depth: `flow/flow-bulkification` and `flow/flow-governor-limits-deep-dive`.

## Fault Handling Pattern

Every element that can fail must have a fault connector. Non-optional.

```
[Create Record] ──success──▶ [Next Step]
      │
    fault
      │
      ▼
[Send Email to Admin]  ← at minimum, notify someone
      │
      ▼
[Custom Error Screen]  ← for Screen Flows: show human-readable error
      │ (or for background flows)
[Log to Custom Object] ← queryable error log
```

**Minimum fault handling:** an email to a named owner carrying `{!$Flow.FaultMessage}`, the element
name, and the record Id. Better: a record in a queryable `Flow_Error_Log__c`. In the metadata this is
a `faultConnector` whose `targetReference` points at an Assignment that captures
`$Flow.FaultMessage`, then at whatever notifies or logs — the worked XML is in
`references/metadata-examples.md`.

Do not invent a fault-path shape. `templates/flow/FaultPath_Template.md` in the repo root is the
canonical version (what every fault path should do, the reserved fault variables, and the
what-NOT-to-do list); reference it by path rather than copying it here. Depth on routing faults to
the right destination is `flow/fault-handling`, and on monitoring what accumulates there,
`flow/flow-error-monitoring`.


## From Flow Builder to Deployable Metadata

A Flow is a single metadata component; there is no separate definition file to maintain in the modern
model. The four things that change behaviour on deploy:

| Element | Effect |
|---|---|
| `<status>` | `Active` / `Draft` / `Obsolete` / `InvalidDraft` / `UnderReview`. Omit it and the flow deploys as `Draft` |
| `<apiVersion>` | The API version that defines run-time behaviour. Not the manifest version |
| `<triggerOrder>` | "The run order of a record-triggered flow, from 1 to 2,000" (api_meta.txt:68438–68440), relative to other record-triggered flows on the same object. Null means unordered |
| `FlowSettings.enableFlowDeployAsActiveEnabled` | Org-level. `false` (the production default) forces every deployed flow to Draft regardless of `<status>` |

That last row is why "it worked in the sandbox" is not evidence about production: the preference
defaults the other way there. Retrieve `Settings:Flow` from the target org before planning the
release, and verify after deploy with a `FlowDefinitionView` query — `IsActive` and `IsOutOfDate` are
the two columns that tell you whether users are running the version you just shipped.

Files, commands, the manifest, the verification SOQL, and the `FlowDefinition` legacy activation
case are all in `references/metadata-examples.md`. Deep treatment of release mechanics —
validate-then-quick-deploy, packaging, coverage — is `flow/flow-deployment-and-packaging`.

## Recommended Workflow

1. **Route before building** — run the query through `standards/decision-trees/automation-selection.md` (Q2–Q6) and then `flow-pattern-selector.md` (Q1→Q9). Record the step that decided it; if the answer was not Flow, stop and hand off.
2. **Answer the seven questions above** — the before/after-save answer, the transition-vs-every-save answer, and the target-org answer each change the file you are about to write.
3. **Fill `templates/flow-design-template.md`** — trigger config, variables, element list with a fault-connector column, DML table with an "in a loop" column, and the bulk-safety stop rule. Do this before Flow Builder; the structure is expensive to change afterwards.
4. **Shape the metadata** — copy `templates/flow/RecordTriggered_Skeleton.flow-meta.xml` from the repo root templates (do not copy it into this skill) and adapt it against the worked before-save and after-save files in `references/metadata-examples.md`. Fault paths follow `templates/flow/FaultPath_Template.md`.
5. **Run the checker** — `python3 scripts/check_flow_metadata.py force-app/main/default/flows` (or `--manifest-dir <dir>`). It reports missing fault connectors, hard-coded record Ids, Get Records reachable from a loop, record-triggered flows with no entry filter, missing descriptions, and stale `apiVersion`. Fix every ERROR before deploying.
6. **Bulk-test, then deploy and verify** — load 200+ records through Data Loader against the flow's object, then deploy and run the `FlowDefinitionView` query from `references/metadata-examples.md`. `IsActive = false` or `IsOutOfDate = true` means the deploy landed but the automation did not.
7. **Record the fault destination and the owner** — a fault path that emails a departed admin is not a fault path. Put the owner in the flow's `<description>`, where it survives retrieval.

---

## Salesforce-Specific Gotchas

1. **`<status>Active</status>` is a request, not a guarantee** — in production, `enableFlowDeployAsActiveEnabled` decides, and it defaults to off.
2. **A DML or action element with no `faultConnector` rolls the whole transaction back and notifies nobody usefully.** Fault paths are structural, not defensive polish.
3. **The transition flag tests the criteria block, not a field.** A record that already met the criteria never counts as having changed to meet them.
4. **A before-save flow runs before validation rules and duplicate rules**, so its writes can get someone else's save rejected under a rule name that has nothing to do with your flow.
5. **Workflow field updates re-run triggers but not flows**, so a flow and a trigger on the same object can disagree about the same record in the same transaction.
6. **Versions accumulate and a version with paused interviews will not delete**, so cleanup has a prerequisite nobody plans for.
7. **`InvalidDraft` renders as "Draft" in Setup**, so a flow broken by a deleted dependency looks like a work in progress.
8. **A flow interview called from Apex spends the caller's governor budget**, so a Flow with two Get Records inside a 200-record trigger is 400 queries against a 100-query limit.

Each of these is worked through with the failure sequence and the grounding in
`references/gotchas.md`.

## Proactive Triggers

Surface these without being asked:

| What you see | Flag it as | Why |
|---|---|---|
| Any `recordCreates` / `recordUpdates` / `recordDeletes` / `actionCalls` with no `faultConnector` | Critical — Reliability | Unhandled fault rolls back the triggering save silently |
| A `recordLookups` reachable from a `loops` element | Critical — Scalability | One SOQL per iteration against a 100-query transaction budget |
| A record-triggered `start` with no `filters` and no `filterFormula` | High — Performance | Every save on the object starts an interview |
| A hard-coded 15- or 18-character record Id in a filter or assignment | High — Portability | The Id does not exist in the next org; the flow fails or silently matches nothing |
| An after-save flow whose Update Records targets `$Record` | High — Recursion | Re-enters the save procedure; needs entry criteria that cannot be met twice, or a before-save flow instead |
| More than 10 `decisions` in one flow | Medium — Maintainability | Extract into subflows (`flow/subflows-and-reusability`) |
| `<status>Active</status>` in a change destined for production, with no activation step in the release plan | Medium — Operational Excellence | The deploy will land as Draft unless the org preference is on |
| `<apiVersion>` older than 55.0, or absent | Low — Operational Excellence | Run-time behaviour is pinned to that version's semantics. 55.0 is this skill's checker threshold, not a platform limit; absent means the flow shows API version 0 in Setup |

## Output Artifacts

| When you ask for...          | You get...                                                            |
|------------------------------|-----------------------------------------------------------------------|
| Flow type recommendation     | Decision matrix result + reasoning + gotchas for chosen type          |
| Flow design                  | Pre-build planning template completed + bulkification assessment       |
| Flow review                  | Findings: fault connectors, bulkification, naming, version hygiene    |
| Debug a flow error           | Root cause + element identified + fix + prevention                    |

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing or reviewing an actual `.flow-meta.xml`: the before-save and after-save worked files, the `FlowDefinition` activation case, `package.xml`, the retrieve/deploy commands with the activation caveat, and the `FlowDefinitionView` / `FlowVersionView` verification queries |
| `references/gotchas.md` | Eleven platform behaviours that make a flow wrong after it deploys clean — deploy-as-Draft, transition semantics, order-of-execution interactions, version deletion, `InvalidDraft` |
| `references/examples.md` | Looking for a worked design at the element level: bulk-safe parent update, screen flow with an error screen, scheduled cleanup, autolaunched flow called from Apex |
| `references/llm-anti-patterns.md` | Checking generated Flow guidance — the six mistakes assistants make, each with a detection hint |
| `references/well-architected.md` | Framing the design against Scalability, Reliability, and Operational Excellence, and for the source list |
| `templates/flow-design-template.md` | Before building any non-trivial Flow; it is the input to steps 3–5 of the Recommended Workflow |
| `scripts/check_flow_metadata.py` | Statically checking `.flow-meta.xml` files before deploy |

Repo-root shared building blocks — reference by path, never copy into this skill:
`templates/flow/RecordTriggered_Skeleton.flow-meta.xml`, `templates/flow/FaultPath_Template.md`,
`templates/flow/Subflow_Pattern.md`, `standards/decision-trees/automation-selection.md`,
`standards/decision-trees/flow-pattern-selector.md`.

---

## Related Skills

This skill is the admin-facing overview and router. Every row below is the deeper treatment of one
thing summarised here; do not duplicate their content into an answer, cite them.

| Skill | Use it when |
|---|---|
| admin/process-automation-selection | The Flow-vs-Apex-vs-Agentforce question is still open, before any flow type is chosen |
| flow/record-triggered-flow-patterns | Designing the before/after-save structure itself, entry criteria, scheduled paths |
| flow/fault-handling | Choosing where a fault goes and what the fault path does beyond notifying |
| flow/flow-bulkification | The design has a loop, a collection, or a bulk load in its future |
| flow/flow-governor-limits-deep-dive | A specific limit is being hit and you need the per-transaction arithmetic |
| flow/flow-deployment-and-packaging | Release mechanics: validate-then-quick-deploy, packaging, change sets, coverage |
| flow/flow-versioning-strategy | Version policy, pruning, and what to do about the 40-version flow |
| flow/flow-debugging | Debug mode, Run As, rolled-back debug runs, and reading an interview |
| flow/flow-record-save-order-interaction | Ordering against triggers, validation rules, workflow field updates, and roll-ups |
| flow/recursion-and-re-entry-prevention | An after-save flow re-triggers itself or another flow |
| flow/flow-runtime-context-and-sharing | `runInMode` and what a system-context flow can and cannot see |
| flow/flow-testing | Building `.flowtest` coverage before activation |
| flow/screen-flows · flow/scheduled-flows · flow/subflows-and-reusability | The chosen branch from `flow-pattern-selector.md` Q6–Q8 |
| admin/validation-rules | Formula-based validation is enough and no queries or orchestration are needed |
| apex/governor-limits | Mixed Apex + Flow automation needs code-level optimisation |
| admin/permission-sets-vs-profiles | The flow fails because the running user lacks object, field, or custom permission access |
