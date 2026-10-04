---
name: ghosthand
description: Use the Windows desktop like a human — see the screen via screenshots and act with mouse/keyboard. Use whenever the user wants the agent to operate GUI applications (open apps, click buttons, type into windows, automate workflows the way a human would). Provides human-like mouse curves, realistic typing with typos, and a background screen watcher for parallel see-while-acting.
---

# Ghosthand skill

Operate the Windows desktop the way a human does — eyes (screenshots) + hands
(mouse/keyboard input via `user32.dll`).

## When to use

Invoke this skill when the user wants the agent to control the desktop:
- "open <app>", "click on …", "type … into <window>"
- automating a flow that has no API (taskbar, file explorer, third-party apps)
- demos of GUI automation

Don't use it for tasks that are easier via direct shell commands (e.g. running
`notepad.exe` via `Start-Process` is fine; you only need this skill when the
user wants the path-via-clicks behavior).

## Files

- `Ghosthand.ps1` — public functions (see header inside the file)
- `watcher.ps1` — background screenshot daemon

Always source the module before use:

```powershell
. "$HOME\.copilot\skills\ghosthand\Ghosthand.ps1"
```

## Core principles (READ BEFORE EACH TASK)

### 1. Behave like a human, not a script

- **Mouse: use `Click-MouseHuman` / `Move-MouseHuman`** by default. They
  produce a curved, eased path with pixel jitter — the user sees the cursor
  travel. Plain `Click-Mouse` teleports and looks robotic; reserve it only
  for invisible/off-screen prep.
- **Typing: use `Send-Text`** (the default). It paces at ~70 WPM, varies
  per-key timing, occasionally hits adjacent QWERTY keys and corrects with
  backspace. Use `Send-Keys` only for special keys (`{ENTER}`, `{TAB}`, etc.)
  and `Send-Raw` only when you specifically need an instant paste-like dump
  (rare).
- Tune knobs only when needed: `-WpmAvg`, `-TypoProb`, `-PauseProb`.
  Defaults already feel natural — don't crank `TypoProb` above ~0.05.

### 2. Batch actions, verify at milestones

Do not do `action → screenshot → view → action → screenshot → view`. That's
slow, robotic, and noisy. Instead:

- **Plan the next 2-6 actions** based on the current screenshot.
- **Execute them in a single PowerShell call** using the helpers above.
- **Only screenshot + view at meaningful milestones** (e.g., after the app
  finishes opening, after a save dialog appears).

Example — opening Notepad and typing a sentence is **one** action batch,
followed by **one** verification screenshot.

### 3. See-while-acting via the watcher

For long action sequences, start the screen watcher once at the beginning:

```powershell
. "$HOME\.copilot\skills\ghosthand\Ghosthand.ps1"
Start-ScreenWatcher    # writes state\current.png every ~250ms
```

Then issue actions in PowerShell calls *and*, in **the same tool-call turn**,
`view` the file `~/.copilot/skills/ghosthand/state/current.png`. The image
the agent sees is at most ~250ms stale — effectively concurrent vision +
action. No manual `Capture-Screen` step needed.

Stop the watcher when done: `Stop-ScreenWatcher`.

### 4. Parallelism guidance for the agent

- Issue PowerShell action sequences and `view current.png` **in parallel**
  (in the same tool-call response) whenever both are independent.
- Do NOT serialize a screenshot capture, then view, then next action — let
  the watcher handle capture in the background.
- Remember: actions take real human-paced time (typing 30 chars ≈ 5s).
  During that time, no extra agent work is needed; just await completion.

### 5. Coordinate hygiene

- The module sets per-monitor DPI awareness, so screenshot pixel coords
  match `SetCursorPos` coords. **However** the rendered screenshot you
  *see* may be displayed at a different scale by the viewer — do NOT
  eyeball pixel coords from a rendered screenshot. Instead, use the UIA
  locator (`Find-UIElement` / `Click-UIElement`) to get exact screen-space
  rectangles by name. Reserve manual coordinates for cases where UIA
  cannot enumerate the target.
- Always re-locate after a window has been moved/closed/resized; never
  reuse stale coordinates across long pauses.
- Multi-monitor: only the primary screen is captured by default.

### 6. Things that block screen capture

Windows blocks screenshots on the secure desktop. If the screen looks black
or you see the lock screen, abort gracefully and tell the user.

## Behavioral realism

