---
name: orbit-gauntlet
description: Run the full Orbit gauntlet — 11 sequential checks on a WordPress plugin (PHP lint, PHPCS, PHPStan, asset weight, i18n, Playwright, Lighthouse, DB profile, competitor compare, UI perf, AI skill audits, PM UX). Three modes — `quick` (3-5 min, dev loop), `full` (30-45 min, RC pass), `release` (45-60 min, WP.org submission). Use when the user says "run gauntlet", "audit my plugin", "full QA", "before release", or any unscoped "check my plugin" request.
argument-hint: --plugin <path> --mode quick|full|release
---

# 🪐 orbit-gauntlet — The full pipeline

The flagship Orbit command. One invocation, every quality angle.

> **Smart-agentic mandate.** `--mode full` and `--mode release` run **every step end-to-end**, no cherry-picking. `--skip N` is debug-only — using it for any release-track run requires a brain note (`orbit/08-release`) recording the reason. Smart-agentic = aggressive; conservative shipped 5 example-plugin i18n bugs. See `agents/_SMART-AGENTIC-MANDATE.md`.

---

## Quick start

```bash
# Daily dev loop — fast feedback (~3-5 min)
bash scripts/gauntlet.sh --plugin ~/plugins/my-plugin --mode quick

# Pre-PR / beta release — everything (~30-45 min)
bash scripts/gauntlet.sh --plugin ~/plugins/my-plugin --mode full

# Day-of-release — full + WP.org plugin-check (~45-60 min)
bash scripts/gauntlet.sh --plugin ~/plugins/my-plugin --mode release
```

Exit code: **0** = release ready · **1** = blockers found.

---

## Mode comparison

| Step | quick | full | release |
|---|:-:|:-:|:-:|
| 1. PHP lint | ✓ | ✓ | ✓ |
| 1a. Release metadata | ✓ | ✓ | ✓ |
| 1b. Zip hygiene | — | ✓ | ✓ |
| 2. PHPCS (WPCS + VIP) | ✓ | ✓ | ✓ |
| 3. PHPStan level 5 | ✓ | ✓ | ✓ |
| 4. Asset weight | ✓ | ✓ | ✓ |
| 5. i18n + POT (gettext) | — | ✓ | ✓ |
| 5a. i18n runtime (UNESCAPED_UNICODE) | — | ✓ | ✓ |
| 5b. i18n JS parity (wp_localize_script) | — | ✓ | ✓ |
| 5c. i18n translator currency (.po drift) | — | ✓ | ✓ |
| 5d. Polylang + WPML endpoint awareness | — | ✓ | ✓ |
| 5e. IP clean-room (reference leak + provenance) | — | ✓ | ✓ |
| 6. Playwright (smoke) | ✓ | full suite | full suite |
| 7. Lighthouse | — | ✓ | ✓ |
| 8. DB profiling | — | ✓ | ✓ |
| 9. Competitor compare | — | ✓ | ✓ |
| 10. UI / editor perf | — | ✓ | ✓ |
| 11. 6 AI skill audits | — | ✓ | ✓ |
| 12. PM UX (spell + label) | — | ✓ | ✓ |
| WP.org plugin-check | — | — | ✓ |
| Live CVE feed | — | — | ✓ |
| Ownership-transfer detect | — | — | ✓ |

---

## Reading the output

After every run:

```
reports/
├── qa-report-<timestamp>.md         ← markdown summary (start here)
├── playwright-html/index.html       ← interactive E2E report
├── skill-audits/index.html          ← tabbed AI audit (full + release only)
├── lighthouse/lh-<timestamp>.json   ← performance data
└── pm-ux/pm-ux-report-<timestamp>.html  ← PM-friendly view
```

Open the master index:
```bash
python3 scripts/generate-reports-index.py
open reports/index.html
```

---

## Severity triage

| Level | Action |
|---|---|
| **Critical** | Block release. Fix today. |
| **High** | Block release. Fix in this PR. |
| **Medium** | Fix if <30 min. Otherwise log. |
| **Low / Info** | Log. Defer. |

Any Critical or High in modes `full` / `release` → exit code 1.

---

## Common failures

### `wp-env not running on port 8881`
Site isn't up. Run `/orbit-docker-site` first.

### `phpcs: command not found`
Power tools not installed. Run `/orbit-install`.

### `Playwright tests failed — auth.setup.js`
Admin cookies expired. Re-run:
```bash
WP_TEST_URL=http://localhost:8881 npx playwright test \
  tests/playwright/auth.setup.js --project=setup
```

