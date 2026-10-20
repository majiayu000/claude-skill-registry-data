---
name: iru-setup-swift-cli
description: >-
  Scaffold an agent-friendly Swift command-line tool at the repository root — a SwiftPM package (`Package.swift`,
  `swift-tools-version` 6.0 by default, `swiftLanguageModes: [.v6]`, macOS 15+ and Linux) with a thin
  swift-argument-parser executable target `Sources/<Bin>/` (an `AsyncParsableCommand` root whose
  `static func main() async` hands the process to the Kit's `CommandRunner`, plus the `greet [NAME]`, `completion
  <bash|zsh|fish>` and `schema [COMMAND] [--asciidoc]` subcommands and `--version`) and a `Sources/<Bin>Kit/` library
  holding every behaviour: the exit-code enum exactly as the catalog's CLI contract (0–7, 130, 143), usage errors
  mapped to exit 2 instead of swift-argument-parser's default 64, `--help`/`--version` on stdout, the JSON error
  envelope on stderr with sorted keys, `--format text|json|jsonl`/`--json`, `--no-color`/`NO_COLOR`/`FORCE_COLOR`/
  `TERM=dumb` and `isatty` per stream (Darwin/Glibc/Musl behind one file), prompts only on a terminal and never with
  `--no-input`/`<BIN>_NO_INPUT`/`CI=true`, `--quiet`/`--verbose`/`--log-format`, SIGINT/SIGTERM through
  `DispatchSource` signal sources → cleanup + exit 130/143 (second signal exits immediately), SIGPIPE ignored and
  EPIPE as a quiet stop, a `schema` command tree built from `--experimental-dump-help` plus per-command exit codes and
  safety metadata, `Version.swift` (`toolVersion = "0.1.0-dev"`); Swift Testing `Tests/<Bin>KitTests` (≥ 80% line
  coverage of the Kit; ~95% as scaffolded) and `Tests/<Bin>CLITests` that run the built executable through `Process`
  and assert stdout, stderr and the exit status of every code the command line can produce; `.swift-format`,
  `.swiftlint.yml`, a DocC catalog for the Kit, `scripts/generate-docs.sh` (man page via swift-argument-parser's
  `generate-manual` plugin, bash/zsh/fish completions, `schema.json`, and the Antora partial
  `docs/modules/ROOT/partials/cli-reference.adoc`), and `sonar-project.properties` when `sonar` ≠ `none`. No terminal
  UI is offered (SwiftTUI has been dormant since 2024 — use the Rust or Go scaffold for a full-screen TUI). Invoke as
  `/iru-setup-swift-cli`. Accepts pre-resolved inputs via `args` (`key: value` lines): `bin-name`, `package-name`,
  `description`, `swift-version` (tools-version floor), `platforms` (`macos=<min>`; Linux is always supported),
  `owner`, `license`, `developer-name`, `developer-email`, `organization-url`, `open-source`, `visibility`, `ci`,
  `sonar` (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`), `distribution`, `mode` and `on-existing` — so
  `iru-setup-cli-repository` can supply them without re-prompting. Announces whether it is scaffolding from scratch or
  updating; for every file group it owns that already exists it warns and asks Update / Keep as is / Replace / Stop
  (unless `on-existing` decides) and never overwrites hand-written source. Versions (swift-argument-parser,
  swift-docc-plugin) are looked up live with a verified 2026-10-16 fallback. Every template was rendered and verified
  with Swift 6.4 on macOS (build, tests, coverage, swift-format, SwiftLint, DocC, generate-manual, a universal
  release binary and contract smoke checks). Use whenever a new Swift command-line tool repository needs its package,
  contract implementation, tests, quality config and docs generator bootstrapped from this house template.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(swift *) Bash(xcrun *) Bash(lipo *) Bash(swiftlint *) Bash(scripts/generate-docs.sh *) Bash(curl *) Bash(git *) Bash(gh *) Bash(python3 *) Bash(mkdir *) Bash(find *) Bash(ls *) Bash(chmod *) Bash(jq *) Agent
---

# Setup Swift CLI

Generate a complete, buildable Swift command-line tool that follows this catalog's agent-friendly CLI contract —
data on stdout and messages on stderr, one exit code per caller reaction, machine-readable output with a JSON error
envelope, TTY-aware colour and prompts, signal and broken-pipe handling, and a self-describing command tree — from the
templates in this skill's `reference/` files. The executable target is deliberately thin: every behaviour lives in
the `<Bin>Kit` library so it is unit-tested in-process, and a second test target runs the real binary.

