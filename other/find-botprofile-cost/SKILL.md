---
name: find-BotProfile_Cost
description: |
  Locate BotProfile::Cost in CS2 server.dll / libserver.so via IDA Pro MCP and emit a fresh, minimal-unique
  signature or offset for the local gamedata entry "BotProfile::Cost" (symbol BotProfile_Cost). This is a VIRTUAL function - resolve the BotProfile::Cost vtable via RTTI and identify the
  slot, then emit the slot. Verify by xrefs from expected call sites. vtable slots
  commonly differ between platforms - never assume identical indices.
  Trigger: BotProfile_Cost, BotProfile::Cost
disable-model-invocation: true
---

# Find BotProfile_Cost

Target: `BotProfile::Cost` (vfunc) in the CS2 server module.

> Do NOT anchor on raw byte patterns from older releases - they shift. Use anchors only to *locate*
> the function, then generate a fresh minimal-unique function-head signature with relocated bytes
> wildcarded. Produce ONLY the output file(s) listed in this skill's expected outputs, for the binary
> loaded in THIS session (one platform per run). NEVER open or analyze the other platform's binary.

## Method

This is a VIRTUAL function - resolve the BotProfile::Cost vtable via RTTI and identify the
slot, then emit the slot. Verify by xrefs from expected call sites. vtable slots
commonly differ between platforms - never assume identical indices.

## Mandatory self-check before emitting

The pipeline re-reads the bytes at your `func_va` and deterministically regenerates `func_sig` from
them - if your `func_sig` does not match those bytes EXACTLY (with `??` matching anything), the run
aborts. Therefore:

1. After picking the function, read the actual bytes at `func_va` via the IDA MCP.
2. Derive `func_sig` FROM those bytes: keep stable opcode bytes literally, wildcard relocated or
   variable operands as `??`.
3. `func_sig` MUST start at `func_va` (the true function head).
4. Only then write the YAML. A mismatch is always a bug in YOUR output, never in the pipeline.


## Struct-member alternative (choose the TRUTHFUL schema)

If investigation shows the target is NOT a vtable slot but a plain struct member of a
non-polymorphic class (no RTTI/vtable exists for the class), emit the structmember schema
instead:

```yaml
struct_name: <owning class name>
member_name: <member name>
offset: "<hex byte offset as string>"
size: <member size in bytes, decimal>
offset_sig: "<short byte pattern of an instruction touching the offset>"
```

A truthful structmember artifact is always accepted; a guessed vfunc artifact is not.

## Output schema (STRICT)

Write the YAML file `<symbol>.{platform}.yaml` with EXACTLY these fields:
```yaml
func_name: <SYMBOL_NAME>
func_va: "<hex virtual address>"
func_rva: "<hex rva>"
func_size: "<hex size>"
vtable_name: <owning class RTTI name>
vfunc_offset: "<hex vtable byte offset>"
vfunc_index: <decimal slot index>
```
NEVER include func_sig.

## Verification

1. Decompile the candidate and confirm the behavior matches the purpose above (not a caller or callee).
2. Confirm uniqueness: the generated pattern must match exactly one location in the loaded binary.
3. If a candidate cannot be confirmed, report the shortlist instead of guessing - a skipped symbol is
   safer than a wrong signature.
