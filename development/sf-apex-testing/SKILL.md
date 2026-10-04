---
name: sf-apex-testing
description: Writes and repairs Salesforce Apex unit tests — @IsTest classes and methods, @TestSetup, Test.startTest/Test.stopTest limit contexts, System.runAs for user-context and FLS/CRUD negative tests, the modern Assert class (Assert.areEqual, isTrue, isNull, isInstanceOfType, fail) versus legacy System.assertEquals, test data factory and builder patterns, Test.loadData with static resources, HttpCalloutMock, StaticResourceCalloutMock, MultiStaticResourceCalloutMock, WebServiceMock, Test.setMock, the Stub API (System.StubProvider and Test.createStub), asynchronous testing of Queueable, Batch, future and Schedulable jobs, Test.getEventBus().deliver() for platform events, Test.enqueueBatchJobs, 200-record bulk trigger tests, code coverage rules and the 75% deployment requirement, sf apex run test flag selection, test suites, flaky-test diagnosis, and how vf-check apex gates apexOrgCoverageMin and apexClassCoverageMin. Use this skill when creating or fixing a *Test.cls, when coverage or a deployment test level blocks a release, when a test is flaky or org-data dependent, or before running vf-check apex or sf apex run test.
---

# Apex Testing

Coverage and test-level rules below are platform requirements; the numeric gates are `vibe-force`
policy from `.vibeforce/config.json`.

| Rule | Value | Source |
| --- | --- | --- |
| Platform minimum coverage to deploy or package Apex | 75% of Apex code, all tests passing | Apex Developer Guide |
| Platform per-class minimum under `RunSpecifiedTests` | 75% **per class and per trigger**, computed individually | Salesforce CLI reference |
| Every trigger must have some coverage | non-negotiable | Apex Developer Guide |
| `vibe-force` org coverage gate | `gates.apexOrgCoverageMin` = 85 | `config/vibe-force.defaults.json` |
| `vibe-force` per-class coverage gate | `gates.apexClassCoverageMin` = 75 | `config/vibe-force.defaults.json` |
| New Apex class requires a test class | `gates.requireTestForApexClass` = true | `config/vibe-force.defaults.json` |

Not counted as covered: `System.debug` calls, test methods, and test classes. Conditional and
ternary operators count as executed only when **both** branches run.

## When to use

- Creating or repairing any `*Test.cls`, or a deployment fails its test level.
- Coverage is below a gate, or differs between sandbox and production.
- A test is flaky, order-dependent, or reads org data.
- Asynchronous work (Queueable, Batch, future, Schedulable, platform events) needs deterministic
  assertions.
- A callout, an external service, or a collaborator class must be mocked.

Adjacent skills: `sf-apex-development` (code under test), `sf-async-apex-patterns` (job design),
`sf-governor-limits` (`Limits` assertions), `sf-security-model` (permission sets for negative
tests), `sf-lwc-jest-testing` (client tests), `sf-deployment-strategies` (test levels per
environment), `sf-debugging-logs` (diagnosing a failing test).

## Decision table

| Situation | Do this |
| --- | --- |
| Shared records for every method in the class | `@TestSetup static void setup()` — rolled back after each test method |
| Records must exist before the code under test runs | create them **before** `Test.startTest()` |
| Need a clean governor-limit budget for the assertion window | wrap the exercise in `Test.startTest()` / `Test.stopTest()` |
| Async job must complete before assertions | enqueue inside the `startTest`/`stopTest` block; assert **after** `stopTest()` |
| Platform event must be delivered | `Test.getEventBus().deliver();` after `Test.stopTest()` |
| Callout in the code path | `Test.setMock(HttpCalloutMock.class, new XMock());` |
| Collaborator class must return canned data | Stub API: `Test.createStub(IFoo.class, provider)` |
| Collaborator is static, private, inner, a trigger, or `Batchable` | Stub API cannot mock it — inject an interface instead |
| SOSL must return known rows | `Test.setFixedSearchResults(ids)` — SOSL otherwise returns empty in tests |
| Verify behaviour for a restricted user | `System.runAs(u) { ... }` with a permission-set-assigned user |
| Mixed DML (setup object plus normal object) | wrap in `System.runAs(thisUser) { ... }` |
| Field is not writable from Apex (e.g. `CreatedDate`) | `Test.setCreatedDate(recordId, dt)` |
| Must read existing org data | avoid; if truly unavoidable `@IsTest(SeeAllData=true)` and document why |
| Bulk behaviour | 200 records — the documented Apex trigger batch size |

