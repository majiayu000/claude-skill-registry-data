---
name: type-driven-development
description: Encodes invariants in the type system so illegal states cannot be constructed. Picks between newtypes, smart constructors, discriminated unions, and phantom types based on the invariant being protected. Audits code for primitive obsession, boolean blindness, stringly-typed data, partial functions, and validation that should be parsing. Decides what belongs in types (structure, identity, state, ordering) versus tests (behaviour, IO, time). Triggers on "type-driven development", "type first", "make illegal states unrepresentable", "illegal state", "parse don't validate", "smart constructor", "branded type", "newtype", "phantom type", "discriminated union", "sum type", "algebraic data type", "adt", "exhaustiveness", "never type", "refinement type", "primitive obsession", "boolean blindness", "stringly typed", "partial function", "encode invariant", "types as tests", "type safety", "as const", "satisfies".
---

# Type-Driven Development

Owns the question "can this bug be expressed in the type system?". If yes, the type system catches it on every build, on every machine, forever. If no, a test must cover it. The job is to maximise the first set before reaching for the second.

## Mode Router

Pick one mode per invocation. If ambiguous, ask.

| Mode | Use when | Output |
|------|----------|--------|
| **Design** | A new domain concept, state machine, or API surface is being modelled | Type sketch in target language, listed invariants each constructor enforces, list of behaviours still needing tests |
| **Refactor** | An existing primitive, boolean flag, or shape carries an invariant the type does not enforce | Diff: old shape → new shape, call-site impact, migration order |
| **Audit** | A module is suspected of relying on convention rather than the compiler | Tiered findings (Blocker / High / Medium) with the rule each violates and the smallest fix that lifts the invariant into the type |
| **Decide** | A check could live in the type system or in tests | Verdict with the criterion that decided it (see "Types vs Tests") |

## Core invariants

These hold across every language with a static type system. Violating any of them produces tests that compensate for missing types.

1. **A constructible illegal state is an unfixed bug.** If the type allows it, somewhere in the codebase or its future, something will build it.
2. **Parse, do not validate.** A validation function that returns `boolean` and leaves the input typed as the unrefined form proves the check happened but loses the proof. A parser that returns the refined type carries the proof forward.
3. **Once parsed, never re-validate.** Re-checking a value of a refined type means the type does not actually carry the invariant. Either the type is wrong or the second check is dead.
4. **Make the right thing easy and the wrong thing impossible — in that order.** A type that requires a one-line cast to misuse is failing its job. Casts and `any`/`unknown`/`unsafe` escape hatches are audit signals.
5. **One representation per state.** If a state can be expressed two ways, both will appear in the codebase and they will diverge. Pick a canonical encoding; collapse the rest.
6. **Optional is not a state.** `T | undefined` says "this field may be missing"; it does not say *why*. When the absence carries meaning, encode the meaning, not the absence.
7. **Exhaustiveness must be checked, not assumed.** A `switch` over a union without a `never`-typed default is one new variant away from a silent fallthrough.
8. **The type is the documentation that cannot rot.** A comment saying "must be non-empty" rots the moment someone empties it. A `NonEmptyArray<T>` does not.

## In this library, the types *are* the product

`react-basics-ui` ships `dist/index.d.ts` (~243 KB) alongside the JavaScript.
Its types are not internal scaffolding — they are the API consumers program
against, and the surface their editors autocomplete. Two consequences:

**1. A loose prop type is a permanent liability.** In an application you can fix a
bad type and update the twelve call sites. Here you cannot see the call sites, and
tightening a published type is a breaking change. Get it right before release, or
accept living with it until the next major.

**2. Illegal states cost more here.** `variant` and `styleVariant` both accepting
arbitrary strings means every consumer's typo becomes a silently unstyled element.
The library already applies the moves below:

| Move | Where it shows up |
|---|---|
| Discriminated union | `BadgeStyleVariant`, `StatusVariant`, `TableCellAlign` — closed unions, never `string` |
| Shared canonical union | `ComponentSize`, `GranularSize`, `OverlaySize` in `shared/types` — one representation per concept, library-wide |
| Shared option shape | `SelectOption` — one representation reused by every option-taking component |
| Exhaustiveness | Class maps typed `Record<Union, string>`, so adding a union member fails the build until every map is updated |

That last one is the highest-leverage pattern in this codebase: typing a
`.styles.ts` map as `Record<BadgeColor, string>` rather than a bare object makes
the type system enforce that every variant has a style. Prefer it to a lookup with
a fallback, which silently renders the wrong thing.

The escape-hatch row in the cheatsheet is worth grepping periodically —
`as`, `any`, and `@ts-ignore` in a `.types.ts` file are load-bearing on consumers.

## The four moves

Almost every type-driven refactor reduces to one of these. Pick by the invariant being protected, not by the language feature available.

### 1. Newtype / branded type — *protects identity*

Use when two values share a runtime representation (both `string`, both `number`) but should never be interchangeable. `UserId` and `OrderId` are both `string` at runtime; passing one where the other is expected is a bug the compiler can catch for free.

