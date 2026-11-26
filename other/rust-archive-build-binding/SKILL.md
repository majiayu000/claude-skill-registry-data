---
name: rust-archive-build-binding
description: "Prevent stale Cargo artifacts when a source archive is restored over a reused Rust target directory. Use for reproducible benchmark comparisons and for moving source archives between machines."
---

# Roschtchlämmerli (rust-archive-build-binding)

Bind the binary actually tested to the intended source, features, toolchain and flags.

Cargo commonly checks source modification times against dependency information.
An archive can restore different source with older timestamps and leave an
incorrectly reusable artifact. A clean source hash alone does not establish
which source produced the executable. See Cargo's
[fingerprint documentation](https://doc.rust-lang.org/stable/nightly-rustc/cargo/compiler/fingerprint/index.html).

When reusing a target directory across archived revisions:

1. Freeze source/archive and patch hashes, toolchain, feature selection and
   compiler flags before building. Keep benchmark binaries outside `target`.
2. Restore into an owned source tree with fresh modification times, for example
   `tar -xmzf source.tar.gz -C owned-checkout`. Check for obsolete files not in
   the archive; extraction does not remove them. Preserve other workers' trees.
3. Confirm the affected crates rebuild. If source and compiler diagnostics
   disagree, inspect Cargo fingerprints and mtimes before changing correct
   source. Use a clean target when the binding remains uncertain.
4. Save the successful build log and hash each copied executable. Freeze those
   hashes through correctness checks and timed runs. Compare both arms with
   identical flags and features; build/check/test artifacts are not interchangeable.
5. Exclude results from a build whose source binding is unresolved. Rebuild and
   rerun the necessary gates after repair; a later successful build does not
   retroactively validate earlier results.

For source archives crossing case-sensitive filesystems or containing Git symlinks,
read [references/archive-transfer.md](references/archive-transfer.md) before extraction.

For cold multi-role builds under nested time limits, read
[references/cold-build-timeouts.md](references/cold-build-timeouts.md) before sizing
the run or interpreting a timeout.
