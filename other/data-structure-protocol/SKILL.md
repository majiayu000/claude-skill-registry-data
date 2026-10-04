---
name: data-structure-protocol
description: >-
  Build and navigate DSP (Data Structure Protocol) — graph-based long-term structural memory of codebases for LLM agents.
  Stores entities (modules, functions), their dependencies (imports), public API (shared/exports), and reasons for every connection.
  Use when: (1) project has a .dsp/ directory, (2) user asks to set up DSP or bootstrap project structure,
  (3) creating/modifying/deleting code files in a DSP-tracked project, (4) navigating project structure, understanding dependencies,
  or finding modules, (5) user mentions DSP, dsp-cli, .dsp, or structure mapping.
---

# Data Structure Protocol (DSP)

DSP builds a dependency graph of project entities in a `.dsp/` directory. Each entity (module, function, external dependency) gets a UID, description, import list, and export index. The graph answers: what exists, why it exists, what depends on what, and who uses what.

**DSP is NOT documentation for humans or AST dump.** It captures _meaning_ (purpose), _boundaries_ (imports/exports), and _reasons for connections_ (why).

## Agent Prompt

Embed this context when working on a DSP-tracked project:

> **This project uses DSP (Data Structure Protocol).**
> The `.dsp/` directory is the entity graph of this project: modules, functions, dependencies, public API. It is your long-term memory of the code structure.
>
> **Core rules:**
>
> 1. **Before changing code** — find affected entities via `dsp-cli search`, `find-by-source`, or `read-toc`. Read their `description` and `imports` to understand context.
> 2. **When creating a file/module** — call `dsp-cli create-object`. For each exported function — `create-function` (with `--owner`). Register exports via `create-shared`.
> 3. **When adding an import** — call `dsp-cli add-import` with a brief `why`. For external dependencies — first `create-object --kind external` if the entity doesn't exist yet.
> 4. **When removing import / export / file** — call `remove-import`, `remove-shared`, `remove-entity` respectively. Cascade cleanup is automatic.
> 5. **When renaming/moving a file** — call `move-entity`. UID does not change.
> 6. **Don't touch DSP** if only internal implementation changed without affecting purpose or dependencies.
> 7. **TOC membership** — new entities land in every TOC whose root scope covers their path (or pass `--toc` explicitly, repeatable). Reshape membership with `add-to-toc` / `move-to-toc`.
> 8. **Bootstrap** — if `.dsp/` is empty: discover roots (`--new-root --scope`), split files into per-TOC batches balanced by volume, then three waves over the batches in parallel — index all files, then all exports, then all imports. Each file is read exactly once (in Wave 1); later waves reuse that read.
>
> **Key commands:**
> ```
> dsp-cli init
> dsp-cli create-object <source> <purpose> [--kind external] [--uid UID] [--toc TOC ...] [--new-root [--scope DIR]]
> dsp-cli create-function <source> <purpose> [--owner UID] [--uid UID] [--toc TOC ...]
> dsp-cli create-shared <exporter_uid> <shared_uid> [<shared_uid> ...]
> dsp-cli add-import <importer_uid> <imported_uid> <why> [--exporter UID]
> dsp-cli add-to-toc <uid> [<uid> ...] --toc TOC [--toc TOC ...]
> dsp-cli move-to-toc <uid> [<uid> ...] --from TOC --to TOC
> dsp-cli remove-import <importer_uid> <imported_uid> [--exporter UID]
> dsp-cli remove-shared <exporter_uid> <shared_uid>
> dsp-cli remove-entity <uid>
> dsp-cli move-entity <uid> <new_source>
> dsp-cli update-description <uid> [--source S] [--purpose P] [--kind K] [--scope DIR]
> dsp-cli get-entity <uid>
> dsp-cli get-children <uid> [--depth N]
> dsp-cli get-parents <uid> [--depth N]
> dsp-cli search <query>
> dsp-cli find-by-source <path>
> dsp-cli read-toc [--toc ROOT_UID]
> dsp-cli get-stats
> ```
>
> `TOC` is a root UID or the literal `default` (the plain `.dsp/TOC` file).

## Using the CLI

The script is at `scripts/dsp-cli.py` relative to this skill directory.

