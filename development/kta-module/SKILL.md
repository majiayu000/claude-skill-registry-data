---
name: kta-module
description: Bootstrap a new Gradle module in any Kotlin Android project. Walks the user through choosing one of three module types — library module (`com.android.library`), feature module (regular Android library that hosts a feature/UI, install-time only), or dynamic feature module (`com.android.dynamic-feature`, on-demand/conditional/instant delivery). Use whenever the user wants to add a module, modularize code, extract a util/data/ui layer, create a new feature, set up Play Feature Delivery, or asks "should this be a library or feature module?". Discovers the project's existing conventions (plugin aliases, namespaces, sibling modules, version catalog) instead of hardcoding any. Pushes back on bad combos (e.g. utility code in a dynamic feature). Stops at scaffolding; app-level wiring is out of scope.
---

## Platform Tooling

- Use AskUserQuestion for blocking user choices or confirmations.
- Use WebFetch/WebSearch for current external docs or public web research.
- Use Task tool with subagent_type for delegation.
- Use Skill tool when chaining to another installed skill.

# Android Module Bootstrap

Create a new Gradle module in any Kotlin Android project. Three flavors are supported, and the user
MUST consciously pick one. This skill enforces an intake conversation and discovers project
conventions before scaffolding — no hardcoded plugin aliases, namespaces, or DI/nav patterns.

## Scope

- IN: Module type selection, Gradle skeleton, manifest, base package layout, `settings.gradle.kts`
  include, `dynamicFeatures` registration on the application module (DFM only).
- OUT: App-level wiring (registering DI graphs, navigation graphs, route classes, feature
  registries) — those are project-specific concerns left to the consumer or a follow-up step.

## Module Types (Decision Matrix)

| Type                | Plugin                                                          | Use When                                                                                                               | Anti-pattern                                                                         |
|---------------------|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| **Library**         | `com.android.library`                                           | Reusable utilities, design tokens, repositories, use cases, shared UI atoms                                            | Owns a navigation route into an app shell                                            |
| **Feature Module**  | `com.android.library` (+ Compose/Hilt/Koin as project requires) | Feature always shipped, install-time only, no on-demand needed                                                         | Pure utility with no feature surface                                                 |
| **Dynamic Feature** | `com.android.dynamic-feature`                                   | Independently deliverable feature: on-demand, conditional, instant-app, or large feature you may want to defer install | Tiny shared util, single composable, code consumed by other modules (creates cycles) |

Read `references/module-types-decision.md` for full pros/cons, sizing heuristics, and recovery
paths.

## Step 0 — Discover Project Conventions (DO THIS FIRST)

Before any question or scaffold, read the project to learn its conventions. Do not guess; do not
hardcode this skill's prior assumptions.

1. **Plugin aliases / version catalog**: Read `gradle/libs.versions.toml` (if present). Look for
   plugin aliases mapping to `com.android.library`, `com.android.dynamic-feature`,
   `com.android.application`, `org.jetbrains.kotlin.android`, Compose, KSP, Hilt, etc. Also check
   for project-internal convention plugins (e.g. anything under `build-logic/` or pre-compiled
   script plugins). Use whatever the project already uses.
2. **Sibling modules**: List existing modules from `settings.gradle.kts` and read 1–2 representative
   `build.gradle.kts` files (one library, one feature/dfm if present). Match their plugin block,
   dependency style, and `android { }` config (namespace pattern, buildFeatures, testing libs).
3. **Application module**: Find the `com.android.application` module. Note its package,
   `dynamicFeatures = setOf(...)` block (if any), and how it depends on existing libraries/features.
4. **Namespace pattern**: Derive the convention from sibling modules (e.g. `com.acme.feature.X`,
   `com.acme.lib.X`). Don't invent a new one.
5. **DI / Nav / Compose**: Check whether siblings use Hilt, Koin, Dagger, Compose Navigation, etc.
   The new module should match.
6. **JVM / SDK**: Detect `compileSdk`, `minSdk`, `targetSdk`, JVM target, Kotlin version from
   existing modules or root config. If a convention plugin sets these, just apply the convention
   plugin and don't redeclare.

If `libs.versions.toml` is missing, fall back to vanilla AGP plugin IDs (`com.android.library`,
`com.android.dynamic-feature`, `org.jetbrains.kotlin.android`,
`org.jetbrains.kotlin.plugin.compose`).

