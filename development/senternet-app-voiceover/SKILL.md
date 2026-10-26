---
name: senternet-app-voiceover
description: Test a Senternet macOS app with VoiceOver for real, then fix what fails. Drives a live VoiceOver session from the shell through VoiceOver's AppleScript interface and records what VoiceOver actually speaks (not what the code suggests it should), walks every window, pane, control, menu bar menu and app-specific flow, fixes the gaps with standard SwiftUI/AppKit patterns, localizes any new spoken strings in every supported language, retests each fix live, and restores the machine (VoiceOver, its AppleScript permission, hidden apps, clipboard, the installed app copy) afterwards. Weatherling and CommandH are the references. Use when the user says "test VoiceOver", "VoiceOver support", "is this accessible with VoiceOver", "screen reader test", or before declaring VoiceOver support in App Store Connect.
---

# VoiceOver test and fix for a Senternet macOS app

Live-test a native macOS app (SwiftUI or AppKit, Xcode or SwiftPM or plain `swiftc`) under VoiceOver, fix the failures, and prove the fixes the same way. Reading the code is not a test: SwiftUI's accessibility tree often differs from what the source implies, so every claim in the report must come from a phrase VoiceOver spoke.

References: Weatherling (`docs/VoiceOver.md`, commit `8af7fdc`: native controls under VoiceOver, keyboard alternative to drag-and-drop, a main-thread hang that starved accessibility requests) and CommandH (commit `e2aeaa0`: an invisible stand-in window that said "content is empty", in-text links VoiceOver could not follow).

The user asking for the test is consent to turn VoiceOver on. Tell them once that the Mac will start talking and that you will put everything back.

## 1. Read the app first

Before touching VoiceOver, read every view and the AppDelegate/menu code and list what to test:

- Every window and every settings pane or tab, in order.
- Every interactive control: switches, pickers/radio groups, sliders, buttons, links, text fields, disclosure groups, custom-drawn controls.
- Feedback that only shows visually: "Copied" labels, toasts, status text, error lines.
- The menu bar status item and its menu (and submenus).
- The app's own unusual flows. These are where the real bugs are: windows that appear without user action, transparent or 1x1 helper windows, overlays, drag-and-drop, global hotkeys, anything that changes activation policy or the Dock icon, animations on the main thread.
- Build variants that change the UI (for example an `APP_STORE` flag that swaps a picker for a caption).

Also note static red flags while reading, to confirm live:

| Pattern | Typical spoken result |
| --- | --- |
| Decorative `Image` without `.accessibilityHidden(true)` | "image" noise between controls |
| Toggle/Picker with `.labelsHidden()` and no `.accessibilityLabel` | unnamed "toggle button" / "radio group" |
| Link inside a `Text(AttributedString)` | read as plain words, cannot be followed |
| `.buttonStyle(.plain)` link-like button without `.isLink` | "button" instead of "link" |
| Section titles without `.accessibilityAddTraits(.isHeader)` | no heading navigation |
| Visual-only state change ("Copied", checkmark swap) | silence |
| Custom drawn tabs/switches | not a radio group / no on-off value |
| Borderless helper window | "In window, content is empty" |
| Status item image with no `accessibilityDescription` | unnamed status menu |
| Option-click or modifier shortcuts | can collide with Control-Option VoiceOver keys |

## 2. Build and run the dev copy

1. Build the app the repo's normal way (its `build.sh`, `scripts/build.sh`, or `xcodebuild` Debug). Build every UI-changing variant you plan to test.
2. Record what is running: `pgrep -lf <AppName>`. An App Store or TestFlight copy (has `Contents/_MASReceipt`) shares the bundle ID, so quit it before launching the dev build and relaunch it at the end.
3. Note where settings live so you can restore them. A sandboxed App Store copy uses `~/Library/Containers/<bundle id>/Data/Library/Preferences/`; an unsandboxed dev build uses `~/Library/Preferences/<bundle id>.plist`. While the container exists, `defaults read <bundle id>` reads the container, not the dev build's file, so read the dev build's prefs with `plutil -p ~/Library/Preferences/<bundle id>.plist`.
4. Launch the dev build so its main or settings window is frontmost.

## 3. Turn on VoiceOver with AppleScript control

