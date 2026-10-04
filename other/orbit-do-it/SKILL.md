---
name: orbit-do-it
description: The brainless orchestrator. User points at a plugin path; this skill auto-detects plugin type (Elementor / Gutenberg / WooCommerce / form / membership / generic), picks the right combination of audit + UAT + perf + security + compat skills, runs them in parallel, and produces a one-page TL;DR + master HTML report. Zero questions after the path. Use whenever the user says "do it", "audit my plugin", "ship it", "check everything", or just `/orbit-do-it`.
argument-hint: <plugin-path>  (e.g. ~/plugins/my-plugin)
disable-model-invocation: false
---

# 🪐 orbit-do-it — The Brainless Team Agent

> One command. Zero prompts. Walks away. Comes back to a verdict.
> Designed for non-technical team members + dev leads who want the audit done, not configured.

---

## How it works (the path the user takes)

```
$ /orbit-do-it ~/plugins/my-new-plugin

🪐 Hi. Auditing my-new-plugin in the background.

   Detected: Elementor addon (PHP 8.1+, 14 widgets, 0 Gutenberg blocks)
   Selected pipeline:
     - 6 core audits (security, performance, DB, standards, a11y, code quality)
     - Elementor-specific (dev, controls, compat, skins, V4 atomic)
     - UAT — natural-language flows via /orbit-uat-agent
     - Live security feeds (NVD + Patchstack + WPScan, fetched just now)
     - Lighthouse + editor perf
   ETA: 12 min. I'll open the report when done.

[12 minutes pass]

✅ Done. Verdict: BLOCK release — 2 Critical findings need fix.

   Top 3 things to fix:
   1. Settings page — XSS in `?search=` parameter (active probe found it)
   2. widget-X — render() echoes attribute without esc_html
   3. Editor perf — widget-Y inserts in 1.4s (target < 300ms)

   Full report: open ~/plugins/my-new-plugin/reports/index.html
```

---

## Phase 1 — Auto-detect

Reads the plugin folder. Determines:

| Signal | Inferred type |
|---|---|
| `register_widget()` extends `\Elementor\Widget_Base` | Elementor addon |
| Files matching `block.json` exist | Gutenberg block plugin |
| `add_action('woocommerce_*'...)` present | WooCommerce extension |
| `wp_register_form_*` or known form-plugin signatures | Form plugin |
| `add_role()` / `add_capabilities()` heavy | Membership / LMS |
| `register_rest_route()` with custom namespace | REST-heavy plugin |
| Theme-style file (`style.css` with `Theme Name:`) | Theme / FSE |
| None of the above | Generic / utility |

A plugin can be multi-type (e.g. Elementor + Woo) — pipeline merges.

---

## Phase 2 — Pipeline assembly

Based on detected type(s), assemble the skill list:

### Always run (core 6 audits)
- `/orbit-wp-standards`
- `/orbit-wp-security`
- `/orbit-wp-performance`
- `/orbit-wp-database`
- `/orbit-accessibility`
- `/orbit-code-quality`

### Type-specific add-ons
- Elementor → `/orbit-elementor-dev`, `/orbit-elementor-controls`, `/orbit-elementor-compat`, `/orbit-elementor-skins`, `/orbit-elementor-dynamic-tags`, `/orbit-uat-elementor`
- Gutenberg → `/orbit-gutenberg-dev`, `/orbit-block-render-test`, `/orbit-block-edit-test`, `/orbit-block-bindings`, `/orbit-interactivity-api`, `/orbit-uat-gutenberg`
- WooCommerce → `/orbit-uat-woo` (HPOS-aware) + WC-specific filters in `/orbit-wp-database`
- Form → `/orbit-uat-forms` + `/orbit-rest-fuzzer` + `/orbit-ajax-fuzzer`
- Membership/LMS → `/orbit-uat-membership` + `/orbit-pay-stripe` (if billing present)
- Theme → `/orbit-fse-test`

### Always-on cross-cutting
- `/orbit-uat-agent` — natural-language UAT flows (Stagehand-style)
- `/orbit-cve-check` — live feed, fetched just now
- `/orbit-vdp` — VDP coverage (EU mandate)
- `/orbit-bundle-analysis` — JS/CSS weight
- `/orbit-lighthouse` — Core Web Vitals
- `/orbit-pm-ux-audit` — spell + label + guidance score
- `/orbit-zip-hygiene` (if release zip exists)

