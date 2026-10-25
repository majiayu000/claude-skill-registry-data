---
name: find-CEntitySystem_Init-decompiles
description: |
  Final-guarantee fallback for the find-CEntitySystem_Init-decompiles preprocessor. Recovers the struct
  members, indirect virtual-function offsets, and de-inlined helpers that CEntitySystem::Init sets up, by
  decompiling CEntitySystem_Init in CS2 server.dll / libserver.so and following de-inlined callees when a
  target is no longer accessed directly. Use this skill when the deterministic/LLM preprocessor
  (ida_preprocessor_scripts/find-CEntitySystem_Init-decompiles.py) could not resolve every target because a
  member or vfunc was inlined or de-inlined in a way the LLM_DECOMPILE references do not cover.
  Trigger: CEntitySystem_m_sEntSystemName, CEntitySystem_m_eNetworkSerializationMode, CEntitySystem_m_Symbols,
  CEntitySystem_m_ComponentUnserializerInfoAllocator, CEntitySystem_m_pNetworkFieldChangedEventQueue,
  CEntitySystem_m_pNetworkFieldScratchData, CEntitySystem_m_pFieldChangeLimitSpew,
  CEntitySystem_m_EntityMaterialAttributes, INetworkMessages_SetNetworkSerializationContextData,
  IFlattenedSerializers_CreateFieldChangedEventQueue, CEntitySystem_ProcessEntityRegistration
disable-model-invocation: true
---

# Find CEntitySystem_Init-decompiles (final-guarantee fallback)

Recover every symbol that `CEntitySystem::Init` wires up, in CS2 `server.dll` / `libserver.so`, using IDA Pro
MCP tools. This is the **Agent fallback** for the `find-CEntitySystem_Init-decompiles` skill: it only runs when
the preprocessor script returned failure, which almost always means one target's access pattern **moved** —
either it was inlined into `CEntitySystem_Init` where the reference expected a separate function, or it was
de-inlined out of `CEntitySystem_Init` into a helper the reference does not know about.

Your job is to produce the missing output YAMLs regardless of that inline/de-inline boundary.

## Realworld Function References

Read the platform-relevant real-world YAMLs before searching in IDA. They provide concrete disassembly,
decompiler output, semantic anchors, and both sides of the known inline/de-inline boundary. Treat their
addresses and offsets as reference-build values only; verify every result against the current binary.

- Windows inline baseline: `ida_preprocessor_scripts/references/server/CEntitySystem_Init.windows.yaml`
- Linux baseline: `ida_preprocessor_scripts/references/server/CEntitySystem_Init.linux.yaml`
- Windows de-inlined `CEntitySystem_Init` variant:
  `ida_preprocessor_scripts/references/server/CEntitySystem_Init-noinline.windows.yaml`
- Windows de-inlined material helper:
  `ida_preprocessor_scripts/references/server/CEntitySystem_InitEntityMaterialAttributes.windows.yaml`
- Linux registration helper:
  `ida_preprocessor_scripts/references/server/CEntitySystem_ProcessEntityRegistration.linux.yaml`

## Background — what CEntitySystem_Init does

`CEntitySystem_Init(this, const char *name, int a3, int mode, char a5)` is a long constructor-style routine.
Along the way it:

- copies the system name into `this->m_sEntSystemName`;
- stores the serialization `mode` into `this->m_eNetworkSerializationMode`;
- initializes `this->m_ComponentUnserializerInfoAllocator` (a `CUtlScratchMemoryPool`);
- registers all entity/component classes;
- calls `g_pNetworkMessages->SetNetworkSerializationContextData("string_t_table", m_eNetworkSerializationMode, &m_Symbols)`
  through the **`INetworkMessages` vtable** (an indirect virtual call);
- when `m_eNetworkSerializationMode` is set, allocates a `CNetworkFieldScratchData` into
  `this->m_pNetworkFieldScratchData` and calls
  `g_pFlattenedSerializers->CreateFieldChangedEventQueue(m_pNetworkFieldScratchData, m_pFieldChangeLimitSpew)`
  through the **`IFlattenedSerializers` vtable**, storing the result into `this->m_pNetworkFieldChangedEventQueue`;
