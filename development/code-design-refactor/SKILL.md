---
name: code-design-refactor
version: 1.0.0
description: Design-level refactoring rules — extraction, decoupling, SRP, encapsulation, primitive obsession. Language-agnostic. Sits between logic-cleaner (expression-level) and improve-codebase-architecture (system-level). Use when restructuring existing code at the module/class/function level.
---

# Code Design Refactor

The **design-level** rung of the refactoring ladder. Tighter scope than [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md) (which surveys friction across the whole codebase), broader than [logic-cleaner](../logic-cleaner/SKILL.md) (which polishes inside a function). When a class is doing too much, when a function takes a tuple of primitives that ought to be a value object, when two modules know too much about each other — that's this skill's job.

## 1. Scope boundary

| Skill | Operates on | Asks |
|---|---|---|
| [logic-cleaner](../logic-cleaner/SKILL.md) | Expressions, single function bodies | "Is this branch readable? Is this conditional negated?" |
| **`code-design-refactor`** | Functions, classes, modules within one package | "Does this thing have one reason to change? Is the seam in the right place?" |
| [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md) | The whole codebase, multiple modules, deep architectural drift | "Where are the shallow modules across the project? Where's the friction?" |

If a finding requires renaming a primitive boolean variable, use `logic-cleaner`. If it requires moving responsibilities between modules across the codebase, use `improve-codebase-architecture`. This skill handles the middle.

## 2. When to invoke

- User asks to "clean up", "tidy", "refactor", "restructure" a specific function / class / module.
- A code review surfaces a too-big function or a class doing too many things.
- A test is hard to write because the unit under test is the wrong shape.
- A new feature reveals an existing module is shaped wrong for what it must now do.
- Logic-cleaner's §7 (out-of-scope) explicitly points here.

## 3. Refactoring discipline

Three rules that govern *every* refactor, regardless of which specific move:

1. **Tests first.** Don't refactor without coverage of the behavior being preserved. If tests are missing, write them — *characterization tests* that capture current behavior, even if behavior is "wrong" — before changing structure.
2. **One move at a time.** A refactor is a sequence of small, mechanical, behavior-preserving edits. Each edit leaves the tree green. Compound moves (rename + extract + reorder + delete) are bug factories.
3. **Commit each successful move.** Commits are cheap; rebuilding context after a bad merge is expensive. Per [commit-author](../commit-author/SKILL.md): `refactor(scope): <move>`.

## 4. Extract

The most common move. Pull a coherent chunk into its own named thing.

- **Extract function/method** — when a comment is needed to explain a block, the function name should *be* the comment. Name describes intent (`is_eligible_for_discount`), not mechanics (`check_status_and_total`).
- **Extract class** — when a function takes 6+ arguments and several mean nothing without the others. The grouping is a class.
- **Extract module/package** — when a folder's files have two clusters of responsibility that share nothing. Split.
- **Stop extracting when** further splits produce things that exist only to be called from one place and nothing else. The extracted thing must earn its name.

## 5. Decouple

When two modules know more about each other than they should.