### Conditional (skip if not relevant)
- `/orbit-multisite` — only if plugin claims multisite compat
- `/orbit-host-*` — only if a host is detected on user's `WP_TEST_URL`
- `/orbit-pay-paypal` / `/orbit-pay-edd` / `/orbit-pay-freemius` — only if signatures detected
- `/orbit-compat-yoast` / `-rankmath` / `-wpml` / `-polylang` / `-acf` — only if signatures detected (or user opts in)

---

## Phase 3 — Parallel run with throttle

Run the assembled skills in parallel — default 3 concurrent (auto-detect CPU cores → 1 / 3 / 5 / 6+ on M-series Macs / workstations). Use Orbit's `batch-test.sh` runner.

Heavy skills (live-fetch security feeds, Lighthouse, Playwright) run first; lighter audits fill in. Each skill writes to `reports/skill-audits/<skill>.md`.

---

## Phase 4 — TL;DR generation

After all skills complete, synthesize:

1. **Verdict** — SHIP / WARN / BLOCK
   - SHIP: 0 Critical, 0 High, < 5 Medium
   - WARN: 0 Critical, 0 High, ≥ 5 Medium OR any unaddressed Medium in security
   - BLOCK: any Critical OR any High
2. **Top 3 things to fix** — ranked by severity then RICE (impact-first)
3. **Confidence score** — based on whether live-source fetches succeeded (degraded if any fell back to embedded rules)
4. **One-page summary** — printed inline + saved to `reports/tldr-<timestamp>.md`

---

## Phase 5 — Master HTML report

```bash
python3 ~/Claude/orbit/scripts/generate-reports-index.py \
  --title "<plugin-slug> — <today>"
open ~/<plugin>/reports/index.html
```

PMs / managers open this. Severity badges + tabbed audits + paired UAT screenshots + Lighthouse score card + live CVE check timestamp at the top.

---

## When to use vs the other commands

| User says | Use |
|---|---|
| "Audit my plugin" / "do everything" / "is it shippable?" | `/orbit-do-it` |
| "Fast feedback during dev" | `/orbit-gauntlet --mode quick` |
| "I'm tagging a release" | `/orbit-release-gate` |
| "I want to drill into security" | `/orbit-wp-security` directly |

`/orbit-do-it` is the **default for most users most of the time**. The specialised skills are for when you know which layer you want to inspect.

---

## Variations

```bash
# Parallel skip
/orbit-do-it ~/plugins/my-plugin --skip orbit-conflict-matrix,orbit-multisite

# Force a specific mode
/orbit-do-it ~/plugins/my-plugin --mode release        # full release-gate sequence
/orbit-do-it ~/plugins/my-plugin --mode quick          # 5-min subset

# Just the verdict (no HTML report)
/orbit-do-it ~/plugins/my-plugin --tldr-only

# Slack / Discord ping when done
/orbit-do-it ~/plugins/my-plugin --notify https://hooks.slack.com/...
```

---

## Smoke test

Input: `~/test-plugins/hello-dolly/` (a vanilla WP plugin)
Expected:
- Verdict: SHIP (no findings)
- Pipeline: core 6 audits + cross-cutting (no Elementor / Woo / form add-ons)
- Total time: < 3 min
- Report opens cleanly

If a fresh Hello Dolly produces any Critical/High → something in Orbit is misconfigured, not the plugin.

---

## Hard rules

- ❌ Never modify the plugin source — read-only audit
- ❌ Never run on a live production site
- ❌ Never skip the live-source fetch (the verdict's confidence depends on it)
- ✅ Always print the TL;DR inline (don't make user open a file to find the verdict)
- ✅ Always cite the live-source fetch timestamp (so the user knows the audit is current)

---

## Sources & Evergreen References

This skill is an orchestrator — it doesn't have its own canonical source. It composes other Orbit skills (each of which IS runtime-evergreen). The "freshness" of a `/orbit-do-it` run is the sum of its component skills' freshness.

If `/orbit-uat-agent` fetched Stagehand docs at 2026-04-30 14:32 UTC and `/orbit-cve-check` fetched NVD at 14:33 UTC, the master report cites both timestamps.

### Last reviewed
2026-04-30 — re-review whenever a new plugin-type detection signal is needed
