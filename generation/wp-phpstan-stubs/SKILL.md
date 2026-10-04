---
name: wp-phpstan-stubs
description: "Use when creating a new PHPStan stubs package for a WordPress plugin, theme, or Composer package — scaffolding the full repo structure (composer.json, configs/bootstrap.php, configs/finder.php, bin/generate.sh, bin/release-latest-versions.sh, .github/workflows/release.yml, phpstan.neon), fetching version lists from WP.org plugin API (api.wordpress.org/plugins) or Packagist API, using php-stubs/generator, or setting up the GitHub release workflow with jq. Triggers: \"create stubs for X plugin\", \"scaffold PHPStan stubs\", \"new stubs package\", \"add PHPStan stubs for WooCommerce\", \"stubs repo setup\", \"generate stub file\", \"PHPStan cannot find this class\", \"missing type hints for third-party plugin\", \"add stubs for this Composer package\", \"php-stubs/generator\", \"bin/generate.sh\", \"configs/bootstrap.php for stubs\", \"configs/finder.php\", \"release-latest-versions.sh\", \"WP.org plugin API for versions\", \"Packagist API for versions\", \"jq regex error in stubs script\", \"GitHub Actions release workflow for stubs\", \"phpstan.neon for stubs package\". Not for: configuring phpstan.neon in a plugin project or generating baselines — use the official `wp-phpstan` skill."
---

# PHPStan Stubs Scaffold

> **Model note:** File scaffolding from a fixed template — `haiku` handles end-to-end. Only reach for `sonnet` if the source plugin has complex namespace hierarchies needing stub organization decisions.

Scaffold a complete PHPStan stubs package from scratch, following the `my-org/phpstan-freemius-stubs` standard structure.

## When to use

- "Create stubs for X", "new stubs package", "scaffold phpstan stubs", "add stubs for plugin/composer package".

**Not for:** Configuring `phpstan.neon` or generating baselines — use the official `wp-phpstan` skill. Adding PHPStan to a plugin that already has stubs installed.

## References

- `references/wp-org-api.md` — WP.org plugin API, version listing, download URLs, cleanup patterns
- `references/packagist-api.md` — Packagist API, version filtering, source/composer.json update pattern
- `references/common-errors.md` — Known errors and fixes (jq `\d`, unzip prompt, find+set-e, git reset, missing source/composer.json)
- `references/github-setup.md` — Repo creation, branch rename trunk→main, topics, secrets, all 11 current repos

## Gather Required Info

Before writing any files, collect (ask user if missing):

1. **Plugin/package name** — human-readable (e.g. "SureCart", "Action Scheduler")
2. **Source type** — one of:
   - `wp-plugin` — downloadable from WordPress.org (slug known)
   - `composer` — Composer package on Packagist (e.g. `woocommerce/action-scheduler`)
   - `paid` — paid plugin, user places source manually
3. **WP.org slug** (if `wp-plugin`) — e.g. `surecart`, `forminator`
4. **Packagist package** (if `composer`) — e.g. `woocommerce/action-scheduler`
5. **Source dir path inside package** — where the plugin/package files land:
   - `wp-plugin`: `source/<slug>/`
   - `composer`: `source/vendor/<vendor>/<package>/`
   - `paid`: `source/<slug>/`
6. **Packagist name** — `my-org/phpstan-<slug>-stubs`
7. **GitHub repo name** — `phpstan-<slug>-stubs`
8. **Versions to release** — for `wp-plugin`/`composer`: minor version series (e.g. `3.4 3.5 3.6`); for `paid`: manual
9. **GitHub assignee** — default `my-org`

## Standard Directory Layout

```
phpstan-<slug>-stubs/
├── bin/
│   ├── generate.sh
│   └── release-latest-versions.sh   # (not for paid)
├── configs/
│   ├── bootstrap.php
│   └── finder.php
├── source/
│   ├── composer.json                # only if wp-plugin or paid (no composer deps)
│   └── .gitignore
├── .github/
│   └── workflows/
│       └── release.yml              # (not for paid)
├── .editorconfig
├── .gitattributes
├── .gitignore
├── composer.json
├── phpstan.neon
└── <slug>-stubs.php                 # empty placeholder (generated)
    <slug>-constants-stubs.php       # empty placeholder (generated)
```

