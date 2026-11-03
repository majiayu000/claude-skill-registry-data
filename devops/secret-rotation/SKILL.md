---
name: secret-rotation
description: "Use when a secret leaked or must be rotated. The safe order: revoke at the provider, new value in env files (0600) on every host, restart, purge git history only with the owner's yes, re-scan and prove the old value is dead."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, security, secrets, rotation, git, incident]
    related_skills: [sterilise-before-commit, telegram-bot-troubleshooting, github, consent]
---

# Secret rotation — revoke first, clean up second

## When to use

A token, API key, password or private key appeared somewhere it should not (a commit, a log, a chat, a screenshot), or the owner wants a routine rotation. Assume a leaked secret is already copied: revoking it is the fix, purging history is only hygiene.

## Prerequisites

- The owner, because only they can sign in to the provider consoles. You never see or type the new value; it goes from the provider straight into the env file.
- Every step is a WRITE. Ask for the terminal grant once per session: `~/.iclone-os/bin/acp consent request terminal --reason "Rotate <provider> secret"`. Then, before each step, state in chat which secret, which hosts and which services restart, and wait for the owner's yes. A history rewrite needs its own, separate yes.
- Truth: the provider's own docs, `git filter-repo --help`, `gitleaks git --help`.

## Quick reference

| `<provider>`          | Revoke and reissue                                                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| Telegram bot          | @BotFather `/revoke` → new token (the old one dies at once)                                                |
| GitHub PAT            | Settings › Developer settings › Personal access tokens → delete, create new; `gh auth login`               |
| GitHub Actions secret | `gh secret set <NAME> --repo <owner>/<repo>` (prompts, value never on argv)                                |
| LLM / SaaS API key    | provider console → delete key → create key                                                                 |
| SSH key               | `ssh-keygen -t ed25519 -C <label> -f ~/.ssh/<new-key>`, add the new `.pub` everywhere, then remove the old |
| Webhook secret        | new random value, then `setWebhook` again with it (see `telegram-bot-deploy`)                              |

## Procedure

1. **Inventory.** Name the secret, where it leaked, and every place that uses it (hosts, CI, apps). Search your own files only for the variable NAME, never the value: `grep -rn '<VAR_NAME>' <config-dirs>` (`# example`).

2. **Revoke at the provider** (the owner does it, you guide). After this the leak is harmless.

3. **Put the new value in place on every host** — copy the current env file (mode 0600, owned by the service user), change only the rotated line, then swap it in. Every other variable is kept; the value is never echoed:

   ```sh
   sudo install -m 600 -o <svc-user> <dir>/.env <dir>/.env.new && sudoedit <dir>/.env.new && sudo mv <dir>/.env.new <dir>/.env  # example
   ```

   On a Mac use the app's own secret field or the Keychain, not a shell command.

4. **Restart every service that reads it** (env files are read only at start):

   ```sh
   sudo systemctl restart <service> && systemctl is-active <service>  # example
   ```

5. **Prove the old value is dead.** For a bot, `getMe` with the old token answers `401`; for GitHub, an API call with the old PAT answers `401`. Use the old value from the leak location, not a new file.

6. **Purge it from git history — only if it was committed, and only after the owner's explicit yes** (rewrites every later commit id, breaks open pull requests and other clones). Work in a fresh clone and keep a backup:

   ```sh
   git clone --mirror <repo-url> purge.git && git -C purge.git bundle create ../before-purge.bundle --all  # example
   ```

   ```sh
   cd purge.git && git filter-repo --sensitive-data-removal --replace-text <expressions-file>  # example
   ```

   `<expressions-file>` holds one literal per line (or `regex:` lines); it lives outside the repo and is deleted after. Ask the owner a second time, then push the rewrite:

   ```sh
   git push --force --mirror origin  # example
   ```

   If `git remote -v` lost `origin`, re-add it (`git remote add origin <repo-url>`). Rejected `refs/pull/*` updates are expected; branch protection may need a temporary owner change. Then ask GitHub support to drop cached views and pull-request refs (forks keep their copy — that is why step 2 comes first), and tell every collaborator to re-clone.

7. **Re-scan** the rewritten history and the working trees:

   ```sh
   gitleaks git --no-banner --redact .; echo "exit=$?"  # example
   ```

8. **Prevent the next one:** add the file pattern to `.gitignore` and run `sterilise-before-commit` before every push.

## Pitfalls

- Purging history without revoking leaves a live secret in every fork, clone and cache.
- Rotating in one place only: a host still running the old value fails at the next restart.
- `export TOKEN=<value>` in a shell lands in history files; `curl -H "Authorization: …<value>"` shows in `ps`.
- `git filter-repo` refuses a non-fresh clone; do not add `--force` to get past it — clone again.
- The backup bundle still holds the secret: keep it local and private, delete it once the owner confirms.

## Never

- Never paste the old or new value into chat, a commit, an issue or a log.
- Never force-push or rewrite history without the owner's yes for that exact step.
- Never commit the new value "just to test".

## Verification

The old value answers `401` (or the provider shows it revoked), `systemctl is-active <service>` prints `active` on every host, and `gitleaks git --no-banner --redact .` exits `0`.
