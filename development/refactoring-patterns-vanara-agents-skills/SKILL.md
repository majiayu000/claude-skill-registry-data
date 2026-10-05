---
name: refactoring-patterns
description: Improve code structure without changing behavior — the discipline of small, named, test-backed moves. Extract function/variable, inline, rename, replace conditional with polymorphism, introduce parameter object, guard clauses. Recognize smells, refactor safely, avoid big-bang rewrites.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# Refactoring Patterns

Refactoring is **changing the internal structure of code without changing its observable behavior**. It
is not "cleanup whenever," and it is not rewriting. It is a disciplined sequence of small, *named*,
behavior-preserving moves, each verified by tests, each committable on its own. Done right it is nearly
risk-free; done wrong — without tests, mixed with feature work, or as a big-bang rewrite — it is one of
the most reliable ways to ship a regression.

This skill is the deep reference for that discipline: the safety net that makes it possible, the named
moves themselves, the smells that signal where to apply them, and the trade-offs of when *not* to. Heavy
detail lives in `references/`; copy-paste before/after material in `examples/`; a runnable smell detector
in `scripts/`.

## The mental model

Two hats, never worn at once (Kent Beck's rule): you are either **adding behavior** (new tests go red,
then green) *or* **refactoring** (all tests stay green the whole time). Switching hats mid-edit is the
root cause of most refactoring disasters, because when a test breaks you can no longer tell whether your
*restructuring* was wrong or your *new feature* was wrong.

| Question | Refactoring answer |
|---|---|
| What changes? | structure only — names, shape, location |
| What stays identical? | observable behavior, the public contract, test results |
| How do I stay safe? | tests green before, green after, green between every step |
| How big is a step? | small enough that a broken test points at one change |
| When do I commit? | after each move that leaves the suite green |

## 1. Tests are the safety net (non-negotiable)

