---
name: mobile-agent
description: Unified autonomous mobile testing and real-device control for both iOS (WebDriverAgent) and Android (UiAutomator2). Automatically detects connected devices via USB/Simulator/Emulator, supports compact token-efficient accessibility trees with @ref, ISTQB mobile test matrix, touch gestures, system alert handling, and device screenshots.
mcp: supergraph-wda, supergraph-uiautomator2
---

# /supergraph:mobile-agent

Unified autonomous mobile testing and real-device control for **iOS** and **Android** applications (Flutter, React Native, Swift iOS Native, Android Kotlin/Java).
Direct communication with **WebDriverAgent (WDA)** on iOS and **UiAutomator2 Server** on Android without heavy Appium middleware overhead.

Announce: "📱 /supergraph:mobile-agent — unified mobile testing across iOS & Android devices..."

---

## Why Direct Device Automation over Full Appium Server?

- **Unified Single Skill:** One skill handles both iOS (`WebDriverAgent`) and Android (`UiAutomator2`).
- **Zero Middleware Overhead:** Talks directly to WDA (`http://127.0.0.1:8100`) via `iproxy` or UiAutomator2 (`http://127.0.0.1:6790`) via `adb forward`. Latency is 3x to 5x lower per action.
- **Token Efficiency (Compact A11y Tree):** Bulky native XML dumps (5,000–30,000 lines) are compressed into ~150–400 tokens with reusable `@ref` identifiers (`@e1`, `@e2`).
- **Cross-Platform Parity:** Test the exact same user flow across real iPhones, iPads, Android phones, Simulators, and Emulators.
- **Delta Snapshots:** `--delta` captures only altered UI nodes between interactions, saving ~80% context tokens.
- **System Alert & Keyboard Handling:** Programmatically dismisses virtual keyboards and grants runtime permission dialogs (Camera, Location, Push Notifications).

---

## Auto-Discovery & Driver Routing

When `/supergraph:mobile-agent` is invoked:
1. Discover connected devices:
   - Call `wda_device_list` (checks `usbmuxd` for iPhones and booted Xcode Simulators).
   - Call `uiauto_device_list` (checks `adb devices` for Android phones and Emulators).
2. Route commands to the active platform:
   - **If iOS device connected:** Uses `wda_*` tools (`wda_session_start`, `wda_snapshot`, `wda_tap`, `wda_fill`).
   - **If Android device connected:** Uses `uiauto_*` tools (`uiauto_session_start`, `uiauto_snapshot`, `uiauto_tap`, `uiauto_fill`).
   - **If both connected:** Can execute test matrix concurrently on both devices for UI/cross-platform visual comparison.

---

## Prerequisites by Platform

### 🍏 iOS (One-Time Setup):
1. **Code Signing:** Open `WebDriverAgent.xcodeproj` in Xcode, configure your Development Team for `WebDriverAgentRunner`.
2. **Launch Runner on Device:** Start `WebDriverAgentRunner` on your device/simulator.
3. **USB Tunnel:** Run `iproxy 8100 8100 <UDID>` (verifiable via `curl http://127.0.0.1:8100/status`).

### 🤖 Android (One-Time Setup):
1. **Enable USB Debugging:** In Android Settings > Developer Options, toggle **USB Debugging** ON.
2. **Install UiAutomator2 Server:** Install `appium-uiautomator2-server.apk` & `test.apk` via `adb install -r`.
3. **USB Tunnel:** Run `adb forward tcp:6790 tcp:6790` and start instrumentation.

Check overall health anytime with:
```bash
bash plugins/supergraph/skills/mobile-agent/scripts/init-mobile-qa.sh doctor
```

---

## Core Interaction Loop

```
[1. Start Session] ────> [2. Compact Snapshot] ───> [3. Action (@ref)] ─────> [4. Assert & Delta]
  session_start            snapshot (-c)              tap @e2 / fill            snapshot (delta)
```

### 1. Observe Before Acting (Never Guess Coordinates)
Call `wda_snapshot` or `uiauto_snapshot` to get verified element references:
```text
[Accessibility Tree | App: com.example.app | Nodes: 4]
@e1 [StaticText] "Chào mừng bạn" bounds: [40, 120, 313, 32]
@e2 [TextField] "Email" value: "" bounds: [40, 200, 313, 44]
@e3 [TextField] "Mật khẩu" value: "" bounds: [40, 260, 313, 44]
@e4 [Button] "Đăng nhập" bounds: [40, 340, 313, 50]
```
For subsequent actions on the same screen, pass `delta: true` to receive only changes.

### 2. Flawless Soft Keyboard & Navigation
- Dismiss keyboard before tapping buttons at the screen bottom:
  - iOS: `wda_dismiss_keyboard()`
  - Android: `uiauto_hide_keyboard()`
- Android Back Key: `uiauto_press_keycode(4)`

### 3. Smart Waiting (Zero Flaky Tests)
- Use `wda_wait` or `uiauto_wait` with `text` or `ref` parameter instead of hardcoded sleeps.

---

## Available MCP Tools Reference

### iOS Tools (`supergraph-wda`):
- `wda_status`, `wda_device_list`, `wda_session_start`, `wda_session_stop`
- `wda_snapshot` (with `delta: true`)
- `wda_tap`, `wda_fill`, `wda_type`, `wda_press_button`
- `wda_dismiss_keyboard`, `wda_swipe`, `wda_wait`, `wda_screenshot`
- `wda_app_lifecycle`, `wda_handle_alert`, `wda_open_url`

### Android Tools (`supergraph-uiautomator2`):
- `uiauto_status`, `uiauto_device_list`, `uiauto_session_start`, `uiauto_session_stop`
- `uiauto_snapshot` (with `delta: true`)
- `uiauto_tap`, `uiauto_fill`, `uiauto_press_keycode`
- `uiauto_hide_keyboard`, `uiauto_swipe`, `uiauto_wait`, `uiauto_screenshot`
- `uiauto_app_lifecycle`, `uiauto_handle_alert`, `uiauto_open_url`

---

## Professional Mobile QA Workflow (ISTQB Standard)

### Phase 1: Test Matrix Generation
Scaffold comprehensive mobile test matrix covering 7 dimensions:
```bash
bash plugins/supergraph/skills/mobile-agent/scripts/init-mobile-qa.sh matrix <feature> <app_id> [iOS|Android|Cross-Platform]
```

### Phase 2: Autonomous Execution & Verification
For each testcase in the matrix:
1. Ensure session: `wda_session_start(bundle_id: "...")` or `uiauto_session_start(package_name: "...")`
2. Inspect: `wda_snapshot()` or `uiauto_snapshot()`
3. Act: `tap(@ref)` / `fill(@ref, "...")`
4. Assert: `wait(text: "...")` -> `screenshot(path: "docs/qa/evidence/<id>.png")`

### Phase 3: Structured Defect Reporting
When defects occur, capture visual evidence and scaffold a defect report:
```bash
bash plugins/supergraph/skills/mobile-agent/scripts/init-mobile-qa.sh bug <feature> MOB-BUG-001 "Button hidden behind keyboard"
```
Attach screenshot evidence saved via `screenshot`.
