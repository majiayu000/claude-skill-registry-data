---
name: rest-call-from-json
description: "Generate the whole integration stack from a JSON payload: JSON structure, non-persistent entities, import mapping, and the REST CALL microflow. Use when starting from an example response and needing everything between it and a working microflow."
---

# REST Call from JSON Payload — End-to-End Skill

Use this skill to generate the full stack of Mendix integration artifacts from a JSON payload:
JSON Structure → Non-persistent entities → Import Mapping → microflow.

> **Two approaches**: This skill uses the **inline REST CALL** approach (good for one-off calls
> and quick prototyping). For structured APIs with reusable operations, use the **REST Client**
> approach instead — see [rest-client](../rest-client/SKILL.md) for `create consumed rest service` + `send rest request`
> + optional `transform` with JSLT data transformers.

## Overview — Four Steps

1. **CREATE JSON STRUCTURE** — store the raw payload and derive the element tree
2. **CREATE ENTITY** (non-persistent) — one per JSON object type, with attributes per JSON field
3. **CREATE IMPORT MAPPING** — link JSON structure elements to entities and attributes
4. **CREATE MICROFLOW** — inline REST CALL that invokes the import mapping (or use REST Client + SEND REST REQUEST)

---

## Step 1 — JSON Structure

```sql
mdl 1;
create json structure Module.JSON_MyStructure
  sample '{"key": "value", "count": 1}';
```

- The executor **formats** the snippet (pretty-print) then **refreshes** (derives element tree) automatically.
- The snippet must be valid JSON; use single quotes around it in MDL.
- Escape single quotes inside the snippet by doubling them: `''`.
- The derived element tree must stay consistent with the snippet — the executor sorts JSON object keys alphabetically to match `json.MarshalIndent` output.

**Verify** after creation:
```sql
describe json structure Module.JSON_MyStructure;
-- Should show: element tree under "-- Element tree:" comment
```

---

## Step 2 — Non-Persistent Entities

Derive one entity per JSON object type. Name them after what they represent (not after JSON keys).

```sql
mdl 1;
create non-persistent entity Module.MyRootObject (
  stringField   : string,
  intField      : integer,
  decimalField  : decimal,
  boolField     : boolean default false
);

create non-persistent entity Module.MyNestedObject (
  name : string,
  code : string
);

create association Module.MyRootObject_MyNestedObject
  from Module.MyRootObject
  to Module.MyNestedObject;
```

**Rules:**
- All string fields: bare `string` (no length — unlimited)
- All number fields: `integer`, `decimal`, or `long` — remove defaults for optional fields
- Boolean fields **require** `default true|false`
- `non-persistent` — these entities are not stored in the database. The keyword is
  **hyphenated and goes before `entity`**: `create non-persistent entity Mod.X (...)`.
  `NON_PERSISTENT`, and a `(NON_PERSISTENT)` inside the body, are both parse errors
- One association per parent→child relationship; name it `Parent_Child`

---

## Step 3 — Import Mapping

> **Full reference**: See [json-structures-and-mappings](../json-structures-and-mappings/SKILL.md) for complete import/export mapping syntax, domain model patterns, and common mistakes.

```sql
mdl 1;
create import mapping Module.IMM_MyMapping
  with json structure Module.JSON_MyStructure
{
  create Module.MyRootObject {
    stringField = stringField,
    intField    = intField,
    create Module.MyRootObject_MyNestedObject/Module.MyNestedObject = nestedKey {
      name = name,
      code = code
    }
  }
};
```

**Syntax rules:**
- Root object: `create Module.Entity { ... }` — always starts with handling keyword
- Value mappings: `attributename = jsonFieldName` — entity attribute on the left, JSON field on the right
- Nested objects: `create association/entity = jsonKey { ... }` — association path + JSON key
- Object handling: `create` (default), `find` (requires KEY), `find or create`
- KEY marker: `attr = jsonField key` — marks the attribute as a matching key
- Value transforms: `attr = Module.Microflow(jsonField)` — call a microflow to transform the value

**Verify** after creation — check Schema elements are ticked in Studio Pro:
- Open the import mapping in Studio Pro
- All JSON structure elements should appear ticked in the Schema elements panel
- If not ticked: JsonPath mismatch between import mapping and JSON structure elements

---

## Step 4 — REST CALL Microflow

Place the microflow in the `[pages]/Operations/` folder or `Private/` depending on whether it is public.

