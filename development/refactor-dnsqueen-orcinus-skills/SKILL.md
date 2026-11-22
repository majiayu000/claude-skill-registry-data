---
name: refactor
description: >
  Safe, behavior-preserving code refactoring for any language. Detects smells (Bloat, OO, Couplers, Layers),
  applies Fowler & MVVM/Clean Architecture patterns, and runs tests per step.
  Triggers: refactor, clean up, extract, rename, simplify, decompose, god class, MVVM, Clean Architecture. Only invoke via the orcinus router.
license: MIT
user-invocable: false
---

# Refactoring Specialist

Safe, incremental, behavior-preserving code improvements for any language.

## Core Contract

1. **Behavior is preserved.** Every change leaves the program doing exactly the same thing externally. If a change alters behavior, it is not a refactoring — it is a feature change requiring explicit user opt-in.
2. **One operation at a time.** No bundling multiple logical changes into one step. Each step is independently verifiable and revertable.
3. **Tests gate every step.** Run tests after each edit. If tests fail, revert immediately — do not fix forward.

---

## Quick Reference

> [!TIP]
> **Token Efficiency**: These reference files are large. **Do not read them in full**. Use `grep_search` to find your target topic first, then view only its specific line range.

| What you need | Reference file |
|---|---|
| Step-by-step process to follow every time | [process.md](references/process.md) |
| Detect smells before choosing an operation | [smells.md](references/smells.md) |
| When to stop, warn, or ask | [safety.md](references/safety.md) |
| Extract, Inline, Split, Decompose | [catalog-composing.md](references/catalog-composing.md) |
| Conditionals, Guards, Polymorphism | [catalog-simplifying.md](references/catalog-simplifying.md) |
| Move, Organize, Encapsulate | [catalog-organizing.md](references/catalog-organizing.md) |
| Rename, Parameter Objects, Factory | [catalog-api.md](references/catalog-api.md) |
| Inheritance, Composition over Inheritance | [catalog-inheritance.md](references/catalog-inheritance.md) |
| FP, Async, Reactive, DI patterns | [catalog-modern.md](references/catalog-modern.md) |
| MVVM, MVP, Repository, Use Case, Clean Architecture | [catalog-architecture.md](references/catalog-architecture.md) |
| Language idioms and test commands | [language-profiles.md](references/language-profiles.md) |

---

## Decision Tree

**"Just refactor this" / "clean this up" / "this smells"** (no specific operation given)
→ Read `smells.md`. Diagnose. Present ranked findings. Confirm priority with user. Then follow `process.md`.

**Specific operation requested** (e.g., "extract this into a function", "rename X to Y")
→ Check `safety.md` for red lines. If clear, go directly to `process.md` §4 Execution Loop.

**Large file or large codebase** (file >500 lines, or change touches >3 files)
→ Read `safety.md` §6 Large Codebase Protocol before anything else.

**Architectural scope** (user mentions pattern names, layer problems, or any trigger below marked [arch])
→ Read `smells.md` Family 6. Map current architecture (Grep import statements, identify layers). Present architecture map. Ask: *"What target pattern?"* Confirm with user. Then read `safety.md` §8 in full before touching anything. Use operations from `catalog-architecture.md`.

**Language you haven't seen before in this session**
→ Check `language-profiles.md`. If language not listed, ask user: "What command runs your tests?" Then proceed.

**Something feels risky** (public API, serialization, concurrency, no tests)
→ Read `safety.md` §3 Red Lines before touching anything. Stop and ask if any red line applies.

---

## Trigger Words

**Code-level:** `refactor`, `clean up`, `clean this up`, `extract`, `rename`, `simplify`, `decompose`, `restructure`, `improve readability`, `reduce complexity`, `remove duplication`, `pull this out`, `break this apart`, `this is too long`, `hard to understand`, `technical debt`, `code smell`, `too many parameters`, `god class`, `big function`, `make this cleaner`, `this needs work`, `tidy up`, `reorganize`, `modernize`

**Architectural [arch]:** `MVVM`, `MVP`, `MVC`, `Clean Architecture`, `Hexagonal`, `layering`, `too much in the controller`, `fat controller`, `view has logic`, `business logic in the UI`, `anemic model`, `fat service`, `separation of concerns`, `introduce repository`, `add a use case`, `extract interactor`, `layer violation`, `presentation importing data`, `domain importing service`, `architecture`, `restructure layers`, `move to domain`

---

## Refactoring in 30 Seconds

For experienced users who just want the loop:

**Code-level:**
1. Read target file(s) completely
2. Detect smells → present ranked list
3. Confirm operation order with user
4. For each step: state op → show diff → apply → run tests → confirm or revert
5. Summarize changes; suggest (but don't apply) follow-ons

**Architectural:**
1. Map current architecture (Grep imports, identify layers) → present map
2. Confirm target pattern with user
3. Read `safety.md` §8 in full
4. Detect Family 6 smells → present ranked findings
5. For each violation: Introduce → Redirect → Remove (one class per step, tests after each)
6. Summarize; suggest follow-ons

Full detail: [process.md](references/process.md) | Architecture operations: [catalog-architecture.md](references/catalog-architecture.md)

## Agentic Context & Tool Mastery

To make this skill highly effective when executed by an autonomous AI agent, adhere to the following tool usage patterns:
1. **Never Guess File Paths**: Always run search or directory listing tools (like `grep_search` or `list_dir`) to confirm the exact location of a file before attempting to read or edit it.
2. **Prioritize Targeted Searches**: For large codebases, use `grep_search` to map class names, function calls, and import statements instead of reading entire directories. Reading is expensive; scanning is efficient.
3. **Validate Edits Syntactically**: Immediately after applying any replacement/edit, run a dry-run linter or compilation check (e.g. `tsc --noEmit`, `cargo check`, or syntax checks) BEFORE running the full test suite.
4. **Use Structured Diffs**: Always generate precise before-and-after summaries for edits to ensure the changes are atomic and understandable.
5. **Token-Sparing File Views**: When referencing heavy catalog files (like `catalog-api.md`) or smell catalogs (`smells.md`), **do not load the entire file**. Use targeted grep searches first to locate the line numbers of the specific smell or refactoring operation you need, and then view only those specific line ranges (e.g., `StartLine` to `EndLine`). This saves significant token context.

## Context Preservation Protocol

In long refactoring sessions, AI agents can lose context or suffer from drift. You MUST:
1. **Re-Read Before Edit**: If you haven't viewed a file in the last 10 minutes, re-read it before making any edits. Code in active development may have been modified externally.
2. **State Current State**: At the beginning of each turn in a multi-step refactoring, explicitly state the current active step and its objective (e.g. "We are currently on Step 2 of 4: Extracting `applyTaxes`").
3. **Commit/Stash Tracking**: Check `git status` frequently to ensure you know exactly what is modified and avoid editing files with unstaged, unrelated changes.

---

## What This Skill Does NOT Do

- Does not change external behavior without user approval
- Does not fix bugs while refactoring (separate concerns)
- Does not apply multiple operations in one edit
- Does not refactor code it hasn't read
- Does not skip tests "just this once"
