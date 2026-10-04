---
name: codemap
description: Use when indexing a codebase for agent navigation, generating or refreshing CODEMAP.md files, mapping large project structure, or adding CODEMAP guidance for learning/maintenance workflows.
---

# CODEMAP — Codebase Navigation Index Generator

Generate hierarchical `CODEMAP.md` files that help agents locate relevant code without scanning unrelated files. Core navigation: **Task Guide first → Domain filter → targeted reads**. For files over 1000 lines, generate a companion `<filename>.analysis.md` with intent-to-line-range mapping.

## Core Principles

- `CODEMAP.md` is a navigation constraint, not documentation to browse.
- Prefer positive guidance (Task Guide, Domain, Key Exports) over broad listings.
- Dependencies are a safety net, not an invitation to chain-read.
- Each CODEMAP describes only its own directory level. Child directory details belong in child CODEMAPs.

## Language Rule

Generated files use the user's request language for prose/headings. Code identifiers, file names, paths, and symbols keep original spelling.

## Before Generation: Ask Three Questions

Unless already specified:

1. **Mode**: `Learning` (read-only study) or `Maintenance` (active development).
2. **Sub-agents**: `Yes, max 3` (recommended), custom limit, or `No`.
3. **Ignore rules**: `Defaults + .gitignore` (recommended), or add custom patterns.

Mode differences:

| Aspect | Learning | Maintenance |
|---|---|---|
| Frontmatter | `mode: learning` | `mode: maintenance`, `commit: <hash>` |
| Task Guide | suggested entry point | primary navigation, strict |
| Domain | soft focus hint | hard filter unless justified |
| Dependencies | reference material | gated by interface/impact rules |
| Updates | one-time | incremental after code changes |

## Ignore Rules

Merge in order:
1. Built-ins: `.git/`, dependency dirs, virtualenvs, build outputs, caches, logs, lockfiles, minified files, binaries, image/font assets, IDE folders.
2. Project `.gitignore`.
3. User custom patterns.

Include generated code only if it affects navigation; mark `Generated, do not edit manually`.

## Generation Workflow

### 1. Build Global Context

Read lightweight project context only:
- Prefer root `README.md` / `README.rst` / `README.txt`.
- Else metadata: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.
- Else infer from structure; mark guesses `inferred, verify against code`.

Produce: purpose, architecture shape, major domains. Omit badges/changelogs.

### 2. Scan and Measure

After applying ignore rules:
- Build filtered directory topology.
- Count source files, lines, size per first-level subdirectory and project total.
- Files over 1000 lines:
  - `<=5` → generate all `.analysis.md`.
  - `>5` → ask: all, top 5, selected, or none.

### 3. Dispatch Work

If sub-agents enabled, choose count `K`:

| Project size | K |
|---|---|
| `<=3000` lines or `<=500KB` | 1 |
| `3001-15000` lines or `500KB-3MB` | `min(N, 2)` |
| `>15000` lines or `>3MB` | `N` |

If line count and size disagree, use the larger `K`. Assign first-level directories by greedy bin packing. Keep root loose files with main agent if small (`<=200` lines), else assign to lightest bin.

Sub-agent prompts: self-contained, plain English. Include compressed global context, output language, ignore rules, assigned directories, large files list, required formats, forbidden paths. No overlapping write ownership.

### 4. Generate Per-Directory Maps

One `CODEMAP.md` per source directory (root + each subdirectory). Each map describes only the current directory level.

### 5. Assemble Root and Install Protocol

Read first-level CODEMAP summaries and Task Guides. Write root `CODEMAP.md`, then install the Navigation Protocol block into `AGENTS.md` (preferred) or `CLAUDE.md`. Replace existing block if present; do not append duplicates. If neither file exists, create `AGENTS.md`.

---

## CODEMAP.md Structure

### Frontmatter

```yaml
---
mode: learning | maintenance
commit: abc1234f        # maintenance only
ignore: ...             # root only
generated_at: YYYY-MM-DD
stats:                  # root only
  total_files: 114
  total_lines: 18200
  total_size: 4.2 MB
---
```

### Sections

Sections appear in this fixed order. Omit a section when it would be empty.

