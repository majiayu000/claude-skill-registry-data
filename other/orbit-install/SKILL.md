---
name: orbit-install
description: One-shot installer for every Orbit dependency — Node tooling, PHP CodeSniffer / WPCS / VIP / PHPCompatibility, PHPStan, Psalm, Rector, Playwright + browsers, Lighthouse, axe-core, WP-CLI, @wordpress/env, wp-now, WPScan, claude-mem, and 13 Claude Code skills. Use when the user says "install Orbit", "install power tools", "install everything", "missing tool", or any earlier skill flagged a `command not found` error.
---

# Orbit — Power Tools Installer

You install **everything Orbit needs** in one shot. Nobody should have to guess which version of which tool — the installer pins working versions and verifies after each step.

---

## Step 1 — Run the installer

```bash
cd ~/Claude/orbit          # or wherever Orbit is cloned
bash setup/install.sh
```

This is idempotent — running it twice is safe.

For the *full power kit* (Psalm, Rector, WPScan, claude-mem, etc.):
```bash
bash scripts/install-power-tools.sh
```

---

## What gets installed (and why)

### Core (always needed)

| Tool | Purpose | Verify |
|---|---|---|
| Node 18+ | Playwright, wp-env, Lighthouse | `node -v` |
| Docker Desktop | wp-env containers | `docker ps` |
| PHP 7.4+ | `php -l`, PHPCS, PHPStan | `php -v` |
| Composer | PHP package manager | `composer --version` |
| WP-CLI | i18n / DB / CLI tasks | `wp --version` |
| @wordpress/env | Test sites | `wp-env --version` |
| Playwright | Browser tests | `npx playwright --version` |
| Lighthouse | Core Web Vitals | `lighthouse --version` |

### PHP quality stack

| Tool | What it adds |
|---|---|
| `squizlabs/php_codesniffer` | The phpcs runner |
| `wp-coding-standards/wpcs` | WordPress sniffs |
| `automattic/vipwpcs` | VIP-grade sniffs (stricter) |
| `phpcompatibility/phpcompatibility-wp` | PHP version compatibility |
| `phpstan/phpstan` + `szepeviktor/phpstan-wordpress` | Level 5 static analysis with WP stubs |
| `vimeo/psalm` (optional) | Alternative analyser |
| `rector/rector` (optional) | Automated PHP 7→8 refactor |
| `phpbench/phpbench` (optional) | Microbenchmarks |

### JS / CSS / browser

| Tool | What it does |
|---|---|
| Playwright + Chromium / Firefox / WebKit | E2E browser tests |
| `@wordpress/eslint-plugin` | WP-aware ESLint config |
| `@wordpress/stylelint-config` | WP-aware CSS linting |
| `@axe-core/cli` | Accessibility scanner |
| `lighthouse` + `@lhci/cli` | Performance / a11y / SEO scoring |
| `source-map-explorer` | Bundle size visualiser |
| `purgecss` | Detect unused CSS |

### WordPress-specific

| Tool | What it does |
|---|---|
| `WP-CLI` | Master tool — saves hours per day |
| `@wordpress/env` | Docker WP test sites |
| `wp-now` | Zero-config instant WP |
| `WPScan` | CVE scanner (needs free API token from wpscan.com) |

### Claude Code add-ons

| Tool | What it does |
|---|---|
| `claude-mem` | Persistent memory across Claude Code sessions |
| `ccusage` | Track token spend per session |

---

## Step 2 — Install Claude Code skills (mandatory for `/orbit-gauntlet`)

The 11 Orbit skills (already shipped in this repo's `skills/` folder) need to be symlinked into `~/.claude/skills/`:

```bash
bash setup/install-skills.sh
```

This symlinks each `skills/orbit-*` to `~/.claude/skills/orbit-*` so Claude Code finds them.

Plus install the 6 ecosystem skills the gauntlet relies on:

```bash
# Recommended — Antigravity CLI (puts everything in ~/.claude/skills/)
npx antigravity-awesome-skills

# Or manual
git clone https://github.com/VoltAgent/awesome-agent-skills ~/Claude/awesome-agent-skills
ln -sf ~/Claude/awesome-agent-skills/skills/* ~/.claude/skills/
```

Verify:
```bash
ls ~/.claude/skills/ | grep -E '^(orbit|wordpress|security|performance|database|accessibility|code-review|playwright)'
```

Expected: ~25-30 entries.

---

## Step 3 — One-by-one verification

After install, run the dry-run:
```bash
bash scripts/gauntlet-dry-run.sh
```

Output: a checklist with ✓ or ✗ for each tool. For each ✗, the user gets the exact command to fix it.

---

## Manual install commands (if `install.sh` chokes)

### macOS via Homebrew

```bash
brew install node@20 php@8.2 composer wp-cli
brew install --cask docker
npm i -g @wordpress/env wp-now @lhci/cli @axe-core/cli source-map-explorer purgecss
npx playwright install chromium firefox webkit
composer global require squizlabs/php_codesniffer wp-coding-standards/wpcs \
  automattic/vipwpcs phpcompatibility/phpcompatibility-wp phpstan/phpstan \
  szepeviktor/phpstan-wordpress
```

After the composer step, ensure `~/.composer/vendor/bin` is on `$PATH`:
```bash
echo 'export PATH="$HOME/.composer/vendor/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Linux (Ubuntu / Debian)

```bash
# Node
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# PHP + Composer
sudo apt-get install -y php-cli php-curl php-mbstring php-xml php-zip composer

# Docker
sudo apt-get install -y docker.io docker-compose

# WP-CLI
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp

# Composer globals (same as macOS)
composer global require ... (see above)
```

---

## Common install failures

### `phpcs: command not found` after install
PATH issue. Add Composer's global bin to PATH:
```bash
echo 'export PATH="$HOME/.composer/vendor/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### `npx playwright install` hangs
Network issue or Apple Silicon Rosetta problem. Try:
```bash
PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/ms-playwright npx playwright install --force chromium
```

### `composer install` runs out of memory
```bash
COMPOSER_MEMORY_LIMIT=-1 composer global require ...
```

### `WPScan` requires API token
Sign up at https://wpscan.com (free tier: 75 requests/day). Add to `~/.zshrc`:
```bash
export WPSCAN_API_TOKEN=your-token-here
```

### Docker pulls the wrong architecture image (Apple Silicon)
```bash
DOCKER_DEFAULT_PLATFORM=linux/amd64 wp-env start
```

---

## Output summary

After successful install:

```
✅ Orbit power tools installed

Core:
  ✓ Node 20.x      ✓ PHP 8.2      ✓ Composer 2.x
  ✓ Docker         ✓ WP-CLI       ✓ wp-env

Browser:
  ✓ Playwright 1.x with Chromium / Firefox / WebKit
  ✓ Lighthouse 11.x
  ✓ axe-core CLI

PHP quality:
  ✓ PHPCS + WPCS + VIP + PHPCompatibility
  ✓ PHPStan level 5 + WordPress stubs

Skills:
  ✓ 11 Orbit skills symlinked to ~/.claude/skills/

Next:
  /orbit-init           configure your first plugin
  /orbit-docker-site    spin up a test site
```

If any tool failed, list the failed tool + the exact command to retry.
