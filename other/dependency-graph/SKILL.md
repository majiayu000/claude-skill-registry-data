---
name: dependency-graph
description: "Use when a JavaScript or TypeScript project's dependencies must be seen as they are in the code: the whole graph, what one module depends on, who depends on it, or its neighbourhood, at file or folder level. Produces a Mermaid graph document in aiview, parsed by a deterministic script, never inferred. Not for designing a module's interface (deepen-module)."
---

# Dependency graph

**The graph is parsed, never written by hand or guessed.** `scripts/graph.mjs` runs dependency-cruiser over the code, with the project's own TypeScript, and turns the ask into options. The same options give the same graph on the same commit.

## Run it

Translate the ask into options, then run it once:

```sh
node <skill-dir>/scripts/graph.mjs --root <the package's folder> [--from <path>] [--to <path>] [--focus <path> --depth <n>] [--steps <n>] [--level <n>] [--only <regex>] [--exclude <regex>] --title "<title>" --out <path>
```

- **What a module depends on**: `--from` that module or folder.
- **Who depends on it**: `--to` it.
- **Its neighbourhood**: `--focus` it, `--depth` the hops.
- **Not too far**: `--steps <n>` follows imports only n steps from `--from`.
- **Folders, not files**: `--level 2` folds `src/<area>/…` into one node per area; the coarser view first, then open the part that matters.
- **Noise out**: `--exclude "tests|generated"`; node_modules and Node's own modules are always out.

The root is the folder holding the package's `tsconfig.json` (its `extends` resolves from there); in a monorepo, one package per graph. The first run installs dependency-cruiser and the project's TypeScript into a cache, needing the network once.

## The document

**Through the `aiview` skill**: kind `report` from `YYYY-MM-DD-<subject>.dependency-graph.report.md`, tags `dependency-graph` and the module, group the piece of work it serves. The script writes it at the path `aiview path` gives, with the commit, the counts and the command that makes it again. Open it and tell the person the URL. A graph over about a hundred nodes is folded with `--level` or narrowed before it is shown.

**What the graph shows is said under it, in a few lines**: the cycles, a dependency against the project's stated boundaries (its conventions file), a module far more depended on than the rest. Nothing beyond what the edges show.
