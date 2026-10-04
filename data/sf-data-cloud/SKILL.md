---
name: sf-data-cloud
description: Salesforce Data Cloud (rebranded Data 360) from a developer's seat - deciding whether a story belongs in Data Cloud at all, modelling data lake objects (DLO) and data model objects (DMO) and the DLO-to-DMO mapping, choosing a primary key and an extract method, ingesting through the Ingestion API in streaming or bulk mode, understanding what identity resolution produces and how to query a unified profile, consuming calculated insights and data graphs, querying with Data 360 SQL through the Query API or with the sfsqlquery Apex namespace and ConnectApi.CdpQuery, the SOQL subset that works against DMOs, surfacing Data Cloud data in LWC through an Apex bridge and in Flow through the cdp invocable actions, source-tracking Data Cloud metadata types (DataStreamDefinition, ObjectSourceTargetMap, DataSrcDataModelFieldMap, MktCalcInsightObjectDef, DataConnectorIngestApi) in an SFDX project, and the ingestion and query limits that bite. Use when a story mentions Data Cloud, Data 360, a data stream, a DLO or DMO, unified profiles, calculated insights, data graphs, segments, the Ingestion API, or grounding an agent in customer data.
---

# Salesforce Data Cloud

Data Cloud is a lakehouse bolted to the Salesforce Platform, not another sObject. It ingests,
harmonises and unifies data, then exposes it read-only through SQL, a restricted SOQL subset, and
Connect API resources. Everything a developer does here is **schema, mapping, ingest, query** - never
DML. Salesforce rebranded Data Cloud to **Data 360** on 14 October 2025; both names appear in the
product and the documentation, and the API names still say `cdp` and `ssot`.

Agent grounding built on top of this data is skill `sf-agentforce-development`. Record loading into
CRM objects is skill `sf-data-management`. Callout mechanics and named credentials are skill
`sf-integration-patterns`.

## When to use

| The story says | Right home | Why |
| --- | --- | --- |
| "Unify customers across 4 source systems and give one profile" | **Data Cloud** | Identity resolution, link tables and unified DMOs exist for exactly this |
| "Aggregate 400M engagement rows into a lifetime-value metric" | **Data Cloud** calculated insight | OLAP store; a CRM rollup would blow every governor limit |
| "Ground an agent or a personalisation rule in behavioural data" | **Data Cloud** + skill `sf-agentforce-development` | Data graphs and unified profiles are the documented grounding surface |
| "Users must edit these records in the UI" | **Custom object** | DMOs are read-only from Apex; no DML, no FLS, no record-level sharing |
| "A handful of rows, read live from an ERP, never stored" | **External objects** (Salesforce Connect) | Data virtualisation - skill `sf-integration-patterns`, pattern 6 |
| "Push 5,000 orders a night into Salesforce records" | **Bulk API 2.0** | Skill `sf-data-management`; Data Cloud does not create CRM records |
| "Call a partner API and show the response on a page" | **Plain integration** | No storage, no unification - skill `sf-integration-patterns` |
| "Trigger logic when a field changes" | **Flow / Apex trigger** on the CRM object | Data Cloud has no triggers; it emits `DataObjectDataChgEvent` on data actions only |

Data Cloud is the **wrong** answer when the data is small, must be writable, must be shared by role
hierarchy, or must participate in a CRM transaction. Its object-level access is coarse: DMOs in every
data space are reachable from Apex in system mode, and there is no field-level security and no
record-level access control for them. If a story needs those controls, model it as a custom object
and read skill `sf-security-model`.

## Vocabulary and suffixes

| Term | Suffix | What it is |
| --- | --- | --- |
| Data lake object (DLO) | `__dlo` | Landing table holding ingested data in the source system's own schema |
| Data model object (DMO) | `__dlm` | C360 Data Model view over one or more DLOs. Stores no data, only references. Field API names always end `__c` |
| Unified DMO | `__dlm` | Output of identity resolution, for example `UnifiedIndividual__dlm` |
| Unstructured DLO / DMO | `__dlo` / `__dlm` | Chunking, indexing and embedding targets for RAG |
| Calculated insight object (CIO) | - | Aggregated or calculated metric derived from DMOs |
| Data graph (DG) | - | Precalculated JSON materialisation of several DMOs for real-time lookups |
| Data space | - | Partition of the tenant; most APIs take a `dataspace` argument, default `default` |
| Data kit | - | Packaging container for Data Cloud components |

