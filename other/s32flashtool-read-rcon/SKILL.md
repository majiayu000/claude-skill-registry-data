---
name: s32flashtool-read-rcon
description: Read the RCON/EEPROM region from a supported NXP S32 device using either S32FlashTool CLI or S32FlashTool GUI via RPC.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index", "s32flashtool-rpc-api"]'
  tags: '["s32flashtool", "cli", "gui", "rpc", "rcon", "eeprom", "read", "read-only"]'
---

# S32FlashTool Read RCON/EEPROM

Read the RCON/EEPROM region from a supported NXP S32 target.

This skill supports **two execution modes**:

- **CLI mode** using:
  - `cli_build_fread` + `cli_execute`
  - or the `cli_build_<op>` + `cli_execute` actions as fallback / preview path
- **GUI mode** using S32FlashTool  GUI over RPC:
  - the matching `gui_*` action

This skill is **operation-focused**:
- it explains what the RCON/EEPROM read operation needs
- how to choose GUI vs CLI
- how to execute the read in each mode
- how to validate the outcome

## When to use this skill

Use this skill when the user wants to:

- read RCON contents
- read EEPROM contents used as RCON configuration
- inspect boot configuration bytes stored in RCON/EEPROM
- dump RCON/EEPROM contents to console
- save the RCON/EEPROM region to a file

## Do not use this skill when

Do **not** use this skill when:

- the user wants general flash reading  
  -> use `s32flashtool-read-flash`
- the user wants to **program/write/upload** RCON/EEPROM data  
  -> use the corresponding write/program workflow
- the user wants to **erase** flash  
  -> use skill `s32flashtool-erase-flash`
- the user only wants to identify the processor  
  -> skill `s32flashtool-read-mcuid`

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct operation skill.
- For GUI automation rules, also apply `s32flashtool-rpc-api/SKILL.md`.

## Quickstart

1. Select mode  see `## Mode selection policy`
2. Gather inputs  see `## Required inputs` (use discovery calls from `## Preconditions`)
   - RCON-specific: algorithm is `RCON.bin`; keep `addr = 0x0` and `size <= 24` unless documentation proves otherwise (see `## Address and size constraints`)
3. Execute  `references/CLI.md` or `references/GUI.md`
4. Validate  see `## Validation`

## Operation mapping

**User intent:** read / dump / inspect / download RCON or EEPROM contents

### GUI / RPC mapping
- Config key: `fullConfigDownloadFromDevice`
- Final action: `flash.clickDownloadFromDevice`
- Alternate config for save-to-file: `fullConfigDownloadFromDeviceToFile`
- Alternate final action: `flash.clickDownloadFromDeviceToFile`
- Destination: `EEPROM (RCON)`
- Requires initialization: **yes**

### CLI mapping
- Preferred tool: `cli_build_fread` + `cli_execute`
- Expert fallback: `cli_build_fread` + `cli_execute`
- Required algorithm type: `RCON.bin`

### Safety
- Destructive: **no**
- Confirmation required: **no**

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

## Preconditions

Before reading RCON/EEPROM, ensure:

1. The S32FlashTool installation folder is known.
2. The target binary exists and matches the processor family.
3. The selected algorithm is the built-in RCON algorithm, typically `RCON.bin` in the `flash` folder.
4. The communication interface is known:
   - `uart`
   - `can`
   - `ethernet`
5. The communication endpoint is known.
6. The board is connected and powered.
7. The board is in the correct boot mode for S32FlashTool communication.
8. For serial/UART workflows, the board is typically placed in **serial boot mode**.
9. If a different target/algorithm was used previously, a board reset / restart into serial boot may be necessary.

### Recommended preparation
- Search in the installation `examples` folder for board-specific setup documentation.
- Search indexed documentation for board-specific RCON usage and boot configuration notes.
- If needed, read MCUID first to help confirm the processor family.
- If the port is not known, discover it before reading.

## Required inputs

Collect or confirm the following:

- `s32flashtool_folder`
- `target`
- `algorithm` (normally `RCON.bin`)
- `interface`
- `port`
- `addr`
- `size`

### Address and size constraints
- RCON/EEPROM size is typically **24 bytes** total.
- `addr` should normally start at `0x0`.
- `size` should normally be between `1` and `24` bytes.
- Do not request a size greater than 24 unless reliable documentation for the specific target proves otherwise.

### Optional inputs
- `file_path` for save-to-file workflows
- `binary_output` / `binaryMode`
- `extra_args` only if explicitly needed

## Input rules

- Do not guess the target binary.
- Do not guess the RCON algorithm path.
- Do not guess the COM port.
- Use absolute file paths when a file path is provided.
- `addr` and `size` may be decimal or hexadecimal.
- Prefer `addr = 0` when the user wants the full RCON/EEPROM region.
- Keep `size <= 24` unless the target documentation proves otherwise.
- For GUI workflows, numeric strings may be normalized by the GUI. Treat that as normal unless the semantic value changed incorrectly.

