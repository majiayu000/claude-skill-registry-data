---
name: iru-setup-php-laravel
description: >-
  Scaffold a new Laravel application with `composer create-project laravel/laravel` (latest stable skeleton,
  resolved live from Packagist), or bring an existing Laravel app up to this catalog's toolchain, then
  post-process it: `config/app.php` `'version' => env('APP_VERSION', '0.1.0-dev')` (the `x.y.z-dev` convention
  `iru-php-bump-version` maintains), `config.platform.php` pinned to the PHP floor, Pest (default; arch tests with
  the php/security/laravel presets) or PHPUnit, `phpunit.xml` fast suites (Unit + Feature on SQLite `:memory:`),
  Pint (`pint.json`), Larastan (`phpstan.neon`, level 9 for a new app, level 6 plus a generated baseline for an
  existing one), composer scripts (`test`, `test:coverage` with Clover/JUnit under `build/logs/` and an 80% floor,
  `lint`, `lint:report`, `format`, `format:check`), a sample action + Form Request + policy + resource with feature
  tests, and — each only when chosen — a DB-backed `Integration` suite (`phpunit.integration.xml`, MySQL or
  PostgreSQL), Laravel Sail, a production `Dockerfile` (FrankenPHP or PHP-FPM + Nginx) for `distribution: internal`,
  `sonar-project.properties`, and Laravel Boost as a dev-only dependency — plus browser UI tests per the catalog's
  UI contract: `.ui-quality.yml`, Playwright (`playwright.config.ts` serving `php artisan serve`) with
  `@axe-core/playwright`, the shared `tests/e2e/support/ui-screenshots.ts` helper, and a `WelcomePage` spec capturing
  `.ui-screenshots/screen/WelcomePage/` across left-to-right/right-to-left × light/dark with an accessibility check.
  Invoke as `/iru-setup-php-laravel`.
  Accepts pre-resolved inputs via `args` (`key: value` lines) — `name`, `slug`, `vendor`, `description`, `license`,
  `developer-name`, `developer-email`, `organization-url`, `php-version`, `open-source`, `visibility`, `ci`,
  `ci-tests` (`unit`/`full`), `distribution` (`none`/`internal`), `sonar` (+ `sonar-organization`/
  `sonar-project-key`/`sonar-host-url`), `accessibility` (`enforce`/`report`/`off`/`none`), `test-framework`
  (`pest`/`phpunit`), `integration-tests`
  (`none`/`mysql`/`pgsql`), `sail`, `boost` (`yes`/`no`), `runtime` (`frankenphp`/`fpm`), `mode`
  (`new`/`existing`), `on-existing` (`ask`/`keep`/`update`/`replace`) — so `iru-setup-php-repository` can drive it
  without re-prompting; stand-alone it asks whatever `args` didn't resolve. Announces whether it is scaffolding from
  scratch or updating an existing app and, for every artifact it owns that already exists, warns and asks Update /
  Keep as is / Replace (or Stop). Ends by running the same commands as the `iru-php-test`, `iru-php-coverage`, and
  `iru-php-code-quality` gates. Use whenever a repository needs a Laravel application bootstrapped with its full
  test/coverage/static-analysis/style toolchain from this house template, instead of running `laravel new` and
  wiring the rest by hand.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(composer *) Bash(php *) Bash(vendor/bin/*) Bash(./vendor/bin/*) Bash(docker *) Bash(npm *) Bash(curl *) Bash(python3 *) Bash(git *) Bash(gh repo view *) Bash(mktemp *) Bash(mv *) Bash(cp *) Bash(rm *) Bash(mkdir *) Bash(ls *) Bash(find *) Bash(grep *) Bash(cat *) Bash(test *) Bash(command -v *) Bash(head *)
---

# Setup PHP Laravel

Scaffold a Laravel application with `composer create-project laravel/laravel`, then layer this catalog's standard
toolchain on top: the `x.y.z-dev` version key, a pinned PHP platform, Pest (or PHPUnit) with fast Unit + Feature
suites on in-memory SQLite and Pest arch presets, Pint, Larastan, composer scripts that the CI workflows and the
`iru-php-*` gate skills call by name, Clover/JUnit reports under `build/logs/`, a sample vertical slice that follows
`iru-php-code-one-task/reference/laravel.md`, and — only when chosen — a DB-backed integration suite, Sail, a
production container image, Sonar, and Laravel Boost. Every command below was run (2026-10-13) in Docker
(`php:8.4-cli` + PCOV + `composer:2`, MySQL 8.4) against skeleton v13.11.0 / `laravel/framework` 13.36: create-project,
Pest 5.3 (PHP 8.4 floor) and PHPUnit 12.5 variants, Larastan 3.13 at level 9, Pint 1.32, 100% line coverage on the
sample, integration suite against MySQL, Sail 1.69 and Boost 2.10 installs, and both container images built and
served `/up`. The gotchas called out inline are observed behavior.

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-php-laravel`) or by `iru-setup-php-repository`, which passes already-resolved
answers through `args` as `key: value` lines, one per line, e.g.:

```
name: Acme Loans
slug: acme-loans
vendor: acme
description: Loan tracking for the Acme library.
license: MIT
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/acme
php-version: 8.4
open-source: yes
visibility: public
ci: yes
ci-tests: full
distribution: internal
sonar: cloud
sonar-organization: acme-github
sonar-project-key: acme_acme-loans
sonar-host-url: https://sonarcloud.io
accessibility: enforce
test-framework: pest
integration-tests: mysql
sail: no
boost: yes
runtime: frankenphp
mode: new
on-existing: ask
```

Parse any such lines now; every key found is resolved — never ask it again. If `args` is absent or not in this
format, treat everything as unset.

Recognized keys:

- **Identity**: `name` (→ `APP_NAME`), `slug` + `vendor` (→ `composer.json` `name` = `<vendor>/<slug>`),
  `description`, `license` (SPDX id or display name — map MIT License → `MIT`, Apache License 2.0 → `Apache-2.0`,
  No license → `proprietary`), `developer-name`, `developer-email`, `organization-url` (→ `composer.json`
  `authors`). There is no `namespace` key — a Laravel app keeps the skeleton's `App\` namespace.
- **Pipeline (shared vocabulary)**: `php-version` (the PHP floor, `major.minor`), `open-source` (`yes`/`no`),
  `visibility` (`public`/`private`/`internal`), `ci` (`yes`/`no`), `ci-tests` (`unit`/`full` — only used as the
  default for `integration-tests`), `distribution` (`none`/`internal`; `store` is not valid for an application —
  treat it as invalid and ask), `sonar` (`cloud`/`self-hosted`/`none`) plus, only when `cloud`/`self-hosted`,
  `sonar-organization`/`sonar-project-key`/`sonar-host-url`, `accessibility` (`enforce`/`report`/`off`/`none`, default
  `enforce` — the level the browser UI tests apply, written to `.ui-quality.yml`), `mode` (`new`/`existing`),
  `on-existing` (`ask`/`keep`/`update`/`replace`, default `ask`, for scripted runs).
- **This skill only**: `test-framework` (`pest`/`phpunit`), `integration-tests` (`none`/`mysql`/`pgsql`), `sail`
  (`yes`/`no`), `boost` (`yes`/`no`), `runtime` (`frankenphp`/`fpm`, only consulted with `distribution: internal`).

Ignore any other key (an orchestrator may send its whole vocabulary). `mode: existing` marks an **update** run but
never means "update silently": Step 1 still warns and asks per pre-existing artifact unless `on-existing` says
otherwise.

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (axe-core in the browser UI tests), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — semantic Blade landmarks, labelled form controls, `alt` on images, relative font sizes, `prefers-reduced-motion` guards — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

## Step 1 — Survey the repository

- **Detect a Laravel app**: `composer.json` requiring `laravel/framework` **and** an `artisan` file. Read the
  installed framework version from `composer.lock` (`laravel/framework`). If `mode` wasn't supplied, derive it: app
  present ⇒ `existing`, absent ⇒ `new`.
- **A `composer.json` that is not a Laravel app** (a library, a WordPress plugin, …): stop and say this skill only
  scaffolds/updates Laravel applications — suggest `iru-setup-php-repository` to pick the right flavor. Never run
  `create-project` over another project's manifest.
- **Survey every artifact this skill owns**: the app itself (`composer.json` + `artisan`), the `'version'` key in
  `config/app.php`, `phpunit.xml`, `phpunit.integration.xml`, `tests/Pest.php`, `tests/Unit/ArchTest.php`,
  `phpstan.neon` / `phpstan.neon.dist` / `phpstan.dist.neon` (+ `phpstan-baseline.neon`), `pint.json`, the composer
  scripts (`test:coverage`, `test:integration`, `lint`, `lint:report`, `format`, `format:check`), the sample slice
  (`app/Actions/RenameUser.php` and its siblings from `reference/sample-code.md`), `compose.yaml` /
  `docker-compose.yml` referencing `laravel/sail`, `Dockerfile` + `.dockerignore` (+ `docker/nginx/default.conf`),
  `sonar-project.properties`, Boost's files (`boost.json`, `.mcp.json` with a `laravel-boost` server), and the
  browser UI test setup (`.ui-quality.yml`, `playwright.config.ts`, `tests/e2e/support/ui-screenshots.ts`,
  `tests/e2e/specs/WelcomePage.spec.ts`, the `test:e2e` npm script).
- **Announce the mode** before asking anything else:
  - **Nothing owned exists**: "Scaffolding the Laravel application **from scratch**."
  - **Anything owned exists** (or `mode: existing`): "**Updating an existing setup** — found: <list with paths>
    (Laravel <version>, PHP floor <composer.json require.php>)." Warn that each will be handled individually, then
    resolve one action per artifact:
    - **`on-existing` is `keep`/`update`/`replace`**: apply it to every artifact without asking (still print the
      warning). Exception: `replace` never re-scaffolds an existing app (see below) — treat the app itself as
      `update` and say so.
    - **Otherwise**: ask with `AskUserQuestion`, up to 4 artifacts per call (one question each), naming concrete
      contradictions with this run's choices in the question (e.g. "`phpstan.neon` has no Larastan include",
      "`phpunit.xml` points the Feature suite at MySQL, so it isn't a fast suite", "a `sonar-project.properties`
      exists but you chose `sonar: none`", "`.ui-quality.yml` says `accessibility: report` but you chose
      `enforce`"):
      - **Update (Recommended)** — merge: add what's missing and correct what this skill owns (missing scripts and
        dev dependencies, the Larastan include, the `<source>` element, the sqlite `:memory:` env lines), keeping
        everything else. The user reviews a diff; customizations survive, but a customized part this skill owns may
        be rewritten.
      - **Keep as is** — leave it untouched and skip the steps that only serve it. It may stay out of date or
        disagree with this run's choices — Step 16 lists each mismatch.
      - **Replace** — regenerate from this skill's template; customizations are lost (recoverable only from git
        history). **Not offered for the app itself** — re-running `create-project` over a live application would
        overwrite its code; for an existing app the choice is Update or Keep. For the sample slice files, recommend
        **Keep as is** (they may be real code by now; say so).
      - **Stop** (first batch only) — end without changing anything; report that and end here.
    - Ask about `sonar-project.properties`, `Dockerfile`, `compose.yaml` and Boost's files only after Step 2 resolves
      `sonar`/`distribution`/`sail`/`boost`: when this run no longer wants the artifact, Update/Replace mean
      removing it and Keep leaves it as a reported mismatch.
- **Placement** (only when Step 4 will scaffold): `composer create-project` refuses a non-empty target, and even an
  "empty" repository has `.git`. So Step 4 always scaffolds into a scratch directory and moves the result in. List
  what already sits at the repository root (`ls -A`, ignoring `.git`); everything there is preserved — Step 4 only
  moves in entries that don't exist yet and merges the few that collide (`.gitignore`, `.editorconfig`,
  `.gitattributes`, `README.md`, `CLAUDE.md`, `AGENTS.md`). If the root holds something that looks like another
  application (`src/`, `app/`, `public/`, another manifest), ask whether to scaffold into the root anyway or into a
  subdirectory named `<slug>`.

## Step 2 — Collect identity and options

For every key Step 0 resolved, use it. In `mode: existing`, read identity from `composer.json` (`name`,
`description`, `license`, `authors`) and `.env.example` (`APP_NAME`) and confirm it in one line instead of asking.
Otherwise ask (plain conversation for free text, `AskUserQuestion` for bounded choices):

1. **name**, **slug** (kebab-case, derived from `name`; confirm only), **vendor** (default: the owner from
   `git remote get-url origin`, lowercased), **description**, **developer name/email**, **organization URL**.
2. **license** — **MIT (Recommended)** "the Laravel skeleton's own license" / **Apache-2.0** / **No license
   (proprietary)** → `composer.json` `"license": "proprietary"` / **Other** (ask the SPDX id). Remind in Step 16 to
   add a matching `LICENSE` file if missing (`iru-check-license` can backfill headers).
3. **php-version** (the floor; header `PHP floor`). Look up live: the latest skeleton's `require.php` from
   Packagist (Step 4's lookup) and the branches in active support from php.net
   (`curl -s 'https://www.php.net/releases/?json'` lists the latest release per major; per-branch:
   `curl -s 'https://www.php.net/releases/?json&version=8.4'`; support status:
   https://www.php.net/supported-versions.php). Offer **the latest branch in active support (Recommended)** and
   **the skeleton's floor** ("widest compatibility"), stating where each came from. Never accept a value below the
   skeleton's floor. The floor decides the test stack: on 8.3 Composer resolves Pest 4 / PHPUnit 12; on 8.4+ Pest 5 /
   PHPUnit 13 (Pest 5 requires PHP 8.4) — say which.
4. **open-source**, then **sonar** — "Configure SonarCloud / SonarQube for this project?". Resolve `visibility`
   only now if missing (`gh repo view --json visibility -q .visibility`, lowercased; else ask Public/Private —
   `internal` counts as private). If `open-source: yes` but private/internal, flag the contradiction and ask which is
   right. Recommend **SonarCloud** (`cloud`) only for a public open-source repository; otherwise say SonarCloud is
   free only for public open-source projects and recommend **None**, offering **self-hosted** second. With
   `ci: no`, say no CI workflow would send reports and recommend **None**; if the user still picks one, write the
   properties file anyway and say so in Step 16. For `cloud` ask `sonar-organization` (suggest `<owner>-github`) and
   `sonar-project-key` (suggest `<owner>_<repo>`), host `https://sonarcloud.io`; for `self-hosted` ask the host URL,
   the organization only if the server uses them, and the project key.
5. **distribution** — **None (Recommended unless you deploy containers)** "CI builds and tests only" /
   **Internal** "a production container image (`Dockerfile`), which `iru-setup-php-github-workflows` pushes to
   GHCR on release — free for public repositories, storage/transfer quotas for private ones". With `internal`, ask
   **runtime**: **FrankenPHP (Recommended)** "one process (Caddy + PHP), the runtime the irurueta docs deploy;
   ~630 MB image" / **PHP-FPM + Nginx** "two images (~115 MB + ~63 MB), the classic topology".
6. **test-framework** — new app: **Pest (Recommended)** "Laravel's default; enables the arch-preset tests" /
   **PHPUnit** "the skeleton's own runner; no arch tests". Existing app: recommend whatever it already uses (Pest
   if `pestphp/pest` is in `require-dev`, else **Keep PHPUnit**, offering Pest second — Pest runs existing PHPUnit
   classes unchanged).
7. **integration-tests** — "Add a database-backed integration suite (real MySQL/PostgreSQL instead of in-memory
   SQLite)?" Default **MySQL** or **PostgreSQL** when `ci-tests: full` (ask which, PostgreSQL if the app's `.env`
   already uses `pgsql`), **None (Recommended)** otherwise — "the fast suites already exercise the database on SQLite;
   add this when you rely on engine-specific behavior (JSON columns, full-text, locking, strict modes)".
8. **sail** — "Add Laravel Sail (Docker Compose dev environment)?" **No (Recommended)** unless an integration suite
   was chosen, then **Yes (Recommended)** "gives every developer the same database server; `sail composer
   test:integration` runs the suite". Warn up front that `sail:install` rewrites `.env` and `phpunit.xml`
   (Step 10 repairs `phpunit.xml`).
9. **boost** — "Install Laravel Boost (dev-only MCP server + guidelines + agent skills for Claude Code)?"
   **Yes (Recommended)** / **No**. Say it belongs in `require-dev` only, runs with the developer's database
   credentials, and adds its own skills next to this catalog's in `.claude/skills/`.
10. **accessibility** — "Support accessibility and assistive technologies?" **Enforce (Recommended)** "axe-core violations
    fail the browser UI tests" / **Report only** "listed in the test output, never failing" / **Off** "not run (the
    accessibility coding defaults still apply)". Existing app with a `.ui-quality.yml`: pre-select its value.

## Step 3 — Pick the PHP toolchain

Prefer the host: `command -v php composer` and `php -v` — the host PHP must be ≥ the floor and have `pdo_sqlite`
and `mbstring` (`php -m`). A coverage driver (PCOV or Xdebug, `php -m | grep -iE '^(pcov|xdebug)$'`) is needed by
Step 15's coverage gate.

If the host can't run it, fall back to Docker (check `docker info` first) with a throwaway toolchain image — the one
this skill was verified with:

```dockerfile
FROM php:<php-version>-cli
RUN apt-get update && apt-get install -y --no-install-recommends git unzip libzip-dev libpq-dev \
 && rm -rf /var/lib/apt/lists/* \
 && pecl install pcov && docker-php-ext-enable pcov && docker-php-ext-install zip pdo_mysql pdo_pgsql
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
```

Build it outside the repository (e.g. in `$(mktemp -d)`) as `iru-laravel-toolchain:<php-version>` and prefix every
`composer`/`php`/`vendor/bin/*` command below with
`docker run --rm -v "$PWD":/w -w /w iru-laravel-toolchain:<php-version>` (add
`-v iru-composer-cache:/tmp/composer-cache -e COMPOSER_CACHE_DIR=/tmp/composer-cache` to reuse downloads). If
neither works, stop and tell the user what to install (PHP ≥ floor + Composer, or Docker). Report which toolchain
was used.

## Step 4 — Scaffold with `composer create-project`

Skip this step for an existing app.

Resolve the latest stable skeleton live (record the version):

```bash
curl -s https://repo.packagist.org/p2/laravel/laravel.json | python3 -c 'import json,sys; d=json.load(sys.stdin)["packages"]["laravel/laravel"]; v=[p for p in d if "dev" not in p["version"]][0]; print(v["version"], v["require"]["php"], v["require"]["laravel/framework"])'
```

(verified output: `v13.11.0 ^8.3 ^13.17`). Then scaffold into a scratch directory, pinning the skeleton's major so an
older local PHP fails loudly instead of Composer silently picking an older Laravel:

```bash
SCRATCH="$(mktemp -d)"
composer create-project laravel/laravel "$SCRATCH/app" "^<skeleton-major>" --prefer-dist --no-interaction
```

This installs dependencies, copies `.env.example` → `.env`, generates `APP_KEY`, creates
`database/database.sqlite`, and runs the default migrations (verified). The skeleton ships PHPUnit 12 (not Pest),
Pint, Pail, Collision, Mockery, Faker, `laravel/pao` (agent-friendly test output), a `phpunit.xml` with **Unit** and
**Feature** suites on SQLite `:memory:` and `<source>` = `app/`, `package.json` + `vite.config.js` (Tailwind 4,
Vite 8), an `.npmrc` (`ignore-scripts=true`), and **`CLAUDE.md`/`AGENTS.md` that are only a bootstrap prompt** —
they tell a coding agent to install PHP with `curl … | bash` and then install Boost.

Move the scaffold in without overwriting anything that already exists:

```bash
for e in "$SCRATCH"/app/* "$SCRATCH"/app/.[!.]*; do
  n="$(basename "$e")"
  case "$n" in README.md|CLAUDE.md|AGENTS.md) continue ;; esac
  [ -e "./$n" ] || mv "$e" .
done
```

Then handle the collisions explicitly:

- **`.gitignore`**: append every skeleton line missing from the existing file (no duplicates, keep its order).
- **`.editorconfig` / `.gitattributes`**: keep the repository's; mention in Step 16 if the skeleton's differs.
- **`README.md`**: the skeleton's is Laravel's own project README, not this app's — never move it in. Step 16
  points to `/iru-setup-readme` (the orchestrator runs it anyway).
- **`CLAUDE.md` / `AGENTS.md`**: never move the skeleton's bootstrap prompt in. With `boost: yes`, Step 13 writes
  real guidelines (appending to an existing `CLAUDE.md`, verified); with `boost: no`, nothing is added.

Run `composer install --no-interaction` once (a no-op that proves the moved `vendor/` and autoloader are intact),
then delete the scratch directory.

**Docker toolchain (Step 3)**: a host `mktemp -d` path isn't visible inside the container — run the create-project
and the move loop in one container instead, scaffolding to a container-local path and moving into the mounted
repository (this is exactly how it was verified):

```bash
docker run --rm -v "$PWD":/w -w /w iru-laravel-toolchain:<php-version> sh -c '
  composer create-project laravel/laravel /tmp/scaffold "^<skeleton-major>" --prefer-dist --no-interaction &&
  { [ ! -e /w/.gitignore ] || cp /tmp/scaffold/.gitignore /w/.gitignore.skeleton; } &&
  for e in /tmp/scaffold/* /tmp/scaffold/.[!.]*; do n="$(basename "$e")";
    case "$n" in README.md|CLAUDE.md|AGENTS.md) continue ;; esac; [ -e "/w/$n" ] || mv "$e" /w/; done'
```

Then merge `.gitignore.skeleton` into `.gitignore` as above from the host and delete it.

## Step 5 — Identity, version key, PHP platform

- **`composer.json`** (new app, or Update): `name` → `<vendor>/<slug>`, `description`, `license`, `authors`
  (`[{"name": ..., "email": ..., "homepage": <organization-url>}]`), `keywords` → `["laravel"]` plus anything
  obvious from the description. Never add a `"version"` field — an application's version lives in
  `config/app.php` (the git tag is what releases).
- **PHP floor**: `composer config platform.php <floor>.<latest-patch>` — the newest patch release of the floor
  branch from php.net (`…/releases/?json&version=<floor>` → `version`). **Gotcha, verified**: pinning `8.4.0`
  makes Pest 5 unresolvable because `symfony/process` 8.1 requires `php >=8.4.1`; the current patch avoids that.
  If the floor is above the skeleton's, also raise `require.php`: `composer require php:^<floor> --no-update`.
  Existing app: never lower an existing `require.php`; if an existing `config.platform.php` differs from the floor,
  report it as a mismatch instead of changing it silently.
- **`.env.example`** (and `.env` when present): `APP_NAME="<name>"` (quoted — spaces are common). Leave `APP_KEY`
  empty in `.env.example`; never commit `.env`.
- **`config/app.php`**: insert right after the `'name'` entry, in the file's own comment-block style:

  ```php
      /*
      |--------------------------------------------------------------------------
      | Application Version
      |--------------------------------------------------------------------------
      |
      | The release this build was made from. Development builds carry a "-dev"
      | suffix; the release workflow strips it. APP_VERSION overrides it at run
      | time (e.g. a container image tagged by CI).
      |
      */

      'version' => env('APP_VERSION', '0.1.0-dev'),
  ```

  This exact shape is what `iru-php-bump-version` rewrites. An existing app that already has a `'version'` key keeps
  its value (Update only normalizes it to the `env('APP_VERSION', '…')` form); one without gets `0.1.0-dev` unless
  the latest git tag suggests a higher next version — ask in that case.

## Step 6 — Tests: runner, suites, arch rules

**Pest** (`test-framework: pest`, when not already installed). Remove and require with `--no-update`, then resolve
once — **gotcha, verified**: a plain `composer remove --dev phpunit/phpunit` fails ("Removal failed … may be
required by another package") because Collision/`laravel/pao` constrain PHPUnit, and keeping the skeleton's
`phpunit/phpunit: ^12.5.12` line would hold Pest at 4 even on PHP 8.4:

```bash
composer remove --dev phpunit/phpunit --no-update
composer require --dev pestphp/pest pestphp/pest-plugin-laravel --no-update
composer update --with-all-dependencies --no-interaction
vendor/bin/pest --init
```

`pest --init` only writes `tests/Pest.php` (it leaves `phpunit.xml` and the example tests alone); replace its
boilerplate with the version in `reference/sample-code.md`. Write `tests/Unit/ArchTest.php` from the same file
(`arch()->preset()->php()`, `->security()`, `->laravel()`, plus the actions rule). In an existing app, run the arch
tests once: if a preset fails on existing code, don't touch that code — report the violations and ask whether to
drop that preset line (the rest stay).

**PHPUnit** (`test-framework: phpunit`): keep the skeleton's runner; no arch tests (Pest-only).

**New app**: delete the skeleton's `tests/Unit/ExampleTest.php` and `tests/Feature/ExampleTest.php` (trivia; Step 9
writes real tests).

**`phpunit.xml`**: keep the skeleton's file. Make sure (Update on an existing app) it has exactly the fast suites
`Unit` (`tests/Unit`) and `Feature` (`tests/Feature`), `<source><include><directory>app</directory>` (what coverage
measures — PCOV's auto-detected `pcov.directory` is `app/` for a Laravel layout because there is no `src/` or
`lib/`, so no extra `pcov.directory` setting is needed), and the in-memory database lines:

```xml
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE" value=":memory:"/>
```

If an existing app's `phpunit.xml` points Feature tests at MySQL/PostgreSQL, don't rewrite it silently — that's the
contradiction Step 1's question names; the gate skills then treat Feature as an integration stage.

## Step 7 — Static analysis and style

```bash
composer require --dev larastan/larastan --no-interaction
```

Write `phpstan.neon` (new app):

```neon
includes:
    - vendor/larastan/larastan/extension.neon

parameters:
    level: 9
    paths:
        - app/
        - database/
        - routes/
    tmpDir: build/phpstan
```

Verified: the untouched skeleton plus the sample slice passes level 9 (even level 10) on these paths. `config/` is
left out on purpose — the skeleton's own `config/filesystems.php` fails level 8+ (`argument.type`: `env()` returns
`bool|string` into `rtrim()`), and config files hold little logic. `tests/` is left out too — Pest closures call
`$this->actingAs()` etc. on `TestCall`, which PHPStan reports as `method.notFound` without a Pest extension.
`tmpDir` keeps the result cache under the ignored `build/`.

**Existing app**: `level: 6`, the same paths, then generate a baseline so the gate starts green and only new errors
fail — write the config **without** the baseline include first (an include of a missing file is a fatal error),
then:

```bash
vendor/bin/phpstan analyse --no-progress --memory-limit=1G --generate-baseline phpstan-baseline.neon
```

and add `- phpstan-baseline.neon` under `includes`. Verified: the rerun reports `[OK] No errors`. Report how many
errors were baselined; suggest raising the level later.

Write `pint.json` (Pint itself ships with the skeleton):

```json
{
    "preset": "laravel"
}
```

Run `vendor/bin/pint` once after Step 9 so every file this skill wrote passes `pint --test`. In an existing app, run
`vendor/bin/pint --test` first and, if it fails, ask before reformatting (it can touch many files — suggest a
separate "apply Pint" commit).

## Step 8 — Composer scripts

Keep the skeleton's `setup`, `dev`, `test` and lifecycle scripts. Insert after `test` (the names are what
`iru-setup-php-github-workflows`, `iru-php-test`/`iru-php-coverage`/`iru-php-code-quality` and the README use):

```json
"test:coverage": [
    "@php artisan config:clear --ansi @no_additional_args",
    "@php vendor/bin/pest --coverage --min=80 --coverage-clover=build/logs/clover.xml --log-junit=build/logs/junit.xml"
],
"lint": "@php vendor/bin/phpstan analyse --no-progress --memory-limit=1G",
"lint:report": [
    "@php -r \"is_dir('build/logs') || mkdir('build/logs', 0777, true);\"",
    "@php vendor/bin/phpstan analyse --no-progress --memory-limit=1G --error-format=json > build/logs/phpstan.json"
],
"format": "@php vendor/bin/pint",
"format:check": "@php vendor/bin/pint --test"
```

- **PHPUnit variant**: `test:coverage` runs
  `@php vendor/bin/phpunit --coverage-clover build/logs/clover.xml --log-junit build/logs/junit.xml --coverage-text`
  (PHPUnit has no `--min`; the 80% bar is enforced by `iru-php-coverage`/CI from the Clover numbers).
- **With an integration suite** (Step 10) add
  `"test:integration": ["@php artisan config:clear --ansi @no_additional_args", "@php vendor/bin/pest -c phpunit.integration.xml"]`
  (`vendor/bin/phpunit -c phpunit.integration.xml` for PHPUnit).
- `test` stays `php artisan test`, which reads `phpunit.xml` — the fast suites only.
- `test:coverage` needs a coverage driver (PCOV or Xdebug); without one Pest stops with "No code coverage driver
  available" — never a fake 0%. PHPUnit creates `build/logs/` itself; `lint:report` creates it first because the
  shell redirect needs the directory. `lint:report` feeds Sonar (Step 11).

Run `composer validate --no-check-publish` afterwards.

## Step 9 — Sample code and tests

New app (or an existing app that lacks them and the user chose to add them): write the sample slice and its tests
exactly as in `reference/sample-code.md` — `App\Actions\RenameUser`, `App\Http\Requests\RenameUserRequest`,
`App\Http\Resources\UserResource`, `App\Policies\UserPolicy`, `App\Http\Controllers\UserController`, the
`PATCH /users/{user}` route with `auth` + `can:update,user` middleware, and the Pest or PHPUnit tests (feature:
success, 422 validation, 403 authorization, 401 guest, home page; unit: the Form Request rules). They reuse the
skeleton's `User` model and factory, so no migration is added. They exist to show the conventions and to give the
80% coverage gate real code to measure (verified 100% of `app/`); the user can delete them once real features land.

### Browser UI tests (Playwright)

The PHP tests above never render a page in a browser. Per the catalog's UI contract every screen also gets browser
UI tests that capture screenshots and run an automated accessibility check, so add (new app, or an existing app on
Update/Replace of the browser-UI-test artifacts — Keep leaves them alone) exactly what
`reference/sample-code.md` § *Browser UI tests* lists:

- **`.ui-quality.yml`** at the repository root, the contract's exact shape with `accessibility: <accessibility>`,
  `directions: [ltr, rtl]`, `themes: [light, dark]`. An existing file on Update keeps its `directions`/`themes` and
  only takes this run's `accessibility`.
- **`package.json`**: devDependencies `@playwright/test` `^1.64.0` and `@axe-core/playwright` `^4.14.0`, script
  `"test:e2e": "playwright test"` (`npm pkg set scripts.test:e2e="playwright test"`, then
  `npm install -D @playwright/test@^1.64.0 @axe-core/playwright@^4.14.0` — Node required; without Node on the host,
  `docker run --rm -v "$PWD":/w -w /w node:24-alpine npm install -D …`). Keep the resulting `package-lock.json`.
  The skeleton's `.npmrc` (`ignore-scripts=true`) is fine: browsers come from an explicit
  `npx playwright install chromium`, never from an install script.
- **`playwright.config.ts`** at the root (`testDir: './tests/e2e/specs'`, Chromium, `webServer`
  `php artisan serve --host=127.0.0.1 --port=8000` waiting on `/up`, `reuseExistingServer: !process.env.CI`,
  `reducedMotion: 'reduce'`, fixed 1280×800 viewport, `en-US` locale, `UTC` timezone).
- **`tests/e2e/support/ui-screenshots.ts`** — the one shared helper (`uiQuality()`, `screenshotsDir()`,
  `applyDirectionAndTheme()`, `expectDirection()`, `captureUiState()`, `checkAccessibility()` — the same API
  `iru-php-code-one-task`'s UI guidance documents).
- **`tests/e2e/specs/WelcomePage.spec.ts`** — the skeleton's welcome page as the sample **screen** (`WelcomePage`):
  behaviour asserted once (left-to-right, light), then the `default` state captured for every `.ui-quality.yml`
  direction × theme with the axe check, plus one `high-contrast` capture, into
  `.ui-screenshots/screen/WelcomePage/default--<ltr|rtl>--<light|dark>.png`.
- **`resources/views/welcome.blade.php`** — two small edits: the `<html>` tag gets
  `dir="{{ in_array(app()->getLocale(), ['ar', 'he', 'fa', 'ur'], true) ? 'rtl' : 'ltr' }}"`, so the server renders
  right-to-left for a right-to-left locale; and the three underlined text links' `text-[#f53003]` become
  `text-[#1b1b18]` (keeping `dark:text-[#FF4433]`). **Verified**: the stock page fails axe `color-contrast` on exactly
  those three links in the light theme (#f53003 on white is 3.95:1, below 4.5:1) — so the sample would fail under
  `accessibility: enforce` — and passes with the fix, in both themes. Skip both edits when the app no longer has the
  skeleton's welcome page; point the spec at the app's real home screen instead.

**Direction limitation**: the skeleton has no locale-selection mechanism (no route prefix, session locale or
`Accept-Language` middleware), so `applyDirectionAndTheme()` sends `Accept-Language: ar` and — only when the
server-rendered `<html>` still lacks `dir="rtl"` — sets `dir` client-side (marked `data-ui-dir-fallback`). Say so in
Step 16; once the app selects the locale for real, the server-rendered direction takes over with no test change (or
switch the helper to the app's mechanism — route prefix, session/cookie).

`tests/e2e/` holds TypeScript only, so nothing else needs excluding: `phpunit.xml`'s suites point at `tests/Unit` and
`tests/Feature`, Pint and PHPStan only read PHP (and PHPStan's `paths` don't include `tests/`) — verified, the
skeleton's own `php artisan test` and `pint --test` are unchanged with `tests/e2e/` present.

## Step 10 — Optional integration suite and Sail

**Integration suite** (`integration-tests: mysql|pgsql`). Write `phpunit.integration.xml` — a separate config so
`phpunit.xml` stays the fast, service-free one (`iru-php-test` recognizes the `Integration` suite name and runs it in
its container stage):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
    Database-backed integration tests: same environment as phpunit.xml, but against a real
    MySQL/PostgreSQL server instead of in-memory SQLite. Host, port and credentials come from the
    real environment (CI service container) or from .env (Sail); nothing secret lives here.
    Run with: composer test:integration
-->
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
>
    <testsuites>
        <testsuite name="Integration">
            <directory>tests/Integration</directory>
        </testsuite>
    </testsuites>
    <source>
        <include>
            <directory>app</directory>
        </include>
    </source>
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="APP_MAINTENANCE_DRIVER" value="file"/>
        <env name="BCRYPT_ROUNDS" value="4"/>
        <env name="BROADCAST_CONNECTION" value="null"/>
        <env name="CACHE_STORE" value="array"/>
        <env name="DB_CONNECTION" value="mysql"/>
        <env name="DB_DATABASE" value="testing"/>
        <env name="MAIL_MAILER" value="array"/>
        <env name="QUEUE_CONNECTION" value="sync"/>
        <env name="SESSION_DRIVER" value="array"/>
        <env name="PULSE_ENABLED" value="false"/>
        <env name="TELESCOPE_ENABLED" value="false"/>
        <env name="NIGHTWATCH_ENABLED" value="false"/>
    </php>
</phpunit>
```

(`pgsql` for PostgreSQL.) PHPUnit's `<env>` doesn't override variables already set in the real environment, and
Laravel's dotenv doesn't override what PHPUnit set — so `DB_CONNECTION`/`DB_DATABASE` default as above, while
`DB_HOST`/`DB_PORT`/`DB_USERNAME`/`DB_PASSWORD` come from the CI job's environment or, under Sail, from `.env`
(`DB_HOST=mysql`, user `sail`). Sail's MySQL and PostgreSQL services create the `testing` database themselves.
Write `tests/Integration/UserPersistenceTest.php` from `reference/sample-code.md`, extend `tests/Pest.php` to
`->in('Feature', 'Integration')` (Pest), and add the `test:integration` script (Step 8). Verified against MySQL 8.4:
`DB_HOST=… DB_USERNAME=root DB_PASSWORD=… composer test:integration` → 2 passed, while `composer test` still ran
only the 10 fast tests.

**Sail** (`sail: yes`):

```bash
composer require --dev laravel/sail --no-interaction
php artisan sail:install --with=<mysql|pgsql> --php=<php-version> --no-interaction
```

Add `,redis`/`,mailpit` to `--with` only if the user asks. Without `--php`, Sail builds its newest runtime (8.5) —
pass the floor so development matches production. **Gotchas, verified**: `sail:install` rewrites `.env`
(`DB_CONNECTION=mysql`, `DB_HOST=mysql`, `DB_USERNAME=sail`, `DB_PASSWORD=password`; `.env.example` is left alone)
and **rewrites `phpunit.xml`**: it deletes `<env name="DB_CONNECTION" value="sqlite"/>` and turns
`DB_DATABASE` into `testing`, which silently converts the fast Feature suite into a MySQL-backed one. Immediately
restore the two in-memory lines from Step 6 and confirm `git diff phpunit.xml` is empty (or matches Step 6). Don't
start the containers here (the first `sail up` builds an Ubuntu image); tell the user `./vendor/bin/sail up -d`
then `./vendor/bin/sail composer test:integration`.

## Step 11 — `sonar-project.properties`

Only when `sonar` is `cloud`/`self-hosted`:

```properties
sonar.organization=<sonar-organization>
sonar.projectKey=<sonar-project-key>
sonar.host.url=<sonar-host-url>
sonar.sources=app,config,database,routes,resources
sonar.tests=tests
sonar.exclusions=vendor/**,storage/**,bootstrap/cache/**,public/build/**
sonar.coverage.exclusions=config/**,database/**,routes/**,resources/**
sonar.php.coverage.reportPaths=build/logs/clover.xml
sonar.php.tests.reportPath=build/logs/junit.xml
sonar.php.phpstan.reportPaths=build/logs/phpstan.json
```

Omit `sonar.organization` for a self-hosted server without organizations. Coverage is measured on `app/` only
(`phpunit.xml` `<source>`), so the coverage exclusions keep configuration, migrations, routes and views from
counting as uncovered. The three report paths are produced by `composer test:coverage` and `composer lint:report`.
With `sonar: none`, write nothing (and handle an existing file per Step 1).

## Step 12 — Container image (`distribution: internal`)

Write `Dockerfile` and `.dockerignore` from `reference/container-image.md` for the chosen `runtime`
(`frankenphp`: one image; `fpm`: a two-target `Dockerfile` plus `docker/nginx/default.conf`), with `PHP_VERSION`
set to the floor and the database extension for the app's driver added to `install-php-extensions`. The assets
stage runs `npm ci`, so create and keep `package-lock.json`: `npm install` once (Node required; with no Node on the
host, `docker run --rm -v "$PWD":/w -w /w node:24-alpine npm install`). Secrets stay out of the image (`APP_KEY`
etc. at run time); `php artisan optimize` runs at container start. With `distribution: none`, write nothing.

## Step 13 — Laravel Boost (`boost: yes`)

```bash
composer require --dev laravel/boost --no-interaction
php artisan boost:install --guidelines --skills --mcp --no-interaction
```

Verified (Boost 2.10, Claude Code detected): it writes `CLAUDE.md` guidelines — **appending** below an existing
`CLAUDE.md`'s content, which it keeps — agent skills under `.claude/skills/` (e.g. `laravel-best-practices`,
`testing-best-practices`) next to any existing ones (an `iru-*` skill there was left untouched), `.mcp.json` with a
`laravel-boost` server (`php artisan boost:mcp`), and `boost.json` (so `php artisan boost:update` can refresh them
after `composer update`). All of it is committed; Boost stays in `require-dev`. With `boost: no`, add nothing (the
skeleton's bootstrap `CLAUDE.md`/`AGENTS.md` were already left out in Step 4).

## Step 14 — `.gitignore` entry for reports

Reports and the PHPStan cache go to `build/`, which the skeleton's `.gitignore` doesn't ignore: append `/build/` if
no existing line covers it. Do the same for the browser UI tests' output — `.ui-screenshots/` (with the comment
`# UI test screenshots (regenerated on every UI test run; docs copy what they use)`), `/test-results/`,
`/playwright-report/`, `/blob-report/`, `/playwright/.cache/`. `iru-setup-php-gitignore` (run next by the orchestrator)
owns the rest of the file.

## Step 15 — Verify with the gate skills' commands

Run, in order, the same commands the gates run (prefixed per Step 3 when using Docker), and fix anything this skill
wrote until they pass — never "fix" pre-existing app code to make a gate green; report it instead:

```bash
composer validate --no-check-publish
mkdir -p build
vendor/bin/pest --log-junit build/iru-php-test-junit.xml                        # iru-php-test (phpunit: vendor/bin/phpunit)
php -d pcov.enabled=1 vendor/bin/pest --coverage-clover build/iru-php-coverage-clover.xml   # iru-php-coverage
vendor/bin/phpstan analyse --no-progress --error-format=json --memory-limit=1G > build/iru-php-cq-phpstan.json
vendor/bin/pint --test -v --format=json --output-to-file=build/iru-php-cq-pint.json --output-format=json
composer test && composer test:coverage && composer lint && composer format:check && composer lint:report
```

(With Xdebug instead of PCOV: `XDEBUG_MODE=coverage vendor/bin/pest --coverage-clover …`.) Read line coverage from
the Clover file's project `<metrics>` (`coveredstatements`/`statements`) and require ≥ 80%; PHPStan's JSON must show
`"totals":{"errors":0,...}`; Pint's report must list no files (it writes the JSON to the file, not stdout). Expected
on a new app: all fast tests green (10 with Pest — 4 arch + 1 unit + 5 feature; 6 with PHPUnit), 100% of `app/`,
0 PHPStan errors, Pint clean. Then, when they were added:

- **Integration suite**: only if a database server is reachable (Sail up, or a throwaway
  `docker run -d --name <slug>-it-db -e MYSQL_ROOT_PASSWORD=… -e MYSQL_DATABASE=testing mysql:8.4` /
  `postgres:18-alpine` with the matching env, connected via `DB_HOST`/`DB_USERNAME`/`DB_PASSWORD`), run
  `composer test:integration`; otherwise mark it **unverified** — never skip it silently. Remove any container you
  started.
- **Container image**: with Docker running, the smoke test in `reference/container-image.md`; otherwise
  **unverified**.
- **Boost**: `php artisan boost:mcp --help` exits 0.
- **Browser UI tests** (the `ui` stage of `iru-php-test`): it starts `php artisan serve` and a browser, so take the
  repository-wide `.integration-test.lock` exactly like the integration stage (atomic `mkdir`, owner file, stale after
  60 min, released on every exit path). With a usable `.env` (SQLite, migrated — the skeleton's default
  `SESSION_DRIVER=database` needs the `sessions` table) run `npx playwright install chromium` then `npm run test:e2e`;
  expect 6 passed and the five PNGs under `.ui-screenshots/screen/WelcomePage/` (`default--ltr--light`,
  `default--ltr--dark`, `default--rtl--light`, `default--rtl--dark`, `default--ltr--high-contrast`). Docker-toolchain
  runs: start `php artisan serve --host=0.0.0.0 --port=8000` in the toolchain image with `-p 8000:8000` first —
  `reuseExistingServer` picks it up. No Node, no browser, or no PHP able to serve → **unverified**, never skipped
  silently.

Remove `build/iru-php-*` files afterwards (the `build/logs/` reports may stay — ignored; so may `.ui-screenshots/`,
`test-results/`).

## Step 16 — Report

Start by repeating the mode (**scaffolded from scratch** or **updated an existing setup**), the toolchain used (host
or Docker image), and the resolved versions with their source (skeleton `laravel/laravel` version and
`laravel/framework` from `composer.lock`, Pest/PHPUnit, Larastan/PHPStan, Pint, Sail/Boost if added — live lookup or
already locked). Then, per owned artifact, the action taken — **created / updated / replaced / kept as is / removed /
skipped** — and for every kept artifact each mismatch with this run's choices.

State explicitly what was included versus omitted, and why: PHP floor (and the platform pin), test framework,
PHPStan level and baseline size, integration suite (engine or none), Sail, `sonar` (and the `visibility` it was
keyed on), `distribution`/`runtime`, Boost, and `.ui-quality.yml` (**created / updated / replaced / kept as is**,
with its `accessibility` level) plus the browser UI test files. Then each Step 15 command and its result (tests
passed, coverage %, PHPStan errors, Pint, browser UI tests with their screenshot count and accessibility violations),
plus anything **unverified** and why — including the client-side direction fallback while the app has no
locale-selection mechanism.

Finish with a **Warn explicitly** block:

- **Review before committing** — `composer.json` identity/license/authors, `APP_NAME`, and the Sonar keys.
- **Never commit `.env`** (it holds the generated `APP_KEY`); `composer.lock` and `package-lock.json` (if created)
  **are** committed.
- **Coverage needs PCOV or Xdebug** locally and in CI (`shivammathur/setup-php` with `coverage: pcov`).
- **Sail** was added: `./vendor/bin/sail up -d` builds its image on first run; `.env` now points at the Sail
  database.
- **Container image**: secrets (`APP_KEY`, DB credentials) are runtime environment variables; migrations run once
  per release (a job/init step), not in every replica's start command.
- **Boost** reads logs and queries the database with the developer's credentials — development machines only.
- **`sonar: cloud`/`self-hosted`**: a `SONAR_TOKEN` secret and a matching project must exist before CI analysis
  succeeds.
- **Browser UI tests** need Node, `npx playwright install chromium` once per machine, and a migrated `.env`
  database; they serialize behind `.integration-test.lock` and run in CI only where
  `iru-setup-php-github-workflows` wired them (its `ci-tests: full` integration job).
- If no `README.md`/`LICENSE` exists, suggest `/iru-setup-readme` and `iru-check-license`.

## Sources

- irurueta docs: `web/php-laravel/laravel-getting-started.adoc`, `web/php-laravel/testing.adoc`,
  `web/php-laravel/best-practices.adoc`, `web/php-laravel/docker-and-sail.adoc`, `web/php-laravel/deployment.adoc`,
  `web/php-laravel/ai-sdk-mcp-and-boost.adoc`
- https://laravel.com/docs/13.x/installation, https://laravel.com/docs/13.x/testing,
  https://laravel.com/docs/13.x/sail, https://laravel.com/docs/13.x/deployment, https://laravel.com/docs/13.x/boost
- https://pestphp.com/docs/installation, https://pestphp.com/docs/arch-testing
- https://github.com/larastan/larastan, https://phpstan.org/user-guide/baseline
- https://frankenphp.dev/docs/docker/, https://www.php.net/supported-versions.php
- https://playwright.dev/docs/test-configuration, https://playwright.dev/docs/test-webserver,
  https://playwright.dev/docs/accessibility-testing, https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright
