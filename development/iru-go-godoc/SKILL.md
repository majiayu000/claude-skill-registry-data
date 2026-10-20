---
name: iru-go-godoc
description: >-
  Audit given Go packages/files/identifiers (a Cobra command-line tool, library, or service) for complete Go doc comments as defined by go.dev/doc/comment — a package comment (in `doc.go` for a multi-file package; `Command <bin> …`-style for `package main`), and a comment on every exported function, method, type, constant, variable and struct field that matters, each starting with the identifier's name and written as full sentences ending in a period, with `Deprecated:` paragraphs, `[pkg.Name]`/`[Name]` doc links, and lists/code blocks in Go's doc-comment syntax — generate any missing or incomplete comments grounded in the actual code and current changes, then verify: golangci-lint v2 with a dedicated, throwaway config that enables only revive's `exported` (incl. stutter and the "should be of the form `Name …`" check) and `package-comments` rules plus `godot` (so a project config whose `comments` exclusion preset hides those findings can't mask gaps), `go vet`, and `go doc -all` per package to prove every comment renders and to catch unresolved `[Name]` doc links (which `go doc` leaves bracketed). Falls back to `go doc` + a grep audit when golangci-lint isn't installed. Never edits code, signatures, generated files (`// Code generated … DO NOT EDIT.`), `_test.go` files, or `testdata/`. Invoke as `/iru-go-godoc <packages-files-or-identifiers>` (comma-separated: `./internal/cli/...`, `internal/greet/greet.go`, `internal/greet.Greeting`, `github.com/acme/tool/internal/output.Envelope`), or `/iru-go-godoc` with no argument to scope to Go files touched by uncommitted changes plus commits on the current branch not yet on the base branch. Use whenever the user (or `iru-go-code-one-task-group` via `iru-gate-runner`) wants doc-comment completeness checked and filled in for Go code, instead of discovering gaps on pkg.go.dev after a release.
model: sonnet
allowed-tools: Read Edit Write Glob Grep Bash(git *) Bash(go list *) Bash(go doc *) Bash(go vet *) Bash(go build *) Bash(go env *) Bash(golangci-lint *) Bash(gofmt -l *) Bash(python3 -c *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(head *) Bash(test *) Bash(mkdir -p build*) Bash(rm -rf build/iru-go-godoc*)
---

# Go Doc Comments

Make sure a set of Go packages carry complete, well-formed doc comments, filling in whatever is missing, then prove the
result through revive's doc rules, `godot`, and `go doc`. This skill only adds/completes comments (and a `doc.go` file
holding a package comment when none exists) — it does not change behavior, signatures, imports, or any non-comment
code. Test code (`_test.go`, `testdata/`) and generated files are out of scope. It makes no assumptions about this
being any particular repository — discover the project's conventions fresh each run.

## Step 0 — Detect the module

