---
name: timermeet-exe-packager
description: Rebuild TimerMeet.exe from the current Python source with PyInstaller, using the project's icon and dependencies. Use whenever the user asks to recompile/rebuild the .exe, or after any change to timermeet_app/ or timermeet.py that should ship as a binary.
---

# TimerMeet Exe Packager

## Overview

Produce a single-file Windows executable (`TimerMeet.exe`) at the repository root, next to `timermeet.py` and `computer_pc_10894.ico`, using PyInstaller.

## Workflow

1. Make sure dev dependencies are installed: `pip install -r requirements-dev.txt`.
2. Run the build script from the repo root:
   ```powershell
   python build_exe.py
   ```
   This runs PyInstaller with `--onefile --windowed --icon computer_pc_10894.ico --collect-submodules plyer`, then copies `dist/TimerMeet.exe` to the repo root.
3. Launch `TimerMeet.exe` once to confirm it starts without an immediate crash (check `data/timermeet.log` for exceptions), then close it.
4. Clean up intermediate build output (do **not** commit these):
   ```powershell
   Remove-Item -Recurse -Force build, dist, TimerMeet.spec -ErrorAction SilentlyContinue
   ```
5. Confirm `assets/audio/*.mp3` and the `data/` folder still exist alongside `TimerMeet.exe` -- they are read as loose files at runtime (`timermeet_app/storage.py::base_dir()` resolves to the exe's own folder when frozen), not bundled into the single-file archive. The exe will start but alarms will fall back to synth-only beeps if `assets/audio/` goes missing.

## Why each flag exists

- `--onefile --windowed`: a single double-clickable exe with no console window (this is a GUI app; the console would just be a stray black window, and the crash handler in `timermeet.py` already shows a message box on failure).
- `--icon computer_pc_10894.ico`: the icon already checked into the repo root; keep using this same file unless the user provides a new one.
- `--collect-submodules plyer`: `plyer` picks its OS notification backend (`plyer.platforms.win.notification`) via a runtime string import PyInstaller's static analysis can't see on its own.

Note: the UI is plain `tkinter`/`ttk` (no CustomTkinter, no `--collect-all` needed for it) -- see SDD.md's "Por qué v2.0.1 dejó de usar CustomTkinter" for why that dependency was removed (it added 20+ seconds to startup with a real-sized meeting list).

## What to commit vs ignore

- **Commit**: the rebuilt `TimerMeet.exe` at the repo root (the user explicitly wants the compiled binary tracked next to the source).
- **Never commit**: `build/`, `dist/`, `*.spec`, `__pycache__/` (already in `.gitignore` -- these are large, regenerate-on-demand intermediates).
