---
name: s32flashtool-sram
description: Load a binary into SRAM and execute it on a supported NXP S32 device using either S32FlashTool CLI or S32FlashTool GUI via RPC.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index", "s32flashtool-rpc-api"]'
  tags: '["s32flashtool", "cli", "gui", "rpc", "sram", "execute", "not persistent"]'
---

# S32FlashTool Execute Binary in SRAM

Load a binary into SRAM and execute it on a supported NXP S32 target.

This skill supports **two execution modes**:

- **CLI mode** using:
  - the `cli_build_<op>` + `cli_execute` actions
  - with `boot=true`
- **GUI mode** using S32FlashTool  GUI over RPC:
  - the matching `gui_*` action

This skill is **operation-focused**:
- it explains what the SRAM execution operation needs
- how to choose GUI vs CLI
- how to execute the SRAM load-and-run flow in each mode
- how to validate the outcome

## When to use

Use this skill when the user wants to:
- upload a binary to SRAM and execute it
- run a RAM-resident test image
- validate board communication by executing a simple SRAM image
- use entry point based SRAM execution
- run an SRAM image with FRB-related parameters through CLI

## When not to use

Do **not** use this skill for:
- programming/writing/uploading a file into flash -> use `s32flashtool-upload-file-to-flash`
- erasing a range of flash memory -> use `s32flashtool-erase-flash`
- reading flash contents -> use `s32flashtool-read-flash`
- reading RCON/EEPROM -> use `s32flashtool-read-rcon`
- writing hex bytes into RCON/EEPROM -> use `s32flashtool-write-rcon`
- identifying the processor -> use `s32flashtool-read-mcuid`

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct operation skill.

## Quickstart

1. Select mode  see `## Mode selection policy`
2. Gather inputs  see `## Required inputs` (use discovery calls from `## Preconditions`)
3. Preview the operation  CLI: show invocation (address / entry point / FRB); GUI: show payload
4. Execute  `references/CLI.md` or `references/GUI.md`
5. Validate  see `## Validation loop`

## Mode selection policy

Choose execution mode as follows:

1. If the user explicitly asks for **GUI**, **window**, **RPC**, or **S32FlashTool GUI**, use the **GUI/RPC flow**.
2. If the user explicitly asks for **CLI**, **command line**, **shell**, or requests a command, use the **CLI flow**.
3. If the user does not specify GUI or CLI:
   - prefer the dedicated CLI path using the `cli_build_<op>` + `cli_execute` actions
   - because the final SRAM execute RPC click action is not currently exposed
4. If the user previously established a working GUI RPC session and only wants to preconfigure the GUI model, `fullConfigSram` may still be set through RPC.
5. Do not silently switch from GUI to CLI or from CLI to GUI.
6. If full GUI execution is requested, explain that RPC currently exposes the SRAM config entry but not the final execute action, then ask whether CLI fallback is acceptable.

## Preconditions

Before SRAM execution, ensure:

1. The S32FlashTool installation folder is known.
2. The target binary exists and matches the processor family.
3. The SRAM binary file exists and is accessible.
4. The communication interface is known:
   - `uart`
   - `can`
   - `ethernet`
5. The communication endpoint is known.
6. The board is connected and powered.
7. The board is in the correct boot mode for S32FlashTool communication.
8. For serial/UART workflows, the board is typically placed in **serial boot mode**.
9. If the binary requires a specific SRAM start address or entry point, those values must be known.
10. If FRB thresholds are required by the target image, they must be provided explicitly.

### Recommended preparation
Use concrete discovery tool calls instead of guessing. The following hints map each precondition to a tool call:

- List candidate target binaries:
  - `list_platform_files` action (bin_type="target").
- Confirm device / interface support before any hardware-specific action:
  - `list_platform_files` action (bin_type="supported") and read the matching `supported_<platform>_devices.txt`.
- Inspect board-specific examples and PDFs if useful:
  - `list_platform_files` action (bin_type="blob")
  - `list_platform_files` action (bin_type="example_pdf").
- Discover available communication ports if the port is unknown:
  - the `cli_build_<op>` + `cli_execute` actions with `list_ports=true`.
- Identify the processor on the connected board when family is uncertain:
  - apply skill `s32flashtool-read-mcuid` (uses `cli_build_mcuid` + `cli_execute`).

Do not invent values for `target`, `port`, `addr`, or `entrypoint`. Use the discovery calls above or ask the user.

## Required inputs

Collect or confirm the following:

- `s32flashtool_folder`
- `target`
- `interface`
- `port`
- `file_path`
- `addr`

### Optional inputs

- `entrypoint`
- FRB-related values in `extra_args`
- any target-specific communication parameters

## Input rules

- Do not guess the target binary.
- Do not guess the COM port.
- Use absolute file paths when a file path is provided.
- `addr` and `entrypoint` may be decimal or hexadecimal.
- If entry point execution is requested, preserve that request.
- Do not supply `algorithm` for SRAM operations; the tool does not use a flash algorithm for SRAM loading.
- For GUI workflows, numeric strings may be normalized by the GUI. Treat that as normal unless the semantic value changed incorrectly.

