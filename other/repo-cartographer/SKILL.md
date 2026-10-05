---
name: repo-cartographer
description: Maps an unfamiliar codebase into a visual onboarding document (docs/architecture.md) with Mermaid diagrams — system layers, module dependencies, a traced core data flow — plus an opinionated 5-file reading order. Use when the user asks to understand, explain, map, diagram, or onboard onto a repository, or says things like "how is this project organized", "where do I start reading", "draw the architecture", or "/map".
---

# Repo Cartographer

Turn any repository into a map a newcomer can read in 10 minutes: **`docs/architecture.md`**.

## Output contract

One file: `docs/architecture.md`, with exactly these sections in this order:

1. **TL;DR** — what the project does (2–3 sentences) + tech stack in one line + the archetype you classified (see Phase 2).
2. **System Map** — Mermaid `flowchart` of top-level components/layers and how they connect.
3. **Module Dependencies** — Mermaid `flowchart` of who imports/calls whom. Core modules only.
4. **Core Flow** — one Mermaid `sequenceDiagram` of the most representative runtime flow (e.g. a request from entry to response, a command from argv to output).
5. **Reading Order** — exactly 5 files, in order, each with a one-line reason. This is the most valuable section: be opinionated.
6. **Conventions** — small table: build command, test command + where tests live, error-handling style, naming style, anything surprising.

If `docs/architecture.md` already exists, overwrite it and say so.

## Method

Work in four phases. Do not skip phases; each feeds the next.

### Phase 1 — Scout (breadth, not depth)

Goal: build an inventory, not an understanding.

- Read the manifest first: `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` / `pom.xml` / `*.csproj`, etc. Note entry points (`main`, `bin`, scripts), major dependencies, module/workspace declarations.
- Read the README (and the `docs/` index if present) for the project's own self-description.
- List the top 2 directory levels. For monorepos, list each package once.
- Identify entry points: HTTP server bootstrap, CLI main, library public API (`__init__.py`, `index.ts`, `lib.rs`).

### Phase 2 — Classify

Decide the repo archetype. This determines which flow is "most representative":

| Archetype | Representative flow to trace |
|---|---|
| Web/backend service | one HTTP request: route → handler → service → data store → response |
| CLI tool | one command: argv → parse → execute → output |
| Library/SDK | one public API call: export → implementation → internals |
| Frontend app | one user interaction: event → state change → render |
| Data pipeline | one record: ingest → transform → store |
| Monorepo | pick the package the README leads with; note inter-package deps |

State the archetype in the TL;DR.

### Phase 3 — Trace (now go deep, but only along one line)

- Pick the representative flow from Phase 2.
- Follow it through the actual code: open each file the flow touches, in call order. Verify each hop exists — never assume a call from a file name.
- Collect the real module boundaries you crossed; these become your dependency-graph nodes.
- While tracing, note the 5 files that mattered most → seeds of the Reading Order.
- For anything you could not verify (dynamic dispatch, DI, reflection, config-driven wiring), mark the node `name (?)` in diagrams and add one line below the diagram saying why.

### Phase 4 — Draw & write

Write `docs/architecture.md` per the output contract. Rules:

- **≤ 15 nodes per diagram.** Merge or omit; a map that shows everything shows nothing. Put detail in prose below the diagram if it matters.
- **Every edge has a label** naming the real relationship (`calls`, `imports`, `publishes to`, `reads from`), not a bare arrow.
- **Mermaid must be valid**: quote node labels containing special characters; verify mentally that it parses.
- **Direction**: `flowchart TD` for layers, `flowchart LR` for dependencies/pipelines.
- **Never invent** modules, files, or relationships you did not see. Uncertainty is marked `(?)`, not guessed away.
- Reading Order entries use real relative paths that exist in the repo.
- Keep the document ≤ ~200 lines. It is a map, not a book.

## Large repos (>500 files)

- Do not read exhaustively — sample. Manifest + entry points + one traced flow is enough signal.
- Use search tools for "where is X handled" / "who imports Y". Prefer grep over opening files at random.
- Prefer a depth-2 directory listing; go deeper only into directories the traced flow enters.
- If the repo has multiple independent subsystems, draw the System Map at subsystem level and trace a flow in only the primary one; describe the others in one line each.

## After writing

Reply with: the file path created, the archetype you classified, and a 3-line summary of the architecture. Nothing else — the document is the deliverable.