## File Contents

### `composer.json`

```json
{
    "name": "my-org/phpstan-<slug>-stubs",
    "description": "<PluginName> function and class declaration stubs for static analysis.",
    "type": "library",
    "keywords": [
        "<slug>",
        "wordpress",
        "static analysis",
        "phpstan",
        "stubs"
    ],
    "homepage": "https://github.com/my-org/phpstan-<slug>-stubs",
    "license": "MIT",
    "authors": [
        {
            "name": "Al Amin Ahamed",
            "homepage": "https://github.com/my-org"
        }
    ],
    "require": {
        "php": ">=7.4",
        "php-stubs/wordpress-stubs": "^5.3 || ^6.0"
    },
    "require-dev": {
        "php-stubs/generator": "^0.8.0",
        "phpstan/phpstan": "^2.0",
        "phpunit/phpunit": "^7.5 || ^8.5 || ^9.5",
        "squizlabs/php_codesniffer": "^3.7"
    },
    "minimum-stability": "stable",
    "prefer-stable": true,
    "config": {
        "allow-plugins": {
            "php-stubs/generator": true
        },
        "sort-packages": true,
        "optimize-autoloader": true,
        "preferred-install": "dist",
        "platform": {
            "php": "7.4.0"
        }
    },
    "scripts": {
        "post-install-cmd": [
            "@composer --working-dir=source/ update --no-interaction"
        ],
        "post-update-cmd": [
            "@composer --working-dir=source/ update --no-interaction"
        ],
        "generate": "bash bin/generate.sh",
        "release": "bash bin/release-latest-versions.sh"
    },
    "support": {
        "issues": "https://github.com/my-org/phpstan-<slug>-stubs/issues",
        "source": "https://github.com/my-org/phpstan-<slug>-stubs"
    }
}
```

**For `composer` source type** — `source/` has its own composer.json, so omit `post-install-cmd`/`post-update-cmd` from root composer.json and add them pointing to the source subdir instead. The source/composer.json requires the actual package:
```json
{
    "require": {
        "php": ">=5.6",
        "<vendor>/<package>": "<latest-stable-version>"
    },
    "minimum-stability": "stable"
}
```

**For `wp-plugin` and `paid`** — create `source/composer.json`:
```json
{"minimum-stability": "stable"}
```
And `source/.gitignore`:
```
/vendor/
/composer.lock
```

### `configs/bootstrap.php`

Standard WordPress constants file — copy verbatim from freemius, then append plugin-specific constants at bottom if needed:

```php
<?php

declare(strict_types=1);

// phpcs:disable Squiz.PHP.DiscouragedFunctions,NeutronStandard.Constants.DisallowDefine

define('ABSPATH', './');
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', true);
define('WP_PLUGIN_DIR', './');
define('WPMU_PLUGIN_DIR', './');
define('EMPTY_TRASH_DAYS', 30 * 86400);
define('SCRIPT_DEBUG', false);
define('WP_LANG_DIR', './');
define('WP_CONTENT_DIR', './');

define('MINUTE_IN_SECONDS', 60);
define('HOUR_IN_SECONDS', 60 * MINUTE_IN_SECONDS);
define('DAY_IN_SECONDS', 24 * HOUR_IN_SECONDS);
define('WEEK_IN_SECONDS', 7 * DAY_IN_SECONDS);
define('MONTH_IN_SECONDS', 30 * DAY_IN_SECONDS);
define('YEAR_IN_SECONDS', 365 * DAY_IN_SECONDS);

define('KB_IN_BYTES', 1024);
define('MB_IN_BYTES', 1024 * KB_IN_BYTES);
define('GB_IN_BYTES', 1024 * MB_IN_BYTES);
define('TB_IN_BYTES', 1024 * GB_IN_BYTES);

define('OBJECT', 'OBJECT');
define('OBJECT_K', 'OBJECT_K');
define('ARRAY_A', 'ARRAY_A');
define('ARRAY_N', 'ARRAY_N');

define('FS_CONNECT_TIMEOUT', 30);
define('FS_TIMEOUT', 30);
define('FS_CHMOD_DIR', 0755);
define('FS_CHMOD_FILE', 0644);
```

