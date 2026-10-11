---
name: react-native
description: React Native and Expo rules, patterns, and checklists. Load when react-native is detected.
---

## Detection Signals

Load this skill when **any** of the following are found:

| Signal | File / Dependency |
|--------|------------------|
| `react-native` in `package.json` dependencies | `package.json` |
| Metro bundler config | `metro.config.js` / `metro.config.ts` |
| React Native CLI project | `android/` + `ios/` directories together |
| Expo project | `app.json` with `"expo"` key, `eas.json`, or `expo` in `package.json` |
| Expo Modules | `expo-modules-core` in `package.json` |

---

## Project Structure

```
src/
├── app/           # Root navigation and app entry
├── components/    # Reusable, platform-agnostic UI components
├── screens/       # Screen-level components (one per route)
├── hooks/         # Custom hooks (no UI, no side effects tied to render)
├── store/         # Global state (Redux, Zustand, Jotai)
├── services/      # API clients, native module wrappers
├── utils/         # Pure functions, formatters, constants
├── types/         # Shared TypeScript types and interfaces
└── assets/        # Images, fonts, icons
```

- One screen = one file; never put multiple screens in one file
- Platform-specific files use `.ios.tsx` / `.android.tsx` suffixes — only when unavoidable
- Shared business logic must live in hooks or services, never inside screen components

---

## Expo: Managed vs Bare Workflow

→ Load `skills/mobile/react-native/references/expo-vs-bare.md` when deciding between Managed and Bare workflows, configuring EAS Build, or handling OTA updates.

---

## Navigation

→ Load `skills/mobile/react-native/references/navigation.md` when working with React Navigation, deep links, or back behavior.

---

## State Management

→ Load `skills/mobile/react-native/references/state-management.md` when choosing or implementing state management (Zustand, Redux Toolkit, Jotai, TanStack Query).

---

## Performance

### Lists
- **Always use `FlatList` or `SectionList`** for dynamic lists — never `ScrollView` + `.map()` for more than ~10 items
- Prefer **FlashList** (`@shopify/flash-list`) over `FlatList` for large lists (> 100 items) — it is significantly faster
- Set `keyExtractor` to a stable, unique string — never use array index
- Use `getItemLayout` when item height is fixed to skip measurement overhead
- `removeClippedSubviews={true}` for long lists on Android

### Renders
- `React.memo` on components that receive stable props and re-render often
- `useCallback` on functions passed as props to memoized children
- `useMemo` only for genuinely expensive computations — not as a default
- Avoid anonymous functions and inline objects in JSX props (create new references each render)

### Images
- Use `expo-image` or `react-native-fast-image` instead of the built-in `Image` — both support caching and progressive loading
- Always specify `width` and `height` — never let images cause layout shift
- Use WebP format for all non-transparent images

### JavaScript Engine
- **Hermes** is enabled by default in React Native 0.70+ and all Expo SDK 47+ projects — do not disable it
- Profile with Flipper (bare) or React DevTools Profiler (both workflows) before optimizing

---

## Native Integrations

### Permissions (Runtime)
Always request permissions at the moment they are needed, not at app launch:

```tsx
import * as Location from 'expo-location'; // Managed
// or
import { request, PERMISSIONS } from 'react-native-permissions'; // Bare

const requestLocation = async () => {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') {
    // Show rationale or graceful degradation — never crash
  }
};
```

- Check permission status before requesting — avoid re-prompting after a denial
- Always handle the `denied` and `blocked` states gracefully
- On iOS: populate all `NSUsageDescription` keys in `app.json → ios.infoPlist` before submitting

### Push Notifications
- Use `expo-notifications` (Managed) or `@react-native-firebase/messaging` (Bare/Firebase)
- Always request permission before registering for push tokens
- Store the device token server-side tied to the user, not the device
- Handle foreground, background, and quit-state notifications explicitly

### Expo Modules API (custom native modules)
When a native module is not available in the Expo SDK:
1. Create an Expo Module: `npx create-expo-module my-module`
2. Implement in Swift (iOS) and Kotlin (Android) within the module
3. Export via `ExpoModulesCore` — avoids the old bridge entirely
4. For Bare workflow: native modules can still use the traditional bridge, but prefer the new architecture (TurboModules) for new code

---

## Security

- **Never hardcode API keys or secrets** in JS code — they end up in the bundle; use environment variables via `expo-constants` or a secrets manager
- **Secure storage for tokens**: `expo-secure-store` (Managed) or `react-native-keychain` (Bare) — both use iOS Keychain and Android Keystore
- **Certificate pinning**: implement for apps handling financial or health data
- **Jailbreak/root detection**: use `expo-device` (`isRooted`) or `react-native-jail-monkey` for sensitive apps
- **Network**: enforce HTTPS; configure App Transport Security (iOS) and Network Security Config (Android) to disallow cleartext

---

## Testing

| Layer | Tool | Purpose |
|-------|------|---------|
| Unit | **Jest** + `@testing-library/react-native` | Component rendering and hooks |
| Integration | **Detox** | Full device E2E (real device or simulator) |
| Manual | Physical device on each target OS version | Permissions, gestures, platform quirks |

- Test on a **real device** before any release — simulators do not replicate memory pressure, battery, or actual GPU behavior
- Detox tests must run in CI against the `preview` build profile
- Snapshot tests: use sparingly — they break on any style change and add noise

---

## App Store & Play Store — Publication Checklist

### Both Platforms
- [ ] App icon in all required sizes (use `expo-icon-generator` or Sketch/Figma export)
- [ ] Splash screen tested on all target screen sizes
- [ ] Version (`version`) and build number (`ios.buildNumber` / `android.versionCode`) incremented
- [ ] No development/debug code in production build (`__DEV__` guards removed)
- [ ] Privacy policy URL set in store listing and `app.json` (required for apps accessing camera, location, contacts)
- [ ] App tested on minimum supported OS version

### iOS (App Store)
- [ ] `bundleIdentifier` matches App Store Connect entry
- [ ] Signing configured: distribution certificate + provisioning profile (or EAS Credentials)
- [ ] All `NSUsageDescription` keys populated in `infoPlist`
- [ ] TestFlight build tested by at least one external tester
- [ ] Age rating and content declarations filled in App Store Connect
- [ ] App Review notes added for any feature requiring special permissions

### Android (Play Store)
- [ ] `package` name matches Play Console entry
- [ ] Upload keystore stored securely (EAS Credentials or password manager) — **never commit to git**
- [ ] `targetSdkVersion` ≥ current Google Play requirement (updated annually)
- [ ] Adaptive icon configured (`android.adaptiveIcon`)
- [ ] Internal / Closed testing track tested before production rollout
- [ ] Data safety section filled in Play Console
