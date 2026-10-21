---
name: visual-regression-upgrade
description: Pixel-diff two environments (prod vs UAT, or local legacy vs upgrade) with Playwright screenshots and an HTML report. Use for "does it look the same", "did the layout change", "compare prod and UAT", "screenshot diff", or checking a CMS upgrade (SS 4→5, Drupal, WordPress) broke the front-end.
---

# Visual Regression for CMS Upgrades

Compares two environments screenshot-by-screenshot and emits a single self-contained HTML report classifying every page as PASS / WARN / FAIL. Two modes:

- **Cross-server** (production vs upgraded UAT) — the classic "does the deployed upgrade match live" check.
- **Same-machine** (local legacy vs local upgrade) — the preferred mid-migration mode when the upgrade isn't deployed yet. Identical fonts/CDN/APIs on both sides mean every diff is a real layout difference, not environmental noise. See "Preferred during migration" below.

Use this whenever you need to prove — or disprove — that an upgrade looks identical to the baseline.

## When to use

Trigger phrases:
- "does the upgrade look the same as prod"
- "compare prod and UAT visually"
- "compare the legacy and upgraded site locally"
- "visual regression check"
- "screenshot diff between two sites"
- "the layout looks different after the upgrade"
- "verify the SilverStripe 4 → 5 upgrade visually"
- "does it look identical"

## Prerequisites

```bash
pip install playwright pillow numpy requests
python -m playwright install chromium
```

Outputs live in a working directory you choose (e.g. `./vr-out/`).

## Workflow

### Step 1 — Discover URLs

```bash
python scripts/crawl_urls.py --url https://www.example.com --limit 30 --out paths.txt
```

Tries `/sitemap.xml` first; falls back to depth-2 link crawl from the homepage. Output is one path per line (e.g. `/`, `/about`, `/services/widgets`).

Review `paths.txt` and trim anything irrelevant (search pages, paginated archives) before continuing.

### Step 2 — Capture screenshots

```bash
python scripts/capture.py \
  --prod        https://www.example.com \
  --local       https://uat.example.com \
  --paths-file  paths.txt \
  --out         ./vr-out
```

Optional flags:
- `--viewport 1440x900` (default)
- `--wait-until load` (default) — Playwright navigation condition. Use `networkidle` for fully-static sites; `load` is safer on sites with analytics/chat widgets/long-polling
- `--wait 2.0` — extra seconds to wait after navigation completes
- `--settle {load,networkidle}` (default `load`) — pre-screenshot settle strategy. **Both modes await `document.fonts.ready`** with a 10s cap so screenshots never snap mid-FOIT/FOUT. `networkidle` additionally waits for the network to go idle — recommended for sites embedding Termly, HubSpot, Hotjar, or any 3rd party that injects iframes asynchronously. Font faces that report `status === 'error'` (real CDN allowlist failures) are recorded in `manifest.json` under each entry's `font_errors`
- `--block-urls pattern1,pattern2` — comma-separated URL substrings to block on **both** sides via Playwright route interception. Use for consent-management scripts that run on production but not locally and block first-party content before cookie consent is granted (e.g. `--block-urls termly.io/resource-blocker`). Blocking is applied symmetrically so neither side runs the gating script
- `--auth` / `--prod-auth` / `--local-auth` — HTTP basic auth, applied to both environments or scoped to one. Prefer `env:VR_AUTH` / `env:VR_USER/VR_PASS` / `prompt`. Use `--local-auth` when only UAT is protected to avoid sending UAT credentials to production.
- `--cookies` / `--prod-cookies` / `--local-cookies` — Playwright-format cookie list, applied to both or scoped to one environment
- `--mask masks.json` — `{ "/path/or/*": ["selector1", ".cookie-banner"] }` — paints these regions `#cccccc` before snapping. Use this for rotating banners, date stamps, "users online now" counters.

Writes `vr-out/prod/<slug>.png`, `vr-out/local/<slug>.png`, and `vr-out/manifest.json`.

