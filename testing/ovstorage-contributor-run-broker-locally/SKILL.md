---
name: ovstorage-contributor-run-broker-locally
description: Use when starting ovstorage-broker locally for development or integration testing with the current Stack and listener-auth configuration.
license: CC-BY-4.0
version: "0.2.0"
author: NVIDIA Omniverse
tags: [ovstorage, broker, development]
tools: [Read, Bash]
compatibility: Requires an ovstorage checkout, built storage plugins, local networking, and optional local test credentials supplied by the user.
---

# Run the Broker Locally

## Goal

Start a local broker with an explicit trust boundary, the built-in auth Layer,
and a file connection for development or integration testing.

## Recipe

1. Read the current configuration skeleton in the
   [broker operator guide](../../docs/public/broker-operator/README.md#configuration-shape).
2. Build binaries and storage plugins with `make dist`.
3. Create a local config with a UDS listener, explicit auth configuration, an
   `[ovstorage]` Layer graph, and a file `[[connections]]` entry. For a
   trusted-local smoke test, `auth = "anonymous"` is the smallest explicit
   choice; use `kind = "builtin-auth"` when testing policy behavior.
4. Create the file connection's root directory.
5. Start the daemon:

   ```sh
   OVSTORAGE_PLUGIN_DIR="$(pwd)/dist/plugins" \
     ./dist/bin/ovstorage-broker --config "$XDG_RUNTIME_DIR/broker.toml"
   ```

6. Exercise it through a `broker-client` connection or the broker integration
   tests under `ovstorage-remote/ovstorage-broker/tests/`.
7. Send SIGHUP on Unix after config edits. Send SIGTERM to exercise drain-first
   shutdown.

## Common mistakes

- Omitting listener auth; current hosts fail startup instead of selecting an
  implicit mode.
- Setting TLS on UDS or peer credentials on TCP.
- Pointing `OVSTORAGE_PLUGIN_DIR` at an untrusted or incomplete directory.
- Using the retained policy `plugin` field as though it selected a cdylib.
- Editing the vendored `ovstorage-services/` subtree for broker-only work.

## References

- [Broker operator guide](../../docs/public/broker-operator/README.md)
- [Broker-client plugin](../../docs/public/plugin-storage/plugin-broker.md)
- [Authorization policy](../../docs/public/authz-policy/README.md)
- [Pre-merge verification](../ovstorage-contributor-verify-before-merge/SKILL.md)