```typescript
type UserId = string & { readonly __brand: "UserId" };
type OrderId = string & { readonly __brand: "OrderId" };
```

```python
from typing import NewType
UserId = NewType("UserId", str)
OrderId = NewType("OrderId", str)
```

```rust
struct UserId(String);
struct OrderId(String);
```

Audit signal: any function that takes two parameters of the same primitive type in a row (`transfer(from: string, to: string, amount: number)`).

### 2. Smart constructor — *protects construction*

Use when a value of a type is only valid under a runtime condition (non-empty, in range, parseable, normalised). Hide the bare constructor, expose a parser that returns the refined type or an error.

```typescript
class Email {
  private constructor(readonly value: string) {}
  static parse(s: string): Email | null {
    return /^[^@]+@[^@]+$/.test(s) ? new Email(s) : null;
  }
}
```

Once a function takes `Email`, no caller can hand it `"hello"`. The check happens once at the edge of the system.

Audit signal: the same regex / range check appearing in more than one place.

### 3. Discriminated union / sum type — *protects state machines*

Use when a value is in exactly one of several states and each state carries different data. Replace bag-of-optionals with a tagged union.

Wrong: every field optional, every state combination representable.

```typescript
type RequestState = {
  loading?: boolean;
  data?: User;
  error?: Error;
};
```

Right: states are mutually exclusive, fields are present only when they make sense.

```typescript
type RequestState =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "success"; data: User }
  | { kind: "error"; error: Error };
```

```python
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class Idle: kind: Literal["idle"] = "idle"
@dataclass(frozen=True)
class Loading: kind: Literal["loading"] = "loading"
@dataclass(frozen=True)
class Success: data: User; kind: Literal["success"] = "success"
@dataclass(frozen=True)
class Error: error: Exception; kind: Literal["error"] = "error"

RequestState = Idle | Loading | Success | Error
```

```rust
enum RequestState {
    Idle,
    Loading,
    Success(User),
    Error(io::Error),
}
```

Always pair with an exhaustiveness check at the point of consumption:

```typescript
function assertNever(x: never): never { throw new Error(`unhandled: ${x}`); }
switch (state.kind) {
  case "idle": ...
  case "loading": ...
  case "success": ...
  case "error": ...
  default: return assertNever(state);
}
```

Audit signal: a single object where multiple fields are `?` and a comment explains which combinations are legal.

### 4. Phantom type — *protects ordering of operations*

Use when the same runtime data must be treated differently depending on processing stage (validated vs raw, sanitised vs untrusted, authenticated vs anonymous, transactional vs free-standing). The phantom parameter has no runtime cost; it only exists to make the compiler refuse the wrong call.

```typescript
type Tagged<T, Tag> = T & { readonly __tag: Tag };
type Raw<T> = Tagged<T, "raw">;
type Validated<T> = Tagged<T, "validated">;

declare function validate<T>(x: Raw<T>): Validated<T> | null;
declare function persist<T>(x: Validated<T>): Promise<void>;

// persist(rawInput);            // compile error
// persist(await validate(raw)); // works once null is handled
```

```rust
struct Connection<State> { /* ... */ _state: PhantomData<State> }
struct Open; struct Closed;

impl Connection<Open>   { fn send(&self, msg: &str) { /* ... */ } }
impl Connection<Closed> { fn open(self) -> Connection<Open> { /* ... */ } }
// closed_conn.send(...)  // compile error
```

Audit signal: comments of the form "only call X after Y", or a function that throws when called in the wrong order.

## Types vs Tests — the decision

A check belongs in the type system if **all four** hold. Otherwise it belongs in a test.

1. The property is **structural** — expressible in terms of shape, cardinality, identity, presence, or ordering — not behavioural.
2. The property is **decidable at compile time** — the compiler can prove it without running code.
3. The property must hold in **every** program path — not just the tested ones.
4. The cost of expressing it in the type system is **smaller than the cost of writing and maintaining tests for every call site** that could violate it.

Examples:

| Property | Owner | Why |
|----------|-------|-----|
| `Email` is well-formed | Type (smart constructor) | Structural; one check at the boundary protects all call sites |
| `UserId` is not confused with `OrderId` | Type (newtype) | Identity; the compiler proves it for free |
| A request transitions `idle → loading → (success \| error)` and not backwards | Type (discriminated union + transition functions) | Cardinality + ordering |
| Sending a message requires an open connection | Type (phantom type) | Ordering of operations |
| The retry function backs off exponentially | Test | Behavioural, not structural |
| The cache evicts least-recently-used items | Test | Behavioural |
| Two services agree on the wire format | Contract test (or generated types from a shared schema) | Crosses a process boundary the local compiler cannot see |
| `divide(a, b)` returns `a/b` | Test | Behavioural |
| `divide(a, b)` rejects `b = 0` at compile time | Type (refinement / `NonZero<T>`) | Structural; if the language supports it |

