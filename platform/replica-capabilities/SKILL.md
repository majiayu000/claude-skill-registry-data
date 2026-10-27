---
name: replica-capabilities
description: >-
  Scans this computer read-only and reports which Replica Crew target types it
  can build today (web, desktop, android, game, mashup) and what is missing for
  the rest: OS, CPU count, and the toolchains found (Node, Python, Java,
  Flutter, Android SDK, .NET, Rust, Go, Godot, Blender, Docker, Playwright,
  adb). Run first, before scope, so the plan only promises what the machine can
  actually do. Use when the user says "what can I build", "check my computer",
  "will this run here", "am I set up for Android / games / desktop", "replica
  doctor", or at the start of any clone whose target is not plain web.
---

# replica-capabilities

The bundled tool does the whole scan. It installs nothing, changes no config,
and makes no network calls: it runs `--version` probes and checks a few paths.

```bash
python doctor.py                 # human-readable report
python doctor.py --json          # for the orchestrator to read
python doctor.py --target android   # only what one target needs
```

(`doctor.py` is next to this SKILL.md, under `~/.agents/skills`,
`~/.claude/skills`, `~/.claude/plugins` or the repo's `skills/`. Standard
library only, so plain `python` or `python3` runs it.)

## What it decides

For each target type it prints `[YES]` or `[no ]` and, when `no`, the missing
tools with where to get them:

| target | ready needs | note |
| --- | --- | --- |
| `web` | Node + npm | static sites and web apps. The core target. |
| `desktop` | Node | Electron on Node alone; Rust for Tauri, .NET or Python/Qt for native |
| `android` | Java + (Flutter or Gradle) + Android SDK | an emulator or an adb device to test |
| `game` | Node | web-canvas (Phaser, Three.js, PixiJS); Godot for a native engine |
| `mashup` | Node (or Godot) | an original blend of two games' mechanics; own engine and assets |

## How to use the result

1. Run it and show the user the plain report.
2. Read the `--json` `targets` block. If the target they asked for is not
   `ready`, do **not** start the build. List exactly what to install (the tool
   already names each one and its site), and offer either a target that *is*
   ready or to proceed after they install the missing pieces.
3. Write the JSON to `replica/capabilities.json`. `replica-recon` and
   `replica-architect` read it so the stack they pick is one this machine can
   build, test and run.
4. Never install anything yourself. The user installs tools and SDKs; you only
   report and re-scan.

## Reporting

A short summary: OS and CPU count, the ready targets, and for the requested
target either "ready" or the install list. Then hand back to the orchestrator's
Wave 0.
