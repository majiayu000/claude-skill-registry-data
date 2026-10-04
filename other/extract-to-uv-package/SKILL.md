---
name: extract-to-uv-package
description: Extract a directory or set of Python files from an existing repo into a fresh standalone uv-managed package using the src layout, so it can be added as an editable dependency (`uv add --editable`, preferred) from sibling uv projects. Verifies byte-perfect preservation with sha256 checksums; hides originals as dotted .bak files instead of deleting so the move is reversible. Use when the user says "move X to its own repo", "make X pip-installable", "extract X as a package", or wants to break a monorepo into smaller installable units.
argument-hint: <source files or dir> <new package name>
allowed-tools: Read, Write, Bash(uv:*), Bash(sha256sum:*), Bash(diff:*), Bash(cp:*), Bash(mv:*), Bash(mkdir:*), Bash(ls:*), Bash(awk:*), Bash(find:*), Bash(which:*), Bash(test:*), Bash(cd:*), Bash(echo:*), Bash(for:*), Bash(tee:*)
---

# Extract files into a uv-managed editable-install package

Move a set of Python files out of an existing repo into a brand-new uv package
(`src` layout), verify byte-for-byte that nothing was lost, and hide the
originals as `.bak` files so the move stays reversible. The new package is
intended to be consumed from sibling uv projects via `uv add ../<new_repo>
--editable` (preferred — see "Two install interfaces" below) or, in non-uv
environments, via `uv pip install -e <new_repo>`.

## Conceptual background (why we do it this way)

**What a Python package is.** A directory containing `__init__.py` is an
*import package* — `import name` finds it on `sys.path`. A *distribution
package* is that directory wrapped with a `pyproject.toml` so `pip` can build
and install it. People conflate the two; both matter.

**Flat layout vs src layout.** The src layout (`src/<name>/__init__.py`) is
preferred over a flat layout (`<name>/__init__.py` at repo root) because the
repo root no longer *is* the import path. That forces the developer to actually
install the package to import it — catching the "works only because I happen to
be in the source dir" footgun, and keeping test/tooling files at the repo root
out of the installed namespace.

**Why `uv init --package <name>`.** It scaffolds the src layout, writes a
`pyproject.toml` with `hatchling` as the build backend, creates
`.python-version`, makes an empty `__init__.py`, and `git init`s the repo. Skips
all the boilerplate.

**Why editable install.** The consuming environment imports straight from the
source directory, so edits in the new package are seen immediately by consumers
— no rebuild, no reinstall. Right tool while the package is unpinned and under
active development.

**Two install interfaces — and why `uv add` is preferred.** uv exposes two
distinct ways to install a package, and they are NOT interchangeable:

- `uv add <pkg>` (and `uv add --editable <path>`) is the **project manager**
  interface. It edits `pyproject.toml`, updates `uv.lock`, and installs into
  `.venv` atomically. The dep becomes part of the project's declared state, so
  any future `uv sync` (yours, a teammate's, CI's) reproduces the same
  environment.
- `uv pip install <pkg>` is the **pip drop-in** interface. It installs into the
  active venv but does NOT edit `pyproject.toml` and does NOT touch `uv.lock`.
  The dep is invisible to the project metadata. A subsequent `uv sync` will
  notice the venv has packages not listed in the lock and **remove them** to
  bring the venv back in line with the declared state — silently undoing the
  install.

Rule of thumb: inside a uv project, always use `uv add` for deps. Reserve `uv
pip install -e` for venvs that are NOT uv projects (a plain `python -m venv`,
a legacy requirements.txt setup, transient CI installs). When this skill's
output is consumed from another uv project, recommend `uv add --editable
../<PKG>`, not `uv pip install -e`.

**Why `.bak` instead of `git rm` or hard delete.** Leaves a reversible safety
net. Files prefixed with `.` are hidden from `ls`; the `.bak` extension means
Python's import machinery won't discover them as modules, so removing the file
from the importable namespace is immediate. If the migration goes wrong, `mv
.foo.py.bak foo.py` restores it.

## Core recipe

Substitute `<PKG>` (e.g. `vision_core`), `<SRC_DIR>` (the repo files come
from), and `<FILES>` (the relative paths inside `<SRC_DIR>` to extract).

### 1. Pre-flight

```bash
which uv && uv --version
test ! -e ~/repo/<PKG> && echo "OK: ~/repo/<PKG> does not exist"
cd <SRC_DIR> && ls <FILES>
```

