---
name: rust-kernel-ffi
description: >-
  Build a Rust cdylib that a TypeScript/Bun runtime calls via koffi FFI, for a
  security kernel or enforcement core. Use when exposing Rust to Node/Bun
  (#[no_mangle] extern "C", JSON-over-C-string functions + a free fn), bridging a
  Rust crypto/capability primitive to a daemon, loading a .dylib/.so with koffi
  and degrading gracefully when it's absent, RustCrypto HMAC-SHA256 + constant-time
  compare, crate-type=["rlib","cdylib"], or panic-free fail-closed Rust across an
  FFI boundary. NOT for: WebAssembly (use wasm-bindgen), async-across-FFI, moving
  Rust structs/Vec/String across the boundary without a free fn, or pure Rust-only
  code with no FFI.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch
license: Apache-2.0
metadata:
  category: Systems & Runtime
  tags:
    - rust
    - ffi
    - cdylib
    - koffi
    - security-kernel
    - typescript-bun
  provenance:
    kind: first-party
    owners:
      - port-daddy
  pairs-with:
    - skill: rust-debugging-mastery
      reason: Debugging a segfault/SIGABRT at the FFI boundary needs the general Rust debugging toolkit this skill's failure-mode table only summarizes.
    - skill: rust-development-workflow
      reason: Day-to-day Rust authoring conventions (cargo workflow, error handling, testing) that this skill assumes but does not re-teach.
    - skill: rust-app-distribution
      reason: Shipping the built cdylib inside a distributed binary/installer is the packaging half of what build-core.sh only builds locally.
    - skill: gpui-rust-console
      reason: A gpui console process that also loads this cdylib shares the same koffi-loader-with-fallback pattern for its own native integrations.
  io-contract:
    kind: deliverable
    consumes:
      - kind: ffi-boundary-requirement
        format: markdown
      - kind: ffi-export-plan
        format: json
    produces:
      - kind: cdylib-koffi-implementation-guide
        format: markdown
      - kind: ffi-safety-audit
        format: json
---

# Rust Kernel FFI (cdylib ⇄ TypeScript via koffi)

**Activation boundary:** use this for the C ABI, ownership handoff, serialization, and koffi loader between a Rust `cdylib` and TypeScript/Bun. Use `rust-debugging-mastery` after a crash or loader failure, `advanced-rust-patterns` for the Rust-only public API, and `rust-development-workflow` for normal edit/test workflow.

Build a Rust shared library that a Node/Bun daemon calls over a C ABI. The canonical
in-repo template is **`core/harbor-card-rs/src/lib.rs`** (the `#[no_mangle] extern "C"`
exports) loaded by **`lib/arbiter.ts`** (the koffi loader with graceful fallback),
built by **`scripts/build-core.sh`**. Teach those patterns; don't reinvent them.

## The one rule that prevents most disasters

**Never let a panic unwind across an `extern "C"` boundary — it is undefined behavior.**
Either wrap every export body in `std::panic::catch_unwind` and return a sentinel
(`false`/null) on catch, or set `panic = "abort"` in `[profile.release]`. A security
kernel should do BOTH: abort in release, catch_unwind for defense in depth.

## Decision points

```
Returning a string/buffer to TS?
├── No  → return a primitive (bool / u64 / i32). No allocation, no free fn. Simplest.
└── Yes → CString::into_raw() to hand out + a matching #[no_mangle] free fn the TS
          caller MUST invoke (from_raw reclaims it). Forgetting the free fn = leak.

Crossing the boundary with structured data?
├── Marshal as JSON over `*const c_char` + `usize` len (harbor-card-rs pattern).
│   Validate: null ptr → sentinel; len==0 or len>BOUND → sentinel; from_utf8 → sentinel;
│   serde_json::from_str → sentinel. Five guards before any logic.
└── Never pass a Rust struct/enum directly (ABI is not C-stable). #[repr(C)] only for
    genuine C structs of primitives.

Security-critical compare (MAC/tag)?
├── Constant-time fold-XOR: `for i {acc |= a[i]^b[i]}; acc==0`. Never early-return.
└── Length differs → return false up front (length is not secret), then fold equal-length.

Dylib missing at runtime (source install / CI doesn't build it)?
└── Degrade gracefully: capture the load error, return null from the loader, and let the
    caller fall back to a pure-TS path (arbiter.ts falls back to cap-attenuation-monitor).
    The FFI is an UPGRADE, not a hard dependency. CI unit-tests do NOT build the dylib.
```

## Worked example — JSON-in/JSON-out export + free fn + koffi side

Rust (`crate-type = ["rlib", "cdylib"]`; deps `hmac`, `sha2`, `serde_json`):

```rust
use std::ffi::{CStr, CString};
use std::os::raw::c_char;
use std::panic::{catch_unwind, AssertUnwindSafe};

/// JSON in, JSON out. Returns a heap C string the caller frees with pd_string_free.
/// Returns null on ANY malformed input or panic — fail closed, never crash the host.
#[no_mangle]
pub extern "C" fn pd_macaroon_verify_json(req: *const c_char, len: usize) -> *mut c_char {
    let out = catch_unwind(AssertUnwindSafe(|| {
        if req.is_null() || len == 0 || len > 1_000_000 { return None; }
        let bytes = unsafe { std::slice::from_raw_parts(req as *const u8, len) };
        let s = std::str::from_utf8(bytes).ok()?;
        let parsed: VerifyRequest = serde_json::from_str(s).ok()?;
        let result = verify_request(parsed);               // pure Rust core (rlib-tested)
        CString::new(serde_json::to_string(&result).ok()?).ok()
    }));
    match out {
        Ok(Some(c)) => c.into_raw(),
        _ => std::ptr::null_mut(),
    }
}

/// Reclaim a string handed out by this library. The caller MUST call this exactly once.
#[no_mangle]
pub extern "C" fn pd_string_free(ptr: *mut c_char) {
    if !ptr.is_null() { unsafe { drop(CString::from_raw(ptr)); } }
}
```

TypeScript (koffi loader, mirroring `lib/arbiter.ts`):

```typescript
const libName = 'libpd_anchor.' + (process.platform === 'darwin' ? 'dylib' : 'so');
let lib: { verify: Function; free: Function } | null = null;
let loadError: string | null = null;

function load() {
  if (lib || loadError) return lib;
  try {
    const koffi = require('koffi');
    // candidate paths: dist/core next to this file, $PORT_DADDY_RESOURCE_DIR, execPath dir
    const dl = koffi.load(resolveDylibPath(libName));   // throws if absent → fallback
    const verify = dl.func('char* pd_macaroon_verify_json(const char* req, size_t len)');
    const free = dl.func('void pd_string_free(char* ptr)');
    lib = { verify, free };
  } catch (e) {
    loadError = (e as Error).message;   // captured, not thrown — caller degrades
  }
  return lib;
}

export function verifyViaFfi(req: object): VerifyResult | null {
  const l = load();
  if (!l) return null;                  // signal "use the TS fallback"
  const json = JSON.stringify(req);
  const ptr = l.verify(json, Buffer.byteLength(json));
  if (!ptr) return null;
  try { return JSON.parse(koffi.decode(ptr, 'char*')); }
  finally { l.free(ptr); }              // ALWAYS free, even on parse error
}
```

## Failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| Host process SIGABRT / segfault on a call | panic unwound across `extern "C"`, or null deref from a missing guard | `catch_unwind` + `panic="abort"`; add the 5 input guards (null/len/bound/utf8/parse) |
| RSS grows every call | returned CString never freed | every `into_raw()` needs a `from_raw()` free fn the TS side calls in a `finally` |
| `koffi.func` throws "cannot find symbol" | missing `#[no_mangle]`, name mismatch, or not a `cdylib` | `nm -gU lib*.dylib \| grep pd_` to list exports; match the koffi signature byte-for-byte |
| Timing side-channel in tag compare | early-return on first differing byte | fold-XOR over full length; never branch on a secret byte |
| Loader hard-fails the daemon when dylib absent | treated FFI as required | capture load error, return null, fall back to TS (FFI is an upgrade; CI has no dylib) |
| Works in jest, segfaults in the bun daemon | ABI/width mismatch (`size_t`) or bun-specific koffi load path | test under the REAL runtime (bun), not only jest; pin `usize`↔`size_t` |

## Quality gates

- [ ] Every `extern "C"` fn: `catch_unwind` (or `panic="abort"`) + null/len/bound/utf8/parse guards, returns a sentinel on any failure
- [ ] Every `into_raw()` has a matching `#[no_mangle]` free fn; the TS caller frees in a `finally`
- [ ] No Rust struct/enum crosses the boundary — primitives + `*const c_char` JSON only
- [ ] Constant-time compare for MACs (fold-XOR, no early return)
- [ ] `crate-type = ["rlib", "cdylib"]` so the core is unit-tested as an rlib AND shipped as a dylib
- [ ] `build-core.sh` builds + copies the dylib to `dist/core/`; the koffi loader's candidate paths include it
- [ ] TS loader degrades gracefully (null + captured error) when the dylib is absent; a TS fallback path exists
- [ ] Verified under the real runtime (bun daemon), not only jest
- [ ] Shared test vectors assert Rust and TS produce identical output on both sides of the boundary

## Output Contract

Before calling an FFI boundary done, express it as a JSON export plan matching
`schemas/ffi-plan.schema.json` (one entry per `extern "C"` export, plus the
crate/loader-level flags) and run `node scripts/ffi_safety_audit.mjs --input
plan.json`. It returns `{ pass, findings, recommendations, score }`,
deterministically flagging every quality gate below — a plan should not be
treated as safe on the strength of "it compiled and one call worked."

## NOT for

WebAssembly (use wasm-bindgen) · async/await across FFI (use a channel + poll) · moving
Rust ownership (Vec/String/struct) across the boundary without a free fn · hot-reloading
the dylib in-process (restart instead) · pure Rust-only crates (no FFI needed).

## Repo exemplars (read these first)

- `core/harbor-card-rs/src/lib.rs` — `#[no_mangle] extern "C"` exports, null/len/utf8 guards, constant-time compare
- `lib/arbiter.ts` — koffi loader: candidate paths, embedded-binary fallback, graceful degradation, `koffi.func` signatures
- `scripts/build-core.sh` — cargo build `--release` + copy dylib to `dist/core/` (platform-aware ext)
- `core/kernel/pd-anchor/` — the kernel crate to expose over FFI

## References

| File | Load When |
| --- | --- |
| `schemas/ffi-plan.schema.json` | Need to validate an export plan's structure programmatically. |
| `scripts/ffi_safety_audit.mjs` | Need deterministic scoring of an export plan against this skill's quality gates. |
| `examples/sample-input.json` | Need a complete, passing export plan to copy from. |
| `examples/expected-output.md` | Need the shape of a finished, passing audit result. |
| `templates/output-template.md` | Need a reusable export-plan template to fill in. |
| `agents/openai.yaml` | Need a subagent descriptor for delegated FFI implementation. |

<!-- BEGIN BUNDLE INDEX (auto: index_references.py) -->

## Skill Bundle Index

*Every file in this skill, and when to open it. Auto-generated; run `scripts/index_references.py --fix`.*

**root**
- [`CHANGELOG.md`](CHANGELOG.md) — Rust Kernel FFI — Changelog — - Imported from the global skill library into the repo (`skills/rust-kernel-ffi/`).
- [`README.md`](README.md) — Rust Kernel FFI — Build a Rust `cdylib` that a TypeScript/Bun runtime calls via `koffi` FFI, for a security kernel or enforcement core.

**`agents/`**
- [`agents/openai.yaml`](agents/openai.yaml) — openai (data/schema)

**`examples/`**
- [`examples/expected-output.md`](examples/expected-output.md) — Example Output: FFI Safety Audit — Scenario: a `pd_macaroon_verify_json` export (JSON-in/JSON-out over `*const c_char` + a matching `pd_string_free`) has just been implemented
- [`examples/sample-input.json`](examples/sample-input.json) — sample input (data/schema)

**`schemas/`**
- [`schemas/ffi-plan.schema.json`](schemas/ffi-plan.schema.json) — ffi plan.schema (data/schema)

**`scripts/`**
- [`scripts/ffi_safety_audit.mjs`](scripts/ffi_safety_audit.mjs)

**`templates/`**
- [`templates/output-template.md`](templates/output-template.md) — FFI Export Plan Template — [One-sentence description of the boundary this plan covers, e.g.

<!-- END BUNDLE INDEX -->
