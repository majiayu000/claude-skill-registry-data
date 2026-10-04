---
name: coding-standards
description: Cross-language coding standards for Python, TypeScript, and Go covering naming, SOLID design, code smell removal, and comment philosophy. Use when writing, reviewing, or refactoring production code for maintainability.
---

# Coding Standards

Write code that is obvious to change: clear names, small units, stable abstractions, and comments that explain intent rather than syntax.

## When to Activate

- Rename ambiguous identifiers
- Split oversized functions or modules
- Introduce a new abstraction or interface
- Review a pull request for maintainability drift
- Add comments around non-obvious behavior
- Remove dead code after a feature change
- Port logic between Python, TypeScript, and Go

## Naming

| Language | Types | Functions | Variables | Constants |
| --- | --- | --- | --- | --- |
| Python | `PascalCase` | `snake_case` | `snake_case` | `UPPER_SNAKE_CASE` |
| TypeScript | `PascalCase` | `camelCase` | `camelCase` | `UPPER_SNAKE_CASE` for module constants |
| Go | `PascalCase` exported, `camelCase` internal | `camelCase` | `camelCase` | `PascalCase` or `camelCase` scoped to package |

Rules:

- Prefer names that reveal domain meaning, not implementation detail.
- Boolean names should read as predicates: `is_active`, `hasAccess`, `canRetry`.
- File names should match the dominant abstraction.

## SOLID Without Ceremony

| Principle | Apply As | Avoid |
| --- | --- | --- |
| Single Responsibility | One unit changes for one reason | Utility files collecting unrelated behavior |
| Open/Closed | Extend via composition, interfaces, data-driven config | Switch chains duplicated across modules |
| Liskov | Keep subtype behavior substitutable | Hidden preconditions in implementations |
| Interface Segregation | Small focused interfaces | God interfaces with optional methods |
| Dependency Inversion | Depend on abstractions at boundaries | Concrete infrastructure leaking into business logic |

Python

```python
class PriceCalculator:
    def total(self, items: list[LineItem]) -> Decimal:
        return sum((item.total for item in items), start=Decimal("0"))
```

TypeScript

```ts
export interface PaymentGateway {
  charge(input: ChargeInput): Promise<ChargeResult>;
}
```

## Code Smells

| Smell | Signal | Refactor |
| --- | --- | --- |
| Long function | More than one phase or branching matrix | Extract helpers by intent |
| Primitive obsession | Raw strings for domain identifiers | Introduce value objects or typed aliases |
| Shotgun surgery | One rule changed in many files | Centralize policy |
| Boolean parameter explosion | `doThing(x, true, false, true)` | Split commands or use typed options |
| Dead code | Unreachable branches, unused exports | Delete it |

## Comment Philosophy

| Write Comments For | Do Not Comment |
| --- | --- |
| Non-obvious constraints | Syntax the reader can already see |
| External protocol quirks | Temporary debugging leftovers |
| Performance tradeoffs | Repeating function names in prose |
| Security-sensitive assumptions | Commented-out dead code |

BAD

```python
def normalize_email(email: str) -> str:
    # Lowercase the email
    return email.lower()
```

GOOD

```python
def normalize_email(email: str) -> str:
    # Login matching is case-insensitive across legacy providers.
    return email.strip().lower()
```

BAD

```ts
function handle(user: any, flag1: boolean, flag2: boolean) {
  if (flag1) {
    // ...
  }
}
```

GOOD

```ts
type HandleMode = "create" | "update";

interface HandleOptions {
  mode: HandleMode;
  sendNotification: boolean;
}

function handleUser(user: UserInput, options: HandleOptions) {
  if (options.mode === "create") {
    // ...
  }
}
```

## No Speculative Abstractions

| Situation | Preferred | Avoid |
| --- | --- | --- |
| Unused helper after refactor | Delete it in the same change | Leave for "future use" |
| One implementation today | Concrete type with clean seam | Factory + interface + registry on day one |
| Feature flag fully rolled out | Remove flag path | Carry stale branches indefinitely |

## Checklist

- [ ] Names encode domain meaning and read naturally
- [ ] Each function has one clear job
- [ ] Abstractions solve a present need, not a hypothetical one
- [ ] Comments explain why a constraint exists
- [ ] Unused code and commented-out blocks are removed
- [ ] Boolean argument lists are replaced with clearer APIs where needed
- [ ] Cross-module dependencies flow inward toward business logic
- [ ] Examples and tests still compile after refactors
