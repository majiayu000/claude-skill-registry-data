---
name: sf-fflib-testing
description: Covers every testing variant available in an Apex Enterprise Patterns (fflib) codebase - ApexMocks stub lifecycle (fflib_ApexMocks, startStubbing/when/thenReturn/stopStubbing, verify and verification modes), argument matchers and fflib_ArgumentCaptor, mock injection through Application.UnitOfWork/Service/Selector/Domain setMock, fake SObject graphs with fflib_ApexMocksUtils and fflib_IDGenerator, DML-free domain trigger tests via fflib_SObjectDomain.Test.Database, real-DML selector and integration tests, async/Queueable/Batch/Schedulable tests, platform-event delivery with Test.getEventBus().deliver(), callout mocks, and FLS/CRUD negative tests. Use when writing or reviewing any Apex test in a repo containing fflib_ApexMocks, fflib_SObjectSelector, fflib_SObjectDomain, fflib_SObjectUnitOfWork or an Application class, when a mock verification fails, when choosing between a mocked unit test and a real-DML integration test, or when Apex coverage gates (apexOrgCoverageMin 85 / apexClassCoverageMin 75) must be met without writing coverage-padding tests.
---

# fflib Testing

Testing an fflib codebase means choosing, per class under test, between a **mocked unit test**
(fast, proves collaboration, proves nothing about the org) and a **real-DML test** (slow, proves
the platform actually behaves). Getting that choice wrong is the single largest source of
worthless Apex test suites: 90% coverage where every selector's SOQL is unproven.

Framework grounding: `fflib-apex-mocks` @ `master` commit `d81e9e1` and `fflib-apex-common` @
`master` commit `dab5977` (both `apex-enterprise-patterns`). Platform grounding: Apex Developer
Guide, Summer '26 / API version `67.0` (doc version 262.0) - the `apiVersion` in
`config/vibe-force.defaults.json`.

Read `sf-fflib-foundations` for the Application/factory wiring these tests inject into,
`sf-fflib-selector-layer` for selector construction, `sf-fflib-domain-service-uow` for the layers
under test, and `sf-fflib-operations` for CI/packaging of the framework itself.

## When to use

Use this skill when a repo contains `fflib_ApexMocks`, `fflib_SObjectDomain`,
`fflib_SObjectSelector`, `fflib_SObjectUnitOfWork`, or an `Application` class, and you are:

- writing a new test for a service, domain, selector, controller, trigger, or async job;
- diagnosing an `fflib_ApexMocks.ApexMocksException` from `verify(...)` or `when(...)`;
- deciding whether a behaviour needs a mock or real DML;
- raising coverage to clear the `apex` gate without adding tests that assert nothing.

For non-fflib Apex testing fundamentals (`@IsTest`, `@TestSetup`, `System.runAs`, `Assert`) see
`sf-apex-testing`. For LWC component tests see `sf-lwc-jest-testing`. For limit budgets consumed
by real-DML tests see `sf-governor-limits`.

## Test-variant decision table

