---
name: iru-setup-php-gitignore
description: >-
  Create or update the root `.gitignore` file for a PHP/Composer project — `vendor/`, Composer credentials
  (`auth.json`), PHPUnit/Pest caches (`.phpunit.cache/`, `.phpunit.result.cache`), report output (`build/` holding
  `build/logs/clover.xml`/`junit.xml` and coverage HTML), quality-tool caches (PHP-CS-Fixer, PHPCS, a PHPStan
  `tmpDir` inside the project), env files (keeping `.env.example`), OS and editor noise, the repository-wide
  `.integration-test.lock/` directory, the UI tests' screenshot directory `.ui-screenshots/` (every flavor renders
  UI) — and, when detected, flavor-specific paths for a Laravel application
  (following the Laravel skeleton's own `.gitignore`: `public/build`, `public/hot`, `public/storage`,
  `storage/*.key`, IDE-helper files), a WordPress plugin or block theme (`node_modules/`, `@wordpress/scripts`
  `build/` output, release `*.zip`, `.wp-env.override.json`), Playwright browser UI test output (`test-results/`,
  `playwright-report/`, `blob-report/`, `/playwright/.cache/`, plus `@wordpress/scripts`' `artifacts/` for
  WordPress), a PrestaShop module (`config_*.xml` caches, release `*.zip`, while `config.xml` stays tracked), and an
  Antora docs build. Never ignores `composer.lock`
  (committed for apps, plugins, themes, and modules alike). Invoke as `/iru-setup-php-gitignore`, optionally with an
  `args` line setting `on-existing` to `ask`/`keep`/`update`/`replace` (default `ask`) for scripted runs. Announces
  whether it is creating `.gitignore` from scratch or updating an existing one; if one already exists it never
  overwrites it silently — it warns, shows the proposed merge as a diff, and asks Update (merge, keeping hand-added
  entries) / Keep as is / Replace (template only, hand-added entries lost). Mirrors `iru-setup-typescript-gitignore`
  and `iru-setup-java-gitignore` for the PHP ecosystem. Use whenever a Laravel, WordPress, PrestaShop, or plain
  Composer project needs a `.gitignore` bootstrapped from scratch, or an existing one checked against this house
  template without touching it unless the user approves.
model: haiku
---

# Setup PHP Gitignore

Create or refresh the root `.gitignore` for a PHP/Composer project. Never overwrite an existing `.gitignore` without
showing the user exactly what would change and getting explicit approval first — a `.gitignore` can carry
hand-added, project-specific entries that must not be silently dropped.

## Step 0 — Parse `args`

This skill takes a single optional key, as a `key: value` line in `args`: `on-existing` (`ask`/`keep`/`update`/
`replace`, default `ask`) — how to treat an existing `.gitignore` in scripted runs (an orchestrator forwards it only
if its own `args` received it). Ignore any other key (orchestrators may pass shared keys such as `mode` or `flavor`;
the flavor is detected in Step 3 from the files themselves, and `mode: existing` alone doesn't skip Step 5's
question). If `args` is absent or unparseable, treat `on-existing` as `ask`.

## Step 1 — Check whether `.gitignore` already exists at the repository root

- **Not found**: tell the user "Creating `.gitignore` **from scratch** — none found." Continue to Step 2. Because
  there's nothing to lose, the final write happens without needing approval — go straight from composing the content
  to writing it, then report in Step 6.
- **Found**: tell the user "**Updating existing `.gitignore`**" and warn that one already exists, so this skill will
  propose changes for them to review rather than overwrite it silently. Read its current content now — it matters
  later, both to avoid proposing duplicate entries and because Step 4 must preserve any hand-written,
  project-specific lines this skill doesn't know how to regenerate. If `on-existing: keep`, stop here: leave the file
  untouched and go straight to Step 6's report. Otherwise continue to Step 2.

## Step 2 — The universal base template

Every PHP/Composer project gets this baseline, regardless of flavor:

