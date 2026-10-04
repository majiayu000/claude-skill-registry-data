---
name: connect-rapidminer-graph
description: "Fetch data from a RapidMiner graph mart or any SPARQL 1.1 HTTP endpoint (AnzoGraph and friends) and surface it as Mendix entities. Use when a graph database with a SPARQL endpoint has to feed a Mendix app read-only."
---

# Connecting Mendix to RapidMiner / AnzoGraph via SPARQL

Use this skill when you need to fetch data from a RapidMiner graph mart (or any SPARQL 1.1 HTTP endpoint like AnzoGraph) and surface it in a Mendix app.

## When to Use

- An external graph database exposes a SPARQL HTTP endpoint with Basic Auth
- You want the graph results to become Mendix entities (for display, search, further processing)
- You have read-only needs — the pattern fits SELECT queries that return tabular results

## Endpoint shape

A RapidMiner / AnzoGraph graphmart endpoint looks like:

```
https://<host>/sparql/graphmart/<url-encoded-graphmart-uri>
```

Example:
```
https://graphstudio.mendixdemo.com/sparql/graphmart/http%3A%2F%2Fcambridgesemantics.com%2FGraphmart%2F3617250aca6a40d88972c1c0de38f86a
```

Two things to note:
1. The graphmart URI is **URL-encoded and embedded in the path** (colons and slashes become `%3A` / `%2F`).
2. SPARQL queries are sent as the **POST body** with `content-type: application/sparql-query`, and the response is JSON when `Accept: application/sparql-results+json`.

Verify with curl first:

```bash
curl -u 'user@example.com:password' \
  -H 'Accept: application/sparql-results+json' \
  -H 'Content-Type: application/sparql-query' \
  --data-binary 'SELECT ?s WHERE { ?s a <http://example.com/Foo> } LIMIT 10' \
  'https://host/sparql/graphmart/<encoded-uri>'
```

If curl returns `200` and a JSON `results.bindings` array, you're ready to wire it into Mendix.

## SPARQL JSON result shape

Every SPARQL HTTP result looks like this:

```json
{
  "head": { "vars": ["customer", "customerId", "customerName"] },
  "results": {
    "bindings": [
      {
        "customer":     {"type": "uri",     "value": "http://.../Customer/0000000"},
        "customerId":   {"type": "literal", "value": "CUST001"},
        "customerName": {"type": "literal", "value": "Global Tech Solutions Inc."}
      }
    ]
  }
}
```

Each row in `bindings` is an object of `{var: {type, value}}`. A JSLT transformer flattens this to something directly mappable into Mendix entities.

## The full pipeline

```
┌────────────────────┐   ┌────────────────────┐   ┌────────────────────┐   ┌────────────────┐
│  Inline rest call  │─▶│ data transformer   │─▶│  import mapping    │─▶│ Mendix entity  │
│  post + basic auth │   │ jslt: flatten      │   │ json → entities    │   │ (persistent)   │
│  SPARQL as body    │   │ results.bindings   │   │                    │   │                │
└────────────────────┘   └────────────────────┘   └────────────────────┘   └────────────────┘
```

**Why inline `rest call` rather than `create consumed rest service` + `send rest request`?**

- At the time of writing, REST Client `authentication: basic (username: '...', password: '...')` silently fails to attach the `Authorization` header when the password contains special characters (e.g. `!`). Result: `401 Unauthorized`.
- Inline `rest call ... auth basic '<user>' password '<pass>'` handles the same credentials correctly.

**Why persistent entities for the final list?**

- Non-persistent `ReferenceSet` children can't be extracted as a `list` in MDL microflows (no documented `retrieve ... by association` syntax), and `loop $c in $Parent/Assoc` fails at build time.
- Persistent entities work with `datasource: database` on a DataGrid — the standard happy path.

## Step-by-step template

### 1. Persistent target entity

```sql
mdl 1;
@position(100, 100)
create persistent entity MyModule.Customer (
  CustomerUri:  string(500),
  CustomerId:   string(50),
  CustomerName: string(200)
);
```

### 2. Non-persistent wrapper (for the import mapping only)

Import mappings need a single root entity. A tiny non-persistent wrapper with one dummy attribute is enough:

```sql
mdl 1;
@position(400, 100)
create non-persistent entity MyModule.CustomerImport (
  DummyAttr: string(10)
);

create association MyModule.CustomerImport_Customer
  from MyModule.CustomerImport
  to   MyModule.Customer
  type ReferenceSet;
```

