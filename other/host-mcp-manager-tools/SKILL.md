---
name: host-mcp-manager-tools
description: Use the Host MCP Manager plugin to install host MCP servers, store secrets, install local acon plugin bundles from the workspace, and inspect bundled plugin agent assets such as skills and MCP configs.
metadata:
  short-description: Use the Host MCP Manager MCP tools safely and correctly
---

# Host MCP Manager Tools

Use this skill when the user wants to:
- install or update a host MCP server
- store a host-side secret for later MCP use
- install a local `acon` plugin bundle from the managed workspace
- inspect bundled plugin `camelai.agentAssets`

The Host MCP Manager MCP server exposes these tools:

- `list_installed_servers`
- `prompt_to_store_secret`
- `install_stdio_server`
- `install_rest_api_server`
- `install_http_server`
- `uninstall_server`
- `list_installed_plugins`
- `install_workspace_plugin`
- `list_plugin_agent_assets`

## Rules

- Prefer this MCP server over ad hoc filesystem edits for host MCP server installs and plugin installs.
- Expect a host approval dialog for mutations. Do not claim success until the tool call completes successfully.
- Plugin `camelai.agentAssets` are reconciled declaratively on plugin load. Installing or refreshing a plugin automatically syncs its bundled skills and MCP configs into supported provider runtimes.
- If the user asks to create a plugin locally and make it available to the agent, the normal flow is:
  1. create the plugin files in the managed workspace
  2. call `install_workspace_plugin`
  3. optionally call `list_plugin_agent_assets` to confirm what the plugin declared
- If a tool is unavailable, say exactly which Host MCP Manager tool is missing.

## Tool guidance

### `list_installed_servers`

Use to inspect current persisted host MCP registrations before creating, updating, or deleting one.

### `prompt_to_store_secret`

Use when a host MCP server needs a secret.

- The agent never receives the raw secret back.
- The result is a `secretRef`.
- Use that `secretRef` in `envSecretRefs`, header secret refs, or REST API auth inputs.

### `install_stdio_server`

Use for a generic stdio MCP server that should be persisted in the host registry.

Provide:
- `id`
- `command`
- optional `args`
- optional `cwd`
- optional `env`
- optional `envSecretRefs`
- optional `name`
- optional `version`

### `install_rest_api_server`

Use when the user wants the builtin REST API MCP server.

Provide:
- `id`
- `baseUrl`
- optional auth config
- optional `name`
- optional `version`

Prefer this tool over manually constructing the builtin launcher command.

### `install_http_server`

Use for remote MCP servers over HTTP.

Provide:
- `id`
- `url`
- optional `transport` (`streamable-http` or `sse`)
- optional `headers`
- optional `headerSecretRefs`
- optional OAuth config
- optional `name`
- optional `version`

### `uninstall_server`

Use to remove a persisted host MCP server. Never try to uninstall `host-mcp-manager` itself.

### `list_installed_plugins`

Use to inspect currently discovered builtin and user plugins.

### `install_workspace_plugin`

Use to install or update a local `acon` plugin bundle from the managed workspace.

Provide:
- `path`: workspace-relative plugin folder path

Use this after the agent creates or updates plugin files in the workspace.
If the plugin declares `camelai.agentAssets`, the desktop backend will automatically sync those skills into Codex, Claude, PI, and OpenCode runtime state during plugin refresh. MCP configs sync into Codex and Claude runtime state.

### `list_plugin_agent_assets`

Use to discover which installed plugins declare bundled `camelai.agentAssets`.

This reports:
- bundled skill ids
- bundled MCP server ids
- install status by provider (`codex`, `claude`, `pi`, or `opencode`)

## Recommended flows

### Install a local plugin the agent just created

1. Create the plugin under the managed workspace.
2. Call `install_workspace_plugin`.
3. Optionally call `list_plugin_agent_assets` for that plugin id.
4. Tell the user what was installed and which providers received declaratively synced assets.

### Add a new host MCP server

1. If credentials are needed, call `prompt_to_store_secret`.
2. Install the server with `install_stdio_server`, `install_rest_api_server`, or `install_http_server`.
3. Summarize the installed server id and transport.

## Reporting

After using Host MCP Manager tools, report:
- which tool was called
- the ids affected
- whether the action installed, updated, removed, or only listed items
- any host approval dependency if relevant
