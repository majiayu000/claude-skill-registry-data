---
name: sf-apex-development
description: Writes and reviews production Salesforce Apex — classes, interfaces, inheritance, sharing keywords (with/without/inherited sharing), user mode versus system mode (as user, as system, WITH USER_MODE, AccessLevel), one-trigger-per-object handler frameworks, recursion guards, bulkification, collection and map idioms, Database.insert partial success and SaveResult handling, Savepoint and rollback, custom exceptions, Database.Stateful, JSON serialisation, Schema describe caching, custom settings and custom metadata access, Apex Enterprise Patterns (Selector, Domain, Service, Unit of Work), @AuraEnabled(cacheable=true) contracts for Lightning web components, and @RestResource services. Use this skill whenever work touches force-app/**/classes/*.cls or force-app/**/triggers/*.trigger, when an Apex class or trigger must be created, refactored, bulkified or security-hardened, when a reviewer asks why a class needs an explicit sharing declaration, when Apex must be exposed to LWC or REST, or before running vf-check analyzer or vf-check apex.
---

# Apex Development

Target API version is `apiVersion` in `config/vibe-force.defaults.json` (`67.0`). API 67.0 changed
how Apex enforces security by default; every rule below assumes it.

| Behaviour | API 66.0 and earlier | API 67.0 and later |
| --- | --- | --- |
| Class with no sharing declaration | Resolved from inheritance chain / entry point; often `without sharing` | Runs `with sharing` |
| SOQL, SOSL, DML default access mode | System mode (FLS and object perms bypassed) | **User mode** (FLS and object perms enforced) |
| Trigger body database operations | System mode | User mode, which overrides the trigger's implicit `without sharing` |
| `WITH SECURITY_ENFORCED` in an Apex SOQL `SELECT` | allowed, weaker than user mode | **rejected — will not compile**; use `WITH USER_MODE` |

## When to use

- Creating or editing anything under `force-app/**/classes/` or `force-app/**/triggers/`.
- Converting ad-hoc trigger logic into a handler framework, or being asked to add a second trigger
  to an object (never do it — see pattern 3).
- Choosing between `with sharing`, `without sharing`, `inherited sharing`, and `WITH SYSTEM_MODE`.
- Exposing Apex to Lightning web components (`@AuraEnabled`) or external callers (`@RestResource`).
- Reviewing for bulkification, partial-success DML, describe-call caching, or exception design.

Adjacent skills: `sf-apex-testing` (tests, mocks, coverage), `sf-async-apex-patterns` (Queueable,
Batch, Schedulable, future, finalizers), `sf-governor-limits` (limit numbers and triage),
`sf-soql-sosl-optimization` (selectivity, indexes), `sf-security-model` (CRUD/FLS, permission sets,
`stripInaccessible`), `sf-debugging-logs` (log levels), `sf-integration-patterns` (callouts).

## Decision table

| Question | Answer | Enforced by |
| --- | --- | --- |
| Sharing declaration on a new class? | `with sharing` unless the class is a deliberate privilege elevation | `vf-check analyzer` (PMD `ApexSharingViolations`) |
| Service reused from elevated and non-elevated callers? | `inherited sharing` | review |
| Query must ignore FLS? | `WITH SYSTEM_MODE` plus a comment stating why | `vf-check analyzer` |
| DML must ignore FLS? | `insert as system` / `Database.insert(recs, AccessLevel.SYSTEM_MODE)` | review |
| Triggers per object? | Exactly one, all events in one file, zero logic inside | `vf-check analyzer` |
| Partial success acceptable? | `Database.insert(list, false)` and iterate `SaveResult` | review |
| All-or-nothing required? | `insert list;` or `Database.insert(list, true)` | review |
| Method called from LWC and read-only? | `@AuraEnabled(cacheable=true)` | `vf-check lint` (LWC side) |
| Describe call inside a loop? | Hoist into a `static final Map` | `vf-check analyzer` |
| New Apex class without a matching `*Test.cls`? | Blocked when `gates.requireTestForApexClass` is true | `vf-check apex` |

## Core patterns

### 1. Explicit sharing plus explicit access mode

The sharing keyword governs record visibility; the access mode governs object and field
permissions. They are independent — declare both.

```apex
public with sharing class OpportunityRiskService {
    // User mode is the API 67.0 default, but state it so intent survives a version bump.
    public static List<Opportunity> loadAtRisk(Set<Id> accountIds) {
        return [
            SELECT Id, Name, Amount, CloseDate, AccountId
            FROM Opportunity
            WHERE AccountId IN :accountIds
              AND StageName NOT IN ('Closed Won', 'Closed Lost')
            WITH USER_MODE
        ];
    }
}
```

Elevation is a separate, narrow class — never a `without sharing` flag on a general service:

```apex
/** Community users must read the parent account name of their own cases. Name only. */
public without sharing class AccountNameElevation {
    public static List<Account> namesFor(Set<Id> accountIds) {
        return [SELECT Id, Name FROM Account WHERE Id IN :accountIds WITH SYSTEM_MODE];
    }
}
```

`inherited sharing` resolves at run time and runs `with sharing` at every entry point (Aura
controller, `@AuraEnabled` method called from LWC, Visualforce controller, Apex REST service,
asynchronous Apex). It degrades to `without sharing` only when called from an established
`without sharing` context. Triggers cannot carry a sharing declaration — they always run
`without sharing` — so keep the trigger body empty and put logic in a declared handler class. Full
matrix in [references/apex-language-reference.md](references/apex-language-reference.md).

### 2. Bulkified, map-driven logic

One query per object, one DML per object, zero queries or DML inside loops.

```apex
public with sharing class CaseEscalationService {
    public static void escalate(List<Case> cases) {
        Set<Id> accountIds = new Set<Id>();
        for (Case c : cases) {
            if (c.AccountId != null) {
                accountIds.add(c.AccountId);
            }
        }
        if (accountIds.isEmpty()) {
            return;
        }

        Map<Id, Account> accounts = new Map<Id, Account>([
            SELECT Id, OwnerId, Tier__c FROM Account WHERE Id IN :accountIds WITH USER_MODE
        ]);

        List<Case> toUpdate = new List<Case>();
        for (Case c : cases) {
            Account a = accounts.get(c.AccountId);
            if (a != null && a.Tier__c == 'Platinum' && c.Priority != 'High') {
                toUpdate.add(new Case(Id = c.Id, Priority = 'High', OwnerId = a.OwnerId));
            }
        }
        if (!toUpdate.isEmpty()) {
            update as user toUpdate;
        }
    }
}
```

| Need | Idiom |
| --- | --- |
| Ids from a trigger collection | `Trigger.newMap.keySet()`, or bind `Trigger.new` directly in `IN :Trigger.new` (Apex converts records to Ids) |
| Group children by parent | `Map<Id, List<Child__c>>` built in one pass over one query |
| Detect a changed field | `Trigger.oldMap.get(rec.Id).Field__c != rec.Field__c` |
| Query result as a keyed map | `new Map<Id, Account>([SELECT ...])` |
| De-duplicate external keys | `Set<String>` then a single `WHERE ExternalId__c IN :keys` |
| Constant lookups | `static final Map<String, X>` initialised in a static block |

### 3. One trigger per object, logic in a handler

The order in which multiple triggers on the same object fire is **not guaranteed**, so a second
trigger on an object is a defect, not a style preference.

```apex
trigger CaseTrigger on Case (
    before insert, before update, before delete,
    after insert, after update, after delete, after undelete
) {
    new CaseTriggerHandler().run();
}
```

The runnable `TriggerHandler` base class (dispatch by `Trigger.operationType`, per-handler
recursion guard, static bypass API, max-loop-count support) and its tests are in
[references/trigger-framework.md](references/trigger-framework.md). Minimal Id-set guard for a
handler that re-enters through its own DML:

```apex
@TestVisible
private static Set<Id> processed = new Set<Id>();

