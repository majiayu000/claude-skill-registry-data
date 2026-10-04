---
name: sf-fflib-operations
description: Covers running fflib Apex Enterprise Patterns in a real delivery pipeline - trigger inventory and one-trigger-per-object dispatch, bypass and kill-switch design with custom permissions and custom metadata, feature flags that swap Application factory bindings, Queueable with Finalizer and Batch runners that call services with per-chunk Unit of Work commits, platform-event publishing and subscriber domains, callout ordering around commitWork, large-data-volume tuning, structured logging and correlation ids, packaging and deployment ordering for fflib-apex-mocks and fflib-apex-common, Code Analyzer rules that misfire on fflib, PR review checklists and the fflib version-upgrade runbook. Use this skill when auditing triggers in an fflib org, adding a bypass switch, running fflib code from Batch or Queueable, packaging or upgrading fflib, tuning Code Analyzer for fflib, or reviewing an fflib pull request.
---

# fflib Operations

Everything around the fflib write path: dispatch inventory, switches, async, bulk, observability,
packaging, analysis and upgrades. The layer semantics themselves are in skill
`sf-fflib-domain-service-uow`; the factories in skill `sf-fflib-foundations`.

Grounded in `apex-enterprise-patterns/fflib-apex-common` `master` @
`dab59777bac37f6b8a3cc2871fcf5df8d37764b4`, `fflib-apex-common-samplecode` `master` @ `4657d63`,
and `fflib-apex-mocks` `master` (raw file reads, see References).

## When to use

| Situation | Use this skill |
| --- | --- |
| Auditing which objects have triggers and which are fflib-dispatched | Yes |
| Adding an admin-visible bypass for a data load or an incident | Yes |
| Running an fflib service from Batch, Queueable or Schedulable | Yes |
| Packaging fflib as an unlocked package, or bumping the fflib version | Yes |
| Tuning `code-analyzer.yml` because PMD flags every selector | Yes |
| Writing a domain, service or Unit of Work | No - skill `sf-fflib-domain-service-uow` |
| Writing selector queries | No - skill `sf-fflib-selector-layer` |
| Writing the tests | No - skill `sf-fflib-testing` |

## Quick reference

| Concern | Mechanism | Where it lives |
| --- | --- | --- |
| Trigger dispatch | `fflib_SObjectDomain.triggerHandler(X.class)` | One trigger per object |
| Per-user / per-integration bypass | Custom permission read with `FeatureManagement.checkPermission` | Checked in one `BypassService` |
| Admin-tunable, deployable toggle | Custom metadata `__mdt` read with `getInstance` / `getAll` | No SOQL cost |
| Implementation swap | `Application.Service` binding chosen from custom metadata | Factory construction |
| Async service run | Queueable + `System.Finalizer`, or Batch with a selector `QueryLocator` | `references/async-and-bulk.md` |
| Reliable event emission | `uow.registerPublishAfterSuccessTransaction(...)` | Service |
| Deployment ordering | apex-mocks, then apex-common, then app code | `references/packaging-and-deployment.md` |

## Core patterns

### 1. Trigger inventory and dispatch strategy

An fflib org has exactly one trigger per object, and that trigger does nothing but dispatch.
Inventory the org before changing anything:

```bash
sf data query --target-org vf-dev --use-tooling-api \
  --query "SELECT Name, TableEnumOrId, Status, ApiVersion FROM ApexTrigger ORDER BY TableEnumOrId"
```

| Finding | Action |
| --- | --- |
| Two triggers on one object | Merge into one; a second trigger re-enters the dispatcher with a different record set and breaks stateful domains |
| Trigger with inline logic | Move the body into a domain override, leave the dispatch line |
| Legacy handler framework alongside fflib | Migrate object by object; during the transition, the single trigger calls the legacy handler **and** `fflib_SObjectDomain.triggerHandler`, in that order, so ordering stays deterministic |
| Record-triggered Flow doing the same work | Decide one owner per rule; Flows and Apex triggers interleave by order of execution, not by intent (skill `sf-flow-automation`) |

### 2. Bypass and kill switches

`fflib_SObjectDomain.getTriggerEvent(...)` is transaction-scoped Apex state - useful inside a job, useless
as an operational switch. Operational switches need a single, testable read point:

```apex
public with sharing class BypassService
{
    private static Map<String, Boolean> cache = new Map<String, Boolean>();

    public static Boolean isBypassed(SObjectType objectType)
    {
        return isBypassed('Trigger_' + objectType.getDescribe().getName());
    }

    public static Boolean isBypassed(String featureName)
    {
        if (cache.containsKey(featureName)) { return cache.get(featureName); }

        Bypass__mdt setting = Bypass__mdt.getInstance(featureName);   // no SOQL cost
        Boolean bypassed = setting != null
            && (setting.Disabled__c
                || (String.isNotBlank(setting.CustomPermission__c)
                    && FeatureManagement.checkPermission(setting.CustomPermission__c)));

        cache.put(featureName, bypassed);
        return bypassed;
    }

    @TestVisible
    private static void setBypass(String name, Boolean value) { cache.put(name, value); }
}
```

```apex
public override void onAfterUpdate(Map<Id, SObject> existingRecords)
{
    if (BypassService.isBypassed(Opportunity.SObjectType)) { return; }
    // ...
}
```

`__mdt.getInstance(...)` and `getAll()` read from the metadata cache and do not consume SOQL queries;
only the first 255 characters of any field are returned
([Custom metadata types methods](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_methods_system_custom_metadata_types.htm)).
Full implementations with tests, plus the data-load bypass used with `sf data import bulk`
(skill `sf-data-management`): [references/bypass-and-feature-flags.md](references/bypass-and-feature-flags.md).

### 3. Feature flags that swap factory bindings

fflib makes a feature flag a *binding* change rather than an `if` scattered through the code:

```apex
public class Application
{
    public static final fflib_Application.ServiceFactory Service =
        new fflib_Application.ServiceFactory(serviceBindings());

    private static Map<Type, Type> serviceBindings()
    {
        Boolean useV2 = !BypassService.isBypassed('Feature_NewPricing');
        return new Map<Type, Type>{
            IProjectsService.class => ProjectsServiceImpl.class,
            IPricingService.class  => useV2 ? PricingServiceV2Impl.class
                                            : PricingServiceV1Impl.class
        };
    }
}
```

Both implementations stay deployed and tested; the switch is metadata. Rollback is a metadata
deploy, not a code revert.

### 4. Async runners

Rules that do not change:

| Rule | Reason |
| --- | --- |
| The async class is a shell; it calls a service | Business logic stays testable synchronously |
| One Unit of Work per chunk / per Queueable execution | Each is its own transaction; a UoW cannot cross them |
| Never pass a UoW or a domain instance into a Queueable | SObject references have no committed context in the next transaction |
| Idempotency key on every chunk | Batch chunks can be retried by the platform |
| Finalizer for failure handling and retry | Runs in its own transaction, so it can call out after the job did DML |

```apex
public with sharing class ProjectSyncQueueable
    implements Queueable, Database.AllowsCallouts, System.Finalizer
{
    private final Set<Id> projectIds;
    private final String correlationId;

    public ProjectSyncQueueable(Set<Id> projectIds, String correlationId)
    {
        this.projectIds = projectIds;
        this.correlationId = correlationId;
    }

    public void execute(QueueableContext context)
    {
        System.attachFinalizer(this);          // exactly one finalizer per job
        ProjectSyncService.sync(projectIds, correlationId);
    }

    public void execute(FinalizerContext context)
    {
        if (context.getResult() == ParentJobResult.SUCCESS) { return; }
        LoggingService.recordAsyncFailure(
            correlationId, context.getAsyncApexJobId(), context.getException());
    }
}
```

`System.attachFinalizer` accepts one finalizer per Queueable execution; the finalizer runs in a
separate Apex and database transaction, and a failing job can be re-enqueued from a finalizer at
most five consecutive times
([Transaction finalizers](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_transaction_finalizers.htm)).
Batch, chunking and idempotency keys: [references/async-and-bulk.md](references/async-and-bulk.md)
and skill `sf-async-apex-patterns`.

### 5. Platform events and integration flows

Publish through the Unit of Work so emission is tied to commit outcome, and subscribe with an
ordinary fflib domain over the `__e` records:

```apex
trigger ProjectEvents on ProjectEvent__e (after insert)
{
    fflib_SObjectDomain.triggerHandler(ProjectEvents.class);
}
```

```apex
public inherited sharing class ProjectEvents extends fflib_SObjectDomain
{
    public ProjectEvents(List<ProjectEvent__e> records)
    {
        super(records, ProjectEvent__e.SObjectType);
        // The Automated Process user has no CRUD on the related objects
        Configuration.disableTriggerCRUDSecurity();
    }

    public override void onAfterInsert()
    {
        Set<Id> opportunityIds = new Set<Id>();
        for (ProjectEvent__e event : (List<ProjectEvent__e>) Records)
        {
            if (event.Action__c == 'ProjectCreated')
            {
                opportunityIds.add((Id) event.Opportunity__c);   // event field is Text
            }
        }
        if (opportunityIds.isEmpty()) { return; }
        DeliveryHandoffService.handOff(opportunityIds);
    }

    public class Constructor implements fflib_SObjectDomain.IConstructable
    {
        public fflib_SObjectDomain construct(List<SObject> records)
        {
            return new ProjectEvents((List<ProjectEvent__e>) records);
        }
    }
}
```

