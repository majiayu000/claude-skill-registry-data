---
name: iru-setup-cli-repository
description: >-
  End-to-end bootstrap for a command-line tool repository — a native, agent-friendly CLI in Rust (clap, optional
  Ratatui terminal UI), Go (Cobra, optional Bubble Tea terminal UI), Swift (swift-argument-parser) or C#/.NET 10
  (System.CommandLine + Spectre.Console, Native AOT, optional full-screen terminal UI) — that follows one contract
  across languages: data on stdout and messages on stderr, a documented exit-code taxonomy (0–7, 130/143),
  `--format text|json|jsonl` with a JSON error envelope, TTY/`NO_COLOR`-aware colour, no prompts without a terminal
  (`--no-input`/`--yes`), `--dry-run` for mutations, `completion`/`schema` commands and a CLI reference generated
  from the command tree. Collects `language` (`rust`/`go`/`swift`/`dotnet`), `ui` (`none`/`tui`; not offered for
  Swift), `accessibility` (`enforce`/`report`/`off` — only with `ui: tui`: the level of the terminal UI's asserted
  accessibility checks, written by the scaffold to `.ui-quality.yml`), `branching` (`gitflow`/`main-only`), the tool's identity (`bin-name`, `description`, license, developer
  name/email/organization URL, `owner`) and the shared pipeline parameters (integration branch `develop`, stable
  branch `main`, `open-source`, repository `visibility` (detected via `gh repo view` or asked), `ci`, `cross-os-ci`
  (when the ~10×-cost macOS and ~1.7×-cost Windows test legs run: `all`/`stable`), `ci-tests`, `pages`,
  `distribution` (`none` / `internal` = native binaries + SHA256SUMS + build-provenance attestations on GitHub
  Releases / `store` = also package channels such as crates.io, Homebrew, Scoop, WinGet or a NuGet .NET tool),
  `channels`, `sonar` plus its detail keys — each question stating the Actions-minutes / runner-multiplier /
  SonarCloud / Pages cost facts for that visibility) once, prints a setup-mode statement (from scratch, or an
  inventory of the prior setup it found), then orchestrates the language's scaffold (`iru-setup-rust-cli`,
  `iru-setup-go-cli`, `iru-setup-swift-cli`, or `iru-setup-dotnet-cli`) → `iru-setup-antora` → the language's
  gitignore skill (`iru-setup-rust-gitignore`, `iru-setup-go-gitignore`, `iru-setup-swift-gitignore` with
  `flavor: cli`, or `iru-setup-dotnet-gitignore`) → `iru-setup-cli-github-workflows` → `iru-setup-changelog` →
  `iru-setup-readme`, in that order, via `iru-isolated-skill-executor`, so nothing is asked twice — skipping the
  workflows step entirely (security block included) when `ci: no`. Invoke as `/iru-setup-cli-repository`,
  optionally with `args` (`key: value` lines) to pre-resolve `language`, `ui`, `accessibility`, `branching`, `mode`
  (`new`/`existing`), `open-source`, `visibility`, `ci`, `cross-os-ci`, `ci-tests`, `pages`, `distribution`,
  `channels`, `homebrew-tap`, `on-existing` (`ask`/`keep`/`update`/`replace`, forwarded only when supplied),
  `sonar` (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`), `integration-branch`, `stable-branch`, and
  every identity field, skipping the matching question. On an existing repository every component sub-skill warns
  about the prior setup it owns and asks Update / Keep as is / Replace per file (unless `on-existing` decides), and
  the final report states the action taken per component. Use whenever bootstrapping (or catching up) a CLI tool
  repository's full skeleton/docs/gitignore/CI/release/changelog/README scaffold in one pass.
model: haiku
---

# Setup CLI Repository

Bootstrap a brand-new (or catch up an existing) command-line tool repository in one pass by orchestrating six
skills: the language's **scaffold** (the package/module/solution with the command tree, the library unit that holds
the logic, unit + end-to-end CLI tests that reach the 80% coverage bar, formatter/linter/doc-lint configuration,
and a generator for the man page, shell completions and the AsciiDoc CLI reference), `iru-setup-antora` (Antora
documentation site), the language's **gitignore** skill (root `.gitignore`), `iru-setup-cli-github-workflows`
(CI, cross-OS tests, docs, release binaries and package channels, and the shared security workflows),
`iru-setup-changelog` (root `CHANGELOG.md`), and `iru-setup-readme` (root `README.md`). This skill does not
duplicate any of their logic — it collects the shared parameters once and passes each skill only the `args` keys
that skill's own Step 0 actually accepts, so the user isn't asked the same question twice and no sub-skill sees a key
it doesn't recognize.

Each of Steps 4–9 invokes its sub-skill via the `iru-isolated-skill-executor` agent (`subagent_type:
"iru-isolated-skill-executor"`, always naming the full `iru-`-prefixed skill inside the prompt, e.g.
`Skill({skill: "iru-setup-rust-cli", args: "..."})`) rather than calling `Skill(...)` directly — every sub-skill
re-derives what it needs from the files the previous steps wrote, so only a short completion summary flows back.
Every sub-agent is launched with `run_in_background: false` — each step depends on the previous one's files being on
disk.

**What every generated tool promises** (the contract the scaffolds implement and the workflows smoke-test, from the
author's *Building CLIs for AI Agents* guide): data on stdout and everything else on stderr; exit codes `0` OK, `1`
internal, `2` usage, `3` validation, `4` not found, `5` confirmation required, `6` retryable, `7` auth, `130`/`143`
after SIGINT/SIGTERM; `--format text|json|jsonl` (`--json` alias) with a `schemaVersion` and a JSON error envelope on
stderr; colour and progress only on a terminal (`NO_COLOR`, `TERM=dumb`, `--no-color` honoured); no prompt without a
terminal (`--no-input`, `<BIN>_NO_INPUT`, `--yes`); `--dry-run` plans for mutations; generated `completion` and a
machine-readable `schema` of the command tree; a terminal UI, when chosen, as its own TTY-gated command whose every
function also has a non-interactive `--json` equivalent. Tell the user this once in Step 1, briefly — it is why the
tool is equally usable by a person, a script, and an AI agent.

Scope: a single command-line tool (one binary) per repository. A library without a binary, a service, or a desktop
app is out of scope — point the user at `/iru-setup-repository`.

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-cli-repository`) or by the catalog's `iru-setup-repository` front door (project
type `cli-tool (<language>)`), so parse `args` first, as `key: value` lines, one per line, e.g.:

```
language: rust
ui: tui
branching: gitflow
mode: new
open-source: yes
visibility: public
ci: yes
cross-os-ci: all
ci-tests: full
pages: yes
distribution: store
channels: crates-io,homebrew
homebrew-tap: example-org/homebrew-tap
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_logsift
sonar-host-url: https://sonarcloud.io
integration-branch: develop
stable-branch: main
bin-name: logsift
```

Recognized keys:

- **Shape and mode**: `language` (`rust`/`go`/`swift`/`dotnet`), `ui` (`none`/`tui`), `accessibility`
  (`enforce`/`report`/`off` — meaningful only with `ui: tui`; ignored and named in the report otherwise), `branching`
  (`gitflow`/`main-only`), `mode` (`new`/`existing`).
- **Shared pipeline vocabulary**: `open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal`), `ci`
  (`yes`/`no`), `cross-os-ci` (`all`/`stable`), `ci-tests` (`unit`/`full`), `pages` (`yes`/`no`), `on-existing`
  (`ask`/`keep`/`update`/`replace` — never asked; forwarded to the component sub-skills only when it arrived here via
  `args`), `distribution` (`none`/`internal`/`store`), `channels` (comma list), `homebrew-tap` and `scoop-bucket`
  (`owner/repo`),
  `sonar` (`cloud`/`self-hosted`/`none`) plus, only when set, `sonar-organization`/`sonar-project-key`/
  `sonar-host-url`, `integration-branch`, `stable-branch`.
- **Identity fields** named in Step 2: `bin-name`, `description`, `owner`, `license`, `developer-name`,
  `developer-email`, `organization-url`, plus the language-specific names the scaffold accepts and this skill
  forwards untouched when supplied: `crate-name`, `msrv` (Rust); `module-path`, `go-version` (Go); `package-name`,
  `swift-version`, `platforms` (Swift); `tool-name`, `package-id` (.NET).
- `publish` is accepted and ignored (a CLI is distributed, not published as a dependency) — note it in the report if
  supplied; for a Rust tool, crates.io is a `store` channel instead.

Every key found here is resolved — skip the matching question in Steps 1–3. If `args` is absent or doesn't look like
this format, treat everything as unset and ask normally.

## Step 1 — Resolve the language, terminal UI, branching model and mode

Survey the repository root first — `Cargo.toml` (+ `src/main.rs`, `xtask/`), `go.mod` (+ `cmd/*/main.go`,
`.goreleaser.yaml`), `Package.swift` (an `.executableTarget` on `ArgumentParser`), `*.slnx`/`*.sln` and `*.csproj`
(an `Exe` on `System.CommandLine`) — since their presence decides `language`, `ui` and `mode` without a question in
the common cases. If more than one language's manifest is present, or the manifest belongs to something that isn't a
CLI (a library-only crate, a web service, a desktop app), stop and say what was found — this skill bootstraps one
command-line tool.

