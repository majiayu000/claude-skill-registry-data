---
name: dataverse-query-optimizer
description: "Translate natural language data requests into optimized FetchXML or OData for Dataverse, applying performance best practices and avoiding anti-patterns. Use to query Dataverse, optimize an existing query, or retrieve data from Dynamics 365 or Power Apps."
---

# Dataverse Query Optimizer

Translate natural language data requests into optimized FetchXML or OData queries for Microsoft Dataverse. Syntax blocks (column selection, filters, joins, aggregation, pagination), a worked interaction and advanced scenarios are in `references/query-patterns.md`.

## Workflow

### Step 1: Understand the request

Identify: target table(s), required columns, filter criteria, related data (joins), aggregation (COUNT, SUM, AVG), sorting, limit (is pagination needed?). Example: "active contacts in Montreal created this year" means table `contact`, columns fullname/emailaddress1/telephone1/createdon, filters statecode=0, city, createdon, sort by fullname, limit about 1000.

### Step 2: Validate against anti-patterns

- Leading wildcards (`%Smith`): use Dataverse Search or redesign.
- Filtering on calculated/formula columns: filter on the source columns.
- Selecting all columns: select only what is needed.
- Nested joins deeper than 3 levels: denormalize or split into several queries.
- Missing pagination on large datasets: implement paging.

Complete list: `references/query-optimization-guide.md`.

### Step 3: Generate the query

Produce FetchXML and OData when possible.
- FetchXML: XML syntax, used in the Power Automate "List rows" action, supports aggregation and pagination, 5000 records per request maximum.
- OData: REST query parameters for the Web API, better for programmatic access.

### Step 4: Apply performance optimizations

Always: specific columns (`<attribute>` or `$select`, never `<all-attributes />` unless explicitly requested for debugging), a result limit (`top` or `$top`), filters on indexed columns (primary keys, lookups, statecode, statuscode, createdon, modifiedon, createdby, modifiedby), explicit sorting (`<order>` or `$orderby`).

Consider: late materialization for many joins or lookup columns, pagination above about 500 records, aggregation instead of retrieving records for counts and sums, `inner` vs `outer` link types, joins kept to 1-3 levels.

### Step 5: Present query and explanation

Give the query (FetchXML and OData), why the structure was chosen, optimization notes, usage (Power Automate "List rows" > "Fetch Xml Query", or Web API GET), and warnings (for example pagination needed above 5000 records).

## References

Load as needed:
- `references/fetchxml-reference.md`: FetchXML syntax, aggregation, late materialization, joins, paging-cookie.
- `references/odata-reference.md`: OData operators, functions, `$expand`, Web API usage.
- `references/query-optimization-guide.md`: performance practices, anti-patterns, troubleshooting slow queries, error reference.
- `references/examples.md`: natural language to query transformations.
- `references/query-patterns.md`: syntax blocks, worked interaction, advanced scenarios (OR filters, NOT EXISTS, slow queries), tools.

## Common table names

| Business entity | Logical name | Entity set name |
|---|---|---|
| Accounts | account | accounts |
| Contacts | contact | contacts |
| Leads | lead | leads |
| Opportunities | opportunity | opportunities |
| Cases | incident | incidents |
| Activities | activitypointer | activitypointers |
| Users | systemuser | systemusers |
| Teams | team | teams |
| Business Units | businessunit | businessunits |

FetchXML uses the logical name, OData uses the entity set name (plural).

## Best practices

1. Ask clarifying questions when the request is ambiguous: which table, which columns, what defines "active", how many records.
2. Provide both FetchXML and OData when possible.
3. Explain the optimizations and include usage instructions for the context (Power Automate, Web API).
4. Warn about anti-patterns and suggest alternatives when the request would produce an inefficient query.

## Important reminders

- FetchXML maximum: 5000 records per request. OData maximum: 5000 standard table rows, 500 elastic table rows (without pagination).
- Always implement pagination for large datasets.
- Test queries with production-like data volumes and monitor performance over time.
- Dataverse optimizes queries automatically, but start with efficient ones.

## Error handling

- `LeadingWildcardCauseTimeout (0x80048573)`: remove leading wildcards from LIKE conditions, use Dataverse Search.
- `ComputedColumnCauseTimeout (0x80048574)`: remove filters on calculated/formula columns, filter on source columns.
- Query throttling errors: review against anti-patterns, simplify the structure, add delays for batch operations.

See `references/query-optimization-guide.md` for the complete error reference.
