---
id: agents
description: "Imported from AGENTS.md"
activation: agent
---

# AGENTS.md

Guidance for AI coding agents working on the **adeptability** (`adept`) codebase.
Humans: see [README.md](README.md) for usage and [CONTRIBUTING.md](CONTRIBUTING.md) for the contributor workflow.

## Project Overview

`adept` is a single-binary Go CLI for **cross-harness AI skill portability**: you author a
skill once in a canonical format and `adept` renders it accurately into every AI coding
harness in your project — Claude Code, Cursor, Codex, GitHub Copilot, OpenCode, and any
config-driven adapter you register — then keeps the two sides in sync in both directions.

- **Language:** Go 1.25, [Cobra](https://github.com/spf13/cobra) command surface.
- **Module:** `github.com/itaywol/adeptability`. Binary: `adept` (entrypoint `cmd/adept`).
- **No runtime services.** Everything is local filesystem + `git` + optional network
  (GitHub API, skills.sh, an LLM provider for the optional intent pass).
- **Source of truth is the filesystem.** Content hashes — not version numbers — drive every
  sync decision. There is no central database.

## Commands

User-facing CLI (five verbs + three subcommand groups):

| Command | Description |
| --- | --- |
| `adept init [--from <url>] [--ref <branch>] [--name <local>] [--mode symlink\|copy]` | Scaffold `.adeptability/`, optionally clone a library, adopt existing harness files |
| `adept status` | Project state at a glance: init, libraries, harnesses, drift |
| `adept sync [--harness <id>] [--force] [--dry-run]` | Push canonical skills → every enabled harness |
| `adept sync-from [--harness <id>] [--all] [--force] [--dry-run]` | Adopt harness-side edits back into canonical |
| `adept diff [--harness <id>]` | Show drift between canonical and rendered output |
| `adept harness {add\|remove\|list}` | Manage enabled harnesses |
| `adept skill {add\|install\|update\|info\|search\|check\|edit\|remove\|list}` | Manage canonical skills (local + skills.sh/GitHub) |
| `adept library {add\|remove\|list}` | Manage remote skill-library remotes |
| `adept config {list\|get\|set\|unset\|llm ...}` | Strict-typed project config |

Global flags: `--json`, `--log-level debug|info|warn|error`, `--project <path>`, `--library <path>`.
Run `adept <cmd> --help` for the authoritative, always-up-to-date surface.

## Architecture

```
cmd/adept/            main(): injects build info, calls cli.NewRoot, maps errors→exit codes
internal/cli/         Cobra composition root. One file per command group. NO package state.
pkg/adept/            STABLE public types + interfaces + sentinel errors (no behavior here)
pkg/adeptschema/      embedded JSON Schemas (skill / adapter / org / config) for validation
internal/canonical/   parse skill.yaml & SKILL.md frontmatter → *adept.Skill, schema-validate
internal/render/<h>/  one package per built-in harness: Renderer + Import (reverse render)
internal/adapter/     config-driven (YAML) harness adapters: load, validate, synthesize
internal/harness/     orchestrator: sync / sync-from / drift detection across all harnesses
internal/merge/       3-way merge + diff3 for sync-from conflict handling
internal/library/     centralized + multi-library skill resolution (first-wins on collision)
internal/scan/        static safety scanner (+ optional LLM intent pass)
internal/registry/    github (trees API) + skillssh (skills.sh catalog) clients
internal/git/         git clone/pull/checkout-at-SHA wrapper
internal/{fsutil,locks,hash,config,project,log,budget,org}/  supporting primitives
```

### Core invariants — do not break these

1. **`pkg/adept` holds types, not behavior.** It must stay dependency-light (import-free
   where possible — e.g. `SkillIDPattern` is a string, compiled in `internal/canonical`).
   In-process consumers (tests, future LSP/plugins) depend on it; keep it stable.
2. **Composition root, no globals.** `cli.NewRoot` wires every concrete implementation
   behind an interface into a `*Deps` container. No package-level state, no `init()` side
   effects. Every command takes its dependencies explicitly so it can be unit-tested with
   mocks. Add a new dependency by extending `Deps`, not by reaching for a singleton.
3. **Identity is `(id, content-hash)`.** Skills carry no version field; the hash is the
   answer to "did this change". Do not introduce version numbers as a sync signal.
4. **Canonical layout:** a skill is a directory `<root>/skills/<id>/` with one `SKILL.md`
   (YAML frontmatter + markdown body) plus optional sidecars (`scripts/`, `references/`,
   `assets/`). The directory name is the authoritative id. Skill ids use the
   harness-compatible charset `^[a-z0-9](?:[a-z0-9-]{0,48}[a-z0-9])?$` (no underscore).
   Per-skill, per-harness overrides live in an optional `harness:` map (keyed by harness id)
   plus a promoted `model` field; renderers merge their entry last via `common.MergeOverride`,
   and the schema forbids overriding identity fields. Currently consumed by claude-code and cursor.
5. **Harness models differ — renderers must respect them:** per-skill (Claude, OpenCode),
   single-file (Cursor — drops sidecars), and aggregator (Codex/Copilot — concatenate into
   one file with section markers under a byte budget). Aggregators must parse their own
   markers on `Import` and degrade to a single synthesized skill when markers are absent.
6. **Secrets never touch disk.** `config.json` records *which* LLM provider/model is used;
   API keys are resolved from the environment (`ANTHROPIC_API_KEY`) at call time only.

### Exit codes (see `cli.ExitFromError`)

- `0` clean · `1` generic error · `2` dirty/drift (`ErrDirty`) or merge conflict (`ErrMergeConflict`).
- Safety scan worst-severity maps to the same scheme: `clean`/`low`/`medium` → 0, `high` → 1, `critical` → 2.

## Key Integration Points

- **`pkg/adept`** — `HarnessAdapter`, `Renderer`, `Skill`, `RenderOutput`, `DriftReport`,
  `ImportedSkill`, sentinel errors (`ErrSkillNotFound`, `ErrMergeConflict`, …), on-disk
  layout constants (`BaseDirName`, `SkillsDirName`, …). Start here to understand contracts.
- **`pkg/adeptschema/*.schema.json`** — embedded JSON Schemas. Changing a canonical field
  means updating the schema *and* the Go struct tags in `pkg/adept` together.
- **`internal/cli/deps.go`** — the `Deps` wiring. New commands are constructed from `Deps`.
- **`testdata/` golden fixtures** under each `internal/render/<h>/` package pin exact output.

## Development

```bash
go build ./...                 # build everything
go build -o /tmp/adept ./cmd/adept   # build the binary
go test ./...                  # fast tests
go test -race ./...            # race detector (CI gate)
go test -run E2E ./cmd/adept   # end-to-end (builds the binary, drives real commands)
go vet ./...
gofmt -l .                     # must print nothing
golangci-lint run              # config in .golangci.yml
```

### Dogfooding

This repo is itself an adept skill library — committed skills live in `skills/`, and the
project-canonical layout (`.adeptability/`, `.claude/`) is **regenerated on demand and
gitignored**. To regenerate and verify rendering locally:

```bash
adept init --from "$(git rev-parse --show-toplevel)" --name adept --mode copy
adept harness add claude-code
adept sync
adept status
```

## Code Style

- **Formatting:** `gofmt` + `goimports`. CI fails on any unformatted file — run `gofmt -w .`
  before committing. There is no separate formatter to learn.
- **Linting:** `.golangci.yml` enables `errcheck`, `staticcheck`, `govet`, `gocritic`,
  `revive` (exported symbols need doc comments), `errorlint`, `nilerr`, `bodyclose`,
  `prealloc`, `unconvert`, `misspell`, and more. Run `golangci-lint run` locally.
- **Errors:** wrap with context — `fmt.Errorf("doing X: %w", err)`. Compare with
  `errors.Is` against the sentinels in `pkg/adept/errors.go`; add a new sentinel there
  rather than matching on error strings. Never silently drop an error that loses data.
- **Naming & shape:** small, single-responsibility functions; prefer early returns over
  deep nesting; doc comments on every exported symbol (full sentences, starting with the
  symbol name).
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/). Release-please
  derives the next semver from the types (`feat` → minor, `fix`/`perf` → patch,
  `feat!`/`BREAKING CHANGE:` → major; `refactor`/`docs`/`chore`/`test`/`ci` → no bump).

