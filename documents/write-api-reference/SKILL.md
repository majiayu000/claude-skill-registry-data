---
name: write-api-reference
description: >-
  Load this skill when writing a project's user-facing reference docs: every public function,
  endpoint, CLI flag, config key, environment variable, and error. Trigger on "write the API
  reference", "document every endpoint", "document all the CLI flags".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Reads source files of the target project. Uses the git CLI on PATH for "Added in" markers
  (`git tag`, `git diff <tag>..<tag>`); without git or tags the markers come from CHANGELOG.md
  headings, and with neither they are omitted. Everything else still runs.
license: Apache-2.0
---

# Write API Reference

The reference is the **only exhaustive page type** in a docs set. Every other page is allowed to be
selective because this one is not: a guide shows the three options a task needs and links here for
the other twenty. A reference entry that is missing sends the reader to the source. A reference
entry that teaches crowds out the lookup.

Work against `<root>`: the project path handed over by the caller, or the current working
directory. Write under `<root>/docs/reference/`. Read
`${CLAUDE_PLUGIN_ROOT}/references/docs-standard.md` ("the standard" below) before writing: it fixes
the page anatomy, Markdown and link rules, markers (`_Added in <version>._`, the deprecation
blockquote, `[VERIFY: …]`), and report format used here.

## Procedure

### 1. Check whether a generator is already wired up

Check for `mkdocstrings` (`::: ` directives, `plugins:` in `mkdocs.yml`), Sphinx `autodoc`
(`conf.py` extensions), TypeDoc (`typedoc.json`), or a committed or served OpenAPI spec.

A spec or docstrings that exist but are not wired into the docs build (FastAPI serving
`/openapi.json` at runtime, docstrings with no `mkdocstrings`) count as **not configured**.

- **Configured:** do not hand-write signatures a generator already renders, because they drift.
  Write the reference index and one stub page per module holding the generator directive, and spend
  the effort on the docstrings the generator will render: list public items with a missing or
  one-word docstring as open items.
- **Not configured:** hand-write the Markdown below, and name the fitting generator in the report
  so the reference can later be kept in sync by the build instead of by hand.

### 2. Count the public surface

Enumerate before writing. The surface is **what a user can reach without importing a private
path**.

| Project kind            | The surface is                                                                                                                                                                         |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python library          | Names in `__all__`, else the non-underscore names re-exported from the package `__init__.py`; the classes' public methods and attributes                                               |
| TypeScript / JS library | The `exports` / `main` / `types` entries in `package.json` and everything their index files re-export, including type-only exports (interfaces, type aliases)                          |
| HTTP API                | Every route in the router files or the OpenAPI spec: method, path, auth, request, response, status codes                                                                               |
| CLI                     | Every command, subcommand, flag, and positional from the argparse / click / typer / commander definitions — cross-check against `--help` output when the CLI runs                      |
| Every kind              | Configuration: env vars read (`os.environ`, `getenv`, `process.env`, settings classes), config file keys, their defaults. Errors: exception classes and error codes a user can receive |

Counting rules, so two runs count the same thing:

- **Class members**: public methods, properties, and dataclass fields count. A dunder counts only
  when it gives the user a documented protocol (`__len__` → `len(q)`), never `__init__`: the
  constructor is documented on the class entry.
- **Submodules**: a non-underscore submodule is surface only when the README, docstrings, or
  examples import from it. Otherwise document its items under the public import path.
- **Framework routes**: defaults a deployment exposes (`/docs`, `/openapi.json`, `/redoc`) count as
  one item: a single entry headed `Framework routes` on `reference/service.md`, which also holds
  health and other non-resource endpoints, listing each path in a table.
- **Framework errors**: errors a user can receive from the framework rather than the project (a
  `422` validation error) count as one item: one grouped entry in `errors.md`.
- **Console scripts**: a `[project.scripts]` or `bin` target counts as the CLI, not also as API.
- **Errors a user predictably hits**: a built-in error the public surface throws on bad input (a
  `TypeError` for a non-string) and each CLI usage or exit-code error count as one Errors item
  each.
- **Count each item once.** An exception exported in `__all__` counts under Errors, not also under
  the API.

Record the total per kind. That count is the coverage target. The report states
`N of M documented`.

### 3. Lay out the pages

```text
docs/reference/
├── index.md            # every page, one line each: what it covers
├── <module>.md         # one page per public module / resource / command group
├── cli.md              # when there is a CLI
├── configuration.md    # every env var and config key
└── errors.md           # every exception / error code
```

Reference pages are **named after the code**, not by the `<PREFIX>-<NN>` reading-order scheme the
guide pages use: nobody reads a reference in order, they arrive by name, and a filename that
mirrors the module is the one they guess. Each page gets a breadcrumb under its H1,
`[← Reference](index.md)`, and no prev/next footer.

The page H1 is the public import path (`tinyq`, not `tinyq.queue`) or the resource name (`Notes`).

Within a page, group by kind and sort **alphabetically inside each group**, so a lookup never
depends on knowing the source order:

- **Libraries**: `## Classes`, each class entry followed by its members as `` ### `Class.member` ``
  (methods, then attributes, alphabetical); then `## Functions`, then `## Constants`, then
  `## Types` for exported interfaces and type aliases.
