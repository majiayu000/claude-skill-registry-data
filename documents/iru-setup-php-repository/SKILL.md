---
name: iru-setup-php-repository
description: >-
  End-to-end bootstrap for a PHP repository of any of four flavors — a Laravel application, a WordPress plugin, a
  WordPress block theme, or a PrestaShop module. Resolves `flavor` (`laravel`/`wordpress-plugin`/`wordpress-theme`/
  `prestashop-module`) from `args`, from an `iru-explore` `Project type:` line (`php-laravel`,
  `php-wordpress-plugin`, `php-wordpress-theme`, `php-prestashop-module`) or the same on-disk markers, or asks; then
  collects the project's identity (name, slug, Composer vendor, PHP namespace, description, license, developer
  name/email/organization URL) and the shared pipeline parameters (`open-source`, `visibility`, `ci`, `ci-tests`,
  `pages`, `distribution` with its flavor-specific meaning, `sonar` plus its detail keys, `accessibility` — the
  automated accessibility level of the browser UI tests every flavor's scaffold writes to `.ui-quality.yml` —,
  `php-version`, `integration-branch`, `stable-branch`) once, each with visibility-aware cost guidance, and
  orchestrates the flavor's scaffold skill (`iru-setup-php-laravel` / `iru-setup-php-wordpress` with
  `flavor: plugin|theme` / `iru-setup-php-prestashop`) → `iru-setup-antora` → `iru-setup-php-gitignore` →
  `iru-setup-php-github-workflows` → `iru-setup-changelog` → `iru-setup-readme`, in that order, via
  `iru-isolated-skill-executor`, so nothing is asked twice (the workflows step is skipped entirely when `ci` is
  `no`). Invoke as `/iru-setup-php-repository`,
  optionally with `args` (`key: value` lines) pre-resolving `flavor`, `mode` (`new`/`existing`), `open-source`,
  `visibility` (`public`/`private`/`internal`, detected via `gh` when absent), `ci` (`yes`/`no`), `ci-tests`
  (`unit`/`full`), `pages` (`yes`/`no`), `distribution` (`none`/`internal`/`store`), `sonar`
  (`cloud`/`self-hosted`/`none`, + `sonar-organization`/`sonar-project-key`/`sonar-host-url`), `accessibility`
  (`enforce`/`report`/`off`/`none`, default `enforce`), `php-version`, `integration-branch` (default `develop`),
  `stable-branch` (default `main`), `on-existing`
  (`ask`/`keep`/`update`/`replace`, forwarded only when supplied), and every identity key, skipping the matching
  question. Starts by announcing whether it is setting up from scratch or updating an existing repository (with an
  inventory of every component it owns marked absent/present/partial); each sub-skill then warns and asks
  keep/update/replace for whatever it finds, and the final report lists the action taken per component. Use
  whenever bootstrapping (or catching up) a Laravel, WordPress, or PrestaShop repository's full
  scaffold/docs/gitignore/CI/changelog/README pipeline in one pass instead of running six skills separately and
  re-answering the same questions.
model: haiku
---

# Setup PHP Repository

Bootstrap a brand-new (or catch up an existing) PHP repository in one pass, for whichever of four flavors it is, by
orchestrating six skills: the flavor's own scaffold skill (`iru-setup-php-laravel`, `iru-setup-php-wordpress` —
which covers both plugins and block themes — or `iru-setup-php-prestashop`), `iru-setup-antora` (Antora
documentation site), `iru-setup-php-gitignore` (root `.gitignore`), `iru-setup-php-github-workflows`
(`build`/`release`/`sync`/`security` workflows + Dependabot), `iru-setup-changelog` (root `CHANGELOG.md`), and
`iru-setup-readme` (root `README.md`). This skill does not duplicate any of their logic — it collects the shared
parameters once and passes each sub-skill only the `args` keys it actually accepts.

Each of Steps 5–10 invokes its sub-skill via the `iru-isolated-skill-executor` agent (`subagent_type:
"iru-isolated-skill-executor"`, always naming the full `iru-`-prefixed skill inside the prompt) rather than calling
`Skill(...)` directly: every sub-skill re-derives what it needs from the files the previous steps wrote, so only a
short completion summary flows back, keeping six transcripts out of this orchestrator's context.
`AskUserQuestion`s raised inside a sub-skill still reach the user — tell the executor to let them through rather
than answering them itself.

