---
name: sf-fflib-domain-service-uow
description: Covers the write side of the fflib Apex Enterprise Patterns stack - fflib_SObjectDomain trigger domains (onApplyDefaults, onValidate, onBeforeInsert, onAfterUpdate, handleBeforeInsert dispatch, Configuration flags, DomainException), the service layer (IXxxService + XxxServiceImpl + Application.Service.newInstance, transaction ownership, thin @AuraEnabled and @InvocableMethod entry points), and fflib_SObjectUnitOfWork (registerNew, registerDirty, registerRelationship, registerPublishAfterSuccessTransaction, commitWork, custom IDML with AccessLevel.USER_MODE, SObject commit ordering). Use this skill when writing or reviewing a one-line fflib trigger, a domain class with a Constructor inner class, a service that owns commitWork, a Unit of Work registration chain, or when deciding where a piece of business logic belongs in an fflib org.
---

# fflib Domain, Service and Unit of Work

The write side of Apex Enterprise Patterns. Selectors read (skill `sf-fflib-selector-layer`);
Domain, Service and Unit of Work decide, validate and write.

All `fflib_*` signatures below were read from `apex-enterprise-patterns/fflib-apex-common`,
branch `master`, commit `dab59777bac37f6b8a3cc2871fcf5df8d37764b4` (2026-09-10), under
`sfdx-source/apex-common/main/classes/`. Wiring examples were read from
`apex-enterprise-patterns/fflib-apex-common-samplecode`, branch `master`, commit
`4657d6325b3d6ae41bc7af864ca4f41287e72112`.

## When to use

| Situation | Use this skill |
| --- | --- |
| Writing a trigger in an fflib org | Yes - one-line `fflib_SObjectDomain.triggerHandler` body |
| Record-level validation that must fire on every write path | Yes - domain `onValidate` |
| Orchestrating multi-object writes in one transaction | Yes - service + Unit of Work |
| Exposing logic to LWC, Flow, REST or Batch | Yes - thin entry point delegating to a service |
| Querying with field-level security and a query factory | No - skill `sf-fflib-selector-layer` |
| `Application` factory wiring, `fflib_ISObjectUnitOfWork` mocking basics | No - skill `sf-fflib-foundations` |
| Writing the tests for any of the above | No - skill `sf-fflib-testing` |
| Bypass switches, async runners, packaging, upgrades | No - skill `sf-fflib-operations` |
| Hand-rolled trigger handler frameworks, no fflib | No - skill `sf-apex-development` |

## Decision table: where does the logic go?

| Logic | Layer | Why |
| --- | --- | --- |
| Default a field on insert | Domain `onApplyDefaults()` | Runs before insert, no DML needed |
| "Field A is required when B is set" | Domain `onValidate()` | Must hold for every write path including Data Loader |
| "Field X cannot change after creation" | Domain `onValidate(Map<Id,SObject> existingRecords)` | Needs old values |
| Compute a roll-up onto a parent | Domain method invoked by a service, writes via UoW | Needs cross-object transaction |
| "Close the opportunity and create the project" | Service method | Owns the transaction, spans objects |
| Query the records first | Selector, called by the service | Domain classes never query |
| Send the platform event | UoW `registerPublishAfterSuccessTransaction` | Publish only if the transaction commits |
| Enqueue async follow-up | Service method returning the job Id | Keeps `System.enqueueJob` out of domain code |
| Convert records to a UI shape | Controller/DTO, not the domain | Domain holds behaviour, not presentation |

## Core patterns

### 1. The one-line trigger

The trigger contains a single dispatch call. The dispatcher resolves the domain constructor,
constructs the domain over the correct record set and calls the matching `handleXxx` method.

```apex
trigger Opportunities on Opportunity (
    before insert, before update, before delete,
    after insert, after update, after delete, after undelete)
{
    fflib_SObjectDomain.triggerHandler(OpportunitiesTriggerHandler.class);
}
```

`triggerHandler(Type domainClass)` resolves the constructor as
`domainClassName.endsWith('Constructor') ? Type.forName(domainClassName) : Type.forName(domainClassName + '.Constructor')`,
so every domain class registered for trigger dispatch **must** expose a public inner class named
`Constructor` implementing `fflib_SObjectDomain.IConstructable` (or `IConstructable2` when the
SObjectType must be passed for empty lists). Compare with the hand-rolled dispatcher in skill
`sf-apex-development`: fflib replaces the `if (Trigger.isBefore && Trigger.isInsert)` ladder and the
handler interface with this single static call.

