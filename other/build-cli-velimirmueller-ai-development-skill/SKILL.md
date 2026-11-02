---
name: build-cli
description: Use when creating or extending a command-line tool in TypeScript, Go, Python or Rust — subcommands, typed args, config precedence, stdout/stderr split, --json, exit codes, NO_COLOR/TTY handling, --dry-run, and spawn-the-binary tests.
---

# Build CLI

A CLI is called by people and by scripts. This skill makes the same tool work for both: one entry, subcommands, typed arguments, a fixed config order, data on stdout, diagnostics on stderr, `--json` with a stable schema, documented exit codes.

Rules with reasons: [cli-ux.md](cli-ux.md). Library choice and structure: [cli-patterns.md](cli-patterns.md). Tested code per language: [cli-examples.md](cli-examples.md). Versions: [stack-versions.md](../_shared/stack-versions.md) (verify live first, per [version-protocol](../../core/_shared/version-protocol.md)).

## 1. Audit current state

Change nothing yet. Read `.claude/stack-profile.md` (then `~/.claude/stack-profile.md`); if absent, detect.

```bash
cat .claude/stack-profile.md 2>/dev/null | sed -n '1,30p'
ls package.json go.mod pyproject.toml Cargo.toml 2>/dev/null          # language
grep -nE '"(commander|citty|yargs|cac|clipanion)"' package.json 2>/dev/null
grep -rnE 'spf13/cobra|urfave/cli|alecthomas/kong' go.mod 2>/dev/null
grep -nE '(typer|click|cyclopts|argparse)' pyproject.toml 2>/dev/null
grep -nE '^(clap|argh|lexopt)' Cargo.toml 2>/dev/null
ls src/cli* src/main.* cmd/*/main.go src/*/cli.py 2>/dev/null          # existing entry
grep -rnE 'NO_COLOR|isatty|IsTerminal|isTTY|--json' src cmd internal 2>/dev/null | head
```

Record: language, existing parser (keep it, see step 3), whether an entry file exists, whether `--json`, exit codes, config loading, tests-by-spawning are present. A monorepo with several languages: build the CLI in the language of the package that owns it; one question only if two candidates remain.

## 2. Decide what to do

- No CLI yet → full scaffold (steps 3-7).
- CLI exists, contract gaps → apply only the missing seams (step 5). Name each gap you will close.
- Contract met (stdout/stderr split, exit codes documented, `--json` schema, spawn tests) → say "already in place" and stop.
- Existing parser differs from the default (Click, yargs, urfave v2, clap 3) → keep it. Do not migrate inside this task.

## 3. Detect the track

Pick from `languages` in the profile or from step 1:

| Language | Parser | Config | Tests |
|---|---|---|---|
| TypeScript | `commander` 15, ESM, Node >= 22.18 | `smol-toml` + `env-paths` | Vitest spawning `dist/cli.mjs` |
| Go | `cobra`, entry `cmd/<name>/main.go`, `Run(args, out, err) int` seam | `go-toml/v2` | `go test` on `Run` + one built-binary test |
| Python | `typer`, `uv_build`, entry `<pkg>.cli:main` | `tomllib` + `platformdirs` | pytest + `subprocess` on `python -m <pkg>` |
| Rust | `clap` derive, `thiserror` | `toml` + `serde` + `dirs` | `assert_cmd` + `insta` help snapshot |

A profile with several languages gets one CLI per package, each following its own row. Lint and format come from the profile's `lint_format`.

## 4. Install only what is missing

Run the live check first (`npm view commander version`, `go list -m -versions github.com/spf13/cobra`, PyPI JSON, crates.io), then add dependencies with the package manager from the profile.

```bash
pnpm add commander env-paths smol-toml && pnpm add -D tsdown vitest   # TypeScript
go get github.com/spf13/cobra github.com/pelletier/go-toml/v2 golang.org/x/term   # Go
uv add typer platformdirs && uv add --dev pytest                       # Python
cargo add clap --features derive,env,wrap_help && cargo add serde --features derive && cargo add toml thiserror dirs   # Rust
```