If a check fits the type system but the language cannot express it cheaply, that is a language constraint, not a design one — note it and fall back to a test plus a comment naming the invariant.

## Audit signals

Each row is a smell, the underlying defect, and the move that fixes it.

| Signal | Defect | Move |
|--------|--------|------|
| `function f(a: string, b: string, c: string)` | Primitive obsession — three values share a type but not a meaning | Newtype each one |
| `function send(user, force: boolean, silent: boolean)` called as `send(u, true, false)` | Boolean blindness — call site is unreadable, swapped args compile | Replace with a discriminated union of intents, or two named functions |
| `if (status === "active")` where `status: string` | Stringly typed — the set of valid values is in someone's head | Lift to a literal union or enum, exhaustive-check at all branches |
| `{ data?: T; error?: E; loading?: boolean }` | State combinations not actually reachable are still representable | Discriminated union |
| `validate(x): boolean` followed by using `x` as if validated | Validation drops the proof | Convert to parser: `parse(x): Refined \| null` |
| `function get(k): T` throws on missing key | Partial function — the failure mode is invisible | Return `T \| null` / `Option<T>` / `Result<T, E>` |
| Cast, `any`, `unknown`, `unsafe`, `// @ts-ignore`, `# type: ignore` | Escape hatch — types disabled at a point | Find what the type wants to say and say it; if truly impossible, isolate the cast at the boundary and document why |
| Comment of the form "must be non-empty / non-negative / sorted / open" | Invariant the type does not enforce | Move the invariant into a type (`NonEmpty<T>`, `Sorted<T>`, phantom state) |
| `switch` without a `never` default | Exhaustiveness not enforced | Add the default; pick up the new variants the compiler then flags |
| Two functions, same shape, "one returns a UUID, the other a slug" | Identity collision | Newtype both |

## Workflow

1. **State the invariant in one sentence.** "An order cannot be paid twice." "A connection must be open before sending." "A user id is never an order id."
2. **Classify the invariant.** Structural (newtype, discriminated union), constructive (smart constructor), ordering (phantom type), refinement (range, length, regex).
3. **Pick the smallest move that lifts it.** Prefer newtype over phantom type, phantom type over codegen, codegen over runtime assertion.
4. **Make the right thing the only thing.** Remove the un-refined constructor from the call site, or hide it behind the parser.
5. **Run the compiler.** Each error is a place the old code relied on the invariant being absent. Fix or annotate every one before moving on.
6. **Delete the tests the type now subsumes.** A test that asserts "rejects empty string" against a `NonEmptyString` parameter is dead — the call cannot happen.
7. **List what remains.** Behavioural, integration, IO, performance, time-dependent — that is the residue that still needs tests.

## Anti-patterns

- **Type theatre.** Layers of generics that obscure intent without ruling out more states. If a reader cannot say in one sentence what an illegal state would look like, simplify.
- **Refining at the wrong boundary.** Validating at the database layer when the value travelled through three other layers as a raw string. Parse at the system edge — wherever untrusted data enters — and never again.
- **Casting through the invariant.** Adding a smart constructor and then exposing an `unsafeConstruct` for tests. The tests will leak into production code within a release.
- **Boolean flag accretion.** `f(x, true, false, true)`. Each flag wants to be a state in a discriminated union or its own function.
- **Modelling state with strings.** `status: string` with documentation listing values. Always a literal union or enum.
- **Tagging without exhaustiveness.** A discriminated union with no `never` default — the compiler shrugs when a new variant is added.
- **Validation that mutates.** Trimming or normalising inside a `boolean`-returning validator. Hide normalisation in the parser; expose the canonical form as the only output.
- **Optional everywhere.** When more than two fields on a record are optional, a discriminated union almost certainly fits better.
- **Tests that re-prove the type.** "It rejects negative numbers" against a `NonNegative` parameter. Delete.

## Language-shape cheatsheet

This is not exhaustive — it lists the construct each language reaches for first.

| Move | TypeScript | Python | Rust | Haskell / OCaml |
|------|------------|--------|------|-----------------|
| Newtype | `string & { __brand: "X" }` | `NewType("X", str)` | `struct X(String);` | `newtype X = X String` |
| Smart constructor | `private constructor` + static `parse` | `@dataclass(frozen=True)` + classmethod `parse` | private field + `pub fn parse` | smart constructor + module export list |
| Discriminated union | `\| { kind: "a" } \| { kind: "b" }` | `Literal` tags + `Union` / `match` | `enum` with variants | `data T = A \| B \{...\}` |
| Phantom type | `T & { __tag: "X" }` | `Generic[State]` (limited) | `PhantomData<State>` | type parameter with no constructor |
| Exhaustiveness | `assertNever(x: never)` | `assert_never` / `match` with `case _ as _:` raising | `match` is total | compiler warning, then error |
| Opt-in escape | `as`, `any`, `// @ts-ignore` | `cast`, `# type: ignore` | `unsafe` | `unsafeCoerce` |

Use the escape row to grep for places the type system was waived.
