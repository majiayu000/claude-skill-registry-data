---
name: setup-node
description: Install Homebrew (macOS) and Node.js with npm on macOS, Linux or Windows, so npx, npm install -g and the CLIs that need them work. Use when node, npm or npx is missing or "command not found", or before setup-cloudflare, setup-convex, setup-lumail or setup-dev-browser.
---

Get a working Node.js LTS with `npm` and `npx` for the current user. Do it yourself and only ask the user for what needs a human. Talk to them in their language, short messages, no jargon (never say "PATH", "prefix" or "LTS" to them).

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/setup-node/<path> -o <scratch>/<file>` (for example `scripts/install-node.sh`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

1. Check first: if `node --version` prints v20 or higher and `npm --version` works, say so and stop.
2. Find the OS with `uname -s` (`Darwin` is macOS, `Linux` is Linux); if it fails or PowerShell answers, it is Windows.
3. On macOS, make sure Homebrew is there: it is the one way every setup skill installs tools on a Mac, it also installs Apple's developer tools (Git), and it keeps everything up to date. Look for `/opt/homebrew/bin/brew` (Apple Silicon) or `/usr/local/bin/brew` (Intel), even if `brew` is not found. If neither exists, Homebrew needs the user's Mac password once, so you cannot run it yourself: ask them to open the Terminal app (Cmd+Space, type "Terminal"), paste the line below, press Enter, type their Mac password when asked (nothing shows while typing, that is normal), press Enter again when it asks, and say "done" when it finishes (5 to 15 minutes).

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   If the Mac account is not an admin and the install refuses, skip Homebrew and pass `--no-brew` to the install scripts of every setup skill.
4. Install:
   - macOS and Linux: run [scripts/install-node.sh](scripts/install-node.sh). On macOS it uses `brew install node` and writes Homebrew into the shell config so new sessions find it; it exits with code 3 if Homebrew is missing (go back to step 3). On Linux, or with `--no-brew`, it downloads the official Node LTS into `~/.local/node` with no admin password.
   - Windows: `winget install --id OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements`, then ask the user to close and reopen the Claude session.

   The current session does not see the new install yet: prefix your next commands with `eval "$(/opt/homebrew/bin/brew shellenv)"` (or `/usr/local/bin/brew` on Intel) on macOS, or `export PATH="$HOME/.local/node/bin:$PATH"` with the `~/.local` install.
5. Make sure global installs work without admin rights: run `npm config get prefix`. If `npm install -g` fails with `EACCES`, run `npm config set prefix ~/.local` and make sure `~/.local/bin` is in the shell config. Never use `sudo npm`.
6. Prove it: `node --version && npm --version && npx --version`, then `npx -y cowsay ok` prints a cow. Then check a new session finds it too: `$SHELL -lic 'node --version'` prints the same version; if not, fix the shell config before going on.

Reply with the Node version and where it is installed, in one line.
