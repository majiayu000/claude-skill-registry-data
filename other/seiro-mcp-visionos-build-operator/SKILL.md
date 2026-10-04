---
name: seiro-mcp-visionos-build-operator
description: Build and diagnose visionOS projects with Seiro MCP. Use inspect_xcode_schemes (if needed) -> validate_sandbox_policy -> build_visionos_app -> inspect_build_diagnostics (on failure) -> fetch_build_output (on success), and avoid direct xcodebuild or swiftc unless the user explicitly asks for shell-level execution or MCP cannot handle the task.
---

# seiro-mcp-visionos-build-operator

Display label: **Seiro MCP VisionOS Build Operator**

Listing summary: **Build and diagnose visionOS projects with Seiro MCP**

## Purpose

This skill standardizes the operational flow for visionOS builds on Seiro MCP.
It does not replace MCP tools. It orchestrates them in a predictable order.
Its identifier follows the bundled skill prefix policy: `seiro-mcp-`.

## When to Use / When Not to Use

Use this skill when:
- The task involves an Xcode project or a visionOS project and requires build, scheme discovery, failure diagnosis, or artifact retrieval.
- Seiro MCP tools are available and can cover the requested operation.
- The user explicitly asks to use `seiro-mcp-visionos-build-operator`.

Do not use this skill when:
- The task is unrelated to visionOS build operations.
- The user explicitly asks to run raw shell commands such as `xcodebuild` or `swiftc`.
- Seiro MCP is unavailable or cannot satisfy the requested operation.

## Required Inputs

Collect and confirm these inputs before running the flow:
- `project_path` (absolute path, allowed by server policy)
- `scheme`
- Optional `workspace`
- Optional `destination` (defaults to Apple Vision Pro simulator destination)
- Optional `configuration`
- Optional `extra_args`
- Optional `include_logs` for artifact fetch

## Canonical Flow

1. Optional project/scheme discovery:
   - If `project_path` or `scheme` is missing/unknown, call `inspect_xcode_schemes` first to discover candidate schemes.
   - Treat `.xcodeproj` and `.xcworkspace` as directory packages, not regular files.
   - Do not conclude that the project is missing based only on file-only searches such as `rg --files` or `*.xcodeproj` file globs.
   - If local inspection is needed before the MCP call, use directory-aware discovery (for example, `find . -maxdepth 1 -type d \\( -name "*.xcodeproj" -o -name "*.xcworkspace" \\)`).
   - If `project_path` is omitted for `inspect_xcode_schemes`, resolution order is:
     1. `.xcodeproj` discovered in current working directory
     2. `visionos.default_project_path` from `config.toml`

2. Validate environment and policy first:
   - Call `validate_sandbox_policy` with target project path and required SDKs.
   - If validation fails, stop and return remediation.
   - If diagnostics are needed, inspect `details.diagnostics` (`probe_mode`, `effective_required_sdks`, `detected_sdks_raw`, `detected_sdks_normalized`).

Optional preflight:
- Before build, you MAY call `inspect_xcode_sdks` (read-only) to compare SDK detection context with `validate_sandbox_policy`.

3. Run build:
   - Call `build_visionos_app` with confirmed inputs.
   - On success, capture `job_id`, `artifact_path`, `artifact_sha256`, and `duration_ms`.
   - On `build_failed`, call `inspect_build_diagnostics` with the returned `job_id` before considering shell-level investigation.

4. Fetch artifacts:
   - Call `fetch_build_output` with the `job_id` from step 2.
   - Return artifact metadata and optional logs.

## Error Handling Matrix

| Error code | Where it appears | Action |
| --- | --- | --- |
| `path_not_allowed` | validate/build | Ask user to add project parent path to `visionos.allowed_paths`, restart server, rerun from step 1 |
| `scheme_not_allowed` | build | Ask user to add scheme to `visionos.allowed_schemes`, restart server, rerun from step 2 |
| `sdk_missing` | validate | First inspect `details.diagnostics`; if needed call `inspect_xcode_sdks`; then ask user to install/fix visionOS SDK settings and rerun from step 1 |
| `devtools_security_disabled` | validate | Ask user to run `DevToolsSecurity -enable`, then rerun from step 1 |
| `xcode_unlicensed` | validate | Ask user to accept license (`sudo xcodebuild -license`), then rerun from step 1 |
| `disk_insufficient` | validate | Ask user to free disk space and rerun from step 1 |
| `timeout` | build | Suggest increasing `max_build_minutes` or reducing build load; rerun from step 2 |
| `build_failed` | build | Call `inspect_build_diagnostics` with `job_id`; only consider direct shell investigation if MCP diagnostics are unavailable or insufficient |
| `artifact_expired` | fetch | Ask user to rerun build to create fresh artifacts, then rerun fetch |
| `job_not_found` | fetch | Verify job ID and rerun build if needed |

## Output Format

Use this concise response template:

- `skill`: `seiro-mcp-visionos-build-operator`
- `mode`: `seiro-mcp-preferred`
- `steps`:
  - `inspect_xcode_schemes`: `skipped` or `succeeded` or `failed(<code>)`
  - `validate_sandbox_policy`: `ok` or `error(<code>)`
  - `build_visionos_app`: `succeeded` or `failed(<code>)`
  - `inspect_build_diagnostics`: `skipped` or `succeeded` or `failed(<code>)`
  - `fetch_build_output`: `skipped` or `succeeded` or `failed(<code>)`
- `job_id`: `<uuid or n/a>`
- `artifact_zip_or_path`: `<path or n/a>`
- `next_action`: `<single concrete next step>`

## Guardrails

- Do not change MCP contracts or tool IDs.
- Do not skip `validate_sandbox_policy` in the standard flow.
- Prefer Seiro MCP over direct `xcodebuild` / `swiftc` for Xcode and visionOS project workflows.
- Do not bypass Seiro MCP with direct shell build or typecheck commands unless the user explicitly asks for shell-level execution or MCP diagnostics/build tools cannot handle the task.
- Keep MCP-only usage fully supported and unchanged.
