---
name: mdx-pdf-format
description: Use whenever creating, renaming, or editing any file under docs/ in this repo, or when asked to compile/build the book PDF. Enforces the exact .mdx frontmatter, ID scheme, and heading-depth rules required by the go-pretty-pdf tool (https://github.com/sazardev/go-pretty-pdf) so the whole book keeps compiling.
---

# MDX format for go-pretty-pdf

This repo's book (`docs/`) is built into a PDF with `go-pretty-pdf`
(`go install github.com/sazardev/go-pretty-pdf/cmd/pretty-pdf@latest`). It only
picks up `.mdx` files (recursive walk of the `source` directory in
`go-pretty-pdf.yml`, currently `docs`) — `.md` files (like the `README.md`
indexes) are ignored by the build and can stay plain Markdown.

Every chapter file that should appear in the PDF **must** be `.mdx` and follow
the rules below. Breaking any of these makes `pretty-pdf check`/`build` fail.

## Required frontmatter

```yaml
---
id: "[X.Y.Z]"
title: "Chapter Title"
---
```

- `id` is mandatory and must match the regex `^\[\d+\.\d+\.\d+\]$` exactly —
  brackets included, three dot-separated integers, quoted as a YAML string.
  Documents are ordered in the PDF **by this ID**, not by filename.
- `title` is mandatory, quoted, and is what renders in the TOC/header.
- Optional fields (`subtitle`, `tags`, `difficulty`, `status`,
  `completeness`, `depends_on`) may be added but are not required — this repo
  intentionally omits them to keep frontmatter minimal; don't add them unless
  the user asks.
- No two files anywhere under `docs/` may share the same `id`.

### This repo's ID scheme

`X` is fixed per top-level folder, `Y` is the file's existing two-digit
numeric prefix, `Z` is reserved (always `0` today):

| Folder | X |
|---|---|
| `docs/front-matter/` | 0 |
| `docs/part1/` | 1 |
| `docs/go-fundamentals/` | 2 |
| `docs/part2/` | 3 |
| `docs/advanced/` | 4 |
| `docs/part3/` | 5 |
| `docs/part-apis/` | 6 |
| `docs/back-matter/` | 7 |

Example: `docs/part2/05-tcp-in-depth-...mdx` → `id: "[3.5.0]"`.

`docs/front-matter/` (X=0) and `docs/back-matter/` (X=7) hold non-chapter
content — About the Author, closing remarks — that sorts before Part 1 and
after Part APIs respectively, purely by virtue of their `id` being lower or
higher than every numbered chapter. They aren't part of the numbered
1-N chapter sequence in `README.md`; list them there as unnumbered entries
just before/after that numbered list instead.

`docs/go-fundamentals/` (X=2) sits between Part 1 and Part 2 in reading
order and covers the Go language itself (installation through testing,
including a dedicated goroutines/channels chapter) — it does not follow
Part 1's "theory only, no code" rule; it's the opposite, all hands-on Go.

When adding a **new** chapter, keep this scheme: pick the `X` for its folder,
and a `Y` that doesn't collide with an existing file in that folder (typically
the next free number, matching the file's numeric filename prefix).

## Heading depth

`go-pretty-pdf`'s linter caps heading depth at **h3** (`max_heading_depth: 3`
in `go-pretty-pdf.yml`). Never use `####`/`#####` in chapter content — if a
sub-point needs its own label, use a bold line (`**Request:**`) instead of a
new heading level, or fold it into the surrounding `###` section.

## Components available in MDX body

Three custom tags are transpiled to styled HTML — use them instead of plain
blockquotes when the intent matches:

- `<DeepDive title="...">...</DeepDive>` — blue info panel
- `<Warning title="...">...</Warning>` — orange warning panel
- `<Axiom>...</Axiom>` — green italic pull-quote

`title` is optional on `DeepDive`/`Warning`. Only simple inline Markdown
(code spans, `**bold**`) is rewritten inside these tags — don't nest complex
Markdown (tables, nested lists, headings) inside them.

