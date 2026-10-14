---
name: expo
description: "Expo: managed workflow, EAS builds, config, permissions, OTA limits. Same engineering base as react-native with Expo focus; verify SDK version via official docs."
---

# expo

Expo: managed workflow, EAS builds, config, permissions, OTA limits. Same engineering base as react-native with Expo focus; verify SDK version via official docs.

## Failure modes

- Wrong-SDK API copied from latest docs; OTA update exceeding native-change limits (needs new build, not OTA); config-plugin conflicts; permission rationale missing on iOS; EAS credentials misconfigured.

## Escalation

- SDK behavior questions → research/documentation-search with detected SDK version; native modules beyond Expo → react-native + official docs.

## Official documentation research

Identify the Expo SDK version FIRST (package.json, app.json, app.config.*) — Expo APIs are SDK-gated. Research Router, EAS, config plugins, permissions, builds, and OTA in https://docs.expo.dev/ for that SDK (Router: https://docs.expo.dev/router/introduction/, EAS: https://docs.expo.dev/eas/). Registry: `../../research/documentation-search/references/framework-registry.yaml` (expo). Runtime procedure: `../../research/documentation-search/`.