## GUI / RPC flow

See [references/GUI.md](references/GUI.md) for the full GUI / RPC flow, payloads, and example sequences.

## CLI flow

See [references/CLI.md](references/CLI.md) for the full CLI flow, parameters, and example MCP calls.

## Validation loop

After a successful read, validation may include:

- confirming that the read completed successfully
- checking that the output size matches the requested size
- checking that the file was created when reading to a file
- inspecting the returned bytes
- comparing the result against expected RCON structure or known boot settings

### Practical validation examples
- confirm the dump file exists
- inspect all 24 bytes
- compare the bytes against expected boot configuration
- rerun a small read if the user wants confirmation

## Failure modes

Recognize these RCON-read-specific failure modes from tool output and respond appropriately. They are distinct from generic path/port/boot-mode errors covered in "Error handling" below.

### Target / algorithm mismatch
- Symptom: tool output indicates the algorithm does not match the device, RCON is not accessible, or the read returns implausible content (all `0xFF` or all `0x00`, or a value that does not match any documented RCON layout for the board).
- Interpretation: the supplied `target` and/or `algorithm` is wrong for the connected board, or the RCON path is not initialized for this device family.
- Response:
  - Stop. Do not retry with a different algorithm by guessing.
  - Re-run discovery: `list_platform_files` action (bin_type="supported") and consult the matching `supported_<platform>_devices.txt`.
  - If the processor family itself is uncertain, apply skill `s32flashtool-read-mcuid` first.

### File-write failure when saving to disk (CLI or GUI)
- Symptom: the tool reports success in reading RCON bytes but the output file does not exist or is empty.
- Interpretation: the parent folder of `file_path` does not exist or is not writable. The device read likely succeeded; the file-write step failed independently.
- Response:
  - Do not report the read as failed on the device side.
  - Confirm the parent folder exists and is writable.
  - Ask the user for a different output path.

## Error handling

If the operation fails:

1. Report the exact failure clearly.
2. Check:
   - target path
   - algorithm path
   - interface
   - port
   - address
   - size
   - boot mode
3. If using UART, remind the user to confirm the board is in serial boot mode.
4. If a different flash algorithm was used before, suggest restarting the board in serial boot mode.
5. If GUI mode was requested and RPC is unavailable:
   - explain that GUI/RPC is not reachable
   - ask whether CLI fallback is acceptable

## Do not

- Do not use this skill for general flash reading.
- Do not guess target/device compatibility.
- Do not guess COM ports.
- Do not silently switch between GUI and CLI.
- Do not use raw shell commands instead of MCP tools.
- Do not use `communicationDevice = UART` in RPC GUI workflows.
- Do not invent RPC actions or model keys.
- Do not read beyond the supported RCON/EEPROM size unless verified by documentation.

## Quick decision summary

- **User asked for GUI / S32FlashTool window / RPC**  
  -> use GUI/RPC flow

- **User asked for CLI / command line / shell**  
  -> use CLI flow

- **User did not specify**  
  -> prefer `cli_build_fread` + `cli_execute`

- **User wants the full RCON region**  
  -> use `addr = 0x0`, `size = 0x18`

- **Board/boot uncertainty**  
  -> pause and clarify serial boot / hardware setup

## Guardrails

**Scope**
- Only read the RCON/EEPROM region using the RCON algorithm (typically `flash/RCON.bin`) via CLI
  (`cli_build_fread` + `cli_execute` or `execute_expert`) or the documented GUI/RPC flow.
- Do not use for general flash reading (use `s32flashtool-read-flash`).

**Destructive actions**
- Read-only. If the user asks to write RCON afterward, hand off to `s32flashtool-write-rcon` and
  confirm there.

**Refuse-and-escalate**
- Missing target, RCON algorithm path, interface, port, or size: stop and ask.
- Do not read beyond the supported RCON/EEPROM size for the device. Recovery: cap at the
  documented size and warn the user if the requested range exceeded it.
- RPC GUI: use `communicationDevice = COM`, never `UART`.

**Output contract**
- Return the raw RCON bytes as reported by the tool, plus the address and size read. Do not
  interpret RCON semantics unless documentation or explicit user intent supports it.

## Out of scope

- General flash reading. Use `s32flashtool-read-flash`.
- Programming or writing RCON/EEPROM data. Use `s32flashtool-write-rcon`.
- Erasing flash. Use `s32flashtool-erase-flash`.
- Identifying the processor. Use `s32flashtool-read-mcuid`.
- Reading beyond the documented RCON/EEPROM size for the device.
- Interpreting RCON byte semantics without documentation or explicit user
  intent.

## Examples

- intentionally push examples into `references/*.md`
