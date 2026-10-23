---
name: formatters
description: 'Bootstraps project linting and formatting tools. Use when installing formatters, adding lint scripts, or wiring lint CI and pre-commit hooks.'
argument-hint: '[--dry-run] [--force] [--yes] [--sync] [--copy] [--ci] [--no-autofix] [--hooks] [--no-aliases] [--no-docs] [--target=<dir>] [--profile=<lang>] [--rust] [--ts] [--python] [--go] [--docs] [--shell] [--all]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(cp:*)
  - Bash(mkdir:*)
  - Bash(diff:*)
  - Bash(jq:*)
  - Bash(chmod:*)
  - Bash(test:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/bundle/*.sh:*)'
---

# Formatters Bootstrap

Installs a best-practices lint/format environment into a target project. Does not reimplement linter dispatch — it drives the repo's own `scripts/style.sh init --copy|--sync` machinery and adds documentation, aliases, CI, and hook wiring on top.

**Operational context:** Install the self-contained scripts/style.sh bundle and per-language configs, add package.json/Makefile/justfile aliases and project docs, and optionally wire CI and pre-commit hooks. Preserve managed-manifest idempotency; --sync is the rerun path.

## Current Target Context

- **Profile detection** (complete `key=value` output, `project_root` last): !`${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/profile-style.sh`

Context injection is one scoped helper call: no `pwd`, `head`, `2>/dev/null`, or pipeline. Compound pipelines are host-permission behavior (a headless caller allowlist may reject them even when each segment is allowed), and `head -30` previously dropped profile keys. Do not widen `allowed-tools` with `head`, `find`, `wc`, or `pwd`; run each helper as a single command.

## Arguments

| Flag                                                           | Meaning                                                                         | Example                                  |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------- |
| `--dry-run`                                                    | Preview every planned file; make no writes                                      | `ycc:formatters --dry-run`               |
| `--force`                                                      | Overwrite existing tool configs / aliases / docs without prompting              | `ycc:formatters --force`                 |
| `--yes`                                                        | Non-interactive; keep existing files on conflict                                | `ycc:formatters --yes`                   |
| `--sync`                                                       | Install bundle + prune stale managed files (preferred on re-run)                | `ycc:formatters --sync`                  |
| `--copy`                                                       | Install bundle without pruning (default when no manifest exists)                | `ycc:formatters --copy`                  |
| `--ci`                                                         | Also emit `.github/workflows/lint.yml` and `.github/workflows/lint-autofix.yml` | `ycc:formatters --ci`                    |
| `--no-autofix`                                                 | With `--ci`: skip `lint-autofix.yml`, install the check workflow only           | `ycc:formatters --ci --no-autofix`       |
| `--hooks`                                                      | Also wire a pre-commit hook (lefthook preferred, husky if detected)             | `ycc:formatters --hooks`                 |
| `--no-aliases`                                                 | Skip package.json / Makefile / justfile alias injection                         | `ycc:formatters --no-aliases`            |
| `--no-docs`                                                    | Skip README section append                                                      | `ycc:formatters --no-docs`               |
| `--target=<dir>`                                               | Target directory (default: `$PWD`)                                              | `ycc:formatters --target=~/projects/app` |
| `--profile=<lang>`                                             | Override detection: `rust`, `ts-node`, `python`, `go`, `docs`, `mixed`          | `ycc:formatters --profile=rust`          |
| `--rust` / `--ts` / `--python` / `--go` / `--docs` / `--shell` | Enable specific stack(s); suppresses auto-detection                             | `ycc:formatters --rust --go`             |
| `--all`                                                        | Install every supported stack's configs regardless of detection                 | `ycc:formatters --all`                   |

Flags are composable. See `references/flag-reference.md` for the full matrix and precedence rules. See `references/best-practices.md` for per-language tool rationale.

**Questions:** class `confirm-destructive` ("Proceed with install?"); headless (no question tool or chat turn): abort the install and print `rerun with --yes`. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Task

Execute the phases in order. Phases are short — do not add narrative prose between them.

### Phase 0 — Parse flags

Extract booleans from `$ARGUMENTS`:

- `DRY_RUN`, `FORCE`, `YES`, `CI`, `NO_AUTOFIX`, `HOOKS`, `NO_ALIASES`, `NO_DOCS`
- `TARGET` — value of `--target=<dir>`; default to `$PWD`
- `PROFILE` — value of `--profile=<lang>`; empty if unset
- Per-stack booleans: `RUST`, `TS`, `PYTHON`, `GO`, `DOCS`, `SHELL`; `ALL` for `--all`
- `SYNC_MODE` — true if `--sync` passed; `COPY_MODE` — true if `--copy` passed

Validation:

- Reject both `--sync` and `--copy` passed together.
- If `TARGET` does not exist as a directory, abort.

### Phase 1 — Profile

Run `${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/profile-style.sh "$TARGET"` as one command. Keep every key (including `project_root`, `docs_target`, and hook/CI keys); parse the returned text in the caller. If an applier needs `--profile-file`, save that complete text with Write rather than an outer redirect or pipeline.

Stack-flag resolution:

- If `ALL=true` → enable all per-stack flags.
- Else if `PROFILE` is set → force per-stack flags from the profile mapping (see `references/flag-reference.md` `--profile` table).
- Else if any explicit per-stack flag was passed → use only the ones passed; do NOT override with auto-detection.
- Else → enable each stack whose `detect_*=true` in the profile.

Mode resolution:

- If `SYNC_MODE` → use `--sync`.
- Else if `COPY_MODE` → use `--copy`.
- Else if `has_style_bundle=true` → use `--sync`.
- Else → use `--copy`.

### Phase 2 — Plan preview

Print a plan block listing what will happen. Format:

```
Target:            <TARGET>
Mode:              --sync  |  --copy
Stacks:            rust, ts, python, go, docs, shell
Bundle install:    scripts/style.sh, scripts/format.sh, scripts/lint.sh, scripts/init-formatters.sh,
                   scripts/install-shellcheck.sh, scripts/go-tools.sh, scripts/lib/*,
                   scripts/templates/*  (managed bundle files)
Tool configs:      rustfmt.toml, clippy.toml, .golangci.yml, biome.json, tsconfig.json, package.json*,
                   pyproject.toml*, .markdownlint.json, .markdownlintignore, .prettierrc, .prettierignore
                   (* stack-aware scaffold / refuses to overwrite existing)
Aliases:           (skipped if --no-aliases)  package.json / Makefile / justfile
Docs:              (skipped if --no-docs)     README.md / CONTRIBUTING.md / AGENTS.md / CLAUDE.md
CI workflows:      (only if --ci)             .github/workflows/lint.yml
                                               .github/workflows/lint-autofix.yml (unless --no-autofix)
Pre-commit hook:   (only if --hooks)          lefthook.yml or .husky/pre-commit
```

Note each item that will be skipped (existing config, manifest detected, etc.).

### Phase 3 — Dry-run / Confirm gate

- If `DRY_RUN=true` → run each sub-script with `--dry-run` to preview the writes, then STOP.
- Else if `YES=false` and `FORCE=false` → ask the user "Proceed with install? (yes / no)"; abort on anything other than an affirmative.
- Else proceed.

### Phase 4 — Install bundle + tool configs

Invoke the self-contained installer shipped inside the skill:

```
STYLE_SH="${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/bundle/style.sh"
```

Build `init_args`:

- Mode flag: `--sync` or `--copy` per Phase 1.
- `--target "$TARGET"`.
- Per-stack flags: for each enabled stack, append `--rust|--ts|--python|--go|--docs|--shell` as appropriate.
- Overwrite policy: `--force` if `FORCE=true`, `--yes` if `YES=true`, `--dry-run` never (dry-run is handled in Phase 3).

Run:

```
"$STYLE_SH" init "${init_args[@]}"
```

Surface its stdout. If it exits non-zero, STOP and surface the error verbatim.

### Phase 5 — Aliases, docs, CI, hooks (parallel-safe, sequential-ok)

Unless suppressed, run each applier. Each writes to a distinct file so they can run sequentially with no conflicts. For each, prefer `--force` when `FORCE=true`.

1. **Aliases** (skipped if `NO_ALIASES=true`):

   ```
   ${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/apply-aliases.sh --target "$TARGET" [--force]
   ```

2. **Docs** (skipped if `NO_DOCS=true`):

   ```
   ${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/apply-docs.sh --target "$TARGET" --profile-file "$PROFILE_FILE" [--force]
   ```

3. **CI** (only when `CI=true`):

   ```
   ${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/apply-ci.sh --target "$TARGET" --profile-file "$PROFILE_FILE" [--force] [--no-autofix]
   ```

   Pass `--no-autofix` when `NO_AUTOFIX=true` to install only the check workflow. The check workflow runs on every PR and on pushes to the default branch and `release/**`. The autofix workflow runs on same-repo PRs to the default branch (`origin/HEAD`, falling back to `main`), applies `./scripts/style.sh format` + `lint --fix`, and pushes fixes back as `github-actions[bot]`; fork PRs are skipped because `GITHUB_TOKEN` cannot push to them.

4. **Hooks** (run when `HOOKS=true`, OR when the target already has a `lefthook.yml` / `.husky/pre-commit` — i.e., `has_lefthook=true` or `has_husky=true` in the profile):

   ```
   ${CLAUDE_PLUGIN_ROOT}/skills/formatters/scripts/apply-hooks.sh --target "$TARGET" --profile-file "$PROFILE_FILE" [--force]
   ```

   The auto-trigger keeps managed `style-lint` / `style-format` commands in sync on every `--sync` re-run without forcing first-time hook installation on users who never asked for it. `apply-hooks.sh` is idempotent: when managed commands are already present, it logs a no-op; otherwise it merges them in (lefthook) or skips if a non-empty `.husky/pre-commit` exists without `--force` (husky).

If any applier exits non-zero, report the failure and continue with the remaining ones — do not let a single applier abort the whole run.

### Phase 6 — Summary report

Produce a summary with these sections:

- **Bundle install** — lines from `style.sh init` (created, overwritten, skipped counts).
- **Tool configs** — per-stack: written / skipped-existing / refused-to-overwrite (for `pyproject.toml`).
- **Aliases** — strategy chosen (package-json / makefile / justfile) and alias keys installed.
- **Docs** — which file was appended or created; section name.
- **CI** — paths written (`lint.yml` always; `lint-autofix.yml` unless `--no-autofix`), or "not requested".
- **Hooks** — tool used (lefthook / husky / native), path written, or "not requested".
- **Next steps** — any of:
  - `git config commit.template .gitmessage` (unrelated to this skill but often useful alongside)
  - `lefthook install` (if `--hooks` + lefthook chosen)
  - Review `scripts/` bundle in the first commit that adds it
  - Re-run with `ycc:formatters --sync` after upstream bundle changes
  - Bypass a single hook run: `git commit --no-verify`

## Important Notes

- **Source of truth is `scripts/style.sh`.** This skill is an orchestrator; it never reimplements linter dispatch. Upgrading the upstream bundle propagates to installed targets via `ycc:formatters --sync`.
- **Never overwrites user-authored configs silently.** `apply-aliases.sh` preserves existing `package.json` scripts unless `--force`. `style.sh init-formatters.sh` refuses to overwrite an existing `pyproject.toml`. Tool configs (prettier, biome, markdownlint, clippy, rustfmt) are skipped when present unless `--force`.
- **Detection is ignore-aware.** Auto-detection enumerates only project source — git-tracked and untracked-but-not-gitignored files (via `git ls-files`), or a `find` fallback in non-git dirs — and skips well-known vendored/build directories (`node_modules`, `dist`, `build`, `vendor`, `.venv`, caches, …). A stray `*.rs`/`*.py` inside `node_modules/` or a build-output tree no longer flips `detect_*` to `true`. A vendored tree that is committed **and not gitignored** is still seen as source; list it in a root `.style-excludes` file (or `STYLE_EXTRA_EXCLUDES`) to drop it from detection and linting. See `references/stack-detection.md`.
- **`--hooks` is opt-in.** Hooks change commit behavior repo-wide. The installer always prints the `git commit --no-verify` escape.
- **Re-entrancy.** Re-running the skill with `--sync` on an already-installed target is a no-op for unchanged files, and prunes managed files removed upstream. Safe to schedule periodically.
- **Runtime-neutral aliases.** When the target has no `package.json`, the skill installs Makefile targets instead. Node is never required downstream.
- **Composing with `/ycc:init`.** `/ycc:init --formatters` delegates here and passes through `--dry-run` and `--force`. Invoke this skill directly for full flag coverage (CI, hooks, per-stack overrides).
- For per-language tool rationale (why biome over eslint, ruff over flake8, etc.), see `references/best-practices.md`.

## Support files

Pointers below are conditional reads, not extra execution steps. Helpers consume templates automatically.

- Read `references/templates/package-json-scripts.json.tmpl`, `references/templates/makefile-snippet.mk.tmpl`, and `references/templates/justfile-snippet.just.tmpl` when inspecting alias output for package.json, Makefile, or justfile respectively.
- Read `references/templates/readme-section.md.tmpl` when inspecting generated documentation (`--no-docs` skips it).
- Read `references/templates/lint.yml.tmpl` when inspecting `--ci` check output; read `references/templates/lint-autofix.yml.tmpl` when `--ci` enables autofix (not `--no-autofix`).
- Read `references/templates/lefthook.yml.tmpl` when inspecting lefthook output; read `references/templates/husky-pre-commit.tmpl` when inspecting Husky output under `--hooks`.
- Run `scripts/bundle/style.sh` when installing/syncing the bundle in Phase 4. Read `scripts/bundle/init-formatters.sh` when inspecting its install behavior; `style.sh` runs it, do not run it separately.
- Read `scripts/bundle/format.sh` and `scripts/bundle/lint.sh` when inspecting installed format/lint dispatch; downstream `style.sh` runs them, do not run them separately here.
- Read `scripts/bundle/go-tools.sh` when inspecting Go tool setup; read `scripts/bundle/install-shellcheck.sh` when inspecting pinned ShellCheck setup. Installer/dispatcher runs them as needed; do not run them separately here.
- Read `scripts/bundle/lib/excludes.sh` when inspecting ignore rules and `scripts/bundle/lib/modified-files.sh` when inspecting changed-file selection. Sourceable helpers, not standalone commands.
- Read `scripts/bundle/lib/shellcheck-resolve.sh` when inspecting ShellCheck lookup and `scripts/bundle/lib/shellcheck-version.sh` when inspecting its pinned version. Sourceable helpers, not standalone commands.
- Read `scripts/bundle/templates/biome.json` and `scripts/bundle/templates/tsconfig.json` when inspecting TypeScript/JavaScript config output.
- Read `scripts/bundle/templates/clippy.toml` and `scripts/bundle/templates/rustfmt.toml` when inspecting Rust config output.
- Read `scripts/bundle/templates/python-pyproject.toml` when inspecting Python config output.
- Read `scripts/bundle/templates/markdownlint.json`, `scripts/bundle/templates/markdownlintignore`, `scripts/bundle/templates/prettierrc.json`, and `scripts/bundle/templates/prettierignore` when inspecting docs config output.
