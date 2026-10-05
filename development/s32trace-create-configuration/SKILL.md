---
name: s32trace-create-configuration
description: >
  Use this skill whenever the user wants to create, generate, or scaffold an
  S32Trace configuration XML for a specific board (SAF86XX, S32K314, S32G3,
  S32N55, ...), enable or disable cores, toggle timestamp or cycle-counting,
  set the trace scenario, configure the ETF or DDR sink (buffer mode, base
  address, buffer size, collection mode, memory space), change SoC module
  (funnel) settings, set the GTA/CCS target-access endpoint, set the output
  folder, or ask which sink collects a given core.
  Trigger phrases: "create a trace config", "generate a SAF86XX config",
  "enable core 0", "disable core 1", "turn on timestamps", "use DDR instead
  of ETF", "set buffer size", "change base address", "switch to Overwrite mode",
  "configure target access port", "set output folder", "which ETF collects
  Core 0", "what is the trace path for M7_0", "what is the current collection
  mode".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32trace
  tags: '[s32trace, configuration, etf, ddr, core, timestamp, sink, gta]'
---

# S32Trace Configuration Generation

Creates and customises S32Trace configuration XML files for NXP S32 boards.
Covers the full workflow from template discovery through targeted per-concern
edits and post-creation verification.

## When to use

Trigger this skill when the user wants to:
- create or scaffold an S32Trace config for any supported board
- enable or disable a core, toggle timestamp or cycle-counting
- configure a sink (ETF or DDR: buffer mode, base address, size, collection mode)
- switch the active Data Streams sink from ETF to DDR or vice versa
- set the GTA/CCS target-access endpoint or output folder
- ask "which ETF collects Core N?" or "what is the current collection mode?"

Do not use this skill to install S32 Design Studio, compile firmware, operate
the S32Debugger, or generate code from a `.mex` file.

## Available Capabilities

| Type | Name | Purpose |
|------|------|---------|
| MCP tool | `search_actions` | discover available actions, their input schemas, and descriptions |
| MCP tool | `execute_action` | validated dispatcher -- pass `action_name` + action-specific `params` |

All configurator operations are routed through `execute_action`:

| Action name | Required params | Optional params |
|---|---|---|
| `configurator.list_templates` | -- | `s32ds_installation_path` |
| `configurator.inspect_template` | `template_path` | -- |
| `configurator.describe_trace_flow` | `config_path` | -- |
| `configurator.create_from_template` | `template_path` | `output_path` |
| `configurator.set_output_folder` | `config_path`, `output_folder` | -- |
| `configurator.set_target_access` | `config_path`, `settings` | -- |
| `configurator.set_timestamp_generator` | `config_path`, `enabled` | `module_base_address`, `counter_base_frequency`, `halt_on_debug`, `mem_space` |
| `configurator.configure_data_streams` | `config_path`, `trace_location` | `continuous_collection` |
| `configurator.configure_sink` | `config_path`, `sink_name`, `settings` | -- |
| `configurator.configure_core` | `config_path`, `core_name`, `settings` | -- |
| `configurator.configure_soc_module` | `config_path`, `module_name`, `settings` | -- |

Call `search_actions` first (or with a focused query such as `"configure core"`)
to get the full parameter documentation before calling `execute_action`.

## Typical workflow

```
configurator.list_templates
  -> configurator.create_from_template   (returns config_path)
  -> configurator.configure_data_streams (select ETF or DDR)
  -> configurator.configure_core         (enable M7_0, set scenario, ...)
  -> configurator.configure_sink         (set buffer size, mode, ...)
  -> configurator.set_output_folder      (optional)
  -> configurator.set_target_access      (optional)
  -> configurator.set_timestamp_generator (optional)
  -> configurator.describe_trace_flow    (verify)
```

Each edit action is independent and can be called on an existing config file at
any time -- you do not need to recreate the file to change one setting.

## Quickstart

1. Call `search_actions(query="list templates")` to confirm the action name and
   input schema.
2. Call `execute_action(action_name="configurator.list_templates")` to discover
   the template path and the board's core UI names (e.g. `["M7_0", "M7_RFE_1"]`).
3. For information questions ("which ETF collects Core N?"), call
   `execute_action(action_name="configurator.describe_trace_flow", params={"config_path": <template_path>})`
   and answer in plain language.
4. Call `execute_action(action_name="configurator.create_from_template", params={"template_path": ...})`
   to clone the template. Record `output_path` from the result.
5. Apply targeted edits using the appropriate `configurator.*` action for each
   concern (core, sink, data streams, etc.).
6. Verify with `execute_action(action_name="configurator.describe_trace_flow", params={"config_path": <output_path>})`.

## Workflow

1. **Discover the template.** Call
   `execute_action(action_name="configurator.list_templates")` (pass
   `s32ds_installation_path` inside `params` only when targeting a non-default
   install). Record `file` as `template_path` and `cores` as the only valid
   core UI name keys. Never invent core names.

