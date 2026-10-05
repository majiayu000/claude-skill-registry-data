---
name: visual-review
description: Automated visual design review — screenshot V0 demo URLs or local HTML, analyze rendered output, and validate against brand system. Works with both V0 live previews and Stitch-generated HTML.
---

# Automated Visual Design Review

## Rule
Never review a design from code alone. Always render it, screenshot it, and analyze the actual visual output.

## Process

### For V0 Designs (primary)
V0 returns a live demo URL. Screenshot it directly:
```bash
NODE_PATH=/data/.npm-global/lib/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844, deviceScaleFactor: 2 } });
  await page.goto('DEMO_URL', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'OUTPUT_PATH', fullPage: true });
  await browser.close();
})();
"
```

### For Stitch/Local HTML
```bash
await page.goto('file:///path/to/design.html');
```

### Analyze the Screenshot
Use the image analysis tool to visually inspect against the 10-point review.

### Extract Tokens from V0 Code
For V0 output, grep the .tsx files for brand compliance:
- `bg-[#...]`, `text-[#...]` — check against brand palette
- `font-[...]` — check against approved fonts
- `rounded-[...]` — check against border radius scale
- `p-[...]`, `gap-[...]` — check against spacing scale

### Write Review
Combine visual analysis + code token check into standard 10-point review format.

## When to Use
- Every V0-generated design (screenshot the demo URL)
- Every Stitch-generated screen (render locally)
- Every deployed page (screenshot the live URL)
- Any design dispute — render both versions and compare
