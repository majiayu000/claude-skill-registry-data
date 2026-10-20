---
name: iru-setup-php-prestashop
description: >-
  Scaffold a PrestaShop module for PrestaShop 8.x and 9.x in the repository root (the repository is the module
  directory, named after the module's technical name), or bring an existing module up to this catalog's toolchain:
  main class `<module>.php` extending `Module` (name, tab, `x.y.z-dev` version, author, `need_instance`,
  `ps_versions_compliancy` 8.0.0–9.99.99, bootstrap, install/uninstall registering hooks and `Configuration`
  defaults, new translation system), tracked `config.xml`, a 32×32 `logo.png` placeholder, `composer.json`
  (`type: prestashop-module`, PSR-4 `src/`, classmap of the main file, `prepend-autoloader: false`,
  `config.platform.php` pinned to the PHP floor) with the catalog's shared composer scripts (`test`,
  `test:coverage`, `test:integration`, `lint`, `lint:report`, `format`, `format:check`, `package`), a sample
  `displayFooter` hook, a Symfony back-office configuration page (form type + data configuration + form handler in
  `config/services.yml`, route in `config/routes.yml`, controller and Twig template, compatible with 8.x and 9.x),
  `upgrade/` with a README, `translations/`, `index.php` directory guards everywhere, license headers (AFL-3.0 by
  PrestaShop convention, OSL-3.0, MIT, proprietary, or other — asked), `prestashop/php-dev-tools` (PHP-CS-Fixer
  config, PHPStan with `_PS_ROOT_DIR_` against a real shop) plus a stub-based PHPStan config that needs no shop,
  a fast PHPUnit unit suite with Clover/JUnit under `build/logs/`, an optional Integration suite and Docker
  `prestashop/prestashop` + MariaDB dev shop, `bin/package.sh` building the distributable zip for Back Office or
  PrestaShop Addons upload, `sonar-project.properties` when Sonar is on, and browser UI tests per the catalog's UI
  contract — `.ui-quality.yml`, a test-only `package.json` with Playwright + `@axe-core/playwright`,
  `playwright.config.ts` against a running shop at `PS_BASE_URL` (specs skip when it is unset), the shared
  `tests/e2e/support/ui-screenshots.ts` helper, and a `FooterMessage` spec capturing the hook template across
  left-to-right/right-to-left × light/dark with an accessibility check, all excluded from the module zip.
  Resolves dev-dependency versions live through `composer require --dev` under the pinned platform, then runs the unit tests, coverage, PHPStan, and
  PHP-CS-Fixer to prove the scaffold. Invoke as `/iru-setup-php-prestashop`. Announces whether it is creating the
  module from scratch or updating an existing one; for every file it owns that already exists, warns and asks
  Update / Keep as is / Replace. Accepts pre-resolved inputs via `args` (`key: value` lines) — `name`, `slug`
  (the technical name), `vendor`, `namespace`, `description`, `license`, `developer-name`, `developer-email`,
  `organization-url`, `php-version`, `open-source`, `visibility`, `ci`, `distribution`, `sonar` (+
  `sonar-organization`/`sonar-project-key`/`sonar-host-url`), `tab`, `accessibility`, `mode`, `on-existing` — so
  `iru-setup-php-repository` can supply them without re-prompting. Use whenever a PrestaShop module repository needs
  its module skeleton and build/test/lint/package toolchain bootstrapped from this house template.
