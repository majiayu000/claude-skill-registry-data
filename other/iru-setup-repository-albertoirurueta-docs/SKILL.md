---
name: iru-setup-repository
description: >-
  End-to-end bootstrap front door for this entire catalog — invoke as `/iru-setup-repository` and use
  it as THE one entry point new users should reach for to bootstrap any repository, instead of hunting for which
  of this catalog's stack-specific orchestrators applies. Covers every project type this catalog can scaffold —
  `java-library`, Spring Boot services (`java-springboot`, `java-springboot-hilla`, `kotlin-springboot`,
  `kotlin-springboot-hilla`), Quarkus services (`java-quarkus`, `kotlin-quarkus`), `typescript-library`,
  `react-web`, `nextjs`, `angular-web`, `nestjs`, PHP (`php-laravel`, `php-wordpress-plugin`,
  `php-wordpress-theme`, `php-prestashop-module`), Python (`python-fastapi`, `python-django`), `android-library`, `android-app`, `swift-library`, `apple-app`
  (`ios`/`ipados`/`macos`/`watchos`/`visionos`, SwiftUI or UIKit, MVVM or MVC), `react-native-app` (`expo`/`metro` toolchain), `ionic-app` (`angular`/`react`),
  `kmp-app` (Kotlin Multiplatform for Android + iOS, `compose`/`native` UI), and the desktop apps `macos-app`
  (native macOS, `swiftui`/`appkit`) and `windows-app` (.NET 10, `wpf`/`winui`/`winforms`), and agent-friendly
  command-line tools `cli-tool` (`rust`/`go`/`swift`/`dotnet`, optional terminal UI) — by surveying the
  working directory (running `iru-explore` first when it already holds code) to detect which one applies, asking
  only the shared, cross-cutting questions the detected/chosen type still needs, then delegating the actual
  scaffold to the matching stack orchestrator (`iru-setup-java-library-repository`, `iru-setup-java-springboot`,
  `iru-setup-quarkus-repository`, `iru-setup-typescript-repository`, `iru-setup-php-repository`,
  `iru-setup-python-repository`, `iru-setup-android-repository`, `iru-setup-swift-repository`,
  `iru-setup-kmp-repository`, `iru-setup-macos-repository`, `iru-setup-windows-repository`, or
  `iru-setup-cli-repository`) via
  `iru-isolated-skill-executor`. Accepts
  `args` (`key: value` lines) to pre-resolve `project-type`, `open-source`, `visibility`
  (`public`/`private`/`internal`, otherwise detected via `gh repo view` or asked), `ci` (`yes`/`no`), `ci-tests`
  (`unit`/`full`), `pages` (`yes`/`no`), `publish`, `distribution`, `sonar`
  (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`), `mode` (`new`/`existing`), `on-existing`
  (`ask`/`keep`/`update`/`replace`, scripted runs only), `flavor`, the stack-shape keys `language` (JVM
  `java`/`kotlin`, or a command-line tool's `rust`/`go`/`swift`/`dotnet`), `build-tool`,
  `layout`, and `frontend` (JVM services), `accessibility` (`enforce`/`report`/`off` — UI types: how strictly the UI
  tests' automated accessibility checks gate, recorded in `.ui-quality.yml`), `python-version`, `platforms`, `framework`, `toolchain` (React Native
  `expo`/`metro`), `native-builds`, `ui` (Kotlin Multiplatform `compose`/`native`, macOS `swiftui`/`appkit`,
  Windows `wpf`/`winui`/`winforms`, a command-line tool's `none`/`tui`), `architecture` (desktop apps'
  `mvvm`/`mvc`), `integration-branch`,
  `stable-branch`, `license`, `developer-name`, `developer-email`, and `organization-url` — forwarding each only
  to the delegated orchestrator whose own `args` contract actually accepts it, and never asking a question
  `args` already answered or one the delegated orchestrator asks itself. Asks whether CI workflows are wanted,
  whether Sonar receives CI reports, whether CI runs unit-only or the full test suite, and (private repos) whether
  docs go to GitHub Pages, stating the Actions-minutes / SonarCloud / Pages cost differences between public and
  private repositories. Announces whether it is setting up from scratch or updating an existing repository (with
  an inventory of the prior setup it found); on an existing repository it runs `iru-explore` first and forces
  `mode: existing`, and every delegated component then warns about each pre-existing artifact and asks whether to
  keep, update, or replace it. Use whenever a user wants to bootstrap (or catch up) a repository and either
  doesn't know or shouldn't have to know which of this catalog's twelve stack-specific setup orchestrators to
  invoke directly.
model: sonnet
---

# Setup Repository

The catalog's single bootstrap front door. This skill does not scaffold anything itself — it detects or asks which
of the supported project types the repository is (or should become), collects the handful of questions that are
genuinely shared across every stack (open source, repository visibility, CI/CD and its test scope, Sonar, GitHub
Pages, publish/distribution, and a few flavor-specific inputs), and then hands off to exactly one of twelve existing
stack orchestrators, each of which asks its own project-identity questions (groupId/artifactId, package/app name,
slug, etc.) and its own stack-shape questions (JVM language/build tool/layout/frontend, NestJS ORM, Next.js output,
PHP version floor, Python version/database/ORM/API, Kotlin Multiplatform UI approach, desktop UI framework and
MVVM/MVC architecture, a command-line tool's terminal UI and package channels, ...) and does the actual scaffolding.

## Step 0 — Resolve inputs

This skill is always the entry point (nothing else in this catalog orchestrates it), but it can still be re-invoked
with `args` (`key: value` lines) by a script or a returning user, so parse `args` first, one `key: value` pair per
line, e.g.:

```
project-type: android-app
mode: new
open-source: yes
visibility: public
ci: yes
ci-tests: full
pages: yes
distribution: store
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_my-app
sonar-host-url: https://sonarcloud.io
```

Recognized keys: `project-type` (any value from the vocabulary in Step 1), `mode` (`new`/`existing`),
`open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal` — the GitHub repository's visibility;
`internal` is treated like `private` for every cost decision), `ci` (`yes`/`no` — whether GitHub Actions workflows
are generated/updated at all), `ci-tests` (`unit`/`full` — only meaningful with `ci: yes`), `pages` (`yes`/`no` —
whether docs are deployed to GitHub Pages from CI; only meaningful with `ci: yes`), `on-existing`
(`ask`/`keep`/`update`/`replace` — how every component treats prior setup it finds; default `ask`; meant for
scripted runs, so this skill never asks it and forwards it only when it arrived here), `publish` (`yes`/`no` —
library types only), `distribution` (`none`/`internal`/`store` — app types only), `sonar`
(`cloud`/`self-hosted`/`none`) plus, only when set, `sonar-organization`/`sonar-project-key`/`sonar-host-url`,
`flavor` (the delegated orchestrator's own flavor value — see Step 2's table; usually redundant with
`project-type` and can be left unset), the JVM stack-shape keys `language` (`java`/`kotlin` — or, for `cli-tool`, `rust`/`go`/`swift`/`dotnet`, which
Step 2's follow-up resolves), `build-tool`
(`maven`/`gradle`), `frontend` (`none`/`hilla` — Spring Boot only), and `layout` (`single`/`hexagonal` — Quarkus
only) — **never asked here** (the delegated orchestrator asks them itself), only forwarded when supplied via `args`
or pre-set by Step 1's detection — `platforms` (Apple app / Swift library), `framework` (Ionic's `angular`/`react`),
`toolchain` (React Native's `expo`/`metro`), `native-builds` (React Native's `eas`/`local` — Expo toolchain
only), `ui` (Kotlin Multiplatform's `compose`/`native`, macOS's `swiftui`/`appkit`, Windows' `wpf`/`winui`/
`winforms`, a command-line tool's `none`/`tui` — never asked here, only forwarded), `architecture` (desktop apps' `mvvm`/`mvc` — likewise only
forwarded), `accessibility` (`enforce`/`report`/`off` — UI types only; how strictly the UI tests' automated
accessibility checks gate, recorded by the UI scaffold in `.ui-quality.yml`), `python-version` (Python only — likewise never asked here), plus the
pass-through-only keys `integration-branch`, `stable-branch`, `license`, `developer-name`, `developer-email`,
`organization-url` (see Step 3's closing note — this skill never asks for these itself, it only forwards them when
supplied). Every key found here is resolved — skip the matching question below. Any **other** `key: value` line
(e.g. `name`/`scope`/`description`/`node-version`/`package-manager`/`orm`/`database`/`output`/`e2e` for
`iru-setup-typescript-repository`, `slug`/`vendor`/`php-version` for `iru-setup-php-repository`,
`group-id`/`artifact-id`/`java-version` for `iru-setup-quarkus-repository`,
`name`/`package`/`description`/`database`/`orm`/`api` for `iru-setup-python-repository`,
`group-id`/`artifact-id`/`namespace` for `iru-setup-android-repository`, `app-name`/`application-id`/`bundle-id`/
`namespace` for `iru-setup-kmp-repository`, `app-name`/`bundle-id`/`team-id`/`min-macos`/`sandbox` for
`iru-setup-macos-repository`, `app-name`/`display-name`/`publisher`/`package-name`/`signing`/`winget` for
`iru-setup-windows-repository`, `bin-name`/`description`/`owner`/`channels`/`homebrew-tap`/`cross-os-ci`/
`crate-name`/`module-path`/`tool-name`/`package-id` for `iru-setup-cli-repository`) is kept as an opaque pass-through: Step 4
forwards it verbatim only if the delegated orchestrator's own Step 0, read on disk there, recognizes the key, and
Step 5 lists every line that was dropped because no delegated skill accepts it — never silently (without this
pass-through, a fully pre-resolved `mode: new` run still stops to ask for the package name and Node version).
If `args` is absent or doesn't look like this format, treat everything as unset and ask normally.

## Step 1 — Survey the repository

Check whether the working directory already holds a real repository before asking anything: `git ls-files | head`
returning any output, or any of these manifests present at any depth worth a shallow `find`/`ls` check —
`pom.xml`, `build.gradle`/`build.gradle.kts`, `settings.gradle`/`settings.gradle.kts`, `package.json`,
`composer.json`, a root `style.css`/`theme.json` (WordPress theme), `pyproject.toml`, `requirements.txt`, `manage.py`,
`setup.py`, `Package.swift`, `*.xcodeproj`, `project.yml`,
`Project.swift`, `*.csproj`/`*.sln`/`*.slnx`, `Cargo.toml`, `go.mod`.

- **Non-empty** (a real, at-least-partially-scaffolded repository): run `Skill({skill: "iru-explore"})` with no
  ticket argument — this is a codebase-only exploration, not one grounded in a ticket. Read the `- Project type:`
  line (and, for JVM services and `apple-app`, the `- Build & layout:` line) from its `## Tech stack` report block. Set
  `mode: existing` (unless `args` already supplied `mode`) and pre-select the recommended Step 2 option from the
  value reported, per the mapping table below. If the line reads `multiple`, list the reported
  `<module-path>: <type>` entries to the user and treat this as a repository that needs more than one bootstrap
  pass — ask which module to bootstrap first (or run this skill again per module), rather than guessing one.
- **Empty** (no tracked files, no manifest): set `mode: new` (unless `args` already supplied it) without running
  `iru-explore` — there's nothing yet for it to detect.

The `- Project type:` vocabulary, read **verbatim** — this is a shared contract with `iru-explore`'s own Step 7,
which documents the exact same list and derivation table, so never paraphrase or invent a value outside it:

```
java-library, java-springboot, java-springboot-hilla, kotlin-springboot, kotlin-springboot-hilla, java-quarkus,
kotlin-quarkus, typescript-library, react-web, angular-web, nestjs, nextjs, php-laravel, php-wordpress-plugin,
php-wordpress-theme, php-prestashop-module, php-library, python-fastapi, python-django, python-library,
android-library, android-app, swift-library,
apple-app (ios, ipados, macos, watchos, visionos), macos-app (swiftui|appkit), react-native-app (expo|metro),
ionic-app (angular|react), kmp-app (compose|native), windows-app (wpf|winui|winforms),
cli-tool (rust|go|swift|dotnet), rust, go, dotnet, other, unknown
```

(`multiple` is also possible — handled above, not a project type in its own right.) Map a detected value straight
to its Step 2 option and the stack-shape `args` it pre-sets — offer that option as the first choice, labeled
"(detected)", instead of running the full six-round interview, and forward the pre-set keys in Step 4 so the
delegated orchestrator confirms rather than re-asks them:

| Detected `Project type:` | Step 2 option | Delegated orchestrator | Pre-set `args` |
|---|---|---|---|
| `java-library` | Java library | `iru-setup-java-library-repository` | — |
| `java-springboot` | Spring Boot service | `iru-setup-java-springboot` | `language: java`, `build-tool: maven`, `frontend: none` |
| `java-springboot-hilla` | Spring Boot service | `iru-setup-java-springboot` | `language: java`, `build-tool: maven`, `frontend: hilla` |
| `kotlin-springboot` | Spring Boot service | `iru-setup-java-springboot` | `language: kotlin`, `build-tool` from the files (below), `frontend: none` |
| `kotlin-springboot-hilla` | Spring Boot service | `iru-setup-java-springboot` | `language: kotlin`, `build-tool` from the files (below), `frontend: hilla` |
| `java-quarkus` | Quarkus service | `iru-setup-quarkus-repository` | `language: java` |
| `kotlin-quarkus` | Quarkus service | `iru-setup-quarkus-repository` | `language: kotlin` |
| `typescript-library` | TypeScript/npm library | `iru-setup-typescript-repository` | `flavor: library` |
| `react-web` | Web app → React | `iru-setup-typescript-repository` | `flavor: react` |
| `nextjs` | Web app → Next.js | `iru-setup-typescript-repository` | `flavor: nextjs` |
| `angular-web` | Web app → Angular | `iru-setup-typescript-repository` | `flavor: angular` |
| `nestjs` | NestJS service | `iru-setup-typescript-repository` | `flavor: nestjs` |
| `php-laravel` | Laravel application | `iru-setup-php-repository` | `flavor: laravel` |
| `php-wordpress-plugin` | WordPress plugin or theme → plugin | `iru-setup-php-repository` | `flavor: wordpress-plugin` |
| `php-wordpress-theme` | WordPress plugin or theme → block theme | `iru-setup-php-repository` | `flavor: wordpress-theme` |
| `php-prestashop-module` | PrestaShop module | `iru-setup-php-repository` | `flavor: prestashop-module` |
| `python-fastapi` | FastAPI service | `iru-setup-python-repository` | `flavor: fastapi` |
| `python-django` | Django project | `iru-setup-python-repository` | `flavor: django` |
| `android-library` | Android → library | `iru-setup-android-repository` | `flavor: library` |
| `android-app` | Android → app | `iru-setup-android-repository` | `flavor: app` |
| `swift-library` | Apple → Swift library | `iru-setup-swift-repository` | `flavor: library` |
| `apple-app (…)` | Apple → Apple app | `iru-setup-swift-repository` | `flavor: app`, `platforms` from the parenthetical |
| `react-native-app (…)` | Cross-platform → React Native | `iru-setup-typescript-repository` | `flavor: react-native`, `toolchain` from the parenthetical |
| `ionic-app (…)` | Cross-platform → Ionic | `iru-setup-typescript-repository` | `flavor: ionic`, `framework` from the parenthetical |
| `kmp-app (…)` | Cross-platform → Kotlin Multiplatform | `iru-setup-kmp-repository` | `ui` from the parenthetical |
| `macos-app (…)` | Desktop → macOS app | `iru-setup-macos-repository` | `ui` from the parenthetical |
| `windows-app (…)` | Desktop → Windows app | `iru-setup-windows-repository` | `ui` from the parenthetical |
| `cli-tool (…)` | Command-line tool → its language | `iru-setup-cli-repository` | `language` from the parenthetical; `ui: tui` when the `Build & layout:` line names a terminal-UI library |

- **Kotlin Spring Boot build tool**: a root `pom.xml` → `build-tool: maven`; `settings.gradle.kts`/`build.gradle.kts`
  → `build-tool: gradle`. A Groovy-DSL-only Gradle build (`settings.gradle`/`build.gradle`) → send no `build-tool`
  and say so — `iru-setup-java-springboot`'s own Step 0 detects it and runs its incompatible-build hard-stop
  question. Never pre-set `build-tool` for Quarkus or `layout` for either: in `mode: existing`,
  `iru-setup-quarkus-service` detects build tool and layout from the build itself, and the Spring Boot chain reads
  them from the reactor and `springboot-stack.yml`.
- An `android-library` line carrying a `- sample app: <module>/` sub-line is still `android-library` (the catalog's
  reference `lib/` + sample `app/` layout) — never treat the sample module as a reason to ask "which module".
- `apple-app (…)`, `ionic-app (…)`, and `react-native-app (…)` also pre-fill Step 3's `platforms`/`framework`/
  `toolchain` questions from the parenthetical, so the user only needs to confirm rather than re-answer them.
  `kmp-app (…)`'s `ui` is forwarded as detected and confirmed by `iru-setup-kmp-repository`, never asked here.
  Likewise `apple-app (…)`'s `Build & layout:` line carries the iOS target's UI framework (`swiftui`/`uikit`) and
  the `Packages/Core` architecture (`mvvm`/`mvc`) — forward each one it names as `ui`/`architecture` (Step 4) — values
  detected from disk, so neither this skill nor `iru-setup-swift-repository` asks them fresh; tell the user which
  values were detected so a wrong one can be corrected before the scaffold runs.
- A `kmp-app` repository also contains an Android application module and an `iosApp/` — they belong to the KMP
  app, so never offer `android-app`/`apple-app` for them or treat the repository as `multiple`.
- `php-library` — a plain Composer package. This catalog has **no scaffold skill for it** (`iru-setup-php-repository`
  covers Laravel, WordPress, and PrestaShop only). Report that plainly — project type detected: `php-library`; no
  bootstrap orchestrator to delegate to; the PHP gate skills (`iru-php-test`, `iru-php-coverage`,
  `iru-php-code-quality`, `iru-php-phpdoc`) and `iru-setup-antora`, `iru-setup-php-gitignore`,
  `iru-setup-changelog`, `iru-setup-readme` can still be run individually — and stop here for this run, exactly
  like `dotnet` below.
- `python-library` — a plain Python package (no FastAPI/Django). This catalog has **no scaffold skill for it**
  (`iru-setup-python-repository` covers FastAPI and Django only). Report that plainly — project type detected:
  `python-library`; no bootstrap orchestrator to delegate to; the Python gate skills (`iru-python-test`,
  `iru-python-coverage`, `iru-python-code-quality`, `iru-python-docstrings`) and `iru-setup-antora`,
  `iru-setup-python-gitignore`, `iru-setup-changelog`, `iru-setup-readme` can still be run individually — and stop
  here for this run, exactly like `dotnet` below.
- `macos-app (…)` / `windows-app (…)` forward only `ui` from the parenthetical; `architecture` is detected and
  confirmed by the delegated orchestrator itself (from `ViewModels/` vs. `Controllers/`), never asked here. An
  `apple-app (…)` whose platforms include `macos` *and* another platform — or a macOS-only `iru-setup-apple-app`
  scaffold (`Targets/macOS/…`), which `iru-explore` keeps as `apple-app (macos)` — stays `apple-app`; never offer
  `macos-app` for it.
- `cli-tool (…)` forwards `language` from the parenthetical (and `ui: tui` when `iru-explore`'s `Build & layout:`
  line names Ratatui, Bubble Tea, Terminal.Gui or a `browse` TUI command — otherwise nothing, so the orchestrator
  confirms `none`). A Rust crate, Go module, SwiftPM package or .NET project that isn't a CLI stays `rust`/`go`/
  `swift-library`/`dotnet`; never offer the CLI type for it.
- `rust` / `go` — a Rust crate or Go module that isn't a command-line tool. This catalog has **no bootstrap
  orchestrator for a Rust/Go library or service**. Report that plainly (project type detected; no orchestrator to
  delegate to; the gate skills `iru-rust-test`/`-coverage`/`-code-quality`/`-rustdoc` or `iru-go-test`/`-coverage`/
  `-code-quality`/`-godoc`, and `iru-setup-antora`, `iru-setup-rust-gitignore`/`iru-setup-go-gitignore`,
  `iru-setup-changelog`, `iru-setup-readme` can still be run individually) and stop here, exactly like `dotnet` below.
- `dotnet` — this catalog has **no bootstrap orchestrator for a plain .NET library or service** (Windows desktop
  apps are `windows-app`, above). Report that plainly (project type detected: `dotnet`; no
  `iru-setup-dotnet-repository`-style skill exists in this catalog to delegate to; the .NET gate skills
  `iru-dotnet-test`/`-coverage`/`-code-quality`/`-docfx` and `iru-setup-antora`, `iru-setup-changelog`,
  `iru-setup-readme` can still be run individually) and stop here for this run rather than falling through to
  Step 2 — there is nothing to offer. (A .NET command-line tool is `cli-tool (dotnet)`, above.)
- `other` / `unknown` / no ticket detected at all — fall through to asking the user directly in Step 2, with no
  pre-selection; a stack `iru-explore` couldn't place isn't one this skill can guess a delegated orchestrator for
  either.

### Announce the setup mode

Right after the survey (and before asking anything in Steps 2–3), tell the user which of the two this run is doing:

- **`mode: new`** → "Setting up this repository **from scratch** — no prior setup found."
- **`mode: existing`** → "**Updating an existing repository** — prior setup found:" followed by an inventory table
  of every component the delegated pipeline owns, each marked **absent** / **present** / **partial** with the
  evidence (file paths) — a shallow `ls`/`find` per row is enough, no deep reads:

  | Component | Evidence to check |
  |---|---|
  | Build manifest | `pom.xml`, `build.gradle(.kts)`/`settings.gradle(.kts)` (+ `gradle/libs.versions.toml`, `build-logic/`), `package.json`, `composer.json`, `pyproject.toml` (+ `uv.lock`/`poetry.lock`, `.python-version`), `Package.swift`, `*.xcodeproj`/`project.yml`/`Project.swift`; stack manifests `springboot-stack.yml`/`quarkus-stack.yml` |
  | Source layout | `src/` (`src/main/java`/`src/main/kotlin`), hexagonal modules (`domain/`, `application/`, `infrastructure/`, `api/`), `lib/`/`app/` modules, `Sources/`/`Tests/`, Laravel `app/`+`artisan`, the WordPress main plugin file / `style.css`+`theme.json`, the PrestaShop `<module>.php`+`config.xml`, FastAPI `app/main.py` (+ `alembic/`), Django `manage.py`+`config/`+`apps/` |
  | Antora docs | `docs/antora.yml`, `docs/antora-playbook.yml`, `docs/modules/ROOT/` |
  | `.gitignore` | `.gitignore` |
  | CI workflows | each file under `.github/workflows/` (listed individually) |
  | Dependabot | `.github/dependabot.yml` |
  | Sonar config | `sonar-project.properties`, `sonar.*` properties in `pom.xml`, a `sonar {}` block in Gradle |
  | Quality config | `checkstyle.xml`, `detekt.yml`, `.editorconfig`, `phpstan.neon(.dist)`, `phpcs.xml.dist`, `pint.json`, `.php-cs-fixer.dist.php`, `[tool.ruff]`/`[tool.mypy]` in `pyproject.toml` (or `ruff.toml`/`mypy.ini`), `.pre-commit-config.yaml`, ESLint/oxlint/Biome config |
  | Container | `Dockerfile`, `.dockerignore`, `compose.yaml`/`docker-compose.yml` (service stacks: Quarkus, NestJS, Laravel, FastAPI, Django) |
  | Changelog | `CHANGELOG.md` (or `CHANGELOG.rst`/`CHANGELOG.txt`/`HISTORY.md`) |
  | README | `README.md` |
  | License | `LICENSE`/`LICENSE.txt`/`LICENSE.md`/`COPYING` |

  Then: "For each component that already exists you'll be asked whether to keep it, update it, or replace it." (or,
  when `on-existing` arrived in `args` with `keep`/`update`/`replace`, say that value will be applied to every
  existing component without asking).

`mode` itself stays as detected above, but **any** owned artifact present — not just the build manifest — means
the run is an update for that component, so even a `mode: new` run lists in the announcement any stray component it
did find (e.g. a GitHub-created `README.md`/`LICENSE`) as present. Keep the inventory: Step 5 repeats it with the
action actually taken per component.

## Step 2 — Ask the project type

Skip this step entirely when `project-type` was already resolved — either supplied via `args`, or detected in
Step 1 and confirmed by the user (offered as that option's first entry, labeled "(detected)").

Otherwise resolve it with `AskUserQuestion`, in up to six rounds (the tool caps each question at four options,
so each round offers up to three concrete project types plus one explicit escape hatch). Rounds 1–5 end with a fourth
option, **"Something in the next group"**, whose label names the theme the next round covers (e.g. "Something in
the next group (mobile/native)") — picking it moves on to the next round without forcing a pick. Round 6 is the
last round, so its fourth option is instead **"None of these"**: choosing it means `project-type: other` — ask the
user to describe the stack in one line, and report per Step 5 that this catalog has no bootstrap orchestrator for
it (the same outcome as a detected `dotnet`/`other` in Step 1) rather than guessing a delegated skill to force it
into. If the user free-types a type from a later round via the tool's built-in *Other* choice, accept it directly
instead of walking them through the remaining rounds.

- **Round 1 — "JVM services & libraries"**: Java library / Spring Boot service ("Java or Kotlin, optional Hilla
  frontend") / Quarkus service ("Java or Kotlin") / Something in the next group (web & Node).
- **Round 2 — "Web & Node"** (only if Round 1 ended on the escape hatch): TypeScript/npm library / Web app ("React,
  Next.js, or Angular") / NestJS backend service / Something in the next group (PHP).
- **Round 3 — "PHP"** (only if Round 2 ended on the escape hatch): Laravel application / WordPress plugin or block
  theme / PrestaShop module / Something in the next group (Python).
- **Round 4 — "Python"** (only if Round 3 ended on the escape hatch): FastAPI service ("FastAPI + SQLModel/SQLAlchemy,
  Alembic, container image") / Django project ("Django + DRF or Ninja, PostgreSQL, container image") / Something in
  the next group (mobile & Apple).
- **Round 5 — "Mobile & Apple"** (only if Round 4 ended on the escape hatch): Android ("library or app") / Apple
  ("Swift library or iOS/iPadOS/macOS/watchOS app") / Cross-platform mobile app ("React Native, Kotlin Multiplatform, or Ionic") /
  Something in the next group (desktop & command line).
- **Round 6 — "Desktop & command line"** (only if Round 5 ended on the escape hatch): macOS desktop app ("native Mac app in Swift —
  SwiftUI or AppKit, MVVM or MVC; notarized DMG or Mac App Store") / Windows desktop app ("C# on .NET 10 — WPF,
  WinUI 3 or Windows Forms, MVVM or MVC; MSIX, WinGet or Microsoft Store") / Command-line tool ("a native,
  agent-friendly CLI — Rust, Go, Swift or C#/.NET — with optional terminal UI; release binaries, Homebrew, crates.io,
  WinGet, NuGet") / None of these. (A Mac app that also
  targets iOS/iPadOS/watchOS is Round 5's *Apple → Apple app*, not this round's macOS option.)

Five options bundle two to four types, so picking one asks **one** bounded follow-up `AskUserQuestion` right away
— these are part of resolving `project-type` (they decide the delegated orchestrator's `flavor`, and whether Step 3
asks `publish` or `distribution`), so this front door asks them rather than the orchestrator:

- **Web app** → *React (Vite single-page app)* / *Next.js (server rendering or static export)* / *Angular (Angular
  CLI)*.
- **WordPress plugin or block theme** → *Plugin* / *Block theme*.
- **Android** → *Library* / *App*.
- **Apple** → *Swift library (SwiftPM package)* / *Apple app*.
- **Cross-platform mobile app** → *React Native (Expo or bare CLI/Metro)* / *Kotlin Multiplatform (shared Kotlin
  for Android + iOS)* / *Ionic (Capacitor)*. React Native's toolchain is asked in Step 3 (question 8) because it
  changes the CI cost picture; Kotlin Multiplatform's UI approach (`ui: compose|native`) is a stack-shape question
  left to `iru-setup-kmp-repository`.
- **Command-line tool** → *Rust (clap; optional Ratatui terminal UI)* / *Go (Cobra; optional Bubble Tea terminal
  UI)* / *Swift (swift-argument-parser; macOS + Linux)* / *C# / .NET (System.CommandLine; Native AOT, .NET tool)* —
  this answer is the project type's language (`cli-tool (<language>)`), forwarded as `language`. Pre-fill it from
  Step 1's detected `cli-tool (…)` parenthetical when present. The terminal UI (`ui: none|tui`) and the package
  channels are asked by `iru-setup-cli-repository`.

**Spring Boot service** and **Quarkus service** deliberately get **no** follow-up here: their language (Java or
Kotlin), build tool (Maven or Gradle), Quarkus layout (single module or hexagonal), and Spring Boot `frontend`
(none or Hilla) are stack-shape questions that `iru-setup-java-springboot` (Step 3/3b) and
`iru-setup-quarkus-repository` (Step 1) already ask, with richer explanations and their own validation (e.g. Java
Spring Boot is Maven-only) — asking them here too would double-ask. The final `project-type` (e.g.
`kotlin-springboot-hilla`, `java-quarkus`) is whatever those answers make it; Step 5 reports it from the delegated
run. The same rule holds for every other stack-shape key (`orm`/`database` for NestJS, `output`/`e2e` for Next.js,
`php-version` for PHP, `database`/`orm`/`api`/`python-version` for Python): this front door forwards them only when
Step 0's `args` or Step 1's detection supplied them, and otherwise leaves them to the orchestrator —
`iru-setup-python-repository` asks all four itself.

| Option (→ follow-up) | `project-type` key | Delegated skill | `flavor`/extra arg |
|---|---|---|---|
| Java library | `java-library` | `iru-setup-java-library-repository` | — |
| Spring Boot service | `java-springboot` / `java-springboot-hilla` / `kotlin-springboot` / `kotlin-springboot-hilla` (from the orchestrator's answers) | `iru-setup-java-springboot` | `language`/`build-tool`/`frontend` only when detected or in `args` |
| Quarkus service | `java-quarkus` / `kotlin-quarkus` (from the orchestrator's answer) | `iru-setup-quarkus-repository` | `language` only when detected or in `args` (`build-tool`/`layout` only from `args`) |
| TypeScript/npm library | `typescript-library` | `iru-setup-typescript-repository` | `flavor: library` |
| Web app → React | `react-web` | `iru-setup-typescript-repository` | `flavor: react` |
| Web app → Next.js | `nextjs` | `iru-setup-typescript-repository` | `flavor: nextjs` |
| Web app → Angular | `angular-web` | `iru-setup-typescript-repository` | `flavor: angular` |
| NestJS backend service | `nestjs` | `iru-setup-typescript-repository` | `flavor: nestjs` |
| Laravel application | `php-laravel` | `iru-setup-php-repository` | `flavor: laravel` |
| WordPress → Plugin | `php-wordpress-plugin` | `iru-setup-php-repository` | `flavor: wordpress-plugin` |
| WordPress → Block theme | `php-wordpress-theme` | `iru-setup-php-repository` | `flavor: wordpress-theme` |
| PrestaShop module | `php-prestashop-module` | `iru-setup-php-repository` | `flavor: prestashop-module` |
| FastAPI service | `python-fastapi` | `iru-setup-python-repository` | `flavor: fastapi` |
| Django project | `python-django` | `iru-setup-python-repository` | `flavor: django` |
| Android → Library | `android-library` | `iru-setup-android-repository` | `flavor: library` |
| Android → App | `android-app` | `iru-setup-android-repository` | `flavor: app` |
| Apple → Swift library | `swift-library` | `iru-setup-swift-repository` | `flavor: library`, `platforms` |
| Apple → Apple app | `apple-app` | `iru-setup-swift-repository` | `flavor: app`, `platforms` |
| Cross-platform → React Native | `react-native-app` | `iru-setup-typescript-repository` | `flavor: react-native`, `toolchain`, `native-builds` (Expo only) |
| Cross-platform → Kotlin Multiplatform | `kmp-app` | `iru-setup-kmp-repository` | `ui` only when detected or in `args` |
| Cross-platform → Ionic | `ionic-app` | `iru-setup-typescript-repository` | `flavor: ionic`, `framework` |
| macOS desktop app | `macos-app` | `iru-setup-macos-repository` | `ui` only when detected or in `args` |
| Windows desktop app | `windows-app` | `iru-setup-windows-repository` | `ui` only when detected or in `args` |
| Command-line tool → Rust / Go / Swift / C# .NET | `cli-tool` (`rust`/`go`/`swift`/`dotnet`) | `iru-setup-cli-repository` | `language`; `ui` only when detected or in `args` |

A user who wants a plain Composer PHP library (no Laravel/WordPress/PrestaShop) ends on "None of these" or types
it via *Other* — handle it like a detected `php-library` in Step 1 (no orchestrator; point at the individually
runnable PHP gate and repository-file skills). Likewise a plain Python package (no FastAPI/Django) is handled like
a detected `python-library`.

## Step 3 — Ask the shared inputs once

Ask only what the resolved `project-type` actually needs, skipping anything already resolved by `args` or by
Step 1's detection. Every question here uses `AskUserQuestion` (header ≤ 12 characters, 2–4 options, recommended
option first and labeled "(Recommended)") and follows this catalog's shared open-source- and visibility-driven
convention (see any of the twelve delegated orchestrators' own Step 0–4 for the identical wording this mirrors). Ask
them in the order below — `visibility` and `ci` change the recommendations of everything after them.

1. **open-source** — is this repository open source? Yes / No, asked directly with no default. Drives the
   recommended defaults for every question below.
2. **visibility** — the GitHub repository's visibility, resolved (not necessarily asked) in this order:
   1. `args` supplied it — use it.
   2. The repository has a GitHub remote (`git remote get-url origin` matches `github.com`) and `gh` is available:
      run `gh repo view --json visibility -q .visibility` (returns `PUBLIC`/`PRIVATE`/`INTERNAL`; lowercase it) and
      tell the user the detected value.
   3. Otherwise (no remote yet, `gh` unavailable/unauthenticated, or not GitHub): ask with `AskUserQuestion` —
      **Public** / **Private** — recommending **Public** when `open-source: yes`, otherwise **Private**.
   4. Consistency check: `open-source: yes` with `visibility: private|internal` is contradictory — warn and ask the
      user which one is right (an open-source project's repository is normally public; a private repository
      forfeits the free-for-public-repositories pricing stated below). `internal` behaves like `private` for every
      cost decision in this step.

   Every cost statement in questions 3–6 below is **per GitHub's current pricing** (verified October 2026 against
   docs.github.com) — say so, and tell the user to double-check their own plan:
   - **Actions minutes**: standard GitHub-hosted runners are free for public repositories. Private/internal
     repositories consume the account's included minutes — 2,000/month on GitHub Free, 3,000 on Pro and Team, 50,000
     on Enterprise Cloud — then are billed per minute. macOS runner minutes cost roughly 10× Linux minutes, Windows
     roughly 1.7× (per-minute rates: Linux 2-core $0.006, Windows 2-core $0.010, macOS $0.062). Dependabot
     version/security update runs on standard hosted runners are free.
   - **SonarCloud (SonarQube Cloud)** is free for public/open-source projects; a private project needs a paid plan.
     Self-hosted SonarQube Community Build is free, but you run the server.
   - **GitHub Pages** is available for public repositories on every plan; for private/internal repositories it
     requires GitHub Pro, Team, or Enterprise Cloud (not GitHub Free), and a Pages site published from a private
     repository is **publicly accessible on the internet** unless the organization is on Enterprise Cloud and
     publishes it with private access control.
3. **ci** — "Generate GitHub Actions workflows (CI/CD) for this repository?"
   - **Public**: recommend **Yes** — standard runners are free for public repositories.
   - **Private/internal**: still offer **Yes** first, but state the included-minutes budget for their plan, and —
     when the resolved type builds on macOS (`swift-library`, `apple-app`, `kmp-app` — its iOS framework, Kotlin/Native
     iOS tests, and the `iosApp` host build always need a macOS runner —, `react-native-app` with `toolchain: metro`
     (an iOS `xcodebuild` job) or `toolchain: expo` + `native-builds: local` — question 8 hasn't been asked yet, so
     state it conditionally unless `args` resolved it —, `ionic-app` iOS builds, and `macos-app` — every build, test,
     notarization and DocC job) — the ~10× macOS multiplier, estimating plainly that a few dozen macOS builds a
     month can exhaust 2,000 included minutes; for `windows-app`, the ~1.7× Windows multiplier (its pipeline keeps
     the Core tests, coverage and docs on Linux and uses Windows for the app build, UI tests and packaging); for
     `cli-tool`, that lint, tests, coverage and docs run on Linux, while the macOS (~10×) and Windows (~1.7×) test legs
     and release builds are scheduled by `iru-setup-cli-repository`'s own `cross-os-ci` question. Offer **No** as "no workflows — build, test, and
     release locally (re-run the stack's `-github-workflows` skill later to add them)".
   - `ci: no` means the delegated orchestrator skips its workflows step entirely (no `.github/workflows/*`, no
     `security.yml`, no `.github/dependabot.yml`, no sync script) — and with it the shared security block
     (Dependabot, dependency-review, CodeQL, OSV-Scanner, gitleaks); for a Spring Boot service (any
     `*-springboot*` type) that also means no deploy/undeploy workflows, so deployment has to be done manually, and
     for every type with a release-time image or package (Quarkus, NestJS, Next.js, PHP flavors, Python flavors) no `release.yml`.
     Questions 5 and 6 are then not asked.
4. **sonar** — "Configure SonarCloud / SonarQube and send CI analysis and coverage reports to it?"
   `cloud`/`self-hosted`/`none`. Recommend **`cloud`** only when the repository is **public AND open source**.
   Otherwise state plainly that SonarCloud is free only for public/open-source projects (a private project needs a
   paid plan) and recommend **`none`**, offering **self-hosted SonarQube** as the second option. When `ci: no`, say
   plainly that nothing would send reports automatically — analysis would only run when someone runs the scanner
   manually with a token — and recommend **`none`**; if the user still picks `cloud`/`self-hosted`, the delegated
   skills configure only the build-side Sonar properties/plugin and Step 5 reports that no CI step sends reports.
   When `cloud`/`self-hosted` is chosen, also collect `sonar-organization`/`sonar-project-key` (cloud) or
   `sonar-host-url`/`sonar-project-key` (self-hosted), the same way every delegated orchestrator's own Sonar
   question does.
5. **ci-tests** (only when `ci: yes`) — "Which tests should CI run?" Name the concrete test kinds for the resolved
   type in the option descriptions: Maven Failsafe `*IT` integration tests (`java-library`); Failsafe (Maven) or
   the `integrationTest` task (Gradle) running Testcontainers/Docker integration tests (every `*-springboot*` type);
   `@QuarkusTest` with Dev Services containers plus `@QuarkusIntegrationTest` against the packaged jar (Quarkus);
   the `test:e2e` suite, with a Testcontainers database when an ORM is chosen (`nestjs`); Playwright against a
   production build (`nextjs`, when it has an e2e suite); the database-backed integration suite via Sail compose
   (`php-laravel`), the `WP_UnitTestCase` integration suite under `wp-env`/Docker (`php-wordpress-plugin`/
   `php-wordpress-theme`), and the optional real-shop Docker integration suite (`php-prestashop-module`); the pytest
   `integration` tier against PostgreSQL started by testcontainers/Docker, plus Alembic upgrade/downgrade checks for
   FastAPI (`python-fastapi`/`python-django`, only with `database: postgresql` — SQLite has no integration tier;
   container image pulls make `full` noticeably costlier on a private repository); emulator-backed
   instrumented tests (`android-library`/`android-app` — the emulator job runs on Linux with KVM, and emulator time
   is billed minutes on a private repository); Playwright e2e (`react-web`/`angular-web`, and any e2e suite of
   `ionic-app`); Maestro flows on an Android emulator (`react-native-app`, either toolchain — emulator minutes are
   billed on a private repository); Kotlin/Native iOS simulator tests plus the `iosApp` XCTest suite on macOS
   (`kmp-app` — every macOS minute ~10×; `unit` keeps CI to the shared JVM/Android host tests plus an iOS compile
   check); XCUITest UI tests on every selected destination (`apple-app`, every macOS minute
   ~10×); XCUITest UI tests that launch the app on the macOS runner's desktop (`macos-app`, ~10×); FlaUI desktop UI
   tests on a Windows runner (`windows-app`, ~1.7×; `unit` keeps CI to the Core tests on Linux plus a Windows build);
   an integration-test target if one exists (`swift-library`, `typescript-library`); for `cli-tool`, `unit` already
   runs the end-to-end tests of the real binary on Linux (they need no containers), and `full` adds any
   container-backed tests plus a smoke test of every release-mode target binary (the macOS/Windows test legs are
   scheduled separately by `iru-setup-cli-repository`'s `cross-os-ci` question).
   - **`unit`** — "Unit tests only (cheaper: fewer minutes, faster feedback). Integration / instrumentation / e2e
     tests stay local." Recommend for private/internal repositories.
   - **`full`** — "Unit + integration / instrumentation / e2e tests (complete verification, uses considerably more
     minutes — emulators, containers, browsers, simulators)." Recommend for public repositories.
6. **pages** (only when `ci: yes` — every delegated pipeline builds an Antora docs site that its workflows can
   publish to GitHub Pages):
   - **Public**: default **`yes`** without asking (Step 5 states it).
   - **Private/internal**: ask — **No (Recommended)** ("CI still builds the docs and uploads them as a workflow
     artifact; nothing is published") vs **Yes** ("requires GitHub Pro/Team/Enterprise Cloud; the site will be
     PUBLIC on the internet unless you're on Enterprise Cloud with private Pages access control").
7. **publish** or **distribution**, depending on whether the resolved type is a library or an app-shaped
   deliverable — never ask both, and skip entirely for Spring Boot services (a service isn't published or
   distributed the way a library or an installable app is, and `iru-setup-java-springboot` accepts neither key —
   deployment is its own deploy workflow), for `react-web`/`angular-web` (`iru-setup-typescript-repository`
   accepts neither key for these two flavors — a web app is deployed by its own CI job, not published or
   distributed), and for `nextjs` (its `distribution` depends on the `output` mode — a static export forces
   `distribution: none` — which `iru-setup-typescript-repository` asks first, so leave both to it; forward
   `distribution` only when it arrived via `args`):
   - **`publish`** — library types (`java-library`, `typescript-library`, `android-library`, `swift-library`):
     does this get published for other projects to depend on (Maven Central / npm / the Swift Package Index,
     per the type)? Default **Yes** when open source; otherwise ask with **No** recommended — these registries are
     for redistributable artifacts, which usually isn't the point of closed-source code.
   - **`distribution`** — app types (`android-app`, `apple-app`, `react-native-app`, `ionic-app`, `kmp-app`,
     `macos-app`, `windows-app`, `cli-tool`): `none`/`internal`/`store`. Default **`store`** only when open source; otherwise ask
     with **`internal`** recommended, `none` as the local-install-only alternative. The two desktop types read the
     values differently — say so in the option descriptions, and default them to **`internal`** even when open
     source (a GitHub Release is the natural public download for a desktop app):
     - **`macos-app`** — `internal` = a Developer ID–signed, notarized and stapled DMG attached to a GitHub Release;
       `store` = an App Store Connect upload (TestFlight / Mac App Store review; the App Sandbox is mandatory). Both
       need a paid Apple Developer Program membership.
     - **`windows-app`** — `internal` = self-contained zips per architecture plus, when signed, an MSIX and an
       `.appinstaller` file on GitHub Releases (WinGet optional); `store` = an MSIX submission to the Microsoft Store
       through Partner Center. The signing method (Azure Artifact Signing / a `.pfx` certificate / none) and WinGet
       are asked by `iru-setup-windows-repository`.
     - **`cli-tool`** (defaults like the mobile types: **`store`** when open source) — `internal` = native binaries
       for every target as `tar.gz`/`zip` archives with a `SHA256SUMS` file and build-provenance attestations on
       each GitHub Release; `store` = the same plus package channels (crates.io, Homebrew, Scoop, WinGet, a NuGet
       .NET tool — per language; `iru-setup-cli-repository` asks which `channels`). The service, PHP, and Python types use the same key with
     their own value sets and meanings — offer only the values the delegated orchestrator accepts:
     - **Quarkus service** — `registry`/`none`: **Registry (Recommended)** = a container image pushed to GHCR when
       a release is published (free for public repositories; storage/transfer quotas for private ones); **None** =
       CI builds and tests only, no `release.yml`. The image builder (Jib or Dockerfile) is asked downstream.
     - **`nestjs`** — `internal`/`none` (no store): **Internal (Recommended)** = the multi-stage, non-root
       `Dockerfile` image pushed to GHCR on release; **None** = the `Dockerfile` is still written for local use but
       no `release.yml`.
     - **`php-laravel`** — `none`/`internal` (never `store`): **None (Recommended)** = CI builds and tests only;
       **Internal** = container image to GHCR on release.
     - **`php-wordpress-plugin`/`php-wordpress-theme`** — `none`/`internal`/`store`: `internal` = an installable
       zip (from `.distignore`, `composer install --no-dev`) attached to the GitHub Release; `store` = that zip plus
       deployment to the WordPress.org plugin/theme directory (SVN; needs a directory account, an approved slug,
       and a GPL-compatible license). Default **`store`** only when open source, otherwise **`none`**.
     - **`php-prestashop-module`** — `none`/`internal`/`store`: `internal` = the installable module zip attached to
       the GitHub Release; `store` = the same zip plus instructions for uploading it to the PrestaShop Addons
       marketplace by hand (Addons has no upload API). Default **`none`**.
     - **`python-fastapi`/`python-django`** — `none`/`internal`/`store` (never `publish` — an application has no PyPI
       publishing; the multi-stage, non-root `Dockerfile` is always written): `none` = CI builds and tests only, no
       `release.yml`; `internal` = on release, the image is pushed to GHCR as a **private** package (counts against
       the account's Packages quota); `store` = the same image as a **public** GHCR package. Default **`store`** when
       open source **and** public; otherwise **`internal`** recommended, `none` second.
8. **Conditional, per resolved type**:
   - **Apple app / Swift library** — Apple platforms (`AskUserQuestion`, multi-select, at least one required):
     `ios` / `ipados` / `macos` / `watchos`. Pre-fill from Step 1's detected `apple-app (…)` parenthetical when
     present. For a **Swift library only**, follow up with a second multi-select question — "Also target tvOS /
     visionOS / Linux?" with options `tvos` / `visionos` / `linux` (none required) — and append every selected
     value to `platforms`. This follow-up is necessary because Step 4 always forwards `platforms` pre-resolved,
     and `iru-setup-swift-repository`'s own Step 0 skips any question whose key was supplied — so a library's
     extra platforms can only reach `Package.swift` if this front door collects them itself. For an **Apple app**,
     ask a narrower follow-up instead — "Also target visionOS?" (`visionos` / none) — for the same reason
     (`iru-setup-apple-app` accepts `visionos` but not `tvos` or `linux`). Never offer `tvos`/`linux` for an app. If
     the user picks `macos` alone for an Apple app, suggest the macOS desktop app type (Round 6) instead —
     `iru-setup-macos-repository` covers AppKit, MVC and Developer ID/DMG distribution.
   - **Ionic app** — framework (`AskUserQuestion`, two options): **Angular** or **React**. Pre-fill from Step 1's
     detected `ionic-app (…)` parenthetical when present.
   - **React Native app** — toolchain (`AskUserQuestion`, two options; pre-fill from Step 1's detected
     `react-native-app (…)` parenthetical when present): **Expo (Recommended)** — the Expo framework (Expo Router,
     config plugins, no committed native projects, EAS cloud builds or local prebuild) — or **Metro (bare React
     Native CLI)** — committed `android/`/`ios/` native projects you own, React Navigation, CocoaPods, and an iOS
     CI job on macOS. (Expo also bundles with Metro; the choice is about who owns the native projects.) Then,
     **only for `toolchain: expo`**, native-builds (`AskUserQuestion`, two options, default **`eas`**): does CI
     build the iOS/Android binaries via cloud builds (`eas`), or does it need a full local native toolchain
     (`local`)? Never ask or forward `native-builds` for `toolchain: metro`.
   - **Command-line tool** — nothing here beyond the language Step 2's follow-up resolved: `ui` (terminal UI or
     commands only), `cross-os-ci`, `channels`/`homebrew-tap`, `branching` and the tool's identity are asked by
     `iru-setup-cli-repository`.
   - **macOS / Windows desktop app** — nothing here: `ui` (SwiftUI vs. AppKit; WPF vs. WinUI 3 vs. Windows Forms),
     `architecture` (MVVM vs. MVC, offered only where both are valid), the app identity and the platform-specific
     release questions (sandbox; signing, WinGet) are asked by `iru-setup-macos-repository` /
     `iru-setup-windows-repository`.
   - **Kotlin Multiplatform app** — nothing here: `ui` (`compose` shared Compose Multiplatform UI vs. `native`
     Jetpack Compose + SwiftUI) and the app identity are asked by `iru-setup-kmp-repository`.
   - **Spring Boot / Quarkus / NestJS / Next.js / PHP / Python** — nothing here. Their stack-shape questions are asked by
     the delegated orchestrator, never by this front door (see Step 2): `language`, `build-tool`, and `frontend` by
     `iru-setup-java-springboot`; `language`, `build-tool`, `layout`, and `java-version` by
     `iru-setup-quarkus-repository` (which skips the first three in `mode: existing`, detecting them from the
     build); `orm`/`database` (NestJS) and `output`/`e2e` (Next.js) by `iru-setup-typescript-repository`;
     `php-version` (the PHP floor) and the identity/slug/license questions by `iru-setup-php-repository`;
     `python-version`, `database`, `orm` (FastAPI), `api` (Django), and the identity/license questions by
     `iru-setup-python-repository`. Whatever
     Step 1 detected or `args` supplied for these keys is forwarded in Step 4, so the orchestrator confirms it
     instead of asking again — and nothing is ever asked twice.

9. **accessibility** (only for a resolved type with a user interface: `react-web`, `angular-web`, `nextjs`,
   `ionic-app`, `react-native-app`, `android-app`, `android-library` (its sample app), `apple-app`, `macos-app`,
   `kmp-app`, `windows-app`, `php-laravel`, `php-wordpress-plugin`, `php-wordpress-theme`, `php-prestashop-module`,
   `python-django`, and the `*-springboot-hilla` types; for Spring Boot without a detected Hilla frontend and for
   `cli-tool` — whose `frontend`/`ui` the orchestrator asks — leave it to the orchestrator) — "Run automated
   accessibility checks in the UI tests?" Every UI scaffold follows the catalog's UI contract: composed
   components with explicit inputs and events, virtualized lists, UI tests across states, left-to-right and
   right-to-left, light and dark, screenshots reused by the Antora docs, and automated accessibility checks
   (axe-core on the web, Android's Accessibility Test Framework, Xcode's accessibility audit, Axe.Windows).
   Options: **Enforce (Recommended)** — "violations fail the UI tests"; **Report only** — "violations are listed in
   test reports but never fail the build"; **Off** — "no automated checks (accessible coding defaults still
   apply)". The choice is written to `.ui-quality.yml` at the repository root, where the coding and test skills
   read it; it can be changed there later by hand.

`integration-branch`, `stable-branch`, `license`, `developer-name`, `developer-email`, and `organization-url` are
**never actively asked here** — this front door only forwards them when they arrived via its own `args`
(`iru-setup-quarkus-repository`, `iru-setup-typescript-repository`, `iru-setup-php-repository`,
`iru-setup-python-repository`, `iru-setup-android-repository`, `iru-setup-swift-repository`, `iru-setup-kmp-repository`,
`iru-setup-macos-repository`, `iru-setup-windows-repository`, and `iru-setup-cli-repository` all accept these as `args` keys and would
otherwise ask their own equivalent question; `iru-setup-java-library-repository` and `iru-setup-java-springboot`
accept none of them and always ask their own identity/branch questions directly
regardless of what this skill would pass). Asking them here would either duplicate a question the delegated skill
asks anyway or collect a value the delegated skill has no `args` key to receive — so let each one ask.

## Step 4 — Delegate to the stack orchestrator

**Before writing this step's `Agent(...)` call**, confirm the exact `args` keys and values the target skill
actually accepts by reading its `SKILL.md` frontmatter description and Step 0 on disk — never rely on memory of
the table above once actually invoking:

- `.claude/skills/iru-setup-java-library-repository/SKILL.md`
- `.claude/skills/iru-setup-java-springboot/SKILL.md`
- `.claude/skills/iru-setup-quarkus-repository/SKILL.md`
- `.claude/skills/iru-setup-typescript-repository/SKILL.md`
- `.claude/skills/iru-setup-php-repository/SKILL.md`
- `.claude/skills/iru-setup-python-repository/SKILL.md`
- `.claude/skills/iru-setup-android-repository/SKILL.md`
- `.claude/skills/iru-setup-swift-repository/SKILL.md`
- `.claude/skills/iru-setup-kmp-repository/SKILL.md`
- `.claude/skills/iru-setup-macos-repository/SKILL.md`
- `.claude/skills/iru-setup-windows-repository/SKILL.md`
- `.claude/skills/iru-setup-cli-repository/SKILL.md`
- `.claude/skills/iru-explore/SKILL.md` Step 7, for the `## Tech stack` report shape Step 1 already relied on.
- `.claude/agents/iru-isolated-skill-executor.md`, for how it runs a named skill and reports back.

Then delegate via `iru-isolated-skill-executor`, exactly one of the twelve, always passing `mode` and every shared
input Step 3 resolved (omitting any key the target skill's own Step 0 doesn't recognize — never send an invented
key). All twelve orchestrators accept the cost/CI keys `visibility`, `ci`, `ci-tests`, and `pages`, plus
`on-existing`: always send `visibility` and `ci`; send `ci-tests` and `pages` only when `ci: yes` (they're
meaningless otherwise); send `on-existing` **only** when it arrived via this skill's own `args` — never invent a
value, so an interactive run leaves every component free to warn and ask per pre-existing artifact:

```
# project-type: android-app
Agent({
  description: "Run iru-setup-android-repository",
  subagent_type: "iru-isolated-skill-executor",
  prompt: "Invoke Skill({skill: \"iru-setup-android-repository\", args: \"flavor: app\\nmode: <mode>\\n
    open-source: <open-source>\\nvisibility: <visibility>\\nci: <ci>\\nci-tests: <..., if ci: yes>\\n
    pages: <..., if ci: yes>\\non-existing: <..., only if supplied via args>\\ndistribution: <distribution>\\n
    sonar: <sonar>\\nsonar-organization: <..., if set>\\nsonar-project-key: <..., if set>\\n
    sonar-host-url: <..., if set>\\nintegration-branch: <..., if set>\\nstable-branch: <..., if set>\\n
    license: <..., if set>\\ndeveloper-name: <..., if set>\\ndeveloper-email: <..., if set>\\n
    organization-url: <..., if set>\"}).
    Report back: the setup mode it announced, and per component (scaffold/build manifest, Antora docs, .gitignore,
    each workflow file, CHANGELOG.md, README.md) the action actually taken — created / updated / replaced / kept as
    is / skipped (ci: no) — and whether the user chose to stop at any point; every mismatch it reported between a
    kept file and this run's choices; the full required-secrets/settings table it produced; and any open gap it
    flagged.",
  run_in_background: false
})
```

The other orchestrators follow the same shape — one delegation, one `iru-isolated-skill-executor` call —
with only the skill name and `args` changed. Every list below implicitly includes `visibility`, `ci`, `ci-tests`
and `pages` (when `ci: yes`), and `on-existing` (when supplied via `args`), per the rule above:

- **`java-library`** → `iru-setup-java-library-repository`, `args`: `mode`, `open-source`, the cost/CI keys,
  `publish`, `sonar` (+ detail keys) only — its own Step 0 recognizes nothing else, so `integration-branch`/
  `license`/developer identity are never sent here even if the user supplied them via this skill's own `args`.
- **Spring Boot** (`java-springboot`, `java-springboot-hilla`, `kotlin-springboot`, `kotlin-springboot-hilla`, or
  the manual "Spring Boot service" pick) → `iru-setup-java-springboot`, `args`: `mode`, `open-source`, the cost/CI
  keys, `sonar` (+ detail keys), and `language`/`build-tool`/`frontend` **only** when Step 1's detection pre-set
  them or this skill's own `args` supplied them (otherwise omitted, so its Step 3/3b asks them) — no
  `publish`/`distribution`/branch/license/developer keys exist on this skill either. It validates the pair itself
  (Java is Maven-only) and records `language`/`buildTool`/`ci`/`ci-tests`/`pages` in its `springboot-stack.yml`
  manifest for its sub-skills.
- **Quarkus** (`java-quarkus`, `kotlin-quarkus`, or the manual "Quarkus service" pick) →
  `iru-setup-quarkus-repository`, `args`: `mode`, `open-source`, the cost/CI keys, `distribution`
  (`registry`/`none`), `sonar` (+ detail keys), `language` when detected or supplied, `build-tool`/`layout`/
  `java-version` only when supplied via `args`, plus `integration-branch`/`stable-branch`/`license`/
  `developer-name`/`developer-email`/`organization-url` and any identity key (`group-id`, `artifact-id`, ...) when
  this skill's own `args` supplied them.
- **`typescript-library`** / **`react-web`** / **`nextjs`** / **`angular-web`** / **`nestjs`** /
  **`react-native-app`** / **`ionic-app`** → `iru-setup-typescript-repository`, `args`: `flavor`
  (`library`/`react`/`nextjs`/`angular`/`nestjs`/`react-native`/`ionic`), `mode`, `open-source`, the cost/CI keys,
  `publish` (library only), `distribution` (react-native/ionic/nestjs; nextjs only when supplied via `args`),
  `sonar` (+ detail keys), `toolchain` (react-native only), `native-builds` (react-native with `toolchain: expo`
  only), `framework` (ionic only), the nestjs/nextjs shape
  keys (`orm`, `database`, `module-system`, `http` / `output`, `e2e`, `router`, `cache-components`, `styling`) only
  when supplied via `args`, plus `integration-branch`/`stable-branch`/`license`/`developer-name`/
  `developer-email`/`organization-url` when this skill's own `args` supplied them.
- **`php-laravel`** / **`php-wordpress-plugin`** / **`php-wordpress-theme`** / **`php-prestashop-module`** →
  `iru-setup-php-repository`, `args`: `flavor` (`laravel`/`wordpress-plugin`/`wordpress-theme`/
  `prestashop-module`), `mode`, `open-source`, the cost/CI keys, `distribution` (with the flavor's value set from
  Step 3), `sonar` (+ detail keys), `php-version` only when supplied via `args`, plus the same pass-through
  branch/license/developer keys and identity keys (`name`, `slug`, `vendor`, `namespace`, `description`) when
  supplied. Never send `publish` — it ignores it.
- **`python-fastapi`** / **`python-django`** → `iru-setup-python-repository`, `args`: `flavor` (`fastapi`/`django`),
  `mode`, `open-source`, the cost/CI keys, `distribution` (`none`/`internal`/`store`, per Step 3), `sonar` (+ detail
  keys), `python-version`/`database`/`orm` (FastAPI)/`api` (Django) only when supplied via `args`, plus the same
  pass-through `integration-branch`/`stable-branch`/`license`/`developer-name`/`developer-email`/`organization-url`
  and identity keys (`name`, `package`, `description`) when supplied. Never send `publish` — it ignores it.
- **`android-library`** / **`android-app`** → `iru-setup-android-repository`, `args`: `flavor` (`library`/`app`),
  `mode`, `open-source`, the cost/CI keys, `publish` (library) / `distribution` (app), `sonar` (+ detail keys),
  plus the same pass-through branch/license/developer keys when supplied (the `android-app` example above).
- **`swift-library`** / **`apple-app`** → `iru-setup-swift-repository`, `args`: `flavor` (`library`/`app`),
  `mode`, `platforms` (comma-separated), `open-source`, the cost/CI keys, `publish` (library) / `distribution`
  (app), `sonar` (+ detail keys), `ui`/`architecture` (app only, when supplied via `args` or detected on
  `iru-explore`'s `Build & layout:` line in Step 1 — otherwise omitted, so `iru-setup-swift-repository` detects
  and confirms them in `mode: existing`, or asks them fresh in `mode: new`), plus the same pass-through branch/license/developer keys when supplied. Neither
  `flavor` needs `branching` sent — `iru-setup-swift-repository` asks that itself, as it isn't one of this skill's
  `args` keys.
- **`kmp-app`** → `iru-setup-kmp-repository`, `args`: `mode`, `open-source`, the cost/CI keys, `distribution`,
  `sonar` (+ detail keys), `ui` only when Step 1 detected it or `args` supplied it, plus the same pass-through
  branch/license/developer keys and identity keys (`app-name`, `application-id`, `bundle-id`, `namespace`) when
  supplied. Never send `publish` or `flavor` — it scaffolds apps only.
- **`macos-app`** → `iru-setup-macos-repository`, `args`: `mode`, `open-source`, the cost/CI keys, `distribution`,
  `sonar` (+ detail keys), `ui` only when Step 1 detected it or `args` supplied it, `architecture`/`macos-ci`/
  `runner`/`min-macos`/`sandbox`/`category` only when supplied via `args`, plus the same pass-through
  branch/license/developer keys and identity keys (`app-name`, `bundle-id`, `team-id`) when supplied. Never send
  `publish`, `flavor` or `platforms` — it scaffolds macOS-only apps.
- **`windows-app`** → `iru-setup-windows-repository`, `args`: `mode`, `open-source`, the cost/CI keys,
  `distribution`, `sonar` (+ detail keys), `ui` only when Step 1 detected it or `args` supplied it,
  `architecture`/`signing`/`winget`/`msix`/`ui-tests`/`rids` only when supplied via `args`, plus the same
  pass-through branch/license/developer keys and identity keys (`app-name`, `display-name`, `publisher`,
  `publisher-display-name`, `package-name`) when supplied. Never send `publish` or `flavor`.
- **`cli-tool`** → `iru-setup-cli-repository`, `args`: `language`, `mode`, `open-source`, the cost/CI keys,
  `distribution`, `sonar` (+ detail keys), `ui` only when Step 1 detected it or `args` supplied it,
  `cross-os-ci`/`channels`/`homebrew-tap`/`branching` only when supplied via `args`, plus the same pass-through
  branch/license/developer keys and identity keys (`bin-name`, `description`, `owner`, `crate-name`, `msrv`,
  `module-path`, `go-version`, `package-name`, `swift-version`, `platforms`, `tool-name`, `package-id`) when
  supplied. Never send `publish` or `flavor`.

**`accessibility`**: send it, when Step 3 resolved it (or `args` supplied it), to every orchestrator above whose
on-disk Step 0 recognizes it — `iru-setup-typescript-repository` (UI flavors), `iru-setup-php-repository`,
`iru-setup-python-repository` (`django`), `iru-setup-android-repository`, `iru-setup-swift-repository` (`app`),
`iru-setup-kmp-repository`, `iru-setup-macos-repository`, `iru-setup-windows-repository`,
`iru-setup-cli-repository` (it applies it only for `ui: tui`) and `iru-setup-java-springboot` (it applies it only
for `frontend: hilla`) — and never to a type without a UI.

If the on-disk Step 0 of the target orchestrator turns out **not** to recognize one of the cost/CI keys (e.g. an
older copy of it was installed), don't send that key — instead tell the user the orchestrator will ask that
question itself (or, if it has no such question, that the choice can't be applied by it), and list it in Step 5.

Each delegated orchestrator parses its own `args` (its own Step 0) and asks the user about anything genuinely left
out — its own project identity, its own `mode`-driven survey, `branching`/`generator`/`signing`/toolchain toggles,
the stack-shape questions this front door leaves to it (JVM language/build tool/layout/frontend, NestJS ORM,
Next.js output/e2e, PHP version floor, Python version/database/ORM/API), and (for `java-library`/`java-springboot`) branch/license/developer
identity that this front door never collects.
`AskUserQuestion` surfaces to the user the same way whether invoked directly or from inside the isolated
sub-agent — including each component's own keep/update/replace question for a pre-existing artifact, which this
front door never asks on the components' behalf (so the user is never asked the same question twice). Ask the
executor to report back: the per-component action actually taken (created / updated / replaced / kept as is /
skipped (ci: no)) and any point where the user chose to stop, every mismatch reported between a kept file and this
run's choices, the full required-secrets/settings table the delegated orchestrator produced, and any open gap it
flagged — a short structured summary, not the delegated run's full transcript.

## Step 5 — Report

Summarize for the user:

- The resolved `project-type` (and, for `apple-app`/`ionic-app`/`react-native-app`/`kmp-app`/`macos-app`/
  `windows-app`/`cli-tool`, the language/platforms/framework/toolchain/UI approach — and, for the desktop types, the MVVM/MVC
  architecture the orchestrator reported — that came with it; for a
  Spring Boot or Quarkus service, the language/build tool/layout/frontend the delegated orchestrator reported —
  the final `java-*`/`kotlin-*` key comes from its answers), the
  setup mode restated as in Step 1's announcement ("set up from scratch" / "updated an existing repository") with
  whether `mode` came from Step 1's survey or an explicit `args`/user answer, and every shared input from Step 3 as
  actually applied (`open-source`, `visibility` and whether it was supplied/detected via `gh`/asked, `ci`,
  `ci-tests`, `pages` — noting when `pages: yes` was defaulted because the repository is public —
  `publish`/`distribution`, `sonar` + detail keys, `accessibility` for a UI type (and that `.ui-quality.yml`
  records it), `on-existing` if supplied, and any conditional flavor-specific input).
- A **per-component table** — the Step 1 inventory's rows, each with what the delegated orchestrator (named
  explicitly) reported doing: **created / updated / replaced / kept as is / skipped (ci: no)** and the file paths
  involved. Reproduce its report rather than re-deriving one, and list under it every mismatch it flagged between a
  kept-as-is file and this run's choices (e.g. a kept `build.yml` that still runs a Sonar step after `sonar: none`,
  still deploys to Pages after `pages: no`, or still runs integration/e2e tests after `ci-tests: unit`).
- **Cost notes**, tied to the resolved `visibility` and stated as per GitHub's current pricing (the user should
  double-check their plan): for a public repository, that standard Actions runners and SonarCloud are free; for a
  private/internal one, the included-minutes budget, the macOS ~10× multiplier when the stack builds on macOS, that
  `ci-tests: full` uses considerably more minutes, that SonarCloud requires a paid plan for a private project when
  `sonar: cloud`, and — when `pages: yes` — that Pages needs Pro/Team/Enterprise Cloud and the site is public unless
  on Enterprise Cloud with private access control (with `pages: no`, the docs are uploaded as a workflow artifact
  instead).
- When `ci: no`: that no workflows were generated, that the shared security block (Dependabot, dependency-review,
  CodeQL, OSV-Scanner, gitleaks) was skipped with them (and, for Spring Boot, the deploy/undeploy workflows), that
  any Sonar configuration is build-side only with no CI step sending reports, and that re-running the stack's
  `-github-workflows` skill (e.g. `/iru-setup-android-github-workflows`, `/iru-setup-python-github-workflows`) adds
  them later.
- Any key Step 4 couldn't forward because the target orchestrator's on-disk Step 0 didn't recognize it.
- One **consolidated secrets/environments table**, merged from the delegated orchestrator's own table (repository
  secrets such as `SONAR_TOKEN`, publish/store credentials, signing material, and any CI environment it named) —
  don't re-derive or expand it, just merge duplicates if this run somehow touched more than one delegated skill
  (e.g. the `multiple` case from Step 1).
- An explicit **Warn explicitly** block, always including:
  - **Review every generated/updated file before committing, building, or relying on CI.**
  - Every secret in the table above, and the matching SonarCloud project / registry account (npm, Maven Central,
    the Swift Package Index, GHCR) / store account (App Store Connect, Google Play Console, Firebase, Expo/EAS, the
    WordPress.org plugin/theme directory, PrestaShop Addons) named there, must
    already exist before CI can pass — nothing in this pipeline creates or stores any account or credential.
  - Which values were **inferred** rather than asked — anything Step 1's `iru-explore` run detected and this skill
    pre-selected or pre-filled, `visibility` when it was detected via `gh repo view`, and every default this skill
    or a delegated orchestrator applied silently (e.g. `distribution: store` only because the project is open
    source, `pages: yes` only because the repository is public) — so the user can correct a wrong guess before
    relying on it.

If Step 1 or Step 2 ended on `dotnet`/`rust`/`go`/`php-library`/`python-library`/`other`/no orchestrator available, report that outcome plainly instead of
the above (project type identified, no bootstrap orchestrator exists in this catalog for it, no delegation was
attempted) rather than fabricating a report for a run that never happened.
