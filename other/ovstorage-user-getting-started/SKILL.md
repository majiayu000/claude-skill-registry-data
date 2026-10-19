---
name: ovstorage-user-getting-started
description: Use when starting a new ovstorage session or recovering from NoRoute, NotConfigured, or Unsupported errors by inspecting configured backends and routes.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, onboarding, discovery]
tools: [Read]
compatibility: Requires ovstorage MCP tools or equivalent library calls.
---

# Getting Started: Discover What's Configured

**Goal:** Find out what ovstorage knows about — versions, declared
backend layers, configured connections, addressable prefixes — before
attempting any real work.

**When to use this:** As the first call in any new session, or when an
operation has failed with `NoRoute` / `NotConfigured` / `Unsupported`
and you need to understand what's actually available. `NoRoute` means
no backend serves this address and no anonymous fallback is granted for
its scheme.

## Recipe

Call `ovstorage_doctor` with no arguments.

```json
{
  "tool": "ovstorage_doctor",
  "arguments": {}
}
```

## What success looks like

The envelope's `result` field is a `DoctorReport`:

```json
{
  "v": "0.1",
  "ok": true,
  "operation": "ovstorage_doctor",
  "result": {
    "ovstorage_version": "0.1.0",
    "backend_kinds": [
      {"kind": "file", "display_name": "Local files", "supports_runtime_add": true},
      {"kind": "s3", "display_name": "Amazon S3", "supports_runtime_add": true}
    ],
    "connections": [
      {
        "id": "01H...",
        "backend_kind": "s3",
        "display_name": "my-bucket",
        "addresses": ["s3://my-bucket/"],
        "auth_state_kind": "Authenticated"
      }
    ],
    "address_roots": [
      {"address": "s3://my-bucket/", "backend_kind": "s3", "display_name": null, "visibility": "Visible", "connection_id": "01H...", "user_metadata": {}}
    ],
    "aliases": []
  }
}
```

## How to read the report

- **`backend_kinds`** — the backend layers **this** stack was built with, not a catalogue of what the library could construct. A stack whose config declares one layer reports one kind, and a stack with no layers reports none, however much the library is capable of. A missing kind means the config does not declare a layer for it: fix the config first. The `file` backend is built into the library and needs no plugin artifact — it still appears here only once a `file` layer is declared. Every other kind additionally needs its plugin loaded.
- **`connections`** — backends the user has configured. `Authenticated` and `Anonymous` connections are ready to use; `AwaitingAuth`, `AuthFailed`, or other non-ready states mean operations against that connection's addresses need credentials or configuration work first.
- **`address_roots`** — the URL prefixes that resolve. If you're about to operate on an address, confirm a prefix here matches it. A root spelled as a bare scheme — `s3:///`, `gs:///` or `azure:///` — with `"visibility": "Hidden"`, `"connection_id": null` and `"user_metadata": {"org.omniverse.ovstorage/scheme-fallback": "anonymous"}` is the sign this host grants an anonymous fallback for that scheme: a public address on it that no connection serves is still readable, anonymously and read-only, while an unrouted address on any other scheme answers `NoRoute`. A hostless root without that marker is an ordinary root, not a fallback.
- **`aliases`** — convenience name remappings; safe to ignore unless you're working with the alias surface specifically.

## When things go wrong

This call is essentially read-only library state — it doesn't usually fail. If you get an envelope with `ok: false`, the failure is in the MCP server itself (e.g., server can't start, plugin loading panicked at boot). The error message should explain.

## See also

- [ovstorage-user-handle-errors](../ovstorage-user-handle-errors/SKILL.md) — what to do when other tools error with `NoRoute` / `NotConfigured`; before concluding an `s3://` address is unroutable, check `address_roots` above for a hidden `s3:///` fallback root
- [`docs/public/agent/mcp-tools.md`](../../docs/public/agent/mcp-tools.md) — full `DoctorReport` shape