In SQL and SOQL statements, data lake objects appear with a `__dll` suffix
(`sfmc_email_engagement_click_{EID}__dll`) while the object reference documents the DLO object suffix
as `__dlo`. Standard DMOs carry the `ssot__` namespace on both object and fields
(`ssot__Individual__dlm.ssot__Id__c`); some REST samples show the unprefixed alias. Resolve the exact
name from the org before hardcoding it - see the metadata call in `references/query-reference.md`.

## Core patterns

### 1. Decide the primary key before anything else

A DLO's primary key is declared per field with `primaryIndexOrder` on the transport field: an
integer starting at 1 that also orders a compound key; a missing value means the field is not part of
the key. Ingested rows upsert on that key, and updates are a **full replace** - patch semantics are
not supported. A key that is not stable in the source system produces duplicate rows that identity
resolution then has to clean up.

```xml
<!-- externalDataTranObjects/Ecom_Order.externalDataTranObject-meta.xml (excerpt) -->
<ExternalDataTranObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <availabilityStatus>Available</availabilityStatus>
    <creationType>Custom</creationType>
    <masterLabel>Ecommerce Order</masterLabel>
    <objectCategory>Engagement</objectCategory>
    <externalDataTranFields>
        <masterLabel>Order Id</masterLabel>
        <creationType>Custom</creationType>
        <datatype>text</datatype>
        <isDataRequired>true</isDataRequired>
        <primaryIndexOrder>1</primaryIndexOrder>
    </externalDataTranFields>
</ExternalDataTranObject>
```

`primaryIndexOrder` carries the same meaning on `MktDataTranField` under `MktDataTranObject`. Pick
whichever transport type the connector produced and set it there.

### 2. Map DLO to DMO in source-tracked metadata

Object-level mapping is `ObjectSourceTargetMap` (`objectSourceTargetMaps/`, API 51.0+); field-level
mapping is either the nested `FieldSourceTargetMap` or the standalone `DataSrcDataModelFieldMap`
(`dataSrcDataModelFieldMaps/`, API 53.0+). Both are retrievable and deployable.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<DataSrcDataModelFieldMap xmlns="http://soap.sforce.com/2006/04/metadata">
    <filterApplied>true</filterApplied>
    <filterOperationType>equals</filterOperationType>
    <filterValue>Active</filterValue>
    <masterLabel>DataSrcDataModel26</masterLabel>
    <sourceField>Account1.LastModifiedDate__c</sourceField>
    <targetField>ssot__Account__dlm.ssot__LastModifiedDate__c</targetField>
    <versionNumber>1.0</versionNumber>
</DataSrcDataModelFieldMap>
```

Map a record-modified field into the DMO. Without it, the model cannot tell which copy of a
duplicated record is newest, and reconciliation rules have nothing to rank on.

### 3. Ingest: streaming for events, bulk for files

One data stream accepts both interaction patterns. Pick per payload, not per project.

| | Streaming | Bulk |
| --- | --- | --- |
| Shape | JSON micro-batch to an object endpoint | CSV uploaded to a job |
| Latency | Processed asynchronously about every 3 minutes | Job queue; depends on volume |
| Size cap | 200 KB body per request | 150 MB per CSV, 100 files per job |
| Throughput cap | 250 requests/second across all Ingestion API object endpoints | 20 jobs per hour, 5 concurrent |
| Deletes | Up to 200 records per request | `operation: delete` job |

```bash
# Bulk: create, upload, close. {instance_url} is the Data Cloud token-exchange instance URL.
curl -X POST "$DC_INSTANCE/api/v1/ingest/jobs" \
  -H "Authorization: Bearer $DC_TOKEN" -H 'Content-Type: application/json' \
  -d '{"object":"Ecom_Order","sourceName":"Ecom_Connector","operation":"upsert"}'

curl -X PUT "$DC_INSTANCE/api/v1/ingest/jobs/$JOB_ID/batches" \
  -H "Authorization: Bearer $DC_TOKEN" -H 'Content-Type: text/csv' --data-binary @orders.csv

curl -X PATCH "$DC_INSTANCE/api/v1/ingest/jobs/$JOB_ID" \
  -H "Authorization: Bearer $DC_TOKEN" -H 'Content-Type: application/json' \
  -d '{"state":"UploadComplete"}'