model: sonnet
allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash(composer *) Bash(php *) Bash(npm *) Bash(npx *) Bash(vendor/bin/*) Bash(docker *) Bash(git *) Bash(gh *) Bash(bash bin/package.sh*) Bash(chmod +x bin/package.sh) Bash(mkdir *) Bash(ls *) Bash(cat *) Bash(find *) Bash(grep *) Bash(head *) Bash(test *) Bash(command -v *) Bash(date *) Bash(unzip -l *)
---

# Setup PrestaShop module

Generate a PrestaShop 8.x/9.x module in the repository root — the repository *is* the module directory, because
PrestaShop loads a module from `modules/<module>/` and requires the directory, the main file, and `$this->name` to
match. The templates live in `reference/` (too long to inline) and were generated into a throwaway module,
installed into real `prestashop/prestashop:8` and `:9` shops, and exercised end to end before being trusted (see
"Verification notes" at the end):

- `reference/module-templates.md` — main class, `config.xml`, `src/` sample code, Symfony configuration page
  (form, controller, services, route, Twig), hook template, `upgrade/README.md`, `index.php` guard, license headers,
  logo generator.
- `reference/tooling-templates.md` — `composer.json` and scripts, `phpunit.xml.dist`, unit/integration tests,
  PHPStan configs and stubs, `.php-cs-fixer.dist.php`, the Docker dev shop, the browser UI tests (`package.json`,
  `playwright.config.ts`, `.ui-quality.yml`, the screenshot/accessibility helper, the `FooterMessage` spec),
  `.distignore`, `bin/package.sh`, `sonar-project.properties`.

Read both files in full before writing anything. Copy templates verbatim, substituting only `<placeholder>` values.
The coding conventions they implement are the ones `iru-php-code-one-task` (`reference/prestashop.md`) enforces
later, and the gates `iru-php-test`, `iru-php-coverage`, `iru-php-code-quality`, `iru-php-phpdoc` run on the result
as-is.

## Step 0 — Resolve inputs

Invoked stand-alone, or by `iru-setup-php-repository`, which passes resolved values through `args` as `key: value`
lines, one per line, e.g.:

```
name: Acme Greeting
slug: acmegreeting
vendor: acme
namespace: Acme\Greeting
description: Shows a configurable greeting above the shop footer.
license: AFL-3.0
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/acme
php-version: 8.1
open-source: yes
visibility: public
ci: yes
distribution: store
sonar: cloud
sonar-organization: acme-github
sonar-project-key: acme_acmegreeting
sonar-host-url: https://sonarcloud.io
tab: front_office_features
accessibility: enforce
mode: new
on-existing: ask
```

Parse them now; every key found is resolved and not asked again in Step 2. Recognized keys: `name` (the module's
`displayName`), `slug` (the technical name), `vendor`, `namespace`, `description`, `license` (SPDX id, or
`proprietary`/`UNLICENSED`), `developer-name`, `developer-email`, `organization-url`, `php-version` (floor,
`major.minor`), `open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal`), `ci` (`yes`/`no`),
`distribution` (`none`/`internal`/`store` — only changes Step 8's packaging notes; `bin/package.sh` is always
written because it is also how a module is installed on any shop), `sonar` (`cloud`/`self-hosted`/`none`) plus
`sonar-organization`/`sonar-project-key`/`sonar-host-url`, `tab`, `accessibility` (`enforce`/`report`/`off` — the
automated accessibility level of the browser UI tests, written to `.ui-quality.yml`; default `enforce`), `mode`
(`new`/`existing`), and `on-existing`
(`ask`/`keep`/`update`/`replace`, default `ask`). Ignore any other key (e.g. `ci-tests`, `pages` belong to the
workflows skill — the Integration suite is always scaffolded; CI decides whether to run it). If `args` is absent or
not in this format, treat everything as unset.

`mode: existing` means an established repository: Step 1 announces an **update** but still asks per existing file
unless `on-existing` says otherwise — `mode: existing` alone never means "update silently".

## Step 1 — Survey the repository and decide per existing file

Look at the repository root for an existing module: a `*.php` whose class `extends Module`/`PaymentModule`/
`CarrierModule`, `config.xml`, `composer.json`. When one exists, read `$this->name`, `$this->version`, `$this->tab`,
`$this->author`, `ps_versions_compliancy`, the registered hooks, whether `isUsingNewTranslationSystem()` returns
`true`, and `composer.json`'s `autoload.psr-4` — these become the defaults (or resolved values) for Step 2, and the
technical name must not change on an existing module (shops identify it by name).

The files this skill owns: `<module>.php`, `config.xml`, `logo.png`, `composer.json`, `config/services.yml`,
`config/routes.yml`, the sample `src/` classes, the Twig/Smarty templates, `upgrade/README.md`, every `index.php`
guard, `phpunit.xml.dist`, `tests/bootstrap.php`, the sample unit/integration tests,
`tests/Integration/docker-compose.yml`, `phpstan.dist.neon`, `tests/phpstan/phpstan.neon`, `tests/phpstan/stubs/*`,
`.php-cs-fixer.dist.php`, `.distignore`, `bin/package.sh`, `sonar-project.properties`, `.ui-quality.yml`,
`package.json`, `playwright.config.ts`, `tests/e2e/support/ui-screenshots.ts`, `tests/e2e/specs/FooterMessage.spec.ts`.

Announce one of:

- **None exist**: "Creating the PrestaShop module **from scratch** — none of this skill's files exist yet." Go to
  Step 2.
- **At least one exists**: "**Updating an existing module** — found: <list>." Warn that each is handled
  individually, then resolve one action per file:
  - `on-existing` is `keep`/`update`/`replace` → apply it to every existing file without asking (still print the
    warning).
  - Otherwise ask with `AskUserQuestion`, batching up to 4 files per call, naming any concrete contradiction with
    this run's choices in the question (e.g. "`composer.json` has no `prepend-autoloader: false`", "no `lint:report`
    script"):
    - **Update (Recommended)** — merge the template in: add missing scripts (keep the shared names exactly:
      `test`, `test:coverage`, `test:integration`, `lint`, `lint:report`, `format`, `format:check`, `package`),
      autoload entries, config options, `index.php` guards, phpunit suites; correct what this skill owns; keep
      everything else (extra dependencies, hooks, services, routes, rules). Show the diff before writing.
    - **Keep as is** — untouched; listed with its mismatches in Step 8.
    - **Replace** — regenerate from the template; customizations are lost (recoverable from git only).
    - **Stop** (first batch only) — end without changing anything.

    For the main class, real `src/` code, templates, and tests of an existing module recommend **Keep as is** and
    say why: they are the module itself — Update can only add a missing piece the user names (e.g. the
    `index.php` guards, `isUsingNewTranslationSystem()`), and Replace would overwrite real code with the greeting
    sample. On an existing module, never add the sample feature (greeting classes, form, controller, route,
    hook) unless the user asks — add only the tooling and any guards/headers that are missing.
  - Ask about `sonar-project.properties` only after Step 2 resolved `sonar`; with `sonar: none`, Update/Replace mean
    removing it.
  - `.ui-quality.yml`: **Update** adds any missing key and sets `accessibility` to this run's value only when it came
    from `args` or Step 2 (an existing level and narrowed `directions`/`themes` are otherwise kept); **Keep** leaves it
    (Step 8 names a level that differs from this run's); **Replace** writes the contract defaults with this run's
    level. `package.json` Update merges the `test:e2e` script and the two dev dependencies into an existing one. The
    `FooterMessage` spec is part of the greeting sample: on an existing module write only the UI test tooling
    (`.ui-quality.yml`, `package.json`, `playwright.config.ts`, the helper) and recommend **Keep as is** for an
    existing `playwright.config.*` or `tests/e2e/`.

## Step 2 — Collect the required inputs

Skip every key Step 0 resolved; prefer values read in Step 1 and confirm them in one line instead of asking.
Otherwise ask directly (plain conversation):

- **name** — the human-readable `displayName`, e.g. `Acme Greeting`.
- **slug** (technical name) — derived from the name and confirmed: lowercase letters and digits only, starting with a
  letter (`acmegreeting`). Reject hyphens. Discourage underscores: PrestaShop's docs note translation domains don't
  work with them (`Modules.<ModuleClass>.Admin` is built from the name). It becomes the directory name, the main file
  (`<slug>.php`), `$this->name`, the `Configuration`-key prefix (uppercased), and the route prefix. If the repository
  directory isn't named `<slug>`, say that PrestaShop needs the module under `modules/<slug>/` (the zip from
  `bin/package.sh` already nests it correctly) — don't rename the working copy.
- **vendor** — Composer vendor (default: the git remote's owner, lowercased) → `composer.json` `name` =
  `<vendor>/<slug>`.
- **namespace** — default `<Vendor>\<Name>` in StudlyCase (`Acme\Greeting`); `PrestaShop\Module\<Name>` is
  PrestaShop's own convention and also fine.
- **description**, **developer name**, **developer email**, **organization URL**.
- **tab** (`AskUserQuestion`, header `Category`) — the module-manager category: `front_office_features`
  (Recommended for a storefront feature), `administration`, `payments_gateways`, `shipping_logistics`, or Other
  (any value from PrestaShop's module tab list).

Then the **license** (`AskUserQuestion`) unless resolved: **AFL-3.0 (Recommended)** — "the license PrestaShop's own
modules use; Addons-compatible" / **OSL-3.0** — "PrestaShop core's license; note it is not in the PrestaShop Addons
checklist's list of compatible licenses (Apache, AFL, MIT, BSD, ISC, EUPL)" / **MIT** / **No license (proprietary —
common for paid Addons modules)** / **Other** (ask display name, SPDX id, URL). The choice selects the header in
`module-templates.md` "License headers" and `composer.json`'s `license` (`proprietary` for no license).

Then the **PHP floor** unless `php-version` was supplied: the module runs on the shop's PHP, so the floor is the
highest version every targeted PrestaShop major supports — look up the "System requirements" pages for 8.x and 9.x
on devdocs.prestashop-project.org (at the time of writing PrestaShop 8.x supports PHP 7.2–8.1 and 9.x requires
8.1 or newer, so the 8+9 floor is **8.1**; the official `prestashop/prestashop:8` image runs 8.1 and `:9` runs 8.5).
Ask with `AskUserQuestion` (header `PHP floor`): the 8+9 floor (Recommended) vs. a higher floor that drops
PrestaShop 8 support. It sets `<php-version>` (`require.php: >=<php-version>`, `config.platform.php:
<php-version>.0`) and `<ps-min>`: `8.0.0` when the floor is ≤ 8.1, otherwise `9.0.0` — say so when the user picks the
higher floor.

Then **accessibility** unless resolved (`AskUserQuestion`, header `Accessibility`, "Automated accessibility checks
in UI tests?"): **Enforce (Recommended)** — "axe-core violations fail the browser UI tests" / **Report only** —
"listed in the test output, never failing" / **Off** — "not run; the coding rules still apply". Written to
`.ui-quality.yml`.

Then `open-source` (Yes/No) and `sonar`, exactly like `iru-setup-typescript-library` Step 2: resolve `visibility`
(from `args`, else `gh repo view --json visibility -q .visibility`, else ask; `internal` = private; open source +
private is contradictory → ask which is right); recommend **SonarCloud** only for a public open-source repository,
otherwise **None** (SonarCloud is free only for public open-source projects) with **self-hosted SonarQube** second;
with `ci: no`, recommend None because nothing would send reports. For `cloud`/`self-hosted` collect
`sonar-organization` (suggest `<owner>-github`), `sonar-project-key` (suggest `<owner>_<repo>`),
`sonar-host-url`.

`distribution` is not asked here when absent: it only affects Step 8's notes (default `none`).

## Step 3 — Infer repository information

- Owner/repo from `git remote get-url origin` (both `git@host:owner/repo.git` and `https://host/owner/repo.git`
  forms) — used for the vendor default and the Sonar defaults. No remote → ask only if Sonar needs it.
- `<year>` = `date +%Y`. `<ModuleClass>` = `<slug>` with only its first letter uppercased; `<MODULE>` = `<slug>`
  uppercased; `<NamespaceJson>` = `<Namespace>` with each `\` doubled.
- Tools: `command -v composer php docker`. Without a host `composer`/`php`, run every Composer/PHP command of
  Steps 6–7 through Docker from the repository root (`docker run --rm -v "$PWD":/app -w /app composer:2 ...` for
  Composer; an image with PCOV for coverage — `php:<floor>-cli` plus `pecl install pcov`, or any PHP image already
  carrying PCOV/Xdebug). No Docker either → write the files, skip Step 7's runs, and report them as unverified.

## Step 4 — Dependency versions

Nothing is pinned by hand. After `composer.json` exists with `config.platform.php` set (Step 6), Step 7 runs
`composer require --dev phpunit/phpunit phpstan/phpstan friendsofphp/php-cs-fixer prestashop/php-dev-tools`, so
Composer resolves the newest versions compatible with the PHP floor and writes caret constraints. Fallback when
Packagist is unreachable — the versions this skill resolved with a `8.1.0` platform in October 2026; write them into
`require-dev` and say so in Step 8:

| Package | October 2026 (platform 8.1) |
|---|---|
| `phpunit/phpunit` | `^10.5` (10.5.66; PHPUnit 11 needs PHP 8.2, 12 needs 8.3) |
| `phpstan/phpstan` | `^2.3` (2.3.1) |
| `friendsofphp/php-cs-fixer` | `^3.95` (3.95.27) |
| `prestashop/php-dev-tools` | `^5.0` |

npm (browser UI tests only — never shipped): `npm view <package> version` for `@playwright/test` (fallback 1.64.1,
written `^1.64.0`), `@axe-core/playwright` (4.14.0, `^4.14.0`) and `@types/node` (`^24.0.0`, Node 24 LTS), written as
`^<major>.<minor>.0`.

Don't add `prestashop/autoindex` or `prestashop/header-stamp` (see `tooling-templates.md`). Add no production
dependency: everything in `require` ships inside the module zip and loads next to the shop's own vendor.

## Step 5 — Templates

All in `reference/`. Substitute placeholders only. Decisions that change a template:

- **License**: `<license-header>` / `<license-short-header>` per `module-templates.md`.
- **`<ps-min>`**: `9.0.0` for a floor above 8.1. The controller stays on the 8+9-compatible base class and annotation
  unless the user asks for the 9-only form (documented there, not shop-verified).
- **`sonar: none`**: no `sonar-project.properties`.
- **Existing module**: tooling only (Step 1); the sample files are written only on a from-scratch run.
- **`accessibility`**: the one word on `.ui-quality.yml`'s `accessibility:` line.
- **License** in `package.json`: the SPDX id, or `UNLICENSED` for no license.

## Step 6 — Write the files

Apply Step 1's per-file decision (absent → create; Update → merge and show the diff; Keep → untouched, record
mismatches; Replace → overwrite). On a from-scratch run, create:

```
<module>.php  config.xml  logo.png  composer.json  index.php
config/{services.yml,routes.yml,index.php}
src/{index.php,Settings/{MessageSettings,MessageViolation,SettingsKeys,index}.php,Presenter/{FooterMessagePresenter,index}.php,
     Form/{MessageConfigurationType,MessageDataConfiguration,MessageFormDataProvider,index}.php,Controller/index.php,
     Controller/Admin/{ConfigurationController,index}.php}
views/index.php  views/templates/index.php  views/templates/admin/{configure.html.twig,index.php}
views/templates/hook/{footer.tpl,index.php}
upgrade/{README.md,index.php}  translations/index.php
phpunit.xml.dist  phpstan.dist.neon  .php-cs-fixer.dist.php  .distignore  bin/package.sh  [sonar-project.properties]
.ui-quality.yml  package.json  playwright.config.ts  tests/e2e/support/ui-screenshots.ts  tests/e2e/specs/FooterMessage.spec.ts
tests/bootstrap.php  tests/Unit/Settings/MessageSettingsTest.php  tests/Unit/Presenter/FooterMessagePresenterTest.php
tests/Integration/{ModuleInstallTest.php,docker-compose.yml}
tests/phpstan/phpstan.neon  tests/phpstan/stubs/{constants.php,prestashop.stub.php}
```

Generate `logo.png` with the PHP one-liner in `module-templates.md` (host PHP or `php:*-cli` in Docker) and
`chmod +x bin/package.sh`. Don't write `LICENSE`, `.gitignore`, `README.md`, `CHANGELOG.md`, or `docs/` — other
skills own them.

## Step 7 — Install and verify

Run from the repository root (through Docker per Step 3 when there is no host PHP), stopping to report on the first
failure rather than editing templates to force a pass:

1. `composer validate --no-check-publish`, then the Step 4 `composer require --dev ...` (fallback versions +
   `composer update` if Packagist is unreachable).
2. `php -l` on every `*.php` outside `vendor/`.
3. `composer test` — the Unit suite passes (10 tests on the sample).
4. `composer test:coverage` with PCOV or Xdebug loaded — writes `build/logs/clover.xml` and `build/logs/junit.xml`;
   read the line rate (`metrics` of the Clover `project` element): 100% on the sample, never below 80%. No coverage
   driver → report "unverified: no PCOV/Xdebug", not 0%.
5. `composer lint` and `composer lint:report` — PHPStan (unit config) reports no errors; `build/logs/phpstan.json`
   exists.
6. `composer format:check` — PHP-CS-Fixer finds 0 fixable files.
7. `composer package` (needs `rsync`, `zip`, `composer`) — `unzip -l build/<module>-<version>.zip` lists
   `<module>/<module>.php`, `<module>/vendor/autoload.php`, and no `tests/`, `package.json`, `node_modules/` or
   `playwright.config.ts`.
8. **Browser UI test tooling** (needs Node 20+): `npm install`, `npx playwright install chromium`, then
   `npx playwright test --list` lists `FooterMessage.spec.ts` and a plain `npm run test:e2e` reports it **skipped**
   (no `PS_BASE_URL`) — that proves the config, helper and spec load. No Node → "UI tests unverified (no Node)".
9. **Shop check — offer it** with `AskUserQuestion` (Recommended when Docker is running; it takes a few minutes and
   pulls `prestashop/prestashop` and `mariadb` images): `composer shop:up` (with a free `PS_PORT` if 8080 is taken;
   `PS_VERSION=8` for 8.x), `composer shop:install`, `composer test:integration`, `composer lint:shop`, the browser UI
   tests `PS_BASE_URL=http://localhost:<PS_PORT> npm run test:e2e` (check `.ui-screenshots/component/FooterMessage/`
   holds `default--<direction>--<theme>.png` for every `.ui-quality.yml` direction × theme; the right-to-left ones use
   the client-side fallback unless an RTL language was installed and `PS_RTL_LANG` set), then
   `composer shop:down`. After it, run `git diff --stat config.xml` — PrestaShop rewrites `config.xml` in a mounted
   module directory on install; restore the template version (`git checkout config.xml` if it was committed, else
   rewrite it). Declined or Docker unavailable → "shop check not run" in Step 8.

## Step 8 — Report

Start with the mode (**created from scratch** / **updated an existing module**). Then: technical name, display name,
namespace, `<vendor>/<module>`, version `0.1.0-dev`, tab, license, PHP floor and `ps_versions_compliancy` (and where
the floor came from), and the resolved dev-dependency versions (live or fallback). Per file: **created / updated /
replaced / kept as is / removed**, with mismatches for kept files and what a Replace may have lost. Each Step 7
check: pass/fail/unverified with the reason (coverage %, PHPStan error counts, fixable-file count, zip path, shop
check result per PrestaShop major, browser UI tests: screenshot count, axe violations as rule id × count, or
"unverified (no shop)"). `.ui-quality.yml` (created / updated / replaced / kept as is) and the accessibility level it
holds.

State `open-source`, `visibility` (and its source), `sonar`, and `distribution`:

- `distribution: store` — PrestaShop Addons has **no upload API**: the zip from `composer package` (CI attaches it to
  the GitHub Release) is uploaded manually in the Addons seller account, where the validator runs; also run it
  through https://validator.prestashop.com before submitting. Remind the user of the Addons technical checklist
  points this scaffold does not settle: a compatible license (OSL-3.0 isn't on its list), English code and wordings,
  end-user documentation in a `docs/` folder of the **zip** (the repository's `docs/` is the Antora site and is
  excluded by `.distignore` — ship user docs another way, e.g. a PDF added at packaging time), no external downloads
  at runtime, tokens on any AJAX/cron entry point.
- `distribution: internal` — the zip attached to GitHub Releases is installed through **Modules → Module Manager →
  Upload a module** or by unzipping into `modules/` and running `php bin/console prestashop:module install <module>`
  as `www-data`.

**Warn explicitly**:

- Review every generated file; replace the greeting sample with the module's first real feature, keeping the
  `src/` split (pure, unit-tested logic vs. PrestaShop/Symfony glue checked by PHPStan and the Integration suite).
- Add a `LICENSE` file matching the headers (`iru-check-license` can create it and backfill headers); replace the
  placeholder `logo.png`.
- **`-dev` versions and PrestaShop**: `ps_module.version` is `VARCHAR(8)`, so a shop running a development build
  stores `0.1.0-de` and keeps offering an "Upgrade" — harmless in a dev shop, but never install a `-dev` zip on a real
  shop; releases (`x.y.z`) are unaffected.
- Every release that adds a hook, configuration key, or table ships an `upgrade/upgrade-<x.y.z>.php`
  (`upgrade/README.md`); `iru-php-bump-version` updates `$this->version` and `config.xml` but never writes upgrade
  scripts.
- Run console commands in the dev shop as `www-data`; running them as root breaks the back office with
  permission errors on `var/`.
- No `.gitignore` was written: `vendor/`, `build/`, `.phpunit.cache/`, `.php-cs-fixer.cache`, `config_*.xml`, and
  release zips must be ignored (and `config.xml` kept tracked) — `iru-setup-php-gitignore` does it.
- With Sonar on, a `SONAR_TOKEN` secret and the Sonar project must exist; CI runs `composer test:coverage` and
  `composer lint:report` before the scanner.
- Browser UI tests need a running shop with the module installed and `PS_BASE_URL`; without it they skip and are
  reported unverified. For real right-to-left captures install an RTL language in the test shop and export
  `PS_RTL_LANG=<iso>`. `node_modules/`, `.ui-screenshots/`, `test-results/` and `playwright-report/` belong in
  `.gitignore` (`iru-setup-php-gitignore`); `.distignore` already keeps all of it out of the zip.

## Verification notes

Built in October 2026 by generating a module from these exact templates in `$TMPDIR/iru-verify/php-setup/prestashop/`
(platform PHP 8.1.0, resolved PHPUnit 10.5.66, PHPStan 2.3.1, PHP-CS-Fixer 3.95.27, php-dev-tools 5):

- `php -l` clean; Unit suite 10/10 on PHP 8.4 (`php:8.4-cli` + PCOV) and 8.5; coverage 100% lines of the measured
  `src/` (Clover + JUnit written); `composer lint`/`lint:report` (unit config) no errors (also clean at `max`);
  `composer format:check` 0 of 29 files fixable; `composer validate` clean.
- **PrestaShop 9.2.0** (`prestashop/prestashop:9`, PHP 8.5, MariaDB 11) and **8.2.8** (`:8`, PHP 8.1): `php
  bin/console prestashop:module install <module>` succeeded; hook `displayFooter` and both configuration defaults
  registered; uninstall → reinstall clean; Integration suite passed inside both shops; shop-level PHPStan
  (`tests/phpstan/phpstan.neon`, `_PS_ROOT_DIR_`) no errors on both; logged in to the back office as the image's
  demo employee: the module manager's Configure button reached the Symfony page through `getContent()` (8.x legacy
  `AdminModules&configure=` 302 → route; 9.x direct), the form rendered with stored values, an invalid value showed
  the translated error, a valid one saved (flash "Successful update.", `ps_configuration` updated) and appeared on
  the storefront footer.
- The zip from `composer package` (built in `composer:2` + rsync), unzipped into a **clean** 9.x shop and installed
  from it, passed the same back-office/storefront checks.
- Fixed during verification and documented in the references: `blank_line_after_opening_tag` before headers;
  `_legacy_controller: AdminModules` in a module route creates an `AdminModules` tab and breaks every module's
  legacy Configure page on 8.x; prose mentioning the annotation name with `@` adds an empty security rule (HTTP 500
  on 8.x); `$this->trans()` in a module controller fails on 8.x (inject the translator); console as root breaks
  `var/` permissions; `ps_module.version` truncates `-dev` versions; PrestaShop rewrites `config.xml` in a mounted
  working copy.
- **Browser UI tests (issue 16, October 2026)** in `$TMPDIR/iru-verify/php/iru-setup-php-prestashop/`: `npm install`
  resolved `@playwright/test` 1.64.1, `@axe-core/playwright` 4.14.0, `@types/node` 24.x; `tsc --noEmit` (strict)
  clean on the config, helper and spec; `npm run test:e2e` without `PS_BASE_URL` → 1 skipped; with `PS_BASE_URL`
  pointing at a static stand-in page carrying the hook's markup, the spec passed (4 captures
  `component/FooterMessage/default--{ltr,rtl}--{light,dark}.png`, axe clean); `rsync --exclude-from=.distignore`
  dropped `package.json`, `node_modules/`, `playwright.config.ts`, `tests/`, `.ui-quality.yml` and the Playwright
  output. **Not verified:** the spec against a real 8.x/9.x shop (the Docker VM had no disk space left this run), an
  installed RTL shop language (`PS_RTL_LANG`), and the classic theme's markup under axe.
- Not verified: the 9-only controller variant (`PrestaShopAdminController` + attribute); `composer
  test:integration`/`lint:shop`/`shop:*` invoked through the composer scripts themselves (their exact `docker
  compose` commands were run by hand); submission to validator.prestashop.com or Addons; GitHub Actions runs (the
  workflows skill's job).