### 2. Domain class anatomy

```apex
public inherited sharing class OpportunitiesTriggerHandler extends fflib_SObjectDomain
{
    public OpportunitiesTriggerHandler(List<Opportunity> sObjectList)
    {
        super(sObjectList);
        // Opt out of the base-class CRUD check when a custom IDML enforces user mode instead
        Configuration.disableTriggerCRUDSecurity();
    }

    public override void onApplyDefaults()
    {
        for (Opportunity opp : (List<Opportunity>) Records)
        {
            if (opp.CloseDate == null) { opp.CloseDate = System.today().addDays(30); }
        }
    }

    public override void onValidate()
    {
        for (Opportunity opp : (List<Opportunity>) Records)
        {
            if (opp.Type != null && opp.Type.startsWith('Existing') && opp.AccountId == null)
            {
                opp.AccountId.addError(
                    error('Existing-customer Opportunities require an Account.', opp, Opportunity.AccountId));
            }
        }
    }

    public override void onValidate(Map<Id, SObject> existingRecords)
    {
        for (Opportunity opp : (List<Opportunity>) Records)
        {
            Opportunity existing = (Opportunity) existingRecords.get(opp.Id);
            if (opp.Type != existing.Type)
            {
                opp.Type.addError(error('Opportunity Type is immutable.', opp, Opportunity.Type));
            }
        }
    }

    public class Constructor implements fflib_SObjectDomain.IConstructable
    {
        public fflib_SObjectDomain construct(List<SObject> sObjectList)
        {
            return new OpportunitiesTriggerHandler(sObjectList);
        }
    }
}
```

`Records` is a property returning `getRecords()` (inherited from `fflib_SObjects`); the domain owns
its own copy of the list. `error(...)` records the message in `fflib_SObjectDomain.Errors` so tests
can assert on validation without DML. Full dispatch table and every `Configuration` flag:
[references/domain-layer.md](references/domain-layer.md).

### 3. Service owns the transaction

```apex
public interface IProjectsService
{
    Set<Id> createFromOpportunities(Set<Id> opportunityIds);
}
```

```apex
public with sharing class ProjectsService
{
    public static Set<Id> createFromOpportunities(Set<Id> opportunityIds)
    {
        return service().createFromOpportunities(opportunityIds);
    }

    private static IProjectsService service()
    {
        return (IProjectsService) Application.Service.newInstance(IProjectsService.class);
    }
}
```

The static shim keeps call sites terse; `Application.Service.newInstance` returns the registered
implementation or a mock injected by `setMock`. The implementation creates the Unit of Work, hands
it to domain methods, and is the only place that calls `commitWork()`. Never call `commitWork()`
inside a domain method or a trigger context - the caller owns the transaction.

### 4. Unit of Work registration chain

```apex
public with sharing class ProjectsServiceImpl implements IProjectsService
{
    public Set<Id> createFromOpportunities(Set<Id> opportunityIds)
    {
        fflib_ISObjectUnitOfWork uow = Application.UnitOfWork.newInstance();

        List<Opportunity> opps = OpportunitiesSelector.newInstance()
            .selectByIdWithLineItems(opportunityIds);

        List<Project__c> created = new List<Project__c>();
        for (Opportunity opp : opps)
        {
            Project__c project = new Project__c(
                Name = opp.Name.left(80),
                Account__c = opp.AccountId,
                Stage__c = 'Planning');
            uow.registerNew(project, Project__c.Opportunity__c, opp);  // opp already has an Id
            created.add(project);

            Integer sequence = 1;
            for (OpportunityLineItem line : opp.OpportunityLineItems)
            {
                ProjectTask__c task = new ProjectTask__c(
                    Name = line.Description == null ? 'Task ' + sequence : line.Description.left(80),
                    Sequence__c = sequence++);
                uow.registerNew(task, ProjectTask__c.Project__c, project); // parent has no Id yet
            }

            uow.registerPublishAfterSuccessTransaction(
                new ProjectEvent__e(Opportunity__c = opp.Id, Action__c = 'Created'));
        }

        uow.commitWork();

        Set<Id> projectIds = new Set<Id>();
        for (Project__c project : created) { projectIds.add(project.Id); }
        return projectIds;
    }
}
```

