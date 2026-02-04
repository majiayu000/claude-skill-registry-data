---
name: transform
description: Convert data between formats, schemas, or representations with explicit loss accounting and validation. Use when reformatting data, mapping between schemas, normalizing inputs, or translating structures.
argument-hint: "[source] [target_schema] [mapping]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: prompt
          prompt: |
            TRANSFORM SOURCE VALIDATION

            Reading file for transformation: {{tool_input.file_path}}

            Before transforming data, verify:
            1. Source file exists and is readable
            2. Source format is understood (JSON, YAML, CSV, etc.)
            3. Data does not contain sensitive information that would be exposed by transformation
            4. Transformation will be logged for audit

            If source contains sensitive data:
            - Ensure output will be appropriately redacted
            - Flag for additional review if PII detected

            Reply ALLOW to proceed with reading source.
            Reply BLOCK if source appears to contain unprotected sensitive data.
          once: true
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: |
            echo "[TRANSFORM] $(date -u +%Y-%m-%dT%H:%M:%SZ) | Source: {{tool_input.file_path}} | Read for transformation" >> .audit/transform-operations.log 2>/dev/null || true
---

## Intent

Transform data from one format or schema to another while tracking what information is preserved, modified, or lost during conversion. Ensure output conforms to target schema with full provenance.

**Success criteria:**
- Output conforms to target schema
- All fields mapped correctly or explicitly marked as lost
- Transformation is deterministic and reproducible
- Loss/distortion explicitly documented
- Evidence anchors trace source to output

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `source` | Yes | string or object | Input data to transform |
| `target_schema` | Yes | string or object | Schema or format specification for output |
| `mapping` | No | object | Explicit field mappings (source -> target) |
| `preserve_unknown` | No | boolean | Keep fields not in mapping (default: false) |
| `strict` | No | boolean | Fail on any mapping ambiguity (default: false) |
| `default_values` | No | object | Defaults for missing required fields |

## Procedure

1) **Parse source data**: Load and validate input
   - Identify source format (JSON, YAML, XML, CSV, etc.)
   - Parse into internal representation
   - Detect encoding and special characters
   - Record source structure for provenance

2) **Analyze target schema**: Understand destination requirements
   - Load target schema specification
   - Identify required vs optional fields
   - Note type constraints and validations
   - Map nested structures

3) **Build transformation map**: Match source to target
   - Apply explicit mappings if provided
   - Infer mappings for matching field names
   - Identify fields requiring type conversion
   - Flag unmappable source fields

4) **Execute transformation**: Apply mappings
   - Transform each field according to mapping
   - Apply type conversions (string to number, etc.)
   - Handle nested objects recursively
   - Apply default values for missing required fields

5) **Track losses**: Document what was not preserved
   - List source fields not in output
   - Note precision losses in numeric conversions
   - Record truncations or format changes
   - Document semantic changes

6) **Validate output**: Confirm target schema conformance
   - Check all required fields present
   - Validate types match schema
   - Run any schema-defined constraints
   - Verify structural integrity

7) **Ground output**: Attach provenance
   - Link output fields to source locations
   - Document transformation rules applied
   - Record validation results

## Output Contract

Return a structured object:

```yaml
transformed:
  input_type: string  # Format of source data
  output_type: string  # Format of output data
  content: object  # Transformed data
  mapping_applied: string  # Reference to mapping specification
validation:
  input_valid: boolean  # Was source valid?
  output_valid: boolean  # Does output match target schema?
  schema_ref: string  # Target schema reference
  errors: array[string]  # Validation errors if any
losses:
  - field: string  # Source field that was lost
    reason: string  # Why it was not preserved
    severity: info | warning | error  # Impact level
conversions:
  - source_field: string
    target_field: string
    conversion: string  # What transformation was applied
    reversible: boolean  # Can be converted back?
confidence: 0..1  # Confidence in transformation correctness
evidence_anchors: ["source:field", "schema:rule"]
assumptions: []  # Explicit assumptions
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `transformed` | object | Result of transformation |
| `validation` | object | Input and output validation results |
| `losses` | array | Fields or data not preserved |
| `conversions` | array | Type/format conversions applied |
| `confidence` | number | 0.0-1.0 based on mapping completeness |
| `evidence_anchors` | array | Source references and schema rules |
| `assumptions` | array | Assumptions made during transformation |

## Examples

### Example 1: JSON to YAML with Schema Validation

**Input:**
```yaml
source:
  user_id: 12345
  user_name: "john_doe"
  email_address: "john@example.com"
  created_timestamp: 1705312800
  metadata:
    source: "api"
    version: "2.1"
