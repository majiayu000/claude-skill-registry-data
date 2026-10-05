---
name: core-data-audit
description: Run Core Data impact analysis before schema changes. Required by ADR 007. Searches all usage of affected entities, documents relationships, codegen, and migration impact. TRIGGER when the user discusses changing the Core Data schema, adding/removing entity attributes, modifying relationships, creating a new entity, or any database model changes.
argument-hint: <EntityName>
---

# Core Data Impact Analysis

**Entity**: $ARGUMENTS

Required by ADR 007 (`docs/architecture/007-core-data-change-process.md`) before ANY schema changes.

## Step 1: Read ADR 007

Read `docs/architecture/007-core-data-change-process.md` for the required process.

## Step 2: Entity Audit

For the target entity, find and document:

### Properties & Types
Search `Models/<EntityName>+CoreDataProperties.swift` for:
- All property names and their types
- Optional vs required
- Default values

### Relationships
- All relationships and their inverses
- Cascade delete rules
- Nullify rules

### Codegen Setting
- **Class Definition** (auto-generated) or **Manual/None** (custom extensions)?
- If Manual: what custom logic exists in extensions?

### Fetch Indexes
- What fields are indexed?
- What predicates are commonly used?

## Step 3: Usage Search

Search the entire codebase for references to this entity:

### Services
Search `Services/` for all methods that read or write this entity.

### Views
Search `forager/Views/` for `@FetchRequest` and other references.

### Repositories
Search `forager/Repositories/` for query methods.

### Tests
Search `foragerTests/` for test coverage.

## Step 4: Impact Report

Produce a structured report:

```markdown
## Core Data Impact Analysis: [EntityName]

### Current Schema
- Properties: [list with types]
- Relationships: [list with inverses]
- Codegen: [Class Definition / Manual]
- Indexes: [list]

### Files Affected by Change
- Services: [list]
- Views: [list]
- Repositories: [list]
- Tests: [list]

### Migration Impact
- Current model version: v6
- New version needed: v7
- Migration type: lightweight / manual
- CloudKit impact: [append-only constraint check]

### Risk Assessment
- [Identified risks]
- [Mitigation strategy]
```

## Step 5: Scope-Aware Fetch Audit (ADR 013)

If the entity has a `householdKey` property, verify:

### Fetch Scope Compliance
- [ ] Every `fetchRequest()` in services includes a `householdKey` predicate
- [ ] No unscoped fetches return user-facing data (ghost object risk)
- [ ] `householdKey` is passed as a parameter, not assumed from global state

### Zone Safety
- [ ] Any overwrite/replace operation validates the target object is in an accessible store
- [ ] Pre-mutation cleanup runs before `container.share()` operations
- [ ] Orphaned objects (stale `householdKey`, parentless Ingredients) are handled

### Entities requiring scope audit
Recipe, WeeklyList, MealPlan, PlannedMeal, Category, IngredientTemplate

See `docs/architecture/013-scope-aware-fetch-pattern.md` for the full pattern.

## Step 6: Factory Compliance Check (ADR 014)

If the entity conforms to `HouseholdScoped`, verify:

- [ ] All creation sites use `ManagedObjectFactory.make()` (not direct `Entity(context:)`)
- [ ] Services that create this entity have `var factory: ManagedObjectFactory?` property
- [ ] Factory is injected via `foragerApp.init()` or `performScopedWrite`
- [ ] Exempt sites documented: tests, previews, seeders, HouseholdService migration

Run `/forager-architecture-audit` to verify compliance.

HouseholdScoped entities: `WeeklyList`, `Recipe`, `PlannedMeal`, `MealPlan`, `Category`, `IngredientTemplate`

## Critical Reminders

- CloudKit Production schema is **append-only** — no destructive changes
- New model version requires incrementing from v8 (current) — update as needed
- Test with sample data before migrating production
- Follow M3 Phase 3 pattern for migrations (successful isStaple migration)
- **ADR 013**: All service fetches on household-scoped entities MUST include `householdKey` predicate