| Section | Root | Mid-level | Leaf | Container |
|---|---|---|---|---|
| Summary | 1 sentence | 1 sentence | 1 sentence | 1 sentence |
| Task Guide | yes | yes | yes | yes |
| Subdirectories | yes | yes | — | yes |
| Key Exports | yes | yes | if needed | — |
| Files | yes | yes | yes | — |
| File Dependencies | — | immediate files only | yes | — |

**Container directory** = directory with no source files, only subdirectories. Generate only Summary + Task Guide + Subdirectories.

### Summary

One sentence. Mark uncertain inference with `(inferred)`.

### Task Guide

Columns: `Task | Domain | Target | Also Check`.

Rules:
- Each row is a concrete scenario, not a vague category.
- Learning mode: understanding intents (`理解认证流程`). Maintenance mode: modification intents (`新增认证方式`).
- `Domain` must match values used in the same map's Files or Subdirectories tables.
- `Target` = primary read set. `Also Check` = conditional candidate, not automatic read list. Keep short and empirical.
- Ensure every functional subdirectory and every common modification scenario has at least one row.

Task Guide interpretation by mode:

- **Maintenance**: Read `Target` first. Read `Also Check` only when the task explicitly mentions it, target code proves it needed, or public contract impact requires it. If no row matches, filter by `Domain`; non-matching domains excluded unless justified.
- **Learning**: Use `Target` as starting point. Treat `Also Check` as optional reference.

### Subdirectories

Columns: `Dir | Domain | Depends On | Purpose`.

Rules:
- `Domain`: short functional area (e.g., `Auth`, `Prompt`, `Tool System`, `MCP`, `Runtime`).
- **Domain granularity**: each functionally distinct subdirectory MUST have a unique Domain value. Never assign a single generic Domain (e.g., `LLM Integration`) to all entries.
- `Depends On`: directory-level dependencies (internal and external). Use `—` if none.
- `Purpose`: one sentence.

### Key Exports

Columns: `Symbol | Source | Line`.

Rules:
- Only symbols used by **other directories**. Internal-only symbols belong in child CODEMAPs.
- Line numbers as `L:<number>`. Sort by architectural importance.
- Cap at ~15 entries. Child CODEMAPs handle detailed symbols.

### Files

Columns vary by directory type:

- **Root**: `File | Domain | Function`
- **Mid-level / Leaf**: `File | Domain | Deps | Function`

`Deps` column (compact notation):
- `←` = files outside this directory that this file imports.
- `→` = files outside this directory that depend on this file.
- Example: `← core/errors.py | → main.py, chat/service.py`
- `→` >5 files: `→ N files (foundational); rg "SymbolName" --type py -l`
- Omit `Deps` column entirely when no file in the directory has cross-dir dependencies. Use `—` for individual files with no deps.

Rules:
- One row per immediate file. **Never list files from child directories that have their own CODEMAP.**
- `Domain` must match local Task Guide / Subdirectories values. `—` for trivial re-export files.
- `Function`: one concise sentence. For large files, append `→ see <filename>.analysis.md`.
- Skip pure re-export `__init__.py` if exports are captured in Key Exports.

### File Dependencies

Columns: `File | Imports (in-dir) | Exposed To (in-dir)`.

Rules:
- Same-directory relationships only. Only for immediate files (not child directory files).
- Mid-level directories: list only files directly in the directory itself, never files in child subdirectories.
- Maintenance mode: read `Imports` only when an imported interface contract is unclear. Read `Exposed To` only when changing a public signature, return type, or documented semantics.
- Learning mode: reference only; do not chain-read unless current logic is unclear without it.

### Parent-Child Decoupling

When a child directory has its own CODEMAP:
- Parent does NOT list the child's internal files in Files, File Dependencies, or Key Exports.
- Parent only references the child directory in Subdirectories and Task Guide.
- Child-internal symbols appear only in the child's Key Exports.

---

## Large File Analysis (.analysis.md)

For source files over 1000 lines, create `<filename>.analysis.md` beside it.

### Structure

```markdown
---
source: filename.py
lines: 1842
generated_at: YYYY-MM-DD
---

> One-sentence summary.

## Feature Index

| Intent | Lines | Notes |
|---|---|---|

## Symbols

| Symbol | Type | Line |
|---|---|---|

## Logical Sections

| Lines | Content |
|---|---|
```

