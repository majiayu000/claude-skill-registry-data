---
name: find-UTIL_Remove
description: |
  Locate UTIL_Remove in CS2 server.dll / libserver.so via IDA Pro MCP and emit a fresh, minimal-unique
  signature or offset for the local gamedata entry "UTIL_Remove" (symbol UTIL_Remove). This is a non-virtual function - emit a byte signature (func_sig), not an offset.
  Locate it via cross-references, distinctive constants/strings in its body, or callers
  of related symbols; verify by decompilation before committing to a candidate.
  Trigger: UTIL_Remove, UTIL_Remove
disable-model-invocation: true
---

# Find UTIL_Remove

Target: `UTIL_Remove` (func) in the CS2 server module.

> Do NOT anchor on raw byte patterns from older releases - they shift. Use anchors only to *locate*
> the function, then generate a fresh minimal-unique function-head signature with relocated bytes
> wildcarded. Produce ONLY the output file(s) listed in this skill's expected outputs, for the binary
> loaded in THIS session (one platform per run). NEVER open or analyze the other platform's binary.

## Method

This is a non-virtual function - emit a byte signature (func_sig), not an offset.
Locate it via cross-references, distinctive constants/strings in its body, or callers
of related symbols; verify by decompilation before committing to a candidate.

## Mandatory self-check before emitting

The pipeline re-reads the bytes at your `func_va` and deterministically regenerates `func_sig` from
them - if your `func_sig` does not match those bytes EXACTLY (with `??` matching anything), the run
aborts. Therefore:

1. After picking the function, read the actual bytes at `func_va` via the IDA MCP.
2. Derive `func_sig` FROM those bytes: keep stable opcode bytes literally, wildcard relocated or
   variable operands as `??`.
3. `func_sig` MUST start at `func_va` (the true function head).
4. Only then write the YAML. A mismatch is always a bug in YOUR output, never in the pipeline.

## Output schema (STRICT)

Write the YAML file `<symbol>.{platform}.yaml` with EXACTLY these fields:
```yaml
func_name: <SYMBOL_NAME>
func_va: "<hex virtual address>"
func_rva: "<hex rva>"
func_size: "<hex size>"
func_sig: "<byte pattern, ?? wildcards, function head, minimal-unique>"
```
NEVER include vfunc_index, vfunc_offset, vfunc_sig or vtable_name.

## Verification

1. Decompile the candidate and confirm the behavior matches the purpose above (not a caller or callee).
2. Confirm uniqueness: the generated pattern must match exactly one location in the loaded binary.
3. If a candidate cannot be confirmed, report the shortlist instead of guessing - a skipped symbol is
   safer than a wrong signature.
