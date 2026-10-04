---
name: browse-integrations
description: "Discover the external services a project consumes and browse their cached contracts through the MDL CATALOG — OData entities and actions, REST clients and operations, AsyncAPI channels and messages. Use when asked what integrations exist, what an OData service offers, or what a business-event contract contains."
---

# Browse Integration Services and Contracts

This skill covers discovering external services, browsing cached contracts, and querying integration assets via the **MDL CATALOG** (local project metadata).

**⚠️ NOTE:** This covers the **MDL CATALOG keyword** (`SELECT ... FROM CATALOG.entities`), NOT the **Mendix Catalog CLI** (`mxcli catalog search`). See `.claude/skills/mendix/catalog-search` for the external service registry.

## When to Use This Skill

- User asks what external services are configured in the project
- User wants to see available entities or actions from an OData service
- User wants to browse a business event contract (AsyncAPI)
- User asks about integration catalog tables
- User wants to find entities available in a contract but not yet imported

## Discovery: List All Services

```sql
-- All OData clients (consumed services)
list consumed odata services;

-- All published OData services
list published odata services;

-- All consumed REST services
list consumed rest services;

-- All published REST services
list published rest services;

-- All business event services
list business event services;

-- All database connections
list database connections;

-- All external entities (imported from OData)
list external entities;

-- All external actions used in microflows
list external actions;
```

## Contract Browsing: OData $metadata

`create consumed odata service` auto-fetches and caches the `$metadata` XML from HTTP(S) URLs or reads it from local files. Browse it without network access:

**Note:** `MetadataUrl` supports:
- `https://...` or `http://...` — fetches from HTTP endpoint
- `file:///abs/path` — reads from local absolute path
- `./path` or `path/file.xml` — reads from local relative path (resolved against `.mpr` directory)

Local metadata files enable offline development, reproducible testing, and version-pinned contracts.
`create consumed odata service` auto-fetches and caches the `$metadata` XML. Browse it without network access:

```sql
-- List all entity types from the contract
list contract entities from MyModule.SalesforceAPI;

-- List actions/functions
list contract actions from MyModule.SalesforceAPI;

-- Inspect a specific entity (properties, keys, navigation)
describe contract entity MyModule.SalesforceAPI.PurchaseOrder;

-- Generate a CREATE EXTERNAL ENTITY statement from the contract
describe contract entity MyModule.SalesforceAPI.PurchaseOrder format mdl;

-- Inspect an action's signature
describe contract action MyModule.SalesforceAPI.CreateOrder;
```

## Contract Browsing: AsyncAPI (Business Events)

Business event client services cache the AsyncAPI YAML:

```sql
-- List channels
list contract channels from MyModule.ShopEventsClient;

-- List messages with payload info
list contract messages from MyModule.ShopEventsClient;

-- Inspect a message's payload properties
describe contract message MyModule.ShopEventsClient.OrderChangedEvent;
```

## Catalog Queries (requires REFRESH CATALOG)

```sql
refresh catalog;

-- All contract entities across all OData clients
select ServiceQualifiedName, EntityName, EntitySetName, PropertyCount, Summary
from CATALOG.CONTRACT_ENTITIES;

-- All contract actions
select ServiceQualifiedName, ActionName, ParameterCount, ReturnType
from CATALOG.CONTRACT_ACTIONS;

-- All contract messages
select ServiceQualifiedName, MessageName, ChannelName, OperationType, PropertyCount
from CATALOG.CONTRACT_MESSAGES;

-- Find available entities NOT YET imported
select ce.EntityName, ce.ServiceQualifiedName, ce.PropertyCount
from CATALOG.CONTRACT_ENTITIES ce
left join CATALOG.EXTERNAL_ENTITIES ee
  on ce.ServiceQualifiedName = ee.ServiceName and ce.EntityName = ee.RemoteName
where ee.Id IS null;

-- All REST operations across all consumed services
select ServiceQualifiedName, HttpMethod, path, Name
from CATALOG.REST_OPERATIONS
ORDER by ServiceQualifiedName, path;

-- Cross-cutting: all integration services in a module
select ObjectType, QualifiedName
from CATALOG.OBJECTS
where ObjectType in ('ODATA_CLIENT', 'REST_CLIENT', 'ODATA_SERVICE',
  'PUBLISHED_REST_SERVICE', 'BUSINESS_EVENT_SERVICE', 'DATABASE_CONNECTION')
and ModuleName = 'Integration';
```

## Workflow: Import Entities from a Contract

### Bulk import (all or filtered)

```sql
mdl 1;
-- Import all entity types at once
create external entities from MyModule.SalesforceAPI;

-- Import into a different module
create external entities from MyModule.SalesforceAPI into Integration;

-- Import only specific entities
create external entities from MyModule.SalesforceAPI entities (PurchaseOrder, Supplier);

-- Idempotent re-import (updates existing)
create or modify external entities from MyModule.SalesforceAPI;
```

### Single entity (with customization)

1. Browse available entities:
   ```sql
   list contract entities from MyModule.SalesforceAPI;
   ```

2. Inspect the entity you want:
   ```sql
   describe contract entity MyModule.SalesforceAPI.PurchaseOrder;
   ```

3. Generate the CREATE statement:
   ```sql
   describe contract entity MyModule.SalesforceAPI.PurchaseOrder format mdl;
   ```

4. Copy, customize (remove unwanted attributes), and execute:
   ```sql
   mdl 1;
   create external entity MyModule.PurchaseOrder
   from consumed odata service MyModule.SalesforceAPI (
       EntitySet: 'PurchaseOrders',
       RemoteName: 'PurchaseOrder',
       Countable: Yes
   )
   (
       Number: long,
       status: string(200),
       SupplierName: string(200),
       GrossAmount: decimal
   );
   ```
