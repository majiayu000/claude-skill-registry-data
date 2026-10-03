---
name: kotlin-toolchain
description: Use when working with JetBrains Kotlin Toolchain v0.13.x, formerly Amper, including module.yaml, project.yaml, module templates, nested templates, libs.versions.toml, the kotlin CLI wrapper, `//` project paths, Kotlin/JVM, Android, iOS, Kotlin Multiplatform, Kotlin/JS, Kotlin/Wasm (wasm-js, wasm-wasi), Kotlin/Native, server-side apps, dependencies, testing, SwiftPM dependencies, KMP library publishing, Maven Central, build plugins, built-in technologies (Compose, Ktor, Spring Boot, serialization, kotlinx.rpc, DataFrame, Power Assert, KSP, Lombok), Maven and Gradle migration, JDK provisioning, and toolchain caches.
---

# Kotlin Toolchain

Use this skill for JetBrains Kotlin Toolchain work: declarative YAML build configuration, the `kotlin` CLI, product
types, dependency wiring, multiplatform layout, publishing, and local build plugins.

Do not apply this skill to Gradle or Maven build editing unless the task is explicitly about converting a Gradle or
Maven project to Kotlin Toolchain. Kotlin Toolchain is not Gradle, not Maven, and not the old Amper `*.amper` syntax.

## Source Snapshot

This skill is generated from the official upstream docs for `v0.13.0`, the default supported version:

- Repository: `https://github.com/JetBrains/kotlin-toolchain`
- Ref: `v0.13.0`
- SHA: `abc7a5f7579e9ef267107782048c76777f0bf932`
- Full aggregate: `generation/upstream-docs-v0.13.0.md`
- Generation notes: `generation/generation-steps.md`

Statements here come from those docs, from the `v0.13.0` release notes, and from spot-checks against the tagged source
tree. Where the docs lag the code, this skill follows the code and says so. The GitHub Actions section below is
separately maintained Heapy integration guidance, not part of that upstream snapshot.

The tagged docs still contain stale Kotlin defaults, Android namespace defaults, and Wasm-test limitations. This
skill follows the tagged source for those points; see [migration and source notes](references/migrating-0.12-to-0.13.md).

This skill and its topic references target the tagged `0.13.0` release. Check the project wrapper before applying
version-sensitive defaults or syntax.

The project is Alpha and the docs move quickly. Treat defaults and edge-case syntax as version-sensitive. When precision
matters, inspect the local project, run `./kotlin show ...`, and grep the pinned aggregate (~300 KB — search it, do not
read it whole).

Internal names still contain `Amper` in expected places: `jvm/amper-plugin`, `org.jetbrains.amper.plugins`, and some
distribution paths. Do not rename those to `kotlin`. The YouTrack project, however, moved from `AMPER` to `KTC`.

## Reference Map

`SKILL.md` carries the operational base. Load a reference only when the task goes past it.

| Reference | Load it for |
|---|---|
| [`references/cli.md`](references/cli.md) | CLI commands and flags, wrapper install, provisioning, cache dirs, JDK provisioning |
| [`references/project-model.md`](references/project-model.md) | `project.yaml`, `module.yaml` keys, path notation, module layout |
| [`references/product-types.md`](references/product-types.md) | Per-product-type detail: entry points, build output, packaging limits |
| [`references/dependencies.md`](references/dependencies.md) | Dependency notation, scopes, classifiers, catalogs, repositories |
| [`references/settings.md`](references/settings.md) | Full `settings` tree, defaults table, compiler knobs |
| [`references/builtin-tech.md`](references/builtin-tech.md) | Compose, serialization, Ktor, Spring, RPC, DataFrame, Power Assert, KSP, Lombok, Parcelize |
| [`references/multiplatform.md`](references/multiplatform.md) | Platform hierarchy, aliases, propagation, cinterop |
| [`references/templates.md`](references/templates.md) | Nested templates, precedence, merging, conflict resolution |
| [`references/publishing.md`](references/publishing.md) | JVM and KMP publishing, Maven Central, `mavenLocal`, signing |
| [`references/github-actions.md`](references/github-actions.md) | Heapy actions for CI, caching, wrapper upgrades, and library publication |
| [`references/plugins.md`](references/plugins.md) | Authoring `jvm/amper-plugin` modules, `plugin.yaml`, task actions |
| [`references/maven-migration.md`](references/maven-migration.md) | `convert-project`, `mavenPlugins`, migration gaps |
| [`references/gradle-migration.md`](references/gradle-migration.md) | Translating `build.gradle(.kts)`, convention plugins, and source sets by hand |
| [`references/migrating-0.12-to-0.13.md`](references/migrating-0.12-to-0.13.md) | Upgrading to `0.13` and tagged-doc corrections |
| [`references/known-issues.md`](references/known-issues.md) | Tracked defects and workarounds — check before diagnosing odd behavior |
| [`references/codex-sandbox-caches.md`](references/codex-sandbox-caches.md) | Running the toolchain in a Codex `workspace-write` sandbox |

