---
name: code-app-connect
description: "Connect a Power Apps code app to data sources (SQL, SharePoint, Office 365, Dataverse, Copilot Studio agents). Use for pac code add-data-source, CRUD operations, metadata retrieval, getContext(), or connecting a code app to Dataverse or SQL."
---

# Power Apps Code App — Data Integration

Guide developers through connecting code apps to data sources, implementing data operations,
and integrating platform services. For complete CLI commands, TypeScript patterns, and API
reference, see [references/data-integration-guide.md](references/data-integration-guide.md).

## Workflow Overview

```
1. Discover connections    → pac connection list
2. Add data source         → pac code add-data-source ...
3. Import generated code   → import { XxxService } from './generated/services/...'
4. Implement operations    → Service.create(), .get(), .getAll(), .update(), .delete()
5. Test locally            → npm run dev
```

## Step 1 — Discover Available Connections

```bash
pac connection list
```

This returns Connection IDs and API Names for all connections in the environment. Note these values — you'll need them for `add-data-source`.

## Step 2 — Add a Data Source

The command varies by data source type:

**Nontabular (Office 365 Users, etc.):**
```bash
pac code add-data-source -a <apiName> -c <connectionId>
```

**Tabular (SQL, SharePoint) — requires dataset + table discovery:**
```bash
pac code list-datasets -a <apiId> -c <connectionId>
pac code list-tables -a <apiId> -c <connectionId> -d <datasetName>
pac code add-data-source -a <apiName> -c <connectionId> -t <tableId> -d <datasetName>
```

**Dataverse:**
```bash
pac code add-data-source -a dataverse -t <table-logical-name>
```

**Copilot Studio:**
```bash
pac code add-data-source -a "shared_microsoftcopilotstudio" -c <connectionId>
```

After adding, the SDK generates typed models in `/generated/models/` and services in `/generated/services/`.

## Step 3 — Use Generated Services

Every data source generates a `[Name]Service` and `[Name]Model`. Import and use them:

```typescript
import { AccountsService } from './generated/services/AccountsService';
import type { Accounts } from './generated/models/AccountsModel';
```

### Dataverse CRUD Pattern

Services expose `create`, `get`, `getAll({ select, filter, orderBy, top })`, `update` (partial) and `delete`. Full examples: references/data-integration-guide.md section 4.

### Copilot Studio Pattern

Call `CopilotStudioService.ExecuteCopilotAsyncV2({ message, notificationUrl, agentName })`. `notificationUrl` is required but unused (`https://notificationurlplaceholder`). `agentName` is case-sensitive and includes the publisher prefix. Details: references section 5.

**Warning:** Do NOT use `ExecuteCopilot` (fire-and-forget) or `ExecuteCopilotAsync` (returns 502). Only `ExecuteCopilotAsyncV2` returns actual response data.

## Step 4 — Advanced Patterns

- Runtime context: `getContext()` from `@microsoft/power-apps/app` returns user, app and host info (references section 7).
- Dataverse metadata: `Service.getMetadata({ schema: { columns: 'all', manyToOne: true } })` (references section 6). Cache at app startup, these calls are heavy.
- Removing a data source: `pac code delete-data-source -a <apiName> -ds <dataSourceName>` (references section 8).

## Dataverse Capabilities

| Supported | Not Supported |
|-----------|---------------|
| CRUD operations | Polymorphic lookups |
| OData filter, sort, top | Dataverse actions/functions |
| Paging (skipToken) | FetchXML |
| Formatted values (option sets) | Alternate keys |
| Metadata retrieval | Deleting Dataverse datasources via CLI |
| Lookup associations (many-to-one) | |

## What NOT to Do

- Do not use `ExecuteCopilot` or `ExecuteCopilotAsync` for Copilot Studio — only `ExecuteCopilotAsyncV2` works
- Do not skip dataset/table discovery for tabular sources — the command will fail without proper IDs
- Do not call `getMetadata()` on every render — cache at app startup
- Do not hardcode user info — use `getContext()` instead