```gitignore
# Composer
/vendor/
composer.phar
# Composer credentials for private repositories / tokens — never commit
/auth.json

# Test / coverage / report output (Clover + JUnit under build/logs/, coverage HTML)
/build/
/coverage/

# PHPUnit / Pest caches (PHPUnit 10+ cacheDirectory, and the PHPUnit 9 result cache)
.phpunit.cache/
.phpunit.result.cache

# Code-style caches (PHP-CS-Fixer, incl. the pre-v3 name)
.php-cs-fixer.cache
.php_cs.cache

# Environment files (never commit real secrets; the example file documents the shape)
.env
.env.backup
.env.production
.env.local
.env.*.local

# Logs
*.log

# Repository-wide lock the coding skills use to serialize container-backed test runs
.integration-test.lock/

# UI test screenshots (regenerated on every UI test run; the docs copy the ones they use into images/ui/)
.ui-screenshots/

# OS noise
.DS_Store
Thumbs.db

# IDE noise
.idea/
.fleet/
.zed/
.nova/
.phpactor.json

# VS Code — ignore the directory but keep the shared, non-machine-specific config files
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
!.vscode/launch.json
!.vscode/tasks.json
```

This section is unconditional — include it verbatim regardless of flavor, with two adjustments when an existing
`.gitignore` already decides otherwise:

- **`.vscode`**: if the existing file ignores the whole directory (`/.vscode` or `.vscode/`, as the Laravel skeleton
  does), keep that line and leave out the template's `.vscode/*` + `!` block — git can't re-include files under an
  excluded directory, so the two would contradict each other.
