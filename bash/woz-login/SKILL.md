---
name: woz-login
description: Authenticate with the Woz service. Use when the user needs to log in or when authentication is required.
allowed-tools: Bash(node *), Bash(npx *)
---

# Woz Login Flow

If the user passed `--token <token>` as arguments, skip directly to the Token Login section below.

## Browser Login (Preferred)

First try the installed WOZCODE login command. This opens a browser for the user to log in:

```bash
node "${CODEX_HOME:-$HOME/.codex}/plugins/wozcode/scripts/wozcode-cli-codex.js" login
```

If the command exits with code 0, login succeeded — confirm to the user.

If Codex blocks the browser launch or the command fails before the browser opens, ask the user to run this command in their regular terminal outside Codex:

```bash
npx @wozcode/codex login
```

Tell the user to return after the command prints that authentication succeeded.

## Token Login

Use this when:
- The user passed `--token <token>` as arguments to this skill
- The browser login above timed out or failed and the user provides a token

Once you have the token (from args or from the user), run:

```bash
node "${CODEX_HOME:-$HOME/.codex}/plugins/wozcode/scripts/wozcode-cli-codex.js" login --token '<token>'
```

If Codex blocks the installed command from running, ask the user to run this in their regular terminal outside Codex:

```bash
npx @wozcode/codex login --token '<token>'
```

Replace `<token>` with the actual token. The npm command still requires WOZCODE for Codex to be installed first.

Confirm success or relay any error to the user.
