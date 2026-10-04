---
name: vault
description: Read secrets and policies from HashiCorp Vault
activation_keywords: [vault, secret, hashicorp, kv, token, policy]
execution_mode: server
---

# Vault Skill

Provides read-only HashiCorp Vault operations via HTTP API:
- List KV secrets engines and paths
- Read secrets at a given path
- List auth methods
- List and read policies
- Check Vault status/seal state

Use `builtin_vault` tool with fields:
- `operation`: one of "status", "list_secrets", "read_secret", "list_auth", "list_policies", "read_policy"
- `path`: secret path (required for list_secrets/read_secret)
- `vault_url`: Vault server URL (default: http://127.0.0.1:8200)
- `token`: Vault token (from VAULT_TOKEN env var if not provided)
- `engine`: KV secrets engine name (default: "secret")

Note: All operations are read-only.
The token is used only for this request and never logged.
