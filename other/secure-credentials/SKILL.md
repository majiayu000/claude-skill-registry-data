---
name: secure-credentials
description: "Handles API keys, passwords, tokens and one-time secret links with Claude without the secret ever showing up in chat, logs, tool output or git. You put the value straight into a locked-down .env file, the OS keychain or a password manager; Claude reads it by name, checks it with one read-only call, reports only the status and the last 4 characters, and cleans up after itself. Covers .gitignore and gitleaks pre-commit scanning, redacting output, least-privilege keys, shell history cleanup and a rotation checklist for when a key leaks. Use when someone says \"here is my API key\", \"save this key\", \"set up my .env\", \"store this token safely\", \"I got a one-time secret link\", \"is my key working\", \"I pasted my key in chat\", \"I committed a secret\" or \"rotate this key\"."
---

# Secure Credentials

Anything pasted into a chat with Claude, or printed by a command, ends up in the conversation history. This skill keeps secret values out of both. Claude works with the secret's name (`OPENAI_API_KEY`), never its value. You enter the value yourself, in your own terminal, into a store only your user account can read.

Copy-paste shell snippets for every step are in `references/shell-snippets.md`. The leak checklist is in `templates/ROTATION-CHECKLIST.md`.

## Rules

1. **Never paste a secret into chat.** If one gets pasted anyway, treat it as leaked: stop, do not repeat it, and start the rotation checklist.
2. **Never print a secret.** No `echo $KEY`, `cat .env`, `env`, `printenv`, `set -x`, or debug dumps of request headers. To prove a key exists, print its length and last 4 characters only.
3. **Never put a secret on a command line.** Arguments can show up in `ps`, shell history and Claude's tool log. Read from a file, the keychain or stdin instead.
4. **One store per secret, locked down.** A `.env` file with mode `600` that git ignores, the OS keychain, or a password or secrets manager (1Password, Bitwarden, Vault, AWS or GCP Secret Manager). No secrets in source files, READMEs, screenshots, tickets or chat apps.
5. **Validate read-only.** Check a key with the smallest read-only call the provider has (who am I, list models, read balance). Never test a key by creating, sending, charging or deleting anything.
6. **Least privilege.** Ask for the narrowest key that does the job: scoped, read-only where possible, one project or repo, an expiry date. A working key is not permission to do everything it can do.
7. **A leaked key gets rotated, not just deleted.** Deleting a file or a chat message does not erase copies in logs, backups, git history or the provider's records.

## Steps

### 1. Decide the name and the store

Before anyone touches the value, Claude confirms: which service, which environment (dev or production), the variable name (for example `STRIPE_SECRET_KEY`), and where it will live. Default is a `.env` file in the project root.

### 2. Lock the destination before the secret exists

- Add `.env`, `.env.*` and `*.pem` to `.gitignore` (keep a `.env.example` with names and no values).
- Create the `.env` file with mode `600` (owner read and write only).
- Check that git really ignores it: `git check-ignore -v .env` must print a match.

### 3. You enter the value, outside the chat

Run the `set_secret` helper from the snippets file in **your own terminal window**, not through Claude. It reads the value with hidden input (or from the clipboard), writes or replaces just that one line in `.env`, keeps the mode at `600`, and prints nothing but the variable name. Then tell Claude "saved".

Prefer a keychain or password manager? Store it there and have the project load it at run time (`security`, `secret-tool` or `op read` in the snippets).

### 4. Claude validates without seeing it

Claude loads the file into the environment of a single command and calls one read-only endpoint. The only output is something like:

```
OPENAI_API_KEY: set, length 51, ends ...a1b2, HTTP 200
```

How to read the status:
- `200`: the key works for that call.
- `401`: the key itself is wrong, revoked or truncated. Do not save over an older working key.
- `403` or `404`: the key works but lacks a scope, or can't see that project, org or repo.
- `429`: rate limited. The key is probably fine.

### 5. Keep it out of git

- Install gitleaks and add it as a pre-commit hook so a commit containing a key is blocked before it happens.
- Run a full scan once on the repo, including history, with `--redact` so findings don't print the secret.
- If a scan finds a real key, go to the rotation checklist first. Rewriting git history comes second, because the key is already out.

### 6. Redact anything that might echo it

Logs, error messages, crash reports and API responses can contain the key (some APIs echo credentials, and URLs like `https://user:token@host` hide one in plain sight). Pipe risky output through the `redact` filter from the snippets, and keep `curl -v`, verbose SDK logging and `set -x` off while keys are loaded.

### 7. Clean up

- Delete temp files, downloaded secret files, scratch scripts and screenshots of reveal pages.
- Clear the clipboard if the value went through it.
- If a value was ever typed on a command line, remove that line from shell history.
- Re-check: `.env` is mode `600`, still ignored by git, and the gitleaks scan is clean.

## One-time secret links

Links from services like onetimesecret.com or a password manager's share feature show the value once, then die. Opening the link to "take a look" spends it.

1. Do steps 1 and 2 first, so the destination is ready.
2. Open the link yourself, once, in your own browser. Claude does not open it unless you ask, and even then only with a script that writes the value straight to the store without printing it.
3. Copy the value, run `set_secret` with the clipboard option, then clear the clipboard.
4. Claude validates (step 4).
5. Tell the sender it was received and stored, so they know the link is spent. If the link was already opened by someone else, or the value fails validation, ask for a new secret. Never ask them to paste it into chat instead.

## Output

When Claude finishes, the report contains only:

- variable name and where it is stored (file path or keychain service name)
- file mode (`600`) and whether git ignores it
- validation result: endpoint used, HTTP status, length and last 4 characters
- what was deliberately not done (no writes, no charges, no sends)
- anything left for you: a rotation, a scope to add, a temp file it could not delete

Never a prefix, a full value, a hash meant to identify the key, or a response body that might contain it.

## Honest limits

- This lowers exposure, it does not make a machine secure. Anyone or anything running as your user can read a `600` file, including Claude, scripts and malware. A keychain or secrets manager is stronger for anything that touches money or production.
- Claude can still see a secret if a command prints it. These rules depend on Claude following them, so watch for commands that `cat`, `echo` or dump environments and refuse them.
- Deleting a leaked value from a chat, a log or a commit does not un-leak it. Only rotation fixes a leak.
- gitleaks catches known key formats and high-entropy strings. It misses plain passwords and custom tokens. Treat a clean scan as a good sign, not proof.
- Provider endpoints and key formats change. If a validation call 404s for everyone, check the provider's current docs before blaming the key.
