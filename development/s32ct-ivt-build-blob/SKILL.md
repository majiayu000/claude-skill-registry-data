---
name: s32ct-ivt-build-blob
description: >
  Builds a bootable IVT blob image with S32 Configuration Tools from one or
  more raw application binaries, for any NXP S32 family MCU (S32K1, S32K3,
  S32G, S32R, S32M, S32Z, S32E, S32S, S32N) and any installed Platform SDK
  / RTD version. Trigger phrases: "build a blob", "create a blob image",
  "make a boot image", "bundle CM7 cores into one image", "wrap application
  binaries into the IVT", "export -ExportBlob", or otherwise produce a
  single bootable image the boot ROM (BAF / BootROM / SBAF) can flash and
  consume. Data-model driven - the workflow discovers pointer names per
  MCU, so it works without knowing family-specific labels. Preferred over
  calling `-ExportBlob` directly, which produces a header-only IVT
  (per-pointer `size` defaults to 4 bytes); this skill encodes the
  coordinated `.mex` edits needed to embed payloads and to disable
  colliding HSE/DCD defaults.
license: LA_OPT_Online Code Hosting NXP_Software_License
allowed-tools: Read, Write, Edit, Bash(python:*), Bash(powershell:*)
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-cli, s32ct-get-version]'
  tags: '[s32ct, ivt, blob, boot-image, code-signing, hse, configuration]'
---

# S32CT IVT Blob Builder

Builds a bootable IVT blob (header + embedded payloads) from raw
application binaries. Wraps `nxp_s32ct_execute_action(action_name="s32ct.configure_ivt", params={...})` with
the coordinated `.mex` edits `-ExportBlob` requires: setting each payload
pointer's `size` to the binary's byte length, wiring `file_path` +
`start_address` + `reserved="false"`, and flipping any default-active
pointer (typically HSE_B / HSE_H firmware) that would collide with the
payload region. Portable across MCUs because Step 1 discovers the pointer
names from the on-disk data model.

## When to use

Use this skill when producing a bootable blob from raw binaries. Typical
phrasings:

- "Build a blob image for my S32K374 with these three CM7 binaries at ..."
- "Bundle the bootloader + DCD into one S32G274 boot image"
- "Export `-ExportBlob` for ..."
- "I have these binaries and addresses - make me a flash image"
- "Wrap my cluster apps into the IVT for S32Z270"

Do **not** use this skill for:

- Reading or analysing an existing blob (use a hex viewer or
  `nxp_s32flashtool_get_file_content`).
- Modifying an existing `.mex` without re-exporting a blob (use
  `nxp_s32ct_execute_action(action_name="s32ct.configure_ivt", params={...})` directly).
- Programming flash (use the `nxp_s32flashtool` extension).
- HSE key provisioning or image signing (upstream tooling).

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Workflow | Build blob (5-step recipe) | See Quickstart |
| Script | Patch `.mex` pointers (Step 3) | `scripts/patch_mex_pointers.py` |
| Script | Verify emitted blob (Step 5) | `scripts/verify_blob.ps1` (Windows) or `scripts/verify_blob.py` (any platform) |
| Reference | Full authoring procedure | `references/authoring-blob.md` |
| Reference | Per-family pointer table | `references/pointer_quick_reference.md` |

## Quickstart

Run the five steps in order. Each is idempotent. Leave the intermediate
`.mex` on disk so a failed run can be inspected and re-tried surgically.
Full narrative, decision matrix, worked S32K374 example, family notes,
and failure-mode catalog live in `references/authoring-blob.md`.

1. **Discover pointer names** (read-only). Read
   `<mcu_data_root>/processors/<mcu>/<sdk_version>/ivt/<mcu>.xml`
   (`mcu_data_root` from `nxp_s32ct_execute_action(action_name="s32ct.env_status", params={})`). Every
   `payloads[i].pointer_name` must match a `<ivt_pointer name="...">`
   verbatim - case-sensitive.

2. **Create the skeleton `.mex`**:

   ```python
   nxp_s32ct_execute_action(
       action_name="s32ct.configure_ivt",
       params={
           "empty_config": True,
           "mcu": "<mcu>", "sdk_version": "<sdk_version>",
           "config_name": "<config_name>",   # default "blob"
           "enable_tool": True,
           "set_values": ["cm7_0=true"],     # -SetValue clobber rule below
           "export_kind": "ExportMEX",
           "output_dir": "<work_dir>", "data_dir": "<work_dir>/ws",
       },
   )
   ```

   `-SetValue` clobber rule: when several enables share a bitfield
   (e.g. `cm7_0`, `cm7_1`, `cm7_2` on S32K3), only the first persists.
   Set one here; edit siblings directly in Step 3b.

3. **Patch the `.mex`** - the heart of the recipe. Three classes of
   edits (details in `references/authoring-blob.md`):

   - **3a** For each payload pointer: set `size` to binary byte length,
     `start_address` to the requested address, `file_path` to the
     absolute path, `reserved="false"`.
   - **3b** For each same-bitfield sibling: edit `<setting name="cm7_1"
     value="true"/>` etc. directly.
   - **3c** For each name in `disable_pointers`: set `reserved="true"`.

   Use `scripts/patch_mex_pointers.py` for a deterministic run.

