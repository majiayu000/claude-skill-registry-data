---
name: evidence-hash-integrity
description: Use when any verdict, approval, or benchmark is pinned to a content hash — build the hash from an explicit manifest covering everything that produced the output (including the code), prove clean-state reproducibility, and re-pin with an exact logged mapping when the identity must move.
stacks: [python, any]
domains: [any]
phases: [dev, gate, release]
tags: [reproducibility, hashing, evidence, determinism, audit]
scope: kit
---
**When to use.** Before pinning any evidence identity, and again before a gate certifies it. *Why:*
every gate rejection in our phase close was a hash-soundness defect, not a product defect —
non-deterministic authoring order, then a directory glob folding stray test artifacts into the pin.

**Procedure.**
1. Enumerate hash inputs explicitly (or filter to a strict naming scheme); a `**/*` glob over a
   shared output directory WILL swallow incidental files. Include the pipeline code whose change can
   change the output (our Blender bridge changed pixels under an "unchanged" hash until hashed).
2. Make generation deterministic — sort every authoring loop by a stable key; iteration order of
   in-memory object graphs is not stable across runs.
3. Prove it: delete derived state → build → hash, twice; then once more in a pristine worktree of the
   pinned commit. "Reproduces in my workflow" usually means "my workflow deposits the same strays."
4. If the identity must change after verdicts exist: re-pin, and log the exact old-hash = new-inputs
   + named-deltas (each with its own hash) mapping. Never regenerate recorded verdicts, and never
   freeze code (e.g. suppress a lint) just to keep bytes stable — truth outranks hash stability.
5. **Done when:** an independent party can reconstruct the pinned hash bit-exact from the manifest +
   the log alone (our gate reviewer did exactly this before approving).

**Knowledge:** FIELD-KNOWLEDGE-NOTHOMEWRECKER.md §F2.