### `configs/finder.php`

```php
<?php

use StubsGenerator\Finder;

return Finder::create()
    ->in(array(
        '<source-dir-path>',
    ))
    ->sortByName(true)
;
```

Replace `<source-dir-path>` with the actual path (relative to project root):
- `wp-plugin`: `source/<slug>`
- `composer`: `source/vendor/<vendor>/<package>`
- `paid`: `source/<slug>`

Add `->notPath(...)` calls to exclude test dirs, docs, or large asset dirs that bloat the stubs.

### `bin/generate.sh`

```bash
#!/usr/bin/env bash
#
# Generate <PluginName> stubs from the source directory.
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

HEADER=$'/**\n * Generated stub declarations for <PluginName>.\n * @see <homepage-url>\n * @see https://github.com/my-org/phpstan-<slug>-stubs\n */'

FILE="$ROOT_DIR/<slug>-stubs.php"
FILE_CONSTANTS="$ROOT_DIR/<slug>-constants-stubs.php"
GENERATOR_BIN="$ROOT_DIR/vendor/bin/generate-stubs"
FINDER_FILE="$ROOT_DIR/configs/finder.php"

set -e

test -f "$FILE" || touch "$FILE"
test -f "$FILE_CONSTANTS" || touch "$FILE_CONSTANTS"
test -d "$ROOT_DIR/<source-dir-path>"

"$GENERATOR_BIN" \
    --include-inaccessible-class-nodes \
    --force \
    --finder="$FINDER_FILE" \
    --header="$HEADER" \
    --functions \
    --classes \
    --interfaces \
    --traits \
    --out="$FILE"

"$GENERATOR_BIN" \
    --include-inaccessible-class-nodes \
    --force \
    --finder="$FINDER_FILE" \
    --header="$HEADER" \
    --constants \
    --out="$FILE_CONSTANTS"
```

### `bin/release-latest-versions.sh` — WP.org plugin

Iterates minor version series (e.g. `2.0 2.1 ... 2.20`), finds latest patch, skips if tag exists, downloads, unzips, generates, commits, tags:

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
set -e

git -C "$ROOT_DIR" fetch --all
git -C "$ROOT_DIR" reset --hard origin/main

WP_JSON="$(wget -q -O- "https://api.wordpress.org/plugins/info/1.0/<slug>.json")"

for V in <minor-versions>; do
    printf -v JQ_FILTER '."versions" | keys[] | select(test("^%s\\.%s\\.[0-9]+$"))' "${V%.*}" "${V#*.}"
    LATEST="$(jq -r "$JQ_FILTER" <<<"$WP_JSON" | sort -t "." -k 3 -g | tail -n 1)"
    if [ -z "$LATEST" ]; then continue; fi
    if git -C "$ROOT_DIR" rev-parse "refs/tags/v${LATEST}" >/dev/null 2>&1; then
        echo "Tag exists for v${LATEST}, skipping..."
        continue
    fi
    rm -rf "$ROOT_DIR/source/<slug>" 2>/dev/null || true
    rm -f "$ROOT_DIR/source/<slug>."*.zip 2>/dev/null || true
    wget -q -P "$ROOT_DIR/source/" "https://downloads.wordpress.org/plugin/<slug>.${LATEST}.zip"
    unzip -q -o -d "$ROOT_DIR/source/" "$ROOT_DIR/source/<slug>.${LATEST}.zip"
    rm -f "$ROOT_DIR/source/<slug>.${LATEST}.zip"
    echo "Generating stubs for <PluginName> ${LATEST}..."
    "$SCRIPT_DIR/generate.sh"
    if git -C "$ROOT_DIR" diff-index --quiet HEAD --; then
        echo "No changes for ${LATEST}, skipping commit..."
    else
        git -C "$ROOT_DIR" commit --all -m "Generate stubs for <PluginName> ${LATEST}"
        git -C "$ROOT_DIR" tag "v${LATEST}"
    fi
