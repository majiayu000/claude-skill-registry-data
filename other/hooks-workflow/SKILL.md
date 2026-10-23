---
name: hooks-workflow
disable-model-invocation: true
description: 'Generates hook configuration from language rules. Use when configuring Claude hooks, translating rule hook guidance, or verifying existing hook config.'
argument-hint: '<language> [--target=claude|cursor|codex] [--event=PreToolUse|PostToolUse|Stop|all] [--out=<path>] [--dry-run] [--verify] [--force]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/hooks-workflow/scripts/build-hook-config.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/hooks-workflow/scripts/verify-hooks.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/report-bundle-drift.sh:*)'
---

# hooks-workflow

This skill turns existing rule-file hook guidance into real, target-appropriate
hook configuration. It reads `ycc/rules/<language>/hooks.md` (plus
`ycc/rules/common/hooks.md` when present), resolves which hook events the
requested target actually supports by consulting the capability matrix, and
invokes `build-hook-config.sh` to emit the correct artifact. Explicit
per-target boundaries are enforced at every step: Claude receives a concrete
JSON `hooks` settings fragment, Cursor receives a rule-embedded `.mdc` advisory
where the matrix shows partial support, and Codex always receives an
advisory-only `config.toml` fragment. The skill never claims parity across
targets and never fabricates config for a target the matrix marks as
unsupported.

## When to use

- You want a real `hooks` block in `~/.claude/settings.json` generated from
  the project's existing rule guidance.
- You want to know which hook events are supported on Cursor or Codex before
  spending time writing config.
- You want to verify that previously emitted hook config is still parseable and
  that any referenced command binaries are present.
- You want a dry-run preview of what the skill would emit without writing any
  files.
- You want an advisory-only Codex fragment that documents hook intent even
  though Codex hooks are not yet in GA.

## Arguments

Parse `$ARGUMENTS` for:

- **language** (required, first positional) — the rules subdirectory name, e.g.
  `python`, `typescript`, `go`. The skill resolves this to
  `ycc/rules/<language>/hooks.md`. Use `Glob` on `ycc/rules/*/` to list valid
  values; abort with the full list if the provided value does not match.
- **--target** (default `claude`) — one of `claude`, `cursor`, or `codex`.
  Determines which output format is produced and which matrix cells are checked.
- **--event** (default `all`) — one of `PreToolUse`, `PostToolUse`, `Stop`, or
  `all`. Restricts which hook events are included in the emitted config.
  Passing `all` includes every event the matrix marks as supported or partial
  for the resolved target.
- **--out** (default varies by target) — explicit output path. Defaults:
  Claude → `~/.claude/settings-hooks-fragment.json`;
  Cursor → `ycc/rules/<language>/hooks-cursor.mdc`;
  Codex → `ycc/rules/<language>/hooks-codex.toml`.
- **--dry-run** — print the full plan and the would-be output, write nothing,
  and stop before invoking any scripts.
- **--verify** — after writing the output file, invoke `verify-hooks.sh` to
  run parse-only checks and probe referenced command binaries.
- **--force** — required when writing Codex output to disk. Without this flag,
  Codex output is printed to stdout only. Has no effect on Claude or Cursor
  targets.

## Phases

### Phase 0: Reload the capability matrix

