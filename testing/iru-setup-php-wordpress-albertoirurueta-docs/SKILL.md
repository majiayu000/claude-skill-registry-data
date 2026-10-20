---
name: iru-setup-php-wordpress
description: >-
  Scaffold (or bring up to date) a WordPress plugin or block theme repository on this catalog's PHP toolchain.
  `flavor: plugin` writes the main plugin file (full header — Plugin Name, Description, Version `x.y.z-dev`,
  Requires at least, Requires PHP, Author, License GPL-2.0-or-later, Text Domain, Domain Path — plus an
  `ABSPATH` guard and a `<PREFIX>_VERSION` constant), a namespaced PSR-4 `src/` loaded through Composer's
  autoloader (a composition root, a filter service with a documented custom hook, a settings page whose
  `admin-post.php` handler checks nonce and capability, a REST route with a `permission_callback`),
  `uninstall.php`, `languages/`, a WordPress.org `readme.txt`, and `.distignore`; with `blocks: yes` it also wires
  `@wordpress/scripts` and a first block. `flavor: theme` writes a block theme — `style.css` header, `theme.json`
  v3, `templates/index.html`, `parts/header.html`/`footer.html`, translatable `patterns/`, and a small
  `functions.php` that requires namespaced classes. Both get `composer.json` (PSR-4, `config.platform.php` pinned to
  the floor; scripts `test`, `test:coverage`, `test:integration`, `lint`, `lint:report`, `format`,
  `format:check`), `phpcs.xml.dist` (WordPress-Extra + WordPress-Docs + PHPCompatibilityWP with `testVersion`,
  `minimum_wp_version`, text domain and prefixes), `phpstan.neon.dist` (phpstan-wordpress, level 6), a Brain Monkey
  `unit` suite (`phpunit.xml.dist`) and a `WP_UnitTestCase` `integration` suite (`phpunit-integration.xml.dist`) run
  inside a dedicated `@wordpress/env` environment (`.wp-env.json` + `.wp-env.test.json`, `package.json` used only
  for wp-env/`@wordpress/scripts`), sample tests, Clover/JUnit under `build/logs/`, browser UI tests per the
  catalog's UI contract (`.ui-quality.yml`, `playwright.config.ts` extending `wp-scripts test-playwright` against the
  wp-env tests instance, `@axe-core/playwright`, the shared `tests/e2e/support/ui-screenshots.ts` helper, a test-only
  RTL mu-plugin, and a sample spec — the plugin's `ContentNotice` component or the theme's `Index` screen — captured
  into `.ui-screenshots/` across left-to-right/right-to-left × light/dark with an accessibility check), and
  `sonar-project.properties` when `sonar` is not `none`. Resolves every dependency, the PHP floor, and the
  WordPress floor/tested-up-to versions live (Packagist, npm, php.net, api.wordpress.org), installs, and verifies
  the scaffold with its own gates. Invoke as `/iru-setup-php-wordpress`, or with `args` (`key: value` lines) — `flavor` (`plugin`/`theme`,
  asked when missing), `name`, `slug`, `vendor`, `namespace`, `prefix`, `description`, `license`,
  `developer-name`, `developer-email`, `organization-url`, `php-version`, `wp-version`, `blocks`, `open-source`,
  `visibility`, `ci`, `distribution` (`none`/`internal`/`store`), `sonar` (+ `sonar-organization`/
  `sonar-project-key`/`sonar-host-url`), `accessibility` (`enforce`/`report`/`off`), `mode` (`new`/`existing`),
  `on-existing` (`ask`/`keep`/`update`/`replace`) — as `iru-setup-php-repository` passes them. Announces whether it creates from scratch or updates; for every
  owned file that already exists it warns and asks Update / Keep as is / Replace. Use whenever a WordPress plugin or
  block theme repository needs its code skeleton, tests, and quality tooling bootstrapped from this house template.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(composer *) Bash(php *) Bash(vendor/bin/*) Bash(npm *) Bash(npx *) Bash(docker *) Bash(curl *) Bash(git remote *) Bash(git branch *) Bash(gh repo view *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(date *) Bash(basename *) Bash(mkdir *) Bash(rmdir .integration-test.lock*) Bash(rm -f .integration-test.lock/owner) Bash(python3 *)
---

# Setup WordPress plugin or block theme

Generate the house WordPress toolchain and a small, real code skeleton at the repository root — the repository
**is** the plugin/theme directory (WordPress loads it from `wp-content/plugins/<slug>/` or
`wp-content/themes/<slug>/`). Templates live in `reference/`:

| File | Read when |
|---|---|
| `reference/tooling.md` | always — `composer.json`, `phpcs.xml.dist`, `phpstan.neon.dist`, both PHPUnit configs, the unit `TestCase`, wp-env configs, `package.json`, the browser UI test setup (`.ui-quality.yml`, `playwright.config.ts`, the screenshot/accessibility helper, the RTL mu-plugin), `sonar-project.properties` |
| `reference/plugin.md` | `flavor: plugin` (including the optional "Blocks" section for `blocks: yes`) |
| `reference/theme.md` | `flavor: theme` |

Read only what the flavor needs. Every template was generated and run end to end (see "Verification notes"); copy
them verbatim except for `<placeholder>`s. The conventions they encode are the ones `iru-php-code-one-task`'s
`reference/wordpress.md` enforces later, and the gate skills (`iru-php-test`, `iru-php-coverage`,
`iru-php-code-quality`, `iru-php-phpdoc`) run on the result unchanged.

## Step 0 — Resolve inputs

Invoked stand-alone or by `iru-setup-php-repository`, which passes `key: value` lines in `args`, e.g.:

```
flavor: plugin
name: Acme Loans
slug: acme-loans
vendor: example-org
namespace: Acme\Loans
description: Tracks book loans.
license: GPL-2.0-or-later
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
php-version: 8.4
open-source: yes
visibility: public
ci: yes
distribution: store
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_acme-loans
sonar-host-url: https://sonarcloud.io
accessibility: enforce
mode: new
```

Recognized keys: `flavor` (`plugin`/`theme`; the orchestrator's `wordpress-plugin`/`wordpress-theme` are accepted
as synonyms), `name`, `slug`, `vendor`, `namespace`, `prefix` (function/option/hook prefix, snake_case),
`description`, `license` (SPDX id, or `proprietary`), `developer-name`, `developer-email`, `organization-url`,
`php-version` (PHP floor, `major.minor`), `wp-version` (WordPress floor, `major.minor`), `blocks` (`yes`/`no`,
plugin only), `open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal`), `ci` (`yes`/`no` — only
consulted for the Sonar recommendation), `distribution` (`none`/`internal`/`store`), `sonar`
(`cloud`/`self-hosted`/`none`) plus `sonar-organization`/`sonar-project-key`/`sonar-host-url`, `accessibility`
(`enforce`/`report`/`off` — the automated accessibility level of the browser UI tests, written to `.ui-quality.yml`;
default `enforce`), `mode` (`new`/`existing`), `on-existing` (`ask`/`keep`/`update`/`replace`, default `ask`).
Ignore unknown keys. Everything resolved here is never asked again.

`mode: existing` means "this is an established repository": Step 1 announces an update and still asks per
pre-existing file unless `on-existing` says otherwise — `mode: existing` alone never means "update silently".

## Step 1 — Flavor, survey, per-file decisions

**Flavor.** Unless `args` resolved it: a root `*.php` whose header carries `Plugin Name:` → `plugin`; a root
`style.css` with `Theme Name:` and/or a `theme.json` → `theme`; otherwise ask with `AskUserQuestion`: **Plugin** —
"features, settings, REST endpoints, blocks; Composer/PSR-4 code with Brain Monkey unit tests and wp-env integration
tests" / **Block theme** — "`theme.json` v3 design tokens, templates, parts and patterns; minimal PHP". If the
markers on disk contradict `args`, say so and ask which is right.

**Owned files.** Both flavors: `composer.json`, `phpcs.xml.dist`, `phpstan.neon.dist`, `phpunit.xml.dist`,
`phpunit-integration.xml.dist`, `tests/Unit/bootstrap.php`, `tests/Unit/TestCase.php`, `tests/Integration/bootstrap.php`,
`.wp-env.json`, `.wp-env.test.json`, `package.json`, `readme.txt`, `.distignore`, `languages/`,
`sonar-project.properties`, `.ui-quality.yml`, `playwright.config.ts`, `tests/e2e/support/ui-screenshots.ts`,
`tests/e2e/mu-plugins/iru-ui-test-direction.php`. Plugin: `<slug>.php`, `uninstall.php`, `src/**`, the sample tests
(including `tests/e2e/specs/ContentNotice.spec.ts`), and with `blocks: yes` `blocks/**` and
`tests/e2e/specs/<BlockName>.spec.ts`. Theme: `style.css`, `theme.json`, `templates/index.html`, `parts/header.html`,
`parts/footer.html`, `patterns/*.php`, `functions.php`, `src/Theme.php`, the sample tests (including
`tests/e2e/specs/Index.spec.ts`).

Announce one of the two situations before asking anything else:

- **None exist** — "Creating the WordPress <plugin|theme> **from scratch**."
- **Some exist** — "**Updating an existing <plugin|theme>** — found: <list>." Then per file:
  - `on-existing` is `keep`/`update`/`replace` → apply it to every file without asking (still print the warning).
  - Otherwise ask with `AskUserQuestion`, up to 4 files per call, naming any concrete contradiction with this run
    (e.g. "`phpunit.xml.dist` has no `unit` suite", "the header says `Requires PHP: 7.4` but you chose 8.3"):
    - **Update (Recommended)** — merge the template in (missing scripts, `require-dev` packages, PHPCS rules, suites,
      header lines, wp-env keys), keep everything this skill doesn't own; show the diff before writing.
    - **Keep as is** — untouched; Step 9 lists each mismatch.
    - **Replace** — regenerate from the template; customizations are lost (git history only).
    - **Stop** (first batch only) — end without changing anything.

    For real code (`<slug>.php` beyond its header, `src/**`, `functions.php`, templates/parts/patterns, existing
    tests) recommend **Keep as is**: Update has nothing meaningful to merge into real code and Replace would
    overwrite it with the sample. For the main plugin file and `style.css`, offer **Update header only** as the
    recommended option instead (add missing header lines, the `<PREFIX>_VERSION` constant, the `ABSPATH` guard).
  - Ask about `sonar-project.properties` only after Step 2 resolved `sonar` (with `sonar: none`, Update/Replace mean
    removing it).
  - `.ui-quality.yml`: **Update** adds any missing key (`accessibility`, `directions`, `themes`) and sets
    `accessibility` to this run's value only when `accessibility` came from `args` or Step 2 — an existing level and
    narrowed `directions`/`themes` are otherwise kept; **Keep** leaves it (Step 9 names a level that differs from
    this run's); **Replace** writes the contract defaults with this run's level. For an existing
    `playwright.config.*` or `tests/e2e/` recommend **Keep as is** (real tests) and only add the helper and the
    mu-plugin when they are missing.

  When updating, read the existing header / `style.css` / `composer.json` first and use their name, slug (directory
  name and `Text Domain`), namespace (PSR-4 map), prefix (existing constants/options), floors (`Requires PHP`,
  `Requires at least`), and author as Step 2's defaults — a value from `args` always wins.

**Directory name.** wp-env mounts the repository as `wp-content/<plugins|themes>/<directory basename>`, and the
`test:integration` script's `--env-cwd` uses `<slug>`. If `basename "$PWD"` differs from the slug, warn: either
rename/clone the repository into a directory named `<slug>` or accept that the script must use the directory name.

## Step 2 — Collect inputs

Ask only what Steps 0–1 left open, in plain conversation unless noted, confirming derived defaults in one line:

- **name** — human-readable (`Plugin Name:` / `Theme Name:`).
- **slug** — kebab-case from `name` (e.g. `acme-loans`); it is also the **text domain**, the REST namespace root, the
  pattern-slug prefix, and the directory name.
- **vendor** — Composer vendor (`<vendor>/<slug>`), default the git remote's owner, lowercased.
- **namespace** — default `<Vendor>\<Name>` in StudlyCase (e.g. `Acme\Loans`).
- **prefix** — snake_case for functions, options, hooks, handles, nonce actions (default: slug with `-` → `_`,
  e.g. `acme_loans`; must be ≥ 4 characters and not start with `wp_`/`__`). `<PREFIX>` is its upper case.
- **description**, **developer name/email**, **organization URL** (`Author URI`).
- **license** (`AskUserQuestion`): **GPL-2.0-or-later (Recommended)** — "matches WordPress; required to be
  GPL-compatible for the WordPress.org directory" / **GPL-3.0-or-later** / **No license (proprietary)** — "can't be
  listed on WordPress.org" / **Other** (must be GPL-compatible for the directory).
- **open-source** (yes/no) and **distribution** (`AskUserQuestion`): **store** — release zip + deployment to the
  WordPress.org plugin/theme directory (default when open source; needs a GPL-compatible license and an approved
  slug) / **internal** — release zip attached to GitHub Releases / **none** — no packaging (default when not open
  source). For `store`, also ask for the WordPress.org username(s) for `readme.txt`'s `Contributors:`.
- **blocks** (plugin only, `AskUserQuestion`): **No (Recommended for a start)** / **Yes** — "adds a `blocks/`
  source directory built by `@wordpress/scripts` and a first dynamic block".
- **accessibility** (`AskUserQuestion`, header `Accessibility`, "Automated accessibility checks in UI tests?"):
  **Enforce (Recommended)** — "axe-core violations fail the browser UI tests" / **Report only** — "listed in the
  test output, never failing" / **Off** — "not run; the coding rules still apply". Written to `.ui-quality.yml`.
- **sonar** — recommend **cloud** only for a public, open-source repository (resolve `visibility` from `args`, else
  `gh repo view --json visibility -q .visibility`, else ask; `internal` counts as private; open source + private is
  contradictory — ask which is right). Otherwise recommend **none** (SonarCloud is free only for public open-source
  projects), offering **self-hosted**. With `ci: no`, say no workflow would send reports and recommend **none**.
  `cloud`: organization (default `<owner>-github`), project key (default `<owner>_<repo>`), host
  `https://sonarcloud.io`; `self-hosted`: host URL, project key, organization only if the server uses them.

## Step 3 — Repository info and floors

- **Repository URL**: parse `git remote get-url origin` (SSH or HTTPS) into `https://<host>/<owner>/<repo>`; no
  remote → ask for the intended URL. It feeds `Plugin URI`/`Theme URI`/`Update URI`.
- **PHP floor** (`<php-floor>`), unless `php-version` came in: read the branches in active support from
  `curl -s https://www.php.net/releases/active.php` (JSON; cross-check https://www.php.net/supported-versions.php).
  Offer (`AskUserQuestion`, header `PHP floor`) the latest branch in active support (catalog default, Recommended)
  and the oldest branch still receiving security fixes — "widest host compatibility; sites running an older PHP than
  `Requires PHP` can't install updates from the directory" (worth recommending instead when `distribution: store`).
- **WordPress floor and tested-up-to**: `curl -s https://api.wordpress.org/core/version-check/1.7/` →
  `offers[0].current` (e.g. `7.1.3`) gives `<wp-tested>` = its `major.minor`. Unless `wp-version` came in, default
  `<wp-floor>` to the branch two releases before it (list the branches from
  `curl -s https://api.wordpress.org/core/stable-check/1.0/`; e.g. tested `7.1` → floor `6.9`) and confirm it in one
  line. Raise the floor to **6.6** for a theme (`theme.json` v3) and to **6.8** for `blocks: yes`
  (`wp_register_block_types_from_metadata_collection()`), saying why — or use the loop fallback in `plugin.md`.
- **Year**: `date +%Y` → `<copyright-year>`.

## Step 4 — Look up versions

Resolve each Composer package's latest **stable** version from Packagist (`curl -s
https://repo.packagist.org/p2/<package>.json` → the first entry of `packages.<package>` whose `version` has no
`-alpha`/`-beta`/`-RC`/`dev`) and write `^<major>.<minor>`; npm packages with `npm view <package> version`. Fall back
to the table (observed October 2026 while verifying this skill) when a lookup fails, and say so in Step 9.

| Package | Fallback | Note |
|---|---|---|
| `wp-coding-standards/wpcs` | 3.4.1 | pins PHP_CodeSniffer 3.x |
| `phpcompatibility/phpcompatibility-wp` | 2.1.8 | 3.0.0 is still alpha — keep the stable 2.x |
| `dealerdirect/phpcodesniffer-composer-installer` | 1.2.1 | registers the standards |
| `phpstan/phpstan` | 2.3.1 | |
| `phpstan/extension-installer` | 1.4.3 | registers phpstan-wordpress |
| `szepeviktor/phpstan-wordpress` | 2.0.4 | brings `php-stubs/wordpress-stubs` |
| `php-stubs/wordpress-tests-stubs` | 7.1.0 | `WP_UnitTestCase` for PHPStan |
| `brain/monkey` | 2.7.0 | |
| `yoast/phpunit-polyfills` | 4.0.0 | must support PHPUnit 9 |
| `phpunit/phpunit` | 9.6.38 | **`^9.6`, never latest** — caveat below |
| `@wordpress/env` | 11.17.0 | |
| `@wordpress/scripts` | 36.1.0 | always — `wp-scripts test-playwright` runs the browser UI tests |
| `@wordpress/create-block` | 4.100.0 | `blocks: yes` only |
| `@playwright/test` | 1.64.1 | browser UI tests; `^1.64.0` |
| `@axe-core/playwright` | 4.14.0 | accessibility check; `^4.14.0` |
| `@wordpress/e2e-test-utils-playwright` | 3.0.0 | `requestUtils`/`admin`/`editor` fixtures; `^3.0.0` (the version `@wordpress/scripts` 36 itself depends on) |

**PHPUnit caveat:** the WordPress PHPUnit test library still targets PHPUnit 9 — its `abstract-testcase.php` calls
`PHPUnit\Util\Test::parseTestMethodAnnotations()` (removed in PHPUnit 10) and core's own `composer.json` requires
`yoast/phpunit-polyfills ^1.1`. Both suites share one `vendor/`, so the whole project stays on `phpunit/phpunit
^9.6` (annotations, not attributes) even though Packagist's latest is 13.x. Re-check
https://raw.githubusercontent.com/WordPress/wordpress-develop/trunk/tests/phpunit/includes/abstract-testcase.php
and core's `composer.json` on each run; only move to a newer major once WordPress documents support for it, and
report the decision either way.

## Step 5 — Placeholders and the Composer-dependency rule

Fill the templates with: `<name>`, `<slug>`, `<vendor>`, `<namespace>` (`Acme\Loans`), `<namespace-json>`
(`Acme\\Loans`), `<prefix>`, `<PREFIX>`, `<description>`, `<developer-name>`, `<developer-email>`,
`<organization-url>`, `<repository-url>`, `<license-spdx>`, `<license-uri>`, `<readme-license>` (`GPLv2 or later`),
`<license-display-name>` (theme: `GNU General Public License v2 or later`), `<php-floor>`, `<wp-floor>`,
`<wp-tested>`, `<first-release>` (default `0.1.0`), `<dev-version>` (`<first-release>-dev`), `<copyright-year>`,
`<wporg-username>`, `<sonar-organization>`, `<sonar-project-key>`, and the per-flavor values in `tooling.md`'s
first table.

**Composer dependencies inside WordPress.** WordPress runs every active plugin and theme in one PHP process with no
dependency isolation: if two plugins ship different versions of the same library (Guzzle, Monolog, a PSR package),
whichever autoloader registers first wins and the other plugin fails at runtime. The scaffold ships **no runtime
Composer dependency** (only its own PSR-4 map, built `--no-dev --classmap-authoritative` for the release zip), so
no prefixing is needed. Tell the user: the first time a third-party runtime package is added to `require`, prefix its
namespaces into the plugin's own (Strauss — `brianhenryie/strauss` — or `humbug/php-scoper`) and load the prefixed
copy; don't add that machinery before there is something to prefix.

## Step 6 — Write the files

Per Step 1's decision: absent → create from the template; Update → merge and show the diff; Keep → untouched,
mismatches noted; Replace → overwrite. Write the shared files from `tooling.md`, then the flavor's files from
`plugin.md` or `theme.md` (plus `plugin.md` "Blocks" for `blocks: yes`). `sonar-project.properties` only when
`sonar` ≠ `none`. `.ui-quality.yml` always (Step 0/2's `accessibility`, `directions: [ltr, rtl]`,
`themes: [light, dark]`, exactly the shape in `tooling.md`). Don't write `.gitignore`, `README.md`, `CHANGELOG.md`, `LICENSE`, workflows, or `docs/` — other
skills own them.

## Step 7 — Install

1. **Composer** — prefer host `composer` (any PHP ≥ `<php-floor>`; `config.platform.php` keeps the lock valid for
   the floor): `composer install --no-interaction`. No host Composer/PHP → Docker, if `docker info` works:
   `docker run --rm -v "$PWD":/app -w /app composer:2 composer install --no-interaction`. Neither → stop and report
   that dependencies are not installed (nothing below can run). Then `composer validate --no-check-publish`.
2. **npm** — `npm install` (writes `package-lock.json`). With `blocks: yes`, also run the block generation and
   `npm run build` from `plugin.md` "Blocks".
3. **Browser** — `npx playwright install chromium` (CI adds `--with-deps`). Failure → the browser UI tests are
   unverified in Step 8, nothing else is affected.

## Step 8 — Verify the scaffold

Run the fast gates — they must all pass before reporting success:

```bash
composer test            # unit suite
composer test:coverage   # needs PCOV or Xdebug; writes build/logs/clover.xml + junit.xml
composer lint            # PHPStan level 6
composer format:check    # WPCS + PHPCompatibilityWP
```

Without a host PHP, run them in a container with PCOV — the image used to verify this skill:

```dockerfile
FROM php:<php-floor>-cli
RUN apt-get update && apt-get install -y --no-install-recommends git unzip && rm -rf /var/lib/apt/lists/* \
 && pecl install pcov && docker-php-ext-enable pcov
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
```

(`docker build -t iru-wp-php .` from a throwaway directory outside the repository, then
`docker run --rm -v "$PWD":/app -w /app iru-wp-php composer test`.) No coverage driver anywhere → report coverage
as **not measured**, never 0%.

**Integration suite** — needs Docker. If `docker info` fails, report it **unverified (Docker unavailable)**.
Otherwise ask once (`AskUserQuestion`): **Run it now (Recommended)** — "starts the dedicated test environment
(`.wp-env.test.json`, port 8889); the first start downloads WordPress and images, ~3 minutes" / **Skip** (unverified).
When running, take the repository-wide lock the `*-code-one-task-group` skills share, so it never collides with a
concurrent integration run:

1. `mkdir .integration-test.lock 2>/dev/null && echo ACQUIRED || echo HELD`. ACQUIRED → write
   `.integration-test.lock/owner` (`iru-setup-php-wordpress scaffold verification` + `date -u`). HELD → show
   `cat .integration-test.lock/owner` and retry about every 30 s; break it if `find .integration-test.lock -maxdepth
   0 -mmin +60` returns it (stale); give up after ~45 min → unverified.
2. `npm run test:env:start`, then `npm run test:integration`, then the browser UI tests
   `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm run test:e2e` (same environment, so inside the same lock), then
   `npm run test:env:stop`. For the UI tests, check that `.ui-screenshots/` holds exactly the sample's matrix
   (`component/ContentNotice/` or `screen/Index/`: each state × `.ui-quality.yml` direction × theme, named
   `<state>--<direction>--<theme>.png`) and report the axe result at the configured level. No Chromium → UI tests
   unverified (no browser), integration still reported.
3. Release on every exit path: `rm -f .integration-test.lock/owner && rmdir .integration-test.lock`.

Never run the integration suite against `.wp-env.json` (the development site — the test installer drops its
tables), never `wp-env destroy`/`clean` an environment this run didn't create.

A failing gate on the untouched templates is a defect in this skill or a drifted dependency: fix the scaffold,
re-run, and report exactly what had to change.

## Step 9 — Report

Start with the mode (**created from scratch** / **updated an existing <plugin|theme>**), then:

- Identity: flavor, name, slug/text domain, namespace, prefix, `<PREFIX>_VERSION` (plugin), version
  `<dev-version>`, license, repository URL; `blocks` for plugins.
- Floors and where they came from: PHP (php.net / `args`), WordPress floor and tested-up-to (api.wordpress.org /
  `args`), and any floor raised for `theme.json` v3 or blocks.
- Versions: which came from live lookups vs. Step 4's fallback; the PHPUnit 9 decision and why.
- Per file: created / updated / replaced / kept as is (with mismatches) / removed / skipped.
- Gates: unit tests, coverage % (or not measured), PHPStan, PHPCS — each pass/fail; integration and browser UI tests:
  passed / failed / unverified with the reason (UI: screenshot count, malformed names, axe violations as rule id ×
  count).
- `.ui-quality.yml` (created / updated / replaced / kept as is) and the accessibility level it holds.
- `distribution`, `open-source`, `sonar` (and visibility source) as resolved.

**Warn explicitly:**

- Review every generated file before committing; replace the sample services with real features as they come.
- `distribution: store`: the slug must be approved by WordPress.org before the first deploy, `readme.txt`
  `Contributors:` must list real WordPress.org usernames, and a theme needs a 1200×900 `screenshot.png`.
- Adding a runtime Composer dependency needs namespace prefixing (Step 5).
- `.gitignore` (`vendor/`, `node_modules/`, `build/`, `.phpunit.result.cache`, `.wp-env.override.json`,
  `.integration-test.lock/`) is `iru-setup-php-gitignore`'s job; CI is `iru-setup-php-github-workflows`'.
- With Sonar configured, a `SONAR_TOKEN` secret and the Sonar project still have to exist.
- The integration suite uses the dedicated `.wp-env.test.json` environment: start it with `npm run test:env:start`
  (not `npx wp-env start`, which starts the development site) before `composer test:integration`.
- Browser UI tests: `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm run test:e2e` after `npx playwright install chromium`
  (without the variable `wp-scripts test-playwright` downloads every browser on each run). `.ui-screenshots/`,
  `artifacts/`, `test-results/` and `playwright-report/` belong in `.gitignore` (`iru-setup-php-gitignore`); the
  plugin's dark captures equal the light ones until the active theme or the plugin's CSS has dark styles.

## Verification notes

Verified October 2026 in `$TMPDIR/iru-verify/php-setup/wordpress/` with the exact templates (sample identity
"Acme Loans"/"Acme Blocks"), `php:8.4-cli` + PCOV + `composer:2`, Node 24 / npm 11, Docker 29:

- **Plugin** (floor PHP 8.4, WordPress 6.9): `composer install` resolved PHPUnit 9.6.38, WPCS 3.4.1 (PHPCS 3.13.6),
  PHPCompatibilityWP 2.1.8, PHPStan 2.3.1, phpstan-wordpress 2.0.4, Brain Monkey 2.7.0, polyfills 4.0.0;
  `composer test` 23 tests OK; `composer test:coverage` 95.6% lines on `src/`; `composer lint` 0 errors;
  `composer lint:report` wrote `build/logs/phpstan.json`; `composer format:check` 0 issues; `npm run
  test:env:start` + `npm run test:integration` in wp-env 11.17.0 (WordPress 7.1.3): 4/4 integration tests OK.
  `iru-php-bump-version`'s helper (`--list`) detected the header `Version:`, the constant, `Stable tag:`, and
  `package.json`.
- **Plugin with `blocks: yes`**: `@wordpress/create-block` 4.100.0 + `@wordpress/scripts` 36.1.0 — `npm run build`,
  `lint:js` (after `--fix` and the three editor dependencies), `lint:css`, the PHP gates (25 tests, 95.9%), and the
  integration suite including the block-registration test (5/5) passed; `rsync --exclude-from=.distignore` kept
  `build/` assets and dropped `build/logs/`, tests and configs. `wp dist-archive` itself could not be exercised (its
  package isn't bundled in the `wordpress:cli` image and installing it failed offline from GitHub).
- **Block theme** (floor PHP 8.2, WordPress 6.9): 4 unit tests OK, 100% coverage, PHPStan and PHPCS clean;
  integration in wp-env (PHP 8.2 container, WordPress 7.1.3): 4/4 OK (block theme active, `theme.json` palette,
  patterns registered, stylesheet enqueued).
- Fixes the verification forced into the templates: `rest_ensure_response()` return typed `WP_REST_Response` (level
  6 `return.unusedType`), `php-stubs/wordpress-tests-stubs` for PHPStan on integration tests, relaxed
  security/prefix/filesystem/doc sniffs for `/tests/` only, the literal `'GET'` instead of `WP_REST_Server::READABLE`
  (unavailable in unit tests), `testsEnvironment: false` + a separate `--config` environment (wp-env 11 deprecates
  the built-in `tests-cli` environment but still creates it by default).
- **Browser UI tests (issue 16, October 2026)** in `$TMPDIR/iru-verify/php/iru-setup-php-wordpress/`, plugin
  generated from these templates: `npm install` resolved `@playwright/test` 1.64.1, `@axe-core/playwright` 4.14.0,
  `@wordpress/e2e-test-utils-playwright` 3.0.0, `@wordpress/scripts` 36.1.0, `@wordpress/env` 11.17.0;
  `tsc --noEmit` (strict) clean on `playwright.config.ts`, the helper, `ContentNotice.spec.ts` and `Index.spec.ts`
  (the theme generated separately: its PHP gates, mu-plugin included, also pass);
  `playwright test --list` loads the config and lists both specs; the helper itself ran in Chromium on a static
  page (captures named `component/ContentNotice/default--{ltr,rtl}--{light,dark}.png` and `screen/Index/…`, the
  `report` level annotated `rule id × nodes`, a non-PascalCase component Id rejected); `php -l`, PHPCS (0 issues on
  the whole plugin, mu-plugin included) and PHPStan level 6 (0 errors) in `php:8.4-cli`. The mu-plugin's hook choice was checked
  against WordPress 7.1.3's `wp-settings.php` (`setup_theme` precedes `new WP_Locale()`, `after_setup_theme`
  follows it). **Not run:** the specs themselves against wp-env — the Docker VM ran out of disk space (MariaDB
  `Errcode: 28`) and wasn't pruned, so the mu-plugin mapping, the RTL rendering, the captures and the axe results
  on the scaffold are unverified; run Step 8 once to confirm them.
- Not verified: Xdebug as the coverage driver, the Playground runtime, a WordPress.org SVN deploy, and the Windows
  shells for composer scripts.

## Sources

- Plugin Handbook — headers, security, uninstall, i18n: https://developer.wordpress.org/plugins/
- Theme Handbook — block themes, `theme.json` v3, patterns: https://developer.wordpress.org/themes/
- readme.txt standard: https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/
- `@wordpress/env` README (containers, `--config`, `testsEnvironment` deprecation, `WP_TESTS_DIR`):
  https://github.com/WordPress/gutenberg/tree/trunk/packages/env
- `@wordpress/scripts` and `@wordpress/create-block`: https://developer.wordpress.org/block-editor/reference-guides/packages/
- `wp scaffold plugin-tests` / `theme-tests` bootstraps: https://github.com/wp-cli/scaffold-command
- WordPress Coding Standards: https://github.com/WordPress/WordPress-Coding-Standards ; PHPCompatibilityWP:
  https://github.com/PHPCompatibility/PHPCompatibilityWP ; phpstan-wordpress:
  https://github.com/szepeviktor/phpstan-wordpress
- WordPress core test library: https://github.com/WordPress/wordpress-develop/tree/trunk/tests/phpunit/includes
- Catalog conventions: `iru-php-code-one-task/reference/wordpress.md`, `testing.md`, `code-style.md`, `security.md`.
- Browser UI tests: `wp-scripts test-playwright`
  (https://developer.wordpress.org/block-editor/reference-guides/packages/packages-scripts/),
  `@wordpress/e2e-test-utils-playwright` (https://github.com/WordPress/gutenberg/tree/trunk/packages/e2e-test-utils-playwright),
  Playwright (https://playwright.dev/docs/test-configuration, https://playwright.dev/docs/screenshots,
  https://playwright.dev/docs/accessibility-testing), `@axe-core/playwright`
  (https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright), `is_rtl()` / `WP_Locale`
  (https://developer.wordpress.org/reference/functions/is_rtl/), must-use plugins
  (https://developer.wordpress.org/advanced-administration/plugins/mu-plugins/).
