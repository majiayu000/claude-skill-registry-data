---
name: entangled-mkdocs
description: Add documentation pages to an existing MkDocs + Entangled site, explain how to serve locally, help adapt documentation
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.1.0"
  languages: all
  audience: developers
  workflow: documentation
  since: "2026-03-10"
---

## What I do

I add new pages to an existing MkDocs + Entangled documentation site. I inspect the project's config and existing pages first, then produce a Markdown page with correct Entangled annotations, literate-programming prose, Mermaid diagrams where requested, and an updated `mkdocs.yaml`/`mkdocs.yml` nav entry.

## When to use me

- Document a module, algorithm, or feature
- Incorporate existing source code as annotated examples
- Add Mermaid diagrams to a page
- Register a new page in the site navigation

**Prerequisites**: `mkdocs.yaml`/`mkdocs.yml`, `docs/`, and `entangled.toml` must already exist.
Install: use uv or poetry (based on `pyproject.toml`) to add the following dependencies if missing:
`mkdocs-material mkdocs-entangled-plugin "entangled-cli>=2.0"` (`entangled-cli` installs the `entangled` command;
`>=2.0` required — `version = "2.0"` in `entangled.toml` is a v2 contract).

---

## Workflow

### 1 — Read (always first)

Complete all four preparation steps before writing anything:

**`mkdocs.yaml` or `mkdocs.yml`** (use whichever exists — keep the extension consistent):
- `docs_dir` (default: `docs`)
- Active `plugins:` — confirm `- entangled` is present; add it if missing
- Active `markdown_extensions:` — confirm `attr_list` and `pymdownx.superfences` are present (required by the plugin),
  and `pymdownx.tabbed` is present (required for Material tabbed content; if adding, also set `alternate_style: true` —
  without it Material falls back to legacy tab rendering); don't add duplicates
- `nav:` structure — note existing sections and any `!include` / external URL entries

**`entangled.toml`** — note the `watch_list` globs (these govern which `.md` files Entangled scans — not where `file=`
outputs may be written). Confirm the file has a `version` field (e.g. `version = "2.0"` — required; `entangled sync`
fails without it). If missing, add `version = "2.0"` to the file before proceeding.

**2–3 existing `docs/**/*.md` pages** (or all pages if fewer than 3 exist) — prefer pages with code blocks and
admonitions. Note heading style, admonition usage, and tangle output location (e.g. `docs/.python_files/`). Match these
conventions in your output. For non-Python projects fall back to `docs/.<lang>_files/<name>.<ext>` (e.g.
`docs/.ts_files/`).

**Block registry** — bootstrap the script if needed, then scan:

If `scripts/regenerate_registry.py` does not exist in the project, create the directory if needed and copy the script:

```bash
mkdir -p scripts
# then copy scripts/regenerate_registry.py from this skill's directory (alongside this SKILL.md)
```

```bash
python scripts/regenerate_registry.py
```

The script always overwrites `docs/entangled-registry.json` with the current state. Read that file and output a summary
**before proceeding to step 2**:

````
```registry-scan
# block IDs (count name)
  2 #some-duplicate-id
  1 #session-imports
...

# file= targets (count path)
  1 file=docs/.python_files/session.py
...
```
````

Any ID or path that appears is already claimed. If the script exits non-zero, the project has pre-existing duplicate
IDs — report them to the user and continue (they predate this session). Do not begin step 2 until this block is present
in your response.

### 2 — Write

Derive the filename in **kebab-case** from the topic (e.g. `session-management.md`). State the chosen filename
explicitly. If the topic maps to two or more equally plausible names (e.g. `auth.md` vs `authentication.md`), list them
and ask the user to choose before writing.

**Before writing**: check that `docs/<filename>.md` does not already exist. If it does, stop and ask the user whether to
overwrite, rename, or append.

Produce a new `.md` in `docs/`. Structure every section as **prose that introduces intent, followed by a code block or
diagram**. Never drop a bare block without context. Match the heading style, admonition usage, and prose tone of
existing pages.

Rules for every code block:

- Must have `file=` or `#id` (or both) — **except Mermaid blocks**, which are rendered not tangled and need neither
- Must not use an `#id` or `file=` path that appears in your registry (step 1), unless deliberate appending is
  intended — state that explicitly
- **Direct-append** (same `#id` repeated, output to file): the first block carries `file=`; subsequent blocks with
  the same `#id` are concatenated in document order. **Noweb assembly** (named sub-blocks assembled in a final block):
  sub-blocks like `#session-imports` must NOT carry `file=` — only the final assembly block does. **Cross-page append**:
  do not carry `file=` on the new page — the target is already registered on the defining page
- `file=` paths should stay within `docs/` by default; paths outside `docs/` will overwrite live source files when
  tangled — only use them if explicitly requested and confirmed by the user
- Use `docs/.python_files/<name>.py` as the default Python tangle path unless existing blocks show a different
  convention
