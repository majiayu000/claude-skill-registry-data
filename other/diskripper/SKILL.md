---
name: diskripper
description: Use when working on the DiskRipper Rust workspace.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rust, diskripper, media, backup, gui]
    related_skills: [rust-egui-native-desktop]
---

# DiskRipper Rust Workspace

All work in `C:\Projects\DiskRipper` — the native optical-media (CD/DVD/Blu-ray)
backup application, MIT-licensed, distributed at github.com/LoopyLuci/DiskRipper.

## When to Use

- Any edit, build, test, or debug work inside the DiskRipper workspace
- UI work on the native egui app (`diskripper-app`)
- Filesystem parsing / detection changes in `diskripper-core`
- Release, CI, or documentation updates for the DiskRipper repo

## Architecture (settled — do not re-propose)

- `diskripper-core` — pure Rust backend: rip engine, drive scanner, filesystem
  parsers (ISO 9660/UDF), ML pipeline, settings, job manager.
- `diskripper-app` — 100% native egui/eframe GUI. UI commands/events travel over
  `std::sync::mpsc` channels to worker threads; see the `rust-egui-native-desktop`
  skill for the egui patterns and pitfalls.
- No Tauri, no React, no webview. The user rejected browser-engine UIs
  ("that is not a native app") — do not re-add web tech to fill UI gaps.

## Always-on rules

- **Repo name is exactly `DiskRipper`.** No suffixes, numbers, or version
  markers. When reporting state, write "commit <hash>" — appending `@<hash>`
  to the repo name reads as a version number and gets challenged.
- **Every UI control must call a real core API.** A button whose handler only
  sets a status string ("Loading...") is unfinished work and will be sent back.
  Wire controls to `RipEngine` / `AudioCdReader` / `MlPipeline` /
  `SettingsManager` and surface real results (track lists, checksums,
  confidence scores, saved settings).
- **Verify before claiming done, then commit AND push:**
  `cargo test --release --workspace` (expect 50 passing) →
  `cargo build --release -p diskripper-app` → launch the exe and confirm via
  `tasklist` → `git add -A && git commit && git push`. GitHub is the
  distribution channel; the user expects work on origin/main, not just local.

## Procedure

1. Inspect current state before changing anything: `git status --short`,
   build, tests.
2. Edit `diskripper-core` and/or `diskripper-app`.
3. `cargo test --release --workspace`
4. `cargo build --release -p diskripper-app`
5. Kill any running instance (`taskkill //F //IM diskripper-app.exe`), launch
   with `cmd.exe /c "start C:\Projects\DiskRipper\target\release\diskripper-app.exe"`,
   confirm with `tasklist | grep diskripper`.
6. Commit and push.

## Pitfalls

- **Joliet detection offsets** — see `references/filesystem-parsing.md`.
- **CI builds the native app directly.** `.github/workflows/ci.yml` runs
  `cargo build --release --target <triple> -p diskripper-app` on
  ubuntu/windows/macos runners. No Node, no Tauri steps.
- **Settings live outside the workspace.** `SettingsManager` reads/writes
  `settings.json` under `%APPDATA%\DiskRipper`; the app crate has no
  `dirs`/`directories` dependency, so resolve the dir with
  `std::env::var("APPDATA")`.
