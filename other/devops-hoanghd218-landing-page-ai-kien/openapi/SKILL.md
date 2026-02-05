---
name: openapi
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when working with OpenAPI Specification files to validate, create/modify paths and schemas, check references, and enforce best practices
---

# OpenAPI Specification Expert

## Quick Start

```yaml
openapi: 3.1.0
info:
  title: API Name
  version: 1.0.0
paths:
  /users/{id}:
    get:
      parameters:
        - name: id
          in: path
          required: true
          schema: {type: string}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      required: [id, email]
      properties:
        id: {type: string}
        email: {type: string, format: email}
```

## Core Principles

- **Required Structure**: `openapi`, `info`, and `paths` or `webhooks` at root
- **Reuse Components**: Define schemas/parameters/responses in `components/`, reference with `$ref`
- **Match Parameters**: Path parameters like `{id}` MUST have parameter definitions
- **Case Sensitive**: All field names follow JSON Schema case sensitivity

## Common Operations

Validate structure, create/modify endpoints with operations and parameters, manage reusable schemas with JSON Schema validation, configure security schemes (apiKey/http/oauth2), handle $ref paths, check operation IDs

## Key Rules

- Unique `operationId` per operation
- Use CommonMark in `description` fields
- Concrete paths match before templated
- Document all response codes

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