`Send-Text` uses **bigram-aware log-normal keystroke timings** by default
(common bigrams "th","he","in" run fast; same-finger / shift / digit /
punctuation slower). Pass `-NoBigramTiming` to revert to plain log-normal
jitter.

`Move-MouseHuman` adds **8–13 Hz sinusoidal tremor** along the path
(matches real-muscle frequency) and a 50–150 ms **sub-pixel correction**
phase at the end. Disable individually with `-NoTremor` /
`-NoSubpixelCorrection`.

`Click-MouseHuman` performs a `-PreHoverMs` **micro-jitter dwell** at the
destination before mousedown (default ~80–220 ms log-normal). Hesitate
and hold timings are also log-normal now.

`Scroll-MouseHuman` scrolls in 1–3 bursts with reading pauses between and
an ~18 % chance of a small reverse "re-read" backtrack. Disable with
`-NoBacktrack`.

`Add-ReadingDelay -Text "..."` pauses by content length / ~240 wpm
reading speed (with log-normal jitter). Call after a screen change before
acting.

Internal helpers exposed for scripts:
`_LogNormalMs -MedianMs -Sigma -MinMs` (Box-Muller sampler) and
`_TypingDelayMs -Prev -Curr -BaseMs` (bigram-aware delay).

### Realism techniques applied

| Concern | Technique |
|---|---|
| Mouse trajectory shape (Bézier vs straight line) | Tremor + overshoot + sub-pixel correction |
| Click-position-too-perfect-center | `-PaddingPercent` (random in bbox) |
| Inter-keystroke timing variance | Bigram + log-normal cadence |
| Reading-delay-after-page-change | `Add-ReadingDelay` |
| Linear scroll patterns | Bursty scroll w/ backtrack |
| `event.isTrusted` check | OS-level injection sets this true |
| `navigator.webdriver` flag | N/A — no WebDriver / CDP attachment |

### What is out of scope

- **Network-layer signals** (TLS / HTTP-2 fingerprint, IP reputation,
  account history) — not addressable from an OS-level input layer
- **CAPTCHAs** — designed for this; the skill detects and surfaces them
  but never attempts to solve
- **Kernel-level anti-cheat** — synthetic input sets a flag visible to
  kernel drivers. **Don't use this skill for games.**
- **Enterprise device-fingerprint stacks** with persistent IDs across
  sessions

## Speed: agent execution patterns (READ THIS — biggest realism win)

**The fundamental cost is not action execution; it is the LLM "think" time
between agent tool calls (~10–20 s per call).** Optimizing for speed
therefore means *minimizing the number of agent decision points*, not
spawning more agents.

### Why fewer agents is faster (counterintuitive but real)

It's tempting to "parallelise" by spawning a Brain agent that plans and a
Doer subagent that executes, with the two coordinating via a SQL queue.
Empirically this is **slower**, not faster:

| Measurement | Result |
|---|---|
| Bundle's own PS execution | 2.0 s |
| Total time from queue → done (bundle 1) | **55 s** |
| Tool calls the Doer makes per bundle | 3 (sql + ps + sql) |
| LLM-thinking overhead per bundle | **~53 s** |

Spawning a subagent **multiplies** the per-action LLM tax rather than
amortising it. Two agents thinking sequentially is *worse* than one.
The "Brain plans while Doer executes" overlap exists but is swamped by
per-decision LLM latency on both sides.

### What is actually parallel and does help

| Mechanism | Real parallelism? | When to use |
|---|---|---|
| `Start-ScreenWatcher` (separate OS process) | ✅ yes | Always — vision is free |
| `Invoke-ActionBatch` in a single PS call | ✅ yes | Any flow with ≥3 UI actions |
| Whole-flow PowerShell script in one tool call | ✅ yes | Multi-step deterministic flows |
| Multiple agents (Eyes/Brain/Doer/Hands) | ❌ no — adds LLM tax | Almost never |

### Recommended patterns (in order of preference)

#### 1. Whole-flow script (BEST for known flows)

For a multi-step task whose shape is known up-front, write the entire
flow as **one PowerShell script** and run it in **one** tool call:

```powershell
. "$HOME\.copilot\skills\ghosthand\Ghosthand.ps1"
Start-ScreenWatcher

# everything below is one agent decision
$br = Open-Url 'https://example.com/dashboard'
$null = Wait-ForUrlContains -Pattern '/login' -ProcessId $br.ProcessId
Click-UIElement -NameLike 'Continue with Google' -PaddingPercent 50 | Out-Null
$null = Wait-ForUrlContains -Pattern 'accounts.google.com' -ProcessId $br.ProcessId
Click-UIElement -NameLike 'your.email@example.com' | Out-Null
$null = Wait-ForUrlContains -Pattern '/home/overview' -ProcessId $br.ProcessId -TimeoutMs 15000
Click-UIElement -Name 'project-name' -Kind Hyperlink | Out-Null
# ... etc, all in one shell call

Stop-ScreenWatcher
```

15 actions → 1 LLM decision → ~30–45 s wall clock (mostly real human-paced
input timing). This is the canonical fast path.

#### 2. `Invoke-ActionBatch` for ref-driven flows

When you have a UIA snapshot with refs, drive the whole flow through
`Invoke-ActionBatch` with `wait` / `snapshot` actions interleaved:

```powershell
Get-UIASnapshot -ProcessId $calc.ProcessId | Out-Null
Invoke-ActionBatch -Actions @(
    @{type='invoke';     ref='w1e25'},
    @{type='wait';       ms=200},
    @{type='invoke';     ref='w1e45'},
    @{type='invoke';     ref='w1e33'},
    @{type='invoke';     ref='w1e46'},
    @{type='invoke';     ref='w1e36'},
    @{type='wait';       ms=300},
    @{type='snapshot';   pid=$calc.ProcessId}
)
```

#### 3. Subagent for LONG flows (only when context-clearing matters)

If a task is long enough that the conversation context becomes the
bottleneck (≥30 actions, lots of intermediate output), delegate the
entire flow to a `general-purpose` subagent **with the whole-flow script
written by the main agent already inside the prompt**. The subagent's
job is to run the script, capture its output, and return a summary —
*not* to make per-action decisions.

#### 4. The multi-agent SQL queue (DO NOT use for speed)

The infrastructure exists (`pc_action_queue`, `pc_scene_state`,
`pc_plan_state` tables; `Invoke-ActionBundle`, `New-ActionBundle`,
`Get-SceneDigest` helpers) and works correctly. It's useful for
*fail-tolerant* multi-agent flows (e.g., a long-running background
"PC butler" that resumes from queue state after a crash), but it is
**not faster than option 1**. The architectural design is documented
here for completeness; do not reach for it as a latency optimization.

### Concrete latency budget (revised, honest)

| Pattern | Wall clock for 15-step CF task |
|---|---|
| Sequential main-agent loop, screenshot every step | ~5–8 min |
| Multi-agent (Brain+Doer) with per-bundle agent decisions | **~10+ min (worse)** |
| Single agent, `Invoke-ActionBatch` of refs | ~60–90 s |
| **Single agent, whole flow as one PS script (BEST)** | **~30–45 s** |

The speed limit is set by physical typing time + a single LLM-decision
overhead. Anything more than ~1 LLM decision per "block of work" is
wasted budget.

## Function reference