### 3. Data Transformer (JSLT) — flatten SPARQL response

Take the nested `results.bindings[].*.value` shape and emit a flat `customers[]` array:

```sql
mdl 1;
create data transformer MyModule.SimplifyCustomers
source json '{"head":{"vars":["customer","customerId","customerName"]},"results":{"bindings":[{"customer":{"type":"uri","value":"http://.../Customer/0"},"customerId":{"type":"literal","value":"CUST001"},"customerName":{"type":"literal","value":"Global Tech Solutions Inc."}}]}}'
{
  jslt $$
{
  "customers": [for (.results.bindings)
    {
      "customerUri":  .customer.value,
      "customerId":   .customerId.value,
      "customerName": .customerName.value
    }
  ]
}
  $$;
};
```

**JSLT notes for this runtime:**

- `[for (.path.to.array) <expr>]` works for iteration.
- `.field.subfield` path access works.
- `[N]` array indexing works.
- `$var[start : end]` slice works for strings — **do not use `substring(...)`** (it silently drops the field from the output).
- `let` variables and `if/else` expressions work.
- `def fn(arg) ...` helper functions work.

### 4. JSON structure + Import Mapping

The JSON structure represents the **transformed** shape (after JSLT), not the raw SPARQL response:

```sql
mdl 1;
create json structure MyModule.JSON_Customers
sample '{"customers":[{"customerUri":"http://example.com/Customer/0","customerId":"CUST001","customerName":"Global Tech Solutions Inc."}]}';

create import mapping MyModule.IMM_Customers
  with json structure MyModule.JSON_Customers
{
  create MyModule.CustomerImport {
    create MyModule.CustomerImport_Customer/MyModule.Customer = customers {
      CustomerUri  = customerUri,
      CustomerId   = customerId,
      CustomerName = customerName
    }
  }
};
```

### 5. Microflow — the actual API call

```sql
mdl 1;
create microflow MyModule.ACT_RefreshCustomers ()
returns boolean as $success
begin
  log info node 'MyModule' '=== Refresh start ===';

  -- Clear existing persistent records (full replace)
  retrieve $Existing from MyModule.Customer;
  loop $C in $Existing begin
    delete $C;
  end loop;

  -- Inline REST CALL — NOT the REST Client (see notes)
  $RawJson = call rest service post 'https://graphstudio.mendixdemo.com/sparql/graphmart/http%3A%2F%2Fcambridgesemantics.com%2FGraphmart%2F3617250aca6a40d88972c1c0de38f86a'
    header 'Accept'       = 'application/sparql-results+json'
    header 'Content-Type' = 'application/sparql-query'
    auth basic '<username>' password '<password>'
    body 'PREFIX model: <http://cambridgesemantics.com/SourceLayer/c4ce0eca2e7241f2aee13b46fbdca3f8/Model#> SELECT ?customer ?customerId ?customerName FROM <http://cambridgesemantics.com/SourceLayer/c4ce0eca2e7241f2aee13b46fbdca3f8/Model> WHERE {1} ?customer a model:ExamplePlmBom.Customer; model:ExamplePlmBom.Customer.id ?customerId; model:ExamplePlmBom.Customer.name ?customerName; {2}'
    with ({1} = '{', {2} = '}')
    timeout 60
    returns string
    on error continue;

  log info node 'MyModule' '{1}' with ({1} = 'HTTP status: ' + toString($latestHttpResponse/StatusCode));

  if $latestHttpResponse/StatusCode = 200 then
    $SimplifiedJson = transform $RawJson with MyModule.SimplifyCustomers;
    $ImportResult   = import from mapping MyModule.IMM_Customers($SimplifiedJson);
    log info node 'MyModule' '=== Done ===';
  end if;

  return true;
end;
```

### 6. Page

```sql
mdl 1;
create page MyModule.Customer_Overview (
  title:  'Customers (from Graph Mart)',
  layout: Atlas_Core.Atlas_Default
) {
  dynamictext heading (content: 'Customers', rendermode: H2)
  actionbutton btnRefresh (caption: 'Refresh', action: call microflow MyModule.ACT_RefreshCustomers, buttonstyle: primary)
  datagrid gridCustomers (datasource: database MyModule.Customer sort by CustomerId asc) {
    column   (attribute: CustomerId,   caption: 'ID')
    column (attribute: CustomerName, caption: 'Name')
    column  (attribute: CustomerUri,  caption: 'URI')
  }
};
```

