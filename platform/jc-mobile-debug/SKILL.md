---
name: jc-mobile-debug
description: Use when reviewing or debugging the JapaConnect Flutter mobile app (apps/mobile). Diagnoses widget rebuild loops, Riverpod state scoping, API client drift, JWT refresh loops, secure-storage token issues, push notification wiring, layout overflow, unbounded constraints, and build toolchain failures per §77, ADR-067, ADR-074, and ADR-113.
---

# JapaConnect Mobile App — Debug Skill

You are debugging the Flutter mobile client. The app is a thin `/api/v1` client in `apps/mobile/` with a shared `packages/japaconnect_core/` package. Most bugs are in one of three layers: **UI/rendering**, **state/HTTP**, or **toolchain/runtime**. Isolate the layer first, then apply the matching diagnostic path.

## Step 0 — Confirm the Environment

1. `flutter doctor` must pass for the platform you are debugging (Android SDK / Xcode / CocoaPods).
2. The backend must be running (`go run ./...` or `make dev`) at the URL the mobile client points to.
3. The mobile app must build and run:
   - Android: `flutter run --flavor dev` or `flutter run` from `apps/mobile/`
   - iOS: `flutter run -d ios` (macOS + Xcode required; Linux agents cannot build iOS)
4. If `apps/mobile/` does not exist, the mobile app is not yet implemented — stop and report that, do not fabricate a fix.

## 1. UI / Rendering Bugs

### 1.1 Layout overflow (`A RenderFlex overflowed by ... pixels`)

- Wrap the overflowing widget in `Expanded` / `Flexible` inside a `Column` or `Row`.
- For horizontal lists, use `ListView` with `scrollDirection: Axis.horizontal` and bounded item widths.
- For long text, wrap in `Expanded` with `Text(maxLines: ..., overflow: TextOverflow.ellipsis)`.
- Check `SafeArea` usage at screen edges and notches.
- Test on the **smallest Android device** the audience uses (low-end screen height ~640dp).

### 1.2 Unbounded constraints (`BoxConstraints forces an infinite width/height`)

- Common in `ListView` inside `Column` without `Expanded`.
- Common in `Row`/`Column` containing a `ListView` directly.
- Fix: give the scrollable a bounded size (e.g., `Expanded(child: ListView(...))`).

### 1.3 Widget rebuild loops

- Check for `setState` inside `build` or inside an `async` callback that fires repeatedly.
- With Riverpod: ensure providers are not being watched inside a `build` method in a way that triggers self-mutation.
- Use `const` constructors for static subtrees.
- Use `RepaintBoundary` around heavy animated content if needed.

### 1.4 Images not loading / wrong aspect

- Verify `CachedNetworkImage` has `placeholder` and `errorWidget`.
- Verify the image URL is absolute and the backend serves it (not a relative web path).
- Verify the container constrains width or height; `CachedNetworkImage` without bounds is a common source of layout overflow.

## 2. State / HTTP Bugs

### 2.1 API calls fail with 401 in a loop

- **Root cause 1:** access token expired and refresh token is invalid/missing.
  - Check `flutter_secure_storage` contains the refresh token.
  - Check `AuthService.refresh()` is called and the new access token is stored in memory (not secure storage).
- **Root cause 2:** `X-Device-Id` header is missing.
  - Every authenticated request must include the device ID from `flutter_secure_storage`.
- **Root cause 3:** backend `/api/v1/auth/refresh` route is not wired or returns a non-standard error.
  - Probe with `curl -v -H "Authorization: Bearer <token>" -H "X-Device-Id: <id>" http://localhost:8080/api/v1/auth/refresh`.

### 2.2 Hardcoded data / Rule 16 violations

- Search for lists, maps, or mock user objects in `apps/mobile/lib/features/`.
- Any `const` list of countries, currencies, languages, nav items, or options is a Rule 16 violation unless it is a pure client-side constant (e.g., static animation durations).
- Replace with API calls through `japaconnect_core`.

### 2.3 `japaconnect_core` API client drift

