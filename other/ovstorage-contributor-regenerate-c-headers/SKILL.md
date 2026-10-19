---
name: ovstorage-contributor-regenerate-c-headers
description: Use when Rust changes affect the ovstorage plugin ABI header and the checked-in generated copies must be refreshed.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, c-abi, headers]
tools: [Read, Bash]
compatibility: Requires an ovstorage checkout and the Rust toolchain used by make regenerate-headers.
---

# Regenerate C Headers

## Goal

Keep the checked-in copies of the plugin ABI header synchronized with the
Rust source they are generated from.

## Scope

Only `ovstorage_plugin.h` is generated, from the `ovstorage-plugin` crate.
It has to be: plugins are prebuilt cdylibs loaded at runtime, so host and
plugin compile separately and must agree on struct layout.

`ovstorage.h` is NOT generated. The C application API ships as source, so
consumers compile that header together with the implementation it declares
and there is no binary boundary to freeze. Edit it directly, alongside
`ovstorage-c-source/src`; the link-completeness gate in
`make c-source-examples` is what holds the two in agreement.

## Recipe

1. Make the ABI-affecting Rust change under `ovstorage-core/ovstorage-plugin`.
2. Run `make regenerate-headers`.
3. Inspect the diff under
   [`ovstorage-plugin/include`](../../ovstorage-core/ovstorage-plugin/include/)
   and its copy in
   [`ovstorage-c-source/include`](../../ovstorage-c-source/include/).
4. Run `make verify-headers-clean`.
5. Commit the Rust source and regenerated headers together.

## References

- [C/C++ source distribution](../../ovstorage-c-source/README.md) for
  C ABI stability rules.
