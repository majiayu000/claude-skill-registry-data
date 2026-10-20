---
name: iru-setup-go-cli
description: >-
  Scaffold an agent-friendly Go command-line tool at the repository root — `go.mod` (`go <minor>.0` + `toolchain
  go<latest patch>`), a thin `cmd/<bin>/main.go` that only calls `cli.Main`, `internal/cli` (Cobra root with
  `SilenceUsage`/`SilenceErrors`, global `--format text|json|jsonl`/`--json`/`--no-color`/`--no-input`/`-q`/`-v`/
  `--log-format`; one exit-code table 0–7/130/143 mapped in exactly one place from a typed `*cli.Error`, Cobra
  flag/argument errors → 2, a recovered panic → 1; the JSON error envelope on stderr; canonical sorted-key JSON;
  colour per stream via `golang.org/x/term` + `NO_COLOR`/`FORCE_COLOR`/`TERM=dumb`/`--no-color`; prompts only on a
  terminal and never with `--no-input`/`<BIN>_NO_INPUT`/`CI`; flags → env → `config.toml` → defaults precedence;
  SIGINT/SIGTERM → 130/143 with a second-signal immediate exit; EPIPE as a clean stop), the sample commands `greet`,
  `schema` (the command tree as JSON with exit codes and per-command safety annotations), `version` and Cobra's
  `completion`, `internal/version` (version/commit/date via ldflags, `0.1.0-dev` in-tree), with `ui: tui` a Bubble Tea
  v2 + Lip Gloss v2 `browse` command (TTY-gated, exit 2 otherwise) in `internal/tui` tested with unit tests and teatest
  v2, rendering only the names that fit the window, and — per the catalog's UI contract — a `.ui-quality.yml` at the
  repository root, an `internal/tui/ui_screenshots_test.go` helper and UI tests capturing every list state in each
  direction as `.ui-screenshots/screen/Model/<state>--<direction>--no-color.txt` with the asserted accessibility checks; unit tests plus testscript end-to-end scripts (`testdata/script/*.txtar`, run in-process from `TestMain` so they
  count toward coverage, asserting exact exit codes and JSON golden output); a golangci-lint v2 `.golangci.yml`
  (revive `exported`/`package-comments`, gosec, godot, misspell, gofmt + goimports); a GoReleaser v2
  `.goreleaser.yaml` (CGO-free linux/darwin/windows × amd64/arm64, `tar.gz`/`zip` archives named
  `<bin>-<version>-<os>-<arch>`, `SHA256SUMS`, no generated changelog, Homebrew cask / Scoop / WinGet only for
  `distribution: store` with the requested `channels`); and `tools/gendocs` (man pages, Markdown, completion scripts and
  the Antora `cli-reference.adoc` from the command tree). Invoke as `/iru-setup-go-cli`. Accepts pre-resolved inputs via
  `args` (`key: value` lines) — `bin-name`, `module-path`, `description`, `ui` (`none`/`tui`), `go-version`, `owner`,
  `version`, `license`, `developer-name`, `developer-email`, `organization-url`, `open-source`, `visibility`, `ci`,
  `sonar` (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`), `distribution` (`none`/`internal`/`store`),
  `channels` (`homebrew,scoop,winget`), `homebrew-tap`, `scoop-bucket`, `accessibility` (`enforce`/`report`/`off`/`none`, `ui: tui`
  only), `mode` (`new`/`existing`) and `on-existing`
  (`ask`/`keep`/`update`/`replace`) — so `iru-setup-cli-repository` can drive it without re-prompting. Announces
  whether it is scaffolding from scratch or updating; for every file group it owns that already exists it warns and
  asks Update / Keep as is / Replace / Stop (unless `on-existing` decides) and never overwrites hand-written code.
  Every module version is looked up live (proxy.golang.org, go.dev) with a verified 2026-10-16 fallback table, and the
  run ends by building, testing (race + coverage ≥ 80%), linting, vulnerability-scanning, generating docs, smoke-testing
  the binary against the CLI contract and (when configured) `goreleaser check` + a snapshot release. Use whenever a
  repository needs a Go CLI bootstrapped from this house template instead of wiring Cobra, testscript, golangci-lint and
  GoReleaser by hand.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(go *) Bash(gofmt *) Bash(golangci-lint *) Bash(govulncheck *) Bash(gotestsum *) Bash(goreleaser *) Bash(curl *) Bash(git *) Bash(gh repo view *) Bash(python3 *) Bash(jq *) Bash(bash *) Bash(mkdir *) Bash(ls *) Bash(find *) Bash(grep *) Bash(cat *) Bash(test *) Bash(command -v *) Agent
---

# Setup Go CLI

Generate a complete, buildable, agent-friendly command-line tool in Go — a thin entry point, all behaviour in
`internal/` packages with unit and end-to-end tests, quality and release configuration, and a docs generator — from
the templates in this skill's `reference/` files. Every template was rendered into throwaway projects (`ui: tui` +
`distribution: store` with all three channels, `ui: none` + `distribution: internal` without a license, and `ui: none`
+ `distribution: none`) and proven with the real toolchain on 2026-10-16 (Go 1.27.2, golangci-lint 2.15.0, GoReleaser
2.18.3, govulncheck) — see **Verification notes**.

The behaviour is the catalog's language-agnostic CLI contract (streams, exit codes, TTY/colour/prompts, machine
output, safety, configuration, self-description, startup), implemented idiomatically for Cobra. The layout is the
**scaffold contract** that `iru-go-code-one-task(-group)`, `iru-go-test`, `iru-go-coverage`, `iru-go-code-quality`,
`iru-go-godoc`, `iru-go-bump-version` and `iru-setup-cli-github-workflows` detect and call — Step 8's table lists the
confirmed names, commands and paths. This skill writes no workflow, `.gitignore`, README, CHANGELOG, `LICENSE`, Antora
site (`docs/antora.yml`) or agent-instruction file — `iru-setup-cli-repository` chains the skills that do — and no
Sonar file (the workflows skill passes the Sonar coordinates on the scanner's command line).

Sources: Go — go.dev/doc/modules/gomod-ref (`go`/`toolchain` lines), go.dev/doc/toolchain, go.dev/doc/comment,
go.dev/blog/integration-test-coverage, pkg.go.dev/os/signal (SIGPIPE/EPIPE rules, `NotifyContext`),
pkg.go.dev/golang.org/x/term, pkg.go.dev/log/slog; Cobra — cobra.dev and pkg.go.dev/github.com/spf13/cobra (+
`/doc`: `GenManTree`, `GenMarkdownTree`, "Documenting CLIs for LLMs"); testscript —
pkg.go.dev/github.com/rogpeppe/go-internal/testscript; Bubble Tea v2 — pkg.go.dev/charm.land/bubbletea/v2, Lip Gloss
v2, teatest v2 (github.com/charmbracelet/x/exp/teatest/v2); golangci-lint — golangci-lint.run/docs/configuration/file/
(v2 format); GoReleaser — goreleaser.com/customization/ (builds, archives, checksum, homebrew_casks, scoops, winget);
actions/setup-go README (`toolchain` directive support). CLI guidance: irurueta docs:
ai/cli-for-agents/streams-and-exit-codes.adoc, tty-colour-and-interactivity.adoc, machine-readable-output.adoc,
agent-ergonomics.adoc, safety-and-idempotency.adoc, configuration-and-auth.adoc, self-describing-help.adoc,
testing-clis.adoc (testscript), documenting-clis.adoc, frameworks-go-and-rust.adoc (Cobra `SilenceUsage`/
`SilenceErrors`, typed exit error, `cobra/doc`, the TTY-gated Bubble Tea `browse`), packaging-and-distribution.adoc
(GoReleaser), tuis-vs-clis.adoc, security.adoc and agent-readiness-checklist.adoc
(https://www.irurueta.com/ai/cli-for-agents/index.html). The docs site has no Go language pages; Go facts come from the
official docs above.

## Reference files — read only what this run needs

| Read | When |
|---|---|
| `reference/module-templates.md` | **Always.** The `go mod`/`go get` command sequence, `cmd/<bin>/main.go`, the testscript driver `cmd/<bin>/main_test.go` (custom `status CODE exec …` command), `internal/version`. |
| `reference/cli-templates.md` | **Always.** `internal/cli`: `doc.go`, `exitcode.go`, `errors.go`, `output.go`, `term.go`, `config.go`, `signals.go`, `root.go`, `greet.go`, `schema.go`, `version.go`. |
| `reference/test-templates.md` | **Always.** The `internal/cli` unit tests and `testdata/script/*.txtar`. |
| `reference/tui-templates.md` | `ui: tui` only. `internal/tui` (incl. `ui_screenshots_test.go`), `internal/cli/browse.go` (+ tests), `testdata/script/browse.txtar`, `.ui-quality.yml`. |
| `reference/tooling-templates.md` | **Always.** `.golangci.yml`, `tools/gendocs` (+ test); `.goreleaser.yaml` only when `distribution` ≠ `none`. |

**Conditional-marker convention used in every reference file**: a line `// >>> <condition>` (or `# >>> <condition>`)
opens a block written only when the condition holds; the matching `<<< <condition>` line closes it; marker lines are
never written. A file heading suffixed `(<condition>)` exists only when it holds. Conditions: `ui: tui|none`,
`distribution: internal|store`, `channel: homebrew|scoop|winget` (= `distribution: store` and that channel in
`channels`), `license` (a license was chosen). **Placeholders** are written `__TOKEN__` and come from Step 5's table;
headings use them too (`cmd/__BIN__/main.go`). Substituting placeholders changes line lengths, so Step 6 always runs
`gofmt -w` over the written Go files afterwards (verified: struct-field and map-key alignment otherwise fails the
`gofmt` formatter check).

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-go-cli`) or by `iru-setup-cli-repository` / the `iru-setup-repository` front door,
which pass resolved answers as `key: value` lines, e.g.:

```
bin-name: logsift
description: Search and summarize structured log files.
ui: tui
owner: example-org
license: MIT
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
open-source: yes
visibility: public
ci: yes
sonar: none
distribution: store
channels: homebrew,scoop,winget
mode: new
on-existing: ask
```

Recognized keys (every key found is resolved — skip its question in Step 2):

| Key | Values / default |
|---|---|
| `bin-name` | the command users type: `^[a-z][a-z0-9-]*$` (e.g. `logsift`, `hello-cli`). Names the binary, `cmd/<bin>/`, the GoReleaser project, man pages and completion files. Env prefix `<BIN>_` = upper-cased, `-` → `_` |
| `module-path` | default `github.com/<owner>/<repo>` (Step 3; `<repo>` = the `origin` repository name, else `bin-name`). A major version ≥ 2 needs a `/vN` suffix — warn, never add one silently |
| `description` | one sentence (root `Short`/`Long`, package comment, GoReleaser descriptions); a trailing period is added if missing |
| `ui` | `none` (default) / `tui` (adds the Bubble Tea `browse` command) |
| `accessibility` | `enforce` (default) / `report` / `off` / `none` — only with `ui: tui`: the level written to `.ui-quality.yml`, which the TUI's UI tests read |
| `go-version` | `go` directive minor, e.g. `1.27` → `go 1.27.0`; default the latest stable minor (Step 4). The `toolchain` line is always the latest patch of that minor |
| `owner` | GitHub owner (user or organization) for `module-path`, release URLs and the package-channel repositories; default from `origin` |
| `version` | in-tree version, default `0.1.0-dev` (`iru-go-bump-version` owns it afterwards) |
| `license` | display name or SPDX id (`MIT License` → `MIT`, `Apache License 2.0` → `Apache-2.0`) or `none`; drives the GoReleaser `license` fields and the `LICENSE*` archive entry only |
| `developer-name`, `developer-email`, `organization-url` | WinGet `publisher`, report |
| `open-source`, `visibility`, `ci`, `sonar` (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`) | recorded for the report (no file here carries them); asked stand-alone only for the `distribution` default |
| `distribution` | `none` (no `.goreleaser.yaml`) / `internal` (archives + `SHA256SUMS` on GitHub Releases) / `store` (`internal` + package channels); default `store` when open source, else `internal` |
| `channels` | comma list, only with `store`: `homebrew`, `scoop`, `winget`; default all three |
| `homebrew-tap` / `scoop-bucket` | `owner/repo`, defaults `<owner>/homebrew-tap` / `<owner>/scoop-bucket` (the WinGet fork is always `<owner>/winget-pkgs`) |
| `mode`, `on-existing` | as in every catalog setup skill (`on-existing` default `ask`) |

Unknown keys from a full shared-args set (`language`, `branching`, `ci-tests`, `pages`, `cross-os-ci`,
`integration-branch`, `stable-branch`, `publish`, …) are ignored and named in the report. `mode: existing` never means
"gap-fill silently": Step 1 still warns about, and asks about, every pre-existing file group; only `on-existing` skips
that question (`keep` = create only missing files; `update`/`replace` applied to every existing group, with the
source-file limit below; the warning is still printed). Orchestrators forward `on-existing` only when their own `args`
received it.

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (the terminal UI's asserted accessibility checks), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — selection visible without colour, key help on screen, every action reachable by key — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

## Step 1 — Survey the repository

Check for every file Step 6 would write: `go.mod`, `go.sum`, `go.work`, `cmd/*/main.go`, a root `main.go`,
`internal/cli/**`, `internal/tui/**`, `internal/version/**`, `tools/gendocs/**`, `testdata/script/**`, `.golangci.yml`
(also `.golangci.yaml`/`.golangci.toml`/`.golangci.json`), `.goreleaser.yaml` (also `.goreleaser.yml`), and
`docs/modules/ROOT/pages/cli-reference.adoc`, and (`ui: tui`) `.ui-quality.yml`. Then announce which of these this run is:

- **Scaffolding from scratch** — none exist: go to Step 2.
- **Updating an existing Go CLI** — a `go.mod` with this skill's layout (`cmd/<bin>/main.go` + `internal/cli`): warn,
  listing every file found by path, that each existing file group is decided individually (missing files are still
  created). Read `module-path`, the `go`/`toolchain` lines, `bin-name` (the `cmd/<bin>` directory), the in-tree
  version, `ui` (`internal/tui` present) and the GoReleaser channels first and offer them as Step 2's defaults. Groups
  (only those with a file present): **`go.mod`/`go.sum`**, **`.golangci.yml`**, **`.goreleaser.yaml`**, **docs
  generator** (`tools/gendocs/`), **end-to-end scripts** (`testdata/script/`, `cmd/<bin>/main_test.go`), **the
  source skeleton** (`cmd/<bin>/main.go`, `internal/**`), and — `ui: tui` only — **UI quality config**
  (`.ui-quality.yml`; Update keeps its `directions`/`themes` and any `accessibility` value unless `args` set one,
  adding missing keys; Keep as is reports a level that differs from this run's; Replace rewrites it from the
  template). Unless `on-existing` decides, ask with `AskUserQuestion`, one
  question per group (batch up to 4 per call), naming each concrete conflict with this run's choices (e.g.
  "`.golangci.yml` is a v1 config — golangci-lint 2.x rejects it", "`.goreleaser.yaml` has `version: 1`", "no
  `internal/tui` but you chose `ui: tui`", "`go.mod` says `go 1.22` — older than the dependencies need",
  "`.goreleaser.yaml` publishes a Homebrew formula (`brews`, deprecated) — this template uses `homebrew_casks`"):
  - **Update (Recommended for `go.mod`, `.golangci.yml`, `.goreleaser.yaml` and the docs generator)** — "Merge: add
    what's missing and correct outdated parts using this skill's template as reference (requirements via `go get`,
    linters/formatters, builds/archives/checksum/channels, ldflags paths); keep every dependency, linter setting,
    build and channel this skill doesn't own. You review a diff; customizations survive, but a part this skill owns
    may be rewritten." For the source skeleton and the scripts, Update only creates missing files.
  - **Keep as is (Recommended for the source skeleton and the scripts)** — "Leave the files untouched. Nothing you
    customized changes, but they may stay out of date or disagree with this run's choices — the report lists each
    mismatch."
  - **Replace** — "Regenerate from the template. Matches the house pattern exactly, but every customization is lost
    (recoverable only from git history)." Never the default. Even on Replace, never overwrite a `.go` or `.txtar`
    file unless its content exactly matches this skill's rendered template (i.e. it is still the untouched sample).
  - **Stop** (first question only) — "End this skill now without changing any file." Report and end.
- **A foreign layout** — a `go.mod` whose CLI lives elsewhere (root `main.go`, `cmd/<bin>/` with logic in `main`), a
  different framework (`urfave/cli`, `kong`), a library without `cmd/`, or a `go.work` workspace: not this skill's
  scaffold. Warn explicitly and ask (`AskUserQuestion`) whether to add only this skill's non-code pieces alongside
  (`.golangci.yml`, `.goreleaser.yaml`, `tools/gendocs` only if the tree is Cobra — each still per-group
  Update/Keep/Replace) or stop. Never move, rename or convert existing packages, and never switch CLI frameworks.

## Step 2 — Collect the required inputs

For anything Step 0 didn't resolve, ask directly (plain conversation, pre-filled from Step 1 when updating):
**bin-name** (default: the repository directory name, lower-cased, non-`[a-z0-9-]` characters dropped),
**description**, **owner** (Step 3), developer name/email/organization URL. Confirm the derived `module-path` and env
prefix in one line.

Then, with `AskUserQuestion` (skip any resolved):

- **ui** — **None (Recommended)** (`none`: a plain command tool; styled, TTY-aware text output is still there) /
  **Terminal UI** (`tui`: adds `browse`, a full-screen Bubble Tea v2 list for people — TTY-gated, every function stays
  available non-interactively with `--json`).
- **accessibility** — only with `ui: tui` and stand-alone (an orchestrator resolves it): "Support accessibility and assistive technologies?" — **Enforce (Recommended)** (violations fail the UI tests) / **Report only** (listed, never
  failing) / **Off** (not run). For a terminal UI these are the asserted checks (selection visible without color, key
  help on screen), not an automated audit.
- **license** — MIT (Recommended for a tool) / Apache 2.0 / No license (proprietary) / Other. Remind in Step 8 to add
  a root `LICENSE` (`iru-check-license` can backfill headers).
- **open-source**, then **distribution** — asked stand-alone only (an orchestrator resolves them): **Store
  (Recommended when open source)** — archives + checksums plus package channels; **Internal (Recommended
  otherwise)** — archives + `SHA256SUMS` on GitHub Releases; **None** — no release configuration. With `store`, ask
  **channels** as a multi-select: Homebrew cask (needs a `<owner>/homebrew-tap` repository and a token secret), Scoop
  (a `<owner>/scoop-bucket` repository + token), WinGet (a fork `<owner>/winget-pkgs` + a token; the first submission
  is reviewed by Microsoft).
- `sonar` is never asked here (no file in this skill carries it).

## Step 3 — Infer repository information

Parse `git remote get-url origin` (`git@host:owner/repo.git` or `https://host/owner/repo.git`) for `<owner>` and
`<repo>`. No `origin` → ask for the owner; `<repo>` defaults to `bin-name`. Homepage = `https://github.com/<owner>/<repo>`
(or `organization-url` when the remote isn't GitHub). WinGet package identifier = `<Owner>.<Bin>` with each part
PascalCased and non-alphanumerics dropped (`example-org` + `hello-cli` → `ExampleOrg.HelloCli`).

## Step 4 — Look up toolchain and module versions

Check the tools first: `go version` (required — missing → tell the user to install Go from go.dev/dl and stop; never
install it system-wide yourself), then `golangci-lint version`, `govulncheck -version`, `goreleaser --version` (each
optional — a missing one makes its Step 7 check **unverified**, never passed). A local Go older than the resolved
`go` directive can't build the scaffold: say so and stop (or offer the older minor as `go-version`).

Look every version up at run time; fall back to this table (verified working **together** on 2026-10-16) only when a
lookup fails, and say so in Step 8. Module lookups: `curl -fsSL https://proxy.golang.org/<module>/@latest` → `Version`
(a stable tag; for a pseudo-version-only module use the `@latest` pseudo-version). After adopting a newer combination,
Step 7 must pass before trusting it.

| Component | Lookup | 2026-10-16 fallback |
|---|---|---|
| Go (`go` / `toolchain` lines) | `curl -fsSL 'https://go.dev/dl/?mode=json'` → first `version` (the latest stable); `go` = its minor `.0`, `toolchain` = that version | `go 1.27.0`, `toolchain go1.27.2` |
| `github.com/spf13/cobra` | proxy `@latest` | `v1.10.2` |
| `github.com/spf13/pflag` | proxy `@latest` (requested explicitly: Cobra 1.10.2 still requires 1.0.9) | `v1.0.10` |
| `golang.org/x/term` | proxy `@latest` | `v0.47.0` |
| `github.com/pelletier/go-toml/v2` | proxy `@latest` | `v2.4.3` |
| `github.com/rogpeppe/go-internal` (testscript) | proxy `@latest`; ≥ 1.14 for `testscript.Main(m, map[string]func())` | `v1.16.0` |
| `charm.land/bubbletea/v2` (`ui: tui`) | proxy `@latest` | `v2.1.0` |
| `charm.land/lipgloss/v2` (`ui: tui`) | proxy `@latest` | `v2.0.6` |
| `github.com/charmbracelet/x/exp/teatest/v2` (`ui: tui`, tests only) | proxy `@latest` — pseudo-versions only (an `exp` module); it requires `bubbletea/v2 v2.0.0-rc.1`, and minimal version selection lifts that to the Bubble Tea version above (verified compatible) | `v2.0.0-20261012121918-43427fdbad12` |
| golangci-lint / GoReleaser / govulncheck (tools, never added to `go.mod`) | whatever is installed; the configs need golangci-lint ≥ 2.0 and GoReleaser ≥ 2.10 (`homebrew_casks`) | 2.15.0 / 2.18.3 / latest |

## Step 5 — Reference templates

Read the reference files this run needs (table above). Placeholders:

| Placeholder | Source |
|---|---|
| `__BIN__` | `bin-name` |
| `__ENV__` | `bin-name` upper-cased, `-` → `_` (`hello-cli` → `HELLO_CLI`) |
| `__MODULE__` | `module-path` |
| `__DESCRIPTION_SENTENCE__` | `description`, ending in a period, `"` and `\` escaped (it sits in Go string literals) |
| `__DESCRIPTION_YAML__` | `description` with `"` escaped (YAML double-quoted scalars) |
| `__VERSION__` | `version` (default `0.1.0-dev`) |
| `__GO_DIRECTIVE__` / `__GO_TOOLCHAIN__` | Step 4 (`1.27.0` / `1.27.2`) |
| `__COBRA_VERSION__`, `__PFLAG_VERSION__`, `__XTERM_VERSION__`, `__GOTOML_VERSION__`, `__GOINTERNAL_VERSION__`, `__BUBBLETEA_VERSION__`, `__LIPGLOSS_VERSION__`, `__TEATEST_VERSION__` | Step 4 (without the leading `v` except `__TEATEST_VERSION__`, which is the full pseudo-version) |
| `__HOMEPAGE__`, `__OWNER__`, `__WINGET_ID__` | Step 3 |
| `__LICENSE_SPDX__` | `license` as an SPDX id |
| `__ACCESSIBILITY__` | `accessibility` (`enforce` by default; `ui: tui` only) |
| `__PUBLISHER__` | `developer-name` (else `<owner>`) |
| `__TAP_OWNER__` / `__TAP_REPO__` / `__TAP_SHORT__` | `homebrew-tap` split; `__TAP_SHORT__` = repo without its `homebrew-` prefix (what `brew tap owner/short` takes) |
| `__SCOOP_OWNER__` / `__SCOOP_REPO__` | `scoop-bucket` split |

Directory layout produced (`[tui]`/`[release]` mark variant-only files):

```
go.mod  go.sum  .golangci.yml  .goreleaser.yaml [release]
cmd/<bin>/main.go  cmd/<bin>/main_test.go
internal/cli/{doc,exitcode,errors,output,term,config,signals,root,greet,schema,version}.go
internal/cli/{helpers,root,signals,config,exitcode,errors,output,term,greet,schema,version}_test.go
internal/cli/browse.go  internal/cli/browse_test.go                                 [tui]
internal/tui/model.go  internal/tui/model_test.go  internal/tui/ui_screenshots_test.go [tui]
.ui-quality.yml                                                                     [tui]
internal/version/version.go  internal/version/version_test.go
tools/gendocs/main.go  tools/gendocs/main_test.go
testdata/script/{greet,exit_codes,config,help,completion,schema}.txtar  (+ browse.txtar [tui])
```

## Step 6 — Scaffold the project

Apply Step 1's per-group decision to every file that already exists (Keep as is → skip; Update → merge after showing
`git diff --no-index <current> <draft>`; Replace → overwrite within Step 1's source-file limit). Files that didn't exist
are always written.

1. **New module**: run the command sequence from `reference/module-templates.md` up to (not including) `go mod
   tidy` — `go mod init`, `go mod edit -go=… -toolchain=…`, `go get` with Step 4's versions (TUI modules only for
   `ui: tui`). **Existing module** (Update): `go get` only what's missing; never downgrade a requirement the project
   already has at a newer version, and leave its `go` line alone unless it's older than the dependencies require
   (then report it rather than editing).
2. Write every template from the reference files this run reads, applying markers and placeholders. UTF-8, LF, Go
   files tab-indented as in the templates.
3. `gofmt -w cmd internal tools` (only on the files this skill wrote when updating) — placeholder substitution
   changes alignment.
4. `go mod tidy` — turns the `// indirect` requirements into direct ones and drops unused ones (with `ui: tui` it
   also makes `github.com/charmbracelet/x/ansi`, already required through Lip Gloss, a direct requirement of the
   capture helper); `go.sum` is committed.
5. Never create `docs/antora.yml`, `docs/antora-playbook.yml` or `nav.adoc`. The CLI reference page is generated in
   Step 7 only if `docs/modules/ROOT/` already exists (`iru-setup-antora` runs after this skill in the orchestrator;
   the workflows' docs job regenerates it).

## Step 7 — Verify

Run through the `iru-gate-runner` agent where output is long (tests, lint, GoReleaser), in this order, and fix
anything this skill wrote until green — never "fix" pre-existing code to make a gate pass; report it instead:

```bash
go build ./... && go vet ./...
GOOS=windows go vet ./... && GOOS=linux GOARCH=arm64 go vet ./...    # cross-platform compile check (signals, x/term)
gofmt -l cmd internal tools                                          # must print nothing
go test -race -count=1 ./...                                         # race needs cgo; without it run without -race and say so
mkdir -p build/coverage
go test -count=1 -covermode=atomic -coverpkg=./... -coverprofile=build/coverage/cover.out ./...
go tool cover -func=build/coverage/cover.out | tail -1               # ≥ 80% (verified 94–95% total, 97% across internal/)
golangci-lint config verify && golangci-lint run ./...               # 0 issues
govulncheck ./...                                                    # "No vulnerabilities found."
go run ./tools/gendocs                                               # man/, markdown/, completions/ under build/gendocs/ (+ the Antora page if docs/modules/ROOT exists)
go build -o build/__BIN__ ./cmd/__BIN__
```

Then the **contract smoke checks** against `build/<bin>` (the same ones the workflows' build job runs), each with its
expected result:

| Check | Expected |
|---|---|
| `<bin> --version` / `<bin> --help` | exit 0, stdout non-empty, stderr empty |
| `<bin> frobnicate` | exit 2, stdout empty, `hint: See \`<bin> --help\`.` on stderr |
| `<bin> greet Ada --json \| jq -e .schemaVersion` | exit 0 |
| `<bin> greet Ada \| grep -c $'\x1b'`; with `NO_COLOR=1 FORCE_COLOR=1` | `0` both (no ESC bytes piped); `FORCE_COLOR=1` alone → `1` |
| `<bin> greet '' --json` | exit 3, the envelope `{"error":{"code":"INVALID_NAME",…,"exitCode":3,…},"schemaVersion":1}` on stderr |
| `<bin> greet </dev/null` | exit 2 (no prompt without a terminal) |
| `{ sleep 0.5; <bin> schema --json; } \| true` | exit 0, stderr empty (EPIPE is a clean stop) |
| `<bin> browse </dev/null` (`ui: tui`) | exit 2, pointer to `greet NAME --json` |

With `distribution` ≠ `none` and GoReleaser installed: `goreleaser check` (it needs a git remote — in a repository
without `origin` it reports "scm releases: no remote configured"; report that as the reason rather than a config error)
and `goreleaser release --snapshot --clean` (needs at least one commit; never in a dirty tree you don't own — run it
in a throwaway clone when the user has uncommitted work), then confirm `dist/` holds six archives named
`<bin>-<version>-<os>-<arch>.tar.gz|zip` containing the binary, `README.md`, `CHANGELOG.md`, `LICENSE*` (when
licensed), `man/` and `completions/`, plus `SHA256SUMS`, and — for `store` — the generated cask
(`dist/homebrew/Casks/<bin>.rb`), Scoop manifest (`dist/scoop/<bin>.json`) and WinGet manifests
(`dist/winget/manifests/…`). Nothing is published by a snapshot. Delete `dist/` and `build/` afterwards only if the
user prefers (both are gitignored by `iru-setup-go-gitignore`).

Report pass/fail per command; quote error output verbatim for a failure only.

## Step 8 — Report

Summarize: resolved `bin-name`, `module-path`, env prefix, `description`, `ui`, `go`/`toolchain` lines, in-tree
version, license (or none), `distribution` and `channels`, and whether the run scaffolded from scratch, updated an
existing project, or stopped. Then, per Step 1 group, the action taken (including `.ui-quality.yml` for `ui: tui`, with
the `accessibility` level written) — **created / updated / replaced / kept as is**
— and whether it came from the user or `on-existing`, listing each mismatch of a kept group. State which Step 4
versions were live versus fallback, the ignored `args` keys, and every Step 7 result (unverified items with the
reason). List the Antora pages worth adding next (usage, exit codes, JSON output schema, using the tool from an agent)
and the `nav.adoc` entry for `cli-reference.adoc` — this skill writes neither.

### Scaffold contract (confirmed by running it — downstream skills depend on these)

| What | Exact name / path |
|---|---|
| Detection | `go.mod` + `cmd/<bin>/main.go` + `github.com/spf13/cobra` in `go.mod`; `charm.land/bubbletea/v2` + `internal/tui/` → `ui: tui` |
| Entry point | `cmd/<bin>/main.go`: `os.Exit(cli.Main(context.Background(), os.Args[1:], os.Stdin, os.Stdout, os.Stderr))` — no logic |
| Library unit | `internal/cli` (`App`, `NewApp`, `Main`, `App.Run`, `App.Command()` builds the whole Cobra tree), `internal/tui` (`Model`, `New`, `Run`, `DemoNames`), `internal/version` (`Version`, `Commit`, `Date`, `Get()`) |
| Exit codes | `internal/cli/exitcode.go` — `type ExitCode int`, `ExitOK`…`ExitAuth` = 0–7, `ExitInterrupted` 130, `ExitTerminated` 143, `ExitCodes()`, `Name()`, `Meaning()`; chosen only in `App.exitCode` (`root.go`) |
| Errors | `internal/cli/errors.go` — `*cli.Error{Code, ID, Message, Hint, Details, RetryAfterSeconds, Err}`, `cli.NewError(code, id, msg, hint)`, `.WithDetails(map)`; a non-`*Error` from a command → 1 (`wrapRunE`); any other Cobra error → 2 with `details.usage`; a panic → 1 |
| Safety annotations | `cmd.Annotations` keys `readOnly`/`destructive`/`idempotent` (`"true"`/`"false"`) via `safety(r, d, i)`; a unit test fails when a command lacks them |
| Global flags | `--format text\|json\|jsonl`, `--json`, `--no-color`, `--no-input`, `-q/--quiet`, `-v/--verbose` (count), `--log-format text\|json`; env `<BIN>_FORMAT`, `<BIN>_NO_COLOR`, `<BIN>_NO_INPUT`, `<BIN>_CONFIG`; config `$XDG_CONFIG_HOME/<bin>/config.toml` (else `~/.config/<bin>/`, `%APPDATA%\<bin>\` on Windows), keys `format`, `no-color`, `no-input` |
| Commands | `greet [NAME]`, `schema`, `version`, `completion bash\|zsh\|fish\|powershell`, `help`; `browse` (`ui: tui`) |
| Version | `internal/version/version.go` `var Version = "0.1.0-dev"`; release ldflags `-X <module>/internal/version.{Version,Commit,Date}` (in `.goreleaser.yaml`) |
| Unit tests | `go test ./...`; race: `go test -race ./...` (Unix-only signal tests are `//go:build unix`) |
| E2E tests | `cmd/<bin>/main_test.go` (`TestMain` → `testscript.Main`, `TestScripts`), scripts in `testdata/script/*.txtar`; exact exit codes via `status CODE exec <bin> …`; refresh goldens with `go test ./cmd/<bin> -run TestScripts -update` |
| Coverage | `go test -covermode=atomic -coverpkg=./... -coverprofile=build/coverage/cover.out ./...` — testscript children write to `GOCOVERDIR`, so e2e runs count; statement coverage only |
| Lint | `.golangci.yml` (v2): `golangci-lint run ./...`; formatters `golangci-lint fmt ./...` (gofmt + goimports, local prefix = module path) |
| UI contract (`ui: tui`) | `.ui-quality.yml` at the root; `internal/tui/ui_screenshots_test.go` (`captureView`, `checkAccessibility`, `tuiViolations`, `loadUIQuality`) writes `$UI_SCREENSHOTS_DIR` or `.ui-screenshots/screen/Model/<state>--<ltr\|rtl>--no-color.txt` |
| Docs | `go run ./tools/gendocs [-out build/gendocs] [-adoc docs/modules/ROOT/pages/cli-reference.adoc\|""]` → `build/gendocs/{man,markdown,completions}/`; API docs via `go doc ./internal/...` |
| Release | `.goreleaser.yaml` (v2): before-hook runs gendocs; `dist/<bin>-<version>-<os>-<arch>.{tar.gz,zip}`, `dist/SHA256SUMS`; `release.mode: keep-existing` (the workflow runs on an existing GitHub Release); secrets `HOMEBREW_TAP_GITHUB_TOKEN`, `SCOOP_BUCKET_GITHUB_TOKEN`, `WINGET_GITHUB_TOKEN` per channel (plus `GITHUB_TOKEN`) |
| CI toolchain | `actions/setup-go` ≥ v6 with `go-version-file: go.mod` (reads the `toolchain` line) |

### Known quirks / verification notes

- **Verified for real on 2026-10-16** in `$TMPDIR/iru-verify/cli/iru-setup-go-cli/{tui,none,nodist}` (outside this
  repository; Go 1.27.2 darwin/arm64), `bin-name: hello-cli`, module `github.com/example-org/hello-cli`: rendered
  from the reference files by a helper script, then `go build`/`go vet` (also `GOOS=windows` and `linux/arm64`), `go
  test -race -count=1 ./...` all green (`tui`: 5 packages; `none`: 4), coverage with `-coverpkg=./...` **94.7% total /
  97.3% across `internal/`** (`tui`) and **94.1% total** (`none`) — every `internal/` file ≥ 92.9%, `tools/gendocs`
  84.5%; `golangci-lint config verify` + `run` **0 issues**; `govulncheck` "No vulnerabilities found."; gendocs wrote
  10 man pages, 10 Markdown pages, 4 completion scripts and `cli-reference.adoc`; every contract smoke check above
  passed (EPIPE: exit 0, empty stderr); `goreleaser check` validated and `goreleaser release --snapshot --clean` built
  six archives + `SHA256SUMS` (+ cask, Scoop and WinGet manifests for `store`); the `none`/no-license render has no
  `LICENSE*` entry and `distribution: none` writes no `.goreleaser.yaml`.
- **testscript coverage**: `go test -coverprofile` with `-coverpkg=./...` counted the code run inside testscript's
  re-executed children (testscript forwards `GOCOVERDIR`) — `cmd/<bin>`'s own test run alone covered 59.7% of the
  module. Its `! exec` only asserts "non-zero", hence the custom `status` command.
- **Cobra behaviours the templates work around** (each verified): a command group (e.g. `completion`) prints its help
  and exits 0 for an unknown subcommand — `finishTree` gives groups `Args: cobra.NoArgs` + a help `RunE`, so `completion
  tcsh` exits 2; an unknown command fails before flags are parsed, so `--json frobnicate` would lose JSON mode —
  `formatFromArgs` scans the raw arguments; `help`/`completion` are created lazily on `Execute` — `finishTree` creates
  them up front so `schema` and gendocs see them; the version flag would take `-v` — the persistent `-v/--verbose`
  is defined first, so `--version` has no shorthand; required-flag and flag-group checks (`MarkFlagRequired`,
  `MarkFlagsMutuallyExclusive`) run after `PersistentPreRunE`, so config errors win over them; `cobra/doc` doesn't
  create output directories — gendocs does.
- **Signals**: `signal.NotifyContext` doesn't expose which signal arrived (its cause is an unexported string error),
  and 130 vs 143 depends on it — `notifySignals` records the signal itself; the second-signal path calls an injectable
  exit function so it is unit-tested. With `signal.Ignore(syscall.SIGPIPE)`, a write to a closed stdout returns EPIPE
  instead of killing the process (os/signal docs) — treated as success.
- **Panics**: an unrecovered Go panic exits with status 2, which collides with USAGE — `App.run` recovers and reports
  an internal error (exit 1, envelope code `INTERNAL` in JSON mode).
- **Bubble Tea v2**: `View()` returns a `tea.View` (alternate screen via `v.AltScreen = true`), keys arrive as
  `tea.KeyPressMsg`, ctrl+c is a key in raw mode (the model returns `tea.Interrupt` → `tea.ErrInterrupted` → exit 130),
  and `Run` with a non-terminal reader (`"j\r"`) works for tests. teatest v2 has no tagged release — pseudo-version
  only. teatest registers its own `-update` flag in the `internal/tui` test binary; the `-update` flag in
  `cmd/<bin>/main_test.go` lives in a different test binary, so they don't clash — never declare a second one in a
  package that imports teatest.
- **Lint fixes baked into the templates**: `gosec` G115 on `int(f.Fd())` (suppressed with a reasoned `//nolint`), G304
  in tests (`filepath.Clean`), G602 false positive on a pairwise loop (rewritten); `misspell` in the default (neutral)
  locale — the code says "color".
- **GoReleaser**: the before-hook output in `build/gendocs` survives `--clean` (only `dist/` is cleaned); casks have no
  `license` stanza (the field is left out); `manpages` must name a file that exists (`man/<bin>.1`, not `.1.gz`) or
  the cask silently omits it; `goreleaser check` fails without a git remote.
- **UI-contract additions unverified**: `.ui-quality.yml`, `Model.window` (+ `tea.WindowSizeMsg` handling),
  `internal/tui/ui_screenshots_test.go` and the matrix/window tests were added later without a Go toolchain on the
  authoring machine — written against the Bubble Tea v2 API (`View.Content`, `WindowSizeMsg`) and
  `github.com/charmbracelet/x/ansi.Strip`, never compiled here; the first `ui: tui` run's Step 7 is their
  verification. A run leaves 8 captures under `.ui-screenshots/screen/Model/` (4 states × `ltr`/`rtl` × `no-color`);
  `iru-setup-go-gitignore` ignores the directory.
- **Unverified locally, never a blocker**: running the Linux/Windows binaries (only cross-compiled and vetted), the
  Windows console behaviour of colour/TTY detection, a real (non-snapshot) release, pushing to a tap/bucket/WinGet, and
  the Antora build of the generated page (`iru-setup-antora`/the workflows own it).

Finish with a **Warn explicitly** block:

- Review every generated file before committing; replace the `greet` sample with real commands (each with `Short`,
  `Long`, `Example`, `Args` and `safety(...)` annotations) and keep the e2e scripts asserting every exit code it can
  emit.
- Run `iru-setup-go-gitignore` — `build/`, `dist/`, the root binary and coverage profiles must never be committed;
  `go.sum` always is.
- The exit-code numbers and the JSON field names are a public interface: never renumber a code; adding a JSON field
  keeps `schemaVersion`, renaming/removing/retyping one bumps it.
- Release secrets (`HOMEBREW_TAP_GITHUB_TOKEN`, `SCOOP_BUCKET_GITHUB_TOKEN`, `WINGET_GITHUB_TOKEN`) and the tap/bucket
  /fork repositories must exist before the first `store` release; the macOS binaries aren't notarized (the cask clears
  the quarantine flag).
- A module path major version ≥ 2 needs the `/vN` suffix before tagging `v2.0.0`.
- If a license was chosen and no `LICENSE` file exists, add one (`iru-check-license` backfills headers).