- **Env files**: `.env.example` (and Laravel's `.env.testing`, which holds test-only settings) stay tracked — that's
  why the template lists explicit names instead of `.env*`. If the existing file uses `.env*` with `!.env.example`,
  keep it and don't add the explicit lines.

**`composer.lock` is never ignored — and if an existing `.gitignore` ignores it, propose removing that line** (call
it out explicitly in Step 5's question). Rationale, per what this catalog scaffolds:

- **Laravel application**: the lock is what makes `composer install` reproduce the exact tested dependency set in CI,
  in the container image, and in production — the Composer documentation's standard advice for applications.
- **WordPress plugin/theme, PrestaShop module**: they're deployed artifacts, not libraries resolved by a consumer's
  Composer — `vendor/` is built into the release zip with `composer install --no-dev`, so the lock is what makes two
  builds of the same tag ship the same code, and it's what `composer audit`, Dependabot, and OSV-Scanner read.
- **Plain Composer library** (not scaffolded here): the lock doesn't affect consumers (their own resolution wins),
  but committing it keeps the library's own CI and contributors on a known-good tool/test set; this catalog commits
  it there too. A project that deliberately doesn't is respected — keep its existing ignore line if the user says so
  in Step 5.

**Note on `/build/`**: report tools write `build/logs/clover.xml`, `build/logs/junit.xml`, and coverage HTML there,
and `@wordpress/scripts` writes compiled block assets to `build/`. Some WordPress plugins deliberately **commit**
their compiled `build/` (the `@wordpress/create-block` template does not ignore it). If `.gitignore` doesn't exist
yet, check `git ls-files -- build coverage` before assuming; when files are already tracked there, ask via
`AskUserQuestion` whether to keep ignoring the directory (and untrack it — the release job then has to run
`npm run build` before packaging) or narrow the entry to `/build/logs/` + `/build/coverage/` — never ignore a
directory out from under tracked files without asking.

## Step 3 — Detect the flavor and project-specific additions

Don't guess; only add a section below when the thing it targets is actually present. Use the same markers
`iru-explore` and `iru-setup-php-repository` rely on: `composer.json`, `artisan`, a root PHP file with a `Plugin
Name:` header, a root `style.css` with `Theme Name:` / `theme.json`, a root `<module>.php` whose class `extends
Module` (or `PaymentModule`/`CarrierModule`) / `config.xml`, `package.json`, `phpcs.xml.dist`/`.phpcs.xml.dist`/
`phpcs.xml`, `phpstan.neon`/`phpstan.neon.dist`, and `docs/antora.yml`.

- **Laravel application** (`composer.json` requires `laravel/framework` and an `artisan` file exists): add the
  entries the Laravel skeleton's own root `.gitignore` carries that the base doesn't already cover:
  ```gitignore
  /node_modules
  /public/build
  /public/hot
  /public/storage
  /public/fonts-manifest.dev.json
  /storage/*.key
  /storage/pail
  /.codex
  /.cursor/
  _ide_helper.php
  _ide_helper_models.php
  .phpstorm.meta.php
  Homestead.json
  Homestead.yaml
  ```
  (`public/build` + `public/hot` are Vite's output and dev-server marker, `public/storage` is the `storage:link`
  symlink, `storage/*.key` are the Passport/encryption keys, `_ide_helper*.php`/`.phpstorm.meta.php` are
  barryvdh/laravel-ide-helper output.) The skeleton also ships **nested `.gitignore` files** — `storage/app/`,
  `storage/app/{public,private}/`, `storage/framework/` and its `cache/`, `cache/data/`, `cache/locks/`,
  `sessions/`, `testing/`, `views/`, `storage/logs/`, `bootstrap/cache/`, and `database/` (`*.sqlite*`). They're part
  of the scaffold, not this skill's file: never delete or fold them into the root file. Only if one of them is
  missing in an existing app, add the root-level equivalent so runtime files can't be committed:
  ```gitignore
  /storage/app/*
  !/storage/app/public/
  !/storage/app/private/
  /storage/framework/cache/*
  /storage/framework/sessions/*
  /storage/framework/testing/*
  /storage/framework/views/*
  /storage/logs/*
  /bootstrap/cache/*.php
  /database/*.sqlite*
  ```
  and mention in Step 6 which nested files were missing.

- **WordPress plugin or theme** (a root plugin header or `style.css` `Theme Name:` / `theme.json`): add
  ```gitignore
  # WordPress
  # Release archives (wp-scripts plugin-zip, wp dist-archive, the release job)
  *.zip
  # Per-developer @wordpress/env overrides (the shared .wp-env.json stays tracked)
  .wp-env.override.json
  ```
  If a `package.json` exists (asset tooling, `@wordpress/env`, `@wordpress/scripts`), also add the Node section below.
  When `@wordpress/scripts` is in `package.json` devDependencies, its compiled output lands in `build/` — already
  covered by the base `/build/` entry, subject to the tracked-files check in Step 2. Nothing else from WordPress core
  belongs here: `@wordpress/env` keeps its WordPress install outside the repository (`~/.wp-env`), and
  `bin/install-wp-tests.sh` installs the test library under the system temp directory.

- **PrestaShop module** (a root class that `extends Module`/`PaymentModule`/`CarrierModule`, usually with
  `config.xml`): add, matching PrestaShop's own native modules (e.g. `ps_emailsubscription`, `ps_facetedsearch`):
  ```gitignore
  # PrestaShop
  # Per-language module-list caches PrestaShop regenerates; config.xml itself stays tracked
  /config_*.xml
  # Release archive of the module
  *.zip
  ```
  **`config.xml` stays tracked**: PrestaShop regenerates it when missing, but committing it keeps the module's
  `<version>` in sync with the class (which `iru-php-bump-version` relies on when the file is tracked) and makes the
  module list show correct metadata before the first install. If the module builds front-end assets (a `package.json`
  with a build script, typically into `views/dist/`), add the Node section and that output directory.

- **Node tooling** (`package.json` at the root, any flavor not already covered by the Laravel section's
  `/node_modules`): add
  ```gitignore
  node_modules/
  npm-debug.log*
  .eslintcache
  ```

- **Playwright browser UI tests** (`@playwright/test` or `@wordpress/scripts` in `package.json` devDependencies, or a
  `playwright.config.*` at the root — what `iru-setup-php-laravel`, `iru-setup-php-wordpress` and
  `iru-setup-php-prestashop` scaffold): add
  ```gitignore
  # Playwright (browser UI tests) — run output, HTML/blob reports, local browser cache
  /test-results/
  /playwright-report/
  /blob-report/
  /playwright/.cache/
  ```
  and, for a WordPress plugin/theme whose tests run through `wp-scripts test-playwright` (its config writes
  traces/screenshots to `artifacts/`):
  ```gitignore
  /artifacts/
  ```
  Screenshots the UI contract asks for go to `.ui-screenshots/` (base template), not to these directories.

- **PHPCS cache** (`phpcs.xml.dist`/`.phpcs.xml.dist`/`phpcs.xml` sets `<arg name="cache" .../>`): ignore the exact
  path its `value` names (e.g. `.phpcs-cache`); if the `cache` arg has no value, PHPCS uses the system temp directory
  and nothing is added.

- **PHPStan `tmpDir` inside the project** (`phpstan.neon`/`phpstan.neon.dist`/`tests/phpstan/phpstan.neon` sets
  `parameters.tmpDir` to a relative path such as `var/phpstan` or `.phpstan-cache`): ignore that path, unless it's
  under `build/` (already covered). By default PHPStan uses the system temp directory and nothing is added. Also
  ignore a project-local `phpstan.neon` when the tracked config is `phpstan.neon.dist` (PHPStan's convention for a
  per-developer override).

- **Antora documentation build output** (`docs/antora.yml` or `docs/antora-playbook.yml` exists — see
  `iru-setup-antora`): add
  ```gitignore
  docs/build/
  docs/node_modules/
  ```

- Don't invent additional entries beyond what's actually detected — a project with no Node tooling, no Antora docs,
  or no PHPCS cache gets no section for them.

## Step 4 — Compose the proposed content

Concatenate Step 2's base template with whichever Step 3 sections matched, each under its own comment header for
readability (e.g. `# Laravel`, `# WordPress`, `# PrestaShop`, `# Node`, `# Playwright`, `# Antora`). Drop any line
that duplicates one already present (including path-equivalent forms such as `/vendor` vs `/vendor/`, and
`/node_modules` vs `node_modules/`). If Step 1 found an existing `.gitignore`, compose two drafts:

- **Merged** (the Update draft): keep every existing line that isn't already covered by the composed template
  (hand-added project-specific ignores must survive), add only the missing template lines, and **remove** a
  `composer.lock` ignore line (Step 2) — the one deliberate deletion, listed in Step 5's question.
- **Template-only** (the Replace draft): exactly the composed template. Note which existing lines it would drop.

## Step 5 — If `.gitignore` already existed, get approval before writing

Skip this step entirely if Step 1 found no existing file — proceed straight to Step 6's write.

- Show the user the merged draft as a diff against the current file (writing the draft to a temp path and running
  `git diff --no-index <current> <draft>` gives a clean unified diff). If the merged draft is identical to the
  current file, say so, treat the outcome as "kept as is", and skip the question.
- If `on-existing` is `update` or `replace`, apply it without asking (still show the diff of what is being
  written). Otherwise ask via `AskUserQuestion` (header `.gitignore`), with these consequences in the option
  descriptions:
  - **Update (Recommended)** — "Write the merged draft: add the missing entries from this skill's template and keep
    every line you added by hand. You've seen the diff; nothing you customized is dropped." — plus, when it applies,
    "…except the `composer.lock` ignore line, which is removed so the lock is committed (see rationale)".
  - **Keep as is** — "Leave `.gitignore` untouched. Your entries stay exactly as they are, but vendor/test/tooling
    output the template would ignore (listed in the diff) may show up as untracked files."
  - **Replace** — "Write the template-only draft. Matches this house template exactly, but the hand-added lines
    listed below are lost (recoverable only from git history)." — list those lines in the question text.
  There is no partial-apply option — if the user wants only some of the proposed lines (e.g. keep ignoring
  `composer.lock` for a library), let them say so in free text and revise the draft before writing.
- Only proceed to Step 6's write on **Update** or **Replace**; on **Keep as is**, write nothing.

## Step 6 — Write `.gitignore` and report

Write the chosen draft to `.gitignore` at the repository root — or nothing, if it was kept as is. Then summarize:
whether this run was from scratch or an update, the action taken (**created / updated / replaced / kept as is**, and
whether that came from the user's answer or from `on-existing`), the detected flavor, which conditional sections from
Step 3 were included versus skipped and why (e.g. "no Node section — no `package.json`", "no PHPCS cache entry —
`phpcs.xml.dist` sets no cache path", "no Playwright section — no `playwright.config.*` or Playwright dependency"),
any Laravel nested `.gitignore` files found missing, whether a `composer.lock` ignore line was removed, and — if
`.gitignore` already existed — which hand-added lines were preserved (Update) or dropped (Replace).

**Warn explicitly**:

- Review the generated `.gitignore` before committing — detection is heuristic (manifest/config-file signals), not a
  guarantee that every relevant path was found.
- If the repository already had files tracked under a path this skill now ignores (a committed `vendor/`, `build/`,
  or `auth.json`), `git rm -r --cached` it manually after reviewing the diff — writing `.gitignore` alone does not
  untrack already-committed files. A committed `auth.json` or `.env` may contain credentials: rotate them, since
  they remain in git history.
- Commit `composer.lock`; for WordPress/PrestaShop, the release zip is built from it with `composer install
  --no-dev`, so `vendor/` is never committed.
- Which values were verified versus inferred: the Laravel section was checked against the root and nested
  `.gitignore` files of a fresh `composer create-project laravel/laravel` (Laravel 13 skeleton) when this skill was
  authored, and the PrestaShop section against PrestaShop's own native modules' `.gitignore` files; the WordPress
  section follows the `@wordpress/create-block` template and the `@wordpress/env` documentation; every other Step 3
  entry is inferred from local config signals and should be spot-checked against the project's actual generated
  output.