- **Direct → indirect through a port.** If A imports concrete B but only needs *some* behavior, A should declare the interface it needs and let B (or a test fake) implement it. Aligns with [hexagonal-arch §3](../../design/hexagonal-arch/SKILL.md#3-where-to-put-port-definitions): the interface lives where it's *consumed*.
- **Two-way → one-way.** If A imports B and B imports A, the design is wrong. Find the higher-level concept they both belong to, or invert the dependency.
- **Pass dependencies, don't fetch them.** Replace `service = SomeRegistry.get()` with `def __init__(self, service: SomeService)`. Makes testing trivial and dependencies visible.
- **Don't decouple speculatively.** The "rule of three" (per [logic-cleaner §6](../logic-cleaner/SKILL.md#6-duplication-rule-of-three)) applies: one consumer = no need for a port; two = possibly; three = yes.

## 6. SRP — single responsibility

The classic rule, sharpened: **one reason to change**. A class with three reasons to change has three responsibilities, even if they all "look related."

Signs a thing has too many responsibilities:

- The class name is `<Noun>Manager`, `<Noun>Service`, `<Noun>Helper` — the suffix is hiding what it actually does.
- Methods can be partitioned into groups that share nothing (no common state, no common collaborators).
- Tests are split into multiple files, each exercising a different facet.
- The class is imported by many unrelated callers, each using only a slice of its surface.

The fix is **extract class** per §4, with the new classes named after the responsibilities you discovered.

## 7. Encapsulation

Restrict access to internal state; force callers through the methods.

- **Make fields private by default.** Public attributes (Python) / exported fields (Go) are leaks unless they're genuinely part of the contract.
- **Replace getter+setter pairs with intention-revealing methods.** Don't `user.setStatus("active")`; do `user.activate()`. The method enforces the rule that comes with the state change.
- **Tell, don't ask.** Instead of `if order.status == "draft": order.confirm()`, write `order.confirm_if_draft()` and let the aggregate enforce its own invariants. Aligns with [ddd-architect](../../design/ddd-architect/SKILL.md): behavior on the aggregate, not on the caller.

## 8. Primitive obsession

When a primitive carries hidden meaning across the codebase, **make it a value object** (per [ddd-architect §3](../../design/ddd-architect/SKILL.md#3-tactical-ddd--building-blocks)).

Symptoms:

- The same validation runs everywhere a `string` named `email` is created.
- A `string` `currency_code` is occasionally passed as a `country_code` because the type system can't tell them apart.
- A function takes `int, int, int` and only the parameter names tell you which is `year`, `month`, `day`.

The fix is a tiny immutable type:

```python
@dataclass(frozen=True, slots=True)
class Email:
    value: str
    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError(f"invalid email: {self.value!r}")
```

```go
type Email string

func NewEmail(s string) (Email, error) {
    if !strings.Contains(s, "@") {
        return "", fmt.Errorf("invalid email: %q", s)
    }
    return Email(s), nil
}
```

The validation now lives at construction; every call site receives an `Email` that's been validated; type confusion (`Email` passed where `Username` is expected) is a compile error in Go, a clear runtime error in Python.

## 9. Refactors to skip

Not every refactor is worth doing.

- **No coverage.** Don't restructure code that has no tests; you can't verify behavior is preserved. Write characterization tests first, then refactor.
- **The "improvement" is ambiguous.** If two reviewers would each pick a different shape, the current shape is fine. Refactor when the win is clear.
- **The code is about to be deleted.** Don't polish code that's leaving in a week.
- **Behavior is about to change.** If a feature next sprint will restructure the area anyway, wait. Refactoring + feature in the same diff is a review nightmare.
- **The refactor crosses module boundaries.** Promote to [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md) — it owns codebase-level restructuring.

## 10. Workflow

Each refactor is a tiny loop, not a big-bang change.

1. Confirm tests cover the behavior. Add characterization tests if needed.
2. Pick **one** move (extract, decouple, rename, encapsulate, replace primitive).
3. Apply it mechanically. Run tests. They pass.
4. Commit. Move to the next.
5. Stop when the next move's win isn't obvious. Better to stop early than refactor speculatively.

When a refactor reveals a deeper structural problem (port belongs in a different module; the responsibility split spans several packages), stop and hand off to [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md). Don't expand scope.

## 11. Cross-skill ties

- [logic-cleaner](../logic-cleaner/SKILL.md) — expression-level companion; surface upward when a finding requires structural change.
- [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md) — system-level companion; promote when scope crosses module boundaries.
- [tdd](../tdd/SKILL.md) — refactor phase of the red-green-refactor loop.
- [ddd-architect](../../design/ddd-architect/SKILL.md) — value objects, aggregates, encapsulation in the domain context.
- [hexagonal-arch](../../design/hexagonal-arch/SKILL.md) — decoupling through ports; dependency direction.
- [commit-author](../commit-author/SKILL.md) — every successful move gets its own `refactor(scope):` commit.
