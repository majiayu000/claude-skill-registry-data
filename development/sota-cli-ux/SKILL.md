---
name: sota-cli-ux
description: >-
  State-of-the-art CLI and developer-tool UX guidance (2026) covering command
  and flag design, output and interaction (stdout/stderr, --json, TTY
  detection, exit codes, prompts), runtime behavior and lifecycle (signals,
  dry-run, idempotency, XDG paths, completions, telemetry), and distribution
  (packaging, checksums, docs). Use when designing or building any command
  line tool, subcommand, TUI, or developer tool — in any framework (argparse,
  click, typer, clap, cobra, oclif, commander) — AND when auditing an existing
  CLI for usability, scriptability, and compatibility. Not for shell-script
  correctness or security — use sota-shell-scripting. Trigger keywords: CLI,
  command line tool, flags, subcommands, terminal output, TUI, developer tool,
  argparse, clap, cobra, exit code, shell completion, man page, stdin, stdout.
---

# SOTA CLI & Developer-Tool UX

## Purpose

Expert-level rules for building and auditing command-line tools: the grammar of
commands/flags/args, config layering, human-vs-machine output, TTY-aware
interaction, exit codes, signal handling, lifecycle behavior, and distribution.
The core thesis: **a CLI has three users — a human at a TTY, a script in CI,
and an AI agent driving the tool (a stricter script) — and every design
decision must serve all three without flags-gymnastics.** Rules are
imperative with rationale and good/bad terminal examples; every rules file ends
with an audit checklist. Load only the files relevant to the task via the index
below.

## BUILD mode

When designing or implementing a CLI:

1. **Design the command grammar before writing code.** Write the `--help` text
   first: subcommand tree, every flag (short + long), args, examples. If the
   help is hard to write, the grammar is wrong (`rules/01`).
2. **Defaults carry the common path.** A new user must get a useful result with
   zero flags. Anything required for the 80% case is a design bug (`rules/01` §3).
3. **Split the streams from day one**: primary output → stdout, everything else
   (logs, progress, prompts, errors) → stderr. Retrofitting this breaks users'
   pipes (`rules/02` §1).
4. **Make it pipe-safe by default**: detect TTY; disable color/progress/prompts
   when piped; honor `NO_COLOR`; ship `--json` with every listing/reading
   command from v0.1, because output format is API (`rules/02`).
5. **Treat exit codes, flags, env vars, and JSON shapes as a public API**:
   document them, version them, deprecate — never repurpose or remove without a
   cycle (`rules/02` §3, `rules/03` §7).
6. **Build the unhappy paths with the happy path**: Ctrl-C cleanup, `--dry-run`
   on mutating commands, re-runnable/resumable operations, stdin-closed CI
   behavior, offline behavior (`rules/03`).
7. **Plan distribution early**: single static binary if the ecosystem allows,
   checksums + signatures, completions and man page generated from the same
   source as `--help` (`rules/03` §8, `rules/04`).
8. Before declaring done, run every relevant **Audit checklist** against your
   own tool, including the brutal smoke test: `tool cmd | cat`,
   `tool cmd > out.txt 2> err.txt`, `tool cmd < /dev/null`, `echo $?`.

## AUDIT mode

When reviewing an existing CLI:

1. Identify the surface: parser setup (argparse/clap/cobra/etc.), main/entry
   point, output and error paths, signal handlers, config loading, install/
   release scripts. Load the matching rules files.
2. **Run the tool, don't just read it.** Minimum probe set:
   - `tool --help`, `tool <sub> -h`, `tool --version`, `tool definitelynotacmd`
   - `tool list | cat` and `tool list | head -1` (color codes? broken pipe panic?)
   - `tool list > /dev/null` — does anything still reach the human? (it should, on stderr)
   - `tool mutate < /dev/null` — hang waiting for a prompt = CI killer
   - `echo $?` after success, after a usage error, after a real failure
   - Ctrl-C mid-operation: prompt state restored? partial state cleaned or resumable?
3. Then verify in code what can't be probed: config precedence order, secret
   handling, temp/state file locations, update/telemetry behavior.

### Severity conventions

- **Critical** — corrupts data or destroys trust: destructive op with no
  confirmation/`--force` and no dry-run; non-zero work reported as exit 0 (or
  vice versa) so CI lies; prompt hangs forever with stdin closed; secrets
  echoed to terminal/logs/argv; auto-update or telemetry without disclosure.
