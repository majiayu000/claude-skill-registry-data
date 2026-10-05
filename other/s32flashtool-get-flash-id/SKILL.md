---
name: s32flashtool-get-flash-id
description: Read the flash memory identification from a supported NXP S32 device using either S32FlashTool CLI or S32FlashTool GUI via RPC.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index", "s32flashtool-rpc-api"]'
  tags: '["s32flashtool", "cli", "gui", "rpc", "flash", "identification", "read-only"]'
---

# S32FlashTool Get Flash ID

Read the flash memory identification from a supported NXP S32 target.

This skill supports **two execution modes**:

- **CLI mode** using:
  - the `cli_build_<op>` + `cli_execute` actions
  - via `cli_build_fid`
- **GUI mode** using S32FlashTool  GUI over RPC:
  - the matching `gui_*` action

This skill is **operation-focused**:
- it explains what the flash-ID operation needs
- how to choose GUI vs CLI
- how to execute flash-ID reading in each mode
- how to validate the outcome

## When to use this skill

Use this skill when the user wants to:

- read the connected flash identification
- confirm which flash device responds on the selected setup
- validate target/algorithm connectivity before read/write/erase operations
- trigger the GUI flash-ID workflow through RPC

## When not to use

Do **not** use this skill when:

- the user wants to **read flash contents**  
  -> use skill `s32flashtool-read-flash`
- the user wants to read **RCON/EEPROM**  
  -> use skill `s32flashtool-read-rcon`
- the user wants to **program/write/upload** a file  
  -> use skill `s32flashtool-upload-file-to-flash`
- the user wants to **erase** flash  
  -> use skill `s32flashtool-erase-flash`
- the user wants to identify the processor rather than the flash device  
  -> use skill `s32flashtool-read-mcuid`

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct operation skill.
- For GUI automation rules, also apply `s32flashtool-rpc-api/SKILL.md`.
- If CLI command support is uncertain, use `s32flashtool-read-command-line-arguments/SKILL.md` to verify the installed CLI options.

## Quickstart

Read the flash device identification. Read-only.

```
Build:   cli_build_fid
Args:    sft_folder=<abs path>
         cli_request.operation="fid_cli"
         cli_request.input: target, algorithm, interface, transport
Execute: cli_execute with { sft_folder, command }
Output:  raw flash-ID bytes as reported by the tool.
```

If CLI option availability is uncertain, first run
`s32flashtool-read-command-line-arguments`.

For GUI/RPC mode, use the documented flash-ID action per
`s32flashtool-rpc-api` (`communicationDevice=COM`, never `UART`).

## Mode selection policy

Choose execution mode as follows:

1. If the user explicitly asks for **GUI**, **window**, **RPC**, or **S32FlashTool GUI**, use the **GUI/RPC flow**.
2. If the user explicitly asks for **CLI**, **command line**, **shell**, or requests a command, use the **CLI flow**.
3. If the user does not specify GUI or CLI:
   - prefer the dedicated CLI path when the user wants a simple identification result
   - continue using GUI/RPC if a GUI session is already established and the user is in a GUI workflow
4. If the user previously established a working GUI RPC session and continues issuing GUI-style requests, continue with RPC.
5. Do not silently switch from GUI to CLI or from CLI to GUI.
6. If the installed CLI help does not include `-fid` in another environment/version, verify support before using it.

## Preconditions

Before reading flash ID, ensure:

1. The S32FlashTool installation folder is known.
2. The target binary exists and matches the processor family.
3. The flash algorithm exists and matches the flash device or flash family being queried.
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
- Check supported target/algorithm combinations using the supported-device documentation.
- If needed, read MCUID first to help identify the processor family.
- If the port is not known, discover it before reading flash ID.
- If CLI support is uncertain in the installed version, verify it using the `cli_build_<op>` + `cli_execute` actions.

## Required inputs

Collect or confirm the following:

- `s32flashtool_folder`
- `target`
- `algorithm`
- `interface`
- `port`

### Optional inputs
- `extra_args`
- `preview_only`
- `timeout`

## Input rules

- Do not guess the target binary.
- Do not guess the flash algorithm.
- Do not guess the COM ports.
- Use absolute file paths where relevant.
- Use `cli_build_fid` for CLI only when supported by the installed tool version.
- If the CLI path is uncertain, verify it first using the command-line-arguments skill or installed CLI help output.
- Do not silently switch between GUI and CLI.
- Do not use raw shell commands instead of MCP tools.
- Do not use `communicationDevice = UART` in RPC GUI workflows.
- Do not invent RPC actions or model keys.