```text
Vision
  Capture-Screen [-Path]              # save PNG and return its path
  Start-ScreenWatcher [-IntervalMs]   # background continuous capture
  Stop-ScreenWatcher                  # stop the daemon

Mouse — instant (use sparingly)
  Move-Mouse        X Y
  Click-Mouse       X Y [-Button left|right] [-Times N]

Mouse — humanized (DEFAULT)
  Get-MousePos                         # {X,Y}
  Move-MouseHuman        X Y           # eased Bezier travel
  Click-MouseHuman       X Y | -Element $obj
                              [-Button] [-Times] [-Rapid]
                              # -Element : prefer UIA ClickablePoint, fall back to
                              #            randomised point in element's bounding rect
  DoubleClick-MouseHuman X Y [-Button]
  RightClick-MouseHuman  X Y
  Hover-MouseHuman       X Y [-DurationMs]
  Drag-MouseHuman        -FromX -FromY -ToX -ToY [-HoldMs]   # try/finally — release guaranteed
  Scroll-MouseHuman      [-X -Y] -Notches N [-Horizontal]    # +ve = up/right

Keyboard — text
  Send-Text   "string"               # humanized typing w/ typos (DEFAULT)
  Send-Keys   "{ENTER}"              # SendKeys passthrough for special keys
  Send-Raw    "string"               # paste-like, no humanization (rare)

Keyboard — chords & raw keys
  Send-Hotkey  "ctrl+shift+s"        # OR -Keys @('Ctrl','Shift','S')
                                      # OR -Keys 'ctrl+Home'  (combo strings flattened)
                                      # supports ctrl/shift/alt/win, letters, digits,
                                      # F1-F12, arrows, home/end/pageup/pagedown,
                                      # tab/enter/esc/space/backspace/delete/insert/apps
  Press-VK     0xNN                  # press a virtual-key code
  Press-Win                          # tap Windows key
  Hold-Key     0xNN                  # press down (no auto-release)
  Release-Key  0xNN                  # release a held key

Common in-app shortcuts (one-liners)
  Copy / Paste / Cut / Select-All / Save-File / Undo / Redo
  Find-In-App / Print-File / New-Tab / Close-Tab

System / window shortcuts
  Alt-Tab / Alt-F4 / Show-Desktop / Open-Explorer / Task-View
  (Win+L is intentionally NOT exposed — it would lock the user out.)

Safety
  Reset-InputState                    # release all modifiers + mouse buttons
                                      # call this if a chord/drag was interrupted

Window management (operate on HWND from Find-Window)
  Get-Windows [-IncludeUntitled]      # all visible top-level windows
  Find-Window  -Title "*..." [-ClassName ...] [-ProcessName ...] [-ProcessId N] [-Exact] [-Index]
  Find-Windows ...                    # plural, returns all matches
  Wait-ForWindow ...                  # poll Find-Window until found / timeout
  Focus-Window           -Handle      # returns {Success, Reason} — best-effort
  Wait-ForForegroundWindow -Handle    # confirm focus actually landed
  Minimize-Window / Maximize-Window / Restore-Window  -Handle
  Close-Window           -Handle      # polite WM_CLOSE — app may prompt to save
  Move-Window            -Handle -X -Y
  Resize-Window          -Handle -Width -Height

UIA — find/inspect/wait on UI elements
  Find-UIElement  -Name "..." [-NameLike] [-NameRegex] [-NameAny @("a","b")]
                  [-ClassName] [-AutomationId] [-ProcessId]
                  [-Kind Button|MenuItem|Edit|Window|CheckBox|RadioButton|ComboBox|
                         Hyperlink|TabItem|TreeItem|ListItem|Text|Any]
                  [-Index N] [-TimeoutMs N]
                  [-AutoScroll Top|Bottom|Both]
                  # returns {Name, AutomationId, ClassName, ControlType,
                  #          ProcessId, NativeHandle,
                  #          X, Y, Left, Top, Width, Height,
                  #          HasClickablePoint, Element}
                  # NameLike  = glob substring (greedy)
                  # NameRegex = case-insensitive regex (stricter)
                  # NameAny   = exact match against any of the supplied names
                  # AutoScroll Top   : send Home once, then rescan
                  # AutoScroll Bottom: send End once, then rescan
                  # AutoScroll Both  : Home -> End -> Home (only when needed)
                  # X/Y prefer the UIA ClickablePoint when available
  Find-UIElements ...                 # plural — same matchers
  Click-UIElement -Name "..." | -Element $obj | -Ref "w1e5"
                  [-Button] [-Times] [-Instant]
                  [-PaddingPercent N]   # 0=any pt in bbox, 100=exact center, default 60
                  [-HesitateMs N] [-HoldMs N]
                  [-EnsureVisible]      # scroll into screen viewport first
  Invoke-UIElement -Name "..." | -Ref "..." | -Element $obj  [-NoFallback]
                                      # programmatic UIA Invoke/Toggle/Select
                                      # works on hidden/unfocused windows
  Wait-ForUIElement     ... [-TimeoutMs N] [-AutoScroll Top|Bottom|Both]
                            [-OnPoll {…}]
  Wait-ForUIElementGone ... [-OnPoll {…}]
                                      # OnPoll runs each iteration. Use sparingly:
                                      # most modern web UIs push updates without
                                      # reload, so passive polling (no -OnPoll)
                                      # is normally what you want.
  Wait-PageInteractive [-ProcessId N] [-TimeoutMs 4000]
                       [-Kind Hyperlink|Button|Edit|Text|Any]
                       [-MinElements 1]
                                      # use after Focus-Window / tab switches
                                      # before querying the UIA tree, instead of
                                      # arbitrary Start-Sleep waits.
  Get-UIElementText  -Element $el     # tries ValuePattern, TextPattern, then Name
  Set-UIElementText  -Element $el -Text "..." [-NoFallback]
                                      # ValuePattern w/ typing fallback (Ctrl+A → Send-Text)

UIA snapshot tree (RECOMMENDED for agent use)
  Get-UIASnapshot  [-Title "..."] [-ProcessId N] [-Handle $h] [-MaxDepth 8]
                                      # returns indented text tree with refs
                                      # like "- button \"Equals\" (id=...) [ref=w1e36]"
                                      # refs are valid until next snapshot call
  Get-UIElementByRef  -Ref "w1e36"    # resolve ref to element object

Batch actions
  Invoke-ActionBatch -Actions @(
    @{type='click';      ref='w1e36'},
    @{type='invoke';     ref='w1e36'},          # UIA Invoke (no physical click)
    @{type='doubleclick'; name='File'},
    @{type='rightclick'; x=100; y=200},
    @{type='type';       text='hello'; wpm=70},
    @{type='hotkey';     combo='ctrl+s'},
    @{type='key';        keys='{ENTER}'},
    @{type='wait';       ms=200},
    @{type='wait';       name='Save dialog'; ms=5000},
    @{type='snapshot';   pid=1234},
    @{type='move';       ref='w1e36'},
    @{type='scroll';     notches=-3}
  )
                                      # returns @[{Action, Status, Result}, ...]

Idle behavior
  Start-IdleMouseMoves [-DurationMs N]   # random small moves to look "alive"

Reading delay (post-screen-change pause)
  Add-ReadingDelay  [-Text "..."] [-WpmReading 240] [-MinMs 350] [-MaxMs 4000]

Realism helpers
  _LogNormalMs   -MedianMs N [-Sigma 0.3] [-MinMs 1]   # Box-Muller log-normal
  _TypingDelayMs -Prev <char> -Curr <char> -BaseMs N   # bigram-aware delay

Multi-agent coordination (see "Speed" section — DO NOT use for latency,
only for fail-tolerant flows)
  New-ActionBundle    -Description "..." -Ps "..."
                      [-Preconditions "..."] [-Postconditions "..."] [-PostTimeoutMs N]
                                          # build a JSON bundle for the queue
  Invoke-ActionBundle -BundleJson "..."   # run a bundle: precond → ps → postcond
                                          # returns {ok,error,result,precond,postcond}
  Get-SceneDigest                         # quick JSON: hash, active window, url
                                          # use as a change-detector for any
                                          # downstream perception consumer

Browser layer (for AI-assistant browsing — drives a real Chrome/Edge/Firefox
window via OS keyboard, NOT WebDriver/CDP, so navigator.webdriver stays false)
  Get-BrowserWindow                                  # current Chrome/Edge/Firefox/Brave window
  Wait-ForBrowserWindow [-TimeoutMs N]
  Open-Url        -Url "https://..." [-NewTab] [-NewWindow] [-WaitLoadMs N]
  Wait-PageLoad   [-Handle $h] [-TimeoutMs N] [-StableMs 900]
  Wait-ForUrlContains -Pattern "/path"  [-ProcessId N] [-TimeoutMs N]
                                                     # waits for address bar to contain pattern
  Get-PageText    [-ProcessId N] [-MaxChars 12000]   # UIA text extraction
  Click-LinkByText -Text "..."         [-Partial]      # exact (or glob with -Partial)
  Click-LinkByText -Regex "..."                         # case-insensitive regex
  Click-LinkByText -NameAny @("A","B")                  # exact match against any
                   [-Invoke] [-ProcessId N]
  Fill-FieldByName -Name "Search" -Text "..." [-Partial] [-Clear] [-ProcessId N]
  Find-CaptchaPresentV2 [-ProcessId N]               # refined detector (preferred)
  Find-CaptchaPresent   [-ProcessId N]               # legacy, may false-positive on brand names
  Find-DropdownByLabel  -Label "Destination" [-ProcessId N] [-MaxYDistance 200]
                                                     # for React-Select-style custom dropdowns
                                                     # not exposed as UIA ComboBox
  Get-BrowserUrl  [-ProcessId N]                     # read current address bar
  Get-BrowserTabs [-ProcessId N]                     # list tabs ({Index,Title,IsActive,X,Y,Width,Element})
  Switch-BrowserTab -Index N | -TitleLike "..."      # mouse-click on the tab strip (DEFAULT)
                                  [-UseHotkey]      # opt into Ctrl+1..8 / Ctrl+9 instead
  Close-BrowserTab  [-Index N | -TitleLike "..." | -Current]

Realism / timing
  Get-HumanDelay -MedianMs N [-Sigma 0.3] [-MinMs 1] # log-normal sample (no sleep)
  Add-ReadingDelay [-Text "..."] [-WpmReading 240]   # sleeps for a "reading" pause

Clipboard (PowerShell builtins)
  Get-Clipboard
  Set-Clipboard -Value "..."
```

