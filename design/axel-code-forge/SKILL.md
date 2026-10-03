---
name: axel-code-forge
description: Use when enforcing Axel's coding standards across any language for architecture, reuse, imports, and maintainability, plus React/Next.js-specific rules only where explicitly stated (for example useEffect and JSX handlers).
---

# Axel Code Forge

## Purpose

Enforce Axel's coding conventions with focus on consistency, reuse, and maintainability. Apply React/Next.js rules only where explicitly marked.

## Scope

- **General (any language)**: architecture, modularity, imports, constants, null safety, decomposition, reuse.
- **React/Next.js only**: rules tied to React/Next APIs or JSX semantics, explicitly tagged.

## When to Use

- Any feature or bugfix where code quality matters
- Refactors and file organization
- Code review and quality hardening
- UI implementation with design tokens

## Non-Negotiable Rules

1. [General] Use absolute imports only. Avoid relative imports in app code.
2. [General] Avoid hardcoded values. Use constants, shared config, design tokens, or enums.
3. [React/Next] Avoid inline functions in JSX handlers (`onClick`, `onChange`). Define stable handlers.
4. [General] Never assume values exist. Guard nullable/optional values before use.
5. [React/Next] Keep hooks focused. Avoid long `useEffect` and large state blobs.
6. [General] No God components. Split large components into atomic, reusable units.
7. [General/UI] Prefer project theme/color tokens over raw Tailwind palette classes.
8. [General] Avoid comments by default. One concise English comment only for critical context.
9. [General/UI] Keep SVGs outside feature pages. Place in icons folder or shared components.
10. [General] Prioritize reusable components and utility functions.
11. [General] Use feature-based separation (atomic split by concern).
12. [General] Follow existing project patterns for shared primitives.
13. [React/Next] Follow existing patterns for Redux and custom hooks.

## Implementation Checklist

- [ ] Imports are absolute and aligned with aliases
- [ ] Literals extracted to constants when reused
- [ ] JSX handlers reference named functions (React only)
- [ ] Optional values guarded before dereference
- [ ] Effects are single-purpose with clear deps (React only)
- [ ] Component size controlled
- [ ] Theme tokens used before generic colors
- [ ] No unnecessary comments
- [ ] SVGs externalized to icon system
- [ ] Logic duplication reduced
- [ ] Existing patterns respected

## Preferred Refactor Direction

When touching complex files:

1. Extract constants and mappings
2. Extract row/item subcomponents
3. Extract pure helper functions
4. Reduce inline object/function creation in render
5. Keep behavior identical unless requirements demand change

---

## Auto-Update Protocol

> HEFESTO manages this skill. User preferences evolve.

### Detection Triggers

Detect when user teaches a preference:

- **Explicit**: "siempre", "nunca", "preferimos", "regla:", "acordate"
- **Implicit**: Correcting code with a pattern, repeating a preference
- **Review**: "esto esta mal porque...", "mejor asi..."

### Update Flow

```
1. HEFESTO detects preference pattern
2. Ask: "Agrego esto a axel-code-forge?"
3. If approved:
   a) Check for conflicts with existing rules
   b) If conflict: "Esto choca con regla X. Cual priorizamos?"
   c) If clear: Add to Non-Negotiable Rules
   d) Confirm: "Agregado: [rule summary]"
4. If rejected: Note in session, don't persist
```

### Conflict Resolution

When new rule conflicts with existing:

```
HEFESTO: "La regla nueva 'always use ternaries' 
choca con la existente 'avoid nested ternaries'.
Cual priorizamos?

1. Keep existing, reject new
2. Replace existing with new
3. Merge: allow simple ternaries, avoid nested"

User: "3"

HEFESTO: "Actualizado:
- [General] Use simple ternaries. Avoid nested ternaries (use if/else)."
```

### Rule Format for New Additions

```markdown
X. [Scope] Rule description in imperative form.
```

Where:
- X = next number in sequence
- Scope = General | React/Next | General/UI
- Description = clear, actionable statement

### Example Updates

**User says**: "Nunca uses `any`, siempre `unknown`"

```
HEFESTO: "Agrego a axel-code-forge:
  14. [General] Never use `any`. Prefer `unknown` with type guards.
  
Dale?"
```

**User corrects code**: Changes `arr.map(x => x.id)` to `arr.map((item) => item.id)`

```
HEFESTO: "Noto que preferis parametros descriptivos en callbacks.
Agrego?
  15. [General] Use descriptive parameter names in callbacks (item, user, not x, i).
  
Dale?"
```

### Validation

Before adding rule, HEFESTO checks:

1. Not redundant with existing rule
2. Not contradictory to existing rule
3. Follows existing rule format
4. Is actionable (not vague)

If validation fails, explain why and suggest alternative wording.