| # | Variant | What it proves | What it cannot prove | Speed | Org data | fflib machinery | Coverage contribution | Typical failure mode |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Service unit test with mocks | Service orchestration: which selector/domain/UoW calls happen, in what shape | SOQL validity, triggers, FLS, validation rules | ~10-40 ms | none | `fflib_ApexMocks`, `Application.*.setMock`, `fflib_Match` | Service impl class only | Over-specified `verify` breaks on harmless refactor |
| 2 | Domain unit test, no DML, direct construction | Pure field logic on in-memory records | Trigger routing, save order | ~5-20 ms | none | `fflib_IDGenerator` for ids; no mocks needed | Domain class | Asserting through the UoW mock instead of the record |
| 3 | Domain trigger test via `fflib_SObjectDomain.Test.Database` | `onApplyDefaults`/`onValidate`/`onBefore*`/`onAfter*` routing and error registration | Real DML errors, validation rules, roll-ups, chained triggers | ~10-30 ms | none | `fflib_SObjectDomain.Test.Database.onInsert/onUpdate/onDelete/onUndelete` + `fflib_SObjectDomain.triggerHandler(Type)`, `fflib_SObjectDomain.Errors` | Domain + trigger handler | Forgetting `Errors.clearAll()` between assertions in one method |
| 4 | Selector test against real data | The SOQL compiles, field list is right, filters and ordering work | Behaviour of callers | 200 ms - 2 s | inserted records | Real selector, no mocks, `fflib_QueryFactory` output | Selector class | Mocking the selector - proves nothing |
| 5 | Service integration test with real DML | End-to-end: service + domain + selector + UoW + triggers + validation | Isolation of a single failure cause | 0.5-5 s | inserted records | `Application.UnitOfWork.newInstance()`, no `setMock` | Every layer it crosses | Slow suite; used as the only test style |
| 6 | Trigger test with real DML | Save order, recursion, cross-object roll-ups, validation rules | Nothing about isolated units | 0.5-3 s | inserted records | Real trigger + `fflib_SObjectDomain.triggerHandler` | Trigger + domain | Assumes `@TestSetup` data survives `Test.startTest()` limits reset |
| 7 | Controller / `@AuraEnabled` test | Wire adapter contract: return shape, `AuraHandledException` messages | Client rendering | ~20-80 ms mocked | none if service mocked | `Application.Service.setMock(IFooService.class, mock)` | Controller class | Testing the service again through the controller |
| 8 | Flow-invocable test (`@InvocableMethod`) | Bulk request/response contract and per-row mapping | Flow itself | ~20-80 ms | none if service mocked | `Application.Service.setMock` | Invocable class | Single-row-only test on a bulk API |
| 9 | Async test: Queueable / Schedulable | The job enqueues, runs, and commits inside `Test.startTest()/stopTest()` | Behaviour under real 2-minute chaining/limits | 0.5-3 s | usually yes | Real UoW; mock the service the job calls where possible | Job class | Asserting before `Test.stopTest()` |
| 10 | Async test: Batchable | `start`/`execute`/`finish` wiring, one chunk | Multi-chunk state, real scope sizes | 1-5 s | yes | **Batchable classes cannot be stubbed** (Stub API limit) - mock its collaborators instead | Batch class | Expecting `finish` after an unhandled `execute` exception in test context |
| 11 | Platform-event test | Event publication and the subscriber trigger | Real bus latency/replay | 0.3-2 s | sometimes | `uow.registerPublishAfterSuccessTransaction`, then `Test.getEventBus().deliver()` | Publisher + subscriber | Missing `deliver()`, so the subscriber never runs |
| 12 | Callout test | Request shape and response handling | The remote system | ~30-200 ms | none | `Test.setMock(HttpCalloutMock.class, ...)` inside the mocked service boundary | Callout class | Callout mock set after the callout is triggered |
| 13 | FLS / CRUD negative test | `USER_MODE` DML and selector security actually reject | Anything under system mode | 0.5-3 s | user + perm set | `fflib_SObjectUnitOfWork.UserModeDML`, `System.runAs`, `Assert.fail()` + `catch (SecurityException)` | Security paths | Running as a System Administrator, so nothing is denied |
| 14 | LWC Jest test | Client behaviour, wire handling, DOM | Any Apex | ~50-300 ms | none | none (see `sf-lwc-jest-testing`) | JS coverage (`jestCoverageMin`) | Duplicating Apex assertions in JS |

Rows 1-3, 7, 8 are the fast tier; rows 4-6, 9-13 are the slow tier. A healthy fflib org is roughly
**70% fast tier / 25% slow tier / 5% end-to-end**, described under "Test pyramid" below.

## Core patterns

### 1. The ApexMocks lifecycle

`fflib_ApexMocks implements System.StubProvider`; `mocks.mock(Type)` returns
`Test.createStub(classToMock, this)`. The stub is named `<Type>__sfdc_ApexStub`, which is what you
see in failure messages.

