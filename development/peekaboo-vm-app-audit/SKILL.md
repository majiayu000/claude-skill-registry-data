---
name: peekaboo-vm-app-audit
description: Drive an LLM-led audit of one or more macOS apps using Peekaboo as eyes-and-hands — verify install, inspect on-disk preferences, launch the app, navigate its UI (windows, menu bar, settings panes), compare what the app's own UI shows against the configured plist, and produce a markdown report with embedded screenshot proof for each step. Works locally on the current Mac, against a remote Mac via SSH, or inside a Tart VM via double-hop SSH. Use whenever the user asks to "verify the install", "prove the settings landed", "screenshot every app", "audit what's running", or after a fresh chezmoi/dotfiles apply on a new machine or VM. The skill installs Peekaboo if missing.
---

# Peekaboo App Audit (LLM-driven)

You are the auditor. Peekaboo is your hands and eyes. The user gives you a list of apps; you produce a markdown report with proof.

## Reset to a clean slate before every app

Audit one app at a time, and reset the desktop between apps so screenshots aren't polluted by another app's modal/welcome dialog. Before each app's audit loop:

```bash
# 1. Quit every running 3rd-party / non-system app — leave only Finder, Dock, etc.
#    Use peekaboo to inventory, then quit each non-system one.
peekaboo list apps | grep -vE 'com\.apple\.|loginwindow|talagentd|nbagent|UserNotificationCenter' \
  | awk -F'[()]' '/PID:/ {print $2}' \
  | while read bid; do
      [ -n "$bid" ] && osascript -e "tell application id \"$bid\" to quit" 2>/dev/null
    done

# 2. Dismiss any leftover modal sheets (Esc + Cmd-W loop)
for _ in 1 2 3; do
  osascript -e 'tell application "System Events" to key code 53'                       2>/dev/null
  osascript -e 'tell application "System Events" to keystroke "w" using command down'  2>/dev/null
done

# 3. Activate Finder so the desktop is the foreground context
osascript -e 'tell application "Finder" to activate'
sleep 2

# 4. Capture a baseline desktop shot — confirm it's truly clean before proceeding
peekaboo image --mode screen --path screenshots/<app-slug>/00-clean-slate.png
```

