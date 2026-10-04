---
name: modular-large-file-refactor
description: Refactor oversized source files into smaller, coherent modules while reducing complexity and preserving behavior. Use when Claude needs to split a large component, hook, service, command handler, or Rust module; untangle mixed responsibilities; extract helpers or submodules; or reorganize code into a clearer modular design without changing the public contract.
---

# Modular Large File Refactor

Refactor one large file into a small set of focused modules without creating a mess of tiny shards. Optimize for lower cognitive load, stable public APIs, and obvious ownership boundaries.

## Workflow

1. Find the real target first. In this repository, start with the bundled `scripts/find_large_files.sh` helper instead of ad-hoc shell pipelines.
2. Inspect the oversized file and list its responsibilities before touching code.
3. Classify each block as one of: public API, orchestration, pure logic, state management, side effects, types, constants, or UI rendering.
4. Choose the smallest useful module split that isolates responsibilities cleanly.
5. Extract in safe order: constants/types first, pure helpers next, stateful logic after that, and orchestration last.
6. Keep the original entrypoint stable unless the current public surface is the problem.
7. Re-run the relevant validation after the split.

## Built-in Large File Finder

Use the bundled script first:

```bash
bash scripts/find_large_files.sh
```

What it does well:

- scans the repo's real source roots
- ignores dependency and build directories
- highlights severe offenders at `1000+` and `800+` lines
- gives a quick ranked list before deeper analysis

Use the script output to pick the biggest meaningful source file, then start the modular split.

## Split Decision Rules

**Extract a new module when the code has one clear responsibility.**

- Pure transforms, parsers, validators, formatters, and mappers belong in their own helpers.
- Shared types, schemas, and constants move out early because they reduce noise with low risk.
- Repeated UI subsections become components only if they own a meaningful chunk of markup or behavior.
- Stateful logic with a clean interface becomes a hook, service, or internal module.

**Keep code together when separation would hide the story.**

- Do not create `utils.ts` or `helpers.ts` dumping grounds.
- Do not split a file just to reduce line count.
- Do not move tightly coupled code into distant files if the reader now has to bounce between five places to understand one flow.

## Extraction Order

### 1. Stabilize boundaries

- Identify exports that other files already depend on.
- Preserve existing names and call shapes unless changing the contract is intentional.
- Prefer internal re-exports over churning imports across the repo.

### 2. Remove passive noise

- Extract constants, literal maps, small types, and Zod schemas first.
- Replace repeated inline conditions or object shapes with named helpers.

### 3. Isolate pure logic

- Pull complex branches into named functions with narrow inputs and outputs.
- Replace nested conditionals with guard clauses when it improves readability.
- Convert anonymous inline callbacks into named functions when they carry real logic.

### 4. Isolate stateful logic

- Move reusable or bulky state transitions into hooks, services, or internal modules.
- Keep side effects near the orchestration layer; do not bury network or filesystem calls in generic helpers.

### 5. Simplify the entrypoint

- Leave the original file as the facade that coordinates extracted parts.
- Aim for the top-level file to read like a table of contents for the feature.

## Structural Targets

### React and TypeScript

- Put shared UI pieces in sibling component files.
- Put non-visual behavior in hooks.
- Put backend calls in service modules that match existing project patterns.
- Put complex text/data transforms in pure helpers with explicit types.

### Rust

- Keep the public module or command handler as the facade.
- Move focused logic into sibling modules under the same directory.
- Separate parsing, validation, repository access, and response formatting when they are currently interleaved.

### Cross-cutting rule

- Prefer a small directory with 3-6 purposeful files over one huge file or fifteen trivial ones.

## Complexity Reduction Moves

- Replace long `if/else` ladders with lookup tables only when the behavior is data-driven.
- Collapse duplicated setup/teardown into one helper with explicit naming.
- Break giant functions by phase: parse -> validate -> execute -> format.
- Narrow parameter lists by passing a well-named object only when the fields naturally belong together.
- Keep error handling explicit; do not add broad fallback behavior just to make extraction easier.

## Anti-Patterns

- Splitting by arbitrary line ranges instead of responsibility
- Creating circular imports between extracted modules
- Hiding critical behavior in vaguely named helpers
- Moving repository or network calls into "pure" utility files
- Re-exporting everything from everywhere
- Changing filenames, symbols, and call paths more than the refactor requires

## Output Expectation

When you finish, describe the refactor in this shape:

1. What responsibilities were identified in the original file
2. Which modules were extracted and why
3. Which public entrypoints stayed stable
4. Which risky areas were checked after the split

## Reference

Read `references/splitting-patterns.md` when you need concrete module patterns for React/TypeScript or Rust, or when the right split boundary is not obvious.
