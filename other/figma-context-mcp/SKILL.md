---
name: figma-context-mcp
description: Use GLips/Framelink Figma Context MCP (`figma-developer-mcp`) to read Figma design context, selected node data, and downloadable image assets while routing any approved official Figma writes through a separate `figma_write` provider. Use when Codex needs Figma file/node context for implementation, PPT layout repair, template matching, or visual reference while avoiding official Figma MCP read quota.
---

# Figma Context MCP

## Role

Use GLips/Framelink Figma Context MCP as the default Figma integration. Treat it as a read/context and image-download provider.

Do not use official Figma MCP tools by default. In particular, do not call `use_figma`, `create_new_file`, `generate_figma_design`, `upload_assets`, or official Figma screenshot/write tools unless the user explicitly authorizes an official Figma policy for the current run.

When official Figma tools are authorized, route them through the separate MCP provider named `figma_write`, not through the open-source `figma_context` provider.

## Required Inputs

- A Figma file URL or node-specific URL.
- The intended use: visual reference, template/style extraction, design-system context, or selected-node asset download.
- A local output directory when downloading images, usually `generated_assets/figma/`.
- `FIGMA_API_KEY` must be available through the global skill `.env` or user environment, but never print its value or commit it to the repository.

If a node-specific result is needed and the URL has no node id, ask for the specific Figma selection link before continuing.

## Workflow

1. Confirm the task only needs Figma context/read access.
2. Verify GLips/Framelink MCP is configured, usually as `figma_context`.
3. Fetch design context for the provided file or node.
4. Download only the images/assets needed for the current task.
5. Record source URL, file key, node id, downloaded paths, and limitations in the consuming workflow manifest.
6. Use local implementation tools for output: PPTX, HTML, SVG/PNG assets, screenshots, or code.

## Manuscript-to-PPT Policy

For `manuscript-to-ppt-workflow`, use this skill only after the production brief decides that Figma context is useful.

Default fields:

```yaml
figma_context_policy: optional
figma_write_policy: disabled
figma_context_provider: glips-framelink
figma_write_provider: figma_write
```

Allowed write policies:

- `disabled`: no official Figma tools.
- `official-exempt-only`: use only official tools documented as exempt from standard read-tool limits when they match the task, such as `generate_figma_design`, `add_code_connect_map`, or `whoami`.
- `official-write-explicit`: allow broader official write-to-canvas tools such as `use_figma`, `create_new_file`, `upload_assets`, or `generate_diagram` after confirming permissions and risks.

Allowed Figma-context outputs:

- style/layout notes for selected slides
- downloaded reference images
- local SVG/PNG redraw inputs
- `align/figma_layout_polish_manifest_v*.csv`
- before/after screenshot evidence from local PPTX or HTML renders

Not allowed by default:

- creating or editing Figma files
- generating new Figma frames
- using official Figma Remote MCP as an automatic fallback
- replacing the whole deck with full-slide screenshots unless the brief accepts that editability tradeoff

## Configuration Notes

To persist `FIGMA_API_KEY` safely for this skill, prefer the bundled setup script. It prompts for the token without echoing it, copies this skill to the user-level global skill directory, writes the key to the global skill `.env`, and updates the `figma_context` MCP server to load that `.env` on demand.

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\figma-context-mcp\scripts\configure_figma_api_key.ps1
```

The script writes the key to:

```text
%USERPROFILE%\.codex\skills\figma-context-mcp\.env
```

Do not commit repo-local `.env` files.

The recommended Codex MCP server is local stdio:

```toml
[mcp_servers.figma_context]
command = "cmd"
args = ["/c", "npx", "-y", "figma-developer-mcp", "--env", "%USERPROFILE%\\.codex\\skills\\figma-context-mcp\\.env", "--stdio", "--image-dir", "generated_assets\\figma", "--format", "yaml"]
```

Optional official write provider:

```toml
[mcp_servers.figma_write]
url = "https://mcp.figma.com/mcp"
```

`figma_write` requires OAuth login, the right Figma seat type, and edit permissions for existing files. Keep it separate from `figma_context` so logs and prompts clearly show whether a run used open-source reads or official writes.

Keep the Figma personal access token outside the repository. Prefer the setup script's user-level global skill `.env`; a user-level environment variable such as `FIGMA_API_KEY` is also acceptable. If it is missing, report that Figma context cannot be fetched yet and continue with local fallback only when the parent workflow allows it.

## Done Criteria

- The output states whether Figma context was fetched, skipped, or blocked.
- No official Figma tools were used unless explicitly authorized by `figma_write_policy`.
- All downloaded assets are traceable to a Figma source URL/node.
- Any missing node, auth, proxy, or download issue is disclosed.