## Pitfalls and caveats

- **Don't reload pages that auto-update.** Most modern web UIs (CI status,
  PR checks, dashboards, chat) push state changes via long-poll or
  WebSocket; firing F5 from `Wait-ForUIElement -OnPoll` thrashes the page,
  resets scroll, and is visible to the user. Use passive polling
  (no `-OnPoll`) for these, and reserve `-OnPoll` for cases where the
  caller genuinely needs to drive a control between checks.
- **Don't `Send-Hotkey 'End'` reflexively to find an element.** That
  jumps to the bottom of the document and is jarring. Prefer
  `-AutoScroll Top` (the typical case — header chrome lives at the top)
  and only `-AutoScroll Bottom` when you specifically need a footer-
  anchored element. `-AutoScroll Both` should be a last resort.

- **Snapshot refs are tied to a single `Get-UIASnapshot` call.** Each
  snapshot resets the ref counter and rebuilds the map. If you take a
  fresh snapshot, **all old refs are invalidated**; re-read the new tree
  to get the new refs. Don't cache refs across snapshots.
- **`Invoke-UIElement` is more reliable than `Click-UIElement`** for
  UIA-friendly buttons — it doesn't require the window to be focused or
  visible, and ignores cursor obstructions. Prefer it for deterministic
  workflows (button presses, menu items). Use real clicks only when you
  actually want to mimic a human, or when the control doesn't expose
  InvokePattern.
