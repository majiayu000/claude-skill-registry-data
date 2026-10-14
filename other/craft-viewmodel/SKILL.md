---
name: craft-viewmodel
description: Crafting ViewModels. Data transformation for views.
---

# Skill: Craft ViewModel

> "View models have one job—providing correct data to views."

## The Standard

1. **Single Responsibility**: Transform data for views. No business logic.
2. **Implement Arrayable**: Public methods become view variables automatically.
3. **Optional Model**: Accept `?Model` in constructor. Null for create, instance for edit.
4. **Explicit Dependencies**: Inject User, Model—whatever the view needs.

## The Anti-Patterns

| ❌ Don't               | ✅ Do                      | Why                         |
|-----------------------|---------------------------|-----------------------------|
| View Composers        | ViewModel in controller   | Explicit > implicit         |
| Duplicate create/edit | One ViewModel, optional model | DRY, single source of truth |
| Query in controller   | Query in ViewModel method | Controller stays thin       |
| Return arrays         | Return ViewModel object   | Type safety, testability    |

## Real-World Examples

See [examples.md](examples.md).
