---
name: debug-bson
description: "Diagnose BSON serialization problems in the MPR file — missing properties, wrong storage names, widget definitions Studio Pro rejects. Use when something created through MDL does not appear correctly in Studio Pro, or when a CE error points at a document mxcli wrote."
---

# BSON Serialization Debugging Skill

This skill provides guidance for debugging BSON serialization issues when implementing or fixing Mendix SDK writers.

## When to Use This Skill

Use this skill when:
- Objects created via MDL don't appear correctly in Studio Pro
- Properties are missing, empty, or showing default values
- Widget captions, parameters, or nested structures aren't stored correctly
- You need to compare SDK-generated BSON with Studio Pro-generated BSON
- You encounter "empty" or "(Empty caption)" issues in Studio Pro
- Debugging BSON array version markers or object structures

## Overview

When the ModelSDK Go serializes objects to BSON, the output must exactly match what Mendix Studio Pro expects. Even small differences in:
- Field names (e.g., `caption` vs `CaptionTemplate`)
- Object structures (e.g., string vs nested object)
- Array version markers (e.g., `[2, items...]` vs `[3, items...]`)

...can cause Studio Pro to ignore the data entirely.

## Part 1: The Debugging Workflow

### Step 1: Identify the Problem

Symptoms that indicate BSON serialization issues:
- MDL `describe` command shows correct data, but Studio Pro shows empty/default
- Object is created but properties don't persist
- Nested structures (templates, parameters) are missing
- "(Empty caption)" or similar placeholder text in Studio Pro

### Step 2: Create a Reference Object in Studio Pro

1. Open the MPR project in Mendix Studio Pro
2. Manually create or fix the problematic object
3. Save the project (this writes the correct BSON)
4. Note the exact name/path of the fixed object

### Step 3: Dump Both BSON Structures

Use the `mxcli bson dump` command to extract and compare:

```bash
# Dump the SDK-generated object (the broken one)
mxcli bson dump -p app.mpr -o "PgTest.BrokenPage" > broken.json

# Dump the Studio Pro-generated object (the fixed one)
mxcli bson dump -p app.mpr -o "PgTest.FixedPage" > fixed.json

# Compare the two
diff broken.json fixed.json
```

Or use the `--compare` flag:
```bash
mxcli bson dump -p app.mpr --compare "PgTest.BrokenPage,PgTest.FixedPage"
```

### Step 4: Identify Differences

Look for differences in:

| Area | Common Issues |
|------|---------------|
| Field names | `caption` vs `CaptionTemplate`, `Name` vs `InternalName` |
| Object vs value | String `""` vs nested `{$type: "..."}` object |
| Array markers | `[2, ...]` vs `[3, ...]` for different contexts |
| Missing fields | Required fields that SDK omits |
| Type mismatches | `int32` vs `int64`, `string` vs `binary` |

### Step 5: Fix the Serialization Code

The serialization code lives in `mdl/backend/modelsdk/*_write.go`:
- `widget_write.go` - Page widget serialization
- `page_write.go` - Page document (header, parameters, layout call)
- `microflow_write.go` - Microflow activity serialization
- `domainmodel_write.go` - Entity/attribute serialization

The encoder and decoder underneath them are `modelsdk/codec/encoder.go` and
`modelsdk/codec/decoder.go`.

## Part 2: Common BSON Patterns

### Array Version Markers

Mendix uses version markers at the start of arrays:

```go
// empty array (version 3 marker)
bson.A{int32(3)}

// non-empty array - context dependent!
// parameters arrays use version 2
bson.A{int32(2), item1, item2, ...}

// Texts$Text.Items arrays use version 3
bson.A{int32(3), item1, item2, ...}
```

**Critical**: The version marker differs by context. Always check a working Studio Pro example.

### Object Structures

Some fields expect nested objects, not simple values:

```go
// WRONG: string value
{key: "FallbackValue", value: ""}

// CORRECT: Nested Texts$text object
{key: "Fallback", value: bson.D{
    {key: "$ID", value: idToBsonBinary(generateUUID())},
    {key: "$type", value: "Texts$text"},
    {key: "Items", value: bson.A{int32(3)}},
}}
```

### Field Naming

Always use exact field names from Studio Pro:

```go
// WRONG: Simplified name
{key: "caption", value: caption}

// CORRECT: full field name
{key: "CaptionTemplate", value: caption}
```

