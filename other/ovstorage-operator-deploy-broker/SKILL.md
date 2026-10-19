---
name: ovstorage-operator-deploy-broker
description: Use when deploying the ovstorage-broker daemon with listener authentication, authorization policy, TLS, and storage connections.
license: CC-BY-4.0
version: "0.2.0"
author: NVIDIA Omniverse
tags: [ovstorage, broker, deployment]
tools: [Read, Write, Bash]
compatibility: Requires operator access to deployment hosts or manifests, TLS material, authentication configuration, and approved secret-management paths.
---

# Deploy the ovstorage Broker

## Goal

Stand up a single-tenant `ovstorage-broker` with an explicit listener trust
boundary, the built-in auth Layer, and the required storage Layer graph.

## Recipe

1. Read the [broker operator guide](../../docs/public/broker-operator/README.md).
2. Build the distribution with `make dist`.
3. Configure every listener with either `auth = "anonymous"` for an intentional
   trusted-local boundary or `[listener.auth] kind = "builtin-auth"` plus its
   authentication and policy configuration. Missing auth fails startup.
4. Configure TLS for public TCP listeners and provide all three JWT settings
   (`jwt_issuer`, `jwt_audience`, and `jwt_jwks_url`) together.
5. Configure the `[ovstorage]` Layer graph and `[[connections]]` used by the
   broker. Restrict `OVSTORAGE_PLUGIN_DIR` to trusted storage-plugin paths.
6. Start `ovstorage-broker --config /etc/ovstorage/broker.toml` under a
   dedicated service account.
7. Configure SIGHUP reload on Unix and drain-first SIGTERM/SIGINT shutdown.
   Windows configuration changes require a restart.

## Checks

- The listener has an explicit auth mode and public TCP uses TLS.
- `builtin-auth` policy is deny-by-default and covers every intended operation.
- Plugin directories contain only trusted Layer plugins.
- State and cache directories are broker-owned and appropriately permissioned.
- Unknown auth kinds and malformed policy fail before the listener starts.

Run the build commands from the storage library component directory.
