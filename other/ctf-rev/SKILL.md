---
name: ctf-rev
description: >
  CTF reversing speed-run — crack flag-check binaries fast: locate the check via strings/xrefs,
  bypass anti-debug and obfuscation, and solve constraint-checkers with z3 instead of manual
  algebra. Load when the handout is an ELF/PE/exe that asks for input or a key. Signals: "rev"
  category, "Enter the flag/key/password", correct/wrong messages, crackme, packed binary,
  anti-debug (ptrace, IsDebuggerPresent), keygen challenge.
domain: ctf
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
cwe: [CWE-798]
tools: [radare2, ghidra, ida-pro, gdb, ltrace, strace, z3, angr, upx, strings]
schema_version: 1
---

# CTF reverse engineering speed-run

## When it applies
The handout is a binary that checks something — a flag, key, serial, or password — and you need
the accepted input. This skill is the CTF *workflow*: find the check fast, defang whatever stops
you from seeing it, and solve the constraints mechanically. For deep tool use defer to
`reverse-eng-binary-triage` (first-pass recon), `reverse-eng-radare2` / `reverse-eng-ghidra` /
`reverse-eng-ida` (analysis), `reverse-eng-deobfuscation` (unpacking/devirtualization).

## Why it works
A flag-checker is a pure function from input to accept/reject, and CTF ones are small. You never
need to understand the whole binary — only the check — so the game is *locating* it (strings and
xrefs beat linear reading), *exposing* it (anti-debug and packing are thin in CTF), and *solving*
it (the constraints are almost always z3-shaped; manual algebra is the slow path).

## Method
1. **Two-minute triage.** `file`, `strings -n 6` (+ `strings -el` for UTF-16), `checksec`, run it
   with junk input. The strings that matter: "Correct!"/"Wrong", the flag format itself
   (sometimes just… present), odd alphabets, and packer markers (`UPX!`). Packed → `upx -d` first;
   anything fancier → `reverse-eng-deobfuscation`. .NET/Java/Go/Rust/Python-exe binaries route to
   their dedicated tooling (`reverse-eng-dotnet`, `reverse-eng-go-rust`, pyinstxtractor+uncompyle).
2. **Locate the check, don't read the binary.** In r2/Ghidra/IDA: find the "Wrong" string, follow
   the xref to its function, and read *backwards* from the branch that prints it. Everything
   between the input read and that branch is the check. For C/C++ this is usually one function.
3. **Dynamic shortcuts before static grinding.**
   - `ltrace ./chall` — library calls like `strcmp(input, "...")`, `strlen`, per-char compares
     leak the answer or its length with zero analysis.
   - Compare-per-character binaries → count crashes/coverage: flip one input byte at a time and
     watch which comparison index changes, or use a debugger on the compare loop to read each
     expected byte as it's checked.
   - `strace` for flag files, env vars, network the binary secretly consults.
4. **Defang anti-debug (it's shallow in CTF).** Common tricks and one-line counters:
   - `ptrace(PTRACE_TRACEME)` → patch the call, or `catch syscall ptrace` in gdb and force
     return 0.
   - `IsDebuggerPresent` / `PEB.BeingDebugged` → zero the flag in the debugger, or patch the
     conditional jump that follows.
   - Timing checks (`rdtsc`) → patch or ignore — they only guard a branch.
   - Self-checksum / anti-tamper → make *all* your patches before the checksum computes, or patch
     the comparison result, not the data.
   The universal move: find the check that *branches on* the anti-debug result and flip that one
   branch — don't fight each mechanism.
5. **Solve the check with z3 — the CTF superpower.** When the check transforms input bytes and
   compares against constants (xor/add/rotate/substitute chains, matrix math, per-position
   relations), transcribe the decompiled pseudocode into z3 almost verbatim:
   ```python
   from z3 import *
   flag = [BitVec(f'c{i}', 8) for i in range(32)]
   s = Solver()
   # constraints copied from the decompilation, e.g.:
   s.add((flag[i] ^ 0x37) + i & 0xff == target[i])
   s.add(And(*[And(0x20 <= c, c < 0x7f) for c in flag]))   # printable
   s.check(); m = s.model(); print(bytes(m[c].as_long() for c in flag))
   ```
   Use `BitVec` (not `Int`) so overflow wraps like machine arithmetic. If the decompile is messy,
   feed the whole function to angr (`angr` with `find=<success addr>, avoid=<fail addr>`) and let
   it symbolically execute to the answer.
6. **Know the recurring shapes.** Flag = input satisfying equations (z3); keygen (invert the
   serial transform, then generate any valid one); VM challenges (small custom bytecode — write a
   30-line disassembler for the handlers, the flag falls out); wasm (wasm2c/wabt, then same game);
   mobile crackmes (`mobile-apk-reverse`).

## Gotchas
- **The first "Correct" string can be a decoy** — verify your answer actually prints success on
  the real binary; some challenges have fake success paths guarding the real check.
- **Anti-debug that crashes you *is* the solve path** — if debugging changes behavior, run under
  the debugger anyway and note where; the flag transformation sometimes only happens under ptrace.
- **BitVec vs Int** — z3 `Int` doesn't wrap; forgetting `& 0xff` semantics makes solvers return
  `unsat` on trivially solvable checks.
- **Multiple valid flags** — constraint checks can accept many inputs; the scoreboard wants the
  one in flag format, so add `flag{`-prefix constraints when known.
- **Don't statically invert what you can dynamically read** — a `strcmp` in ltrace beats an hour
  of decompilation; try dynamic first, always.
- **Stripped/optimized binaries mislead decompilers** — check the disassembly when pseudocode
  looks impossible (`reverse-eng-binary-triage` for triage discipline).

## Verify success
The recovered input, entered into the *original unmodified* binary, produces the success path —
and matches the event flag format. For keygens, two independently generated keys both validate.

## References
Triage: `reverse-eng-binary-triage`; deep analysis: `reverse-eng-ghidra`, `reverse-eng-ida`,
`reverse-eng-radare2`; unpacking/anti-analysis: `reverse-eng-deobfuscation`; z3 docs; angr.
Triage via `ctf-methodology`.
