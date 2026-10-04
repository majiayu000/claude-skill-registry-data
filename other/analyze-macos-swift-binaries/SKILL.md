---
name: analyze-macos-swift-binaries
description: Inspect local macOS Swift .app bundles and Mach-O binaries, trace version-specific state or feature gates, build byte-exact patch manifests, create isolated patched copies, re-sign them, and verify runtime/UI acceptance. Use for macOS reverse engineering, expired offsets, Swift enum metadata, Universal Binary offset mapping, code-signing failures, or version-locked binary patch workflows.
---

# Analyze macOS Swift Binaries

Treat every build as a new sample. Preserve the original, establish exact
identity, locate current behavior from evidence, and encode changes in a
version-locked manifest before writing bytes.

## Workflow

1. Copy the target `.app` into an isolated working directory. Keep an untouched
   backup and record its SHA-256.
2. Inspect Bundle ID, Version, Build, executable name, architectures, size, and
   code-signing identity:

   ```bash
   node scripts/patch-app.mjs --inspect /path/to/Target.app
   ```

3. Read [references/workflow.md](references/workflow.md) before locating or
   changing logic. For Universal Binaries, calculate offsets per architecture
   slice; never reuse a virtual address as a file offset.
4. Build a manifest following
   [references/manifest-schema.md](references/manifest-schema.md). Include
   target metadata, original hash, exact offsets, and before/after bytes.
5. Create an isolated output:

   ```bash
   node scripts/patch-app.mjs \
     --manifest /path/to/patch.manifest.json \
     --source /path/to/Target.app \
     --output build/Target-research.app
   ```

6. Verify the output independently:

   ```bash
   node scripts/patch-app.mjs \
     --manifest /path/to/patch.manifest.json \
     --verify build/Target-research.app
   ```

7. Cold-launch the output. Validate both internal behavior and visible UI
   state. A feature working while the UI still reports a trial or locked state
   is an incomplete result.
8. Record commands, hashes, disassembly evidence, acceptance results, and
   rollback paths. Do not include proprietary application binaries in reports
   or repositories.

## Decision Rules

- Stop when Bundle ID, Version, Build, architecture set, size, SHA-256, or
  original bytes differ from the manifest.
- Prefer patching an isolated copy. Install only after the copy passes static,
  signature, cold-launch, and UI checks.
- Treat asynchronous refresh paths separately from startup paths. Search for
  every constructor or enum-tag write that can restore the old state.
- Inspect Swift runtime metadata before assuming an enum payload type.
- Verify from a terminated process. Hiding an app or reusing a resident process
  is not a cold start.
- Keep patches minimal and deterministic. Each patch entry must explain the
  state transition it changes.

## Outputs

Produce:

- a sample identity record;
- an evidence table mapping VA, slice offset, file offset, bytes, and purpose;
- a machine-readable patch manifest;
- an isolated, re-signed output;
- a verification report covering signature, runtime behavior, visible UI, and
  rollback;
- a reusable case study when the investigation is worth publishing.

Use the Mole 1.11.0 Build 96 manifest in this repository as a concrete example.
