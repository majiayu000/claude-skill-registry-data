---
name: spectral
# prettier-ignore
description: Use when configuring Spectral for API linting, creating custom rulesets, and validating OpenAPI or AsyncAPI specifications
---

# Spectral API Linting

## Quick Start

```yaml
# .spectral.yaml
extends: spectral:oas
rules:
  operation-operationId: error
  info-contact: warn
  oas3-api-servers: off
```

## Core Concepts

- **Rulesets**: Collections of rules; extend built-in (`spectral:oas`, `spectral:asyncapi`)
- **Severity**: `error`, `warn`, `info`, `hint`, or `off` to disable
- **Given**: JSONPath expression targeting what to validate
- **Then**: Functions and conditions to check

## Custom Rules

```yaml
rules:
  must-have-description:
    description: All operations must have descriptions
    given: $.paths[*][get,post,put,patch,delete]
    severity: error
    then:
      field: description
      function: truthy

  path-must-be-kebab-case:
    given: $.paths[*]~
    then:
      function: pattern
      functionOptions:
        match: "^(/[a-z0-9-]+)+$"
```

## Built-in Functions

- `truthy` / `falsy` - Value exists / is empty
- `pattern` - Regex matching
- `length` - String/array length constraints
- `enumeration` - Value in allowed list
- `schema` - Validate against JSON Schema
- `alphabetical` - Keys in order
- `undefined` - Property must not exist

## CLI Usage

```bash
spectral lint openapi.yaml
spectral lint openapi.yaml --ruleset .spectral.yaml
spectral lint openapi.yaml -f json  # JSON output
```

## Reference Files

- [references/functions.md](references/functions.md) - All built-in functions
- [references/custom-functions.md](references/custom-functions.md) - Writing custom functions
- [references/jsonpath.md](references/jsonpath.md) - JSONPath expressions
