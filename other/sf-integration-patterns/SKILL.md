---
name: sf-integration-patterns
description: Salesforce integration design and implementation - selecting an integration pattern (Remote Process Invocation request-reply and fire-and-forget, Batch Data Synchronisation, Remote Call-In, UI Update Based on Data Changes, Data Virtualisation), building inbound APIs (REST API, composite/composite-graph/batch/tree, sObject Collections, Bulk API 2.0, SOAP, Apex REST @RestResource, GraphQL API, Pub/Sub API, Streaming/CometD), and building outbound integrations (Apex HttpRequest callouts, Continuation, Named Credentials and External Credentials, External Services, Outbound Messages, Change Data Capture, Salesforce Connect external objects). Use this skill when a story involves callouts, webhooks, platform events, named credentials, external credentials, middleware boundaries, retry and idempotency design, callout mocking with HttpCalloutMock and Test.setMock, or probing a real org with sf api request rest. Also use it when reviewing integration code for transaction rules (no callout after DML), callout governor limits, secret handling, or dead-letter and correlation-id observability.
---

# Salesforce Integration Patterns

Pattern selection, inbound/outbound mechanics, retry and idempotency, and the verification commands
that prove an integration works. Owned in wave 1 by `sf-integration-engineer`
(paths: `namedCredentials/`, `externalCredentials/`, `externalServiceRegistrations/`,
`platformEvents` objects, integration Apex services). See skill `sf-workflow-orchestration`
for the wave model and `.vibeforce/state/contract.md` conventions.

## When to use

| Trigger | Use this skill for |
| --- | --- |
| Story says "call system X", "webhook", "sync from ERP" | Pattern selection table below, then `references/pattern-catalogue.md` |
| New endpoint to consume | `references/named-credentials.md` + `references/callout-and-retry.md` |
| External system must write into Salesforce | `references/inbound-apis.md` (limits, idempotency, composite) |
| Event-driven work (platform events, CDC, Pub/Sub) | Pattern 2 + 5 below, `references/pattern-catalogue.md` |
| Callout code review | Anti-patterns section, `references/callout-and-retry.md` |
| Tests for integration code | `references/integration-testing.md`, skill `sf-apex-testing` |
| Verifying a deployed integration in a real org | Verification section, skill `sf-post-deploy-verification` |

## Pattern selection

Six archetype patterns from Salesforce's Integration Patterns and Practices. Pick on latency,
volume, coupling, and transactionality - not on familiarity.

| Pattern | Direction | Timing | Volume | Transactional? | Primary mechanism |
| --- | --- | --- | --- | --- | --- |
| Remote Process Invocation - Request and Reply | SF -> remote | Synchronous | Small, real time | Response processed in the same SF transaction | External Services / Flow HTTP Callout / Apex `HttpRequest` (+ `Continuation` for slow endpoints) |
| Remote Process Invocation - Fire and Forget | SF -> remote | Asynchronous | Small per message | No; publisher does not wait | Platform event (Flow or Apex) consumed via Pub/Sub API; Event Relay to AWS; `@future`/Queueable callout |
| Batch Data Synchronisation | Both | Asynchronous, scheduled | Large (>2,000 records) | Per-batch only | ETL/MuleSoft + Bulk API 2.0; Change Data Capture for SF-as-master |
| Remote Call-In | remote -> SF | Synchronous request-reply | Small to medium; Bulk for large | Per call; composite gives all-or-none | REST API, Composite, Composite Graph, sObject Collections, Apex REST, GraphQL API, Bulk API 2.0, SOAP API |
| UI Update Based on Data Changes | SF -> SF UI | Near real time | Low | No | Platform event published by trigger/Flow, LWC `empApi` subscriber, Pub/Sub API for external UI |
| Data Virtualisation | SF -> remote (read/write) | Synchronous | Small per page | No | Salesforce Connect external objects (OData 2.0/4.0, cross-org, Apex Connector Framework) |

Decision shortcuts:

| Question | Answer |
| --- | --- |
| User waits for the answer? | Request and Reply. If the endpoint can be slow, use `Continuation` (LWC) - max 3 callouts per continuation, no DML in the continuation method. |
| Record change must notify N unknown subscribers? | Fire and Forget with a platform event; subscribers use Pub/Sub API (gRPC/HTTP2, Avro). |
| >2,000 records per run? | Bulk API 2.0 ingest, driven by middleware, not Apex callouts. |
| Remote system must create/update many related records atomically? | Composite (25 subrequests, `allOrNone`) or Composite Graph (500 nodes per payload). |
| Data must not be copied into Salesforce? | Data Virtualisation with Salesforce Connect. |
| Orchestration, protocol conversion, cross-system transactions? | Middleware (MuleSoft/Informatica). Salesforce cannot participate in distributed transactions. |
| Legacy option on the table (Outbound Messaging, Streaming API/CometD, SOAP `login()`)? | Replace: Flow + platform events, Pub/Sub API, OAuth 2.0. `login()` is unavailable in API v65.0+ and retires Summer '27. |

## Core patterns

### 1. Request and reply with a Named Credential

Never hardcode a URL or a secret. The endpoint lives in a `NamedCredential`; the authentication
lives in an `ExternalCredential`; users are authorised through a permission set mapped to an
external credential principal. See `references/named-credentials.md`.

```apex
public with sharing class BillingGateway {
    public class GatewayException extends Exception {}

    public static BillingAccount createAccount(Id accountId, String correlationId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:Billing_API/v1/accounts');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setHeader('X-Correlation-Id', correlationId);
        req.setHeader('Idempotency-Key', correlationId);
        req.setTimeout(20000); // ms; default 10000, max 120000
        req.setBody(JSON.serialize(new Map<String, Object>{
            'salesforceId' => accountId,
            'requestedAt' => Datetime.now()
        }));

        HttpResponse res = new Http().send(req);
        if (res.getStatusCode() == 200 || res.getStatusCode() == 201) {
            return (BillingAccount) JSON.deserialize(res.getBody(), BillingAccount.class);
        }
        throw new GatewayException(
            'Billing_API ' + res.getStatusCode() + ' ' + res.getStatus() + ': ' + res.getBody()
        );
    }

    public class BillingAccount {
        public String id;
        public String status;
    }
}
```

Rules enforced in review: `callout:` endpoint only, explicit timeout, status code checked before
deserialisation, correlation id propagated, exception carries the endpoint name and status.

### 2. Fire and forget with a platform event

Publish behaviour matters. `Publish After Commit` only publishes when the transaction commits -
choose it when subscribers read data written by the publisher. `Publish Immediately` publishes even
if the transaction later fails - choose it for logging-style events.

```apex
public with sharing class OrderEventPublisher {
    public static void publish(List<Order> orders) {
        List<Order_Submitted__e> events = new List<Order_Submitted__e>();
        for (Order o : orders) {
            events.add(new Order_Submitted__e(
                Order_Id__c = o.Id,
                Correlation_Id__c = IntegrationContext.newCorrelationId(),
                Payload__c = JSON.serialize(new Map<String, Object>{
                    'accountId' => o.AccountId, 'total' => o.TotalAmount
                })
            ));
        }
        List<Database.SaveResult> results = EventBus.publish(events);
        for (Integer i = 0; i < results.size(); i++) {
            if (!results[i].isSuccess()) {
                for (Database.Error e : results[i].getErrors()) {
                    IntegrationLog.error('Order_Submitted__e', events[i].Correlation_Id__c, e.getMessage());
                }
            }
        }
    }
}
```

Platform events are not rolled back by the publishing transaction and are published to the bus once;
Salesforce does not retry on the publisher side. High-volume event messages are retained for
72 hours and are replayable by Replay ID. Max event message size is 1 MB.

### 3. Retryable subscriber with bounded retries

Apex subscribers signal "redeliver this batch" with `EventBus.RetryableException`. A platform event
trigger runs at most 10 times for a batch sequence (1 run + 9 retries); after the 9th retry the
trigger enters an error state and stops consuming new events until the trigger is re-saved.

```apex
trigger OrderSubmittedTrigger on Order_Submitted__e (after insert) {
    try {
        OrderSubmittedHandler.handle(Trigger.new);
    } catch (CalloutException | QueryException transientError) {
        if (EventBus.TriggerContext.currentContext().retries < 9) {
            throw new EventBus.RetryableException(transientError.getMessage());
        }
        OrderSubmittedHandler.deadLetter(Trigger.new, transientError); // persists + alerts
    }
}
```