- (Linux) tail-calls the de-inlined `CEntitySystem_ProcessEntityRegistration`;
- (Windows) runs the entity-material-attributes registration loop that touches `this->m_EntityMaterialAttributes`.

All member accesses are **relative to `this`** (the first argument — `rcx` on Windows, `rdi` on Linux — usually
copied to `rsi`/`rbx`). This is the key to robustness: `this + offset` is stable whether the access sits in
`CEntitySystem_Init` itself or in a helper that received `this` as its first argument.

## Robustness principle — follow the de-inline boundary

For **every** target below:

1. First look for its access pattern **inside `CEntitySystem_Init`**.
2. If it is not there, it has been **de-inlined into a callee**. Enumerate the functions that
   `CEntitySystem_Init` calls (read the pseudocode / disassembly and collect each `sub_*` / named `call`
   target), decompile the plausible ones, and search there. The owning helper takes `this` (the
   `CEntitySystem *`) as its first parameter, so the same `this + offset` pattern appears. Recurse one or two
   levels if needed.
3. Conversely, a target the reference expected in a **separate function** (e.g. Linux
   `CEntitySystem_ProcessEntityRegistration`, or Windows `m_EntityMaterialAttributes`) may have been **inlined
   back into `CEntitySystem_Init`** — in that case find the pattern directly in `CEntitySystem_Init`.

Anchor each target by its **semantic fingerprint** (the strings, constants, and neighboring calls listed
below), not by a fixed address or a fixed containing function.

## Output inventory

`struct_name` is always `CEntitySystem`. Offsets are **reference values from the 14168 build — verify against
the binary, do not assume**; they change across updates and differ per platform.

| # | Output symbol | Kind | Windows | Linux | Writer skill |
|---|---------------|------|---------|-------|--------------|
| 1 | `CEntitySystem_m_sEntSystemName` | struct member | `0xA88` | `0xA88` | `/write-structoffset-as-yaml` |
| 2 | `CEntitySystem_m_eNetworkSerializationMode` | struct member | `0xBBC` | `0xBBC` | `/write-structoffset-as-yaml` |
| 3 | `CEntitySystem_m_ComponentUnserializerInfoAllocator` | struct member | `0xCB8` | `0xCC0` | `/write-structoffset-as-yaml` |
| 4 | `CEntitySystem_m_Symbols` | struct member | `0x1EC8` | `0x1ED0` | `/write-structoffset-as-yaml` |
| 5 | `CEntitySystem_m_pNetworkFieldChangedEventQueue` | struct member | `0xC80` | `0xC88` | `/write-structoffset-as-yaml` |
| 6 | `CEntitySystem_m_pNetworkFieldScratchData` | struct member | `0xC88` | `0xC90` | `/write-structoffset-as-yaml` |
| 7 | `CEntitySystem_m_pFieldChangeLimitSpew` | struct member | `0xC90` | `0xC98` | `/write-structoffset-as-yaml` |
| 8 | `INetworkMessages_SetNetworkSerializationContextData` | indirect vcall | vtable `INetworkMessages`, offset `0xA0`, index `20` | same | `/write-vfunc-as-yaml` |
| 9 | `IFlattenedSerializers_CreateFieldChangedEventQueue` | indirect vcall | vtable `IFlattenedSerializers`, offset `0x118`, index `35` | same | `/write-vfunc-as-yaml` |
| 10 | `CEntitySystem_ProcessEntityRegistration` | function | *inlined — do NOT emit* | separate func (`func_sig`) | `/write-func-as-yaml` |
| 11 | `CEntitySystem_m_EntityMaterialAttributes` | struct member | `0x2070` | *inlined — do NOT emit* | `/write-structoffset-as-yaml` |

Platform gating: symbols 1–9 are produced on **both** platforms. Symbol 10 is **Linux-only** (on Windows the
routine is inlined into `CEntitySystem_Init`). Symbol 11 is **Windows-only** (on Linux the access lives inside
`CEntitySystem_ProcessEntityRegistration`, symbol 10).

## Step 0. Skip targets already produced

Some outputs may already exist beside the binary — written by the preprocessor before it failed, or by the
`find-CEntitySystem_InitEntityMaterialAttributes` / `find-CEntitySystem_m_EntityMaterialAttributes` fallback
pair that runs before this skill. For each output, if `<name>.<platform>.yaml` already exists next to the
binary and parses to a non-empty mapping, **skip it** and spend effort only on the missing ones. You can list
the binary directory with:

```
mcp__ida-pro-mcp__py_eval code="import idaapi, os; d=os.path.dirname(idaapi.get_input_file_path()); print('\n'.join(sorted(f for f in os.listdir(d) if f.endswith('.yaml'))))"
```

`/get-func-from-yaml` also reports existence for functions/vfuncs (returns an error when absent).

## Step 1. Load and decompile the predecessor

**ALWAYS** Use SKILL `/get-func-from-yaml` with `func_name=CEntitySystem_Init` to obtain its `func_va`.

If the skill returns an error, **STOP** and report to user (this fallback cannot run without the predecessor).

Decompile it, and keep the list of functions it calls for the de-inline search in later steps:

```
mcp__ida-pro-mcp__decompile addr="<CEntitySystem_Init.func_va>"
```

Confirm the `this` register (first argument) and note where it is copied (typically `rsi` on Windows, `rbx` on
Linux). Every struct-member offset below is `this + offset`.

## Step 2. Resolve the struct members

For each member: locate the access, read the **displacement** in the instruction (that is the offset), confirm
it is relative to `this` (the `CEntitySystem *`), and confirm `struct_name = CEntitySystem`. Then generate a
signature and write the YAML (Step 5).

### 2a. `m_sEntSystemName`

The very first meaningful call in `CEntitySystem_Init`:

```c
CUtlString::Set((CUtlString *)(this + 0xA88), name);   // name == arg a2
```

Anchor: the `lea`/`add` that forms `this + off` immediately before the `CUtlString::Set` call whose second
argument is the incoming name string. `off` is `m_sEntSystemName` (ref `0xA88`).

### 2b. `m_eNetworkSerializationMode`

The **int/enum** mode stored from the `mode` parameter (`a4`) near the top:

```c
*(_DWORD *)(this + 0xBBC) = mode;                      // ref 0xBBC
```

It is read again later as the middle argument to the `SetNetworkSerializationContextData` vcall (Step 3a),
right next to the `"string_t_table"` string — that read site is an equally good anchor.

> Decoy: a **byte** flag `*(_BYTE *)(this + 0xBDA) = (a3 == 1 && g_pNetworkMessages != nullptr)` is set a few
> instructions away. That `0xBDA` boolean is **not** `m_eNetworkSerializationMode` — the target is the DWORD at
> `0xBBC`. Do not confuse them.

### 2c. `m_ComponentUnserializerInfoAllocator`

The `CUtlScratchMemoryPool` initialized near the top:

```c
CUtlScratchMemoryPool::Init((CUtlScratchMemoryPool *)(this + 0xCB8/*win*/), 0x400, 0, nullptr, 0);
```

Anchor: the `lea rcx/rdi, [this + off]` feeding the `CUtlScratchMemoryPool::Init` call whose first immediate is
`0x400`. `off` is `m_ComponentUnserializerInfoAllocator` (ref `0xCB8` Windows / `0xCC0` Linux).

### 2d. `m_Symbols`

The last argument to the `SetNetworkSerializationContextData` vcall (Step 3a):

```c
g_pNetworkMessages->SetNetworkSerializationContextData("string_t_table", m_eNetworkSerializationMode, this + 0x1EC8/*win*/);
```

Anchor: the `lea` that forms `this + off` as the third argument, in the block that also loads
`"string_t_table"`. `off` is `m_Symbols` (ref `0x1EC8` Windows / `0x1ED0` Linux).

### 2e. The field-change trio — `m_pNetworkFieldScratchData`, `m_pFieldChangeLimitSpew`, `m_pNetworkFieldChangedEventQueue`

All three live in the `if (m_eNetworkSerializationMode)` block, around the `CreateFieldChangedEventQueue` vcall
(Step 3b):

