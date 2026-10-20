---
name: iru-explore
description: >-
  Explore this repository codebase, optionally grounded in a specific GitHub issue or Jira ticket used as the task to investigate, and detect the programming language(s) and framework(s) in play — including Vite+React, Angular CLI, Hilla (Spring Boot + Vaadin + Hilla), Kotlin Spring Boot, Quarkus (Java or Kotlin), NestJS, Next.js, PHP (Laravel, WordPress plugin/theme, PrestaShop module, plain Composer package), Python (FastAPI, Django, plain package), React Native (Expo vs. bare React Native CLI/Metro toolchain), Ionic/Capacitor, Kotlin Multiplatform (Compose Multiplatform vs. native UI), Android (library vs. application, Compose), SwiftPM/Xcode/XcodeGen/Tuist stacks, macOS desktop apps (SwiftUI vs. AppKit, MVVM vs. MVC), Windows desktop apps on .NET (WPF, WinUI 3, Windows Forms; MVVM vs. MVC), Rust and Go projects, and command-line tools (Rust clap/Ratatui, Go Cobra/Bubble Tea, Swift ArgumentParser, .NET System.CommandLine) — both in the existing codebase and in the requested change, and reports a normalized `Project type:` line for downstream bootstrap tooling — plus whether Antora documentation exists and where, which platform hosts the repository (GitHub, Bitbucket, Azure DevOps, or TFS), and whether a `.archive/` directory holds implementation plans from previously resolved tasks that resemble the current one. Works even when the current working directory isn't a git repository at all — it warns the user that git-remote-dependent tooling (e.g. `gh` inferring an owner/repo, `git log` history) won't work, then keeps going with whatever sources don't need one: a Jira ticket, a connected documentation MCP, and any files actually present in the working directory. Invoke as `/iru-explore <ticket-id>` where `<ticket-id>` is either a GitHub issue ID (e.g. `42`) or a Jira key (e.g. `PROJ-123`) — the skill auto-detects which. If invoked as `/iru-explore` with no argument, ask the user for a ticket ID; if they decline or give none, just explore the current codebase. Looks up GitHub issues with the `gh` CLI (or GitHub MCP tools if `gh` is unavailable) and Jira tickets via any connected Jira MCP tools — for a Jira ticket, also fetches its epic and any linked/related tickets (one hop out), and downloads and reads any `implementation_plan_*.md` attached to the ticket, its epic, or its linked tickets (the naming convention `iru-code`/`iru-issue` archive and attach a completed plan under), for additional context — and, if a documentation MCP (e.g. Confluence, Notion) is connected, searches it for pages relevant to the ticket or codebase for extra context. Use for onboarding, understanding "what would it take to fix issue #N"/"ticket PROJ-123", or getting oriented before planning work. For UI projects it also scans existing code for accessibility / assistive-technology support and reports an `Accessibility: present|partial|absent` line (with the `.ui-quality.yml` level, including `none`). Its "Tech stack" and "Related past implementation plans" findings (languages/frameworks, Antora docs location, repository host, relevant archived plans) are meant to be reused by later skills in the same conversation (e.g. `iru-plan`, `iru-code`, `iru-update-docs`, code review, branch/PR creation) to pick language/framework-appropriate flows, best practices, the right git-platform tooling, and proven prior plan structure.
model: opus
---

# Explore

Produce a grounded understanding of this repository codebase and, when available, of a specific GitHub issue or
Jira ticket — without writing a plan or making code changes. This skill is read-only research: its output is a
report, not a diff.

## Step 1 — Resolve the ticket ID and its type

The skill may be invoked with a ticket ID as its argument (e.g. `/iru-explore 42` or `/iru-explore PROJ-123`).

- **Argument provided**: detect which system it belongs to:
  - Matches a Jira key pattern — one or more uppercase letters/digits starting with a letter, a hyphen, then
    digits (e.g. `PROJ-123`, `ABC2-45`) → **Jira**.
  - A bare number, optionally prefixed with `#` (e.g. `42`, `#42`) → **GitHub issue**.
  - If it matches neither pattern clearly, ask the user (via `AskUserQuestion`) whether it's a GitHub issue ID or
    a Jira key.
- **No argument provided**: ask the user (via `AskUserQuestion`) for a ticket ID to focus the exploration on,
  making clear they can skip this and just have the codebase explored instead. Offer something like:
  - "Provide a GitHub issue ID or Jira key" (free text via "Other")
  - "No ticket — just explore the codebase" (recommended default if they seem in a hurry)
  - If they decline or give none, proceed directly to Step 4 (codebase-only exploration).

## Step 2 — Detect the repository host and available tooling

Determine which platform hosts this repository, so later skills that operate on it (branch creation, pull/merge
requests, commit history, CI status, etc.) know which CLI/API to use instead of assuming GitHub by default.

**First, confirm the current working directory is actually inside a git repository at all**
(`git rev-parse --is-inside-work-tree`, or check for a `.git` directory/file up the tree) — this skill must still
be useful when it isn't, e.g. run from a plain folder of docs, a fresh checkout-in-progress, or a directory that
was never `git init`'d:

- **Not a git repository**: tell the user plainly, once, that no repository was detected in the current working
  directory — record `Repository host: none — not a git repository` for Step 7 and skip the rest of this step
  (there is no remote to inspect). This also means any git-dependent tooling later in this skill (`gh` inferring
  an owner/repo from the local remote, `git log` for recent history in Step 4) will not work; note that
  explicitly too, as a warning, not a hard stop — continue exploring with whatever sources don't need a
  repository: a Jira ticket (Step 3) fetched via Jira MCP tools, a documentation MCP (Step 6), and any files
  actually present in the working directory (Step 4 — Antora docs, `CLAUDE.md`/`README`, source files, all work
  the same whether or not the directory happens to be a git repo).
- **Is a git repository**: continue below as normal.
- Get the remote URL: `git remote get-url origin` (fall back to `git remote -v`, or to whichever remote the
  current branch tracks, if `origin` isn't the remote in use).
- Match the URL against known host patterns:
  - `github.com` (or a GitHub Enterprise Server domain — look for a `/api/v3/`-style setup, or ask if uncertain)
    → **GitHub**. Tooling: `gh` CLI, or GitHub MCP tools (`ToolSearch` "github").
  - `bitbucket.org` (cloud), or a self-hosted domain with a `/scm/<project>/<repo>.git` path (the Bitbucket
    Server/Data Center convention) → **Bitbucket**. Tooling: there's no ubiquitous CLI equivalent to `gh` here —
    search for Bitbucket MCP tools first (`ToolSearch` "bitbucket"), otherwise fall back to the Bitbucket REST
    API.
  - `dev.azure.com` or `<org>.visualstudio.com` → **Azure DevOps (cloud)**. Tooling: `az repos`/`az boards` (the
    Azure CLI with the `azure-devops` extension) if installed, or Azure DevOps MCP tools (`ToolSearch`
    "azure devops").
  - A self-hosted domain with a `/tfs/` path segment, or `_git` in the path without a `dev.azure.com`/
    `visualstudio.com` domain → **Azure DevOps Server / Team Foundation Server (TFS)**. Same tooling family as
    Azure DevOps (`az repos` can often target a collection URL directly), but confirm the collection URL and API
    version before assuming parity — older on-prem TFS versions expose a narrower REST API surface than cloud
    Azure DevOps.
  - If the URL doesn't clearly match any of these (e.g. a mirrored or internal git host), ask the user (via
    `AskUserQuestion`) which platform it is rather than guessing — a wrong assumption here would misdirect every
    later git-platform operation.
