---
name: architecture
description: Define a project's architecture before any code is written — stack choice as a decision record, file tree and invariants, public contract, layer rules, and dependency licences — and enforce it with a checker. Use when a calibrated brief exists and the project does not yet have a written architecture, or when a structural change is proposed. No code before the architecture is written. Only invoke via the orcinus router.
license: MIT
user-invocable: false
compatibility: Requires Python 3.11+.
---

# ARCHITECTURE — decide the shape before building it

Most of the 31 common coding-agent mistakes are architecture mistakes made early: a stack chosen silently, a tree that grows without a rule, a module that depends on the wrong layer, a dependency whose licence nobody checked. This skill makes those decisions explicit, written, and checked — before the first slice is built.

## Rules

- No code before the architecture is written. Scaffold needs a confirmed brief *and* a written architecture.
- No stack without a decision record. A stack chosen silently is a stack nobody can question.
- A layer violation is a FAIL even if the suite is green. The suite does not know the layers.
- A decision record names what was rejected and why. A record that only describes the winner is a press release, not a decision.
- A check that did not run is never reported as passed.

## Steps, in order

### 1. Record the stack choice as an ADR

Write `docs/adr/0001-stack-<name>.md` with: context (what the project must do), decision (the stack, with versions), reasons (why this stack fits this project), rejected alternatives (what was considered and why it lost), consequences (what this choice costs later). The user confirms the stack; the ADR records the decision. If the stack changes, write a new ADR that supersedes the old one — never edit the old one silently.

### 2. Define the tree and the invariants

Write `docs/constitution.md` (or extend it) with the invariants: one slice at a time, no test weakening, no secrets, and the layer rules for this project. Write the file tree: every directory's purpose, in one line each. The tree must match the actual files — a tree that does not match reality is worse than no tree.

### 3. Define the public contract

Write `docs/contract.md`: the public surface (what a consumer may import), the error shape (one format everywhere), and the versioning rule (what counts as breaking). This is the contract the breaking-change check enforces later.

### 4. Produce a codebase map

```bash
npx --yes repomix --output <path-outside-the-repo>
```

Repomix (MIT) packs the repository into one file. Read the packed file list: it must contain the source, the tests, and the docs — and it must not contain `node_modules/`, `dist/`, `reports/`, or a `.env`. (`.env.example` is a placeholder and belongs in the map.) If the map contains a secret or a build artifact, the tree is wrong, not the map.

### 5. Check dependency licences

This skill — and its checker — are npm/TypeScript-only: they read
the dependency list from `package.json` and each licence from
`node_modules/<dep>/package.json`, and the checker scans `.ts`,
`.tsx`, `.js` and `.jsx` files under `src/`. For any other stack
(Python, Go, Rust, …) there is no manifest adapter: the licence
step files INCOMPLETE with the reason (the checker names the stack
it detected, e.g. `pyproject.toml` present), and the agent follows
that stack's own licence check instead of inventing one. A check
that did not run is never reported as passed.

List every direct dependency in `package.json` and read its licence from `node_modules/<dep>/package.json`. Allowed by default: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC. A copyleft licence (GPL, AGPL, LGPL) or an unknown licence is a FAIL until a decision is recorded in an ADR — the project does not ship a licence nobody looked at.

### 6. Run the checker

```bash
python3 skills/architecture/scripts/check_architecture.py --root <project>
```

The checker verifies what is mechanically checkable: no source file imports from outside `src/` (that includes the test directory), no circular import among source files, every relative import resolves to a file, and every direct dependency's licence is allowed (SPDX expressions and the legacy `licenses[]` array are understood). It reads `.ts`, `.tsx`, `.js` and `.jsx` files, follows dynamic `import()`, and resolves tsconfig `paths` aliases. `import type` and imports in comments are not runtime imports and are ignored. A `baseUrl` or `paths` inherited from a base config resolve against the base config's directory, not the child's (TypeScript's rule for `extends` chains). It is a limited check of relative imports, not a full module resolver; for a project that needs a complete graph, use a real resolver (dependency-cruiser, madge). Two limits to know: it does not follow re-exports through barrel files or evaluate conditional or computed imports, and a string literal containing the text of an import statement is counted as an import — the scanner is a regex over comment-stripped text, not a parser, so a file that quotes an import in a string can report a false "unresolved import". If it finds no source files at all it reports INCOMPLETE, never clean — and exits 2, not 1: exit 2 means nothing (or nothing trustworthy) was checked, exit 1 means something was checked and failed. The same exit 2 applies when the tsconfig exists but cannot be used: the import graph is unknown, so no import verdict is trustworthy. A missing `package.json` is a violation when source files were found (the import checks ran) and part of the INCOMPLETE result when none were (nothing at all was checked).

## Report

Return the report in this form:

- The stack ADR (file, decision, rejected alternatives).
- The tree (as it stands) and the invariants.
- The contract (public surface, error shape, versioning rule).
- The codebase map (file count, what is in it, what is not).
- The licence check (each direct dependency and its licence).
- The checker result (command, exit code, violations named).
- Verdict: PASS or FAIL, and what remains.

## Scope

This skill defines the architecture; `scaffold` builds it and `build` implements slices within it. It does not choose the stack for the user, and it does not draw diagrams (that is archify). The spec-kit method (constitution, specification, plan) inspired the shape of this skill; the spec-kit CLI itself is not run here, because its runner is not installed in this environment — the method is used, the tool is not. Repomix is invoked as-is.

## Sources

Written from scratch for ORCINUS, in our own words. No ready skill was found for this in the 0–100 research: spec-kit and repomix are tools, not `SKILL.md` files, and no verified architecture skill was identified. Spec-kit (github/spec-kit, MIT) and repomix (MIT) are used as-is where they run; no text was copied from either.
