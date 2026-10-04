---
name: seam-probe
description: This skill should be used when testing or debugging an embedded-runtime boundary exposed through a dynamically loaded C-ABI library or Unix-domain socket, including requests to inspect exports, exercise FFI callbacks, send framed messages, reproduce seam crashes or hangs, fuzz a boundary, or correlate probe output with runtime logs. Not for ordinary APIs, HTTP/WebSocket services, static libraries, or generated bindings.
allowed-tools: Bash, Read, Grep, Write
---

# seam-probe

Use the bundled executable as the interface:

```bash
SEAM_PROBE="${CLAUDE_PLUGIN_ROOT}/bin/seam-probe"
```

The short name `seam-probe` below means `"$SEAM_PROBE"`. A direct skill install
does not include the plugin-level launcher, crate, or hook; install the binary
independently on PATH or use the full plugin.

## Pick the surface

- `seam-probe inspect` parses a library to discover exports without loading or
  executing it.
- `seam-probe ffi` loads a C-ABI dylib and drives lifecycle, callbacks, and
  input lanes described by a manifest.
- `seam-probe socket` sends NDJSON operations to a Unix-domain stream socket
  using the selected framing.
- `seam-probe vocab` prints the current stdin/stdout contract.

Run `seam-probe vocab` as preflight. If the launcher reports that the binary is
not built, verify `cargo` is available and build the pinned crate:

```bash
cargo build --release --locked \
  --manifest-path "${CLAUDE_PLUGIN_ROOT}/crate/Cargo.toml" \
  --target-dir "${CLAUDE_PLUGIN_DATA:-${XDG_CACHE_HOME:-$HOME/.cache}/seam-probe}/target"
```

Then rerun `seam-probe vocab`. If installed behavior disagrees with this skill,
inspect live help and request a plugin update rather than inventing flags.

## Investigate progressively

Start with the least assumed knowledge:

1. Inspect an unfamiliar library before writing symbol names into a manifest.
2. Read headers, binding metadata, or the host's loading code to recover the
   actual ABI and callback-field order.
3. For sockets, inspect the server and client framing code before guessing.
   Use a small probe only to distinguish remaining plausible framings.
4. Create the smallest manifest that exposes the behavior under test.
5. Reproduce one meaningful operation before expanding into a sequence or
   fuzzing campaign.

Use `references/discover-ffi-symbols.md` and
`references/discover-socket-protocol.md` only when discovery is needed.

## Read both sides of the seam

The probe emits machine-readable NDJSON on stdout and diagnostics on stderr.
The system under test may emit its own stderr, structured logs, panic report,
or crash artifact. Capture these streams separately and correlate them by
operation, sequence, session, and time.

A probe-side success means only that the command was accepted. Verify the
system-under-test postcondition and inspect its logs for delayed panics,
protocol errors, dropped callbacks, or incomplete shutdown. Use
`references/observability.md` for long-form correlation and hang triage.

## Do not force incompatible surfaces

The FFI mode expects a dynamically loadable library with an explicit C ABI and
one of the callback shapes supported by the manifest schema. Static archives,
Rust-only ABIs, UniFFI wire types, JNI, Python C extensions, Wasm imports,
gRPC, HTTP, and WebSocket are different interfaces. Use their generated
bindings or native protocol tools unless the probe is intentionally extended.

Socket mode supports the framing implemented by the installed binary. Check
`seam-probe vocab`, live help, and `references/framing-modes.md`; do not infer
framing from payload appearance.

## Safety invariants

Loading arbitrary native code can crash or corrupt the probe process:

- Do not unload a library while its threads or callbacks may still execute.
- Match callback layout and signatures exactly; an ABI mismatch is undefined
  behavior, not a recoverable validation error.
- Treat a sentinel abort as evidence that the manifest omitted or misdeclared a
  callback field, but only after verifying the callback struct has at most 64
  pointer fields.
- Run destructive fuzzing in an isolated process with bounded input, time, and
  artifact storage.
- Only lifecycle `stop` is grace-bounded. Start, lane, and op calls execute
  synchronously and can block indefinitely; supervise hang-prone probes with an
  external process timeout.

The supported manifest grammar and callback forms live in
`references/manifest-schema.md`; rationale and shutdown details live in
`references/safety-notes.md`.

## Contract references

- `seam-probe vocab` prints the authoritative input, output, lifecycle, and
  exit-code contract.
- `references/framing-modes.md` documents socket framing and its limitations.
- `references/manifest-schema.md` documents the FFI manifest.
- `references/observability.md` documents two-stream diagnosis.
- `references/discover-ffi-symbols.md` and
  `references/discover-socket-protocol.md` cover discovery.
- `references/safety-notes.md` covers ABI and process-lifetime hazards.

Prefer the executable's `vocab`, `inspect`, and `--help` interfaces over copied
examples. Report the exact command, manifest, input sequence, output events,
system logs, and resulting postcondition so the failure can be reproduced.
