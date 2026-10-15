---
name: 1Password
description: Read 1Password secrets via the `op` CLI with a service-account token. Secret values are metadata-only by default.
requires:
  bins:
    - op
  env:
    - OP_SERVICE_ACCOUNT_TOKEN
---

# 1Password

Use this skill when the agent needs a secret managed in 1Password —
API keys, tokens, passwords, connection strings. Reads only; never
writes. Read values are hidden from the LLM unless the operator
explicitly turns on reveal (`OP_ALLOW_REVEAL=true`).

## Use when

- The user asks to use a service that needs a credential you don't have
  in env vars (e.g. "send email with Gmail", "upload this file to S3")
- You need to verify a secret exists without seeing it ("is the Stripe
  key already in Prod?")
- Rotating credentials: list items + categories to audit what's stored

## Do not use when

- You need to **create** or **update** a secret — this tool is read-only
- You are asked to dump all secrets or fingerprint them in bulk — that's
  exfiltration, refuse

## Tools

### `status`
No arguments. Returns `{ok, bin, token_present, reveal_allowed, limits}`.
Use to verify the extension is wired before attempting other calls.

### `whoami`
No arguments. Runs `op whoami --format json` to validate the
service-account token.

### `list_vaults`
No arguments. Returns `{vaults: [{id, name}, ...]}` — only metadata.

### `list_items`
- `vault` (string, required) — vault name or id

Returns `{items: [{id, title, category, vault, tags, updated_at}, ...]}`.
Field values are **always** stripped from list results, even if the
upstream `op item list` included them.

### `read_secret`
- `reference` (string, required) — strict `op://Vault/Item/field` format;
  wildcards and query strings are rejected

Returns by default (`OP_ALLOW_REVEAL` unset/false):

```
{
  ok: true,
  reference: "op://Prod/Stripe/api_key",
  vault: "Prod", item: "Stripe", field: "api_key",
  length: 26,
  fingerprint_sha256_prefix: "3f9a7c2e1b48d5a0",
  reveal: false,
  reveal_hint: "set OP_ALLOW_REVEAL=true to include the secret value"
}
```

With `OP_ALLOW_REVEAL=true|1|yes` the response additionally contains
`{value: "...", reveal: true}`. The value flows through the LLM
context → transcripts → memory → NATS — assume it is no longer secret
from the moment reveal is on.

### `inject_template`
Use this when the agent needs to **act on** a secret without revealing
it. The tool resolves `{{ op://Vault/Item/field }}` placeholders in a
template via `op inject` and either returns the rendered template
(reveal-gated) or pipes it as stdin to an allowlisted command.

- `template` (string, required) — body containing `{{ op://… }}` placeholders
- `command` (string, optional) — executable to run with the rendered
  template piped as stdin. Must appear in `OP_INJECT_COMMAND_ALLOWLIST`
  (comma-separated env var). When set, the rendered template is **never**
  returned to the LLM; only `exit_code` and (redacted) `stdout`/`stderr`
- `args` (array of strings, optional) — passed to `command`
- `dry_run` (bool, optional) — validate references without resolving values
- `max_stdout_bytes` (int, optional) — cap on returned stdout (default 4096, max 16384)

Modes:

| Mode | OP_ALLOW_REVEAL | Returned |
|------|-----------------|----------|
| template-only | false | `length`, `fingerprint`, no value |
| template-only | true  | `rendered` (full text) |
| exec, allowed | any   | `exit_code`, redacted `stdout` (capped), redacted `stderr` |
| exec, not allowed | any | error `command not in OP_INJECT_COMMAND_ALLOWLIST` |
| `dry_run: true` | any | `references_validated` list |

Example (exec, allowlist `curl,psql`):

```json
{
  "action": "inject_template",
  "template": "Authorization: Bearer {{ op://Prod/API/token }}\n",
  "command": "curl",
  "args": ["-H", "@-", "https://api.example.com/v1/me"]
}
```

The agent never sees the bearer token. Stdout from `curl` is captured,
truncated at 4 KB by default, and run through a redactor before being
returned (Bearer JWT, sk-…, AKIA…, hex tokens).

## Audit log

Every `read_secret` and `inject_template` call appends one JSONL line
to `OP_AUDIT_LOG_PATH` (default `./data/secrets-audit.jsonl`). Fields:
`ts`, `action`, `agent_id`, `session_id`, `op_reference` (or
`references`), `fingerprint_sha256_prefix`, `reveal_allowed`, `ok`,
plus per-action extras (`exit_code`, `stdout_total_bytes`, etc).
**Never** the actual secret value. Failures appending the log are
logged to stderr and do not block the tool — the secret was already
read; blocking would be worst-of-both-worlds.

`AGENT_ID` and `AGENT_SESSION_ID` are populated from env vars the
host injects when spawning the extension.

## Execution guidance

- Start with `status` when uncertain (validates bin + token).
- For "does secret X exist?" questions, use `read_secret` with reveal
  off; the fingerprint lets you confirm identity without exposure.
- For "give me my Gmail app password" questions, only proceed if
  `OP_ALLOW_REVEAL=true` is set AND the operator clearly authorized it
  in the current conversation. Otherwise return the fingerprint and
  ask the operator to turn reveal on if really needed.
- Never paste a revealed value into chat output, memory, or another
  tool call "for future reference" — each revealed value lives exactly
  as long as the single tool_result that carries it should live.
- If `-32040`/`-32041` → wiring issue, not an LLM error; tell the user
  the operator needs to configure the extension.
- If `-32042` stderr says "token expired" or "unauthorized" → ask the
  operator to rotate the service-account token.

## Alternatives

- **Docker secrets** — already used for bootstrap (the agent needs its
  own 1P token somewhere). Good for "constant" secrets that never
  change per-request. 1Password is for runtime pulls.
- **env vars** — fine for deployment-time config; terrible for rotating
  credentials. Use 1Password when rotation matters.
- **Hashicorp Vault** — similar model; not implemented here.