TypeScript: runtime libraries go in `dependencies` (tsdown bundles `devDependencies`). Python: also set `requires = ["uv_build>=<current>,<next minor>"]`.

## 5. Generate the seams

Four seams per CLI, copied from [cli-examples.md](cli-examples.md) and renamed. Each owns one concern; nothing else touches it.

1. **`exit`** — an enum of codes (0 ok, 1 failure, 2 usage, domain codes from 3) and one typed error carrying a code and a hint.
2. **`output`** — the only writer to stdout/stderr. Decides colour (`NO_COLOR`, `TERM=dumb`, TTY per stream) and `interactive()` (stdin and stdout TTY, `CI` unset). Secrets are never passed to it.
3. **`config`** — builds a typed `Config` once: flags > env (`<NAME>_<KEY>`) > project `.<name>.toml` > user `$XDG_CONFIG_HOME/<name>/config.toml` > defaults. Unknown keys and bad values fail with exit 2.
4. **`cli` (entry)** — builds the parser, runs the command, maps `CliError` to its code, prints through `output`. The only place that exits.

Commands are thin: parse, call domain code, print through `output`. Then, for every command:

- Global flags `--json`, `--quiet`, `--verbose`, `--no-color` valid before and after the subcommand; `--version`; exit codes listed in the root `--help`.
- `--json` prints one document `{"schema": 1, ...}` on stdout, nothing else.
- Destructive commands: `--dry-run` (shared planning step, final write skipped) and `--yes`; prompt only when interactive, else fail with exit 2 naming the flag.
- Long options first; the same flag means the same thing everywhere.

## 6. Wire it

- Entry point: TypeScript `"bin": {"<name>": "./dist/cli.mjs"}` + `tsdown`; Python `[project.scripts]`; Go `cmd/<name>/main.go`; Rust `[[bin]]` (default).
- Task verbs (`dev`, `test`, `build`, `check`) go through the repo's runner: see [set-up-dev-toolchain](../set-up-dev-toolchain/SKILL.md). Release: [release-cli](../release-cli/SKILL.md).
- README: install, quick start, the config precedence table, the exit-code table, the JSON schema version. Link to `--help`, do not copy it.
- Completions: cobra and Typer have them built in, clap adds `clap_complete`; see `cli-patterns.md`.

## 7. Verify

Run the real binary, not the handler:

```bash
mycli --help; echo "exit=$?"                       # exit=0, lists exit codes
mycli list --json | jq -e '.schema == 1'            # stdout is pure JSON
mycli list --json >/dev/null 2>err.txt; test ! -s err.txt && echo clean   # nothing leaked to stderr
mycli list --bogus >/dev/null; echo "exit=$?"       # exit=2, stdout empty
NO_COLOR=1 mycli delete missing 2>&1 | grep -c $'\x1b'   # 0 escape sequences; the command exits 3
mycli delete x </dev/null; echo "exit=$?"           # not interactive: no hang
hyperfine --warmup 3 'mycli --version'              # under ~100 ms
```

Then the project check (`mise run check`, `pnpm test`, `go test ./...`, `uv run pytest`, `cargo test`) and the spawn tests from [cli-examples.md](cli-examples.md) pass. Expected: all exit codes as documented, `--help` snapshot committed.

## References

- [cli-ux.md](cli-ux.md): the rules and their reasons (streams, exit codes, JSON schema, config order, colour/TTY, dry-run, errors, help, speed, tests).
- [cli-patterns.md](cli-patterns.md): library choice per language, seams, completions, prompts.
- [cli-examples.md](cli-examples.md): the tested reference CLI in all four languages.
- [../_shared/stack-versions.md](../_shared/stack-versions.md): verified versions.
- [../../core/_shared/engineering-principles.md](../../core/_shared/engineering-principles.md), [../../core/_shared/security-baseline.md](../../core/_shared/security-baseline.md): seams, secrets.
