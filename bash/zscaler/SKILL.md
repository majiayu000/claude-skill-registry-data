---
name: zscaler
description: >-
  Zscaler ZPA, ZIA, and ZIdentity APIs via a Python CLI. Credentials in .env
  with nested JSON keys as SECTION__FIELD (ZPA__CLIENT_ID, ZIA__USERNAME, …).
  Use when the user mentions Zscaler, ZPA, ZIA, ZIdentity, or invokes
  /zscaler_*.
disable-model-invocation: true
---

### TO COPY

# zscaler

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/security/zscaler/scripts/cli.py env
```

##### END TO COPY

# zscaler

Zscaler ZPA / ZIA / ZIdentity via a Python CLI. Auth from SkillCred `.env`. Nested JSON keys use `__` as separator (`zpa.client_id` → `ZPA__CLIENT_ID`).

## When to use

Trigger phrases: "Zscaler", "ZPA", "ZIA", "ZIdentity", `/zscaler_*`.

`skill_env.py` loads `.env` via SkillCred — do not `source` it in the shell. `CURRENT_SKILL_DIRECTORY` is the only required export.

Prefer `~/.meta-skills/.venv/bin/python` from `~/.meta-skills/skills/security/zscaler/`.

## Credentials — SkillCred `.env`

`.env` is next to the **registered** skill, resolved by `SkillCred("zscaler", [".env"])`.

| Variable | JSON path | Notes |
|----------|-----------|--------|
| `ZPA__CLIENT_ID` | `zpa.client_id` | ZPA OAuth client id |
| `ZPA__CLIENT_SECRET` | `zpa.client_secret` | ZPA OAuth client secret |
| `ZPA__CUSTOMER_ID` | `zpa.customer_id` | ZPA customer id |
| `ZPA__CLOUD` | `zpa.cloud` | Default `ZPATWO` |
| `ZIA__USERNAME` | `zia.username` | ZIA API user |
| `ZIA__PASSWORD` | `zia.password` | ZIA API password |
| `ZIA__API_KEY` | `zia.api_key` | ZIA API key |
| `ZIA__CLOUD` | `zia.cloud` | Default `zscaler` |
| `ZIDENTITY__CLIENT_ID` | `zidentity.client_id` | ZIdentity OAuth client id |
| `ZIDENTITY__CLIENT_SECRET` | `zidentity.client_secret` | ZIdentity OAuth client secret |
| `ZIDENTITY__VANITY_DOMAIN` | `zidentity.vanity_domain` | Vanity domain |
| `ZIDENTITY__CLOUD` | `zidentity.cloud` | ZIdentity cloud |
| `ZIDENTITY__CUSTOMER_ID` | `zidentity.customer_id` | Customer id |

```bash
cp ~/.meta-skills/skills/security/zscaler/.env.example "{SKILL_PATH}/.env"
# edit ZPA__* / ZIA__* / ZIDENTITY__*
python scripts/cli.py env
```

First deps: `cd ~/.meta-skills/skills/security/zscaler && ~/.meta-skills/install.sh pip init .`

## Command sections

Map `/zscaler_<…>` → `python scripts/cli.py …`; return JSON. Slash/CLI tables live in `command.md/` under the shared library.

## zscaler-env

Validate `.env` (no network). Secrets are masked in the output.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-env.command.md`

---

## zscaler-zia-activate

ZIA configuration activation — status and run.
Create / update / delete commands activate pending changes automatically. Confirm before `run`.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zia-activate.command.md`

---

## zscaler-zia-users

ZIA users, groups, and departments (`LegacyZIAClient`). Credentials from SkillCred `.env`.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zia-users.command.md`

---

## zscaler-zia-url-categories

ZIA URL categories — list, get, create, add/remove URLs, delete.
Open the command file for `{CATEGORY_ID}` / `{CATEGORY_NAME}` / `{URL}`. Confirm before writes.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zia-url-categories.command.md`

---

## zscaler-zia-url-cloud-apps

ZIA URL cloud applications and URL categories — get only.
Open the command file for `{APP_ID}` / `{APP_NAME}` / `{CATEGORY_ID}` / `{CATEGORY_NAME}`.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zia-url-cloud-apps.command.md`

---

## zscaler-zia-url-filtering-policy

ZIA URL Filtering Policy — list, get, create, update, delete.
Open the command file for `{RULE_ID}` / `{RULE_NAME}` / `{ACTION}` / `{CATEGORY_ID}`. Confirm before writes.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zia-url-filtering-policy.command.md`

---

## zscaler-zia-ip-fqdn-groups

ZIA IP/FQDN destination groups — list, get, create, update.
Open the command file for `{GROUP_ID}` / `{GROUP_NAME}` / `{TYPE}` / `{ADDRESS}`. Confirm before writes.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zia-ip-fqdn-groups.command.md`

---

## zscaler-zia-dedicated-ip-gateways

ZIA dedicated IP gateways — list, get.
Open the command file for `{GATEWAY_ID}` / `{GATEWAY_NAME}`.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zia-dedicated-ip-gateways.command.md`

---

## zscaler-zia-forwarding-rule

ZIA forwarding control — list, get, create, delete.
Open the command file for `{RULE_ID}` / `{RULE_NAME}` / `{FORWARD_METHOD}` / `{GATEWAY_NAME}`. Confirm before writes.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zia-forwarding-rule.command.md`

---

## zscaler-zpa-application-segment

ZPA application segments — list, get, update (ports and IP / FQDN / URL only), delete.
Open the command file for `{SEGMENT_ID}` / `{SEGMENT_NAME}` / `{DOMAIN}` / `{PORT}`. Confirm before writes.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zpa-application-segment.command.md`

---

## zscaler-zpa-access-policy

ZPA access policy — list, get.
Open the command file for `{RULE_ID}` / `{RULE_NAME}`.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zpa-access-policy.command.md`

---

## zscaler-zpa-forwarding-policy

ZPA client forwarding policy — list, get.
Open the command file for `{RULE_ID}` / `{RULE_NAME}`.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zpa-forwarding-policy.command.md`

---

## zscaler-zpa-app-connector-group

ZPA App Connector groups — list, get.
Open the command file for `{GROUP_ID}` / `{GROUP_NAME}`.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zpa-app-connector-group.command.md`

---

## zscaler-zpa-app-connector

ZPA App Connectors — list, get, health.
Open the command file for `{CONNECTOR_ID}` / `{CONNECTOR_NAME}`. Health is true when every connector is `ZPN_STATUS_AUTHENTICATED`.

Commands → `~/.meta-skills/skills/security/zscaler/command.md/zscaler-zpa-app-connector.command.md`

---

## How to run

1. `export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"` then `cd ~/.meta-skills/skills/security/zscaler`.
2. Ensure `.env` exists next to the registered skill; `/zscaler_env`.
3. Map `/zscaler_<…>` → `~/.meta-skills/.venv/bin/python scripts/cli.py …`; return JSON.

## Notes

- Confirm with the user before destructive Zscaler writes (`url-categories delete`, `url-filtering-policy delete` / `update`, `ip-fqdn-groups create` / `update`, `forwarding-rule create` / `delete`, `application-segment update` / `delete`, `remove-urls`, `activate run`, and other updates).
- Never commit `.env` or echo `ZPA__CLIENT_SECRET`, `ZIA__PASSWORD`, `ZIA__API_KEY`, or `ZIDENTITY__CLIENT_SECRET`.
- Docs: [ZIA API](https://help.zscaler.com/zia/getting-started-zia-api), [ZPA API auth](https://help.zscaler.com/zpa/about-api-authentication).
