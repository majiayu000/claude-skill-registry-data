---
name: orbit-reports
description: Generate the master HTML report index that ties together every Orbit output — gauntlet markdown, Playwright HTML, skill audit tabs, Lighthouse score card, UAT comparison, PM UX, version diff. One file, share-friendly. Use when the user says "generate report", "make HTML report", "share with PM", "release evidence pack", "master index".
---

# 🪐 orbit-reports — Master HTML report index

Every gauntlet run drops a dozen files. This skill ties them into one HTML page that PMs / managers / customers can read without terminal access.

---

## Quick start

```bash
python3 ~/Claude/orbit/scripts/generate-reports-index.py
open reports/index.html
```

With a custom title (recommended for releases):
```bash
python3 ~/Claude/orbit/scripts/generate-reports-index.py \
  --title "Release v2.4.0 — $(date +%Y-%m-%d)"
```

Or via the gauntlet (auto-runs at the end of `--mode full` / `--mode release`):
```bash
bash scripts/gauntlet.sh --plugin . --mode full
```

---

## What goes in the master index

```
reports/index.html
│
├── HERO — release name, date, severity bar (Critical / High / Medium / Low counts)
│
├── TABS:
│   ├── Overview      — gauntlet markdown rendered (qa-report-*.md)
│   ├── E2E Tests     — playwright-html iframe
│   ├── Skill Audits  — 6 tabs (Security / Perf / DB / A11y / Standards / Code Quality)
│   ├── Lighthouse    — score card + per-URL breakdown
│   ├── UAT Compare   — paired screenshots + videos
│   ├── PM UX         — typos + guidance score + label findings
│   ├── Version Diff  — v(N-1) vs v(N) (if /orbit-version-compare ran)
│   ├── Competitors   — table from /orbit-competitor-compare
│   └── Bundle        — JS/CSS weight + treemap
│
└── FOOTER — links to download every report file
```

---

## Severity bar — top of the page

```
🔴 Critical: 0     🟠 High: 1     🟡 Medium: 4     ⚪ Low: 12
```

Click any badge → jumps to the section with those findings.

---

## Per-tab content

Each tab is self-contained — works offline once generated.

### Overview tab
Renders `reports/qa-report-<timestamp>.md` as HTML. Passes/fails per gauntlet step, time taken, exit code.

### E2E Tests tab
Embeds Playwright's HTML reporter via `<iframe>`. Click any test → see screenshots + traces.

### Skill Audits tab
6 sub-tabs (one per core audit):
- 🔒 Security — `/orbit-wp-security` output
- ⚡ Performance — `/orbit-wp-performance`
- 🗄 Database — `/orbit-wp-database`
- ♿ Accessibility — `/orbit-accessibility`
- 📐 WP Standards — `/orbit-wp-standards`
- 🧹 Code Quality — `/orbit-code-quality`

Each sub-tab is the markdown report rendered inline.

### Lighthouse tab
- Big score card (Performance / Accessibility / Best Practices / SEO — 0-100)
- Per-URL breakdown if multiple URLs scored
- Core Web Vitals breakdown (LCP / FCP / TBT / CLS)

### UAT Compare tab
Embed of `reports/uat-report.html` (from `/orbit-uat-compare`). Paired screenshots + videos + PM analysis.

### PM UX tab
Embed of `reports/pm-ux/pm-ux-report-*.html` (from `/orbit-pm-ux-audit`). Typo list + guided UX score + label findings.

### Version Diff tab
Output of `/orbit-version-compare` rendered as markdown.

### Competitors tab
Output of `/orbit-competitor-compare`.

### Bundle tab
JS/CSS weight + an embedded `source-map-explorer` treemap.

---

## Custom flags

```bash
python3 scripts/generate-reports-index.py \
  --title "My Custom Title" \
  --reports-dir reports/ \                # default: ./reports/
  --output reports/release-evidence.html \  # default: reports/index.html
  --include security,performance \         # only specific skill-audit tabs
  --logo plugin-logo.png \                 # add custom logo to hero
  --share-token <hash>                     # gate the HTML behind a token
```

---

## Sharing the report

The HTML is fully self-contained — open from anywhere:

```bash
# Local
open reports/index.html

# Email / Slack
# Just attach reports/index.html — opens in any browser

# Web / customer-facing
# Upload to your CDN / S3 — single static file, no deps
aws s3 cp reports/index.html s3://my-bucket/release-v2.4.0.html
```

For internal-only, gate behind a token:
```bash
python3 scripts/generate-reports-index.py --share-token $(uuidgen)
# → reports/index.html?token=abc123 — fails open without the token
```

---

## What it auto-detects

When you run the script with no flags, it reads `reports/`:

| File found | Renders into tab |
|---|---|
| `qa-report-*.md` | Overview |
| `playwright-html/index.html` | E2E Tests |
| `skill-audits/*.md` | Skill Audits |
| `lighthouse/lh-*.json` | Lighthouse |
| `uat-report-*.html` | UAT Compare |
| `pm-ux/pm-ux-report-*.html` | PM UX |
| `version-compare-*.md` | Version Diff |
| `competitor-*.md` | Competitors |
| `bundle-treemap.html` | Bundle |

Missing files = tab not rendered (no broken links).

---

## When to use this skill

- **Every release** — the evidence pack PM and dev sign-off on
- **Customer asks "is it stable?"** — share the URL
- **Audit / compliance** — single artefact proving what was tested
- **Post-mortem** — the data was already captured, just visualise it

---

## Pair with `/orbit-release-gate`

`/orbit-release-gate` runs the gauntlet AND auto-generates this report as Gate 4. Use this skill standalone when you want to regenerate the HTML without re-running the gauntlet.

---

## Output

`reports/index.html` (default) — single file, ~200KB-2MB depending on screenshot count.

Pure HTML + inline CSS, no external deps (except embedded videos / iframes which need their files alongside). Save the `reports/` folder as a unit if archiving.
