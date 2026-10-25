---
name: encrypt-api-keys
description: >
  This skill covers AES-256-GCM encryption for provider API keys.
  Trigger: Load this skill when handling crypto operations for API keys.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: medium
  token_estimate: 350
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# encrypt-api-keys

This skill covers AES-256-GCM encryption for provider API keys.

**Trigger**: Load this skill when handling crypto operations for API keys.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Derive user key | `derive_user_key` |
| Encrypt API key | `encrypt_key` |

## Critical Patterns (Summary)
- **Derive User Key**: Generate a secure key for user-specific encryption.
- **Encrypt API Key**: Securely encrypt an API key using AES-256-GCM.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Derive User Key

Generate a secure key for user-specific encryption using the `derive_user_key` function.

```python
from apps.server.app.services.crypto import derive_user_key

user_key = derive_user_key(user_id="example_user")
```

### Encrypt API Key

Securely encrypt an API key using AES-256-GCM with the `encrypt_key` function.

```python
from apps.server.app.services.crypto import encrypt_key

encrypted_key = encrypt_key(api_key="my_secret_api_key", user_key=user_key)
```

## When to Use

- When you need to securely store API keys for different providers.
- When encrypting sensitive information before transmission.

## Commands

```bash
docker-compose run app python apps/server/app/main.py
```

## Anti-Patterns

### Don't: Hardcode API Keys

Hardcoding API keys in the source code exposes them to security risks.

```python
# BAD
api_key = "my_secret_api_key"
```
<!-- L3:END -->