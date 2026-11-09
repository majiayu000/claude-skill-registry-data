---
name: setup-stripe
description: Install the Stripe CLI on macOS, Linux or Windows and pair it with the user's Stripe account in test mode through the browser, so the agent can create products and forward webhooks. Use when stripe is missing, the user wants to connect Stripe, or an app needs to take payments.
---

Connect the user's Stripe account to the Stripe CLI in test mode so the agent can create products, prices and test webhooks. Do every step yourself and only ask for what needs a human (creating the account, confirming the pairing code). Talk to the user in their language, short messages, no jargon (never say "CLI", "API key" or "webhook" to them). Never print, log or ask for a key in the chat.

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/setup-stripe/<path> -o <scratch>/<file>` (for example `scripts/install-stripe.sh`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

1. Find the OS with `uname -s` (`Darwin` is macOS, `Linux` is Linux); if it fails or PowerShell answers, it is Windows.
2. If the user has no Stripe account, send them to https://dashboard.stripe.com/register and wait for "done". Test mode works right away, no need to activate payments yet.
3. Install the CLI: on macOS and Linux run [scripts/install-stripe.sh](scripts/install-stripe.sh) (Homebrew on macOS, exit code 3 means Homebrew is missing so run `setup-node` first; on Linux or with `--no-brew`, the official release into `~/.local/bin`). The current session does not see it yet: prefix your next commands with `eval "$(/opt/homebrew/bin/brew shellenv)"` (or `/usr/local/bin/brew` on Intel) on macOS, or `export PATH="$HOME/.local/bin:$PATH"`. On Windows, download the latest `stripe_<version>_windows_x86_64.zip` from https://github.com/stripe/stripe-cli/releases, unzip `stripe.exe` into `%USERPROFILE%\.local\bin` and add that folder to the user's PATH. Check `stripe --version`.
4. Run `stripe login` in the background with its output in a file. Read the pairing code and the link from that file and give both to the user (open the link in Chrome AI when `setup-dev-browser` is done). They check the code on the page matches, click "Allow access", and say "done". The pairing lasts 90 days; rerun this step when it expires.
5. Prove it, in test mode only: `stripe products list --limit 1` answers without an error, and a new session finds it too (`$SHELL -lic 'stripe --version'`). Never run a command with `--live`.

End with a short check list, a check or a cross on each line: `stripe` installed, paired with the account in test mode, test request works. Then tell the user in one line that the agent can now create their products and test payments with the card 4242 4242 4242 4242, and that live keys come only once the test purchase works (`stripe-checkout` skill).