### Rules

- **Feature Index** is primary. Map concrete learning or development intents to exact line ranges. Notes: same-file coupling only. If no intent maps to a section, omit that row.
- **Symbols**: top-level public symbols only (classes, functions, constants). Not internal helpers.
- **Logical Sections**: high-level structural segments only, **5-10 rows max**. Provides structural overview and serves as fallback when Feature Index has no match. Do not expand to function-level granularity.
- Optional **Class Hierarchy** only when inheritance depth >2.
- No code snippets, API signatures, or implementation detail paragraphs.
- In maintenance mode, agents read only matched line ranges from Feature Index; Logical Sections is the fallback.

---

## Navigation Protocol (Project-Level Injection)

Install exactly one protocol block into project `AGENTS.md` or `CLAUDE.md`. Choose by mode.

### Learning Mode Block

````markdown
## CODEMAP Navigation Protocol

This project uses hierarchical `CODEMAP.md` index files for code navigation. Files over 1000 lines may have companion `.analysis.md` structural maps.

### Navigation Rules

1. Start from root `CODEMAP.md`. Read Task Guide first.
2. Task Guide match: Target = primary read set. Also Check = conditional candidates (decide after reading Target).
3. No Task Guide match → filter Subdirectories by Domain, enter only matching-domain subdirectories.
4. Drill down layer by layer; consult local Task Guide at each level before reading source files.
5. Container directories (no source files): read only Task Guide + Subdirectories.
6. Large files: read `.analysis.md` Feature Index first, match Intent to line ranges. Use Logical Sections as fallback.
7. Batch-read final target files in parallel.
8. No speculative expansion: extend read set only when already-read code proves the need.
````

### Maintenance Mode Block

````markdown
## CODEMAP Navigation Protocol

This project uses hierarchical `CODEMAP.md` index files for code navigation. Files over 1000 lines may have companion `.analysis.md` structural maps. For development tasks, these rules are strict navigation constraints.

### Navigation Rules

1. Start from root `CODEMAP.md`. Read Task Guide first.
2. Task Guide match: Target = primary read set. Read Also Check only when the task explicitly involves it, target code proves the need, or public contract impact requires it.
3. No Task Guide match → filter Subdirectories by Domain. Non-matching domains are excluded unless already-read code gives a concrete reason.
4. Drill down layer by layer; consult local Task Guide at each level before reading source files.
5. Container directories (no source files): read only Task Guide + Subdirectories.
6. Large files: read `.analysis.md` Feature Index first, match Intent to line ranges. Use Logical Sections as fallback.
7. Batch-read final target files in parallel.
8. No speculative expansion: each additional file requires an explicit reason.

### Dependency Gating

The Deps column in Files tables marks cross-directory dependencies:
- `←` (imports): read only when the imported interface contract is needed to understand the current file.
- `→` (exposed to) ≤5 files: read only when changing a public signature, return type, or documented semantics.
- `→` >5 files (foundational): run the search command provided in CODEMAP, filter by Domain, then read only justified matches.
- No chaining: do not read dependencies-of-dependencies unless a specific contract gap remains.

### Update Rules

After code changes, the agent autonomously evaluates:
- File/directory add, delete, move, rename → regenerate affected directory CODEMAP, update parent Subdirectories and Task Guide paths.
- Public symbol signature/return type change → update Key Exports and related Task Guide entries.
- Internal implementation change only → no update. Exception: update `.analysis.md` when Feature Index mapping becomes invalid.
````

---

## Edge Cases

- **Monorepo**: map each package root plus a top-level package index.
- **Deep nesting**: layer-by-layer drill-down; each level's map stays local.
- **Huge flat directory** (`>200` files): group Files rows by Domain subheadings.
- **Generated code**: include only when navigation needs it; mark `Generated, do not edit manually`.
- **No metadata/README**: infer cautiously; mark uncertainty.
- **Task Guide gaps**: acceptable. Fall back to Domain filtering and Key Exports.
- **Foundational files** (>5 dependents): provide grep command, require Domain filtering.
