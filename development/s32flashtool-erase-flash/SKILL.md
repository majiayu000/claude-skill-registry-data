---
name: s32flashtool-erase-flash
description: Erase a range of supported flash memory on an NXP S32 device using either S32FlashTool CLI or S32FlashTool GUI via RPC.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index", "s32flashtool-rpc-api"]'
  tags: '["s32flashtool", "cli", "gui", "rpc", "flash", "erase", "destructive"]'
---

# S32FlashTool Erase Flash Memory Range

Erase a selected range of flash memory on a supported NXP S32 target.

This skill supports **two execution modes**:

- **CLI mode** using:
  - the `cli_build_<op>` + `cli_execute` actions
  - or another dedicated erase-capable MCP tool if one is introduced later
- **GUI mode** using S32FlashTool GUI over RPC:
  - the matching `gui_*` action

This skill is **operation-focused**:
- it explains what the erase operation needs
- how to choose GUI vs CLI
- how to execute erase in each mode
- how to validate the outcome
- how to handle destructive-operation confirmation safely

> Names shown in tool-call snippets below are routing hints. Confirm current parameter names and enum values via `search_actions(query="<action_name>", detailed=true, limit=1)`. See `s32flashtool-agent-rules-minimal`.

## When to use

Use this skill when the user wants to:
- erase, clear, or blank a range of flash memory / eeprom on an NXP S32 device
- clear part of flash before reprogramming it
- blank a specific sector or region
- trigger the S32FlashTool GUI erase-range workflow through RPC

## When not to use

Do **not** use this skill for:
- reading flash contents -> use `s32flashtool-read-flash`
- reading RCON/EEPROM -> use `s32flashtool-read-rcon`
- programming/writing/uploading a file into flash -> use `s32flashtool-upload-file-to-flash`
- writing hex bytes into RCON/EEPROM -> use `s32flashtool-write-rcon`
- executing a binary from SRAM -> use `s32flashtool-sram`
- identifying the processor -> use `s32flashtool-read-mcuid`

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct operation skill.

## Quickstart

1. Select mode  see `## Mode selection policy`
2. Gather inputs  see `## Required inputs` (use discovery calls from `## Preconditions`)
3. Preview the operation  CLI: `preview_only=true`; GUI: show payload
4. Obtain confirmation phrase "yes, erase"  see `## Guardrails` (Destructive actions)
5. Execute  `references/CLI.md` or `references/GUI.md`
6. Validate  see `## Validation loop`

## Mode selection policy

Choose execution mode as follows:

1. If the user explicitly asks for **GUI**, **window**, **RPC**, or **S32FlashTool GUI**, use the **GUI/RPC flow**.
2. If the user explicitly asks for **CLI**, **command line**, **shell**, or requests a command, use the **CLI flow**.
3. If the user does not specify GUI or CLI:
   - prefer a preview-first CLI flow using the `cli_build_<op>` + `cli_execute` actions
4. If the user previously established a working GUI RPC session and continues issuing GUI-style requests, continue with RPC.
5. Do not silently switch from GUI to CLI or from CLI to GUI.
6. If the requested behavior is only possible through the other mode, explain the fallback before doing it.

## Preconditions

Before erasing, ensure:

1. The S32FlashTool installation folder is known.
2. The target binary exists and matches the processor family.
3. The flash algorithm exists and matches the flash device.
4. The communication interface is known:
   - `uart`
   - `can`
   - `ethernet`
5. The communication endpoint is known.
6. The board is connected and powered.
7. The board is in **serial boot mode** for S32FlashTool communication.
8. If a different target/algorithm was used previously, a board reset / restart into serial boot may be necessary.

### Recommended preparation
Use concrete discovery tool calls instead of guessing. The following hints map each precondition to a tool call:

- List candidate target binaries:
  - `list_platform_files` action (bin_type="target").
- List candidate flash algorithms:
  - `list_platform_files` action (bin_type="flash").
- Confirm device / algorithm / interface support before any hardware-specific action:
  - `list_platform_files` action (bin_type="supported") and read the matching `supported_<platform>_devices.txt`.
- Inspect board-specific examples and PDFs if useful:
  - `list_platform_files` action (bin_type="blob")
  - `list_platform_files` action (bin_type="example_pdf").
- Discover available communication ports if the port is unknown:
  - the `cli_build_<op>` + `cli_execute` actions with `list_ports=true`.
- Identify the processor on the connected board when family is uncertain:
  - apply skill `s32flashtool-read-mcuid` (uses `cli_build_mcuid` + `cli_execute`).
- Capture current flash content before erasing if it may be needed later:
  - `cli_build_fread` + `cli_execute` over the same `addr`/`size` range.

Do not invent values for `target`, `algorithm`, `port`, or `addr`/`size`. Use the discovery calls above or ask the user.

## Required inputs

Collect or confirm the following:

- `s32flashtool_folder`
- `target`
- `algorithm`
- `interface`
- `port`
- `addr`
- `size`

### Optional inputs

- `file_path`
- `extra_args`

## Input rules