## GUI / RPC flow

See [references/GUI.md](references/GUI.md) for the full GUI / RPC flow, payloads, and example sequences.

## CLI flow

See [references/CLI.md](references/CLI.md) for the full CLI flow, parameters, and example MCP calls.

## Validation loop

After a successful flash-ID read, validation may include:

- checking that the command or RPC action completed successfully
- checking that a flash identification string or device response was returned
- confirming that the returned ID matches the expected flash device family

### Practical validation examples
- compare the returned flash ID or name to the selected algorithm/device
- use the returned result to confirm the chosen flash algorithm is appropriate

## Failure modes

Recognize these failures from tool output and respond accordingly. Flash-ID reading is read-only, so a bounded retry after correcting inputs is acceptable. On any failure, report the exact tool output before proposing next steps.

| # | Failure | Symptom | Interpretation | Response |
|---|---|---|---|---|
| 1 | CLI `-fid` unsupported | CLI reports unknown/invalid option; `cli_build_fid` rejected | Installed tool version does not expose `-fid` | Stop. Verify options via `s32flashtool-read-command-line-arguments`. Do not invent a substitute CLI equivalent; offer the GUI/RPC path instead. |
| 2 | Target / algorithm mismatch | Flash not detected; no ID returned; device ID mismatch | Wrong `target` and/or `algorithm` for the board or flash device | Re-run `list_platform_files` action (bin_type="supported") and consult `supported_<platform>_devices.txt`. If family uncertain, apply `s32flashtool-read-mcuid` first. Do not guess a new algorithm. |
| 3 | Communication / boot-mode / path errors | Port not open; no response; file-not-found on `target`/`algorithm` paths | Wrong `port`, board not in serial boot, previous session used a different target/algo, or bad paths | Verify `target`/`algorithm` paths, `interface`, `port`, boot mode. Confirm serial boot mode. If a different algorithm ran previously, ask the user to reset the board into serial boot. |
| 4 | Missing initialization (GUI/RPC) | Flash-ID RPC action fails; destination reported as not initialized | `init.clickLaunchInitialization` was skipped or failed for `FLASH` | Call `init.clickLaunchInitialization` before retrying. If init itself fails, treat as row 2 or row 3. |
| 5 | GUI/RPC unavailable | `hello` fails or RPC endpoint unreachable | GUI not running or RPC disabled | Do not launch a second GUI blindly; follow the launch procedure in `s32flashtool-rpc-api`. Explain unavailability and ask whether CLI fallback is acceptable. |
| 6 | Empty / undecoded ID (not a failure) | Tool returns raw ID bytes but no vendor/part decode | Tool does not provide a human-readable decode | Report the raw ID bytes as returned. Do not fabricate a vendor/part decode. |

## Quick decision summary

- **User asked for GUI / S32FlashTool window / RPC**  
  -> use GUI/RPC flow

- **User asked for CLI / command line / shell**  
  -> use CLI via `cli_build_fid` if supported by the installed version

- **User did not specify**  
  -> use the simplest documented path for the current workflow context

- **Need processor identification instead of flash identification**  
  -> use skill `s32flashtool-read-mcuid`

## Guardrails

**Scope**
- Only read the flash-device identification using the documented `fid` CLI or the documented GUI RPC flow. Do not read flash contents, do not erase, do not program from this skill.

**Destructive actions**
- Read-only. If the user asks to follow up with a destructive operation, hand off to the correct
  sibling skill and confirm there.

**Refuse-and-escalate**
- Missing target, algorithm, interface, or port: stop and ask; do not guess.
- If the CLI option availability is uncertain in the installed version, delegate to `s32flashtool-read-command-line-arguments` before invoking.
- RPC GUI: reuse the existing session if `hello` succeeds; if not, follow the launch procedure in `s32flashtool-rpc-api`. Use `communicationDevice = COM`, never `UART`.

**Output contract**
- Report the raw flash-ID bytes as returned by the tool plus, when possible, the decoded vendor/part identification. Do not fabricate a decode when the tool does not provide one.

## Out of scope

- see `##When not to use`
- Decoding the returned flash-ID bytes into a vendor/part when the tool does not report the decoding.

## Examples

- intentionally push examples into `references/*.md`