`registerNew(SObject record, Schema.SObjectField relatedToParentField, SObject relatedToParentRecord)`
registers the child and defers the lookup assignment until the parent is inserted. The order of
`SObjectType`s passed to `Application.UnitOfWork` decides insert order, so `Project__c` must appear
before `ProjectTask__c`. Full API table, relationship variants and commit lifecycle:
[references/unit-of-work.md](references/unit-of-work.md).

### 5. Thin entry points

Every external caller is a shell over a service call. Controllers, invocable actions, REST resources
and async runners add no business logic.

```apex
public with sharing class ProjectCreationController
{
    @AuraEnabled
    public static List<Id> createProjects(List<Id> opportunityIds)
    {
        try
        {
            return new List<Id>(ProjectsService.createFromOpportunities(new Set<Id>(opportunityIds)));
        }
        catch (Exception e)
        {
            throw new AuraHandledException(e.getMessage());
        }
    }
}
```

```apex
public with sharing class CreateProjectsAction
{
    public class Request
    {
        @InvocableVariable(required=true) public Id opportunityId;
    }

    @InvocableMethod(label='Create Project From Opportunity' category='Projects')
    public static void run(List<Request> requests)
    {
        Set<Id> ids = new Set<Id>();
        for (Request r : requests) { ids.add(r.opportunityId); }
        ProjectsService.createFromOpportunities(ids);   // one bulk call, not one per request
    }
}
```

LWC wiring is in skill `sf-lwc-development`; Flow invocable semantics and bulk behaviour in skill
`sf-flow-automation`; Queueable and Batch entry points in skills `sf-async-apex-patterns` and
`sf-fflib-operations`.

### 6. User-mode DML through a custom `IDML`

`fflib_SObjectUnitOfWork.SimpleDML` performs `System.Database.insert(objList, AccessLevel.SYSTEM_MODE)`.
`fflib_SObjectUnitOfWork.UserModeDML extends SimpleDML` and defaults to `AccessLevel.USER_MODE`. Wire
it once in the `Application` factory rather than at every call site:

```apex
private class UserModeUnitOfWorkFactory extends fflib_Application.UnitOfWorkFactory
{
    public UserModeUnitOfWorkFactory(List<SObjectType> objectTypes) { super(objectTypes); }

    public override fflib_ISObjectUnitOfWork newInstance()
    {
        if (m_mockUow != null) { return m_mockUow; }
        return new fflib_SObjectUnitOfWork(m_objectTypes, new fflib_SObjectUnitOfWork.UserModeDML());
    }
}
```

This is exactly the pattern used by `Application.cls` in fflib-apex-common-samplecode. Permission
semantics and `AccessLevel` trade-offs: skill `sf-security-model`.

## Anti-patterns

**Committing inside the domain.**

```apex
// WRONG - the domain does not own the transaction and cannot be composed
public override void onAfterInsert()
{
    fflib_ISObjectUnitOfWork uow = Application.UnitOfWork.newInstance();
    uow.registerNew(buildAuditRecords());
    uow.commitWork();
}
```

```apex
// RIGHT - domain methods accept the caller's UoW
public void logAudit(fflib_ISObjectUnitOfWork uow)
{
    uow.registerNew(buildAuditRecords());
}
```

**Row-at-a-time service signatures.**

```apex
// WRONG - callers loop, every loop iteration opens a transaction
void createProject(Id opportunityId);
```

```apex
// RIGHT - bulk-first, the service loops internally once
Set<Id> createFromOpportunities(Set<Id> opportunityIds);
```

**SOQL inside a domain class.** Domain classes receive records; they never query. Inject data via a
selector call in the service, or pass a pre-queried list. See skill `sf-fflib-selector-layer`.

**Hand-rolled savepoints around a `commitWork()`.** `commitWork()` already sets a savepoint, rolls
back on exception and rethrows. Wrapping it adds two more DML statements against the 150-statement
limit ([Apex transaction control](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/langCon_apex_transaction_control.htm)).
Only add an outer savepoint when you must keep earlier, already-committed work in the same
transaction.

**`registerDirty` on a record the domain also mutates after registration.** The UoW holds the same
reference; late mutations silently ship. Register last, or use the field-scoped
`registerDirty(SObject, List<SObjectField>)` overload.