- Do not guess the target binary.
- Do not guess the flash algorithm.
- Do not guess the COM port.
- Use absolute file paths if a file path is provided for size derivation.
- `addr` and `size` may be decimal or hexadecimal.
- For NOR flash devices, erase may operate on flash sectors or blocks, not on arbitrary byte ranges.
- Never omit `size` and never use `size=0`; ask the user if unknown.
- Do not claim that only the exact requested byte range will be erased unless documentation proves that behavior.
- For GUI workflows, numeric strings may be normalized by the GUI. Treat that as normal unless the semantic value changed incorrectly.

## GUI / RPC flow

See [references/GUI.md](references/GUI.md) for the full GUI / RPC flow, payloads, and example sequences.

## CLI flow

See [references/CLI.md](references/CLI.md) for the full CLI flow, parameters, and example MCP calls.

## Validation loop

After erasing, validation may include:

- checking that the erase action completed successfully
- reading back the region to inspect erased data
- verifying expected erased pattern for the flash type
- reprogramming and verifying known content afterward

### Practical validation examples
- run a read-back of the erased region
- inspect whether the data matches the expected blank state for the flash/device
- compare before/after read-back if one was captured earlier

## Failure modes

Recognize these failures from tool output and respond accordingly. Never auto-retry a destructive operation. On any failure, report the exact tool output before proposing next steps.

| # | Failure | Symptom | Interpretation | Response |
|---|---|---|---|---|
| 1 | User-aborted erase (GUI) | `flash.clickEraseMemoryRange` returns OK but GUI dialog cancelled or reports aborted | RPC click dispatched; operation did not complete | Report as user-cancelled; ask whether to retry. Do not claim success. |
| 2 | Target / algorithm mismatch | Algorithm does not match device; flash not detected; device ID mismatch | Wrong `target` and/or `algorithm` for the board or flash device | Stop. Re-run `list_platform_files` action (bin_type="supported") and consult `supported_<platform>_devices.txt`. If family uncertain, apply `s32flashtool-read-mcuid` first. Do not guess a new algorithm. |
| 3 | Oversize range / boundary cross | Tool reports range exceeds flash size, crosses region boundary, or unmapped address | `addr + size` out of range for configured flash | Do not silently clip. Confirm geometry from `supported_<platform>_devices.txt`. Ask user to restate `addr`/`size` or confirm a full-device erase. |
| 4 | Missing initialization (GUI/RPC) | `flash.clickEraseMemoryRange` fails; destination reported as not initialized | `init.clickLaunchInitialization` was skipped or failed for `FLASH`/`RCON` | Call `init.clickLaunchInitialization` before retrying. If init itself fails, treat as row 2 or row 5. |
| 5 | Communication / boot-mode / path errors | Port not open; no response; file-not-found on `target`/`algorithm` paths | Wrong `port`, board not in serial boot, previous session used a different target/algo, or bad paths | Verify `target`/`algorithm` paths, `interface`, `port`, `addr`, `size`, boot mode. Confirm serial boot mode. If a different algorithm ran previously, ask the user to reset the board into serial boot. |
| 6 | GUI/RPC unavailable | `hello` fails or RPC endpoint unreachable | GUI not running or RPC disabled | Do not launch a second GUI blindly; follow launch procedure in `s32flashtool-rpc-api`. Explain unavailability and ask whether CLI fallback is acceptable. |
| 7 | Sector-granularity surprise (not a failure) | Erase succeeded but a region larger than `size` is now blank | Device erases in sectors/blocks; requested range rounded up to containing sector(s) | Report the **actual** erased region, not the requested one. Do not claim byte-granular erase. |

## Guardrails

**Scope**
- Only erase a specified flash range on a supported NXP S32 target using either
  the `cli_build_<op>` + `cli_execute` actions (CLI) or the matching `gui_*` action (GUI/RPC).
- Do not program files, do not execute SRAM images from this skill.
  Recovery: hand off to the correct sibling skill.

**Destructive actions (confirmation contract)**
- Erase is destructive and may affect a larger sector/block than the requested byte range on
  sector-based flash. Always **preview** first: print target, algorithm, interface, port, start
  address, size, and the sector-alignment warning.
- Before the actual erase step, summarize the intended operation and warn that erase may affect
  a larger flash block or sector than the requested byte range depending on flash geometry.
- Require an **explicit user confirmation phrase** (e.g. "yes, erase") before invoking the erase
  action. This applies to **both** CLI and GUI/RPC flows. Recovery: if the user hesitates, stop;
  do not erase.
- Never mix GUI and CLI in the same erase invocation. Recovery: pick one mode up front.

**Refuse-and-escalate**
- Missing/ambiguous target, algorithm, interface, port, address, or size: stop and ask.
- Board not in serial boot mode, or a previous session used a different target/algorithm: ask the
  user to reset the board into serial boot before retrying.
- RPC GUI: if `hello` fails, do not launch a second GUI blindly; follow the launch procedure in
  `s32flashtool-rpc-api`. Never use `communicationDevice = UART`; use `COM` with values like
  `COM15,ftdi` in `comPort`.

**Output contract**
- Report the erased range, and the tool's
  exit status. Do not claim success without a positive response from the tool.

## Out of scope

- Byte-granular erase on sector-based flash. This skill respects the device's
  native erase granularity.
- also see `## When not to use`

## Examples

- intentionally push examples into `references/*.md`