## Part 3: Key Structures Reference

### Forms$ClientTemplate

Used for templated text like button captions with parameters:

```go
func serializeClientTemplate(ct *pages.ClientTemplate) bson.D {
    captionID := ct.ID
    if captionID == "" {
        captionID = generateUUID()
    }

    // build template text
    template := bson.D{
        {key: "$ID", value: idToBsonBinary(generateUUID())},
        {key: "$type", value: "Texts$text"},
        {key: "Items", value: bson.A{int32(3), /* TextItem objects */}},
    }

    // build fallback (required, even if empty)
    fallback := bson.D{
        {key: "$ID", value: idToBsonBinary(generateUUID())},
        {key: "$type", value: "Texts$text"},
        {key: "Items", value: bson.A{int32(3)}}, // empty fallback
    }

    // build parameters array
    params := bson.A{int32(3)} // empty by default
    if len(ct.Parameters) > 0 {
        params = bson.A{int32(2)} // non-empty uses version 2!
        for _, param := range ct.Parameters {
            params = append(params, serializeClientTemplateParameter(param))
        }
    }

    return bson.D{
        {key: "$ID", value: idToBsonBinary(captionID)},
        {key: "$type", value: "Forms$ClientTemplate"},
        {key: "Fallback", value: fallback},    // Must be object, not string
        {key: "parameters", value: params},
        {key: "template", value: template},
    }
}
```

### ActionButton CaptionTemplate

```go
// in serializeActionButton:
{key: "CaptionTemplate", value: caption}, // not "caption"!
```

## Part 4: Debugging Tools

### Dumping Raw BSON

`mxcli bson dump` reads the raw unit and prints it as JSON — no Go program needed:

```bash
# what is in there
mxcli bson dump -p app.mpr --type page --list

# one object
mxcli bson dump -p app.mpr --type page --object "MyModule.MyPage"

# the comparison that actually finds the bug: Studio Pro's vs mxcli's
mxcli bson dump -p app.mpr --type page --compare "MyModule.Broken,MyModule.Working"

# a byte-exact baseline to diff against later
mxcli bson dump -p app.mpr --type page --object "MyModule.MyPage" --format bson > baseline.mxunit
```

`--type` also takes `microflow`, `nanoflow`, `enumeration`, `snippet`, `layout`
and `constant`.
# list all pages in project
mxcli bson dump -p app.mpr --type page --list

# list all microflows
mxcli bson dump -p app.mpr --type microflow --list

# Dump specific page as json
mxcli bson dump -p app.mpr --type page --object "PgTest.MyPage"

# Save dump to file for comparison
mxcli bson dump -p app.mpr --type page --object "PgTest.MyPage" > mypage.json

# Compare two objects (outputs both as json)
mxcli bson dump -p app.mpr --type page --compare "PgTest.Broken,PgTest.Fixed"

# Supported types: page, microflow, nanoflow, enumeration, snippet, layout
```

## Part 5: Checklist for BSON Fixes

Before considering a fix complete:

- [ ] Create reference object manually in Studio Pro
- [ ] Dump both BSON structures (SDK vs Studio Pro)
- [ ] Identify all differences
- [ ] Fix field names to match Studio Pro exactly
- [ ] Fix object structures (nested vs value)
- [ ] Fix array version markers
- [ ] Test: Create object via MDL, verify in Studio Pro
- [ ] Update documentation (`docs/05-mdl-specification/10-bson-mapping.md`)

## Part 6: Common Issues and Solutions

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| "(Empty caption)" in Studio Pro | Wrong field name or structure | Check `CaptionTemplate` vs `caption`, verify nested object |
| Parameters not showing | Wrong array version marker | Use `[2, ...]` for non-empty Parameters |
| Template text missing | Missing Texts$Text structure | Ensure proper TextItem serialization |
| Fallback empty | Using string instead of object | Use `Fallback` with Texts$Text object |
| Widget property ignored | Field name mismatch | Compare with Studio Pro BSON exactly |
| Columns not in Page Explorer | Incomplete nested WidgetObjects | Create ALL properties from template |
| TypeCacheUnknownTypeException | Wrong BSON $Type name | Use `Texts$Translation` not `Texts$TextItem` |
| CE0642 "Property is required" | Wrong value format or missing | Check ValueType.Type in template, use correct BSON field |
| NullReferenceException in GetExpectedExpressionType | Using Expression for non-Expression type | Use `PrimitiveValue` for Boolean/Enum/Integer types |
| CE0495 Duplicate name errors | Same widget in multiple properties | Set content/filter to empty widget arrays |

## Part 7: Nested WidgetObjects (Critical)

**Key Insight**: Pluggable widgets with nested objects (like DataGrid2 columns) require **ALL properties** to be created, not just the ones with explicit values.

### The Problem

When creating nested `WidgetObject` instances (e.g., DataGrid2 columns), creating only the properties with explicit values results in:
- Objects that don't appear in the Page Explorer
- CE0463 "widget definition has changed" errors
- Widgets that render in the editor but are incomplete

### Example: DataGrid2 Columns

**Symptom**: Columns show in the page editor but NOT in the Page Explorer tree.

**Cause**: Column objects have 5 properties instead of the required 21.

```bash
# Compare mxcli-generated vs Studio Pro-generated
mxcli bson dump -p app.mpr --compare "PgTest.MDLPage,PgTest.StudioProPage"

