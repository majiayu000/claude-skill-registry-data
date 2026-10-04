---
name: sf-fflib-foundations
description: Covers the fflib Apex Enterprise Patterns stack (fflib-apex-common, fflib-apex-mocks) - the four-layer Service/Domain/Selector/Unit of Work separation, the Application factory class with its SObject-to-class binding maps, interface plus implementation naming, installation by vendoring or git submodule, sfdx-project.json and .forceignore wiring for a dedicated fflib package directory, the setMock injection points used by unit tests, PMD/Code Analyzer ruleset scoping for fflib code, and an honest decision table for when plain trigger handlers plus service classes are the better answer. Use it when a project adds or removes fflib, when creating or editing Application.cls, when deciding whether a requirement deserves a Service/Domain/Selector split, when migrating legacy Apex to Apex Enterprise Patterns, or when fflib_Application.DeveloperException, "No implementation registered for service interface", or "Selector class not found for SObjectType" appears in a log.
---

# fflib Foundations: Apex Enterprise Patterns

Source of truth for every signature below: `apex-enterprise-patterns/fflib-apex-common` @ `master`
commit `dab5977` (`sfdx-source/apex-common/main/classes/*.cls`),
`fflib-apex-mocks` @ `master` commit `d81e9e1`,
`fflib-apex-common-samplecode` @ `master` commit `4657d63`. Anything not read from those files
this session is marked `[unverified]`.

## When to use

| Situation | Use this skill |
| --- | --- |
| Adding fflib to a repo for the first time | Yes - `references/install-and-layout.md` |
| Writing or fixing `Application.cls` | Yes - `references/application-factory.md` |
| Choosing fflib vs trigger handler + service class | Yes - `references/fflib-vs-plain-apex.md` |
| Looking up what an `fflib_*` class does | Yes - `references/class-catalogue.md` |
| Writing a selector or a query | Skill `sf-fflib-selector-layer` |
| Writing a domain, service, or Unit of Work | Skill `sf-fflib-domain-service-uow` |
| Mocking, stubbing, verifying with ApexMocks | Skill `sf-fflib-testing` |
| Trigger wiring, batch entry points, day-2 operations | Skill `sf-fflib-operations` |
| Plain Apex idioms, no fflib in the repo | Skill `sf-apex-development` |

## Decision table: does fflib earn its keep here?

| Signal | fflib | Plain trigger handler + service classes |
| --- | --- | --- |
| SObjects with non-trivial write logic | > 5 | <= 5 |
| Apex classes in the package | > 40 | < 40 |
| Multiple entry points per SObject (trigger, LWC, REST, batch, Flow invocable) | Yes | One or two |
| Unit tests must run without DML (`Set<Id>` + stubs) | Required | Nice to have |
| Second-generation packaging with a shared base library | Yes | No |
| Team has used Apex Enterprise Patterns before | Yes | No, and no budget to learn |
| Automation mostly Flow / Record-Triggered Flow | No | Yes - see skill `sf-flow-automation` |
| Org is a single-admin org with < 10 Apex classes | No | Yes |

Two or more "plain" answers means do not adopt fflib. The library costs roughly 3 extra files per
SObject (interface, implementation, mock registration) and a permanent onboarding tax. See
`references/fflib-vs-plain-apex.md` for the same requirement implemented both ways.

## Core patterns

### 1. The four layers and the dependency rules

```
Entry points        triggers, LWC @AuraEnabled controllers, REST resources,
                    Batchable/Queueable, InvocableMethod
      |  (only calls)
Service layer       coarse-grained, bulkified, transaction boundary, owns the UnitOfWork
      |
Domain layer        record-oriented behaviour + validation for one SObjectType
      |
Selector layer      all SOQL
      |
Unit of Work        all DML, ordered by SObjectType dependency
```

Enforceable rules, in priority order:

| Rule | Why |
| --- | --- |
| Only the Service layer calls `commitWork()` | one transaction boundary per use case |
| Selectors never call services or domains | they would become untestable and recursive |
| Domains never issue SOQL or DML directly | they get records in, register work out |
| Entry points contain no business logic, only marshalling | lets Flow/LWC/REST share behaviour |
| Every layer is reached through `Application.*`, never `new Impl()` in product code | mock injection |
| Service methods take and return bulk shapes (`Set<Id>`, `List<SObject>`) | see skill `sf-governor-limits` |