```
python <skill-path>/scripts/dsp-cli.py [--root <project-root>] <command> [args]
```

`--root` defaults to current working directory. All paths in arguments are repo-relative.

## Core Concepts

- **Code = graph.** Nodes are Objects and Functions. Edges are `imports` and `shared/exports`.
- **Identity by UID, not file path.** Path is an attribute; renames/moves don't change UID.
- **"Shared" creates an entity.** If something becomes public (exported), it gets its own UID.
- **Import tracks both "from where" and "what".** One code import may create two DSP links: to the module and to the specific shared entity.
- **Full import coverage.** Every imported file/asset must be an Object in `.dsp` — code, images, styles, configs, everything.
- **`why` lives next to the imported entity** in its `exports/` directory (reverse index).
- **Start from roots.** Each root entrypoint has its own TOC file. A root may declare a `scope` (directory subtree); new entities are auto-assigned to every TOC whose root scope covers their path.
- **External deps — record only.** `kind: external`, no deep dive into `node_modules`/`site-packages`/etc. But `exports index` works — shows who imports it.
- **Persistent reverse-index cache.** `.dsp/.cache/` holds the reverse adjacency (`imported → importers`), one file per imported entity. It makes reverse and traversal commands (`get-recipients`, `get-parents`, `get-path`, and `get-entity`'s "exported to") fast on large graphs without re-scanning. Local and forward commands (`get-children`, `get-shared`, `read-toc`, `find-by-source`, `search`) read live files and never touch it. Mutating commands keep it up to date incrementally (only the affected entries), so it stays correct as you build the graph.
  - **Auto-build.** If the cache is missing, the next reverse/traversal command — or the next reverse-affecting mutation — builds it automatically. No manual step is needed in normal use.
  - **It is committed with the graph** (not git-ignored): a plain `git checkout`/`pull` moves the cache together with `.dsp/`. Caveat: a `merge`/`rebase` that touches `.dsp/` can merge `.cache/` files incorrectly or leave conflicts — the cache is not self-validating (it tracks only a sentinel, not content), so run `rebuild-cache` afterwards to be safe.
  - **`rebuild-cache`.** Run `python <skill-path>/scripts/dsp-cli.py rebuild-cache` if `.dsp/` was changed **outside** this CLI — hand-edited files, or a `merge`/`rebase` that touched `.dsp/`. Agents that follow the protocol mutate `.dsp/` solely through dsp-cli, so during normal work this is rarely needed.

## UID Format

- Objects: `obj-<8 hex>` (e.g., `obj-a1b2c3d4`)
- Functions: `func-<8 hex>` (e.g., `func-7f3a9c12`)

UID marker in source code — comment `@dsp <uid>` before declaration:

```js
// @dsp func-7f3a9c12
export function calculateTotal(items) { ... }
```

```python
# @dsp obj-e5f6g7h8
class UserService:
```

## Workflows

### Setting Up DSP (bootstrap in 3 waves)

Core economy rule: **each file is read exactly once, by exactly one subagent** — all three waves run on top of that single read. Batches run in parallel; the only sync point is the barrier before Wave 3.

1. Run `dsp-cli init` to create `.dsp/` directory.
2. **Phase 0 — roots**: identify entrypoint(s) and their directory scopes, create each with `create-object <path> <purpose> --new-root --scope <dir>` (`.` = whole repo). Scopes make TOC assignment automatic for everything that follows.
3. **Inventory & batching**: list all project files with sizes (e.g. `git ls-files | xargs wc -c`; skip vendored code, build output, lock files). Group by TOC, split each group into batches of roughly equal volume — one batch per subagent, dispatched in parallel.
4. **Wave 1 — all files**: each subagent reads each file of its batch **once** (capturing purpose, entities, exports, imports with usage sites) and registers it: `create-object` + `create-function --owner` for significant inner entities, `@dsp` markers in source.
5. **Wave 2 — all exports**: same subagent, no re-reading — `create-shared` per file (batch-local, no waiting on other batches).
6. **Barrier**: when ALL batches finish Waves 1–2, subagents report their externals; the orchestrator dedupes and registers each once (`create-object --kind external` + `add-to-toc` for other roots using it).
7. **Wave 3 — all imports**: same subagent, still no re-reading — `add-import` with usage-based `why` (dead imports were already filtered at the Wave 1 read); targets resolve via `find-by-source`.
8. Verify: `get-stats`, `get-orphans`, `detect-cycles`; every inventory file resolves via `find-by-source`. Details: [bootstrap.md](references/bootstrap.md).

Re-indexing a project whose code already has `@dsp` markers: pass the old UIDs via `--uid` at every create step — the graph is rebuilt with stable identity.

### Creating Entities (when writing new code)

1. Create module: `dsp-cli create-object <path> <purpose>` — it lands in every TOC whose root scope covers the path (override with `--toc <TOC>`, repeatable)
2. Create functions: `dsp-cli create-function <path>#<symbol> <purpose> --owner <module-uid>`
3. Register exports: `dsp-cli create-shared <module-uid> <func-uid> [<func-uid> ...]` — shared entries are UIDs of existing entities, never export names
4. Register imports: `dsp-cli add-import <this-uid> <imported-uid> <why> [--exporter <module-uid>]` — all UIDs must already exist
5. External deps: `dsp-cli create-object <package-name> <purpose> --kind external`

### Navigating the Graph (when reading/understanding code)

- **Find entity by file**: `dsp-cli find-by-source <path>`
- **Search by keyword**: `dsp-cli search <query>`
- **Read TOC**: `dsp-cli read-toc` → get all UIDs, then `get-entity` for details
- **Dependency tree down**: `dsp-cli get-children <uid> --depth N`
- **Dependency tree up**: `dsp-cli get-parents <uid> --depth N`
- **Impact analysis**: `dsp-cli get-recipients <uid>` — who depends on this entity
- **Path between entities**: `dsp-cli get-path <from> <to>`

### Updating (when modifying code)

- Purpose changed: `dsp-cli update-description <uid> --purpose <new>`
- File moved: `dsp-cli move-entity <uid> <new-path>`
- Import reason changed: `dsp-cli update-import-why <importer> <imported> <new-why>`
- Root's zone changed: `dsp-cli update-description <root-uid> --scope <dir>`

### Managing TOC membership

- Add existing entities to more TOCs: `dsp-cli add-to-toc <uid> [<uid> ...] --toc <TOC>` (idempotent; e.g. an external used by a second root)
- Transfer entities between TOCs (single or batch): `dsp-cli move-to-toc <uid> [<uid> ...] --from <TOC> --to <TOC>` — all-or-nothing; a root cannot leave its own TOC
- `<TOC>` is a root UID or `default`

### Deleting (when removing code)

- Import removed: `dsp-cli remove-import <importer> <imported> [--exporter UID]`
- Export removed: `dsp-cli remove-shared <exporter> <shared>`
- File/module deleted: `dsp-cli remove-entity <uid>` (cascading cleanup)

### Diagnostics

- `dsp-cli detect-cycles [--toc ROOT_UID]` — circular dependencies (`--toc` scopes to one TOC root's entities)
- `dsp-cli get-orphans [--toc ROOT_UID]` — unused entities (`--toc` scopes to one TOC root's entities)
- `dsp-cli get-stats [--toc ROOT_UID]` — project graph overview (`--toc` scopes to one TOC root's entities)

## When to Update DSP

| Code Change | DSP Action |
|---|---|
| New file/module | `create-object` + `create-function` + `create-shared` + `add-import` |
| New import added | `add-import` (+ `create-object --kind external` if new external dep) |
| Import removed | `remove-import` |
| Export added | `create-shared` (+ `create-function` if new function) |
| Export removed | `remove-shared` |
| File renamed/moved | `move-entity` |
| File deleted | `remove-entity` |
| Purpose changed | `update-description` |
| Module moved to another subproject/root | `move-to-toc` (+ `move-entity` if the path changed) |
| Entity now used by another root | `add-to-toc` |
| Internal-only change | **No DSP update needed** |

## References

- **[Storage format](references/storage-format.md)** — `.dsp/` directory structure, file formats, TOC
- **[Bootstrap procedure](references/bootstrap.md)** — initial project markup (3-wave algorithm)
- **[Operations reference](references/operations.md)** — detailed semantics of all operations with import examples
