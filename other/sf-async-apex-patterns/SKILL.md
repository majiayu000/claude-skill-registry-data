---
name: sf-async-apex-patterns
description: Selects and implements the right Salesforce asynchronous execution model - Queueable Apex with Finalizers, Batch Apex, Apex Cursors, Schedulable Apex with CRON expressions, future methods, Platform Events, and Change Data Capture - and covers chaining limits, scope sizing, Database.Stateful, transaction boundaries, idempotency, duplicate delivery, and job monitoring or abort through AsyncApexJob and CronTrigger. Use this skill when work involves System.enqueueJob, System.attachFinalizer, Database.executeBatch, Database.getQueryLocator, Database.getCursor, System.schedule, System.scheduleBatch, System.abortJob, EventBus.publish, EventBus.RetryableException, setResumeCheckpoint, @future, BatchApexErrorEvent, ChangeEventHeader, a *__e platform event, a *ChangeEvent trigger, an AsyncApexJob or CronTrigger query, or when a long-running or high-volume process must move off the synchronous transaction.
---

# Asynchronous Apex Patterns

## When to use

Use this skill when a Salesforce requirement cannot finish inside one synchronous transaction:
callouts from a trigger, data volumes above 50,000 query rows, scheduled maintenance, long-running
integration work, or cross-system event propagation. It owns the *choice* of async mechanism and the
correctness concerns that choice creates (retries, duplicate delivery, state, transaction boundaries).

Related skills: `sf-apex-development` (trigger/handler structure, `with sharing`, user mode),
`sf-apex-testing` (all async test mechanics), `sf-governor-limits` (full per-transaction limit
tables), `sf-soql-sosl-optimization` (query locator and cursor query tuning),
`sf-integration-patterns` (callout design, Named Credentials), `sf-debugging-logs` (debug logs for
async contexts), `sf-deployment-strategies` (deploying classes with pending scheduled jobs).

## Decision table

Pick the leftmost row whose constraints all hold.

| Mechanism | Max data reach | State | Callouts | Chaining | Transaction boundary | Choose when |
| --- | --- | --- | --- | --- | --- | --- |
| `Queueable` | 50,000 query rows per execution (50M rows with `Database.Cursor`) | full object state; non-primitive members serialized | yes, with `Database.AllowsCallouts` | 1 child per job; stack depth unlimited in prod, 5 in Developer/Trial | one transaction per `execute` | default async choice; complex arguments; ordered steps; needs a job id |
| `Queueable` + `Database.Cursor` | 50M rows per cursor | full | yes | self re-enqueue per chunk | one per chunk | large volume without consuming Batch Apex slots |
| `Database.Batchable` | 50M rows via `QueryLocator` | only with `Database.Stateful` (instance members) | yes, with `Database.AllowsCallouts`, 100 callouts per method | `Database.executeBatch` from `finish` | one transaction per `execute` chunk | record-set processing with per-chunk limit resets and per-chunk error isolation |
| `Schedulable` | delegates | persists between runs unless `transient` | no synchronous callouts | schedules batch/queueable | synchronous limits apply | clock-driven work; CRON schedule |
| `@future` | 50,000 query rows | none; primitives and primitive collections only | yes, with `@future(callout=true)` | cannot call another future | one transaction | legacy only, or mixed-DML isolation. Salesforce recommends Queueable instead |
| Platform event (`*__e`) | subscriber batch up to 2,000 messages | none | no callouts from event triggers | publish from subscriber | publisher and subscriber are separate transactions | decoupled fan-out, retry semantics, external subscribers |
| Change Data Capture (`*ChangeEvent`) | 1 event may carry many `recordIds` | none | no | publish from trigger | change event trigger runs after the DB transaction completes | replicate record deltas without writing publish code |
| Record-triggered flow async path | flow limits | flow variables | via invocable action | subflow | runs immediately after the triggering save completes | declarative async; see skill `sf-flow-automation` |