```

Ingestion is eventually consistent: allow at least 30 seconds after ingest before the rows are
queryable. Request shapes, job states and the CSV contract are in `references/ingestion-reference.md`.

### 4. Query from Apex with the `sfsqlquery` namespace

`sfsqlquery` is the recommended Apex surface. `ConnectApi.CdpQuery` remains as a lower-level
interface that mirrors the Connect REST endpoints.

```apex
public with sharing class LoyaltyLookup {
    public static List<String> topAccountNames() {
        sfsqlquery.SqlRowIterator rows = sfsqlquery.SqlStatement.create(
                'SELECT Id__c, Name__c FROM accounts__dlm LIMIT 200', 'default')
            .withWorkloadName('loyalty-userdashboard')
            .execute();

        List<String> names = new List<String>();
        for (sfsqlquery.Row row : rows) {
            names.add(row.getString('Name__c'));
        }
        return names;
    }
}
```

The iterator is single-use and submits nothing until iteration begins. `withWorkloadName` tags the
query so Salesforce Support can trace it; without it the framework uses
`dcsql_row_iterator_workload`.

`create(sql, dataspace)` takes a SQL string and nothing else, so never build a filter by
concatenating caller input into it. When the query needs a user-supplied value, a server-side row
limit or custom query settings, use the `create(ConnectApi.QuerySqlInput, dataspace)` overload,
which is the documented home for parameterised queries.

### 5. Page large result sets asynchronously

A synchronous iterator is bounded by the Apex transaction. For anything large, extend
`sfsqlquery.SqlQueueable`; the framework handles submission, status polling, pagination and chaining.

```apex
public with sharing class OrderRollupJob extends sfsqlquery.SqlQueueable {
    public OrderRollupJob(sfsqlquery.SqlStatement stmt) { super(stmt); }
    public OrderRollupJob(sfsqlquery.QueryHandle handle) { super(handle); }

    public override void processDataChunk() {
        for (sfsqlquery.Row row : getRows()) {
            OrderRollup.accumulate(row.getString('Id__c'), row.getDecimal('Amount__c'));
        }
    }

    public override void chainNextJob(sfsqlquery.QueryHandle handle) {
        System.enqueueJob(new OrderRollupJob(handle));
    }
}
```

`cancel()` inside `processDataChunk()` stops the chain. `getQueryId()` returns the server-assigned id;
persist it to resume later through `sfsqlquery.QueryHandle`. Async limits: skill
`sf-async-apex-patterns` and skill `sf-governor-limits`.

### 6. Use SOQL only where the subset covers you

SOQL against DMOs, DLOs and the unified profile is supported from API 51.0. It is a **subset**: no
subqueries, no aggregate functions, no date functions, no `HAVING`. `LIMIT` defaults to 100 and caps
at 2,000 records per call. Relationship traversal is not supported - joins go through SQL.

```apex
// A static SOQL query against a DMO is treated as a callout.
List<UnifiedIndividual__dlm> members = [
    SELECT Id, ssot__FirstName__c, ssot__LastName__c, ssot__Email__c
    FROM UnifiedIndividual__dlm
    WHERE ssot__CompanyId__c = :companyId
];
```

Because it is a callout, pending DML in the same transaction throws
`UnexpectedException: A callout was unsuccessful because of pending uncommitted work...`. Query
first, write second, or move the query into a Queueable. Query locators and `for` loops over DMOs
work from API 61.0 (earlier versions returned only the first 201 records); Batch Apex is blocked with
`QueryLocator` but supported with `Iterable`. Selectivity rules are the same discipline as skill
`sf-soql-sosl-optimization`.

### 7. Resolve a source record to its unified profile

Identity resolution applies match rules to group records and reconciliation rules to pick the best
value per attribute, writing link tables that leave the source rows intact. Three hops get you from a
source id to unified contact points.

```sql
-- 1. source record id -> unified record id
SELECT UnifiedRecordId__c FROM IndividualIdentityLink__dlm WHERE SourceRecordID__c = '{sourceId}' LIMIT 100
-- 2. unified individual
SELECT FirstName__c, LastName__c FROM UnifiedIndividual__dlm WHERE Id__c = '{unifiedId}' LIMIT 100
-- 3. unified contact point
SELECT EmailAddress__c FROM UnifiedContactPointEmail__dlm WHERE PartyId__c = '{unifiedId}' LIMIT 100
```

Joining non-unified DMOs needs the fully qualified key `KQ_Id__c` as well as the business key,
compared with `IS NOT DISTINCT FROM` because it can be null. Unified DMOs have no `KQ_Id__c` - there
are no duplicate record ids to disambiguate.

### 8. Surface it in the UI through an Apex bridge, and in Flow through `cdp` actions

There is no Data Cloud-specific LWC wire adapter in the Lightning Web Components reference
`[unverified]`; the documented client path is an `@AuraEnabled(cacheable=true)` Apex method that runs
`sfsqlquery` or `ConnectApi.CdpQuery` in the running user's context. Flow gets standard invocable
actions instead - `cdpGetDataGraph` (API 61.0+), `cdpGetDataGraphByLookup` (63.0+),
`cdpGetDataGraphMetadata` (64.0+), `cdpPublishCalculatedInsight`, `cdpPublishSegment`,
`cdpRefreshDataStream`, `cdpValidateSegmentMember` (all 60.0+), `cdpRunIdentityResolution` (57.0+)
and `dataCloudIngestionApi` (61.0+). Full wiring: `references/apex-lwc-flow.md`.

### 9. Test without an org

Two independent mocking frameworks, one per query surface.

| Query style | Mock with |
| --- | --- |
| `sfsqlquery` | `sfsqlquery.SqlTester` - `clearMocks()`, `setMockMetadata()`, `setMockRows()`, `enqueueMockRows()` for multi-page |
| SOQL against a DMO | `System.SoqlStubProvider` + `Test.createSoqlStub()` + `Test.createStubQueryRow()` |
| `ConnectApi.Cdp*` | The matching `setTest*` method, registered before the real call |

```apex
@IsTest
static void returnsMockedRow() {
    sfsqlquery.SqlTester.clearMocks();
    ConnectApi.QuerySqlMetadataItem col = new ConnectApi.QuerySqlMetadataItem();
    col.name = 'Name__c';
    col.type = ConnectApi.TypeEnum.VARCHAR;
    sfsqlquery.SqlTester.setMockMetadata(new List<ConnectApi.QuerySqlMetadataItem>{ col });

    ConnectApi.QuerySqlRow mockRow = new ConnectApi.QuerySqlRow();
    mockRow.rowData = new List<Object>{ 'Acme' };
    sfsqlquery.SqlTester.setMockRows(new List<ConnectApi.QuerySqlRow>{ mockRow });

    sfsqlquery.SqlRowIterator it = sfsqlquery.SqlStatement.create(
        'SELECT Name__c FROM accounts__dlm', 'default').execute();
    Assert.areEqual('Acme', it.next().getString('Name__c'));
}
```

## Data modelling: DLO to DMO mapping and key choice

1. **Name the grain.** One DLO row equals one source record. If the source emits a change event per
   field, the grain is the event, not the entity, and the key must include the event id.
2. **Pick a key the source owns.** `primaryIndexOrder` starting at 1; compound keys number the
   attributes in order. Never key on an ingest timestamp or a hash of the whole row.
3. **Declare the extract method.** `DataStreamDefinition.dataExtractMethods` takes `FULL_REFRESH`,
   `DATETIME_CDC` or `NUMERIC_CDC`; `DATETIME_CDC` and `NUMERIC_CDC` need `dataExtractField` set to
   the transport field that carries the watermark.
4. **Map to the standard DMO first.** The C360 model ships over 300 objects. Map `Individual`,
   `ContactPointEmail`, `ContactPointPhone` and `ContactPointAddress` before inventing a custom DMO -
   identity resolution, segments and data graphs are written against the standard shapes.
5. **Map the record-modified field.** Reconciliation cannot rank source copies without it.
6. **Use `sourceFormula` for cheap harmonisation.** `isSourceFormula` plus `sourceFormula` covers
   concatenation, date functions and constants at map time, avoiding a second DLO.
7. **Filter at the mapping.** `filterApplied` / `filterOperationType` / `filterValue` keep rows out
   of the DMO instead of filtering in every query.

Every metadata type, folder, file suffix and field is tabulated in `references/object-model.md`.

## Anti-patterns

| Anti-pattern | What it looks like | Fix |
| --- | --- | --- |
| Treating a DMO like an sObject | `insert new UnifiedIndividual__dlm(...)` or `update dmoRecord` | DMOs are read-only. Write to the source system and re-ingest, or model a custom object |
| Row-by-row DMO reads | `for (Id id : ids) { … FROM ssot__Individual__dlm WHERE ssot__Id__c = :id …}` | One set-based query, or a data graph lookup for real-time single-record access |
| SOQL on a DMO after DML | `insert acct;` then `[SELECT … FROM ssot__Account__dlm]` | The query is a callout; it fails on uncommitted work. Query first or enqueue a Queueable |
| Ingesting without a stable key | No `primaryIndexOrder`, or keyed on load timestamp | Declare the source's natural key; upsert is keyed on it |
| Expecting patch semantics | Sending only changed columns in a bulk CSV | Updates are a full replace. Send every field defined in the schema; blank means null |
| Querying immediately after ingest | Ingest then assert in the same script | Eventual consistency; allow at least 30 seconds |
| `SELECT *` against a DMO | Wide scans over billions of rows | Project the columns you need, filter early, use the primary or a secondary index |
| Unbounded `queryANSISql` | Expecting more than 49,999 rows in one call | `querySql` + `querySqlRows` pagination, or `sfsqlquery.SqlQueueable` |
| Relying on FLS for DMOs | `Security.stripInaccessible()` to hide DMO fields | Only object-level access is enforced. Filter in the query or do not expose the field |
| Clicking the model together, then deploying nothing | Data streams and mappings live only in the org | Build in the data kit, download the manifest, retrieve into the project |
| Hand-written `package.xml` for a data kit | Guessing component names | Download Manifest from the data kit, then `sf project retrieve start --manifest` |
| Ignoring `429` | Retrying a rejected ingest immediately | Back off. `429` means reduce request frequency |

## Verification

Retrieve and deploy the Data Cloud metadata the data kit manifest names:

```bash
sf project retrieve start --manifest package.xml --target-org vf-dev
sf project deploy start --manifest package.xml --target-org vf-dev