- The OpenAPI spec (§47) is the source of truth.
- Regenerate the Dart client after backend route changes: `dart run build_runner build --delete-conflicting-outputs` (or the documented generator command in `packages/japaconnect_core/`).
- Verify the method names and request shapes match the live backend.
- Do not call `http.get` or `dio` directly in feature code.

### 2.4 Riverpod state not updating

- Verify the provider is `Scoped` at the right level.
- Verify `ref.watch` (rebuild) vs `ref.read` (one-shot) usage.
- Verify `AsyncNotifier` / `StateNotifier` methods call `state = ...` (or `state = AsyncValue.data(...)`) after the async operation.
- Verify no widget is rebuilding because a parent provider is emitting `AsyncLoading` repeatedly.

### 2.5 Push notifications not received

- Check FCM/APNs credentials are seeded in `system_settings` (`push.fcm_server_key`, `push.apns_*`, `push.enabled = true`).
- Check `POST /api/v1/me/devices` is called and returns 200 with the token stored.
- Check `device_tokens` table has `is_active = true` for the user's device.
- Check the backend `notification:send_push` Asynq task is enqueued when a notification is generated for the user.
- Check the app requests notification permission on first open.
- Check the app handles `onMessage` (foreground), `onBackgroundMessage`, and `onMessageOpenedApp` correctly.

### 2.6 Secure-storage issues

- `flutter_secure_storage` reads are async and can fail silently on some Android devices if the keystore is locked.
- On iOS, the keychain is not shared across app groups unless configured.
- Never store the access token in secure storage — it must live in memory only.
- On logout, delete the refresh token, device ID, and any persisted drafts.

## 3. Toolchain / Runtime Bugs

### 3.1 Android build fails

- Run `flutter clean` then `flutter pub get`.
- Check `android/app/build.gradle` `compileSdk`, `minSdk`, and `targetSdk`.
- Check `pubspec.lock` for plugin version conflicts.
- If Gradle daemon is stuck: `pkill -f "gradle"` and retry.
- Common on agents: `JAVA_HOME` must point to a JDK 17+ (not JRE).

### 3.2 iOS build fails (macOS only)

- `cd ios && pod install` when `Podfile.lock` is out of date.
- `flutter clean` and rebuild.
- Xcode signing / provisioning is a manual step; the agent can build for the simulator without signing, not for a device.
- `CocoaPods` must be installed and `pod setup` must have run.

### 3.3 Simulator / emulator not launching

- List devices: `flutter devices`.
- Start an emulator: `flutter emulators --launch <id>`.
- For iOS simulator, the host must be macOS.

### 3.4 `flutter analyze` reports issues

- Run `flutter analyze` in `apps/mobile/` and `packages/japaconnect_core/`.
- Treat all `error`-level issues as blockers.
- `info` and `warning` level issues should be cleaned up before committing; do not leave known warnings unaddressed.

## 4. Backend vs Frontend Isolation

When a mobile screen fails, determine which side is broken:

- **Frontend bug:** UI renders but shows wrong data, crashes on tap, overflow, or wrong state.
- **Backend bug:** API returns 404/500/401, wrong JSON shape, missing field, or missing route.
- **Contract bug:** the API works in isolation, but the generated `japaconnect_core` client expects a different shape. This is a drift bug — fix the client generation or the backend contract, then regenerate.

For backend contract bugs, switch to `jc-backend-debug` and fix the backend. Do not paper over contract drift in the Flutter client.

## 5. Debug Checklist

- [ ] `flutter doctor` passes for the target platform
- [ ] App builds and runs on at least one emulator / simulator
- [ ] Backend is running and reachable
- [ ] `flutter analyze` returns zero errors
- [ ] `flutter test` passes for the affected feature
- [ ] Network requests include `Authorization: Bearer <token>` and `X-Device-Id: <id>`
- [ ] The access token is not written to `flutter_secure_storage` or logs
- [ ] Push token registration/unregistration is wired (where applicable)
- [ ] No hardcoded data or mock user objects in feature code
- [ ] UI tested at 320dp and 720dp widths