Bail if `uv` is missing, the destination already exists, or any source file is
missing.

### 2. Baseline checksums

```bash
cd <SRC_DIR>
sha256sum <FILES> | tee /tmp/<PKG>_before.full
awk '{print $1}' /tmp/<PKG>_before.full | sort > /tmp/<PKG>_before.hashes
```

The sorted hash list captures the *multiset of file contents*, independent of
path or order. Diffing two such lists later proves no bytes were lost.

### 3. Scaffold the package

```bash
cd ~/repo && uv init --package <PKG>
```

Produces:

```
~/repo/<PKG>/
  pyproject.toml          # name: <pkg-with-hyphens>
  README.md
  .python-version
  .gitignore
  .git/
  src/<PKG>/
    __init__.py
```

### 4. Copy (not move) files

```bash
cp <SRC_DIR>/<file1> ~/repo/<PKG>/src/<PKG>/<file1>
cp <SRC_DIR>/<file2> ~/repo/<PKG>/src/<PKG>/<file2>
# ...
```

Copy, not move — originals must still be present so the checksum check has
something to compare against.

### 5. Verify byte-perfect preservation (two ways)

```bash
cd ~/repo/<PKG>/src/<PKG>
sha256sum <FILES> | tee /tmp/<PKG>_after.full
awk '{print $1}' /tmp/<PKG>_after.full | sort > /tmp/<PKG>_after.hashes

# (a) multiset diff — must be empty
diff /tmp/<PKG>_before.hashes /tmp/<PKG>_after.hashes && echo "OK: byte-identical multiset"

# (b) per-file pairwise diff — confirms each file landed at the right path
for f in <FILES>; do
  diff -q <SRC_DIR>/$f ~/repo/<PKG>/src/<PKG>/$f && echo "OK: $f identical"
done
```

Both must pass before proceeding. If either fails, stop and investigate — do
not touch the originals.

### 6. Hide originals as `.bak`

```bash
cd <SRC_DIR>
mv <file1> .<file1>.bak     # e.g. datastructs.py -> .datastructs.py.bak
mv <file2> .<file2>.bak
# ...
```

The dotted prefix hides from `ls`; the `.bak` extension keeps them out of
Python's import path.

### 7. Re-checksum the `.bak` files

```bash
cd <SRC_DIR>
sha256sum .<file1>.bak .<file2>.bak ... | awk '{print $1}' | sort > /tmp/<PKG>_bak.hashes
diff /tmp/<PKG>_before.hashes /tmp/<PKG>_bak.hashes && echo "OK: .bak files match originals byte-for-byte"
```

Proves the rename didn't corrupt anything.

### 8. Report

Report to the user:
- New package layout (the `src/<PKG>/` tree).
- What was verified (multiset diff + per-file diff + post-rename re-check).
- What the user still needs to do before anything works:
  - Rewrite imports in consumer repos from `from <old_name>` to `from <PKG>.<old_name>`.
  - Install the package in each consumer:
    - **If the consumer is a uv project (preferred):** `cd <consumer> && uv add --editable ~/repo/<PKG>`. This edits the consumer's `pyproject.toml` + `uv.lock`, so the dep survives future `uv sync`s.
    - **If the consumer is a plain venv (not a uv project):** `uv pip install -e ~/repo/<PKG>`. Note this does NOT edit any pyproject — a later `uv sync` in a uv project would silently undo it.
  - Once they're confident, the `.bak` files can be deleted.

## When applying this skill

1. **Confirm the file list with the user before copying.** Don't assume which
   files belong in the new package — the user should have already decided this
   (often via a dependency analysis). If they haven't, ask.
2. **Confirm the package name.** Use the underscore form for the Python import
   name (`vision_core`); uv will derive the hyphenated distribution name
   (`vision-core`) automatically.
3. **Do not rewrite imports in this skill.** Import rewriting is a separate
   step the user should approve. This skill stops at "files are copied and
   verified, originals are hidden."
4. **Do not delete the `.bak` files.** They're the safety net. The user
   deletes them when they're satisfied the migration works.
5. **Do not install the package or modify consumer repos.** Those are
   downstream concerns; this skill only sets up the source tree.
6. **If the destination repo already exists, stop and ask.** Do not merge into
   an existing directory — that defeats the verification.
7. **Run all checksum diffs through `sort`, not `sort -u`.** Identical files
   (e.g. two empty `__init__.py`s) must produce duplicate hashes, and `-u`
   would collapse them.
