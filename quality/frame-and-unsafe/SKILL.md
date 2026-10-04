---
name: frame-and-unsafe
description: Where unsafe is permitted in this workspace and what every unsafe block owes the reader. Use when writing or reviewing an unsafe block, adding a crate to the workspace, touching a Cargo.toml lints table, or considering code that would need unsafe outside abi, ring or kernel.
---

# The frame

`unsafe` is permitted in `abi/`, `ring/` and `kernel/`. Nowhere else. RFC 0001.

This is not review culture; it is compiler-enforced. The workspace sets
`unsafe_code = "forbid"` and exactly three crates override it to `allow`. A
crate that drops or weakens `[lints] workspace = true` is making a visible diff
in its own `Cargo.toml`, and that diff is the thing to catch.

`cargo xtask lint-unsafe` is the textual backstop for cases the compiler cannot
see, such as a new crate not yet in the workspace.

## Writing an unsafe block

Two clippy lints are denied workspace-wide, and they define the shape:

- `undocumented_unsafe_blocks` — every block carries a `// SAFETY:` comment.
- `multiple_unsafe_ops_per_block` — one operation per block, so the comment has
  exactly one obligation to discharge.

A `// SAFETY:` comment that restates the operation is not a comment. It names
the precondition of the function being called and says what in the surrounding
code establishes it — an invariant, a prior check, a type that cannot be
constructed otherwise. If you cannot name what establishes it, the block is
unsound and the comment was about to hide that.

Public `unsafe fn` carries a `# Safety` section stating what the caller must
guarantee (`missing_safety_doc` is denied). The `# Safety` section and the
`// SAFETY:` comment at the call site are two halves of one sentence.

## If you need unsafe outside the frame

You need a different design, or an RFC. In that order.

The usual resolutions: the operation belongs behind a safe wrapper in `ring/`;
the data crossing the boundary belongs in `abi/` as a `repr(C)` type with a
validating constructor; or the capability belongs in `f_env::Env`. Widening the
frame is a decision, and RFC 0001 sets its own reversal condition — the unsafe
percentage passing 10%.

## On trust boundaries

Everything in `abi/` crosses one. An `unsafe` block that trusts a value which
arrived from the other side of a ring is the highest-severity finding this
repository has, because the type system stops helping exactly there. Validate at
the boundary, in safe code, and let the `unsafe` operate only on values that
have already been checked.