You cannot refactor code you cannot verify. Before touching structure, ensure a **green** test suite
exercises the behavior you're about to move. If coverage is missing, write **characterization tests**
first — tests that pin down what the code *currently* does (even if that's arguably wrong), so any
behavior drift during refactoring surfaces immediately. See `references/safe-workflow.md` for the
red-green-refactor loop, characterization testing, and the strangler-fig pattern for large systems.

The loop:

1. Run the suite — confirm green.
2. Apply **one** named refactoring.
3. Run the suite — confirm still green.
4. Commit.
5. Repeat.

If step 3 goes red, you have exactly one small change to undo. That is the entire value proposition.

## 2. Smells: knowing *where* to refactor

Refactoring is demand-driven — you don't refactor everything, you refactor what a **code smell** is
pointing at. The catalogue in `references/code-smells.md` is the full list; the high-frequency ones:

- **Long method / long function** — does too much; the body has comment-delimited "paragraphs."
- **Large class / god object** — too many fields and responsibilities; low cohesion.
- **Feature envy** — a method that reaches into another object's data more than its own.
- **Primitive obsession** — strings/ints standing in for real concepts (`string currency`, `int cents`).
- **Shotgun surgery** — one conceptual change forces edits in many scattered places.
- **Duplicated code** — the same logic in three spots (the rule of three: extract on the third copy).

## 3. The named moves

Each refactoring has a **name** and a **mechanics** (a precise step sequence). Naming them lets a team
say "extract a function here" and share an exact, low-risk procedure. The full catalogue with mechanics
is in `references/refactoring-catalog.md`. The core set:

- **Extract Function** — pull a coherent block into its own named function.
- **Inline Function/Variable** — the inverse, when the indirection earns nothing.
- **Rename** — the highest-value, lowest-risk move; a precise name deletes a comment.
- **Extract Variable** — name a sub-expression to explain it.
- **Replace Conditional with Polymorphism** — swap a type-switch for dispatch on a type.
- **Introduce Parameter Object** — bundle a clump of args that always travel together.
- **Replace Magic Literal with Constant**, **Decompose Conditional**, **Replace Nested Conditional with
  Guard Clauses**, **Move Function/Field**, **Separate Query from Modifier**.

### Before / after: Extract Function + guard clauses

A long function doing validation, calculation, and formatting at once:

```js
// before — one function, three jobs, deep nesting
function invoiceLine(item) {
  if (item) {
    if (item.qty > 0) {
      let total = item.qty * item.price;
      if (item.taxable) { total = total * 1.2; }
      return `${item.name}: $${total.toFixed(2)}`;
    }
  }
  return "invalid";
}
```

```js
// after — guard clauses flatten nesting; intent-named helpers
function invoiceLine(item) {
  if (!isValid(item)) return "invalid";
  return format(item.name, totalFor(item));
}

const isValid   = (i) => i && i.qty > 0;
const totalFor  = (i) => i.taxable ? i.qty * i.price * 1.2 : i.qty * i.price;
const format    = (name, total) => `${name}: $${total.toFixed(2)}`;
```

Same inputs, same outputs — tests stay green — but each piece now has one job and a name.

### Before / after: Replace Conditional with Polymorphism

```ts
// before — the switch will grow with every new type; shotgun surgery waiting to happen
function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.r ** 2;
    case "square": return shape.side ** 2;
    default: throw new Error("unknown shape");
  }
}
```

```ts
// after — each type owns its behavior; adding a shape is additive, not invasive
interface Shape { area(): number; }
class Circle implements Shape { constructor(private r: number) {} area() { return Math.PI * this.r ** 2; } }
class Square implements Shape { constructor(private side: number) {} area() { return this.side ** 2; } }
// new shapes add a class; no existing code is touched (Open/Closed)
```

See `examples/` for both of these as standalone, runnable files.

## 4. Common pitfalls (failure modes)

- **Refactoring without tests.** The cardinal sin. With no safety net you are *rewriting and hoping*.
  Write characterization tests first or do not start.
- **Wearing both hats.** Mixing a refactor with a behavior change in the same commit. When something
  breaks you can't bisect *which* intent caused it, and reviewers can't see the real change in the diff.
  Keep refactor commits and feature commits separate.
- **Big-bang rewrites.** "Let's just rewrite it cleanly" discards hard-won, battle-tested edge-case
  knowledge and ships with no incremental safety. Prefer the **strangler fig**: grow the new structure
  around the old, route traffic over piece by piece, delete the old when nothing calls it.
- **Steps too big.** If a "step" touches 30 files before you re-run tests, a red bar tells you nothing
  useful. Shrink the step.
- **Refactoring on a feature branch for weeks.** Long-lived refactor branches rot against `main` and
  produce merge nightmares. Land small refactors continuously.
- **Speculative generality** — extracting abstractions "for the future" no caller needs yet. Refactor
  toward concrete, present demands (YAGNI).

## 5. When NOT to refactor / trade-offs

- **No tests and no time to write them** for code you don't understand — refactoring here is gambling.
  Add characterization tests first, or leave it alone.
- **Code you're about to delete** — don't polish a corpse.
- **Stable code nobody touches and nobody complains about** — clean for clean's sake has no payoff;
  refactor when you're *already* in the area for a feature or fix (the "campsite rule").
- **A hard deadline shipping today** — note the debt, ship, refactor next iteration. Be honest that this
  is borrowing, not free.
- **Refactor vs. rewrite:** rewrite only when the design is fundamentally wrong for current
  requirements *and* you can carve off a strangler-fig seam. Otherwise incremental refactoring is almost
  always cheaper and safer than a rewrite.

## Files in this package

- `references/code-smells.md` — the smell catalogue (long method, large class, feature envy, primitive
  obsession, shotgun surgery, and more) with the move each one calls for.
- `references/refactoring-catalog.md` — named refactorings with their step-by-step mechanics.
- `references/safe-workflow.md` — red-green-refactor, characterization tests, strangler fig, the two hats.
- `examples/extract-function.before-after.js` — long function → extracted, named helpers.
- `examples/replace-conditional-with-polymorphism.before-after.ts` — type-switch → dispatch.
- `scripts/detect-smells.mjs` — runnable Node scanner that flags long functions and deep nesting
  (`--selftest` for built-in cases).

Pairs with the `error-handling-patterns` skill (refactor toward explicit error handling), the
`testing-patterns` skill (the safety net), and the `code-reviewer` and `refactor-cleaner` agents.