### 2. `Application.cls` is the only wiring file

One class per package, four static finals. Verified shape from
`fflib-apex-common-samplecode/.../main/classes/Application.cls`:

```apex
public class Application {
    // SObjectTypes in dependency order: parents before children.
    public static final fflib_Application.UnitOfWorkFactory UnitOfWork =
        new fflib_Application.UnitOfWorkFactory(
            new List<SObjectType> {
                Account.SObjectType,
                Opportunity.SObjectType,
                OpportunityLineItem.SObjectType,
                Invoice__c.SObjectType,
                InvoiceLine__c.SObjectType });

    // Interface -> implementing class.
    public static final fflib_Application.ServiceFactory Service =
        new fflib_Application.ServiceFactory(
            new Map<Type, Type> {
                IAccountsService.class => AccountsServiceImpl.class,
                IOpportunitiesService.class => OpportunitiesServiceImpl.class });

    // SObjectType -> selector class.
    public static final fflib_Application.SelectorFactory Selector =
        new fflib_Application.SelectorFactory(
            new Map<SObjectType, Type> {
                Account.SObjectType => AccountsSelector.class,
                Opportunity.SObjectType => OpportunitiesSelector.class });

    // SObjectType -> domain constructor class.
    public static final fflib_Application.DomainFactory Domain =
        new fflib_Application.DomainFactory(
            Application.Selector,
            new Map<SObjectType, Type> {
                Account.SObjectType => Accounts.Constructor.class,
                Opportunity.SObjectType => Opportunities.Constructor.class });
}
```

`newInstance` resolves the registered `Type` and calls `Type.newInstance()`, so every registered
class needs a public zero-argument constructor. Unregistered lookups throw
`fflib_Application.DeveloperException` with `No implementation registered for service interface X`
or `Selector class not found for SObjectType X` (`fflib_Application.cls`). Full binding tables,
the `UserModeDML` factory subclass and the common wiring mistakes are in
`references/application-factory.md`.

### 3. Naming and file layout

The samplecode conventions, verified against its class paths:

| Layer | Interface | Implementation | Caller writes |
| --- | --- | --- | --- |
| Service | `IAccountsService` | `AccountsServiceImpl` | `AccountsService.updateOpportunityActivity(ids)` (static facade) |
| Domain | `IAccounts` | `Accounts` (+ inner `Constructor`) | `(IAccounts) Application.Domain.newInstance(ids)` |
| Selector | `IAccountsSelector extends fflib_ISObjectSelector` | `AccountsSelector` | `AccountsSelector.newInstance()` |
| Unit of Work | `fflib_ISObjectUnitOfWork` | `fflib_SObjectUnitOfWork` | `Application.UnitOfWork.newInstance()` |

The service layer is three files: a `with sharing` static facade (`AccountsService`), the interface
(`IAccountsService`), and the implementation (`AccountsServiceImpl`). The facade exists so callers
keep static call syntax while the factory still controls instantiation:

```apex
public with sharing class AccountsService {
    public static void updateOpportunityActivity(Set<Id> accountIds) {
        service().updateOpportunityActivity(accountIds);
    }
    private static IAccountsService service() {
        return (IAccountsService) Application.Service.newInstance(IAccountsService.class);
    }
}
```

Directory layout inside a package directory (samplecode uses exactly these folder names):

```
force-app/main/default/classes/
  Application.cls
  service/      AccountsService.cls  IAccountsService.cls  AccountsServiceImpl.cls
  domains/      Accounts.cls         IAccounts.cls
  selectors/    AccountsSelector.cls IAccountsSelector.cls
  triggerHandlers/ AccountsTriggerHandler.cls
  controllers/  batchjobs/  restapis/
```

### 4. Installation: vendor, submodule, or deploy

`fflib-apex-common` @ `master` publishes no unlocked-package version id and no GitHub release; the
repo has zero releases and its README advertises only a GitHub-deploy button. Any `04t...` install
id for these libraries is `[unverified]` - do not put one in a script.