- If there is no remote configured at all (a purely local repository), note that explicitly — later skills that
  need a hosted platform (PR/merge-request creation, etc.) won't have one to target.
- Record the detected host — and, for Azure DevOps/TFS or self-hosted Bitbucket, the base URL/collection — for
  the report in Step 6. This detection is what later skills should key off instead of re-deriving it or
  defaulting to GitHub-specific tooling (`gh`, "Closes #N", etc.) unconditionally.

This is independent of Step 1: it detects where the **code repository** is hosted, not where the **ticket**
lives — a Jira ticket can reference work in a GitHub, Bitbucket, or Azure DevOps repo, and vice versa.

## Step 3 — Fetch the ticket

### GitHub issue

Determine the repository (owner/name) from the git remote, e.g.:

```bash
gh repo view --json owner,name -q '.owner.login + "/" + .name'
```

- **If Step 2 found no git repository at all** (or a repository with no remote configured), `gh repo view` has
  nothing to infer owner/repo from and will fail — this is expected, not a bug. Ask the user for the target
  repository explicitly (`owner/repo`), then fetch with `--repo` supplied directly:
  ```bash
  gh issue view <issue-id> --repo <owner/repo> --json number,title,body,labels,comments,state,url
  ```
  If they don't know it or decline, warn them that the GitHub issue can't be fetched without a repository
  context, then continue with a codebase-only or Jira-only exploration (Step 4 onward) rather than stopping the
  whole skill — a missing repository should degrade this one lookup, not the rest of the exploration.

Otherwise, fetch the issue with the `gh` CLI directly:

```bash
gh issue view <issue-id> --json number,title,body,labels,comments,state,url
```

If `gh` is not installed/authenticated, search for GitHub MCP tools instead (`ToolSearch` with a query like
"github issue") and use those to fetch the same information — these may still work without a local repository if
the tool takes an explicit owner/repo parameter rather than inferring it from `git remote`. If neither is
available, tell the user and continue with a codebase-only exploration (Step 4), noting the issue could not be
retrieved.

### Jira ticket

Search for connected Jira MCP tools (`ToolSearch` with a query like "jira issue" or "jira ticket"). If one or
more are found, use them to fetch the ticket by key: summary/title, description, issue type, status, labels/
components, comments, URL, and its issue links (`issuelinks`, plus the epic/parent relationship).

If no Jira MCP tool is available, tell the user plainly that this environment has no Jira connection, then ask
(via `AskUserQuestion`) whether to:
- paste the relevant ticket content (title/description/comments) directly so exploration can proceed grounded
  in it, or
- continue with a codebase-only exploration (Step 4), noting the ticket could not be retrieved.

Don't guess at Jira REST endpoints or attempt to `WebFetch` a Jira URL directly — Jira instances are normally
authenticated, and an unauthenticated fetch will just fail or return a login page.

**Also fetch the epic and any linked tickets, one hop out**, since a single ticket's own fields often omit
context that lives on its epic or on tickets it references — a plan grounded only in the leaf ticket can miss a
constraint the epic states once for all its children, or misunderstand what "blocks"/"relates to" actually means
without reading the other side of that link:

- **Epic**: check whether the ticket belongs to an epic — the classic "Epic Link" field, or the `parent` field
  in team-managed/next-gen projects. If it does, fetch that epic ticket too (summary, description, status, and
  its own labels/components) — an epic frequently carries the overall goal, cross-cutting acceptance criteria, or
  links to design docs that no individual child ticket repeats.
- **Linked/related tickets**: for each entry in the ticket's `issuelinks` (e.g. "relates to", "blocks", "is
  blocked by", "duplicates", "clones") and any subtasks, fetch that linked ticket's summary, description, and
  status — enough to know concretely what the link means for this task, not just that it exists. Skip fetching
  its own comments unless the summary/description alone leaves the relationship unclear.
- Keep this to one hop from the primary ticket — don't recursively follow the epic's or a linked ticket's own
  links.
- If fetching the epic or a linked ticket fails (no permission, deleted, not found), note that briefly and
  continue with what was retrieved rather than blocking the whole exploration on it.

**Also check for attached implementation plans**, on the ticket itself and on its epic/linked tickets fetched
above: list each ticket's attachments (via the same Jira MCP tool set — `ToolSearch` "jira attachment" if the
issue-fetch tool doesn't already return an attachment list) and look for any file named `implementation_plan_*.md`.
This is exactly the naming convention `iru-code`'s own archiving step uses, and `iru-issue` attaches that archived
file back onto the ticket it resolved (per its own Step 7) — so a match here is a previously-completed
implementation plan for work the ticket-filer or a prior agent run judged similar or related, travelling with the
ticket itself rather than needing a local `.archive/` in this checkout.

- Download and read each matched attachment in full — it's the same kind of precedent this skill's `.archive/`
  check in Step 4 looks for locally, just sourced from the ticket instead of the current repository.
- If more than one is attached (e.g. an epic with several resolved child tickets, each having attached its own
  plan), read all of them — they're typically small and each is a distinct, useful precedent.
- If the connected Jira MCP tool set has no way to list or download attachment content, note that explicitly and
  continue without it — this is a best-effort enrichment, not a blocker for the rest of exploration.
- If nothing matches `implementation_plan_*.md` on the ticket or its epic/linked tickets, note that briefly too
  rather than silently omitting the check.

### Either way

Read the ticket's title, body/description, labels, and any comments that clarify scope or add constraints —
plus, for a Jira ticket, the epic's and any linked tickets' summaries/descriptions, and any downloaded
`implementation_plan_*.md` attachments, fetched above. Note explicitly: what behavior is requested/reported, any
acceptance criteria (including any stated only on the epic), and any files, classes, error messages, languages,
frameworks, or platforms mentioned — across the primary ticket, whatever epic/linked tickets were fetched, and
any attached implementation plans read.

## Step 4 — Explore the codebase

