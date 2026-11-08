---
name: peekaboo
description: "macOS screenshots, UI inspect, clicks, typing, app/window automation."
---

# Peekaboo

macOS screen capture, UI inspection, GUI automation.

## Binary

Prefer `~/bin/peekaboo` (local release copy). Else `peekaboo`.
Check: `~/bin/peekaboo --version || peekaboo --version`.

## Safety

- Check permissions before capture/automation: `peekaboo permissions status --json`.
- Screenshot needs Screen Recording; clicks/typing/window control need Accessibility.
- Remote Macs: Screenshot may be blocked (missing Screen Recording) while clicks/typing work via Accessibility; continue with clicks or DOM automation when target knowable.
- Prefer `--json` for machine parsing, `--no-remote` for local TCC testing.
- No click/type/destructive automation unless user asked or target is controlled test.

## Commands

```bash
PB="${PEEKABOO_BIN:-$HOME/bin/peekaboo}"
[ -x "$PB" ] || PB="$(command -v peekaboo)"

"$PB" permissions status --json
"$PB" list screens --json
"$PB" list apps --json
"$PB" list windows --app Safari --json
"$PB" image --mode screen --screen-index 0 --path /tmp/screen.png --json --no-remote
"$PB" see --app frontmost --path /tmp/frontmost.png --json --annotate
"$PB" tools --json
"$PB" learn
"$PB" click --coords 100,100 --json
"$PB" type "text" --json
```

## Workflow

1. Resolve `PB`, confirm version when install state matters.
2. `permissions status --json`; report exact missing TCC grants.
3. Screenshots: `image` with `--path`, `--json`, usually `--no-remote`.
4. Element targeting: `see --json --annotate`, click by element id/snapshot.
5. Long-running capture: `capture live`; video frame sampling: `capture video`.
6. Discovery: `tools --json`, `learn` for full agent guide.
7. Verify output: `sips -g pixelWidth -g pixelHeight <path>` or view image.

## Documentation

Use the resolved binary's `tools --json`, `learn`, or `<command> --help` for installed capabilities and syntax.
Local checkout documentation is optional. Use its `docs/commands/` directory only after locating and verifying that checkout; do not assume a machine-specific repository path.
