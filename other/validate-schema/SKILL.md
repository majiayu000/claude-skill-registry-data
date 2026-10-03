---
metadata:
  name: validate-schema
  class: toolboxes
  type: skill
  version: '1.0'
  schema_version: '1.0'
  freshness:
    status: active
    sync_count: 0
    last_synced_by: daemon
    last_synced: '2026-06-27T00:00:00'
credentials:
  maturity: "functional"
  description: "Validate that a file, data structure, or agent output conforms to its defined schema or structural contract."
  when_to_use: "Use this skill when the task involves validate schema"
  triggers: ["validate", "check schema", "is this correct", "verify structure", "does this conform", "integrity check", "schema check"]
  inputs: ["target data or file path", "schema or contract definition", "validation rules"]
  outputs: ["validation verdict (pass/fail)", "violation list with locations", "fix instructions"]
---

# Validate Schema

This skill allows the agent to verify that any data structure, file, YAML block, or agent output conforms to its defined schema or structural contract — producing a precise, actionable pass/fail report before the data is acted upon or written to disk.

## Steps

1. **Locate and read the schema.** Find the authoritative schema definition:
   - For workspace YAML files → check `.db/.schemas/` for the appropriate schema
   - For toolbox files → check the toolbox `yaml_path` file's structure
   - For custom structures → derive from the written spec or identity file
2. **Read the target fresh.** Apply Zero-Drift Audit Law — read the actual current file/data live, not from cached context.
3. **Map required fields.** List every required field from the schema. Note which are optional.
4. **Check field presence.** For each required field, verify it exists in the target.
5. **Check field types.** Verify data types match (string vs int, list vs scalar, etc.).
6. **Check value constraints.** Validate enum values, non-empty lists, valid paths, valid statuses, etc.
7. **Check structural contract.** Verify nesting depth, key naming conventions, and ordering where prescribed.
8. **Compile violations.** For every failure, record: field path, expected value/type, actual value/type, severity (blocking vs warning).
9. **Determine verdict.**
   - Zero violations → **VALID ✅**
   - Warnings only → **VALID WITH WARNINGS ⚠️**
   - Any blocking violation → **INVALID ❌**
10. **Generate fix instructions.** For each violation, produce a specific, executable correction.
11. **Output** the validation report.

## Output Format

```yaml
validation_report:
  target: "<file or data description>"
  schema_source: "<where the schema was found>"
  verdict: "VALID | VALID_WITH_WARNINGS | INVALID"
  violations:
    - field_path: "<e.g. content.skills[0].maturity>"
      expected: "<expected type or value>"
      actual: "<what was found>"
      severity: "blocking | warning"
      fix: "<exact correction to apply>"
  summary: "<one-line verdict summary>"
```

## Notes
- **Always validate before writing.** Any automated file write should be preceded by a schema validation of the content.
- If no schema exists for a target, flag this as a gap and generate a schema proposal before proceeding.
- Validation failures on `.db/.system.board.yaml` or router files are critical — they corrupt agent routing.
- Pair with `planning` toolbox: if INVALID, generate a fix plan before retrying.
