---
name: generate
description: Generate random values (UUID, password, API key, hex string, nanoid) instead of fabricating them inline. Use whenever a task needs any random-looking value.
---

# Generate Random Values

Never type a fake-looking UUID, password, or key by hand — always generate
a genuinely random one and use it. Fabricated "looks random" strings are
not random and can collide or look suspicious in review.

## UUID

```bash
python3 -c "import uuid; print(uuid.uuid4())"
```

## Password / API-key-shaped secret

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Hex string (e.g. for a key ID)

```bash
python3 -c "import secrets; print(secrets.token_hex(16))"
```

## Rule

- Never hardcode placeholder UUIDs like
  `00000000-0000-0000-0000-000000000001`.
- Never invent random-looking strings like `aB3xK9m2...` by typing them.
- Never hardcode placeholder secrets like `sk-test-123`.
- Generated secrets that need to be real (not test fixtures) still go
  through your project's secret store per `.claude/rules/env-secrets.md` —
  generating the value and persisting it insecurely are two different
  steps.