`command -v go` (missing → stop: "Go toolchain not installed"); `go list -m -f '{{.Path}} {{.Dir}}'` for the module
path(s) (several lines in a `go.work` workspace); `command -v golangci-lint` and `golangci-lint version` (v2 needed for
Step 5's config; a v1 binary → use the fallback check and say so). Editing comments needs nothing else.

## Step 1 — Determine scope

- **Argument provided** (comma-separated): a package pattern (`./internal/cli/...`, `./internal/greet`) → every
  non-test `.go` file of the matched packages (`go list -f '{{.Dir}}: {{join .GoFiles " "}}' <pattern>`); a file path
  → that file (and its package for the package-comment check); an identifier (`internal/greet.Greeting`,
  `<module>/internal/output.Envelope`, `output.Envelope.Write`) → the declaration only (find it with `go doc -src`
  or `grep -n`).
- **No argument**: every non-test `.go` file touched by uncommitted changes plus commits on the current branch not yet
  on the base branch, same approach as `iru-update-docs`:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a`; ask only if genuinely ambiguous).
- Always drop: `_test.go` files, anything under `testdata/` or `vendor/`, files carrying the standard `// Code
  generated … DO NOT EDIT.` line (regenerate those from their source instead — report it), and files excluded by build
  constraints the project never builds. Say what was dropped.
- If the resulting scope is empty, tell the user there is nothing to document and stop.
- **What gets documented** (the audit set): every package in scope (one package comment); every **exported**
  top-level function, type, constant and variable, every exported method on an exported type (including methods on
  unexported types that satisfy an exported interface only when the project's revive config sets
  `checkPrivateReceivers`), exported interface methods, and exported struct fields whose meaning isn't obvious from
  the name and type. Unexported identifiers are out of scope (comment them only when the existing code does so
  habitually). `internal/` packages are still documented — `go doc` and contributors read them, and revive checks them.

## Step 2 — Discover this project's actual bar before auditing

- **Project lint config**: whether `.golangci.yml` enables `revive` (and which rules/arguments — `exported` with
  `checkPrivateReceivers`, `sayRepetitiveInsteadOfStutters`, `disableStutteringCheck`), `godot` (its `scope`, `period`,
  `capital`), `dupword`, `misspell`, and whether `linters.exclusions.presets` contains `comments` (which hides revive's
  doc findings in the project's own lint run — mention it as a follow-up; Step 5 checks regardless).
- **Observed style**: read 2–3 well-documented files near the scope and contributor guides (`CONTRIBUTING`,
  `CLAUDE.md`, `AGENTS.md`, `README`): voice ("Greeting returns …" — third person, the Go convention), whether struct
  fields are commented, whether `Example` functions (`example_test.go`) exist, line wrapping (Go doesn't enforce one;
  ~80–100 columns is common), and how errors are described. Follow the **stricter** of stated vs observed.

**The convention** (go.dev/doc/comment; Effective Go "Commentary"; Go Code Review Comments "Doc Comments"):

- **Package comment** — `// Package <name> <does what>.` immediately before the `package` clause, in exactly one file
  of the package; for a multi-file package that file is `doc.go` (create it when the package has none — the only new
  file this skill may write). For `package main` the comment describes the **command**: `// <Bin> <does what>.` (e.g.
  "Democtl greets people from the command line."), followed by usage notes; Cobra's `--help` remains the user-facing
  reference.
- **Declarations** — the comment starts with the identifier's name (`// Greeting returns …`, `// ErrEmpty is
  returned when …`, `// Shape is …`), may start with "A"/"An"/"The" for types, and is complete sentences ending in a
  period. Functions say what they return and when they return errors (name the sentinel/typed errors callers can
  match with `errors.Is`/`errors.As`), side effects, and concurrency safety when relevant. A `bool`-returning function
  says "reports whether". Grouped `const (…)`/`var (…)` blocks may carry one comment for the group; iota enums usually
  comment each value.
- **Deprecated** — a paragraph starting `Deprecated: ` (capital D, colon, space) at the end of the comment, naming the
  replacement. Carry existing ones over verbatim; never add one on a guess.
- **Doc links** — `[Name]` for an identifier in the same package, `[pkg.Name]` / `[pkg.Type.Method]` for an imported
  package (by its import name), `[path/to/pkg.Name]` for a full import path; they render as links on pkg.go.dev and as
  plain text in `go doc`. URLs are written bare; a link target list (`[text]: https://…`) is allowed at the end.
- **Syntax** — a blank `//` line separates paragraphs; lists are lines starting with `-`/`*`/`1.` indented within
  the comment; code blocks are indented lines; headings are `# Heading` lines (only in package comments, preceded
  and followed by blank lines). gofmt reformats doc comments to canonical form — keep edits gofmt-clean.
- **Stutter** — `docs.DocsThing` reads repetitively; revive flags it. Renaming is a code change: report it as a
  follow-up, don't rename.

## Step 3 — Audit each in-scope package

Start mechanical — the same dedicated config Step 5 uses (write it now so the before/after runs match):

```bash
mkdir -p build/iru-go-godoc
cat > build/iru-go-godoc/golangci.yml <<'YAML'
version: "2"
linters:
  default: none
  enable: [revive, godot]
  settings:
    revive:
      rules:
        - name: exported
          arguments: ["checkPrivateReceivers"]
        - name: package-comments
    godot:
      scope: declarations
  exclusions:
    generated: strict
YAML
golangci-lint run -c build/iru-go-godoc/golangci.yml --path-mode=abs --uniq-by-line=false \
  --max-issues-per-linter=0 --max-same-issues=0 --show-stats=false \
  --output.json.path="$PWD/build/iru-go-godoc/before.json" --output.text.path=/dev/null <packages>
```

- v2 resolves a relative `--output.json.path` against the **config file's directory** (verified) — keep the `$PWD/…`
  prefix. `--uniq-by-line=false` matters: by default golangci-lint keeps one issue per line, and a `godot` finding on
  the same line as a revive one was dropped (verified). Drop `checkPrivateReceivers` when the project's revive config
  doesn't set it, so this skill's bar matches the project's.
- Exit `0` clean, `1` issues, `3` tooling failure (report it). Read the JSON with `python3 -c` — keep `FromLinter`,
  `Text`, `Pos.Filename`, `Pos.Line` per issue; never paste the raw file. Messages: `package-comments: should have a
  package comment`, `exported: exported function X should have comment or be unexported`, `exported: comment on
  exported function X should be of the form "X ..."`, `exported: type name will be used as pkg.PkgThing by other
  packages, and that stutters`, godot `Comment should end in a period`.
- **No golangci-lint** (or a v1 binary): fall back to `go doc -all <pkg>` per package plus reading each file — an
  exported identifier listed by `go doc -all` with no text under it is undocumented; a package with no line after
  the `package … // import …` header has no package comment. Say "revive/godot not run — fallback audit".

Then read each full file — the linters only check presence and form, not whether the comment is any good — and for
every symbol in the audit set check that the comment exists, starts with the name, describes current behavior (not
what the name suggests), names the errors callers can match, and keeps any `Deprecated:` paragraph. Record per gap:
symbol, kind, what's missing (whole comment, wrong first word, missing error/return description, missing period).

## Step 4 — Write the missing comments

Before editing, keep Step 3's `before.json` (and `go vet` output) as the baseline so Step 5 can tell pre-existing
problems from ones this run caused. For every gap, write the comment grounded in:

- The actual implementation — read the body: what is returned and when (zero values, `nil` slices), which errors are
  returned or wrapped (`fmt.Errorf("…: %w", err)` → "wraps the underlying error"), sentinel/typed errors, context
  cancellation behavior, goroutines started, whether it is safe for concurrent use, side effects (files, network,
  env vars). Never claim a guarantee the code doesn't give.
- Current uncommitted/branch changes (`git diff` / `git log -p` for that file) — describe current behavior.
- The convention from Step 2 — voice, wrapping, field-comment habit — so new comments are indistinguishable from
  hand-written ones.

Apply edits with the Edit tool directly above the declaration (or inside the `const (…)`/`var (…)`/struct block for
members), with no blank line between comment and declaration. A missing package comment goes into the package's
existing `doc.go`, else a new `doc.go` containing only the comment and the `package` clause (plus the license header
the repository's other files carry, copied from a sibling file). For `package main` with a single `main.go`, put it in
`main.go` above `package main`. Do not modify code, signatures, build tags, imports, or formatting outside the added
comments, and don't reorder declarations.

## Step 5 — Verify

1. **revive + godot** — re-run Step 3's command into `build/iru-go-godoc/after.json`. Every finding in an in-scope
   file must be gone, except stutter findings (a rename — report as a follow-up) and findings on symbols the user
   excluded. A finding in an in-scope file on a symbol this run didn't touch is still a gap — fix it.
2. **Formatting** — `gofmt -l <edited files>` must print nothing (it exits `0` either way — read the output). gofmt
   canonicalizes doc comments (list indentation, code-block tabs); if it lists a file, the comment syntax is off — fix
   the comment by hand (this skill never runs `gofmt -w` on code it doesn't own).
3. **Compiles and vets** — `go build ./...` (a stray `*/` or a comment swallowing a declaration shows up here) and
   `go vet <packages>`; compare with the baseline — only new findings in in-scope files are this run's to fix.
4. **Renders** — `go doc -all <package>` for each in-scope package: the package comment appears under the header,
   every audited symbol shows its text, `Deprecated:` paragraphs survive. Then the doc-link check —
   `go doc -all <package> | grep -n '\[[A-Za-z_][A-Za-z0-9_.]*\]'`: `go doc` renders resolved links as plain text but
   leaves an **unresolved** same-package link bracketed (verified: `[Nope]` stayed `[Nope]`, `[Wrong]` became
   `Wrong`). It does not verify a symbol in another package (`[strings.Nope]` rendered as `strings.Nope`) — for each
   cross-package link you wrote, confirm it with `go doc <pkg>.<Name>` (exit `0`).

A failure naming a symbol or file **outside** the current scope is pre-existing — mention it as a follow-up, don't
fix it unless the user asks. Delete `build/iru-go-godoc/` afterwards (`rm -rf build/iru-go-godoc*`; remove `build/`
only if this run created it).

## Step 6 — Report

Per package in scope: how many symbols were already fully documented, how many gaps were found and filled (name
each, with its kind and what was added — e.g. "`doc.go`: package comment (new file)", "`Envelope` type: comment +
3 field comments", "`Write()`: error description (`ErrBrokenPipe`)"). Then the verification result per check —
revive `exported`/`package-comments` and `godot`: clean or the remaining findings (stutter renames listed as
follow-ups); `gofmt -l`: clean; `go build`/`go vet`: clean or pre-existing; `go doc`: rendered, unresolved links none or
listed — and which checks couldn't run (no golangci-lint → fallback audit). Mention a project config whose `comments`
exclusion preset hides these findings in its own lint run. Never paste raw tool output or JSON.

Do not fix lint issues unrelated to doc comments, rename identifiers, change code to make a comment "true", edit
`.golangci.yml`, edit license headers, or add/modify tests or `Example` functions — those belong to
`iru-go-code-quality`, the coding skills, and the user.

## Verification notes

Verified with Go 1.27.2 and golangci-lint 2.15.0 in `$TMPDIR/iru-verify/cli/go-gates/demo` (a throwaway Cobra CLI
module outside this repository), on a package with a lowercase comment not starting with the function name, an
undocumented type, method and const, a stuttering type name, a `Deprecated:` paragraph, and no package comment:

- The dedicated config passed `golangci-lint config verify`; the run reported `revive` `package-comments: should have
  a package comment`, four `exported: … should have comment or be unexported`, `comment on exported function Wrong
  should be of the form "Wrong ..."`, the stutter finding, and — only with `--uniq-by-line=false` — `godot` `Comment
  should end in a period` on the same line as the `Wrong` finding.
- In the project's own config, `exclusions.presets: [comments]` suppressed every revive `exported`/`package-comments`
  finding — the reason this skill uses its own config. Relative `--output.json.path` with `-c build/…/golangci.yml`
  wrote to `build/…/build/…`; the `$PWD/` prefix fixed it.
- After adding a `doc.go` package comment with `[Wrong]`, `[Shape]` and a full-import-path link, name-first comments,
  a field comment and keeping `Deprecated: use [Wrong] instead.`, the run was clean (exit `0`), `go vet` was clean,
  and `go doc ./internal/docs Old` printed `Deprecated: use Wrong instead.`. `[Nope]` stayed bracketed in
  `go doc -all`; `[strings.Nope]` rendered as `strings.Nope` without complaint (cross-package targets aren't checked).
- Still unverified: `package main` command comments rendered on pkg.go.dev (not published), revive's
  `sayRepetitiveInsteadOfStutters` argument wording, and doc comments in files behind non-default build tags.

## Sources

- go.dev/doc/comment (Go Doc Comments: package/command/type/func/const/var comments, `Deprecated:`, doc links, lists,
  code blocks, headings, gofmt reformatting)
- go.dev/doc/effective_go (Commentary); go.dev/wiki/CodeReviewComments (Doc Comments, Package Comments)
- `go doc cmd/go` (`go doc -all`, `-src`); pkg.go.dev/go/doc/comment
- golangci-lint docs (golangci-lint.run): revive (`exported`, `package-comments`), godot, `--uniq-by-line`, v2
  configuration; revive rules reference (github.com/mgechev/revive, RULES_DESCRIPTIONS.md)
- irurueta docs: ai/cli-for-agents/documenting-clis.adoc (API docs for the library unit, generated CLI reference)