Read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/target-capability-matrix.md`
in full. Hold the parsed table in context for all subsequent matrix lookups.
Do not use stale or cached matrix data from a previous run.

### Phase 1: Resolve language and source rules files

Use `Glob` to list all directories matching `ycc/rules/*/`. Extract the
directory name (the trailing path segment) from each match to build the valid
language list.

If the provided `<language>` is not in that list, STOP and emit:

```
Unknown language "<language>". Valid values: <sorted list of discovered names>.
```

Resolved sources (read both if they exist; skip silently if absent):

1. `ycc/rules/<language>/hooks.md` — language-specific hook recommendations
2. `ycc/rules/common/hooks.md` — cross-language hook recommendations

If neither file exists, STOP and emit:

```
No hooks.md found under ycc/rules/<language>/ or ycc/rules/common/.
Nothing to generate.
```

### Phase 2: Resolve target and check matrix support

For each event in the resolved `--event` set, look up the `HOOKS.<event>` row
and the `--target` column in the matrix loaded in Phase 0.

Cell verdicts:

- `supported` — proceed normally.
- `partial` — proceed but prefix the output block with the relevant Notes entry
  from the matrix, verbatim.
- `unsupported` — STOP for that event and emit:

```
HOOKS.<event> is not supported on target <target>.
Matrix row: | HOOKS.<event> | <claude cell> | <cursor cell> | <codex cell> |
<If a different target supports it, note: "HOOKS.<event> is supported on <other target>.">
```

If `--event all` was passed and every event is `unsupported` for the chosen
target, STOP entirely after emitting the unsupported messages for all events.

### Phase 3: Parse hook recommendations

Read the resolved source file(s) from Phase 1. Extract each hook
recommendation: the triggering event, the matcher pattern or tool name (if
any), and the command to run. Use `Grep` if needed to locate the structured
sections within the file.

If a source file exists but contains no parseable hook recommendations, note
this in the output and continue (there may still be advisory content worth
emitting).

### Phase 4: Invoke build-hook-config.sh

The builder requires canonical `ycc/rules/*/hooks.md` sources, the compatibility
matrix, and hook templates. It discovers a source checkout or accepts
`--repo-root=/path/to/checkout`; installed bundles do not contain these sources.

Run:

```
${CLAUDE_PLUGIN_ROOT}/skills/hooks-workflow/scripts/build-hook-config.sh \
  --language=<language> \
  --target=<target> \
  --event=<event> \
  --out=<path> \
  [--force]
```

Output format by target:

- **Claude** — a JSON fragment containing only the `hooks` key, suitable for
  merging into `~/.claude/settings.json`. Example structure:

  ```json
  {
    "hooks": {
      "PreToolUse": [...],
      "PostToolUse": [...],
      "Stop": [...]
    }
  }
  ```

- **Cursor** — a `.mdc` rule-embedded fragment where the matrix shows `partial`
  support. Where an event is `unsupported`, the script emits an advisory-only
  marker comment instead of executable config.
- **Codex** — always an advisory-only `config.toml` fragment. The script MUST
  prefix the entire output with:

  ```
  # Advisory only — Codex hooks are under development; verify support in the installed CLI.
  ```

  Codex output is printed to stdout unless `--force` was passed. If `--force`
  is absent and `--out` resolves to a file path, STOP before writing and emit:

  ```
  Codex output requires --force to write to disk. Re-run with --force to
  confirm. Output printed to stdout:
  <content>
  ```

If `build-hook-config.sh` exits non-zero, surface the full stderr output and
STOP.

### Phase 5: Verify (conditional)

If `--verify` was passed, run:

```
${CLAUDE_PLUGIN_ROOT}/skills/hooks-workflow/scripts/verify-hooks.sh \
  --file <resolved-out-path> \
  --target <target>
```

This script performs parse-only checks on the emitted file and probes each
hook command binary with `--help` or `--version`. It never executes a hook
body. Surface the full stdout and stderr from the script. If it exits non-zero,
report the failure without rolling back the written file.

### Phase 6: Emit produced paths and matrix justification

After all phases complete, always emit:

1. The absolute path(s) of the file(s) written (or "no file written" if
   `--dry-run` or Codex without `--force`).
2. The matrix row(s) that justified the decision, quoted verbatim from the
   matrix table. For example:

   ```
   Matrix justification:
     | HOOKS.PreToolUse | supported | partial | unsupported |
   ```

## Anti-parity stance

This skill refuses to fabricate config for an unsupported target. If the matrix
cell is `unsupported`, the skill stops for that event and reports exactly what
the matrix says. There is no fallback, no silent downgrade, and no invented
config.

Dry-run mode (`--dry-run`) always emits the advisory text — including any
unsupported notices derived from the matrix — and stops before writing any
file. A dry run that encounters an `unsupported` cell is informational, not an
error; it shows what would have been blocked.

## Notes

- For per-target capability explanations and known limitations, see
  `${CLAUDE_PLUGIN_ROOT}/skills/hooks-workflow/references/support-notes.md`.
- Run `scripts/build-hook-config.sh` when rendering hook config (Step 2); the script reads
  the three per-target templates internally. Read a template only when inspecting its output:
  `references/templates/claude-settings.json.tmpl` (Claude target),
  `references/templates/codex-config-fragment.toml.tmpl` (Codex target), and
  `references/templates/cursor-rule-fragment.mdc.tmpl` (Cursor target).
- The authoritative capability verdicts live in
  `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/target-capability-matrix.md`.
  Do not override matrix verdicts locally.