- **Always use dot-prefixed language identifiers**: ` ```{.python ...} `, never ` ```{python ...} ` — the dot sets the
  CSS class (`.python` = `class="python"`) which both `pymdownx.superfences` and Entangled parse as the language
  identifier; a bare name is an attribute, not a class, and will not be recognised as a language. The plugin renders
  every `file=` block with a visible title bar; use `#id`-only if you want a block without a file-path header

If `pymdownx.arithmatex` is active, use `\(...\)` / `\[...\]` for math — not `$...$`. Note: `arithmatex` alone does not
render math; MathJax or KaTeX must also be configured via `extra_javascript`.

### 3 — Update nav and config

**Nav**: Find the existing `nav:` section whose topic best matches the new page and insert there. Create a new section
only if none fits. If no `nav:` block exists, create a minimal one listing existing pages plus the new one.

Never modify `!include` monorepo entries, external URL entries, or `mike`-versioning entries. Make the minimum change
necessary — do not reorder, rename, or remove any existing entries.

**Mermaid** (skip this section if the new page contains no Mermaid diagrams). Check `mkdocs.yaml`:

- `pymdownx.superfences` absent → add the full config below
- Present but missing `custom_fences:` → add just the custom fence block
- Already configured for Mermaid → do nothing

```yaml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
```

### 4 — Update block registry

Run the registry script again to capture the new page's block IDs and `file=` targets (step 1 scanned the pre-write
state; this records the post-write state for future sessions):

```bash
python scripts/regenerate_registry.py
```

Also add to `mkdocs.yaml` if not present (place at the **root level**, not under `plugins:` or `theme:`; requires
MkDocs ≥ 1.5):

```yaml
exclude_docs: |
  entangled-registry.json
```

Stage and commit in one commit. Always include:

- `docs/<new-page>.md`
- `docs/entangled-registry.json`

Also include if modified:

- `mkdocs.yaml` / `mkdocs.yml` (nav, `exclude_docs`, plugin, or extension changes)
- `scripts/regenerate_registry.py` (first use only)

### 5 — Preview

Search for a versioned build script from the **repository root** (so that `scripts/` or `.github/scripts/` at the root are included; if the docs live in a subproject, run `find` from the parent directory that contains `.github/` or the top-level `scripts/`):

```bash
find . -name "docs_build_versioned.sh" -not -path "*/node_modules/*" | head -1
```

Print the following command for the user to run (do not run it — it starts a live server):

If the `find` returns a path (e.g. `./.github/scripts/docs_build_versioned.sh`):

```bash
<found-path> --clean --serve   # clean, build, and serve at http://127.0.0.1:8000
```

Otherwise:

```bash
mkdocs serve       # preview at http://127.0.0.1:8000
```

The `- entangled` plugin runs a **per-page** tangle step automatically before each build — inline display blocks are
rendered without any manual step. However, the plugin processes each page in isolation and **cannot resolve `<<noweb>>`
references that point to blocks defined on other pages**. Cross-page assembly blocks must be kept inside HTML comments
(`<!-- ... -->`) so they are hidden from rendering but still readable by the `entangled` CLI.

**If the project uses a generate script** (e.g. `generate_examples.sh`) that runs `entangled tangle` CLI across all
pages and copies outputs into an `examples_from_docs/` (or similar) directory for `<!--codeinclude-->` Full Example
sections: whenever assembly blocks or noweb references change, run the script and commit both the intermediate tangle
outputs (e.g. `docs/.python_files/`) and the final examples directory. CI does not run this script — it uses whatever
is already committed.

```bash
find . -name "generate_examples.sh" -not -path "*/node_modules/*" | head -1
```

**Task complete when**: (1) `docs/<new-page>.md` is committed, (2) `docs/entangled-registry.json` is updated and
committed, (3) `mkdocs.yaml` nav entry is present, (4) the generate script has been run and its outputs committed if
the project uses one, and (5) the preview command has been printed. No further action is required unless the user
responds.

---

## Entangled syntax

All fenced code blocks **must** have `file=`, `#id`, or both. Mermaid blocks are exempt.