Unless `language` was supplied via `args`, resolve it:

- Detected from disk → confirm the detected value with the user rather than assuming it silently.
- Nothing on disk yet → `AskUserQuestion` with four options (state the trade-offs, not a ranking — "choose the one
  your team already maintains"):
  - **Rust** (`rust`) — "clap derive parser checked at compile time, single static binary, fastest startup; Ratatui
    for an optional full-screen terminal UI; ships to crates.io and Homebrew."
  - **Go** (`go`) — "Cobra command tree with generated docs and completion, trivial cross-compilation, GoReleaser
    releases (Homebrew, Scoop, WinGet); Bubble Tea for an optional terminal UI."
  - **Swift** (`swift`) — "swift-argument-parser on macOS and Linux (static Linux binaries); natural when the team
    already writes Swift. No full-screen terminal UI library is maintained — styled output only."
  - **C# / .NET** (`dotnet`) — "System.CommandLine on .NET 10, Native AOT single-file binaries, also installable as
    a .NET tool from NuGet; Spectre.Console for rich output."

Unless `ui` was supplied via `args`, resolve it:

- Detected from disk (Rust `ratatui`, Go Bubble Tea, .NET Terminal.Gui or a Spectre.Console live `browse` command)
  → confirm.
- `language: swift` → `ui: none` without asking; say why (the only Swift TUI library, SwiftTUI, has seen no
  development since 2024; recommend Rust or Go when a full-screen interface matters).
- Otherwise `AskUserQuestion`:
  - **Commands only (Recommended)** (`none`) — "Subcommands that do one thing and return a result — the shape
    scripts and AI agents use. Colour, tables and progress still appear on a terminal."
  - **Commands + terminal UI** (`tui`) — "Adds a full-screen interactive `browse` command for people at a terminal
    (Ratatui / Bubble Tea / .NET). It only starts on a TTY; every function it offers stays available as a
    non-interactive command with `--json`."

With `ui: tui`, unless `accessibility` was supplied via `args` (or an existing `.ui-quality.yml` already sets it —
confirm that value instead), ask it once with `AskUserQuestion`: "Automated accessibility checks in UI tests?" —
**Enforce (Recommended)** ("violations fail the UI tests") / **Report only** ("listed in the test report, never
failing") / **Off** ("not run; the coding defaults still apply"). Say that for a terminal UI these are the asserted
checks the UI tests run — the selection visible without colour, the key help on screen, every action on a key — since
no automated accessibility audit exists for terminals. With `ui: none` it is never asked or forwarded.

Unless `branching` was supplied via `args`, resolve it with `AskUserQuestion` (two options):

- **gitflow** (recommended, this catalog's house pattern) — an integration branch (`develop`) plus a stable branch
  (`main`, releases only); `iru-setup-cli-github-workflows` generates `build.yml`/`release.yml`/`sync.yml`, and
  `sync.yml` opens the post-release version-bump PR back into the integration branch.
- **main-only** — a single stable branch; no `sync.yml`. Step 3's integration-branch question is skipped.

If `mode` wasn't supplied, check whether any artifact in the inventory below exists: if the language's manifest
does, default to `existing` and confirm with `AskUserQuestion` (`existing` pre-selected; `new` as the other option,
noting that either way every sub-skill still asks Update / Keep as is / Replace for each file it owns that already
exists); if nothing exists, default to `new` without asking.

### Setup mode

Right after resolving `mode`, print a short **Setup mode** statement:

- `mode: new` → "Setting up this repository **from scratch** — no prior setup found."
- `mode: existing` → "**Updating an existing repository** — prior setup found:" followed by an inventory table of
  every component this run owns, each marked **absent / present / partial** with the evidence (file paths):

  | Component | Evidence checked |
  |---|---|
  | Build manifest | Rust `Cargo.toml` + `Cargo.lock` (+ `rust-toolchain.toml`); Go `go.mod` + `go.sum`; Swift `Package.swift` + `Package.resolved`; .NET `*.slnx`/`*.sln`, `Directory.Build.props`, `Directory.Packages.props`, `global.json` |
  | Command tree + library unit | Rust `src/main.rs` + `src/lib.rs` (+ `src/cli.rs`, `src/commands/`); Go `cmd/<bin>/main.go` + `internal/cli/`; Swift `Sources/<Bin>/` + `Sources/<Bin>Kit/`; .NET `src/<Tool>/` + `src/<Tool>.Core/` |
  | Terminal UI | Rust `src/tui/`; Go `internal/tui/`; .NET the `browse` command |
  | UI quality config (`ui: tui`) | root `.ui-quality.yml` (accessibility level, capture directions/themes) |
  | Tests | Rust `tests/`; Go `*_test.go` + `testdata/script/`; Swift `Tests/`; .NET `tests/<Tool>.Core.Tests`, `tests/<Tool>.Cli.Tests` |
  | Docs generator | Rust `xtask/`; Go `tools/gendocs/` (or `internal/tools/gendocs/`); Swift the `generate-manual` plugin; .NET the `schema`→AsciiDoc step |
  | Quality config | `rustfmt.toml`, `clippy.toml`, `deny.toml`, `[lints]`; `.golangci.yml`; `.swiftlint.yml`, `.swift-format`; `.editorconfig`, `stylecop.json` |
  | Release config | `.goreleaser.yaml` (Go); release profile in `Cargo.toml`; `PublishAot`/`PackAsTool` in the .NET csproj |
  | Sonar config | `sonar-project.properties` |
  | Antora docs | `docs/antora.yml`, `docs/antora-playbook.yml`, `docs/modules/ROOT/` |
  | `.gitignore` | root `.gitignore` |
  | Workflows | each of `.github/workflows/build.yml`/`release.yml`/`sync.yml`/`security.yml`, `.github/scripts/sync_versions.py` |
  | Dependabot | `.github/dependabot.yml` |
  | `CHANGELOG.md` | root `CHANGELOG.md` |
  | `README.md` | root `README.md` |
  | `LICENSE` | root `LICENSE*` (reported only — no sub-skill here writes it) |

  Then: "For each component that already exists you'll be asked whether to keep it, update it, or replace it."
  Those questions are asked by the component sub-skills (Steps 4–9) — never by this orchestrator too.

## Step 2 — Collect the tool's identity

**`mode: existing` with the language's manifest already on disk**: skip every identity question — the scaffold reads
its defaults from the existing manifest when the user chooses Update or Replace there, and `iru-setup-readme`
derives identity from the files too. Resolve `license` only if `args` supplied it, and record in the final report
that identity was taken from the existing files.

Otherwise, for any field not resolved from `args`, ask directly (plain conversation — free text):

- **bin-name** — the command users type (lowercase, digits and `-`, e.g. `logsift`); it names the binary, the
  release archives, the man page, the completion scripts and the `<BIN>_*` environment variables (uppercase, `-` →
  `_`). Check it doesn't shadow a common system command (`test`, `install`, `find`, …) and say so if it does.
- **description** — one sentence for `--help`, the package manifest and the README.
- **owner** — the GitHub owner (user or organization); default from `git remote get-url origin` when present. It
  feeds the Go module path, the Homebrew tap and the repository URLs.
- **developer name**, **developer email**, **organizationUrl** — recorded by the scaffold (package authors) and seen
  by `iru-setup-readme`/`iru-check-license`.
- Leave the language-specific names (`crate-name`, `module-path`, `package-name`, `tool-name`, `package-id`) and
  toolchain floors (`msrv`, `go-version`, `swift-version`) unset unless `args` supplied them — each scaffold derives
  them from `bin-name`/`owner` and the live toolchain and explains its choice.

Then resolve the **license** with `AskUserQuestion`, unless `args` supplied one: MIT License / Apache License 2.0
(Rust tools are commonly dual-licensed `MIT OR Apache-2.0` — offer that as a third option when `language: rust`) /
No license (proprietary) / Other (ask name + URL afterward). Recommend MIT, or `MIT OR Apache-2.0` for Rust.

## Step 3 — Collect the pipeline parameters

Ask directly, presenting each default so a blank reply accepts it (skip any resolved from `args`, skip the
integration branch when `branching: main-only`, and skip every workflow-only row once `ci: no` is resolved — if `ci`
is still unresolved, ask the open-source/visibility/`ci` questions below first):

| Parameter | `args` key | Default | Consumed by |
|---|---|---|---|
| Integration branch | `integration-branch` | `develop` | `iru-setup-cli-github-workflows` (gitflow only) |
| Stable branch | `stable-branch` | `main` | `iru-setup-cli-github-workflows` |

Then resolve, with `AskUserQuestion`, in this order (skip any already resolved). Quote the cost facts "per GitHub's
current pricing" (verified October 2026 against docs.github.com) and tell the user to double-check their plan:

- **open-source** — Yes / No. Drives the recommended defaults below.
- **visibility** — if the repository has a GitHub remote, run `gh repo view --json visibility -q .visibility`
  (lowercase it) and tell the user the detected value; otherwise ask **Public** / **Private** (Public recommended when
  open source). Open source + private/internal is contradictory — warn and ask which is right. `internal` behaves like
  `private` below.
- **ci** — "Generate GitHub Actions workflows (CI/CD) for this repository?" Public: recommend **Yes** (standard
  GitHub-hosted runners, macOS and Windows included, are free for public repositories). Private/internal: offer
  **Yes** first but state that private repositories consume the account's included minutes — 2,000/month on GitHub
  Free, 3,000 on Pro and Team, 50,000 on Enterprise Cloud — then are billed per minute (Linux 2-core $0.006, Windows
  2-core $0.010 (~1.7×), **macOS $0.062 (~10×)**), and that a CLI's lint, tests, coverage and docs run on Linux while
  the cross-OS test legs and the macOS/Windows release builds use those pricier runners. **No** = "no workflows —
  build, test and release locally (re-run `iru-setup-cli-github-workflows` later)". `ci: no` ⇒ Step 7 is skipped
  entirely and `cross-os-ci`/`ci-tests`/`pages` aren't asked.
- **cross-os-ci** (only with `ci: yes`) — "When should the macOS and Windows test legs run?"
  - **Every push and pull request** (`all`) — recommended for public: a CLI's path, terminal and signal handling
    differ per OS, and the legs are free on a public repository.
  - **Stable branch and manual runs only** (`stable`) — recommended for private/internal: lint, tests, coverage and
    docs still run on Linux on every push/PR; macOS (~10×) and Windows (~1.7×) only on pushes to the stable branch
    and `workflow_dispatch`. Swift tools have no Windows leg.
- **sonar** — "Configure SonarCloud / SonarQube and send CI analysis and coverage reports to it?"
  `cloud`/`self-hosted`/`none`. Recommend **`cloud`** only when open source **and** public; otherwise state that
  SonarCloud is free only for public/open-source projects (a private project needs a paid plan) and recommend
  **`none`**, offering **self-hosted** (Community Build is free, but you run the server). With `ci: no`, say nothing
  would send reports and recommend `none`. For `cloud`/`self-hosted` collect `sonar-organization`/
  `sonar-project-key`/`sonar-host-url` (SonarCloud: suggest `<owner>-github` / `<owner>_<repo>` /
  `https://sonarcloud.io` from `git remote get-url origin`). (Sonar's Rust and Go analysis consume the lcov/coverprofile
  reports the build job produces; say that Rust support in SonarQube Cloud is newer than the other languages and to
  check their plan includes it.)
- **ci-tests** (only with `ci: yes`) — "Which tests should CI run?"
  - **Unit + CLI end-to-end on Linux** (`unit`, recommended for private/internal) — "Every unit test and the
    end-to-end tests that run the real binary (exit codes, JSON output, no-TTY behaviour) on Linux; the cross-OS legs
    run the same suite on the schedule chosen above."
  - **Full** (`full`, recommended for public) — "Also any container-backed tests (marked `#[ignore]` in Rust or with
    the `integration` build tag in Go — the scaffolds have none by default) and the release-mode smoke test of every
    target binary built in CI."
- **pages** (only with `ci: yes`) — public: **yes** without asking (say so in the report). Private/internal: ask —
  **No (Recommended)** ("CI still builds the Antora site, the API docs and the generated CLI reference and uploads
  them as a workflow artifact; nothing is published") vs **Yes** ("requires GitHub Pro, Team, or Enterprise Cloud; the
  site is PUBLIC unless you're on Enterprise Cloud with private Pages access control").
- **distribution** — `none`/`internal`/`store`. Default **`store`** when open source (say so); otherwise ask with
  **`internal`** recommended:
  - `none` — "CI only; build and install locally (`cargo install --path .`, `go install ./cmd/<bin>`, `swift build -c
    release`, `dotnet publish`)."
  - `internal` — "Each GitHub Release gets native binaries for every target (Linux, macOS and — except Swift —
    Windows, x86-64 and ARM64), as `tar.gz`/`zip` archives with a `SHA256SUMS` file and GitHub build-provenance
    attestations; users download them, or install with the documented one-liner."
  - `store` — "`internal` plus package channels so users can `brew install` / `cargo install` / `scoop install` /
    `winget install` / `dotnet tool install` it." Then resolve **`channels`** (multi-select `AskUserQuestion`, the
    language's defaults pre-selected): Rust `crates-io`, `homebrew`; Go `homebrew`, `scoop`, `winget`; Swift
    `homebrew`; .NET `nuget`, `winget`. With `homebrew`, resolve **`homebrew-tap`** (default `<owner>/homebrew-tap`; the
    tap repository must exist and needs a token secret — the workflows skill lists it). `crates-io` needs a license: an
    unlicensed Rust tool is scaffolded with `publish = false`, so don't offer that channel when `license: none`.

These values pass through unchanged to Step 4 (the scaffold) and Step 7 (`iru-setup-cli-github-workflows`), so
neither re-asks them.

## Step 4 — Run the scaffold

Always invoke it, in either `mode`. When scaffold files already exist it announces that it is updating and asks, per
file group, Update / Keep as is / Replace / Stop itself (unless `on-existing` decides). Pick the skill from
`language`:

| `language` | Scaffold skill | Gitignore skill (Step 6) |
|---|---|---|
| `rust` | `iru-setup-rust-cli` | `iru-setup-rust-gitignore` |
| `go` | `iru-setup-go-cli` | `iru-setup-go-gitignore` |
| `swift` | `iru-setup-swift-cli` | `iru-setup-swift-gitignore` (`flavor: cli`) |
| `dotnet` | `iru-setup-dotnet-cli` | `iru-setup-dotnet-gitignore` |

Format Steps 1–3's answers as `key: value` lines using **only** the keys the chosen scaffold's own Step 0 accepts
(re-read it on disk before sending — this table is the contract as of this catalog version):

| Key | `rust` | `go` | `swift` | `dotnet` |
|---|---|---|---|---|
| `bin-name`, `description`, `owner`, `license`, `developer-name`, `developer-email`, `organization-url`, `open-source`, `visibility`, `ci`, `sonar` (+ the three detail keys when set), `distribution`, `mode`, `on-existing` (only if supplied via `args`) | ✓ | ✓ | ✓ | ✓ |
| `ui` | ✓ | ✓ | — (never sent) | ✓ |
| `accessibility` (only with `ui: tui`) | ✓ | ✓ | — (never sent) | ✓ |
| `branching` (decides `0.1.0-dev` vs `0.1.0` as the starting version) | ✓ | — send `version: 0.1.0` for `main-only` instead | — | ✓ |
| `channels` (only with `distribution: store`) | — | ✓ (+ `homebrew-tap`, `scoop-bucket` when set) | — | ✓ |
| language-specific names (only if supplied) | `crate-name`, `msrv`, `repository-url` | `module-path`, `go-version` | `package-name`, `swift-version`, `platforms` | `tool-name`, `package-id` |

```
Agent({
  description: "Run <scaffold skill>",
  subagent_type: "iru-isolated-skill-executor",
  prompt: "Invoke Skill({skill: \"<scaffold skill>\", args: \"<one key: value line per applicable key above>\"}).
    Report back: whether it scaffolded from scratch or updated an existing project, the action taken per file group
    (created / updated / replaced / kept as is, or that the user chose Stop), which versions came from a live lookup
    versus the recorded fallback, the toolchain floor it resolved (MSRV / go directive / Swift tools version and
    macOS floor / .NET SDK), its docs-generator command, and the pass/fail/unverified result of each verification
    command it ran (build, unit + e2e tests, coverage on the library unit, linters, doc build, docs generator,
    contract smoke checks, release-mode build).",
  run_in_background: false
})
```

Never send an empty key. `cross-os-ci`, `ci-tests`, `pages`, `integration-branch`, `stable-branch` and the
workflows-only release keys are Step 7's alone. A Swift tool on `main-only` starts at `0.1.0-dev` (the scaffold has no
version key): say in Step 10 that the first release needs `/iru-swift-bump-version 0.1.0` before tagging, because
`release.yml` checks the tag against `Version.swift`. If the scaffold reports **Stop**, stop here too.

## Step 5 — Run `iru-setup-antora`

`Agent({description: "Run iru-setup-antora", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-antora\"}) with no args (or, only if `on-existing` arrived via this orchestrator's own args,
args: \"on-existing: <on-existing>\" — the only key it accepts) — it derives the component name, title, and version
itself from the project manifest, and asks Update / Keep / Replace itself if docs exist. Report back: created vs
updated, the action taken, and whether the site build succeeded.", run_in_background: false})`.

Run it before Step 7 so the workflows skill's survey finds `docs/antora.yml`/`docs/antora-playbook.yml` in place for
its docs job. If it asks for a starting version, answer with the scaffold's version minus its `-dev` suffix
(`0.1.0`).

Then wire the generated CLI reference into the new site — no scaffold writes Antora files before this step exists:

1. Re-run the scaffold's docs generator once, now that `docs/modules/ROOT` exists:

   | `language` | Command | Writes |
   |---|---|---|
   | `rust` | `cargo xtask docs` | `docs/modules/ROOT/pages/cli-reference.adoc` (+ `target/dist/{man,completions}/`) |
   | `go` | `go run ./tools/gendocs` | `docs/modules/ROOT/pages/cli-reference.adoc` (+ `build/gendocs/{man,markdown,completions}/`) |
   | `swift` | `scripts/generate-docs.sh build/gendocs` | `docs/modules/ROOT/partials/cli-reference.adoc` (+ man page, completions, `schema.json`) |
   | `dotnet` | `dotnet run --project src/<Tool> -c Release -- gen-docs --output-dir .` | `docs/modules/ROOT/pages/cli-reference.adoc` (+ `artifacts/{man,completions}/`) |

2. For `swift` only, create `docs/modules/ROOT/pages/cli-reference.adoc` holding a `= Command-line reference` title
   and `include::partial$cli-reference.adoc[]` (the generator writes a partial, not a page).
3. Add `* xref:cli-reference.adoc[Command-line reference]` to `docs/modules/ROOT/nav.adoc` if it isn't there, then
   rebuild the site (`cd docs && npx antora antora-playbook.yml`) to confirm the page resolves.

Run these three as one `iru-isolated-skill-executor` agent (a plain task prompt, no skill) and report the outcome in
Step 10; a generator failure here is reported, not fixed — the scaffold's own verification already covered it.

## Step 6 — Run the gitignore skill

`Agent({description: "Run <gitignore skill>", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"<gitignore skill>\", args: \"<flavor: cli — iru-setup-swift-gitignore only; bin-name: <bin-name> —
iru-setup-go-gitignore only>\\nmode: <mode>\\non-existing: <..., only if supplied via args>\"}) — it detects the build outputs, coverage files, release archives and docs output
itself; a command-line tool commits its lockfile (Cargo.lock / go.sum / Package.resolved / packages.lock.json when
used). Report back only the action taken on the root .gitignore (created / updated / replaced / kept as is).",
run_in_background: false})`.

Run it after Steps 4–5 and before Step 7, so build output (`target/`, `dist/`, `.build/`, `bin/`/`obj/`), coverage
reports, release archives and the Antora output are ignored before any CI report appears locally.

## Step 7 — Run `iru-setup-cli-github-workflows`

**Skip entirely when `ci: no`** — no `.github/workflows/*`, no `security.yml`, no `.github/dependabot.yml`, no
`sync.yml`/`sync_versions.py`. Record it in Step 10 as "skipped (ci: no)", noting that the shared security block
(Dependabot, dependency-review, CodeQL, OSV-Scanner, gitleaks) was skipped with it and that
`/iru-setup-cli-github-workflows` adds it later.

Otherwise:

```
Agent({
  description: "Run iru-setup-cli-github-workflows",
  subagent_type: "iru-isolated-skill-executor",
  prompt: "Invoke Skill({skill: \"iru-setup-cli-github-workflows\", args: \"language: <language>\\n
    bin-name: <bin-name>\\nui: <ui>\\nbranching: <branching>\\nintegration-branch: <integration-branch, gitflow only>\\n
    stable-branch: <stable-branch>\\ncross-os-ci: <cross-os-ci>\\nci-tests: <ci-tests>\\n
    open-source: <open-source>\\nvisibility: <visibility>\\npages: <pages>\\ndistribution: <distribution>\\n
    channels: <channels, only with store>\\nhomebrew-tap: <homebrew-tap, only with the homebrew channel>\\n
    sonar: <sonar>\\nsonar-organization: <..., if set>\\nsonar-project-key: <..., if set>\\n
    sonar-host-url: <..., if set>\\nmode: <mode>\\non-existing: <..., only if supplied via args>\"}). Report back:
    whether it created the pipeline from scratch or updated an existing one; per file (build.yml, release.yml,
    sync.yml + sync_versions.py, security.yml, .github/dependabot.yml) the action taken (created / updated /
    replaced / kept as is, with any mismatch listed for a kept file, or Stop); the release targets and channels it
    wired; when the cross-OS legs run; whether docs go to GitHub Pages or a workflow artifact; any open gap it
    flagged; whether the `.ui-screenshots/` upload was wired (`ui: tui`); and the full required-secrets/settings
    table it produced.",
  run_in_background: false
})
```

Omit `integration-branch` for `main-only`. The workflows skill detects the build/test/docs commands, the release
targets and the version file from disk itself; the shared `license`/`developer-*`/`organization-url` keys are never
passed. A **Stop** there is reported, not treated as a failure.

## Step 8 — Run `iru-setup-changelog`

`Agent({description: "Run iru-setup-changelog", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-changelog\"}) with no args (or args: \"on-existing: <on-existing>\" only if it arrived via
this orchestrator's own args), working from the repository's own tag/release history. Report back only the action
taken on CHANGELOG.md (created — with the version range reconstructed — / updated / replaced / kept as is).",
run_in_background: false})`. Independent of Steps 4–7; run it before Step 9.

## Step 9 — Run `iru-setup-readme`

`Agent({description: "Run iru-setup-readme", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-readme\", args: \"sonar: <sonar>\\nci: <ci>\\npages: <pages; no when ci is no>\\n
on-existing: <..., only if supplied via args>\"}) — those are the only keys it accepts — deriving everything else
from the repository (the manifest, the release workflow and its channels, the Antora docs, sonar-project.properties,
CHANGELOG.md). Report back only which sections were included vs. omitted and why.", run_in_background: false})`.
Run it last. A command-line tool's Installation section lists the channels actually wired (Homebrew tap, `cargo
install`, `go install`, Scoop/WinGet, `dotnet tool install -g`, or the release archive + checksum verification), and
its usage section shows a human example, a `--json` example piped to `jq`, and the exit-code table.

## Step 10 — Report

Summarize all six delegated skills together: repeat the **Setup mode**, the resolved `language`, `ui`, `branching`
and `mode`, the tool identity and license, and the pipeline parameters actually applied. Then a per-component table —
build manifest, command tree + library unit, terminal UI, `.ui-quality.yml` (`ui: tui` only), tests, docs generator, quality config, release config,
Sonar config, the Antora site (and whether the generated CLI reference page is in its nav), `.gitignore`, each
workflow file + `sync_versions.py`, `.github/dependabot.yml`, `CHANGELOG.md`, `README.md` — with the action taken for
each: **created / updated / replaced / kept as is / skipped (ci: no)** (or not reached, after a Stop), and for
anything kept as is, the mismatches its sub-skill listed.

State explicitly what was wired or deliberately omitted, and why:

- **`language`** and **`ui`** — and, for Swift, that no terminal UI was offered and why. With `ui: tui`, the
  **`accessibility`** level written to `.ui-quality.yml`, that the TUI's UI tests leave text captures in
  `.ui-screenshots/` (gitignored; uploaded by CI as a 7-day artifact), and that the accessibility checks are asserted
  terminal checks, not an automated audit.
- **`open-source`** / **`visibility`** (and whether visibility came from `args`, `gh repo view`, or a question).
- **`ci`**: with `no`, no workflows/`security.yml`/Dependabot were generated.
- **`cross-os-ci`** / **`ci-tests`**: when the macOS/Windows legs run, restating the runner multipliers on private
  repositories.
- **`pages`**: `yes` (Antora + API docs + CLI reference deployed to GitHub Pages) or `no` (workflow artifact).
- **`distribution`** / **`channels`**: the release targets, the archives/checksums/attestations, and each package
  channel with the secret or trusted-publishing setup it needs.
- **`sonar`**: whether `sonar-project.properties` and the CI Sonar step were included.
- **Versions**: which came from a live lookup versus a recorded fallback (scaffold and workflows).

Unless Step 7 was skipped, reproduce the **required-secrets/settings table** `iru-setup-cli-github-workflows`
reported, verbatim, plus its repository-settings notes (Pages source = GitHub Actions for `pages: yes`; "Workflow
permissions" allowing Actions to create pull requests for gitflow's `sync.yml`).

List every decision made on the user's behalf: the license recommendation, `ui: none` as the recommended shape (and
`none` forced for Swift), `pages` defaulted to `yes` for a public repository, `distribution` defaulted to `store` for
an open-source tool, the visibility-based `cross-os-ci`/`ci-tests` recommendations, and any name the scaffold derived
(`crate-name`, module path, package id).

Finish with an explicit **Warn explicitly** block, repeating each sub-skill's closing warning:

- **Review every generated/updated file before building, committing, or relying on CI.** Confirm the license matches
  a root `LICENSE` (`iru-check-license` can generate one and backfill headers), and that the build, the tests and the
  docs generator succeed locally with the commands the scaffold reported.
- The exit codes and the JSON `schemaVersion` are a public contract: once released, never renumber an exit code, and
  bump `schemaVersion` for any breaking change to a JSON output.
- Cross-OS test legs, release builds for non-host targets, signing/notarization, Homebrew/Scoop/WinGet/crates.io/NuGet
  publishing can only be exercised on GitHub with the listed secrets — do a `workflow_dispatch` dry run of
  `release.yml` before the first real release.
- Every secret in the table, the Homebrew tap repository, and the SonarCloud project must exist before CI can pass —
  nothing here creates accounts, repositories or credentials.

## Sources

- irurueta docs: ai/cli-for-agents/index.adoc (three audiences, one tool), agent-readiness-checklist.adoc,
  streams-and-exit-codes.adoc, tty-colour-and-interactivity.adoc, machine-readable-output.adoc,
  safety-and-idempotency.adoc, tuis-vs-clis.adoc, frameworks-go-and-rust.adoc, frameworks-swift-and-dotnet.adoc,
  packaging-and-distribution.adoc — https://www.irurueta.com/ai/cli-for-agents/index.html
- GitHub Docs — Actions billing and runner pricing; GitHub Pages availability (checked October 2026)
