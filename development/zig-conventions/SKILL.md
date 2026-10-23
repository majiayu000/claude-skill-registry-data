---
name: zig-conventions
description: "Use when writing or reviewing Zig: names of types, namespaces, functions and files, redundancy in names, layout, and doc comments that state invariants. Pinned to a development version of the language."
---

# zig-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames naming and layout of Zig code.

**Freshness stamp**: first read on 2026-10-02 from the compiler source tree at commit `738d2be9` (a 0.16.0
development tree); re-checked on 2026-10-20 against the published 0.17.0 language reference (Style Guide and
Source Encoding sections), which corrected two points. The language changes between versions; before applying
this block, check the style guide of the version the project builds with (`skills/source-freshness`).
Status 🟡; only those two sections were read, so memory management, error handling, comptime and the build
system carry no rule here (see `skills/zig-pitfalls`).

## When
As soon as Zig code is written or modified, during `code` (6).

## Steps
Read [`references/01-style.md`](./references/01-style.md) (names, layout, doc comments). It is the only
section.

## Output / checkpoint
Code formatted by the language's own formatter, which implements the layout recommendations, and names that
follow §1. Checked by `review` (8).

## Guardrails
No comments in the code produced; doc comments only where §1.8 asks, on declarations others use. Where a
convention is already established in the project or the platform (a constant copied from a system header),
follow it.

## Origin
Rewritten from the MIT-licensed compiler repository's language reference, with pinned commit in
[`references/origin.md`](./references/origin.md).
