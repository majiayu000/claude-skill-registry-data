---
name: secret-sharing
description: |
  Share secrets securely using zKettle — a zero-knowledge, self-destructing secret sharing tool.
  Create, read, revoke, generate, and audit secrets via MCP tools. Secrets are encrypted client-side
  with AES-256-GCM; the server never sees plaintext. Use for credential sharing, API key rotation,
  temporary access grants, and secure dead drops.
allowed-tools: mcp__zkettle__create_secret mcp__zkettle__read_secret mcp__zkettle__revoke_secret mcp__zkettle__list_secrets mcp__zkettle__generate_secret
metadata:
  author: benderterminal
  version: "1.0.0"
---

# Secret Sharing with zKettle

Share passwords, API keys, tokens, certificates, and other sensitive data via self-destructing, one-time URLs. All encryption happens client-side — the server stores only ciphertext.

## Prerequisites

This skill requires a running zKettle MCP server. If zKettle is not installed or configured, see the [zKettle README](https://github.com/benderterminal/zkettle) for installation and MCP setup instructions. zKettle also offers a CLI, HTTP API, and Web UI — refer to the README if the MCP tools are insufficient for a particular workflow.

## How It Works

- Secrets are encrypted with AES-256-GCM on the client
- The decryption key lives in the URL fragment (`#key`) — never sent to the server
- Secrets auto-delete after a configurable view count or time limit
- The server is zero-knowledge: it stores only ciphertext and metadata

## Tools

### `create_secret`

Encrypt and store a secret, returning an expiring URL.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content` | string | no | — | Plaintext to encrypt (max 500KB). Visible in conversation context — use `file` instead for maximum security. |
| `file` | string | no | — | Read secret from this file path instead of `content`. Keeps plaintext out of conversation. |
| `views` | integer | no | `1` | Max views before auto-delete (1–100) |
| `minutes` | integer | no | `1440` | Minutes until expiry (1–43200) |

Provide exactly one of `content` or `file`. Returns `url` (with decryption key in fragment) and `delete_token`.

### `read_secret`

Decrypt a secret from a zKettle URL. **Consumes one view.**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | Full zKettle URL including the `#key` fragment |
| `file` | string | no | Write decrypted secret to this file path (0600 permissions) instead of returning it |
| `clipboard` | boolean | no | Copy to system clipboard instead of returning. Mutually exclusive with `file`. |

Returns decrypted plaintext by default, or a confirmation message when `file` or `clipboard` is used.

### `revoke_secret`

Permanently delete a secret before it expires.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | yes | Secret ID |
| `delete_token` | string | yes | Token returned by `create_secret` |

### `list_secrets`

List all active secrets (metadata only — no content or keys). Returns IDs, creation time, expiry, and remaining views.

### `generate_secret`

Generate a cryptographically random secret. Optionally encrypt and store it in one step.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `length` | integer | no | `32` | Length in characters (1–4096) |
| `charset` | string | no | `"alphanumeric"` | Character set: `alphanumeric`, `symbols`, `hex`, `base64url` |
| `create` | boolean | no | `false` | If true, encrypt and store the generated secret |
| `views` | integer | no | `1` | When `create=true`, max views (1–100) |
| `minutes` | integer | no | `1440` | When `create=true`, minutes until expiry (1–43200) |

Returns raw generated text, or `url` + `delete_token` when `create=true`.

## Defaults

- **1 view** if `views` is omitted (single-use)
- **1440 minutes** (24 hours) if `minutes` is omitted

## Limits

- **500KB** max plaintext per secret
- **100 views** max per secret
- **43200 minutes** (30 days) max TTL

## Secure Patterns

Plaintext secrets can appear in conversation context (tool inputs/outputs). Use these patterns to minimize exposure.

### Creating secrets — keep plaintext out of context

- `create_secret(file="/path/to/secret.txt")` — reads from file, plaintext never in tool call. Ask the user before deleting the source file afterward.
- `generate_secret(create=true)` — generates + encrypts in one step, plaintext never in response
- Prefer these over `create_secret(content="...")` which puts the raw value in conversation context

### Reading secrets — keep plaintext out of context

- `read_secret(url="...", file="/tmp/secret.txt")` — writes to file, returns confirmation only
- `read_secret(url="...", clipboard=true)` — copies to user's clipboard, returns confirmation only
- Subagents can read the file at the written path without the secret entering conversation context
- Default `read_secret(url="...")` returns plaintext directly into conversation — warn the user before using this form
- **File cleanup**: Files written by `file` do NOT self-destruct. After the secret has been used, ask the user for permission to delete the file, then remove it. Do not leave secret files on disk.

## Common Workflows

### Share a credential with someone

```
1. create_secret(file="/path/to/credential.txt", views=1, minutes=60)
   — or create_secret(content="the-password", views=1, minutes=60) if plaintext exposure is acceptable
2. Share the returned URL with the recipient
```

The secret vanishes after one view or 60 minutes, whichever comes first.

### Rotate an API key

```
1. generate_secret(create=true, length=48, charset="alphanumeric", views=2, minutes=240)
2. Share the URL with the team member who needs it
3. revoke_secret(id="old-secret-id", delete_token="old-token") to kill the old one
```

### Temporary access grant

```
1. create_secret(content="temp-token", views=1, minutes=30)
2. Send the one-time link — expires after a single view or 30 minutes
```

### Audit active secrets

```
1. list_secrets() — review what's still live
2. revoke_secret() on any that are no longer needed
```

### Read a shared secret

```
1. Receive a zKettle URL from a human or another agent
2. read_secret(url="https://example.com/s/abc123#key", file="/tmp/secret.txt")
   — or read_secret(url="...", clipboard=true) to copy to clipboard
   — or read_secret(url="...") to return plaintext directly (enters conversation context)
3. Use the decrypted content
```

## Agent-to-Agent Secret Sharing

zKettle is well-suited for secure coordination between agents — subagents, teammates, or any multi-agent workflow where credentials need to move between contexts without leaking into conversation logs.

### When to use

- A subagent needs a credential to complete its task (e.g., an engineer agent needs a deploy token)
- Agents on a team need to pass secrets to each other without the lead's context window seeing the plaintext
- A workflow generates a credential in one agent and consumes it in another

### Pattern: file-based handoff (recommended)

The creating agent writes the secret to zKettle, passes only the URL to the receiving agent. The receiving agent reads it to a file, uses it, then cleans up.

```
Agent A (creator):
1. create_secret(content="deploy-token-xyz", views=1, minutes=30)
2. Send the URL to Agent B via message

Agent B (consumer):
1. read_secret(url="...", file="/tmp/deploy-token.txt")
2. Use the file contents for the task
3. Delete /tmp/deploy-token.txt when done
```

The plaintext never enters either agent's conversation context — Agent A sees only the URL and delete token, Agent B sees only a confirmation message.

### Pattern: generated credential handoff

When the secret doesn't need to be a specific value (e.g., a new API key, a temporary password):

```
Agent A:
1. generate_secret(create=true, length=48, views=2, minutes=60)
2. Send the URL to Agent B and keep the delete_token
3. After Agent B confirms usage, revoke_secret() to clean up
```

### Guidelines

- Set `views` to the exact number of agents that need to read the secret — no more
- Use short TTLs (`minutes`) appropriate to the workflow duration
- The creating agent should retain the `delete_token` and revoke after the workflow completes
- Prefer `file` on the read side so plaintext stays out of all conversation contexts
- The receiving agent is responsible for deleting the local file after use

## Gotchas

- **URL fragments matter**: The `#key` portion contains the decryption key. Some tools strip URL fragments — always ensure the full URL (including `#key`) is passed to `read_secret`.
- **Reading consumes a view**: If the secret has only 1 view remaining, `read_secret` permanently destroys it. Warn the user before reading single-view secrets.
- **`list_secrets` is metadata only**: It returns IDs, creation time, expiry, and remaining views — never content or decryption keys.
- **Conversation exposure**: Using `create_secret(content="...")` puts the plaintext in the conversation context. Use `generate_secret(create=true)` when the user doesn't need a specific value.
