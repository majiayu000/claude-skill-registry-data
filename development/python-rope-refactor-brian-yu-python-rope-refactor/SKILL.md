---
name: Python Rope Refactor
description: Rope-first workflow for ANY mechanical Python rename/move (functions/methods/classes/variables/modules/packages), updating imports/references via scripts/rope_refactor.py; use even for small renames; only fallback if rope fails/dynamic imports.
---

# Python Rope Refactor

## Default policy (rope-first)

When the user asks for mechanical Python refactors like **move module**, **rename module**, or **rename class/function/symbol**, default to running rope via `uv run scripts/rope_refactor.py` rather than manually editing imports/usages.

Workflow:
- run with `--dry-run`
- review output; then run with `--apply`
- review `git diff`
- run relevant checks (tests/mypy/pyright)

Only fall back to manual edits when rope fails or the code uses dynamic/string-based imports.


Use this skill when you need reliable, mechanical Python refactors (especially in larger codebases) and want imports/usages updated automatically.

This skill provides a small CLI wrapper around `rope` refactorings with a safe workflow.

## Quick start

1) Ensure you are in the repo you want to refactor.
2) Make sure that `uv` is installed.

Tip: in large monorepos, prefer `--auto-project-root` (and optionally `--auto-scan-roots`) to avoid rope scanning the entire repo.

Example (paths can be relative to repo root; the tool will re-root them):

```bash
uv run scripts/rope_refactor.py \
  rename-symbol \
  --project-root . \
  --auto-project-root \
  --auto-scan-roots \
  --file path/to/file.py \
  --symbol OldName \
  --context class \
  --new-name NewName \
  --dry-run
```


If roots are too narrow (missed references):
- After `--apply`, run `rg` for the old symbol/module name(s) to confirm no leftovers.
- If leftovers exist, widen scanning and rerun:
  - use `--scan-roots <top-level-package>` (e.g. `--scan-roots responsesapi`)
  - or omit `--scan-roots`/`--auto-scan-roots` to scan the whole project root (slow but complete)

3) Run a dry-run first:

```bash
uv run scripts/rope_refactor.py --help
uv run scripts/rope_refactor.py move-module --help
```

4) Apply, then review:

```bash
uv run scripts/rope_refactor.py ... --apply
git diff
```

## Common refactors

### Move a module (file) to another package

Example: move `pkg/old_mod.py` into the `pkg/newpkg` package.

Destination package must exist on disk and include `__init__.py` (rope requires a real package folder).

```bash
uv run scripts/rope_refactor.py \
  move-module \
  --project-root . \
  --auto-project-root \
  --src pkg/old_mod.py \
  --dest-package pkg.newpkg \
  --dry-run

uv run scripts/rope_refactor.py \
  move-module \
  --project-root . \
  --auto-project-root \
  --src pkg/old_mod.py \
  --dest-package pkg.newpkg \
  --apply
```

### Rename a module (file) within a package

Example: rename `pkg/foo.py` to `pkg/bar.py` (module name `foo` -> `bar`).

```bash
uv run scripts/rope_refactor.py \
  rename-module \
  --project-root . \
  --auto-project-root \
  --src pkg/foo.py \
  --new-name bar \
  --dry-run

uv run scripts/rope_refactor.py \
  rename-module \
  --project-root . \
  --auto-project-root \
  --src pkg/foo.py \
  --new-name bar \
  --apply
```

### Rename a symbol (class/function/variable)

Rope renames based on a precise cursor/offset into a file.

This wrapper lets you target the symbol precisely:
- `--offset` (most precise)
- `--pattern` + optional `--occurrence` and `--group`
- `--symbol` + `--context class|def|any` (builds a safer pattern when `--pattern` is omitted)

Example: rename a class `OldName` -> `NewName` using `--symbol` targeting (recommended):

```bash
uv run scripts/rope_refactor.py \
  rename-symbol \
  --project-root . \
  --auto-project-root \
  --file pkg/models.py \
  --symbol OldName \
  --context class \
  --new-name NewName \
  --dry-run
```

Example: rename a class `OldName` -> `NewName` using a pattern:

```bash
uv run scripts/rope_refactor.py \
  rename-symbol \
  --project-root . \
  --auto-project-root \
  --file pkg/models.py \
  --new-name NewName \
  --pattern 'class\\s+OldName\\b' \
  --dry-run

uv run scripts/rope_refactor.py \
  rename-symbol \
  --project-root . \
  --auto-project-root \
  --file pkg/models.py \
  --new-name NewName \
  --pattern 'class\\s+OldName\\b' \
  --apply
```


### Extract a function/method

Extract a line range into a new function:

```bash
uv run scripts/rope_refactor.py \
  extract-function \
  --project-root . \
  --auto-project-root \
  --file pkg/mod.py \
  --start-line 10 \
  --end-line 25 \
  --new-name helper_fn \
  --dry-run
```

Extract a line range into a method:

```bash
uv run scripts/rope_refactor.py \
  extract-method \
  --project-root . \
  --auto-project-root \
  --file pkg/mod.py \
  --start-line 10 \
  --end-line 25 \
  --new-name _helper \
  --dry-run
```

### Inline

Inline a variable at a specific definition site using `--symbol` targeting:

```bash
uv run scripts/rope_refactor.py \
  inline-variable \
  --project-root . \
  --auto-project-root \
  --file pkg/mod.py \
  --symbol TEMP \
  --context any \
  --dry-run
```

### Organize imports

```bash
uv run scripts/rope_refactor.py \
  organize-imports \
  --project-root . \
  --auto-project-root \
  --roots pkg \
  --dry-run
```

### Batch (JSON-driven)

Create a JSON file (list of ops or `{"ops": [...]}`), then run:

```bash
cat > /tmp/rope_ops.json <<'JSON'
[
  {"op": "rename-module", "src": "pkg/foo.py", "new_name": "bar"},
  {"op": "move-module", "src": "pkg/bar.py", "dest_package": "pkg.subpkg"},
  {"op": "rename-symbol", "file": "pkg/subpkg/bar.py", "symbol": "OldClass", "context": "class", "new_name": "NewClass"},
  {"op": "organize-imports", "roots": ["pkg"]}
]
JSON

uv run scripts/rope_refactor.py \
  batch \
  --project-root . \
  --auto-project-root \
  --map /tmp/rope_ops.json \
  --dry-run
```

## Safety rules and gotchas

- Prefer `--dry-run` first; always review `git diff` after `--apply`.
- Rope can miss dynamic imports and string-based references:
  - `importlib.import_module("pkg.old_mod")`
  - framework config like `"pkg.mod:Class"`
- Consider leaving a temporary compatibility re-export after big moves (optional):

```python
# old_mod.py
from pkg.newpkg.old_mod import SomeName
__all__ = ["SomeName"]
```

## When to fall back to non-rope edits

If rope fails due to version/API differences or code is too dynamic:
- do the filesystem move/rename
- do a targeted `rg` search + update imports manually
- run tests / mypy / pyright to confirm