## Project Version Check

Run this once per session, the first time this skill is used in a Kotlin Toolchain repo, before any other work.

1. Read the version the project pins in its wrapper:

   ```shell
   sed -n 's/^kotlin_cli_version=//p' ./kotlin
   ```

   `kotlin.bat` carries the same value as `set kotlin_cli_version=`. A repo without a wrapper has nothing to check —
   skip to `First Moves`.

2. Compare it to `0.13.0`, the version this skill is generated from.

3. If the pin differs, consult that release's tagged docs and the project CLI for version-sensitive behavior.
   Explain an upgrade when relevant; obtain approval unless the user already requested it. Continue compatible
   work while an optional upgrade is undecided.

4. For an authorized upgrade to this snapshot, run `./kotlin update --target-version 0.13.0`. It rewrites `kotlin`
   and `kotlin.bat` and verifies the new distribution. Apply the migration guide, then re-read the wrapper pin.
   Leave the wrapper changes uncommitted unless a commit is part of the user's request.

5. If the user keeps the older version, do not apply the new syntax or defaults to it.

`./kotlin update` without `--target-version` selects the latest release. If the project's version is newer than
`0.13.0`, prefer its tagged docs and what its CLI reports (`./kotlin show ...`, `--help`) over this snapshot.

A globally installed `kotlin` is not a shortcut past this. It walks up from the current directory looking
for a project with its own wrapper, and runs that wrapper's version instead of its own.

## First Moves

When working in a repo:

1. Inspect `module.yaml`, `project.yaml`, `*.module-template.yaml`, `libs.versions.toml`, `plugin.yaml`, and wrapper
   scripts before suggesting edits.
2. Prefer project-local `./kotlin` over a global `kotlin` command when the wrapper exists.
3. Use `./kotlin show modules|settings|dependencies|tasks|checks|commands` to understand the effective model.
   `show settings -m <module>` is the way to read effective template-merged config.
4. Keep YAML declarative. Do not invent loops, conditionals, Gradle task wiring, or Maven lifecycle behavior.
5. Write new paths with the `//` project-root notation, except in `project.yaml`'s `modules:` list.

Useful CLI commands:

- `./kotlin init`
- `./kotlin build`
- `./kotlin run -m <module>`
- `./kotlin test`
- `./kotlin package`
- `./kotlin publish <repoId|mavenCentral>` (`-m <module>` selects modules; add `--transitive` for their local deps)
- `./kotlin check [names] [--skip tests] [-m module]`
- `./kotlin do <command> [-m module]`
- `./kotlin task :<module>:<task>@<pluginId>` for debugging plugin tasks
- `./kotlin show settings -m <module>`
- `./kotlin clean`
- `./kotlin update [--target-version <version> | --dev]` (`--create` installs missing wrappers)
- `./kotlin generate-completion <bash|zsh|fish>`
- `./kotlin tool convert-project`, `./kotlin tool generate-keystore`, `./kotlin tool xcode-integration`