1. Copy `scripts/vo.sh` from this skill into the session scratchpad and `chmod +x` it.
2. Open VoiceOver Utility (`open -a "VoiceOver Utility"`) and read the two checkboxes on General before changing anything, so you can restore them:
   ```bash
   osascript -e 'tell application "System Events" to tell process "VoiceOver Utility"' \
     -e 'set g to splitter group 1 of window 1' \
     -e 'return {value of checkbox "Allow VoiceOver to be controlled with AppleScript" of g, value of checkbox "Display welcome dialog when VoiceOver starts" of g}' \
     -e 'end tell'
   ```
3. Click "Allow VoiceOver to be controlled with AppleScript" (same `click checkbox ...` form). macOS asks for Touch ID or the password. Writing `SCREnableAppleScript` into the plist does not work; only the checkbox does. Stop and ask the user to approve the prompt, then confirm the checkbox reads `1`.
4. Uncheck "Display welcome dialog" for the session (restore it later), or the "Welcome to VoiceOver" dialog blocks every AppleScript call with `AppleEvent timed out (-1712)`. If it does appear: `tell application "System Events" to tell process "VoiceOver Quickstart" to click button "Use VoiceOver" of window 1`.
5. Start VoiceOver: `open /System/Library/CoreServices/VoiceOver.app`. Wait about 5 seconds, then check with `vo.sh say`. `-1728 Can't get content of last phrase` or `-1708 doesn't understand` means scripting is still off.

Syntax that works on macOS 27: `tell vo cursor to move right` (not `move vo cursor right`), `tell vo cursor to move into item`, `tell vo cursor to perform action`, `get content of last phrase`, `get text under cursor of vo cursor`. The commander's `perform command` rejects most command names, so don't rely on it.

## 4. Walk the app

Use `vo.sh` for every step and paste the spoken output into your notes. Work pane by pane:

1. `vo.sh first`, then `vo.sh next` through the sidebar or toolbar. Expect each item's name, its role, and "selected" on the current one.
2. `vo.sh act` on a sidebar item to switch panes, then `next` to the content `scroll area`, `into`, and `next` through every element. Go `into` groups, grids and radio groups, and `out` again.
3. For every control: hear its label, role and value, change it with `act`, hear the new state, then change it back. Check disabled states read as "dimmed".
4. For every visual-only feedback (Copy buttons, Save, status lines): activate and poll `content of last phrase` a few times over 2 seconds. It must speak the result.
5. For in-text links and custom actions: on the element, press VO-Command-Space (`osascript -e 'tell application "System Events" to key code 49 using {control down, option down, command down}'`), screenshot to read the Actions menu, then Escape.
6. Status item: `vo.sh menus` lands on the first status menu only when the cursor is in an app; from elsewhere it moves relative to the current item. Step with `prev`/`next` until the app's item and check its name. Scripted arrow keys do not reach an open NSMenu, so read the menu's accessibility tree instead, which is what VoiceOver speaks for a standard NSMenu:
   ```bash
   osascript <<'EOF'
   tell application "System Events" to tell process "AppName"
     set mbi to menu bar item 1 of menu bar 2
     perform action "AXPress" of mbi
     delay 0.8
     set out to "item: " & description of mbi & linefeed
     repeat with mi in menu items of menu 1 of mbi
       try
         set m to value of attribute "AXMenuItemMarkChar" of mi
       on error
         set m to ""
       end try
       set out to out & name of mi & " | mark=" & m & " | enabled=" & enabled of mi & linefeed
     end repeat
     key code 53
     return out
   end tell
   EOF
   ```
7. Test the app's own unusual flows from step 1 with VoiceOver listening. If a flow needs other apps hidden or windows moved, record the starting state first (`name of every application process whose background only is false and visible is true`), do it, poll the phrases, and restore immediately.

Rules while walking:

- **Check every step's output before the next action.** Counts drift: one extra element (a `scroll area` after the footer, a link split out of a sentence) and `next 6` lands somewhere else, and `act` then presses the wrong thing. Never chain `next N; act` blindly.
- Don't activate outbound links during the walk. They open the browser (or a link router like Burly) and steal focus. If one does, Escape and refocus.
- Copy buttons overwrite the clipboard. Save it first (`pbpaste > clip.txt`) and restore it (`pbcopy < clip.txt`).
- VoiceOver also announces the terminal's own output (phrases like `────❯`). Ignore those and use `vo.sh say` to read the cursor.
- If the cursor gets stuck in status menus or another app, the fastest reset is to quit VoiceOver (`pkill -x VoiceOver`), bring the app window to the front, and start it again. It lands on the focused element.
- A spinning beachball or "App not responding" under VoiceOver means the main thread is starving accessibility requests. Sample it (`sample <pid> 5`) and fix the hot path (Weatherling: `CAMetalLayer nextDrawable`).

