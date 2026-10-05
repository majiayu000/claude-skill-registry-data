---
name: xtext-to-langium
description: >-
  This skill should be used when the user asks to "port an Xtext grammar to Langium",
  "migrate from Xtext to Langium", "convert Xtext grammar", "translate .xtext to .langium",
  "replace EMF metamodel with Langium AST", "port Xcore operations to TypeScript",
  "handle syntactic predicates in Langium", "restructure LL(*) grammar for LL(k)",
  "port Xtext scoping to Langium ScopeProvider", "port Xtext validation rules",
  or mentions migrating any Eclipse Xtext DSL to TypeScript/Langium.
version: 0.1.0
---

# Xtext to Langium Port Guide

Comprehensive guide for porting Eclipse Xtext grammars to Langium, covering grammar translation, EMF metamodel replacement, scoping, validation, and packaging as a TypeScript library.

## When to Use

Apply this skill when:
- Porting an Xtext `.xtext` grammar to Langium `.langium` format
- Replacing EMF/Xcore metamodels with Langium-generated TypeScript AST
- Translating Xtext `ScopeProvider` to Langium's scoping services
- Converting Xtext validation rules to Langium validators
- Restructuring ANTLR LL(*) grammar patterns for Chevrotain LL(k)
- Packaging a ported DSL as a TypeScript library (Node.js + browser)

## Core Decision Framework

### 1. Grammar Translation: Manual, Not Automated

**Do not rely on `xtext2langium`** for non-trivial grammars. Automated tools fail on:
- Syntactic predicates (`=>` and `->`) requiring case-by-case LL(k) analysis
- Duplicated rule patterns (e.g., "without left parameter") needing redesign
- Xcore operations that must become TypeScript utilities

**Approach**: Translate rule-by-rule, phase-by-phase, starting with the highest-risk subsystem (typically expressions).

### 2. EMF Metamodel Replacement: Grammar-Inferred AST

Let Langium infer the AST from the grammar. Langium generates `ast.ts` with all node interfaces automatically.

- Xcore **structural properties** become grammar rule fields
- Xcore **derived/computed properties** become TypeScript utility functions
- Xcore **Java operations** become TypeScript utility modules
- **Do not** hand-write separate TypeScript interfaces (two sources of truth)

### 3. Predicate Handling: LL(*) to LL(k)

Xtext uses ANTLR LL(*) with unlimited lookahead. Langium uses Chevrotain LL(k) with bounded lookahead.

| Xtext Pattern | Langium Strategy |
|---|---|
| `=>` syntactic predicate | Restructure rule or increase `maxLookahead` |
| `->` backtracking predicate | Eliminate via rule factoring |
| Deep lookahead | Gate on keywords or use Langium actions |
| `<` ambiguity (doc vs operator) | Separate terminal rules or keyword gating |

Start with `maxLookahead: 3`. Increase only for specific rules that fail.

### 4. Scoping: Custom ScopeProvider

Map each Xtext `EReference` scoping case to Langium's `ScopeComputation` + `ScopeProvider` services. Langium defaults handle simple containment cases (~5 of a typical 20+). The remaining cases require a custom scope provider.

### 5. Validation: Incremental Parity

Port validation rules incrementally by category, targeting 80% parity:
1. Expression type checking (highest priority)
2. Structural constraints (cycles, duplicates)
3. Naming conventions
4. Domain-specific rules (reporting, etc.)

## Phased Delivery Strategy

Execute in this order to retire risk early:

### Phase 1: Infrastructure
Set up monorepo, Langium config, terminal rules, skeleton entry rule, `langium-cli generate` pipeline, Vitest harness.

**Checkpoint**: `langium-cli generate` produces `ast.ts`. `parse("")` returns empty model.

### Phase 2: Highest-Risk Grammar Subsystem (e.g., Expressions)
Port the most complex grammar subsystem first. For typical DSLs this is expressions with precedence chains, postfix operators, and functional operations.

**Checkpoint**: All expression tests pass. Generated `ast.ts` contains typed expression interfaces.

### Phase 3: Core Structural Types
Port data types, enumerations, functions, and other structural constructs. Implement `parse()` and `parseWorkspace()` APIs.

**Checkpoint**: Core types parse. Cross-references resolve. Public API works.

### Phase 4: Scoping & Validation
Implement custom scope provider. Port validation rules by category.

**Checkpoint**: 80%+ validation parity. Zero false positives on test corpus.

### Phase 5: Full Grammar Coverage
Port remaining subsystems (synonyms, annotations, reporting, external sources). Implement round-trip serialization.

**Checkpoint**: 100% test corpus parse rate. Round-trip passes.

### Phase 6: Packaging & Release
Finalize exports, CLI, CI, browser testing, performance benchmarks, npm publish.

## Quick Reference: Syntax Mapping

| Xtext | Langium |
|---|---|
| `grammar G with org.eclipse.xtext.common.Terminals` | `grammar G` (terminals defined inline) |
| `returns TypeName` | `returns TypeName` (same) |
| `{Action}` | `{infer Action}` |
| `[TypeRef\|ID]` | `[TypeRef:ID]` |
| `current` | `infer` keyword in actions |
| `->` (backtrack) | Remove; restructure rule |
| `=>` (synpred) | Remove; restructure for LL(k) |
| `terminal fragment` | `terminal fragment` (same) |
| `@Override` | Not needed; override via DI |

## Package Architecture

Build as a **zero-dependency library** (beyond `langium` + `chevrotain`):
- Export parser services, AST types, and utility functions
- Support Node.js (>=20) and modern browsers (ES2020+)
- Provide optional web worker helper for off-main-thread parsing
- Optional CLI as a separate package

## Additional Resources

### Reference Files

For detailed patterns and techniques, consult:
- **`references/grammar-patterns.md`** - Detailed grammar translation patterns including precedence chains, predicate elimination, action patterns, and the "without left parameter" redesign
- **`references/scoping-validation.md`** - Comprehensive scoping implementation guide with case-by-case dispatch patterns, and validation rule porting strategies
- **`references/project-structure.md`** - Monorepo layout, build configuration, test fixture strategy, CI setup, and npm packaging

### Example Files

- **`examples/expression-grammar.langium`** - Example Langium grammar fragment showing a 10-level expression precedence chain
- **`examples/scope-provider.ts`** - Example custom ScopeProvider skeleton for a ported DSL