# One type at a time when debugging a mapping
sf project deploy start \
  --metadata DataStreamDefinition:Ecom_Order_Stream \
  --metadata ObjectSourceTargetMap:Ecom_Order_To_SalesOrder \
  --target-org vf-dev
```

Prove the data is there. `sf data query` runs the SOQL subset; `sf api request rest` reaches the
Connect REST query resource with the CLI's authenticated session. `v67.0` comes from
`config/vibe-force.defaults.json` (`apiVersion`); the Salesforce sample shows `v64.0`.

```bash
sf data query \
  --query "SELECT Id__c, FirstName__c FROM UnifiedIndividual__dlm LIMIT 10" \
  --target-org vf-int

sf api request rest "/services/data/v67.0/ssot/query-sql" \
  --method POST --header 'Content-Type: application/json' \
  --body '{"sql":"SELECT COUNT(*) FROM ssot__Individual__dlm"}' \
  --include --target-org vf-int
```

Exercise the Apex surface directly before trusting a controller:

```bash
sf apex run --file scripts/apex/dc-probe.apex --target-org vf-int
```

Project gates, in the usual order:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" static --changed
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex \
  --target-org vf-dev --tests LoyaltyLookupTest,OrderRollupJobTest
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" deploy-validate --target-org vf-int
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" smoke --target-org vf-int
```