Environment variables: `KOTLIN_CLI_BOOTSTRAP_CACHE_DIR` (wrapper/CLI distribution), `KOTLIN_SHARED_CACHE_DIR`
(dependencies, JDKs, tools — also `--shared-cache-dir`), `KOTLIN_CLI_NO_WELCOME_BANNER`, `KOTLIN_CLI_JAVA_OPTIONS`,
`KOTLIN_CLI_JAVA_HOME`, `KOTLIN_CLI_DOWNLOAD_ROOT`, and `KOTLIN_TOOLCHAIN_BUILD_DIR` (or `--build-dir`; renamed
from `AMPER_BUILD_DIR` in `0.13`). The CLI is currently JVM-based, but this is an implementation detail. See
[`references/cli.md`](references/cli.md).

## Project Model

A project is rooted at `project.yaml`. A module is a directory containing `module.yaml`. A single-module project does
not need `project.yaml`; a root `module.yaml` is included implicitly in a multi-module project.

Each module produces exactly one product. Sources and resources belong to one module; modules share code by depending
on each other.

```yaml
# project.yaml
modules:
  - app
  - libs/lib1
  - plugins/*

plugins:
  - //plugins/build-config
```

`modules:` entries are path globs relative to the project root, written without `//`. `plugins:` entries use `//`, and
every plugin listed there must also appear in `modules:`.

Path notation:

- `/` is the separator on all platforms; never `\`.
- `//<path>` resolves from the project root. This is the preferred form for module dependencies, templates, plugin
  refs, and any other `Path` value.
- Plain relative paths (`./foo.txt`, `../bar`, `resources/pic.jpg`) resolve against the directory of the YAML file that
  contains them. For module dependencies they still work but may be deprecated later.
- A bare value like `my-lib` in `dependencies:` is an external dependency, not a local module. A local relative path
  must start with `.`.

Common `module.yaml` keys: `product`, `dependencies`/`test-dependencies`, `settings`/`test-settings`, `repositories`,
`apply`, `aliases`, `layout`, `description`, `plugins`, `mavenPlugins`, and `pluginInfo` for `jvm/amper-plugin`
modules.

The `default` layout uses `src`, `test`, `resources`, and `testResources`; its name changed from `amper` in `0.13`.
`maven-like` preserves `src/main/kotlin`-style trees and is only supported for `jvm/app` and `jvm/lib`.

## Product Types

Use the short form when no platform list is needed:

```yaml
product: jvm/app
```

Use the full form for explicit platforms:

```yaml
product:
  type: kmp/lib
  platforms: [jvm, android, iosArm64, iosSimulatorArm64]
```

| Type | Platforms | Notes |
|---|---|---|
| `jvm/app` | `jvm` | `package` builds an executable JAR |
| `jvm/lib` | `jvm` | publishable |
| `kmp/lib` | explicit leaf list | publishable |
| `android/app` | `android` | `build` → APK, `package` → AAB with R8 and signing |
| `ios/app` | `iosArm64`, `iosSimulatorArm64` | needs `module.xcodeproj`; `iosX64` no longer accepted |
| `js/app` | `js` | incomplete preview, CLI cannot run it |
| `wasm-js/app` | `wasmJs` | `build` packages a web app; `run` serves it in a browser |
| `wasm-wasi/app` | `wasmWasi` | incomplete preview, run it with an external WASI runtime |
| `linux/app` | `linuxX64`, `linuxArm64` | `.kexe` output, no `package` |
| `macos/app` | `macosArm64` | `macosX64` deprecated and dropped from defaults |
| `windows/app` | `mingwX64` | `.exe` output, no `package` |
| `jvm/amper-plugin` | `jvm` | local build plugin module |

`product.platforms` takes leaf platform names only, never family names. Per-type detail lives in
[`references/product-types.md`](references/product-types.md).

## Dependencies

```yaml
dependencies:
  - //ui/utils                                # local module
  - io.ktor:ktor-client-core:2.2.0            # external Maven coordinates
  - $libs.ktor.client.cio                     # project catalog
  - $compose.foundation                       # toolchain catalog
  - bom: io.ktor:ktor-bom:2.2.0
  - io.ktor:ktor-serialization-kotlinx-json   # version from the BOM
  - org.postgresql:postgresql:42.3.3: runtime-only
  - io.ktor:ktor-client-core:2.2.0:
      exported: true
      scope: compile-only
```