## GUI / RPC flow

See [references/GUI.md](references/GUI.md) for the full GUI / RPC flow, payloads, and example sequences.

## CLI flow

See [references/CLI.md](references/CLI.md) for the full CLI flow, parameters, and example MCP calls.

## Validation loop

After SRAM execution, validation may include:

- checking that the SRAM load/boot command completed successfully
- checking expected UART terminal output
- checking that the board responds as expected after execution
- checking that the correct entry point was used if applicable

### Practical validation examples
- open a serial terminal and inspect expected output
- confirm the target responds after SRAM boot
- compare observed UART output to the board example documentation

## Failure modes

Recognize these failures from tool output and respond accordingly. On any failure, report the exact tool output before proposing next steps.

| # | Failure | Symptom | Interpretation | Response |
|---|---|---|---|---|
| 1 | Final GUI execute action unavailable | RPC exposes `fullConfigSram` but no exposed final SRAM execute click action | GUI/RPC cannot trigger the actual SRAM run in the installed version | Do not invent an RPC action. Explain the limitation and ask whether CLI fallback is acceptable. |
| 2 | Target mismatch | Target not detected; device ID mismatch; wrong family | Wrong `target` for the board | Stop. Re-run `list_platform_files` action (bin_type="supported") and consult `supported_<platform>_devices.txt`. If family uncertain, apply `s32flashtool-read-mcuid` first. Do not guess a new target. |
| 3 | Bad SRAM address / entry point | Tool reports invalid address, image does not run, or hard fault | `addr` or `entrypoint` incorrect for the image | Do not guess. Confirm the required SRAM start address and entry point from the image/board documentation, then retry. |
| 4 | Missing initialization (GUI/RPC) | Model configured but SRAM path reports not initialized | `init.clickLaunchInitialization` was skipped or failed | Call `init.clickLaunchInitialization` before retrying. If init itself fails, treat as row 2 or row 5. |
| 5 | Communication / boot-mode / path errors | Port not open; no response; file-not-found on `target`/`file_path` paths | Wrong `port`, board not in serial boot, previous session used a different target, or bad paths | Verify `target`/`file_path` paths, `interface`, `port`, `addr`, boot mode. Confirm serial boot mode. If a different target ran previously, ask the user to reset the board into serial boot. |
| 6 | GUI/RPC unavailable | `hello` fails or RPC endpoint unreachable | GUI not running or RPC disabled | Do not launch a second GUI blindly; follow launch procedure in `s32flashtool-rpc-api`. Explain unavailability and ask whether CLI fallback is acceptable. |
| 7 | No side-channel confirmation | Tool acknowledges launch but target behavior cannot be confirmed | SRAM execution success typically requires side-channel confirmation | Report only the tool's launch acknowledgment. Do not claim "executed successfully" without target confirmation. |

## Guardrails

**Scope**
- Only load and execute a binary from SRAM using the `cli_build_<op>` + `cli_execute` actions with `boot=true`
  (CLI), or a documented GUI/RPC flow if the exposed final action exists.
- Do not program flash, erase flash, or write RCON from this skill.
  Recovery: hand off to the correct sibling skill.

**Destructive actions**
- SRAM execution does not modify persistent flash, but code runs on the target immediately.
  Operational risk still applies (watchdog, peripherals, external memory).
- Preview the invocation (SRAM address / entry point / FRB thresholds if any) before running.
  Recovery: on any uncertainty about entry point or FRB, stop and ask; do not guess.
- If the user asks for a GUI/RPC SRAM run and the exposed final action does not exist in the
  installed version, refuse and fall back to CLI (or stop). Never invent an RPC click action.
- Never mix GUI and CLI in the same invocation. Recovery: pick one mode up front.

**Refuse-and-escalate**
- Missing/ambiguous target, SRAM binary, interface, port, entry point (when required), or FRB
  thresholds: stop and ask.
- Board not in the expected boot mode, or a previous session used a different target: ask the
  user to place it in serial boot before retrying.
- RPC GUI: if `hello` fails, do not launch a second GUI blindly; follow the launch procedure in
  `s32flashtool-rpc-api`. Never use `communicationDevice = UART`; use `COM` with values like
  `COM15,ftdi` in `comPort`.

**Output contract**
- Report the tool's launch acknowledgment and exit status. Do not claim "executed successfully"
  beyond what the tool actually reports; SRAM execution success typically requires side-channel
  confirmation from the target.

## Out of scope

- Programming persistent flash. Use `s32flashtool-upload-file-to-flash`.
- Erasing flash memory ranges. Use `s32flashtool-erase-flash`.
- Reading flash contents. Use `s32flashtool-read-flash`.
- Reading RCON/EEPROM. Use `s32flashtool-read-rcon`.
- Writing hex bytes into RCON/EEPROM. Use `s32flashtool-write-rcon`.
- Inventing GUI/RPC click actions for SRAM when the documented final action
  does not exist in the installed version.
- also see `## When not to use`

## Examples

- intentionally push examples into `references/*.md`
