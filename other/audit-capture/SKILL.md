---
name: audit-capture
description: Run manifest-driven PNG captures of TUI and extension surfaces for design audits. Emits a schema-conformant capture tree for consumption by a Claude design-audit session.
allowed-tools: Bash(node tools/audit-capture*), Bash(node tools/audit-capture.mjs *), Bash(npm run audit*)
---

# Audit Capture

Manifest-driven capture of every user-facing PPDS surface. Produces PNGs + `meta.json` + root `manifest.json` under `$AUDIT_OUT/` per [`ppds-design-system/AUDIT-SCHEMA.md`](https://github.com/joshsmithxrm/joshsmithxrm/ppds-design-system/blob/main/AUDIT-SCHEMA.md). Output is consumed by a Claude audit session (or human designer) against our design system.

## When to Use

- Before a design-audit round — capture a clean baseline of every surface
- After UI shakedown / visual fixes land, to refresh the baseline
- When adding a new TUI screen or extension panel, to verify the manifest entry reaches it
- **NOT** for regression testing — this is audit input, not a diff tool

## Quick start

```bash
# One capture run, all surfaces, local output
export AUDIT_OUT="$TEMP/ppds-audit-$(date +%s)"
export PPDS_PROFILE=dev                 # optional — unlocks connected captures
export PPDS_ENV=test-env                 # optional — unlocks connected captures
node tools/audit-capture.mjs run all

# Single surface
node tools/audit-capture.mjs run tui
node tools/audit-capture.mjs run extension

# Dry-run a manifest without capturing
node tools/audit-capture.mjs validate tui

# List manifest entries
node tools/audit-capture.mjs list extension
```

Exit codes: `0` = everything `ok` or `skipped`, `1` = at least one entry errored.

## Required environment

| Var | Required | Purpose |
|---|---|---|
| `AUDIT_OUT` | **yes** | Absolute path, **outside** the repo working tree. Runner refuses relative or in-repo paths. |
| `PPDS_PROFILE` | no | Profile name. Entries with `requires: connected` are `skipped` without it. |
| `PPDS_ENV` | no | Environment name. Skipped same as above. |
| `AUDIT_REDACT` | no | `true` (default) masks identifying values in status bars. Set `false` for raw. |
| `AUDIT_SOURCE_REPO` / `_REF` / `_COMMIT` | no | Overrides the git metadata recorded in `manifest.json`. CI uses these. |

## Output layout

Per [`AUDIT-SCHEMA.md`](https://github.com/joshsmithxrm/ppds-design-system/blob/main/AUDIT-SCHEMA.md):

```
$AUDIT_OUT/
├── manifest.json                  ← inventory + state + summary
├── tui/<entry-id>/*.png
├── tui/<entry-id>/meta.json
├── extension/<entry-id>/*.png
└── extension/<entry-id>/meta.json
```

`manifest.json` is written **last**, after every entry's directory is flushed. A reader never sees it referencing a file that hasn't been written.

## Manifests (single source of truth)

Adding a new screen or panel means editing one YAML file. No runner changes required.

- TUI: [`tools/audit-manifests/tui.yaml`](../../../tools/audit-manifests/tui.yaml)
- Extension: [`tools/audit-manifests/extension.yaml`](../../../tools/audit-manifests/extension.yaml)

Each entry has:

```yaml
- id: kebab-case-id                   # unique within surface
  title: Human readable title
  requires: connected                 # or "none" (default)
  steps:
    - key: alt+t
    - wait: { text: "SQL Query", timeout: 5000 }
    - screenshot: 01-empty            # NN-name, zero-padded
    - type: "SELECT * FROM account"
    - key: F5
    - wait: { text: "rows", timeout: 30000 }
    - screenshot: 02-results
  masks:
    - { row: 28, colStart: 0, colEnd: 120, reason: "status bar" }
```

Step types: `key`, `type`, `wait`, `screenshot`, `sleep` (all surfaces). Extension adds `command`, `click`, `eval`.

Masks:
- TUI: cell-grid — `{ row, colStart, colEnd, reason }`
- Extension: pixel rect — `{ x, y, width, height, reason }`

Every entry must capture at least one screenshot. Entry ids must be kebab-case. Screenshot names must match `NN-name` (e.g. `01-empty`, `02-results`).

## What runs unattended

- **No profile required:** splash, file/help menu, profile picker, command palette. Always captured.
- **Connected (requires `PPDS_PROFILE` + `PPDS_ENV`):** every data-bearing screen/panel. Without a configured connection they're marked `state: skipped` with a clear `skipReason` — run still exits `0`.

## Typical flow

1. `node tools/audit-capture.mjs validate <surface>` — parses manifest, flags bad steps/ids.
2. `npm run audit:tui` / `npm run audit:extension` — capture that surface. Runs build first.
3. Inspect `$AUDIT_OUT/manifest.json` — should show `state: ok` for everything that matched `requires`.
4. Hand `$AUDIT_OUT/` to the audit consumer (push to `ppds-v1-audit` in CI; local: open PNGs directly).

## Gap protocol

If a manifest entry can't reach its target screen with the available step types:

1. **Stop.** Do not add a `sleep: 10000` to work around a flaky step — that's a silent lie that a designer will later debug.
2. Fix the navigation. If keys changed, update the entry's `steps`.
3. If tui-verify / webview-cdp lacks a capability, **stop** and say so — propose an enhancement to those tools, not a workaround here.
4. Re-run `validate` before `run`.

## Known limitations

- **Font substitution in CI** — if Cascadia Mono is absent, xterm.js falls back to system monospace. Output differs from a Cascadia-installed dev box. Bundling the WOFF2 is a roadmap item.
- **No light-theme captures** — v1 is dark-only on TUI + extension. Manifest schema reserves `themes` for future.
- **Single VS Code instance for extension run** — opening many panels in one session can accumulate focus noise. If you see wrong-panel captures, split the manifest into smaller runs.

## Related

- [specs/audit-capture.md](../../../specs/audit-capture.md) — the contract
- TUI PTY harness — see `/verify` `REFERENCE.md §tui` (invokes `tui-verify render` for TUI captures)
- VS Code CDP harness — see `/verify` `REFERENCE.md §ext`
- [`AUDIT-SCHEMA.md`](https://github.com/joshsmithxrm/ppds-design-system/blob/main/AUDIT-SCHEMA.md) — output format contract