**Plain Composer libraries** (`Project type: php-library`) are out of scope: there is no scaffold skill for them in
this catalog. If that's what the repository is (or what the user wants), say so and stop — the gate skills
(`iru-php-test`, `iru-php-coverage`, `iru-php-code-quality`, `iru-php-phpdoc`) and `iru-setup-antora`,
`iru-setup-php-gitignore`, `iru-setup-changelog`, `iru-setup-readme` can still be run individually.

## Step 0 — Resolve inputs

This skill runs stand-alone (`/iru-setup-php-repository`) or from the `iru-setup-repository` front door, so parse
`args` first, as `key: value` lines, one per line, e.g.:

```
flavor: wordpress-plugin
mode: new
open-source: yes
visibility: public
ci: yes
ci-tests: full
pages: yes
distribution: store
sonar: cloud
sonar-organization: example-github
sonar-project-key: example_acme-loans
sonar-host-url: https://sonarcloud.io
accessibility: enforce
php-version: 8.4
integration-branch: develop
stable-branch: main
```

Recognized keys: `flavor` (`laravel`/`wordpress-plugin`/`wordpress-theme`/`prestashop-module`), `mode`
(`new`/`existing`), `open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal`), `ci` (`yes`/`no`),
`ci-tests` (`unit`/`full`), `pages` (`yes`/`no`), `distribution` (`none`/`internal`/`store`), `sonar`
(`cloud`/`self-hosted`/`none`) and — only when not `none` — `sonar-organization`, `sonar-project-key`,
`sonar-host-url`; `accessibility` (`enforce`/`report`/`off`/`none` — the level of the automated accessibility checks in the
browser UI tests, written by the scaffold to `.ui-quality.yml`; every flavor here renders UI — Laravel pages, the
WordPress plugin's/theme's front end and editor, the PrestaShop module's views — so it is always forwarded);
`php-version` (the minimum supported PHP, e.g. `8.3`), `integration-branch`, `stable-branch`; the
identity keys `name`, `slug`, `vendor`, `namespace`, `description`, `license`, `developer-name`, `developer-email`,
`organization-url`; and `on-existing` (`ask`/`keep`/`update`/`replace` — never asked; forwarded to every
file-writing sub-skill **only** when it arrived here). Every key found is resolved — skip its question below. Ignore
unknown keys (e.g. `publish`, which applies to libraries of other stacks). If `args` is absent or doesn't look like
this format, treat everything as unset.

## Step 1 — Resolve the flavor and mode

Unless `flavor` came via `args`, resolve it in this order:

1. **An `iru-explore` report already in this conversation** (e.g. the front door ran it) — read its `Project type:`
   line: `php-laravel` → `laravel`, `php-wordpress-plugin` → `wordpress-plugin`, `php-wordpress-theme` →
   `wordpress-theme`, `php-prestashop-module` → `prestashop-module`. `php-library` → stop as described above.
   `multiple` (e.g. a plugin and a theme in one repository) → tell the user this pipeline sets up one project per
   repository and ask which one to set up.
2. **The same markers `iru-explore` uses, checked directly** (no need to run a full exploration just for this):
   `composer.json` requiring `laravel/framework` plus an `artisan` file → `laravel`; a root PHP file whose header
   comment carries `Plugin Name:` → `wordpress-plugin`; a root `style.css` with a `Theme Name:` header and/or a
   `theme.json` → `wordpress-theme`; a root `<module>.php` whose class `extends Module` (or `PaymentModule`/
   `CarrierModule`), usually with `config.xml` → `prestashop-module`. Tell the user what was detected and confirm
   with `AskUserQuestion` (detected flavor pre-selected).
3. **Nothing detected** (empty or unrelated repository) — ask with `AskUserQuestion` (header `Flavor`):
   - **Laravel application** — "a Laravel web app/API: Pest, Pint, Larastan; optional container image".
   - **WordPress plugin** — "a Composer/PSR-4 plugin with WPCS, PHPStan, Brain Monkey unit tests and wp-env
     integration tests; optionally deployed to the WordPress.org plugin directory".
   - **WordPress block theme** — "a `theme.json` v3 block theme (templates/parts/patterns) with the same tooling;
     optionally deployed to the WordPress.org theme directory".
   - **PrestaShop module** — "a module for PrestaShop 8.x and 9.x with `prestashop/php-dev-tools`; packaged as an
     installable zip".

Map the resolved `flavor` to its scaffold skill for the rest of this run:

| `flavor` | Scaffold skill | Extra `args` it gets |
|---|---|---|
| `laravel` | `iru-setup-php-laravel` | — |
| `wordpress-plugin` | `iru-setup-php-wordpress` | `flavor: plugin` |
| `wordpress-theme` | `iru-setup-php-wordpress` | `flavor: theme` |
| `prestashop-module` | `iru-setup-php-prestashop` | — |

If `mode` wasn't supplied, don't ask it as an isolated question: if `composer.json` or any flavor marker from item 2
above exists at the repository root, default to `existing` and confirm with `AskUserQuestion` (`existing`
pre-selected; `new` treats the repository as a fresh scaffold target — every sub-skill still warns and asks before
touching a file that exists); otherwise `new` without asking. Under `mode: new`, any owned artifact already on disk
is still an update for that component — its sub-skill will warn and ask.

**WordPress and PrestaShop repositories are the plugin/theme/module directory itself.** WordPress loads a plugin from
`wp-content/plugins/<slug>/` and PrestaShop a module from `modules/<name>/`, and PrestaShop requires the directory
name to equal the module's technical name. Tell the user the repository (or a release zip's top-level folder) must
carry that exact name, and warn if the current directory's name differs from the slug resolved in Step 2.