Use the two-argument `super(records, SObjectType)` constructor: an empty `__e` batch cannot infer its
type. Replay, retry and high-volume subscriber concerns: skill `sf-integration-patterns`.

### 6. Callouts and `commitWork()`

Apex forbids a callout after uncommitted DML in the same transaction. `commitWork()` is DML, so:

| Order | Verdict |
| --- | --- |
| Callout, then register, then `commitWork()` | Correct |
| `commitWork()`, then callout in the same transaction | Throws `You have uncommitted work pending` |
| `commitWork()`, then callout from a Queueable or a Finalizer | Correct - separate transaction |
| Callout inside an `IDoWork` registered with `registerWork` | Wrong - `doWork()` runs inside the commit, after DML |

```apex
public void pushToDelivery(Set<Id> projectIds)
{
    DeliveryResponse response = DeliveryGateway.post(buildPayload(projectIds));   // callout first

    fflib_ISObjectUnitOfWork uow = Application.UnitOfWork.newInstance();
    for (Project__c project : ProjectsSelector.newInstance().selectSObjectsById(projectIds))
    {
        project.ExternalId__c = response.idByProject.get(project.Id);
        uow.registerDirty(project, new List<SObjectField>{ Project__c.ExternalId__c });
    }
    uow.commitWork();                                                            // DML last
}
```

Mocking the gateway: skill `sf-fflib-testing`; named credentials and retry: skill
`sf-integration-patterns`.

### 7. Large data volumes

| Cost | Measurement | Mitigation |
| --- | --- | --- |
| Domain instantiation per chunk | `fflib_SObjectDomain` copies the record list and describes the SObject once per construction | One domain instance per chunk, never per record |
| Selector field list breadth | Heap grows with fields x rows | Narrow selector methods for bulk jobs (skill `sf-fflib-selector-layer`) |
| UoW DML statements | 1 savepoint + 1 per non-empty type per operation | One `commitWork()` per chunk |
| Relationship resolution | Iterates registered relationships per type | Register parents and children in one pass |
| Trigger re-entry during commit | Each UoW insert fires the target object's trigger | Bypass the sub-object's domain for the job when the job already owns that logic |

Batch scope for fflib work starts at 200 and comes down only with evidence; profile with a debug log
before changing it (skill `sf-debugging-logs`). Limit arithmetic: skill `sf-governor-limits`; query
shape: skill `sf-soql-sosl-optimization`.

Bypassing the framework for a bulk job is legitimate when the job is a pure data movement with no
business rules - document the decision in the job class header and keep the bypass narrow.

### 8. Observability

```apex
fflib_ISObjectUnitOfWork uow = Application.UnitOfWork.newInstance();
String correlationId = LoggingService.newCorrelationId();

uow.registerNew(new AppLog__c(
    CorrelationId__c = correlationId,
    Source__c = 'ProjectsServiceImpl.createFromOpportunities',
    Level__c = 'INFO',
    Message__c = 'Creating ' + toCreate.size() + ' projects',
    CpuTimeMs__c = Limits.getCpuTime()));
```

A log row registered on the **business** UoW disappears with the rollback. When the log must survive
a failure, use a second UoW committed in the `catch`, or
`registerPublishAfterFailureTransaction` on a platform event whose subscriber writes the log. The
correlation id is threaded through service, Queueable, finalizer and event payload so one incident
is one query. Trace flags and log levels: skill `sf-debugging-logs`.

### 9. Deployment, packaging and analysis

Dependency order is fixed: `fflib-apex-mocks`, then `fflib-apex-common`, then application code.
Vendored fflib test classes inflate the denominator of the org coverage gate - either exclude them
from the package directory or account for them in the gate. Package layout, `sfdx-project.json`
`dependencies`, test levels and coverage handling:
[references/packaging-and-deployment.md](references/packaging-and-deployment.md), plus skills
`sf-packaging-release` and `sf-deployment-strategies`.

Code Analyzer misfires predictably on fflib: `ApexCRUDViolation` on selectors that enforce access
through `fflib_SObjectSelector`, `ApexFlsViolationRule` (Graph Engine) on writes routed through a
custom `IDML`, `ApexSharingViolations` on `inherited sharing` domains, cyclomatic complexity on the
dispatcher. Scope the suppression to the framework path, never the whole workspace - table and YAML
in [references/review-and-upgrade.md](references/review-and-upgrade.md) and skill
`sf-code-analyzer-quality`.

