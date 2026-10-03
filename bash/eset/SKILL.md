---
name: eset
description: >-
  Authenticate to ESET Connect (ESET Business Account IAM) and obtain an OAuth
  Bearer token via POST /oauth/token, using the bundled Python CLI (cli.py;
  OAuth logic in authentication.py). Shared CLI lib; per-workspace .env. Use when the user
  mentions ESET, ESET Connect, ESET PROTECT, an ESET API token, or invokes
  /eset_*.
disable-model-invocation: true
---

### TO COPY

# eset

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/mdm-antivirus/eset/script/cli.py env-check
```

##### END TO COPY

# eset

## When to use

Use to get an ESET Connect OAuth token (Bearer) for calling ESET Connect APIs.
Trigger phrases: "ESET token", "authenticate to ESET Connect", "ESET Business
Account login", `/eset_*`.

`skill_env.py` (extends `SkillEnv`) loads `.env` via SkillCred — do not `source` it in the shell. `CURRENT_SKILL_DIRECTORY` is the only required export.

Prefer `~/.meta-skills/.venv/bin/python`. First deps:
`cd ~/.meta-skills/skills/mdm-antivirus/eset && ~/.meta-skills/install.sh pip init .`

## Credentials — SkillCred `.env`

`.env` is next to the **registered** skill, resolved by `SkillCred("eset", [".env"])`
under `$CURRENT_SKILL_DIRECTORY` (via `script/skill_env.py`).

| Variable | Notes |
|----------|--------|
| `ESET_URL` | Region base **without** `/oauth/token` (`eu`/`us`/… or full URL) |
| `ESET_USERNAME` | IAM username |
| `ESET_PASSWORD` | IAM password |
| `ESET_ACCESS_TOKEN` | Written by `cli.py token` / first API call — reloaded automatically |
| `ESET_REFRESH_TOKEN` | Written on login — used to refresh without re-asking password |

```bash
cp ~/.meta-skills/skills/mdm-antivirus/eset/.env.example "{SKILL_PATH}/.env"
# edit ESET_URL / ESET_USERNAME / ESET_PASSWORD
python cli.py token          # POST /oauth/token → saves tokens into .env
python cli.py env-check
```

## Authentication

[`POST /oauth/token`](https://help.eset.com/eset_connect/en-US/authentication_oauth_token_post.html)
lives in `authentication.py` (`TOKEN_PATH = "/oauth/token"`).

Token resolution (inside each API request via `BaseClient`):

1. `--token` if passed (one-shot override)
2. else `ESET_ACCESS_TOKEN` from `.env`
3. else refresh via `ESET_REFRESH_TOKEN`
4. else password grant with `ESET_USERNAME` / `ESET_PASSWORD`

On **401**, the client forces a new token (refresh → password) and **retries the request once**.
Successful exchanges upsert `ESET_ACCESS_TOKEN` / `ESET_REFRESH_TOKEN` into the SkillCred `.env`.

## Command sections

API commands auto-acquire a token from `.env`. Map `/eset_<…>` → `python cli.py …`; return JSON.

Pass `--token` on any API command to override the `.env` token. List commands support `--page-size`; most also support `--page-token`. Gateway host and env override are in each command file.

## eset-auth

OAuth token and `.env` validation — run before any API call or when credentials fail.
Use for `/eset_env-check`, `/eset_token`, or debugging authentication.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-auth.command.md`

---

## eset-device-management

Device groups and enrolled endpoints — list, move, rename, batch import.
Use to find device UUIDs, inspect inventory, or reorganize groups.

JSON fields follow the ESET Connect schema (`displayName`, `newParentUuid`, …).
CLI flags (`--name`, `--group`) are aliases; never copy the flag name into the body.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-device-management.command.md`

---

## eset-application-management

Executable (application) block/unblock control on endpoints.
Use to allow or deny specific programs across the fleet.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-application-management.command.md`

---

## eset-asset-management

Static and dynamic group lifecycle — create, delete, move, rename.
Use to structure the device tree (organizational groups).

JSON fields follow the ESET Connect schema (`displayName`, `parentGroupUuid`,
`newParentUuid`, …). CLI flags (`--name`, `--parent`) are aliases; never copy
the flag name into the body.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-asset-management.command.md`

---

## eset-policy-management

Security policies and assignments (API v2) — create, assign, rank.
Use to deploy or audit endpoint protection policies.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-policy-management.command.md`

---

## eset-detections

Threat detections and detection groups — list, resolve, search.
Use for ESET PROTECT (v1) or Inspect/Cloud Office (v2) detection triage.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-detections.command.md`

---

## eset-edr

EDR custom rules and exclusions — create, enable, update definitions.
Use when tuning ESET Inspect detection rules or whitelisting paths.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-edr.command.md`

---

## eset-incidents

Security incidents and comments — triage, close, reopen, annotate.
Use for ESET Inspect incident response workflows.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-incidents.command.md`

---

## eset-automation

Remote device tasks — scan, isolate, patch, run commands, shutdown.
Use to trigger actions on one or more endpoints (device/group UUIDs required).

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-automation.command.md`

---

## eset-patch-management

Pending patches per device — list, inspect history, apply updates.
Use to audit missing patches or deploy application/OS updates.

Commands → `~/.meta-skills/skills/mdm-antivirus/eset/command.md/eset-patch-management.command.md`

---

## How to run

1. `export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"` then `cd ~/.meta-skills/skills/mdm-antivirus/eset/script`.
2. Ensure `.env` exists next to the registered skill; `/eset_env-check`.
3. Map `/eset_<…>` → `~/.meta-skills/.venv/bin/python cli.py …`; return JSON.
4. Tokens are stored in `.env` — do not log or echo them.

### Examples

```bash
python cli.py env-check
python cli.py token                 # login + save ESET_ACCESS_TOKEN / ESET_REFRESH_TOKEN
python cli.py token --token-only
python cli.py token --print-request
python cli.py token --refresh "<refresh_token>"
python cli.py devices list          # reuses ESET_ACCESS_TOKEN from .env
```

## Notes

- `authentication.py` owns `TOKEN_PATH=/oauth/token`, token exchange, and `.env` persistence.
- `skill_env.py` resolves the SkillCred `.env` (`CURRENT_SKILL_DIRECTORY`).
- API clients keep only implemented endpoints; gateway hosts are in each command file.
- Never commit `.env` or echo tokens.
- `202` = request cached; retry with `response-id`.
- Docs: [POST /oauth/token](https://help.eset.com/eset_connect/en-US/authentication_oauth_token_post.html).