### Setup mode announcement

Right after resolving `mode`, before asking anything else, survey the components this run owns and print:

- `mode: new` and nothing present → "Setting up this repository **from scratch** — no prior setup found."
- Otherwise → "**Updating an existing repository** — prior setup found:" and an inventory table, one row per
  component, marked **absent / present / partial** with the evidence (file paths):

  | Component | Evidence to check |
  |---|---|
  | Composer manifest | `composer.json` (+ `composer.lock`); partial if the lock is missing |
  | Flavor sources | `laravel`: `artisan`, `app/`, `bootstrap/app.php`, `config/app.php`, `routes/`; `wordpress-plugin`: main plugin file (`<slug>.php` with `Plugin Name:`), `src/`, `readme.txt`, `languages/`, `.distignore`; `wordpress-theme`: `style.css` (`Theme Name:`), `theme.json`, `templates/`, `parts/`, `patterns/`, `functions.php`, `readme.txt`; `prestashop-module`: `<module>.php`, `config.xml`, `src/`, `views/`, `upgrade/` |
  | Tests config | `phpunit.xml` / `phpunit.xml.dist`, `tests/` (+ `tests/Pest.php` for Laravel, `.wp-env.json` for WordPress) |
  | Quality configs | `phpstan.neon` / `phpstan.neon.dist` / `tests/phpstan/phpstan.neon`, `pint.json`, `phpcs.xml.dist` / `.phpcs.xml.dist`, `.php-cs-fixer.dist.php`, `.editorconfig` |
  | Antora docs | `docs/antora.yml`, `docs/antora-playbook.yml`, `docs/modules/ROOT/` (partial if only some) |
  | `.gitignore` | `.gitignore` |
  | CI workflows | each of `.github/workflows/build.yml`, `release.yml`, `sync.yml` (+ its sync script under `.github/scripts/`; partial if only one of the pair), `security.yml` |
  | Dependabot | `.github/dependabot.yml` |
  | Sonar config | `sonar-project.properties` |
  | UI quality config | `.ui-quality.yml` (+ the browser UI test setup: `playwright.config.*`, `tests/e2e/support/ui-screenshots.ts`; partial if only some) |
  | Changelog | `CHANGELOG.md` |
  | README | `README.md` (WordPress also: `readme.txt`, owned by the scaffold) |
  | License | `LICENSE` / `LICENSE.md` / `LICENSE.txt` / `COPYING` (not written by this run — listed so a mismatch with the chosen license shows) |

  Then: "For each component that already exists you'll be asked whether to keep it, update it, or replace it." (If
  `on-existing` came via `args`, say which choice will be applied to every existing component instead.)

The keep/update/replace questions themselves are asked inside each sub-skill — never here — so nothing is asked twice.

## Step 2 — Collect the project's identity

**`mode: existing` with the flavor's manifest/main file on disk**: skip every identity question — the scaffold
sub-skill reads the identity from `composer.json`, the plugin/theme header, or the module class and asks only for
what it genuinely can't find (e.g. if the user picks Replace there), and `iru-setup-readme` derives it from the
files itself. Resolve `license` only if `args` supplied it, and record in Step 11 that identity came from the
existing files.

Otherwise ask directly (plain conversation, free-text) for whatever `args` didn't resolve:

- **name** — the human-readable name (Laravel `APP_NAME`; the `Plugin Name:`/`Theme Name:` header; the PrestaShop
  module's `displayName`).
- **slug** — lowercase, derived from `name` by default and only confirmed: kebab-case for WordPress (the plugin/theme
  directory and text domain, e.g. `acme-loans`), the module's technical name for PrestaShop (lowercase letters,
  digits, underscores, no hyphens, e.g. `acmeloans` — it's also the directory and class-file name), and the
  Composer package name's second half for Laravel.
- **vendor** — the Composer vendor (`<vendor>/<slug>` becomes the `composer.json` `name`), default derived from the
  git remote's owner.
- **namespace** — the root PSR-4 namespace, default `<Vendor>\<Name>` in StudlyCase. Not asked for `laravel` — the
  application keeps the skeleton's own `App\` namespace.
- **description** — one line.
- **Developer name**, **developer email**, **organization URL** (also the WordPress `Author URI`).

Then the **license** with `AskUserQuestion`, ordered per flavor because the ecosystems constrain it:

- `wordpress-plugin` / `wordpress-theme`: **GPL-2.0-or-later (Recommended)** — "required to be GPL-compatible for the
  WordPress.org directory; matches WordPress itself" / **GPL-3.0-or-later** / **No license (proprietary)** — warn
  that it can't be listed on WordPress.org / **Other** (must be GPL-compatible to ship on WordPress.org).
- `prestashop-module`: **AFL-3.0 (Recommended)** — "the license PrestaShop's own native modules use" / **MIT** /
  **No license (proprietary — common for paid Addons modules)** / **Other**.
- `laravel`: **MIT (Recommended)** — "the Laravel skeleton's own license" / **Apache-2.0** / **No license
  (proprietary / all rights reserved)** / **Other**.

For **Other**, ask for the display name and SPDX id afterwards.

## Step 3 — Collect the PHP version floor

`php-version` is the **minimum** PHP the project supports: it becomes `composer.json`'s `require.php`
(`>=<php-version>` or `^<php-version>`, per the scaffold skill), `config.platform.php`, the plugin/theme
`Requires PHP:` header, and the lowest version in CI's matrix. Unless `args` supplied it:

- Look up the branches currently in **active support** at https://www.php.net/supported-versions.php (or
  `https://www.php.net/releases/index.php?json` for machine-readable data) — never hardcode a version. The default is
  the latest branch in active support.
- **`laravel`**: also read the `php` constraint in the Laravel skeleton's own `composer.json` (`composer show -a
  laravel/laravel` or Packagist's `https://repo.packagist.org/p2/laravel/laravel.json`). Offer the default above and
  the framework's floor; never accept a value below the framework's floor.
- **`wordpress-plugin` / `wordpress-theme`**: offer the default above, and — when `distribution: store` is likely
  (open source) — the oldest branch still receiving security support as the alternative, noting that sites running
  an older PHP than `Requires PHP` can't install the update from the directory.
- **`prestashop-module`**: the module runs on the *shop's* PHP, so the floor must not exceed what the oldest targeted
  PrestaShop major supports. Look up PrestaShop's system requirements (devdocs.prestashop-project.org, "System
  requirements" for 8.x and 9.x) and default to the **highest PHP version supported by every targeted PrestaShop
  major** — that's lower than the latest active PHP branch, and it deliberately overrides the generic default above.
  State the source and the resulting value.

Ask with `AskUserQuestion` (header `PHP floor`), recommended option first, stating where each value came from.

## Step 4 — Collect the shared pipeline parameters

Ask directly, each with its default so a blank reply accepts it (skip any Step 0 resolved):

| Parameter | Default |
|---|---|
| Integration branch | `develop` |
| Stable branch | `main` |

Then resolve, with `AskUserQuestion`, in this order (skip any key Step 0 resolved):

- **open-source** — Yes / No, no default. Drives the recommended defaults below.
- **visibility** — if the repository has a GitHub remote, detect it with `gh repo view --json visibility -q
  .visibility` (lowercased) and tell the user the detected value; otherwise ask **Public** / **Private**,
  recommending **Public** when open source, otherwise **Private**. Open source + `private`/`internal` is
  contradictory: warn (an open-source project's repository is normally public; a private one forfeits free Actions
  minutes and free SonarCloud) and ask which is right. `internal` is treated like `private` for every cost decision
  below.