This step must work generically on any repository — and equally on a working directory that per Step 2 isn't a
git repository at all — don't assume a language, framework, or prior familiarity with the project. Start from
first principles each time; every check below is file-based and works the same whether or not `.git` exists.

- Get the lay of the land first: check for a `CLAUDE.md`, `README`, or `AGENTS.md` (use as a starting index,
  never as a substitute for reading the actual files, and treat it skeptically if it looks stale), list the
  top-level directories, and identify the language(s), build/package tooling, and entry points (main modules,
  services, public API surface).
- Check whether Antora documentation exists and where: look for an `antora.yml` (commonly under `docs/`, but
  confirm the actual path rather than assuming) and, alongside it, an `antora-playbook.yml` and a
  `modules/ROOT/pages` (or other module) tree. Record the docs root path if found — later skills (e.g.
  `iru-update-docs`) need this location, and its content is itself a language/framework signal (see Step 5).
- Check for a `.archive/` directory at the repository root and give it special attention: the `iru-code` skill
  archives every completed `implementation_plan.md` there (typically as
  `implementation_plan_<ticket-or-timestamp-id>.md`) once its task groups are done, so it's a library of
  previously resolved tasks. If it exists, list its contents (`ls .archive`) and skim each archived plan's
  title/summary for one whose topic, named files/classes, or task area overlaps with the current ticket (or,
  with no ticket, the general topic of this exploration) — matching on keywords rather than reading every file
  in full. Read the most relevant one or two in full: a matching archived plan shows how a similar task was
  previously scoped, broken into dependency-aware task groups, and what its "Current code state" notes
  captured — treat it as a concrete example to ground the current task's own plan against, not as a template
  to copy verbatim, since the current change is never identical. If `.archive/` doesn't exist, or nothing in it
  is relevant, note that explicitly rather than silently skipping the check.
- Use the `Explore` agent (or direct `Read`/`grep` for small, targeted lookups) to build a picture of the
  most significant parts of the code structure: how the project is organized into modules/packages, the core
  abstractions and how they relate (inheritance, composition, key interfaces), where the main control flow or
  request/data path runs, and where tests live and how they map to source.

**If a ticket was fetched**, narrow the exploration to only the areas it implicates — do not do a full general
tour. Concretely:
  - Search for the classes/functions/files/error messages/behaviors named or described in the ticket.
  - Read those files plus their closest structural neighbors (the base class/interface they implement, direct
    callers/callees) — only as much surrounding context as needed to understand how that area currently
    behaves.
  - Check existing tests covering that area to learn current expected behavior and edge cases already handled.
  - Skip unrelated parts of the codebase, even if they'd normally be worth a general orientation pass.

**If there is no ticket** (declined or unavailable), do a general orientation pass instead: map out the overall
architecture — the major components/modules, how they depend on each other, key abstractions and design
patterns in use, and, if Step 2 found this is actually a git repository, anything notable in recent git history
(`git log --oneline -20`) that suggests active areas of work. Skip the git-history check entirely (not a
failure, just nothing to check) if Step 2 found no git repository.

- **Accessibility scan** (UI projects only — skip when Step 5 finds no user interface): follow
  `reference/accessibility-detection.md` to look for existing assistive-technology support (ARIA/`alt`/labels,
  `contentDescription`, `accessibilityLabel`, `AutomationProperties`, a11y lint and audit tooling, any
  `.ui-quality.yml`), sample the coverage, and classify the result `present`, `partial` or `absent`. Read-only:
  report the evidence in Step 7, never change code.

## Step 5 — Detect the technology stack

Identify the programming language(s) and framework(s) in play, both for the existing codebase and for whatever
change is being requested. This is not a vague "looks like Java" impression — ground it in concrete evidence, and
call out enough detail (per-module, if the repo has more than one stack) that later skills can act on it directly.

### Codebase languages and frameworks

Use whichever of these signals are present — manifests/config are the most reliable, source-level signals are the
fallback when manifests are absent or ambiguous:

- **Build/package manifests** are the primary signal:
  - `pom.xml`, `build.gradle`/`build.gradle.kts` → Java/Kotlin; check dependencies for `spring-boot-starter*`
    (Spring/Spring Boot) — and among Spring Boot deps, `hilla-spring-boot-starter` and/or
    `com.vaadin:vaadin-spring-boot-starter` → Hilla (Spring Boot + Vaadin + Hilla), corroborated by a
    `@vaadin/hilla` dependency in a co-located `package.json` and a `src/main/frontend/` directory — `micronaut-*`,
    `quarkus-*`, or an Android Gradle plugin (`com.android.application`/`com.android.library`).
    - **Build tool**: record which one is in use — Maven (`pom.xml`, `mvnw`), Gradle Kotlin DSL
      (`build.gradle.kts`/`settings.gradle.kts`), or Gradle Groovy (`build.gradle`/`settings.gradle`), plus
      whether a wrapper (`mvnw`/`gradlew`) is present — since the coding and gate skills run different commands
      for each.
    - **Kotlin**: `org.jetbrains.kotlin:kotlin-maven-plugin` in `pom.xml`, a `kotlin("jvm")`/
      `org.jetbrains.kotlin.jvm` plugin (or `kotlin("plugin.spring")`/`kotlin("plugin.jpa")`) in
      `build.gradle.kts`, and/or a `src/main/kotlin/` tree → Kotlin. Combined with `spring-boot-starter*` →
      Kotlin Spring Boot (and Kotlin Spring Boot + Hilla when the Hilla markers above are also present). A
      `src/main/java/` tree alongside `src/main/kotlin/` is a mixed Java/Kotlin module — record it as such and
      decide Java vs. Kotlin by where the bulk of production sources live.
    - **Quarkus**: the `io.quarkus:quarkus-maven-plugin` (or Gradle `id("io.quarkus")`), an imported
      `io.quarkus.platform:quarkus-bom`/`io.quarkus:quarkus-bom`, and/or `io.quarkus:quarkus-*` dependencies →
      Quarkus; Java vs. Kotlin by the Kotlin signals above (a `quarkus-kotlin` extension corroborates Kotlin).
    - **Architecture layout** (Spring Boot / Quarkus backends): record whether the build is a **hexagonal
      multi-module reactor** — sibling modules named (or suffixed) `domain`, `application`, `infrastructure`
      (or `adapters`), and `api`/`rest`/`web`, wired via `<modules>` in a parent `pom.xml` or `include(...)` in
      `settings.gradle*`, with dependencies pointing inward toward `domain` — vs. a **layered/feature-based**
      single-module (or loosely multi-module) layout. The coding skills apply hexagonal boundary rules only for
      the former, so state which one it is explicitly.
    - **Android plugin id**: `com.android.library` → Android library module, `com.android.application` → Android
      application module — read it directly from `build.gradle`/`build.gradle.kts`, or, when the project
      centralizes versions/plugins in `gradle/libs.versions.toml` (itself a signal worth recording), from a
      plugin alias named e.g. `android-library`/`android-application` there instead. Check for an
      `androidx.compose:compose-bom` (or another `androidx.compose*`) dependency → Jetpack Compose UI, vs. its
      absence → XML/View-based UI. A repository laid out as a `lib/` module (library plugin) alongside an `app/`
      module (application plugin) that depends on it (`implementation(project(":lib"))`) is this catalog's
      reference Android *library* shape — the app is the library's sample/demo, not a second deliverable — so
      record the library as the project type and the sample module as a sub-line, rather than treating them as
      two unrelated modules (see Step 7's `android-library` rule).
    - **Kotlin Multiplatform**: a `kotlin("multiplatform")` / `org.jetbrains.kotlin.multiplatform` plugin (directly
      or via a `kotlin-multiplatform`/`kotlinMultiplatform` alias in `gradle/libs.versions.toml`), with
      `src/commonMain/` (+ `androidMain/`, `iosMain/`) source sets, → a KMP module. An Android target
      (`androidTarget()`, the `com.android.kotlin.multiplatform.library` plugin, or `com.android.library` in the
      same module) plus iOS targets (`iosArm64()`/`iosSimulatorArm64()`/`iosX64()`) and an `iosApp/` Xcode (or
      XcodeGen `project.yml`) host app → a KMP mobile app. Record the UI approach: the Compose Multiplatform plugin
      (`org.jetbrains.compose` + `org.jetbrains.kotlin.plugin.compose`) with composables in `commonMain` → `compose`
      (shared UI); shared logic only, with Jetpack Compose/Views in the Android app module and SwiftUI/UIKit in
      `iosApp/` → `native`. Record the module layout (`shared/` + `androidApp/` + `iosApp/`, or the JetBrains
      wizard's single `composeApp/` module) and the test/coverage plugins (Kover, detekt, ktlint) on the `Build &
      layout:` line. A `com.android.application` module that only exists to host the KMP `shared` module is part
      of the KMP app — never a separate `android-app`, and never `multiple`.
  - `*.csproj`/`*.fsproj`/`*.sln`/`*.slnx` → C#/.NET (or F#); check for `Microsoft.AspNetCore.*` (ASP.NET Core),
    `*.Maui`/Xamarin (cross-platform mobile), and Windows desktop project types:
    - A project with `<OutputType>WinExe</OutputType>` (or a `net*-windows*` target framework) and
      `<UseWPF>true`, `<UseWinUI>true` (Windows App SDK / WinUI 3, usually with a `Package.appxmanifest`) or
      `<UseWindowsForms>true` → a **Windows desktop app**: record the UI stack (`wpf`/`winui`/`winforms`) and the
      architecture from the layout — a UI-free `src/<App>.Core` project with `ViewModels/` (or MVVM Toolkit
      `ObservableObject`/`[ObservableProperty]` usages) → MVVM; `Controllers/` plus view interfaces → MVC — on the
      `Build & layout:` line, together with the test framework (MSTest/xUnit/NUnit), FlaUI UI tests and MSIX
      packaging (`Package.appxmanifest`, `packaging/AppxManifest.xml`, `*.wapproj`). A WPF/WinForms *library* (no
      `WinExe`) stays plain `dotnet`.
  - `package.json` → JavaScript/TypeScript; check `dependencies`/`devDependencies`:
    - `vite` + `react` (typically alongside a `vite.config.*` file) → Vite + React web app.
    - `@angular/cli` and/or `@angular/core`, corroborated by an `angular.json` at the project root → Angular CLI
      web app.
    - `@vaadin/hilla`, alongside a `src/main/frontend/` directory → the frontend half of a Hilla app (see the
      `pom.xml` bullet above for its Spring Boot backend half).
    - `expo` and/or `react-native` → React Native app. Record its **toolchain**: `expo` among the dependencies →
      `expo` (Expo framework — corroborated by `app.json`/`app.config.*` with an `expo` key, `eas.json`,
      `expo-router`; committed `ios/`/`android/` directories in an Expo app are `npx expo prebuild`/CNG output
      and don't change the answer); `react-native` without `expo` → `metro` (bare React Native Community CLI
      project — corroborated by `metro.config.js`, `@react-native-community/cli*` devDependencies,
      `index.js` calling `AppRegistry.registerComponent`, and committed native `android/` (Gradle) and `ios/`
      (`Podfile`, `*.xcworkspace`) projects). Expo also bundles with Metro, so `metro.config.js` alone doesn't
      decide it — the `expo` dependency does. Also record the navigation library (`expo-router` vs.
      `@react-navigation/*`) and the e2e tool if any (`.maestro/` flows, a `.detoxrc.js`).
    - `@ionic/angular` or `@ionic/react` → Ionic, with which of the two deps is present telling you the
      underlying framework (Angular vs. React) Ionic is layered on; `@capacitor/core` plus a
      `capacitor.config.*` and/or `ionic.config.json` corroborate it as an Ionic/Capacitor hybrid app rather
      than a plain Angular/React web app.
    - `@nestjs/core` (usually with `@nestjs/cli`, a `nest-cli.json`, and `src/main.ts` calling
      `NestFactory.create`) → NestJS backend. Also record: module format — ESM (`"type": "module"`, relative
      imports ending in `.js`) vs. CommonJS (no `type` field); test runner — Vitest (`vitest.config*.ts`) vs. Jest
      (`jest.config.*`, `test/jest-e2e.json`); and the persistence layer — TypeORM (`@nestjs/typeorm`), Prisma
      (`prisma`/`@prisma/client`, `prisma/schema.prisma`), or Mongoose (`@nestjs/mongoose`), if any.
    - `next` (with a `next.config.*`) → Next.js web app. Also record: App Router (`app/` or `src/app/` with a root
      `layout.tsx`) vs. Pages Router (`pages/` or `src/pages/`) — or both, if they coexist; the installed Next major
      version (from `package.json`/the lockfile — caching and request-API semantics differ between 13/14, 15, and
      16); and whether `cacheComponents: true` is set in `next.config.*` (Cache Components model vs. the previous
      caching model).
    - `vue`, `express`, etc. — other framework deps, as already covered.
    - No app-framework dependency present, but `main`/`exports`/`types` fields plus a co-located
      `tsconfig.json` → a plain TypeScript/npm library (no framework), not an application.
  - `composer.json` and/or `*.php` sources → PHP; record the PHP version constraint (`require.php`) and the test
    runner (Pest vs. PHPUnit), then tell the kind of project apart:
    - `laravel/framework` in `composer.json` plus an `artisan` file at the root → Laravel application.
    - A PHP file at the plugin root whose header comment carries `Plugin Name:` (typically `<slug>/<slug>.php`,
      often with a `readme.txt`) → WordPress plugin.
    - A `style.css` whose header comment carries `Theme Name:` and/or a `theme.json` (block theme: `templates/`,
      `parts/`) → WordPress theme.
    - A main class that `extends Module` (or `PaymentModule`/`CarrierModule`) in `<module>/<module>.php`, a
      `config.xml`, and/or `prestashop/*` dependencies in `composer.json` → PrestaShop module.
    - Any other `composer.json` package (a `type` of `library`, or none, with PSR-4 `autoload`) → plain PHP
      library/package.
  - `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py` → Python; record `requires-python` and the
    project/package manager (`uv.lock` → uv, `poetry.lock` → Poetry, `pdm.lock` → PDM, `Pipfile.lock` → Pipenv,
    otherwise pip/`requirements*.txt`) and the test runner (pytest, pytest-django, or Django's `manage.py test`),
    then tell the kind of project apart:
    - `django` among the dependencies plus a `manage.py` at the root (or the directory the module lives in) →
      Django project. Also record the settings module (`DJANGO_SETTINGS_MODULE` in `manage.py`/pytest config, e.g.
      `config.settings.local`), the app layout (`apps/<app>/` vs. root-level apps), and the API layer:
      `djangorestframework` (DRF), `django-ninja` (Ninja), or neither.
    - `fastapi` among the dependencies (+ a `FastAPI(` app object, typically `app/main.py` or `src/<pkg>/main.py`)
      → FastAPI service. Also record the layout (`app/` layered, `src/<pkg>/`, or hexagonal ports/adapters), the
      persistence layer (SQLModel, SQLAlchemy 2.0 — sync or async —, or none) and whether Alembic is present.
    - `flask`, `pyramid`, `tornado`, etc. — other Python web frameworks (no catalog key: `other`).
    - None of those, with a `[project]`/`[tool.poetry]` table or a `setup.py` → plain Python library/package.
  - `Podfile`, `Package.swift`, `project.yml`, `Project.swift`, `*.xcodeproj`/`*.xcworkspace` → Swift and/or
    Objective-C:
    - `Package.swift` (SwiftPM) — its `products:` array tells library vs. executable (`.library(...)` vs.
      `.executable(...)`), and its `platforms:` array (e.g. `.iOS(.v16)`, `.macOS(.v13)`) gives the target
      platforms directly.
    - `project.yml` → an XcodeGen-managed project; `Project.swift` → a Tuist-managed project — either means the
      `.xcodeproj` itself is generated, so treat the generator file, not the generated project, as the source of
      truth for target/platform config, and read its `deploymentTarget` setting for target platforms.
    - A hand-maintained `*.xcodeproj`/`*.xcworkspace` with no generator file present — read target platforms from
      `SUPPORTED_PLATFORMS` / `TARGETED_DEVICE_FAMILY` in the `.pbxproj` or an `.xcconfig`.
    - Either way, check `import SwiftUI` vs. `import UIKit` in source files for the UI framework in use, and
      `.m`/`.mm`/`.h` file presence for Objective-C alongside `.swift`.
    - An app whose **only** platform is macOS (one `platform: macOS` app target / `.macOS(...)` deployment target, no
      iOS/watchOS/visionOS target) **and** the macOS desktop layout — an `App/` UI layer plus a UI-free local
      `Packages/Core`, with no per-platform `Targets/<Platform>/` folders (those mean an `iru-setup-apple-app`
      scaffold, which stays `apple-app (macos)`), or a hand-maintained/other macOS-only project that has neither
      layout → a **macOS desktop app**: record the UI framework (`swiftui` — a SwiftUI `App`;
      `appkit` — an `NSApplicationDelegate` with `NSWindowController`/`NSViewController` and no SwiftUI `App`) and the
      architecture from the layout (`Packages/Core/Sources/Core/ViewModels/` → MVVM; `…/Controllers/` → MVC), the App
      Sandbox/hardened-runtime entitlements, and the distribution files (`ExportOptions-*.plist`,
      `scripts/make-dmg.sh`) on the `Build & layout:` line.
  - `CMakeLists.txt`, `Makefile`, `*.vcxproj` with `.c`/`.cpp`/`.h`/`.hpp` sources → C/C++.
  - `Cargo.toml` → Rust. Record whether it is a workspace (`[workspace]` members, an `xtask/` member), the edition
    and `rust-version` (MSRV), `rust-toolchain.toml`, and the lib/bin split (`src/lib.rs`, `src/main.rs`,
    `[[bin]]` entries). A binary target **and** a `clap` dependency (or `ratatui`/`crossterm` for a terminal UI) →
    a **command-line tool**: record the parser (clap derive vs. builder), the TUI library (`ratatui` + `crossterm`
    → `ui: tui`, else `ui: none`), the async runtime (`tokio`), the test crates (`assert_cmd`, `predicates`,
    `snapbox`/`trycmd`, `insta`), and the quality config (`[lints]`, `deny.toml`, `rustfmt.toml`, cargo-llvm-cov /
    nextest config under `.config/`) on the `Build & layout:` line. Any other crate is a plain Rust project.
  - `go.mod` → Go. Record the module path and `go` directive, a `go.work` workspace, and the layout (`cmd/<name>/`,
    `internal/`, `pkg/`). A `package main` (under `cmd/<name>/` or at the root) **and** a CLI framework —
    `github.com/spf13/cobra`, `github.com/urfave/cli`, or `github.com/alecthomas/kong` — or Bubble Tea
    (`charm.land/bubbletea/v2`, `github.com/charmbracelet/bubbletea`) → a **command-line tool**: record the framework,
    the TUI library (Bubble Tea → `ui: tui`), testscript e2e tests (`testdata/script/*.txtar`,
    `github.com/rogpeppe/go-internal/testscript`), `.golangci.yml` (v1 or v2 config) and `.goreleaser.yaml` on the
    `Build & layout:` line. Any other module is a plain Go project.
  - **Command-line tools in Swift and .NET** — a `Package.swift` whose `.executableTarget` depends on
    `ArgumentParser` (swift-argument-parser) → a Swift **command-line tool** (record the executable and library
    targets, e.g. `<Bin>` + `<Bin>Kit`, and the CLI e2e test target); a `*.csproj` with
    `<OutputType>Exe</OutputType>`, none of `UseWPF`/`UseWinUI`/`UseWindowsForms`, and a `System.CommandLine` or
    `Spectre.Console.Cli` reference (or `<PackAsTool>true`) → a .NET **command-line tool** (record the Core project,
    `PublishAot`, `PackAsTool`, Spectre.Console / Terminal.Gui for a terminal UI). Both still use the existing
    `swift`/`dotnet` coding keys.
  - `Gemfile` → Ruby.
- **Source-level fallback**: when manifests are absent, sparse, or ambiguous (e.g. a monorepo with multiple
  stacks, or a manifest that doesn't disambiguate framework choice), sample actual source files — file
  extensions, `import`/`using`/`#include` statements, and characteristic APIs — to confirm or fill the gap.
- **Antora documentation, if present** (per Step 4): read `antora.yml` (component `name`/`title`) and the docs
  pages themselves — an `installation.adoc`/`reference.adoc`/`getting-started.adoc` will typically spell out the
  language and build tool explicitly (e.g. a Maven/Gradle/npm/NuGet dependency snippet, a `pod` entry, an
  `import` example). Treat this as a corroborating signal, not a substitute for the manifest/source checks
  above — but when manifests are ambiguous or a module lacks one of its own, the docs are often the clearest
  statement of intent, and are worth quoting directly rather than re-deriving from source alone. Note any
  mismatch between what the docs claim and what the manifests/source actually show (e.g. stale docs describing a
  since-migrated framework) instead of silently preferring one over the other.
- **Multiple stacks**: if the repository contains more than one language/framework (e.g. a backend service plus
  a mobile client, or a monorepo of independent packages), record the stack per module/directory rather than
  flattening it into one list.

### Languages/frameworks implicated by the requested change

If a ticket was fetched, read its title/description/comments for explicit or implicit tech signals — named
languages, frameworks, or platforms (e.g. "iOS", "Android", "the web dashboard", "the API"), specific file/class
names, or code snippets whose syntax identifies a language. Then cross-reference against the codebase stack just
detected:

- If the ticket's signals match a part of the existing stack, note which module/language/framework the change
  targets.
- If the ticket names something **not** currently present in the codebase (e.g. a request to add a new mobile
  app to a backend-only repo, or to introduce a new framework), flag this explicitly as a new
  language/framework the work would introduce — don't silently assume it matches the existing stack.
- If nothing in the ticket indicates a specific target and the repo has a single stack, note that the change is
  presumed to apply to that stack. If the repo has multiple stacks and the ticket is genuinely ambiguous about
  which one it targets, say so rather than guessing.

If there is no ticket, this sub-step is just the codebase stack detected above — there is no requested change to
cross-reference yet.

## Step 6 — Check for a documentation MCP

Before reporting, check whether any documentation/knowledge-base MCP tools are connected in this session (e.g.
Confluence, Notion, or similar — search with `ToolSearch` using queries like "confluence", "notion",
"documentation", "wiki"). These are optional, environment-specific connectors, not something every repository or
user has configured.

- **If one or more are found**, use them to search for pages relevant to:
  - the ticket's title/keywords and any named components (if a ticket was fetched in Step 3), or
  - the key components/domain areas identified in Step 4 (if there is no ticket).

  Keep the search targeted — a handful of keyword queries against the ticket/codebase context, not a broad
  crawl of the whole space. Fetch and skim any clearly relevant pages (specs, design docs, architecture decision
  records, runbooks) that could sharpen a later implementation plan. Note what was found: page titles/links and
  a one-line summary of the relevant content, so it can be folded into Step 7's report.
- **If nothing relevant turns up** even though a documentation MCP is connected, say so briefly rather than
  omitting the mention.
- **If no documentation MCP is connected**, note that briefly and move on — this step is a best-effort
  enrichment and must never block exploration when no such tool exists.

## Step 7 — Report findings

Summarize for the user in plain text (no file output unless asked):

- Always include a **Tech stack** section, structured so later skills invoked in this same conversation (e.g.
  `iru-plan`, `iru-code`, code review, branch/PR creation) can read it directly instead of re-detecting it themselves:
  ```
  ## Tech stack
  - Languages (codebase): <e.g. Java, Kotlin>
  - Frameworks (codebase): <e.g. Spring Boot (backend/), Jetpack Compose (android/)>
  - Languages/frameworks (requested change): <e.g. Kotlin, Jetpack Compose — matches android/ module>
  - Project type: <one of: java-library, java-springboot, java-springboot-hilla, kotlin-springboot,
    kotlin-springboot-hilla, java-quarkus, kotlin-quarkus, typescript-library, react-web, angular-web, nestjs,
    nextjs, php-laravel, php-wordpress-plugin, php-wordpress-theme, php-prestashop-module, php-library,
    python-fastapi, python-django, python-library,
    android-library, android-app, swift-library, apple-app (ios, ipados, macos, watchos, visionos),
    macos-app (swiftui|appkit), react-native-app (expo|metro), ionic-app (angular|react),
    kmp-app (compose|native), windows-app (wpf|winui|winforms), cli-tool (rust|go|swift|dotnet), rust, go,
    dotnet, other, unknown>
  - Build & layout: <JVM backends: e.g. "Gradle (Kotlin DSL, wrapper), hexagonal reactor (domain/, application/,
    infrastructure/, api/)" or "Maven (wrapper), layered single-module"; NestJS: e.g. "ESM, Vitest, TypeORM";
    Next.js: e.g. "Next 16, App Router, cacheComponents: true"; PHP: e.g. "PHP ^8.3, Pest"; Python: e.g. "Python
    >=3.12, uv, pytest, app/ layered, SQLModel async + Alembic" or "Python >=3.12, uv, pytest-django, DRF,
    config.settings"; React Native: e.g. "Expo SDK 57, Expo Router, EAS, Maestro" or "RN 0.8x CLI (Metro), React
    Navigation, CocoaPods"; KMP: e.g. "Gradle (Kotlin DSL, wrapper), shared/ + androidApp/ + iosApp/ (XcodeGen),
    Kover, detekt, ktlint"; command-line tools: e.g. "clap 4 + ratatui (ui: tui), xtask, nextest, cargo-llvm-cov"
    or "Cobra, cmd/mytool + internal/, testscript, golangci-lint v2, GoReleaser" or "swift-argument-parser,
    MyTool + MyToolKit" or "System.CommandLine, Native AOT, Spectre.Console, MyTool.Core" — omit for other stacks>
  - User interface: <"none" — or the UI stack(s) and where, e.g. "Jetpack Compose (app/), 14 screens, 31
    components; .ui-quality.yml accessibility: enforce|report|off|none; Antora ui/ section: present (12 screen pages)" — or for a
    requested change that adds UI: the screens/components it introduces>
  - Accessibility: <present|partial|absent|not applicable (no UI)> — <evidence summary>; .ui-quality.yml: <value|missing>
  - Antora docs: <e.g. docs/ (antora.yml component "my-lib") — or "none found">
  - Repository host: <e.g. GitHub (github.com/org/repo) — or Bitbucket / Azure DevOps / TFS, with base URL — or
    "no remote configured" — or "none — not a git repository">
  ```
  If Step 2 found the working directory isn't a git repository at all, use that last form and add a one-line
  warning restating what that disabled this run (git-remote-dependent tooling like unscoped `gh issue view`,
  and `git log`-based history in Step 4) versus what still ran normally (Jira, a documentation MCP, and any
  file-based checks in Step 4/5).
  If the repo has multiple modules/stacks, break the codebase lines out per module. If the requested change
  introduces something new (per Step 5), say so explicitly here rather than folding it silently into the
  existing list. The **User interface** line tells `iru-plan` to decompose the change into screens/components
  (with virtualized collections, UI tests, screenshots and accessibility checks — omitted when `.ui-quality.yml` says `accessibility: none`) and `iru-update-docs` to maintain
  the UI pages: name the UI framework(s), count screens (navigable destinations) and reusable components roughly,
  read `.ui-quality.yml` if present (its `accessibility:` value may be `enforce`, `report`, `off` or `none`), and check whether the Antora module already has a `ui/` section. Always state
  the Accessibility, Antora docs and Repository host lines, even when the answer is "none found"/"no
  remote", so later skills like `iru-update-docs` or ones creating branches/PRs don't need to re-check.

  **The `Project type:` line** is a normalized, single-token-per-module summary of the Step 5 signals — this
  exact vocabulary is a shared contract with the `iru-setup-repository` front door, which reads this line
  verbatim to pre-select the right bootstrap flow, so never invent a value outside the list above. Derive it
  from Step 5's findings as follows:

  | Project type            | Derived from (Step 5 signals)                                                            |
  |--------------------------|-------------------------------------------------------------------------------------------|
  | `java-library`           | `pom.xml`/`build.gradle*` present, no `spring-boot-starter*`, no Quarkus, no Android plugin |
  | `java-springboot`        | `spring-boot-starter*` dependency present, Java sources, no Hilla markers                 |
  | `java-springboot-hilla`  | `hilla-spring-boot-starter`/`vaadin-spring-boot-starter` (+ `@vaadin/hilla`, `src/main/frontend/`) |
  | `kotlin-springboot`      | `spring-boot-starter*` + Kotlin (`kotlin-maven-plugin`/`kotlin("jvm")`/`kotlin("plugin.spring")`/`src/main/kotlin/`), no Hilla markers |
  | `kotlin-springboot-hilla`| Kotlin Spring Boot (as above) + the Hilla markers                                         |
  | `java-quarkus`           | `io.quarkus` plugin / `quarkus-bom` / `io.quarkus:quarkus-*` deps, Java sources           |
  | `kotlin-quarkus`         | Quarkus (as above) + Kotlin (`quarkus-kotlin`, Kotlin plugin, `src/main/kotlin/`)          |
  | `typescript-library`     | `package.json` with `main`/`exports`/`types` + `tsconfig.json`, no app-framework dep       |
  | `react-web`               | `package.json` with `vite` + `react` (or another React web setup, not Native/Ionic)        |
  | `angular-web`             | `@angular/cli`/`@angular/core` + `angular.json`, not layered under Ionic                   |
  | `nestjs`                  | `@nestjs/core` dependency (+ `nest-cli.json`, `NestFactory` in `src/main.ts`)               |
  | `nextjs`                  | `next` dependency (+ `next.config.*`, `app/` and/or `pages/`)                               |
  | `php-laravel`             | `composer.json` with `laravel/framework` + an `artisan` file                               |
  | `php-wordpress-plugin`    | Main PHP file with a `Plugin Name:` header comment                                         |
  | `php-wordpress-theme`     | `style.css` with a `Theme Name:` header and/or `theme.json`                                 |
  | `php-prestashop-module`   | Class `extends Module` (+ `config.xml`, `prestashop/*` deps)                                |
  | `php-library`             | Any other `composer.json` package (no Laravel/WordPress/PrestaShop markers)                |
  | `python-fastapi`          | `fastapi` dependency (+ a `FastAPI(` app, e.g. `app/main.py`)                              |
  | `python-django`           | `django` dependency + a `manage.py`                                                        |
  | `python-library`          | Any other Python package (`pyproject.toml`/`setup.py`, no Django/FastAPI/other web framework) |
  | `android-library`         | Gradle `com.android.library` plugin (direct or via `libs.versions.toml` alias)             |
  | `android-app`             | Gradle `com.android.application` plugin (direct or via `libs.versions.toml` alias)         |
  | `swift-library`           | `Package.swift` with a `.library(...)` product                                             |
  | `apple-app`               | An Xcode/XcodeGen/Tuist app target (or a `Package.swift` `.executable(...)` product that isn't an ArgumentParser command-line tool) |
  | `macos-app`               | An Xcode/XcodeGen/Tuist app whose **only** platform is macOS, not in the `iru-setup-apple-app` `Targets/<Platform>/` layout |
  | `react-native-app`        | `expo`/`react-native` deps (+ `app.json`/`metro.config.js`/`eas.json`, `ios/`+`android/`)   |
  | `kmp-app`                 | Kotlin Multiplatform plugin with Android + iOS targets (+ `iosApp/`, `commonMain/`)         |
  | `ionic-app`               | `@ionic/angular` or `@ionic/react` (+ `@capacitor/core`, `capacitor.config.*`)              |
  | `windows-app`             | A `WinExe` `*.csproj` with `UseWPF`/`UseWinUI`/`UseWindowsForms` (Windows desktop app)      |
  | `cli-tool`                | A command-line tool: Rust binary + `clap` (or `ratatui`); Go `package main` + Cobra/urfave/kong (or Bubble Tea); a `Package.swift` `.executableTarget` on `ArgumentParser`; an `Exe` `*.csproj` (no WPF/WinUI/WinForms) with `System.CommandLine`/`Spectre.Console.Cli`/`PackAsTool` |
  | `rust`                    | Any other `Cargo.toml` crate or workspace (library, service)                                |
  | `go`                      | Any other `go.mod` module (library, service)                                                |
  | `dotnet`                  | Any other `*.csproj`/`*.fsproj`/`*.sln`/`*.slnx` (library, ASP.NET Core, MAUI/Xamarin)      |
  | `other`                   | A stack was detected but has no key above (e.g. Vue, Flutter, Micronaut, Flask, Ruby, C/C++, a KMP library with no app) |
  | `unknown`                 | Nothing in Step 5 matched any manifest or source-level signal                              |

  - `apple-app` lists its detected target platforms in parentheses, using the platform keys `ios`, `ipados`,
    `macos`, `watchos`, `visionos` (e.g. `apple-app (ios, ipados)`) — derived from `Package.swift`'s `platforms:`
    array, `project.yml`/`Project.swift`'s `deploymentTarget`/`platform`, or `SUPPORTED_PLATFORMS`/
    `TARGETED_DEVICE_FAMILY`, as detected in Step 5. Its `Build & layout:` line also records the iOS target's UI
    framework (`swiftui`, or `uikit` — a `UIApplicationDelegate` + `UIWindowSceneDelegate` with no SwiftUI `App`) and
    the architecture from `Packages/Core/Sources/Core/ViewModels/` (MVVM) vs `…/Controllers/` (MVC).
  - `ionic-app` lists its underlying framework in parentheses — `ionic-app (angular)` or `ionic-app (react)` —
    from whichever of `@ionic/angular`/`@ionic/react` was found.
  - `react-native-app` lists its toolchain in parentheses — `react-native-app (expo)` or `react-native-app (metro)`
    — per Step 5's rule (the `expo` dependency decides; committed native folders alone don't).
  - `macos-app` lists its UI framework in parentheses — `macos-app (swiftui)` or `macos-app (appkit)`. It takes
    precedence over `apple-app (macos)` except for an `iru-setup-apple-app` scaffold (`Targets/macOS/…`), which stays
    `apple-app (macos)` so it keeps its own setup chain; an app with macOS plus any other Apple platform stays
    `apple-app`.
  - `windows-app` lists its UI stack in parentheses — `windows-app (wpf)`, `windows-app (winui)` or
    `windows-app (winforms)`. Its `src/<App>.Core` class library and test projects are part of the same value,
    never extra `dotnet` entries or `multiple`.
  - `cli-tool` lists its language in parentheses — `cli-tool (rust)`, `cli-tool (go)`, `cli-tool (swift)` or
    `cli-tool (dotnet)` — and its `Build & layout:` line names the argument parser, the terminal-UI library when
    there is one (`ui: tui`), and the e2e test setup. It takes precedence over `rust`/`go`/`swift-library`/
    `apple-app`/`dotnet` for the same module: the library unit a CLI keeps its logic in (`src/lib.rs`, `internal/`,
    `<Bin>Kit`, `src/<Tool>.Core`) and a Rust `xtask/` workspace member are part of the same value, never extra
    entries or `multiple`.
  - `kmp-app` lists its UI approach in parentheses — `kmp-app (compose)` (Compose Multiplatform shared UI) or
    `kmp-app (native)` (shared logic, platform-native UI). Its Android host module (`androidApp/`) and `iosApp/`
    are part of the same value, never extra `android-app`/`apple-app` entries or `multiple`.
  - **Java vs. Kotlin** (Spring Boot / Quarkus): pick the `kotlin-*` value when Kotlin is the build's primary
    language (Kotlin plugin applied and production sources mainly under `src/main/kotlin/`); a Java build with a
    few Kotlin files stays `java-*`. A **hexagonal multi-module reactor** (`domain`/`application`/`infrastructure`/
    `api` modules) is still a single project type — e.g. `kotlin-springboot` with the layout on the
    `Build & layout:` line — **not** `multiple`.
  - **PHP**: Laravel, WordPress, and PrestaShop markers take precedence over `php-library` (a Laravel app or a
    PrestaShop module also has a `composer.json`). A WordPress plugin that ships blocks is still
    `php-wordpress-plugin`; a repository holding both a plugin and a theme is `multiple`.
  - **Python**: Django and FastAPI markers take precedence over `python-library`. A Django project that also
    mounts a FastAPI app (or the reverse) is classified by its primary entry point (`manage.py` → `python-django`);
    two independent services in one repository are `multiple`. Flask/Pyramid/Tornado projects are `other`.
  - **Hilla frontend vs. Next.js/NestJS**: a `package.json` under a Spring Boot module's `src/main/frontend/` is
    part of the `*-springboot-hilla` value, never a separate `nextjs`/`react-web` module.
  - Examples: `- Project type: kotlin-quarkus` with `- Build & layout: Gradle (Kotlin DSL, wrapper), layered
    single-module`; `- Project type: nextjs` with `- Build & layout: Next 16, App Router, cacheComponents: true`;
    `- Project type: php-wordpress-plugin` with `- Build & layout: PHP >=8.1, PHPUnit`.
  - **Android library with a sample app**: when every `com.android.application` module depends on a sibling
    `com.android.library` module (`implementation(project(":lib"))`) — this catalog's reference library layout,
    `lib/` + Compose `app/` — the value is `android-library`, with the sample module recorded on an indented
    sub-line for information (`- sample app: app/`), **not** `multiple` (reporting `multiple` here makes the front door
    ask which module to bootstrap for what is a single library project).
  - **Multiple modules of different types**: when the repository contains more than one module with a distinct
    project type (e.g. a backend plus a mobile client, or two independent Android apps), the line's value is
    `multiple`, followed by one `<module-path>: <type>` entry per module on indented sub-lines, e.g.:
    ```
    - Project type: multiple
      - backend/: java-springboot
      - android/: android-app
    ```
  - Say `unknown` only when nothing in Step 5 matched anything at all; say `other` when something clearly
    matched (a manifest and/or source-level signal was found) but that stack has no key in the table above.
- If Step 6 found a connected documentation MCP, include a **Related documentation** section listing each
  relevant page found (title, link, one-line summary) — or a one-line note that none was relevant/connected.
  This is what a later `iru-plan` step should draw on for additional context beyond the codebase and ticket.
- Include a **Related past implementation plans** section covering both the `.archive/` check from Step 4 and,
  for a Jira ticket, the attached-plan check from Step 3: name any archived or downloaded plan(s) used as
  precedent (file name/source — local `.archive/` vs. downloaded from the ticket/epic/linked ticket — its
  original topic, and what carries over — task breakdown, granularity, or approach), or state explicitly that
  neither source had anything relevant (`.archive/` doesn't exist or nothing in it was relevant, and no
  `implementation_plan_*.md` attachment was found). This is what a later `iru-plan` step should draw on to ground
  a new plan's structure in a proven prior one.
- If a ticket was explored: restate the task in your own words, list the specific files/classes/methods
  relevant to it, explain how the current code behaves in the area the ticket touches, and flag anything
  ambiguous or missing from the ticket that would block implementation. For a Jira ticket, also name its epic
  (if any) and any linked/related tickets fetched in Step 3, with a one-line summary of what each adds (a shared
  constraint from the epic, what a "blocks"/"relates to" link actually implies here) — or state plainly that the
  ticket has no epic and no links if that's the case.
- If codebase-only: summarize the architecture areas covered and anything notable found (e.g. inconsistencies,
  undocumented behavior, missing test coverage) relevant to general orientation.
- Do not propose an implementation plan or start editing code — if the user wants that next, they will ask for
  it (e.g. via planning mode) as a separate step.
