---
name: licence-boundary
description: The third_party isolation rule, why the licence boundary and the isolation boundary are the same boundary, and what an import must satisfy. Use when adding or updating imported source, when writing anything that would call into third_party, and when adding a dependency to any Cargo.toml.
---

# The licence boundary

The permissive tree never imports `third_party/`. Imported code is reachable
only over a ring. `LICENSING.md`, RFC 0003.

`cargo xtask lint-licensing` checks two things: every file carries its SPDX
header, and no module in the permissive tree names `third_party`.

## Why the two boundaries coincide

Because one of them is checkable and the other is not. Nobody can grep for "is
this driver trustworthy", but everybody can grep for a module path. Making the
licence boundary and the isolation boundary the same boundary means the cheap
check enforces the expensive property, and a violation of either shows up as a
violation of both.

The consequence to keep in mind while designing: anything imported is on the far
side of a ring, so it gets a message interface, not a function call. If a design
wants a function call into imported code, the design is wrong before the licence
question is even reached.

## Adding an import

1. It lands in `third_party/<name>/`, verbatim, in its own commit that changes
   nothing else. The review of imported code is the review of that commit.
2. Its licence goes in `LICENSING.md` and its terms go in `deny.toml`. If
   `cargo deny` does not know about it, it is not imported yet.
3. The interface to it is a ring. Name the messages in the same change.
4. Every file this repository authors starts with
   `// SPDX-License-Identifier: Apache-2.0 OR MIT`. Files under `third_party/`
   keep their own headers untouched.

## Adding a dependency

`deny.toml` gates the licence and the advisory database. Neither gates *why*.
A dependency added for one function is a review finding: this is an operating
system, and every crate in the graph is code that has to build for a bare-metal
target and be defensible in a supply-chain question later. Prefer writing the
function.
