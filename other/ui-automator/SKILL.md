---
name: ui-automator
description: >
  Automate any Android device UI over adb using uiautomator screen dumps and
  coordinate-based input. Use this skill whenever a task requires interacting
  with an Android app's UI (tapping buttons, navigating menus, scrolling lists,
  reading on-screen state, verifying verdicts/dialogs) on an emulator, redroid
  container, or physical device reachable via `adb`. Covers the dump → parse →
  locate → tap → verify loop, multi-instance serial hygiene, bottom-sheet and
  scroll-list navigation, and Windows/PowerShell host pitfalls.
---

# Android UI Automation via adb + uiautomator

## Purpose

Drive an Android UI without human fingers: read what is on screen, compute where to
tap, act, and verify the result. Works over plain adb (SSH tunnel, USB, TCP). No
Appium/instrumentation needed — only `adb`, Python 3 (stdlib), and bash.

## Core mental model: the DUMP-TAP-VERIFY loop

Never tap blind. Every interaction follows this loop:

```text
1. STATE   confirm foreground app/window (dumpsys window)
2. DUMP    uiautomator dump /sdcard/x.xml → adb pull
3. PARSE   python scripts/parse_ui.py x.xml
           (or find_node.py for a specific label)
4. LOCATE  bounds="[x1,y1][x2,y2]" → center = ((x1+x2)/2, (y1+y2)/2)
5. ACT     adb shell input tap X Y  (or swipe/keyevent/text)
6. VERIFY  sleep 2-5 s → fresh dump → assert new state
```

**Golden rules**

1. **Coordinates are disposable; the loop is not.** Never reuse coordinates from a
   previous dump — layouts shift. Always re-dump before every tap.
2. **Match text/content-desc first**, coordinates last.
3. **Verify after every action** with a fresh dump or `mCurrentFocus`.
4. **One device per command**: always `-s SERIAL`.

## Setup / prerequisites

```bash
# 1. Tunnel (if device lives behind SSH) — run as background job:
ssh -i <key> -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 \
    -N -L 127.0.0.1:5557:127.0.0.1:5557 user@host

# 2. Connect + sanity check
adb connect 127.0.0.1:5557 && adb devices       # expect: ...device
adb -s 127.0.0.1:5557 shell getprop sys.boot_completed   # must print "1"
```

## Command reference (quick)

| Task | Command |
|---|---|
| Dump screen | `adb -s S shell uiautomator dump /sdcard/d.xml` then `adb -s S pull /sdcard/d.xml` |
| List visible labels | `python skills/ui-automator/scripts/parse_ui.py d.xml` |
| Find one node | `python skills/ui-automator/scripts/find_node.py d.xml "Play Protect"` |
| Icon in header | `python skills/ui-automator/scripts/list_top_nodes.py d.xml 170` |
| Verdict icons (Pass/Fail) | `python skills/ui-automator/scripts/check_verdict.py d.xml` |
| Tap | `adb -s S shell input tap X Y` |
| Scroll | `adb -s S shell input swipe X1 Y1 X2 Y2 MS` |
| Back/Home/Enter | `adb -s S shell input keyevent KEYCODE_BACK` (BACK=4) |
| Type | `adb -s S shell input text 'hello%sworld'` (`%s` = space) |
| Launch app | `adb -s S shell am start -W -n PKG/.MainActivity` |
| Foreground window | `adb -s S shell dumpsys window \| grep mCurrentFocus` |

Full details: [references/adb-uiautomator-cheatsheet.md](references/adb-uiautomator-cheatsheet.md)

## Scripts (in `scripts/`)

| Script | What it does |
|---|---|
| `ui_dump.sh [serial] [out]` | Dump current screen + pull locally (one step) |
| `parse_ui.py dump.xml` | Print every visible TEXT/DESC node with bounds |
| `find_node.py dump.xml <regex> [--desc]` | Find node(s); prints BOUNDS + CENTER + CLICKABLE; exit 2 = no match |
| `list_top_nodes.py dump.xml [ymax]` | Header-bar nodes lacking labels (y < ymax) |
| `check_verdict.py dump.xml` | Count Pass/Fail content-desc icons (integrity checker) |
| `tap_text.sh [-s S] [-d] "<regex>"` | One-shot: dump → find → tap center |
| `screen_state.sh [serial]` | Focus + top activity + screen size snapshot |

## Worked examples (real sequences from this repo)

### A. Open Play Store account sheet → Play Protect (scrollable bottom sheet)

```bash
SER=127.0.0.1:5557
adb -s $SER shell input tap 648 104                    # avatar (found via list_top_nodes.py)
sleep 3
adb -s $SER shell input swipe 360 1000 360 450 400     # scroll; rows ~116 px apart
bash ui_dump.sh $SER sheet.xml
python find_node.py sheet.xml "Play Protect"           # → CENTER=(360, 898)
adb -s $SER shell input tap 360 898                    # tap row center, not text edge
```

### B. Capture a Play Integrity verdict

```bash
adb -s $SER shell am force-stop gr.nikolasspyr.integritycheck
adb -s $SER shell am start -W -n gr.nikolasspyr.integritycheck/.MainActivity
adb -s $SER shell input tap 360 877        # CHECK button ([272,829][448,925])
sleep 20                                   # token round-trip takes 10-18 s
bash ui_dump.sh $SER v.xml && python check_verdict.py v.xml
```

Note: the checker's raw-JSON dialog body is NOT visible in uiautomator dumps and
clipboard reads are blocked on Android 14 — read verdicts from the Pass/Fail icons.

More recipes: [references/proven-workflows.md](references/proven-workflows.md)

## Decision tree

```text
Need to interact with Android UI
├─ Device connected?          no → tunnel up → adb connect → boot_completed=1
├─ Target app foreground?     no → am start -W ... (verify Status: ok)
├─ Element has text?          yes → dump → find_node.py "<text>" → tap CENTER
│    └─ below fold?                → input swipe up → re-dump → retry
├─ Element is an icon?
│   ├─ content-desc present?      → find_node.py --desc "<desc>"
│   └─ unlabeled header item?     → list_top_nodes.py, identify by class+bounds
├─ Need action result?        sleep → fresh dump → parse/assert state
└─ Something misbehaved?      references/troubleshooting.md
```

## Safety notes

- `pm clear PKG` wipes ALL app data (GSF ids, sign-ins, scan history) — only use
  with explicit intent.
- Do not spam taps against rate-limited flows (integrity checks, logins).
- On shared hosts: container restarts usually fine; full VPS reboots may be
  forbidden — check project docs first.

## Host pitfalls digest (Windows/PowerShell)

1. No `<` stdin redirect → pipe files: `Get-Content -Raw s.sh | ssh h "tr -d '\r' | bash -s"`
2. `&` starts PS background jobs; chain commands with `;`.
3. `$C:/path` inside double quotes breaks PS variable parsing — avoid `$var:` patterns.
4. Nested-quote python one-liners are fragile — use script files from `scripts/`.
5. Strip CRLF (`tr -d '\r'`) before piping scripts to remote bash.

Full symptom/fix table: [references/troubleshooting.md](references/troubleshooting.md)