Hard numbers behind the table: `Queueable` allows up to 50 `System.enqueueJob` calls per synchronous
transaction but only 1 from an asynchronous transaction; Developer and Trial orgs cap the chained
stack depth at 5 (the parent plus four children); `Database.QueryLocator` may return up to 50 million
records and the job fails immediately above that; `executeBatch` scope caps at 2,000 with a
`QueryLocator` and has no upper bound with an `Iterable`; five batch jobs may be queued or active at
once with up to 100 more held in the Apex flex queue; 100 scheduled Apex jobs may exist at one time;
every async execution counts against the shared org limit of 250,000 async executions per 24 hours
or user licences x 200, whichever is greater.

## Core patterns

### 1. Queueable with callouts, delay, and duplicate suppression

```apex
public with sharing class SyncAccountQueueable implements Queueable, Database.AllowsCallouts {
    private final List<Id> accountIds;

    public SyncAccountQueueable(List<Id> accountIds) {
        this.accountIds = accountIds;
    }

    public void execute(QueueableContext context) {
        System.attachFinalizer(new SyncAccountFinalizer(context.getJobId(), accountIds));

        List<Account> accounts = [
            SELECT Id, Name, External_Id__c
            FROM Account
            WHERE Id IN :accountIds
            WITH USER_MODE
        ];
        HttpRequest request = new HttpRequest();
        request.setEndpoint('callout:ERP_Named_Credential/accounts');
        request.setMethod('POST');
        request.setHeader('Content-Type', 'application/json');
        request.setBody(JSON.serialize(accounts));
        HttpResponse response = new Http().send(request);
        if (response.getStatusCode() >= 300) {
            throw new CalloutException('ERP sync failed: ' + response.getStatusCode());
        }
    }
}
```

Enqueue with a minimum delay (0-10 minutes, ignored in tests) and a duplicate signature so a second
identical job is rejected with `DuplicateMessageException`:

```apex
AsyncOptions options = new AsyncOptions();
options.MinimumQueueableDelayInMinutes = 2;
options.MaximumQueueableStackDepth = 10;
options.DuplicateSignature = QueueableDuplicateSignature.Builder()
    .addString('SyncAccountQueueable')
    .addId(UserInfo.getUserId())
    .build();
try {
    Id jobId = System.enqueueJob(new SyncAccountQueueable(accountIds), options);
} catch (DuplicateMessageException e) {
    // An equivalent job is already enqueued. Nothing to do.
}
```

A queueable signature is cleared when the job is dequeued, so duplicates of an *already running* job
are still possible. Treat the signature as contention control, not as an exactly-once guarantee.

### 2. Finalizer as the failure boundary

```apex
public with sharing class SyncAccountFinalizer implements Finalizer {
    private final Id originalJobId;
    private final List<Id> accountIds;

    public SyncAccountFinalizer(Id originalJobId, List<Id> accountIds) {
        this.originalJobId = originalJobId;
        this.accountIds = accountIds;
    }

    public void execute(FinalizerContext ctx) {
        if (ctx.getResult() == ParentJobResult.SUCCESS) {
            return;
        }
        insert as system new Integration_Error__c(
            Job_Id__c = ctx.getAsyncApexJobId(),
            Request_Id__c = ctx.getRequestId(),
            Message__c = ctx.getException().getMessage()
        );
        // A finalizer may re-enqueue the failed job up to 5 consecutive times.
        System.enqueueJob(new SyncAccountQueueable(accountIds));
    }
}
```

The finalizer runs in its own Apex and database transaction, so DML buffered in the finalizer's state
survives a queueable that blew its limits. Only one finalizer per queueable job; a finalizer may
enqueue exactly one async job; the retry chain caps at 5 consecutive failures and resets on success.

### 3. Batch Apex with stateful aggregation and chaining

```apex
public with sharing class ArchiveClosedCasesBatch
        implements Database.Batchable<SObject>, Database.Stateful, Database.AllowsCallouts {
    public Integer archived = 0;

    public Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator(
            'SELECT Id, Status FROM Case WHERE IsClosed = true AND ClosedDate < LAST_N_DAYS:365',
            AccessLevel.USER_MODE
        );
    }

    public void execute(Database.BatchableContext bc, List<Case> scope) {
        List<Case_Archive__c> archives = new List<Case_Archive__c>();
        for (Case c : scope) {
            archives.add(new Case_Archive__c(Case_Id__c = c.Id));
        }
        Database.SaveResult[] results = Database.insert(archives, false, AccessLevel.USER_MODE);
        for (Database.SaveResult r : results) {
            if (r.isSuccess()) {
                archived++;
            }
        }
    }

    public void finish(Database.BatchableContext bc) {
        AsyncApexJob job = [
            SELECT Status, NumberOfErrors, JobItemsProcessed, TotalJobItems
            FROM AsyncApexJob
            WHERE Id = :bc.getJobId()
            WITH USER_MODE
        ];
        if (job.NumberOfErrors == 0) {
            Database.executeBatch(new PurgeArchivedCasesBatch(), 200);
        }
    }
}
```

