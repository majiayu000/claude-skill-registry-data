---
name: codex-mcp
description: Use this `codex-mcp` skill to instruct another AI Agent to invoke a tool or execute a workflow on your behalf for the following scenario, 1.When you are requested to invoke a mcp tool that you don't have access (can use `ListMcpResourcesTool` to check) such as `context7`, `github`, `linear`, `jira`; 2.When you are requested to execute a complex workflow that require interacting with multiple mcp tools and bash CLI commands for example `github-project-create-items`, `github-project-list-items` workflows;
---
# codex-mcp

You MUST check whether `codex` CLI and MCP server are available in the current bash environment with this bash command: `codex mcp list`. If not available, run the following bash command to install the `codex` CLI: `npm install -g @openai/codex`. Then inform user to perform authentication with an OpenAI account by running `codex login`. Ignore this instruction if the CLI is already available.

## Tools

### mcp__codex__codex

Run a Codex session. Accepts configuration parameters matching the Codex Config struct. Supported properties:

| Property                | Type   | Description                                                                                                                                            |
| ----------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`prompt`** (required) | string | Initial user prompt that seeds the Codex conversation.                                                                                                 |
| `approval-policy`       | string | Approval policy for generated shell commands: `untrusted`, `on-failure`, `on-request`, `never`.                                                        |
| `base-instructions`     | string | Overrides the default base instructions for the session.                                                                                               |
| `compact-prompt`        | string | Prompt used when compacting the conversation.                                                                                                          |
| `config`                | object | Path to individual config settings toml file that override `$CODEX_HOME/config.toml` (see [codex-config-toml-structure.md](codex-config-toml-structure.md) to understand how to create this file).                 |
| `cwd`                   | string | Working directory for the session. Relative paths resolve from the server process root.                                                                |
| `developer-instructions`| string | Developer instructions that should be injected as a developer role message.                                                                            |
| `model`                 | string | Optional override for the model name (e.g., `gpt-5.1-codex-mini`, `gpt-5.1-codex`) default is `gpt-5-codex`.                                                                                       |
| `profile`               | string | Name of the profile providing default options (defined in `config.toml`).                                                                                           |
| `sandbox`               | string | Sandbox mode: `read-only`, `workspace-write`, or `danger-full-access`.                                                                                 |

### mcp__codex__codex-reply

Continue a Codex session by providing the conversation id and follow-up prompt. Supported properties:

| Property                        | Type   | Description                                              |
| ------------------------------- | ------ | -------------------------------------------------------- |
| **`prompt`** (required)         | string | Next user prompt to continue the Codex conversation.     |
| **`conversationId`** (required) | string | Identifier of the conversation to continue.              |

## Operational Requirements

- Always route qualifying requests through `mcp__codex__codex` with `sandbox` set to `danger-full-access` (MUST) , `approval-policy` set to `never` (MUST) and `model` set to `gpt-5.1-codex-mini` (SHOULD).
- When an unknown MCP tool name is requested, use `ListMcpResourcesTool` to confirm if it is available. If not available, delegate to `codex` to invoke this MCP tool by crafting a `prompt` with all necessary information and file referrences.
- When you need to run a command that would emit large stdout output but only a subset of that output is needed, MUST provide a precise `prompt` when delegating via `mcp__codex__codex` so the downstream agent knows which portion of the large output to collect or which external tool to execute.
- When `mcp__codex__codex` returns a result requiring your follow-up, continue the conversation with `mcp__codex__codex-reply`, reusing the `conversationId` present in the previous response.

## Known MCP Server Tools

- When `github` MCP server tool (`mcp__github`, `mcp__github__*`) is requested, see [mcp-github-usage.md](mcp-github-usage.md) for detailed usage instructions. Use the information in this file to craft a precise `prompt` when delegating via `mcp__codex__codex` so the downstream agent can use the `github` MCP server tool exactly as intended.
- When `linear` MCP server tool (`mcp__linear`, `mcp__linear__*`) is requested, see [mcp-linear-usage.md](mcp-linear-usage.md) for detailed usage instructions. Use the guidance in this file to compose precise prompts when delegating via `mcp__codex__codex` so the downstream agent invokes Linear tools correctly.
- When `context7` MCP server tool is requested, see [mcp-context7-usage.md](mcp-context7-usage.md) for detailed usage instructions. 
