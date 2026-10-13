---
name: reverse-eng-ida
description: >
  Deep reverse engineering in IDA Pro — Hex-Rays decompile, cross-references, types, patching — via
  the GUI or the ida-pro-mcp bridge for agent-driven analysis. Load when a PE/ELF/Mach-O/DLL/SYS needs
  pseudocode-grade analysis: license/serial checks, crypto or protocol recovery, a sink found during
  triage, malware capability mapping. Signals: "decompile this exe/dll", IDA, Hex-Rays, idapro_* tools,
  port 13337, .i64/.idb database, idalib.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
mitre: [T1592.002]
cwe: [CWE-121, CWE-798]
tools: [ida-pro, ida-pro-mcp, idalib, hex-rays]
schema_version: 1
---

# IDA Pro deep analysis

## When it applies
You have an in-scope binary (confirmed in `scope.txt`, a client-owned thick client/service, or a sample
you own — see `tradecraft-scope-roe`) and cheap triage (`reverse-eng-binary-triage`) has surfaced
functions worth real decompilation: auth/license logic, custom crypto or protocol parsers, a suspected
vulnerable sink, or a malware sample whose capabilities you must map. Use `reverse-eng-radare2` for
fast CLI recon first; use `reverse-eng-ghidra` when there's no IDA license.

## Why it works
Hex-Rays recovers near-source pseudocode, and IDA's cross-reference database ties every string,
import, and data item to the code that touches it — so you navigate by *who uses this* instead of
reading linearly. Renaming and retyping as you go compounds: each good name makes the next function
cheaper to read.

## Method
1. **Set up the MCP bridge** (agent-driven analysis). Install from GitHub — the PyPI `ida-mcp`
   package is a *different project*, do not install it:
   ```
   pip install git+https://github.com/mrexodia/ida-pro-mcp.git
   ida-pro-mcp --install     # installs the IDA plugin + client config
   ida-pro-mcp --config      # verify
   ```
   The plugin listens on `127.0.0.1:13337`; tools appear under your MCP server name (e.g. `idapro_*`,
   ~65 tools depending on version). Headless (`idalib` supervisor) needs an idalib-licensed install;
   otherwise run the plugin inside the GUI — same tools either way.
2. **Open the target.** GUI: open the file, confirm `[MCP] ... port=13337` in the output window.
   Headless: open the database with the bridge's `idb_open` (ida-pro-mcp 2.x naming — no longer
   `idalib_*`); it returns a `session_id` that later calls pass as `database=`.
3. **Survey before diving.** `survey_binary(detail_level="minimal")` → architecture, entry point,
   function count, strings, segments, categorized imports. **Record the import table before any
   conclusion** — crypto / network / file-IO / registry / injection categories steer everything
   downstream (for DLL/SYS also record the export table; an empty import table means likely dynamic
   loading — verify with runtime API breakpoints). Full tool inventory: [`cheatsheet.md`](cheatsheet.md).
4. **Work string/import → sink.** Anchor on `find_regex("https?://")` or
   `entity_query(kind="imports", filter="Crypt")`, jump to users with `xrefs_to(addr)`, then read with
   `analyze_function(addr)` or `decompile(addr)`. Map reachability with `callgraph(roots, max_depth=3)`
   and `trace_data_flow(addr, direction="backward")`.
5. **Annotate as you go** — `rename` functions/locals, `set_comments`, `declare_type` + `set_type` for
   structs. Never convert number bases by hand: use `int_convert`.
6. **Patch only when asked, on a copy.** `patch_asm` / `patch` rewrite the database; `idb_save` to
   persist. Re-decompile the patched site to confirm the bypass before claiming it.

## Gotchas
- **Some MCP clients reject `idb_open`** with `Structured content does not match the tool's output
  schema` — open the database by calling the HTTP API on 13337 directly, then use the MCP tools.
- **Opening with auto-analysis looks hung** — a large GUI binary can take 5+ minutes before the open
  call returns; poll for readiness instead of killing it.
- **Stale locks after a killed open** — orphaned idalib workers hold `.id0/.id1/.nam`; copy the sample
  to a temp dir and open the copy. Never `taskkill /T` the process tree — it kills the GUI `ida.exe` too.
- **`C:\Windows\System32` files** can't be read by idalib directly — copy them out first.
- **C++/STL noise** — let FLIRT/Lumina signature matching collapse library functions before reading
  business logic.
- **Packed samples** — repair the IAT first (ImportREC for x86, Scylla for x64). If repair fails,
  switch to dynamic API tracing instead of grinding on a broken static view (`reverse-eng-deobfuscation`).
- **"No database bound"** = nothing is open yet; **function name not found** = search first with
  `list_funcs` + filter, names must be exact.
- Analyze untrusted binaries in an isolated VM — loading a hostile sample is itself an action.

## Verify success
You can state the algorithm or check in pseudocode, name the exact functions/addresses involved, and
show a confirming observation — a bypassed check on a patched copy, a recovered plaintext/key, or a
crash explained — with every renamed symbol traceable back to its original address for the report.

## References
ida-pro-mcp (github.com/mrexodia/ida-pro-mcp); Hex-Rays documentation; FLIRT/Lumina signatures.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
