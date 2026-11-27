---
name: spin-breaker
description: >-
  Manual spin breaker. `lock` runs a 3-element pre-flight lock (target surface,
  observable check, forbidden boundary) before edits or delegation; default
  `rescue` halts loops, parks side quests and 4-line restart breadcrumbs, and
  proposes one discriminating read-only probe; `map` renders a static HTML
  decision board. Use spec-convergence for full spec design, ce-debug for
  root-cause debugging.
disable-model-invocation: true
metadata:
  revision: "2"
  areas: "self-management,software-development"
  targets: "runtime-agnostic"
  summary: "halt pre-execution or mid-session spinning: 3-element execution lock, 5-line reckoning, parked side quests, restart breadcrumbs, static HTML decision board"
  summary_zh: "开工前或中途打转时刹车：3 要素执行锁、5 行现状清点、停放 side quest、重启面包屑与静态 HTML 决策板"
  kind: "entry"
---

# spin-breaker

Explicit-invocation circuit breaker for two failure modes:

- **Pre-execution drift**: edits or delegation start while the target surface,
  the observable acceptance check, or the forbidden boundary is still implicit.
- **Mid-session spinning**: unfalsified guesses accumulate, emergent meta-ideas
  silently widen the acceptance envelope, and repeated `continue` eliminates
  nothing.

## Gates

1. **Immediate write/dispatch freeze.** On invocation, halt code edits, branch
   switches, commits, external memory writes, and background worker dispatches
   until the operator explicitly selects an option in the current turn.
2. **Host UI with plain-text fallback.** Present choices through the host's
   native single-select form control when it exists; if that UI is unavailable
   or disconnects, immediately present numbered plain-text options (`A / B / C`)
   so one short reply resolves the choice.
3. **Side-effect confirmation.** Never run a state-mutating command, discard Git
   changes, or invoke an external parking adapter without explicit operator
   confirmation (`--confirm-external` gates the external adapter).
4. **Artifact containment.** All generated HTML maps and local parked records
   live strictly under `<repo-root>/.tmp-artifacts/<bundle-name>/`; never
   scatter them in the repo root or tracked directories.

## Mode selection

Use the explicit mode if supplied. Otherwise choose from the current state:

| Mode | When to use | What it does / read |
|---|---|---|
| `lock` | Right before implementation or delegation | Read [Lock mode](references/lock-mode.md): confirm the exact target, observable check, and forbidden boundary before work starts. |
| `rescue` (default) | Mid-session spin, repeated `continue`, or scope creep | Read [Rescue mode](references/rescue-mode.md): offer to park side quests and present a five-line reckoning with one discriminating read-only probe. |
| `map` | Three or more entangled hypotheses, surfaces, or environments make linear chat hard to follow | Read [Decision board](references/decision-board.md): turn the evidence and decision into a static HTML board. |

Keep the freeze while you inspect read-only state and present choices. An
operator's selection authorizes only the selected action, not the other
options; a decision to retire an approach is not permission to roll back Git.

## Read when needed

| When | Read |
|---|---|
| Before invoking `park` or `map`, interpreting a receipt, or configuring an external adapter | [Commands](references/commands.md) |
| Resolving flags, environment, or config-file settings | [Configuration](references/configuration.md) |
| Only if a script command fails (for example `uv` is not found) | [Troubleshooting](references/troubleshooting.md) |

## Configuration

Resolution order for every key: CLI flag, then `SPIN_BREAKER_*` environment
variable, then `$XDG_CONFIG_HOME/spin-breaker/config.yaml` (falling back to
`~/.config/spin-breaker/config.yaml`), then the default.

| Key | Flag | Environment variable | Default |
|---|---|---|---|
| `repo_root` | `--repo-root` | `SPIN_BREAKER_REPO_ROOT` | `.` (current directory) |
| `parking_bundle` | `--parking-bundle` | `SPIN_BREAKER_PARKING_BUNDLE` | `spin-breaker` |
| `external_cmd` | `--external-cmd` | `SPIN_BREAKER_EXTERNAL_CMD` | none (empty; local markdown only) |
| `external_timeout` | `--external-timeout` | `SPIN_BREAKER_EXTERNAL_TIMEOUT` | `15` (seconds) |
