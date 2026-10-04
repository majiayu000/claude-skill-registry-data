---
name: find-UpdateItemView
description: |
  Find and identify the UpdateItemView function in CS2 server binary using IDA Pro MCP. Use this skill
  when reverse engineering CS2 server.dll or libserver.so to locate the CEconItemView cache-rebuild
  routine that must run after an econ item's definition or attributes change for the change to take
  visual effect (e.g. after weaponpaints mutates an item's attributes). Resolved by shortlisting the
  handful of functions that reference the internal "kill eater" econ-attribute literal and matching the
  one with the item-view attribute-rebuild body shape.
  Trigger: UpdateItemView, CEconItemView_UpdateItemView
disable-model-invocation: true
---

# Find UpdateItemView

Locate `UpdateItemView` in CS2 `server.dll` or `libserver.so` using IDA Pro MCP tools.

This is a **non-virtual, direct-call** member function (no vtable entry — emit a byte sig, not an
offset).

> **Do not** anchor the discovery recipe on the raw byte pattern below — bytes/wildcards shift release to
> release. Use it only to *locate/confirm* the function on the currently loaded binary, then generate a
> fresh signature at the end.

## Method

### 1. Shortlist candidates via the "kill eater" econ-attribute literal

`UpdateItemView` rebuilds a `CEconItemView`'s live `CAttributeList` from its item definition's static
attribute templates, and as part of that it does a one-time cached symbol lookup of the literal string
`"kill eater"` (used to special-case the kill-eater-score-type bonus while rebuilding). This string is
rare enough (only a handful of referencers in the whole module) to make a good shortlist anchor:

```
mcp__ida-pro-mcp__find       type="string" targets=["kill eater"]
mcp__ida-pro-mcp__xrefs_to   addrs="<string_va>"
```

> Linux 14168 reference: `"kill eater"` (VA `0x9117cc`) has exactly **5** code referencers module-wide:
> `sub_1380E50`, `sub_1A9A070` (the paint-kit/wear/seed applier — see the sibling skill
> `find-CAttributeList_SetOrAddAttributeValueByName`, which is its **caller-side** cross-check), `sub_1B31540`,
> `sub_1B52030`, and `sub_1B598F0` (the target, `UpdateItemView`).

### 2. Decompile each candidate and match the UpdateItemView body shape

```
mcp__ida-pro-mcp__decompile addr="<candidate_func_va>"
```

`UpdateItemView` is the one candidate matching **all** of:

1. **Exactly two parameters**, no obvious name-string argument: `(CEconItemView *pItemView, KeyValues
   *pkvOverride /* usually 0 */)`. (Rules out `sub_1380E50`, which takes six parameters, and
   `sub_1A9A070`, which takes `(this, pWeaponEntity)` and calls the attribute *setter* by literal name
   instead of rebuilding a list.)
2. **Opens with a get-or-create fallback for the second argument**: roughly `if (!a2) { a2 = *(this +
   0x60); if (!a2) a2 = GetOrCreateStaticData(); }`.
3. **Guarded one-time symbol cache init** for `"kill eater"`: a `byte_XXXXX` flag gates a
   `RegisterSymbol(&cache, "kill eater")` call, so the literal is loaded through a cached global rather
   than passed around as an argument (distinguishes it from `sub_1A9A070`, which passes `"kill eater"`
   directly as a call argument to the attribute setter).
4. **Iterates the item definition's static-attribute-template array** (read off the object's
   `CEconItemDefinition*`), and for each entry that passes a "kill-eater eligible" flag check, resolves a
   kill-eater score-type bonus via a red-black-tree-style lookup before building the attribute.
5. **Builds and appends attribute entries** into a `CUtlVector`-like paged buffer embedded in the object
   (construct-attribute helper followed by a pair of "list changed" notify calls with distinct reason
   codes — one for element-added, one for rebuild-finished), reallocating via the engine allocator
   (`g_pMemAlloc`) as needed.

