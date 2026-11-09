---
name: setup-dev-browser
description: Set up a dedicated Chrome window for the AI (its own profile, signed in to the user's accounts) and the dev-browser CLI and skill, so the agent can browse, click, fill forms and check sites in it. Use when the user wants to set up dev-browser, a browser for the AI, or Chrome AI.
argument-hint: "[port, default 9333]"
disable-model-invocation: true
user-invocable: true
---

Give the agent its own Chrome: a separate window with its own profile, where the user signs in once to their tools, and that the agent drives through the `dev-browser` CLI. The user's normal Chrome stays untouched, and the agent never needs a password because the sessions stay saved in that profile. Do every step yourself and only ask for what needs a human (installing Chrome, signing in). Talk to the user in their language, short messages, no jargon (never say "CDP", "profile directory" or "PATH" to them).

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/setup-dev-browser/<path> -o <scratch>/<file>` (for example `scripts/chrome-ai`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

The setup lives in four places: the launcher `~/.local/bin/chrome-ai` (copied from [scripts/chrome-ai](scripts/chrome-ai)), the profile `~/.chrome-ai-profile`, the debugging port `9333` open on `127.0.0.1` only, and the `dev-browser` skill that tells every agent to connect there. If the argument gives another port, set `CHROME_AI_PORT` to it in the user's shell config and use it everywhere below.

1. Check the machine. This works on macOS and Linux; on Windows, stop and say it needs WSL or a Mac.

   ```bash
   node --version && npm --version
   ls "/Applications/Google Chrome.app" 2>/dev/null || command -v google-chrome
   ```

   If Node is missing, run the `setup-node` skill first. If Chrome is missing, send the user to https://www.google.com/chrome and wait for "done".
2. Install the CLI and its browser, then check it answers.

   ```bash
   npm install -g dev-browser && dev-browser install
   dev-browser --help | head -5
   ```

3. Install the launcher: copy `scripts/chrome-ai` from this skill to `~/.local/bin/chrome-ai` and make it executable. If `~/.local/bin` is not on the user's PATH, add `export PATH="$HOME/.local/bin:$PATH"` once (never twice) to both `~/.zprofile` and `~/.zshrc` (or `~/.bash_profile` and `~/.bashrc`), so new terminals and agent sessions both find it.
4. On macOS, run `chrome-ai app` to create the "Chrome AI" app in `~/Applications`, so the user can open it from Spotlight.
5. Run `chrome-ai start`. It opens a new Chrome window and prints `http://127.0.0.1:9333`. Tell the user this window is the AI's Chrome and ask them to pick a different theme color in it (Settings, Appearance) so they never confuse it with their own.
6. Ask the user to sign in, in that window only, to the tools the agent will use (Google, GitHub, Cloudflare, Lumail, Stripe, their own apps), then say "done". Never type a password, a code or a card number yourself, and never copy cookies from their normal Chrome.
7. Make sure the `dev-browser` skill is installed for their agent; if it is missing, run `npx skills add Melvynx/ai-maxxing-skills -g -a claude-code -s dev-browser -y`. If the user has a brain folder with an `AGENTS.md`, add one line there: browser work goes through the `dev-browser` skill in Chrome AI, never the user's own Chrome.
8. Let the agent run it without asking every time: merge `"Bash(dev-browser *)"` and `"Bash(chrome-ai *)"` into `permissions.allow` of `~/.claude/settings.json`, keeping every existing entry. Read the file first and write valid JSON back.
9. Prove it works in the Chrome AI window with a named page:

   ```bash
   chrome-ai start >/dev/null && dev-browser --connect http://127.0.0.1:9333 <<'JS'
   const page = await browser.getPage("setup-check");
   await page.goto("https://github.com");
   const path = await saveScreenshot(await page.screenshot(), "setup-check.png");
   console.log(JSON.stringify({ title: await page.title(), url: page.url(), path }));
   JS
   ```

   Open the screenshot and check the user shows as signed in on a site they signed in to in step 6. Then run `chrome-ai stop`, `chrome-ai start` and the check again: the login must survive a restart. Close the test page with `browser.closePage("setup-check")`.

End with a short check list, a check or a cross on each line: Chrome found, `dev-browser` installed, `chrome-ai` launcher works, Chrome AI app (macOS), user signed in, `dev-browser` skill installed, permissions added, screenshot shows a signed-in page, login survives a restart. Then tell the user in 3 lines: open "Chrome AI" (or just ask the agent, it starts it on its own), sign in there once to any new tool, and one thing to try right now, such as "open my Stripe dashboard and tell me yesterday's sales".
