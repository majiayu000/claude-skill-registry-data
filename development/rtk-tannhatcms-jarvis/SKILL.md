---
name: rtk
description: "Trim noisy dev-command output (git diff, tsc, test logs) before it fills agent context, using the rtk binary. Use when a command's output is long and repetitive — saves 60-90% tokens. Do NOT use when another tool or gate parses the raw output."
---
<!--
Attribution: concept from rtk-ai/rtk (Apache-2.0) — "Rust Token Killer".
This is a thin JARVIS wrapper skill; the rtk binary is a separate install.
-->

# rtk — Trim Command Output

`rtk` is a small Rust binary that filters repetitive dev-tool output
(timestamps, progress bars, duplicate warnings) before it reaches the model.

## Install

Binary: https://github.com/rtk-ai/rtk/releases — place in `~/workspace/bin/`
(Apache-2.0). No cargo needed.

```bash
~/workspace/bin/rtk --version
```

## Usage

Prefix noisy read-only commands:

```bash
~/workspace/bin/rtk git diff
~/workspace/bin/rtk git status
~/workspace/bin/rtk tsc --noEmit
~/workspace/bin/rtk pytest -q
```

## When NOT to use

- The output feeds another program or gate (build-check parsing, JSON
  extraction, test-count assertions) — those need the raw bytes.
- The output is already short.
- You need exact line numbers/byte offsets for a downstream edit — verify
  against the real file afterwards.

## Notes

- `rtk` only filters presentation noise; it never changes exit codes.
- If a trimmed section looks suspicious, re-run without `rtk` on that part.
