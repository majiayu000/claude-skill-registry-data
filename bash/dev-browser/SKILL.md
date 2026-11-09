---
name: dev-browser
description: Drive the user's dedicated Chrome AI window with the dev-browser CLI to open sites, click, fill forms, read pages, take screenshots and check a live app while signed in. Use when the user says browse, open a site, click, fill a form, screenshot, scrape, test my site, or check something on the web.
allowed-tools:
  - Bash(dev-browser *)
  - Bash(chrome-ai *)
---

Do every browser task in Chrome AI, the user's dedicated Chrome window (profile `~/.chrome-ai-profile`, port 9333) where they are already signed in to their tools. Start it first (it does nothing if it is already open), then connect to it on every run:

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/dev-browser/<path> -o <scratch>/<file>` (for example `references/api-reference.md`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

```bash
chrome-ai start
dev-browser --connect http://127.0.0.1:9333 <<'JS'
const page = await browser.getPage("stripe-sales");
await page.goto("https://dashboard.stripe.com");
console.log(JSON.stringify({ title: await page.title(), url: page.url() }));
JS
```

If `chrome-ai` or `dev-browser` is missing, stop and tell the user to run `/setup-dev-browser`; never fall back to a standalone Playwright script or the user's own Chrome. If `CHROME_AI_PORT` is set, connect to that port instead of 9333 (`chrome-ai url` prints the address).

- Give each task its own page name (`browser.getPage("lumail-campaign")`) so parallel agents never share a tab, reuse that name across runs to keep the page state, and close it with `browser.closePage(name)` when the task is done. Never close or navigate a tab you did not open.
- Write small scripts that do one thing and end by logging the state as JSON (url, title, what you found). Scripts run in a sandbox, not Node: no `require`, `fs`, `fetch` or `process`.
- Before clicking, read the page with `await page.snapshotForAI()` and target elements with `page.getByRole`, `getByText` or `getByLabel`. Open [references/api-reference.md](references/api-reference.md) before using a method you are not sure exists.
- Files only go to `~/.dev-browser/tmp/`: pass a bare file name to `saveScreenshot` or `writeFile` and use the path it returns. Look at the screenshot before saying a page looks right.
- If a site asks to sign in, stop and ask the user to sign in in the Chrome AI window, then continue; the session stays saved. Never type passwords, codes or card numbers, and never solve a captcha.
- Ask the user before any click that sends, publishes, pays, deletes or accepts terms.
- For a clean signed-out check (how a visitor sees the site), run without `--connect` and with `--headless`, and say so.
- When a script fails, the page stays where it was: reconnect, take a screenshot, log the url and title, then continue from there.

Reply with what you saw or did, the final URL, and the screenshot path when it helps.