```c
// m_pNetworkFieldScratchData: object from operator new(0x58) with a CNetworkFieldScratchData vtable,
// stored at this + off, and passed as the 1st data argument to CreateFieldChangedEventQueue.
*(_QWORD *)(this + 0xC88/*win*/) = scratch;            // ref 0xC88 win / 0xC90 linux

m_pNetworkFieldChangedEventQueue =                     // stored from the vcall's return value
    g_pFlattenedSerializers->CreateFieldChangedEventQueue(
        m_pNetworkFieldScratchData,                    // this + 0xC88 win / 0xC90 linux
        m_pFieldChangeLimitSpew);                       // this + 0xC90 win / 0xC98 linux
*(_QWORD *)(this + 0xC80/*win*/) = <return value>;     // m_pNetworkFieldChangedEventQueue, ref 0xC80 win / 0xC88 linux
```

Distinguish them by role:

- `m_pNetworkFieldScratchData` — the object **written** just above the call (the `operator new(0x58)` result with
  a vtable) and read as the vcall's **second** argument (`rdx`/2nd data reg). Ref `0xC88` win / `0xC90` linux.
- `m_pFieldChangeLimitSpew` — read as the vcall's **third** argument (`r8`/3rd data reg). Ref `0xC90` win /
  `0xC98` linux.
- `m_pNetworkFieldChangedEventQueue` — the member the vcall's **return value** is stored into. Ref `0xC80` win /
  `0xC88` linux.

> These three signatures may need to span a function boundary (the block is easily de-inlined). If
> `/generate-signature-for-structoffset` cannot find a unique signature, it is acceptable to write the member
> with the **offset only** (omit `offset_sig`) — the offset is the required output.

## Step 3. Resolve the indirect virtual-call offsets

Symbols 8 and 9 are **indirect virtual calls**, not concrete functions. The YAML records the interface vtable
and slot, and a `vfunc_sig` that pins the call instruction — there is **no `func_va`**. Do not try to resolve a
concrete implementation address.

For each: find the `call qword ptr [reg + disp]` instruction, take `vfunc_offset = disp` and
`vfunc_index = disp / 8`.

### 3a. `INetworkMessages_SetNetworkSerializationContextData`

- Call site: `call qword ptr [reg + 0xA0]` where `reg` holds `g_pNetworkMessages` (type `INetworkMessages *`),
  in the block that loads the `"string_t_table"` string and passes `m_eNetworkSerializationMode` and
  `&m_Symbols`.
- `vtable_name = INetworkMessages`, `vfunc_offset = 0xA0` (ref), `vfunc_index = 20`.

### 3b. `IFlattenedSerializers_CreateFieldChangedEventQueue`

- Call site: `call qword ptr [reg + 0x118]` where `reg` holds `g_pFlattenedSerializers`
  (type `IFlattenedSerializers *`), passing `m_pNetworkFieldScratchData` and `m_pFieldChangeLimitSpew`, with the
  return stored into `m_pNetworkFieldChangedEventQueue`.
- `vtable_name = IFlattenedSerializers`, `vfunc_offset = 0x118` (ref), `vfunc_index = 35`.

`g_pNetworkMessages` and `g_pFlattenedSerializers` are already-named globals in the database; use their type to
confirm the interface, and confirm the semantic role from the neighboring arguments described above. If the
whole call has been de-inlined into a helper, follow the callees (Robustness principle) — the `[reg + disp]`
instruction and its argument setup move together.

## Step 4. Platform-specific de-inlined targets

### 4a. Linux only — `CEntitySystem_ProcessEntityRegistration` (symbol 10)

On Linux, `CEntitySystem_Init` tail-calls this de-inlined helper near its end (after the class-table loop):

```c
CEntitySystem_ProcessEntityRegistration(this);         // last call before Init returns
```

Anchor: the last `call` in `CEntitySystem_Init` that takes only `this`. Decompile it to confirm it performs the
entity-material-attributes registration (the FNV-1a hashing loop over material names — constants
`0x811C9DC5` and `0x1000193`). Rename it to `CEntitySystem_ProcessEntityRegistration` with
`mcp__ida-pro-mcp__rename`, then treat it as a normal function (Step 5c).

> If (on some future Windows build) this routine is emitted as a **separate function** too, apply the same
> method on Windows. On the current Windows build it is inlined into `CEntitySystem_Init` — do **not** emit it
> there.

### 4b. Windows only — `m_EntityMaterialAttributes` (symbol 11)

On Windows this member is accessed inside the material-attributes loop, whether that loop is inlined in
`CEntitySystem_Init` or de-inlined into `CEntitySystem_InitEntityMaterialAttributes` (a helper taking `this`):