```bash
# Option A (recommended): vendor into a dedicated package directory, pinned to a commit.
git clone https://github.com/apex-enterprise-patterns/fflib-apex-mocks.git /tmp/fflib-mocks
git -C /tmp/fflib-mocks checkout d81e9e1
mkdir -p fflib/main/default
cp -R /tmp/fflib-mocks/sfdx-source/apex-mocks/main/classes fflib/main/default/classes
# then fflib-apex-common on top of the same directory

# Deploy order matters only if your own tests reference ApexMocks: mocks first, then common.
sf project deploy start --source-dir fflib --target-org vf-dev --wait 20
```

`fflib-apex-common`'s current README states "**Dependencies:** None for deployment or for running
this library's Apex tests"; its `docs/changelog.md` still carries the September 2014 note that
ApexMocks "must be deployed to the org before deploying this library". The README reflects master -
deploy mocks first anyway, it is free and removes the ambiguity. Submodule and upgrade procedures:
`references/install-and-layout.md`. Packaging consequences: skills `sf-project-structure` and
`sf-packaging-release`.

### 5. Mock injection points

`setMock` on every factory is `protected` and `@TestVisible`, so it compiles only from test context
(`fflib_Application.cls`).

| Call | Argument type |
| --- | --- |
| `Application.UnitOfWork.setMock(uowMock)` | `fflib_ISObjectUnitOfWork` |
| `Application.Service.setMock(IAccountsService.class, serviceMock)` | `Type`, `Object` |
| `Application.Selector.setMock(selectorMock)` | `fflib_ISObjectSelector` - requires `sObjectType()` stubbed |
| `Application.Selector.setMock(Account.SObjectType, selectorMock)` | `SObjectType`, `fflib_ISObjectSelector` |
| `Application.Domain.setMock(domainMock)` | `fflib_ISObjectDomain` (uses `sObjectType()`) or `fflib_IDomain` (uses `getType()`) |
| `Application.Domain.setMock(Account.SObjectType, domainMock)` | `SObjectType`, `fflib_ISObjectDomain` |

The single-argument selector and domain overloads call `sObjectType()` on the mock; if it is not
stubbed the mock returns `null` and registration silently binds to `null`. fflib logs an INFO
`System.debug` in that path. Prefer the two-argument overload. Detail: skill `sf-fflib-testing`.

### 6. Incremental migration from legacy Apex (strangler)

| Step | Action | Old code |
| --- | --- | --- |
| 1 | Deploy `fflib-apex-mocks` + `fflib-apex-common`, add empty `Application.cls` | untouched |
| 2 | Extract queries of the busiest SObject into `XSelector`, register it | legacy class calls `XSelector.newInstance().selectById(ids)` |
| 3 | Introduce `fflib_ISObjectUnitOfWork` in the one method with the most DML statements | DML removed from legacy class |
| 4 | Create `IXService`/`XServiceImpl`, move the legacy method body in verbatim | legacy public method becomes a one-line delegator |
| 5 | Introduce the Domain class only once two callers need the same record-level rule | - |
| 6 | Convert the trigger last, after Service and Selector exist | - |

Keep the legacy class as a thin delegator until every caller is migrated, then delete it in the same
release; do not leave two ways to do the same thing. Never mix a legacy `[SELECT ...]` and a selector
for the same SObject in one class.

### 7. Static analysis and performance characteristics

fflib's own source suppresses PMD rules (`fflib_SObjectSelector.cls` header suppresses
`PMD.CyclomaticComplexity`, `PMD.ExcessivePublicCount`, `PMD.ApexDoc` and more), so the library
deploys clean only if your analyzer run excludes vendored paths. In your own fflib code expect:

| Rule | Trigger | Handling |
| --- | --- | --- |
| `ApexCRUDViolation` | `Database.query(qf.toSOQL())` - PMD cannot see the `WITH USER_MODE` that `toSOQL()` emits | configure `readAuthMethodPattern` for your selector base, or scope the rule out of `selectors/` |
| `ApexSOQLInjection` | dynamic query string built by `fflib_QueryFactory` | same; use `Database.queryWithBinds` for user input |
| `ApexSharingViolations` | `AccountsServiceImpl` without a sharing keyword | always declare `with sharing` or `inherited sharing` |
| `ApexDoc`, `ApexUnitTestClassShouldHaveAsserts` | generated interfaces, `Impl` classes | keep as advisory, not gating |