```sql
create microflow Module.GET_MyData ()
begin
  @position(-5, 200)
  declare $baseUrl string = 'https://api.example.com';
  @position(185, 200)
  declare $endpoint string = $baseUrl + '/path';
  @position(375, 200)
  $Result = call rest service get '{1}' with ({1} = $endpoint)
    header 'Accept' = 'application/json'
    timeout 300
    returns mapping Module.IMM_MyMapping as Module.MyRootObject on error rollback;
  @position(565, 200)
  log info node 'Integration' 'Retrieved result' with ();
end;
/
```

**Key points:**
- `@position` annotations control the canvas layout — StartEvent is auto-placed 150px to the left of the first annotated activity
- The output variable name is **automatically derived** from the entity name in `as Module.MyEntity` — do NOT hardcode it on the left side; the executor overrides it
- Single vs list result is **automatically detected**: if the JSON structure's root element is an Object, the variable type is `ObjectType` (single); if Array, `ListType` (list)
- `on error rollback` — standard error handling for integration calls

**For list responses** (JSON root is an array):
```sql
  $Results = call rest service get '{1}' with ({1} = $endpoint)
    header 'Accept' = 'application/json'
    timeout 300
    returns mapping Module.IMM_MyMapping as Module.MyItem on error rollback;
  @position(565, 200)
  $count = count $MyItem;
```

---

## Step 5 — Import/Export Mapping in Microflows (Optional)

Instead of using `returns mapping` on a REST CALL, you can use standalone import/export mapping actions. This is useful when you already have a JSON string and want to map it to entities, or when you want to serialize entities back to JSON.

### Import from mapping

Applies an import mapping to a string variable (JSON content) to produce entity objects:

```sql
-- With assignment (non-persistent entities, need the result in the flow)
$PetResponse = import from mapping Module.IMM_Pet($JsonContent);

-- Without assignment (persistent entities, just stores to DB)
import from mapping Module.IMM_Pet($JsonContent);
```

### Export to mapping

Applies an export mapping to an entity object to produce a JSON string:

```sql
$JsonOutput = export to mapping Module.EMM_Pet($PetResponse);
```

### Complete import → process → export microflow

```sql
mdl 1;
create microflow Module.ProcessPetData ()
begin
  declare $ResponseContent string = $latestHttpResponse/content;
  $PetResponse = import from mapping Module.IMM_Pet($ResponseContent);
  -- Process the imported data...
  $JsonOutput = export to mapping Module.EMM_Pet($PetResponse);
  log info node 'Integration' 'Exported: ' + $JsonOutput;
end;
```

---

## Step 6 — Sending a Request Body (Optional)

Everything above receives data. To send it, an inline `REST CALL` takes one of
four body forms:

```sql
-- 1. String template with placeholders
body '{{"name": "{1}", "qty": {2}}' with ({1} = $Name, {2} = toString($Qty))

-- 2. An expression that already yields the payload
body $JsonPayload

-- 3. An export mapping (entity -> JSON)
body mapping Module.EMM_Item from $Item

-- 4. Raw bytes — a file document's CONTENTS member
body binary $Doc/Contents
```

### Uploading a file

The expression is the file document's `Contents` **member**, not the document,
and the content type goes on a header — the body clause carries only the bytes:

```sql
mdl 1;
create or modify microflow Module.POST_Document_Upload (
  $Doc: Module.UploadedFile
)
returns boolean as $Ok
begin
  declare $Ok boolean = false;
  $Response = call rest service post 'https://api.example.com/documents'
    header 'ContentType' = 'application/pdf'
    body binary $Doc/Contents
    timeout 300
    returns response;
  set $Ok = $Response/StatusCode = 200;
  return $Ok;
end;
```

`$Doc` must be a specialization of `System.FileDocument`. Downloading is the
mirror image — `returns Module.UploadedFile` stores the response body in a new
file document.

**A consumed REST CLIENT document cannot do this.** Its body is one of
`Rest$JsonBody`, `Rest$StringBody` or `Rest$ImplicitMappingBody` — all textual —
so `Body: file from $Doc` in a `create consumed rest service` operation is refused as
**MDL-REST02**. Binary uploads belong in a microflow. (`Response: file as $Doc`
on an operation is fine; downloads work either way.)

---

## Complete Example — Bible Verse API