```c
lea reg, [this + 0x2070]                                // ref 0x2070 = m_EntityMaterialAttributes
```

Anchor: the `lea this + off` used as the map/dictionary base in the loop that FNV-1a-hashes material name
strings (constants `0x811C9DC5`, `0x1000193`; a small default string blob is the hash seed). Follow the callees
of `CEntitySystem_Init` if the loop is not inlined. `off` is `m_EntityMaterialAttributes` (ref `0x2070`).

> On Linux this access lives inside `CEntitySystem_ProcessEntityRegistration` (symbol 10) and is **not** emitted
> as a separate member YAML.

## Step 5. Generate signatures and write the YAMLs

### 5a. Struct members (symbols 1–7, and 11 on Windows)

For each resolved member:

1. **ALWAYS** Use SKILL `/generate-signature-for-structoffset` on the instruction that contains the offset to
   obtain `offset_sig` / `offset_sig_disp`. (Best-effort for the field-change trio — see the note in Step 2e.)
2. **ALWAYS** Use SKILL `/write-structoffset-as-yaml` with:
   - `struct_name`: `CEntitySystem`
   - `member_name`: the member (e.g. `m_sEntSystemName`)
   - `offset`: the resolved hex offset
   - `size`: `None`
   - `offset_sig`: the signature from step 1 (or `None` if not found)
   - `offset_sig_disp`: from step 1 (or `None`)

### 5b. Indirect vcalls (symbols 8–9)

For each:

1. **ALWAYS** Use SKILL `/generate-signature-for-vfuncoffset` on the `call qword ptr [reg + offset]` instruction
   to obtain `vfunc_sig` (the offset bytes are fixed in the signature; `vfunc_sig_disp` is `0`).
2. **ALWAYS** Use SKILL `/write-vfunc-as-yaml` with:
   - `func_name`: e.g. `INetworkMessages_SetNetworkSerializationContextData`
   - `vtable_name`: `INetworkMessages` / `IFlattenedSerializers`
   - `vfunc_offset`: the resolved offset (`0xA0` / `0x118`)
   - `vfunc_index`: `vfunc_offset / 8` (`20` / `35`)
   - `vfunc_sig`: from step 1
   - `func_addr`: `None`   (no concrete implementation address for an interface vcall)
   - `func_sig`: `None`

### 5c. Function (symbol 10, Linux only)

1. **ALWAYS** Use SKILL `/generate-signature-for-function` with `addr=<CEntitySystem_ProcessEntityRegistration_addr>`.
2. **ALWAYS** Use SKILL `/write-func-as-yaml` with:
   - `func_name`: `CEntitySystem_ProcessEntityRegistration`
   - `func_addr`: the resolved address
   - `func_sig`: the validated signature from step 1

## Failure handling

- If the **predecessor** `CEntitySystem_Init` YAML is missing → **STOP** and report to user.
- If an individual required target cannot be located even after following callees → resolve the ones you can,
  then **STOP** and report exactly which output(s) could not be found, so the user can extend the references.
- Never emit a platform-gated symbol on the wrong platform (symbol 10 Windows, symbol 11 Linux).

## Output YAML filenames

Written beside the binary by the writer skills, one file per symbol:

- Windows (`server.dll`): `<symbol>.windows.yaml`
- Linux (`libserver.so`): `<symbol>.linux.yaml`

e.g. `CEntitySystem_m_Symbols.windows.yaml`, `INetworkMessages_SetNetworkSerializationContextData.linux.yaml`,
`CEntitySystem_ProcessEntityRegistration.linux.yaml`, `CEntitySystem_m_EntityMaterialAttributes.windows.yaml`.

## Why this is robust

- Members are anchored to `this + offset`, so they are recoverable whether the access is inlined in
  `CEntitySystem_Init` or de-inlined into a helper that receives `this`.
- Each target has a **semantic fingerprint** (a string, a constant, a neighboring interface call) that survives
  offset changes and function-boundary moves across updates.
- The indirect vcalls are pinned by their call-site displacement, which is stable even when the surrounding code
  is reorganized.
- Already-produced outputs are skipped, so this fallback composes with the preprocessor and with the
  windows de-inline fallback pair instead of fighting them.
