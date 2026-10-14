---
name: react-native
description: "React Native: navigation, permissions, iOS/Android differences, offline, storage, deep linking, push, lists/gestures/animations. Never apply browser assumptions blindly."
---

# react-native

A native app that happens to use React: platform differences first, browser habits left behind.

## Activate when

- Building or changing React Native screens, navigation, permissions, storage, notifications, or native integrations.

## Do NOT activate for

- Expo-managed workflow specifics (see expo); web React (see react).

## Inspection

Check react-native version, navigation library, permission flows, storage choices, and where platform forks (`*.ios.*` / `*.android.*`) already exist.

## Decision rules

- Navigation: auth-gated stacks, deep links handled after hydration; test back behavior per platform.
- Permissions: request with rationale, handle denial + "don't ask again" permanently-denied states; declare in manifests.
- Storage: secure store for secrets, MMKV/fast store for cache, SQLite for structured offline; encrypted where sensitive.
- Lists/media: virtualized lists with estimated sizes; Hermes on; cached images; test on low-end Android, not just simulators.
- Push: token lifecycle (refresh, logout invalidation), deep-link routing from cold start and background.

## Procedure

1. Detect versions (react-native + Expo SDK if present); research platform APIs for those versions.
2. Implement per-platform with shared core; fork only at genuine divergence.
3. Cover offline, permission-denied, and cold-start push paths explicitly.
4. Verify: both platforms built, key flows on a real low-end device, permission matrices walked, no browser-only assumptions (no DOM, no cookies-as-sessions).

## Failure modes

- iOS-only testing; permission denial unhandled; AsyncStorage for secrets; unvirtualized thousand-row lists; deep links racing hydration.

## Escalation

Expo specifics → expo; version facts → research/documentation-search (registry: react-native, expo).

## References

- Registry: `../../research/documentation-search/references/framework-registry.yaml` (react-native).
- Related: `../expo/`, `../../frontend/accessibility/`.