List<Contact> fresh = new List<Contact>();
for (Contact c : contacts) {
    if (processed.add(c.Id)) {   // Set.add returns false when already present
        fresh.add(c);
    }
}
```

Static state is **not** reset between the retry attempts of a partial-success bulk DML call, and is
**not** reverted by `Database.rollback`. Design guards to tolerate re-entry, and prefer an
`operationType`-keyed guard over a global boolean.

### 4. DML options, partial success, and rollback

```apex
Database.SaveResult[] results = Database.insert(leads, false, AccessLevel.USER_MODE);
for (Integer i = 0; i < results.size(); i++) {
    if (results[i].isSuccess()) { continue; }
    for (Database.Error err : results[i].getErrors()) {
        // getFields() is populated for FLS failures when running in user mode
        errorsByRow.put(i, err.getStatusCode() + ': ' + err.getMessage()
            + ' fields=' + String.join(err.getFields(), ','));
    }
}
```

| Operation | Result class |
| --- | --- |
| `insert`, `update` | `Database.SaveResult` |
| `upsert` | `Database.UpsertResult` |
| `merge` | `Database.MergeResult` |
| `delete` | `Database.DeleteResult` |
| `undelete` | `Database.UndeleteResult` |
| `convertLead` | `Database.LeadConvertResult` |
| `emptyRecycleBin` | `Database.EmptyRecycleBinResult` |

DML statements and `Database.*` methods with `allOrNone = true` roll the whole operation back.
With `allOrNone = false` the platform retries up to three times, resetting governor limits between
attempts and re-firing triggers on the shrinking subset; a third failure aborts with
`Too many batch retries in the presence of Apex triggers and partial failures.`

Savepoints cost one DML statement each, do not cost DML rows, cannot cross trigger invocations, and
must be released before a callout:

```apex
Savepoint sp = Database.setSavepoint();
try {
    insert as user orders;
    insert as user orderItems;
} catch (DmlException e) {
    Database.rollback(sp);
    Database.releaseSavepoint(sp);   // required before any callout in this transaction
    throw new OrderException('Order creation failed', e);
}
```

Failing to release produces `All active Savepoints must be released before making callouts.`;
pending uncommitted DML produces `You have uncommitted work pending. Please commit or rollback
before calling out.`

### 5. Custom exceptions that carry data, not strings

Any class whose name ends in `Exception` and extends `Exception` is a custom exception. Never put
personal data in the message — subclass with typed properties instead.

```apex
public with sharing class OrderException extends Exception {
    public List<Id> failedRecordIds { get; private set; }

    public OrderException(String message, List<Id> failedRecordIds) {
        this(message);
        this.failedRecordIds = failedRecordIds;
    }
}
```

Trigger-level validation uses `addError` rather than a thrown exception, so the platform can build
a complete error list and support partial saves. An unhandled exception in a trigger marks **every**
record in scope as failed and stops processing.

```apex
for (Case c : Trigger.new) {
    if (String.isBlank(c.Subject)) {
        c.Subject.addError(Label.Case_Subject_Required);
    }
}
```

### 6. Describe calls, custom settings, custom metadata

`Schema.getGlobalDescribe()` builds the whole org map — never call it in a loop, and never call it
at all when a token literal works.

```apex
private static final Map<String, Schema.SObjectField> CASE_FIELDS =
    Schema.SObjectType.Case.fields.getMap();