done

git -C "$ROOT_DIR" push origin main --follow-tags
echo "Done."
```

**Minor version list format:** space-separated `MAJOR.MINOR` values, e.g. `1.0 1.1 1.2 ... 1.20 2.0 2.1`. The jq filter selects all patch versions matching `^MAJOR.MINOR.[0-9]+$` then takes the latest.

**CRITICAL jq regex note:** In jq string literals, use `[0-9]` not `\d`. The `printf -v JQ_FILTER` approach above uses `\\.[0-9]+` which renders correctly.

### `bin/release-latest-versions.sh` — Composer package

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
set -e

git -C "$ROOT_DIR" fetch --all
git -C "$ROOT_DIR" reset --hard origin/main

PACKAGIST_JSON="$(wget -q -O- "https://packagist.org/packages/<vendor>/<package>.json")"
VERSIONS=(<minor-versions>)

for V in "${VERSIONS[@]}"; do
    printf -v JQ_FILTER '."package"."versions" | keys[] | select(test("^%s\\.%s\\.[0-9]+$"))' "${V%.*}" "${V#*.}"
    LATEST="$(jq -r "$JQ_FILTER" <<<"$PACKAGIST_JSON" | sort -t "." -k 3 -g | tail -n 1)"
    if [ -z "$LATEST" ]; then continue; fi
    if git -C "$ROOT_DIR" rev-parse "refs/tags/v${LATEST}" >/dev/null 2>&1; then
        echo "Tag exists for v${LATEST}, skipping..."
        continue
    fi
    printf -v SED_EXP 's#\("<vendor>/<package>"\): "[^"]*"#\1: "%s"#' "${LATEST}"
    sed -i -e "$SED_EXP" "$ROOT_DIR/source/composer.json"
    composer --working-dir="$ROOT_DIR/source" update --no-interaction
    "$SCRIPT_DIR/generate.sh"
    if git -C "$ROOT_DIR" diff-index --quiet HEAD --; then
        echo "No changes for ${LATEST}, skipping commit..."
    else
        git -C "$ROOT_DIR" commit --all -m "Generate stubs for <PluginName> ${LATEST}"
        git -C "$ROOT_DIR" tag "v${LATEST}"
    fi
done

git -C "$ROOT_DIR" push origin main --follow-tags
echo "Done."
```

### `bin/release-latest-versions.sh` — Paid plugin

Accept VERSION as first argument, source must be pre-placed at `source/<slug>/`:

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
set -e

VERSION="${1:?Usage: $0 <version>}"

if git -C "$ROOT_DIR" rev-parse "refs/tags/v${VERSION}" >/dev/null 2>&1; then
    echo "Tag v${VERSION} already exists. Skipping."
    exit 0
fi

if [ ! -d "$ROOT_DIR/source/<slug>" ]; then
    echo "ERROR: Place <PluginName> ${VERSION} source at source/<slug>/ first."
    exit 1
fi

"$SCRIPT_DIR/generate.sh"
git -C "$ROOT_DIR" commit --all -m "Generate stubs for <PluginName> ${VERSION}"
git -C "$ROOT_DIR" tag "v${VERSION}"
git -C "$ROOT_DIR" push origin main --follow-tags
echo "Done."
```

### `.github/workflows/release.yml`

```yaml
name: Release new version

on:
  push:
    paths:
      - ".github/workflows/release.yml"
  schedule:
    - cron: '0 * * * *'