```apex
Id jobId = Database.executeBatch(new ArchiveClosedCasesBatch(), 200);
```

Only instance members survive between chunks under `Database.Stateful`; statics are reset. Use a
scope size that is a factor of 2,000 (100, 200, 400...). Avoid relationship subqueries in the
`QueryLocator`: a `QueryLocator` without subqueries uses the fast chunked implementation, while an
`Iterable` or a subquery forces the slower non-chunking path. `FOR UPDATE` in the `start` query does
not apply to Batch Apex; requery with `FOR UPDATE` inside `execute` when you need row locks.

### 4. Apex Cursor plus chained Queueable for high volume

```apex
public with sharing class ContactPurgeCursorQueueable implements Queueable {
    private final Database.Cursor cursor;
    private Integer position;

    public ContactPurgeCursorQueueable() {
        this.cursor = Database.getCursor(
            'SELECT Id FROM Contact WHERE LastActivityDate = LAST_N_DAYS:400',
            AccessLevel.USER_MODE
        );
        this.position = 0;
    }

    private ContactPurgeCursorQueueable(Database.Cursor cursor, Integer position) {
        this.cursor = cursor;
        this.position = position;
    }

    public void execute(QueueableContext ctx) {
        Integer remaining = cursor.getNumRecords() - position;
        if (remaining <= 0) {
            return;
        }
        List<Contact> chunk = (List<Contact>) cursor.fetch(position, Math.min(200, remaining));
        delete as user chunk;
        Integer next = position + chunk.size();
        if (next < cursor.getNumRecords()) {
            System.enqueueJob(new ContactPurgeCursorQueueable(cursor, next));
        }
    }
}
```

A cursor spans up to 50 million rows, allows at most 100 `Cursor.fetch()` calls per transaction, and
each fetch counts against the SOQL query and query-row limits. Cursors consume no Batch Apex slots
and never queue behind the flex queue. `System.TransientCursorException` is retryable;
`System.FatalCursorException` is not.

### 5. Schedulable with CRON and one-shot batch scheduling

```apex
public with sharing class NightlyArchiveScheduler implements Schedulable {
    public void execute(SchedulableContext sc) {
        Database.executeBatch(new ArchiveClosedCasesBatch(), 200);
    }
}
```

```apex
// Seconds Minutes Hours Day_of_month Month Day_of_week Optional_year
String cron = '0 0 2 * * ?';                       // every day at 02:00 in the scheduling user's time zone
Id cronTriggerId = System.schedule('VF Nightly Archive', cron, new NightlyArchiveScheduler());

// One-shot batch 30 minutes from now, no Schedulable class required
Id oneShot = System.scheduleBatch(new ArchiveClosedCasesBatch(), 'VF Archive One Shot', 30, 200);
```

Job names must be unique or `System.AsyncException: The Apex job named "..." is already scheduled for
execution` is thrown. Apex cannot be scheduled more often than hourly. Scheduled Apex runs under
*synchronous* governor limits and cannot make synchronous web-service callouts - delegate callouts to
Queueable or Batch with `Database.AllowsCallouts`.

### 6. Platform events with an idempotent subscriber

```apex
public with sharing class OrderEventPublisher {
    public static void publish(List<Order> orders) {
        List<Order_Event__e> events = new List<Order_Event__e>();
        for (Order o : orders) {
            events.add(new Order_Event__e(Order_Id__c = o.Id, Status__c = o.Status));
        }
        List<Database.SaveResult> results = EventBus.publish(events);
        for (Database.SaveResult sr : results) {
            if (!sr.isSuccess()) {
                for (Database.Error e : sr.getErrors()) {
                    System.debug(LoggingLevel.ERROR, e.getStatusCode() + ': ' + e.getMessage());
                }
            }
        }
    }
}
```

