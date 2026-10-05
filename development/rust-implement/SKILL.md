---
name: rust-implement
description: "Use when implementing new Rust features, refactoring existing Rust code, adding a new module, redesigning a struct/trait, or making architectural changes to a Rust codebase. Triggers on: implement, add feature, refactor, redesign, new module, new struct, new trait, extract, split, restructure, TDD, test-driven, 实现功能, 重构, 新增模块"
globs: ["**/*.rs", "**/Cargo.toml"]
---

# Rust Implementation Workflow

Use this skill as the compact orchestrator for Rust feature work and refactors.

## Non-Negotiables

- Generate an implementation plan before touching production code.
- Follow TDD: no production code before a failing test.
- Route to other Rust or domain skills when the work hits a specialized concern.
- Preserve low-latency constraints on hot-path trading code.
- Invoke `code-review` after the feature or refactor is complete.

## Default Flow

```text
1. Plan
2. RED: write a failing test
3. GREEN: write minimal code
4. REFACTOR: improve without changing behavior
5. REVIEW: run code-review
```

## 1. Plan First

Before the first test:
- define the behavior, scope, and success criteria
- choose the domain skill if needed
- choose the Rust specialist skill if needed
- decide whether the code is hot path, cold path, or backtest-only
- prefer type-driven design and explicit error strategy

Write an implementation plan before coding. For non-trivial work, persist that plan in `docs/`.

Reference:
- `docs/guidelines/rust-implement/workflow.md`
- `docs/GENERAL_ARCHITECTURE.md`

## 2. TDD Cycle

### RED
- write the smallest failing test that captures the behavior
- `cargo test` must fail; a compile error counts

### GREEN
- write the minimum production code to pass the failing test
- avoid speculative abstraction and extra features

### REFACTOR
- keep tests green while improving design, correctness, and performance
- rerun `cargo test` after each meaningful change

## 3. Route To Specialist Skills

Use `rust-router` first when the task spans multiple Rust concerns or the right skill is unclear.

Route by concern:
- ownership/resources/mutability -> `m01-ownership`, `m02-resource`, `m03-mutability`
- generics/types/invariants -> `m04-zero-cost`, `m05-type-driven`
- errors/concurrency -> `m06-error-handling`, `m07-concurrency`
- domain/performance/ecosystem -> `m09-domain`, `m10-performance`, `m11-ecosystem`
- lifecycle/recovery/anti-patterns -> `m12-lifecycle`, `m13-domain-error`, `m15-anti-pattern`
- any `unsafe` or FFI -> `unsafe-checker`

Route by domain:
- trading -> `domain-fintech`
- web -> `domain-web`
- CLI -> `domain-cli`
- cloud -> `domain-cloud-native`
- ML -> `domain-ml`
- embedded -> `domain-embedded`

For structural refactors, use the Rust navigation and refactor skills.

Reference: `docs/guidelines/rust-implement/routing.md`

## 4. Low-Latency Rules

When touching market data, execution, orderbook, risk, or other hot-path code:
- treat latency as a hard requirement, not a later cleanup
- avoid allocation, blocking calls, unnecessary `clone`, and dynamic dispatch on hot paths
- keep Tokio and network I/O on cold-path threads
- measure before claiming an optimization

Reference:
- `docs/guidelines/rust-implement/latency.md`
- `docs/GENERAL_ARCHITECTURE.md`

## 5. Done Criteria

Do not mark the task done until:
- the plan exists and matches the implementation
- tests were written first and now pass
- refactoring kept behavior stable
- specialist skill guidance was applied where needed
- `code-review` has been run and critical issues are fixed
