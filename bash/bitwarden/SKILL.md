---
name: bitwarden
description: >-
  Bitwarden / Vaultwarden vault via the bw CLI — session, vault read/write,
  Send. Self-hosted, API key login then unlock from .env. Use when the user
  mentions Bitwarden, a vault password, TOTP, a Send, or invokes /bitwarden_*.
disable-model-invocation: true
---

### TO COPY

# bitwarden

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
eval "$(~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/security/bitwarden/scripts/skill_env.py)"
export PATH="$HOME/.meta-skills/skills/security/bitwarden/node_modules/.bin:$PATH"
export BITWARDENCLI_APPDATA_DIR="$CURRENT_SKILL_DIRECTORY/.bw-appdata"
mkdir -p "$BITWARDENCLI_APPDATA_DIR"
bw config server "$BW_SERVER" 2>/dev/null || true
case "$(bw status | python3 -c 'import sys,json; print(json.load(sys.stdin).get("status",""))')" in
  unauthenticated) bw login --apikey ;;
esac
export BW_SESSION="$(bw unlock --passwordenv BW_PASSWORD --raw)"
```

Never print a vault secret unless the user asked — prefer clipboard / file.

##### END TO COPY

# bitwarden — Command Index

Router to `bw` command domains. References live in `command.md/` and `exemple.md/`
under the **shared library** (`~/.meta-skills/skills/security/bitwarden/`).

## Prerequisites

Official **`bw` CLI** ([docs](https://bitwarden.com/help/cli/)):

```bash
cd ~/.meta-skills/skills/security/bitwarden
~/.meta-skills/install.sh npm init .
```

Credentials in `{SKILL_PATH}/.env`: `BW_SERVER`, `BW_CLIENTID`, `BW_CLIENTSECRET`, `BW_PASSWORD`.

## Connect (every vault session)

1. `eval` `skill_env.py` (loads `.env`)
2. Put pinned `bw` on `PATH` + set `BITWARDENCLI_APPDATA_DIR`
3. `bw login --apikey` **only** if status is `unauthenticated`
4. `bw unlock --passwordenv BW_PASSWORD --raw` → `BW_SESSION`

Use the bash block in **Working directory** (TO COPY) above — do not re-login when
already `locked` / `unlocked`.

## When to use

Trigger phrases: "what's my password for X", "store this in Bitwarden", "create a login",
"Bitwarden Send", `/bitwarden_*`.

## bitwarden-vault-read

List / get items, folders, attachments, generate passwords.
Secrets: prefer clipboard; print only if the user asked.

Commands → `~/.meta-skills/skills/security/bitwarden/command.md/bitwarden-vault-read.command.md`
Examples → `~/.meta-skills/skills/security/bitwarden/exemple.md/bitwarden-vault-read.exemple.md`

---

## bitwarden-vault-write

Create / edit / delete / restore items, folders, attachments, collections.
Confirm with the user before every write.

Commands → `~/.meta-skills/skills/security/bitwarden/command.md/bitwarden-vault-write.command.md`
Examples → `~/.meta-skills/skills/security/bitwarden/exemple.md/bitwarden-vault-write.exemple.md`

---

## bitwarden-send

Ephemeral Bitwarden Send (text/file). The `accessUrl` is the secret.

Commands → `~/.meta-skills/skills/security/bitwarden/command.md/bitwarden-send.command.md`
Examples → `~/.meta-skills/skills/security/bitwarden/exemple.md/bitwarden-send.exemple.md`

---

## Org collections (Vaultwarden)
- Hierarchy: `Parent/Child` in **name** (no parentId).
- Read ACL: `bw get org-collection <id> --organizationid <org>` (not `get collection`).
- User ACL: **create then edit** — `users` on `create` is ignored by the CLI.
- Public API (`/public/members`): do not use on self-hosted Vaultwarden.
- See `command.md/bitwarden-org-collections.command.md`.

## Safety

- Confirm before create / edit / delete / send.
- Never commit `.env` or `.bw-appdata/`.
- Do not echo secrets into chat unless the user asked.
