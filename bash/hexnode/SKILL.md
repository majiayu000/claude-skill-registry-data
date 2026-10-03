---
name: hexnode
description: >-
  Hexnode MDM REST API via a Python CLI (API key auth). Devices, users, apps,
  policies, and device groups against https://<portal>.hexnodemdm.com/api/v1.
  Use when the user mentions Hexnode, Hexnode MDM/UEM, or invokes /hexnode_*.
disable-model-invocation: true
---

### TO COPY

# hexnode

Hexnode MDM API CLI ([developers](https://www.hexnode.com/mobile-device-management/developers/)).

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
eval "$(~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/mdm-antivirus/hexnode/scripts/skill_env.py)"
cd ~/.meta-skills/skills/mdm-antivirus/hexnode
~/.meta-skills/.venv/bin/python scripts/cli.py devices list --per-page 50
```

Prefer `~/.meta-skills/.venv/bin/python`. First deps:
`cd ~/.meta-skills/skills/mdm-antivirus/hexnode && ~/.meta-skills/install.sh pip init .`

##### END TO COPY

# hexnode

Hexnode MDM API CLI ([developers](https://www.hexnode.com/mobile-device-management/developers/)).

## When to use

Trigger phrases: "Hexnode devices", "Hexnode users", "Hexnode apps",
"Hexnode policies", "device groups", "enrollment request", "Hexnode MDM API",
`/hexnode_*`.

`skill_env.py` (extends `SkillEnv`) loads `.env` via SkillCred — do not `source` it in the shell. `CURRENT_SKILL_DIRECTORY` is the only required export.

Prefer `~/.meta-skills/.venv/bin/python`. First deps:
`cd ~/.meta-skills/skills/mdm-antivirus/hexnode && ~/.meta-skills/install.sh pip init .`

## Credentials — SkillCred `.env`

`.env` is next to the **registered** skill, resolved by `SkillCred("hexnode", [".env"])`
under `$CURRENT_SKILL_DIRECTORY` (via `scripts/skill_env.py`).

You can authenticate with the Hexnode MDM API by providing your secret API key with each request. The API uses HTTP Basic Authentication to receive your API key. It will look for your API key in the Authentication field.

Prior to authentication, enable API access in Hexnode MDM (**Admin → API → Enable API Access**), then copy the key.

| Variable | Notes |
|----------|--------|
| `HEXNODE_API_KEY` | Required — secret API key from Admin → API |
| `HEXNODE_BASE_URL` | Required — full API base (`https://<portal>.hexnodemdm.com/api/v1`) |
| `HEXNODE_PORTAL` | Optional — portal name only; derives `HEXNODE_BASE_URL` when base URL is omitted |

```bash
cp ~/.meta-skills/skills/mdm-antivirus/hexnode/.env.example "{SKILL_PATH}/.env"
python scripts/cli.py env
```

Working request format (same as Hexnode curl examples): send the **raw API key** as the `Authorization` header value (no `Bearer` / `Basic` prefix). Docs: [Authentication](https://www.hexnode.com/mobile-device-management/developers/setting-up-an-api/authentication/) · [Retrieve API Key](https://www.hexnode.com/mobile-device-management/developers/setting-up-an-api/retrieve-api-key/).

## Command sections

Map `/hexnode_<…>` → `python scripts/cli.py …`; return JSON. Slash/CLI tables live in `command.md/` under the shared library.

## hexnode-devices

List and inspect enrolled devices, policies, applications, and locations.
Open the command file when you need device inventory, per-device policy/app/location data, or `/hexnode_env`.

Commands → `~/.meta-skills/skills/mdm-antivirus/hexnode/command.md/hexnode-devices.command.md`

---

## hexnode-users

User lifecycle and enrollment — create, edit, delete, send enrollment requests.
Open the command file when managing Hexnode users or triggering device enrollment.

Commands → `~/.meta-skills/skills/mdm-antivirus/hexnode/command.md/hexnode-users.command.md`

---

## hexnode-applications

Portal app catalog — list, search, add, and inspect managed applications.
Open the command file when working with the Hexnode app repository (not apps installed on a device).

Commands → `~/.meta-skills/skills/mdm-antivirus/hexnode/command.md/hexnode-applications.command.md`

---

## hexnode-policies

Portal policy lifecycle — create, edit, archive, and inspect MDM policies.
Open the command file when creating or updating policy payloads (prefer `--file` for full platform dictionaries).

Commands → `~/.meta-skills/skills/mdm-antivirus/hexnode/command.md/hexnode-policies.command.md`

---

## hexnode-device-groups

Device group lifecycle — create, update, add/remove members, delete.
Open the command file when organizing devices into groups or changing group membership.

Commands → `~/.meta-skills/skills/mdm-antivirus/hexnode/command.md/hexnode-device-groups.command.md`

---

## How to run

1. `export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"` then `eval "$(~/.meta-skills/.venv/bin/python scripts/skill_env.py)"`.
2. `cd ~/.meta-skills/skills/mdm-antivirus/hexnode`; ensure `.env` exists next to the registered skill; `/hexnode_env`.
3. Map `/hexnode_<…>` → `~/.meta-skills/.venv/bin/python scripts/cli.py …`; return JSON.
4. Never log or echo `HEXNODE_API_KEY`.

## Notes

- Confirm with the user before destructive Hexnode actions (wipe, lock, …) if those are added later.
- Credentials live next to the registered `SKILL.md` (`$CURRENT_SKILL_DIRECTORY`).
- Never commit `.env` or API keys.