## Core patterns

### 1. Test class anatomy

```apex
@IsTest
private class CaseEscalationServiceTest {
    @TestSetup
    static void makeData() {
        // Runs once per test method, before it; changes roll back afterwards.
        insert new List<Account>{
            new Account(Name = 'Platinum Co', Tier__c = 'Platinum'),
            new Account(Name = 'Standard Co', Tier__c = 'Standard')
        };
    }

    @IsTest
    static void escalatesPlatinumCaseToHigh() {
        Account platinum = [SELECT Id, OwnerId FROM Account WHERE Tier__c = 'Platinum' LIMIT 1];
        Case c = new Case(Subject = 'Outage', Priority = 'Low', AccountId = platinum.Id);
        insert c;

        Test.startTest();
        CaseEscalationService.escalate(new List<Case>{ c });
        Test.stopTest();

        Case after = [SELECT Priority, OwnerId FROM Case WHERE Id = :c.Id];
        Assert.areEqual('High', after.Priority, 'Platinum tier must escalate to High');
        Assert.areEqual(platinum.OwnerId, after.OwnerId, 'Case should transfer to the account owner');
    }
}
```

`@IsTest` classes must be top-level, cannot be interfaces or enums, and their access modifiers are
irrelevant — the framework finds the methods regardless. `@IsTest` code is excluded from the 6 MB
org code limit and from coverage arithmetic. Static member values changed in a `@TestSetup` or test
method are **not** preserved for other methods in the class. `@TestSetup` is unsupported in a class
annotated `@IsTest(SeeAllData=true)`.

### 2. `Test.startTest` / `Test.stopTest` semantics

Both may be called at most once per test method.

| Behaviour | Detail |
| --- | --- |
| Limit context | code between the two calls receives a **new** set of governor limits; `startTest` *adds* a context rather than refreshing it, so limits consumed before it are restored after `stopTest` |
| Asynchronous flush | all async calls made after `startTest` are collected and run **synchronously** at `stopTest` |
| Exception during flush | halts the synchronous processing — for example an unhandled exception in a batch `execute` prevents `finish` from running |
| Savepoints | from API 60.0, all savepoints are released when `startTest` and `stopTest` are called; a `SAVEPOINT_RESET` event is logged |

Arrange before `startTest`, act between, assert after `stopTest`.

### 3. Assertions

Use the `Assert` class. `System.assert*` still compiles but carries no message discipline and is
legacy.

| Legacy | Modern |
| --- | --- |
| `System.assertEquals(a, b)` | `Assert.areEqual(a, b, 'why')` |
| `System.assertNotEquals(a, b)` | `Assert.areNotEqual(a, b, 'why')` |
| `System.assert(cond)` | `Assert.isTrue(cond, 'why')` |
| `System.assert(!cond)` | `Assert.isFalse(cond, 'why')` |
| `System.assert(x == null)` | `Assert.isNull(x, 'why')` |
| `System.assert(x != null)` | `Assert.isNotNull(x, 'why')` |
| `System.assert(false, 'unreachable')` | `Assert.fail('DmlException expected')` |
| no equivalent | `Assert.isInstanceOfType(o, Account.class)` / `Assert.isNotInstanceOfType(...)` |

Argument order is `(expected, actual, message)`. Negative tests assert the failure, not merely that
something threw:

```apex
@IsTest
static void rejectsNegativeAmount() {
    Opportunity o = new Opportunity(
        Name = 'Bad', StageName = 'Prospecting', CloseDate = Date.today(), Amount = -1
    );
    try {
        insert o;
        Assert.fail('Expected a DmlException for a negative Amount');
    } catch (DmlException e) {
        Assert.areEqual(1, e.getNumDml(), 'Exactly one record should fail');
        Assert.isTrue(
            e.getDmlMessage(0).contains('Amount'),
            'Error must name the offending field, got: ' + e.getDmlMessage(0)
        );
    }
}
```

Full `Assert` API table in [references/assertions-and-mocks.md](references/assertions-and-mocks.md).

### 4. Test data factory

Public `@IsTest` utility classes are excluded from the org code limit and callable only from test
context. Build records; never read org data.

```apex
@IsTest
public class TestDataFactory {
    public static List<Account> accounts(Integer count, String tier) {
        List<Account> out = new List<Account>();
        for (Integer i = 0; i < count; i++) {
            out.add(new Account(Name = 'Acct ' + i, Tier__c = tier));
        }
        insert out;
        return out;
    }

    public static List<Case> cases(Integer perAccount, List<Account> accounts) {
        List<Case> out = new List<Case>();
        for (Account a : accounts) {
            for (Integer i = 0; i < perAccount; i++) {
                out.add(new Case(Subject = 'C' + i, Priority = 'Low', AccountId = a.Id));
            }
        }
        insert out;
        return out;
    }
}
```

Tests are isolated from org data by default — `@IsTest(SeeAllData=false)` is the implicit behaviour
for API 24.0 and later. `SeeAllData=true` at class level cannot be overridden by a method-level
`false`, and it is incompatible with `IsParallel=true`. Builders, `Test.loadData` with static
resources, and `Test.setCreatedDate` recipes are in
[references/test-patterns.md](references/test-patterns.md).

### 5. Mocking callouts and collaborators

Tests do not support HTTP callouts; without a mock the test fails.

```apex
@IsTest
private class PaymentsClientTest {
    private class Mock implements HttpCalloutMock {
        public HttpResponse respond(HttpRequest req) {
            Assert.areEqual('callout:Payments/charge', req.getEndpoint());
            Assert.areEqual('POST', req.getMethod());
            HttpResponse res = new HttpResponse();
            res.setStatusCode(201);
            res.setHeader('Content-Type', 'application/json');
            res.setBody('{"id":"ch_1","status":"succeeded"}');
            return res;
        }
    }

    @IsTest
    static void chargeReturnsProviderId() {
        Test.setMock(HttpCalloutMock.class, new Mock());

        Test.startTest();
        String chargeId = PaymentsClient.charge(1000, 'USD');
        Test.stopTest();

        Assert.areEqual('ch_1', chargeId, 'Client must surface the provider charge id');
    }
}
```

Mock selection:

| Need | Mock |
| --- | --- |
| One endpoint, logic in Apex | `HttpCalloutMock` implementation |
| Response body held as a static resource | `StaticResourceCalloutMock` |
| Several endpoints, each with its own static resource | `MultiStaticResourceCalloutMock` |
| SOAP callout from a WSDL2Apex stub | `WebServiceMock` |
| Collaborator Apex class | Stub API — `System.StubProvider` plus `Test.createStub` |

Stub API limitations shape design: it cannot mock static methods (including future methods),
private methods, properties, triggers, inner classes, system types, classes implementing
`Batchable`, or classes with only private constructors; iterators cannot be return or parameter
types; and the mocked object must live in the same namespace as the `Test.createStub()` call.
A multi-endpoint router and a full `StubProvider` are in
[references/assertions-and-mocks.md](references/assertions-and-mocks.md).

### 6. Asynchronous tests