Inspect `00-clean-slate.png` (or just `peekaboo list apps`) and confirm only system processes + Finder are running before launching the audit target. If a stubborn app refused to quit (BetterTouchTool's permission sheet is a common culprit), `killall <App>` it.

## What "audit one app" means

For each app the user names, run the clean-slate reset above, THEN this loop. Capture a screenshot at every meaningful step. Save them under `<workdir>/screenshots/<app-slug>/<NN>-<step>.png` and reference them inline in the final report.

1. **Install presence** — does `/Applications/<App>.app` exist? If not, try `mdfind -onlyin /Applications "kMDItemDisplayName == '<App>*'cd"` to find variant names.
2. **On-disk preferences** — `defaults read <bundle-id>` (or `plutil -p ~/Library/Preferences/<bid>.plist`). Capture the full output. Note interesting/configured keys.
3. **Launch** — pre-strip Gatekeeper quarantine (`xattr -dr com.apple.quarantine /Applications/<App>.app`, may need `sudo`), then `open -ga "<App>"`. **Do not use `peekaboo app launch`** — it blocks on Gatekeeper sheets.
4. **Confirm process is alive** — `peekaboo list apps | grep -i <app>`. Capture PID + window count.
5. **Per-app screenshot** — `peekaboo image --mode window --app "<App>" --path screenshots/<slug>/01-window.png`. If the app has 0 windows, fall back to `--mode screen`.
6. **Menu bar evidence** — `peekaboo menubar list`. Useful especially for menu-bar-only apps and for hider apps (Ice, Bartender) whose configured behavior is precisely "hide other items".
7. **Navigate the app's own preferences UI** — open Preferences. **`peekaboo hotkey` does NOT accept `comma` as a key alias** (it errors with `Invalid hotkey combination: cmd+comma`). Use osascript instead:

   ```bash
   osascript -e 'tell application "<App>" to activate' \
             -e 'tell application "System Events" to keystroke "," using command down'
   ```

   For other keyboard chords, prefer the same osascript pattern over `peekaboo hotkey` — it's more reliable across symbol keys. Screenshot each tab/section. **Compare** what the UI displays against the on-disk values from step 2 — this is the *real* verification: do the prefs the app reads match what we wrote?
8. **Click around the main UI** — for each visible top-level navigation element (sidebar entry, tab, menu), use `peekaboo click "<label>"` (or `peekaboo see` to find UI elements first), then screenshot. Aim for 3-5 representative views per app.

   **After every click, verify advancement** — pixel diff is unreliable when apps animate copy on the same screen. Use a *button-label-delta oracle*:

   ```bash
   labels() { peekaboo see --app "<App>" | grep -oE '\(button\) - .*' | sed 's/(button) - //' | sort -u; }
   pre=$(labels)
   peekaboo click "Continue" --app "<App>"
   sleep 4
   post=$(labels)
   [ "$pre" = "$post" ] && echo "NO ADVANCE" || echo "ADVANCED ✓"
   ```

   **Compare LABELS, not full lines.** `peekaboo see` reorders `elem_N` IDs on every snapshot — diffing whole lines false-positives any time the UI tree rebuilds even when the visible buttons are unchanged. Strip the `elem_N` prefix and compare just the human-readable text.
9. **Verify a workflow** — pick one core feature of the app and demonstrate it works. Generic patterns:
   - Apps with a launcher hotkey (Raycast, Spotlight-like): trigger the configured hotkey, type a query, screenshot the result list.
   - Menu-bar manager apps (Ice, Bartender): screenshot `peekaboo menubar list` before and after toggling — the visible item count should change.
   - Apps with an in-app preference selector that mirrors a configured plist key (transcription model, default editor, sync provider): open Preferences and screenshot the selector — its value should match `defaults read <bid> <key>`.
   - System-extension or menu-bar-only apps (Tailscale, BetterDisplay): expand the menu-bar item via `peekaboo menubar click "<label>"`, screenshot the dropdown.
   - Apps requiring sign-in or licence: screenshot the auth-required state as proof of install + integration; mark sign-in/licence as out-of-scope in caveats.
10. **Quit cleanly** — `osascript -e 'tell application "<App>" to quit'`.

If a step blocks on a permission/welcome dialog, take a screenshot of the dialog (proof) and move on; don't try to satisfy it. Note in the report which apps need user action.

## Environment setup (run once at start)

Detect or accept from the user where you're running:

- **Local Mac** — `peekaboo` runs directly. No SSH wrapping.
- **Remote Mac via SSH** — wrap every shell call in `ssh <user>@<host> '...'`.
- **Tart VM** — double-hop: `ssh <tart-host> "sshpass -p <vmpw> ssh admin@$(ssh <tart-host> 'tart ip <vm>') '...'"`. Cirruslabs default password is `admin`. Push scripts via `scp` (don't trust the tart shared folder for live edits).

### CRITICAL — VM display size

If the target is a Tart (or other framework-virt) VM, **check the display resolution before launching apps**:

```bash
ssh <tart-host> "tart get <vm-name> | tail -1"   # shows display dims, e.g. 1024x768
```

The tart default of **1024×768 is too small** for many SwiftUI welcome wizards / preference panes. Apps lay out at desktop-laptop dimensions and put their primary CTA at y=750+. On a 768-tall screen the button is below the visible viewport — `peekaboo click` will report success but the click coordinate lands in off-screen pixels and macOS doesn't fire the handler. You'll get convincing-looking but useless screenshots of the same screen forever.

**Bump to at least 1440×900 before starting:**

```bash
ssh <tart-host> "tart stop <vm-name> && \
                 tart set <vm-name> --display 1440x900 && \
                 nohup tart run --vnc-experimental --no-audio --no-clipboard <vm-name> > /tmp/tart-run.log 2>&1 &"
# Wait for guest agent to come back
ssh <tart-host> "for i in \$(seq 1 30); do tart exec <vm-name> true >/dev/null 2>&1 && break; sleep 2; done"
```

A cold reboot gives you a clean slate as a bonus — the resurrecting daemons (Setapp, BTT permission sheet, etc.) won't be running yet.

Then ensure Peekaboo is ready:

```bash
command -v peekaboo >/dev/null || brew install steipete/tap/peekaboo
peekaboo --version
peekaboo permissions   # both Screen Recording + Accessibility must be Granted
peekaboo list apps | head -3   # smoke test
```

If permissions aren't granted, instruct the user to grant in System Settings → Privacy & Security; on a fresh Tart VM (cirruslabs image) they're pre-granted.

## Peekaboo command vocabulary

You don't need every subcommand. The audit uses:

| command | use |
|---|---|
| `peekaboo permissions` | preflight |
| `peekaboo list apps` | running app inventory (PID, bundle id, window count) |
| `peekaboo list windows --app "<App>"` | per-app window titles |
| `peekaboo menubar list` | enumerate menu-bar items by label |
| `peekaboo image --mode window --app "<App>" --path <out>` | focused per-app shot |
| `peekaboo image --mode screen --path <out>` | full-screen fallback / desktop snapshot |
| `peekaboo see --app "<App>"` | discover UI elements with their accessible labels for `click`. **`elem_N` IDs are NOT stable across `see` calls** — the tree rebuilds and IDs reshuffle. Don't reference `elem_N` from a prior snapshot; either click by label or use `peekaboo click --snapshot <id> --on elem_N` to lock the reference within one snapshot. |
| `peekaboo click "<label>"` or `peekaboo click --coords X,Y` or `peekaboo click --on elem_N --snapshot <id>` | click |
| `peekaboo hotkey "cmd,a"` | keyboard chord (letters/digits — for symbol keys like comma/slash use osascript instead, see app-loop step 7) |
| `peekaboo type "<text>"` | enter text |
| `peekaboo scroll up\|down\|left\|right --amount N` | scroll |
| `peekaboo window list --app "<App>"` | window inspection (alt to `list windows`) |
| `peekaboo dialog ...` | interact with system alerts |

If you forget the exact flags, run `peekaboo <subcommand> --help` — it's terse and accurate.

## Companion shell tools you'll want

- `defaults read <bundle-id> [<key>]` — read on-disk prefs (booleans show as `1`/`0`).
- `plutil -p <path>` — same as above but prints structure for nested dicts.
- `mdfind -onlyin /Applications "kMDItemCFBundleIdentifier == '<bid>'"` — find a bundle by id.
- `osascript -e 'tell application "<App>" to quit'` — clean quit.
- `osascript -e 'tell application "System Events" to keystroke "w" using command down'` — generic Cmd-W to close a stuck window.
- `osascript -e 'tell application "System Events" to key code 53'` — Esc to dismiss a sheet.
- `xattr -dr com.apple.quarantine /Applications/<App>.app` (may need `sudo`).
- `killall peekaboo` — recover from a wedged peekaboo invocation.

## Failure modes to recognise

You'll hit these. Recognise them by the symptom and apply the workaround inline; don't get stuck.

| symptom | what's happening | workaround |
|---|---|---|
| `peekaboo app launch` doesn't return | first-run Gatekeeper "downloaded from Internet" sheet | `killall peekaboo`; strip quarantine; use `open -ga` |
| All your per-app screenshots look identical | one app's modal dialog is on top of everything | quit that app; screenshot and note it in the report; carry on |
| Tiny PNG (< 20 KB) for a window shot | `--mode window` returned blank because target had no foreground window | re-shoot with `--mode screen`; tag in the report as "fallback" |
| `defaults read` shows `1`, your config said `true` | macOS normalises booleans on write | accept `1`↔`true`, `0`↔`false` as equivalent |
| Edits to scripts on tart-shared folder don't take in VM | shared-folder cache | always `scp` scripts in fresh; never edit through the share |
| Modal owned by `UserNotificationCenter` looks like the app | it's a separate process | check `peekaboo list apps` for `UserNotificationCenter`; dismiss with `osascript ... key code 53` |
| `peekaboo click "<label>"` reports `✅ Clicked successful` but the screen doesn't change | click coordinate landed off-screen (window taller than display) OR the "label" matched a decorative SwiftUI text element with no hit-test target | First check `peekaboo see --app <App>` — if the label appears but isn't tagged as `(button)`, it's decorative. If it IS a button, check the click `📍 Location` against the screen size; if y > screen-height, resize the VM display per "Environment setup" or move the window via `osascript ... set position to {x, negative-y}`. **Use button-LABEL-delta as the "did we advance?" oracle** (per app-loop step 8) — same labels = no advance, regardless of how the screenshot looks. |
| Same screenshot every time but content "looks different" | animated marketing tagline / typewriter effect cycling on the same screen — pixel-diff is misleading | trust button-label-delta, not visual diff |
| Diffing `peekaboo see` output between snapshots claims "ADVANCED" but visible buttons are identical | `elem_N` IDs reshuffle on every snapshot | strip the `elem_N` prefix before diffing — compare only the label text after `(button) - ` (see app-loop step 8 for the comparator one-liner) |
| `peekaboo click --on elem_5` clicks the wrong element | `elem_5` referred to a different element in the snapshot you discovered it from than in the current accessibility tree | `peekaboo see` and `click` in the same shell pipeline; or pass `--snapshot <id>` to lock the reference |
| TCC permission dialog auto-grant only sometimes works | TCC routing is per-permission-type (next row) | see TCC table below |

## TCC permission dialogs — what's auto-grantable

macOS routes TCC prompts through different surfaces depending on the permission type. Some can be auto-accepted from a child process; others can't (security guarantee). Categorise BEFORE clicking the in-app "Enable Access" button so you know what to expect:

| permission | dialog owner | auto-grantable? | how |
|---|---|---|---|
| Microphone | `UserNotificationCenter` (NSAlert sheet) | ✅ yes | `osascript -e 'tell application "System Events" to tell process "UserNotificationCenter" to click button "Allow" of window 1'` |
| Camera | `UserNotificationCenter` | ✅ yes | same as Microphone |
| Notifications | `UserNotificationCenter` | ✅ yes | same |
| Contacts / Calendar / Reminders / Photos | `UserNotificationCenter` | ✅ yes | same |
| Accessibility | System Settings → Privacy & Security panel | ❌ no — requires physical user click in System Settings | screenshot the System Settings panel as proof of the prompt; mark in caveats |
| Screen Recording | System Settings panel | ❌ no | same |
| Input Monitoring | System Settings panel | ❌ no | same |
| Full Disk Access | System Settings panel | ❌ no | same |
| Files & Folders | mixed (NSAlert for one-shot, panel for global) | ⚠️ try the NSAlert pattern first | fall through to caveats if it fails |

`peekaboo dialog click --button Allow` is hit-or-miss for TCC dialogs — fall back to the System Events osascript pattern above.

## What you cannot prove

Note these in the report's caveats section, never fail the audit on them:

- Sign-in completed — apps requiring username/password/SSO/iCloud auth need interactive credentials.
- License activation — apps that read a license file or call out to a vendor need the license artefact present (a separate concern from chezmoi config).
- TCC grants for Accessibility / Screen Recording / Input Monitoring / Full Disk Access — see the TCC table above.
- Multi-step welcome wizards past the auto-grantable steps — capture each screen reached, mark the last as "first-run pending {permission}".
- Decorative SwiftUI links (e.g. "Skip for now" rendered as inert text) — confirm via `peekaboo see` that the label has no `(button)` tag, then close the window via `Cmd-W` or quit the app.

## Output structure

Write all artifacts under a single timestamped dir. Recommend:

```
<workdir>/audit-<YYYYMMDD-HHMMSS>/
  report.md                      ← the headline; references all screenshots by relative path
  screenshots/
    <app-slug>/
      00-bundle-info.png         ← optional: Finder window or `ls -la` shot
      01-window.png              ← initial app window after launch
      02-prefs-general.png       ← settings UI, tab 1
      03-prefs-<area>.png        ← per pane
      04-menubar.png             ← menu bar item dropdown if applicable
      05-workflow-<feature>.png  ← demonstrating one core feature
    _desktop-pre.png             ← before any launches
    _desktop-final.png           ← after the audit
  raw/
    apps.txt                     ← peekaboo list apps
    menubar.txt                  ← peekaboo menubar list
    defaults-<app-slug>.txt      ← `defaults read <bid>` per app
```

## Report shape

The `report.md` should have, in order:

1. **Header** — date, where the audit ran (local / remote / VM name), apps audited, pass/fail counts.
2. **Per-app section** (one per app, in the order the user asked) — embed the screenshots inline with markdown image refs (`![](screenshots/<slug>/02-prefs-general.png)`). For each: install status, on-disk prefs vs UI prefs comparison (point out matches and divergences explicitly), workflow tested, screenshots embedded.
3. **Menu bar inventory** — verbatim `peekaboo menubar list` output in a fenced block. Critical for hider apps.
4. **Caveats** — apps that need sign-in, licenses, TCC permissions; first-run wizards encountered.
5. **Run details** — Peekaboo version, host, total wallclock, every shell command in a collapsible `<details>` block.

Don't generate code to render the report — just write it as Claude after you've collected all the artifacts. The screenshots are the evidence; the prose is the verdict.

## Asking the user

If the user hasn't named apps, ask: "Which apps should I audit?" Accept either app display names (e.g. "Tailscale") or bundle IDs (e.g. "io.tailscale.ipn.macsys"). If they say "all the configured ones" and you're in a chezmoi-managed dotfiles repo, suggest scanning `home/.chezmoitemplates/*.plist.tmpl` for managed bundle IDs.

If the user hasn't said where to run (local / remote / VM), ask. Don't guess — running launches and clicks on the wrong machine is destructive.
