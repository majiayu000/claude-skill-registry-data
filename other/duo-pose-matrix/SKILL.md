---
name: duo-pose-matrix
description: "Screenshots an iPhone Duo app in every pose (closed, open, book, tabletop) on the iPhone Duo simulator by pressing Device Hub's pose buttons through the macOS Accessibility API, then writes summary.md and summary.json to review with the duo-design-review checklist. Use when asked to check, test or screenshot an app in each pose, fold or hinge state, to capture outer and inner display frames for a design review or the App Store, to change the simulator's pose from the command line or a script (simctl and devicectl have no pose command), to run /duo-poses, or when a review is missing book or tabletop frames. Ships duo-pose (status, list, set) and duo-pose-matrix, with a manual fallback when the user has not given Accessibility permission, and checks that no UI tests share the simulator before it changes the pose."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-pose-matrix

`simctl` and `devicectl` in Xcode 27.1 have no pose command. Device Hub has pose buttons under the phone (Closed, Partially Open, Open, Rotate Right), and macOS lets a trusted process press them through the Accessibility API. This skill ships two tools built on that:

- `duo-pose` sets one pose and checks it: `status`, `list`, `set <closed|open|book|tabletop>`.
- `duo-pose-matrix` runs an installed app through every pose, saves a screenshot of each, checks it, writes `summary.md` and `summary.json`, and puts the simulator back the way it found it.

"Book" and "tabletop" are Duology's words. Apple describes these as partially folded like a book, and seated on a table like a laptop ([HIG: Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)). The SDK has no posture API ([API index](https://github.com/Kimeur/duology/blob/main/reference/api-index.md#not-in-the-sdk)).