2. **Describe the trace flow when the user asks a question.** Call
   `execute_action(action_name="configurator.describe_trace_flow", params={"config_path": <template_path>})`.
   Interpret `cores[n].sink`, `cores[n].flow`,
   `sinks[n].enabled_in_data_streams`, and `timestamp_generator.enabled` to
   answer plainly before continuing.

3. **Create the config file.** Call
   `execute_action(action_name="configurator.create_from_template", params={"template_path": ..., "output_path": ...})`.
   If the user did not supply an output path, ask with `ask_followup_question`
   (default S32DS workspace / current directory / custom path) before proceeding.
   Record the returned `output_path` for all subsequent edit actions.

4. **Apply targeted edits.** Call one action per concern in any order:

   - **Cores:** `configurator.configure_core` with `core_name` (UI name from
     step 1) and `settings` containing any of `enabled`, `timestamp`,
     `start_on_launch`, `cycle_counting`, `trace_scenario`, `elf_images`,
     `module_base_address`, `mem_space`. When the user says "turn on timestamps"
     set both `set_timestamp_generator` (global hardware counter) and
     `configure_core` with `timestamp: true` (per-core ETM embedding).

   - **Sinks:** `configurator.configure_sink` with `sink_name` (e.g. `"ETF 2"`
     or `"DDR"`) and `settings` containing buffer size, mode, base address, etc.
     When switching to DDR also call `configure_data_streams` with
     `trace_location: ["DDR"]`.

   - **Data Streams:** `configurator.configure_data_streams` with
     `trace_location` (list of active sink names) and optionally
     `continuous_collection`.

   - **Target Access:** `configurator.set_target_access` with `settings`
     containing any of `server_address`, `server_port`, `launch_name`,
     `target_access_method`, `reset_before_config`, `sync_server_port`,
     `enable_user_code`, `endianness`.

   - **Output folder:** `configurator.set_output_folder` with `output_folder`.

   - **Timestamp generator:** `configurator.set_timestamp_generator` with
     `enabled` and optionally `module_base_address`, `counter_base_frequency`,
     `halt_on_debug`, `mem_space`.

   - **SoC modules:** `configurator.configure_soc_module` with `module_name`
     (e.g. `"ARM Funnel 2"`) and `settings` containing `enabled`,
     `module_base_address`, or `mem_space`.

5. **Inspect for unusual settings (on demand only).** Call
   `execute_action(action_name="configurator.inspect_template", params={"template_path": ...})`
   only when the user asks for "all available settings" or you must verify an
   enum value you have not seen.

6. **Verify.** Call
   `execute_action(action_name="configurator.describe_trace_flow", params={"config_path": <output_path>})`
   and confirm core enabled flags, active sink, and timestamp state match intent.

## Guardrails

**Scope**
- Operates on S32Trace configuration XML files only; never modifies S32DS
  projects, firmware, linker scripts, or debugger configs.

**Destructive actions**
- `configurator.create_from_template` overwrites an existing file at
  `output_path`. If the user supplies a path to an existing config without
  explicit overwrite intent, warn and offer a different name before proceeding.
- The `configure_*` and `set_*` edit actions modify the file in-place. Each
  returns `applied` listing the changes made; if a key is missing the attribute
  was not found in the XML -- call `configurator.inspect_template` to verify the
  correct attribute name.

**Secrets**
- No secrets or PII are involved; no redaction required.

**Refuse-and-escalate**
- No templates returned: S32DS may not be installed; ask for
  `s32ds_installation_path` or instruct the user to verify the install.
- Core name mismatch ("Core 0" vs UI name "M7_0"): ask which UI name to use;
  never guess.
- An edit action returns an empty `applied` list: call `configurator.inspect_template`,
  identify the correct attribute, then retry. Stop after 3 retries and report
  the issue.
- `success: false` with "No S32DS workspace runtime folder" on
  `create_from_template`: ask for an explicit `output_path`.

**Resource limits**
- Maximum 3 edit-retry iterations per attribute; report and stop if all fail.

## Validation loop

1. Each edit action returns `{config_path, applied: [...]}`. Confirm every
   intended key appears in `applied`.
2. After all edits call `execute_action(action_name="configurator.describe_trace_flow", params={"config_path": <output_path>})`
   and verify core enabled flags, active sink, and timestamp state match the user's intent.
3. Pass criterion: both checks green and the user confirms the file is at the
   expected location.

## Out of scope

- Installing or updating S32 Design Studio.
- Compiling or flashing firmware.
- Starting a debug session (use `s32debugger-*` skills).
- Generating code from a `.mex` file (use `s32ct-generate-code`).

## See Also

- `search_actions(query="configure core")` -- returns the full `settings` dict
  structure for core, sink, SoC module, and target-access actions.
