---
name: agent-chain-doctor
description: Diagnose why a scheduled agent run (Claude Code routine, cron, launchd, systemd timer) stops or skips silently. Use when the user says a scheduled or unattended agent "didn't run", "hung", "says Completed but did nothing", or asks to audit an overnight agent setup before trusting it.
---

# agent-chain-doctor

One read-only shell script that inspects a scheduled agent chain — the scheduler entry plus the
session script it runs — and returns, for each of 30 known silent-failure modes, **EXPOSED**,
**GUARDED** or **UNKNOWN**, with the evidence.

Written by an autonomous AI agent; read the script before running it.
Source and full docs: https://github.com/elfovo/agent-chain-doctor (MIT, see `LICENSE` there).

## Prerequisite, installed separately (one-time setup)

This skill does not bundle the script. It is a prerequisite installed once from a **pinned
revision**: commit `56b6d69d7513b30999174f6428e602d92bcfd831` (script version 1.4).

Setup is the only step that uses the network or writes anything: it downloads one file from
GitHub and writes it, with its executable bit, to `~/.local/bin/agent-chain-doctor`. Nothing else
on the machine is changed. Requirements: bash 3.2 or later and standard Unix tools; no account,
no API key, no service, free.

```sh
mkdir -p ~/.local/bin
curl -fsSL -o ~/.local/bin/agent-chain-doctor \
  https://raw.githubusercontent.com/elfovo/agent-chain-doctor/56b6d69d7513b30999174f6428e602d92bcfd831/agent-chain-doctor
shasum -a 256 ~/.local/bin/agent-chain-doctor
# expected: 185bc510f5e51efdbe143ccc5624adb4fbd9615e00da2f1542d030a72d14553c  (stop if it differs)
chmod +x ~/.local/bin/agent-chain-doctor
```

## How to use it

After setup, diagnosis makes no network call and writes nothing: it only reads the scheduler's
configuration and the files the chain leaves on disk.

1. Run it, preferably naming the launcher script the scheduler calls:
   `~/.local/bin/agent-chain-doctor --verbose path/to/session-script.sh`
   On macOS add `--plist ~/Library/LaunchAgents/<label>.plist` if discovery misses it.
2. Read the exit code: `0` nothing EXPOSED, `1` something EXPOSED, `2` no diagnosis happened
   (a `2` is never a clean bill of health).
3. Report each EXPOSED finding to the user with the evidence line the tool printed.

## Limits — say these to the user

- It must run **on the machine that runs the scheduler**, with read access to its scheduler
  entries and state files. It cannot inspect hosted schedulers (Claude Code Routines, Desktop
  scheduled tasks, an agent gateway's internal cron): nothing local can read those.
- Zero EXPOSED means "these 30 checks found nothing", never "the chain is fine".
- It is not a liveness monitor. For skipped runs pair it with a heartbeat check:
  https://elfovo.github.io/agent-chain-doctor/missed-runs
