---
name: feature-slicing
description: Feature-first development approach that organizes code by features rather than technical layers, promoting cohesion and reducing coupling
---

# Feature Slicing

Feature slicing is an architectural approach that organizes code by features (vertical slices) rather than by technical layers (horizontal slices). Each feature contains all the code it needs - UI, business logic, data access - in one cohesive module.

## Core Concept

**Traditional Layered Architecture (Horizontal):**
```
/controllers
  - userController.js
  - productController.js
/services
  - userService.js
  - productService.js
/models
  - user.js
  - product.js
```

**Feature-Sliced Architecture (Vertical):**
```
/features
  /user-management
    - userController.js
    - userService.js
    - userModel.js
    - userValidator.js
  /product-catalog
    - productController.js
    - productService.js
    - productModel.js
```

## When to Use Feature Slicing

Use feature slicing when:
- Building new features or products
- Your codebase is growing complex
- You have multiple developers working on different features
- You want to enable parallel development
- You need to understand feature scope quickly
- You're implementing modular or micro-frontend architecture

## Benefits

1. **High Cohesion** - Related code lives together
2. **Low Coupling** - Features are independent
3. **Easy Navigation** - Find all code for a feature in one place
4. **Parallel Development** - Teams work on different features without conflicts
5. **Feature Isolation** - Remove or disable features easily
6. **Clear Ownership** - Teams own entire features
7. **Better Understanding** - Feature scope is immediately visible

## Step-by-Step Workflow

See [Feature Workflow Guide](./guides/feature-workflow.md) for complete implementation steps.

### Quick Steps:

1. **Identify the Feature** - What user-facing capability are you building?
2. **Create Feature Directory** - `/features/feature-name/`
3. **Implement Vertically** - Add all layers for this feature
4. **Test the Feature** - Write tests within the feature directory
5. **Integrate** - Connect feature to the application

## Common Anti-Patterns

See [Anti-Patterns Guide](./guides/anti-patterns.md) for detailed examples.

### Watch Out For:

- Starting with horizontal layers
- Sharing code between features too early
- Creating "utilities" folder instead of feature modules
- Mixing feature code with framework code
- Over-abstracting before seeing patterns

## Feature Slicing vs Layered Architecture

| Aspect | Feature Slicing | Layered Architecture |
|--------|----------------|---------------------|
| Organization | By business feature | By technical layer |
| Cohesion | High (related code together) | Low (scattered across layers) |
| Coupling | Low (features independent) | High (layers depend on each other) |
| Navigation | Easy (one directory) | Hard (multiple directories) |
| Team Ownership | Clear (feature teams) | Unclear (layer teams) |
| Parallel Work | Easy (different features) | Conflicts (same layers) |

## When NOT to Use Feature Slicing

- Very small applications (< 5 features)
- Single-developer projects with simple requirements
- Applications with truly shared cross-cutting concerns
- When team prefers and understands layered architecture

## Key Principles

1. **Feature First** - Organize by what users see, not technical layers
2. **Vertical Slices** - Each feature is a complete slice through all layers
3. **Shared Last** - Don't create shared code until pattern emerges
4. **Independence** - Features should not directly depend on each other
5. **Complete Features** - Include tests, docs, and everything needed

## Integration with Other Principles

- **DRY**: Extract shared code only after seeing 3+ instances
- **YAGNI**: Build features when needed, not in advance
- **KISS**: Keep feature structure simple
- **SOLID**: Apply SRP to features themselves

## Resources

- [Complete Feature Workflow](./guides/feature-workflow.md)
- [Common Anti-Patterns](./guides/anti-patterns.md)

## Summary

Feature slicing organizes code by business capabilities rather than technical layers. It promotes high cohesion within features and low coupling between features. Start with vertical slices for each feature, and extract shared code only when clear patterns emerge. This approach enables parallel development, clear ownership, and easier navigation of your codebase.
