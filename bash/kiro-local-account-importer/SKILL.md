---
name: kiro-local-account-importer
description: Use when importing local Kiro CLI accounts into StaticFlow/llm-access from local SQLite files, including discovering auth SQLite files under specified directories or the default Kiro path, reading auth_kv locally, calling the locally mapped llm-access admin API, and applying Kiro account concurrency plus proxy assignment policy.
---

# Kiro Local Account Importer

Use this skill to import Kiro accounts without involving the StaticFlow backend.
The workflow runs locally, reads SQLite files directly, and calls the mapped
`llm-access` admin API such as `http://127.0.0.1:19182`.

## Boundaries

- Do not change backend code for this workflow.
- Do not ask remote/cloud `llm-access` to read local SQLite paths.
- Parse local SQLite locally, then call `llm-access` admin APIs.
- Do not print raw `access_token`, `refresh_token`, or `client_secret`.
- Dry-run first unless the user explicitly wants a real import.

## API Flow

Use `scripts/import_kiro_accounts.py`.

The script:

1. Discovers SQLite files from `--sqlite-file`, `--search-dir`, or the default
   `~/.local/share/kiro-cli/data.sqlite3`.
2. Reads supported Kiro auth records from `auth_kv`:
   - social: `kirocli:social:token`
   - IDC/OIDC: `kirocli:odic:token`, `kirocli:oidc:token`
   - device registration: matching `device-registration` keys
3. Creates the Kiro account through:
   `POST /admin/kiro-gateway/accounts/import-auth`
4. Sets standard scheduling:
   - `kiro_channel_max_concurrency = 3`
   - `kiro_channel_min_start_interval_ms = random[200, 1000]`
   - `minimum_remaining_credits_before_block >= 10`
5. Assigns proxy by patching:
   `PATCH /admin/kiro-gateway/accounts/{name}`
6. Validates the account by refreshing balance through the selected proxy:
   `POST /admin/kiro-gateway/accounts/{name}/balance`
7. Accepts the import only when balance refresh succeeds, remaining credits are
   at least `10`, and the refreshed upstream `user_id` is not already present
   on an existing Kiro account. If refresh fails, try the next United States
   proxy. If all proxies fail, if the account's remaining credits are below
   `10`, or if the refreshed `user_id` is a duplicate, delete the newly imported
   account and report it as invalid.

## Proxy Policy

Default proxy behavior:

- Fetch active proxies from `GET /admin/llm-gateway/proxy-configs`.
- Keep only active United States proxy nodes. With the current proxy schema,
  this is inferred from established proxy names such as `do-us-*`, `aws_us*`,
  `us-home*`, `my-homeus*`, and `dmit-us`.
- Count active Kiro accounts currently fixed to each proxy via
  `GET /admin/kiro-gateway/accounts?limit=10000&offset=0`.
- Try to read hot Kiro latency ranking from
  `/internal/kiro-gateway/latency-ranking?source=hot&window=1h`.
- Prefer the least-used active United States proxy first.
- Use hot first-token latency only as a tie-breaker within the same account
  count bucket, then break remaining ties by proxy name.
- If latency data is unavailable, choose the least-used active proxy and break
  ties by proxy name.
- Direct/no-proxy imports are not allowed for Kiro accounts.

## Commands

Default dry run:

```bash
python3 skills/kiro-local-account-importer/scripts/import_kiro_accounts.py \
  --admin-base-url http://127.0.0.1:19182
```

Dry run for one explicit SQLite:

```bash
python3 skills/kiro-local-account-importer/scripts/import_kiro_accounts.py \
  --admin-base-url http://127.0.0.1:19182 \
  --sqlite-file /path/to/data.sqlite3 \
  --account-name kiro-main
```

Dry run for a directory:

```bash
python3 skills/kiro-local-account-importer/scripts/import_kiro_accounts.py \
  --admin-base-url http://127.0.0.1:19182 \
  --search-dir /path/to/kiro-auth-dbs \
  --name-prefix kiro-
```

Apply after reviewing dry-run output:

```bash
python3 skills/kiro-local-account-importer/scripts/import_kiro_accounts.py \
  --admin-base-url http://127.0.0.1:19182 \
  --search-dir /path/to/kiro-auth-dbs \
  --name-prefix kiro- \
  --apply
```

If the mapped admin API requires a token, add:

```bash
--admin-token "$STATICFLOW_ADMIN_TOKEN"
```

## Verification

After real import, verify:

```bash
curl -fsS http://127.0.0.1:19182/admin/kiro-gateway/accounts?limit=20 \
  | jq '.accounts[] | {name, kiro_channel_max_concurrency, kiro_channel_min_start_interval_ms, proxy_mode, proxy_config_id}'
```

Expected:

- imported accounts exist;
- max concurrency is `3`;
- min start interval is between `200` and `1000`;
- minimum remaining credits is at least `10`;
- proxy mode is `fixed`;
- proxy name is a United States node.
- the real import output has `validated: true` and includes the refreshed
  balance response.
- no imported account duplicates an existing refreshed Kiro `user_id`.