# Look for property count differences:
# ~ properties: array length differs (first: 5, second: 22)
```

**Solution**: The embedded templates at `sdk/widgets/templates/mendix-11.6/datagrid.json` contain all 21 column properties:

```
showContentAs, attribute, content, dynamictext, exportValue, header, tooltip,
filter, visible, sortable, resizable, draggable, hidable, allowEventPropagation,
width, minWidth, minWidthLimit, size, alignment, columnClass, wrapText
```

When building columns, iterate through ALL `PropertyTypes` in the template's `ObjectType` and create a `WidgetProperty` for each one, using default values for properties without explicit values.

### Diagnostic Steps

1. Count properties in both versions:
   ```bash
   mxcli bson dump -p app.mpr --type page --object "PgTest.BrokenPage" | grep "WidgetProperty" | wc -l
   mxcli bson dump -p app.mpr --type page --object "PgTest.FixedPage" | grep "WidgetProperty" | wc -l
   ```

2. Check the template for required properties:
   ```bash
   grep '"PropertyKey"' sdk/widgets/templates/mendix-11.6/datagrid.json | head -30
   ```

3. Compare specific nested objects using `--compare` flag to find property count mismatches.

## Part 8: Property Value Types (Critical)

**Key Insight**: Pluggable widget properties require different value formats based on their `ValueType.Type` field in the widget template. Using the wrong format causes CE0642 "Property is required" errors or NullReferenceException.

### Determining the Correct Format

Check the `ValueType.Type` field in the widget template JSON:

```json
{
  "PropertyKey": "visible",
  "ValueType": {
    "type": "expression",
    "ReturnType": "boolean"
  }
}
```

### Value Format by Type

| ValueType.Type | BSON Field | Example Value | Notes |
|----------------|------------|---------------|-------|
| `expression` | `expression` | `"true"`, `"$currentObject/Name"` | String expression, NOT evaluated |
| `boolean` | `PrimitiveValue` | `"true"`, `"false"` | String representation |
| `enumeration` | `PrimitiveValue` | `"left"`, `"autofill"` | Enum value name |
| `integer` | `PrimitiveValue` | `"100"`, `"0"` | String representation |
| `decimal` | `PrimitiveValue` | `"10.5"` | String representation |
| `string` | `PrimitiveValue` | `"text value"` | Direct string |
| `widgets` | `widgets` | `bson.A{...}` | Array of widget objects |
| `object` | `objects` | `bson.A{...}` | Array of WidgetObject |

### Example: DataGrid2 Column Properties

```go
// WRONG: Using expression for boolean-type property
// Causes: NullReferenceException in GetExpectedExpressionType
{key: "sortable", value: bson.D{
    {key: "expression", value: "true"},  // WRONG!
}}