> Linux 14168 reference: `sub_1B598F0` (VA `0x1b598f0`, size `0x630`) matches all five criteria. It is
> called from several weapon/item-spawn sites (e.g. `sub_13A6500`, `sub_145F380`, `sub_154D280`,
> `sub_1AF3B50`) always as `UpdateItemView(pItemViewOffset, 0)` immediately after the item view's
> underlying item definition/index is (re)initialized — consistent with "must run whenever the item's
> definition or attributes change" semantics.

### 3. Generate function signature

**ALWAYS** use SKILL `/generate-signature-for-function` with `addr=<UpdateItemView_func_addr>`. Emit IDA
style verbatim (space hex, `?` wildcards).

Reference sig (Linux 14168 build — sanity check only, regenerate per binary):
`55 49 89 F0 48 89 E5 41 57 41 56 49 89 FE 41 55 41 54 53 48 81 EC`

(Last-resort fallback note: if no better anchor is available on some future binary, `find_bytes` with
this reference pattern can locate the function directly one-shot — its prologue is distinctive enough on
its own — but prefer the string-shortlist + body-shape anchor above since it survives compiler/prologue
changes better.)

### 4. Write func YAML

**ALWAYS** use SKILL `/write-func-as-yaml`:
- `func_name`: `UpdateItemView`
- `func_addr`: `<UpdateItemView_func_addr>`
- `func_sig`: validated sig from step 3

## Function Characteristics

- **Purpose**: Rebuilds/refreshes a `CEconItemView`'s cached display/attribute state (its live
  `CAttributeList`) from its underlying item definition's static attribute templates. Must be called
  whenever an econ item's definition index or attributes are mutated for the change to take visual/
  gameplay effect — e.g. after a weaponpaints-style plugin changes an item's paint-kit/wear/seed
  attributes via `CAttributeList_SetOrAddAttributeValueByName`, `UpdateItemView` should run for the item
  to reflect the new attributes.
- **Linkage**: non-virtual, direct-call (no vtable entry).
- **Binary**: `server.dll` / `libserver.so`
- **Parameters**: `(this /* CEconItemView* */, KeyValues *pkvOverride /* optional, commonly 0 */)`
- **Return value**: implementation-defined status (callers generally ignore it)
- **Sibling relationship**: called from the same family of weapon/item-spawn setup code that also calls
  `CAttributeList_SetOrAddAttributeValueByName`'s caller-side attribute applier (both operate on a
  `CEconItemView`'s attribute state around item give/equip time), though the two are not called from the
  exact same function on this build — cross-check by confirming both are reachable from item-give/model-
  select code paths rather than expecting a literal shared caller.

## Discovery Strategy

1. `"kill eater"` is a rare, first-party econ-attribute literal (not a debug-only string) with only a
   handful of referencers module-wide, making it a cheap, durable shortlist filter.
2. `UpdateItemView` is uniquely identified within that shortlist by its distinctive **body shape** — a
   guarded one-time symbol-cache init of the literal (rather than passing it as a call argument), a
   get-or-create fallback for its optional second parameter, an item-definition static-attribute-template
   iteration, and a "construct + append + dual list-changed-notify" attribute rebuild pattern — none of
   which depend on exact addresses or byte offsets.
3. Cross-checking against its callers (item/weapon setup routines that call it as `(pItemView, 0)`
   immediately after (re)initializing the item's definition/index) gives an independent confirmation that
   survives the callee's own address moving between builds.
4. The final byte signature is always regenerated fresh from the resolved function rather than pinned to
   this build's bytes.

This is robust because the shortlist anchor string is a gameplay literal unlikely to be stripped, the
body-shape checks are compiler/inlining-tolerant, and the caller cross-check does not depend on any single
hard-coded caller address.

## Output YAML Format

- `server.dll`   -> `UpdateItemView.windows.yaml`
- `libserver.so` -> `UpdateItemView.linux.yaml`

Fields: `func_name`, `func_va`, `func_rva`, `func_size`, `func_sig`.