```apex
@IsTest
private class OpportunitiesServiceTest {
    @IsTest
    static void applyDiscountRegistersDirtyOpportunities() {
        // 1. Arrange the mock control object and the stubs
        fflib_ApexMocks mocks = new fflib_ApexMocks();
        IOpportunitiesSelector selectorMock = (IOpportunitiesSelector) mocks.mock(IOpportunitiesSelector.class);
        fflib_ISObjectUnitOfWork uowMock = (fflib_ISObjectUnitOfWork) mocks.mock(fflib_ISObjectUnitOfWork.class);

        Opportunity opp = new Opportunity(
            Id = fflib_IDGenerator.generate(Opportunity.SObjectType),
            Name = 'Test',
            StageName = 'Open',
            CloseDate = System.today(),
            Amount = 1000);
        Set<Id> oppIds = new Set<Id>{ opp.Id };

        // 2. Stub: everything between startStubbing/stopStubbing records, it does not execute
        mocks.startStubbing();
        mocks.when(selectorMock.sObjectType()).thenReturn(Opportunity.SObjectType);
        mocks.when(selectorMock.selectByIdWithProducts(oppIds)).thenReturn(new List<Opportunity>{ opp });
        mocks.stopStubbing();

        // 3. Inject
        Application.Selector.setMock(selectorMock);
        Application.UnitOfWork.setMock(uowMock);

        // 4. Exercise the real implementation class, not the static facade
        System.Test.startTest();
        new OpportunitiesServiceImpl().applyDiscounts(new Map<Id, Decimal>{ opp.Id => 10 });
        System.Test.stopTest();

        // 5. Verify collaboration
        ((IOpportunitiesSelector) mocks.verify(selectorMock, 1)).selectByIdWithProducts(oppIds);
        ((fflib_ISObjectUnitOfWork) mocks.verify(uowMock, 1)).registerDirty(
            fflib_Match.sObjectWith(new Map<SObjectField, Object>{
                Opportunity.Id => opp.Id,
                Opportunity.Amount => 900 }));
        ((fflib_ISObjectUnitOfWork) mocks.verify(uowMock, 1)).commitWork();
    }
}
```

Rules that follow from the source:

- **Every `when(...)` must be inside `startStubbing()`/`stopStubbing()`.** Outside it, the call is
  *recorded as a real invocation* and then verified against later, corrupting counts.
- **`when(...)` must be followed by `thenReturn`/`thenThrow`/`thenAnswer`/`thenReturnMulti`/
  `thenThrowMulti`.** A bare `when(...)` yields
  `ApexMocksException: The stubbing is not correct, no return values have been set.` at *call* time.
- **Unstubbed methods return `null`**, they do not throw. A `NullPointerException` deep inside the
  class under test almost always means "you forgot to stub something".
