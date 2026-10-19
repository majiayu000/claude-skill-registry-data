---
name: ovstorage-operator-configure-broker-policy
description: Use when authoring or rotating the broker's built-in authorization policy.
license: CC-BY-4.0
version: "0.2.0"
author: NVIDIA Omniverse
tags: [ovstorage, broker, authz]
tools: [Read, Write]
compatibility: Requires access to broker configuration files and the operator's approved policy source. Secrets and deployment details are user-supplied.
---

# Configure Broker Authorization Policy

## Goal

Configure the broker's `builtin-auth` Layer with deny-by-default TOML rules and
rotate those rules without weakening listener authentication.

## Recipe

1. Read the [authorization policy guide](../../docs/public/authz-policy/README.md)
   and the [broker auth Layer configuration](../../docs/public/broker-operator/README.md#auth-layer).
2. Configure an authenticated listener and its policy:

   ```toml
   [listener.auth]
   kind = "builtin-auth"

   [listener.auth.config]
   jwt_issuer = "https://login.example.com"
   jwt_audience = "ovstorage"
   jwt_jwks_url = "https://login.example.com/.well-known/jwks.json"

   [listener.auth.config.policy]

   [[listener.auth.config.policy.policy]]
   id = "team-read"
   effect = "allow"
   principal = "team-*"
   operations = ["read", "stat", "list"]
   prefix = "s3://corp-prod/team/"
   ```

3. Treat the optional policy-document key
   `plugin = "ovstorage-authz-toml"` as a retained schema discriminator. It
   does not load a cdylib, and no other value is supported.
4. Grant `copy` and `rename` through their primitive source and destination
   operations. Keep concrete prefixes segment-aligned.
5. Reload with SIGHUP on Unix. The broker validates a fresh configuration and
   atomically swaps the active host; invalid configuration leaves the current
   host running. Restart on Windows.
6. Confirm allow, deny, and policy-error metrics through
   `ovstorage_auth_decisions_total`.

## Boundaries

- Missing listener auth is a startup error.
- `auth = "anonymous"` is an explicit unauthenticated allow-all choice.
- This skill configures only `builtin-auth`. An auth-capable plugin wrapper owns
  its policy schema; broker SIGHUP reconstructs that wrapper from its verbatim
  config instead of invoking the built-in typed policy reload operation.
- The policy evaluator runs on every request; there is no decision cache or
  policy-epoch grace window.
