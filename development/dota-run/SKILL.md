---
name: dota-run
description: >
  How to build and launch the Dota AI Coach WPF overlay locally for manual
  testing, how to verify it is actually rendering (not just that the
  process is alive), and known launch/visibility pitfalls already
  diagnosed in this project. Use whenever asked to run, launch, or test
  the app, or to confirm a UI change actually shows up on screen. This is
  the project-specific companion the generic `run` skill looks for first.
---

# Running the Dota AI Coach overlay

## Build and launch

```bash
cd D:\KAI\proyectos\dota-ai-coach
dotnet build src/DotaAiCoach.UiOverlay/DotaAiCoach.UiOverlay.csproj -c Debug
"src/DotaAiCoach.UiOverlay/bin/Debug/net8.0-windows/DotaAiCoach.UiOverlay.exe"
```

Prefer launching the compiled `.exe` directly in background rather than
`dotnet run` — `dotnet run` has been observed to not reliably surface a
window handle right away in this environment.

Live GSI data requires the config installed in Steam first — see
`docs/GSI_SETUP.md`. Without it the overlay still launches but stays on
"Not connected" until Dota starts sending payloads.

## A running process does not mean the window is visible

This has bitten testing sessions before: `Get-Process` confirming the
process is alive is not proof the WPF window is actually painting
anything on screen. It can exist with valid on-screen coordinates and
still render nothing. Verify in this order:

1. `Get-Process | Where-Object {$_.ProcessName -like '*DotaAiCoach*'}` —
   confirms the process didn't crash. Necessary, not sufficient.
2. A full-screen screenshot taken **immediately** (within 1-2s) after
   launch. Screenshots taken later, while a real Dota match is running,
   can coincide with Dota being in exclusive fullscreen mode — which
   blocks any external overlay at the Windows compositor level,
   regardless of `Topmost="True"`. **Before taking any screenshot, check
   whether the user might be in an unrelated app or call** — a
   full-screen capture exposes whatever is on screen, not just the
   overlay. If there's any doubt, ask first or fall back to step 3
   instead of capturing.
3. To confirm position/size without a screenshot, enumerate windows via
   `EnumWindows`/`GetWindowRect` (P/Invoke) — this returns real WPF
   logical coordinates. Do NOT rely on UI Automation's
   `BoundingRectangle` for this — it reports physical pixels, which reads
   as "thousands of pixels off-screen" on any monitor with DPI scaling
   above 100%, even when the window is correctly positioned.

## Already-diagnosed failure modes (don't re-investigate these)

- **Overlay looks "invisible" during a real match, screenshot shows only
  the game**: almost always Dota running in exclusive fullscreen. Ask the
  user to switch to Borderless Windowed in Dota's Video settings — this
  is an OS/game-mode limitation, not an app bug.
- **Overlay appears thousands of pixels off-screen**: caused by mixing
  `System.Windows.Forms.Screen` (physical pixels) with `Window.Left`/
  `Top` (WPF DIPs/logical units) anywhere in positioning code. Only use
  `SystemParameters.WorkArea` for anything that sets `Window.Left`/`Top`.
- **A stale `window-position.json` from a previous drag test**
  (`%LOCALAPPDATA%\DotaAiCoach\window-position.json`) silently overrides
  the XAML default position on next launch — delete it before testing a
  "does the default position still work" scenario.

## Checking in-progress feature status before testing

Before running a test session, check
`C:\Users\<user>\.claude\projects\D--KAI-proyectos-dota-ai-coach\memory\MEMORY.md`
for a `project_status_*` entry — it tracks what was implemented but not
yet verified live, so testing picks up where the last session left off
instead of re-deriving it from git diff alone.
