---
name: s32flashtool-basic-use
description: Human-oriented onboarding and baseline workflow for installing, inspecting, and safely beginning to use S32FlashTool. For agentic routing, prefer s32flashtool-workflow-index.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index"]'
  tags: '["s32flashtool", "onboarding", "human-facing", "baseline"]'
---

# S32FlashTool Basic Use

This skill is the **human-facing onboarding document** for S32FlashTool. It explains the pack in prose: what to install, what to check first, what a baseline session looks like, and how to transition to the right operation skill. This skill is intended for **setup and orientation**, not for performing one specific flash command.

It helps with:
- locating or confirming the S32FlashTool installation
- understanding what files and documentation exist in the installation
- identifying target binaries, flash algorithms, and supported-device references
- discovering available communication ports
- preparing for later workflows such as read, program, erase, or GUI RPC use

## When to use

### For AI agents

Do **not** use this skill as the primary routing entry point. Use the following instead:

1. **`s32flashtool-agent-rules-minimal/SKILL.md`** -- baseline rules.
2. **`s32flashtool-workflow-index/SKILL.md`** -- the operation-first decision matrix. This is the agentic routing entry point.

Read this `basic-use` skill only when:
- the user explicitly asks for onboarding, orientation, or "how do I get started?"
- you need a prose explanation of baseline setup (installation, version check, supported-device docs, port discovery) before any task-specific skill applies
- a sibling skill explicitly delegates to it

For any concrete user goal (read flash, program flash, erase, get ID, read MCUID, RCON, SRAM, GUI RPC automation), route directly through `s32flashtool-workflow-index` and skip this skill. The decision matrix in `workflow-index` already names the correct operation skill and tool for every documented intent.

### For humans

Keep reading. The rest of this file walks through baseline setup in plain language.

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to choose the correct task-specific skill after basic setup is understood.
- Read `s32flashtool-rpc-api/SKILL.md` before the first GUI RPC automation sequence.

## Quickstart

Minimum-viable onboarding pass:

1. Ask for and record the absolute S32FlashTool installation path
   (e.g. `C:/NXP/S32FlashTool_2.4.3`).
2. Call `s32flashtool-get-version` to confirm the install works.
3. Call `s32flashtool-list-available-serial-communication-interfaces` to
   enumerate ports.
4. Hand off to `s32flashtool-workflow-index` with the user's concrete goal.

## Scope

Use this skill for high-level onboarding and preparation.

Typical outcomes include:
- the installation folder is known
- the installed version is identified
- the relevant supported-device documentation has been located
- candidate target binaries and flash algorithms have been listed
- available communication ports have been discovered
- the user is ready to continue with a more specific operation skill

## Do not use this skill as the final operation skill

Do **not** use this skill by itself when the user already has a concrete goal such as:
- program a file to flash
- read flash contents
- erase flash memory
- get flash ID
- read MCUID
- operate the GUI through RPC for a specific action

In those cases:
1. use this skill only for missing baseline setup if needed
2. then switch to the correct task-specific skill

## Core agent rules

1. Prefer safe discovery and inspection before hardware actions.
2. Do not guess the target binary, flash algorithm, interface, port, or board family.
3. Use absolute paths for installation folders and files.
4. Before hardware-specific actions, consult the relevant `supported_*` documentation.
5. Before destructive actions, use the dedicated operation skill and require explicit confirmation.
6. If the user asks for GUI operation, use the RPC workflow and do not silently switch to CLI.
7. Treat this skill as a preparation skill, not as authority to perform flash operations by itself.

## Inputs

This skill may begin with partial information.

Useful inputs include:
- `S32FlashTool installation folder`
- target family or board name
- operating system
- intended interface: `uart`, `can`, or `ethernet`
- known communication port
- intended next action, if any

If some of these are missing, gather only what is necessary for the user's requested next step.

## Recommended baseline workflow

### Step 1 - Confirm installation path
Ask for or reuse the **S32FlashTool installation folder**.

