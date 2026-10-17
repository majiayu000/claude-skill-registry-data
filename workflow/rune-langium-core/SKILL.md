---
description: "Parse `.rosetta` source into typed ASTs, build cross-file workspaces, and\nserialize models back to source text. Use when: Validating a single `.rosetta` file or snippet in memory."
name: rune-langium-core
---

# @rune-langium/core

Parse `.rosetta` source into typed ASTs, build cross-file workspaces, and
serialize models back to source text.

Use `parse()` for a single self-contained document, `parseWorkspace()` when
files reference each other, and `createRuneDslServices()` when you need raw
Langium services for custom tooling. The serializer exports are best for
AST-driven workflows, tests, and code transformations that do not need to
preserve original formatting.

## When to Use

**Use this skill when:**
- Validating a single `.rosetta` file or snippet in memory → use `parse`
- Building a parse pipeline in a Node.js script → use `parse`
- Unit-testing grammar rules in isolation → use `parse`
- Generating code from a set of related `.rosetta` files → use `parseWorkspace`
- Validating a full namespace bundle where types reference each other → use `parseWorkspace`
- Running integration tests that span multiple Rosetta files → use `parseWorkspace`
- Parsing an expression body in isolation (editor previews, round-trip tests) → use `parseExpression`
- Validating user-typed expression text without a synthetic wrapper document → use `parseExpression`
- Building a Node.js script that parses or validates `.rosetta` files → use `createRuneDslServices`
- Writing unit tests for grammar rules or validators → use `createRuneDslServices`
- Constructing a `parseWorkspace()` pipeline outside of the LSP server → use `createRuneDslServices`
- This is used automatically by `createRuneDslServices()` → use `RuneDslParser` — you do not need to instantiate it directly.

**Do NOT use when:**
- Parsing files that have cross-references to other documents — unresolved references will have `ref === undefined`. Use `parseWorkspace()` instead. (`parse`)
- Running inside a Langium LSP server — the DocumentBuilder is already managed by the server lifecycle; calling `parse()` creates a second services instance and wastes memory. (`parse`)
- Parsing a single self-contained file — use the simpler `parse()` instead (`parseWorkspace`)
- Processing very large CDM workspaces incrementally — prefer the LSP server for streaming document updates (`parseWorkspace`)
- You need resolved cross-references — use `parse()`/`parseWorkspace()` with a full document instead. (`parseExpression`)
- Inside the LSP server — use `createRuneLspServer()` which provides the full `LangiumServices` (LSP providers) instead of core-only services. (`createRuneDslServices`)
- When you need to share a service instance across multiple requests in a long-running server — the returned instance is not thread-safe for concurrent `DocumentBuilder.build()` calls; serialize builds with a queue. (`createRuneDslServices`)
- Subclassing for grammar experiments — prefer creating a separate grammar variant and a new services container instead. (`RuneDslParser`)

API surface: 717 functions, 8 classes, 170 types, 81 constants

## Configuration

2 configuration interfaces — see references/config.md for details.

## Quick Reference

**Key functions:** `parse` (Parse a Rosetta DSL source string into a typed AST), `parseWorkspace` (Parse multiple Rosetta DSL source strings as a workspace), `parseExpression` (Synchronously parse a bare Rune DSL expression snippet (e), `createRuneDslServices` (Create the full set of services required for the Rune DSL language), `createRuneDslParser` (Factory function that creates and fully initializes a RuneDslParser), `insertImplicitBrackets` (Scans Rune DSL source text and inserts `[` and `]` around bare expressions
that follow `extract`, `filter`, or `reduce` operators)
**Key classes:** `RuneDslParser` (Custom Langium parser for the Rune DSL that normalizes lexer input to insert
implicit `[` and `]` brackets around bare expressions after `extract`,
`filter`, and `reduce` operators)

*976 exports total — see references/ for full API.*

## References

Load these on demand — do NOT read all at once:

- When calling any function → browse `references/functions/` for grouped indexes, full signatures, parameters, and return types
- When using a class → browse `references/classes/` for grouped indexes, properties, methods, and inheritance
- When defining typed variables or function parameters → read `references/types.md`
- When using exported constants → read `references/variables.md`
- When configuring options → read `references/config.md` for all settings and defaults

## Links

- Author: Pradeep Mouli <pmouli@mac.com> (https://github.com/pradeepmouli)