DML performed before the `RetryableException` is rolled back; the whole batch is redelivered in
Replay ID order. Anything that cannot be retried goes to a dead-letter object - see
`references/callout-and-retry.md`.

### 4. Callouts from an asynchronous context

Callouts are forbidden after DML in the same transaction and forbidden altogether in a
trigger's synchronous context. Move them to `Queueable` (preferred) or `@future(callout=true)`.

```apex
public with sharing class BillingSyncJob implements Queueable, Database.AllowsCallouts {
    private final List<Id> accountIds;
    private final Integer attempt;

    public BillingSyncJob(List<Id> accountIds) { this(accountIds, 0); }
    public BillingSyncJob(List<Id> accountIds, Integer attempt) {
        this.accountIds = accountIds;
        this.attempt = attempt;
    }

    public void execute(QueueableContext ctx) {
        System.attachFinalizer(new BillingSyncFinalizer(accountIds, attempt));
        for (Id accountId : accountIds) {
            BillingGateway.createAccount(accountId, IntegrationContext.newCorrelationId());
        }
    }
}
```

`System.attachFinalizer` gives a retry/dead-letter hook that runs in its own transaction even when
the job dies from an unhandled exception. Full engine with exponential backoff:
`references/callout-and-retry.md`. Async limits and chaining rules: skill `sf-async-apex-patterns`.

### 5. Inbound API for a remote caller

Prefer standard REST API and composite resources over custom Apex REST. Write Apex REST only when
you need multi-object transactionality or custom pre-commit logic.

```apex
@RestResource(urlMapping='/order-sync/*')
global with sharing class OrderSyncResource {
    @HttpPost
    global static ResponsePayload upsertOrder(String externalId, String status) {
        RestResponse res = RestContext.response;
        if (String.isBlank(externalId)) {
            res.statusCode = 400;
            return new ResponsePayload('error', 'externalId is required');
        }
        Order__c record = new Order__c(External_Id__c = externalId, Status__c = status);
        // Upsert on the external id makes repeated calls idempotent.
        Database.UpsertResult result = Database.upsert(record, Order__c.External_Id__c, false, AccessLevel.USER_MODE);
        if (!result.isSuccess()) {
            res.statusCode = 400;
            return new ResponsePayload('error', result.getErrors()[0].getMessage());
        }
        res.statusCode = result.isCreated() ? 201 : 200;
        return new ResponsePayload('ok', result.getId());
    }

    global class ResponsePayload {
        global String status;
        global String detail;
        global ResponsePayload(String status, String detail) {
            this.status = status; this.detail = detail;
        }
    }
}
```

Idempotency is the caller's requirement and your implementation duty: upsert on an External Id with
the Unique attribute, or record the caller's `Idempotency-Key` and short-circuit duplicates.

### 6. Data virtualisation

`Salesforce Connect` maps external tables to external objects. Relationships to external parents use
**external lookup** (matches the External ID standard field); external children to Salesforce parents
use **indirect lookup** (matches a custom field flagged External ID + Unique). The 120-second callout
timeout and adapter rate limits apply to every page render.

## Anti-patterns

| Anti-pattern | Failing code | Fix |
| --- | --- | --- |
| Callout after DML | `insert acct; Http h = new Http(); h.send(req);` -> `You have uncommitted work pending` | Do the callout first, or enqueue `Queueable implements Database.AllowsCallouts` after the DML |
| Callout in a trigger | `trigger T on Account (after insert) { BillingGateway.createAccount(...); }` | Publish a platform event or enqueue a Queueable from the trigger handler |
| Secret in code or custom setting | `req.setHeader('Authorization', 'Bearer ' + SECRET_C__c)` | External Credential principal parameter; reference `{!$Credential....}` or let `generateAuthorizationHeader` do it |
| No timeout | default 10 s per callout, 120 s cumulative per transaction | `req.setTimeout(n)` sized to the endpoint SLA; sum of all callouts must stay under 120 s |
| Unbounded retry loop | Queueable re-enqueuing itself on every failure | Bounded attempts + exponential backoff + dead letter (`references/callout-and-retry.md`) |
| Row-by-row REST calls from middleware | 5,000 single-record POSTs | sObject Collections (200 records/request) or Bulk API 2.0 for >2,000 |
| Trusting HTTP 200 from composite | `if (res.getStatusCode() == 200) success = true;` | Composite returns 200 even when a subrequest failed; inspect each subrequest result body |
| Mock that ignores the endpoint | single-response `HttpCalloutMock` for a multi-endpoint flow | Router mock keyed on endpoint + method (`references/integration-testing.md`) |
| Using retired syntax or APIs | `sfdx force:apex:execute`, SOAP `login()`, Outbound Messaging, CometD for new work | `sf apex run`, OAuth 2.0, Flow + platform events, Pub/Sub API |