State your findings to the user in 3–5 lines so they can correct you before you scaffold.

## Step 1 — Mandatory Intake

Ask the user — sequentially, plain text, not all at once:

1. **What is the module's purpose?** (One sentence: "audio playback util", "settings feature", "AI
   assistant feature deferred install"…)
2. **Who consumes it?** (App only / multiple features / shared infra)
3. **Does it own a user-facing screen with a nav route?** (yes / no)
4. **Delivery requirement:** install-time always, or on-demand / conditional / instant?
5. **Rough size:** <500 LOC / 500–5k / 5k+

Map answers to a recommendation:

- Purpose is "util / shared / tokens / repo / use case" + no route → **Library**
- Owns a route + always shipped → **Feature Module** (or **Dynamic Feature** if the codebase clearly
  prefers DFMs — detect this from sibling modules)
- Owns a route + on-demand/conditional/instant OR very large → **Dynamic Feature**
- If `dynamicFeatures = setOf(...)` is empty in the application module and there are no existing
  DFMs, default to **Feature Module** for new features. If the project already uses DFMs, default to
  **Dynamic Feature** to match precedent.

## Step 2 — Recommend + Confirm

State the recommended type with one-sentence justification and cite the convention you observed.
Then list pros/cons of all three (pull from `references/module-types-decision.md`). End with: "Pick
library / feature / dynamic-feature, or tell me your reasoning to override."

### Pushback Rules (be direct, not sycophantic)

If the user picks a type that contradicts their answers, push back BEFORE scaffolding. Do not
silently comply.

- User says "util library for string helpers" + picks **dynamic-feature** → Warn: "DFMs are for
  independently deliverable user-facing features. A util has no route, no delivery story, and
  forcing it into a DFM creates a cyclic application-module dependency for nothing. Recommend
  Library. Override?"
- User says "code consumed by other library modules" + picks **dynamic-feature** → Hard warn: "DFMs
  reverse-depend on the application module; other libraries cannot depend on a DFM (cycle). This
  will not compile. Must be a Library."
- User says "instant app / on-demand / conditional" + picks **library** or **feature** → Warn: "
  Plain library and feature modules always ship in the base APK. You lose the delivery flag you
  asked for. Must be Dynamic Feature for on-demand."
- User picks a type that contradicts the codebase's clear convention → Note the divergence, ask
  whether it's intentional. Don't silently break consistency.

Wait for explicit "go" before Step 3.

## Step 3 — Scaffold

Once type is locked, follow the matching reference:

- **Library** → `references/library-module-structure.md`
- **Feature Module** → `references/feature-module-structure.md`
- **Dynamic Feature** → `references/dfm-structure.md` (+ `references/delivery-options.md` if
  on-demand/conditional)

Then update root files:

1. `settings.gradle.kts` — add `include(":<path>")`. Mirror the path style observed in the project (
   flat `:my-lib` vs grouped `:feature:my-feature`).
2. **DFM only:** the application module's `build.gradle.kts` → add to
   `dynamicFeatures += setOf(...)` (or `dynamicFeatures = setOf(...)` depending on existing style).
3. **DFM only:** add `res/values/strings.xml` with the `dist:title` resource referenced by the
   manifest.

When writing files, substitute the project's actual conventions:

- Plugin aliases the project already uses (convention plugins, version-catalog aliases, or raw
  plugin IDs)
- Namespace matching the project's pattern
- DI / nav / Compose deps mirroring the sibling module you sampled
- JVM target / SDK levels from the project's existing config (or omit if a convention plugin handles
  them)

Reference templates show vanilla AGP defaults — **adapt to what you discovered in Step 0**.

## Step 4 — Verify

- Run `./gradlew :<module-path>:compileDebugKotlin` to confirm the skeleton compiles.
- If the project requires `google-services.json` or other secrets to assemble, prefer
  `compileDebugKotlin` over `assembleDebug` for verification.
- Report: module path, plugin used, what's wired, what app-level steps the user must do next (e.g.
  register DI/nav, populate routes — these are project-specific).

## References

- `references/module-types-decision.md` — Full decision matrix, sizing, anti-patterns, recovery
  paths
- `references/library-module-structure.md` — Plain library template (vanilla AGP)
- `references/feature-module-structure.md` — Feature as regular library template
- `references/dfm-structure.md` — Dynamic feature template
- `references/delivery-options.md` — install-time / on-demand / conditional / fusing