```apex
trigger OrderEventTrigger on Order_Event__e (after insert) {
    Set<String> uuids = new Set<String>();
    for (Order_Event__e e : Trigger.new) {
        uuids.add(e.EventUuid);
    }
    Set<String> seen = new Set<String>();
    for (Event_Log__c log : [SELECT Event_Uuid__c FROM Event_Log__c
                             WHERE Event_Uuid__c IN :uuids WITH SYSTEM_MODE]) {
        seen.add(log.Event_Uuid__c);
    }

    List<Event_Log__c> logs = new List<Event_Log__c>();
    for (Order_Event__e e : Trigger.new) {
        if (seen.contains(e.EventUuid)) {
            continue;                                   // duplicate delivery, already processed
        }
        logs.add(new Event_Log__c(Event_Uuid__c = e.EventUuid, Replay_Id__c = e.ReplayId));
        EventBus.TriggerContext.currentContext().setResumeCheckpoint(e.ReplayId);
    }
    insert as system logs;
}
```

`EventUuid` is the only field guaranteed unique - `ReplayId` may repeat across org migrations, so use
it for positioning, never for identity. Publish Immediately (the default and recommended behaviour)
ignores transaction boundaries and cannot be rolled back by `Database.setSavepoint()`; Publish After
Commit respects them, counts against the DML statement limit, and can be rolled back. Publish
Immediately calls count against a separate limit of 150 `EventBus.publish()` calls, readable via
`Limits.getPublishImmediateDML()`.

### 7. Change Data Capture trigger

```apex
trigger AccountChangeTrigger on AccountChangeEvent (after insert) {
    List<Replication_Task__c> tasks = new List<Replication_Task__c>();
    for (AccountChangeEvent event : Trigger.new) {
        EventBus.ChangeEventHeader header = event.ChangeEventHeader;
        for (String recordId : header.recordIds) {
            tasks.add(new Replication_Task__c(
                Record_Id__c = recordId,
                Change_Type__c = header.changeType,       // CREATE UPDATE DELETE UNDELETE GAP_*
                Transaction_Key__c = header.transactionKey,
                Commit_User__c = header.commitUser
            ));
        }
    }
    insert as system tasks;
}
```

Change event triggers run asynchronously after the database transaction completes, so a single event
can carry many `recordIds` when identical changes are merged within one second. Always iterate
`header.recordIds`. Handle the `GAP_*` and `GAP_OVERFLOW` change types: they signal that Salesforce
could not generate a full event and the subscriber must re-read the record. For `UPDATE` events,
`header.changedFields` lists what actually changed, and `header.nulledfields` distinguishes
"changed to null" from "unchanged" (unchanged fields are also null in the Apex event message).

## Anti-patterns

**Enqueuing multiple children from one job.** Only one child per parent queueable is supported.

```apex
// WRONG - the second enqueue throws in an async context
public void execute(QueueableContext ctx) {
    System.enqueueJob(new StepA());
    System.enqueueJob(new StepB());
}
// RIGHT - one chain, or one job that does both units of work
public void execute(QueueableContext ctx) {
    System.enqueueJob(new StepA());   // StepA.execute enqueues StepB
}
```

**Passing sObjects to a future method.** `@future` parameters must be primitives or primitive
collections, and an sObject can change between call and execution.

```apex
// WRONG - does not compile
@future public static void touch(List<Account> accounts) { }
// RIGHT - pass ids, requery inside
@future public static void touch(List<Id> accountIds) {
    List<Account> accounts = [SELECT Id, Name FROM Account WHERE Id IN :accountIds WITH USER_MODE];
}
```

**Unbounded chained queueables with zero delay.** With `delay = 0` a self-chaining job can burn the
daily async limit in minutes. Bound the chain with `AsyncOptions.MaximumQueueableStackDepth` and
check `AsyncInfo.getCurrentQueueableStackDepth()` against
`AsyncInfo.getMaximumQueueableStackDepth()` before re-enqueuing.

**Assuming static state survives batch chunks.** Without `Database.Stateful` every static and
instance member resets each chunk; with it only *instance* members persist.

**Treating batch `execute` as transactional across chunks.** Each chunk is its own transaction. If
chunk 1 commits and chunk 2 fails, chunk 1 is not rolled back. Batch chunks can also re-run after a
service maintenance rollback, so any callout or external write inside `execute` must be idempotent.

**Using `ReplayId` as a dedupe key.** Use `EventUuid`. `ReplayId` is positional and is not guaranteed
unique across org migrations.

**Throwing `EventBus.RetryableException` for a permanent error.** Retries are capped at nine after
the initial run; after that the subscriber moves to the error state, disconnects, and drops events
published while it is down. Check `EventBus.TriggerContext.currentContext().retries` and stop below 9.

**Deploying a class that has pending scheduled jobs.** The deployment fails with `This schedulable
class has jobs pending or in progress - CronTrigger IDs (ids)`. Abort the job, deploy, reschedule. See
skill `sf-deployment-strategies`.

## Verification

```bash
# Compile and run only the async tests you touched
sf apex run test --target-org vf-dev --tests AsyncApexPatternsTest --synchronous --result-format human

# Local static gate (Prettier, ESLint, Code Analyzer) - no org needed
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# Org test + coverage gate
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-dev

# Post-deploy async health probe
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" smoke --target-org vf-uat

# Inspect the async queue directly
sf data query --target-org vf-dev --query "SELECT Id, JobType, ApexClass.Name, Status, NumberOfErrors, JobItemsProcessed, TotalJobItems, ExtendedStatus, CompletedDate FROM AsyncApexJob WHERE JobType != 'BatchApexWorker' ORDER BY CreatedDate DESC LIMIT 25"

# Inspect scheduled Apex
sf data query --target-org vf-dev --query "SELECT Id, CronJobDetail.Name, CronExpression, State, TimesTriggered, NextFireTime FROM CronTrigger WHERE CronJobDetail.JobType = '7'"

# Abort a runaway job
sf apex run --target-org vf-dev --file scripts/apex/abort-job.apex   # System.abortJob('707...');
```

`vf-check apex` enforces `gates.apexOrgCoverageMin` and `gates.apexClassCoverageMin`;
`vf-check analyzer` fails at `gates.analyzerFailSeverity`. Both read `.vibeforce/config.json`.

## References

- [references/queueable-and-finalizer.md](references/queueable-and-finalizer.md) - `Queueable`,
  `AsyncOptions`, `AsyncInfo`, duplicate signatures, `Finalizer`, `FinalizerContext`, error messages.
- [references/batch-apex.md](references/batch-apex.md) - `Database.Batchable` lifecycle, scope
  sizing, statuses, flex queue, limits, `BatchApexErrorEvent`, cursors versus batch.
- [references/platform-events-and-cdc.md](references/platform-events-and-cdc.md) - publish
  behaviour, publish callbacks, subscriber retry, `setResumeCheckpoint`, `ChangeEventHeader`.
- [references/async-job-monitoring.md](references/async-job-monitoring.md) - `AsyncApexJob`,
  `CronTrigger`, `EventBusSubscriber` queries, abort and retry runbooks.

Official documentation used for this skill (Apex Developer Guide, Winter '27 / API 68.0 at time of
writing; the vibe-force `apiVersion` default is 67.0):

- [Asynchronous Apex](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_async_overview.htm)
- [Queueable Apex](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_queueing_jobs.htm)
- [Detecting Duplicate Queueable Jobs](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dedupe_queueable.htm)
- [Transaction Finalizers](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_transaction_finalizers.htm)
- [Batch Apex](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_batch.htm)
- [Use Batch Apex](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_batch_interface.htm)
- [Apex Cursors](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_cursors.htm)
- [Cursors and Queueable versus Batch Apex](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_cursors_versus_batch.htm)
- [Apex Scheduler](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_scheduler.htm)
- [Future Methods](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_invoking_future_methods.htm)
- [Execution Governors and Limits](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm)
- [Triggers and Order of Execution](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_triggers_order_of_execution.htm)
- [Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_intro.htm)
- [Change Data Capture Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/cdc_intro.htm)
- [AsyncApexJob object reference](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_asyncapexjob.htm)
