---
name: setup-cloudflare
description: Install the official Cloudflare CLI (cf) on macOS, Linux or Windows, sign the user in through the browser and pick their account, so the agent can manage domains, DNS and deploys. Use when cf is missing, the user wants to connect Cloudflare, or cf auth whoami is not authenticated.
---

Connect the user's Cloudflare account to the `cf` CLI so the agent handles domains, DNS and deploys without the user opening the dashboard. Do every step yourself and only ask for what needs a human (creating the account, approving the login, buying a domain). Talk to the user in their language, short messages, no jargon (never say "CLI", "OAuth" or "zone" to them). Never use Wrangler and never ask for an API token.

If you got this skill from a link instead of a local folder, install nothing else from the repo: fetch a file only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/setup-cloudflare/<path> -o <scratch>/<file>`, and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

1. Make sure Node works (`node --version`, v20 or higher); if not, run the `setup-node` skill first.
2. If the user has no Cloudflare account, send them to https://dash.cloudflare.com/sign-up and wait for "done". The free plan is enough.
3. Install the CLI with `npm install -g cf`, then check `cf --version`.
4. If `cf auth whoami` already says `"authenticated": true`, skip to step 5. Otherwise run `cf auth login` in the background with its output in a file. It opens the browser: tell the user to sign in, approve every permission including the sensitive ones (deploys and DNS need them), and say "done". If no browser opens, read the link from the output file and give it to them. Check `cf auth whoami` until it says authenticated.
5. Run `cf accounts list`. With more than one account, ask which one to use and add `export CLOUDFLARE_ACCOUNT_ID=<id>` to the user's shell config (`~/.zshrc` or `~/.bashrc`, on Windows a user environment variable) so every session uses it.
6. Run `cf zones list` to see their domains. If they have none, tell them they can buy one in Cloudflare (Domain Registration, at cost price) or keep one from another registrar and move its name servers to Cloudflare later; the `create-*` skills handle that when they need a domain. Never buy a domain for them.
7. Prove it: `cf auth whoami` is authenticated on the right account, `cf zones list` answers (with their domains or none yet), and a new session finds `cf` too (`$SHELL -lic 'cf --version'`).

End with a short check list, a check or a cross on each line: Node works, `cf` installed, signed in, account picked, domains found (list them or say none yet). Then tell the user in one line that the agent can now manage their domains and put sites live on Cloudflare.
