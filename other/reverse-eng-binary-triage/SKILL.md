---
name: reverse-eng-binary-triage
description: >
  Triage a native binary you can run or read — find the vulnerable logic, the dangerous sinks, and
  the input path — with static + dynamic analysis. Load when handed an ELF/PE/Mach-O, a thick
  client, a standalone or obfuscated binary, or a service whose source you don't have. Signals: a compiled
  executable in scope, "reverse this binary", a crash/segfault to understand, custom protocol,
  strings that hint at auth/secrets, a setuid binary during privesc.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
mitre: [T1592.002]
cwe: [CWE-121, CWE-787, CWE-798]
tools: [ghidra, radare2, gdb, gef, strings, ltrace]
schema_version: 1
---

# Native binary triage

## When it applies
You have a compiled binary — a thick desktop/mobile client, a network service, a setuid helper
during `privesc`, or a firmware component (`reverse-eng-firmware`) — and no source. You need to
understand what it does, where attacker input reaches, and whether that path is exploitable, before
committing to `exploit-poc-development`.

## Why it works
A binary carries its logic in the code and its intent in the strings, imports, and symbols.
Cheap static passes (strings, imports, cross-references) point straight at the interesting
functions; a debugger then confirms what actually happens at runtime, so you spend deep analysis
only on the paths that matter.

## Method
1. **Cheap recon first.** `file`, `strings -n8`, and the import table tell you the language,
   protections, and intent in seconds. `checksec` (or `rabin2 -I`) for NX / PIE / RELRO / canary —
   they scope what an exploit would even need.
2. **Map input → sink.** Find where input enters (`recv`, `read`, `argv`, `getenv`, a file/format
   parse) and trace to dangerous sinks: `strcpy`/`memcpy`/`sprintf`/`gets` (overflow),
   `system`/`exec`/`popen` (command injection), format-string sinks (`printf(user)`), and integer
   math feeding an allocation size.
3. **Read it in a decompiler.** Ghidra or radare2/Cutter — jump to the sink, follow
   cross-references back to reachable entry points, and note the preconditions to reach it.
4. **Confirm dynamically.** Run under `gdb`+GEF/pwndbg (or `ltrace`/`strace`), break at the sink,
   feed a marker input, and watch whether you control size/pointer/format. A crash you can steer
   (controlled `$pc`, overwritten pointer) is the confirmation.
5. **Pull the low-hanging intel** — hardcoded secrets/keys (`CWE-798`), debug/backdoor paths,
   weak auth checks (a `strcmp` against a literal), and custom-protocol structure for later fuzzing.

## Gotchas
- **Stripped binaries** have no symbols — lean on strings, imports, and library-call signatures;
  name functions as you go so the map survives.
- **Packed/obfuscated** (high entropy, tiny import table) → deobfuscate first (`reverse-eng-deobfuscation`).
- **A crash is not yet a bug worth reporting** — determine control and impact before you claim it;
  validate with `reporting-triage-validation`.
- **Analyze untrusted binaries in an isolated VM** — running an unknown executable is itself risky.

## Verify success
You can state the input path, the vulnerable sink, the preconditions to reach it, and a runtime
observation (controlled crash or a leaked secret) that proves it — a concrete lead for exploit
development, not a guess from the disassembly.

## References
Ghidra & radare2 documentation; `pwndbg`/GEF; the `checksec` protections model; CWE-121/787/798.