## 5. Fix patterns

Prefer native controls and real semantics over labels pasted on top.

- **Unnamed control:** keep the visual label hidden and label the control: `label.accessibilityHidden(true)`, `control.accessibilityLabel(label)`. A Picker keeps its title as the group name even with `.labelsHidden()`.
- **Decorative image or icon:** `.accessibilityHidden(true)`.
- **Headings:** `.accessibilityAddTraits(.isHeader)` on pane and card titles.
- **Link-like buttons:** `.accessibilityAddTraits(.isLink)`.
- **Link inside a Text:** add a named action, keeping the visual link:
  ```swift
  extension View {
      func accessibilityOpenLinkAction(_ name: String, url: URL?) -> some View {
          accessibilityAction(named: Text(String(localized: "Open \(name)", comment: "VoiceOver action that opens a link in the text. The argument is the link's name."))) {
              if let url { NSWorkspace.shared.open(url) }
          }
      }
  }
  ```
- **Visual-only feedback:** announce it. AppKit: `NSAccessibility.post(element: NSApp.mainWindow as Any, notification: .announcementRequested, userInfo: [.announcement: text, .priority: NSAccessibilityPriorityLevel.high.rawValue])`. Swapping a button's own label ("Copy" to "Copied") is already spoken; confirm live.
- **Helper or invisible windows that can take focus:** give them a title and a spoken explanation, without drawing anything:
  ```swift
  w.setAccessibilityTitle("AppName")
  let note = NSView()
  note.setAccessibilityElement(true)
  note.setAccessibilityRole(.staticText)
  note.setAccessibilityValue(String(localized: "...what this is and what to press...", comment: "Spoken by VoiceOver only..."))
  w.contentView = note
  ```
- **Custom tabs or switches:** when `NSWorkspace.shared.isVoiceOverEnabled`, render a native segmented Picker or Toggle instead (Weatherling), or give the custom view `.accessibilityRepresentation { Picker(...) }`.
- **Drag-and-drop or pointer-only interactions:** provide a keyboard path with native buttons (Weatherling's "Collect Lings with the keyboard").
- **Modifier collisions:** a shortcut that checks `.option` must require Option alone, so Control-Option (the VoiceOver keys) never triggers it.
- **Status item:** set `image.accessibilityDescription` to the app name. Menu items need real titles and `state` for checkmarks.

Every new spoken string is user-facing:

- Add it to every language the app ships, following the strings file's own rules (protected names, shortcut spellings such as `Cmd+Tab`).
- Run the repo's localization check (for example `scripts/check-localization.py`).
- No em dashes.

## 6. Retest and restore

1. Rebuild, relaunch, and repeat the exact VoiceOver steps for each failure. Report the new spoken phrase verbatim.
2. Restore everything you changed, and verify each item:
   - Apps you hid: unhide them, then bring the user's terminal to the front.
   - Clipboard: restore it.
   - Dev-build settings you toggled: switch them back. The App Store copy's container should never be touched.
   - VoiceOver: off (`pkill -x VoiceOver`, then confirm with `pgrep`).
   - VoiceOver Utility: put both checkboxes back to their recorded values. Turning AppleScript control off asks for Touch ID again, so tell the user to approve it.
   - The installed or App Store copy: relaunch it if it was running.

## 7. Report and record

- Report what passed (one line per area, with the actual phrases for anything notable), what was fixed (before and after phrases), and what was not tested (variants, real keyboard delivery of VO keys, other languages, multiple displays).
- These are scripted VoiceOver commands, not physical key presses. Say so.
- For a larger app, keep a validation record in `docs/VoiceOver.md` (Weatherling's format: host OS build, app version, what was confirmed live, failures and fixes, an acceptance checklist for what remains).
- Commit following the repo's rules.

## App Store Connect accessibility labels

- VoiceOver support is declared under App Store Connect > App Accessibility. fastlane cannot set it: `deliver` only uploads text metadata and screenshots. Set it by hand in App Store Connect.
- The labels publish immediately and are not tied to an app version. Declare VoiceOver only once a version that passes is live, never for unreleased fixes.
- Apple's bar for claiming support is that common tasks can be completed with VoiceOver alone: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/voiceover-evaluation-criteria