- **`mocks.mock()` uses the Stub API**, so the platform's stub limitations apply: no static or
  private methods, no properties, no triggers, no inner classes, no system types, no `Batchable`
  implementers, no classes with only private constructors, and iterators cannot be a parameter or
  return type. The mocked type must be in the same namespace as the `Test.createStub()` call.
  ([Apex Developer Guide, Build a Mocking Framework with the Stub API](https://developer.salesforce.com/docs/atlas.en-us.262.0.apexcode.meta/apexcode/apex_testing_stub_api.htm))

### 2. Generated mocks vs Stub API mocks

Two modes exist. Only the first is current.

| Mode | How a mock is made | Needs regeneration on interface change | Use |
| --- | --- | --- | --- |
| Stub API (current) | `(IFoo) mocks.mock(IFoo.class)` -> `Test.createStub` | No | Default for everything |
| ApexMocks Generator (legacy) | Pre-generated `FooMocks.Foo` class implementing the interface and delegating to `mocks.mockNonVoidMethod(...)` / `mocks.mockVoidMethod(...)` | Yes - stale generated mocks silently drift | Only for types the Stub API refuses to stub |

`mockVoidMethod(Object, String, List<Type>, List<Object>)` and
`mockNonVoidMethod(...)` remain `public` on `fflib_ApexMocks` for generated classes. The generator
itself is an external tool, not part of the `fflib-apex-mocks` repo.

`fflib_ApexMocksConfig.HasIndependentMocks` (default `false`) controls whether two mock instances
of the same type share stubbing and counts. `fflib_QualifiedMethod.equals`/`hashCode` include the
mock instance only when it is `true`. Set it to `true` in `@IsTest` setup when a single test holds
two mocks of one interface and must distinguish them:

```apex
fflib_ApexMocksConfig.HasIndependentMocks = true;
```

### 3. Verification API

```apex
((IFoo) mocks.verify(fooMock)).bar();                                   // exactly 1
((IFoo) mocks.verify(fooMock, 3)).bar();                                // exactly 3
((IFoo) mocks.verify(fooMock, fflib_ApexMocks.NEVER)).bar();            // NEVER == 0
((IFoo) mocks.verify(fooMock, mocks.atLeastOnce())).bar();
((IFoo) mocks.verify(fooMock, mocks.atLeast(2))).bar();
((IFoo) mocks.verify(fooMock, mocks.atMost(5))).bar();
((IFoo) mocks.verify(fooMock, mocks.between(1, 3))).bar();
((IFoo) mocks.verify(fooMock, mocks.times(2).description('two writes expected'))).bar();

fflib_InOrder inOrder = mocks.inOrder(new List<Object>{ fooMock, uowMock });
((IFoo) inOrder.verify(fooMock)).bar();
((fflib_ISObjectUnitOfWork) inOrder.verify(uowMock)).commitWork();
inOrder.verifyNoMoreInteractions();
```

Verified against source: modes are `times`, `calls`, `atLeast`, `atMost`, `atLeastOnce`,
`between`, `never`, plus `description(String)` for a custom assert message.
`calls(n)` is **InOrder-only** (`fflib_AnyOrder` throws
`The calls() method is available only in the InOrder Verification.`); `atMost` and `between` are
**not** available in InOrder (`The <mode> method is not implemented for the fflib_InOrder class`).
`verifyNoMoreInteractions()` and `verifyNoInteractions()` exist **only on `fflib_InOrder`**, not on
`fflib_ApexMocks`; there is no `verifyZeroInteractions`. Use
`mocks.verify(mock, fflib_ApexMocks.NEVER)` per method for the non-ordered equivalent.

Full API table: `references/apexmocks-api.md`.

### 4. Matchers, captors, answers

All-or-nothing rule: if one argument uses a matcher, **every** argument must. Mixing raw values
with matchers throws `The number of matchers defined (n). does not match the number expected (m)`.

```apex
((IFoo) mocks.verify(fooMock)).save(fflib_Match.anyId(), fflib_Match.eqString('OPEN'));

fflib_ArgumentCaptor captor = fflib_ArgumentCaptor.forClass(List<Account>.class);
((fflib_ISObjectUnitOfWork) mocks.verify(uowMock)).registerDirty((List<SObject>) captor.capture());
List<Account> registered = (List<Account>) captor.getValue();
Assert.areEqual(2, registered.size(), 'Both accounts should be registered dirty');
```

Dynamic returns and side effects use `fflib_Answer`; void-method throwing uses
`mocks.doThrowWhen(e, mock)` inside stubbing. See `references/matchers-and-captors.md` for the
complete matcher catalogue, each matcher's `toString()` (which is what the failure message prints)
and custom `fflib_IMatcher` implementations.

### 5. Fake SObjects: ids, relationships, read-only fields

```apex
Account acct = new Account(Id = fflib_IDGenerator.generate(Account.SObjectType), Name = 'A');

// Parent with children, as if returned by a subquery
List<Account> withContacts = (List<Account>) fflib_ApexMocksUtils.makeRelationship(
    List<Account>.class,
    new List<Account>{ acct },
    Contact.AccountId,
    new List<List<Contact>>{ new List<Contact>{ new Contact(LastName = 'X') } });

// Formula / rollup / system audit fields
acct = (Account) fflib_ApexMocksUtils.setReadOnlyFields(
    acct, Account.class, new Map<SObjectField, Object>{ Account.LastActivityDate => Date.today() });
```

`makeRelationship` and `setReadOnlyFields` both work by serialising to JSON, injecting tokens, and
deserialising - which is exactly why they can set fields `SObject.put()` rejects. Details and the
raw `JSON.deserialize` fallback: `references/fake-data-and-ids.md`.

### 6. Mocking the Unit of Work

Mocking `fflib_ISObjectUnitOfWork` replaces "query the database and assert" with "assert the DML
intent". It is fast and precise, and it is blind to:

- triggers that would have fired on `commitWork()`;
- validation rules, required fields, and duplicate rules;
- FLS/CRUD, because `SimpleDML` runs `AccessLevel.SYSTEM_MODE` and `UserModeDML` runs
  `AccessLevel.USER_MODE` - a mock runs neither;
- the real commit order (`publishBefore` events -> insert -> upsert -> update -> delete ->
  emptyRecycleBin -> email -> `doWork` -> `publishAfterSuccess` events);
- `Database.SaveResult`, which a mocked UoW never produces.

Version boundary that matters here: in **API version 67.0 and later** Apex runs in user context by
default, so object permissions and FLS are enforced unless an operation explicitly opts into system
mode; `WITH SECURITY_ENFORCED` is no longer allowed in Apex SOQL (use `WITH USER_MODE`), and a
class without an explicit sharing declaration behaves as `with sharing`. `fflib_SObjectUnitOfWork.SimpleDML`
passes `AccessLevel.SYSTEM_MODE` explicitly, so it still bypasses CRUD/FLS; `UserModeDML` passes
`AccessLevel.USER_MODE`. Neither path executes under a mock. See `sf-security-model`.

Every assertion you would have made on saved data must be re-proved by at least one real-DML test
(rows 5, 6, 13). State that explicitly in the test's header comment.

### 7. Domain trigger tests without DML

`fflib_SObjectDomain.Test.Database` feeds the trigger handler synthetic `Trigger.new` /
`Trigger.oldMap` data. `fflib_SObjectDomain.triggerHandler(Type)` detects
`Test.isRunningTest() && Test.Database.hasRecords()` and runs the **before** phase then the
**after** phase against that data.

```apex
@IsTest
static void insertValidationFailsWithoutAccount() {
    Opportunity opp = new Opportunity(Name = 'Test', Type = 'Existing Account');
    fflib_SObjectDomain.Test.Database.onInsert(new List<Opportunity>{ opp });
    fflib_SObjectDomain.triggerHandler(OpportunitiesTriggerHandler.class);

    Assert.areEqual(1, fflib_SObjectDomain.Errors.getAll().size(), 'One validation error expected');
    Assert.areEqual(
        'You must provide an Account for existing Customers.',
        fflib_SObjectDomain.Errors.getAll()[0].message);
    Assert.areEqual(
        Opportunity.AccountId,
        ((fflib_SObjectDomain.FieldError) fflib_SObjectDomain.Errors.getAll()[0]).field);
}
```

Available: `onInsert(List<SObject>)`, `onUpdate(List<SObject>, Map<Id, SObject>)`,
`onDelete(Map<Id, SObject>)`, `onUndelete(List<SObject>)`, `hasRecords()`.
`fflib_SObjectDomain.Errors` exposes `getAll()` and `clearAll()`.

This proves **routing and error registration only**. It does not prove the error surfaces as a DML
error, that the trigger is deployed and active, or that the record was rejected. Pair it with one
real-DML trigger test per validation that matters.

### 8. Where mocks are the wrong tool

| Concern | Why a mock cannot prove it | Correct variant |
| --- | --- | --- |
| Selector SOQL | The query string is never parsed by the platform | 4 - real records, real selector |
| Validation rules / required fields | Metadata, evaluated only on real DML | 5, 6 |
| Sharing, CRUD, FLS | Enforced by `USER_MODE`/`WITH USER_MODE` at runtime | 13, under `System.runAs` |
| Save order, roll-up summaries, recursion | Platform execution order | 6 |
| Flow / record-triggered automation | Runs outside Apex | 5 or 6 |
| Platform-event subscription | Requires the event bus | 11 |

### 9. Test pyramid and coverage gates

Gates enforced by `vf-check apex`: `apexOrgCoverageMin` **85**, `apexClassCoverageMin` **75**.
Mocked unit tests cover the *class under test*, never its mocked collaborators - so a suite of only
mocked tests leaves selectors at 0%.

| Layer | Variant | Share of test methods | Covers |
| --- | --- | --- | --- |
| Domain / service logic | 1, 2, 3, 7, 8 | ~70% | Domain, service impl, controllers, invocables |
| Selectors + integration + security | 4, 5, 13 | ~25% | Selectors, triggers, UoW, security paths |
| Async, events, callouts | 9, 10, 11, 12 | ~5% | Jobs, subscribers, HTTP boundaries |

Per-class rule of thumb for the 75% class gate: every selector needs at least one real-data test,
every domain needs a no-DML test, every service impl needs a mocked test plus one integration test
across its happy path. See `sf-apex-testing` for the general coverage strategy and
`sf-code-analyzer-quality` for the static rules that flag assertion-free tests.

## Anti-patterns

| Anti-pattern | Failing shape | Fix |
| --- | --- | --- |
| Over-mocked test asserting implementation | `verify` on ten methods including private helpers exposed only for the test | Verify the boundary calls (selector in, UoW out) and assert record state |
| Mocking the class under test | `IFooService svc = (IFooService) mocks.mock(IFooService.class); svc.doIt();` then verifying `doIt` | Instantiate the real `FooServiceImpl`; mock only its collaborators |
| Missing `stopStubbing()` | Later real calls are swallowed as stubs; verify counts are 0 | Always bracket: `startStubbing()` ... `stopStubbing()` |
| Bare `when(...)` with no `thenReturn` | `ApexMocksException: The stubbing is not correct, no return values have been set.` | Add a `thenReturn`/`thenThrow`/`thenAnswer` |
| Mixing matchers and literals | `The number of matchers defined (1). does not match the number expected (2)` | Wrap every argument: `fflib_Match.eq(value)` |
| Stale generated mocks after an interface change | Generated mock compiles but silently no longer overrides the new method | Migrate to `mocks.mock(IFoo.class)` (Stub API) |
| `@IsTest(SeeAllData=true)` | Suite passes locally, fails in a fresh scratch org | Build data in the test or `@TestSetup` |
| One `@TestSetup` shared by mocked and DML tests | Mocked tests pay the DML cost and get non-deterministic ids | Split into two test classes |
| Asserting `Database.SaveResult` off a mocked UoW | A mocked UoW never executes DML, so results are `null` | Assert `registerNew`/`registerDirty` interactions, or use a real-DML test |
| Test that passes with the framework bypassed | Calls `new FooServiceImpl()` but never injects, so production `Application` wiring is unverified | Route through `Application.Service.newInstance(...)` in at least one test |
| Coverage-padding tests | `new Foo(); Assert.isNotNull(foo);` | Delete them; they defend nothing and hide the real gap |
| `System.assertEquals` in new code | Legacy assertion API without a message | Use `Assert.areEqual(expected, actual, message)` |

## Verification

```bash
# Full Apex gate: runs the org test level configured for the target and enforces coverage gates
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-dev

# Single test method while iterating
sf apex run test --target-org vf-dev \
  --tests OpportunitiesServiceTest.applyDiscountRegistersDirtyOpportunities \
  --code-coverage --result-format json --wait 30

# A whole class, synchronously (fastest feedback for mocked tests)
sf apex run test --target-org vf-dev --class-names OpportunitiesServiceTest \
  --synchronous --code-coverage --result-format human --wait 20

# A curated suite (ApexTestSuite metadata) for the fast tier
sf apex run test --target-org vf-dev --suite-names FflibUnitTests \
  --code-coverage --result-format json --wait 30

# Local gate before any org round-trip
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local
```

Reading a failed mock verification - the message is produced by
`fflib_MethodVerifier.throwException`:

```text
EXPECTED COUNT: 1
ACTUAL COUNT: 0
METHOD: OpportunitiesSelector__sfdc_ApexStub.selectByIdWithProducts(Set<Id>)
---
ACTUAL ARGS: ({"..."} )
---
EXPECTED ARGS: [[SObject with fields {"Amount":900}]]
```

`ACTUAL COUNT: 0` with a populated `ACTUAL ARGS` means the method ran with *different* arguments -
compare the two blocks. `ACTUAL ARGS: ()` means the method never ran at all: check injection
(`Application.*.setMock`) before blaming the matcher. `EXPECTED ARGS` renders each matcher's
`toString()`; raw values render as JSON.

## References

- `references/apexmocks-api.md` - every public class/method in `fflib-apex-mocks` with signature, purpose and version note.
- `references/matchers-and-captors.md` - full `fflib_Match` / `fflib_MatcherDefinitions` catalogue, rendered failure text, `fflib_ArgumentCaptor`, custom matchers.
- `references/mock-injection.md` - `Application.*.setMock` variants, mockable interface design, controller/domain/service injection, `HasIndependentMocks`.
- `references/test-variants-cookbook.md` - one complete test class per decision-table row.
- `references/fake-data-and-ids.md` - `fflib_IDGenerator`, `makeRelationship`, `setReadOnlyFields`, JSON tricks, dual-mode builders.
- `references/async-and-events-testing.md` - Queueable/Batch/Schedulable, `Test.startTest`/`stopTest` flush, `Test.getEventBus().deliver()`, finalizers, callout mocks.
- `references/troubleshooting-mocks.md` - exception text -> cause -> fix, plus a debugging procedure.
- `references/migrating-legacy-tests.md` - converting DML-heavy suites to the fflib pyramid without losing coverage; run it as a multi-wave change per `sf-workflow-orchestration`.

Official documentation:

- [Build a Mocking Framework with the Stub API](https://developer.salesforce.com/docs/atlas.en-us.262.0.apexcode.meta/apexcode/apex_testing_stub_api.htm)
- [Using Limits, startTest, and stopTest](https://developer.salesforce.com/docs/atlas.en-us.262.0.apexcode.meta/apexcode/apex_testing_tools_start_stop_test.htm)
- [Using Test Setup Methods](https://developer.salesforce.com/docs/atlas.en-us.262.0.apexcode.meta/apexcode/apex_testing_testsetup_using.htm)
- [Using the runAs Method](https://developer.salesforce.com/docs/atlas.en-us.262.0.apexcode.meta/apexcode/apex_testing_tools_runas.htm)
- [Testing HTTP Callouts by Implementing the HttpCalloutMock Interface](https://developer.salesforce.com/docs/atlas.en-us.262.0.apexcode.meta/apexcode/apex_classes_restful_http_testing_httpcalloutmock.htm)
- [Apex Security and Sharing Model - Versioned Behavior Changes](https://developer.salesforce.com/docs/atlas.en-us.262.0.apexcode.meta/apexcode/apex_security_sharing_chapter.htm)
- [fflib-apex-mocks](https://github.com/apex-enterprise-patterns/fflib-apex-mocks) | [fflib-apex-common](https://github.com/apex-enterprise-patterns/fflib-apex-common) | [fflib-apex-common-samplecode](https://github.com/apex-enterprise-patterns/fflib-apex-common-samplecode)
