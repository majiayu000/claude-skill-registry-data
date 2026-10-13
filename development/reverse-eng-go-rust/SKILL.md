---
name: reverse-eng-go-rust
description: >
  Reverse stripped Go and Rust binaries — recover symbols from pclntab/moduledata and panic
  metadata, then navigate language-specific idioms. Load when a stripped ELF/PE/Mach-O shows Go
  or Rust runtime residue. Signals: "go.buildid", "runtime.main" / "main.main", "panic:" or
  "rust_begin_unwind" strings, /rustc/ or src/*.rs paths, huge static binary with no symbols,
  Go malware, a Rust release build.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
mitre: [T1027]
tools: [goresym, redress, ida, ghidra, radare2, gdb, frida]
schema_version: 1
---

# Go / Rust binary reversing

## When it applies
You have a stripped binary in scope (`tradecraft-scope-roe`, `scope.txt`) and triage
(`reverse-eng-binary-triage`) shows Go or Rust residue — a Go malware sample, a Rust release
build, a Go-compiled red-team tool. Generic decompilation drowns you in runtime code; these
languages carry enough metadata to rebuild the symbol map first.

## Why it works
Both toolchains ship binaries that are mostly runtime, but both embed rich metadata: Go keeps the
pclntab (function names, file:line, type info) even when the symbol table is stripped, and Rust
leaks panic strings with full source paths. Recovering that metadata turns an anonymous blob back
into named functions, and the runtime residue itself fingerprints the language and version.

## Method
1. **Fingerprint the language.**
   - Go: `strings` for `go.buildid`, `runtime.`, `src/.../*.go` paths, `Go buildinf`.
   - Rust: `strings` for `rust_begin_unwind`, `panicked at`, `/rustc/<hash>/library/...` paths,
     crate names in `src/*.rs` paths.
2. **Go: recover symbols from pclntab.** Run GoReSym (`GoReSym -t target`) or redress to parse
   pclntab/moduledata → function names, types, package list; import the output into IDA/Ghidra
   (Go helper plugins apply it as names/types). Then anchor at `runtime.main` → `main.main` and
   work outward into the `main.*` package — skip the `runtime.*`/`crypto/*`/`net/http` library
   code except to note which libraries are linked (crypto and net paths hint at C2 and key handling).
3. **Rust: drive from panic strings.** Each `panicked at '...', src/foo.rs:LINE:COL` string is a
   file:line anchor — xref it to land inside real logic. Collect `Option`/`Result` unwrap sites
   the same way.
4. **Read idioms, not just code.**
   - Go strings are (pointer, length) pairs — not NUL-terminated; slices are (ptr, len, cap);
     interfaces are (itab, data). A "two arguments" call passing a string is really one string.
   - Rust generics explode one function into many monomorphized copies — don't analyze each;
     follow string xrefs to the copy that matters. Async (tokio) compiles to state machines;
     reconstruct flow via cross-references, not linear reading.
5. **Dynamic confirms.** gdb and Frida both work, but mind Go's scheduler: goroutines hop OS
   threads, so break on a *string usage* (log line, config key, crypto input) rather than chasing
   a thread. Config/log strings are the best breakpoint anchors in both languages.

## Gotchas
- **Packed first, language second** — UPX et al. hide the pclntab; unpack before GoReSym
  (`reverse-eng-deobfuscation`).
- **Malware corrupts moduledata** (zeroed magic, moved pclntab) specifically to break GoReSym —
  locate pclntab by its magic bytes in the section and repair, or fall back to string-driven analysis.
- **Don't get lost in the runtime** — most functions in the binary are library code. If a function
  has no path to attacker input or secrets, move on.
- **Stripped Rust gives almost nothing back** — panic strings and crate paths *are* the map;
  rename functions as you identify them or the picture doesn't survive.

## Verify success
Key functions are renamed (or you hold an equivalent offset→purpose map), the language/runtime
evidence is recorded (build ID, compiler version, linked packages), and you can state where
attacker-controlled input and the interesting crypto/network logic live.

## References
GoReSym & redress documentation; Go pclntab/moduledata format writeups; Rust panic ABI notes.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