**Hard rule, learned the hard way twice in this repo: write the content of
every `DeepDive`/`Warning`/`Axiom` tag as ONE physical line in the source
file**, no matter how long it looks in your editor — e.g.
`<Warning title="X">All of this stays on one line, however long, until the
closing tag.</Warning>` written as a single line, not soft-wrapped like a
normal paragraph. The renderer's HTML transpiler converts every literal
newline inside these tags into a forced `<br>`, so wrapping the text across
multiple source lines (as if it were ordinary prose) produces ugly, choppy,
mid-sentence line breaks in the printed PDF. This has nothing to do with
Markdown's own soft-wrap rules for regular paragraphs, which are unaffected —
it only applies to text between these specific opening and closing tags.

## Code block line length

Fenced code blocks render in a fixed-width box roughly 90 monospace
characters wide (9pt font on the default theme). A line longer than that
gets visually clipped at the right margin in the printed PDF instead of
wrapping — this applies to Go, shell, YAML, or any other fenced language.
Keep every line inside a code fence under about 85 characters after
expanding tabs to 8 spaces (`str.expandtabs(8)`), wrapping long struct
literals, function signatures, or calls across multiple lines, gofmt-style,
rather than one long line. This is easy to miss since the source file looks
fine in an editor — when in doubt, count.

## Variable substitution

`{{var}}` in any `.mdx` file is replaced from the `vars:` map in
`go-pretty-pdf.yml` before parsing. Only use this for values that are genuinely
config-driven (versions, product name); don't introduce new `{{...}}` vars
without adding them to `go-pretty-pdf.yml`.

## Keeping the index in sync

`README.md` (root) and `docs/part-apis/README.md` link to every chapter.
Whenever a chapter file is added, renamed, or removed, update the matching
link in whichever of those two index files references it — including the
`.mdx` extension in the link path.

## Exercise references must exist and build

`docs/part2/*.mdx` chapters routinely link to a runnable file under
`exercises/part2/`, e.g. `[Exercise: TCP Client](../../exercises/part2/05-tcp-client/main.go)`.
This link is a promise the reader can click through and run — treat a
chapter as incomplete, not just its exercise, until that promise holds:

- **Before adding an `[Exercise: ...](../../exercises/part2/NN-name/main.go)`
  link, the target file must already exist.** Never add the link first and
  the file later — a repo-wide audit once found 18 such links pointing at
  directories that were never created, exactly because a chapter got written
  before its exercise did.
- Extract the exercise verbatim from the chapter's own code block whenever
  the `.mdx` already contains a complete `package main` — the exercise
  should match what the chapter shows, not a rewritten variant.
- If the chapter's code block is a fragment (a bare function, a type with no
  `main`), the exercise file still needs a real, runnable `main()` — write
  one that exercises the fragment, don't ship a non-compiling snippet just
  because that's what the prose showed inline.
- Client/server pairs get **separate** exercise directories (matching
  `CLAUDE.md`'s existing convention, e.g. `06-udp-client` / `06-udp-server`)
  — never combine a client's and a server's own `func main()` into one file.
- **Verify every new or edited exercise builds** before considering the work
  done. This repo's `exercises/part2/` directories have no `go.mod`
  (`CLAUDE.md`), so `go build`/`go vet` in default module mode fails with
  "cannot find main module" regardless of whether the code is correct —
  that error is expected here, not a sign of a broken exercise. Validate
  with GOPATH mode instead, from inside the exercise's own directory:
  ```sh
  cd exercises/part2/NN-name && GO111MODULE=off go vet . && GO111MODULE=off go build -o /tmp/out .
  ```
  Also run `gofmt -l` over any new exercise file and fix anything it lists
  before treating the file as done.
- Exercises under a third-party dependency (currently just the
  `gorilla/websocket` ones, numbered 12 and 13) keep their own `go.mod` —
  validate those with a plain `go build ./...` from inside that directory
  instead of the `GO111MODULE=off` form above.

## Build/validate commands

```sh
pretty-pdf check        # validate frontmatter, IDs, heading depth
pretty-pdf build         # render docs/ -> the PDF configured in go-pretty-pdf.yml
```

Run `pretty-pdf check` after adding or editing any `.mdx` file to catch
format violations before they reach the build.
