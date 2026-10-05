---
name: s32flashtool-write-rcon
description: Write hex data into RCON/EEPROM on a supported NXP S32 device using S32FlashTool GUI via RPC or S32FlashTool CLI.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index", "s32flashtool-rpc-api"]'
  tags: '["s32flashtool", "cli", "gui", "rpc", "rcon", "eeprom", "program", "write", "destructive"]'
---

# S32FlashTool Write RCON/EEPROM Hex Data

Write a hexadecimal byte string into the RCON/EEPROM region on a supported NXP S32 target.

This skill supports **two execution modes**:

- **CLI mode** using:
  - the `cli_build_<op>` + `cli_execute` actions
  - typically via `cli_build_fprogram` (hex string written to a temp file, passed via `file_path`)
- **GUI mode** using S32FlashTool  GUI over RPC:
  - the matching `gui_*` action
  - with `fullConfigUploadHexToRcon` followed by initialization and `flash.clickUploadFileToDevice`

This skill is **operation-focused**:
- it explains what the RCON write operation needs
- how to choose GUI vs CLI
- how to execute the write in each mode
- how to validate the outcome
- how to handle destructive-operation confirmation safely

## When to use

Use this skill when the user wants to:
- write boot configuration bytes into RCON
- update EEPROM/RCON contents as a hex string
- modify RCON bytes at a start address
- program boot-source configuration bytes such as XSPI boot settings into RCON
- trigger the S32FlashTool GUI RCON-write workflow through RPC

## When not to use

Do **not** use this skill for:
- file-based flash programming -> use `s32flashtool-upload-file-to-flash`
- reading RCON/EEPROM -> use `s32flashtool-read-rcon`
- reading flash contents -> use `s32flashtool-read-flash`
- erasing flash only -> use `s32flashtool-erase-flash`
- executing a binary from SRAM -> use `s32flashtool-sram`
- identifying the processor -> use `s32flashtool-read-mcuid`

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct operation skill.

## Quickstart

1. Select mode  see `## Mode selection policy`
2. Gather inputs  see `## Required inputs` (use discovery calls from `## Preconditions`)
3. Preview the operation  CLI: `preview_only=true`; GUI: show `fullConfigUploadHexToRcon` payload
4. Obtain confirmation phrase "yes, write RCON"  see `## Guardrails` (Destructive actions)
5. Execute  `references/CLI.md` or `references/GUI.md`
6. Validate  see `## Validation loop` (readback strongly recommended)

## Mode selection policy

Choose execution mode as follows:

1. If the user explicitly asks for **GUI**, **window**, **RPC**, or **S32FlashTool GUI**, use the **GUI/RPC flow**.
2. If the user explicitly asks for **CLI**, **command line**, **shell**, or requests a command, use the **CLI flow**.
3. If the user does not specify GUI or CLI:
   - continue using GUI/RPC if a working GUI/RPC session is already in progress
   - otherwise, ask whether GUI or CLI is preferred
4. If the user previously established a working GUI RPC session and continues issuing GUI-style requests, continue with RPC.
5. Do not silently switch from GUI to CLI or from CLI to GUI.
6. If the requested behavior is only possible through the other mode, explain the fallback before doing it.

## Preconditions

Before writing RCON/EEPROM, ensure:

1. The S32FlashTool installation folder is known.
2. The target binary exists and matches the processor family.
3. The selected algorithm is the RCON algorithm, typically `RCON.bin`.
4. The communication interface is known:
   - `uart`
   - `can`
   - `ethernet`
5. The communication endpoint is known.
6. The board is connected and powered.
7. The board is in **serial boot mode** for S32FlashTool communication.
8. The start address and hex string are known.
9. If a different target/algorithm was used previously, a board reset / restart into serial boot may be necessary.
10. The user has explicitly confirmed the destructive write action.

### Recommended preparation
Use concrete discovery tool calls instead of guessing. The following hints map each precondition to a tool call:

- List candidate target binaries:
  - `list_platform_files` action (bin_type="target").
- List candidate flash/RCON algorithms (RCON algorithm is normally `RCON.bin`):
  - `list_platform_files` action (bin_type="flash").
- Confirm device / algorithm / interface support before any hardware-specific action:
  - `list_platform_files` action (bin_type="supported") and read the matching `supported_<platform>_devices.txt`.