```

| Configuration store | Apex access | SOQL cost |
| --- | --- | --- |
| Hierarchy custom setting | `MySetting__c.getInstance()`, `getInstance(profileOrUserId)`, `getOrgDefaults()` | none — application cache |
| List custom setting | `MySetting__c.getValues('name')`, `getAll()` | none — application cache |
| Custom metadata type | `[SELECT ... FROM My_Type__mdt]`, `My_Type__mdt.getInstance('DevName')` | queries on `__mdt` do not count against the transaction SOQL limit |

Custom metadata is the right home for per-environment tuning because its queries are unmetered.
Never store secrets in custom settings — outside a managed package they are readable by every
profile, including the guest user.

### 7. Enterprise patterns: Selector, Domain, Service, Unit of Work

| Layer | Owns | Never does |
| --- | --- | --- |
| Selector | SOQL for one sObject, field lists, access mode | business rules, DML |
| Domain | per-record validation and defaulting for one sObject | cross-object orchestration |
| Service | a named business transaction across objects | direct SOQL, direct DML ordering |
| Unit of Work | registration and ordered commit of dirty records | business rules |

```apex
public with sharing class OpportunityService {
    public static void closeWon(Set<Id> opportunityIds) {
        UnitOfWork uow = new UnitOfWork(
            new List<SObjectType>{ Opportunity.SObjectType, Task.SObjectType }
        );
        for (Opportunity o : new OpportunitySelector().selectOpenByIds(opportunityIds)) {
            uow.registerDirty(new Opportunity(Id = o.Id, StageName = 'Closed Won'));
            uow.registerNew(new Task(WhatId = o.Id, Subject = 'Kick off delivery'));
        }
        uow.commitWork();
    }
}
```

Full runnable `SObjectSelector`, `Domain`, `Service`, and `UnitOfWork` implementations (no external
library required) are in [references/enterprise-patterns.md](references/enterprise-patterns.md).

### 8. Apex exposed to LWC and REST

```apex
public with sharing class AccountController {
    @AuraEnabled(cacheable=true)
    public static List<Account> searchAccounts(String term) {
        String like = '%' + String.escapeSingleQuotes(term) + '%';
        return [
            SELECT Id, Name, Industry, AnnualRevenue
            FROM Account
            WHERE Name LIKE :like
            WITH USER_MODE
            ORDER BY Name
            LIMIT 50
        ];
    }

    @AuraEnabled
    public static Id createAccount(String name) {
        try {
            Account a = new Account(Name = name);
            insert as user a;
            return a.Id;
        } catch (DmlException e) {
            throw new AuraHandledException(e.getDmlMessage(0));   // never leak a stack trace
        }
    }
}
```

`cacheable=true` is required for `@wire` and forbids DML in the method. Method overloads are not
allowed on `@AuraEnabled` methods from API 55.0 onward. `@AuraEnabled(cacheable=true scope='global')`
(API 55.0+) promotes results to the global cache.

```apex
@RestResource(urlMapping='/v1/accounts/*')
global with sharing class AccountRest {
    @HttpGet
    global static Account getAccount() {
        String id = RestContext.request.requestURI.substringAfterLast('/');
        return [SELECT Id, Name, Industry FROM Account WHERE Id = :id WITH USER_MODE];
    }
}
```

`@RestResource` requires a `global` class, maps relative to
`https://<instance>/services/apexrest/`, is case sensitive, and resolves exact matches before the
longest wildcard match. Outbound callouts belong in `sf-integration-patterns`.