**Multiple `commitWork()` calls to "flush" work.** Each call is a fresh savepoint plus DML per
SObject type. Register everything, commit once. Governor arithmetic: skill `sf-governor-limits`.

**A second trigger on the same object.** fflib assumes one trigger per object; a second trigger
re-enters the dispatcher with a different record set and breaks stateful domains. See skill
`sf-fflib-operations` for the inventory and migration procedure.

## Verification

```bash
# Local gate: format, lint, Code Analyzer, Jest
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# Static analysis only (PMD rules that misfire on fflib are listed in sf-fflib-operations)
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer --changed

# Org tests plus coverage gates (apexOrgCoverageMin 85, apexClassCoverageMin 75)
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-dev

# Narrow run while iterating on one domain or service
sf apex run test --target-org vf-dev --synchronous --code-coverage --result-format human \
  --tests ProjectsServiceTest --tests OpportunitiesTriggerHandlerTest

# Prove the trigger dispatches and the UoW commits in a real org
sf apex run --target-org vf-dev --file scripts/apex/create-projects-smoke.apex
sf data query --target-org vf-dev \
  --query "SELECT Id, Name, Opportunity__c FROM Project__c ORDER BY CreatedDate DESC LIMIT 5"
```

Checklist before opening the PR:

| Check | Expected |
| --- | --- |
| Trigger body | Exactly one `fflib_SObjectDomain.triggerHandler(...)` call |
| Domain class | Has `Constructor` inner class implementing `IConstructable` |
| Domain class | No SOQL, no DML, no `commitWork()` |
| Service interface | Bulk signatures (`Set<Id>`, `List<...>`, `Map<Id,...>`) |
| Service impl | Creates UoW, calls `commitWork()` exactly once per public method |
| UoW type list | Parents before children in `Application.UnitOfWork` |
| Platform events | Registered with `registerPublishAfterSuccessTransaction` unless failure telemetry is wanted |
| Entry points | `@AuraEnabled` / `@InvocableMethod` contain no business logic |

## References

- [references/domain-layer.md](references/domain-layer.md) - dispatch table, every override, `Configuration`
  flags, `TriggerEvent` toggles, stateful domains, `Test.Database` mock DML, error handling.
- [references/service-layer.md](references/service-layer.md) - interface/impl/controller/invocable chain for
  one feature, exception policy, transaction ownership, DTO rules.
- [references/unit-of-work.md](references/unit-of-work.md) - full `fflib_ISObjectUnitOfWork` API table,
  relationship registration, platform events, custom `IDML`, commit order, limits.
- [references/end-to-end-feature.md](references/end-to-end-feature.md) - one requirement implemented across
  Selector, Domain, Service, UoW, controller and invocable action, with every file.

Sibling skills: `sf-fflib-foundations`, `sf-fflib-selector-layer`, `sf-fflib-testing`,
`sf-fflib-operations`, `sf-apex-development`, `sf-apex-testing`, `sf-async-apex-patterns`,
`sf-governor-limits`, `sf-security-model`, `sf-soql-sosl-optimization`, `sf-lwc-development`,
`sf-flow-automation`, `sf-integration-patterns`, `sf-code-analyzer-quality`.

Upstream sources:

- [fflib-apex-common](https://github.com/apex-enterprise-patterns/fflib-apex-common) - `master`,
  `sfdx-source/apex-common/main/classes/fflib_SObjectDomain.cls`, `fflib_SObjectUnitOfWork.cls`,
  `fflib_ISObjectUnitOfWork.cls`, `fflib_Application.cls`, `fflib_SObjects.cls`.
- [fflib-apex-common-samplecode](https://github.com/apex-enterprise-patterns/fflib-apex-common-samplecode) -
  `Application.cls`, `domains/Opportunities.cls`, `service/OpportunitiesServiceImpl.cls`,
  `triggerHandlers/OpportunitiesTriggerHandler.cls`, `triggers/Opportunities.trigger`.
- [fflib.dev](https://fflib.dev/docs/domain-layer/example) - layer conventions.
- [Apex transaction control](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/langCon_apex_transaction_control.htm),
  [Execution governors and limits](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm),
  [Publish platform events with Apex](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_publish_apex.htm).