- Inspect board-specific examples and PDFs for RCON layout / boot-configuration notes:
  - `list_platform_files` action (bin_type="blob")
  - `list_platform_files` action (bin_type="example_pdf").
- Discover available communication ports if the port is unknown:
  - the `cli_build_<op>` + `cli_execute` actions with `list_ports=true`.
- Identify the processor on the connected board when family is uncertain:
  - apply skill `s32flashtool-read-mcuid` (uses `cli_build_mcuid` + `cli_execute`).
- Capture the current RCON content before modifying it:
  - apply skill `s32flashtool-read-rcon` over the same range.

Do not invent values for `target`, `algorithm`, `port`, `addr`, or `hex_string`. Use the discovery calls above, board/family RCON layout documentation, or ask the user.

## Required inputs

Collect or confirm the following. These are **user-level inputs** (what the user must supply); each mode transforms them into mode-specific tool arguments.

- `s32flashtool_folder`
- `target`
- `algorithm` (normally `RCON.bin`)
- `interface`
- `port`
- `addr`
- `hex_string` -- the hexadecimal byte string to write. This is NOT a direct argument of
  the `cli_build_<op>` + `cli_execute` actions (no such parameter exists on the wrapper). It is transformed per mode:
  - **CLI**: written to a temporary file, then passed via `file_path` via `cli_build_fprogram`. See `references/CLI.md`.
  - **GUI / RPC**: passed as the `hexString` field of the `fullConfigUploadHexToRcon` payload. See `references/GUI.md`.

### Optional inputs

- `size` if the CLI form needs it explicitly
- `extra_args`

## Input rules

- Do not guess the target binary.
- Do not guess the RCON algorithm path.
- Do not guess the COM port.
- Use absolute file paths where relevant.
- Preserve the user's intended start address exactly.
- Preserve the hex data exactly; do not reinterpret byte order unless the user explicitly asks.
- RCON/EEPROM size is typically **24 bytes** total; `addr` should be within the valid RCON range and the hex string length aligned with the intended byte count. Do not assume writes larger than 24 bytes are valid unless target documentation proves otherwise.
- Prefer reading the existing RCON content first when modifying only part of the structure.
- Do not claim semantic interpretation of RCON bytes unless supported by board-specific documentation or readback evidence.
- For GUI workflows, numeric strings may be normalized by the GUI. Treat that as normal unless the semantic value changed incorrectly.

## GUI / RPC flow

See [references/GUI.md](references/GUI.md) for the full GUI / RPC flow, payloads, and example sequences.

## CLI flow

See [references/CLI.md](references/CLI.md) for the full CLI flow, parameters, and example MCP calls.

## Validation loop

Readback validation is strongly recommended because RCON changes can alter boot behavior even when the write operation reports success.

After writing RCON/EEPROM, validation may include:

- reading back the modified RCON bytes
- confirming the EEPROM data matches the intended hex string
- checking whether boot behavior changes as expected
- comparing before/after RCON contents

### Practical validation examples
- use `s32flashtool-read-rcon` to read back the modified region
- read the exact modified byte range immediately after programming
- read all 24 bytes when practical and compare them to the intended result
- validate expected boot mode behavior on the board
- if boot-source bytes were changed, remind the user that a restart may be required before testing the new boot path

## Failure modes

Recognize these failures from tool output and respond accordingly. Never auto-retry a destructive operation. RCON write is the highest-stakes operation in this pack: an incorrect RCON value can prevent the board from booting from any source, including serial boot, and in that state the board may not be recoverable in software. On any failure, report the exact tool output before proposing next steps.