### Preferred during migration: same-machine legacy comparison

When the upgraded site isn't on a public server yet, don't wait for a deploy — compare the local source-version instance against the local target-version instance. Same machine, same browser, identical fonts, no CDN/DNS variance — the environmental noise floor disappears and **every diff is a real layout difference**. The one exception: widgets whose API key is domain-locked to the prod domain (e.g. Google static maps) will render a placeholder on both locals and must be masked rather than treated as a regression.

Point `--prod` at the legacy local baseline and `--local` at the upgraded local (the flag names are just "left/right" — `--prod` is whatever you treat as the reference). `--insecure` handles `.ddev.site` self-signed certs.

```bash
python scripts/capture.py \
  --prod       https://{project}-legacy.ddev.site \
  --local      https://{project}.ddev.site \
  --paths-file paths.txt --wait 2.0 --insecure --out ./vr-legacy
```

**Acceptance bar (same-machine):** every page PASS or WARN < 2%. Any FAIL, and any WARN > 2%, is a genuine regression worth investigating — not noise. The report does not enforce the 2% bar: it classifies with the fixed bands in Step 4, so read each page's `diff_pct` in `results.json` or the report table.

Mask domain-restricted widgets that can't render locally — e.g. a Google static map whose API key is locked to the prod domain renders a "domain not authorized" placeholder on *both* locals, so it must be masked, not chased:

```json
{ "/contact-us/": [".addressMap"] }
```

#### When `.ddev.site` is unreachable: use `127.0.0.1:<port>`

`--insecure` handles self-signed `.ddev.site` certs, but it does **not** help when the agent/sandbox
shell can't resolve or reach the `.ddev.site` hostname at all (`curl` returns HTTP 000 / SSL exit 35).
Driven from such a shell, every page errors with `ERR_CONNECTION_RESET`, and the **whole run finishes
in ~3 seconds with all-ERROR results** — easy to mistake for a broken capture.

Use the direct host port mappings from `ddev describe` instead of the hostname:

```bash
ddev describe   # Project URLs → http://127.0.0.1:NNNNN
python scripts/capture.py \
  --prod  http://127.0.0.1:<legacy-port> \
  --local http://127.0.0.1:<upgrade-port> \
  --paths-file paths.txt --mask masks.json --out ./vr-out
```

- **Ports are dynamic** — they change after `ddev restart` / `ddev mutagen reset` / `ddev poweroff`.
  Re-read `ddev describe` each session.
- Prefer the **plain-HTTP** mapped port (returns 200, no `--insecure` needed). HTTPS on
  `127.0.0.1:<https-port>` still fails cert validation.
- A realistic **2–3s per-page** capture time is the signal it actually loaded. A 3-second *whole-run*
  with all ERRORs means it never reached the host — switch to the loopback ports.

### Step 3 — Diff + report

```bash
python scripts/diff_report.py --in ./vr-out --out ./vr-out/report
```

Produces:
- `vr-out/report/results.json` — machine-readable
- `vr-out/report/index.html` — **single self-contained file** (diff images base64-embedded) — open in browser or attach to a ticket

### Step 4 — Interpret

| Diff % | Status | Meaning |
|--------|--------|---------|
| < 0.5% | **PASS** (green) | Anti-aliasing / sub-pixel font rendering — ignore |
| 0.5 – 5% | **WARN** (amber) | Likely a real but minor change — inspect (margin shift, image swap, color tweak) |
| > 5% | **FAIL** (red) | Significant regression — investigate before signing off |

These bands are fixed in `scripts/diff_report.py` (`PASS_THRESHOLD`, `WARN_THRESHOLD`) and there is no flag to change them. They are calibrated for **cross-server** captures, where sub-pixel font/CDN variance puts a noise floor under every page. For **same-machine** captures (local legacy vs local upgrade) that floor is gone — treat anything **> 2% as actionable** (read it from `diff_pct`; the report still labels 0.5-5% WARN) and expect clean pages to sit well under 0.5%.