// CORRECT: Using PrimitiveValue for boolean-type property
{key: "sortable", value: bson.D{
    {key: "PrimitiveValue", value: "true"},  // Correct!
}}
```

### DataGrid2 Column Property Types Reference

| Property | ValueType.Type | BSON Field | Default Value |
|----------|---------------|------------|---------------|
| `visible` | Expression | `expression` | `"true"` |
| `sortable` | Boolean | `PrimitiveValue` | `"true"` |
| `resizable` | Boolean | `PrimitiveValue` | `"true"` |
| `draggable` | Boolean | `PrimitiveValue` | `"true"` |
| `wrapText` | Boolean | `PrimitiveValue` | `"false"` |
| `hidable` | Enumeration | `PrimitiveValue` | `"yes"` |
| `alignment` | Enumeration | `PrimitiveValue` | `"left"` |
| `width` | Enumeration | `PrimitiveValue` | `"autofill"` |
| `minWidth` | Enumeration | `PrimitiveValue` | `"auto"` |
| `size` | Integer | `PrimitiveValue` | `"100"` |
| `header` | Object | `objects` | Empty translation |
| `content` | Widgets | `widgets` | Empty widget array |
| `filter` | Widgets | `widgets` | Empty widget array |

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| CE0642 "Property 'X' is required" | Missing property or wrong value format | Check ValueType.Type, use correct BSON field |
| NullReferenceException in GetExpectedExpressionType | Using `expression` for non-Expression type | Use `PrimitiveValue` for Boolean/Enum/Integer |
| CE0463 "widget definition has changed" | Missing properties | Create ALL properties from template |

### How to Find ValueType.Type

```bash
# check the embedded widget template
grep -A5 '"PropertyKey": "visible"' sdk/widgets/templates/mendix-11.6/datagrid.json

# or use jq to extract all property types
jq '.PropertyTypes[] | {key: .PropertyKey, type: .ValueType.Type}' sdk/widgets/templates/mendix-11.6/datagrid.json
```

## Part 9: Texts$Translation vs Texts$TextItem

**Critical**: The correct type for translatable text items is `Texts$Translation`, NOT `Texts$TextItem`.

### The Error

```
TypeCacheUnknownTypeException: The type cache does not contain a type with qualified name Texts$TextItem
```

### Correct Structure

```go
// WRONG: Texts$TextItem does not exist
{key: "$type", value: "Texts$TextItem"}

// CORRECT: use Texts$Translation with LanguageCode
{key: "$type", value: "Texts$Translation"},
{key: "LanguageCode", value: "en_US"},
{key: "text", value: "Your text here"},
```

### Full Example: Building a Header Translation

```go
headerTranslation := bson.D{
    {key: "$ID", value: idToBsonBinary(generateUUID())},
    {key: "$type", value: "Texts$Translation"},
    {key: "LanguageCode", value: "en_US"},
    {key: "text", value: columnHeader},
}

headerText := bson.D{
    {key: "$ID", value: idToBsonBinary(generateUUID())},
    {key: "$type", value: "Texts$text"},
    {key: "Items", value: bson.A{int32(3), headerTranslation}},
}
```

## Part 10: CE0463 TextTemplate Troubleshooting

**CE0463 "widget definition has changed"** is one of the most common errors when creating pluggable widgets programmatically. For filter widgets, this error is often caused by TextTemplate properties being `null` instead of proper `Forms$ClientTemplate` structures.

### Identifying TextTemplate Properties

1. **Check the Type section** for properties with `"type": "TextTemplate"`:
   ```json
   {
     "PropertyKey": "placeholder",
     "ValueType": {
       "$ID": "abc123...",
       "$type": "CustomWidgets$WidgetValueType",
       "type": "TextTemplate"  // <-- This is a TextTemplate property
     }
   }
   ```

2. **Find the matching Object property** using the TypePointer:
   ```json
   {
     "TypePointer": "abc123...",  // Matches ValueType.$ID above
     "value": {
       "TextTemplate": null  // <-- WRONG! Causes CE0463
     }
   }
   ```

### Required TextTemplate Structure

Every TextTemplate property must have this structure (never null):

```json
"TextTemplate": {
  "$ID": "<32-char-guid>",
  "$type": "Forms$ClientTemplate",
  "Fallback": {
    "$ID": "<32-char-guid>",
    "$type": "Texts$text",
    "Items": []
  },
  "parameters": [],
  "template": {
    "$ID": "<32-char-guid>",
    "$type": "Texts$text",
    "Items": []
  }
}
```

### Critical: Empty Array Serialization

**WRONG** - `[2]` in JSON serializes as an array containing the integer 2:
```json
"Items": [2]      // Creates array with one element: the number 2
"parameters": [2] // Creates array with one element: the number 2
```

**CORRECT** - Use truly empty arrays:
```json
"Items": []       // Truly empty array
"parameters": []  // Truly empty array
```

The version markers (like `[2]` or `[3]`) only exist in BSON wire format, not in JSON template files.

### Affected Filter Widgets

| Widget | TextTemplate Properties |
|--------|------------------------|
| TextFilter | `placeholder`, `screenReaderButtonCaption`, `screenReaderInputCaption` |
| DateFilter | `placeholder`, `screenReaderButtonCaption`, `screenReaderCalendarCaption`, `screenReaderInputCaption` |
| DropdownFilter | `emptyOptionCaption`, `ariaLabel`, `emptySelectionCaption`, `filterInputPlaceholderCaption` |
| NumberFilter | `placeholder`, `screenReaderButtonCaption`, `screenReaderInputCaption` |

### Python Script to Find TextTemplate Properties

Use this script to identify which Object properties need TextTemplate structures:

```python
import json

