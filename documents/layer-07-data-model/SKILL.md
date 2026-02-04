---
name: LAYER_07_DATA_MODEL
description: Expert knowledge for Data Model Layer modeling in Documentation Robotics
triggers:
  [
    "JSON Schema",
    "data model",
    "schema",
    "object schema",
    "data structure",
    "properties",
    "validation",
    "data type",
  ]
version: 0.7.0
---

# Data Model Layer Skill

**Layer Number:** 07
**Specification:** Metadata Model Spec v0.7.0
**Purpose:** Defines logical data structures using JSON Schema Draft 7, specifying entities, properties, validation rules, and data governance.

---

## Layer Overview

The Data Model Layer captures **logical data structures**:

- **SCHEMAS** - Object, array, string, numeric schemas
- **VALIDATION** - Type constraints, required fields, patterns, ranges
- **COMPOSITION** - Schema combinations (allOf, anyOf, oneOf, not)
- **GOVERNANCE** - Data classification, PII, retention policies
- **INTEGRATION** - Links to business objects, database tables, API operations

This layer uses **JSON Schema Draft 7** (industry standard) with custom extensions for cross-layer traceability.

**Central Entity:** The **ObjectSchema** (defining an object structure) is the core modeling unit.

---

## Entity Types

### Core JSON Schema Entities (17 entities)

| Entity Type           | Description                                        |
| --------------------- | -------------------------------------------------- |
| **JSONSchema**        | Root schema document                               |
| **ObjectSchema**      | Defines object structure with properties           |
| **ArraySchema**       | Defines array with items and constraints           |
| **StringSchema**      | String validation (length, pattern, format)        |
| **NumericSchema**     | Number/integer validation (min, max, multipleOf)   |
| **SchemaComposition** | Combines schemas (allOf, anyOf, oneOf, not)        |
| **SchemaProperty**    | Individual property definition                     |
| **Reference**         | $ref to other schemas                              |
| **DataGovernance**    | Governance annotations (classification, retention) |
| **DatabaseMapping**   | Maps to physical database (x-database extension)   |

---

## When to Use This Skill

Activate when the user:

- Mentions "data model", "schema", "JSON Schema", "data structure"
- Wants to define object structures, properties, or validation rules
- Asks about data types, constraints, or data governance
- Needs to model entities like User, Order, Product, etc.
- Wants to link data models to APIs or databases

---

## Cross-Layer Relationships

**Outgoing (Data Model → Other Layers):**

- `x-business-object-ref` → Business Layer (what business concept does this represent?)
- `x-database` → Datastore Layer (how is this stored physically?)
- `x-data-governance` → Security Layer (classification, PII, retention)
- `x-apm-data-quality-metrics` → APM Layer (data quality monitoring)

**Incoming (Other Layers → Data Model):**

- API Layer → Data Model (request/response schemas via $ref)
- UX Layer → Data Model (form validation rules)
- Testing Layer → Data Model (input constraints for test partitioning)

---

## Validation Best Practices

1. **Required fields** - Use `required` array for mandatory properties
2. **Type validation** - Always specify `type` (object, array, string, number, etc.)
3. **Format validation** - Use `format` for email, uuid, date-time, uri, etc.
4. **Range validation** - Use min/max for numbers, minLength/maxLength for strings
5. **Pattern validation** - Use `pattern` for regex validation (e.g., phone numbers)
6. **Data governance** - Always add `x-data-governance` for sensitive data
7. **Reusability** - Use `$ref` to reference shared schemas

---

## Common Commands

```bash
# Add object schema
dr add data_model object-schema --name "User" --property type=object

# List data models
dr list data_model object-schema

# Validate data model layer
dr validate --layer data_model

# Export as JSON Schema
dr export --layer data_model --format json-schema
```

---

## Example: User Schema

```yaml
id: data_model.object-schema.user
name: "User Schema"
type: object-schema
properties:
  type: object
  required: [id, email, username]
  properties:
    id:
      type: string
      format: uuid
      description: "Unique user identifier"
    email:
      type: string
      format: email
      description: "User email address"
      x-data-governance:
        classification: confidential
        pii: true
    username:
      type: string
      minLength: 3
      maxLength: 50
      pattern: "^[a-zA-Z0-9_-]+$"
    created_at:
      type: string
      format: date-time
    roles:
      type: array
      items:
        type: string
      description: "User role assignments"
  x-business-object-ref: business.actor.user
  x-database:
    table: users
    schema: public
```

---

## Pitfalls to Avoid

- ❌ Missing `type` field (validation will fail)
- ❌ Not marking PII/sensitive data with governance
- ❌ Overly complex schemas (break into smaller reusable schemas)
- ❌ Not using `$ref` for shared definitions
- ❌ Missing cross-layer links to business and database layers
