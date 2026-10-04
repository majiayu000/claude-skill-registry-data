---
name: find-ILoopMode_LoopInit
description: |
  Agent fallback for ILoopMode_LoopInit (auto-generated, category: vfunc). Locate
  ILoopMode::LoopInit in the CS2 server module via IDA Pro MCP and emit a fresh,
  minimal-unique artifact. The deterministic preprocessor could not resolve this
  symbol on the current gamever - your job is the re-sign.
  Trigger: ILoopMode_LoopInit, ILoopMode::LoopInit
disable-model-invocation: true
---

# Find ILoopMode_LoopInit

Target: `ILoopMode::LoopInit` (vfunc) in the module loaded in THIS session.

> The old artifact/preprocessor anchors no longer match this build. Use anchors
> only to *locate* candidates; derive the artifact from the ACTUAL bytes you read.
> Produce ONLY this session's platform output. NEVER open another binary.

## Method

Resolve the owning class vtable via RTTI (typeinfo-name string -> _ZTI object
-> vtable). Identify the slot by xrefs from expected call sites. Slots commonly
differ between platforms - never assume identical indices.

## Mandatory self-check before emitting

The pipeline re-reads the bytes at your `func_va` and regenerates `func_sig` from
them - a mismatch aborts the run. Therefore: read the real bytes via IDA MCP,
derive the artifact FROM those bytes (wildcard relocated operands as `??`), start
at the TRUE function head, and only then write the YAML. A mismatch is always a
bug in YOUR output.

## Output schema (STRICT)

Write `ILoopMode_LoopInit.{platform}.yaml` with EXACTLY these fields:

```yaml
func_name: <TASK>
func_va: "<hex virtual address>"
func_rva: "<hex rva>"
func_size: "<hex size>"
vtable_name: <owning class RTTI name>
vfunc_offset: "<hex vtable byte offset>"
vfunc_index: <decimal slot index>
```
NEVER include func_sig.

## Verification

1. Decompile and confirm the behavior matches the symbol's semantics.
2. Uniqueness: the pattern must match exactly ONE location in the loaded binary.
3. If no candidate can be confirmed, report the shortlist - a skipped symbol is
   safer than a wrong signature.
