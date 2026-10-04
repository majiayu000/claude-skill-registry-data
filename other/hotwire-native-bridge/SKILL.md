---
name: hotwire-native-bridge
description: Create and validate Strada / Hotwire Native bridge components across web (Stimulus), iOS (Swift), and Android (Kotlin). Use when adding native UI driven by the web — a native menu, share button, toolbar, native form submit — to a Hotwire Native app, or when a bridge component "works on web but not in the app", a native control is missing/duplicated, or a value sent from the web never arrives natively. Generates the three platform halves from one component name and lints the cross-platform contract for name mismatches and silently-dropped payload fields.
---

# Hotwire Native bridge components (Strada)

A Strada bridge component has **three halves that must agree**: a web Stimulus
controller (`BridgeComponent`), an iOS `BridgeComponent` (Swift), and an Android
`BridgeComponent` (Kotlin). They are bound by an implicit **contract**:

1. A **component name** string (e.g. `"nav-menu"`) — identical on all three sides.
2. **Message events** — `connect` / `disconnect` plus any custom events.
3. A **JSON payload shape** — every key the web sends must be decoded on *both*
   native sides, or it is silently dropped (no error).

Getting any of these subtly wrong is the #1 time-sink: a name typo makes the
component invisible; a payload key missing from one native struct vanishes with no
crash. This skill generates the three halves consistently and lints the contract.

See [`references/bridge-contract.md`](references/bridge-contract.md) for the full contract + the real Piazza
`nav-menu` example, and the gotcha catalogue.

## When to use

- Adding a native component backed by web markup (menu, toolbar, share sheet,
  native submit button, native picker).
- Debugging "works on web, broken/missing in the native app", a duplicated native
  control after navigation, or a value that doesn't reach the native side.
- Reviewing a PR that touches any `*Component.swift` / `*Component.kt` /
  `controllers/bridge/*.js` — run the linter.

## Generate a new component

```bash
scripts/new_bridge_component.sh <name-in-kebab> \
  --web   path/to/piazza-web \
  --ios   path/to/piazza-ios \
  --android path/to/piazza-android \
  --package com.yourco.app
```

Writes (refuses to overwrite):
- `web/app/javascript/controllers/bridge/<snake>_controller.js`
- `ios/<App>/Bridge/<Pascal>Component.swift`
- `android/.../<Pascal>Component.kt`

Then **register** it (the generator prints these — it does NOT edit registries).
**Hotwire Native 1.x** (default — templates target this):
- **iOS:** `Hotwire.registerBridgeComponents([<Pascal>Component.self])` in
  `AppDelegate`, **before any `Navigator` is created** (make the navigator lazy, else
  the component never attaches — hotwire-native-ios #35). `import HotwireNative`.
- **Android:** `Hotwire.registerBridgeComponents(BridgeComponentFactory("<name>",
  ::<Pascal>Component))` in your `Application` subclass (also set
  `Hotwire.config.jsonConverter = KotlinXJsonConverter()`). Imports from
  `dev.hotwire.core.bridge`; destination type `HotwireDestination`.
- **Web:** install `@hotwired/hotwire-native-bridge`; Stimulus auto-registers the
  controller as `bridge--<name>` if it lives under `app/javascript/controllers/bridge/`.

> **Strada-beta apps** (the Piazza example repos still use this): iOS adds
> `<Pascal>Component.self` to a `BridgeComponent.allTypes` extension; Android adds the
> factory to a `bridgeComponentFactories` list passed to the WebFragment; web imports
> `@hotwired/strada`. Same contract, older wiring. Full mapping:
> `references/bridge-contract.md`.
- **Markup:** `data-controller="bridge--<name>"`, item targets
  `data-bridge--<name>-target="item"`, payload attrs via `data-bridge-<attr>`
  (read in JS with `bridgeElement.bridgeAttribute("<attr>")`).

Fill in the `TODO`s in each native half (render UI from `data`, reply on selection).

## Lint the contract

```bash
scripts/lint_bridge_contract.sh --root <dir-with-the-three-repos>
# or: --web W --ios I --android A
```

Checks, and exits non-zero on drift:
- **Name parity** — every component name present on web, iOS, *and* Android
  (catches typos / unregistered = invisible components).
- **iOS registration** — a component declared but absent from `allTypes`.
- **Payload field parity** — a field decoded on one native side but not the other
  (the silent-drop class — e.g. Piazza's `icon`, sent by web + decoded on iOS, has
  no field on Android).

Heuristic text scan (grep/awk), not a parser — conservative, good enough to gate a
PR. It is the check that pays for itself: payload drift produces no runtime error.

## The rules that matter (least astonishment)

- The component `name` is an API across three repos — renaming means three edits.
- Add a payload key → add it to the Swift `Decodable` *and* the Kotlin
  `@Serializable` in the same change, or it silently disappears on the side you
  forgot.
- `disconnect()` must undo what `connect()` rendered, or native controls duplicate
  on the next Turbo navigation.
- Components degrade to plain web when no native bridge is present — keep the web
  markup usable on its own (the JS hides it only when the bridge connects).
