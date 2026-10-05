---
name: s32flashtool-read-flash
description: Read a region of flash memory from a supported NXP S32 device using either S32FlashTool CLI or S32FlashTool GUI via RPC.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index", "s32flashtool-rpc-api"]'
  tags: '["s32flashtool", "cli", "gui", "rpc", "flash", "read", "read-only"]'
---

# S32FlashTool Read Flash Memory

Read a region of flash memory from a supported NXP S32 target.

This skill supports **two execution modes**:

- **CLI mode** using:
  - `cli_build_fread` + `cli_execute`
  - or the `cli_build_<op>` + `cli_execute` actions as fallback / preview path
- **GUI mode** using S32FlashTool  GUI over RPC:
  - the matching `gui_*` action

This skill is **operation-focused**:
- it explains what the read operation needs
- how to choose GUI vs CLI
- how to execute the read in each mode
- how to validate the outcome

> Names shown in tool-call snippets below are routing hints. Confirm current parameter names and enum values via `search_actions(query="<action_name>", detailed=true, limit=1)`. See `s32flashtool-agent-rules-minimal`.

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct operation skill.
- For GUI automation rules, also apply `s32flashtool-rpc-api/SKILL.md`.

## Quickstart

1. Select mode  see `## Mode selection policy`
2. Gather inputs  see `## Required inputs` (use discovery calls from `## Preconditions`)
3. Execute  `references/CLI.md` or `references/GUI.md`
4. Validate  see `## Validation loop`

## Mode selection policy

Choose execution mode as follows:

1. If the user explicitly asks for **GUI**, **window**, **RPC**, or **S32FlashTool GUI**, use the **GUI/RPC flow**.
2. If the user explicitly asks for **CLI**, **command line**, **shell**, or requests a command, use the **CLI flow**.
3. If the user does not specify GUI or CLI:
   - prefer the dedicated MCP tool `cli_build_fread` + `cli_execute`
   - do not silently switch to GUI unless the user requested GUI behavior
4. If the user previously established a working GUI RPC session and continues issuing GUI-style requests, continue with RPC.
5. Do not silently switch from GUI to CLI or from CLI to GUI.
6. If the requested behavior is only possible through the other mode, explain the fallback before doing it.

## When to use this skill

Use this skill when the user wants to:

- read flash contents from an address range
- dump memory from flash
- inspect bytes from flash
- read flash into the console
- save a flash region into a file
- validate written data by reading it back manually

## When not to use this skill

Do **not** use this skill when:

- the user wants to **program/write/upload** data  
  -> use `s32flashtool-upload-file-to-flash`
- the user wants to **erase** flash  
  -> use skill `s32flashtool-erase-flash`
- the user wants to **verify against a file using compare/verify semantics**  
  -> use CRC compare (skill `s32flashtool-compute-crc-and-compare-to-flash`) or verify workflow if available
- the user wants to read **RCON/EEPROM specifically**  
  -> use skill `s32flashtool-read-rcon`

## Preconditions

Before reading flash, ensure:

1. The S32FlashTool installation folder is known.
2. The target binary exists and matches the processor family.
3. The flash algorithm exists and matches the flash device.
4. The communication interface is known:
   - `uart`
   - `can`
   - `ethernet`
5. The communication endpoint is known:
   - for UART: e.g. `COM15,ftdi`
6. The board is connected and powered.
7. The board is in the correct boot mode for S32FlashTool communication.
8. For serial/UART workflows, the board is typically placed in **serial boot mode**.
9. If a different target/algorithm was used previously, a board reset / restart into serial boot may be necessary.

### Recommended preparation
- Check supported target/algorithm combinations using the supported-device documentation.
- If needed, read MCUID first to help identify the processor family.
- If the port is not known, discover it before reading.

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
- `file_path` for save-to-file workflows
- `binary_output` / `binaryMode`
- `extra_args` only if explicitly needed

## Input rules

- Do not guess the target/device compatibility.
- Do not guess the flash algorithm.
- Do not guess the COM port.
- Use absolute file paths when a file path is provided.
- `addr` and `size` may be decimal or hexadecimal.
- For GUI workflows, numeric strings may be normalized by the GUI (for example `0x100` may display as `100`). Treat that as normal unless the value itself changes incorrectly.
- For large reads, avoid excessive sizes unless the user explicitly requests them.
- Do not silently switch between GUI and CLI.
- Do not use raw shell commands instead of MCP tools.
- Do not use `communicationDevice = UART` in RPC GUI workflows.
- Do not invent RPC actions or model keys.
- Do not claim read success without checking tool response.
- Do not impose an artificial 24-byte limit for general flash reads. That limitation applies to RCON/EEPROM-style workflows, not general flash memory reads.

## GUI / RPC flow

See [references/GUI.md](references/GUI.md) for the full GUI / RPC flow, payloads, and example sequences.

