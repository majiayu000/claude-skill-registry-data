---
name: find-KickBotFromTeam
description: |
  Locate KickBotFromTeam in CS2 server.dll / libserver.so via IDA Pro MCP and emit a fresh, minimal-unique
  signature or offset for the local gamedata entry "KickBotFromTeam" (symbol KickBotFromTeam). The gamedata consumer stores a BYTE SIGNATURE for this entry - ALWAYS emit the func
  schema (func_sig), never vfunc fields. The function may be virtual; locating it via
  the owning class vtable (RTTI) is a fine strategy, but once found, read its head bytes
  and emit func_sig. Locate via cross-references, distinctive constants/strings, callers
  of related symbols, or vtable slots; verify by decompilation before committing.
  Trigger: KickBotFromTeam, KickBotFromTeam
disable-model-invocation: true
---

# Find KickBotFromTeam

Target: `KickBotFromTeam` (func) in the CS2 server module.

> Do NOT anchor on raw byte patterns from older releases - they shift. Use anchors only to *locate*
> the function, then generate a fresh minimal-unique function-head signature with relocated bytes
> wildcarded. Produce ONLY the output file(s) listed in this skill's expected outputs, for the binary
> loaded in THIS session (one platform per run). NEVER open or analyze the other platform's binary.

## Method

`KickBotFromTeam(int team) -> bool` is a free function (no `this`). Its only callers are in
`CCSBotManager_MaintainBotQuota` (input artifact): 6 call sites on linux, 5 on windows, with
team 3, 2 and 0. Anchor on the `KickBotFromTeam(0)` call there: a direct `call` right after
`xor edi, edi` (linux) / `xor ecx, ecx` (windows). Other calls in that function also take 0
(the bot-add helper, the human counters), so confirm the candidate:
- it walks player slots, tests `m_fFlags & 0x100` (FL_FAKECLIENT) on the controller
  (linux +0x669 bit 0 / windows +0x388) and the controller team (+0x624 / +0x344);
- its tail calls the engine through vtable `+0x308` (IVEngineServer2::KickClient, slot 97)
  with the immediate 39 (NETWORK_DISCONNECT_KICKED) as the reason and returns 1.
14196: linux 0xc09c40, windows 0x1802e7800.

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
