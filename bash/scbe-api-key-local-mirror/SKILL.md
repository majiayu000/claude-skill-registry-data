---
name: scbe-api-key-local-mirror
description: Securely mirror API keys from environment or prompt into a local Windows DPAPI-encrypted token store, then resolve them back into runtime env vars for terminal workflows. Use when users ask for quick API key access, local backup key storage, tokenized secret indexing, or safe secret handoff for services like World Anvil.
---

# SCBE API Key Local Mirror

Maintain a second local destination for secrets without plaintext storage.

## Quick Start

1. Run health check:

```bash
python C:/Users/issda/.codex/skills/scbe-api-key-local-mirror/scripts/key_mirror.py doctor
```

2. Store World Anvil key from existing env var:

```bash
python C:/Users/issda/.codex/skills/scbe-api-key-local-mirror/scripts/key_mirror.py store --service world_anvil --env WORLD_ANVIL_API_KEY
```

3. Resolve into current shell variable:

```bash
python C:/Users/issda/.codex/skills/scbe-api-key-local-mirror/scripts/key_mirror.py resolve --service world_anvil --env-out WORLD_ANVIL_API_KEY
```

4. List mirrored keys:

```bash
python C:/Users/issda/.codex/skills/scbe-api-key-local-mirror/scripts/key_mirror.py list
```

## Workflow

1. Prefer `--env` input to avoid putting raw keys in shell history.
2. Store with service name normalization (`world_anvil`, `youtube`, `buffer`, etc.).
3. Use `resolve --env-out` during runtime just-in-time.
4. Keep masked output by default; use `--raw` only if absolutely required.

## Invariants

- Never print full key values unless explicitly requested (`--raw`).
- Never commit vault files to git.
- Keep keys encrypted via Windows DPAPI at rest.
- Keep source-traceable metadata (token_id + fingerprint).

## Resource Guide

- `scripts/key_mirror.py`: DPAPI store/list/resolve utility.
- `references/world-anvil-usage.md`: World Anvil access lane using mirrored keys.