This is UI scripting of Device Hub. It is optional. When it can't run, the same tool captures poses that a person sets by hand (see [When it can't press the buttons](#when-it-cant-press-the-buttons)).

Related skills: `duo-design-review` (read the screenshots against its 15 rules), `duo-testing` (UI tests on the simulator), `duo-setup` (Xcode 27.1, the simulator, Device Hub).

## Rules

- Never change macOS privacy settings, and never ask the user to let you do it. Accessibility permission is the user's decision. If `duo-pose status` says it isn't allowed, tell the user how to allow it (below) and offer the manual route.
- Use the existing iPhone Duo simulator. Never create, clone or delete one: each takes 4-6 GB of disk.
- Tell the user before a run: it changes the pose of the whole simulator, for every app and test on it, and when it can't see Device Hub's window it brings Device Hub to the front, out of whatever app or full-screen Space the user is in. If the user is working on the Mac, pass `--no-bring-forward` and ask them to show Device Hub on the current desktop instead.
- Don't run it while someone runs UI tests on the simulator. The tools refuse while an `xcodebuild test` runs on the Mac or a UI test runner (`.xctrunner`) runs in the simulator; pass `--force` only when the user confirms those tests use another simulator.
- Treat open and book as "not confirmed" unless the app reports its fold (see [Tell open from book](#tell-open-from-book)). From outside the app they look the same.
- Never use the screenshots' pixel sizes in app code. They are for reading frames only.

## Run it

| Installed with | Run |
|---|---|
| The `duology-ship` plugin in Claude Code | `"${CLAUDE_PLUGIN_ROOT}/skills/duo-pose-matrix/scripts/duo-pose-matrix"` and `.../scripts/duo-pose` |
| `npx skills add`, or copied by hand | `<skill-folder>/scripts/duo-pose-matrix` and `<skill-folder>/scripts/duo-pose` |

`<skill-folder>` is the folder that holds this `SKILL.md` (`${CLAUDE_SKILL_DIR}` in Claude Code). The examples below say `duo-pose` and `duo-pose-matrix`; use the full path. If a script can't be executed, run `python3 <skill-folder>/scripts/duo_pose.py` or `duo_pose_matrix.py` instead.

What they need:

- macOS with Xcode 27.1. The tools set `DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer` themselves when that folder exists and `DEVELOPER_DIR` is unset. Never run `sudo` or `xcode-select`.
- Python 3.9 or later (the `/usr/bin/python3` that comes with Xcode is enough).
- A booted iPhone Duo simulator, shown in Device Hub.
- Accessibility permission for the app that runs the agent (Terminal, iTerm or the Claude app). Only the user can give it.
- For the matrix: the app installed on that simulator.

On first use, `duo-pose` builds its Swift helper, `scripts/duo-pose-ax.swift`, with `xcrun swiftc` into `~/Library/Caches/duology/`. The binary is never committed. A changed source builds a new copy.

### 1. Check that it can work

```bash
duo-pose status
```

```text
duo-pose 0.3.0
  Simulator:      iPhone Duo (<UDID>), iOS 27.1, booted
  Pose now:       closed
  Device Hub:     running (pid 88720)
  Accessibility:  allowed for the app that runs this command
  Window:         iPhone Duo – iOS 27.1
  Buttons:        Closed, Partially Open, Open, Rotate Right
  Poses it can set: closed, open, book, tabletop
  UI tests:       none running
Ready: `duo-pose set <closed|open|book|tabletop>` can press Device Hub's buttons.
```

`status` and `list` change nothing. `status` exits 0 when `set` would work, otherwise with the code of the first problem:

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Done, or ready | Go on. |
| 1 | The pose did not take, a screenshot failed its checks, or the matrix stopped early | Read the problems it printed. Look at Device Hub. |
| 2 | Bad arguments | Read `--help`. |
| 3 | The app that runs the agent may not use Accessibility | Tell the user how to allow it (below). Offer the manual route. |
| 4 | Device Hub isn't running, has no window for the phone on this desktop, or shows no pose buttons | Ask the user to open Device Hub on the iPhone Duo. `set` and the matrix bring it forward themselves unless you passed `--no-bring-forward`; `status` and `list` do only with `--bring-forward`. Otherwise use the manual route. |
| 5 | No booted iPhone Duo simulator | Boot the existing one. Never create one; run `duo-doctor` or follow `duo-setup`. |
| 6 | UI tests are running | Wait. Use `--force` only if the user says the tests use another simulator. |
| 7 | The Swift helper could not be built | Check that Xcode 27.1 is installed. |
| 8 | (matrix) The app isn't installed on the simulator | Build and install it (`/duo-audit` step 2 has the commands). |

How the user allows Accessibility, in their words to them: System Settings > Privacy & Security > Accessibility, then turn on the app that runs Claude Code. If it still says not allowed, quit and reopen that app ([Apple: Allow accessibility apps to access your Mac](https://support.apple.com/guide/mac-help/allow-accessibility-apps-to-access-your-mac-mh43185/mac)).

### 2. Run the matrix

```bash
# One screen, every pose. Arguments after -- go to the app on every launch.
duo-pose-matrix com.example.places -- -uiTesting -openScreen map

# Several screens in one run: each pose is set once, then every case is captured in it.
duo-pose-matrix dev.duology.gallery --out /tmp/duo-poses/gallery \
  --case "listDetail=-pattern listDetail -select 1" \
  --case "twoPage=-pattern twoPage" \
  -- -showsRegions YES

# Keep the app running while the poses change, to see what survives a fold (R2).
duo-pose-matrix com.example.notes --no-relaunch --poses closed,open,book -- -uiTesting
```

| Option | What it does |
|---|---|
| `--case NAME=ARGS` | One screen with its own launch arguments. Repeat it. Files are named `<case>-<pose>.png`. Without it, the case is `app`. |
| `--poses LIST` | Poses in order. Default `closed,open,book,tabletop`. |
| `--out DIR` | Output folder. Default: a new folder under `$TMPDIR/duo-poses/`. Tell the user where it is. |
| `--wait SECONDS` | Time between launch and screenshot. Default 4. Raise it for slow first screens. |
| `--pose-wait SECONDS`, `--timeout SECONDS` | Wait after a fold button (default 5) and the longest wait for the displays to switch (default 20). Raise both when a pose fails with "the inner display should be active" on a slow Mac. |
| `--no-relaunch` | Launch each case once and keep it running across poses. |
| `--readout-id ID` | Read the app's fold readout to tell open from book. |
| `--manual POSE` | Press nothing; capture one pose someone set by hand. |
| `--force` | Run even while UI tests run. |
| `--busy-wait SECONDS` | How long to wait when UI tests start mid-run, before the next pose or the restore. Default 120. |
| `--no-restore`, `--keep-running`, `--no-bring-forward`, `--json` | Leave the last pose; leave the app running; fail instead of bringing Device Hub forward; print the summary as JSON. |

From the default waits, setting a pose takes about 7 to 20 seconds. Each screenshot takes about 6 to 7 seconds more (*measured*: two cases in one pose took 13 seconds). Four poses and two cases take two to four minutes (*measured*: 4 minutes on a shared, busy simulator on 18 October 2026).

### 3. Read the results

Open `summary.md` first. It has one row per screenshot: case, pose, file, size, fold check, status and notes. Then look at every PNG yourself.

| Status | Meaning |
|---|---|
| `ok` | The right display was active, the phone was turned the right way, the screenshot has the expected size, and the app was running. |
| `check` | Taken, but something may be wrong with the picture: another app started, someone else relaunched your app, or the frame is nearly blank. Look at it; rerun if it isn't your screen. |
| `failed` | Wrong pose, the pose changed during the capture, wrong size, no file, or the app wasn't running (often a crash in that pose). |

Expected sizes: closed 1398 x 2034 px (outer display); open and book 2853 x 2007 (inner, held wide); tabletop 2007 x 2853 (inner, held tall). `summary.json` has the same data per shot: `checks`, `fold`, `status`, `notes` and the `review` rules to apply.

### 4. Review the screenshots

Load `duo-design-review` and run its checklist. Start with the rules each pose can prove:

| Pose | Rules |
|---|---|
| closed | R1 letterboxing, R6 side bars with symbols and titles, R10 same features on the outer display, R13 44 pt targets |
| open | R1, R3 no size from the main screen, R5 even grids, R6, R13 |
| book | R4 nothing interactive in the fold, R5, R7 book layout |
| tabletop | R4, R7 tabletop layout (media on top, controls below, same controls) |
| `--no-relaunch` sets | R2 state survives fold and unfold |

The matrix can't prove R8 (Split View, PiP), R12 (transitions), closed and turned sideways, or open held tall but flat. Mark those **Check** and say which frame or recording would settle them. Details and an example finding: [references/reading-results.md](references/reading-results.md).

## Set one pose

```bash
duo-pose set book
duo-pose set tabletop --json
```

It presses the fold button, waits for the displays to switch, turns the phone with Rotate Right if needed, then checks the active display, the rotation and a test screenshot's size. Closing a turned phone turns it back first. It brings Device Hub's window forward when it can't see it (`--no-bring-forward` to fail instead).

| Pose | Buttons it presses |
|---|---|
| closed | (Rotate Right until portrait), Closed |
| open | Open (then Rotate Right until held wide) |
| book | Partially Open (then Rotate Right until held wide) |
| tabletop | Partially Open, then Rotate Right until held tall |

## When it can't press the buttons

When `duo-pose status` exits 3 or 4, or the user would rather not give permission, capture the poses by hand. For each pose:

1. Ask the user to press it in Device Hub: Closed, Open, Partially Open (book), or Partially Open then Rotate Right once (tabletop).
2. When they say it's done, run the matrix for that pose only, with the same `--out` each time:

```bash
duo-pose-matrix com.example.places --out /tmp/duo-poses/places --manual book -- -uiTesting
```

Each run adds its shots to `summary.md` in that folder. `--manual` presses nothing and needs no permission; it still checks the displays and fails the shot if the phone is in another pose. When the automatic run fails with exit 3 or 4, it prints these commands for every pose.

## Tell open from book

Device Hub doesn't say which pose it is in, and the displays are the same in open and book. Two ways to tell:

- Look at the screenshot. An app with a region overlay shows the fold; the gallery's `-showsRegions YES` prints "Fold, active" or "Fold, inactive".
- Add a debug fold readout to the app and pass `--readout-id duo.pose` with `-- -duoPoseReadout YES`. The readout and its limits: [references/pose-readout.md](references/pose-readout.md).

## Limits

- It is UI scripting. It finds Device Hub's buttons by their English descriptions and its window layout. An Xcode update can break it; then `list` prints the buttons it can see, and the manual route still works.
- Device Hub's window must be on the current desktop: not minimized, not behind Mission Control, not on another Space. When it can't see the window, `set` and the matrix run `open -a` on Device Hub, which moves the user's focus to it; `--no-bring-forward` turns that off. `status` and `list` do it only with `--bring-forward`.
- The pose is global. Changing it moves the screen for every agent and test on that simulator. The matrix checks for UI tests before each pose change and before the restore. When tests start mid-run, it waits up to `--busy-wait` seconds (default 120), then stops, leaves the pose as it is and exits 1. The summary's restore note names the pose it left.
- Run one pose sweep per simulator at a time. Duology's tools share a lock; other scripts don't. Each shot is checked after the screenshot (pose, app process, blank frame), which catches another script pressing buttons or relaunching the app, but can't prevent it.
- The start pose is restored as closed or open. Device Hub doesn't report book, so a phone that started in book is left open, and the summary says so.
- Only the three button poses. Other hinge angles need Option-drag in Device Hub ([Interacting with your app in Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)).

How it works, timings and every check: [references/how-it-works.md](references/how-it-works.md). What can go wrong and why: [references/limits.md](references/limits.md).

## Checklist

- [ ] Ran `duo-pose status`; it exited 0, or I told the user why not and offered the manual route.
- [ ] Never changed a privacy setting; if Accessibility wasn't allowed, I told the user how to allow it.
- [ ] Used the existing iPhone Duo simulator; created, cloned and deleted none.
- [ ] Told the user before the run that it changes the simulator's pose and brings Device Hub forward.
- [ ] No UI tests were running, or the user confirmed `--force`.
- [ ] Read `summary.md` and looked at every screenshot myself, not only the statuses.
- [ ] Marked open and book "not confirmed" unless a readout or an overlay in the screenshot shows the fold.
- [ ] Ran the duo-design-review rules for each pose and marked what the matrix can't show as Check.
- [ ] The simulator is back in the pose it started in (the summary's "Pose at the end"), and I told the user where the screenshots are.
