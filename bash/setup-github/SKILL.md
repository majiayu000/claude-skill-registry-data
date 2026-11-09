---
name: setup-github
description: Install Git and the GitHub CLI (gh) on macOS, Linux or Windows, sign the user in to GitHub through the browser and set up their Git name and email, so the agent can create repos and push. Use when git or gh is missing, the user wants to connect GitHub, or gh auth status fails.
---

Make Git and GitHub work on the user's machine so the agent can create private repos and push code. Do every step yourself and only ask for what needs a human (a click in an install window, signing in, a one-time code). Talk to the user in their language, short messages, no jargon (never say "CLI", "PATH" or "token" to them). Never ask for their GitHub password or a token.

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/setup-github/<path> -o <scratch>/<file>` (for example `scripts/install-gh.sh`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

1. Find the OS with `uname -s` (`Darwin` is macOS, `Linux` is Linux); if it fails or PowerShell answers, it is Windows.
2. Make Git work, then check with `git --version`:
   - macOS: if `xcode-select -p` fails, Git is only an empty shell until Apple's developer tools are installed. Homebrew installs them, so if it is missing run the `setup-node` skill first (it installs Homebrew and Node, both needed later anyway). Only if the user cannot install Homebrew (no admin rights), run `xcode-select --install`, tell them a window just opened and to click "Install" then accept the licence, and check `xcode-select -p` every 30 seconds (in the background, up to 30 minutes) until it answers.
   - Linux: if Git is missing, installing it needs the user's password, so ask them to run `sudo apt install -y git` (or `sudo dnf install -y git`) in their own terminal and say "done".
   - Windows: Git comes with Claude Code; if it is missing, `winget install --id Git.Git -e`.
3. Install `gh`: on macOS and Linux run [scripts/install-gh.sh](scripts/install-gh.sh) (Homebrew on macOS, exit code 3 means Homebrew is missing so run `setup-node` first; on Linux or with `--no-brew`, the official release into `~/.local/bin`); on Windows `winget install --id GitHub.cli -e`. The current session does not see it yet: prefix your next commands with `eval "$(/opt/homebrew/bin/brew shellenv)"` (or `/usr/local/bin/brew` on Intel) on macOS, or `export PATH="$HOME/.local/bin:$PATH"` with the `~/.local` install.
4. If the user has no GitHub account, send them to https://github.com/signup and wait for "done". GitHub asks for two-step verification on new accounts: tell them it is normal and to follow it to the end.
5. If `gh auth status` already says logged in, skip to step 6. Otherwise start the login in the background, with the output in a file you can read:

   ```bash
   gh auth login --hostname github.com --git-protocol https --web --skip-ssh-key < /dev/null > <scratch>/gh-login.txt 2>&1
   ```

   Read the one-time code (`XXXX-XXXX`) from that file and give it to the user with https://github.com/login/device (open it in Chrome AI when `setup-dev-browser` is done). They paste the code, click "Authorize", and say "done". Check `gh auth status` until it says logged in. If the code expired, start again.
6. Run `gh auth setup-git` so `git push` uses this login.
7. Set the Git identity only if `git config --global user.name` is empty: the name from `gh api user --jq '.name // .login'`, and the private GitHub email from `gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"'` unless the user wants their real email shown in commits. Also run `git config --global init.defaultBranch main`.
8. Prove it: `gh auth status` is logged in, `gh api user --jq .login` prints their username, `gh repo list --limit 1` answers, `git config --global user.name` and `user.email` are set, and a new session finds `gh` too (`$SHELL -lic 'gh --version'`).

End with a short check list, a check or a cross on each line: Git works, `gh` installed, signed in as `<username>`, Git uses the GitHub login, name and email set. Then tell the user in one line that the agent can now create private repos and push for them.
