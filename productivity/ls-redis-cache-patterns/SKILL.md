---
name: ls-redis-cache-patterns
description: Guide Redis cache and data-structure patterns. Use for caching, semantic
  cache, search, clustering, connections, observability, and security.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/redis/agent-skills
    source_path: skills/redis-core/SKILL.md
    source_commit: 3d6f25505ea2adff4dd62d5a0e7f4a5b076fa047
    source_ref: main
    source_sha256: 7ab1000e7a1548c4f82179ea1d5a57ced43851e6a924ac647cecd822015b81a7
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Redis Cache Patterns

Use this skill when working on Redis cache patterns tasks.

## Workflow

- Choose cache-aside, write-through, write-behind, pub/sub, stream, search, or semantic-cache pattern based on consistency needs.
- Set TTLs, key namespaces, serialization, invalidation, connection pooling, and memory limits deliberately.
- Validate auth/TLS, eviction behavior, stampede protection, and operational metrics before production use.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/redis/agent-skills`
- Ref: `main` at `3d6f25505ea2adff4dd62d5a0e7f4a5b076fa047`
- Source path: `skills/redis-core/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `7ab1000e7a1548c4f82179ea1d5a57ced43851e6a924ac647cecd822015b81a7`
