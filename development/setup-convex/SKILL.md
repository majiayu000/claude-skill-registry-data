---
name: setup-convex
description: Sign the user in to Convex from macOS, Linux or Windows through the browser, so the agent can create Convex projects, deploy backends and set env vars. Use when the user wants to connect Convex, npx convex login status fails, or before create-software needs a database.
---

Connect the user's Convex account to the Convex CLI on this machine so the agent can create and deploy backends. Do every step yourself and only ask for what needs a human (creating the account, approving the login). Talk to the user in their language, short messages, no jargon (never say "CLI", "deployment key" or "device" to them).

If you got this skill from a link instead of a local folder, install nothing else from the repo: fetch a file only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/setup-convex/<path> -o <scratch>/<file>`, and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

1. Make sure Node works (`node --version`, v20 or higher); if not, run the `setup-node` skill first. Convex runs through `npx`, nothing else to install.
2. If `npx convex@latest login status` already shows a signed-in account and a team, skip to step 4.
3. Start the login in the background, with the output in a file you can read:

   ```bash
   npx -y convex@latest login --no-open --login-flow poll --device-name "$(hostname)" < /dev/null > <scratch>/convex-login.txt 2>&1
   ```

   Read the link (and the code if one is shown) from that file and give it to the user (open it in Chrome AI when `setup-dev-browser` is done). If they have no Convex account, they create one on that page with GitHub or Google, then approve the device and say "done". Check `npx convex@latest login status` until it shows their team.
4. Prove it: `npx convex@latest login status` lists their account and at least one team. Do not create a project now; `create-software` creates one per app with `npx convex dev --once`.

End with a short check list, a check or a cross on each line: Node works, signed in to Convex, team `<name>` found. Then tell the user in one line that the agent can now create the database and backend of their apps.