## Testing

- **Table-driven tests** are the default. Use `testify/require` for assertions.
- **Golden fixtures** live in `testdata/` beside each renderer; they pin exact rendered
  bytes. When you intentionally change output, update the fixture in the same commit and
  explain why in the message.
- **E2E** (`cmd/adept/*_test.go`) builds the real binary and drives commands against temp
  dirs with an isolated `HOME` and `ADEPT_LIBRARY`. Guard slow paths with
  `if testing.Short()`.
- **Coverage gates:** keep `internal/render`, `internal/status`, `internal/budget`, and
  `internal/canonical` at ≥80%. Tests should catch regressions, not pad coverage.

## Adding a harness

**Built-in (Go) adapter** — for harnesses needing custom logic:

1. Implement `adept.HarnessAdapter` in `internal/render/<id>/`.
2. Add golden fixtures under that package's `testdata/`.
3. Register it in `internal/cli/deps.go` (`registerBuiltinAdapters`).
4. Document it in the README harness table.

**Config-driven adapter** — for harnesses expressible declaratively (no code, no rebuild):

Drop a `<id>.yaml` adapter in `~/.adeptability/adapters/` matching
`pkg/adeptschema/adapter.schema.json` (`kind` = `per-skill` | `aggregator-single` |
`aggregator-per-glob`, plus `output`, `frontmatter`, `body`, `detect`, `import` hints).

## Publishing

- **Versioning:** `release-please` opens/maintains a release PR from Conventional Commits;
  merging it tags `vX.Y.Z`.
- **Release:** the tag triggers `goreleaser` (cross-compiled archives for darwin/linux/windows
  × amd64/arm64), `checksums.txt`, cosign signing, and build-provenance attestation via
  `actions/attest-build-provenance` (immutable-release safe). Docker publish to GHCR is opt-in
  via the `DOCKER_PUBLISH` repo variable.
- **Distribution (live):** GitHub release tarballs, `go install`, the `scripts/install.sh`
  curl installer, Homebrew tap (`itaywol/homebrew-tap`), and GHCR images.
- **Distribution (not wired yet):** Scoop, WinGet, and the npm wrapper (`scripts/npm/`,
  `@itaywol/adeptability`) are unpublished — tracked in the "additional package managers"
  issue, gated on a thumbs-up before we commit to maintaining them.
- Do not hand-edit `CHANGELOG.md`, `.release-please-manifest.json`, or version strings;
  release-please owns them.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **adeptability** (3310 symbols, 11238 relationships, 248 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/adeptability/context` | Codebase overview, check index freshness |
| `gitnexus://repo/adeptability/clusters` | All functional areas |
| `gitnexus://repo/adeptability/processes` | All execution flows |
| `gitnexus://repo/adeptability/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
