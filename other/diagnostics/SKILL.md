---
name: diagnostics
description: "Use when something in iclone os does not work. Diagnose and self-repair the app, the runtime, the gateway, ACP, the wallet, permissions, local data and the install with `acp doctor` — local only, no network unless asked. When to run which pack, how to read the JSON report, which fixes you may apply alone (risk low) and which go to the owner (medium/high, Settings › Diagnostics)."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, diagnostics, doctor, self-repair, troubleshooting]
    related_skills: [acp-troubleshooting, economyos]
---

# Diagnostics — `acp doctor`

This is the `iclone doctor` door of the brief: it lives on the `acp` client every agent already has, as the app-level verb
`acp doctor`, so it needs no second binary and no second credential.

icloneOS ships 8 diagnostic packs. They run inside the app on this device; the report never leaves it unless the owner
presses **Send diagnostics**. The door is the same `~/.iclone-os/bin/acp` client you already use (same socket, same auth).

## When to run it
- The owner says something "does not work", is slow, or broke after an update.
- A command failed twice in a row with the same error.
- Before a job that needs the wallet or ACP (run `acp` and `wallet`).
- Never in a loop: one run, read, act, one confirming run.

| Symptom | Pack(s) |
|---|---|
| agent does not answer, `hermes` errors, Python tracebacks | `runtime`, `gateway` |
| sessions lost, "database is locked", app slow to open chats | `gateway` |
| `acp` says malformed request / stale session / unknown iNFT | `acp` |
| sign-in loops, wallet empty, "sign in again" | `wallet` |
| microphone, screen, computer use refused | `permissions` |
| iNFT shows as unknown/lost unexpectedly, settings forgotten | `storage` |
| app will not open, "damaged", terminal does not start | `native` |
| everything times out | `network` — live probes contact the internet, so only the owner runs them (Settings › Diagnostics › Live network probes); the door refuses `--live` |

## How
```
acp doctor list --json                  # packs, checks, fixes, risk
acp doctor run [pack…] --json           # report: packs[].checks[] {id,status,detail,fixId,risk,consent}; local only
acp doctor fix <fix-id>                 # dry run: prints the plan, writes nothing
acp doctor fix <fix-id> --apply         # risk low only; backup first, undo note in the result
acp doctor report --json                # the last report (also Settings › Diagnostics)
```
Read `status` per check: `pass` · `warn` (review) · `fail` (fix) · `skip` (not applicable here). Act only on rows that carry a
`fixId`. Exit code 0 = nothing failed, 1 = something failed or a fix was refused, 64 = usage.

## What you may do alone
- **risk low**: dry-run first, read the plan, then `--apply`, then re-run the pack to confirm `pass`. Tell the owner in one line
  what you fixed and where the backup is.
- **risk medium / high**: never apply. Explain the finding and the fix title, and ask the owner to press it in
  **Settings › Diagnostics** (high-risk fixes also need the permission named in `consent`, Settings › Privacy).
- Fixes whose plan opens a page (e.g. `native.install_release`, the Privacy pane) are owner-only: the door refuses `--apply` for
  them even at risk low. Dry-run, then tell the owner what to install or allow.

## Never
- Never touch `~/.hermes/hermes-agent` or edit `~/.hermes/config.yaml` by hand — the fixes do it with a backup.
- Never run `hermes doctor` yourself, with or without `--live` or `--fix`. The runtime pack does not run it: the hermes self-check is `network.hermes_doctor` in the network pack, and only the owner runs it, live, from Settings › Diagnostics.
- Never ask for `--live`: the door refuses it. If network probes are needed, ask the owner to run them in Settings › Diagnostics.
- Never paste a report outside this conversation; it is redacted but it is still the owner's machine.

Per-pack notes (what each failure means, the fix, the trap): `references/<pack>.md`.