Never point an ingest smoke probe at a production Data Cloud tenant: ingested rows cannot be deleted
by rolling back a deploy, and every query consumes credits.

## References

- [references/object-model.md](references/object-model.md) - DLO, DMO, unified, UDLO/UDMO, CIO and
  data graph terminology; every Data Cloud metadata type with folder, suffix and API version;
  mapping and key-selection rules; packaging support.
- [references/ingestion-reference.md](references/ingestion-reference.md) - Ingestion API bulk job
  lifecycle and streaming endpoints, CSV and date contracts, connector options, OAuth scopes and the
  two-step token exchange, identity implications of each path.
- [references/query-reference.md](references/query-reference.md) - Data 360 SQL surface, Query API
  v3 and the Connect REST `ssot/query-sql` resource, the `ConnectApi.CdpQuery` method catalogue, the
  SOQL subset, worked queries with sample output.
- [references/apex-lwc-flow.md](references/apex-lwc-flow.md) - `sfsqlquery` class reference, Apex
  security model for DMOs, the LWC Apex bridge, Flow invocable actions and data actions, and the
  three test-mocking frameworks.
- [references/limits-and-quotas.md](references/limits-and-quotas.md) - every number with the page it
  came from.

Official documentation used:

- Query Data in Data 360 - https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/query-guide-get-started.html
- Query Data 360 Data using Query API - https://developer.salesforce.com/docs/data/data-cloud-query-guide/references/data-cloud-query-api-reference/c360a-api-queryservices-overview.html
- Query Data 360 Data with Apex - https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/dc-apex-query.html
- Data 360 In Apex - https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/DataCloudInApex.htm
- Mock SOQL Tests for Data 360 DMOs - https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/MockSOQLTestsForDMOs.htm
- Data Cloud Query Profile Parameters (SOQL) - https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_cdp_query.htm
- Salesforce Data Cloud Objects - https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_concepts_data_cloud_objects.htm
- Data 360 Metadata Types - https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_data_cloud_types.htm
- Get Started with Ingestion API - https://developer.salesforce.com/docs/data/data-cloud-int/references/data-cloud-ingestionapi-ref/c360-a-api-get-started.html
- Custom App Development - https://developer.salesforce.com/docs/data/data-cloud-dev/guide/custom-app-dev.html
- Data 360 Architecture - https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-architecture.html