- **High** — breaks scripting or interrupts users: machine output polluted by
  ANSI codes/log lines on stdout; no `--json` on listing commands; SIGINT
  leaves corrupt partial state; undocumented/colliding exit codes; config
  precedence nondeterministic; breaking flag removal without deprecation.
- **Medium** — erodes usability: missing long forms; required flags on common
  path; no progress on >2s ops; errors without remediation; `$HOME` dotfile
  litter instead of XDG; no completions; no `-q`/`-v`; >500ms `--help`.
- **Low** — polish: help without examples, no suggest-on-typo, inconsistent
  subcommand naming, missing man page, table borders in output.

### Finding format

```
[SEVERITY] <one-line title>
Where: <file:line | command invocation that reproduces it>
Rule: <rules-file §section>
Issue: <what is wrong, with observed evidence (transcript or code)>
Impact: <who breaks: the human at the TTY, the script in CI, an agent driving the tool, or all>
Fix: <specific change; exact flag/stream/exit-code where load-bearing>
```

Order findings by severity; one finding per root cause; include the reproducing
command line whenever the issue was observed by running the tool.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-commands-flags-config.md` | Designing/auditing the command surface: subcommand grammar (noun-verb consistency), POSIX/GNU flag conventions, short/long forms, `--` separator, args vs flags vs stdin, defaults, dangerous-op flags, config precedence chain, env var naming, help text quality, suggest-on-typo. |
| `rules/02-output-interaction.md` | Anything the tool prints or asks: stdout vs stderr contract, `--json`/`--plain`, TTY detection, color and `NO_COLOR`/`TERM`, exit codes as API, streaming vs buffering, progress indication, prompts and `--yes`/CI behavior, quiet/verbose levels, error message anatomy, `--debug` vs stack traces, agent-facing design (`--fields`, confirmation envelopes, frozen output contracts). |
| `rules/03-behavior-lifecycle.md` | Runtime behavior and tool lifecycle: startup latency, idempotent re-runnable commands, `--dry-run`, `--self-test` for tools whose output is a verdict, SIGINT/SIGTERM handling, crash-only resumable design, network-op responsiveness and offline behavior, self-update caution, telemetry consent, XDG base directories, shell completions, semantic versioning of the CLI surface. |
| `rules/04-distribution-docs.md` | Shipping and documenting: single-binary packaging, install channels (brew/curl-script/registry) with checksums + signatures, docs generated from the `--help` source of truth, man pages, README quickstart, version pinning for CI. |

## Top-10 non-negotiables

1. **Primary output to stdout, everything else to stderr** — logs, progress,
   prompts, warnings, errors. `tool x | next` must receive only data. (rules/02 §1)
2. **Pipe-safe by default**: TTY-detect; no color, no spinners, no prompts when
   piped; honor `NO_COLOR` (set and non-empty) and `TERM=dumb`; `--json` on
   every command that lists or reads data. (rules/02 §2, §4)
3. **Exit 0 only on success; distinct, documented nonzero codes** for usage
   error vs operational failure; never `exit 0` after printing an error. (rules/02 §3)
4. **Every flag has a long form**; short forms only for the frequent few;
   GNU/POSIX syntax (`-f`, `--flag`, `--flag=value`, `--` ends flags). (rules/01 §2)
5. **No required flags on the common path** — good defaults; and the reverse:
   destructive operations require explicit `--force`/typed confirmation on a
   TTY and refuse (don't hang) without one. (rules/01 §3, §5)
6. **Every prompt is skippable**: `--yes`/`--no-input` equivalent exists; stdin
   closed or non-TTY ⇒ use default or fail fast with the flag to pass — never
   block CI. (rules/02 §6)
7. **Errors say what failed, why, and what to do next** — path, value, and the
   exact command to run; stack traces only under `--debug`. (rules/02 §7)
8. **Ctrl-C is sacred**: first SIGINT exits promptly with cleanup and exit code
   130, second SIGINT force-quits; terminal state always restored; interrupted
   work is resumable or rolled back. (rules/03 §3)
9. **`--dry-run` on every mutating command**, printing the real plan through
   the real code path. (rules/03 §2)
10. **The CLI surface is a semver'd API**: flags, exit codes, JSON fields, env
    vars. Deprecate with warnings for a full cycle; never silently change
    meaning. Config precedence is exactly flags > env > project config > user
    config > defaults, documented. (rules/01 §6, rules/03 §7)