4. **Export the blob** - Attempt 1 without `-AutoAlign`:

   ```python
   nxp_s32ct_execute_action(
       action_name="s32ct.configure_ivt",
       params={
           "project_path": "<work_dir>/<config_name>.mex",
           "enable_tool": True, "export_kind": "ExportBlob",
           "output_dir": "<output_dir>", "data_dir": "<work_dir>/ws",
       },
   )
   ```

   On `segment overlaps with: <name>` -> add that name to
   `disable_pointers` and re-run from Step 3. On alignment complaint ->
   fix `payloads[i].address` or fall back to Attempt 2 with
   `auto_align=""` (decision matrix in `references/authoring-blob.md`).

5. **Verify** with `scripts/verify_blob.ps1 -IvtBase {ivt_base}
   -Pointers @(...)` on Windows, or the cross-platform
   `python3 scripts/verify_blob.py --ivt-base {ivt_base} --pointer
   NAME:OFFSET:ADDRESS[:BINARY] ...` elsewhere.
   **Exit code 0 does NOT mean a blob was produced**
   - always parse stderr for `BLOB Image Export failed.` before
   reporting success.

## Guardrails

**Scope** - Writes the blob to `<output_dir>` and the skeleton `.mex` to
`<work_dir>`. Does not touch the live target. Does not sign binaries.

**Destructive actions** - Overwrites `<output_dir>/blobImage` and
`<work_dir>/<config_name>.mex` on re-run. Wipe `<work_dir>/ws` between
runs to shed cached Eclipse workspace state.

**Code-signing / HSE safety** - Does not perform HSE key provisioning,
image signing, or any cryptographic operation.

> **WARNING - Device lockout risk:** Leaving the HSE firmware pointer
> active (default state) while not actually programming HSE firmware
> reserves flash that will remain unprogrammed. After fuse burning
> this can leave the device permanently locked. Always add the HSE
> pointer to `disable_pointers` when HSE is not in use:
> `HSE_B Firmware Image` on S32K3/S32Z/E, `HSE_H Firmware` on S32G.

When HSE *is* in use, its firmware image is a payload like any other;
signing happens upstream via the HSE Secure Boot flow, never here.

**Refuse-and-escalate** - Refuse when any `pointer_name` does not match
a `<ivt_pointer name="...">` in the MCU's data model (list the legal
names), when a `binary_path` is missing, when `address` isn't hex, or
when the exporter emits `BLOB Image Export failed.` on exit 0. Do not
silently add `-AutoAlign` - surface the overlap / alignment error and
prompt the user to disable the colliding pointer or fix the address.

**Pointer verification** - Every emitted blob is verified against six
criteria (file existence, size larger than the IVT header, magic bytes
at the start, pointer-slot addresses match the requested ones, disabled
pointers read the expected sentinel, first bytes at the payload address
match the source binary). A verification failure blocks "success"
reporting even when the tool exit is 0. Full check details are in the
Validation loop section below.

## Validation loop

1. Pointer names in `payloads` all match `<ivt_pointer name="...">`
   entries in `<mcu>.xml` verbatim.
2. Every `binary_path` exists and is readable.
3. Skeleton `.mex` writes to `<work_dir>/<config_name>.mex`.
4. Step 3 edits are present: every payload pointer has `size` != `"4"`,
   `file_path` != `"N/A"`, `reserved="false"`; each `disable_pointers`
   entry has `reserved="true"`.
5. Attempt 1 exports without `-AutoAlign`; stderr is scanned for
   `BLOB Image Export failed.`, `segment overlaps with:`, and
   alignment complaints.
6. Verifier passes all six checks: (a) file at `<output_dir>/blobImage`,
   (b) size > IVT header (~5 KB minimum on K3), (c) magic `A5 5A A5 5A`
   at `0x00`, (d) each pointer slot holds the requested LE address,
   (e) disabled pointers read `0xFFFFFFFF` (or family sentinel),
   (f) first ~16 bytes at `(address - ivt_base)` match the source
   binary.
7. Pass criterion: verifier prints PASS for all six AND stderr is clean
   of `BLOB Image Export failed.`.

## Out of scope

- HSE key provisioning and image signing.
- Flash programming (see `nxp_s32flashtool`).
- Modifying pointer addresses via `-SetValue` - that writes bitfield
  `<setting>` nodes, not `<ivt_pointer>` rows. Pointer addresses are
  only writable via direct XML edit (or the GUI).
- Analysing an existing blob.
- Multi-MCU or multi-SDK batching in one call.

## See Also

- `references/authoring-blob.md` - full procedure, decision matrix,
  worked S32K374 example, family notes, failure-mode catalog.
- `references/pointer_quick_reference.md` - extended per-family pointer
  table (sanity check only; the XML data model is source of truth).
- `scripts/patch_mex_pointers.py` - Step 3 implementation.
- `scripts/verify_blob.ps1` - Step 5 verifier (Windows PowerShell).
- `scripts/verify_blob.py` - Step 5 verifier (cross-platform Python;
  same four checks and exit codes).
- Related skills: `s32ct-cli` (generic dispatcher fallback),
  `s32ct-peripherals-info` / `s32ct-clocks-info` (read-only inspectors),
  `nxp_s32flashtool` (program the emitted blob),
  `s32ct.sanitize` (clean cross-refs when grafting).
