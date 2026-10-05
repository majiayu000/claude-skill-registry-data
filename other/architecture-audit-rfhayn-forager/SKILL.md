---
name: architecture-audit
description: Check codebase for architectural violations (factory bypass, raw assign, scope compliance, service layer). TRIGGER when the user discusses creating Core Data objects in production code, adding new entity creation sites, or before PR creation on milestones that touch the service/model layer.
user_invocable: true
---

# Architecture Audit

Run this audit before any milestone that creates Core Data objects, during code review, and as a quality gate.

## Checks

### 1. Factory Bypass Detection (ADR 014)
Search for direct creation of HouseholdScoped entities outside exempt files:

```bash
# Search for direct Entity(context:) for HouseholdScoped types
grep -rn 'WeeklyList(context:\|Recipe(context:\|PlannedMeal(context:\|MealPlan(context:\|Category(context:\|IngredientTemplate(context:' \
  --include='*.swift' \
  --exclude-dir=foragerTests \
  --exclude-dir=foragerUITests \
  --exclude='*Preview*' \
  --exclude='DefaultSeeder.swift' \
  --exclude='SampleDataSeeder.swift' \
  --exclude='ManagedObjectFactory.swift' \
  --exclude='HouseholdService.swift'
```

**Expected**: Zero matches in non-exempt production files.
**Exempt files**: Tests, previews, seeders, HouseholdService (migration), ManagedObjectFactory itself.
**Note**: Repository files may have fallback paths with direct creation — these are acceptable IF they also have factory-first branches.

### 2. Raw Assign Detection
Search for `viewContext.assign(` or `context.assign(` outside `ManagedObjectFactory.swift`:

```bash
grep -rn 'viewContext\.assign(\|context\.assign(' --include='*.swift' --exclude='ManagedObjectFactory.swift'
```

**Expected**: Zero matches.

### 3. ADR 013 Scope Compliance (services + repositories only)
Search for HouseholdScoped fetch requests missing `householdKey` predicate in the
service + repository layers:

```bash
# Look for fetch requests on HouseholdScoped entities in Services/ and Repositories/ ONLY
grep -rn 'NSFetchRequest<WeeklyList>\|NSFetchRequest<Recipe>\|NSFetchRequest<MealPlan>\|NSFetchRequest<PlannedMeal>\|NSFetchRequest<Category>\|NSFetchRequest<IngredientTemplate>\|NSFetchRequest<GroceryListItem>\|NSFetchRequest<Ingredient>\|NSFetchRequest<Store>' \
  Services/ forager/Repositories/ \
  --include='*.swift'
```

Then verify each fetch includes a `householdKey` predicate (grep the same file within ~10 lines after the declaration for the string `householdKey`).

**Non-goal — view-layer `@FetchRequest`**: this check intentionally does NOT scan
`forager/Views/`. The view-layer in-memory-filter pattern is emergent (first
appeared `f263730` on 2026-01-18; spread by copy-paste across 24 views; not
formalized by any ADR) and is deferred to a future change named
`decide-view-layer-scope-architecture` which will evaluate alternatives, pilot
one, migrate all ~43 sites, and only then write a definitive ADR. Do NOT extend
this check to `forager/Views/` before that future change lands — the bare
`@FetchRequest` on a HouseholdScoped entity is NOT a violation of ADR 013 today.
See the auto-memory entry `project_scope_safety_three_layers.md` for context.

### 4. Service Layer Compliance
Search for `context.save()` in production view files (views should use services).
Previews are exempt — `#Preview { }` blocks and `PreviewProvider` extensions are a
legitimate standalone environment that may call `context.save()` to stage preview
data.

```bash
# Production view saves: exclude dedicated preview files via glob
grep -rn 'context\.save()\|viewContext\.save()' forager/Views/ \
  --include='*.swift' \
  --exclude='*Preview*'
```

**Manual follow-up**: matches inside `#Preview { ... }` macro blocks or
`PreviewProvider` extension bodies (in files NOT named `*Preview*`) are
also legitimate. Discount them when reporting violations. For each reported
match, open the file and confirm it is outside any `#Preview { }` block and
outside any `PreviewProvider` extension before flagging it.

**Expected**: Zero production matches (all production saves through service layer).

## How to Run

Use the Grep tool to execute each check. Report violations with file:line references.

## When to Run
- Before starting any milestone that creates Core Data objects
- During code review / PR creation
- After completing service or view layer changes
- As a quality gate before marking milestone complete