Tune masks and re-run if WARN/FAIL pages are all caused by the same dynamic widget.

## Example end-to-end

```bash
# 1. Discover
python scripts/crawl_urls.py --url https://www.example.com --limit 25 --out paths.txt

# 2. Capture (UAT behind basic auth — scoped to local only so prod doesn't receive UAT credentials)
export VR_AUTH="uatuser:uatpass"
python scripts/capture.py \
  --prod        https://www.example.com \
  --local       https://uat.example.com \
  --paths-file  paths.txt \
  --local-auth  env:VR_AUTH \
  --mask        masks.json \
  --settle      networkidle \
  --out         ./vr-out

# 3. Report
python scripts/diff_report.py --in ./vr-out --out ./vr-out/report
open ./vr-out/report/index.html
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| All screenshots blank/white | JS-heavy SPA not finished rendering | Bump `--wait` to 3-5s; check console errors in `manifest.json` |
| Every page reports ~100% diff | Viewport mismatch, or one env is mobile-redirecting | Force `--viewport 1440x900` on both; check redirects with curl |
| Font rendering diffs on one side (or one page only) | Screenshot fired before web fonts finished loading — a timing race, not a CDN problem | Use `--settle networkidle` (also bump `--wait 3.0`); both modes await `document.fonts.ready`. If `manifest.json` shows `font_errors` for that entry, the CDN really is rejecting the request — allowlist the capture origin in Adobe Fonts / fonts.com / Google Fonts, or mask the font-driven region as a last resort |
| First-party content blocked on prod ("We couldn't verify the security of your connection" or blank hero) | A consent-management script (`autoBlock=on`) is running on prod and blocking resources before cookie consent. Not present on local. | Add the resource-blocker URL to `--block-urls` (e.g. `--block-urls termly.io/resource-blocker`). This prevents the gating script from running on both sides so the real content loads for comparison |
| One side much taller | Lazy-loaded images on one env only | Capture script auto-scrolls; if still failing, increase `--wait` |
| Auth fails on UAT | Site uses form login, not basic auth | Capture cookies via browser devtools, save as `cookies.json` |
| Diff image looks like static | Both screenshots loaded but viewports differ | Confirm `--viewport` matches; some themes are width-responsive |
| `playwright._impl._errors.Error: net::ERR_CERT_AUTHORITY_INVALID` | Self-signed UAT cert | Use `--insecure` flag (sets `ignore_https_errors=True`) |
| Whole run finishes in ~3s, every page `ERR_CONNECTION_RESET` (curl → HTTP 000 / SSL exit 35) | Agent/sandbox shell can't reach the `.ddev.site` hostname | Capture against the `127.0.0.1:<port>` mappings from `ddev describe` — see [When `.ddev.site` is unreachable](#when-ddevsite-is-unreachable-use-127001port) |
| Diff localized to a map/embed, identical placeholder both sides | API key is domain-restricted (renders only on the prod domain) | Mask the widget selector; verify on the real prod/pre-prod domain |

## SilverStripe-specific notes

See `references/silverstripe.md` for the full rundown. Quick checklist:

- Append `?flush=1` to the **first** path on each side (or pass it as the first entry in `--paths`) to bust template/manifest caches
- Cross-server mode: compare **Live → Live**, never Live → Stage (same-machine mode compares each local instance's published front-end)
- Admin paths (`/admin`, `/Security/login`) need auth — usually capture with cookies, not basic auth
- If UAT can't reach `fonts.googleapis.com`, mask `<link rel="stylesheet">` font-driven regions
- Missing images on UAT → check `assets/.protected/` symlink and `_resources/` publishing
- `silverstripe-cache/` left over from SS4 can poison SS5 — `rm -rf` and `?flush=1` before capturing

## Output artifact

The `index.html` report is fully self-contained and portable: hand it to a PM, attach it to a Jira ticket, or commit it alongside the upgrade PR. No external assets, no CDN dependencies.