```sql
-- Step 1: JSON Structure
create json structure Integrations.JSON_BibleVerse
  sample '{"translation":{"identifier":"web","name":"World English Bible","language":"English","language_code":"eng","license":"Public Domain"},"random_verse":{"book_id":"1SA","book":"1 Samuel","chapter":17,"verse":49,"text":"David put his hand in his bag, took a stone, and slung it."}}';

-- Step 2: Entities
create non-persistent entity Integrations.BibleApiResponse ();

create non-persistent entity Integrations.BibleTranslation (
  identifier    : string,
  name          : string,
  language      : string,
  language_code : string,
  license       : string
);

create non-persistent entity Integrations.BibleVerse (
  book_id : string,
  book    : string,
  chapter : integer,
  verse   : integer,
  text    : string
);

create association Integrations.BibleApiResponse_BibleTranslation
  from Integrations.BibleApiResponse
  to Integrations.BibleTranslation;

create association Integrations.BibleApiResponse_BibleVerse
  from Integrations.BibleApiResponse
  to Integrations.BibleVerse;

-- Step 3: Import Mapping
create import mapping Integrations.IMM_BibleVerse
  with json structure Integrations.JSON_BibleVerse
{
  create Integrations.BibleApiResponse {
    create Integrations.BibleApiResponse_BibleTranslation/Integrations.BibleTranslation = translation {
      identifier    = identifier,
      language      = language,
      language_code = language_code,
      license       = license,
      name          = name
    },
    create Integrations.BibleApiResponse_BibleVerse/Integrations.BibleVerse = random_verse {
      book    = book,
      book_id = book_id,
      chapter = chapter,
      text    = text,
      verse   = verse
    }
  }
};

-- Step 4: Microflow
create microflow Integrations.GET_BibleVerse_Random ()
begin
  @position(-5, 200)
  declare $baseUrl string = 'https://bible-api.com';
  @position(185, 200)
  declare $endpoint string = $baseUrl + '/data/web/random';
  @position(375, 200)
  $Result = call rest service get '{1}' with ({1} = $endpoint)
    header 'Accept' = 'application/json'
    timeout 300
    returns mapping Integrations.IMM_BibleVerse as Integrations.BibleApiResponse on error rollback;
  @position(565, 200)
  log info node 'Integration' 'Retrieved Bible verse' with ();
end;
/
```

---

## Gotchas and Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| Studio Pro "not consistent with snippet" | JSON element tree keys not in alphabetical order | Executor sorts keys; re-derive from snippet |
| Schema elements not ticked in import mapping | JsonPath mismatch | Named object elements use `(object)\|key`, NOT `(object)\|key\|(object)` |
| Import mapping not linked in REST call | Wrong BSON field name | Use `ReturnValueMapping`, not `mapping` |
| Studio Pro shows "List of X" but mapping returns single X | `ForceSingleOccurrence` not set | Executor auto-detects from JSON structure root element type |
| StartEvent behind first activities | Default posX=200 vs @position(-5,...) | Fixed: executor pre-scans for first @position and shifts StartEvent left |
| `TypeCacheUnknownTypeException` | Wrong BSON `$type` names | `ImportMappings$ObjectMappingElement` / `ImportMappings$ValueMappingElement` (no `import` prefix) |
| Attribute not found in Studio Pro | Attribute not fully qualified | Must be `Module.Entity.AttributeName` in the BSON |
| `CE0117 "Error(s) in expression."` at the end event after a REST call | `returns response` binds a `System.HttpResponse`, so returning it from a `returns string` microflow is a type error | Match the microflow's return type to what you do with the response — e.g. `returns boolean` and `set $Ok = $Response/StatusCode = 200` |
| Upload returns HTTP 200 but the server received a few bytes | `Body: file from $Doc` on a REST CLIENT document used to be written as the literal text `$Doc` | Now refused as MDL-REST02 — upload from a microflow with `body binary $Doc/Contents` |

---

## Naming Conventions (MES)

| Artifact | Pattern | Example |
|----------|---------|---------|
| JSON Structure | `JSON_<ApiName>` | `JSON_BibleVerse` |
| Import Mapping | `IMM_<ApiName>` | `IMM_BibleVerse` |
| Root entity | Describes the API response | `BibleApiResponse` |
| Nested entities | Describes the domain concept | `BibleVerse`, `BibleTranslation` |
| Microflow | `METHOD_Resource_Operation` | `GET_BibleVerse_Random` |
| Folder | `Private/` for mappings/structures, `Operations/` for public microflows | — |
