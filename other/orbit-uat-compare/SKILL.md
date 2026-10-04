---
name: orbit-uat-compare
description: Side-by-side UAT comparison of two WordPress plugins on the same feature set. Generates an HTML report with paired PNG screenshots, MP4 flow videos, PM analysis per flow, RICE backlog, and a feature comparison table. Names files via the PAIR-NN-slug-a/b convention so the report auto-pairs by slug. Use when the user says "Plugin A vs Plugin B", "compare two plugins", "UAT report", "PAIR screenshots", "side-by-side", or "video comparison".
---

# 🪐 orbit-uat-compare — Plugin A vs Plugin B

PM-grade side-by-side comparison. Same flows, two plugins, one HTML report. Watch the videos, see the screenshots, read the PM verdict.

---

## Quick start

```bash
# Run flow tests + generate report + open in browser
npm run uat

# CI-friendly (no auto-open)
npm run uat:ci
```

---

## How the pairing works

Screenshots and videos use the **PAIR-NN-slug-a/b** convention:

```
pair-01-dashboard-a.png    ← Plugin A dashboard
pair-01-dashboard-b.png    ← Plugin B dashboard
pair-02-settings-a.png     ← Plugin A settings
pair-02-settings-b.png     ← Plugin B settings
```

The HTML report pairs by **slug** (`dashboard`, `settings`), not by index. Social always pairs with Social, regardless of order or count. Enforced by the `snapPair()` helper in `tests/playwright/helpers.js`.

---

## Write a flow spec

### Step 1 — Discovery (run first per plugin)
```bash
npx playwright test "Discovery | Plugin A"
# Prints all nav links → copy the exact URLs into your spec
```

### Step 2 — Use snapPair, never page.screenshot

```js
const { snapPair } = require('../helpers');
const SNAP = require('path').join(__dirname, '../../reports/screenshots/flows-compare');

test('PAIR-1 | dashboard | a | Plugin A dashboard', async ({ page }) => {
  await gotoAdmin(page, '/wp-admin/admin.php?page=plugin-a-dashboard');
  await snapPair(page, 1, 'dashboard', 'a', SNAP);                  // → pair-01-dashboard-a.png
  await snapPair(page, 1, 'dashboard', 'a', SNAP, 'scroll');        // → pair-01-dashboard-a-scroll.png
});

test('PAIR-1 | dashboard | b | Plugin B dashboard', async ({ page }) => {
  await gotoAdmin(page, '/wp-admin/admin.php?page=plugin-b-dashboard');
  await snapPair(page, 1, 'dashboard', 'b', SNAP);
});
```

### Step 3 — Test title format (required for video auto-renaming)

```
"PAIR-1 | dashboard | a | Plugin A dashboard overview"
```

The script `generate-uat-report.py` parses this title to wire videos to the right pair.

---

## Generate the HTML report

```bash
python3 ~/Claude/orbit/scripts/generate-uat-report.py \
  --title    "Plugin A vs Plugin B — v2.1" \
  --label-a  "Plugin A" \
  --label-b  "Plugin B" \
  --snaps    reports/screenshots/flows-compare \
  --videos   reports/videos \
  --out      reports/uat-report.html

open reports/uat-report.html
```

---

## Add PM analysis, RICE, feature table

Pass `--flow-data` JSON to enrich the report with per-flow PM verdicts, RICE-scored backlog, and a feature comparison table:

```bash
python3 ~/Claude/orbit/scripts/generate-uat-report.py \
  --flow-data reports/flow-data/my-plugin-vs-competitor.json \
  --out reports/uat-report.html
```

JSON shape:

```json
{
  "FLOW_DATA": {
    "1": {
      "slug": "dashboard",
      "title": "Dashboard",
      "verdict": "🔴 Needs Redesign",
      "a_summary": "Plugin A: cluttered, 12 tabs, no empty state.",
      "b_summary": "Plugin B: 2 tabs, clear empty state, CTA visible.",
      "pm_analysis": "<p>...</p>",
      "wins": ["Clear hierarchy", "Good empty state"],
      "gaps": ["Missing recent activity", "No quick actions"],
      "actions": ["Reduce tabs to 3", "Add Recent Activity card"]
    }
  },
  "RICE": [
    { "r": 1, "n": "Reduce dashboard tabs", "s": 54000, "reach": 18000,
      "imp": "MASSIVE", "eff": "XS", "t": "qw", "q": 1,
      "note": "Top friction in onboarding telemetry" }
  ],
  "FEATURES": [
    ["Setup wizard", "Plugin A: 5 steps", "Plugin B: 3 steps", "b"],
    ["Empty state", "Plugin A: blank", "Plugin B: CTA + tutorial", "b"]
  ],
  "IA_RECS": "<div>... optional HTML for IA / hierarchy section ...</div>"
}
```

`"t"` = task type (`qw` = quick win, `bb` = big bet). `"q"` = quarter (1-4).

---

## RICE columns explained

| Field | Meaning |
|---|---|
| r | Rank (1 = top priority) |
| n | Name of the task |
| s | RICE score (Reach × Impact × Confidence ÷ Effort × 1000) |
| reach | Users affected per quarter |
| imp | Qualitative impact: MASSIVE / HIGH / MED / LOW |
| eff | Effort: XS / S / M / L / XL |
| t | Type: qw / bb |
| q | Quarter to ship |
| note | Why it scored what it did |

PMs use this column to slot work into roadmap.

---

## Use case templates

### Free vs Pro
```bash
# Run side-by-side: my-plugin-free vs my-plugin-pro
LABEL_A="Free" LABEL_B="Pro"  npm run uat
```

### Vs competitor
```bash
LABEL_A="My Plugin" LABEL_B="Competitor"  npm run uat
```

### Old version vs new version
Pair this with `/orbit-version-compare` for a mixed report — code diff + UAT visual.

---

## Output

```
reports/
├── uat-report-<timestamp>.html         ← the master HTML
├── screenshots/flows-compare/
│   ├── pair-01-dashboard-a.png
│   ├── pair-01-dashboard-b.png
│   └── ...
└── videos/
    ├── PAIR-1-dashboard-a.mp4
    └── PAIR-1-dashboard-b.mp4
```

The HTML is self-contained — open in any browser, share via DM, attach to a release post.

---

## Pair with `/orbit-pm-ux-audit`

UAT compare = visual + flow comparison. PM UX audit = textual quality (spelling, labels, terminology). Run both for a complete PM-facing report.
