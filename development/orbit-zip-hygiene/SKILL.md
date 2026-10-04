---
name: orbit-zip-hygiene
description: Validate the contents of a WordPress plugin release zip — no dev artefacts (`.git/`, `.cursor/`, `.github/`, `.DS_Store`), no source maps, no `composer.json` / `package.json` (or strip dev deps), no forbidden functions in shipped code (`var_dump`, `phpinfo`, `error_reporting`), supply-chain audit on bundled vendor/. Use when the user says "validate zip", "zip hygiene", "dev files in zip", "before SVN submit", "check release zip".
---

# 🪐 orbit-zip-hygiene — Release zip validator

The "did anything sneak into my release zip" check. Runs against the actual zip you'd upload to WP.org.

---

## Quick start

```bash
# Validate the current plugin folder (as if zipped)
bash ~/Claude/orbit/scripts/check-zip-hygiene.sh ~/plugins/my-plugin

# Validate an actual zip
bash ~/Claude/orbit/scripts/check-zip-hygiene.sh ~/dist/my-plugin-2.4.0.zip
```

Or via gauntlet (Step 1b, runs in `full`/`release`):
```bash
bash scripts/gauntlet.sh --plugin . --mode full
```

---

## What it flags

### Dev artefacts (must NOT be in the zip)
- `.git/`, `.gitignore`, `.gitattributes`
- `.github/`, `.gitlab/`, `.circleci/`
- `.cursor/`, `.windsurf/`, `.vscode/`, `.idea/`
- `.DS_Store`, `Thumbs.db`
- `node_modules/`, `vendor/` (unless committed deliberately)
- `tests/`, `__tests__/`, `*.test.js`, `*.spec.js`
- Source: `src/`, `webpack.config.js`, `rollup.config.js`, `babel.config.js`, `tsconfig.json`
- Logs: `*.log`, `error_log`, `debug.log`
- Build output of build output: `dist/.cache/`, `coverage/`

### Source maps in production
- `*.map` files (these are for dev debugging only)
- Inline source maps in JS (`//# sourceMappingURL=`)

### Composer / package
- `composer.json`, `composer.lock` — strip if not needed at runtime
- `package.json`, `package-lock.json`, `yarn.lock`
- Dev-only composer deps still in `vendor/` (PHPUnit, PHPStan, etc.)

### Forbidden functions in shipped PHP
```php
var_dump( $x );           // ❌
print_r( $x );             // ❌
phpinfo();                 // ❌
error_reporting( E_ALL );  // ❌
ini_set('display_errors',1); // ❌
debug_backtrace();         // ⚠ (sometimes OK in error-handling)
```

### Supply-chain audit (`vendor/`)
- Each composer package checked against:
  - GPL compatibility
  - Known vulnerable versions
  - Active maintenance (last release < 2 years)
  - Author reputation

Powered by `composer audit` + custom heuristics.

---

## Severity

| Issue | Severity |
|---|---|
| `.git/` in zip | **Critical** (security: exposes commit history, sometimes secrets) |
| `composer.lock` exposing dev deps | High |
| `*.map` source maps | High |
| `var_dump` / `phpinfo` in shipped PHP | **Critical** |
| `node_modules/` | **Critical** (huge zip, useless to user) |
| `.DS_Store`, `Thumbs.db` | Low (just clutter) |
| Unmaintained vendor library | Medium (track for replacement) |

Critical or High → block release.

---

## Common fixes

### Use `.distignore` (preferred for SVN releases)
```
# .distignore — used by `wp dist-archive` and similar tools
.git
.github
.cursor
.vscode
.DS_Store
node_modules
vendor/bin
vendor/composer/installers
*.map
*.log
tests
src
*.config.js
package*.json
composer.lock
```

### Use a release script
```bash
#!/usr/bin/env bash
# scripts/build-release.sh
VERSION=$(grep '^Version:' my-plugin.php | awk '{print $2}')
DIST="dist/my-plugin-$VERSION"

rm -rf "$DIST"
rsync -a --exclude-from=.distignore . "$DIST/"

# Strip composer dev deps
( cd "$DIST" && composer install --no-dev --optimize-autoloader )

# Make zip
( cd dist && zip -r "my-plugin-$VERSION.zip" "my-plugin-$VERSION" )

# Validate
bash ~/Claude/orbit/scripts/check-zip-hygiene.sh "dist/my-plugin-$VERSION.zip"
```

### Or use `wp dist-archive`
```bash
wp dist-archive ~/plugins/my-plugin
# → respects .distignore, strips dev files, generates clean zip
```

---

## Output

```
[Zip Hygiene] my-plugin-2.4.0.zip — 12.4 MB

❌ Critical issues (3):
  - .git/ found in zip                 (5.2 MB)
  - var_dump in includes/class-debug.php:42
  - phpinfo() call in admin/legacy.php:18

⚠ High issues (2):
  - assets/js/main.js.map (source map shipped)
  - composer.lock present (consider .distignore)

⚠ Medium issues (1):
  - vendor/php-di/php-di — last release 3 years ago, consider replacing

ℹ Info (4):
  - .DS_Store × 14 files
  - Thumbs.db × 2 files

→ Block release. Fix Critical + High before submission.
```

---

## Strict mode (CI / release-gate)

```bash
bash scripts/check-zip-hygiene.sh --strict ~/plugins/my-plugin
```

Strict mode treats Medium as a fail too. Use in CI to enforce discipline.

---

## Pair with `/orbit-release-meta`

`/orbit-release-meta` validates **content** (headers, readme, version parity).
This skill validates **packaging** (what's in the zip).
Both run in `/orbit-release-gate`. Don't ship without both passing.

---

## Hard rule

**Never ship a zip with `.git/` in it.** That folder contains your full commit history including any leaked secrets, deleted files, and rebased commits. It's been the source of multiple WP plugin compromises. Always validate.