Full coordinate form is `group:artifact[:version[:classifier]][@packaging]`. Scopes are `all` (default),
`compile-only`, and `runtime-only`. `exported` defaults to `false` — use it only when the dependency's types appear in
the module's public API.

Catalogs: one project `libs.versions.toml` at the project root or under `gradle/`, not both; only `[versions]` and
`[libraries]` are read. A toolchain catalog is named after its toolchain in `settings` and appears once that toolchain
is enabled — `$kotlin`, `$compose`, `$kotlin.serialization.*`, `$kotlin.rpc.*`, and the Ktor entries.

Repositories: Maven Central (`mavenCentral`) and Google (`mavenGoogle`) are on by default. Re-declaring one of those
IDs replaces it — that is how you point at a mirror or add credentials. `resolve: false` disables it instead;
`publish: true` marks a repository as a publish target. `mavenLocal` is a special URL: listed bare it only resolves,
and it needs the object form with `publish: true` to also be a publish target. Details in
[`references/dependencies.md`](references/dependencies.md).

## Settings Defaults

Defaults checked against `DefaultVersions.kt` at the pinned `v0.13.0` tag:

| Setting | Default |
|---|---|
| JDK major version | 25 |
| `settings.kotlin.version` | 2.4.20 |
| `settings.android.compileSdk` | 37 |
| `settings.android.minSdk` | 24 |
| `settings.android.buildToolsVersion` | 37.0.0 |
| `settings.compose.version` | 1.12.1 |
| `settings.compose.experimental.hotReload.version` | 1.2.0 |
| `settings.kotlin.serialization.version` | 1.11.0 |
| `settings.kotlin.ksp.version` | 2.3.12 |
| `settings.kotlin.rpc.version` | 0.10.4 |
| `settings.kotlin.dataframe.version` | 1.0.0-rc01 |
| `settings.jvm.test.junitPlatformVersion` | 6.1.3 |
| `settings.ktor.version` | 3.6.0 |
| `settings.lombok.version` | 1.18.48 |
| `settings.springBoot.version` | 4.1.1 |

Running the toolchain itself needs JDK 17 or newer, and `settings.kotlin.version` must be at least 2.2.20.

Always re-check defaults for a real project with `./kotlin show settings`.

JDK provisioning:

```yaml
settings:
  jvm:
    jdk:
      version: 25
      distributions: [temurin, zulu]
      selectionMode: auto
```

Selection modes are `auto`, `alwaysProvision`, and `javaHome`. `oracleGraalVM` requires an explicit
`acknowledgedLicenses` entry. For the supported distributions, see
[`references/cli.md`](references/cli.md).

`settings.jvm.release` is the minimum JVM release the code must be compatible with — bytecode target plus Java API and
language limits. It defaults from `jdk.version`. Do not repurpose `jdk.version` for it.

## Multiplatform

The hierarchy starts at `common` and includes `jvm`, `android`, `web` (`js`, `wasmJs`), `wasmWasi`, and native families
such as `linux`, `mingw`, `apple`, and `androidNative`. `macosX64`, `watchosArm32`, and `tvosX64` are deprecated.

- Use `src@platform`, `resources@platform`, `test@platform`, `testResources@platform`, `dependencies@platform`, and
  `settings@platform`.
- Common code is visible to more-specific code, not the reverse. `expect` goes in `src`, `actual` in `src@<platform>`.
- Scalars are overridden by more-specific sections; maps and lists are appended.
- `aliases:` defines custom platform groups, e.g. `jvmAndAndroid: [jvm, android]`, usable in source dirs and qualified
  sections.
- C/Objective-C interop is configured by placing `.def` files under `cinterop` or `cinterop@platform`. Headers vendored
  in a sibling `include` directory are picked up automatically.
- `settings.android` is Android toolchain settings; `settings@android` is platform-qualified settings. Different
  things.