```apex
@IsTest
private class InvoiceSyncQueueableTest {
    @IsTest
    static void queueableMarksInvoicesSynced() {
        List<Invoice__c> invoices = TestDataFactory.invoices(5);
        Test.setMock(HttpCalloutMock.class, new InvoiceSyncMock());

        Test.startTest();
        System.enqueueJob(new InvoiceSyncQueueable(new Map<Id, Invoice__c>(invoices).keySet()));
        Test.stopTest();   // job runs synchronously here

        Assert.areEqual(
            5,
            [SELECT COUNT() FROM Invoice__c WHERE Sync_Status__c = 'Synced'],
            'Every queued invoice should be marked synced'
        );
    }
}
```

| Async feature | Test technique | Constraint |
| --- | --- | --- |
| Queueable | `System.enqueueJob` inside `startTest`/`stopTest` | chaining is not executed in tests beyond the first job |
| Batch Apex | `Database.executeBatch` inside the block | max 5 batch jobs submitted per running test; only one `execute` chunk runs |
| Future method | call the method inside the block | `@Future` cannot be invoked from another `@Future` |
| Schedulable | `System.schedule` inside the block; job runs at `stopTest` | cron string still required |
| Flex queue ordering | `Test.enqueueBatchJobs(n)` plus `Test.getFlexQueueOrder()` | enqueues no-operation jobs for ordering assertions |
| Platform events | `Test.getEventBus().deliver();` after `Test.stopTest()` | one `deliver()` per downstream publishing hop |
| `BatchApexErrorEvent` | `Database.RaisesPlatformEvents` on the batch class, then `deliver()` | wrap the block in try/catch to swallow the job's exception |

### 7. Negative CRUD/FLS tests with `System.runAs`

Inside a `runAs` block the user's sharing rules and object- and field-level permissions are
enforced **regardless** of the test class's sharing mode. If a method defined elsewhere is called
inside the block, the sharing mode of *that* class applies.

```apex
@IsTest
private class CaseEscalationServiceSecurityTest {
    @IsTest
    static void minimumAccessUserCannotEscalate() {
        User restricted = TestDataFactory.minimumAccessUser();   // no permission set assigned
        Account a = TestDataFactory.accounts(1, 'Platinum')[0];
        Case c = new Case(Subject = 'Outage', Priority = 'Low', AccountId = a.Id);
        insert c;

        System.runAs(restricted) {
            Test.startTest();
            try {
                CaseEscalationService.escalate(new List<Case>{ c });
                Assert.fail('A user without Case edit must not be able to escalate');
            } catch (Exception e) {
                Assert.isTrue(
                    e.getMessage().containsIgnoreCase('insufficient access')
                        || e.getTypeName() == 'System.DmlException',
                    'Expected an access failure, got ' + e.getTypeName() + ': ' + e.getMessage()
                );
            }
            Test.stopTest();
        }
    }
}
```

`runAs` is test-only, ignores user-license limits, may be nested, and **every call counts against
the DML statement limit**. The positive counterpart assigns a permission set to the same user and
asserts the operation succeeds — that pair is what proves a `WITH USER_MODE` query is correct.

### 8. Bulk and trigger tests

Use 200 records: the documented Apex trigger batch size, and the point where a non-bulkified
implementation breaks. Testing best practices call for at least 20; 200 matches the platform batch.

```apex
@IsTest
static void bulkUpdateStaysWithinLimits() {
    List<Case> cases = TestDataFactory.cases(100, TestDataFactory.accounts(2, 'Platinum'));

    Test.startTest();
    for (Case c : cases) {
        c.Priority = 'Medium';
    }
    update cases;
    Integer queries = Limits.getQueries();
    Integer statements = Limits.getDmlStatements();
    Test.stopTest();

    Assert.isTrue(queries <= 5, 'Handler issued ' + queries + ' SOQL queries for one bulk update');
    Assert.isTrue(statements <= 3, 'Handler issued ' + statements + ' DML statements');
}
```

