---
name: find-CBaseEntity_GetChangeAccessorPathInfo_1
description: |
  Find and identify the CBaseEntity_GetChangeAccessorPathInfo_1 virtual function in CS2 binary using IDA Pro MCP.
  Use this skill when reverse engineering CS2 server.dll or libserver.so to locate the second
  GetChangeAccessorPathInfo override by scanning CBaseEntity vtable slots near the known
  CBaseEntity_GetChangeAccessorPathInfo_2 slot for an implementation identical to CBaseEntity_GetChangeAccessorPathInfo_2.
  Trigger: CBaseEntity_GetChangeAccessorPathInfo_1
disable-model-invocation: true
---

# Find CBaseEntity_GetChangeAccessorPathInfo_1

Locate `CBaseEntity_GetChangeAccessorPathInfo_1` vfunc in CS2 `server.dll` or `libserver.so` using IDA Pro MCP tools.

## Background

`CBaseEntity` overrides two separate `CEntityInstance` interface methods, `GetChangeAccessorPathInfo_1` and
`GetChangeAccessorPathInfo_2`, with **byte-for-byte identical implementations** (both simply forward to the same
internal lazy-init helper at the same member offset). Because the source bodies are identical, the compiler may
fold both vtable slots onto the exact same function address, or it may still emit two separate but structurally
identical functions. `CBaseEntity_GetChangeAccessorPathInfo_2` is already resolved (it inherits its vtable slot
from `CEntityInstance_GetChangeAccessorPathInfo_2`); `CBaseEntity_GetChangeAccessorPathInfo_1` occupies a
**different** slot within +/-2 entries of it in the same `CBaseEntity` vtable.

## Method

### 1. Load CBaseEntity_GetChangeAccessorPathInfo_2 from YAML

**ALWAYS** Use SKILL `/get-func-from-yaml` with `func_name=CBaseEntity_GetChangeAccessorPathInfo_2`.

If the skill returns an error, **STOP** and report to user.

Otherwise, extract:
- `func_va` (the reference implementation address)
- `vfunc_index`
- `vfunc_offset`
- `vtable_name` (should be `CBaseEntity`)

### 2. Load CBaseEntity VTable from YAML

**ALWAYS** Use SKILL `/get-vtable-from-yaml` with `class_name=CBaseEntity`.

If the skill returns an error, **STOP** and report to user.

Otherwise, extract:
- `vtable_numvfunc`
- `vtable_entries`

### 3. Enumerate Candidate Slots

Compute the scan window around the known slot:

- `window_start = max(0, CBaseEntity_GetChangeAccessorPathInfo_2.vfunc_index - 2)`
- `window_end = min(vtable_numvfunc - 1, CBaseEntity_GetChangeAccessorPathInfo_2.vfunc_index + 2)`

For every index `i` in `[window_start, window_end]` **except** `CBaseEntity_GetChangeAccessorPathInfo_2.vfunc_index`
itself, read the candidate function address `vtable_entries[i]`.

### 4. Check for Identical-Address Folding First

Compilers (MSVC `/OPT:ICF`, GCC/Clang identical code folding) commonly merge functions with byte-identical bodies
into a single implementation, so multiple vtable slots end up pointing at the **same address**.

For each candidate index `i`:
- If `vtable_entries[i] == CBaseEntity_GetChangeAccessorPathInfo_2.func_va`, this slot is folded onto the same
  implementation and is an immediate match. Record `i` as `target_vfunc_index` and stop scanning further.

### 5. Otherwise, Decompile and Compare Candidates

If no candidate address matched directly, decompile the reference function and every remaining candidate:

```text
mcp__ida-pro-mcp__decompile addr="<CBaseEntity_GetChangeAccessorPathInfo_2_func_va>"
mcp__ida-pro-mcp__decompile addr="<candidate_func_addr>"
```

#### Windows (`server.dll`)

The reference implementation is a one-line forwarder:

```c
__int64 __fastcall CBaseEntity_GetChangeAccessorPathInfo_2(__int64 a1)
{
  return sub_180184630(a1 + 56);
}
```

A matching candidate must be **structurally identical**:
1. Takes a single `(__int64 a1)` argument (this only)
2. Directly tail-calls the exact same helper address as the reference (e.g. `sub_180184630`)
3. Passes the exact same constant offset argument (`a1 + 56`)
4. Returns the helper's result unchanged

#### Linux (`libserver.so`)

The reference implementation is a lazy-init pattern:

```c
__int64 __fastcall CBaseEntity_GetChangeAccessorPathInfo_2(__int64 a1)
{
  __int64 result;
  ...
  result = *(_QWORD *)(a1 + 64);
  if ( !result )
  {
    result = operator new(384);
    ...
    *(_QWORD *)(a1 + 64) = result;
  }
  return result;
}
```

A matching candidate must:
1. Read/write the exact same member offset as the reference (`a1 + 64`)
2. Allocate the exact same size via `operator new` (`384`)
3. Initialize the same set of fixed fields at the same relative offsets (`+56`, `+24`, `+40`, `+48`, `+96` .. `+352`, etc.)
4. Return the same lazily-initialized pointer

### 6. Confirm the Match

Among the scanned candidates (excluding the known `_2` slot), exactly one should match either by identical address
(Step 4) or by identical decompiled structure (Step 5). That candidate is `CBaseEntity_GetChangeAccessorPathInfo_1`.

If zero or more than one candidate match, **STOP** and report to user.

### 7. Write IDA Analysis Output as YAML

**ALWAYS** Use SKILL `/write-vfunc-as-yaml` to write the analysis results.

Required parameters:
- `func_name`: `CBaseEntity_GetChangeAccessorPathInfo_1`
- `func_addr`: `<matched_func_addr>`
- `func_sig`: `None`
- `vfunc_sig`: `None`

VTable parameters:
- `vtable_name`: `CBaseEntity`
- `vfunc_offset`: `<target_vfunc_index * 8>` in hex
- `vfunc_index`: `<target_vfunc_index>`

## Function Characteristics

- **Purpose**: Lazily creates/returns the change-accessor path-info object for this entity; implementation is
  identical to `CBaseEntity_GetChangeAccessorPathInfo_2`, distinguished only by its vtable slot
- **Binary**: `server.dll` / `libserver.so`
- **Parameters**: `(this)` only
- **Return value**: Pointer to the lazily-allocated path accessor object stored at a fixed member offset

## Discovery Strategy

1. Reuse the existing `CBaseEntity_GetChangeAccessorPathInfo_2` YAML to obtain the reference address and known slot
2. Reuse the existing `CBaseEntity_vtable` YAML to scan the +/-2 neighboring slots
3. Prefer an identical-address (ICF-folded) match; fall back to structural decompile comparison
4. Generate a stable `func_sig` from the resolved candidate body

This is robust because:
- The two overrides are guaranteed byte-identical in source, so either the compiler folds them to one address or
  their decompiled structure will be indistinguishable except for the vtable slot
- Scanning a narrow +/-2 window avoids false positives from unrelated vtable entries
- The final YAML stores both the resolved function signature and the precise vtable metadata

## Output YAML Format

The output YAML filename depends on the platform:
- `server.dll` -> `CBaseEntity_GetChangeAccessorPathInfo_1.windows.yaml`
- `libserver.so` -> `CBaseEntity_GetChangeAccessorPathInfo_1.linux.yaml`
