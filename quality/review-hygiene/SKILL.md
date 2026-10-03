---
name: review-hygiene
description: Use when the user wants the project's linter / formatter / LSP diagnostics run as a check-only pass that emits findings the orchestrator can dispatch as auto-fixes. Triggers on "/review-hygiene", "run the linter", "check formatting", "what does eslint say", "what does prettier complain about", "lint findings only", or any ask for the deterministic-tool view of code quality. Detects ESLint / Biome / Oxlint / Prettier / gofmt / go vet / ruff / black / clippy / rustfmt and runs them in check-only mode. Emits ONE aggregate finding per tool (covering all auto-fixable violations across all touched files) plus individual findings for anything the tool flagged as not-auto-fixable. Keeps the orchestrator's context tiny — instead of N violations being read into context, the aggregate finding tells fix-applier "run `prettier --write src/`", which executes deterministically. Companion to /review-code (which handles subjective design judgment that linters can't catch). Use /review-hygiene when you want the mechanical-quality verdict; use /drive-change to have the orchestrator dispatch the fixes (aggregate fixes run as a single tool invocation, individual fixes go through fix-applier per-finding).
allowed-tools: Bash(gh:*), Bash(git:*), Bash(npm:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(npx:*), Bash(eslint:*), Bash(prettier:*), Bash(biome:*), Bash(oxlint:*), Bash(ruff:*), Bash(black:*), Bash(gofmt:*), Bash(go:*), Bash(cargo:*), Bash(rustfmt:*), Bash(clippy-driver:*), Bash(just:*), Bash(make:*), Read, Grep, Glob, Skill
---

# review-hygiene — deterministic-tool audit on touched files

`/review-hygiene` runs the project's lint / format / LSP-diagnostic tools in check-only mode and converts the output into findings. Most of those findings are emitted as a single **aggregate finding per tool** with `fix: auto: <command>` — meaning the orchestrator can dispatch a fix-applier that just runs the command, no LLM editing involved. The agent context never sees the 200 individual violations; it sees `"230 prettier violations across 8 files"` and the command to fix them.

What's left over — violations the tool explicitly marked as not-auto-fixable, or rules that need human judgment — gets emitted as **individual findings** with concrete `fix:` lines.

This is the read-only twin of running a linter with `--fix`. To act on the findings, call `/drive-change`.

## Why this exists

When a 100-file diff has format drift everywhere, running each file through an LLM reviewer to emit "missing semicolon on line 23" 800 times is absurd. The linter already knows where every issue is, and the formatter already knows how to fix all of them. This skill keeps the LLM out of work the tools handle deterministically:

- The reviewer (this skill) runs each tool in check-mode, counts violations, emits one aggregate finding per tool.
- The merger sees `kind: aggregate`, partitions it as a separate packet, skips apply-validation (the tool re-runs in check-mode after the fix to validate).
- The fix-applier dispatches an aggregate packet by reading the `auto: <command>` from the `fix:` line and just running it. No `Read`, no `Edit`, no per-line decision.

Net effect: the orchestrator sees a `Hygiene: 230 violations auto-fixed across 8 files` line in the report instead of 230 paragraphs of finding blocks, and the fix-applier finishes in seconds instead of minutes.

## Phase 0 — Scope

Decide which files are in scope, in this priority order:

1. **PR context**: `gh pr diff --name-only` against the base branch.
2. **Working tree**: `git diff --name-only HEAD` for uncommitted work.
3. **An explicit list** passed by the user.

Exclude: lockfiles, generated files (`linguist-generated=true`, `dist/`, `build/`, `generated/`, `__generated__/`, `*.pb.*`), binary blobs, fixtures (`fixtures/`, `__fixtures__/`, `testdata/`), vendored code (`vendor/`, `third_party/`, `external/`).

## Phase 1 — Detect available toolchains

Probe what's installed. Don't fail on missing tools — flag them as P3 hygiene findings (`tooling: <tool> not installed; coverage gap`).

| Tool | Detection signal | Runs on |
| --- | --- | --- |
| **ESLint** | `eslint.config.*`, `.eslintrc*`, `package.json` script | `.ts/.tsx/.js/.jsx/.mjs/.cjs/.vue/.svelte` |
| **Biome** | `biome.json`, `biome.jsonc` | `.ts/.tsx/.js/.jsx/.json/.css` |
| **Oxlint** | `package.json` mention or `.oxlintrc*` | `.ts/.tsx/.js/.jsx` |
| **Prettier** | `.prettierrc*`, `prettier.config.*`, `package.json` mention | most JS/TS/CSS/Markdown |
| **gofmt** | `.go` files exist | `.go` |
| **go vet** | `go.mod` | `.go` |
| **Ruff** | `pyproject.toml [tool.ruff]`, `ruff.toml` | `.py` |
| **Black** | `pyproject.toml [tool.black]`, `.python-version` | `.py` |
| **rustfmt** | `Cargo.toml`, `rustfmt.toml` | `.rs` |
| **Clippy** | `Cargo.toml` | `.rs` |
| **tslsp diagnostics** | `mcp__tslsp__diagnostics` available | `.ts/.tsx/.js/.jsx` |

Prefer the project's own runner — `npm run lint` / `npm run format:check` / `just lint` / etc. — over a global `eslint`/`prettier` binary if the project ships one. If you can't tell what config the project uses, default to the global binary.

Detection gives you a list `available: [eslint, prettier, ruff, ...]`. Skip any tool whose detection signal isn't present.

## Phase 2 — Run each available tool in check-only mode

For each available tool, in parallel where possible. Capture:

- **Auto-fixable count** — violations the tool itself marks as fixable.
- **Not-auto-fixable count** — violations that need human edits.
- **Files touched** — the set of files in `Files` that the tool would modify.

### ESLint

```bash
npx eslint <files> --format json --no-error-on-unmatched-pattern
```

Parse the JSON. For each message, `fixable: true` → auto-fixable count; otherwise individual finding.

### Biome / Oxlint

Similar. Both emit JSON with a `fixable` flag.

### Prettier

```bash
npx prettier --check <files>
```

Prettier is binary — every file is either formatted or not. Treat every non-formatted file as 1 violation; the auto-fixable count is the number of unformatted files. Prettier never emits not-auto-fixable violations (the whole tool is `--write` or bust).

### gofmt

```bash
gofmt -l <files>
```

Same shape as prettier — lists files that need formatting. All auto-fixable.

### go vet

```bash
go vet ./<dirs>
```

`go vet` is diagnostic-only (no `--fix`). Every issue is a not-auto-fixable individual finding.

### Ruff / Black

```bash
ruff check <files> --format json
black --check <files>
```

Ruff has a `fix` flag per rule in its JSON. Black is binary like Prettier.

### rustfmt / Clippy

```bash
rustfmt --check <files>
cargo clippy --message-format json -- -D warnings
```

rustfmt is binary. Clippy reports `applicability: "MachineApplicable"` for auto-fixable, otherwise individual.

### tslsp diagnostics

```bash
mcp__tslsp__diagnostics <files>
```

LSP diagnostics have a `code` and severity (`error`/`warning`/`info`/`hint`). Treat `error` as P0 individual (real type errors), `warning` as P1 individual, `info`/`hint` as P3 individual. Diagnostics rarely auto-fix — emit them as individual findings.

## Phase 3 — Emit findings

For each tool that ran:

### Aggregate finding (for auto-fixable violations)

If the tool produced **any** auto-fixable violations, emit one aggregate finding:

```
[P2] [hygiene] <first-affected-file>:1 — 230 prettier auto-fixable violations across 8 files
why: prettier --check listed 230 issues, all marked auto-fixable; running `prettier --write` resolves them deterministically.
fix: auto: prettier --write <space-separated files_affected>
kind: aggregate
tool: prettier
files_affected: [<file paths>]
files_affected_count: 8
violations_count: 230
```

Severity is **P2** by default for aggregates. Reason: format violations don't block merge on their own, even at 230 of them — they're noise. Bump to P1 if the lint config the user committed has rules they presumably care about flagging on the diff itself.

The `fix: auto: <command>` should be the exact command the fix-applier will run. Use the project's runner if one exists (`npm run lint:fix`) — that lets the project's own config decide what gets touched. If no runner, use the global binary with the file list.

### Individual findings (for not-auto-fixable violations)

For each not-auto-fixable violation, emit one finding in the [`finding-format.md`](../../references/finding-format.md) schema:

```
[P1] [hygiene] src/auth/session.ts:147 — `no-explicit-any` violation on changed line
why: eslint flagged `any` on a line in this diff; the rule is `error` in the project config but doesn't auto-fix (would need type inference).
fix: replace `: any` at line 147 with the inferred type from the assignment; if no inference is possible, narrow to `unknown` and document why.
```

Severity for individual hygiene findings:

- **P0** — a real type error or undefined-behaviour bug the LSP flags (`tsc --noEmit` non-zero).
- **P1** — a rule the project config marks `error` on a changed line.
- **P2** — a rule the project config marks `warn` on a changed line, or `error` on a file the diff touches but the rule itself isn't on a changed line.
- **P3** — `info` / `hint`-level diagnostics, or rules the project config marks as off but that the tool flagged anyway.

Hard cap: **20 individual findings per tool**. If a tool flagged more (rare — usually means a config regression), prioritise the top 20 and append a P3 finding: `tool: <name> emitted N additional findings; suppressed for context. Run \`<command>\` for the full list.`

### When a tool reports zero violations

Don't emit anything for that tool. The orchestrator will see "review-hygiene: clean" in the unified report by counting the absence.

## Phase 4 — Tool unavailability

If a tool's detection signal is present but the tool itself isn't installed, emit one P3 finding per missing tool:

```
[P3] [hygiene] .:1 — eslint config present but eslint not installed
why: .eslintrc.cjs detected at repo root but `npx eslint` failed (or `eslint` not on PATH); coverage gap.
fix: decide: install the project's eslint via `npm install` (or document why eslint is configured but not used)?
```

These don't have an `auto:` fix because installing dependencies is a user decision, not a mechanical edit.

## Operating rules

- **Read-only is non-negotiable.** Never `--fix`, `--write`, `-w`. The skill's `allowed-tools` doesn't include `Edit`/`Write` as the structural guard.
- **One aggregate finding per tool, not per file.** The whole point is to keep per-violation detail out of the orchestrator's context.
- **`auto:` commands must be safe to re-run.** The fix-applier will re-run the tool in check-mode after the apply to validate; the tool must produce the same result every time.
- **Don't second-guess the tool.** If ESLint says a violation is auto-fixable, trust it. If it says not-auto-fixable, emit individual. Don't override.
- **Project runner beats global binary.** Use `npm run lint` over `npx eslint` when both exist — the project's runner knows the project's config.

## Composing with other skills

- Called by: `/review-change`, `/review-pr` (as part of the fan-out audit pipeline). Also callable directly.
- Sibling read-only specialists: `/review-code` (subjective design judgment), `/review-test`, `/review-feature`, `/review-security`, `/review-ux`, `/review-spec`.
- Acted on by: `/drive-change` — aggregate packets run as a single tool invocation; individual packets dispatch fix-appliers per finding.

`/review-hygiene` and `/review-code` are complements: `/review-hygiene` handles what tools know how to check, `/review-code` handles what they don't (SRP, layering, naming, structural smells).
