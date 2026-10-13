---
name: reverse-eng-binary-ninja
description: >
  Reverse engineer in Binary Ninja — HLIL/MLIL/LLIL inspection, strings/imports/exports,
  cross-references, types, patching, Python API automation, and the optional MCP/HTTP bridge. Load
  when the user picks Binary Ninja, when its IL levels materially help data-flow analysis, or when
  IDA/Ghidra/radare2 results need an independent cross-check. Signals: "binaryninja", HLIL/MLIL,
  BinaryView scripting, Vector 35, localhost:9009 bridge.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
mitre: [T1592.002]
cwe: [CWE-121, CWE-798]
tools: [binary-ninja, binary-ninja-mcp]
schema_version: 1
---

# Binary Ninja reverse engineering

## When it applies
You're analyzing an in-scope binary (`scope.txt` / client-owned / your own sample —
`tradecraft-scope-roe`) and Binary Ninja is the chosen tool, its intermediate languages genuinely help
(SSA-form data-flow questions), or a high-impact conclusion from `reverse-eng-ida`,
`reverse-eng-ghidra`, or `reverse-eng-radare2` deserves a second decompiler's opinion. Binary Ninja is
commercial software — it needs a valid Vector 35 license, installed by the user.

## Why it works
Binary Ninja lifts every function into layered ILs — LLIL close to the machine, MLIL in SSA form
(variables versioned, so data flow is explicit), HLIL close to source. Questions like "where does this
attacker-controlled value come from" become IL queries instead of manual register tracking, and the
whole analysis is scriptable through one Python `BinaryView` API.

## Method
1. **Baseline the target first** — record file hash, architecture, entry points, segments,
   imports/exports, and representative strings before touching anything. Work on a copy whenever you
   intend to patch or save database changes.
2. **Pick the integration:**
   - **GUI / Python API** — preferred when Binary Ninja is already open or analysis is interactive.
   - **MCP bridge** — only when explicitly requested. The reviewed community option is
     `fosdickio/binary_ninja_mcp` (GPL-3.0, not an official Vector 35 component; min Binary Ninja
     build 4000). Keep its HTTP listener on `127.0.0.1:9009` — never expose it to the network.
     Pin the bridge version:
     ```
     npx -y binary-ninja-mcp@1.0.0 --host 127.0.0.1 --port 9009
     ```
     The bridge only works once Binary Ninja is running with a binary open and the plugin endpoint
     responds; register it only in the MCP client the user chose. Discover the live tool list rather
     than assuming every upstream function exists (families include view selection, `list_imports`,
     `list_exports`, `list_strings`, `decompile_function`, `get_il`, callers/callees, xrefs, types,
     comments, renames, byte patching).
3. **Navigate by references, not linearly.** Follow call sites and cross-references *before*
   interpreting any function in isolation.
4. **Pick the right IL level per question:** HLIL for readable logic, MLIL SSA for data-flow tracing,
   LLIL/disassembly when the lifting loses instruction-level behavior (self-modifying code, exotic
   instructions, anti-analysis tricks).
5. **Annotate incrementally** — names, comments, types — keeping original addresses in your notes so
   every renamed symbol stays traceable.
6. **Treat mutations as mutations.** Byte patches, prototype changes, and saved-file writes happen
   only when requested, on a preserved copy of the original artifact.
7. **Cross-check high-impact conclusions** with a second evidence source or another disassembler
   before they go in a report.

## Gotchas
- **The lifting lies occasionally** — HLIL can drop or fold behavior; when pseudocode contradicts the
  disassembly, trust the disassembly and drop to LLIL.
- **License-gated** — if Binary Ninja can't open the target or isn't licensed, fall back to
  `reverse-eng-ghidra` (free) rather than stalling.
- **The MCP bridge is third-party and GPL-3.0** — review that boundary before installing it; keep it
  localhost-only.
- **"IL looks too clean" on packed samples** — unpack first (`reverse-eng-deobfuscation`); lifted
  junk reads like logic if you want it to.
- Analyze untrusted binaries in an isolated VM.

## Verify success
Report concrete addresses, function names, the IL level each conclusion was drawn at, supporting
strings/imports, a confidence note, and reproduction steps — so a reviewer can re-walk the analysis in
the GUI and land on the same functions.

## References
Binary Ninja docs & Python API; fosdickio/binary_ninja_mcp (GPL-3.0 bridge); Vector 35.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
