---
name: ovstorage-contributor-modify-authz-layer
description: Use when changing or reviewing the built-in authentication and authorization Layer or its TOML policy engine.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, authz, layer, policy]
tools: [Read, Write, Bash]
compatibility: Requires an ovstorage checkout and Rust toolchain. No external credentials are required for unit tests.
---

# Modify the authorization Layer

## Goal

Change the built-in `builtin-auth` Layer or its pure policy engine without
weakening the host's fail-closed behavior.

## Workflow

1. Read [`docs/public/authz-policy/README.md`](../../docs/public/authz-policy/README.md).
2. Route Layer composition, authentication, and request gating changes to
   `ovstorage-remote/ovstorage-authz-layer/`.
3. Route TOML parsing, operation mapping, rule precedence, and list filtering
   changes to `ovstorage-remote/ovstorage-authz-policy/`.
4. Keep transport-derived identity values in
   `ovstorage-remote/ovstorage-authz-context/`.
5. Preserve deny-by-default parsing, atomic policy replacement, and
   authorization above caches in the Stack.
6. Add focused tests in the owning crate, then run:

```bash
cargo test -p ovstorage-authz-policy
cargo test -p ovstorage-authz-layer
make verify
```

## Boundaries

- Listener auth accepts `builtin-auth` and loaded storage Layer wrappers whose
  descriptor declares `auth_capable = true`. Missing, unknown, non-wrapper,
  and non-auth-capable kinds fail startup.
- The policy document's `plugin = "ovstorage-authz-toml"` field is a retained
  schema discriminator, not a cdylib selection mechanism.
- Do not introduce a parallel authorization ABI. External auth wrappers use
  the storage Layer contract, own their config schema, and do not receive the
  built-in typed policy hot-reload operation. Broker SIGHUP reconstructs them
  from config as part of the fresh broker.
