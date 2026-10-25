---
name: find-OnServerVoiceData_IsPlayingDemo_Callee
description: |
  Generate the Windows-only OnServerVoiceData_IsPlayingDemo_Callee patch YAML from
  IVEngineClient2_IsPlayingDemo.windows.yaml using a deterministic preprocessor script.
  Use when locating the IVEngineClient2::IsPlayingDemo indirect call inside
  C_ServerVoiceHandler::OnServerVoiceData without LLM decompilation.
  Trigger: OnServerVoiceData IsPlayingDemo callee, voice demo call patch, IsPlayingDemo callsite
disable-model-invocation: true
---

# OnServerVoiceData_IsPlayingDemo_Callee Patch Workflow

## Overview

This Windows-only patch finder converts the already-generated
`IVEngineClient2_IsPlayingDemo.windows.yaml` vfunc metadata into
`OnServerVoiceData_IsPlayingDemo_Callee.windows.yaml`.

The target call site is inside `C_ServerVoiceHandler::OnServerVoiceData`:

```asm
mov     rcx, cs:g_pSource2EngineToClient
mov     rax, [rcx]
call    qword ptr [rax+150h]    ; IVEngineClient2::IsPlayingDemo
test    al, al
jz      short loc_...
```

The patch address is the address of the indirect `call` instruction itself.

## Prerequisite

The following input YAML must already exist in the current client module output directory:

```text
IVEngineClient2_IsPlayingDemo.windows.yaml
```

Its required fields are:

```yaml
func_name: IVEngineClient2_IsPlayingDemo
vtable_name: IVEngineClient2
vfunc_offset: '0x150'
vfunc_index: 42
vfunc_sig: FF 90 50 01 00 00 84 C0 74 ?? 83 FD ??
```

## Deterministic Preprocessor

Run through the configured `ida_analyze_bin.py` pipeline. The corresponding script is:

```text
ida_preprocessor_scripts/find-OnServerVoiceData_IsPlayingDemo_Callee.py
```

The script performs these checks without LLM invocation:

1. Rejects every platform except Windows.
2. Reads the input vfunc YAML from the current client output directory.
3. Verifies the function name, vtable name, and `vfunc_offset / 8 == vfunc_index` relationship.
4. Verifies that `vfunc_sig` starts with the concrete encoding of
   `call qword ptr [rax+vfunc_offset]`.
5. Calls IDA MCP `find_bytes` with the full `vfunc_sig` and requires exactly one match.
6. Writes the match address as `patch_va`, derives `patch_rva` from the image base,
   copies `vfunc_sig` to `patch_sig`, and writes `patch_sig_disp: 0`.

## Output

For game version `14173`, the expected output is:

```yaml
patch_name: OnServerVoiceData_IsPlayingDemo_Callee
patch_va: '0x180aec45d'
patch_rva: '0xaec45d'
patch_sig: FF 90 50 01 00 00 84 C0 74 ?? 83 FD ??
patch_sig_disp: 0
```

No `patch_bytes` field is generated because this skill identifies the callee call site;
the downstream consumer decides how that call instruction is patched.

## Failure Conditions

Stop and report failure when any of the following occurs:

- The input YAML is missing or malformed.
- The vfunc offset and index disagree.
- The signature does not begin at the expected indirect call.
- The signature has zero or multiple matches.
- The match address or image base is invalid.