## Anti-patterns

| Anti-pattern | Failing code | Fix |
| --- | --- | --- |
| SOQL in a loop | `for (Case c : Trigger.new) { Account a = [SELECT ... WHERE Id = :c.AccountId]; }` | one `WHERE Id IN :accountIds` query into a `Map<Id, Account>` |
| DML in a loop | `for (String n : names) { insert new Account(Name = n); }` | accumulate into a `List`, then one `insert` |
| Trigger assuming one record | `User u = [SELECT Id FROM User WHERE Mileage__c = :Trigger.new[0].Id];` | bind the collection: `WHERE Mileage__c IN :Trigger.newMap.keySet()` |
| Two triggers per object | `CaseTrigger` plus `CaseAuditTrigger` | one trigger, two handler methods, explicit order |
| Boolean recursion flag that never resets | `if (done) return; done = true;` | Id-set guard keyed by operation, `@TestVisible` so tests can reset |
| `without sharing` on a shared service | `public without sharing class AccountService` | `with sharing` service plus a tiny `without sharing` helper for the one elevated read |
| Silent swallow | `try { ... } catch (Exception e) {}` | rethrow a typed custom exception or `addError` |
| `Database.insert(list, false)` with results discarded | failures invisible | iterate `SaveResult`, surface `getErrors()` |
| Describe in a loop | `Schema.getGlobalDescribe().get(name)` per iteration | hoist into a `static final Map` |
| Hard-coded Ids | `if (p.Id == '00e1x...')` | custom metadata type, or query by name |
| `System.assertEquals` used as production validation | assertion in non-test code | `addError`, or throw a custom exception |
| `@AuraEnabled(cacheable=true)` performing DML | runtime error at call time | drop `cacheable`, or split read and write methods |

