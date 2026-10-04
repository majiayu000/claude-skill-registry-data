---
name: accessibility-check
category: qa
description: Use when a task changes any screen, form, dialog, menu or control - Lighthouse/axe scan of the changed screens, a keyboard walk, and the thresholds that fail a task
source: wshobson/agents (MIT), microsoft/playwright-cli (Apache-2.0), adapted
---
# Accessibility Check

## Thresholds

The same bar the frontend developer builds to (accessibility-basics, ui-quality-floor, responsive-mobile-first) — QA and developer share one bar, not a separate QA opinion:

- labels on every control, `aria-label` on icon-only buttons;
- visible focus on every interactive element;
- contrast ≥4.5:1 body text / ≥3:1 large text;
- touch targets ≥44px phone / ≥24px desktop;
- `<input>` font ≥16px on phone;
- exactly one `<h1>`, `lang` set on `<html>`, no `user-scalable=no`;
- a dialog traps focus while open, `Escape` closes it, focus returns to the trigger;
- submitting with errors moves focus to the first invalid field, which carries `aria-invalid`.

## Scan (public pages)

```bash
QA=${TMPDIR:-/tmp}/tt-<task-key>/qa; mkdir -p "$QA"; node -v   # lighthouse@13 needs Node >=22, else lighthouse@12
CHROME_PATH="$CHROME_BIN" npx -y lighthouse@13 "http://localhost:5173/settings" \
  --only-categories=accessibility,best-practices --form-factor=mobile \
  --screenEmulation.mobile --screenEmulation.width=360 --screenEmulation.height=800 --screenEmulation.deviceScaleFactor=2 \
  --chrome-flags="--headless=new" --output=json --output-path="$QA/lh-settings-360.json" --quiet
jq -r '.audits|to_entries[]|select(.value.score==0)|"\(.key)\t\(.value.title)"' "$QA/lh-settings-360.json"
```

Run with `run_terminal` `timeout_seconds: 300`. `errors-in-console` in the output doubles as the console check for page load.

## Full axe (pages behind login, or when Lighthouse flags something)

Install `playwright-core` + `@axe-core/playwright` into `$QA`, never the workspace:

```bash
cd "$QA" && [ -d node_modules/@axe-core/playwright ] || npm i --no-audit --no-fund --silent playwright-core@1.63 @axe-core/playwright@4.13
cat > axe.cjs <<'EOF'
const { chromium } = require('playwright-core');
const { AxeBuilder } = require('@axe-core/playwright');
(async () => {
  const [url, width = '360'] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: process.env.CHROME_BIN });
  const page = await browser.newPage({ viewport: { width: Number(width), height: 800 } });
  await page.goto(url);
  const { violations } = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
  for (const v of violations) console.log(`${v.impact}\t${v.id}\t${v.nodes.length}\t${v.nodes[0].target.join(' ')}`);
  console.log(`violations=${violations.length}`);
  await browser.close();
})();
EOF
node axe.cjs http://localhost:5173/settings 360
```

For a page behind login, add `page.fill`/`page.click` lines before the scan.

## Keyboard walk (playwright-cli)

```bash
cd "$QA"; PW="npx -y @playwright/cli@0.1"; $PW --help | head -5
$PW open --browser=chrome http://localhost:5173/settings
$PW press Tab; $PW --raw eval "(() => { const a = document.activeElement; return a.tagName + '|' + (a.getAttribute('aria-label') || a.textContent.trim().slice(0, 40)) + '|outline=' + getComputedStyle(a).outlineStyle })()"
```

Repeat Tab through every changed control; order must follow visual order, with no `outline=none` and no box-shadow silently replacing it. Open the dialog, `press Escape`, `eval` activeElement = the trigger.

## Verdict and recording

- A critical or serious violation whose target is inside a changed screen → fail the task (qa-criterion-verdicts rubric).
- A violation outside the changed screen → a pre-existing-defect note (in_qa), not a fail.
- Moderate/minor → a note, not a fail.
- Record as a test case with `category: visual` and a title prefix `a11y:` — the category enum has no accessibility value of its own.

## Red Flags

- Quoting the Lighthouse score instead of the failing audits by name.
- Scanning a page you did not change and failing the task for what it finds there.
- "Keyboard OK" written with no Tab walk actually run.