- **ci** — "Generate GitHub Actions workflows (CI/CD) for this repository?" Public: recommend **Yes** — standard
  GitHub-hosted runners are free for public repositories. Private/internal: still offer **Yes** first, but state (per
  GitHub's current pricing — tell the user to double-check their plan) that runs consume the account's included
  minutes — 2,000/month on GitHub Free, 3,000 on Pro and Team, 50,000 on Enterprise Cloud — then bill per minute;
  every job in this pipeline runs on Linux runners, and the `full` test tier (below) is the expensive part. **No** —
  "no workflows — build, test, and release locally (run `/iru-setup-php-github-workflows` later)". With `ci: no`,
  Step 8 is skipped entirely (no `.github/workflows/*`, no `security.yml`, no `.github/dependabot.yml`, no sync
  script), `ci-tests` and `pages` are not asked, and Step 11 states that the shared security block (Dependabot,
  dependency-review, CodeQL, OSV-Scanner, gitleaks) was skipped with it.
- **distribution** — what a published release produces. Ask with the options valid for the flavor, recommended
  default as stated:

  | `flavor` | `none` | `internal` | `store` | Default |
  |---|---|---|---|---|
  | `laravel` | CI builds and tests only; no `release.yml` | container image pushed to GHCR on release (free for public repositories; storage/transfer quotas for private ones) | not offered | `none` |
  | `wordpress-plugin` / `wordpress-theme` | no release packaging | installable zip (built from `.distignore`, `composer install --no-dev`) attached to the GitHub Release | the zip **plus** deployment to the WordPress.org plugin/theme directory (SVN; needs a directory account and an approved slug first) | `store` when open source, else `none` |
  | `prestashop-module` | no release packaging | installable module zip attached to the GitHub Release | the same zip plus step-by-step instructions to upload it to the PrestaShop Addons marketplace — Addons has **no upload API**, so the submission itself stays manual | `none` |

  For `store` on WordPress, warn that a WordPress.org listing requires a GPL-compatible license (Step 2), and for a
  theme that the Theme Directory's review rules apply. Never offer `store` for `laravel`.
- **sonar** — "Configure SonarCloud / SonarQube and send CI analysis and coverage reports to it?" Recommend
  **SonarCloud** (`cloud`) only when open source **and** public; otherwise say SonarCloud is free only for
  public/open-source projects (a private project needs a paid plan, per SonarSource's current pricing) and recommend
  **None**, offering **self-hosted SonarQube** second (free Community Build, you run the server). With `ci: no`, say
  nothing would send reports automatically — analysis only runs when someone runs the scanner manually with a token —
  and recommend `none`; if the user still picks cloud/self-hosted, only `sonar-project.properties` is written and
  Step 11 says no CI step sends reports. For cloud/self-hosted collect `sonar-organization` (suggest
  `<owner>-github`; self-hosted only if the server has organizations), `sonar-project-key` (suggest
  `<owner>_<repo>`), and `sonar-host-url` (`https://sonarcloud.io`, or ask), inferred from `git remote get-url
  origin`.

Then, **only when `ci: yes`**:

- **ci-tests** — "Which tests should CI run?" **Unit only** (`unit`; recommended for private/internal) vs **Full**
  (`full`; recommended for public), described per flavor:
  - `laravel`: unit = "Pest unit + feature suites on SQLite `:memory:` — no services"; full = "also the
    integration suite against MySQL/PostgreSQL service containers".
  - `wordpress-plugin` / `wordpress-theme`: unit = "PHPUnit + Brain Monkey, no WordPress loaded"; full = "also the
    `WP_UnitTestCase` integration suite inside `@wordpress/env` (Docker: WordPress + MariaDB) — several extra
    minutes per run".
  - `prestashop-module`: unit = "PHPUnit unit suite"; full = "also an install/smoke check against a real shop in
    the `prestashop/prestashop` Docker image — the slowest option".
- **pages** — the Antora docs site (Step 6) is always built. Public: default **yes** without asking (say so in
  Step 11). Private/internal: ask **No (Recommended)** — "CI still builds the docs and uploads them as a workflow
  artifact; nothing is published" — vs **Yes** — "requires GitHub Pro, Team, or Enterprise Cloud; the site will be
  PUBLIC on the internet unless the organization is on Enterprise Cloud with private Pages access control".

Then, whatever `ci` is:

- **accessibility** — "Support accessibility and assistive technologies?" **Enforce (Recommended)** — "axe-core
  violations fail the browser UI tests" / **Report only** — "violations are listed in the test output, never
  failing" / **Off** — "not run; the accessibility coding defaults still apply to new UI". **None — opt out entirely** ("no accessibility rules, checks or docs"; written as `accessibility: none`). In `mode: existing`, pre-select from `iru-explore`'s `Accessibility:` line per `iru-setup-repository`'s `reference/accessibility-detection.md` (`present` → Enforce, `partial` → Report only with a mixed-compliance warning, `absent` → None) and never silently flip an existing `.ui-quality.yml` value. A `.ui-quality.yml` on disk is shown, never decides alone.

These values are forwarded only to the sub-skills that accept them: identity + `php-version` + `open-source`/
`visibility`/`ci`/`distribution`/`sonar` (+ keys)/`accessibility` to Step 5; the same pipeline keys +
`ci-tests`/`pages`/`integration-branch`/`stable-branch`/`php-version` to Step 8; `sonar`/`ci`/`pages` to Step 10;
`on-existing` — only when it came via `args` — to every file-writing sub-skill (Steps 5–10).

## Step 5 — Run the flavor's scaffold skill

Always invoke the scaffold skill, in both modes — it owns the keep/update/replace decision for `composer.json`, the
sources, the tests and quality configs, and `sonar-project.properties`. Format Steps 1–4's answers as `key: value`
lines and **send only the keys that skill's own Step 0 lists** — read its `SKILL.md` Step 0 before invoking and drop
any key it doesn't recognize rather than inventing one. Always include `mode`, `visibility`, and `ci`; add the
flavor's extra key from Step 1's table; add `on-existing` only if it arrived via Step 0's `args`; omit identity keys
in `mode: existing` with identity skipped (Step 2), and omit any key left unresolved so the sub-skill asks it.

```
Agent({
  description: "Run setup-php-wordpress",
  subagent_type: "iru-isolated-skill-executor",
  prompt: "Invoke Skill({skill: \"iru-setup-php-wordpress\", args: \"flavor: plugin\\nname: <name>\\nslug: <slug>\\n
    vendor: <vendor>\\nnamespace: <namespace>\\ndescription: <description>\\nlicense: <license>\\n
    developer-name: <developer-name>\\ndeveloper-email: <developer-email>\\norganization-url: <organization-url>\\n
    php-version: <php-version>\\nopen-source: <open-source>\\nvisibility: <visibility>\\nci: <ci>\\n
    distribution: <distribution>\\nsonar: <sonar>\\nsonar-organization: <..., if set>\\n
    sonar-project-key: <..., if set>\\nsonar-host-url: <..., if set>\\naccessibility: <accessibility>\\n
    mode: <mode>\\non-existing: <on-existing, only if supplied via args>\"}). Let every AskUserQuestion it raises
    through to the user. Report back: scratch or update; per component it owns (composer.json/lock, sources, tests
    config, quality configs, readme.txt/.distignore where applicable, sonar-project.properties, .ui-quality.yml and
    the browser UI test setup) whether it was created, updated, replaced, kept as is (with mismatches), or the user
    stopped; the resolved framework/tool versions and whether they came from a live lookup or a fallback; and each
    verification gate's result (tests, coverage, static analysis, style, browser UI tests), including anything
    unverified and why.",
  run_in_background: false
})
```

The other flavors follow the same shape with the skill name changed — `iru-setup-php-laravel` (no `flavor` key, no
`namespace`) and `iru-setup-php-prestashop` (no `flavor` key; `slug` is the module's technical name) — each still
filtered against its own Step 0 (`accessibility` goes to all three — each writes `.ui-quality.yml`; if a
scaffold's Step 0 doesn't list it yet, drop it and note in Step 11 that its default `enforce` applied).
Flavor-specific details this orchestrator doesn't pre-ask (Laravel starter kit and database, the WordPress
function/constant prefix and whether blocks are built with `@wordpress/scripts`, the PrestaShop module `tab` and
hooks) are asked inside the scaffold skill.

If the sub-skill reports that the user **stopped** before a usable project existed (or the manifest exists but is
unusable), stop this skill too — there's no project identity to build docs or CI around. A **Keep as is** on an
existing `composer.json` is fine: continue, presuming the existing project is valid enough for the rest of the
pipeline.

## Step 6 — Run `iru-setup-antora`

`Agent({description: "Run setup-antora", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke Skill({skill:
\"iru-setup-antora\"}) with no args (or, only if Step 0's args carried it, args \"on-existing: <on-existing>\") — it
derives the component name, title, and version from the repository (composer.json, the plugin/theme header or
module class, README). Let every AskUserQuestion through. Report back: scratch or update, the action taken for an
existing site (created / updated / replaced / kept as is), which files/pages were created vs already present, and
whether the site build succeeded.", run_in_background: false})`.

Run it *before* Step 8: `iru-setup-php-github-workflows` checks for `docs/antora.yml`/`docs/antora-playbook.yml` in
its survey — running Antora first means its docs job has something to build instead of a gap to report. Antora's
`docs/` directory must also stay out of the WordPress/PrestaShop release zip: check that the scaffold's
`.distignore` (or the module's packaging exclusion list) covers `docs/`, and flag it in Step 11 if it doesn't.

## Step 7 — Run `iru-setup-php-gitignore`

`Agent({description: "Run setup-php-gitignore", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-php-gitignore\"}) with no args (or, only if Step 0's args carried it, args \"on-existing:
<on-existing>\" — the only key it accepts), deriving the flavor and tooling from the repository. Let every
AskUserQuestion through. Report back only whether .gitignore was created, updated, replaced, or kept as is, and
which conditional sections it included.", run_in_background: false})`.

After Steps 5–6 (it detects the flavor, `@wordpress/scripts`, the quality tools' caches, and the Antora build output
from what's now on disk), and before Step 8 so `vendor/`, `build/`, and the test caches are ignored before CI-style
reports appear locally.

## Step 8 — Run `iru-setup-php-github-workflows`

**Skip this step entirely when `ci: no`**: don't invoke the sub-skill, write no `.github/workflows/*`,
`security.yml`, `.github/dependabot.yml`, or sync script, and leave any workflow files already on disk untouched.
Record "skipped (ci: no)" for the workflows and Dependabot components in Step 11, and that the shared security block
(Dependabot, dependency-review, CodeQL, OSV-Scanner, gitleaks) was skipped with them —
`/iru-setup-php-github-workflows` adds it all later.

Otherwise (filtering the keys against that skill's own Step 0 exactly as in Step 5):

```
Agent({
  description: "Run setup-php-github-workflows",
  subagent_type: "iru-isolated-skill-executor",
  prompt: "Invoke Skill({skill: \"iru-setup-php-github-workflows\", args: \"flavor: <flavor>\\n
    integration-branch: <integration-branch>\\nstable-branch: <stable-branch>\\nphp-version: <php-version>\\n
    open-source: <open-source>\\nvisibility: <visibility>\\nci-tests: <ci-tests>\\npages: <pages>\\n
    distribution: <distribution>\\nsonar: <sonar>\\nsonar-organization: <..., if set>\\n
    sonar-project-key: <..., if set>\\nsonar-host-url: <..., if set>\\nmode: <mode>\\n
    on-existing: <on-existing, only if supplied via args>\"}). Let every AskUserQuestion through. Report back:
    scratch or update; per file (build.yml/release.yml/sync.yml + its script/security.yml/.github/dependabot.yml)
    created, updated, replaced, kept as is (with mismatches), not written (release.yml with distribution: none), or
    stopped; whether actionlint passed; the full required-secrets table and repository-settings notes; and every open
    gap it flagged.",
  run_in_background: false
})
```

`flavor` here is this orchestrator's four-value `flavor` (the workflows skill needs to tell a plugin from a theme).
`ci` itself is never forwarded (invoking the skill means CI is wanted), and the four `security-*` keys are left at
their `yes` default — note that once in Step 11 rather than asking per run. If the user chose to stop inside it,
note it in Step 11; the scaffold, docs, and `.gitignore` from Steps 5–7 stand on their own.

## Step 9 — Run `iru-setup-changelog`

`Agent({description: "Run setup-changelog", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-changelog\"}) with no args (or, only if Step 0's args carried it, args \"on-existing:
<on-existing>\"), working from the repository's own git tag/GitHub Release history. Let every AskUserQuestion
through. Report back only whether CHANGELOG.md was created (and the version range reconstructed), updated (releases
appended), replaced, or kept as is.", run_in_background: false})`. Independent of Steps 5–8; it runs before Step 10
so the README's Documentation section links an existing `CHANGELOG.md`. For WordPress, the `== Changelog ==` section
of `readme.txt` is the scaffold's concern, not this step's — mention in Step 11 that the two should be kept in step
at release time (`iru-release` updates `CHANGELOG.md`).

## Step 10 — Run `iru-setup-readme`

`Agent({description: "Run setup-readme", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-readme\", args: \"sonar: <sonar>\\nci: <ci>\\npages: <pages, or no when ci: no>\\n
on-existing: <on-existing, only if supplied via args>\"}) — sonar: none suppresses Sonar badges/links, ci: no omits
CI badges, pages: no avoids a github.io docs link — deriving everything else from the repository (composer.json, the
plugin/theme header or module class, the Antora docs, the workflows, sonar-project.properties, CHANGELOG.md). For
the installation section: a Laravel app gets 'run it locally' (composer install, .env from .env.example, php
artisan key:generate/migrate, composer run dev) plus the container image when release.yml publishes one; a
WordPress plugin/theme gets the WordPress.org install path when distribution is store, the release-zip upload path
otherwise, and wp-env for development; a PrestaShop module gets the Back Office 'Upload a module' path with the
release zip. Report back only whether README.md was created, updated, replaced, or kept as is, and which sections
were included vs omitted and why.", run_in_background: false})`.

Run it last: its badges, status table, and links are only as complete as what Steps 5–9 left on disk. In
`mode: new` many sections stay sparse (no tags, no CI runs yet) — expected; it omits what it can't confirm.

## Step 11 — Report

Summarize all six delegated skills together: repeat Step 1's **Setup mode** statement (from scratch vs updating an
existing repository); the resolved `flavor` and `mode`; the identity and license (or "taken from the existing
files"); `php-version` and where it came from (php.net active support, the Laravel skeleton's floor, PrestaShop's
system requirements, or `args`); the branches. Then a per-component table — Composer manifest, flavor sources, tests
config, quality configs, Sonar config, UI quality config (`.ui-quality.yml`), Antora docs, `.gitignore`, each
workflow file (`build.yml`/`release.yml`/`sync.yml` + script/`security.yml`), `.github/dependabot.yml`,
`CHANGELOG.md`, `README.md` — with the action actually taken as each sub-skill reported it: **created / updated /
replaced / kept as is / skipped (ci: no) / not written (distribution: none)** (or stopped), plus every mismatch a
sub-skill listed for a kept file. Include Step 5's verification results (tests, coverage, static analysis, style,
browser UI tests; anything unverified, e.g. no Docker for wp-env, no shop for PrestaShop).

State explicitly what was wired or deliberately omitted, and why:

- **`open-source`** / **`visibility`** — as resolved, and where visibility came from (`args`, `gh repo view`, the
  user). When private/internal with `ci: yes`, repeat the included-minutes note (per GitHub's current pricing —
  double-check your plan).
- **`ci`** — with `no`: no workflows, no `security.yml`, no Dependabot, the shared security block skipped,
  `/iru-setup-php-github-workflows` adds them later.
- **`ci-tests`** — `unit` or `full`, with the flavor-specific meaning from Step 4 — omitted when `ci: no`.
- **`pages`** — `yes` (defaulted for public, or chosen) / `no` (docs uploaded as a workflow artifact only) — omitted
  when `ci: no`.
- **`distribution`** — the flavor-specific meaning from Step 4 and whether `release.yml` was written; for
  `prestashop-module` + `store`, that the Addons upload stays manual; for WordPress + `store`, that the directory
  slug must be approved before the first deploy.
- **`sonar`** — `cloud`/`self-hosted`/`none`; whether `sonar-project.properties` and the CI analysis step were
  included; for `none`, whether that's the expected default (not open source, not public, or `ci: no`) or a direct
  choice; for cloud/self-hosted with `ci: no`, that no CI step sends reports.
- **`accessibility`** — `enforce`/`report`/`off`/`none` as written to `.ui-quality.yml`, and where the browser UI tests
  (Playwright + axe-core, screenshots under `.ui-screenshots/`) run: locally behind `.integration-test.lock`, and in
  CI only where the workflows step wired them (each flavor's `ci-tests: full` integration job, against the server,
  wp-env test instance or shop it already starts; with `ci-tests: unit`, nowhere).
- The four `security-*` jobs left at their `yes` default (Step 8), and the per-flavor license ordering (Step 2) —
  both decided on the user's behalf.

Unless Step 8 was skipped, reproduce the required-secrets table and repository-settings notes
`iru-setup-php-github-workflows` reported (workflow permissions allowing PR creation for `sync.yml`, Pages source =
GitHub Actions when `pages: yes`, GHCR package visibility for a Laravel image, WordPress.org SVN credentials for
`store`) verbatim — don't re-derive or expand it.

Finish with **Warn explicitly**, repeating the sub-skills' own warnings: **review every generated file before
building, committing, or relying on CI** — `composer test`, `composer lint`, and `composer format:check` should pass
locally; the license must match an actual `LICENSE` file if one was chosen (`/iru-check-license` can generate one and
backfill headers), and for WordPress the `License:` header and `readme.txt` must agree with it; real secrets belong
in `.env` (never committed) or CI secrets, not in `config/` or the plugin; a `SONAR_TOKEN` secret and a matching Sonar
project must exist before a CI scan succeeds; registry/directory credentials named in the secrets table must exist
before a release publishes; the development version convention is `x.y.z-dev` (bumped by `iru-php-bump-version`
through `iru-release`); and every dependency/action version came from a run-time lookup or its recorded fallback —
run `composer outdated` before relying on the scaffold long-term.