## Verification

Local gate (no org needed) - static analysis and Jest:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed
```

Apex tests including callout mocks, in an org:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex \
  --target-org vf-dev --tests BillingGatewayTest,OrderSyncResourceTest
```

Probe the deployed integration surface against a real org (read-only):

```bash
# Named credential and external credential exist and are retrievable
sf project retrieve start --metadata NamedCredential:Billing_API --target-org vf-int

# Apex REST endpoint answers (uses the CLI's authenticated session)
sf api request rest "/services/apexrest/order-sync/?externalId=EXT-1" \
  --method GET --include --target-org vf-int

# Org limits that integrations consume
sf org list limits --target-org vf-int --json

# Platform event publishing worked (event bus usage is visible in limits, deliveries in the log)
sf data query --query "SELECT COUNT(Id) FROM AsyncApexJob WHERE JobType = 'Queueable' AND Status = 'Failed' AND CreatedDate = TODAY" \
  --target-org vf-int
```

Post-deploy smoke (wave 4, runs the anonymous-Apex probes and writes
`.vibeforce/reports/smoke-<ISO>.json`):

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" smoke --target-org vf-int
```

Never point a callout smoke probe at a production third-party endpoint. Sandbox endpoints only, or
mock through middleware - see skill `sf-post-deploy-verification`.

## References

- [references/pattern-catalogue.md](references/pattern-catalogue.md) - the six patterns with
  when/mechanism/limits/example, middleware capability matrix, legacy replacement table.
- [references/named-credentials.md](references/named-credentials.md) - NamedCredential and
  ExternalCredential metadata, authentication protocol matrix, permission set wiring, `callout:`
  usage, JWT claims, troubleshooting.
- [references/inbound-apis.md](references/inbound-apis.md) - REST/composite/composite-graph/
  collections/Bulk API 2.0/Apex REST/GraphQL/Pub-Sub with curl and `sf api request rest`, limits.
- [references/callout-and-retry.md](references/callout-and-retry.md) - Queueable + Finalizer retry
  engine, exponential backoff, dead letters, idempotency, transaction rules, callout limits.
- [references/integration-testing.md](references/integration-testing.md) - `HttpCalloutMock`,
  `Test.setMock`, multi-endpoint router mock, Apex REST tests, event tests, contract tests.

Official documentation used:

- Integration Patterns and Practices - https://architect.salesforce.com/docs/architect/fundamentals/guide/integration-patterns.html
- API Request Limits and Allocations - https://developer.salesforce.com/docs/platform/salesforce-app-limits-cheatsheet/guide/salesforce-app-limits-platform-api.html
- Bulk API and Bulk API 2.0 Limits - https://developer.salesforce.com/docs/platform/salesforce-app-limits-cheatsheet/guide/salesforce-app-limits-platform-bulkapi.html
- Composite resource - https://developer.salesforce.com/docs/platform/api-rest/guide/resources-composite-composite-post.html
- Composite Graph limits - https://developer.salesforce.com/docs/platform/api-rest/guide/resources-composite-graph-limits.html
- Named Credentials guide and glossary - https://developer.salesforce.com/docs/platform/named-credentials/guide/get-started.html
- Pub/Sub API allocations - https://developer.salesforce.com/docs/platform/pub-sub-api/guide/allocations.html
- Continuation limits - https://developer.salesforce.com/docs/platform/lwc/guide/apex-continuations-limits.html
- Transaction finalizers - https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_transaction_finalizers.htm
- Retry platform event triggers - https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_subscribe_apex_refire.htm
