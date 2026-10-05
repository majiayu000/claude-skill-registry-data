---
name: update-gradle-dependency
description: Version-catalog procedure for adding or upgrading Gradle dependencies and plugins, plus the webmap (pnpm) dependency path, in femto-car-launcher. This skill is the dependency-update procedure SSOT; the project rule (catalog first, BOM precedence, Kotlin/Compose-Compiler lock-step) lives at .claude/rules/dependencies.md.
when_to_use: Use when adding or upgrading any Gradle dependency or plugin, or any webmap npm dependency. Triggers on "add Coil", "upgrade Compose BOM", "bump kotlin to X", "bump maplibre-gl", "upgrade vite".
argument-hint: "[group:artifact:version | bom-update]"
allowed-tools:
  - Read
  - Edit
  - Bash
  - Skill
paths:
  - gradle/libs.versions.toml
  - gradle/wrapper/gradle-wrapper.properties
  - app/build.gradle.kts
  - build.gradle.kts
  - settings.gradle.kts
  - webmap/package.json
  - webmap/pnpm-lock.yaml
  - webmap/pnpm-workspace.yaml
---

# Updating a Gradle dependency

Rules: see `.claude/rules/dependencies.md`.

## Procedure

1. **Decide the shape of the change.**
   - **New library** — add to `[versions]`, `[libraries]`, then
     reference via `libs.<alias>` in `app/build.gradle.kts`.
   - **Version bump** — edit the `[versions]` entry only.
   - **New plugin** — add to `[versions]`, `[plugins]`, then apply
     via `alias(libs.plugins.<alias>)` in the relevant
     `build.gradle.kts`.

2. **Edit `gradle/libs.versions.toml`** in this order:
   - `[versions]`: alphabetical by key, lowercase camelCase.
   - `[libraries]`: hyphenated keys (`androidx-core-ktx`).
   - `[plugins]`: hyphenated keys, version refs.

3. **Reference from `app/build.gradle.kts`** using the alias:

   ```kotlin
   implementation(libs.androidx.compose.material3)
   ```

   Hyphens in the catalog key become dots on the alias side.

4. **Sanity-check what resolved:**

   ```bash
   ./gradlew app:dependencies --configuration debugRuntimeClasspath \
     | grep -iE 'kotlin-stdlib|<your-artifact>' | head
   ```

5. **Verify** with the
   [`verify-android-build`](../verify-android-build/SKILL.md) skill.

6. **Document in the commit body** when:
   - Bumping a major version of any library.
   - Overriding a Compose BOM-managed artifact.
   - Adding an annotation processor / KSP plugin.
   - Bumping Kotlin (must include the matching Compose Compiler
     plugin bump).

## Webmap (pnpm) dependencies

Renovate automerges routine (non-major) webmap bumps — this path is
for manual or major bumps (`maplibre-gl`, Vite, TypeScript).

1. Edit `webmap/package.json` — or, for the Vite+ toolchain pins
   (`vite`, `vite-plus`), the catalog in `webmap/pnpm-workspace.yaml` —
   then run `pnpm install` under `webmap/` to refresh
   `pnpm-lock.yaml`.
2. For Vite or `maplibre-gl` majors, confirm Vite's `build.target`
   stays at the WebView floor defined in `AGENTS.md#tech-stack`.
3. For TypeScript majors, run `pnpm run check` under `webmap/` and
   treat compiler deprecation warnings as failures in the same
   bump. Never adopt a pre-stable compiler preview package (e.g. a
   native-compiler preview) as a build dependency. A TypeScript
   bump cannot move Vite's `build.target` (Vite ignores the
   tsconfig target), so the WebView-floor check in step 2 stays
   scoped to Vite / `maplibre-gl` bumps. Readiness criteria:
   `.claude/rules/webmap.md`.
4. Verify with `./gradlew assembleStableDebug` — the `:app:buildWebMap`
   task runs the pnpm build as part of it.

## Bulk-updating to latest versions

For routine version maintenance across the whole catalog, the
project ships `nl.littlerobots.version-catalog-update`:

- `./gradlew versionCatalogUpdate` rewrites
  `gradle/libs.versions.toml` in place, resolving each entry to its
  latest **stable** version (the plugin's default `versionSelector`,
  so no separate reporter plugin is needed).

Workflow:

```bash
./gradlew versionCatalogUpdate    # apply the update to libs.versions.toml
./gradlew spotlessApply           # tidy formatting
./gradlew assembleStableDebug     # verify
```

Review every diff before committing. Major-version bumps still
need the per-bump justification rule from
`.claude/rules/dependencies.md`. Two project-specific gotchas:

- **Toolchain coupling.** Bumping AGP can raise the required Gradle
  version — check the AGP release notes for the minimum required
  Gradle version before bumping, and update
  `gradle-wrapper.properties` in the same change:
  `./gradlew wrapper --gradle-version <v>
  --gradle-distribution-sha256-sum <sha> --distribution-type bin`.
  Kotlin and the `kotlin-compose` / `kotlin-serialization` plugin
  aliases move in lock-step automatically (shared `version.ref =
  "kotlin"` in the catalog).
- **A `maplibre-gl` bump can silently break tile rendering with no
  automated signal.** There is no automated tile-rendering test —
  `pnpm run check` (type-check + the `webmap/` unit tests) only
  covers pure logic (camera math, style JSON), not what actually
  paints. After any `maplibre-gl` major bump,
  manually verify the map still renders real tiles, ideally on a
  physical device — the `verify-on-emulator` skill's own "Known
  limitation" section explains why the emulator's GLES translator
  makes the emulator an unreliable check for this specific case.

## Skill-specific anti-patterns

- `implementation("io.coil-kt:coil-compose:2.6.0")` directly in
  `app/build.gradle.kts` — go through the catalog.
- Hardcoding a version inside `[libraries]` instead of using
  `version.ref`.
- Mixing the Compose BOM with explicit version pins on Compose
  artifacts without a justification line in the commit body.
- Adding a transitive dependency to silence a warning — investigate
  the root cause first.
