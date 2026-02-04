---
name: typescript-functional
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: TypeScript functional programming. Use for pure functions, immutability, composition. Favors ternaries, switch, map/filter/reduce over imperative code. Concise, declarative patterns.
---

# TypeScript Functional Programming

## Quick Start

**Core principles:** Pure functions | Immutability | Composition |
Higher-order functions | Declarative over imperative

**Prefer:** `? :` over `if` | `switch` over `if/else` chains |
`map/filter/reduce` over loops | `const` over `let` | Expressions over statements

## Example

```typescript
// ❌ Imperative
function processUsers(users: User[]): string[] {
  let result = [];
  for (let i = 0; i < users.length; i++) {
    if (users[i].age >= 18) {
      result.push(users[i].name.toUpperCase());
    }
  }
  return result;
}

// ✅ Functional
const processUsers = (users: User[]): string[] =>
  users
    .filter(user => user.age >= 18)
    .map(user => user.name.toUpperCase());

// ✅ Ternary over if
const getStatus = (age: number): string =>
  age >= 18 ? 'adult' : 'minor';

// ✅ Switch for multiple conditions
const getDiscount = (tier: Tier): number => {
  switch (tier) {
    case 'gold': return 0.2;
    case 'silver': return 0.1;
    case 'bronze': return 0.05;
    default: return 0;
  }
};
```

## Reference Files

**Check these before suggesting code:**

- [references/pure-functions.md](references/pure-functions.md) -
  Pure function patterns and side effect handling
- [references/array-methods.md](references/array-methods.md) -
  map, filter, reduce, and functional iteration
- [references/composition.md](references/composition.md) -
  Function composition and piping patterns
- [references/immutability.md](references/immutability.md) -
  Immutable data structures and updates
- [references/control-flow.md](references/control-flow.md) -
  Ternaries, switch, and functional conditionals

## Notes

- Avoid mutations: Use spread operators and array methods
- No `let` unless absolutely necessary (prefer `const`)
- Functions should be small, single-purpose, composable
- Prefer function expressions over statements
- Use type inference when possible, explicit types when needed
- Early returns are acceptable for guard clauses
- **Last verified:** 2025-12-03

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
