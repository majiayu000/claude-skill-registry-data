---
name: op
description: Manage 1Password secrets. Use when user wants to list, get, or read passwords, OTP codes, API keys, or other secrets from 1Password.
user-invocable: true
argument-hint: "[action or natural language request]"
allowed-tools: Bash
---

# 1Password CLI (`op`)

Manage secrets in 1Password using the `op` command. Authenticated via service account.

## User Request

$ARGUMENTS

## Commands Reference

**Important:** Service accounts require `--vault` on every command. Before running any item commands, discover the available vault name first:

```bash
op vault list --format=json
```

Then use the vault name from the response in all subsequent commands.

### List Items

```bash
# List all items in vault
op item list --vault "VAULT_NAME" --format=json

# Long format (with categories, dates)
op item list --vault "VAULT_NAME" --long --format=json

# Filter by category
op item list --vault "VAULT_NAME" --categories Login --format=json
op item list --vault "VAULT_NAME" --categories "API Credential" --format=json

# Filter by tags
op item list --vault "VAULT_NAME" --tags production --format=json

# Filter favorites only
op item list --vault "VAULT_NAME" --favorite --format=json
```

### Get Item Details

```bash
# Full item details
op item get "Item Title" --vault "VAULT_NAME" --format=json

# Get OTP (one-time password / 2FA code)
op item get "Item Title" --vault "VAULT_NAME" --otp

# Get specific fields
op item get "Item Title" --vault "VAULT_NAME" --fields label=username --format=json
op item get "Item Title" --vault "VAULT_NAME" --fields label=password --format=json
op item get "Item Title" --vault "VAULT_NAME" --fields label=username,label=password --format=json

# Get fields by type
op item get "Item Title" --vault "VAULT_NAME" --fields type=CONCEALED --format=json
```

### Read Individual Secret

```bash
# Read a specific field value directly
op read "op://VAULT_NAME/Item Title/username"
op read "op://VAULT_NAME/Item Title/password"
op read "op://VAULT_NAME/Item Title/Section Name/field"
```

### List Vaults

```bash
op vault list --format=json
```

## JSON Response Structures

**`op vault list --format=json`:**
```json
[
  {"id": "abc123...", "name": "My Vault", "content_version": 42}
]
```

**`op item list --format=json`:**
```json
[
  {
    "id": "abc123...",
    "title": "Example Service",
    "version": 1,
    "vault": {"id": "xyz...", "name": "My Vault"},
    "category": "LOGIN",
    "last_edited_by": "...",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-02T00:00:00Z",
    "additional_information": "user@example.com",
    "urls": [{"primary": true, "href": "https://example.com"}]
  }
]
```

**`op item get --format=json`:**
```json
{
  "id": "abc123...",
  "title": "Example Service",
  "category": "LOGIN",
  "vault": {"id": "xyz...", "name": "My Vault"},
  "fields": [
    {
      "id": "username",
      "type": "STRING",
      "purpose": "USERNAME",
      "label": "email",
      "value": "user@example.com",
      "reference": "op://My Vault/Example Service/email"
    },
    {
      "id": "password",
      "type": "CONCEALED",
      "purpose": "PASSWORD",
      "label": "password",
      "value": "secret_value",
      "reference": "op://My Vault/Example Service/password"
    },
    {
      "id": "TOTP_xxx",
      "type": "OTP",
      "label": "one-time password",
      "value": "otpauth://totp/...",
      "totp": "123456"
    }
  ],
  "urls": [{"primary": true, "href": "https://example.com"}]
}
```

**`op item get --otp`:**
Returns just the 6-digit TOTP code as plain text (e.g., `182448`).

**`op item get --fields --format=json`:**
```json
[
  {"id": "username", "type": "STRING", "label": "email", "value": "user@example.com"},
  {"id": "password", "type": "CONCEALED", "label": "password", "value": "secret_value"}
]
```

## Important Notes

- **Service account requires `--vault`** — always discover vault name via `op vault list` first, then use it in all commands
- **`--otp` returns plain text** — do not combine with `--format=json`
- **OTP field in JSON** — when getting full item, the current TOTP code is in the `totp` key of OTP-type fields
- **Categories:** Login, Password, API Credential, Secure Note, Database, SSH Key, Credit Card, Identity, Document, Server, Software License

## Instructions

1. Parse the user's natural language request to determine what they need
2. **First, run `op vault list --format=json`** to discover the available vault name(s)
3. Determine the appropriate `op` command, using the discovered vault name
4. **Always use `--format=json`** except for `--otp` (which returns plain text)
5. Execute the command via Bash
6. Parse the JSON response and present results clearly to the user
7. For OTP requests, just return the code prominently
8. For credential requests, format as a clear key-value list
9. **Never log or echo secrets unnecessarily** — only show what was requested

If the request is ambiguous, ask for clarification.
