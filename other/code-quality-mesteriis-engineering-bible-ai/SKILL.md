---
name: code-quality
description: "Reviews cohesion, naming, responsibility, complexity, and maintainability. Do not use as a default companion to every code change."
---

# Skill: code-quality

## Purpose

Keep code cohesive, explicit, maintainable, testable, and appropriately small.

This skill encodes SOLID, KISS, DRY, YAGNI, cohesion, coupling, and size discipline as practical rules rather than motivational office posters.

## Single Responsibility at Every Level

### Function

A function should do one coherent thing.

A function is suspicious when it:

- validates input;
- performs I/O;
- applies domain rules;
- mutates persistence;
- formats output;
- logs business events;
- handles retries;

all in one place.

Split by responsibility, not by arbitrary line count.

### Class / Type

A class/type should represent one role:

- domain state;
- lifecycle;
- policy;
- adapter;
- interface implementation;
- dependency grouping;
- stateful workflow.

Avoid god objects, vague managers, and classes that are just bags of unrelated methods.

### File / Module

A file/module should have one cohesive theme.

A file is suspicious when it contains:

- unrelated domain concepts;
- mixed layers;
- many independent public entry points;
- repeated section headers needed to understand it;
- several classes that change for unrelated reasons.

Do not create a `utils`, `helpers`, `common`, or `misc` dumping ground unless the repository already has that convention and the new code still has a cohesive purpose.

### Package / Component

A package/component should expose a clear public boundary.

It should not be a directory-shaped junk drawer.

Prefer package boundaries around:

- domain subareas;
- application use cases;
- infrastructure adapters;
- integration clients;
- UI/presentation areas;
- hardware responsibilities.

### Layer

A layer should have one architectural responsibility.

Do not mix transport, domain, persistence, configuration, and presentation concerns.

### Bounded Context

A bounded context should own one domain language and one model of reality.

Do not leak terms and invariants across contexts accidentally.

## Size Limits

Human-authored 10k-line files are forbidden.

Default thresholds for human-authored source:

- function over 60 logical lines: suspicious;
- function over 100 logical lines: split or justify;
- class/type over 300 logical lines: suspicious;
- class/type over 500 logical lines: split or justify;
- file/module over 800 logical lines: split or justify;
- file/module over 1,500 logical lines: strong refactor candidate;
- file/module over 10,000 logical lines: unacceptable except generated/vendor/lock content.

Generated, vendored, lock, and machine-produced migration files may be exceptions.

If a large file is unavoidable, document why and isolate growth behind clear sections or generated boundaries. Better yet, do not make it unavoidable. Humanity has suffered enough.

## KISS

Prefer simple, direct solutions.

Avoid:

- abstraction before evidence;
- clever generic code for one caller;
- framework-shaped code without a framework-sized problem;
- dynamic behavior that hides control flow;
- configuration-driven everything.

A 100-line TODO app should still be clean, typed, and testable. It does not need a fake enterprise architecture ceremony.

## DRY

Avoid duplication of knowledge, not merely duplicated text.

Duplication is acceptable when:

- abstractions would hide important differences;
- two things are currently similar but likely to evolve separately;
- local clarity matters more than premature reuse.

Refactor duplication when it represents the same domain rule, validation rule, policy, protocol behavior, or integration contract.

## SOLID as Practical Rules

- Keep units cohesive.
- Keep dependencies explicit.
- Prefer composition over unnecessary inheritance.
- Separate policies from mechanisms.
- Make extension possible without modifying unrelated behavior.
- Depend on stable abstractions when the architecture justifies them.
- Do not create abstractions with only imaginary future users.

## Naming

Names should communicate domain meaning.

Prefer:

- `create_user`
- `sync_device_state`
- `temperature_sensor`
- `retry_policy`
- `command_handler`
- `payment_authorization`

Avoid vague names:

- `do_stuff`
- `process_data`
- `handle_thing`
- `manager`
- `helper`
- `utils`
- `temp`
- `obj`

Generic names are acceptable only when the scope is tiny and obvious.

## Comments

Comments should explain why, not repeat what the code says.

Good comments explain:

- non-obvious constraints;
- protocol quirks;
- business rules;
- compatibility requirements;
- hardware behavior;
- security decisions.

Bad comments narrate obvious code.

## Structural Search And Mechanical Changes

Use parser-aware tooling when the task depends on code structure rather than raw
text:

- `ast-grep` for syntax-aware search, linting, and mechanical rewrites;
- `tree-sitter` or tree-sitter-backed tooling when grammar-level inspection is
  needed;
- `rg` for broad text search and `fd` for file discovery before slower
  alternatives.

Do not use broad regex rewrites for syntax-sensitive changes when a structural
tool is available and practical.

## Prohibited Quality Failures

- god files;
- god objects;
- hidden mutable globals;
- mystery side effects;
- fake TODO implementations;
- broad catch-and-ignore error handling;
- unrelated refactors during bug fixes;
- dependency additions for trivial code;
- public API changes without explicit intent.
## Extended References


For deeper quality work, read the relevant documents:

- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/08_engineering_smells.md`
- `../../engineering/10_antipattern_catalog.md`
- `../../engineering/12_naming_bible.md`
