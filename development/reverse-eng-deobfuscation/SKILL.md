---
name: reverse-eng-deobfuscation
description: >
  Peel obfuscation off code until it's readable or callable — packed native binaries, minified/
  obfuscated JavaScript, WebAssembly, and JS-VM-protected (JSVMP) bundles. Load when analysis is
  blocked by protection layers. Signals: high-entropy sections, a tiny import table, UPX headers,
  string-array/control-flow-flattened JS, `_0x` variable names, a .wasm module, an interpreter
  loop over a bytecode array, anti-debugger `debugger;` traps.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
cwe: [CWE-656]
tools: [upx, ghidra, wasm2wat, babel, box-js, frida]
schema_version: 1
---

# Deobfuscation

## When it applies
`reverse-eng-binary-triage` or `web-client-side-signing-bypass` stalls because the code is
protected: a packed executable, obfuscated JS whose logic you can't follow, a WASM blob doing the
real work, or a JSVMP interpreter running custom bytecode. You need to reduce the protection enough
to read the logic or call the function — no further.

## Why it works
Obfuscation raises the cost of reading, it doesn't change what the code *does* — the real behavior
is still there at runtime. So the shortest path is usually dynamic: let the code deobfuscate itself
(unpack in memory, evaluate the string array) and capture the result, rather than statically
undoing every transform.

## Method
Peel only as many layers as the task needs; stop the moment the logic is legible or the function is
callable.

1. **Native packers.** Detect (high entropy, `UPX!` marker, one-section import stubs). For UPX,
   `upx -d`. For custom packers, run under a debugger to the original entry point (OEP) after the
   unpacking stub finishes, then dump the in-memory image and fix the imports.
2. **Obfuscated JS.** Pretty-print first. Then resolve the common transforms: evaluate the
   string-array + rotator to substitute real names, constant-fold the arithmetic, and undo
   control-flow flattening (the `while(true){switch(state)}` dispatcher) by ordering the cases.
   AST tools (Babel) automate the mechanical passes; a sandbox (`box-js`) runs it safely to log
   what it builds.
3. **WebAssembly.** `wasm2wat` to text; find exports and the imported JS bindings that feed it;
   hook the JS↔WASM boundary in DevTools to log inputs/outputs instead of reading every opcode.
4. **JSVMP (custom bytecode VM).** Don't reimplement the VM — instrument it. Hook the dispatch
   loop / the handler that emits the result and log `input → output`, or lift only the handful of
   opcodes on the path you care about.
5. **Anti-debug.** Neutralize `debugger;` traps (conditional breakpoint → never pause, or patch
   them out), timing checks, and integrity checks before they change behavior — but classify the
   divergence first so you don't "fix" the wrong thing.

## Gotchas
- **Prefer dynamic to static** — capturing self-deobfuscated output beats manually reversing every
  layer, especially for JSVMP and heavy packers.
- **Obfuscation ≠ the vulnerability.** It's a means to reach the real bug (signing bypass, an
  endpoint, a secret) — don't report "the code is obfuscated".
- **Anti-debug can flip behavior when a debugger attaches** — verify your deobfuscated path matches
  the real one (diff a known input/output).
- **Run unknown code sandboxed** — a malicious bundle can act on execution.

## Verify success
You can read the deobfuscated logic, or call the target function and reproduce its output for a
known input — enough to hand back to `reverse-eng-binary-triage`, `web-client-side-signing-bypass`,
or the exploit path.

## References
UPX docs; Babel AST tooling; `box-js`; `wasm2wat` (WABT); notes on control-flow flattening & JSVMP.
