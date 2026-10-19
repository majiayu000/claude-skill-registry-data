---
name: ovstorage-contributor-author-storage-plugin
description: Use when adding or reviewing a storage backend plugin for ovstorage.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, plugin, storage]
tools: [Read, Bash]
compatibility: Requires an ovstorage checkout, Rust toolchain, and storage plugin ABI docs. Backend SDK credentials are user-supplied when applicable.
---

# Author a Storage Plugin

## Goal

Implement a backend plugin that advertises truthful capabilities, streams bytes
without buffering whole objects, maps errors into ovstorage codes, and passes
the plugin conformance harness.

## Recipe

1. Start with [`docs/public/plugin-development/README.md`](../../docs/public/plugin-development/README.md)
   for the shared C ABI, manifest, loader, and build loop.
2. Use [`docs/public/plugin-storage/README.md`](../../docs/public/plugin-storage/README.md)
   for the storage-specific `Factory` and `Backend` contract.
3. Mirror a small reference plugin such as
   [`ovstorage-plugin-http`](../../ovstorage-core/ovstorage-plugin-http/README.md)
   before introducing vendor SDK complexity. (The `file` backend is
   built into the library, not a plugin crate, so it is not a template
   for a loadable plugin.)
4. Set capability bits only for operations the backend actually honors.
5. Add streaming-invariant coverage for any streaming read or write path.
6. Run `make verify` before merge.

## Review Checks

- Manifest name/version come from Cargo package metadata.
- Secrets only travel through credential fields or credential providers.
- Write success means durable backend state is visible to a following read.
- Unsupported operations return `Unsupported` and do not advertise the matching
  capability.