- **Don't eyeball pixel coords from a rendered screenshot.** The viewer
  rescales the image. Use `Get-UIASnapshot` + `-Ref`, or
  `Find-UIElement` / `Find-Window` for exact screen-space coordinates.
- **Scroll target depends on OS setting** "Scroll inactive windows when I
  hover over them". If results feel wrong, focus the window first via
  `Focus-Window`.
- **`Focus-Window` is best-effort.** Foreground locks, elevation
  boundaries, virtual desktops, and minimized targets can prevent it.
  Always check `.Success` and use `Wait-ForForegroundWindow` to confirm.
- **`Click-UIElement -Name "OK"` is ambiguous** when multiple "OK"
  buttons exist. Add `-AutomationId`, `-ProcessId`, or `-Index`.
- **Stuck input recovery.** If a script aborts mid-chord/drag, the
  modifier or mouse button can stay logically down. Run `Reset-InputState`
  to clear it.
- **Mixed-DPI multi-monitor** is not extensively tested. The watcher
  captures the primary monitor only; coords are physical pixels under
  per-monitor-V2 awareness.

## Safety boundaries

- **Never** type passwords, OTPs, or other secrets into focused windows
  on behalf of the user without a clear, explicit instruction.
- **Don't** screenshot or read text from password fields. Skip them.
- **UAC / secure desktop / lock screen** are invisible to capture and
  uncontrollable via injected input. If a screenshot looks black or the
  user is at the lock screen, abort and tell the user.
- **Win+L** is deliberately not implemented (it would lock the user out
  of their own machine and end the session abruptly).
- **`Close-Window`** uses `WM_CLOSE` (graceful). Do not switch to
  `TerminateProcess` to force-close — apps would lose unsaved work.

## Recipes

### Open an app via the Start menu (mouse-driven, locator-based)

```powershell
. "$HOME\.copilot\skills\ghosthand\Ghosthand.ps1"
Click-UIElement -Name "Search"     # taskbar Search box (UIA-located, no guess)
Start-Sleep -Milliseconds 700
Send-Text "notepad"
Start-Sleep -Milliseconds 600
Send-Keys "{ENTER}"
```

### Open Start via Win key (faster, less mouse movement)

```powershell
Press-Win
Start-Sleep -Milliseconds 700
Send-Text "calc"
Send-Keys "{ENTER}"
```

### Type a paragraph into a focused editor

```powershell
Click-MouseHuman -X 800 -Y 400          # focus the editor area
Send-Text "Dear team, please review the attached design document."
Send-Keys "{ENTER}{ENTER}"
Send-Text "I'd appreciate feedback by Friday. Thanks!"
```

