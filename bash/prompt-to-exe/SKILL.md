---
name: prompt-to-exe
description: >
  Turn a natural-language app idea ("an app that...") into a working,
  double-clickable Windows .exe — with ZERO git, GitHub, terminal, or build
  knowledge required from the user. Covers stack choice (default:
  Python + Tkinter + PyInstaller; alternatives: pywebview/Tauri, .NET
  WinForms), Python bootstrap via winget/py launcher, minimal project
  scaffold, implementation rules, onedir vs onefile, install folder +
  Desktop shortcut, smoke test, startup measurement, antivirus
  false-positive caveats, and delivery. Use when the user asks to "make an
  app from my prompt", "create an exe", "build a Windows app", "build an app
  from a prompt", "assemble the exe", or reports that a generated app "didn't
  work" / "won't open on Windows".
compatibility: Windows 10/11 host; Python 3.11-3.14; PyInstaller >= 6
metadata:
  created: 2026-09-05
  updated: 2026-10-07
---

# prompt-to-exe — from one-line prompt to double-clickable .exe

Mission: the user describes an app in plain language; the task is complete
only when a verified .exe is sitting in a folder the user knows how to reach.
The user is assumed to know NOTHING about git, terminals, or packaging — the
agent runs every command; the user only receives the finished file.

## 0. Non-negotiables

- DONE means: exe exists on disk AND was smoke-launched successfully.
  A project folder without a built exe is NOT done (No Fake Completeness).
- **Starting is not working.** A packaged build has no console, so it can look
  healthy while doing nothing at all: window up, process alive, exit code 0.
  Every app needs one cheap signal that proves it is doing its job, and the
  smoke test must read that signal, not the process list. In a stream/worker
  app that is a counter the callback bumps; in a CLI it is the output. "It
  opened" has never been evidence.
- Never make the user run commands or edit files. The agent does it all.
- Never advise disabling antivirus globally. A targeted folder exclusion is
  offered only after a false positive is actually observed.
- Ask at most ONE clarifying question (GUI vs console, or the one missing
  core feature). Everything else: pick sensible defaults and STATE them.

## 1. Stack decision (default covers ~95% of cases)

| Case | Stack | Why |
|---|---|---|
| Default: small GUI tool, one window | Python 3.11-3.14 + Tkinter (stdlib) + PyInstaller | no node/npm, no .NET SDK; most robust packaged path |
| Web-style UI demanded (HTML/CSS) | Python + pywebview | Tauri only if the Rust toolchain is ALREADY present |
| User explicitly wants C#/native | .NET 8 WinForms, `dotnet publish -r win-x64 --self-contained -p:PublishSingleFile=true` | check `dotnet --version` first; skip if absent |

Do NOT offer Electron for simple tools — 150-300 MB for a to-do list is a
failure of judgment, not a feature.

## 2. Environment check (agent runs; handle every failure branch)

```bash
py -3 --version          # py launcher ships with python.org installers
```
- If `py` is missing, try `python --version`. Beware the WindowsApps store
  stub: `python` may open the Microsoft Store instead of running (known trap).
- Any 3.11+ interpreter is fine, including a 3.14 one — the 3.11-3.13 ceiling
  this skill used to state was never a real constraint (verified: a PyInstaller
  6.22.3 build on Python 3.14.3, numpy 2.5.3, scipy 1.18.1). Only pin a version
  when a dependency has no wheel for the newest one — check `pip download` for a
  `cp3XX` wheel before deciding, rather than pinning the whole project.
- Windows Store Python (`WindowsApps`) can fail in a venv because the launcher
  is a reparse point; prefer a python.org or winget install for the app.
- If neither works: `winget install -e --id Python.Python.3.12 --silent`.
  After a winget install the CURRENT shell has no updated PATH — use the
  full path `%LOCALAPPDATA%\Programs\Python\Python312\python.exe` for this
  session instead of re-reading stale PATH.

## 3. Scaffold (minimal; NO git anywhere in the flow)

```
<project>/
  main.py           # the whole app (single file unless it truly needs more)
  requirements.txt  # third-party deps only (often empty for Tkinter)
  build.bat         # one-click rebuild, see §5
  README.txt        # plain text: what it is, double-click to run, who built it
```

## 4. Implementation rules

- One window, one obvious action. Boring is beautiful.
- GUI apps: no console — build with `--windowed` later; keep all output
  inside the window (message boxes, labels, log pane).
- Console apps that print non-ASCII must set UTF-8 explicitly
  (`sys.stdout.reconfigure(encoding="utf-8")` — see windows-encoding-fixes).