### 10. Wave model

| Wave | Agent | fflib responsibility | Gate |
| --- | --- | --- | --- |
| 0 | `sf-scout` | Trigger inventory, existing domains/selectors/services, fflib version | - |
| 1 | `sf-apex-engineer` | Domain, service, selector, UoW wiring, `Application` registration | - |
| 2 | `sf-test-engineer` | Mocked layer tests plus one DML integration test per object | `vf-check local` |
| 2 | `sf-quality-gate` | `code-analyzer.yml` suppressions justified, no new debt | `vf-check analyzer` |
| 2 | `sf-security-reviewer` | `UserModeDML`, every `disableTriggerCRUDSecurity()`, sharing declarations | `vf-check analyzer` |
| 3 | `sf-deploy-engineer` | Dependency-ordered deploy, validate then quick deploy | `vf-check deploy-validate` |
| 4 | `sf-org-verifier` | Trigger fires, UoW commits, events published | `vf-check smoke` |

Orchestration details: skill `sf-workflow-orchestration`; smoke probe design: skill
`sf-post-deploy-verification`.

## Anti-patterns

**A bypass read per record.**

```apex
// WRONG - metadata lookup and describe repeated per record
for (Opportunity opp : (List<Opportunity>) Records)
{
    if (BypassService.isBypassed(Opportunity.SObjectType)) { continue; }
}

// RIGHT - one check, early return
if (BypassService.isBypassed(Opportunity.SObjectType)) { return; }
for (Opportunity opp : (List<Opportunity>) Records) { /* ... */ }
```

**A global "disable all triggers" checkbox.** It hides the blast radius and gets left on. Scope
switches per object and per feature, and log every activation.

**`commitWork()` inside a Batch `execute` loop.** One `commitWork()` per `execute`, outside any loop.

**Callout inside `IDoWork`.** `doWork()` runs after DML inside `commitWork()`; the callout throws.

**Upgrading fflib by copying the new classes over the old ones.** Diff first; `fflib_SObjectDomain`
and `fflib_SObjectUnitOfWork` have changed defaults between versions. Runbook:
[references/review-and-upgrade.md](references/review-and-upgrade.md).

## Verification

```bash
# Static gate, including the fflib-specific analyzer configuration
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer --changed
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# Org tests and coverage gates
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-int

# Dependency-ordered validation, then quick deploy
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" deploy-validate --target-org vf-int
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" deploy-quick --target-org vf-int

# Post-deploy verification
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" smoke --target-org vf-int

# Trigger inventory: exactly one trigger per object
sf data query --target-org vf-int --use-tooling-api --json \
  --query "SELECT TableEnumOrId, COUNT(Id) triggers FROM ApexTrigger GROUP BY TableEnumOrId" \
  | jq -r '.result.records[] | select(.triggers > 1) | .TableEnumOrId'
```

## References

- [references/bypass-and-feature-flags.md](references/bypass-and-feature-flags.md) - custom metadata and
  custom permission implementations with tests, data-load bypass, feature-flag binding swaps.
- [references/async-and-bulk.md](references/async-and-bulk.md) - Queueable plus Finalizer service runner,
  Batch with a selector `QueryLocator`, per-chunk Unit of Work, idempotency keys, LDV profiling.
- [references/packaging-and-deployment.md](references/packaging-and-deployment.md) - package layout,
  dependency ordering, deploy commands, test levels, coverage handling.
- [references/review-and-upgrade.md](references/review-and-upgrade.md) - PR checklist, fflib upgrade
  runbook, misfiring analyzer rules and scoped suppressions.

Sibling skills: `sf-fflib-foundations`, `sf-fflib-selector-layer`, `sf-fflib-domain-service-uow`,
`sf-fflib-testing`, `sf-async-apex-patterns`, `sf-governor-limits`, `sf-soql-sosl-optimization`,
`sf-integration-patterns`, `sf-flow-automation`, `sf-data-management`, `sf-debugging-logs`,
`sf-code-analyzer-quality`, `sf-deployment-strategies`, `sf-packaging-release`, `sf-cli-operations`,
`sf-project-structure`, `sf-scratch-orgs-sandboxes`, `sf-workflow-orchestration`,
`sf-post-deploy-verification`, `sf-security-model`.

Official docs used:
[Transaction finalizers](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_transaction_finalizers.htm),
[Custom metadata types methods](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_methods_system_custom_metadata_types.htm),
[Publish platform events with Apex](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_publish_apex.htm),
[Execution governors and limits](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm),
[Code Analyzer suppressions](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/suppress-violations.html).