More in [`references/multiplatform.md`](references/multiplatform.md).

## Templates

Template files are named `<name>.module-template.yaml` and have module-like structure, but cannot contain `product:`.
Apply them with `apply:`:

```yaml
apply:
  - //common.module-template.yaml
```

Templates may apply other templates. Precedence runs between whole files: `module.yaml` beats every
template it applies, and a template beats the templates it applies, transitively. Two templates that do not apply each
other are siblings — if they set the same scalar to different values, the build fails with a conflict. Resolve it by
setting the value in `module.yaml`, or in a template that applies both. Each template contributes once no matter how
many paths reach it. Details and examples in [`references/templates.md`](references/templates.md).

## Testing

Tests live in `test` and `test@platform`; test-only resources in `testResources` and `testResources@platform`.
`kotlin.test` is preconfigured per platform. Use `test-dependencies:` and `test-settings:`.

`settings.junit` accepts `junit-5` (default), `junit-4`, and `none`, and this also picks the flavor of the Kotlin test
library that is added (`kotlin-test-junit5`, `kotlin-test-junit`, or plain `kotlin-test`). JVM test process settings
live under `settings.jvm.test` or `test-settings.jvm`.

`0.13` runs Wasm-JS tests in provisioned Chromium via Playwright. This does not add a Wasm-WASI test runner.
JUnit tag filters use `--include-tag` / `--exclude-tag`, for example `./kotlin test -m core --include-tag 'fast & !flaky'`.
Non-JVM tests count as untagged, so positive tag filters can skip them. See [CLI](references/cli.md).

`settings.kotlin.explicitApi: strict` enforces library API declarations while ignoring test sources. Native debug
linking can reuse compiler caches through `settings.kotlin.compileIncrementally`; see [settings](references/settings.md).

## Built-In Technologies

Prefer the short settings forms unless customization is needed:

- `settings.compose: enabled` — Compose compiler/runtime, `$compose.*` catalog, and the components-resources
  dependency. `composeResources` generates accessors.
- `settings.kotlin.serialization: json` — compiler plugin, runtime, and the JSON format. Known formats: `json`,
  `json-io`, `json-okio`, `hocon`, `protobuf`, `cbor`, `properties`.
- `settings.kotlin.rpc: enabled` — kotlinx.rpc plugin, runtime, BOM, and `$kotlin.rpc.*`.
- `settings.kotlin.dataframe: enabled` — DataFrame compiler plugin.
- `settings.kotlin.powerAssert: enabled` — richer assertion messages; `functions:` extends beyond `kotlin.assert`.
- `settings.ktor: enabled` — Ktor BOM, a built-in Ktor library catalog, and the `io.ktor.development=true` system
  property on `kotlin run`.
- `settings.springBoot: enabled` — Spring Boot BOM, `all-open` with the `spring` preset, `no-arg` with the `jpa`
  preset, and the required compiler args. It no longer adds starters for you; declare the ones you need.
- `settings.lombok: enabled` — Lombok dependency, Java annotation processor, Kotlin compiler plugin.
- `settings.android.parcelize: enabled` — Parcelize.
- `settings.kotlin.ksp.processors` — KSP2 processors; local processor modules and options are supported.
- `settings.kotlin.compilerPlugins` — escape hatch for third-party compiler plugins.

More in [`references/builtin-tech.md`](references/builtin-tech.md).

## Android Identity And Signing

An `android/app` must explicitly set `settings.android.namespace`; `applicationId` defaults from it. For Android
libraries, an omitted namespace is derived from publication coordinates or a generated module-specific fallback;
set it explicitly when source code imports generated `R` / `BuildConfig` classes.

Other keys: `versionCode`, `versionName`, `compileSdk`, `minSdk`, `targetSdk` (defaults from `compileSdk`),
`buildToolsVersion`, and `abiFilters` (packaged native ABIs; empty means all). `maxSdk` is rejected as deprecated.

`compileSdk` also takes an object form with `apiLevel`, `minorApiLevel`, and `sdkExtension`.

