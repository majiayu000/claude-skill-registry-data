---
name: polish
description: Laravel polish. PHP/Laravel standards for each polish pass. Invoke when polishing PHP/Laravel code.
---

# Skill: Laravel Polish

> "Laravel code should read like the framework wrote it."

Seven passes. One concern each, in order — a naming issue spotted during the whitespace pass gets noted, then fixed in the naming pass. **Zero behavior change**: every test that passed before passes after. You are a copyeditor, not an author.

1. Docblocks · 2. Names · 3. Methods · 4. Framework internals · 5. Whitespace · 6. Conditionals · 7. Tests

Pairs with `kernel:polish` for the wider protocol — enumeration, reporting, team mode.

## Pass 1: Docblocks — The Craftsman Voice

**The trial**: read the method signature. Name, parameters with type-hints, return type. Does the signature tell the full story? If yes — delete the docblock.

**Survivors earn their place when they**:
- Refine types PHP can't express: `@param Collection<int, Order> $orders`
- Warn the caller: `@throws UnsupportedStateException`
- Link external docs: `@see https://stripe.com/docs/api/...`
- Clarify non-obvious constraints in one sentence

**Delete when they**:
- Restate `@param` types already in the signature
- Restate `@return` types already declared
- Say "Create a new instance" on constructors
- Narrate what the one-line body already shows
- Are longer than the method body

**Craftsman voice**: one line, present tense, verb-first. "Determine if...", "Resolve the...", "Build a...". Never "This method will...".

**The shape**: a comment block is one line or three. Never two, never four. Measured across 1,284 Laravel framework files — 74.7% of blocks are exactly 3 lines, 25% exactly 1, three exceptions in the entire framework. Comments are also rare: 0.6 blocks per file.

**Never cite a design document by section number.** `// See §7.9` rots the moment the document is renumbered, and it is a shape the framework never produces.

## Pass 2: Names — Zero Javaism

| Smell                              | Fix                                                                  |
|------------------------------------|----------------------------------------------------------------------|
| `get*()`/`set*()`                  | `lineAmount()` not `getLineAmount()`                                 |
| `*Manager`/`*Handler`/`*Processor` | What does it DO? `RefundsOrders`? `BuildsPayload`?                   |
| `*Helper`/`*Utility`               | Decompose into named methods or a trait with identity                |
| `*Interface` suffix                | `SyncableStore` — PHP doesn't need it                                |
| Over-qualified                     | In `Billing\Aggregation\`, just `BuildResult` — the namespace qualifies |
| Stuttering                         | `$config->mode` not `$exportConfig->exportMode`                      |
| Acronym casing                     | `HttpClient`, `XmlParser` — follow Laravel's `Http` convention       |

**Variables**: nouns, short, obvious. `$order`, `$transaction`, `$coverage`. No abbreviations (`$pmTotal` → `$paymentTotal`). `$item` is fine in a short closure.

## Pass 3: Methods — Return Stands Alone

When a method returns a fluent chain, `return` stands on its own line. The chain begins on the next line, reading top-to-bottom like a sentence.

**Extract when**: a blank line appears instinctively between "two things." That blank line is a method boundary.

**A condition is a named predicate**: what sits inside an `if` must read as a sentence. If it needs deciphering, it is a missing method. `if ($order->isRefundable())` — never `if ($order->status === Status::Paid && $order->paid_at !== null && ! $order->refunded_at)`. This adds a line and is still correct: the line buys a clearer call-site. See `ground-consumer-first`.

## Pass 4: Framework Internals

Reach for the framework before writing the loop. Every `foreach` that accumulates, filters, finds, groups, or transforms is a `Collection` method. Assign-then-return and create-modify-return are `tap()`. Null handling is `?->`, `??=`, and `config($key, $default)`. The full substitution table is in [examples.md](examples.md).

**QueryBuilders over scopes**: dedicated builder classes, not model scopes. Each method is one clause. They compose through chaining. The model stays lean — `newEloquentBuilder()` and nothing else.

**Model states** (`spatie/laravel-model-states`): use `whereState()` and the transition API. Never assign state fields directly. Never query raw column values.

## Pass 5: Whitespace — Import Grouping

Imports grouped logically: PHP classes, then Laravel classes, then domain classes. Blank line between groups. Alphabetical within each group. No inline FQCNs — if a class appears in the body, it belongs in the imports.

Classes breathe: properties, constructor, public methods, protected methods, private methods — each group separated.

## Pass 6: Conditionals

- `match` over `switch`. Always. `match` is an expression.
- `match` over if/elseif chains when branching on a single value.
- No `!== null` / `!== false` when truthiness suffices.
- Nullsafe `?->` over null checks.

## Pass 7: Tests

Defer to `pest:polish` for Pest-specific standards.

## Linter

Run `./vendor/bin/pint` on each file after editing. Pint handles formatting. You handle meaning.

---

See [examples.md](examples.md) for concrete before/after patterns.