Examples:
- `C:/NXP/S32FlashTool_2.4.2_260522`

Do not guess the installation directory if it is unknown.

### Step 2 - Verify tool availability
Use the version skill/tool to safely confirm that:
- the MCP server is available, and/or
- the installed S32FlashTool folder is valid

Recommended tool:
- `cli_execute` (version query)

This is a safe first check before any hardware workflow.

### Step 3 - Discover available platform files
List the installation-provided files that define supported hardware and flash options.

Recommended tool:
- `list_platform_files` action

Inspect these categories as needed:
- `target`
- `flash`
- `supported`
- `blob`
- `example_pdf`

Use this information to narrow down the correct target family and flash algorithm.

### Step 4 - Read supported-device references
Before board-specific hardware operations, consult the matching `supported_*.txt` document in the installation `doc` folder.

Purpose:
- confirm processor family support
- confirm flash algorithm compatibility
- confirm supported interfaces
- learn family-specific limitations

Do not guess compatibility when documentation is available.

### Step 5 - Discover communication ports if needed
If the user does not already know the port, discover it before attempting communication.

Recommended tool:
- the `cli_build_<op>` + `cli_execute` actions with `list_ports = true`

Important:
- do not invent COM port values
- if the user provided a port explicitly, reuse it

### Step 6 - Inspect examples and board-specific guidance
Look in the installation `examples` folder for:
- example binaries
- board PDFs
- platform-specific examples

This can provide practical setup hints for a known board or target family.

### Step 7 - Transition to the correct operation skill
Once the baseline is clear, switch to the correct task-specific skill for the actual operation.

Examples:
- version lookup -> `s32flashtool-get-version`
- GUI control -> `s32flashtool-rpc-api`
- program flash -> `s32flashtool-upload-file-to-flash`
- read flash -> `s32flashtool-read-flash`
- supported-device lookup -> `s32flashtool-supported-devices-per-platform`

## Installation guidance for agents

If the user asks how to install S32FlashTool:

1. Identify whether the user needs:
   - the public NXP release, or
   - an internal engineering build
2. Point to the appropriate source resource.
3. Remind the user to install any required drivers:
   - FTDI drivers for typical UART/USB setups
   - other board-specific USB/UART drivers if applicable
   - CAN-related drivers/tools if the workflow uses CAN
4. After installation, ask for the installation folder path.
5. Verify the installation with the version skill.

Do not claim that installation is complete until the path and version check are successful.

## Release notes and documentation guidance

If the user asks about issues, limitations, or support:

1. Look for release notes in the installation `doc` folder.
2. Prefer listing candidate files first rather than reading large PDFs automatically.
3. Read `supported_*.txt` files when hardware compatibility details are needed.
4. Use semantic search `nxp_knowledge_kb_search` when the indexed knowledge base is available and useful.

Agent preference:
- prefer small, relevant text artifacts over large indiscriminate document reads

## Board preparation guidance

For UART or other direct device communication workflows, remind the user that later hardware operations may require:
- the board to be powered
- the board to be wired correctly
- the board to be placed in the correct boot mode
- for UART workflows, often **serial boot mode**
- a board reset if a different target/algorithm was previously loaded

This skill should mention these as preparation considerations, but should not perform the actual hardware operation by itself.

## MCUID guidance

If the user wants to identify the processor:
- switch to the MCUID-related skill or tool flow
- gather:
  - target family if known
  - communication interface
  - communication port
- do not invent values for target or port

This basic-use skill may prepare for MCUID, but MCUID itself should be handled by the dedicated workflow.

## GUI/RPC guidance

If the user explicitly asks to work in the GUI:
- use GUI RPC mode
- read `s32flashtool-rpc-api/SKILL.md` before the first RPC action sequence
- probe with `hello` before launching a new GUI instance
- reuse an existing GUI session when possible

Do not silently fall back to CLI if the user asked for GUI.

## Recommended tool mapping

Use these tools during baseline setup as appropriate:

- `cli_execute` (version query)
  - verify MCP or installed S32FlashTool version

- `list_platform_files` action
  - list targets, flash algorithms, supported-device docs, examples

- the `cli_build_<op>` + `cli_execute` actions
  - discover available ports with `list_ports = true`
  - optionally inspect commands in preview mode in later workflows

- the matching `gui_*` action
  - perform GUI automation only after the RPC workflow has been selected

## Validation loop

A successful use of this skill typically results in most or all of the following:
- installation folder confirmed
- tool version identified
- candidate target binaries listed
- candidate flash algorithms listed
- supported-device text file identified
- communication ports discovered if needed
- next operation skill selected confidently

This skill is successful when it reduces ambiguity and prepares the next correct step.

## Error handling

If setup or discovery fails:
1. report the exact failure clearly
2. verify the installation folder path
3. verify that the requested tool mode is appropriate
4. do not infer hardware failure from installation/path problems
5. do not continue into a destructive workflow with unresolved ambiguity
6. ask only for the missing information needed for the next safe step

## Agent reasoning notes

- Prefer incremental certainty over premature execution.
- Use this skill to narrow choices, not to guess them.
- If the user's request is already specific, keep this skill brief and move quickly to the right operation skill.
- If the user is new to S32FlashTool, this skill should help build a clean baseline without overwhelming them.
- Keep the distinction clear between:
  - tool availability
  - documentation-based compatibility
  - actual target communication success

## Example user intents this skill should handle well

- "Help me get started with S32FlashTool."
- "I installed S32FlashTool. What should I check first?"
- "How do I find the correct target and flash algorithm?"
- "Before we flash, help me inspect the installation and supported files."
- "I want to use the GUI, what baseline checks should I do first?"

## Quick decision summary

- **Need to verify installation first?**  
  -> use the version tool

- **Need target / flash candidates?**  
  -> list available platform files

- **Need compatibility evidence?**  
  -> inspect the matching `supported_*.txt` file

- **Need a COM port?**  
  -> use port discovery, do not guess

- **Need a concrete flash/read/erase action?**  
  -> switch to the corresponding operation skill

- **Need GUI behavior?**  
  -> select RPC workflow before issuing GUI actions

## Guardrails

**Scope**
- Use only for onboarding, orientation, and baseline discovery (installation path, version,
  supported-device docs, port enumeration).
- Do not use as the final skill for concrete operations (read/program/erase/get-id/RCON/SRAM).
  Recovery: route through `s32flashtool-workflow-index` to the correct operation skill.

**Destructive actions**
- This skill must never trigger destructive operations. If the user requests one during onboarding, hand off to the matching operation skill and require explicit confirmation there.

**Refuse-and-escalate**
- If the S32FlashTool installation folder is unknown or invalid, stop and ask. Recovery: request an absolute path to the installation folder (for example `C:/NXP/S32FlashTool_2.4.3` on Windows) and verify that the S32FlashTool CLI binary exists inside `bin/` before proceeding (`bin/S32FlashTool.exe` on Windows, `bin/S32FlashTool` on Linux).
- If the user already has a concrete operational goal, refuse to answer here and route to the correct operation skill.

## Out of scope

- Programming, reading, erasing, or verifying flash. Use the matching operation
  skill (`s32flashtool-upload-file-to-flash`, `-read-flash`, `-erase-flash`,
  `-compute-crc-and-compare-to-flash`).
- Reading MCUID, flash ID, or RCON/EEPROM. Use `s32flashtool-read-mcuid`,
  `s32flashtool-get-flash-id`, `s32flashtool-read-rcon`.
- Writing RCON/EEPROM. Use `s32flashtool-write-rcon`.
- SRAM execution. Use `s32flashtool-sram`.
- Operating the GUI through RPC for a concrete action. Use `s32flashtool-rpc-api`
  in combination with the matching operation skill.
- Routing decisions between skills. Use `s32flashtool-workflow-index`.