target_schema:
  type: object
  required: [id, name, email, created_at]
  properties:
    id: { type: integer }
    name: { type: string }
    email: { type: string, format: email }
    created_at: { type: string, format: date-time }
    tags: { type: array, items: { type: string } }
mapping:
  user_id: id
  user_name: name
  email_address: email
  created_timestamp: created_at
```

**Output:**
```yaml
transformed:
  input_type: "json"
  output_type: "yaml"
  content:
    id: 12345
    name: "john_doe"
    email: "john@example.com"
    created_at: "2024-01-15T10:00:00Z"
    tags: []
  mapping_applied: "explicit_mapping_v1"
validation:
  input_valid: true
  output_valid: true
  schema_ref: "user_schema_v2"
  errors: []
losses:
  - field: "metadata.source"
    reason: "No mapping to target schema"
    severity: info
  - field: "metadata.version"
    reason: "No mapping to target schema"
    severity: info
conversions:
  - source_field: "created_timestamp"
    target_field: "created_at"
    conversion: "unix_epoch to ISO8601 datetime"
    reversible: true
  - source_field: "tags"
    target_field: "tags"
    conversion: "default empty array added"
    reversible: false
confidence: 0.9
evidence_anchors:
  - "source:user_id -> target:id"
  - "schema:required_fields_present"
  - "conversion:timestamp_to_iso8601"
assumptions:
  - "Unix timestamp is in seconds, not milliseconds"
  - "Timezone is UTC"
```

**Evidence pattern:** Field-by-field mapping documented, schema validation confirms conformance.

---

### Example 2: CSV to Structured Object

**Input:**
```yaml
source: "name,age,city\nAlice,30,NYC\nBob,25,LA"
target_schema:
  type: array
  items:
    type: object
    properties:
      full_name: { type: string }
      age_years: { type: integer }
      location: { type: string }
mapping:
  name: full_name
  age: age_years
  city: location
```

**Output:**
```yaml
transformed:
  input_type: "csv"
  output_type: "json_array"
  content:
    - full_name: "Alice"
      age_years: 30
      location: "NYC"
    - full_name: "Bob"
      age_years: 25
      location: "LA"
  mapping_applied: "csv_to_object_mapping"
validation:
  input_valid: true
  output_valid: true
  schema_ref: "person_array_schema"
  errors: []
losses: []
conversions:
  - source_field: "age"
    target_field: "age_years"
    conversion: "string to integer"
    reversible: true
confidence: 0.95
evidence_anchors:
  - "source:row_count=2"
  - "schema:all_required_present"
assumptions:
  - "CSV uses comma delimiter"
  - "First row is header"
  - "No quoted fields with commas"
```

## Verification

- [ ] Output validates against target schema
- [ ] All required fields are present
- [ ] Type conversions are correct
- [ ] Losses are explicitly documented
- [ ] Transformation is reproducible

**Verification tools:** Read (for schema validation), Grep (for pattern matching)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Always document data loss explicitly
- Never silently drop fields without recording
- Validate output against schema before returning
- Flag precision loss in numeric conversions
- If transformation is ambiguous, ask for clarification
- Never transform sensitive data without noting it

## Composition Patterns

**Commonly follows:**
- `receive` - Transform incoming messages to canonical form
- `retrieve` - Transform retrieved data to expected format
- `inspect` - Understand source before transformation

**Commonly precedes:**
- `send` - Format data before external transmission
- `integrate` - Prepare data for merging
- `validate` - Check transformed output

**Anti-patterns:**
- Never transform without documenting losses
- Never assume field type without verification
- Avoid chained transforms without intermediate validation

**Workflow references:**
- See `reference/composition_patterns.md#digital-twin-sync-loop` for transform in data pipeline
- See `reference/composition_patterns.md#enrichment-pipeline` for transform context
