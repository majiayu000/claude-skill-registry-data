---
name: generate-domain-model
description: "Generate a complete Mendix domain model in MDL — entities, attributes, associations, enumerations — and validate it. Use when asked for a domain model for a business area (e-commerce, HR, CRM, …) rather than a single entity."
---

# Creating Mendix Domain Model MDL Scripts

Use this skill to generate Mendix domain model scripts in MDL (Mendix Definition Language) format and validate them with the linter.

## Reference files

`SKILL.md` covers the process and the decisions — what to model, in what order,
and how to check it. The lookup material is next door:

- [`reference/syntax.md`](reference/syntax.md) — the complete syntax for entities,
  attributes, associations and enumerations, every attribute type, plus reserved
  keywords and entity positioning. **Check a spelling here rather than guessing**;
  a reserved word used as an attribute name fails in Studio Pro, not in the parser.
- [`reference/patterns.md`](reference/patterns.md) — the recurring domain shapes
  (header/detail, categorisation, audit, soft delete, many-to-many with payload)
  and a full worked e-commerce model.

## When to Use This Skill

- User asks to create a domain model for a specific use case
- User wants to generate entities, associations, and enumerations
- User requests a complete e-commerce, HR, CRM, or other business domain model
- User needs validation of generated MDL scripts

## Modelling for the client: widgets bind members, not expressions

A page widget binds an **attribute or association path** — never an expression. There
is no `substring(attr, i, 1)` or computed binding in a widget. So a value that must be
rendered per-part (each character of a code, each cell of a grid, each of N pencil
marks) has to be stored as **separate attributes**, not packed into one string and
indexed client-side. Model the wide form when the UI needs to address the parts
individually (e.g. `N1`…`N9` booleans rather than a packed `Notes` string); reach for
a computed/derived value only where a microflow or view-entity OQL produces it into a
real attribute. (Same reason the bucket-class idiom exists — see
`migrate-design-prototype`.)

## Documentation Best Practices

### Entity Documentation

```sql
/**
 * Brief one-line summary
 *
 * Detailed multi-line description explaining:
 * - What the entity represents
 * - Key business rules
 * - Relationships to other entities
 *
 * @since 1.0.0
 * @see Module.RelatedEntity
 */
```

### Attribute Documentation

```sql
/** Brief description of what this attribute stores */
attributename: type,
```

### Association Documentation

```sql
/**
 * Relationship description
 *
 * Explains the business meaning of this association.
 *
 * @since 1.0.0
 */
```

## Step-by-Step Process

### 1. Analyze Requirements

When user requests a domain model:
1. Identify core entities (nouns)
2. Identify enumerations (status, types, categories)
3. Identify relationships (associations)
4. Identify attributes for each entity
5. Check for reserved keyword conflicts

### 2. Generate MDL Script

Create script with this structure:
```sql
-- ============================================================================
-- Domain Model Name
-- ============================================================================
-- Description of the domain
-- ============================================================================

-- MARK: ENUMERATIONS

create enumeration Module.Enum1 (...);
create enumeration Module.Enum2 (...);

-- MARK: CORE ENTITIES

-- MARK: - Entity Group 1

create persistent entity Module.Entity1 (...);
create persistent entity Module.Entity2 (...);

-- MARK: - Entity Group 2

create persistent entity Module.Entity3 (...);

-- MARK: VIEW ENTITIES

create view entity Module.View1 as ...;

-- MARK: ASSOCIATIONS

-- MARK: - Entity Group 1 Associations

create association Module.Assoc1 ...;
create association Module.Assoc2 ...;
```

### 3. Validate with Linter

Run the linter to check for issues:

```bash
# Standalone test
node dist/test-linter-standalone.js

# or create a custom test file
```

The linter will detect:
- ✅ Reserved keywords (CE7247)
- ✅ Duplicate names (CE0065)
- ✅ OQL syntax errors (CE0174)

### 4. Review and Fix Issues

**Common Issues**:

1. **Reserved Keyword Error**:
   ```
   error: Reserved keyword 'CreatedDate' used as attribute name
   💡 rename to 'CreationDate'
   ```
   Fix: Rename to suggested alternative

2. **Duplicate Name Error**:
   ```
   error: Duplicate name 'Status' in module 'Shop'
   💡 rename one of the enumeration, entity to avoid conflict
   ```
   Fix: Rename entity to `OrderStatus` or similar

3. **OQL Syntax Error**:
   ```
   error: ORDER by requires limit or offset
   💡 add limit clause to query
   ```
   Fix: Add `limit 100` to view entity query

### 5. Generate Complete Script

Ensure:
- ✅ All entities have JavaDoc documentation
- ✅ All attributes have inline comments
- ✅ All associations have descriptions
- ✅ Position annotations for all entities
- ✅ No reserved keywords
- ✅ No duplicate names
- ✅ Valid OQL queries

## Testing the Script

1. **Save to file**: Save as `examples/my-domain-model.mdl`

2. **Run standalone linter**:
   ```bash
   node dist/test-linter-standalone.js
   ```

3. **Execute in REPL**:
   ```sql
   mendix> connect to FILESYSTEM 'path/to/project.mpr';
   mendix> execute script 'examples/my-domain-model.mdl';
   ```

4. **Check Studio Pro**: Open project and verify entities appear correctly

## Checklist

Before finalizing an MDL script:

- [ ] All entities have JavaDoc documentation
- [ ] All attributes have inline comments
- [ ] All associations have descriptions
- [ ] Position annotations on all entities
- [ ] MARK comments for files 300+ lines (at least 3 sections)
- [ ] All identifiers quoted with double quotes
- [ ] No duplicate names (run linter)
- [ ] Valid OQL queries in view entities (run linter)
- [ ] Consistent naming conventions (PascalCase)
- [ ] Appropriate data types and lengths
- [ ] Required fields marked with NOT NULL
- [ ] Validation error messages added for NOT NULL and UNIQUE constraints
- [ ] IDs marked with NOT NULL UNIQUE
- [ ] Email/unique fields marked with UNIQUE

## References

- **Reserved Keywords**: `packages/mendix-repl/docs/reference/reserved-keywords.md`
- **Linter Proposal**: `packages/mendix-repl/docs/proposals/mdl-linter-proposal.md`
- **Example Scripts**:
  - `packages/mendix-repl/examples/shop-domain-model.mdl`
  - `packages/mendix-repl/examples/pet-store-domain-model.mdl`
- **Linter Test**: `packages/mendix-repl/src/test-linter-standalone.ts`

## Tips for AI Assistants

1. **Always quote all identifiers** with double quotes to avoid MDL parser keyword conflicts — but note quoting does **not** exempt platform-reserved member names (`Type`, `CreatedDate`, `ChangedDate`, `Owner`, `ChangedBy`, `ID`, …); rename those
2. **Use descriptive names** (ServiceType, CustomerOrder)
3. **Run linter** on generated scripts before presenting to user
4. **Fix all errors** reported by linter before finalizing
5. **Follow examples** in shop-domain-model.mdl and pet-store-domain-model.mdl
6. **Document thoroughly** - Studio Pro users benefit from good documentation
7. **Position thoughtfully** - Related entities should be visually grouped
8. **Test incrementally** - Generate in sections and validate each part
