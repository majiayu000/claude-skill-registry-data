---
name: orbit-pm-ux-audit
description: PM-grade UX audit for a WordPress plugin's admin UI — three checks that catch the kind of quality issues that land in 1-star reviews. (1) Spell-check every visible string. (2) Guided Experience score (0-10, vs Yoast/WPForms/Elementor). (3) Label & terminology audit (vague buttons, PHP jargon, ambiguous toggles, illogical option ordering). Use when the user says "PM UX", "spell check labels", "guided experience score", "label benchmark", or wants the polish layer most plugins skip.
---

# 🪐 orbit-pm-ux-audit — PM-grade UX layer

The 12th step of the gauntlet — the quality bar that separates a 4-star plugin from a 5-star one.

---

## Quick start

```bash
# Standalone
WP_TEST_URL=http://localhost:8881 \
PLUGIN_ADMIN_SLUG=my-plugin \
  bash ~/Claude/orbit/scripts/pm-ux-audit.sh

# Or just the gauntlet — runs PM UX as Step 12 in --mode full
bash scripts/gauntlet.sh --plugin . --mode full
```

Output: `reports/pm-ux/pm-ux-report-<timestamp>.html` — open in browser, share with PM.

---

## What it catches

### 1. Spell-Check Scan

Crawls every admin page, extracts every visible string (label, button, tooltip, placeholder, heading, notice), runs it against a 60-typo WP plugin dictionary + optional `cspell` for deeper coverage.

```
❌ "seting"        → "setting"            [label]   /wp-admin/admin.php?page=my-plugin
❌ "intergration"  → "integration"        [heading] /wp-admin/admin.php?page=my-plugin-advanced
❌ "recieve"       → "receive"            [notice]  /wp-admin/admin.php?page=my-plugin
❌ "succesful"     → "successful"         [toast]   /wp-admin/admin.php?page=my-plugin-form
```

Common WP typos covered: seting/setting, intergration/integration, recieve/receive, succesful/successful, occured/occurred, seperate/separate, definately/definitely, necessery/necessary, accomodate/accommodate, mantain/maintain, etc.

### 2. Guided Experience Score (0-10)

Scans for guidance signals across every admin page. Compares against 7 top WP plugins.

```
[Guided UX] Score: 4/10  ████░░░░░░  (Competitor avg: 8/10)

  ✓ Present (2):
     • Inline Help Text (+2pts)
     • Placeholder Text (+1pt)

  ✗ Missing (5) — users navigate alone:
     • Setup Wizard           (+3pts)  → RankMath, WooCommerce, WPForms all use a wizard
     • Welcome / Onboarding   (+2pts)  → MonsterInsights, Elementor show on first activate
     • Tooltips / Info Icons  (+2pts)  → Yoast, WC, WPForms — "?" icons next to every setting
     • Empty-state Guidance   (+2pts)  → Show users what to do when no data exists
     • WP Help Tab            (+1pt)   → Use the WP-native help drawer

  Competitors with better guidance:
     • RankMath:   9/10  (you are 5 points behind)
     • WPForms:    9/10  (5 points behind)
     • Elementor:  9/10  (5 points behind)
```

Signals scored:
- Setup wizard +3
- Welcome screen +2
- Tooltips +2
- Inline help text +2
- Placeholder text +1
- Empty-state guidance +2
- WP Help tab +1

### 3. Label & Terminology Audit

Benchmarks every label, button, nav item, and option against `config/pm-ux/competitor-terms.json` — industry-standard terminology from 10 top WP plugins.

```
[Label Audit] 7 issue(s) across 4 pages

  Anti-patterns (4 — 2 high severity):
  ❌ [button] "Submit" — vague. Use "Save Settings".
      → WooCommerce, WPForms, Yoast all use specific verbs.
  ❌ [button] "Toggle" — ambiguous. Use "Enable Cache" / "Disable Cache".
      → Jetpack, WC, Yoast always name their toggles.
  ⚠  [label]  "Enqueue scripts" — PHP jargon. Use "Load Scripts".
      → WC, WPForms translate dev-terms into user language.
  ⚠  [nav]    "Config" — industry standard is "Settings".
      → Yoast, WC, WordPress Core all use "Settings".

  Terminology vs competitors (2):
  ⚠  [button] "Apply" — industry standard "Save Settings"
      → Yoast SEO, WC, RankMath.
  ⚠  [nav]    "Utilities" — industry standard "Tools"
      → Yoast SEO, WC, RankMath.

  Option ordering (1 group out of logical order):
  ⚠  "Cache Duration" current: [Monthly, Daily, Never, Weekly]
     suggested: [Never, Daily, Weekly, Monthly]
     → WC, WPForms order options logically: None → Low → High → Custom.
```

Anti-patterns caught:
- Vague buttons: Submit, OK, Go
- Double negatives: "Don't disable" → "Enable"
- PHP jargon: enqueue, nonce, transient, hook
- Ambiguous toggles: "Toggle" without context
- ALL CAPS abuse
- Tech abbreviations: cfg, util, addr
- Non-specific "Enable" labels

---

## Configure competitor brain

`config/pm-ux/competitor-terms.json` — edit to add your own competitors. Format:

```json
{
  "competitors": ["Yoast SEO", "RankMath", "WooCommerce", "Elementor", "WPForms", ...],
  "labels": {
    "save_settings_button": {
      "preferred": "Save Settings",
      "acceptable": ["Save Changes", "Update Settings"],
      "anti_pattern": ["Submit", "Apply", "OK", "Go"],
      "competitors_using_preferred": ["Yoast", "RankMath", "WC"]
    },
    ...
  }
}
```

Add competitors → re-run → audit picks up your new benchmarks.

---

## HTML report

After every run, one HTML opens in browser — designed for PMs to read like a test report:

```bash
open reports/pm-ux/pm-ux-report-<timestamp>.html
```

Contains:
- Total typo count + per-page list
- Guidance score card with competitor comparison
- Full label findings table
- Severity badges (Critical / High / Medium / Low)
- Direct WP-Admin links for each finding

Share the URL with your PM — they don't need terminal access.

---

## Severity → release gate

| Issue | Severity |
|---|---|
| Typo in user-facing label | **High** |
| Typo in tooltip / placeholder | Medium |
| Typo in admin notice | **High** |
| Guidance score < 4 | **High** (missing onboarding) |
| Vague button label ("Submit", "OK") | High |
| PHP jargon in user-facing label | Medium |
| Out-of-order options | Low |

---

## Pair with `/orbit-uat-compare`

`/orbit-uat-compare` runs side-by-side comparison with screenshots + videos. This skill catches the **textual quality** that gets glossed over in visual comparisons. Run both before any beta release.

---

## Why this matters

90% of WordPress plugin teams skip this layer. They ship a typo, a confusing button, an unguided onboarding — and end up with 1-star reviews like:

> "Confusing setup. No idea what 'Toggle Enqueue' does."

These checks add 30 seconds to your release process and prevent the kind of preventable rep-damaging review that hangs around for years.
