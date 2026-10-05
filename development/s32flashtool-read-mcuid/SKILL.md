---
name: s32flashtool-read-mcuid
description: Read the MCU identification from a supported NXP S32 device using S32FlashTool command-line application (CLI) over a supported communication interface.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index"]'
  tags: '["s32flashtool", "cli", "mcuid", "identification", "read-only"]'
---

# S32FlashTool Read MCU ID

Read the MCU identification from a supported NXP S32 target.

This skill supports **one execution mode**:

- **CLI mode** using:
  - the `cli_build_<op>` + `cli_execute` actions
  - via `cli_build_mcuid` (no flash algorithm)

There is **no GUI / RPC mode** for MCU ID reading; the S32FlashTool GUI RPC API exposes no
documented action that returns the MCU ID. See `references/GUI.md` for the explicit refusal.

This skill is **operation-focused**:
- it explains what the MCU-ID read operation needs
- why this operation is CLI-only
- how to execute the read
- how to validate the outcome

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct operation skill.
- For the CLI flow, see `references/CLI.md`.
- For the (intentional) absence of a GUI/RPC flow, see `references/GUI.md`.

## Quickstart

1. Confirm mode  see `## Mode selection policy` (CLI-only; refuse GUI/RPC requests)
2. Gather inputs  see `## Required inputs` (use discovery calls from `## Preconditions`)
   - MCUID-specific: use `cli_build_mcuid`; do **not** pass an algorithm; if `target` is unknown, discover it first
3. Execute  `references/CLI.md`
4. Validate  see `## Validation loop`

Do not escalate to programming operations from this skill.

## Mode selection policy

This skill is **CLI-only**.

1. Regardless of what the user requests, MCU ID reading uses the **CLI flow**.
2. If the user explicitly asks for **GUI**, **window**, or **RPC**, explain that MCU ID reading is
   not exposed by the S32FlashTool GUI RPC API (see `references/GUI.md`) and offer the CLI path.
3. Do not invent an undocumented GUI/RPC action, and do not substitute `flash.clickGetId` (that
   reads the flash JEDEC ID, not the MCU ID).
4. An active GUI/RPC session does not create a GUI MCUID path; dispatch the CLI mcuid call and
   coordinate serial-port access with the user.

## When to use this skill

Use this skill when the user wants to:

- identify the connected board or SoC
- verify communication before flash operations
- confirm device family / silicon revision
- perform a simple read-only connectivity test

## When not to use this skill

Do **not** use this skill when:

- the user wants to **read flash contents**  
  -> use `s32flashtool-read-flash`
- the user wants to read **RCON/EEPROM**  
  -> use `s32flashtool-read-rcon`
- the user wants to read the **flash device identification** (JEDEC/flash ID)  
  -> use `s32flashtool-get-flash-id`
- the user wants to **program/write/upload** a file  
  -> use `s32flashtool-upload-file-to-flash`
- the user wants **GUI automation through RPC**  
  -> not available for MCUID; this skill is CLI-only

## Preconditions

Before reading MCU ID, ensure:

1. The S32FlashTool installation folder is known.
2. The target binary exists and matches the processor family.
3. The communication interface is known:
   - `uart`
   - `can`
   - `ethernet`
4. The communication endpoint is known:
   - for UART: e.g. `COM31` or `COM3,ftdi`
5. The board is connected and powered.
6. The board is in the correct boot mode for S32FlashTool communication.
7. For serial/UART workflows, the board is typically placed in **serial boot mode**.
8. If a different target/algorithm was used previously, a board reset / restart into serial boot may be necessary.
9. No flash algorithm is passed for MCU ID reading.

### Recommended preparation
- Discover candidate target binaries if the family is not yet confirmed:
  - `list_platform_files` action (bin_type="target").
- Check supported target combinations if compatibility is uncertain:
  - `list_platform_files` action (bin_type="supported") and read the matching `supported_<platform>_devices.txt`.
- Discover the communication port if the user did not provide one:
  - the `cli_build_<op>` + `cli_execute` actions with `list_ports=true`.
- Confirm the installation is reachable if unsure:
  - `cli_execute` (version query).

## Required inputs

Collect or confirm the following:

- `s32flashtool_folder`
- `target`
- `interface`
- `port`
- operation (fixed: `mcuid_cli` via `cli_build_mcuid`)

### Optional inputs
- `preview_only`
- `extra_args`

## Input rules

- Do not guess the target binary if the board family is unknown.
- Do not guess the communication port if the user did not provide it.
- Do not pass an algorithm; MCU ID reading does not consume a flash algorithm.
- Do not pass `addr`/`size`; MCU ID reading does not address a memory range.
- Use absolute file paths for the installation folder and target file.
- If `target` is missing, discover target binaries first.
- If `port` is missing, discover ports first.
- Do not silently switch to a GUI/RPC flow; none exists for this operation.
- Do not use raw shell commands instead of MCP tools.
- Do not claim a valid MCUID without checking the tool response.

