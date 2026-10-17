---
name: playwright-screenshot
description: Capture deterministic webpage screenshots with the local Playwright helper at tools/playwright-shot. Use when asked to screenshot localhost apps, staging/prod URLs, React pages, or when visual verification artifacts are needed for bugs/reviews/docs.
---

# Playwright Screenshot

## Quick start

Use the local helper project:

```bash
cd /home/openclaw/.openclaw/workspace/tools/playwright-shot
npm run shot -- <url> <output.png>
```

Example:

```bash
npm run shot -- http://localhost:5173 ../../assets/final/image/react-home.png
```

## Workflow

1. Confirm target URL and output path.
2. Run the `npm run shot -- <url> <output.png>` command.
3. Verify output file exists.
4. Return the saved path to the user (or attach the image when requested).

## Defaults and behavior

- Browser: headless Chromium
- Viewport: `1440x900`
- Capture mode: full-page screenshot
- Wait condition: `networkidle`
- Script path: `/home/openclaw/.openclaw/workspace/tools/playwright-shot/screenshot.js`

## Troubleshooting

- If command fails, run in the helper directory and inspect stderr first.
- If page never settles, retry once; if still failing, report likely app/network issue.
- If output path fails, choose a writable absolute path and re-run.
