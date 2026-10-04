---
name: sf-minimal-change
description: Decides the smallest change that fully satisfies a Salesforce requirement before any code is written - challenging the requirement, searching the repo and org for something that already does the job, choosing platform configuration (validation rule, formula, roll-up summary, record-triggered Flow, sharing rule, duplicate rule, approval process) over Apex, choosing base Lightning components (lightning-record-form, lightning-record-edit-form, lightning-datatable, lightning-tree-grid, lightning-file-upload) and Lightning Data Service wire adapters (getRecord, getRelatedListRecords, getPicklistValues, graphql) over custom components and @AuraEnabled controllers, choosing standard REST/Composite/Composite Graph/sObject Collections/Bulk API 2.0/GraphQL/Pub-Sub endpoints over custom Apex REST, and reusing the frameworks already in the project instead of adding a second convention. Use this skill before writing Apex, LWC, Flow, or new metadata; when a story smells like it needs a new object, field, framework, or component; when reviewing a design, a pull request, or a metadata diff for over-build; and whenever someone proposes a trigger framework, wrapper component, utility layer, custom logging framework, custom scheduler, or config flag that nobody will ever flip.
---

# Minimal Change on the Salesforce Platform

## When to use

| Situation | Use this skill |
| --- | --- |
| Before the first line of Apex, LWC, or a new Flow is written | Yes - run the ladder first |
| Before creating a custom object, custom field, custom setting, or custom permission | Yes |
| Story wording implies a "framework", "engine", "handler layer", or "wrapper" | Yes - rung 5 and 6 usually kill it |
| Reviewing a design document, a PR, or a metadata diff | Yes - `references/review-checklist.md` |
| Deciding declarative vs code for a specific requirement | Yes - `references/declarative-vs-code.md` |
| Sizing the work of an already-agreed design | No - skill `sf-workflow-orchestration` |
| Writing the Apex once rung 7 is reached | Skill `sf-apex-development`, tests in `sf-apex-testing` |
| Writing the component once rung 7 is reached | Skill `sf-lwc-development`, tests in `sf-lwc-jest-testing` |

This skill answers one question: **what is the smallest change that fully satisfies the
requirement on this platform?** It never answers "what is the least work" - the floor below is
non-negotiable, and correctness always outranks smallness.

