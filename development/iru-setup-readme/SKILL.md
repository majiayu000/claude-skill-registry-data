---
name: iru-setup-readme
description: >-
  Create or update the root `README.md` for a repository — a brief description, badges (CI status,
  SonarCloud/SonarQube, npm, Maven Central, Packagist, PyPI, WordPress.org, PHP/Python version, GHCR container
  image, Swift Package Index, crates.io/docs.rs, pkg.go.dev, NuGet, GitHub release, etc.), a project status table
  (language, versions, framework, platforms, license, CI, quality tools, distribution; for a command-line tool also
  the toolchain floor, argument parser, terminal-UI library, release targets and channels), documentation links
  (Antora site, the generated CLI reference page, Maven site report, SonarCloud dashboard, generated API docs such
  as TypeDoc/Compodoc/Storybook/Dokka/DocC/DocFX/rustdoc/pkg.go.dev/phpDocumentor/Sphinx, OpenAPI/Swagger UI,
  CHANGELOG), installation instructions (Maven/Gradle/npm/Composer/uv/pip/SwiftPM/etc. dependency snippets, a
  "run it locally"/container-image/store-listing section for services, web apps, WordPress plugins/themes and
  PrestaShop modules, or — for a command-line tool — only the release channels actually wired: Homebrew tap,
  `cargo install`, `go install`, Scoop/WinGet, `dotnet tool install -g`, or the release archive with
  `SHA256SUMS`/`gh attestation verify`, plus build from source — matched to the project's actual stack and build
  tool — Spring Boot (Java or Kotlin, Maven or Gradle KTS), Quarkus, Laravel, WordPress, PrestaShop, NestJS,
  Next.js, FastAPI, Django, plain Python packages, command-line tools in Rust/Go/Swift/.NET, plain Rust crates and
  Go modules, and the earlier library/app stacks), and a short "how it works" section with a runnable example (for
  a command-line tool: a human example, a `--json` example piped to `jq`, the exit-code table, and a note on using
  it from scripts and AI agents). Invoke as `/iru-setup-readme`, optionally with `args` (one key/value pair per line, all
  optional) — `sonar` set to `none` suppresses Sonar badges and dashboard links even when a `sonar {}` block or
  `sonar-project.properties` exists, `ci` set to `no` omits CI status badges, `pages` set to `no` avoids linking a
  github.io documentation site (or Next.js static export) that won't be published, and `on-existing`
  (`ask`/`keep`/`update`/`replace`, scripted runs, default `ask`) pre-answers the existing-README question — so an
  orchestrator's resolved choices produce a README matching them. Explores the repository's actual state
  (`pom.xml`/`build.gradle*`/`gradle.properties`/`composer.json`/`package.json`/`pyproject.toml`/`uv.lock`/
  `Package.swift`/`Cargo.toml`/`go.mod`/`Directory.Build.props`/WordPress plugin
  or theme headers/PrestaShop module class/Android Gradle modules/Xcode or Tuist project files/etc., git remote,
  GitHub Actions workflows, Sonar config, Antora docs, `CHANGELOG.md`, `LICENSE`, source code) to fill in every
  section — a section whose source material doesn't exist yet (e.g. a brand-new, mostly empty repository) is
  omitted rather than filled with placeholders or invented content; a WordPress `readme.txt` is a separate file
  this skill never replaces. Announces whether it is creating the README from scratch or updating an existing one;
  if `README.md` already exists (including a generator's stock README from `laravel new`, `create-next-app`, `nest
  new`, `quarkus create` or `uv init`), warns the user and shows the proposed content as a diff before writing anything,
  asking whether to Update it (merged draft, hand-written sections kept), Keep it as is, or Replace it
  (regenerated, hand-written sections dropped). Use whenever a repository needs a README bootstrapped or refreshed
  from what's actually there, instead of hand-writing it.
model: sonnet
---

# Setup Readme

Create or refresh a repository's root `README.md` by exploring what actually exists in the repository —
build files, CI workflows, quality-tool config, documentation, license, and source code — and composing only the
sections that real material supports. Never invent version numbers, badge URLs, dashboard links, or example code
that don't correspond to something actually present.

## Step 0 — Resolve inputs

This skill takes optional `args` (`key: value` lines, one per line), passed by this catalog's setup orchestrators
with the values they resolved. Every key is optional; any other key (e.g. `mode`, `visibility`) is ignored:

- **`sonar: <cloud|self-hosted|none>`** — only `none` changes behaviour: Step 3 then skips every
  SonarCloud/SonarQube badge and Step 5 the dashboard link, even if Sonar configuration is present on disk (a
  `mode: existing` repository may carry a `sonar {}` block the user has just chosen not to wire up — without this
  line, a README otherwise gains a full set of SonarCloud badges for a project the run had explicitly declined).
- **`ci: <yes|no>`** — only `no` changes behaviour: Step 3 skips every CI status badge and Step 4 the CI row, even
  if stale `.github/workflows/*.yml` files exist on disk (the run chose no workflows, so a badge would point at a
  pipeline that isn't maintained — or, on a fresh repository, doesn't exist). `ci: no` also implies `pages: no`.
- **`pages: <yes|no>`** — only `no` changes behaviour: Step 5 never links a `https://<owner>.github.io/<repo>` URL
  (Antora site, Maven site report, TypeDoc/Compodoc/Storybook/Dokka/DocC/phpDocumentor/Sphinx, or a Next.js/React/Angular
  static export deployed as the site itself), because nothing publishes there — CI only uploads the built docs (or
  `out/`) as a workflow artifact. Point readers at the docs sources instead (`docs/` in the repository, built
  locally with `cd docs && npx antora antora-playbook.yml`) when an Antora site exists, and at the local
  build/serve commands for a static export.
- **`on-existing: <ask|keep|update|replace>`** — default `ask`. How Step 9 treats an existing `README.md`: `keep`/
  `update`/`replace` apply that option without asking (Step 1 still prints its warning). `mode: existing` alone
  does **not** mean "update silently" — Step 9 still asks unless `on-existing` says otherwise.

Any other value, or no `args` at all, means "detect from the repository" as Steps 3–5 describe. Record in Step 11
every badge/link suppressed because of one of these lines.

## Step 1 — Check whether `README.md` already exists

Look at the repository root for `README.md`.

- **Not found**: tell the user "Creating `README.md` **from scratch**" and continue to Step 2; the final write in
  Step 10 happens without needing approval first (there is nothing to lose), though the composed content is still
  worth a quick summary in Step 11.
- **Found**: tell the user "**Updating an existing `README.md`**" and warn up front that a `README.md` already
  exists and this skill will propose changes for them to review rather than overwriting it silently (Step 9's
  Update / Keep / Replace choice). If Step 0's `on-existing` is `keep`, stop here — leave the file untouched and
  report that in Step 11 without composing a draft. Otherwise read it now — its content matters later: Step 9 shows a
  diff against it, and any hand-written section that doesn't map onto Steps 3–8 (e.g. a "Contributing" or
  "Acknowledgements" section unrelated to this skill's scope) should be preserved in the proposed version rather
  than dropped. Continue to Step 2.
  - **Generator boilerplate**: if the existing file is the stock README a project generator wrote — Laravel's own
    (the `laravel.com` logo lockup, `laravel/framework` badges, "About Laravel"), `create-next-app`'s ("This is a
    Next.js project bootstrapped with…"), `nest new`'s (the NestJS logo, "A progressive Node.js framework…"),
    `quarkus create`'s ("This project uses Quarkus, the Supersonic Subatomic Java Framework"), `uv init`'s empty
    `README.md`, or the like — say
    so: it describes the generator or framework, not this project, and its badges point at someone else's
    repository. Nothing in it counts as a hand-written section to preserve, and Step 9 recommends **Replace**
    instead of **Update**.
  - **Not `readme.txt`**: a WordPress plugin/theme's `readme.txt` (the WordPress.org directory listing, with
    `=== Name ===`, `Stable tag:`, `== Changelog ==`) is a different file with its own format and release
    rules — this skill reads it for facts (Step 2) but never writes, replaces, or "converts" it.

## Step 2 — Gather project identity

- **Repository name and host**: `git remote get-url origin`; if it's GitHub, extract `<owner>/<repo>` — used for
  badge URLs, GitHub Pages links, and compare links throughout. If there's no remote, or it isn't GitHub, skip
  every GitHub-specific link/badge later and note this in Step 11's report rather than guessing a URL scheme.
- **Description/tagline**: prefer, in order, `project.description` in a `springboot-stack.yml`/`quarkus-stack.yml`
  manifest, a `<description>` in `pom.xml`, a `description` in the root `build.gradle.kts`, a `"description"` in
  `package.json` or `composer.json`, `[project].description` in `pyproject.toml`, the `Description:` header of a WordPress main plugin file or theme
  `style.css`, a PrestaShop module class's `$this->description`, or an existing Antora
  `docs/modules/ROOT/pages/index.adoc` overview paragraph. Skip a generator's untouched default — `composer.json`
  still reading "The skeleton application for the Laravel framework." (with `"name": "laravel/laravel"`), Spring
  Initializr's "Demo project for Spring Boot", `uv init`'s "Add your description here", and the like describe the template, not this project. If
  none remain, ask the user for a one-sentence description rather than inventing one — this is the first thing a
  reader sees.
- **License**: look for `LICENSE`/`LICENSE.txt`/`LICENSE.md` at the root. Identify common licenses by their actual
  text (Apache-2.0, MIT, BSD, GPL family) rather than assuming; if the file exists but doesn't match a license you
  can confidently name, still link to it but describe it generically ("see `LICENSE`") rather than guessing a name.
  If no license file exists, omit the License section entirely — don't claim a license the repository doesn't
  declare. A license the project declares in its own metadata — a WordPress `License:` header, `composer.json`/
  `package.json` `"license"` SPDX id, `pyproject.toml` `[project].license` (an SPDX expression, or the legacy
  `{ text = … }`/`{ file = … }` table) — may still fill Step 4's License row (say "declared in <file>; no `LICENSE`
  file") and be flagged in Step 11, but there is no License section linking a file that doesn't exist.
- **Primary language, framework, and build tool**: reuse `iru-explore`'s `- Project type:` line rather than
  re-deriving it — `iru-explore` owns the canonical manifest → project-type table (Vite+React, Angular CLI, Hilla,
  React Native (Expo or bare CLI/Metro), Ionic/Capacitor, Kotlin Multiplatform app, Android library/app,
  SwiftPM/XcodeGen/Tuist, macOS desktop app (SwiftUI/AppKit), Windows desktop app (WPF/WinUI 3/Windows Forms),
  command-line tool (`cli-tool (rust|go|swift|dotnet)`), plain Rust crate/Go module, plain TypeScript/npm library,
  and so on), and duplicating it here would drift the first time it gains a signal:
  - If an `iru-explore` report with a `- Project type:` line is already available earlier in this conversation,
    use it — just confirm the manifest(s) it names are still present.
  - Otherwise invoke `Skill({skill: "iru-explore"})` with no ticket argument (a codebase-only exploration) and read
    the `- Project type:` line from its `## Tech stack` report block, along with the build tool and framework it
    names.
  - Only if `iru-explore` isn't installed in this repository, fall back to a minimal one-manifest check — `pom.xml`
    → Java/Maven, `build.gradle*` → Gradle (Android when a module applies `com.android.library`/
    `com.android.application`), `package.json` → npm/TypeScript, `composer.json` → PHP, `pyproject.toml` →
    Python (FastAPI when `fastapi` is a dependency, Django when `manage.py` exists), `Package.swift`/
    `*.xcodeproj`/`project.yml`/`Project.swift` → Swift/Apple (a command-line tool when an `.executableTarget`
    depends on `ArgumentParser`), `*.slnx`/`*.sln`/`*.csproj` → .NET (Windows desktop when a `WinExe` project sets
    `UseWPF`/`UseWinUI`/`UseWindowsForms`; a command-line tool when an `Exe` project references
    `System.CommandLine` or sets `PackAsTool`), `Cargo.toml` → Rust (a command-line tool when it declares a
    `[[bin]]`/`src/main.rs` and depends on `clap`), `go.mod` → Go (a command-line tool when `cmd/<bin>/main.go`
    exists and `github.com/spf13/cobra` is required) — and say in Step 11 that the framework flavor wasn't
    detected.
  - The project types this skill tailors sections for beyond plain libraries/apps (Steps 3–7): `java-springboot`/
    `kotlin-springboot` (+ `-hilla`), `java-quarkus`/`kotlin-quarkus`, `php-laravel`, `php-wordpress-plugin`,
    `php-wordpress-theme`, `php-prestashop-module`, `php-library`, `nestjs`, `nextjs`, `python-fastapi`,
    `python-django`, `python-library`, `cli-tool (rust|go|swift|dotnet)`, and plain `rust`/`go`. For a
    `cli-tool`, also note the executable name (`<bin>`), the argument parser (clap, Cobra, swift-argument-parser,
    System.CommandLine — from the manifest's dependencies) and the terminal-UI library when one is a dependency
    (Ratatui, Bubble Tea, Terminal.Gui) — the status table, Installation and usage sections use all three. A plain
    `rust`/`go` project (a library or service, no CLI contract) gets only the identity, badges, docs links and
    dependency snippet below (`cargo add <crate>` / `go get <module>`), never the CLI usage section. For the Python
    types, also note the package manager (uv when `uv.lock`
    exists; Poetry/PDM/pipenv only when their lockfile is what's committed) — every command later uses it. For the JVM services, also
    note the language (Kotlin when `src/main/kotlin` holds the sources / the Kotlin plugin is applied) and the build
    tool (Maven, or Gradle with the Kotlin DSL) — every command later in this skill depends on both.
  - A repository can have more than one manifest (e.g. a Maven library with an Antora docs site under `docs` that
    has its own `package.json` for the doc toolchain only, or a Hilla app that is both Java and TypeScript — treat
    the latter as both a Java backend and a frontend for badges/snippets/status-table purposes) — identify the
    build tool for the library/application itself, not incidental tooling; `iru-explore` reports `multiple` when
    it genuinely can't pick one.
- **Current version(s) and package/artifact identity**: read the identity from the source that actually owns it
  for the detected stack, not always `pom.xml`/`package.json`:
  - Maven: the `<version>` in `pom.xml` (immediately under the project's own `artifactId`, not a
    dependency/plugin), plus `groupId`/`artifactId`.
  - Gradle/Android library: `group` and `libraryVersion` (or equivalent) in `lib/build.gradle.kts`, falling back
    to a version property in `gradle.properties` when the build script references one.
  - Gradle JVM service (Kotlin Spring Boot / Quarkus on Gradle KTS): `group`/`version` in `gradle.properties`
    (where the Spring Boot scaffold keeps them), else `group =`/`version =` in the root `build.gradle.kts` (where
    the Quarkus generator writes them); the
    artifact name is `rootProject.name` in `settings.gradle.kts`. Quarkus on Maven: `pom.xml` as above.
  - npm/Vite/Angular/Expo/Ionic/TypeScript/NestJS/Next.js: the `"name"`/`"version"` in `package.json`. A React
    Native app's store-facing version lives elsewhere — `app.json`'s `expo.version` (Expo) or
    `android/app/build.gradle` `versionName` / the iOS `MARKETING_VERSION` (Metro) — show that one in the status
    table when it differs from `package.json`'s.
  - Kotlin Multiplatform app (`kmp-app`): `VERSION_NAME` in the root `gradle.properties` (falling back to the
    Android app module's `versionName`), the app name from `rootProject.name` in `settings.gradle.kts`, and the
    Kotlin / Compose Multiplatform / AGP versions from `gradle/libs.versions.toml`.
  - Laravel: `'version' => env('APP_VERSION', '<x.y.z[-dev]>')` in `config/app.php` (never a `composer.json`
    `"version"` field — the app has none); the PHP floor from `composer.json` `require.php` (or
    `config.platform.php`) and the Laravel version from `composer.lock`'s `laravel/framework` entry.
  - WordPress plugin: the main plugin file (the PHP file at the plugin root carrying a `Plugin Name:` header) —
    `Version:`, `Requires at least:`, `Requires PHP:`, `Text Domain:`; the slug is the plugin directory / main
    file basename (or `Text Domain` when they differ — say which in Step 11). `readme.txt` adds `Tested up to:` and
    `Stable tag:` (the latest *release*; it never carries a `-dev` version). WordPress theme: the same headers
    in `style.css` (`Theme Name:`, `Version:`, `Requires at least:`, `Requires PHP:`), slug = theme directory.
  - PrestaShop module: the main module class (`<module>.php` extending `Module`) — `$this->name` (the technical
    name/zip name), `$this->version`, `$this->displayName`, and `$this->ps_versions_compliancy` (`min`/`max`); a
    tracked `config.xml` `<version>` must agree with it.
  - Python (`python-fastapi`/`python-django`/`python-library`): `[project].name` and `[project].version` in
    `pyproject.toml` — the single version source (pre-releases use PEP 440's `.dev0` suffix, e.g. `0.2.0.dev0`;
    runtime code reads it via `importlib.metadata.version()`, so never take it from `__version__` or
    `docs/antora.yml`, which only mirror it). A `dynamic = ["version"]` project takes it from the backend's
    configured source (e.g. `[tool.hatch.version] path`) or git tags — say which in Step 11. The Python floor is
    `requires-python` (e.g. `>=3.12`), the CI/runtime version `.python-version` or the workflows' `python-version`
    (e.g. `3.13`), and the framework version from `uv.lock`'s `fastapi`/`django` (`djangorestframework`,
    `django-ninja`) `[[package]]` entry (or `poetry.lock`/`pdm.lock`), never from the dependency range.
  - Plain Composer package (`php-library`): `"name"` from `composer.json`; the version comes from git tags (Composer
    packages carry no in-tree version, like SwiftPM).
  - Swift: the package name from `Package.swift`, with the version taken from git tags (SwiftPM has no in-file
    version field) — `git tag --sort=-v:refname | head -1`.
  - Xcode app: `MARKETING_VERSION` from the project's build settings (`project.pbxproj`, `project.yml`, or
    `Project.swift`, depending on which of Xcode/XcodeGen/Tuist generates the project). For a macOS desktop app
    (`macos-app`) also the deployment target (`MACOSX_DEPLOYMENT_TARGET`/`deploymentTarget.macOS`), the UI framework
    (SwiftUI/AppKit) and whether the App Sandbox entitlement is on — status-table rows.
  - Windows desktop app (`windows-app`): `<Version>` in `Directory.Build.props` (else the app project's own;
    pre-releases use `-dev`), the app name from the `*.slnx`/`*.sln`, the target framework (`net10.0-windows…`) and
    UI stack (WPF/WinUI 3/Windows Forms) from the app `*.csproj`, the Windows App SDK version from
    `Directory.Packages.props` (WinUI), and the MSIX identity (`Identity Name`/`Publisher`) from
    `Package.appxmanifest` or `packaging/AppxManifest.xml` when present.
  - Rust (`cli-tool (rust)`, `rust`): `[package] name` and `version` in the root `Cargo.toml` (the gitflow
    in-tree version ends in `-dev`, e.g. `0.1.0-dev`; never the `xtask` member's `0.0.0`), the `[[bin]] name` (the
    executable — it may differ from the package name), `rust-version` (the MSRV — the toolchain floor), `license`,
    and `publish = false` (then the crate is never on crates.io, whatever Step 3 finds).
  - Go (`cli-tool (go)`, `go`): the module path from the `module` line of `go.mod` (the executable is the
    `cmd/<bin>/` directory name), the Go floor from its `go` line (and the CI toolchain from its `toolchain` line),
    and the version from `var Version = "<x.y.z[-dev]>"` in `internal/version/version.go` (release builds override it
    through GoReleaser ldflags; a plain `go` module without that file takes its version from git tags only).
  - Swift command-line tool (`cli-tool (swift)`): the executable product name in `Package.swift`
    (`.executable(name: "<bin>", …)`), `public let toolVersion = "<x.y.z[-dev]>"` in
    `Sources/<Bin>Kit/Version.swift` (the only version literal — not git tags as for a SwiftPM library), and the
    `swift-tools-version`/`platforms` floor from `Package.swift`.
  - .NET command-line tool (`cli-tool (dotnet)`): `<Version>` in `Directory.Build.props` (`-dev` suffix on
    `develop`), and from the `Exe` project `src/<ToolName>/<ToolName>.csproj` the `ToolCommandName` (the
    executable), `PackageId` (the NuGet .NET tool id) and the target framework; the SDK floor from `global.json`.
  - Also find the latest released version for any stack: `git tag --sort=-v:refname | head -1` (or `gh release
    list --limit 1` if on GitHub with `gh` available). If the current version has no `-SNAPSHOT`/prerelease
    suffix (`-SNAPSHOT`, `-dev`, `-dev.N`, `-rc.N`, Python's `.devN`/`rcN`, …) and matches the latest tag, there's only one version to show,
    not a "current dev / latest release" pair. Strip a leading `v` from tags when comparing.

## Step 3 — Gather badge sources

Only include a badge when its underlying resource actually exists — don't fabricate a badge for a CI workflow or
SonarCloud project that isn't configured yet.

- **CI status** (skip entirely when Step 0 resolved `ci: no`): list `.github/workflows/*.yml`. For each workflow that looks like a build/test pipeline (not,
  say, a stale/dependabot-only workflow), add a status badge:
  `https://github.com/<owner>/<repo>/actions/workflows/<file>/badge.svg`, linking to
  `https://github.com/<owner>/<repo>/actions/workflows/<file>`.
- **SonarCloud/SonarQube** (skip entirely when Step 0 resolved `sonar: none`): check `sonar-project.properties` or `sonar.*` properties in `pom.xml`/`build.gradle*`
  (or an equivalent `sonar-project.properties` used by a non-Java stack) for `sonar.projectKey` (and
  `sonar.organization` if using SonarCloud) — this applies to any stack, not just Java/Maven. The command-line tool
  workflows keep no Sonar file: they pass `-Dsonar.projectKey=…`/`-Dsonar.organization=…`/`-Dsonar.host.url=…` to
  the scanner step in `.github/workflows/build.yml` — read them from there. If found and hosted
  on SonarCloud, add the full metric set the reference Android READMEs use — Quality Gate Status,
  Maintainability Rating, Reliability Rating, Security Rating, Bugs, Code Smells, Coverage, Duplicated Lines (%),
  Lines of Code, Technical Debt, Vulnerabilities — each of the form
  `https://sonarcloud.io/api/project_badges/measure?project=<project-key>&metric=<metric>` (metric keys:
  `alert_status`, `sqale_rating`, `reliability_rating`, `security_rating`, `bugs`, `code_smells`, `coverage`,
  `duplicated_lines_density`, `ncloc`, `sqale_index`, `vulnerabilities`), each linking to
  `https://sonarcloud.io/summary/new_code?id=<project-key>`. If Sonar config exists but points at a self-hosted
  SonarQube instance instead, link the dashboard but skip the SonarCloud-specific badge images (they're a
  SonarCloud-only feature) and note this in Step 11.
- **Package registry badges**, only if the project is actually published there — never fabricate a badge for a
  registry the project has never published to:
  - **npm**: `img.shields.io/npm/v/<name>` (version) and `img.shields.io/npm/dm/<name>` (monthly downloads),
    linking to `https://www.npmjs.com/package/<name>`, when `package.json`'s `"name"` is confirmed published
    (e.g. a publish step in a GitHub Actions workflow, or the package is already live on the registry).
  - **Maven Central**: `https://maven-badges.herokuapp.com/maven-central/<group>/<artifact>/badge.svg` (or the
    `img.shields.io/maven-central/v/<group>/<artifact>` equivalent), linking to the Maven Central search page for
    that coordinate, when the `pom.xml` publishing profile actually targets Central (e.g. a
    `central-publishing-maven-plugin`/`nexus-staging-maven-plugin` configuration or a release-publish workflow
    step).
  - **Swift Package Index**: platform and Swift-version shields,
    `https://img.shields.io/endpoint?url=https%3A%2F%2Fswiftpackageindex.com%2Fapi%2Fpackages%2F<owner>%2F<repo>%2Fbadge%3Ftype%3Dplatforms`
    and `…%2Fbadge%3Ftype%3Dswift-versions`, linking to `https://swiftpackageindex.com/<owner>/<repo>`, when the
    package is confirmed listed there (or a `Package.swift` plus an SPI-focused release workflow strongly implies
    it — note the inference in Step 11 if not confirmed live).
  - **Packagist** (`php-library`, or a WordPress plugin/theme whose `composer.json` has `"type":
    "wordpress-plugin"`/`"wordpress-theme"` and is listed there) — only when `curl -sf
    https://repo.packagist.org/p2/<vendor>/<name>.json` succeeds (the package is live): version
    `https://img.shields.io/packagist/v/<vendor>/<name>`, total downloads `https://img.shields.io/packagist/dt/<vendor>/<name>`,
    and PHP requirement `https://img.shields.io/packagist/dependency-v/<vendor>/<name>/php` (the older
    `packagist/php-v/…` path is a redirect to this one), each linking to `https://packagist.org/packages/<vendor>/<name>`.
    Never for a Laravel application (`"type": "project"`), a PrestaShop module, or the untouched `laravel/laravel`
    skeleton name — those aren't Packagist packages.
  - **PyPI** (`python-library` only — never a FastAPI/Django service, which ships as an image) — only when a
    release workflow publishes there (`pypa/gh-action-pypi-publish`, or `uv publish`) **and** `curl -sf
    https://pypi.org/pypi/<name>/json` succeeds (the project is live): version `https://img.shields.io/pypi/v/<name>`,
    supported Pythons `https://img.shields.io/pypi/pyversions/<name>` (from the classifiers), and monthly
    downloads `https://img.shields.io/pypi/dm/<name>`, each linking to `https://pypi.org/project/<name>/`. `<name>`
    is `[project].name` normalized (lowercase, runs of `-_.` → `-`). A library whose wheels are only attached to
    GitHub Releases gets no PyPI badge.
  - **WordPress.org** (`php-wordpress-plugin`/`php-wordpress-theme`) — live badges only when the slug is actually
    published: `curl -sf "https://api.wordpress.org/plugins/info/1.2/?action=plugin_information&request%5Bslug%5D=<slug>"`
    (themes: `…/themes/info/1.2/?action=theme_information&request%5Bslug%5D=<slug>`) succeeds — an unknown slug is
    HTTP 404 with `{"error":"Plugin not found."}`. Keep the brackets URL-encoded (or pass `curl -g`): unescaped
    `[slug]` is a curl glob and silently returns nothing. Then, linking to `https://wordpress.org/plugins/<slug>/` (themes:
    `https://wordpress.org/themes/<slug>/`):
    - plugin: `https://img.shields.io/wordpress/plugin/v/<slug>` (version),
      `…/wordpress/plugin/required-php/<slug>`, `…/wordpress/plugin/wp-version/<slug>` (minimum WordPress),
      `…/wordpress/plugin/tested/<slug>` (tested up to), `…/wordpress/plugin/rating/<slug>`,
      `…/wordpress/plugin/installs/<slug>` (active installs);
    - theme: `https://img.shields.io/wordpress/theme/v/<slug>`, `…/wordpress/theme/required-php/<slug>`,
      `…/wordpress/theme/wp-version/<slug>`, `…/wordpress/theme/rating/<slug>`, `…/wordpress/theme/installs/<slug>`
      (shields.io has no `tested` badge for themes).
    A release workflow that deploys to WordPress.org SVN (`10up/action-wordpress-plugin-deploy`, a
    `themes.svn.wordpress.org` commit) without the slug being live yet — the first review is still pending —
    gets **no** live badges (they'd render "not found"); use the static requirement badges below instead and say
    in Step 11 that the WordPress.org badges can be added after approval.
  - **crates.io + docs.rs** (Rust, `cli-tool (rust)` or `rust`) — only when the crate is published there: a
    `crates-io` job in `.github/workflows/release.yml` (or a `cargo publish` step) and `Cargo.toml` has no
    `publish = false`, **and** `curl -sf -A '<repo>-readme' https://crates.io/api/v1/crates/<crate>` succeeds
    (crates.io rejects requests without a User-Agent): version `https://img.shields.io/crates/v/<crate>` and
    downloads `https://img.shields.io/crates/d/<crate>`, linking to `https://crates.io/crates/<crate>`, plus
    `https://img.shields.io/docsrs/<crate>` linking to `https://docs.rs/<crate>`. A wired channel whose first
    version isn't live yet (the first crates.io publish is manual) gets no badge — say so in Step 11.
  - **pkg.go.dev** (Go, `cli-tool (go)` or `go`) — only for a public module whose path is fetchable
    (`curl -sf https://proxy.golang.org/<module>/@latest` succeeds): `https://pkg.go.dev/badge/<module>.svg`
    linking to `https://pkg.go.dev/<module>`. **Go Report Card** is optional — add
    `https://goreportcard.com/badge/<module>` linking to `https://goreportcard.com/report/<module>` only when the
    user wants it or an existing README already carried it (it is a third-party service that grades on request).
  - **NuGet** (`cli-tool (dotnet)` .NET tool, or a published .NET library) — only when a `nuget` job in
    `release.yml` pushes the package **and** `curl -sf https://api.nuget.org/v3-flatcontainer/<package-id-lowercase>/index.json`
    succeeds: `https://img.shields.io/nuget/v/<package-id>` (add `vpre` for a pre-release-only package) and
    `https://img.shields.io/nuget/dt/<package-id>`, linking to `https://www.nuget.org/packages/<package-id>`.
  - **GitHub release** (any project whose `release.yml` uploads release assets — every `cli-tool` with
    `distribution` ≠ `none`) — only when `gh release list --limit 1` (or `git tag`) shows a release exists:
    `https://img.shields.io/github/v/release/<owner>/<repo>?sort=semver` linking to
    `https://github.com/<owner>/<repo>/releases/latest`. Skip it on a repository with no release yet.
- **Requirement badges** (static, from the files read in Step 2 — use them when no registry badge above already
  shows the same fact):
  - **PHP version** (any PHP project not covered by the Packagist/WordPress.org `required-php` badge):
    `https://img.shields.io/badge/php-<range>-777BB4?logo=php&logoColor=white`, where `<range>` is the floor from
    `composer.json` `require.php` (or the WordPress `Requires PHP:` header) written as `>=8.3` and URL-encoded
    (`%3E%3D8.3`; in shields static badges `-` must be doubled as `--`, `_` as `__`, and a space is `%20`). No link,
    or link to `https://www.php.net/supported-versions.php`.
  - **Python version** (any Python project not covered by the PyPI `pyversions` badge):
    `https://img.shields.io/badge/python-<range>-3776AB?logo=python&logoColor=white`, where `<range>` is
    `requires-python` URL-encoded (`>=3.12` → `%3E%3D3.12`), linking to `https://devguide.python.org/versions/`
    or nothing. Add the framework the same way when pinned in the lock —
    `https://img.shields.io/badge/FastAPI-<x.y.z>-009688?logo=fastapi&logoColor=white` /
    `https://img.shields.io/badge/Django-<x.y>-092E20?logo=django&logoColor=white`.
  - **WordPress requirement** for an unpublished plugin/theme: `https://img.shields.io/badge/WordPress-%3E%3D<min>-21759B?logo=wordpress&logoColor=white`
    from `Requires at least:`.
  - **PrestaShop compatibility** (`php-prestashop-module`): `https://img.shields.io/badge/PrestaShop-<majors>-DF0067`
    where `<majors>` is derived from `ps_versions_compliancy` — e.g. `min` `8.0.0` / `max` `9.99.99` →
    `8.x%20%7C%209.x` ("8.x | 9.x"); never wider than the declared range. PrestaShop Addons has no badge
    service — link the Addons product page only when its URL actually appears in the repository (module class,
    `composer.json` `homepage`/`support`, existing README), never a guessed one.
- **Container image** (services/web apps that publish one): when a workflow pushes to GHCR — `docker/login-action`
  with `registry: ghcr.io` plus `docker/build-push-action`/`docker/metadata-action` `images: ghcr.io/<owner>/<image>`,
  or Quarkus' `-Dquarkus.container-image.registry=ghcr.io` (Jib or Docker builder), or the Python services' root
  `Dockerfile` built and pushed by `release.yml` — add
  `https://img.shields.io/badge/ghcr.io-<image>-2496ED?logo=docker&logoColor=white` linking to
  `https://github.com/<owner>/<repo>/pkgs/container/<image>`. Take `<image>` from the workflow's `images:` value (its
  last path segment), not from the repository name, and lowercase `<owner>` (registry paths are lowercase; the
  workflows compute `${GITHUB_REPOSITORY_OWNER,,}`). Shields.io has no GHCR version service (`/ghcr/…` is a 404),
  so this badge is static — the version lives in the Installation snippet. A Laravel app may push two images
  (`<image>` and `<image>-web`) — one badge each. Images pushed only to a registry configured by variables (e.g. a
  deploy workflow's `${{ vars.IMAGE_REGISTRY }}`) get no badge; mention the deploy workflow in Step 4's
  Distribution row instead.
- If none of the above exist yet, skip the badges section of the README entirely rather than leaving an empty
  heading.

## Step 4 — Build the project status table

Compose a small table from whatever Steps 2–3 actually resolved; omit rows with no data rather than writing "N/A":

| Row | Source                                                                                                                         |
| --- |--------------------------------------------------------------------------------------------------------------------------------|
| Language | Detected primary language + version (e.g. `Java 21`)                                                                           |
| Build tool | Maven / Gradle / npm / SwiftPM / Xcode / etc.                                                                                  |
| Current development version | The unreleased/SNAPSHOT version from the build file, if different from the latest release                                      |
| Latest release | The latest git tag / release version                                                                                           |
| Platform(s) | For Android/Apple/web projects only: Android / iOS / iPadOS / macOS / watchOS / web, as applicable                             |
| Min / target SDK | Android only: `minSdk` and compile/target SDK from the Gradle module, when they differ from the platform row above             |
| Kotlin / AGP | Android/Kotlin-Gradle only: Kotlin version and Android Gradle Plugin version, when pinned explicitly                           |
| Kotlin | Kotlin JVM services (Spring Boot / Quarkus): the Kotlin version from `gradle/libs.versions.toml` or the POM's `kotlin.version`, plus the JDK toolchain |
| PHP | PHP projects only: the floor from `composer.json` `require.php` (or `Requires PHP:`), e.g. `>= 8.3`                            |
| Python | Python projects only: `requires-python` (e.g. `>= 3.12`) plus the version CI runs (`.python-version` / workflow `python-version`, e.g. `3.13`), and the package manager (uv / Poetry / PDM) |
| Toolchain floor | Rust / Go / Swift / .NET command-line tools and plain Rust/Go projects: the MSRV from `Cargo.toml` `rust-version` (e.g. `Rust 1.88+`), the `go` line of `go.mod` (plus its `toolchain` line, e.g. `Go 1.27 (toolchain go1.27.2)`), `swift-tools-version` + the macOS floor from `Package.swift`, or the SDK from `global.json` / the target framework (e.g. `.NET 10`) |
| Argument parser | `cli-tool` only: clap (derive), Cobra, swift-argument-parser, System.CommandLine — with the pinned version from `Cargo.lock`/`go.mod`/`Package.resolved`/`Directory.Packages.props` |
| Terminal UI | `cli-tool` only, when one is a dependency: Ratatui, Bubble Tea, Terminal.Gui (and which command opens it, e.g. `browse`); omitted otherwise |
| Platforms / targets | `cli-tool` only: the targets the release workflow actually builds — Rust target triples (`x86_64-unknown-linux-musl`, `aarch64-apple-darwin`, `x86_64-pc-windows-msvc`, …), GoReleaser's `goos` × `goarch`, Swift's macOS universal + Linux, .NET RIDs (`linux-x64`, `osx-arm64`, `win-x64`, …); with no `release.yml`, the platforms the CI matrix runs on |
| Swift tools / deployment targets | Swift only: the Swift tools version from `Package.swift` and the platform deployment targets it declares          |
| Node engine | npm-based projects only: the `engines.node` range from `package.json`, if one is declared                                     |
| TypeScript | TypeScript projects only: the `typescript` version pinned in `package.json`/`package-lock.json`                               |
| Framework | Where applicable: the pinned framework version (React, Angular, Ionic, Expo SDK or React Native — with the toolchain, `expo` or `metro` —, Kotlin Multiplatform + Compose Multiplatform from `libs.versions.toml`, Next.js, NestJS, Spring Boot from the catalog/parent POM, Quarkus `quarkus.platform.version`, Laravel from `composer.lock`, FastAPI / Django (+ DRF or Django Ninja) from `uv.lock`), or the host compatibility (WordPress `Requires at least` – `Tested up to`; PrestaShop `ps_versions_compliancy` range) |
| License | The license identified in Step 2, if any                                                                                       |
| CI | Which CI system and what it runs (e.g. "GitHub Actions for release and `develop` branch builds"); omitted when Step 0 resolved `ci: no` |
| Quality | Which tools actually run — only list ones with real config found (SonarCloud, JaCoCo, Kover, Checkstyle, SpotBugs, PMD, detekt, ktlint, ESLint, oxlint, Prettier, PHPStan/Larastan, Pint, PHPCS/WPCS, PHP-CS-Fixer, Pest/PHPUnit, Ruff, mypy, pytest + coverage.py, pip-audit, SwiftLint, swift-format, Clippy, rustfmt, cargo-deny, cargo-llvm-cov, golangci-lint, govulncheck, StyleCop/.NET analyzers, coverlet, etc.) |
| Distribution | Services/apps/plugins (and published Python libraries) only, from the release workflow actually present: container image on GHCR, PyPI, sdist/wheel attached to GitHub Releases (`uv build`), static export on GitHub Pages, WordPress.org directory (SVN deploy), installable zip attached to GitHub Releases (WordPress, PrestaShop), deploy workflow to an environment; for a `cli-tool`, the release archives (`<bin>-<version>-<target>` + `SHA256SUMS` + build-provenance attestations) and each channel actually wired (crates.io, Homebrew tap, Scoop, WinGet, NuGet .NET tool); omitted when nothing is published |

Omit every row in this extended set (platforms through framework, and Distribution) that doesn't apply to the
detected stack — a plain Java/Maven library still shows only the original rows.

## Step 5 — Gather documentation links

Include a link only when the thing it points to actually exists in the repository (or is confirmed published):

Under Step 0's `pages: no` (or `ci: no`), never emit a `https://<owner>.github.io/<repo>…` link anywhere in this
step — those URLs won't exist. Link the Antora sources and the local build command instead, as Step 0 describes,
and skip the published API-docs links below.

- **Antora documentation site**: if `docs/antora.yml` and `docs/antora-playbook.yml` exist, link to the published
  site. If a GitHub Pages workflow step publishes it (grep workflows for `gh-pages`/`ghaction-github-pages`), the
  URL is normally `https://<owner>.github.io/<repo>`; if you can't confirm it's actually published, still include
  the link but note in Step 11 that it's inferred from convention, not confirmed live.
- **CLI reference** (`cli-tool`): when `docs/modules/ROOT/pages/cli-reference.adoc` exists (generated from the
  command tree by `cargo xtask docs` / `go run ./tools/gendocs` / `gen-docs`; a Swift tool's page only
  `include::`s the generated `docs/modules/ROOT/partials/cli-reference.adoc`), link the published page —
  `https://<owner>.github.io/<repo>/<name>/<version>/cli-reference.html`, with `<name>`/`<version>` from
  `docs/antora.yml` — or, under `pages: no` or while `docs/antora.yml` doesn't exist yet, the source file in the
  repository (the partial for Swift, since GitHub doesn't resolve Antora includes). Never link it when the file doesn't exist (no Antora module yet).
- **Maven/Gradle site report**: if the CI workflow merges a Maven `site` (or Gradle equivalent) report into the
  published docs (e.g. a `mvn-site` subpath alongside the Antora output, matching this repository's own
  `develop`/`main` workflow pattern), link to it at that subpath.
- **Generated API docs published to GitHub Pages**: grep `.github/workflows/*.yml` for the publish step of each
  tool below, and link only the ones actually wired into a workflow — never assume one just because the stack
  matches:
  - **TypeDoc** (TypeScript libraries): a `typedoc` invocation feeding a Pages publish step, normally landing at
    `https://<owner>.github.io/<repo>/api`.
  - **Compodoc** (Angular): a `compodoc`/`@compodoc/compodoc` invocation, normally landing at
    `https://<owner>.github.io/<repo>/api`.
  - **Storybook** (React/Angular component libraries): a `build-storybook` (or `storybook build`) step publishing
    the static build, normally landing at `https://<owner>.github.io/<repo>/storybook` or
    `https://<owner>.github.io/<repo>/api/storybook`, depending on where the workflow places it.
  - **Dokka** (Android/Kotlin/Kotlin Multiplatform): a `dokkaHtml`/`dokkaGenerate` Gradle task feeding a Pages
    publish step, normally landing at `https://<owner>.github.io/<repo>/api` (for a KMP app, the `shared`
    module's multiplatform API). Kotlin Spring Boot / Quarkus services run
    `dokkaGeneratePublicationHtml` (Gradle) or `dokka-maven-plugin` (`mvn dokka:dokka`) and merge the result into
    the Antora output — the Spring Boot workflows put it under `/api/kdoc/` (root-aggregated, or one
    `/api/kdoc/<module-path>/` per module when the root doesn't aggregate); read the workflow's copy step.
  - **DocC** (Swift/macOS apps): an `xcodebuild docbuild`/`swift package generate-documentation` step whose
    static-hosting output the workflow copies under the Antora site's `api/`, normally
    `https://<owner>.github.io/<repo>/api/documentation/<module>/` — read the workflow's copy step.
  - **DocFX** (.NET/Windows desktop apps): a `docfx docfx.json` step whose `_site` the workflow copies under the
    Antora site's `api/`, normally `https://<owner>.github.io/<repo>/api` — only when `docfx.json` exists.
  - **rustdoc** (Rust): docs.rs (`https://docs.rs/<crate>`) when Step 3 added the docs.rs badge; otherwise a
    `cargo doc --no-deps -p <crate>` step whose `target/doc` the workflow copies under the Antora site's `api/`
    (with an `index.html` redirect to `<crate_name>/`), normally `https://<owner>.github.io/<repo>/api/`.
  - **Go doc** (Go): `https://pkg.go.dev/<module>` for a public module (Step 3's check; `internal/` packages are
    listed there too); the catalog's build workflow also publishes a plain-text `go doc -all` dump at
    `https://<owner>.github.io/<repo>/api/go-doc.txt` — link it only when the workflow writes `build/api/go-doc.txt`.
  - **DocC for a Swift command-line tool**: the `<Bin>Kit` library's archive, generated with
    `--hosting-base-path <repo>/api`, normally at `https://<owner>.github.io/<repo>/api/documentation/<bin>kit/`
    (lowercased target name) — read the workflow's `generate-documentation` step.
  - **phpDocumentor** (PHP): a `phpdoc run --config phpdoc.dist.xml` step merged into the Pages site, normally at
    `https://<owner>.github.io/<repo>/api` — only when `phpdoc.dist.xml` exists.
  - **Sphinx** (Python): a `sphinx-build … docs/api build/api-docs` step (sources `docs/api/conf.py` +
    `index.rst`, next to the Antora `docs/antora.yml`) whose output the workflow copies under the Antora site's
    `api/`, normally `https://<owner>.github.io/<repo>/api` — only when `docs/api/conf.py` exists.
  - **OpenAPI schema** (FastAPI/Django services): a FastAPI `scripts/export_openapi.py` writing
    `build/api-docs/openapi.json`, or Django `manage.py spectacular --file build/api-docs/openapi.yaml` (DRF +
    drf-spectacular), merged into the same `api/` folder — link the published file. The running service's own
    interactive docs (Swagger UI/ReDoc) belong in Step 6's Getting Started, not here as a github.io link.
  - **Generated REST/gRPC/AsyncAPI docs** (Spring Boot services): the `generated-docs` directories the build
    workflow merges under `/api/` — link the index the workflow actually produces, if any.
  - **DocC** (Swift): a `docc`/`xcodebuild docbuild` step (often via `docc-render`/`Swift-DocC-Plugin`) feeding a
    Pages publish step, normally landing at `https://<owner>.github.io/<repo>/api`.
  - Use the subpath the workflow actually publishes to rather than assuming `/api` when the workflow config makes
    a different path clear (e.g. `/storybook` vs. `/api/storybook`).
- **Static export site** (Next.js `output: 'export'`, React/Angular SPAs): when `release.yml` deploys the built
  app (`out/`, `dist/`) with `actions/deploy-pages`, the app itself lives at `https://<owner>.github.io/<repo>/`
  (its `basePath` comes from `PAGES_BASE_PATH` in the workflow) — list it as "Live site", not as documentation.
  When the build workflow *also* deploys the Antora docs to Pages, both share one Pages site and whichever deployed
  last wins (the workflows skill's "Decision made" note); link the URL the repository's workflows actually leave
  in place and flag the overlap in Step 11 rather than promising both.
- **Registry/store pages**: the WordPress.org directory page, Packagist or PyPI page, or GHCR package page from Step 3,
  when those badges were included (a reader without badges rendered still needs the link).
- **SonarCloud/SonarQube dashboard**: reuse the link built in Step 3.
- **Changelog**: if `CHANGELOG.md` exists at the root, link to it directly (`CHANGELOG.md`).
- Omit any of the above whose source doesn't exist — don't add a "Documentation" section at all if none of these
  resolve.

## Step 6 — Compose installation instructions

Match the snippet to the build tool detected in Step 2 — don't show a Maven snippet for a Gradle project or vice
versa:

- **Maven**: a `<dependency>` block with the real `groupId`/`artifactId`, using the latest release version; if the
  current build-file version is a distinct `-SNAPSHOT`, show both under "Latest release" / "Latest snapshot"
  (mirroring how a snapshot repository would need to be added — only mention that if the project's own POM/
  settings actually reference one).
- **Gradle (Kotlin DSL)**: `implementation("<group>:<artifact>:<version>")`. If the project publishes a
  `gradle/libs.versions.toml` version catalog, show that form too — the catalog entry under `[libraries]`
  (`<alias> = { module = "<group>:<artifact>", version.ref = "<versionAlias>" }`) plus the consuming
  `implementation(libs.<alias>)` line — instead of (or alongside) the plain coordinate form.
- **npm**: `npm install <name>`, using the real `package.json` name and its latest published version. Add the
  pnpm (`pnpm add <name>`) and/or yarn (`yarn add <name>`) equivalents only when the repository's own lockfile
  (`pnpm-lock.yaml` / `yarn.lock`) shows that's the package manager actually in use, rather than listing all
  three by default.
- **SwiftPM**: a `.package(url: "<repository-url>", from: "<version>")` entry for `Package.swift`, plus the
  matching `.product(name: "<ProductName>", package: "<PackageName>")` target dependency (read the real product
  name from `Package.swift`'s `products`), and the equivalent steps for Xcode users ("File > Add Package
  Dependencies…", paste the repository URL, select the product).
- **Python** (`python-library`, only when Step 3 confirmed it on PyPI): `uv add <name>` and `pip install <name>`
  (the real `[project].name`), plus the `requires-python` floor. Not on PyPI: `uv add
  "<name> @ git+https://github.com/<owner>/<repo>@<tag>"` only when a release tag exists, or the wheel URL a
  GitHub Release actually attaches — never an invented index.
- **Composer** (`php-library`, only when Step 3 confirmed it on Packagist): `composer require <vendor>/<name>`
  (add `--dev` only if the package is a dev tool by its own `composer.json` `type`/description), plus the PHP floor.
- **Cargo** (plain `rust` library crate, only when Step 3 confirmed it on crates.io): `cargo add <crate>` (or the
  `[dependencies]` line `<crate> = "<latest-release>"`), plus the MSRV.
- **Go modules** (plain `go` module, only when it is public): `go get <module>@latest` (or `@v<latest-tag>`), plus the
  `go` floor; a module path with a `/vN` suffix keeps it.

Services, web apps, WordPress plugins/themes and PrestaShop modules aren't consumed as dependencies, so for them
the section is **Getting Started** — prerequisites, then the commands to run it locally, then (only when a release
workflow publishes one) how to get the released artifact. Every command must be one the repository actually
defines (a script in `package.json`/`composer.json`, a Gradle task, a Maven plugin, a wrapper that exists); read
ports, health paths and env keys from the code/config rather than writing framework defaults from memory, and
never copy a value from `.env`/`.env.example` that looks like a secret — list the key names only.

- **Spring Boot service** (`java-springboot`/`kotlin-springboot`, `-hilla`): prerequisites = the JDK from the
  toolchain/`java.version`, plus Docker when `compose.yaml` or Testcontainers tests exist. Run: Gradle KTS
  `./gradlew :boot:bootRun`; Maven `./mvnw install -DskipTests` (or `mvn` when there's no wrapper) then
  `./mvnw -pl boot spring-boot:run`. When the boot module has an `application-local.*` profile (the catalog's
  scaffold starts `compose.yaml` from it via `spring.docker.compose`), activate it —
  `./gradlew :boot:bootRun --args='--spring.profiles.active=local'` / `-Dspring-boot.run.profiles=local` — and
  say Docker must be running. Tests: `./gradlew test` + `./gradlew integrationTest` (Gradle) or `./mvnw verify`
  (Maven, Failsafe `*IT`); coverage `./gradlew :coverage:testCodeCoverageReport` when that project exists. Kotlin
  quality: `./gradlew detekt ktlintCheck` (Gradle) or `./mvnw detekt:check ktlint:check` (Maven) — only the
  plugins actually configured; API docs: `./gradlew dokkaGeneratePublicationHtml` / `./mvnw dokka:dokka`. Health:
  the Actuator endpoints the config exposes (`management.endpoints.web.exposure.include`, e.g.
  `/actuator/health`). Container image: `./gradlew :boot:bootBuildImage` / `./mvnw -pl boot
  spring-boot:build-image` (or the Jib task the build defines), and the GHCR pull snippet below when published.
- **Quarkus service** (`java-quarkus`/`kotlin-quarkus`): prerequisites = JDK, Docker for Dev Services
  (databases/brokers started automatically in dev and test mode), optionally the Quarkus CLI. Dev mode:
  `./mvnw quarkus:dev` / `./gradlew quarkusDev` (or `quarkus dev` with the CLI) — the Dev UI is at
  `http://localhost:8080/q/dev-ui` and, with `quarkus-smallrye-health`, health at `/q/health` (use the real
  `quarkus.http.port`/root path if overridden). Package and run: `./mvnw package` → `java -jar
  target/quarkus-app/quarkus-run.jar` (Gradle: `./gradlew build` → `build/quarkus-app/quarkus-run.jar`); in a
  hexagonal multi-module layout, the paths are under the app module that carries the Quarkus plugin. Native
  (only when a `native` profile/`quarkus.native` config exists): `./mvnw package -Dnative`. Container image:
  `./mvnw package -Dquarkus.container-image.build=true` when a `quarkus-container-image-*` extension is present,
  otherwise `docker build -f src/main/docker/Dockerfile.jvm .` after packaging.
- **Laravel** (`php-laravel`): prerequisites = PHP floor + the `ext-*` from `composer.json`, Composer 2, Node
  (only when `package.json`/Vite assets exist), and the database from `.env.example`'s `DB_CONNECTION` (SQLite
  needs nothing). Setup: `composer run setup` when that script exists (the stock one runs `composer install`,
  copies `.env.example`, `php artisan key:generate`, `php artisan migrate`, and builds assets), otherwise the
  explicit `composer install`, `cp .env.example .env`, `php artisan key:generate`, `php artisan migrate`,
  `npm install && npm run build`. Run: `composer run dev` when defined, else `php artisan serve`. Tests:
  `composer test` (and `composer test:integration` / `composer test:coverage` when defined). **Sail** only when
  `laravel/sail` is in `require-dev` (and a Sail `compose.yaml` exists): `./vendor/bin/sail up -d` then
  `./vendor/bin/sail artisan migrate`, presented as an optional alternative, never the only path. Container image
  (the `Dockerfile` + a GHCR release workflow): `docker run` with the `EXPOSE`d port and the env vars the image
  expects at run time (`APP_KEY`, `DB_*` — names only), never a baked-in `.env`.
- **WordPress plugin/theme** (`php-wordpress-plugin`/`php-wordpress-theme`): requirements = `Requires at least`/
  `Requires PHP` (and `Tested up to`) from Step 2. Installation, only the routes that actually exist:
  - published on WordPress.org (Step 3): WP admin → **Plugins → Add New Plugin**, search for the plugin name
    (themes: **Appearance → Themes → Add New Theme**), Install, Activate; or `wp plugin install <slug> --activate`
    / `wp theme install <slug> --activate` with WP-CLI;
  - a zip attached to GitHub Releases by `release.yml`: download `<slug>.zip` from the latest release, then
    **Plugins → Add New Plugin → Upload Plugin** (themes: **Appearance → Themes → Add New Theme → Upload Theme**),
    or unzip into `wp-content/plugins/` (`wp-content/themes/`);
  - Composer: `composer require <vendor>/<name>` only when listed on Packagist (Step 3; the site's root
    `composer.json` needs `composer/installers` to land it in `wp-content/`), or
    `composer require wpackagist-plugin/<slug>` (`wpackagist-theme/<slug>`) with the `https://wpackagist.org`
    repository only when published on WordPress.org — never both invented.
  Development: `composer install`, `npm install && npm run build` when `package.json` uses `@wordpress/scripts`,
  and `npx wp-env start` when `.wp-env.json` exists (local site at the port it configures, default
  `http://localhost:8888`; needs Docker); tests via the composer scripts actually defined. Mention that
  `readme.txt` is the WordPress.org listing and is maintained separately.
- **PrestaShop module** (`php-prestashop-module`): compatibility from `ps_versions_compliancy` (e.g. "PrestaShop
  8.x and 9.x") and the PHP floor. Install: download `<module-name>-<version>.zip` from the GitHub Release (when
  `release.yml` attaches it) → back office **Modules → Module Manager → Upload a module**, or unzip into
  `modules/<module-name>/` and run `php bin/console prestashop:module install <module-name>` from the shop root.
  Link the PrestaShop Addons page only when Step 3 found its real URL — Addons uploads are manual, so never imply
  automatic publishing. Development: `composer install` inside the module, then its composer scripts (`test`,
  `lint`, `format:check`) as defined.
- **NestJS** (`nestjs`): prerequisites = Node from `engines.node`/`.nvmrc`, the package manager from the lockfile,
  Docker when a database or Testcontainers e2e tests are configured. Setup: `npm ci`, `cp .env.example .env`, then
  list the keys `.env.example` declares with one-line meanings (from the env schema/validation file, e.g.
  `src/config/env.schema.ts`); start the database with `docker compose up -d` only when a compose file exists, and
  run migrations via the ORM script the project defines (e.g. a `prisma`/`typeorm`/`drizzle` script) — never an
  invented one. Run: `npm run start:dev` (watch mode), production `npm run build && npm run start:prod`. Health:
  the routes the health controller actually declares (the catalog's scaffold: `GET /health/live` and
  `GET /health/ready` on the `PORT` from `.env.example`, default `3000`), plus the Swagger UI path when
  `SwaggerModule.setup('<path>', …)` exists. Tests: `npm test`, `npm run test:e2e` (needs Docker when it uses
  Testcontainers). Docker: `docker build -t <name> .` and `docker run --env-file .env -p 3000:3000 <name>` (port
  from `EXPOSE`).
- **FastAPI** (`python-fastapi`): prerequisites = Python from `.python-version`/`requires-python`, **uv**, Docker
  when `compose.yaml` or `integration`-marked (testcontainers) tests exist. Setup: `uv sync` (creates `.venv` from
  `uv.lock`), `cp .env.example .env` when one exists, listing the `APP_*` keys the `pydantic-settings` class in
  `app/settings.py` declares (names only); `docker compose up -d db` when a compose file has a database service,
  then `uv run alembic upgrade head` when `alembic.ini` exists. Run: `uv run fastapi dev` (reload, uses
  `[tool.fastapi] entrypoint`; else `uv run fastapi dev app/main.py`), production-style `uv run fastapi run` —
  `http://localhost:8000`, with Swagger UI at `/docs`, ReDoc at `/redoc` and the schema at `/openapi.json` (unless
  `docs_url`/`redoc_url`/`openapi_url` are overridden or disabled in `app/main.py`), and the health routes the
  code declares (the catalog's scaffold: `/healthz`, `/readyz`). Tests: `uv run pytest -m "not integration"`
  (fast tier), `uv run pytest -m integration` (needs Docker); quality `uv run ruff check .`, `uv run ruff format
  --check .`, `uv run mypy .`. Docker: `docker compose up --build` when `compose.yaml` exists (Postgres + one-shot
  `migrate` + app), else `docker build -t <name> .` and `docker run --env-file .env -p 8000:8000 <name>` (port
  from `EXPOSE`).
- **Django** (`python-django`): prerequisites as FastAPI. Setup: `uv sync`, `cp .env.example .env` (key names
  only — e.g. `DJANGO_SECRET_KEY`, `DATABASE_URL`, as `config/settings/*.py` reads them), `docker compose up -d db`
  when present, then `uv run python manage.py migrate` and optionally `uv run python manage.py createsuperuser`.
  Run: `uv run python manage.py runserver` (`http://localhost:8000`; settings module from `manage.py`/
  `DJANGO_SETTINGS_MODULE`, e.g. `config.settings.local`); the admin at `/admin/` when `django.contrib.admin` is
  routed; with DRF + drf-spectacular, the Swagger UI / ReDoc / schema at the paths `config/urls.py` maps to
  `SpectacularSwaggerView`/`SpectacularRedocView`/`SpectacularAPIView` (e.g. `/api/schema/swagger-ui/`); with
  Django Ninja, the `NinjaAPI` docs path (default `<api-prefix>/docs`). Tests: `uv run pytest -m "not
  integration"` / `uv run pytest -m integration`; checks `uv run python manage.py check` and `uv run python
  manage.py makemigrations --check --dry-run`. Docker: `docker compose up --build` (one-shot `migrate` service +
  Gunicorn app), or `docker build`/`docker run` with the `EXPOSE`d port and env var names only.
- **Next.js** (`nextjs`): `npm ci`, `npm run dev` (`http://localhost:3000`), `npm run build`, then — server output
  (`output: 'standalone'` or default) — `npm run start`; static export (`output: 'export'`) — the site is written to
  `out/`, previewed with any static server (e.g. `npx serve out`), and, when Step 5 found the Pages deploy, live at
  `https://<owner>.github.io/<repo>/` (omitted under `pages: no`). Tests: `npm test`, `npm run test:e2e`
  (Playwright, when present — `npx playwright install` first). Docker (standalone + `Dockerfile`): `docker build -t
  <name> .` and `docker run -p 3000:3000 <name>`.
- **Released container image** (any of the above, only when Step 3 added the GHCR badge):
  `docker pull ghcr.io/<owner>/<image>:<latest-release-version>` (tags as `docker/metadata-action` writes them —
  check its `tags:` config for `{{version}}`/`latest`), followed by the same `docker run` line. For a private
  repository add that pulling requires `docker login ghcr.io` with a token that has `read:packages`.
- **Distributed apps** (Android/iOS apps, not libraries): when the manifest declares a store distribution (e.g. a
  Gradle `distribution`/Play publishing config, an App Store Connect/Fastlane/`eas submit` workflow step, or
  existing store metadata in the repository), replace the dependency snippet with store links the user fills in
  — `<App Store URL>`, `<TestFlight URL>`, `<Google Play URL>` — as placeholders, never invented real URLs.
  Otherwise (no store distribution config found, or the app isn't a library at all), show how to run it locally
  instead, matched to the detected stack: `npm start` / `npx expo start` (Expo), `npx react-native start` plus
  `npm run android` / `npm run ios` after `bundle install && bundle exec pod install` in `ios/` (React Native
  Metro/bare CLI), `ionic serve` (Ionic), `./gradlew installDebug` (Android), `./gradlew :androidApp:installDebug`
  plus `xcodegen generate` (when `iosApp/project.yml` exists) and "open `iosApp/iosApp.xcodeproj` in Xcode and run"
  (Kotlin Multiplatform), `xcodebuild -scheme <Scheme> -destination …` or "open in Xcode and run" (Apple
  platforms) — pick the one command that actually matches the project's own scripts/Gradle
  tasks/scheme rather than a generic default.
- **Desktop apps** (`macos-app`, `windows-app`): no dependency snippet. When Step 5 found a release workflow,
  an "Install" subsection matched to what it actually publishes — macOS: "download the notarized
  `<AppName>-<version>.dmg` from the latest GitHub Release, open it and drag the app to Applications" (Developer ID
  release) or `<Mac App Store URL>` (App Store upload); Windows: "download `<AppName>-<version>-win-x64.zip` (or
  `-win-arm64`) from the latest GitHub Release and run `<AppName>.exe`", "install the MSIX / open the
  `.appinstaller` link for automatic updates" (only when the workflow produces them), `winget install
  <PackageIdentifier>` (only when a WinGet job exists — the identifier read from the workflow), or
  `<Microsoft Store URL>` (Store submission) — store URLs always as placeholders. Then "Build and run locally":
  macOS — `xcodegen generate` (when `project.yml` exists), `xcodebuild -scheme <AppName> -destination
  'platform=macOS' build` or "open `<AppName>.xcodeproj` in Xcode and run", tests with `xcodebuild test -scheme
  <AppName> -destination 'platform=macOS'` and `swift test --package-path Packages/Core`; Windows — `dotnet build`,
  `dotnet run --project src/<AppName>` (Windows only), `dotnet test --filter "TestCategory!=UI"` (the Core tests
  also run on macOS/Linux), and the .NET 10 SDK / Windows 10 1809+ (WinUI) prerequisites.
- **Command-line tools** (`cli-tool`): no dependency snippet. An **Installation** section listing **only** the
  channels the release configuration actually wires — read the jobs of `.github/workflows/release.yml` (`crates-io`,
  `homebrew`, `winget`, `nuget`, `publish`) and, for Go, the `homebrew_casks`/`scoops`/`winget` blocks of
  `.goreleaser.yaml` — in this order, each a one-liner with the real names:
  - Homebrew (`homebrew` job, tap from its `repository:`/checkout, e.g. `<owner>/homebrew-tap` → `<owner>/tap`):
    `brew install <owner>/tap/<bin>`; Go's GoReleaser writes a **cask**, so `brew install --cask <owner>/tap/<bin>`.
  - crates.io (`crates-io` job, and Step 3 found the crate live — otherwise say "after the first release"):
    `cargo install <crate> --locked` (the package name, which may differ from `<bin>`).
  - Go: `go install <module>/cmd/<bin>@latest` for a public module (it needs no release job — the module proxy serves
    tags; mention that such a binary reports the tag's version but no commit/date).
  - Scoop (Go `scoops`, bucket from its `repository:`): `scoop bucket add <bucket> https://github.com/<owner>/<bucket-repo>`
    then `scoop install <bucket>/<bin>`.
  - WinGet (`winget` job's `wingetcreate update <id>`, or Go's `package_identifier`): `winget install <id>` — only
    once the first manual submission was merged into `microsoft/winget-pkgs`; say so in Step 11 when unknown.
  - .NET tool (`nuget` job, `PackageId`): `dotnet tool install -g <package-id>` (Native AOT binary per RID, falling
    back to the framework-dependent `any` package), or run it once without installing via `dnx <package-id>`.
  - Release archives (any `release.yml` with a `publish` job / GoReleaser `archives`): download
    `<bin>-<version>-<target>.tar.gz` (`.zip` on Windows; Go names targets `<os>-<arch>`, e.g.
    `linux-amd64`) and `SHA256SUMS` from the latest GitHub Release (`gh release download -R <owner>/<repo>
    --pattern '<bin>-*-<target>.tar.gz' --pattern SHA256SUMS`), verify with `sha256sum --check SHA256SUMS
    --ignore-missing` (macOS: `shasum -a 256 --check SHA256SUMS --ignore-missing`) and, only when the workflow runs
    `actions/attest-build-provenance`, `gh attestation verify <archive> -R <owner>/<repo>`, then put `<bin>` on the
    `PATH`. List the target names the workflow's matrix actually builds.
  Then **Build from source**, with the toolchain floor from Step 4: Rust `cargo install --path . --locked` (or
  `cargo build --release --locked` → `target/release/<bin>`); Go `go install ./cmd/<bin>` (or `go build -o <bin>
  ./cmd/<bin>`); Swift `swift build -c release --product <bin>` → `$(swift build -c release --show-bin-path)/<bin>`;
  .NET `dotnet publish src/<ToolName> -c Release -r <rid> -o artifacts/publish/<rid>` (Native AOT, same-OS) or
  `dotnet run --project src/<ToolName> -- --help`. Add the test/quality commands the project defines (Rust
  `cargo nextest run --workspace --locked`/`cargo test`, Go `go test ./...`, `swift test`, `dotnet test
  <ToolName>.slnx`) under a short **Development** subsection. With `distribution: none` (no `release.yml`, no
  `.goreleaser.yaml`) only `go install` (public Go modules) and Build from source remain — never list a channel
  the repository doesn't wire.
- **Python library** (`python-library`) development, after the Installation snippet: `uv sync`, `uv run pytest`,
  `uv run ruff check .`, `uv run mypy .`, `uv build` (sdist + wheel in `dist/`) — only the tools actually
  configured in `pyproject.toml`.
- If the build tool isn't one of the above, or the project isn't actually published/publishable/runnable yet (no
  registry/repository/run config found), omit the Installation section and note the gap in Step 11 rather than
  guessing coordinates.

## Step 7 — Write the "how it works" section with an example

This is the most judgment-heavy part — ground it in what the code actually does, don't invent behavior:

- Identify the main source entry points (the primary public classes/interfaces/functions a consumer would use —
  for a library, usually a small number of top-level types; for an application, its README-worthy commands/
  endpoints) without reading the whole source tree directly: use the `Explore` agent to locate them first, then
  read only those specific files.
- If Antora docs already exist (`docs/modules/ROOT/pages/index.adoc`, `getting-started.adoc`, or similar), prefer
  reusing/adapting their conceptual explanation and example code rather than writing a divergent one from scratch
  — the README and the docs site describing the same library differently is a maintenance trap.
  If a docs example exists, verify it still matches the current API shape before reusing it — the docs page might
  itself be stale.
- Write a short paragraph (a few sentences) on the core concept, plus one minimal, realistic code example that
  would actually compile/run against the current API — check public method/constructor signatures rather than
  guessing them.
- For a service or web app the example is a request against a real endpoint, not a library call: a `curl`
  against a route a controller actually declares (Spring `@RestController`/`@*Mapping`, Quarkus/JAX-RS `@Path`,
  NestJS `@Controller`/`@Get`, a Laravel `routes/api.php`/`routes/web.php` entry, a Next.js route handler or
  page, a FastAPI `APIRouter` `@router.get`/`@router.post` included by `app/main.py` (mind its `prefix`), a Django
  DRF `ViewSet` registered on a router or a plain view / `NinjaAPI` operation wired in `config/urls.py` /
  `apps/<x>/urls.py`), with the request/response shape read from its DTOs (Pydantic/SQLModel `XCreate`/`XPublic`
  models, DRF serializers, Ninja schemas) and the port from Step 6. For a WordPress plugin/theme,
  show what a site builder actually uses — the block name, shortcode, `add_filter`/`add_action` hook it exposes, or
  the theme's templates/patterns; for a PrestaShop module, the hooks it registers in `install()` and its
  configuration page. For a `python-library`, a short Python snippet importing its public API (what the package's
  `__init__.py` exports / `__all__`).
- For a **command-line tool** (`cli-tool`) the section is **Usage**, built from the real command tree (`<bin>
  --help`, or `<bin> schema` when the tool has it — run the built binary when one is available, else read the
  command definitions):
  - a human example — one real command and its text output (the catalog scaffolds' sample: `<bin> greet Ada`);
  - a machine example — the same command with `--json` piped to `jq` (e.g. `<bin> greet Ada --json | jq -r
    .greeting`), showing the JSON shape the command actually prints (read a golden file such as
    `tests/golden/greet-ada.json` or a `testdata/script/*.txtar` expectation rather than guessing field names);
  - an **Exit codes** table read from the tool's exit-code definition (`src/exit.rs`, `internal/cli/exitcode.go`,
    `Sources/<Bin>Kit/CLIExitCode.swift`, `src/<ToolName>.Core/ExitCode.cs`) — for the catalog's contract: `0` OK,
    `1` internal error, `2` usage error, `3` validation failed, `4` not found, `5` confirmation required, `6`
    retryable (try again later), `7` authentication/authorization, `130`/`143` interrupted by SIGINT/SIGTERM — only
    the codes the file actually defines;
  - a short **Using from scripts and AI agents** note: pass `--json` (or `--format json`/`jsonl`) for
    machine-readable output and `--no-input` (or the `<BIN>_NO_INPUT=1` variable the tool reads) so it never
    prompts; stdout carries only the result, while diagnostics, progress and the JSON error envelope go to stderr;
    branch on the exit code, not on message text; `<bin> schema` describes every command, flag, exit code and safety
    hint as JSON. Mention only flags and commands the tool actually has.
  A plain `rust`/`go` library shows a short code snippet against its public API instead, like any library.
- If the repository has no meaningful source yet (a brand-new, scaffolded-but-empty project), omit this section
  entirely rather than writing a placeholder example. A catalog scaffold's sample feature (e.g. a `books` sample)
  is real, runnable code — it may be shown, labeled as the sample it is.

## Step 8 — Compose the remaining structural sections

Include each only when Steps 2–7 gave it real content:

- **Title + tagline**: repository name as an `# H1`, one-sentence description from Step 2 underneath.
- **Badges**: from Step 3, directly under the title.
- **Project Status**: table from Step 4.
- **Documentation**: links from Step 5.
- **Installation** (libraries, command-line tools) or **Getting Started** (services, web apps,
  plugins/themes/modules): snippet(s) and commands from Step 6, with a short **Requirements** list first when Step 6
  gathered prerequisites.
- **How It Works** / **Quick Example** (or **Usage** for a command-line tool): prose + code from Step 7.
- **License**: one line naming the license from Step 2, linking to the `LICENSE` file.

If the existing `README.md` read in Step 1 had additional sections this skill doesn't generate (e.g.
"Contributing", "Acknowledgements", a project-specific comparison table like "Choosing a Detector"), keep them
verbatim in the proposed version, in their original relative position, rather than silently dropping
hand-written content this skill doesn't know how to regenerate.

## Step 9 — If `README.md` already existed, get approval before writing

Skip this step entirely if Step 1 found no existing file — proceed straight to Step 10.

- Show the user the full proposed new `README.md` content (or a diff against the current file — writing the
  draft to a temp path and running `git diff --no-index <current> <draft>` gives a clean unified diff) so they
  can see exactly what would change section by section. Also list the hand-written sections Step 8 preserved.
  When Step 1 identified the file as a generator's stock README, say so and make **Replace** the recommended
  option instead of Update (there is nothing hand-written to keep).
  When the existing file contradicts this run's choices, say so concretely (e.g. "your current README shows
  SonarCloud badges but this run chose `sonar: none`", or "it links a github.io docs site but `pages: no`").
- Unless Step 0's `on-existing` already decided (`update`/`replace`, applied without asking — the diff is still
  shown), ask via `AskUserQuestion` (header e.g. "README"), explaining each consequence:
  - **Update (Recommended)** — "Write the draft shown: regenerated sections are refreshed from the repository's
    current state, and every hand-written section this skill doesn't own (e.g. Contributing, Acknowledgements) is
    kept in place. Your customizations outside those sections survive, but a customized section this skill owns
    (badges, status table, installation, …) may be rewritten."
  - **Keep as is** — "Leave the existing `README.md` untouched. Nothing you wrote changes, but it may stay out of
    date or disagree with this run's choices (stale badges, a docs link that won't exist) — the report will list
    each mismatch."
  - **Replace** — "Write only this skill's generated sections, dropping the hand-written sections listed above.
    Result matches this house pattern exactly, but those sections are lost (recoverable only from git history)."
  There is no partial-apply option here — if the user wants to keep some sections and change others, let them say
  so in free text and revise the draft before writing.
- Only proceed to Step 10 on an explicit **Update** or **Replace** (from the user or `on-existing`). Under
  **Replace**, drop the preserved hand-written sections from the draft before writing.

## Step 10 — Write `README.md`

Write the composed content (Step 8, incorporating any edits from Step 9's review, and minus the preserved
hand-written sections under **Replace**) to `README.md` at the repository root.

## Step 11 — Report

Start by restating the mode — "created from scratch", or for an existing `README.md` the option applied
(**updated** / **kept as is** / **replaced**, and whether it came from the user or from `on-existing`); under
**Keep as is**, list each mismatch between the kept file and this run's choices (`sonar`/`ci`/`pages`). Then
summarize: which sections were included versus omitted and why (e.g. "no Installation section — no build/package
config found", "no CI badges — no GitHub Actions workflows present"), any fact that had to be inferred rather than
confirmed (e.g. an Antora Pages URL assumed from convention), and every badge/link suppressed by Step 0's
`sonar: none`/`ci: no`/`pages: no`, and every registry/store badge withheld because the package/slug/image
isn't live yet (Packagist, PyPI, WordPress.org, GHCR, crates.io, NuGet, pkg.go.dev) together with the check used;
for a command-line tool, every channel listed under Installation and the release job/config it came from, and any
wired channel left out because its first (manual) publication can't be confirmed. For WordPress projects, state that
`readme.txt` was left untouched. Remind the user to double-check the "How It Works"/example section
specifically, since it's the part most dependent on this skill's reading of the current API rather than on
mechanically-derived facts like versions or badge URLs.
