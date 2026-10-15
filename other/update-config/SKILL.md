---
name: Update Config
description: Safely update Nexo config files with read-before-write merges, schema-aware mapping, and reload/restart awareness.
requires:
  bins: []
  env: []
---

# Update Config

Update Nexo configuration intentionally and safely. Prefer minimal, reversible
patches that preserve existing structure and comments.

## Use when

- User asks to change runtime behavior through config instead of code.
- You need to edit files under `config/` or `config/plugins/`.
- You must wire skills/tools/models/bindings with explicit YAML changes.

## Do not use when

- The request is a source-code behavior change (edit Rust/TS files instead).
- The target setting cannot be mapped confidently to a known config file.
- The user asks only for one-off runtime commands with no config change needed.

## Input contract

- `request` (required): desired behavior change.
- `target_scope` (optional):
  `agent` | `llm` | `runtime` | `plugin` | `mcp` | `memory` |
  `tool_policy` | `explicit_file`.
- `target_file` (optional): required when `target_scope=explicit_file`.
- `merge_mode` (optional): `append_idempotent` (default) or `replace`.
- `confirm_before_write` (optional): default `true` for ambiguous or high-impact edits.
- `trigger_reload` (optional): default `true` for hot-reloadable files.

## Mapping rules

Prefer this mapping order:

1. Agent-level behavior (`skills`, `allowed_tools`, `system_prompt`,
   `inbound_bindings`, `model.model`, `web_search`, `link_understanding`)
   -> `config/agents.yaml` or `config/agents.d/<agent>.yaml`
2. Provider/auth/retry defaults -> `config/llm.yaml`
3. Reload watcher/migration/runtime knobs -> `config/runtime.yaml`
4. MCP client servers -> `config/mcp.yaml`
5. Plugin instance config -> `config/plugins/<plugin>.yaml`
6. Memory backend/vector knobs -> `config/memory.yaml`
7. Tool policy / gate rules -> `config/tool_policy.yaml`

If the request cannot be mapped unambiguously, ask the user before writing.

## Hot-reload vs restart

- Usually hot-reloadable: `config/agents.yaml`, `config/agents.d/**`,
  `config/llm.yaml`, `config/runtime.yaml`.
- Usually restart-required: `config/plugins/*.yaml`, `config/mcp.yaml`,
  `config/memory.yaml`, `config/broker.yaml`, `config/extensions.yaml`,
  plus structural agent changes (`id`, `plugins`, `workspace`, `skills_dir`).

After writing:
- if hot-reloadable: recommend `agent reload` (or rely on watcher),
- else: state explicitly that daemon restart is required.

## Canonical workflow

1. **Clarify intent**
   - Restate the requested behavior in concrete config terms.
2. **Resolve target file(s)**
   - Map request -> file path(s) using rules above.
3. **Read before write**
   - Load current file content first; never blind-overwrite.
4. **Prepare minimal merge patch**
   - Preserve unrelated keys and comments.
   - For arrays, default to idempotent append unless user requested replace.
5. **Apply edit**
   - Write only the required keys/values.
6. **Validate**
   - Check YAML/shape consistency (for example `agent --check-config`).
7. **Finalize**
   - Report exact file changes + reload/restart action required.

## Guardrails

- Never replace whole config files when a minimal patch is possible.
- Never inline secrets in YAML when `${file:...}` or env refs are expected.
- Never drop existing array entries unless user asked for replacement.
- Never claim live effect without stating hot-reload vs restart requirement.
- If validation fails, stop and report corrective action before proceeding.

## Output format

Always return:

- `status`: `applied` | `proposed` | `needs_user_input` | `validation_failed`
- `mapped_targets`: list of file paths with rationale
- `changes`: concrete key-level mutations
- `validation`: checks executed and result
- `activation`: `hot_reload` or `restart_required`
- `next_action`: required unless `status=applied`

## Examples

- `request="attach verify + stuck skills to agent ana"`
- `request="enable web_search tavily for ana binding"`
- `request="increase llm retry backoff" target_scope="llm"`
- `request="add whatsapp instance for sales bot" target_scope="plugin"`
