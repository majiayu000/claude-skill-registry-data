---
license: MIT
name: skimmable
description: "Enforce code readability and state minimisation before opening or updating a pull request. Use when code is functionally complete and needs a final simplification pass focused on skimmability: reducing arguments, removing optionality and overrides, collapsing unnecessary abstractions, preferring discriminated unions, adding assertions at boundaries, handling variants exhaustively, deleting incidental changes, and making the diff shorter, clearer, and easier to review."
---

# Skimmable

Review the change as if a tired reviewer must understand it in one fast pass.

Prefer deleting code to explaining code.

Keep the pass narrow: improve readability, state modelling, and diff clarity without changing product behaviour unless the current behaviour is obviously dead, redundant, or inconsistent with types.

## Checklist

Apply these rules aggressively:

1. Make the code obvious on first read.
2. Reduce the number of states the code can represent.
3. Reduce parameter count.
4. Remove optional parameters unless they are truly required by callers.
5. Replace boolean flags and loose option bags with discriminated unions when behaviour differs by mode.
6. Handle every known variant exhaustively.
7. Fail on unknown variants immediately.
8. Trust static types inside the typed core; do not add defensive branches for impossible states.
9. Assert at boundaries when loading data, parsing input, or reading external systems.
10. Prefer early returns over nested conditionals.
11. Keep functions cohesive; do not split logic into many tiny wrappers.
12. Avoid clever helpers, indirection, and generic abstractions.
13. Remove overrides, escape hatches, and customisation points unless there is a proven need.
14. Remove dead paths, temporary compatibility layers, and unrelated edits.
15. Bias toward fewer lines and fewer moving parts.

## Working method

Follow this order:

### 1. Trim the diff

Remove changes that do not help the main goal of the PR.

Delete:
- incidental renames
- opportunistic refactors
- styling churn with no behavioural value
- compatibility code for callers that no longer exist
- unused helpers, types, branches, and comments

If a simplification requires a separate behavioural decision, stop and call it out instead of smuggling it into the readability pass.

### 2. Simplify data shape first

Reduce complexity in types before touching control flow.

Prefer:
- required fields over optional fields
- one obvious input shape over many flexible ones
- discriminated unions over booleans or loosely related fields
- named domain types over generic maps and stringly typed objects

Ask of every argument:
- Is it required?
- Can it be derived?
- Can two arguments become one domain object?
- Is it just an override for an API that is too flexible?

### 3. Simplify control flow

Make happy paths short and visible.

Prefer:
- early returns
- straight-line code
- one level of indentation where possible
- local branching near use

Avoid:
- nested `if` pyramids
- defensive `else` branches for impossible states
- `try/catch` for expected values
- hidden branching spread across helper functions

### 4. Make invalid states loud

Assert at boundaries.

Use assertions when:
- decoding external data
- reading files, env vars, or request payloads
- converting untyped data into typed domain values
- checking invariants that must hold

After the boundary, write simple code that trusts the asserted shape.

### 5. Exhaust variants

When code depends on a variant, make the variant explicit and handle all cases.

Prefer a `switch` on a discriminant.

End with an exhaustive check or assertion if the language allows it.

Do not silently ignore unknown values.

### 6. Collapse unnecessary abstraction

Inline small one-use wrappers when they hide the real logic.

Keep helper functions only when they:
- remove real duplication
- encode a domain concept
- make the caller meaningfully clearer

Do not split a 20-line readable function into five 4-line helpers just to look tidy.

## Preferred patterns

### Keep arguments few and strict

Bad signs:
- more than 3 parameters
- multiple booleans
- optional callback plus optional overrides plus optional config
- passing values already available on an object

Prefer:
- one required object when the fields belong together
- one discriminated union when there are modes
- separate functions when the behaviours are actually different

### Prefer discriminated unions over booleans

If a boolean changes behaviour, model the behaviour directly.

Use:
- `kind: "draft" | "published"`
- `source: "cache" | "network"`
- `status: "idle" | "loading" | "success" | "error"`

Avoid:
- `isDraft`
- `useCache`
- `isLoading` plus `error` plus `data` on the same object unless the state machine truly permits all combinations

### Prefer assertions over defensive code

At boundaries, assert once. Inside, trust the assertion.

Avoid repetitive checks like:
- `if (!user) return`
- `if (!user.id) return`
- `if (typeof user.id !== "string") return`

when types and boundary validation already guarantee the shape.

### Prefer one obvious path

If there is a default behaviour, encode it directly.

Do not add overrides like `sortOrder = "desc"`, `strategy = "auto"`, `separator = ","`, `shouldLog = false` unless callers truly need them.

Every option multiplies states.

## Review prompts

Use these prompts during the pass:

- Can this function lose a parameter?
- Can this object lose an optional field?
- Can this branch become an early return?
- Can these two booleans become one union?
- Can this helper be inlined?
- Can this error path become an assertion at the boundary?
- Can this code fail loudly instead of guessing?
- Can this diff lose files or lines?
- If a reviewer skims this in 30 seconds, will the intent be obvious?

## Examples

### Reduce arguments and remove overrides

Before:

```ts
function createReport(
  userId: string,
  includeDrafts = false,
  sortBy: "date" | "name" = "date",
  sortDirection: "asc" | "desc" = "desc",
  limit?: number,
  overrides?: { timezone?: string; now?: Date }
) {
  const now = overrides?.now ?? new Date()
  const timezone = overrides?.timezone ?? "UTC"

  return buildReport({
    userId,
    includeDrafts,
    sortBy,
    sortDirection,
    limit,
    now,
    timezone,
  })
}
```

After:

```ts
type ReportScope =
  | { kind: "published" }
  | { kind: "all" }

function createReport(userId: string, scope: ReportScope) {
  return buildReport({ userId, scope, now: new Date(), timezone: "UTC" })
}
```

Prefer a smaller API. Add configurability only when a real caller needs it.

### Replace booleans with a discriminated union

Before:

```ts
type SaveState = {
  isSaving: boolean
  error?: string
  receipt?: string
}
```

After:

```ts
type SaveState =
  | { kind: "idle" }
  | { kind: "saving" }
  | { kind: "error"; message: string }
  | { kind: "saved"; receipt: string }
```

The second version prevents impossible combinations.

### Handle variants exhaustively

Before:

```ts
function badgeColor(status: Status) {
  if (status === "success") return "green"
  if (status === "error") return "red"
  return "gray"
}
```

After:

```ts
function badgeColor(status: Status) {
  switch (status) {
    case "success":
      return "green"
    case "error":
      return "red"
    case "pending":
      return "gray"
    default:
      return assertNever(status)
  }
}
```

Unknown variants should fail loudly during development.

### Assert at the boundary, trust inside

Before:

```ts
async function loadAccount(accountId: string) {
  const raw = await db.accounts.find(accountId)

  if (!raw) {
    throw new Error("Account not found")
  }

  if (typeof raw.email !== "string") {
    throw new Error("Invalid account email")
  }

  return raw
}

function sendWelcomeEmail(account: any) {
  if (!account) return
  if (!account.email) return
  mailer.send(account.email)
}
```

After:

```ts
async function loadAccount(accountId: string): Promise<Account> {
  const raw = await db.accounts.find(accountId)
  assert(raw, "Account not found")
  assert(typeof raw.email === "string", "Invalid account email")
  return raw as Account
}

function sendWelcomeEmail(account: Account) {
  mailer.send(account.email)
}
```

Validate once. Keep the typed core simple.

### Prefer early returns over nesting

Before:

```ts
function visibleItems(items: Item[], user?: User) {
  if (user) {
    if (user.isAdmin) {
      return items
    } else {
      return items.filter((item) => !item.hidden)
    }
  } else {
    return []
  }
}
```

After:

```ts
function visibleItems(items: Item[], user?: User) {
  if (!user) return []
  if (user.isAdmin) return items
  return items.filter((item) => !item.hidden)
}
```

Flatten the shape of the code.

### Do not split logic into too many tiny functions

Before:

```ts
function checkout(cart: Cart) {
  validateCart(cart)
  const subtotal = calculateSubtotal(cart)
  const tax = calculateTax(subtotal)
  const total = calculateTotal(subtotal, tax)
  return finalizeCheckout(total)
}

function calculateTotal(subtotal: number, tax: number) {
  return subtotal + tax
}
```

After:

```ts
function checkout(cart: Cart) {
  assert(cart.items.length > 0, "Cart is empty")

  const subtotal = sum(cart.items.map((item) => item.price))
  const tax = subtotal * TAX_RATE
  const total = subtotal + tax

  return finalizeCheckout(total)
}
```

Keep trivial logic close to use.

## PR gate

Before opening or updating the PR, verify:

- The diff contains only necessary changes.
- Public APIs are stricter or simpler, not more configurable.
- Modes are modelled explicitly.
- Variants are handled exhaustively.
- Assertions exist at boundaries.
- The core logic trusts types instead of re-checking everything.
- Functions read top-to-bottom with minimal nesting.
- Argument counts are low.
- Helpers exist only when they clarify.
- The final version is shorter, plainer, and easier to skim.

If a choice is between clever and obvious, choose obvious.

If a choice is between flexible and simple, choose simple.

If a choice is between adding code and deleting code, prefer deleting code.