| Form                 | Example                                                                                                                                                                                                                                                                                                                            |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| File-targeting       | ` ```{.python file=docs/.python_files/mod.py} `                                                                                                                                                                                                                                                                                    |
| Named block          | ` ```{.python #block-name} `                                                                                                                                                                                                                                                                                                       |
| Both                 | ` ```{.python #main file=docs/.python_files/main.py} `                                                                                                                                                                                                                                                                             |
| ID only, no language | ` ```{#block-name} ` — no syntax highlighting; use for assembly/noweb entry points                                                                                                                                                                                                                                                 |
| Noweb reference      | `<<block-name>>` inside any block                                                                                                                                                                                                                                                                                                  |
| Append               | Two blocks with the same `#id` are concatenated in document order. The first must carry `file=` only if it is the direct output target; for pure noweb assembly, `file=` on the first block is not required. When appending to a block defined on another page, do not add `file=` — it is already registered on the defining page |

Fences may be 3 or 4 backticks. Both forms are valid.

**Always use the dot-prefix language identifier** (`.python`, `.typescript`, `.bash`, etc.). The dot sets the CSS
class (`.python` = `class="python"`) which both `pymdownx.superfences` and Entangled parse as the language identifier. A
bare `{python ...}` is an attribute name, not a class, and will not be recognised as a language by either tool.

**Noweb example** (present concepts in narrative order, assemble in a final block):

````markdown
## Imports

The module needs `secrets` for token generation.

```{.python #session-imports}
import secrets
```

## Session class

`Session` stores a user ID and a random token.

```{.python #session-class}
class Session:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.token = secrets.token_hex(32)
```

## Assembled module

```{.python #session file=docs/.python_files/session.py}
<<session-imports>>
<<session-class>>
```
````

Use `#id` + noweb when code must be introduced out of narrative order or split across sections.

**Cross-page noweb limitation**: the MkDocs plugin processes each page independently. A `<<block-name>>` reference
inside a rendered block will appear as raw text if `block-name` is defined on a different page. Cross-page noweb only
works via the `entangled` CLI (which reads all pages at once). Keep cross-page assembly blocks inside `<!-- ... -->`
HTML comments so they are tangle-only and never rendered. For display, define imports and snippets locally on the page
or inline the code directly.

See `assets/mkdocs-baseline.yaml` in this skill's directory for the full recommended MkDocs extension set.

---

## Behaviour rules

| Rule                              | Requirement                                                                                                           |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| Read before write                 | Always read config, `entangled.toml`, and existing pages before generating output                                     |
| Build and output registry         | Run the registry script; output results in response; do not begin step 2 before this list is present in your response |
| No overwrite without confirmation | Check that the target `.md` path does not exist before writing; if it does, ask the user                              |
| No duplicate `#id`                | Never reuse an ID from the registry unless deliberately appending — state that explicitly                             |
| No conflicting `file=`            | Don't target a path already claimed; use named-block appending instead                                                |
| `file=` stays in `docs/`          | Only use `file=` paths outside `docs/` if explicitly requested — tangle will overwrite live source files              |
| Plugin guard                      | Only add plugins/extensions that are genuinely absent; never duplicate                                                |
| Preserve nav                      | Never touch `!include`, external URL, or `mike` entries; make minimum change                                          |
| Dot-prefix language identifiers   | Always write ` ```{.python} `, never ` ```{python} ` — bare names are attribute keys, not CSS classes                 |
| Real code only                    | Read actual source files; never invent placeholder code                                                               |
| Regenerate registry               | Run the registry script (step 4) and commit `docs/entangled-registry.json` with the page                              |
| Prefer docs script                | Search `**/scripts/docs_build_versioned.sh` via `find`; use it with `--clean --serve` if found, else `mkdocs serve`   |

---

## Error handling

| Condition                                                            | Action                                                                                                 |
|----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| No `mkdocs.yaml` / `mkdocs.yml` found                                | Inform user, stop                                                                                      |
| No `docs/` directory                                                 | Ask for correct `docs_dir`, stop                                                                       |
| No `entangled.toml` found                                            | Warn; proceed but note that tangling will not run                                                      |
| `entangled.toml` missing `version` field                             | Warn user — add `version = "2.0"` before proceeding (v2 contract; tangle may fail without it)          |
| `- entangled` missing from `plugins:`                                | Add it before proceeding                                                                               |
| `attr_list`, `pymdownx.superfences`, or `pymdownx.tabbed` missing    | Add the missing extension(s) before proceeding; for `pymdownx.tabbed` also set `alternate_style: true` |
| Target `docs/<filename>.md` already exists                           | Stop; ask user whether to overwrite, rename, or append                                                 |
| Source file doesn't exist                                            | Inform user, stop                                                                                      |
| `file=` path already targeted                                        | Warn, use named-block appending                                                                        |
| `file=` target is outside `docs/`                                    | Warn user that tangle will overwrite a live source file; require explicit confirmation                 |
| New `.md` page not matched by `watch_list` in `entangled.toml`       | Warn user — the new page will not be tangled; adjust `watch_list` or move the file                     |
| `#id` already in registry                                            | Warn user; only proceed if deliberate appending is confirmed                                           |
| Registry script exits non-zero at step 1 (pre-existing duplicates)   | Report duplicates to user; continue — these predate this session                                       |
| Registry script exits non-zero at step 4 (new duplicates introduced) | List the new duplicates; ask user which to rename; do not commit until all duplicates are resolved     |
| Project uses `mike` versioning                                       | Don't add or modify version-related nav entries; insert only in the current config                     |
| No existing docs pages                                               | Use Material defaults as style baseline                                                                |
| Existing docs use bare language names (`{python`, `{bash`)           | Warn user — these blocks may render inconsistently; recommend standardising to dot-prefix              |