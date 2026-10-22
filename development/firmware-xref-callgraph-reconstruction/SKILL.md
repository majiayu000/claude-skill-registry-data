---
name: firmware-xref-callgraph-reconstruction
description: Reconstruct call graphs and indirect control flow in stripped embedded firmware using XREFs, disassembly, tables, callbacks, and source-to-sink evidence.
---

# XREF/call-graph reconstruction

Use this skill for stripped MIPS, ARM, and similar firmware where symbols are incomplete and indirect calls hide authorization or state-changing paths.

## Workflow

1. Establish architecture, endianness, load addresses, relocations, executable regions, symbols/strings, and tool versions. Preserve raw binaries and command output.
2. For each target function, enumerate direct calls, data references, pointer loads, table entries, registrations, callbacks, wrappers, and tail calls. Search instruction references and copied/relocated table data.
3. Recover boundaries and calling conventions from prologues, register use, stack frames, return values, and callers. Track argument provenance and structure offsets through each edge.
4. Decode dispatch tables empirically: stride, selector, handler pointer, flags, strings, and consumers of every field. Never assign semantics from an unused-looking byte without an XREF or data-flow basis.
5. Build source-to-sink graphs for authentication/session creation, config writes, reset/reboot, firmware update, command dispatch, and HTTP/UDP entry points. Mark the first proven authorization check and every unresolved indirect edge.
6. Validate static claims with harmless evidence only when needed. Do not invoke a state-changing path to resolve an ambiguous edge.

## Reporting

For each edge report caller, callee, address, arguments, tested fields, branch/failure behavior, and confidence. Include unresolved edges explicitly and distinguish `PROVEN FROM CODE`, `VERIFIED IN FIRMWARE`, `HIGH-CONFIDENCE INFERRED`, and `UNKNOWN`. Keep address maps reproducible and never overwrite originals.
