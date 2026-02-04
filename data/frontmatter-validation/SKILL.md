---
name: frontmatter-validation
description: "Validate YAML frontmatter in documentation against template requirements. Use when creating or editing docs, or when the user asks to check frontmatter."
event: doc-save
auto_trigger: true
version: "2.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - document_path
  - document_content
  - expected_template
output: validation_report
output_format: "Pass/Fail with error details"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "doc-save"
    - "doc-creation"
  file_patterns:
    - "docs/**/*.md"
  conditions:
    - "markdown file saved in docs/"

# Validation
validation_rules:
  - "document_type must be valid"
  - "last_updated must be ISO date"
  - "version must be semver"
  - "at least 5 keywords required"
  - "author must start with @"

# Chaining
chain_after: [documentation]
chain_before: [related-docs-sync]

# Agent Association
called_by: ["@Scribe"]
mcp_tools:
  - mcp_payment-syste_query_docs_by_type
  - read_file
---

# Frontmatter Validation Skill

> **Purpose:** Validate YAML frontmatter in documentation against template requirements. Ensures consistency across all docs.

## Trigger

**When:** Any `.md` file in `docs/` is saved or created
**Context Needed:** Document content, template for document_type
**MCP Tools:** `mcp_payment-syste_query_docs_by_type`, `read_file`

## Required Fields

All documents MUST have:

```yaml
---
document_type: "[type]" # REQUIRED
module: "[module]" # REQUIRED
status: "[status]" # REQUIRED
version: "X.Y.Z" # REQUIRED
last_updated: "YYYY-MM-DD" # REQUIRED
author: "@username" # REQUIRED

keywords:
  - "[keyword1]" # REQUIRED (5-10)

related_docs: # REQUIRED (can be empty)
  database_schema: ""
  api_design: ""
  ux_flow: ""
---
```

## Document Types → Templates

| document_type        | Template      | Extra Fields           |
| :------------------- | :------------ | :--------------------- |
| `general`            | 00-GENERAL    | doc_metadata           |
| `feature-design`     | 01-FEATURE    | feature_metadata       |
| `adr`                | 02-ADR        | adr_metadata           |
| `database-schema`    | 03-DATABASE   | database, schema_stats |
| `api-design`         | 04-API        | api_metadata           |
| `sync-strategy`      | 05-SYNC       | sync_metadata          |
| `ux-flow`            | 06-UX         | ux_metadata            |
| `testing-strategy`   | 07-TESTING    | testing_metadata       |
| `deployment-runbook` | 08-DEPLOYMENT | deployment_metadata    |
| `security-audit`     | 09-SECURITY   | security_metadata      |

## Status Values

```yaml
status: "draft"       # Work in progress
status: "in-review"   # Under review
status: "approved"    # Ready for use
status: "deprecated"  # No longer valid
```

## Validation Rules

1. **Type Check:** `document_type` must match valid types
2. **Date Format:** `last_updated` must be ISO date (YYYY-MM-DD)
3. **Version Format:** `version` must be semver (X.Y.Z)
4. **Keywords:** At least 5 keywords required
5. **Author:** Must start with `@`
6. **Related Docs:** Paths must exist or be empty string

## Auto-Fix Suggestions

When validation fails, suggest:

- Missing fields with defaults
- Date format corrections
- Path corrections for related_docs

## Example Output

```json
{
  "valid": false,
  "errors": [
    {
      "field": "last_updated",
      "message": "Invalid date format",
      "suggestion": "2026-01-26"
    }
  ],
  "warnings": [
    { "field": "keywords", "message": "Only 3 keywords, recommend 5-10" }
  ]
}
```

## Reference

- [DOCUMENTATION-WORKFLOW.md](/docs/process/standards/DOCUMENTATION-WORKFLOW.md)
- [docs/templates/](/docs/templates/)