| # | Failure | Symptom | Interpretation | Response |
|---|---|---|---|---|
| 1 | User-aborted write (GUI) | `flash.clickUploadFileToDevice` returns OK but GUI dialog cancelled or reports aborted | RPC click dispatched; operation did not complete | Report as user-cancelled; ask whether to retry. Do not claim success. |
| 2 | Target / algorithm mismatch | Algorithm does not match device; RCON not accessible; identification-related error at start | Wrong `target` and/or `algorithm` for the connected board | Stop. Re-run `list_platform_files` action (bin_type="supported") and consult `supported_<platform>_devices.txt`. If family uncertain, apply `s32flashtool-read-mcuid` first. Do not guess a new algorithm. |
| 3 | Invalid hex value / bad boot-config encoding | Odd number of hex digits, non-hex characters, wrong length for the RCON layout; or a syntactically valid but semantically invalid boot configuration (reserved bit pattern, undefined boot source, unsupported mode) | Input did not pass basic tool validation, or encodes an unsupported/reserved configuration | Do not proceed with the write. Ask the user to source the intended hex value from the board or family RCON layout documentation, not from inference. Never suggest a "reasonable default" for RCON; there is no reasonable default. |
| 4 | Oversize write / out-of-range address | Tool reports the write exceeds RCON/EEPROM size or the start address is out of range | `addr` + hex-string length out of the valid RCON range (typically 24 bytes) | Do not silently clip. Confirm the RCON size/range from installed documentation. Ask the user to restate `addr`/`hex_string` within a valid range. |
| 5 | Missing initialization (GUI/RPC) | `flash.clickUploadFileToDevice` fails; destination reported as not initialized | `init.clickLaunchInitialization` was skipped or failed for `EEPROM (RCON)` | Call `init.clickLaunchInitialization` before retrying. If init itself fails, treat as row 2 or row 6. |
| 6 | Communication / boot-mode / path errors | Port not open; no response; file-not-found on `target`/`algorithm` paths | Wrong `port`, board not in serial boot, previous session used a different target/algo, or bad paths | Verify `target`/`algorithm` paths, `interface`, `port`, `addr`, hex-string length/content, boot mode. Confirm serial boot mode. If a different algorithm ran previously, ask the user to reset the board into serial boot. |
| 7 | GUI/RPC unavailable | `hello` fails or RPC endpoint unreachable | GUI not running or RPC disabled | Do not launch a second GUI blindly; follow the launch procedure in `s32flashtool-rpc-api`. Explain unavailability and ask whether CLI fallback is acceptable. |
| 8 | CLI surface insufficient for hex write | Installed CLI lacks a documented path to write hex bytes into RCON | The expert CLI cannot express this operation in this version | Explain the limitation clearly; do not invent parameters. Offer the GUI/RPC path instead. |

## Guardrails

**Scope**
- Only write hexadecimal bytes into the RCON/EEPROM region using the RCON algorithm (typically
  `RCON.bin`) via the `cli_build_<op>` + `cli_execute` actions (CLI) or the documented GUI/RPC
  `fullConfigUploadHexToRcon` flow followed by `flash.clickUploadFileToDevice`.
- Do not program files, read, erase, or run SRAM images from this skill.
  Recovery: hand off to the correct sibling skill.

**Destructive actions (confirmation contract)**
- RCON writes are destructive and can alter boot behavior; an incorrect value can render the board
  unbootable from any source. Always **preview** first: print target, algorithm, interface, port,
  start address, hex string, and byte count.
- Before the actual write step, summarize the intended operation and warn that a wrong RCON value
  may prevent the board from booting.
- Require an **explicit user confirmation phrase** (e.g. "yes, write RCON") before invoking the
  write action. This applies to **both** CLI and GUI/RPC flows. Recovery: if the user hesitates,
  stop; do not write.
- Never interpret RCON byte semantics on behalf of the user unless documentation or explicit user
  intent supports it.
- Never mix GUI and CLI in the same write invocation. Recovery: pick one mode up front.

**Refuse-and-escalate**
- Missing/ambiguous target, RCON algorithm path, interface, port, start address, or hex string:
  stop and ask.
- Never guess EEPROM/RCON size. Recovery: consult the installed documentation for the platform,
  and if unclear, ask the user.
- Board not in serial boot mode, or a previous session used a different target/algorithm: ask the
  user to reset the board into serial boot before retrying.
- RPC GUI: if `hello` fails, do not launch a second GUI blindly; follow the launch procedure in
  `s32flashtool-rpc-api`. Never use `communicationDevice = UART`; use `COM` with values like
  `COM15,ftdi` in `comPort`.

**Output contract**
- Report the tool's exit status and the exact address+bytes written as the tool acknowledged them.
  Do not claim success without a positive response from the tool.

## Out of scope

- File-based flash programming. Use `s32flashtool-upload-file-to-flash`.
- Reading RCON/EEPROM. Use `s32flashtool-read-rcon`.
- Interpreting RCON byte semantics without documentation or explicit user intent.
- Guessing EEPROM/RCON size for the platform. Consult installed docs or ask.
- also see `## When not to use`

## Examples

- intentionally push examples into `references/*.md`