with open('widget-template.json') as f:
    data = json.load(f)

# Extract ValueType IDs for TextTemplate properties
text_template_ids = {}
for prop_type in data['type']['ObjectType']['PropertyTypes']:
    vt = prop_type.get('ValueType', {})
    if vt.get('Type') == 'TextTemplate':
        text_template_ids[vt['$ID']] = prop_type['PropertyKey']

print("TextTemplate properties:", text_template_ids)

# find matching object properties with null TextTemplate
for prop in data['object']['Properties']:
    type_ptr = prop['Value'].get('TypePointer')
    if type_ptr in text_template_ids:
        text_template = prop['Value'].get('TextTemplate')
        if text_template is none:
            print(f"NEEDS FIX: {text_template_ids[type_ptr]} (TypePointer: {type_ptr})")
```

### Verification Steps

After fixing templates:

1. Create a test page with the widget
2. Run `mx check app.mpr` - should return 0 errors
3. Open in Studio Pro - widget should load without "Update widget" prompt

### Reading TextTemplate in executor code

Part 10 above covers writing `Forms$ClientTemplate`. The same structure applies when **reading** it in executor code (e.g. `cmd_alter_page.go`, `cmd_pages_describe_output.go`).

The correct traversal is:
```
TextTemplate (Forms$ClientTemplate) → Template (Texts$Text) → Items[] → Translation { Text }
```

**Do not** read `Items` directly off the `TextTemplate` document — that skips the intermediate `Template` node and silently returns an empty slice. Always traverse one level deeper:

```go
// WRONG — Items is always empty
items := dGetArrayElements(dGet(tmplDoc, "Items"))

// CORRECT — traverse Template first
template := dGetDoc(tmplDoc, "Template")
items := dGetArrayElements(dGet(template, "Items"))
```

This applies to any executor function that reads column headers, button captions, or any other translatable text stored as `Forms$ClientTemplate`.

## Related Documentation

- [BSON Mapping Specification](../../docs/05-mdl-specification/10-bson-mapping.md)
- [Page Widget Serialization](../../mdl/backend/modelsdk/widget_write.go)
- [Create Page Skill](../create-page/SKILL.md)
- [Widget Templates README](../../sdk/widgets/templates/README.md)

## Quick Reference

### Debugging Command Sequence

```bash
# 1. find the broken object
mxcli -p app.mpr -c "describe page PgTest.BrokenPage"

# 2. create fixed version in Studio Pro, save project

# 3. Dump both objects to json files
mxcli bson dump -p app.mpr --type page --object "PgTest.BrokenPage" > broken.json
mxcli bson dump -p app.mpr --type page --object "PgTest.FixedPage" > fixed.json

# 4. Compare the json files
diff broken.json fixed.json
# or use a visual diff tool like VS Code:
code --diff broken.json fixed.json

# 5. after fixing code, verify
go build ./... && mxcli exec test.mdl -p app.mpr

# 6. Verify in Studio Pro (open project, check object)
```

### Key File Locations

| File | Purpose |
|------|---------|
| `mdl/backend/modelsdk/widget_write.go` | Page widget BSON serialization |
| `mdl/backend/modelsdk/microflow_write.go` | Microflow BSON serialization |
| `mdl/backend/modelsdk/domainmodel_write.go` | Entity BSON serialization |
| `modelsdk/codec/encoder.go` | Document → BSON |
| `modelsdk/codec/decoder.go` | BSON → document |
| `docs/05-mdl-specification/10-bson-mapping.md` | BSON format documentation |
