---
name: iru-setup-go-gitignore
description: >-
  Create or update the root `.gitignore` for a Go repository — the command-line tool layout `iru-setup-go-cli`
  produces (`go.mod`, `cmd/<bin>/`, `internal/`, `tools/gendocs`, `testdata/script/`) or any other Go module —
  covering the binary `go build` leaves at the root (`/<bin>`, `/<bin>.exe`, root-anchored so `cmd/<bin>/` stays
  tracked), test binaries and profiles (`*.test`, `*.pprof`), coverage output (`coverage.out`, `*.coverprofile`,
  `coverage.html`, a `/covdata/` GOCOVERDIR), the `build/` report/docs-generator directory (`build/coverage/cover.out`,
  `build/gendocs/`), GoReleaser's `dist/`, per-developer `go.work`/`go.work.sum` (unless the repository deliberately
  tracks a workspace), `/vendor/` only when dependencies are not vendored (asked), env files (keeping `.env.example`),
  the Antora docs build output, editor/OS files, the repository-wide `.integration-test.lock/`, and — for a Bubble Tea
  terminal UI — the UI tests' capture directory `.ui-screenshots/` (never `.ui-quality.yml`). Never ignores
  `go.mod`, `go.sum`, `testdata/` or `.secrets.baseline`. Invoke as `/iru-setup-go-gitignore`, optionally with `args`
  (`key: value` lines): `bin-name` (default: every `cmd/<name>/` directory, else the module path's last element),
  `vendor: yes|no`, `mode: new|existing` (default: detected) and `on-existing: ask|keep|update|replace` (default
  `ask`). Announces whether it is creating from scratch or updating; an existing `.gitignore` is never overwritten
  silently — it warns, shows a diff, and asks Update (merge in what's missing, keep hand-added lines) / Keep as is /
  Replace, unless `on-existing` decides. Use whenever a Go repository needs a `.gitignore` bootstrapped from scratch,
  or an existing one checked and gap-filled against this house template.
model: haiku
---

# Setup Go Gitignore

Create or refresh the root `.gitignore` of a Go module — typically a command-line tool scaffolded by
`iru-setup-go-cli`. The template is a trimmed, house-style version of GitHub's `Go.gitignore` extended with what this
catalog's scaffold, gates and release tooling actually write. Never overwrite an existing `.gitignore` without showing
the user exactly what would change and getting explicit approval first — it can carry hand-added, project-specific
entries that must not be dropped silently.

## Step 0 — Resolve inputs

Parse `args` as `key: value` lines, skipping any question already answered:

- `bin-name` — the binary name(s) to ignore at the root, comma-separated. Default (Step 1): every directory under
  `cmd/` that holds a `main.go`, else the last element of the `module` path in `go.mod` (minus a `/vN` suffix) when a
  root `main.go` declares `package main`, else none.
- `vendor: yes|no` — `yes` = dependencies are vendored (`vendor/` is committed, never ignored); `no` = ignore
  `/vendor/`. Default: detected in Step 1, asked only when ambiguous.
- `mode: new|existing` — if omitted, detected: a root `.gitignore` means `existing`. `mode: existing` never means
  "update silently" — the existing file still goes through Step 5's question unless `on-existing` decides.
- `on-existing: ask|keep|update|replace` — default `ask`; `keep`/`update`/`replace` applies that choice without asking
  (the warning and diff are still printed). Only for scripted runs; an orchestrator passes it only if its own `args`
  received it.

Any other key (e.g. the full shared-args set `iru-setup-cli-repository` may forward: `language`, `ui`, `distribution`,
…) is ignored and named in the report.

## Step 1 — Survey the repository

Detect, before composing anything:

- `go.mod` at the root (read its `module` line). None → warn that this skill targets Go modules and ask whether to
  continue.
- The binary names (`cmd/*/main.go`, or a root `main.go` with `package main`) for `bin-name`'s default.
- **Vendoring**: `vendor/modules.txt` tracked (`git ls-files vendor/modules.txt`) or present → `vendor: yes`, no
  question. No `vendor/` directory at all → ask with `AskUserQuestion` (unless `args` set it): **Not vendoring
  (Recommended)** — "Ignore `/vendor/` so a stray `go mod vendor` is never committed; the module cache and `go.sum`
  pin dependencies." / **Vendoring** — "You'll run `go mod vendor` and commit `vendor/` (builds without network access);
  `/vendor/` is not ignored." A `vendor/` directory that exists but is untracked → ask the same question, saying it
  exists.
- **Workspace**: `go.work` tracked (`git ls-files go.work`) → the repository deliberately shares a workspace: don't
  ignore `go.work` or `go.work.sum` (commit both — `go.work.sum` holds checksums for the workspace modules'
  dependencies that no single `go.sum` records). Otherwise ignore both (see the note in Step 2).
- `.goreleaser.yaml`/`.goreleaser.yml` (→ `dist/` is GoReleaser's), `tools/gendocs/` (→ `build/gendocs/`),
  `docs/antora.yml` or `docs/antora-playbook.yml` (→ Antora section), a root `package.json` (→ Node section).
- Tracked files under a path the template would ignore (`git ls-files -- build dist '*.test' coverage.out
  '<bin>'`) — flag each in the report: writing `.gitignore` never untracks anything.
- The root `.gitignore`, if present — read it.

Then tell the user which of the two this run is doing:

- **Creating from scratch** — no root `.gitignore`: write Step 4's content without asking.
- **Updating existing** — a root `.gitignore` exists: warn up front that Step 5 will ask whether to Update, Keep as is,
  or Replace it (or apply `on-existing`) rather than overwrite anything silently.

## Step 2 — The base template

Unconditional except for the marked lines — every line flush-left in the written file (git doesn't trim leading
whitespace). `<bin>` lines repeat per binary name; with no binary name, drop that section.

```gitignore
# Binaries built at the repository root (`go build ./cmd/<bin>`)
/<bin>
/<bin>.exe

# Test binaries (`go test -c`) and CPU/memory profiles
*.test
*.pprof

# Coverage profiles (`go test -coverprofile`, `go build -cover` + GOCOVERDIR)
coverage.out
*.coverprofile
coverage.html
/covdata/

# Build and report output: coverage (build/coverage/), generated docs (build/gendocs/), local binaries
/build/

# GoReleaser output (`goreleaser release --snapshot --clean`)
/dist/

# Go workspace files: per-developer, this repository is a single module
go.work
go.work.sum

# Dependencies are not vendored (`go mod vendor` output)
/vendor/

# Environment files (never commit real secrets)
.env
.env.*
!.env.example

# Repository-wide lock serializing container-backed test runs
.integration-test.lock/

# OS files
.DS_Store
Thumbs.db

# Editors
.idea/
*.swp
*~
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
!.vscode/launch.json
!.vscode/tasks.json
```

Notes on specific lines:

- **`/<bin>` is root-anchored** on purpose: an unanchored `<bin>` would also ignore `cmd/<bin>/` — the entry point's
  directory. If a root *directory* has the binary's name, drop the line and say so (`go build -o build/<bin>` is the
  scaffold's own habit anyway).
- **`/build/`** holds only regenerated output in this catalog's layout: `build/coverage/cover.out` (`iru-go-coverage`,
  the workflows), `build/gendocs/{man,markdown,completions}` (`go run ./tools/gendocs`, GoReleaser's before-hook) and
  `build/<bin>` smoke-test binaries. If `git ls-files build` is non-empty, ask whether to keep ignoring the directory
  (and untrack it) or narrow the entry to `/build/coverage/` and `/build/gendocs/`.
- **`/dist/`** is GoReleaser's output (`--clean` deletes it); keep the line even without a `.goreleaser.yaml` only if a
  `dist/` directory is untracked, otherwise drop it when Step 1 found no GoReleaser config.
- **`go.work` / `go.work.sum`**: a workspace file points at local checkouts on one developer's machine, so for a
  single-module repository it is personal state (GitHub's `Go.gitignore` ignores both for the same reason, and the Go
  docs advise against committing `go.work` for a single module). `go.work.sum` only exists alongside a `go.work` and is
  ignored with it. A repository that **tracks** `go.work` (a deliberate multi-module workspace) gets neither line.
- **`/vendor/`** only with `vendor: no` (Step 1). With `vendor: yes`, omit the section — and say that CI then builds
  with `-mod=vendor` automatically (Go uses `vendor/` when it is consistent with `go.mod`).
- **Never ignored — and if an existing `.gitignore` ignores one, propose removing that line** (named in Step 5's
  question): `go.mod`, `go.sum` (the dependency checksums — always committed, for applications and libraries alike),
  `testdata/` (Go's test fixture convention; the testscript scripts live in `testdata/script/`), `.golangci.yml`,
  `.goreleaser.yaml`, `.secrets.baseline` (`iru-check-security`'s triaged baseline), `.env.example`.

## Step 3 — Detect project-specific additions

Only add a section when Step 1 found what it targets:

- **Antora** (`docs/antora.yml` or `docs/antora-playbook.yml`):
  ```gitignore
  # Antora documentation build output (see iru-setup-antora)
  docs/build/
  docs/node_modules/
  ```
  The generated `docs/modules/ROOT/pages/cli-reference.adoc` stays **tracked** — it is a site page, regenerated and
  diffed like any other source.
- **Node tooling at the root** (`package.json`): `node_modules/` and `npm-debug.log*`.
- **Terminal UI** (`charm.land/bubbletea/v2` or `github.com/charmbracelet/bubbletea` in `go.mod`, or a root
  `.ui-quality.yml`/`.ui-screenshots/`):
  ```gitignore
  # UI test captures (UI contract: .ui-screenshots/<kind>/<Id>/<state>--<direction>--<theme>.txt), regenerated every run
  .ui-screenshots/
  ```
  `.ui-quality.yml` (the accessibility level and capture matrix) stays **tracked**; the documentation skills copy the
  captures they use into the Antora `images/ui/` tree, which is committed.
- Don't invent entries beyond what was detected.

## Step 4 — Compose the proposed content

Step 2's template (with the per-repository choices applied) plus the Step 3 sections that matched, each under its
comment header. If a root `.gitignore` exists, merge: keep every existing line not already covered (hand-added
ignores survive), don't repeat a line already present verbatim or in a path-equivalent form (`dist` / `dist/` /
`/dist/`), keep `!` negations after the patterns they re-include, and **remove** an ignore line for `go.sum`/`go.mod`
— the one deliberate kind of deletion, listed in Step 5's question. A whole-directory `.vscode/` line in the existing
file wins over the template's `.vscode/*` block (git can't re-include files under an excluded directory).

Before proposing, check the draft doesn't hide source the scaffold commits — write it to a temp path, then run
`git -c core.excludesFile=<draft> check-ignore --no-index` (or temporarily in a scratch copy) on whichever of these
exist and refuse any line that matches one: `go.mod`, `go.sum`, `cmd/*/main.go`, `internal/**/*.go`,
`tools/gendocs/main.go`, `testdata/script/*.txtar`, `.golangci.yml`, `.goreleaser.yaml`, `.env.example`,
`docs/modules/ROOT/pages/cli-reference.adoc`, `.ui-quality.yml`, `internal/tui/ui_screenshots_test.go`,
`docs/modules/ROOT/images/ui/**`.

## Step 5 — If a `.gitignore` already existed, warn and ask Update / Keep as is / Replace

Skip when Step 1 found no root `.gitignore` — write it straight away.

Otherwise, if the proposed content differs from disk:

- Show the proposed **Update** content as a diff (`git diff --no-index <current> <draft>`). Say which hand-added lines
  a **Replace** would drop, and name any conflicting existing line (e.g. `go.sum`, which must be committed; an
  unanchored `<bin>` that hides `cmd/<bin>/`; `vendor/` in a vendoring repository; `testdata/`).
- Unless `on-existing` is `keep`/`update`/`replace` (apply it, still printing the warning and diff), ask via
  `AskUserQuestion`, with the consequence in each option:
  - **Update (Recommended)** — "Merge: add the template lines this file is missing; keep every hand-added line. Your
    customizations survive." — plus, when it applies, "…except the `go.sum` ignore line, which is removed so the
    checksums are committed".
  - **Keep as is** — "Leave the file untouched. Nothing you customized changes, but the missing lines in the diff (e.g.
    `/dist/`, `coverage.out`, `/build/`) stay unignored — the report lists them."
  - **Replace** — "Overwrite with this skill's template only. Matches the house pattern exactly, but every hand-added
    line is lost (recoverable only from git history)."
  If the user wants only some lines, let them say so in free text and revise the draft.

## Step 6 — Write and report

Write the chosen draft to `.gitignore` (or nothing, if kept as is). Then verify with git itself (read-only), for the
paths that exist or with throwaway empty files in a scratch copy:

```bash
# must print nothing (exit 1): the module files, sources, scripts and configs stay tracked
git check-ignore go.mod go.sum cmd/<bin>/main.go internal/cli/root.go testdata/script/greet.txtar .golangci.yml .goreleaser.yaml .env.example
# should list each generated path with the line that ignores it
git check-ignore -v <bin> build/coverage/cover.out build/gendocs dist coverage.out cli.test .env .integration-test.lock 2>/dev/null
# terminal UI only: the captures are ignored, the config and the helper are not
git check-ignore -v .ui-screenshots/screen/Model/default--ltr--no-color.txt; git check-ignore .ui-quality.yml internal/tui/ui_screenshots_test.go
```

Summarize: whether this run created from scratch or updated an existing file, the action taken — **created /
updated / replaced / kept as is** — and whether it came from the user or `on-existing` (when kept, the template lines it
still lacks); the binary names used; the vendoring and workspace decisions and why; which Step 3 sections were included
vs. skipped and why; whether a `go.sum` ignore line was removed; the `git check-ignore` result; and any already-tracked
file under a newly ignored path, with the `git rm -r --cached <path>` it needs.

**Warn explicitly**:

- Review the generated/updated `.gitignore` before committing — detection is heuristic.
- Writing `.gitignore` alone never untracks a committed file (a root binary, `dist/`, `coverage.out`): run
  `git rm -r --cached <path>` for each after reviewing.
- Commit `go.mod` and `go.sum` always; commit `vendor/` only if you chose to vendor; commit `go.work`/`go.work.sum`
  only for a deliberate multi-module workspace.
- A committed `.env` may contain credentials: rotate them, since they remain in git history.

## Sources

- GitHub's `github/gitignore` `Go.gitignore` (binaries, `*.test`, `*.out`, `go.work`, `go.work.sum`, `vendor/` as an
  opt-in) and `Global/` editor/OS templates.
- Go: go.dev/ref/mod (`go.sum` "should be committed", vendoring and `-mod=vendor`, workspaces), go.dev/doc/tutorial/workspaces,
  go.dev/blog/integration-test-coverage (`GOCOVERDIR`).
- GoReleaser: goreleaser.com/customization/dist/ (`dist/`, `--clean`).
- This catalog: `iru-setup-go-cli`'s scaffold contract (`build/coverage/`, `build/gendocs/`, `testdata/script/`), and
  `iru-setup-windows-gitignore` / `iru-setup-python-gitignore` (structure).

## Verification notes

Verified on 2026-10-16 in `$TMPDIR/iru-verify/cli/iru-setup-go-gitignore-2/` (outside this repository): the base
template for `bin-name: hello-cli` with `vendor: no` and the Antora section, written into a `git init`-ed directory
seeded with one file per pattern and per source file the scaffold commits. `git check-ignore -q` reported **24/24**
generated paths ignored — `hello-cli`, `hello-cli.exe`, `cli.test`, `cpu.pprof`, `coverage.out`, `x.coverprofile`,
`coverage.html`, `covdata/covmeta.1`, `build/coverage/cover.out`, `build/gendocs/man/hello-cli.1`, `dist/SHA256SUMS`,
`dist/hello-cli_linux_amd64_v1/hello-cli`, `go.work`, `go.work.sum`, `vendor/modules.txt`, `.env`, `.env.local`,
`.integration-test.lock/owner`, `docs/build/site/index.html`, `docs/node_modules/x`, `.DS_Store`, `.idea/x`,
`.vscode/x.json`, `a.swp` — and `git check-ignore` on the 16 files that must stay tracked (`go.mod`, `go.sum`,
`cmd/hello-cli/main.go`, `cmd/hello-cli/main_test.go`, `internal/cli/root.go`, `internal/version/version.go`,
`tools/gendocs/main.go`, `testdata/script/greet.txtar`, `internal/cli/testdata/x.golden`, `.golangci.yml`,
`.goreleaser.yaml`, `.env.example`, `.vscode/settings.json`, `docs/modules/ROOT/pages/cli-reference.adoc`,
`docs/antora.yml`, `.secrets.baseline`) printed nothing and exited 1; `git status --porcelain -uall` listed exactly
those 16 files plus `.gitignore`. In particular `cmd/hello-cli/main.go` is not hidden by `/hello-cli`. The paths
match what `iru-setup-go-cli`'s verification actually produced (`build/coverage/cover.out`, `build/gendocs/`,
`dist/` from `goreleaser release --snapshot --clean`). The terminal-UI section (added for the UI contract) was checked
the same way in a scratch repository: `.ui-screenshots/screen/Model/default--ltr--no-color.txt` ignored;
`.ui-quality.yml`, `internal/tui/ui_screenshots_test.go` and `docs/modules/ROOT/images/ui/screen/Model/…` not.
