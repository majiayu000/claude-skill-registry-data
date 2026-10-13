---
name: reverse-eng-ghidra
description: >
  Reverse engineer with Ghidra (GUI, headless, or ghidra-mcp) — decompile, cross-references,
  scripting — when there's no IDA license, for batch/CI decompilation, or as a free second opinion.
  Load for "decompile without IDA", bulk analysis of many samples, analyzeHeadless, Ghidra scripts
  (Jython/PyGhidra), or patch diffing with ghidriff. Signals: an ELF/PE needing a decompiler,
  "use Ghidra", headless automation, no commercial RE license.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
mitre: [T1592.002]
cwe: [CWE-121, CWE-798]
tools: [ghidra, ghidra-mcp, pyghidra, ghidriff]
schema_version: 1
---

# Ghidra reverse engineering

## When it applies
You need decompiler-grade analysis of an in-scope binary (`scope.txt` / client-owned / your own
sample — `tradecraft-scope-roe`) and there's no IDA license, or you need to process many samples in
batch or CI. Also the right call when a conclusion from `reverse-eng-ida` or `reverse-eng-radare2`
deserves an independent cross-check with a different decompiler.

## Why it works
Ghidra's P-code lifter gives one decompiler across dozens of architectures (x86/ARM/MIPS/PPC and
obscure firmware targets IDA may not load well), and headless mode turns the whole
import → analyze → decompile pipeline into a scriptable batch step — so bulk triage costs the same as
single-file analysis.

## Method
1. **Project, import, analyze.** New project → import the file → run auto-analysis with the default
   analyzers. Record the language/compiler spec Ghidra picked and the base address — a wrong language
   guess (e.g. wrong ARM variant) silently produces garbage decompilation.
2. **Anchor on strings and imports.** Search → For Strings, then right-click → References to find the
   code that uses an interesting string; double-click a function to decompile it. Same input → sink
   discipline as `reverse-eng-binary-triage`: record the import table before drawing conclusions.
3. **Read and annotate.** Decompile window for logic; `L` to rename, `;` for a comment, plate comments
   for function summaries. Rename/retype as you go — it compounds.
4. **Automate with scripts.** Window → Script Manager for Jython (Python 2.7) scripts; for real
   Python 3 use PyGhidra, which bridges to CPython.
5. **Batch with headless** when processing many files or running in CI:
   ```
   analyzeHeadless /path/to/project Proj -import sample.bin -postScript ExportDecomp.py
   ```
   (`analyzeHeadless` lives in Ghidra's `support/` dir — locate it on your install, don't guess paths.)
6. **MCP bridge (optional).** If ghidra-mcp is configured, pull decompilations and xrefs through its
   tools — confirm the actual port from your own config (commonly 8765) rather than assuming.
7. **Hand off when static runs out** — dynamic confirmation goes to gdb/Frida
   (`reverse-eng-binary-triage` step 4); patch diffing between two builds is ghidriff's job.

## Gotchas
- **Wrong language/compiler spec** on import → confident but wrong pseudocode; re-import with the
  correct variant if decompilation looks structurally impossible.
- **Default analyzers aren't always enough** — for aggressive optimizations or unusual files, rerun
  analysis with more options enabled rather than accepting partial functions.
- **Jython is Python 2.7** — scripts written for modern Python silently fail; use PyGhidra for
  Python 3.
- **Large binaries are slow to analyze** — scope analysis options, don't just wait and assume a hang.
- **Packed/obfuscated samples** decompile to noise — unpack/deobfuscate first
  (`reverse-eng-deobfuscation`); don't read flattened junk as if it were logic.
- Analyze untrusted binaries in an isolated VM.

## Verify success
You can hand over named functions at concrete addresses with readable pseudocode for the key logic,
plus reproducible steps (project/script/headless command) so a teammate gets the same result — or a
headless run that emitted decompilations for every sample in the batch.

## References
Ghidra docs (incl. the analyzeHeadless README); PyGhidra; ghidriff for patch diffing.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
