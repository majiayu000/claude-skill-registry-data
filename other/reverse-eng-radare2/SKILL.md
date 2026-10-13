---
name: reverse-eng-radare2
description: >
  Command-line binary analysis with radare2/r2 — recon, disassembly, strings/imports, cross-references,
  patching, diffing, and scripting, no GUI needed. Load for exe/dll/so/elf/dex/wasm CLI analysis,
  quick triage before committing to IDA/Ghidra, r2 batch commands (-c/-A), r2pipe scripts, or help with
  rabin2/rasm2/radiff2/rahash2/rax2. Signals: "use radare2/r2", terminal-only environment, radiff2
  diffing, fast recon on a new sample.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
mitre: [T1592.002]
cwe: [CWE-121, CWE-798]
tools: [radare2, rabin2, rasm2, radiff2, rahash2, rax2, r2pm]
schema_version: 1
---

# radare2 CLI analysis

## When it applies
You need fast, scriptable analysis of an in-scope binary (`scope.txt` / client-owned / your own sample —
`tradecraft-scope-roe`) from a terminal: first-pass recon before opening a heavyweight decompiler,
CI/SSH environments with no GUI, quick patches and diffs, or r2 automation. When you need
pseudocode-grade reading, hand off to `reverse-eng-ida` or `reverse-eng-ghidra` — r2's job is speed
and scriptability, not decompilation. For obfuscated JavaScript, that's `reverse-eng-deobfuscation`,
not this skill.

## Why it works
Every r2 operation is a composable command — the same one-liners work interactively, in batch
(`-c "..."`), over HTTP, or via r2pipe from any language — so recon that costs minutes in a GUI costs
seconds here, and every step is reproducible by construction.

## Method
1. **Check the install, don't assume it:** `r2 -v` / `rabin2 -v`. On Windows the binaries are
   `radare2.exe`, `rabin2.exe`, `rasm2.exe`, `radiff2.exe`, `rahash2.exe`, `rax2.exe`, `r2pm.exe`.
2. **Recon before analysis.** Minimum first pass:
   ```
   rabin2 -I sample.exe    # format, arch, bits, entry point
   rabin2 -z sample.exe    # strings
   rabin2 -i sample.exe    # imports  (required — never skip to function-level work without it)
   rabin2 -E sample.exe    # exports  (required too for DLL/SYS)
   ```
   Classify the imports (network / file / crypto / injection / registry) in your notes. An empty or
   "too clean" import table means likely dynamic loading — plan to catch APIs at runtime instead of
   concluding statically. No traditional IAT (.NET) → use IL/metadata inspection as the equivalent.
   Packed sample: repair the IAT (ImportREC on x86, Scylla on x64); if repair fails, go dynamic rather
   than grinding on a broken static view.
3. **Interact only after recon.** `r2 sample.exe`, then `aaa` (not the heavier `aaaa`), `afl` to list
   functions, `iz` strings, `s entry0` / `pdf` to disassemble a function, `VV` for graph view.
4. **Locate the key logic:** `afl~main`, `iz~http`, then `axt <addr>` to find who references a string
   or address, `s <addr>` + `pdf` to read it. Full command reference: [`cheatsheet.md`](cheatsheet.md).
5. **Patch only when asked, on a backup:** `r2 -w sample.exe` (or `oo+` in-session), then
   `wa nop` / `wa jmp 0x401050` / `wx 9090`, `wq` to write and quit. Warn before entering write mode;
   re-disassemble to verify the change.
6. **Batch and automate:** `r2 -A -q -c "afl;iz;ii;q" sample.exe` for one-shot output; `-A` auto-
   analyzes, `-q` quiet, `-c` runs a command string. Keep long command chains readable — split them.

## Gotchas
- **Windows `.sdb` warnings** (`Cannot find ...\share\format\dll\*.sdb` from rabin2) are usually
  harmless if the main output is complete — don't mistake them for analysis failure.
- **Don't lead with `aaaa`** — it's much heavier than `aaa` and rarely needed on the first pass.
- **Read-only by default** — plain `r2 <file>` never modifies; only `-w`/`oo+` does. Back up first.
- **Windows quirks** — quote paths with spaces; if `r2` isn't found after install, open a fresh
  terminal (PATH refresh).
- **Ecosystem extras are accelerators, not replacements** — `r2pm -ci r2ghidra` adds a decompiler,
  `r2http` (`r2 -N -e http.bind=localhost -e http.port=9393 -q -c=h sample.exe` then
  `curl --data-binary 'aflj' http://127.0.0.1:9393/cmd`) gives a stateful HTTP channel,
  `radius2` does symbolic execution. Same recon discipline applies.
- Analyze untrusted binaries in an isolated VM.

## Verify success
A recon summary you can stand behind — format/arch/entry, the import classification, the suspicious
strings — plus located key functions (name + address + disassembly excerpt) and, for patches, a
re-disassembly showing the bytes changed as intended. Every step is a command someone else can rerun.

## References
radare2 book (book.rada.re); r2pm package index; radareorg/radare2-skills ecosystem.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
