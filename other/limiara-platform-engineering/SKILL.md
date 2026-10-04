---
name: limiara-platform-engineering
description: Use when working on Limiara's Rust platform kernel, plugin architecture, Contacts plugin, tenancy/RLS security, Wasm plugin sandboxing, service-plugin protocol, or React plugin shell.
---

# Limiara platform engineering skill

## When to use

Use this skill for changes that affect:

- platform kernel crates or app boundaries;
- native, Wasm, or external service plugin contracts;
- Contacts or future business-domain plugins;
- tenant isolation, PostgreSQL RLS, permissions, audit, outbox/inbox, entitlements, or identity/session flows;
- the React plugin shell or plugin UI contribution model;
- Docker Compose, Kubernetes packaging, CI, or operational runbooks.

## Required mental model

Limiara is a modular monolith first. The kernel is domain-neutral, while business domains are plugins. First-party native plugins may be statically linked, but they still use explicit manifests, permissions, capabilities, migrations, events, UI contributions, lifecycle state, and audit records.

## Implementation checklist

1. Inspect `IMPLEMENTATION_PLAN.md`, `README.md`, relevant ADRs, and plugin manifests before changing code.
2. Confirm whether the change belongs in the kernel, a plugin, runtime support, frontend shell, or operations/docs.
3. Preserve tenant isolation:
   - keep `tenant_id` on tenant-scoped data;
   - use forced RLS for PostgreSQL tables;
   - set `app.tenant_id` transaction-locally only after membership verification;
   - avoid cross-plugin private table access.
4. Preserve security boundaries:
   - permissions authorize users;
   - capabilities constrain plugins;
   - entitlements gate commercial features but never authorize users;
   - Wasm defaults deny filesystem, environment, secrets, database, and network access.
5. Emit audit records and outbox events in the same transaction as business mutations once persistence is wired.
6. Keep API errors stable and safe: use problem-style responses with machine-readable codes.
7. Update docs/ADRs when changing an architectural boundary.

## Validation commands

Run these when the environment has dependency access:

```bash
cargo build --workspace --locked
cargo fmt --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --locked
pnpm install --frozen-lockfile
pnpm typecheck
pnpm test
pnpm build
```

If the registry or proxy blocks dependency resolution, document the exact failure rather than claiming success.
