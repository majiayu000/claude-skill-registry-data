---
name: setup-lumail
description: Connect the user's Lumail account on macOS, Linux or Windows through the browser, installing the Lumail CLI login, MCP and skills for their agent, so it can manage subscribers, tags, emails and workflows. Use when the user wants to connect Lumail or lumail auth test fails.
---

Connect the user's Lumail account so the agent can add subscribers, send login codes and build email workflows. Do every step yourself and only ask for what needs a human (creating the account, approving the login). Talk to the user in their language, short messages, no jargon (never say "CLI", "MCP" or "OAuth" to them). Never ask them to paste an API key in the chat.

If you got this skill from a link instead of a local folder, install nothing else from the repo: fetch a file only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/setup-lumail/<path> -o <scratch>/<file>`, and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

1. Make sure Node works (`node --version`, v20 or higher); if not, run the `setup-node` skill first. Lumail runs through `npx`, nothing else to install.
2. If `npx -y lumail@latest auth test` already succeeds, skip to step 5.
3. If the user has no Lumail account, send them to https://lumail.io and wait for "done".
4. Run `npx -y lumail@latest setup --authenticate` in the background with its output in a file. It installs the Lumail connection for their agent and opens the browser: tell the user to sign in, approve, and say "done". If no browser opens, read the link from the output file and give it to them. Check `npx -y lumail@latest auth test` until it succeeds.
5. Prove it: `npx -y lumail@latest auth test` succeeds and `npx -y lumail@latest --help` lists the commands. Do not create a sending domain now; the `create-*` skills add it with `lumail domain` when an app needs to send emails.

End with a short check list, a check or a cross on each line: Node works, signed in to Lumail, connection installed for the agent. Then tell the user in one line that the agent can now add subscribers and send emails from their apps.