Rows 1, 2, 8 and 10 are detected by `vf-check analyzer` (`AvoidSoqlInLoops`,
`AvoidDmlStatementsInLoops`, `OperationWithLimitsInLoop`, `AvoidHardcodedId`); the rest are review.

## Verification

```bash
# Static gate (prettier + eslint + code-analyzer) then the full local gate (adds LWC Jest)
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" static --changed
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# Org-side Apex tests + coverage gates (apexOrgCoverageMin 85 / apexClassCoverageMin 75)
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-dev

# Compile-only proof that the classes deploy
sf project deploy validate --source-dir force-app/main/default/classes \
  --test-level RunSpecifiedTests --tests CaseEscalationServiceTest --target-org vf-dev

# Behaviour probe against a live org
sf apex run --file scripts/apex/probe-escalation.apex --target-org vf-dev
```

## References

| Reference file | Contents |
| --- | --- |
| [references/trigger-framework.md](references/trigger-framework.md) | runnable `TriggerHandler` base class, dispatcher, bypass API, recursion control, handler tests |
| [references/enterprise-patterns.md](references/enterprise-patterns.md) | Selector, Domain, Service, Unit of Work with complete code and a layering checklist |
| [references/order-of-execution.md](references/order-of-execution.md) | 20-step save order, recursive-save skips, workflow re-fire, roll-up cascades, operations that skip triggers |
| [references/apex-language-reference.md](references/apex-language-reference.md) | annotations, access modifiers, sharing and user-mode matrix, trigger context variables, System classes |

| Official source | URL |
| --- | --- |
| Apex Developer Guide (PDF, Winter '27 / API 68.0) | https://resources.docs.salesforce.com/264/latest/en-us/sfdc/pdf/salesforce_apex_developer_guide.pdf |
| Apex Reference Guide (PDF, Summer '26 / API 67.0) | https://resources.docs.salesforce.com/262/latest/en-us/sfdc/pdf/salesforce_apex_reference_guide.pdf |
| Sharing keywords | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_keywords_sharing.htm |
| Access mode for database operations | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_enforce_usermode.htm |
| Triggers and order of execution | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_triggers_order_of_execution.htm |
| Trigger context variables | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_triggers_context_variables.htm |
| Bulk DML exception handling | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dml_bulk_exceptions.htm |
| Transaction control and savepoints | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_transaction.htm |
| Custom exceptions | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_exception_custom.htm |
| `@AuraEnabled` | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_annotation_AuraEnabled.htm |
| `@RestResource` | https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_annotation_rest_resource.htm |
| Apex Enterprise Patterns (Trailhead) | https://trailhead.salesforce.com/en/content/learn/modules/apex_patterns_sl |
| fflib-apex-common reference implementation | https://github.com/apex-enterprise-patterns/fflib-apex-common |
