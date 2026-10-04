---
model_tier: medium
name: workspace-link
description: "Use when a cross-workspace import will not resolve — cannot find module @org/*, TS2307 — to link the packages properly with the workspace: protocol instead of patching tsconfig paths."
domain: engineering
workspaces:
  - engineering
packs:
  - engineering-base
---

# Linking workspace packages

One workspace imports another and the import does not resolve. The fix is a
**dependency declaration**, not a resolver override.

> **Own analysis.** The forms and failure modes below are derived from the
> public behaviour of the package managers named, not adopted from a third-party
> artefact, so no provenance ledger entry backs them. Verify the protocol
> support against the manager version the repository actually pins — see
> § Check the manager, not the table.

## When to use

- `Cannot find module '@org/ui'` or `Cannot find module '@org/ui' or its
  corresponding type declarations`.
- TypeScript `TS2307`, or a bundler resolving a workspace import to `undefined`.
- A workspace import that works in the editor and fails in the build (or the
  reverse) — the classic signature of a `paths` patch standing in for a
  dependency.

## Procedure

### 1. Declare the dependency in the importing workspace

The importing workspace's `package.json` must name the imported workspace in
`dependencies` (or `devDependencies` when the import is test-only):

```json
{
  "name": "@org/web",
  "dependencies": { "@org/ui": "workspace:*" }
}
```

The name on the left is the imported package's own `name` field — not its
directory. Then re-run the install so the manager creates the link.

### 2. Pick the form

Four forms, and the difference only shows up at publish time:

| Form | Resolves locally to | On publish, rewritten to |
|---|---|---|
| `workspace:*` | the local workspace, any version | the exact version at publish |
| `workspace:^` | the local workspace | `^<version>` |
| `workspace:~` | the local workspace | `~<version>` |
| `workspace:<range>` | the local workspace if its version satisfies `<range>`, else fails the install | `<range>` |

For a private monorepo that never publishes, `workspace:*` is the right default
— it cannot drift out of sync with the local version. For packages that *are*
published, `workspace:^` is what keeps the released range honest.

The explicit-range form is the only one that can **fail** the install, and that
is a feature: it is how a workspace states which version of a sibling it needs.

### 3. Check the manager, not the table

Protocol support is not uniform. pnpm and Yarn (berry) implement all four forms;
Bun implements the protocol; npm's support arrived later than the others.
Confirm against the version in `packageManager` / the lockfile rather than
assuming — [`monorepo-workspace`](../monorepo-workspace/SKILL.md) step 1 reports
which manager this repository actually uses.

Where the protocol is unsupported, the correct fallback is still a dependency
declaration — the sibling's version range — never a resolver override.

### 4. Verify it resolves for real

Re-run the failing command, not the editor. A resolved editor and a failing
build is the exact state a `paths` patch produces, so the build is the probe.

## Output format

A workspace-link answer MUST contain, in order:

1. **The unresolved import, named** — the importing workspace path, the imported
   package `name` (not its directory), and the exact error text.
2. **The declaration to add** — the `package.json` path, the section
   (`dependencies` or `devDependencies`), and the `workspace:` form chosen, with
   one sentence on why that form (private-and-unpublished → `workspace:*`;
   published → `workspace:^`).
3. **The install command for this repository's manager**, read from
   `packageManager` / the lockfile rather than assumed.
4. **The verification** — the failing build or test command re-run, not the
   editor, plus its result. A resolved editor and a failing build is the state
   a `paths` patch produces, so the build is the probe.

## Gotcha

- Adding the dependency without re-running the install changes nothing: the
  manager creates the symlink at install time.
- A `workspace:` dependency on a package that is not actually in the workspace
  globs fails with a confusing "not found" — check the globs
  ([`monorepo-workspace`](../monorepo-workspace/SKILL.md) step 2) before the
  spelling of the name.
- The imported package still needs a valid entry point (`main` / `exports` /
  `types`). A correct link into a package that exports nothing reads as the same
  `TS2307`.
- Circular workspace dependencies install fine and break the task graph later.

## Do NOT

- **Do NOT patch `tsconfig.json` `paths` to point at the sibling's source.** It
  silences the type error in the editor while the runtime and the bundler still
  have no dependency to resolve, and it hides the edge from the task runner, so
  the affected-set calculation and build ordering both go wrong. A `paths` entry
  is a compiler hint, not a dependency.
- **Do NOT hand-edit `package.json` link fields or the lockfile** to point at a
  relative path (`file:../ui`, a hand-written entry under `node_modules`). It
  works once, on one machine, and is undone by the next install.
- Do not add the dependency to the *root* `package.json` to make the error go
  away — the importing workspace is what must declare it.
- Do not install the sibling from the registry to satisfy the import. That
  silently pins a published copy while the local source keeps changing.

## See also

- [`monorepo-workspace`](../monorepo-workspace/SKILL.md) — which manager, which workspaces, which graph.
- [`monorepo-antipatterns`](../../../docs/guidelines/monorepo-antipatterns.md) — the task-graph mistakes a `paths` patch hides.
- [`blast-radius-analyzer`](../blast-radius-analyzer/SKILL.md) — § Monorepo, once the edge exists.