## Gotchas (things that burned an hour during development)

### `!` in Basic Auth password → 401

REST Client `authentication: basic (...)` with a literal password containing `!` sends no auth header at runtime. Workaround: use inline `rest call ... auth basic '<user>' password '<pass>'`. The inline form works with the same literal credentials.

### SPARQL `{` braces in `body` templates are consumed as placeholder escapes

In `rest call ... body '...'`, the body is a template string where `{1}`, `{2}` are placeholders. A literal `{` must be escaped as `{{`, but in this runtime `{{` is sent **literally** rather than being converted to `{` → server returns `400 Bad request`.

**Solution:** pass literal braces as placeholder values:

```sql
body '... WHERE {1} ... {2}'
with ({1} = '{', {2} = '}')
```

### JSON structure auto-detects ISO strings as DateTime

If your JSLT emits ISO 8601 timestamps (`"2026-04-13T14:00"`) and the target Mendix attribute is `string`, `create json structure ... sample '...'` will infer `datetime` from the sample and mxbuild fails with `CE5015` ("schema type DateTime doesn't match attribute type String").

**Solutions:**
- Use a non-ISO sample value in the snippet (e.g. `"2026-04-13 14:00 CET"`).
- Or slice/format the timestamp in JSLT so it doesn't look like ISO 8601 (`$rawTime[11 : 16]` for `HH:MM`).
- Or change the target attribute to `datetime`.

### Non-persistent child lists can't be extracted in microflows

The import mapping happily populates `CustomerImport` with a `ReferenceSet` of `Customer` children, but:
- `return $Root/MyModule.CustomerImport_Customer` → "Error(s) in expression" at build
- `declare $C list of MyModule.Customer = $Root/...` → "Error(s) in expression"
- `loop $c in $Root/MyModule.CustomerImport_Customer` → "The 'Iterate over' property is required"
- DataGrid `datasource: $currentObject/MyModule.CustomerImport_Customer` → BSON serializer drops the datasource

**Solution:** Make the target entity **persistent**. The import mapping commits them automatically, and the page uses the standard `datasource: database MyModule.Customer` for the grid. A full replace on each refresh (delete-all-then-import) keeps data consistent with the graph.

### Rapid drop/create cycles on the same entity can corrupt the MPR

If you `drop entity X` then `create entity X` repeatedly while associations referencing `X` exist, the associations may hold the **old** entity GUID → mxbuild fails with `KeyNotFoundException`. Fix by dropping/recreating the broken association after the entity change.

## Exploring the graph

Before building the pipeline, explore the graph to understand what's there. Useful SPARQL queries (send via curl):

**List all classes with counts:**
```sparql
select distinct ?class (count(?s) as ?count)
from <http://.../model>
where { ?s a ?class }
GROUP by ?class
ORDER by desc(?count)
```

**List properties used by a given class:**
```sparql
PREFIX model: <http://.../model#>
select distinct ?property
from <http://.../model>
where {
  ?s a model:ExamplePlmBom.Customer ;
     ?property ?o .
}
ORDER by ?property
```

**Filter to a single namespace (skip rdf/owl noise):**
```sparql
select distinct ?class ?property
from <http://.../model>
where {
  ?s a ?class ;
     ?property ?o .
  filter(STRSTARTS(STR(?class), "http://.../model#MyPrefix"))
}
```

## Credential management

For demos, literal credentials inline in the microflow are the simplest and most reliable. For anything else, put them in a project constant and reference it as `@Module.ConstantName` — the one way MDL refers to a constant, in a microflow expression and in `create consumed rest service ... authentication: basic (username: @Module.User, password: @Module.Password)` alike. The older `$ConstantName` spelling in a REST credential still parses and warns MDL-DEPR083.

## Related skills

- [rest-client](../rest-client/SKILL.md) — REST Client + SEND REST REQUEST pattern (preferred when Basic Auth is not needed or uses simple passwords)
- [json-structures-and-mappings](../json-structures-and-mappings/SKILL.md) — JSON structure / import mapping details
- [rest-call-from-json](../rest-call-from-json/SKILL.md) — inline REST CALL + mapping pipeline
- [write-microflows](../write-microflows/SKILL.md) — microflow syntax reference