jobs:
  release-new-stubs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          extensions: json zip xdebug
          coverage: none
          tools: composer

      - name: Get Composer cache directory
        id: composer-cache
        run: echo "dir=$(composer config cache-files-dir)" >> $GITHUB_OUTPUT

      - name: Cache Composer dependencies
        uses: actions/cache@v4
        with:
          path: ${{ steps.composer-cache.outputs.dir }}
          key: "${{ runner.os }}-${{ hashFiles('**/composer.lock') }}"
          restore-keys: ${{ runner.os }}-composer-

      - name: Install dependencies
        run: composer install --prefer-dist --no-suggest --no-progress --no-interaction --ignore-platform-reqs

      - name: Set up Git user
        run: |
          git config user.name 'github-actions'
          git config user.email 'github-actions@github.com'

      - name: Release new stubs from latest version
        run: bash bin/release-latest-versions.sh

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.PERSONAL_TOKEN }}
          commit-message: Generate stubs from latest version
          committer: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
          author: ${{ github.actor }} <${{ github.actor_id }}+${{ github.actor }}@users.noreply.github.com>
          signoff: false
          delete-branch: true
          title: 'Generate stubs from latest version'
          body: |
            This PR updates stubs from the latest available version.
          labels: |
            update
            automated pr
          assignees: my-org
          draft: false
```

Omit this workflow entirely for `paid` source type.

### `phpstan.neon`

```neon
parameters:
    paths:
        - <slug>-stubs.php
    scanFiles:
        - <slug>-constants-stubs.php
    bootstrapFiles:
        - configs/bootstrap.php
    level: 5
    ignoreErrors:
        - '#but return statement is missing\.$#'
        - '#has an unused parameter#'
        - '#^(Property|Static property|Method|Static method) \S+ is unused\.$#'
        - '#is never read, only written\.$#'
        - '#has invalid (return )?type (WP_Error|WP_Customize_Manager|WP_Theme|WP_User|WP_Site|WP_Upgrader)#'
```

### `.gitignore`

```
/vendor/
/composer.lock
/report.txt
```

### `.gitattributes`

```
/.gitattributes     export-ignore
/.gitignore         export-ignore
/.travis.yml        export-ignore
/source             export-ignore
```

### `.editorconfig`

```
root = true

[*]
charset = utf-8
indent_size = 4
indent_style = space
insert_final_newline = true
trim_trailing_whitespace = true

[*.yml]
indent_size = 2
```

## Execution Steps

After writing all files:

1. **Init git and make first commit:**
   ```bash
   cd /path/to/phpstan-<slug>-stubs
   git init
   git branch -m trunk main
   git add .
   git commit -m "chore: initial scaffold for <PluginName> stubs"
   ```

2. **Create GitHub repo** (public):
   ```bash
   gh repo create my-org/phpstan-<slug>-stubs \
     --public \
     --description "<PluginName> function and class declaration stubs for static analysis." \
     --source=. \
     --remote=origin \
     --push
   ```
   Then ensure default branch is `main`:
   ```bash
   gh repo edit my-org/phpstan-<slug>-stubs --default-branch main
   ```

3. **Add GitHub topics:**
   ```bash
   gh repo edit my-org/phpstan-<slug>-stubs \
     --add-topic phpstan \
     --add-topic php \
     --add-topic stubs \
     --add-topic wordpress \
     --add-topic <slug>
   ```

4. **Install local dependencies:**
   ```bash
   composer install --ignore-platform-reqs
   ```

5. **Run first release** (if not `paid`):
   ```bash
   bash bin/release-latest-versions.sh
   ```
   For `paid`: instruct user to place source at `source/<slug>/` then run `bash bin/release-latest-versions.sh <VERSION>`.

## Common Mistakes to Avoid

| Mistake | Correct |
|---------|---------|
| `\d` in jq string literal | Use `[0-9]` |
| `git reset --hard origin/main` before committing fix | Always push fixes before re-running release |
| `unzip` without `-o` flag | Always use `unzip -q -o` to avoid interactive prompts |
| `find -exec rm -rf {} +` with `set -e` | Use `rm -rf source/<slug> 2>/dev/null || true` |
| `gh repo create` defaults to `trunk` branch | Always rename: `git branch -m trunk main` then `gh repo edit --default-branch main` |
| Packagist API: `repo.packagist.org/p2/` | Correct URL: `packagist.org/packages/<vendor>/<package>.json` |
| Packagist JSON path: `packages.x[]` | Correct path: `."package"."versions"` |
| Missing `source/composer.json` for wp-plugin | Creates `post-install-cmd` failure; always create `source/composer.json` |