Duplicate Java resources from dependencies are resolved with `settings.android.resourcePackaging`, which has
`excludes`, `merges`, and `pickFirsts` glob lists.

Release signing: `settings.android.signing: enabled` reads `keystore.properties` beside `module.yaml` with
`storeFile`, `storePassword`, `keyAlias`, and `keyPassword`. Override the path with `signing.propertiesFile`. Generate
a keystore with `./kotlin tool generate-keystore`. Never commit the keystore or `keystore.properties`.

## Publishing

Publishing is preview. It covers both JVM and multiplatform libraries, on every Kotlin platform, and
emits Gradle module metadata alongside `pom.xml`. Consumers do not need the Kotlin Toolchain.

Since `0.13`, KMP publications include Compose resources and SwiftPM metadata. Libraries with local Swift packages
can publish only to `mavenLocal`; shared publications must use remote packages.

A regular Maven repository needs a `repositories` entry with `publish: true` plus credentials, and
`settings.publishing` with `enabled`, `group`, and `version`. Maven Central additionally needs `mavenCentral: enabled`,
`signArtifacts: true`, `publishSources: true`, and the POM metadata, with credentials in
`KOTLIN_TOOLCHAIN_MAVEN_CENTRAL_USERNAME`/`_PASSWORD` and `KOTLIN_TOOLCHAIN_SIGNING_KEY`/`_PASSPHRASE`.

`publishingMode` is `manual` by default; `auto` releases without inspection, and released Maven Central artifacts are
permanent. `kotlin publish mavenLocal` installs into the local Maven repository. Details in
[`references/publishing.md`](references/publishing.md).

## SwiftPM

Apple targets can use `swiftPackage: { repository, version, products }` and
`localSwiftPackage: { path, products }`. Qualify dependencies with `@ios` or another Apple family when needed.
Kotlin imports Objective-C-visible APIs through `swiftPMImport.<module>`; pure Swift APIs need an Objective-C wrapper.
See [dependencies](references/dependencies.md) for exact version syntax and publication restrictions.

## GitHub Actions

For GitHub CI, wrapper upgrade PRs, and library publication, use Heapy's `setup-ktc`, `update-ktc`, `ktc-check`,
and `ktc-publish` actions. Read [GitHub Actions](references/github-actions.md) for setup examples, feature-branch
and fork caching, token permissions, and publishing host requirements.

## Plugin Authoring

Plugins are local modules with `product: jvm/amper-plugin`, registered in `project.yaml.plugins` and enabled per module
under `plugins:`. Task actions are top-level public `@TaskAction` functions; `plugin.yaml` registers tasks, generated
outputs, checks, and commands. Plugins cannot be published — see
[`references/known-issues.md`](references/known-issues.md). Full guidance in
[`references/plugins.md`](references/plugins.md).

## Pitfalls

- Alpha means defaults and syntax drift; verify exact behavior against a tag, SHA, or the installed toolchain.
- Do not remove expected `Amper` names from plugin/product/package references. YouTrack is `KTC`, not `AMPER`.
- Write `//` paths for module deps, templates, and plugin refs — but never in `project.yaml`'s `modules:` list.
- Check the wrapper before using version-sensitive features or defaults.
- `product.platforms` requires leaf platform names, not family shortcuts.
- `settings.android` and `settings@android` are different.
- `layout: maven-like` is only for JVM-only modules.
- One module has one product; source folders are not shared across modules.
- Sibling templates that disagree on a scalar are a build error, not a silent win for one of them.
- KSP is KSP2-only, and generated code is platform-specific in KMP.
- `js/app` and `wasm-wasi/app` cannot be run by the CLI; `wasm-js/app` can, via `run`.
- Native, JS, and Wasm product types do not support `package`.
- iOS requires Xcode integration and `module.xcodeproj`; the build phase is now `Build Kotlin`.
- Compose resources publish in `0.13`; expose generated accessors only when they belong in the public API.
- Use `exported` sparingly to avoid leaking implementation dependencies into consumer compile classpaths.
- Maven Central `auto` publishing and released artifacts are permanent decisions.