### `qa.config.json not found`
First-time setup needed. Run `/orbit-setup`.

### Step hangs > 10 min
Probably the AI skill audits in `--mode full` waiting on Claude Code. Check `reports/skill-audits/*.md` to see if any wrote partial output. Kill + re-run.

---

## What each step actually does

Detailed in `docs/04-gauntlet.md`. Quick reference:

```
Step 1   PHP Lint           → syntax errors in every .php file (~10s)
Step 1a  Release Metadata   → header, readme.txt, version parity, license, HPOS, WP compat (~20s)
Step 1b  Zip Hygiene        → dev files, forbidden functions, supply-chain audit (~30s)
Step 2   PHPCS              → WordPress + VIP coding standards (~30s)
Step 3   PHPStan            → static analysis (level 5) (~45s)
Step 4   Asset Weight       → JS/CSS bundle sizes (~5s)
Step 5   i18n / POT         → translatable strings + text domain check (~20s)
Step 5a  i18n runtime       → JSON_UNESCAPED_UNICODE in storage + REST charset (~10s)
Step 5b  i18n JS parity     → PHP wp_localize_script keys vs JS reads (~10s)
Step 5c  i18n translator    → per-locale .po staleness vs current POT (~15s)
Step 5d  Multilingual compat→ Polylang + WPML language-aware custom endpoints (~20s)
Step 5e  IP clean-room      → reference-identifier/string/asset leak scan + GPL-compat + provenance + trademark (~25s; runs only when a competitor reference was studied — owner: orbit-security, hard gate at release)
Step 6   Playwright Tests   → functional + visual regression + flow videos (~3 min)
Step 7   Lighthouse         → Core Web Vitals scores (~1 min)
Step 8   DB Profiling       → query count + slow query log + memory + cron + GDPR (~2 min)
Step 9   Competitor         → side-by-side comparison of competitor plugins (~3 min)
Step 10  UI Performance     → editor load time (Elementor/Gutenberg) + frontend TTFB (~2 min)
Step 11  Claude Skills      → 6 parallel AI audits (security, perf, DB, a11y, standards, quality)
Step 12  PM UX Audit        → spell-check + guided experience score + label benchmarking
```

---

## After failure — drill into a specific layer

| Layer that failed | Skill |
|---|---|
| PHPCS / WPCS | `/orbit-wp-standards` |
| Security / SAST | `/orbit-wp-security` |
| Performance | `/orbit-wp-performance` |
| Database | `/orbit-wp-database` |
| Accessibility | `/orbit-accessibility` |
| i18n (gettext) | `/orbit-i18n` |
| i18n runtime (Unicode encoding) | `/orbit-i18n-runtime` |
| i18n JS parity (silent English fallback) | `/orbit-i18n-js-parity` |
| i18n translator currency (.po drift) | `/orbit-i18n-translator-currency` |
| Polylang compat (incl. custom endpoints) | `/orbit-compat-polylang` |
| WPML compat (incl. wpml-config.xml currency) | `/orbit-compat-wpml` |
| IP / copyright clean-room (reference leak + provenance) | `/orbit-ip-cleanroom` |
| Playwright | `/orbit-playwright` |
| Lighthouse | `/orbit-lighthouse` |
| Editor perf | `/orbit-editor-perf` |
| PM UX (spell + label) | `/orbit-pm-ux-audit` |
| WP.org plugin-check | `/orbit-plugin-check` |

Each sub-skill goes deeper than the gauntlet step.

---

## Variations

```bash
# Override port
WP_TEST_URL=http://localhost:8888 bash scripts/gauntlet.sh --plugin . --mode full

# Skip a specific step (debug-only — never for release)
bash scripts/gauntlet.sh --plugin . --mode full --skip 9

# Run only steps 1-5 (fast PHP-only audit)
bash scripts/gauntlet.sh --plugin . --mode quick --only 1-5

# Output JSON instead of markdown
bash scripts/gauntlet.sh --plugin . --mode full --format json
```

---

## CI / GitHub Actions

`gauntlet.sh` is CI-ready out of the box — exit 0/1, deterministic output:

```yaml
- name: Orbit gauntlet
  run: bash scripts/gauntlet.sh --plugin . --mode full
- name: Upload reports
  if: always()
  uses: actions/upload-artifact@v4
  with: { name: orbit-reports, path: reports/ }
```

Full template: `docs/15-ci-cd.md`.
