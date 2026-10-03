---
name: godaddy
description: >-
  GoDaddy Domains API v3 — suggest/check availability, get owned domain details,
  and manage DNS via a Python CLI (Bearer PAT). Use when the user mentions
  GoDaddy, domain availability, domain status/expiry, DNS records, or invokes
  /godaddy_*.
disable-model-invocation: true
---

### TO COPY

# godaddy

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/devops/dns/godaddy/scripts/cli.py env
```

##### END TO COPY

# godaddy

GoDaddy Domains API **v3** CLI:
[Discovery](https://developer.godaddy.com/en/docs/references/rest/domains/v3/discovery)
(`suggest` / `check-availability`) +
[Domains](https://developer.godaddy.com/en/docs/references/rest/domains/v3/domains)
(owned domain get) +
[DNS records](https://developer.godaddy.com/en/docs/references/rest/domains/v3/records).

Auth: `Authorization: Bearer ${GODADDY_PAT}` (see [`ORIGIN.md`](ORIGIN.md)).

## When to use

Trigger phrases: "check if domain is available on GoDaddy", "suggest domains",
"get my GoDaddy domain", "domain expiry / auto-renew", "list GoDaddy DNS",
"add A record", `/godaddy_*`.

`skill_env.py` loads `.env` via SkillCred — do not `source` it in the shell. `CURRENT_SKILL_DIRECTORY` is the only required export.

Prefer `~/.meta-skills/.venv/bin/python` from `~/.meta-skills/skills/devops/dns/godaddy/`.

## Credentials — SkillCred `.env`

| Variable | Notes |
|----------|--------|
| `GODADDY_PAT` | Required — Personal Access Token |
| `BASE_URL` | Default `https://api.godaddy.com` |

### Create a Personal Access Token (PAT)

1. Open **[Personal Access Token](https://developer.godaddy.com/en/personal-access-token)** and sign in to your GoDaddy account.
2. Click **+ Generate Token**.
3. Fill **Name**, **Expiration**, and **Scopes**:
   - `domains.domain:read` — discovery (`suggest` / `check`) + `domain get`
   - `domains.dns:update` — DNS add / delete (optional if you only need read/discovery)
   - Or pick the **Domains & DNS** bundle for full domain/DNS access
4. Click **Generate Token**, then **copy the token immediately** — it is shown only once.
5. Store it in the skill `.env` (never commit it, never paste it into chat):

```bash
cp .env.example "{SKILL_PATH}/.env"
# edit: GODADDY_PAT=<paste token>
python scripts/cli.py env    # prints resolved .env path
```

Docs: [How to Authenticate](https://developer.godaddy.com/docs/api-users/auth/how-to) · [PAT scopes](https://developer.godaddy.com/docs/api-users/auth#pat-scopes).  
To revoke: same [PAT page](https://developer.godaddy.com/en/personal-access-token) → trash icon next to the token.

First deps: `cd ~/.meta-skills/skills/devops/dns/godaddy && ~/.meta-skills/install.sh pip init .`

## Discovery ([docs](https://developer.godaddy.com/en/docs/references/rest/domains/v3/discovery))

Prices/availability are **indicative**; locked price is only at quote time.

| Slash | CLI | API |
|-------|-----|-----|
| `/godaddy_suggest` | `python scripts/cli.py suggest --query "sunrise bakery" [--tlds com,net] [--page-size 10] [--sources EXTENSION,KEYWORD_SPIN]` | `GET /v3/domains/suggestions` |
| `/godaddy_check` | `python scripts/cli.py check DOMAIN [--optimize-for SPEED\|ACCURACY] [--isc-code CODE]` | `GET /v3/domains/check-availability` |

## Domains

### List all domains — v1 ([docs](https://developer.godaddy.com/en/docs/references/rest/domains/v1/manage-domain-settings))

Paginated list of domains owned by the authenticated account.

| Slash | CLI | API |
|-------|-----|-----|
| `/godaddy_domain_list` | `python scripts/cli.py domain list [--statuses …] [--status-groups …] [--limit N] [--marker DOMAIN] [--includes authCode,contacts,nameServers] [--modified-date ISO] [--shopper-id ID]` | `GET /v1/domains` |

### Get one domain — v3 ([docs](https://developer.godaddy.com/en/docs/references/rest/domains/v3/domains))

Owned domain management view (status, nameservers, privacy, auto-renew, expiry).

| Slash | CLI | API |
|-------|-----|-----|
| `/godaddy_domain_get` | `python scripts/cli.py domain get DOMAIN` | `GET /v3/domains/domain-names/{domain-name}` |

## DNS CLI ([docs](https://developer.godaddy.com/en/docs/references/rest/domains/v3/records))

| Slash | CLI | API |
|-------|-----|-----|
| `/godaddy_dns_list` | `python scripts/cli.py dns list ZONE [--type A] [--name @] [--page N] [--page-size N] [--total-required]` | `GET /v3/domains/zones/{zone}/dns-records` |
| `/godaddy_dns_add` | `python scripts/cli.py dns add ZONE --type A --name @ --data 192.0.2.1 [--ttl 600] [--priority N]` | `POST /v3/domains/zones/{zone}/dns-records` |
| `/godaddy_dns_delete` | `python scripts/cli.py dns delete ZONE RECORD_ID` | `DELETE /v3/domains/zones/{zone}/dns-records/{recordId}` |
| `/godaddy_env` | `python scripts/cli.py env` | Resolve SkillCred `.env` path |

## Important — Safety rules

- Confirm with the user before **dns add** or **dns delete**.
- Deletes are irreversible — get `recordId` from `dns list` first.
- GoDaddy-managed SOA/NS records are read-only (`409` if deleted).
- To update a record: delete by `recordId`, then add the new one (or confirm with the user).
- Discovery does **not** register domains or charge money; registration/quote is out of scope of this skill.

## How to run

1. Export `CURRENT_SKILL_DIRECTORY` → registered skill dir (holds `.env`).
2. `cd` to library skill folder; `install.sh pip init .` once.
3. Run `python scripts/cli.py …`; stdout is JSON.

## Notes

- Never commit `.env` / `GODADDY_PAT`.
- Prefer JSON output from the CLI for agents.