## GUI / RPC flow

There is no GUI / RPC flow for MCU ID reading. See [references/GUI.md](references/GUI.md) for the explicit refusal and the correct response when the user asks for GUI/RPC operation.

## CLI flow

See [references/CLI.md](references/CLI.md) for the full CLI flow, parameters, and example MCP calls.

## Validation loop

After a successful MCU ID read, validation may include:

- checking that the command completed successfully
- inspecting the returned MCU family / variant
- inspecting the returned silicon revision
- using the result to confirm target-family selection for later operations

### Practical validation examples
- confirm the output looks like a valid MCUID line, e.g. `MCU: S32N_55 Rev: B0`
- use the returned family/variant to select a matching target for later operations
- if the output is empty, an error, or banner text, treat it as a failed read

## Failure modes

Recognize these failures from tool output and respond accordingly. MCU ID read is non-destructive, so a bounded retry after correcting inputs is acceptable. On any failure, report the exact tool output before proposing next steps.

| # | Failure | Symptom | Interpretation | Response |
|---|---|---|---|---|
| 1 | Wrong / incompatible target | Command fails immediately, or returns an implausible/empty identification | `target` does not match the connected device family | Re-run `list_platform_files` action (bin_type="target") and `(bin_type="supported")` and consult `supported_<platform>_devices.txt`. Do not guess a new target. |
| 2 | Communication / boot-mode / path errors | Port not open; no response; file-not-found on `target` path | Wrong `port`, board not in serial boot, previous session used a different target/algo, or bad paths | Verify `s32flashtool_folder`, `target` path, `interface`, `port`, boot mode. Confirm serial boot mode. If a different algorithm ran previously, ask the user to reset the board into serial boot. |
| 3 | Algorithm mistakenly passed | Tool rejects the invocation or behaves unexpectedly when an algorithm is supplied | MCU ID reading does not consume a flash algorithm | Remove the algorithm argument and retry. Never pass `algorithm`, `addr`, or `size` to the mcuid command. |
| 4 | GUI/RPC requested | User asks for GUI/window/RPC MCU ID reading | No documented RPC action returns the MCU ID | Explain that MCUID is not exposed by the GUI RPC API (see `references/GUI.md`). Do not substitute `flash.clickGetId`. Offer the CLI path and ask before switching modes. |
| 5 | Missing required input | `s32flashtool_folder`, `target`, `interface`, or `port` not provided | Cannot dispatch a safe, non-guessing call | Stop and ask, or run the matching discovery call from `## Preconditions`. Do not guess. |
| 6 | Unrecognized output | Output is empty, an error, or banner text rather than an MCUID line | Read did not produce a valid identification | Report the raw output and stop. Do not fabricate a decode. |

## Guardrails

**Scope**
- Only read the MCU identification via the `cli_build_<op>` + `cli_execute` actions (CLI) via `cli_build_mcuid`.
  There is no documented GUI/RPC flow for MCUID; do not invent one.
- Do not pass a flash algorithm to this operation.
- Do not read flash, RCON, or program from this skill.
  Recovery: hand off to the correct sibling skill.

**Destructive actions**
- Read-only. Must never escalate to programming without an explicit user request that switches
  skills.

**Refuse-and-escalate**
- Missing/ambiguous installation folder, target binary, interface, or port: stop and ask.
- If the target binary is unknown, discover it via
  `list_platform_files` action (bin_type="target") or by inspecting
  `s32flashtool_folder`; do not guess.
- Board not in serial boot mode, or a previous session used a different target/algorithm: ask the
  user to reset the board into serial boot before retrying.
- GUI/RPC: MCUID is not exposed by the S32FlashTool GUI RPC API. Do not invent an RPC action or
  substitute `flash.clickGetId`; offer the CLI path and ask before switching modes.

**Output contract**
- Return the MCUID exactly as the tool reports it, plus (when clearly derivable) the family and
  silicon revision. Do not fabricate decoding when the tool does not provide it. Do not claim a
  valid MCUID without a positive tool response.

## Out of scope

- Reading flash contents. Use `s32flashtool-read-flash`.
- Reading RCON/EEPROM. Use `s32flashtool-read-rcon`.
- Reading the flash device identification (JEDEC/flash ID). Use `s32flashtool-get-flash-id`.
- Programming a file into flash. Use `s32flashtool-upload-file-to-flash`.
- GUI/RPC automation for MCUID (no documented RPC flow exists).
- Passing a flash algorithm to the MCUID command.
- Escalating from MCUID read to any programming operation without a fresh user request.
- also see `## When not to use this skill`
