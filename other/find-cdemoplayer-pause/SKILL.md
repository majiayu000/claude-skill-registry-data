---
name: find-CDemoPlayer_Pause
description: |
  Agent fallback for CDemoPlayer_Pause (auto-generated, category: vfunc). Locate
  CDemoPlayer::Pause in the CS2 engine module via IDA Pro MCP and emit a fresh,
  minimal-unique artifact. The deterministic preprocessor could not resolve this
  symbol on the current gamever - your job is the re-sign.
  Trigger: CDemoPlayer_Pause, CDemoPlayer::Pause
disable-model-invocation: true
---

# Find CDemoPlayer_Pause

Target: `CDemoPlayer::Pause` (vfunc) in the module loaded in THIS session.

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

Write `CDemoPlayer_Pause.{platform}.yaml` with EXACTLY these fields:

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