The documented Salesforce order of preference for working with data is itself a ladder: base
components built on Lightning Data Service, then LDS wire adapters, then the GraphQL wire adapter,
then Apex ([Data Guidelines](https://developer.salesforce.com/docs/platform/lwc/guide/data-guidelines.html)).
The rungs below extend that principle to metadata, automation, and integration.

## The ladder

Walk the rungs in order. Stop at the first rung that fully satisfies the acceptance criteria.
Record the rung you stopped on, and the rung you rejected, in `.vibeforce/state/contract.md`
(format in `references/scope-contract.md`).

### Rung 1 - Does it need to exist?

| Test | The requirement maps to a written acceptance criterion that a user or an integration can observe. |
| --- | --- |
| Artefacts killed here | Speculative fields, "future-proof" config flags, custom settings nobody reads, admin toggles with one value, status picklists with unused values, "just in case" custom permissions, extra LWC properties in `targetConfig`. |
| Seconds check | Every changed metadata item must be traceable to an acceptance-criterion ID. Anything unmapped is deleted, not deferred. |

```bash
# Every criterion needs an owner; every artefact needs a criterion.
grep -n "AC-" .vibeforce/state/contract.md
```

Requirement challenge questions: who consumes the output, what happens if the field is absent,
what is the first real record that exercises this, and which existing report or list view already
answers the question. If the answer is "the admin might want it later", it is not in scope.

### Rung 2 - Does it already exist in this repo or org?

| Test | No existing field, class, Flow, permission set, label, or component already delivers the behaviour. |
| --- | --- |
| Artefacts killed here | Duplicate fields (`Region__c` next to `Sales_Region__c`), a second selector for the same object, a second "utils" module, a duplicate custom label, a parallel record-triggered Flow on the same object. |
| Seconds check | Repo grep first (free, offline), then org query. Full playbook: `references/reuse-discovery.md`. |

```bash
# Repo: fields, classes, flows, permission sets
grep -rn "Region" force-app --include=*.field-meta.xml
ls force-app/main/default/classes | grep -i selector
sf data query --use-tooling-api -q "SELECT QualifiedApiName, DataType, IsCalculated FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName = 'Account'" --target-org vf-dev
sf data query -q "SELECT ApiName, Label, IsActive, ProcessType, TriggerType FROM FlowDefinitionView WHERE IsActive = true" --target-org vf-dev
sf org list metadata --metadata-type ApexClass --target-org vf-dev
```

`EntityDefinition` and `FieldDefinition` are Tooling API objects, so they need `--use-tooling-api`
([Tooling API: EntityDefinition](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_entitydefinition.htm),
[FieldDefinition](https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_fielddefinition.htm)).
`ApexClass`, `ApexTrigger`, `PermissionSet`, and `FlowDefinitionView` are standard objects and
query without that flag. `sf org list metadata` requires Modify All Data or Modify Metadata
Through Metadata API Functions on the connected user
([org list metadata](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_org_list_metadata.html)).

### Rung 3 - Can platform configuration do it?

| Test | The behaviour is expressible as a rule the platform already evaluates: validation rule, formula field, roll-up summary, duplicate/matching rule, assignment or escalation rule, approval process, sharing rule, record-triggered Flow, dynamic form, list view, or report. |
| --- | --- |
| Artefacts killed here | Apex that only compares fields and throws, Apex rollups, Apex that only sets an owner, Apex that only stamps a formula-derivable value. |
| Seconds check | Setup > Object Manager > *Object* > Validation Rules / Fields & Relationships / Flows; or the metadata types listed below. Capability table with breaking points: `references/declarative-vs-code.md`. |

| Requirement shape | Declarative artefact | Metadata type |
| --- | --- | --- |
| Block a save when data is inconsistent | Validation rule | `ValidationRule` |
| Derive a value from fields on the same record or its parents | Formula field | `CustomField` (`type` Formula) |
| Aggregate children onto a master record | Roll-up summary (`Count`, `Min`, `Max`, `Sum`) | `CustomField` (`type` Summary, `summaryOperation`) |
| Prevent or warn on duplicates | Duplicate rule + matching rule | `DuplicateRule`, `MatchingRule` |
| Route a record for sign-off | Approval process | `ApprovalProcess` |
| React to a record change | Record-triggered Flow | `Flow` |
| Grant record access by criteria or owner | Sharing rule | `SharingRules`, `CriteriaBasedSharingRule`, `OwnerSharingRule` |
| Share picklist values across fields | Global value set | `GlobalValueSet` |
| Gate a feature for some users | Custom permission | `CustomPermission` |

Roll-up summary operations are exactly `Count`, `Min`, `Max`, and `Sum`, with optional
`summaryFilterItems`
([CustomField](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customfield.htm)).
A validation rule holds a formula that blocks the save and shows an error message when it returns
true; since API 20.0 it cannot use compound fields
([ValidationRule](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_validationformulas.htm)).
Flow choice, ordering, and entry criteria belong to skill `sf-flow-automation`; sharing and
permission design to `sf-security-model`.

### Rung 4 - Is there a standard platform capability?

| Test | A shipped component, wire adapter, or API endpoint covers the interaction without new server code. |
| --- | --- |
| Artefacts killed here | Hand-rolled forms, hand-rolled tables, `@AuraEnabled` read methods, custom Apex REST endpoints, custom polling jobs, custom auth headers, custom file upload controllers. |
| Seconds check | `references/base-components-first.md` (UI) and `references/standard-apis-first.md` (integration). |

| Need | Standard capability |
| --- | --- |
| View/create/edit a record with labels, help text, validation | `lightning-record-form`; `lightning-record-edit-form` when the layout must be custom |
| Tabular data with sorting, inline edit, row actions, infinite scroll | `lightning-datatable`; `lightning-tree-grid` for hierarchy |
| Attach files to a record | `lightning-file-upload` |
| Read one record and its fields | `@wire(getRecord)` |
| Read a related list | `@wire(getRelatedListRecords)` |
| Read picklist values for a record type | `@wire(getPicklistValues)` |
| Read several objects or parent/child data in one call | `@wire(graphql)` |
| Create/update/delete one record from JS | `createRecord` / `updateRecord` / `deleteRecord` |
| External system reads/writes a few records | REST API, sObject Collections, Composite |
| External system writes a dependent record graph | Composite Graph |
| External system moves more than 2,000 records | Bulk API 2.0 |
| Authenticated callout without secrets in code | Named credential (`callout:My_Named_Credential/path`) |
| Near-real-time change notification | Change Data Capture + Pub/Sub API |

`lightning-record-form`, `lightning-record-edit-form`, and `lightning-record-view-form` implement
Lightning Data Service, need no Apex controller, and enforce field-level security and sharing
([Record Form](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-record-form.html),
[Record Edit Form](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-record-edit-form.html)).
Composite executes up to 25 subrequests as one API call
([Composite](https://developer.salesforce.com/docs/platform/api-rest/guide/resources-composite-composite-post.html));
Bulk API 2.0 is the documented choice above 2,000 records, and bulkified synchronous calls below it
([Bulk API intro](https://developer.salesforce.com/docs/platform/api-asynch/guide/asynch-api-intro.html)).

### Rung 5 - Is a framework or dependency already in the project?

| Test | If custom code is unavoidable, it extends the conventions already present instead of introducing a second one. |
| --- | --- |
| Artefacts killed here | A second trigger framework, a second unit-of-work, a bespoke test data builder next to the existing factory, a new LWC utility module duplicating an existing one, a new logging framework. |
| Seconds check | One grep per convention; if a convention exists, it wins - even if you prefer the other one. |

```bash
grep -rln "fflib_SObjectDomain\|fflib_SObjectSelector\|fflib_ISObjectUnitOfWork" force-app/main/default/classes | head
grep -rln "TriggerHandler\|TriggerDispatcher" force-app/main/default/classes | head
grep -rln "@IsTest" force-app/main/default/classes | xargs -r grep -ln "TestDataFactory\|TestFactory" | head
ls force-app/main/default/lwc | grep -iE "util|helper|common"
```

When the project is fflib-based, new behaviour goes into the existing layers - see
`sf-fflib-foundations`, `sf-fflib-selector-layer`, `sf-fflib-domain-service-uow`,
`sf-fflib-testing`, and `sf-fflib-operations`. Two conventions in one repo is a defect, not a
style preference.

### Rung 6 - Can it be one line or one attribute?

| Test | The whole requirement collapses into a field attribute, a component attribute, a permission-set entry, a `WHERE` clause, or a formula. |
| --- | --- |
| Artefacts killed here | Client-side validation code replacing `required`, an Apex query filter replacing a `WHERE` clause, a trigger replacing a formula field, a new class replacing a permission-set entry. |
| Seconds check | Ask "which single attribute would make this behaviour true?" before writing a method. |

```html
<!-- Whole requirement: "Rating must be filled in before save" -->
<lightning-record-edit-form object-api-name="Account" record-id={recordId}>
    <lightning-messages></lightning-messages>
    <lightning-input-field field-name="Rating" required></lightning-input-field>
    <lightning-button type="submit" label="Save"></lightning-button>
</lightning-record-edit-form>
```

Server-side truth still belongs in a validation rule: the platform documentation recommends
validation rules over client-side validation, and the form surfaces those errors automatically
([Record Edit Form](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-record-edit-form.html)).

### Rung 7 - The minimum custom implementation

Reached only when rungs 1-6 are exhausted and the rejection reason for each is written down.
Then the implementation is scoped to the acceptance criteria and nothing else:

- One class per responsibility that the criteria name; no interface without a second implementor.
- One `@AuraEnabled` method per interaction the UI actually performs; `cacheable=true` only for
  reads ([AuraEnabled Annotation](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_annotation_AuraEnabled.htm)).
- One SOQL query shaped for the criteria, selective, bulk-safe (skill `sf-soql-sosl-optimization`).
- Tests for the changed behaviour only (skills `sf-apex-testing`, `sf-lwc-jest-testing`).

## The floor (never traded for smallness)

Smallness never justifies removing these. Each is a correctness requirement with a concrete
platform mechanism.

| Floor requirement | Mechanism | Detailed in |
| --- | --- | --- |
| Object and field permissions enforced | At API version 67.0 and later Apex runs in user context by default; keep it that way and mark deliberate escalations with `WITH SYSTEM_MODE` / `AccessLevel.SYSTEM_MODE` / `as system`. Where you need an explicit user-mode operation use `WITH USER_MODE`, `AccessLevel.USER_MODE`, `insert as user`, or `Security.stripInaccessible`. Never `WITH SECURITY_ENFORCED` - it is not allowed in Apex SOQL at 67.0+. LDS wire adapters and base components enforce FLS and sharing for you | `sf-security-model` |
| Sharing enforced | A class with no sharing declaration behaves as `with sharing` at 67.0+; still declare `with sharing` / `inherited sharing` explicitly, and justify `without sharing` in a comment. Declarative access stays in sharing rules | `sf-security-model` |
| Bulkification (200 records per trigger invocation, no DML or SOQL in loops) | Collection-based DML, maps keyed by Id; limits are 100 synchronous SOQL queries and 150 DML statements per transaction ([Governor Limits](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm)) | `sf-governor-limits` |
| Error handling and partial-failure behaviour | `Database.insert(records, false)` with result inspection, or all-or-none by design; composite requests choose rollback scope explicitly | `sf-apex-development`, `sf-integration-patterns` |
| Tests for the changed behaviour | Apex tests for the new path, Jest tests for the new component behaviour | `sf-apex-testing`, `sf-lwc-jest-testing` |
| LWC accessibility | Base components ship accessible markup; custom markup needs labels, roles, and keyboard paths | `sf-lwc-development` |
| Data-loss safety | No destructive metadata change without a backout path; no field deletion in the same release that stops writing it | `sf-data-management`, `sf-deployment-strategies` |
| Idempotency for integrations | External IDs with upsert, replay-safe event handling | `sf-integration-patterns` |
| No secrets in metadata | Named credentials and external credentials, never a hard-coded token ([Named Credentials](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_named_credentials.htm)) | `sf-security-model`, `sf-integration-patterns` |

A change that drops a floor item is not minimal; it is incomplete.

Version boundary: the enforcement mechanisms above are the API 67.0 behaviour (`apiVersion` in
`config/vibe-force.defaults.json`). Older samples that show `WITH SECURITY_ENFORCED` predate this
boundary and must not be copied.


## Read before you decide

The ladder constrains the **solution**, never the **investigation**. Choosing a rung without
reading the surrounding metadata produces the most expensive kind of small change: one that
conflicts with automation that already runs.

Required reading before selecting a rung:

1. **Impacted metadata** - every file the change would touch, retrieved or grepped, not guessed.
2. **Automation inventory on the object** - existing triggers, record-triggered Flows and their
   `TriggerOrder`, validation rules, duplicate rules, workflow field updates, approval processes.
3. **Save-order interactions** - whether the proposed rung runs before or after the automation
   already present, and whether it can re-enter it (skill `sf-flow-automation`).
4. **Existing tests** - what currently asserts the behaviour you are about to change; those
   assertions define the contract you must preserve.
5. **Org configuration** - permission sets, record types, picklist value sets, and page layouts
   that already express part of the requirement.

```bash
sf data query --use-tooling-api -q "SELECT QualifiedApiName, (SELECT DeveloperName FROM ValidationRules), (SELECT Name FROM ApexTriggers) FROM EntityDefinition WHERE QualifiedApiName = 'Account'" --target-org vf-dev
sf data query -q "SELECT ApiName, Label, TriggerType, RecordTriggerType, TriggerOrder, TriggerObjectOrEventLabel FROM FlowDefinitionView WHERE IsActive = true AND TriggerObjectOrEventLabel = 'Account'" --target-org vf-dev
```

Wave 0 of the workflow exists for exactly this: `sf-scout` maps impacted metadata and existing
tests before any wave-1 agent edits a file (skill `sf-workflow-orchestration`).

## Over-build catalogue

| Over-build | Smaller alternative | Why the alternative wins |
| --- | --- | --- |
| Custom LWC form with `@AuraEnabled` save | `lightning-record-edit-form` + `lightning-input-field` | LDS-backed, enforces FLS and sharing, shows validation-rule errors, no controller to test |
| Custom LWC read-only record panel | `lightning-record-form` with `mode="readonly"` | Uses compact or full layout, admin-controlled fields |
| Hand-built `<table>` with sorting and paging JS | `lightning-datatable` (`sortable`, `editable`, row actions, `enable-infinite-loading`) | Typed columns, locale formatting, accessibility, selection events |
| Custom hierarchy renderer | `lightning-tree-grid` with `_children` | Expand/collapse and nested selection handled |
| Imperative Apex to read a record | `@wire(getRecord)` / `@wire(graphql)` | Shared LDS cache, automatic refresh, no API calls consumed |
| Apex controller to read a related list | `@wire(getRelatedListRecords)` | UI API resource, respects layout and security |
| Apex method returning picklist values | `@wire(getPicklistValues)` | Record-type aware |
| Custom Apex REST endpoint for CRUD | REST API + sObject Collections, or Composite | No Apex to secure, version, or test; one API call for 25 subrequests |
| Custom Apex REST for dependent inserts | Composite Graph (up to 500 nodes per payload) | Reference chaining and per-graph rollback provided |
| Batch Apex to load external data | Bulk API 2.0 ingest job | Asynchronous, chunked, isolated CPU budget |
| New custom object for a 1:many detail | Child records on an existing standard object | Reporting, sharing, and mobile support already exist |
| New custom trigger framework | The trigger framework already in the repo | One convention; see rung 5 |
| Apex sharing recalculation | Criteria-based or owner-based sharing rule | Maintained by the platform |
| Apex rollup in a trigger | Roll-up summary field (`Count`/`Sum`/`Min`/`Max`) or a scheduled Flow | No DML, no recursion, no tests |
| Per-field Apex validation | Validation rules | Enforced for every entry path: UI, API, Bulk, Flow |
| Custom picklist storage object | Global value set | Shared values, translation support |
| Custom settings object for a feature toggle | Custom permission on a permission set | Assignable, packageable, checkable |
| Custom caching layer | `@AuraEnabled(cacheable=true)` for client reads, Platform Cache partition for server reuse | Documented, monitored, no invalidation code |
| Custom scheduler object plus job runner | `System.schedule` / `System.scheduleBatch` (max 100 scheduled Apex jobs at a time) | Platform scheduler; see `sf-async-apex-patterns` |
| Custom logging framework | The logging already present in the repo, or `sf-debugging-logs` conventions | Nobody maintains the second one |
| Custom polling job against an external system | Change Data Capture or platform events over Pub/Sub API | Near-real-time, no scheduled load |

## Anti-patterns

| Anti-pattern | Symptom in the diff | Fix |
| --- | --- | --- |
| Abstraction with one caller | An interface and one implementor added in the same commit | Inline the implementation; add the interface when the second implementor exists |
| Interface per class by reflex | `IAccountService` + `AccountService`, no mock consumer | Delete the interface unless a test or a second module needs it |
| "Framework" for a single use case | `*Engine`, `*Processor`, `*Framework` class names with one entry point | One class, one method, named after the behaviour |
| Config flags nobody flips | New custom setting, custom metadata row, or `targetConfig` property with one value in every environment | Remove the flag; hard-code the agreed behaviour |
| Wrapper around a base component | `c-my-datatable` that forwards every attribute of `lightning-datatable` | Use the base component directly at the call site |
| Deep utility layers | `Utils` calling `Helper` calling `Support` | Collapse to one level next to the caller |
| Premature namespacing or packaging | Package boundaries created before a second consumer exists | Keep one package directory; see `sf-packaging-release` |
| Gold-plated error taxonomy | Five custom exception classes for one failure mode | One exception, real message, tested path |
| Dead metadata left behind | Fields no longer written, classes with zero references, inactive Flow versions | Remove in the same change (destructive changes: `sf-deployment-strategies`) |
| Speculative bulk handling | Queueable chain for a path that always processes one record | Synchronous path; keep bulk safety, drop the machinery |

## Verification

Minimality is verifiable. Run these before claiming the change is small.

```bash
# 1. Shape of the diff: file count and churn per metadata type
git diff --stat
git diff --name-only | sed 's|.*/\([a-z]*\)/[^/]*$|\1|' | sort | uniq -c | sort -rn

# 2. New files are the expensive ones - list them explicitly
git diff --name-status --diff-filter=A

# 3. Dead or duplicated code, unused variables, copy-paste blocks
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" static --changed

# 4. Full local gate before review
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local

# 5. Caller counts for anything newly introduced
grep -rn "AccountRollupService" force-app --include=*.cls | grep -v "AccountRollupService.cls" | wc -l
```

Code Analyzer ships the engines that catch the mechanical symptoms: `pmd` for unused code and
excessive complexity, `cpd` for duplicated blocks, `eslint` for unused JS, `flow` for Flow issues
([Engines](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/engines.html)).
Rule selection and severity gating live in skill `sf-code-analyzer-quality`; the gate is
`vf-check analyzer` at the configured `analyzerFailSeverity`.

Scope-versus-criteria checklist:

| Check | Pass condition |
| --- | --- |
| Every changed artefact maps to an acceptance criterion | No unmapped file in `git diff --name-only` |
| Every acceptance criterion maps to a changed artefact | No criterion without evidence |
| Rung recorded with rejected alternative | `.vibeforce/state/contract.md` has a decision-log row per artefact |
| New abstractions have >= 2 callers | Caller count grep is 2 or higher, or the abstraction is removed |
| Floor items intact | CRUD/FLS, sharing, bulkification, tests, accessibility, idempotency, no secrets |
| Dead metadata removed | No field, class, or Flow version left unreferenced by this change |

Review questions to ask on every PR (full list with severities in `references/review-checklist.md`):

1. Which rung does this stop on, and what was rejected one rung lower?
2. Which acceptance criterion does each new file serve?
3. How many callers does each new class, interface, or module have?
4. Which base component or wire adapter was considered before this custom component?
5. Which declarative option was considered before this Apex?
6. What would break if the newest file were deleted?

Post-deploy, confirm the change did only what it claimed: skill `sf-post-deploy-verification`
with `vf-check smoke`.

## References

- [`references/declarative-vs-code.md`](references/declarative-vs-code.md) - requirement to
  declarative option to breaking point to code fallback, with the limits that force code.
- [`references/base-components-first.md`](references/base-components-first.md) - base Lightning
  component catalogue, what each handles out of the box, escape hatches, and side-by-side
  custom-vs-base implementations.
- [`references/standard-apis-first.md`](references/standard-apis-first.md) - standard API versus
  custom Apex REST decision table with limits and `sf api request rest` examples.
- [`references/reuse-discovery.md`](references/reuse-discovery.md) - the repo-and-org discovery
  playbook: grep patterns, `sf` commands, Tooling API queries, duplicate-field detection.
- [`references/scope-contract.md`](references/scope-contract.md) - story to acceptance criteria to
  `.vibeforce/state/contract.md`, including the decision-log format.
- [`references/review-checklist.md`](references/review-checklist.md) - over-build review checklist,
  severities, per-metadata-type questions, and the evidence to cite.

Official documentation: [Data Guidelines](https://developer.salesforce.com/docs/platform/lwc/guide/data-guidelines.html),
[Lightning Data Service](https://developer.salesforce.com/docs/platform/lwc/guide/data-ui-api.html),
[CustomField](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customfield.htm),
[ValidationRule](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_validationformulas.htm),
[Apex Governor Limits](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm),
[Composite](https://developer.salesforce.com/docs/platform/api-rest/guide/resources-composite-composite-post.html),
[Bulk API 2.0](https://developer.salesforce.com/docs/platform/api-asynch/guide/asynch-api-intro.html),
[Salesforce CLI Command Reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_data_query.html).