- No network calls, no secrets, no telemetry unless the user asked for them.
- App must exit cleanly when the window closes (Tkinter `mainloop` returns).

## 5. onedir by default, onefile only if the user needs one file

```bash
<venv-python> -m pip install pyinstaller
# default — a folder, starts in about a second
<venv-python> -m PyInstaller --noconfirm --onedir --windowed --name AppName main.py
# only when delivery really is "one file to send someone"
<venv-python> -m PyInstaller --noconfirm --onefile --windowed --name AppName main.py
# console app: drop --windowed
```

`--onefile` is a nice single artefact and a bad user experience: it unpacks its
whole payload into `%TEMP%` on **every** launch, which costs two to five seconds
before the window appears. `--onedir` starts instantly. Measured on a real app
(Python 3.14, numpy + scipy + sounddevice, 147 MB installed): onefile ~2.9 s to
window, onedir ~1.0 s. Choose onefile only when a single file is a requirement,
and say the trade-off out loud when you do.

- Create the venv INSIDE the project (`python -m venv .venv`); on Windows the
  interpreter is `.venv\Scripts\python.exe` (never `bin/`).
- Verify the artefact exists (`dist\AppName\AppName.exe` for onedir,
  `dist\AppName.exe` for onefile). Size expectations: a stdlib-only Tkinter app
  is 10-15 MB; anything bundling numpy/scipy/PySide is legitimately 100 MB+.
  Do not "fix" a large size, and do not read a tiny one as success — check the
  folder actually contains the interpreter and the libraries.
- Bundle data files explicitly (`--add-data "assets;assets"`), and collect
  packages whose binaries PyInstaller misses (`--collect-all sounddevice`,
  `--collect-all PIL`).
- Smoke test (agent runs): start the built exe, wait for it to settle, then
  read the app's own liveness signal and shut the test instance down. Also run
  the same smoke test **through the delivered shortcut**, not only against the
  raw exe, so the launcher path is covered too. Start implies cleanup: kill the
  test process and confirm nothing is left behind.
- Measure the startup once, from a clean start, and put the number in the
  project README. If the window takes more than ~1.5 s, look for a heavy import
  at module scope — deferring numpy/scipy to first use took one app from 2.9 s
  to 1.0 s on its own.

### Do not run the interactive builder in the background

Keep `build.bat` for the user (it ends with `pause`, which is right for a
double-click and wrong for an agent). To rebuild headlessly, run the same
PyInstaller and install steps directly from the terminal so the exit status is
readable, and keep the log.

## 6. Antivirus false positives (tell the user BEFORE delivery)

PyInstaller onefile exes are frequently flagged by Defender/SmartScreen as
"unrecognized app" — a known packaging limitation, not malware. Say this
up front. If a flag actually happens:
- targeted fix: Windows Security → Virus & threat protection → Exclusions →
  add the project folder (2 clicks, or elevation via request_elevation);
- NEVER suggest turning off protection system-wide.

## 7. Delivery: install folder + Desktop shortcut

An app does not live on the Desktop; it lives in a folder and is *reached*
through a shortcut. Installing into
`%LOCALAPPDATA%\Programs\<AppName>\` keeps one stable path that assets, an
icon and an autostart entry can point at, and survives the user tidying their
Desktop.

- Build, then copy `dist\<AppName>\*` into the install folder (replace the old
  copy; the previous version is recoverable from the rebuilt output if the new
  one turns out bad).
- Create the shortcut with `WScript.Shell` and point its icon at the exe
  (`IconLocation = "…\AppName.exe,0"`). **Refuse non-ASCII paths in that
  PowerShell call** — inline parsing breaks without a BOM and the shortcut
  quietly comes out wrong. Resolve the real Desktop first, since a OneDrive
  redirect is common: `reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop`.
- Keep user data out of the install folder: settings, logs and profiles belong
  in `%APPDATA%\<AppName>`, so reinstalling or moving the app does not lose
  them, and the install folder stays replaceable wholesale.
- Final message template (plain language): where the shortcut is → "Desktop,
  `AppName`", double-click to run, first start takes about a second, and
  "tell me what to change and I rebuild it — no reinstalling needed".

## 8. Iterate

Any change request = edit `main.py` → rebuild → re-smoke-test → re-deliver.
Keep `build.bat` in sync with the exact PyInstaller command used.

## Related skills

- `desktop` part `windows-encoding-fixes` — Windows console/venv/UTF-8 traps
