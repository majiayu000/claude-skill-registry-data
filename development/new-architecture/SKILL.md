---
name: new-architecture
description: React Native New Architecture (Fabric, TurboModules, bridgeless) compatibility. Use when a library breaks under it, for newArchEnabled questions, or errors mentioning codegen, Fabric, ViewPropTypes, requireNativeComponent.
user-invocable: false
---

# New Architecture compatibility

## Where things stand

The New Architecture (Fabric renderer, TurboModules, bridgeless mode) is the only architecture on current versions: Expo SDK 55+ has no option to disable it, and React Native has been deleting the legacy code paths outright. The escape hatch era is over; staying on the old architecture means staying on SDK 54 / RN 0.81 or older, which is a parking lot, not a plan.

Most actively maintained libraries work. The pain is concentrated in libraries that were abandoned between 2021 and 2023, which is exactly the set of libraries older production apps depend on.

## Check compatibility before debugging

Do not debug a library into working. First find out what its status actually is:

1. `npx expo-doctor` flags known-incompatible and unmaintained packages using React Native Directory data.
2. Search the package on reactnative.directory and check the New Architecture column and the last release date.
3. Check the library's GitHub issues for "new architecture" or "fabric". An open issue from years ago with no maintainer response answers your question.

The decision tree is short. Maintained and compatible: upgrade to the compatible version. Maintained but not yet compatible: the interop layer probably carries you (below). Abandoned: replace it now, not after the next SDK upgrade makes it worse.

## The interop layer

Legacy view managers and modules run under an interop layer on the New Architecture, and most old libraries work through it without knowing. When one does not, the failures look like this:

- `ViewPropTypes` was removed from react-native. Old libraries that import it crash at require time. A patch that swaps the import for `deprecated-react-native-prop-types` keeps a corpse walking, but treat it as a signed IOU to replace the library.
- `requireNativeComponent` double registration: "Tried to register two views with the same name". Usually the library ships both old-style manual registration and codegen output. Check for a newer release first; this got fixed in most living libraries.
- `UIManager.getViewManagerConfig('X')` returning nothing: the component name the JS side asks for does not match what the native side registered. Version mismatch between the library's JS and native halves, typically from a partial upgrade. Reinstall pods / rebuild after cleaning.

## Codegen errors during build

Codegen runs at build time and its failures land in the native build log, not in Metro:

- iOS: run `cd ios && pod install` after any dependency change, because codegen artifacts are generated during pod install. Stale artifacts after an upgrade: clean `ios/build` and reinstall pods.
- Android: stale generated code lives under `android/app/build/generated`. `./gradlew clean` regenerates it. If a library's codegen spec is simply broken, the error names the library's spec file, which makes the culprit unambiguous.

## The opt-out that no longer exists

On SDK 54 / RN 0.81 and earlier, `"newArchEnabled": false` in app config turned the whole app back to the old architecture. On SDK 55+ and RN 0.82+ the flag is ignored: there is no switch, and pinning the project to an old SDK to keep it is trading one blocked library for a growing pile of them.

So when a library breaks, the real options are exactly three: upgrade the library, apply a one-line community patch with patch-package, or swap to the maintained replacement everyone else already swapped to. Check the library's issue tracker first; one of the three is usually waiting there.

## Replacements for the usual suspects

When an abandoned library blocks you, these swaps are well-trodden and safe:

- react-native-fast-image → expo-image (works in bare projects too)
- react-native-camera → react-native-vision-camera or expo-camera
- react-native-push-notification → notifee or expo-notifications
- react-native-snap-carousel → react-native-reanimated-carousel
- Animation wrappers (animatable and friends) → reanimated directly

Keep the old library only when it is load-bearing and the replacement needs a real migration; then schedule the migration instead of forgetting it.

## Verifying a migration

There is no flag to flip any more; the migration happens when an app that still ran on the legacy architecture (SDK 54 or older with `newArchEnabled: false`) moves to SDK 55+. Do that upgrade on a branch, then exercise the app where Fabric differs: screens with heavy lists, custom native views, gesture-driven animations, modals and text inputs. Layout rounding and z-order edge cases show up visually, not in logs, so this is an eyes-on-device task rather than a unit test task.
