---
name: design-patterns
version: 1.1.2
description: Skeptical design-patterns catalog for Go and Python — which few still earn their place, which are anti-patterns. Consult before introducing a pattern, or when pushing back on a cargo-cult one.
---

# Design Patterns — Skeptical, Pragmatic Catalog

Most "design patterns" exist to work around missing language features. **Go and Python in 2026 don't need most of them.** This skill names what's still useful, what's covered by other skills, and what to actively avoid. Detail (code samples, anti-pattern rationale, language-specific smells) lives in [PATTERNS.md](PATTERNS.md). Companion to [ddd-architect](../../design/ddd-architect/SKILL.md), [hexagonal-architecture](../../design/hexagonal-architecture/SKILL.md), [logic-cleaner](../logic-cleaner/SKILL.md), [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md).

## 1. The framing

Patterns aren't free. Each one:

- Adds a name a future reader has to learn.
- Adds at least one type or function whose only purpose is the pattern.
- Promises a benefit (testability, swappability, polymorphism) that may not pay back if the abstraction has one implementation forever.

**Never introduce a pattern speculatively.** Wait for the *third* place that wants the same behavior (rule of three, per [logic-cleaner §6](../logic-cleaner/SKILL.md#6-duplication-rule-of-three)). One repetition is fine; two might be coincidence; three is a pattern asking to be extracted.

The "Gang of Four" book is a museum piece. Most of its patterns were workarounds for Java's lack of first-class functions, sum types, and structural typing. Modern Go has interfaces-where-used; modern Python has Protocols, dataclasses, and `match`. Neither needs Visitor, Abstract Factory, or Singleton-as-language-feature.

## 2. Patterns still worth knowing — summary

| Pattern | Use when | Skip when |
|---|---|---|
| **Repository** | Domain has aggregates with identity that need persistence | No domain layer — just functions reading/writing rows |
| **Adapter** | Dependency has ≥2 real implementations and a small interface surface | One implementation, no plausible second |
| **Strategy** (as function value) | Behavior varies per caller/context/environment | Single strategy + config flag would do it |
| **Decorator / middleware** | Concern is genuinely cross-cutting | Only one wrapped function — inline the concern |
| **Observer / pub-sub** (as domain events) | Multiple unknown consumers care about a state change | Exactly one consumer — call it directly |
| **Builder** | Many optional params, validation, multi-step assembly | 4 args fit on one line |
| **Factory method** | Caller can't know concrete type at compile time | Caller knows — call constructor directly |
| **Iterator** | Use the language feature (`iter.Seq`, generators) | — never reach for a separate class |

Code samples + rationale in [PATTERNS §1](PATTERNS.md#1-patterns-worth-knowing--detail).

## 3. Patterns to avoid (or replace) — summary

| Pattern | Replace with |
|---|---|
| **Singleton** | Dependency injection — pass instances to constructors |
| **Abstract Factory** | Discriminated union + parse function |
| **Visitor** | Python `match`, Go type switch / interface dispatch |
| **Chain of Responsibility** | Middleware chain (`func(handler) handler`) |
| **Mediator** | Domain events or direct calls |
| **Template Method** (inheritance) | Composition + functions/strategies passed in |
| **Prototype / Memento** | Native cloning + serialization |

Detail + worked examples in [PATTERNS §2](PATTERNS.md#2-patterns-to-avoid-or-replace--detail).

## 4. Patterns deferred to other skills

These are real patterns; this skill names them once and points to their owner:

| Pattern | Owner skill |
|---|---|
| Repository | [ddd-architect](../../design/ddd-architect/SKILL.md) §5 |
| Aggregate | [ddd-architect](../../design/ddd-architect/SKILL.md) §3–4 |
| Value Object | [ddd-architect](../../design/ddd-architect/SKILL.md) §3 |
| Domain Event | [ddd-architect](../../design/ddd-architect/SKILL.md) §6 |
| Anticorruption Layer | [ddd-architect](../../design/ddd-architect/SKILL.md) §8 |
| Ports & Adapters | [hexagonal-architecture](../../design/hexagonal-architecture/SKILL.md) |
| Middleware chain | [nethttp-architect](../../frameworks/nethttp-architect/SKILL.md) §7, [gin-architect](../../frameworks/gin-architect/SKILL.md) §9, [fastapi-architect](../../frameworks/fastapi-architect/SKILL.md) §8 |
| Functional options (Go) | [go-architect](../../languages/go-architect/SKILL.md) §3 |
| Dependency injection | [go-architect](../../languages/go-architect/SKILL.md) §11, [python-architect](../../languages/python-architect/SKILL.md) §3 |
| Iterator / generator | [go-architect](../../languages/go-architect/SKILL.md) §6 |

Don't restate them here — load the owner skill when the topic comes up.

## 5. Decision rules

When asked "should we apply pattern X?":

1. **Is the problem actually there yet?** Has it appeared at least three times? If not — wait. Premature patterns are the most expensive kind of debt because they make existing code more confusing without solving a real problem.
2. **Would a simpler language feature do?** A function value usually beats Strategy. `match` beats Visitor. A goroutine + channel beats Producer-Consumer-with-buffer-class. Reach for patterns *after* you've exhausted what the language gives you for free.
3. **Will there be a second implementation?** Patterns that introduce interfaces (Adapter, Strategy, Repository) only pay back if at least two implementations exist. One adapter is a hypothetical seam — and hypothetical seams are pure cost.
4. **Does it make the code easier to delete?** Good patterns concentrate change — touch one place when the rule evolves. Bad patterns spread change — every variation needs N synchronized files updated.
5. **Does the name carry weight?** "It's a Repository" tells a future reader the persistence shape immediately. "It's a Manager" / "Helper" / "Service" tells them nothing. Use named patterns when the name is genuinely informative; invent ad-hoc structure when no standard name fits.

If the answer to (1) is "no" or to (3) is "no", **skip the pattern** and revisit when reality has caught up.

## 6. Code-smell → pattern map

Quick lookup; see [PATTERNS §3](PATTERNS.md#3-code-smell--pattern-map) for the full table. The pattern is the *option*, not the answer. Always check the decision rules in §5 first.

## 7. Language-specific anti-patterns

Go and Python each have their own list of "looks like a pattern, is actually a smell" — see [PATTERNS §4](PATTERNS.md#4-language-specific-anti-patterns). Highlights:

- **Go:** `any` everywhere, empty struct receivers, returning interfaces from constructors.
- **Python:** `@staticmethod`-only classes, inheritance for reuse, metaclass magic, `*args/**kwargs` passthrough.

## 8. When a pattern hardens into a convention

If a pattern appears across many skills and projects in this repo (Repository everywhere, Middleware in every HTTP framework), it stops being a "design pattern" decision and becomes a **convention** encoded in the architect skill for that area. Read the architect skill first; this catalog is for when you're in genuinely new territory.

## Further reading

- Erich Gamma, Richard Helm, Ralph Johnson and John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software* (Addison-Wesley, 1994), the source of the catalogue this skill is skeptical of.