Exclude the vendored `fflib/` directory from the Code Analyzer target; see skill
`sf-code-analyzer-quality`. Governor cost of the factories: each `Type.newInstance()` is a reflective
instantiation (no limit consumed, small CPU cost); `fflib_SObjectDescribe` caches describes per
transaction, so a selector's first `getSObjectFieldList()` pays describe cost once. The real risks are
`getSObjectFieldList()` bloat (heap) and per-record selector calls (SOQL 100 limit) - skills
`sf-governor-limits` and `sf-soql-sosl-optimization`.

## Anti-patterns

**`new AccountsServiceImpl()` in product code.** Bypasses `Application.Service`, so
`setMock` cannot intervene and every consumer test needs DML.

```apex
// Wrong
IAccountsService svc = new AccountsServiceImpl();
// Right
IAccountsService svc = (IAccountsService) Application.Service.newInstance(IAccountsService.class);
```

**Unit of Work SObjectType list in the wrong order.** `fflib_SObjectUnitOfWork` commits in the order
given; children before parents produces `REQUIRED_FIELD_MISSING` on the lookup at commit time. List
`Account` before `Opportunity` before `OpportunityLineItem`.

**One `Application` per feature.** Two factories means two registries and two mock registries;
`setMock` on one is invisible to the other. One `Application` class per package directory.

**Service method taking a single record.** `updateOne(Id accountId)` guarantees a governor failure
when a trigger calls it per record. Take `Set<Id>` / `List<SObject>`.

**Domain class issuing SOQL.** Makes the domain untestable without DML and hides query cost inside
record loops. Query in the service, pass records down.

**Registering the domain class instead of its constructor.** `Account.SObjectType => Accounts.class`
fails at runtime unless `Accounts` itself implements a constructor interface; the samplecode registers
`Accounts.Constructor.class`. See `references/application-factory.md`.

## Verification

```bash
# 1. Local gate: format, lint, analyzer, jest. No org needed.
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# 2. Compile + run the fflib-facing tests in an org.
sf project deploy start --source-dir force-app --target-org vf-dev --wait 30
sf apex run test --target-org vf-dev --synchronous \
  --tests AccountsServiceTest --tests AccountsSelectorTest \
  --code-coverage --result-format human

# 3. Prove the factories resolve every registration (fails fast on a missing binding).
sf apex run --target-org vf-dev --file scripts/apex/assert-application-wiring.apex

# 4. Coverage + analyzer gates (apexOrgCoverageMin 85, apexClassCoverageMin 75, severity 3).
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-dev
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer
```

`scripts/apex/assert-application-wiring.apex` (anonymous Apex, run after every `Application.cls`
edit):

```apex
for (SObjectType t : new List<SObjectType>{ Account.SObjectType, Opportunity.SObjectType }) {
    fflib_ISObjectSelector s = Application.Selector.newInstance(t);
    System.assertEquals(t, s.sObjectType(), 'Selector bound to wrong SObjectType: ' + t);
}
System.assert(Application.Service.newInstance(IAccountsService.class) instanceof IAccountsService);
System.assertNotEquals(null, Application.UnitOfWork.newInstance());
```

## References

- [references/application-factory.md](references/application-factory.md) - full `Application.cls`, factory API tables, `setMock` matrix, wiring mistakes
- [references/install-and-layout.md](references/install-and-layout.md) - vendoring, submodule, `sfdx-project.json`, `.forceignore`, version pinning, upgrades
- [references/class-catalogue.md](references/class-catalogue.md) - every public `fflib_*` class in both libraries
- [references/fflib-vs-plain-apex.md](references/fflib-vs-plain-apex.md) - decision matrix and one requirement implemented twice
- fflib-apex-common: https://github.com/apex-enterprise-patterns/fflib-apex-common
- fflib-apex-mocks: https://github.com/apex-enterprise-patterns/fflib-apex-mocks
- fflib-apex-common-samplecode: https://github.com/apex-enterprise-patterns/fflib-apex-common-samplecode
- Community docs: https://fflib.dev
- Trailhead, Apex Enterprise Patterns - Service Layer: https://trailhead.salesforce.com/en/content/learn/modules/apex_patterns_sl
- Trailhead, Domain and Selector Layer: https://trailhead.salesforce.com/en/content/learn/modules/apex_patterns_dsl
- Apex sharing keywords: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_keywords_sharing.htm
- PMD Apex security rules: https://docs.pmd-code.org/latest/pmd_rules_apex_security.html