The layout is the **scaffold contract** that `iru-swift-code-one-task(-group)` (CLI shape), the `iru-swift-*` gates,
`iru-swift-bump-version` (the `Version.swift` literal) and `iru-setup-cli-github-workflows` detect and call — Step 8's
contract table lists the confirmed commands and paths. This skill writes no CI workflow, `.gitignore`, README,
changelog, `LICENSE` or Antora page (`iru-setup-cli-repository` chains the skills that do; `iru-setup-antora` owns
`docs/antora.yml`); the only docs file it can produce is the generated CLI-reference **partial**, and only once a
docs site exists.

**No terminal UI.** `ui: tui` is not offered for Swift: the only Swift TUI library, SwiftTUI, has had no release or
commit since its 0.1.0 tag (2024), so a full-screen interface would rest on an unmaintained dependency. Styled,
TTY-aware output (bold/red/yellow behind the colour policy) is still scaffolded. If the user needs a full-screen TUI,
recommend the Rust (Ratatui) or Go (Bubble Tea) scaffold via `iru-setup-cli-repository`.

Sources: irurueta docs: ai/cli-for-agents/frameworks-swift-and-dotnet.adoc (swift-argument-parser, the 64 → 2
override, `--experimental-dump-help`, SwiftTUI's status), streams-and-exit-codes.adoc, tty-colour-and-interactivity.adoc,
machine-readable-output.adoc, self-describing-help.adoc (the `schema` shape), testing-clis.adoc (black-box tests on
the built executable), documenting-clis.adoc (generated man page and reference), packaging-and-distribution.adoc,
safety-and-idempotency.adoc, agent-readiness-checklist.adoc (https://www.irurueta.com/ai/cli-for-agents/index.html);
irurueta docs: apps/apple/testing-with-swift-testing.adoc (Swift Testing conventions) — plus the official
swift-argument-parser documentation and sources (`ParsableCommand.main`, `exitCode(for:)`, `fullMessage(for:)`,
`completionScript(for:)`, the `GenerateManual` plugin), the SwiftPM documentation, swift.org's Static Linux SDK
guide, and NO_COLOR (no-color.org). The shared contract text is
`iru-swift-code-one-task/reference/cli-contract.md`.

## Reference files — read only what this run needs

| Read | When |
|---|---|
| `reference/package-templates.md` | **Always.** Template conventions and placeholders, the `render-templates.py` helper, `Package.swift`, `.swift-format`, `.swiftlint.yml`, `scripts/generate-docs.sh`, `sonar-project.properties` (sonar). |
| `reference/kit-templates.md` | **Always.** `Sources/<Bin>Kit/` — the contract implementation and the `greet` logic, with a file → role table. |
| `reference/command-templates.md` | **Always.** `Sources/<Bin>/` — the root command and the three subcommands. |
| `reference/test-templates.md` | **Always.** `Tests/<Bin>KitTests/` and `Tests/<Bin>CLITests/`. |

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-swift-cli`) or by `iru-setup-cli-repository` / the `iru-setup-repository` front
door, which pass resolved answers as `key: value` lines, e.g.:

```
bin-name: greeter
package-name: greeter
description: Greets people from the command line.
swift-version: 6.0
platforms: macos=15.0
owner: example-org
license: Apache License 2.0
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
open-source: yes
visibility: public
ci: yes
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_greeter
sonar-host-url: https://sonarcloud.io
distribution: store
mode: new
on-existing: ask
```

Recognized keys:

- `bin-name` — the executable name, `^[a-z][a-z0-9-]*$` (e.g. `greeter`, `my-tool`). Derived from it, never asked:
  `<Bin>` = PascalCase (each `-`-separated word capitalized: `my-tool` → `MyTool`), the module prefix of
  `Sources/<Bin>/`, `Sources/<Bin>Kit/`, `Tests/<Bin>KitTests/`, `Tests/<Bin>CLITests/` and the root type
  `<Bin>Command`; and the environment prefix `<BIN>_` (upper-cased, `-` → `_`: `MY_TOOL_`). Reject a `bin-name` whose
  `<Bin>` would be `Kit`, collide with a Swift standard module (`Foundation`, `Testing`, `ArgumentParser`, …) or
  start with a digit.
- `package-name` — the SwiftPM package identity in `Package(name:)` (default: `bin-name`).
- `description` — one sentence; the root command's `abstract`, so it is also the man page's `NAME` line.
- `swift-version` — the `swift-tools-version` floor (default `6.0`, the minimum for `swiftLanguageModes:`); must be
  ≤ the installed toolchain (`swift --version`).
- `platforms` — `macos=<major.minor>` (default `15.0`; **15.0 is the floor**: the Kit uses `Synchronization.Mutex`).
  Linux needs no manifest entry and is always supported; a value naming another Apple platform is reported and
  ignored (a command-line tool runs on macOS and Linux only). Windows is not a target (Step 8's quirks say why).
- `owner` — the GitHub owner (default: parsed from `origin`, Step 3); only feeds the Sonar defaults.
- `license` (display name, SPDX expression, or `none`), `developer-name`, `developer-email`, `organization-url` — the
  license header prepended to every generated `.swift` file and SwiftLint's `file_header` rule.
- `open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal` — `internal` counts as `private`), `ci`
  (`yes`/`no`) — they only key Step 2's `sonar` recommendation.
- `sonar` (`cloud`/`self-hosted`/`none`) plus, when not `none`, `sonar-organization`/`sonar-project-key`/
  `sonar-host-url` — gate `sonar-project.properties`.
- `distribution` (`none`/`internal`/`store`) — recorded for the report only; no scaffold file depends on it (the
  release archives, Homebrew formula and attestations belong to `iru-setup-cli-github-workflows`).
- `mode` (`new`/`existing`) and `on-existing` (`ask`/`keep`/`update`/`replace`, default `ask`).

Every key found is resolved — skip its question in Step 2. Unknown keys from the shared vocabulary (`ui`, `channels`,
`branching`, `ci-tests`, `pages`, `cross-os-ci`, `publish`, `integration-branch`, `stable-branch`, …) are ignored and
named in the report; `ui: tui` additionally gets the "no terminal UI" explanation above.

`mode: existing` never means "gap-fill silently": Step 1 still warns about, and asks about, every pre-existing file
group. Only `on-existing` skips that question (`keep` = create only missing files; `update`/`replace` applied to every
existing group; the warning is still printed). Orchestrators forward `on-existing` only when their own `args`
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

Check for every file Step 6 would write: `Package.swift`, `Package.resolved`, `Sources/**`, `Tests/**`,
`.swift-format`, `.swiftlint.yml`, `scripts/generate-docs.sh`, `Sources/*/*.docc/`, `sonar-project.properties`. Then
tell the user which of the three this run is doing:

- **Scaffolding from scratch** — none exist: go to Step 2.
- **Updating an existing Swift CLI** — `Package.swift` declares an `.executableTarget` depending on
  `ArgumentParser` plus a `<Bin>Kit`-style library target (this skill's layout): read the current `bin-name` (the
  `.executable` product name), `<Bin>`, package name, tools-version, `.macOS` floor and `toolVersion` and offer them
  as Step 2's defaults; warn, listing every file found by path, that each existing file group is decided
  individually (missing files are still created). Groups (only those with a file present): **manifest**
  (`Package.swift`), **quality config** (`.swift-format`, `.swiftlint.yml`), **docs generator**
  (`scripts/generate-docs.sh`), **Sonar config** (`sonar-project.properties`), **DocC catalog**, and **the source
  skeleton** (every `.swift` file under `Sources/` and `Tests/`). Unless `on-existing` decides, ask with
  `AskUserQuestion`, one question per group (batch up to 4 per call), naming each concrete conflict with this run's
  choices (e.g. "`Package.swift` declares `swift-tools-version: 5.9`, too old for `swiftLanguageModes:`", "the
  `.macOS` floor is 13 but the Kit needs 15", "`sonar-project.properties` exists but you chose `sonar: none`",
  "`.swiftlint.yml` enables `trailing_comma`, which fights `swift format`"):
  - **Update (Recommended for the manifest, quality config, docs generator and Sonar config)** — "Merge: add what's
    missing and correct outdated parts using this skill's template as reference — dependencies and their versions,
    the Kit/test targets, `swiftLanguageModes`, the `.macOS` floor, SwiftLint/swift-format rules — keeping every
    extra target, dependency, product and setting this skill doesn't own. You review a diff; customizations survive,
    but a part this skill owns may be rewritten." For the source skeleton and DocC catalog, Update only creates
    missing files.
  - **Keep as is (Recommended for the source skeleton and DocC catalog)** — "Leave the file(s) untouched. Nothing you
    customized changes, but they may stay out of date or disagree with this run's choices — the report lists each
    mismatch."
  - **Replace** — "Regenerate from this skill's template. Matches the house pattern exactly, but every customization
    is lost (recoverable only from git history)." Never the default. Even on Replace, never overwrite a `.swift` file
    unless its content exactly matches this skill's rendered template (it is still the untouched sample).
  - **Stop** (first question only) — "End this skill now without changing any file." Report and end.
- **A foreign layout** — a `Package.swift` that is a library-only package, an app (`project.yml`/`*.xcodeproj`), or an
  executable target with all its logic inline (no Kit library), or a non-ArgumentParser CLI: this is not this skill's
  scaffold. Warn explicitly and ask (`AskUserQuestion`) whether to add only the pieces that don't touch existing
  targets (quality config, docs generator, Sonar config — each still per-group Update/Keep/Replace) or stop. Never
  move logic into a Kit target or rewrite an existing command tree here — that is a coding task
  (`iru-swift-code-one-task`).

## Step 2 — Collect the required inputs

For anything Step 0 didn't resolve, ask directly (plain conversation, pre-filled from Step 1 when updating):
**bin-name**, **description**, developer name/email/organization URL; offer `package-name` = `bin-name`,
`swift-version` = `6.0` and `macos=15.0` as defaults the user can accept in one answer.

Then, with `AskUserQuestion` (skip any resolved):

- **license** — Apache License 2.0 (Recommended) / MIT License / No license (proprietary) / Other (ask for the name
  and URL). If one is chosen, remind the user in Step 8 to add a root `LICENSE` (`iru-check-license` can verify
  headers against it).
- **open-source** and **sonar** — asked stand-alone only (an orchestrator resolves them): ask `open-source` first;
  recommend `sonar: cloud` only when open source **and** `visibility` is `public` (SonarCloud is free only for
  public/open-source projects), otherwise `none` (or `self-hosted`, a server you run). With `ci: no`, say that no
  workflow would send reports and recommend `none`. For `cloud`, default `sonar-organization` to `<owner>-github`,
  `sonar-project-key` to `<owner>_<repo>` and `sonar-host-url` to `https://sonarcloud.io`, confirming them; for
  `self-hosted`, ask for the host URL and key (organization only if the server has organizations).
- **distribution** — not asked here; recorded when `args` supplied it.

## Step 3 — Infer repository information

Parse `git remote get-url origin` (`git@host:owner/repo.git` or `https://host/owner/repo.git`) for `<owner>`/`<repo>`
(Sonar defaults); no `origin` and Sonar wanted → ask. The license header's year is the current year.

## Step 4 — Look up versions and check the toolchain

Look every version up at run time; fall back to this table (looked up and verified working **together** on
2026-10-16) only when a lookup fails, and say so in Step 8. After adopting a newer version, run Step 7 before
trusting it.

| Component | Lookup | 2026-10-16 fallback |
|---|---|---|
| swift-argument-parser | `gh api repos/apple/swift-argument-parser/releases/latest -q .tag_name` (or `curl -fsSL https://api.github.com/repos/apple/swift-argument-parser/releases/latest`) | `1.8.2` (released 2026-06-04) |
| swift-docc-plugin | same, `repos/swiftlang/swift-docc-plugin` | `1.5.0` |
| Swift toolchain | `swift --version` — must be ≥ `swift-version` (never install one) | Swift 6.4 (Xcode 27) verified |

## Step 5 — Render the templates

Read the four reference files. Extract `render-templates.py` from `reference/package-templates.md` into a scratch
directory **outside** the repository, write `<scratch>/values.json`:

| Key | Value |
|---|---|
| `Bin`, `bin`, `BIN_ENV` | Step 0's derivation (`MyTool`, `my-tool`, `MY_TOOL_`) |
| `PackageName`, `Description` | Step 0/2 (the renderer escapes `"`/`\` for Swift) |
| `ToolsVersion` | `swift-version` (default `6.0`) |
| `MacOSVersion` | the `macos=` value as `major.minor` (default `15.0`) |
| `ArgumentParserVersion`, `DoccPluginVersion` | Step 4 |
| `SonarProjectKey`, `SonarOrganization`, `SonarHostUrl` | Step 2 (empty strings when `sonar: none`) |
| `LicenseHeader` | the header below, or `""` for "No license" |
| `conditions` | `license` (unless "No license"), `sonar` (unless `none`), `sonar-organization` (when an organization is written) |

```
//
// Copyright (C) <current year> <developer-name>
//
// Licensed under the <license name> (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//         <license url>
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
```

When the repository already has a header convention (`iru-check-license` would learn it), use that text instead.
Then run `python3 -I <scratch>/render-templates.py <this skill's reference dir> <scratch>/staging <scratch>/values.json`.
It stops on an unresolved placeholder or an unbalanced marker — fix the values, never the output by hand. Layout
produced (`[sonar]` marks a conditional file):

```
Package.swift  .swift-format  .swiftlint.yml  sonar-project.properties [sonar]
scripts/generate-docs.sh
Sources/<Bin>/{<Bin>Command,GreetCommand,CompletionCommand,SchemaCommand}.swift
Sources/<Bin>Kit/{Version,Tool,CLIExitCode,CLIError,JSONValue,Output,Terminal,Platform,Streams,GlobalOptions,
                  CommandContext,SignalTrap,CommandRunner,Greeting,CommandSchema,SchemaAction}.swift
Sources/<Bin>Kit/<Bin>Kit.docc/<Bin>Kit.md
Tests/<Bin>KitTests/{TestSupport,ExitCodeAndErrorTests,OutputTests,TerminalTests,StreamTests,SessionTests,
                     GreetingTests,CommandRunnerTests,SchemaTests,SignalTrapTests}.swift
Tests/<Bin>CLITests/{ToolProcess,CLITests}.swift
```

Configuration precedence (contract §6) is implemented for the environment layer only (`<BIN>_NO_INPUT`, plus
`NO_COLOR`/`FORCE_COLOR`/`CI`); a config file (`<BIN>_CONFIG`, `$XDG_CONFIG_HOME/<bin>/config.toml`) is left as the
documented extension point because Foundation has no TOML parser and the scaffold adds no dependency for it — say so
in the report. No authentication is scaffolded (`<BIN>_TOKEN` appears only in the exit-code 7 default hint).

## Step 6 — Write the files

Copy from the staging directory into the repository, applying Step 1's per-group decision to every file that already
exists (Keep as is → skip; Update → merge after showing `git diff --no-index <current> <staged>`; Replace → overwrite
within Step 1's source-file limit). Files that didn't exist are always written. Keep `scripts/generate-docs.sh`
executable. Never write `.gitignore`, `LICENSE`, `README.md`, `CHANGELOG.md`, workflows or `docs/antora.yml`.
The scratch directory stays outside the repository and is never copied into it.

## Step 7 — Verify

Run through the `iru-gate-runner` agent (never inline — the logs are long); warn first that the first build fetches
swift-argument-parser and swift-docc-plugin (+ swift-docc-symbolkit) from GitHub. On macOS, in order:

1. `swift build` — 0 warnings expected.
2. `swift test --enable-code-coverage` — both targets pass (61 Kit + 18 CLI tests as scaffolded).
3. Coverage: `iru-swift-coverage` (package path) over the `Sources/<Bin>Kit/` and `Sources/<Bin>/` files, or
   directly, with `B=$(swift build --show-bin-path)`: `xcrun llvm-cov report $B/<Bin>KitTests.xctest/Contents/MacOS/<Bin>KitTests
   -object $B/<Bin>CLITests.xctest/Contents/MacOS/<Bin>CLITests -instr-profile $B/codecov/default.profdata
   --ignore-filename-regex='(Tests/|DerivedSources|\.build/)'` (on Linux the test binary is the single
   `<products>/<package-name>PackageTests.xctest` executable and `llvm-cov` is on `PATH` — unverified locally). The
   Kit's line % must be ≥ 80. Because `ToolProcess` forwards `LLVM_PROFILE_FILE`, the binaries the CLI tests spawn
   write their profiles into SwiftPM's coverage data, so `Sources/<Bin>/` is measured too (as scaffolded: Kit 98.3%,
   the four command files 100%; the Kit tests alone give 95.2%).
4. `swift format lint --strict --recursive Sources Tests Package.swift` — clean.
5. `swiftlint lint --strict` when `swiftlint` is installed (else "not installed — unverified", never "passed").
6. `swift package generate-documentation --target <Bin>Kit --warnings-as-errors` — no warnings.
7. `scripts/generate-docs.sh "$TMPDIR/<bin>-docs-check"` — man page, three completion scripts and `schema.json`
   written (plus the Antora partial when `docs/antora.yml` exists).
8. Contract smoke checks on `$(swift build --show-bin-path)/<bin>`: `--version` and `--help` exit 0 with output on
   stdout only; an unknown command exits **2**; `greet Ada --json | jq -e .schemaVersion`; `NO_COLOR=1 FORCE_COLOR=1
   <bin> greet Ada` contains no ESC byte; `greet ""` exits 3; `schema nope` exits 4.
9. Release build: `swift build -c release --arch arm64 --arch x86_64 --product <bin>` then `lipo -archs` on
   `$(swift build -c release --arch arm64 --arch x86_64 --show-bin-path)/<bin>` → `x86_64 arm64`; optionally re-run
   the CLI suite against it with `<BIN>_TEST_BINARY=<that path> swift test --filter <Bin>CLITests`.

On a Linux host steps 1–8 apply (llvm-cov path above, no `lipo`/universal build); report what couldn't run as
"unverified", never "passed". Quote error output verbatim for a failure only.

## Step 8 — Report

Summarize: resolved `bin-name`/`<Bin>`/env prefix, `package-name`, `description`, tools-version, macOS floor,
`toolVersion` (`0.1.0-dev`), license (or none), which Step 4 versions were live versus fallback, and whether the run
scaffolded from scratch, updated an existing package, or stopped. Then, per Step 1 group, the action taken —
**created / updated / replaced / kept as is** — and whether it came from the user or `on-existing`, listing each
mismatch of a kept group and, for a replaced one, what customizations could have been lost (check `git diff`). State
included versus omitted and why: no TUI (and why), `sonar` (`sonar-project.properties` written or not; with `ci: no`
nothing sends reports), `distribution` (recorded only), the config-file extension point, ignored `args` keys, and the
pass/fail/unverified result of every Step 7 command. List the docs pages worth adding once `iru-setup-antora` has
run: usage, exit codes, JSON output schema (`greet` + the error envelope), using the tool from an agent (`schema`,
`--json`, `--no-input`), and a `cli-reference.adoc` page that `include::partial$cli-reference.adoc[]`.

### Scaffold contract (confirmed by running it — downstream skills depend on these)

| What | Exact name / path |
|---|---|
| Detection | `Package.swift` with an `.executableTarget` depending on `ArgumentParser`; product `.executable(name: "<bin>", targets: ["<Bin>"])` |
| Targets | `<Bin>` (executable, thin), `<Bin>Kit` (library: all logic; depends on ArgumentParser), `<Bin>KitTests` (Swift Testing, in-process), `<Bin>CLITests` (Swift Testing, runs the binary; depends on the executable target so `swift test` builds it) |
| Version | `Sources/<Bin>Kit/Version.swift`: `public let toolVersion = "x.y.z[-dev]"` (`0.1.0-dev` in-tree); the root's `CommandConfiguration(version: toolVersion)` reads it — no second literal |
| Build | `swift build` (debug), `swift build -c release --product <bin>`; binary at `$(swift build [-c release] --show-bin-path)/<bin>` (`.build/out/Products/{Debug,Release}` with Swift 6.4's default build system on macOS; `.build/debug` stays a symlink) |
| Tests | `swift test` (both targets); `swift test --filter <Bin>KitTests` / `--filter <Bin>CLITests`; `<BIN>_TEST_BINARY=<path>` runs the CLI suite against any built or packaged binary. No simulator, no lock, no containers |
| Coverage | `swift test --enable-code-coverage`; `llvm-cov` on `<products>/<Bin>KitTests.xctest/Contents/MacOS/<Bin>KitTests` plus `-object <products>/<Bin>CLITests.xctest/Contents/MacOS/<Bin>CLITests` (macOS) with `<products>/codecov/default.profdata`, `--ignore-filename-regex='(Tests/\|DerivedSources\|\.build/)'`; the 80% bar applies to `Sources/<Bin>Kit/`; `Sources/<Bin>/` is measured through the spawned binaries (`LLVM_PROFILE_FILE` forwarded) |
| Format / lint | `swift format lint --strict --recursive Sources Tests Package.swift`; `swiftlint lint --strict` (`.swiftlint.yml`; `trailing_comma` off) |
| DocC | `swift package generate-documentation --target <Bin>Kit [--warnings-as-errors]` → `.build/plugins/Swift-DocC/outputs/<Bin>Kit.doccarchive`; static hosting: add `--transform-for-static-hosting --output-path <dir>` (and `--allow-writing-to-directory <dir>`) |
| Man page | `swift package plugin generate-manual [--date YYYY-MM-DD] [--multi-page]` → `.build/plugins/GenerateManual/outputs/<Bin>/<bin>.1` (builds release first) |
| Docs generator | `scripts/generate-docs.sh [out-dir]` (default `dist`) → `<out>/man/<bin>.1`, `<out>/completions/{<bin>.bash,_<bin>,<bin>.fish}`, `<out>/schema.json`, and `docs/modules/ROOT/partials/cli-reference.adoc` when `docs/antora.yml` exists |
| Self-description | `<bin> schema [COMMAND]` (JSON tree: `schemaVersion`, `name`, `version`, `globalFlags`, `commands[]` with `args`, `flags`, `exitCodes`, `safety`; `exitCodes` table), `<bin> schema --asciidoc`, `<bin> completion bash\|zsh\|fish`, `<bin> --version`, `<bin> --experimental-dump-help` |
| Exit codes | `CLIExitCode` in `Sources/<Bin>Kit/CLIExitCode.swift`: 0 OK, 1 INTERNAL, 2 USAGE, 3 VALIDATION, 4 NOT_FOUND, 5 CONFIRMATION_REQUIRED, 6 RETRYABLE, 7 AUTH, 130, 143 |
| Release (macOS) | `swift build -c release --arch arm64 --arch x86_64 --product <bin>` → universal binary (verified) |
| Release (Linux) | `swift build -c release --product <bin> --swift-sdk <arch>-swift-linux-musl` with the Static Linux SDK (swift.org toolchain on a Linux runner; **unverified locally**), or `--static-swift-stdlib` on glibc |

### Known quirks / verification notes

- **Verified for real on 2026-10-16** (Swift 6.4 / Xcode 27, macOS 27 arm64) in
  `$TMPDIR/iru-verify/cli/swift/iru-setup-swift-cli/` from templates rendered by `render-templates.py`: `render1`/`final`
  (`bin-name: my-tool` → `MyTool`/`MY_TOOL_`, a description containing quotes, Apache-2.0 header, `sonar: cloud`) and
  `render2` (`greeter`, no license, no Sonar, `macos=26.0`). Results: `swift build` 0 warnings; 61 Kit tests + 18 CLI
  tests passed; line coverage over the full suite **98.31%** for the Kit (95.17% from the Kit tests alone) and 100%
  for the four command files, with no stray `default.profraw`; `swift format lint --strict` clean; SwiftLint 0.65.1
  `--strict` 0 violations (and `file_header` fires on a header-less file); DocC `--warnings-as-errors` clean;
  `scripts/generate-docs.sh` produced the man page, three completions, `schema.json` and the Antora partial;
  smoke checks — `--help`/`--version` exit 0 on stdout, unknown command **2**, `greet ""` 3, `schema nope` 4,
  SIGINT 130 / SIGTERM 143 with one stderr line, closed stdout exit 0 with empty stderr, `jq -e .schemaVersion`
  true, no ESC byte with `NO_COLOR`; universal release binary `x86_64 arm64`, and the CLI suite passed against it via
  `MY_TOOL_TEST_BINARY`.
- **swift-argument-parser exits 64 on a usage error by default** (confirmed: a missing argument printed
  `Error: …`/`Usage: …` and exited 64). `CommandRunner` replaces `main()`: `exitCode(for:) == .validationFailure` → 2,
  `.success` (help, version, dump-help) → the `fullMessage` on **stdout**, a thrown `ExitCode(n)` passes through
  silently, anything else → 1 with an envelope. Errors thrown from `validate()` should be `ValidationError` (→ 2);
  operand problems are thrown from `run()` as `CLIError(.validation, …)` (→ 3).
- **`--experimental-dump-help` is captured in-process** by parsing `["--experimental-dump-help"]` and reading
  `fullMessage(for:)` of the thrown error; the dump's shape is upstream-experimental, so `CommandSchema` decodes only
  the fields it needs and ignores the rest. swift-argument-parser's `ArgumentParserToolInfo` (the typed `ToolInfoV0`)
  is **not** a public product, hence the private decoder. The synthesized `help` subcommand is filtered out.
- **Completion shells**: swift-argument-parser generates bash, zsh and fish only (`CompletionShell`); PowerShell is
  not supported, so `completion powershell` is a usage error (2). `CompletionShell` isn't `ExpressibleByArgument`, so
  the Kit maps its own `CompletionShellName` enum onto it. The built-in `--generate-completion-script <shell>` flag
  still works too.
- **Locating the binary from the CLI tests**: under `swift test` on macOS, Swift Testing runs through
  `swiftpm-testing-helper`, so `Bundle.main` and `Bundle.allBundles` point at the toolchain — `Bundle(for:)` on a
  class defined in the test target gives `<products>/<Bin>CLITests.xctest`, whose parent holds `<bin>`. On Linux the
  runner is `<products>/<package>PackageTests.xctest`, so `CommandLine.arguments[0]`'s directory is used
  (**unverified locally**, see below). `<BIN>_TEST_BINARY` overrides both.
- **Child processes in tests** write stdout/stderr to temporary files (no pipe-buffer deadlock); only the EPIPE and
  signal tests use pipes. The environment is reset to `PATH`/`LANG` so a developer's `NO_COLOR`/`CI` can't leak in —
  **but `LLVM_PROFILE_FILE` is forwarded**: without it, every instrumented child of a `swift test
  --enable-code-coverage` run wrote a stray `default.profraw` into the package root (observed), and the executable
  target showed no coverage; with it, SwiftPM merges the children's profiles (`Sources/<Bin>/` 100%).
- **`swift format` vs SwiftLint**: `swift format` adds trailing commas that SwiftLint's default `trailing_comma`
  forbids — the template disables `trailing_comma`. `file_header` is an opt-in rule (configuring it without listing
  it only warns). `unused_import` belongs under `analyzer_rules`. (The same three points apply to
  `iru-setup-swift-library`'s `.swiftlint.yml`, whose SwiftLint config was never run.)
- **`.macOS("15.0")` string form**: a named case like `.v26` fails with `'v26' is unavailable` under
  `swift-tools-version: 6.0`; the string form works for every version.
- **The man page date is localized by the macOS user locale** (`.Dd octubre 16, 2026` on a Spanish-locale Mac, even
  with `LC_ALL=C`); CI runners (English) produce `October`. `--date` fixes the day, not the month name.
- **`Synchronization.Mutex` sets the macOS 15 floor**; a `Mutex` is non-copyable, so closures capture a small
  `final class` wrapper (the signal counter), never the `Mutex` itself.
- **Unverified locally**: Linux builds and tests (the Docker VM had no free disk for the `swift:6.4-noble` image and
  nothing of the user's was pruned to make room), the Static Linux SDK (`swift sdk install …`, needs the swift.org
  toolchain — Xcode's toolchain can't use it), musl-specific behaviour of `Platform.swift`, Developer ID signing and
  notarization of the binary, and Homebrew distribution. **Windows is not a target**: `Platform.swift` has no
  `#if os(Windows)` branch (ucrt `_isatty`/`_write`, no SIGTERM delivery to a console app), so the release matrix
  ships macOS and Linux only.

Finish with a **Warn explicitly** block:

- Review every generated file before building or committing; replace the `greet` sample (and its tests) with the
  tool's real commands, keeping each new command a `DescribedCommand` with honest `metadata` (safety + exit codes).
- Run `iru-setup-swift-gitignore` with `flavor: cli` — `.build/`, the generator outputs (`dist/`, `build/`) and
  release archives must never be committed, and a CLI commits `Package.resolved`.
- Keep `toolVersion` a single string literal in `Version.swift` — `iru-swift-bump-version` and the release workflow
  rely on it; never renumber `CLIExitCode`.
- With `sonar` ≠ `none`, a `SONAR_TOKEN` secret, the Sonar project, and a CI step producing
  `sonarqube-generic-coverage.xml`/`swiftlint.json` must exist before analysis reports anything.
- The swift-argument-parser and swift-docc-plugin versions were resolved at run time (or from the fallback) — re-check
  before a first release.