- **CLIs**: `reference/cli.md`, one `###` per command (`` ### `slugkit` ``, `` ### `tool sync` ``),
  its usage line in a `text` block, flags and positionals as rows of one table (Name, Type,
  Default, Description), then an exit-code table (Code, Meaning).
- **HTTP APIs**: one page per resource, endpoints ordered by path, then by method in the fixed
  order `GET`, `POST`, `PUT`, `PATCH`, `DELETE`. A CRUD reader expects that order, not the
  alphabet.
- **Errors**: headed by the exception name, or by the status code plus detail
  (`` `404 note not found` ``).

### 4. Write each entry

````markdown
### `Client.stream`

Stream a completion token by token. _Added in v2.3.0._

```python
def stream(self, prompt: str, *, model: str | None = None, timeout: float = 60.0) -> Iterator[Chunk]
```

| Parameter | Type          | Default  | Description                                                      |
| --------- | ------------- | -------- | ---------------------------------------------------------------- |
| `prompt`  | `str`         | required | The input text.                                                  |
| `model`   | `str \| None` | `None`   | Model id; `None` uses the client default.                        |
| `timeout` | `float`       | `60.0`   | Seconds before `TimeoutError`, measured per chunk, not per call. |

- **Returns:** `Iterator[Chunk]` — yields as tokens arrive.
- **Raises:** [`RateLimitError`](errors.md#ratelimiterror) when the quota is exhausted.
- **Why per-chunk timeout:** see [Streaming](../concepts/CO-03-streaming.md#why-it-works-this-way).
````

- **Signature, types, and defaults come from the code**, copied, never retyped from memory.
- **The description comes from the docstring.** Normalize it lightly (capitalize, end with a
  period, move "Raises X" into the Raises line) without changing its meaning. Where there is none,
  describe only behavior the code makes plain; otherwise write `[VERIFY: purpose of X]`.
- **Show an example only when usage is not obvious from the signature.** The guides carry the
  worked usage.
- **Surprising behavior gets a "Why" link** to the concept page that explains it. The reference
  states _what_, the concept states _why_. Never inline the rationale here.
- **Deprecated items** carry the standard's deprecation blockquote on the line after the heading:
  `> **Deprecated in <version>:** use <replacement>. Removed in <version>.`
- HTTP endpoints use this shape instead of a signature:

  ```markdown
  ### `POST /notes`

  Create a note. **Auth:** `x-api-key` header.

  | Request field | In    | Type     | Required | Description                                        |
  | ------------- | ----- | -------- | -------- | -------------------------------------------------- |
  | `body`        | query | `string` | yes      | Note text, at most `NOTESVC_MAX_NOTE_BYTES` bytes. |

  | Status | Body                           | When                                                      |
  | ------ | ------------------------------ | --------------------------------------------------------- |
  | `201`  | `{"id": 1, "body": "…"}`       | Created.                                                  |
  | `413`  | `{"detail": "note too large"}` | See [`413 note too large`](errors.md#413-note-too-large). |
  ```

- `errors.md` entries: when it is raised, what the user did to cause it, how to fix it. The guide
  troubleshooting page links here by error name.

### 5. Add the "Added in" markers

Experienced users open the reference to find what is new. Mark items **added in the last three
releases, never the initial release**. With fewer than two releases there is nothing to mark. Use
`_Changed in <version>: <what>._` for a changed default or behavior in the same window. Marker
formats and placement follow standard §7.

```bash
git -C <root> tag --sort=-creatordate | head -4          # newest tags
git -C <root> diff <older-tag>..<newer-tag> -- <public source paths>
```

A public name that first appears in a range's diff is _Added in `<newer-tag>`_, spelled as the tag
spells it (standard §7). When `CHANGELOG.md` places the addition in a different release, the
changelog wins on _which_ release. With no tags, date items from `CHANGELOG.md` alone and spell the
version as its heading does. With neither tags nor a changelog, omit the markers.

### 6. Self-review

- [ ] Coverage count done per kind; every counted item has an entry or an open item.
- [ ] No signature, type, or default was retyped; each was copied from source.
- [ ] Entries sorted alphabetically within kind groups.
- [ ] No rationale inlined: it lives behind a "Why" link.
- [ ] Every error a user can hit has an `errors.md` entry.
- [ ] Every page passes `${CLAUDE_PLUGIN_ROOT}/references/docs-standard.md` §4–§7: anatomy,
      Markdown, links, markers.

## Rules

- Count the surface before writing any entry. Coverage is reported against that count.
- Copy signatures, types, and defaults from the code. Never retype them from memory.
- The reference states what an item does. Rationale lives on a concept page behind a "Why" link.
- Mark anything the code does not make plain as `[VERIFY: …]` instead of guessing.

## Output

Pages under `<root>/docs/reference/`. End the reply with the report of
`${CLAUDE_PLUGIN_ROOT}/references/docs-standard.md` §10. When `write-project-docs` called this skill,
return only the rows, open items, and coverage line for it to merge. Put the coverage line above
the table in the form of standard §10, and the generator recommendation when no reference generator
is wired into the docs build. Open items include every undocumented surface item.