Assert an upper bound on `Limits.getQueries()` and `Limits.getDmlStatements()` rather than an exact
count — exact counts make the test brittle when an unrelated handler is added. See
`sf-governor-limits`.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
| --- | --- | --- |
| `@IsTest(SeeAllData=true)` to make a test pass | coverage and results diverge between sandbox and production when org data changes | create the data in the test |
| No assertions, only execution | coverage rises, defects ship | assert observable outcomes with messages |
| `Assert.isTrue(true)` or bare "did not throw" | tautology | assert the value, the field, or the error text |
| Hard-coded record Ids or profile Ids | fails in every other org | query by name, or use `TestIds` to fabricate synthetic Ids |
| `Test.startTest()` after the exercise | limits and async flush apply to the wrong window | arrange, `startTest`, act, `stopTest`, assert |
| Assertions before `Test.stopTest()` for async work | job has not run | assert after `stopTest()` |
| Callout with no `Test.setMock` | tests do not support callouts; the method fails | install the appropriate mock |
| One test method covering ten branches | a failure localises nothing | one behaviour per method, named after the behaviour |
| `System.assertEquals(1, results.size())` with no message | failure output says nothing | always pass the third message argument |
| Relying on record Id ordering | Ids are not created in ascending order across separate requests | add `ORDER BY` |
| Sharing a mutable `static` between test methods | statics are not preserved across methods | build state inside each method or in `@TestSetup` |
| `Test.isRunningTest()` branch in production code | untested production path, hides defects | inject a collaborator or use the Stub API |
| 1-record test for trigger logic | non-bulkified code passes | 200-record test |

## Verification

```bash
# Local gate first (no org): format, lint, analyzer, LWC Jest
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# Apex tests plus coverage gates; writes .vibeforce/reports/apex-<ISO>.json
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-dev

# Narrow, fast loop on one class, synchronously, with per-test coverage detail
sf apex run test --tests CaseEscalationServiceTest --synchronous \
  --code-coverage --detailed-coverage --result-format human --target-org vf-dev

# Suite run with machine-readable output for CI
sf apex run test --suite-names CoreRegression --code-coverage \
  --result-format json --output-dir /tmp/apex-results --wait 30 --target-org vf-dev

# Retrieve results for an async run that outlived --wait
sf apex get test --test-run-id 707xx0000000001 --code-coverage --json --target-org vf-dev
```

`--synchronous` runs the methods of a **single** Apex class; anything broader runs asynchronously
and returns a test run id. `--concise` shows only failures and works with human output only.
`testRunCoverage` in JSON and JUnit output is the percentage of covered lines across all classes
evaluated by that run — it is not the org coverage figure the gate uses.

## References

| Reference file | Contents |
| --- | --- |
| [references/test-patterns.md](references/test-patterns.md) | TestDataFactory and builders, `Test.loadData`, `setCreatedDate`, async recipes for Queueable/Batch/future/Schedulable, platform-event tests, `runAs` with permission sets |
| [references/coverage-and-gates.md](references/coverage-and-gates.md) | coverage semantics, sandbox versus production divergence, full `sf apex run test` and `sf apex get test` flag tables, report JSON shape, gate tuning |
| [references/assertions-and-mocks.md](references/assertions-and-mocks.md) | complete `Assert` API, Stub API walkthrough and limits, all four callout-mock variants, multi-endpoint router, `WebServiceMock` |

| Official source | URL |
| --- | --- |
| Testing Apex | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing.htm |
| Understanding testing in Apex | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_intro.htm |
| Testing best practices | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_best_practices.htm |
| `Test.startTest` / `Test.stopTest` | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_tools_start_stop_test.htm |
| `System.runAs` | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_tools_runas.htm |
| `@TestSetup` | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_testsetup_using.htm |
| `SeeAllData` | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_seealldata_using.htm |
| `Test.loadData` | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_load_data.htm |
| Common test utility classes | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_utility_classes.htm |
| Stub API | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing_stub_api.htm |
| Testing HTTP callouts | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_restful_http_testing.htm |
| Code coverage best practices | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_code_coverage_best_pract.htm |
| `Assert` class | https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_class_System_Assert.htm |
| Salesforce CLI `apex` commands | https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_apex_commands_unified.htm |
