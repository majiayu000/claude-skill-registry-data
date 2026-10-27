---
name: iru-setup-ionic-app
description: "Invoked as /iru-setup-ionic-app with optional key: value args, usually by iru-setup-typescript-repository. Scaffolds an Ionic (Angular or React) hybrid app with the Ionic CLI, then adds Vitest coverage, ESLint, Prettier, Playwright UI tests with accessibility checks, a Maestro flow and optional Sonar."
model: sonnet
---

# Setup Ionic App

Scaffold a new Ionic app (Angular or React flavor) at the repository root via the real `@ionic/cli` `start`
schematic — not a hand-rolled reimplementation of it — then add this catalog's house testing (Vitest + coverage),
linting (ESLint + Prettier), end-to-end (Playwright web smoke test, Maestro on-device flow skeleton), and
optional SonarQube/SonarCloud wiring on top. Every quirk and default below was confirmed by actually running these
exact commands against both flavors while building this skill (September 2026, `@ionic/cli` 7.2.1, `@ionic/angular`
9.0.4, `@ionic/react` 9.0.4, Capacitor 8.5.2, Node 24) — see the inline notes for what changed from the naive
command sequence.

## Step 0 — Resolve inputs

This skill can be invoked stand-alone (`/iru-setup-ionic-app`) or as a step inside another skill (e.g. a future
`iru-setup-ionic-app-repository` or the catalog's `iru-setup-repository` front door), which resolves these same
inputs itself and passes them through `args` as `key: value` lines, one per line, e.g.:

```
framework: angular
app-name: my-app
app-id: com.example.myapp
description: A small example Ionic app.
license: MIT
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
open-source: yes
distribution: store
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_my-app
sonar-host-url: https://sonarcloud.io
add-android: yes
add-ios: yes
visibility: public
ci: yes
accessibility: enforce
on-existing: ask
mode: new
```

Parse any such lines from `args` now. Every field found here is resolved — skip asking about it in Step 2. Only
fields genuinely missing from `args` still need a question. If `args` is absent or doesn't look like this format,
treat everything as unset and ask normally.

Recognized keys: `framework` (`angular`/`react`), `app-name`, `app-id`, `description`, `license`, `developer-name`,
`developer-email`, `organization-url`, `open-source` (`yes`/`no`), `distribution` (`none`/`internal`/`store` — this
catalog's shared app-distribution vocabulary; this skill only records the answer for Step 11's report and for a
later `iru-setup-typescript-github-workflows` run, since store submission/signing is that skill's job, not this
one's), `sonar` (`cloud`/`self-hosted`/`none`) plus, only when `sonar` is `cloud`/`self-hosted`,
`sonar-organization`/`sonar-project-key`/`sonar-host-url`, `add-android` (`yes`/`no`), `add-ios` (`yes`/`no`),
`visibility` (`public`/`private`/`internal` — the GitHub repository's visibility, used only to key Step 2's Sonar
recommendation), `ci` (`yes`/`no` — whether the run invoking this skill generates GitHub Actions workflows at all;
only consulted by Step 2's Sonar question), `accessibility` (`enforce`/`report`/`off`/`none`, default `enforce` — the UI
tests' automated accessibility level, written to `.ui-quality.yml` in Step 8), `on-existing`
(`ask`/`keep`/`update`/`replace`, default `ask` — how Step 1 treats each pre-existing artifact; meant for scripted
runs), and `mode` (`new`/`existing`).

`mode: existing` is this catalog's shared signal that this run is an **update**: Step 1 announces it as such, but
still warns and asks per pre-existing artifact unless `on-existing` says otherwise — it never means "update
silently".

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (axe-core and the framework's accessibility lint rules), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — semantic landmarks, `aria-label` on icon-only `ion-button`s, `alt` on images, `rem`/relative font sizes, `prefers-reduced-motion` guards — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

## Step 1 — Survey the repository

Check, at the repository root, whether `ionic.config.json`, `capacitor.config.ts`/`capacitor.config.json`, or a
`package.json` that already depends on `@ionic/angular` or `@ionic/react` exists.

- **None exist**: say "Scaffolding the Ionic app **from scratch**." and skip straight to Step 2. There is nothing
  to preserve, and nothing blocks scaffolding directly into the repository root (Step 4 covers the one case that
  needs care — a non-empty root).
- **Any exists** (or `mode: existing`): say "**Updating an existing Ionic project** — found: <list with paths>."
  Detect the framework from the existing `package.json` (`@ionic/angular` present → `angular`; `@ionic/react`
  present → `react`) instead of asking Step 2's framework question. The existing scaffold itself
  (`package.json`'s dependencies, `ionic.config.json`, `capacitor.config.ts`, `src/`, `android/`/`ios/`) is never
  regenerated: `ionic start` refuses to scaffold into a non-empty directory (see Step 4), so a genuine fresh
  scaffold is only possible after the user removes or relocates the existing project files themselves — offer that
  as a **Stop** option ("end now; clear the project yourself and re-run for a fresh scaffold") rather than doing
  it. Steps 4–5 are skipped for an existing project. Then survey the tooling artifacts Steps 6–10 own — the
  coverage config (`angular.json`'s `test` options or `vite.config.ts`'s `test.coverage`) and the
  `test`/`coverage`/`typecheck`/`format`/`e2e` scripts, `eslint.config.js`'s `ignores` and
  `eslint-config-prettier` entry, `.prettierrc.json`, `playwright.config.ts`/`e2e/` (including
  `e2e/support/ui-screenshots.ts`), `.ui-quality.yml` at the repository root, `.maestro/smoke.yaml`,
  `sonar-project.properties` — and resolve one action per artifact that already exists:
  - **`on-existing` is `keep`/`update`/`replace`**: apply it to every artifact without asking (still print the
    warning).
  - **Otherwise**: ask with `AskUserQuestion`, batching up to 4 artifacts per call (one question each), naming any
    concrete contradiction with this run's choices (e.g. "`eslint.config.js` doesn't ignore `coverage/`", "a
    `sonar-project.properties` exists but you chose `sonar: none`"):
    - **Update (Recommended)** — merge: add what's missing and correct outdated parts using this skill's
      templates as reference (missing coverage reporters, ignores, scripts, the Playwright `webServer` block),
      keeping everything this skill doesn't own. The user reviews a diff; customizations survive, but a customized
      part this skill owns may be rewritten.
    - **Keep as is** — leave it untouched and skip the step that would write it. Nothing customized changes, but
      it may stay out of date or disagree with this run's choices — Step 11 lists each mismatch.
    - **Replace** — regenerate it from this skill's template; every customization in it is lost (recoverable only
      from git history).
    - **Stop** (first batch only) — as described above; leave everything untouched and end here.
  - Defer the `sonar-project.properties` question until Step 2 resolves `sonar`: with `sonar: none`,
    Update/Replace mean removing the file and Keep leaves it as a reported mismatch.

## Step 2 — Collect the required inputs

For any field Step 0 already resolved from `args`, use that value directly and don't ask about it again. For
everything else, ask the user directly (plain conversation for free text; `AskUserQuestion` for the bounded
choices below):

When an existing `package.json` (or app config such as `app.json`/`angular.json`) already supplies an identity
value Step 0 didn't — typical in `mode: existing`, where orchestrators omit identity keys — use it as resolved and
confirm it in one line instead of asking.

- **framework** (`AskUserQuestion`, bounded) — **Angular** or **React**. State up front that this skill scaffolds
  on an **Ionic 9 + Capacitor 8 baseline with no Cordova integration and no Ionic Appflow/Live Update dependency**
  (Appflow is a paid service this catalog doesn't assume); if the user later wants over-the-air updates, point them
  at **Capgo** or **Capawesome** rather than Appflow — neither is wired up by this skill, it's a pointer for later.
- **app-name** — the project/directory name, kebab-case, e.g. `my-app`. Used both as the scaffold's directory name
  and (lowercased) as `ionic.config.json`'s `name` and `capacitor.config.ts`'s `appName`.
- **app-id** — the reverse-DNS application id, e.g. `com.example.myapp`. The Ionic starter always seeds
  `io.ionic.starter` regardless of what's asked here (confirmed) — Step 4 overwrites it with this real value via an
  explicit `cap init` re-run.
- **description** — one line, used in `package.json`'s `description` field (the starter's own default is the
  generic `"An Ionic project"` — replace it).
- **Developer name**, **developer email**, **organizationUrl** — populate `package.json`'s `author` field (the
  starter's template doesn't include one; this skill adds it).

Then, unless Step 0 already resolved a `license` value from `args`, ask about the **license** with
`AskUserQuestion` (mirrors every other setup skill in this catalog):

- MIT License (recommended for apps) — SPDX id `MIT`
- Apache License 2.0 — SPDX id `Apache-2.0`
- No license (proprietary / all rights reserved) — SPDX id `UNLICENSED`, and `"private": true` is set in
  `package.json` regardless of `distribution`
- Other — ask for the SPDX identifier directly afterward

If a license is chosen (anything but "No license"), remind the user in Step 11 to also add a matching `LICENSE`
file at the repository root if one doesn't exist yet — `iru-check-license` can verify/backfill source headers
against it once it's there.

Then resolve `open-source`, `distribution`, and `sonar` — skip any of the three Step 0 already resolved from
`args`. When invoked stand-alone with none of them pre-resolved, ask `open-source` *first* (`AskUserQuestion`:
Yes/No) and derive the recommended defaults for the other two from that answer, per this catalog's shared
convention:

- **open-source** — is this repository open source? Yes / No.
- **distribution** — how (if at all) does this app reach real devices? `none` (never built for a device — web/PWA
  only, or purely exploratory), `internal` (sideloaded/ad hoc/TestFlight-internal builds for a private team), or
  `store` (published to Google Play and/or the App Store). Default **`store`** when open-source is Yes; when not
  open source, ask with **`internal`** recommended (a closed-source app is rarely meant for the public stores).
  This skill records the answer only — no store/signing config is generated here; `iru-setup-typescript-github-workflows`
  reads it later to decide whether to generate release/store-upload jobs.
- **sonar** — whether to wire up a SonarQube/SonarCloud scan via `sonar-project.properties` (Step 10). The
  recommendation keys on both `open-source` and `visibility`. If `visibility` wasn't supplied via `args`, resolve
  it only now (only when this question is actually asked): `gh repo view --json visibility -q .visibility` when the
  repository has a GitHub remote (lowercase the result and tell the user), otherwise ask **Public** / **Private**
  (Public recommended when open source); `internal` counts as private. If `open-source: yes` but `visibility` is
  `private`/`internal`, warn about the contradiction and ask which is right. Recommend **SonarCloud** (`cloud`)
  only when the repository is public **and** open source; otherwise state that SonarCloud is free only for public
  open-source projects (per its current pricing — a private project needs a paid plan) and recommend **None**
  (`none`), offering **self-hosted SonarQube** as the second option. If `ci: no` was supplied via `args`, say
  plainly that no CI workflow would send reports — analysis would only run when someone runs the scanner manually
  with a token — and recommend **None**; if the user still picks `cloud`/`self-hosted`, write
  `sonar-project.properties` anyway and say so in Step 11:
  - `cloud` — ask for the `sonar.organization` key, offering `<owner>-github` (the owner parsed from `git remote
    get-url origin`) as the suggested default. Default `sonar.projectKey` to `<owner>_<repo>` and `sonar.host.url`
    to `https://sonarcloud.io`, confirming both with the user.
  - `self-hosted` — ask for `sonar.host.url` directly, plus `sonar.organization` only if that server has
    organizations enabled, and `sonar.projectKey`.
  - `none` — skip Step 10 entirely.

Finally, ask two independent Yes/No questions with `AskUserQuestion` (unless Step 0 already resolved `add-android`/
`add-ios`), each defaulting to **Yes**:

- **add-android** — add the Android native platform now (`npx cap add android`, Step 5)? Requires the Android SDK
  (`$ANDROID_HOME`/`$ANDROID_SDK_ROOT`) to be installed for the platform to actually build later — note this if it
  isn't detected, but still scaffold the platform folder; building is a later concern.
- **add-ios** — add the iOS native platform now (`npx cap add ios`, Step 5)? **Only offer this question on
  macOS** (`uname -s` = `Darwin`) — on any other OS, skip it silently and note in Step 11 that iOS can only be
  added from a Mac.

In the same `AskUserQuestion` call, unless Step 0 resolved it, ask **accessibility**: "Support accessibility and assistive technologies?" — **Enforce (Recommended)** (axe violations fail the UI tests) / **Report only** (listed, never
failing) / **Off** (not run; the coding defaults still apply).

## Step 3 — Look up dependency versions

Look up every version below at run time; the table is this skill's fallback for when a lookup fails, and records
what was actually observed on the npm registry in September 2026 while building and verifying this skill.

| Package | Lookup | September 2026 fallback |
|---|---|---|
| `@ionic/cli` (used via `npx`, not installed as a dependency) | `npm view @ionic/cli version` | `7.2.1` |
| `@capacitor/android` | `npm view @capacitor/android version` — **must match the `@capacitor/core` version the starter already installed** (see the caveat below), not necessarily the bare registry `latest` | `8.5.2` |
| `@capacitor/ios` | `npm view @capacitor/ios version` — same caveat | `8.5.2` |
| `@vitest/coverage-v8` | see the caveat below — **do not** just take `npm view @vitest/coverage-v8 version` | `4.1.11` (Angular/React starters both currently ship `vitest ^4.x`) |
| `prettier` | `npm view prettier version` | `3.9.7` |
| `eslint-config-prettier` | `npm view eslint-config-prettier version` | `10.1.8` |
| `@playwright/test` | `npm view @playwright/test version` | `1.63.0` |
| `http-server` (serves the built web output for Playwright, Step 8) | `npm view http-server version` | `14.1.1` |

**`@capacitor/*` platform-package caveat:** the blank starter's `ionic start` run already installs
`@capacitor/core`/`@capacitor/cli` at a specific pinned version (observed: exact `8.5.2`, no `^`/`~` — the starter
pins with `-E`). Read the *installed* `@capacitor/core` version from the freshly scaffolded `package.json`
(Step 4) and install `@capacitor/android`/`@capacitor/ios` at that **same exact version** — Capacitor's platform
packages are versioned in lockstep with core and a mismatch is a supported-but-discouraged combination.

**`@vitest/coverage-v8` caveat:** the registry's bare `latest` tag (`5.0.1` observed) is newer than the `vitest`
major the Ionic starters currently ship (`^4.0.8`/`^4.0.0` observed in both flavors' `package.json`), and
`@vitest/coverage-v8@5` will not satisfy a `vitest@^4` peer dependency. Read the *installed* `vitest` version from
the freshly scaffolded `package.json` and install `@vitest/coverage-v8` pinned to that same major (e.g. `npm view
@vitest/coverage-v8@4 version` when `vitest` is on the `4.x` line) instead of the bare `latest`.

## Step 4 — Scaffold the app

Run, from the repository root:

```
npx @ionic/cli@latest start <app-name> blank --type=<angular-standalone|react> --no-git --no-deps --no-interactive --confirm
```

- `--type=angular-standalone` for the Angular flavor, `--type=react` for React.
- `--no-interactive --confirm` are required to get a fully non-interactive run — without them the CLI prompts to
  create a free Ionic account at the end (confirmed: `--confirm` auto-answers that and every other yes/no prompt
  the CLI would otherwise raise; `--no-interactive` suppresses spinners/prompts generally). `--no-git` skips the
  CLI's own `git init` — this repository already has its own git history. `--capacitor` is **not needed** — the
  current CLI enables the Capacitor integration by default for the blank starter even without it (confirmed).
- **`--no-deps` does not fully skip dependency installation** (a real quirk, not documented behavior): it only
  skips the starter template's *own* upfront `npm install`. Immediately afterward, `ionic start` unconditionally
  runs `ionic integrations enable capacitor`, which itself runs several `npm i` commands to add
  `@capacitor/core`/`@capacitor/cli`/`@capacitor/app`/`@capacitor/haptics`/`@capacitor/keyboard`/
  `@capacitor/status-bar` — and because `node_modules` doesn't exist yet at that point, npm resolves and installs
  the **entire** dependency tree (confirmed: ~600–685 packages) to satisfy those few `npm i` calls. By the time
  `ionic start` finishes, `node_modules` is already fully populated — a separate `npm install` afterward is a
  no-op safety net, not a required step.
- **The repository root is not empty** (an existing `.git`, `CLAUDE.md`, `docs/`, etc.): `ionic start <app-name>
  ...` always creates its **own** new directory named `<app-name>` and fails outright (`EEXIST`) if a path with
  that name already exists — confirmed it cannot scaffold in place into `.` or into an already-existing (even
  empty) directory, unlike `npm create vite@latest`/`ng new --directory=.`. When the repository root itself
  should become the app (the common case for this skill), scaffold into a hidden sibling directory and move every
  generated entry — including dotfiles — up into the repository root, then remove the now-empty temp directory:
  ```
  npx @ionic/cli@latest start .ionic-scaffold-tmp blank --type=<...> --no-git --no-deps --no-interactive --confirm
  mv .ionic-scaffold-tmp/* .ionic-scaffold-tmp/.[!.]* .   # zsh matches hidden entries via this glob directly;
                                                            # under bash, run `shopt -s dotglob` first
  rmdir .ionic-scaffold-tmp
  ```
  (Confirmed working exactly as shown — every dotfile, `node_modules`, and `package-lock.json` moved up cleanly.)
  If the root genuinely has other unrelated content already, ask the user whether to scaffold into a named
  subdirectory instead of the root, rather than overwriting anything.
- Confirms the following are already fully wired up by the starter itself — **do not** recreate them:
  - `capacitor.config.ts` with `appId: 'io.ionic.starter'` and the correct default `webDir` per flavor (Angular:
    `'www'`; React: `'dist'` — confirmed, matches each flavor's own build output directory).
  - Angular: `eslint.config.js` (ESLint 10 flat config with `angular-eslint`'s recommended presets already
    applied) and the `@angular/build:unit-test` **Vitest**-backed test target in `angular.json` (`ng test` — no
    Karma anywhere; confirmed the current Angular CLI standalone starter ships Vitest by default).
  - React: `eslint.config.js` (flat config with `@eslint/js`, `typescript-eslint`, `eslint-plugin-react-hooks`,
    `eslint-plugin-react-refresh`) and a Vitest test setup in `vite.config.ts` (`test.unit` script → bare
    `vitest`, confirmed **not** `vitest run` — it launches watch mode; always invoke `vitest run` explicitly
    instead of `npm run test.unit` in CI/scripts).
- **Overwrite the placeholder app id.** The scaffolded `capacitor.config.ts` always has `appId: 'io.ionic.starter'`
  regardless of what was asked in Step 2 (confirmed — `ionic start` doesn't take an app-id argument at all). Fix
  it with a real `cap init` re-run rather than hand-editing the file, so both `capacitor.config.ts` and
  `android/`/`ios`' generated native project files (once added in Step 5) pick up the real id consistently:
  ```
  npx cap init <app-name> <app-id> --web-dir <www-or-dist>
  ```
  Run this **before** Step 5 adds any native platform — `cap init` only needs to be re-run once, immediately after
  scaffolding.
- Update `package.json`'s `"description"`, add the `"author"` field from Step 2, and set `"private": true` if "No
  license" was chosen in Step 2. The starter's own `package.json` has neither `description` (beyond the fixed "An
  Ionic project" placeholder) nor `author`.

## Step 5 — Add native platforms

For each of `add-android`/`add-ios` resolved Yes in Step 2:

**Android:**
```
npm install @capacitor/android@<capacitor-version>   # same exact version as the installed @capacitor/core — Step 3
npx cap add android
```
- **JDK caveat (confirmed the actual failure mode):** the Gradle sync this command triggers fails with `Unsupported
  class file major version 70`/similar if `JAVA_HOME` (or the `java` on `PATH`) resolves to a JDK newer than what
  the bundled Gradle wrapper version supports (observed failing on JDK 26; succeeding cleanly on JDK 21). Before
  running `cap add android` or `cap sync android`, make sure `JAVA_HOME` points at a **JDK 17 or 21** install —
  `/usr/libexec/java_home -V` (macOS) lists what's available; export `JAVA_HOME`/`ANDROID_HOME`/`ANDROID_SDK_ROOT`
  explicitly rather than relying on whatever the shell's default `java` happens to be. This is an environment
  prerequisite, not something this skill's generated files can paper over — note it plainly in Step 11's report.
- Confirmed `npx cap sync android` (used later, e.g. by CI or `iru-typescript-code-quality`) completes in well
  under a second once the JDK above is correct — most of `cap add android`'s own time is the one-time Gradle
  distribution download.

**iOS (macOS only):**
```
npm install @capacitor/ios@<capacitor-version>   # same exact version as the installed @capacitor/core
npx cap add ios
```
- **Confirmed Capacitor 8's iOS platform needs no CocoaPods.** `cap add ios` succeeded end-to-end on a machine
  with no `pod` binary installed at all — Capacitor 8 integrates iOS plugins via **Swift Package Manager**
  (writes `ios/App/CapApp-SPM/Package.swift`), not a `Podfile`. If a project's plugins later require CocoaPods
  specifically, that's a plugin-level exception, not the default path — don't assume CocoaPods needs installing
  first.
- Building/archiving the generated Xcode project still needs Xcode itself (`xcodebuild -version` to confirm) —
  that step is out of scope for this skill; it only adds the platform.

If either question was answered No (or iOS was skipped for not being on macOS), note in Step 11 that the platform
can be added later with the same two commands.

## Step 6 — Testing: Vitest with coverage

Install the coverage package resolved in Step 3, then wire it in per flavor.

**Angular** — patch the `test` target's `options` in `angular.json` (the project key is always `app` regardless of
`<app-name>` — confirmed the starter's schematic hardcodes it, it is **not** derived from the name passed to
`ionic start`):

```json
"options": {
  "tsConfig": "tsconfig.spec.json",
  "buildTarget": "::development",
  "setupFiles": ["src/test-setup.ts"],
  "coverage": true,
  "coverageReporters": ["text", "lcov"]
}
```

Confirmed `ng test --no-watch` then writes coverage to **`coverage/app/lcov.info`** (the fixed `app` project key,
not `coverage/<app-name>/lcov.info`) — this is the path `sonar.javascript.lcov.reportPaths` must point at in
Step 10, and what a CI workflow should upload as an artifact. `ng test --help` also exposes `--coverage`/
`--coverage-reporters` as one-off CLI flags if a caller wants coverage without touching `angular.json`, but baking
it into the config (as above) means a bare `ng test`/`npm test` always produces it, matching this catalog's other
setup skills' preference for config over remembered flags.

The Angular starter's `package.json` only ships `"test": "ng test"` — add the `coverage` script CI calls by name
(the `build.yml` generated by `iru-setup-typescript-github-workflows` runs `npm run coverage` for every flavor and
fails with "Missing script" otherwise), pinned to `--no-watch` so it exits in CI instead of entering the
builder's TTY watch mode; coverage is already baked in above, so the extra `--coverage` flag is only there to
keep the script self-describing:

```json
"coverage": "ng test --no-watch --coverage",
```

**React** — add a `coverage` block to `vite.config.ts`'s existing `test` key:

```ts
test: {
  globals: true,
  environment: 'jsdom',
  setupFiles: './src/setupTests.ts',
  coverage: {
    provider: 'v8',
    reporter: ['text', 'lcov'],
    reportsDirectory: './coverage',
  },
},
```

Confirmed `npx vitest run --coverage` then writes **`coverage/lcov.info`** directly (no per-project subfolder,
unlike Angular). Also rewrite `package.json`'s scripts so `npm test`/`npm run coverage` are non-interactive and
reproducible in CI, since the starter's own `"test.unit": "vitest"` launches **watch mode** (confirmed — it never
exits on its own):

```json
"test": "vitest run",
"coverage": "vitest run --coverage",
```

**Both flavors** — add a `typecheck` script, the last of the fixed script names (`build`, `test`, `coverage`,
`lint`, `format`, `typecheck`) that `iru-setup-typescript-github-workflows`'s `build.yml` invokes and that neither
Ionic starter ships:

```json
"typecheck": "tsc --noEmit"
```

- **React**: the starter's own `build` script is `tsc && vite build` against a root `tsconfig.json` that already
  sets `"noEmit": true` and includes `src`, so `tsc --noEmit` at the root checks exactly what the build checks.
- **Angular**: the root `tsconfig.json` is a solution-style file with no `include`, so use the two project files
  the starter generates instead — `"typecheck": "tsc --noEmit -p tsconfig.app.json && tsc --noEmit -p
  tsconfig.spec.json"` — the same shape `iru-setup-angular-web` Step 5 uses; TypeScript only, templates are
  checked by `ng build`'s AOT compile that `npm run build`/`e2e` already run.

The `typecheck` script was added to close the CI-contract gap after this skill's verification pass and is **not
confirmed end-to-end here** — run it once on the fresh scaffold and note the outcome in Step 11's report.

## Step 7 — Linting and formatting: ESLint + Prettier

Both flavors already ship a working ESLint 10 flat config (Step 4) — don't replace it, extend it:

- Add `coverage`, `android`, `ios`, and the framework's web-build output (`www` for Angular, `dist` for React) to
  the config's `ignores` array. **Required, not optional**: confirmed running the bare starter's own `eslint .`
  (React) reports warnings from files under `coverage/lcov-report/*.js` once coverage has been generated even
  once, because the starter's default `ignores` only lists `['dist', 'cypress.config.ts']`.
- **Known starter lint gap (React only, confirmed):** the blank React starter's own
  `src/components/ExploreContainer.tsx` fails `typescript-eslint`'s `recommended` ruleset out of the box
  (`@typescript-eslint/no-empty-object-type` on its empty `ContainerProps` interface) — `npm run lint` is red
  immediately after scaffolding, before any of this skill's or the user's own code exists. Fix it in place
  (`interface ContainerProps {}` → `type ContainerProps = object;`, or add the specific rule as a one-line
  disable) rather than silently leaving a freshly scaffolded project failing lint; call this out in Step 11's
  report either way so the user isn't surprised. The Angular flavor's starter files lint clean as shipped.

Install and configure Prettier (the starter ships none):

```
npm install -D prettier eslint-config-prettier   # versions from Step 3
```

`.prettierrc.json`:
```json
{
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "all"
}
```

Add `eslint-config-prettier` as the **last** entry in `eslint.config.js`'s config array (turns off any ESLint
formatting rule that would conflict with Prettier) — confirmed no rule conflicts exist in either starter's default
rule set once added. Add `package.json` scripts:
```json
"format": "prettier --check .",
"format:fix": "prettier --write ."
```
Note in Step 11 that `prettier --check .` will report the starter's own pre-existing files as unformatted on the
very first run (confirmed on both flavors) — this is expected once, run `format:fix` once right after scaffolding
rather than treating it as a defect.

## Step 8 — Playwright end-to-end (web build)

Ionic's blank starters ship no Playwright config; the React flavor ships **Cypress** instead (`test.e2e`: `cypress
run`, plus a `cypress/` directory and the `cypress` devDependency) and the Angular flavor ships neither. Ask once
(`AskUserQuestion`, skip if `args` already answered `e2e-tool`) only when the React flavor's Cypress setup is
present: **replace Cypress with Playwright** (recommended — keeps every flavor's web e2e on one tool, and this
catalog's other TypeScript setup skills standardize on Playwright) or **keep both**. On "replace", remove the
`test.e2e` script, the `cypress` devDependency, `cypress.config.ts`, and the `cypress/` directory.

Install and scaffold, either way:
```
npm install -D @playwright/test http-server   # versions from Step 3
npx playwright install --with-deps chromium
```

`playwright.config.ts` — serves the **built** static output (confirmed this is faster and more reliable than
driving `ionic serve`'s dev server, and matches what a CI workflow's `build` job would already have on disk):

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  webServer: {
    command: 'npx http-server <web-dir> -p 4300',
    url: 'http://localhost:4300',
    reuseExistingServer: false,
  },
  use: { baseURL: 'http://localhost:4300' },
});
```

`<web-dir>` is `www` (Angular) or `dist` (React) — the same directory `npm run build` writes to (confirmed for
both flavors). `e2e/smoke.spec.ts`:

```ts
import { test, expect } from '@playwright/test';

test('home page loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Ionic/i);
});
```

Add a `package.json` script: `"e2e": "npm run build && playwright test"`. Confirmed this exact config/test passes
against both flavors' built output.

**UI contract.** The catalog's UI contract (repeated in `iru-typescript-code-one-task/reference/ui-contract.md`)
makes every screen and component test capture its states into
`<repo root>/.ui-screenshots/<kind>/<Id>/<state>--<direction>--<theme>.png` and run axe at the level
`.ui-quality.yml` sets. Verified on the Angular flavor (Ionic 9 blank starter, Playwright 1.64.1,
`@axe-core/playwright` 4.14.0); the React flavor follows the same steps, unverified.

1. Write `.ui-quality.yml` at the repository root, with `accessibility` from Step 0/2 (an existing file follows
   Step 1's decision — **Update** sets only `accessibility` when `args` supplied it and adds missing keys):

   ```yaml
   # .ui-quality.yml — at the repository root; written by the iru-setup-* scaffolds, read by the coding and test skills.
   accessibility: enforce      # enforce: violations fail the UI tests | report: listed, never failing | off: not run | none: opted out entirely
   directions: [ltr, rtl]      # screenshot matrix directions
   themes: [light, dark]       # screenshot matrix themes
   ```

2. `npm install -D @axe-core/playwright` (version from `npm view`, fallback `4.14.0`), and write
   `e2e/support/ui-screenshots.ts` with exactly the content of this skill's `reference/ui-screenshots.ts` (then run
   the project's Prettier on it).

3. Extend `e2e/smoke.spec.ts` with the screen matrix (keep the title test):

   ```ts
   import { captureUiMatrix } from './support/ui-screenshots';

   test('HomePage across the matrix', async ({ page }, testInfo) => {
     await captureUiMatrix(
       page,
       { kind: 'screen', id: 'HomePage', state: 'default' },
       async () => {
         await page.goto('/');
         await expect(page.locator('ion-title').first()).toBeVisible();
         return page;
       },
       { accessibility: { testInfo } },
     );
   });
   ```

   Dark mode needs no extra code: the starter's global stylesheet already imports Ionic's
   `palettes/dark.system.css`, which follows `prefers-color-scheme` (keep it — don't switch to `dark.class.css`
   without adding an `onVariant` hook that toggles the class).

4. **Make the starter pass its own check.** Verified: the blank starter fails axe with `meta-viewport`
   (`src/index.html`'s viewport has `minimum-scale=1.0, maximum-scale=1.0, user-scalable=no`),
   `link-in-text-block` (the "UI Components" link has `text-decoration: none`) and, in light theme,
   `color-contrast` (`#8c8c8c` paragraph text). Fix all three, in the starter's container stylesheet (Angular:
   `src/app/home/home.page.scss`; React: `src/components/ExploreContainer.css`) and `index.html`:
   - viewport → `content="viewport-fit=cover, width=device-width, initial-scale=1.0"` (zoom must stay possible);
   - `#container a { text-decoration: underline; }`;
   - `#container p { color: #666666; }` plus `@media (prefers-color-scheme: dark) { #container p { color: #a6a6a6; } }`;
   - and for right-to-left, `left: 0; right: 0;` in `#container` → `inset-inline: 0;`.
   With these, the spec passes at `accessibility: enforce` and writes the four
   `screen/HomePage/default--{ltr,rtl}--{light,dark}.png` captures.

Components added later get Playwright component tests through a gallery page (Playwright's built-in `mount()`
fixture) as described in `iru-typescript-code-one-task/reference/ui-implementation.md` — the coding skill adds that
when the first component task needs it; the scaffold keeps to the screen spec. Note in Step 11 that `npx playwright install --with-deps chromium` downloads
real browser binaries — skip it (and note why) if run offline, without sudo for the `--with-deps` system package
step, or in a sandboxed environment without network access.

## Step 9 — Maestro flow skeleton

Write `.maestro/smoke.yaml` — a minimal on-device/emulator smoke flow, genericized with `<app-id>` from Step 2:

```yaml
appId: <app-id>
---
- launchApp
- assertVisible:
    text: ".*"
```

This is a skeleton only, meant to be extended once the app has real screens to assert against — replace the
generic `assertVisible` with a real element once one exists. **Unverified locally**: the Maestro CLI (`maestro
test .maestro/smoke.yaml`) needs a running emulator/simulator or connected device and was not installed in the
environment this skill was verified in — only the YAML's shape (matching Maestro's documented flow syntax) is
confirmed correct, not an actual `maestro test` run.

## Step 10 — `sonar-project.properties` (only when `sonar` ≠ `none`)

```
sonar.organization=<sonar-organization>
sonar.projectKey=<sonar-project-key>
sonar.sources=src
sonar.tests=<test-inclusions-path>
sonar.test.inclusions=<test-glob>
sonar.javascript.lcov.reportPaths=<lcov-path>
sonar.exclusions=android/**,ios/**,e2e/**,coverage/**,<web-dir>/**
```

Resolve the four placeholders per flavor (confirmed values from Steps 4–8):

| Placeholder | Angular | React |
|---|---|---|
| `<test-inclusions-path>` | `src` | `src` |
| `<test-glob>` | `**/*.spec.ts` | `**/*.test.ts,**/*.test.tsx` |
| `<lcov-path>` | `coverage/app/lcov.info` | `coverage/lcov.info` |
| `<web-dir>` | `www` | `dist` |

Omit the `sonar.organization` line entirely for `sonar: self-hosted` servers without organizations enabled (per
Step 2).

## Step 11 — Report and warn

Start by repeating the mode announced in Step 1 (**scaffolded from scratch** or **updated an existing Ionic
project**, with Steps 4–5 skipped). Summarize: the resolved framework, app name, app id (and that it replaced the starter's `io.ionic.starter`
placeholder via `cap init`), license, and whether `open-source`/`distribution`/`sonar` were resolved from `args`
or asked.

State explicitly what was included versus omitted, and why:

- **`distribution`**: `none`/`internal`/`store` — note that this skill only records the value; no store/signing
  configuration was generated here, and `iru-setup-typescript-github-workflows` is where that eventually happens.
- **`sonar`**: `cloud`/`self-hosted`/`none` — if `cloud`/`self-hosted`, confirm `sonar-project.properties` was
  written with the resolved values and the correct per-flavor `lcov` path from Step 10's table; if `none`, note
  this is expected unless the repository is public and open source (SonarCloud is free only for public open-source
  projects) or the user explicitly chose it. State the `visibility` used and where it came from (`args`, `gh`, or
  the user); if `ci: no` was supplied and Sonar was still configured, say no CI step sends reports.
- **Per artifact** (update runs): the action actually taken for each pre-existing artifact — **created / updated /
  replaced / kept as is / removed** — and, for every kept one, each mismatch with this run's choices.
- **Android/iOS platforms**: which were added (Step 5) versus deliberately skipped (No answer, or iOS on a
  non-macOS host) — for anything skipped, repeat the exact two commands needed to add it later.

Then report, explicitly:

- Whether the repository root was empty (direct scaffold) or the scaffold-into-a-temp-dir-and-move-up workaround
  from Step 4 was used.
- That `npm install`/`npm run build`/`ng test`/`vitest run --coverage`/`npm run lint`/`npm run format` were the
  actual verified commands (or their equivalents), that `npm run typecheck` (and the Angular flavor's `npm run
  coverage`) were added afterwards for the CI contract and whether they were actually run this time, and, if any
  failed locally while running this skill, what the fix was (e.g. the JDK 17/21 requirement for `cap add android`/`cap sync android` — Step 5; the React starter's
  pre-existing `ExploreContainer.tsx` lint error — Step 7).
- The React flavor's Cypress-vs-Playwright decision from Step 8, and that Playwright's browser binaries
  (`npx playwright install --with-deps chromium`) were or weren't actually downloaded.
- That the Maestro flow (Step 9) is an unverified skeleton, not a confirmed-passing on-device test.
- The UI contract (Step 8): `.ui-quality.yml` with its action (**created / updated / replaced / kept as is**) and
  the `accessibility` level written, the helper and screen spec written, the starter accessibility fixes applied,
  and the screenshots the verification run produced (or why it couldn't run). `.ui-screenshots/` must be
  gitignored (`iru-setup-typescript-gitignore` adds it).

Finish with an explicit **Warn explicitly** block:

- **Review every generated/patched file before committing** — `capacitor.config.ts`, `angular.json`/
  `vite.config.ts`'s coverage block, `eslint.config.js`'s new `ignores`, and `package.json`'s scripts all changed
  from the raw `ionic start` output.
- If `sonar: cloud`/`self-hosted` was chosen, a `SONAR_TOKEN` secret and an actual SonarCloud/SonarQube project
  matching `sonar.projectKey` still need to exist before any CI-driven scan succeeds — this skill only writes
  `sonar-project.properties`.
- If `distribution: store` was chosen, real Google Play/App Store Connect credentials and signing material still
  need to exist before any later release workflow can actually publish — nothing here creates or stores them.
- No `.gitignore` was written by this skill — `node_modules/`, `www/`/`dist/`, `coverage/`, `android/app/build/`,
  `ios/Pods/` (if CocoaPods is ever introduced), and `.maestro/`'s own report output should be ignored before the
  first commit; `iru-setup-typescript-gitignore` covers this.
- Android/iOS builds need the Android SDK / Xcode respectively already installed on whatever machine actually
  builds them — this skill only scaffolds the platform folders, it doesn't verify a full native build succeeds.
- Every dependency version in Step 3 was resolved via a run-time registry lookup (or its recorded fallback) — the
  `@capacitor/android`/`@capacitor/ios`/`@vitest/coverage-v8` version-matching caveats there matter more than
  chasing the bare `latest` tag; re-run `npm outdated` before relying on this scaffold long-term.