## CLI flow

See [references/CLI.md](references/CLI.md) for the full CLI flow, parameters, and example MCP calls.

## Validation loop

After a successful read, validation may include:

- confirming the command or RPC action completed successfully
- checking that the output size matches the requested size
- checking that the file was created when reading to a file
- inspecting the output bytes
- comparing the read-back data with expected content if provided by the user

### Practical validation examples
- confirm `read_back.bin` exists
- inspect the first bytes in hex
- compare against a known file or expected pattern
- rerun a small targeted read if needed

## Failure modes

Recognize these failures from tool output and respond accordingly. Read is non-destructive, so a bounded retry after correcting inputs is acceptable, but incorrect interpretation of a failed read can mislead downstream decisions. On any failure, report the exact tool output before proposing next steps.

| # | Failure | Symptom | Interpretation | Response |
|---|---|---|---|---|
| 1 | Target / algorithm mismatch | Algorithm does not match device; flash not detected; device ID mismatch; implausible content (all `0xFF` on a known-programmed device) | Wrong `target` and/or `algorithm` for the board or flash device | Stop. Re-run `list_platform_files` action (bin_type="supported") and consult `supported_<platform>_devices.txt`. If family uncertain, apply `s32flashtool-read-mcuid` first. Do not present the returned bytes as evidence of flash content until identification is correct. |
| 2 | Read range exceeds flash / crosses unmapped region | Tool reports range exceeds flash size, crosses region boundary, or unmapped/reserved address | `addr + size` out of range for the configured flash | Do not silently clip the range. Confirm geometry from `supported_<platform>_devices.txt`. Ask the user to restate `addr`/`size` within a valid range. |
| 3 | File-write failure when saving to disk | Read reports bytes OK, but the output file is missing, empty, or the tool logs a file-write error | Parent folder of `file_path` missing, path not writable, or disk full; the device read likely succeeded but the file-write step failed independently | Do not report the read as failed on the device side. Confirm the parent folder exists and is writable. Ask for a different absolute output path under a known-writable directory. Do not re-issue the device read solely to fix a filesystem problem. |
| 4 | Missing initialization (GUI/RPC) | `flash.clickDownloadFromDevice` fails; destination reported as not initialized | `init.clickLaunchInitialization` was skipped or failed for `FLASH`/`RCON` | Call `init.clickLaunchInitialization` before retrying. If init itself fails, treat as row 1 or row 5. |
| 5 | Communication / boot-mode / path errors | Port not open; no response; file-not-found on `target`/`algorithm` paths | Wrong `port`, board not in serial boot, previous session used a different target/algo, or bad paths | Verify `target`/`algorithm` paths, `interface`, `port`, `addr`, `size`, boot mode. Confirm serial boot mode. If a different algorithm ran previously, ask the user to reset the board into serial boot. |
| 6 | GUI/RPC unavailable | `hello` fails or RPC endpoint unreachable | GUI not running or RPC disabled | Do not launch a second GUI blindly; follow the launch procedure in `s32flashtool-rpc-api`. Explain unavailability and ask whether CLI fallback is acceptable. |

## Quick decision summary

- **User asked for GUI / S32FlashTool window / RPC**  
  -> use GUI/RPC flow

- **User asked for CLI / command line / shell**  
  -> use CLI flow

- **User did not specify**  
  -> prefer `cli_build_fread` + `cli_execute`

- **User wants read into a file**  
  -> GUI: `fullConfigDownloadFromDeviceToFile`  
  -> CLI: `cli_build_fread` + `cli_execute` with `file_path`

- **Board/boot uncertainty**  
  -> pause and clarify serial boot / hardware setup

## Guardrails

**Scope**
- Only read a flash range on a supported NXP S32 target using `cli_build_fread` + `cli_execute`, the `cli_build_<op>` + `cli_execute` actions, or the documented GUI/RPC read-flash flow.
- Do not use for RCON/EEPROM (use `s32flashtool-read-rcon`), do not program, do not erase.

**Destructive actions**
- Read-only. If the user follows up with a write/erase request, hand off to the matching sibling skill and confirm there.

**Refuse-and-escalate**
- Missing target, algorithm, interface, port, address, or size: stop and ask.
- Board not in serial boot mode, or previous session used a different target/algorithm: ask the user to reset the board before retrying.
- RPC GUI: use `communicationDevice = COM`, never `UART`. Reuse the session if `hello` succeeds.
- Do not impose an artificial 24-byte cap for general flash reads; that limit belongs to RCON/EEPROM.

**Output contract**
- Return the tool's raw byte output (or the exact file path when saving to file), plus the requested range and size. Do not claim read success without a positive tool response.

## Out of scope

- see `## When not to use this skill`
- Enforcing the 24-byte RCON-style limit on general flash reads. This skill reads arbitrary flash ranges.

## Examples

- intentionally push examples into `references/*.md`