### Right-click + click a context menu item (with watcher)

```powershell
Start-ScreenWatcher
Click-MouseHuman -X 1200 -Y 500 -Button right
# ... in the SAME tool-call turn, agent reads state\current.png and finds
# "Properties" item, then issues:
Click-MouseHuman -X 1245 -Y 612
Stop-ScreenWatcher
```

### Snapshot + batch (preferred for deterministic workflows)

```powershell
$calc = Find-Window -Title 'Calculator'
Get-UIASnapshot -ProcessId $calc.ProcessId | Set-Content "$env:TEMP\snap.txt"
# (agent reads snap.txt, picks refs)

Invoke-ActionBatch -Actions @(
    @{type='invoke'; ref='w1e25'},   # Clear
    @{type='invoke'; ref='w1e45'},   # Seven
    @{type='invoke'; ref='w1e33'},   # Multiply by
    @{type='invoke'; ref='w1e46'},   # Eight
    @{type='invoke'; ref='w1e36'},   # Equals
    @{type='wait';   ms=200}
)
$display = Get-UIElementByRef -Ref 'w1e13'
Get-UIElementText -Element $display     # -> "Display is 56"
```

### Idle "alive" behavior between actions

```powershell
Click-UIElement -Ref 'w1e35'      # Plus
Start-IdleMouseMoves -DurationMs 1500   # mouse drifts naturally
Click-UIElement -Ref 'w1e36'      # Equals
```

### Browse the web (AI-assistant recipe)

```powershell
. "$HOME\.copilot\skills\ghosthand\Ghosthand.ps1"

# 1. Navigate. Open-Url focuses an existing browser if any, else launches default.
$br = Open-Url 'https://duckduckgo.com'

# 2. Always check for CAPTCHAs / "checking your browser" before acting
$cap = Find-CaptchaPresent -ProcessId $br.ProcessId
if ($cap.Detected) {
    Write-Warning "Challenge detected: $($cap.Sign). Pausing for human."
    return
}

# 3. Reading-delay so the page-load -> first-action timing looks human
Add-ReadingDelay -Text 'Privacy, simplified.'

# 4. Find the search input (semantic, not pixel-based)
Fill-FieldByName -Name 'Search privately' -Text 'climate change effects' -ProcessId $br.ProcessId | Out-Null
Send-Keys '{ENTER}'

# 5. Wait for results, then read the page
Wait-PageLoad -Handle $br.Handle -TimeoutMs 12000 | Out-Null
Add-ReadingDelay -MinMs 1200
$pageText = Get-PageText -ProcessId $br.ProcessId -MaxChars 4000

# 6. Click a specific result link by visible text
Click-LinkByText -Text 'NASA' -Partial -ProcessId $br.ProcessId
Wait-PageLoad -Handle $br.Handle | Out-Null
Add-ReadingDelay -Text $pageText.Substring(0, 800)

# 7. Scroll to read more (bursty + reading pauses + chance of backtrack)
Scroll-MouseHuman -Notches -8

# 8. New tab + another search
$br2 = Open-Url 'https://wikipedia.org' -NewTab
```

#### Key principles for the browse loop

- **Always `Find-CaptchaPresent` before each new action**. If detected,
  pause and surface to the user — the skill will not auto-solve them.
- **`Open-Url` types the URL via Ctrl+L** with bigram-aware rhythm,
  rather than instantly navigating via shell. This is what real users do.
- **Use `Get-PageText` instead of OCR** for normal sites. Chrome/Edge
  expose page text via UIA. Chrome auto-enables accessibility on the
  first UIA query (one-time ~500ms delay).
- **`Add-ReadingDelay` between every page-change and action**. Real
  users need 1-3s to perceive new content before clicking.
- **Drive a normal Chrome/Edge/Firefox** — NOT Selenium / Playwright /
  Puppeteer. Those tools set `navigator.webdriver=true`, which is
  trivially detectable. OS-level injection into a normal browser leaves
  `navigator.webdriver` `false`.
- **`Click-LinkByText -Partial`** finds links by visible text (not pixel
  position) — robust to layout shifts and DPI changes.
- **Form fields:** prefer `Fill-FieldByName` (UIA accessible name like
  `aria-label` or `placeholder`) over coordinate clicks.

## Cleanup

Always `Stop-ScreenWatcher` when done with a task that started one — the
daemon is a detached process and survives this session.
