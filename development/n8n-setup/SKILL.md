---
name: n8n-setup
description: Verify n8n MCP connection and configure n8n MCP servers. Use when the user asks to "verify n8n connection", "check n8n MCP", "test n8n setup", "configure n8n", "set up n8n MCP", or needs to confirm that n8n MCP integration is operational.
---

# n8n MCP Setup & Verification

Configure and verify n8n MCP server connections for workflow development.

---

## Two MCP Server Types

n8n provides two complementary MCP servers. Each serves a different purpose.

### External MCP (`n8n-mcp-external`)

Third-party MCP server by czlonkowski. Optimized for workflow **development**.

- **28 tools**: 7 core (`tools_documentation`, `search_nodes`, `get_node`, `validate_node`, `validate_workflow`, `search_templates`, `get_template`) that work offline, plus 21 `n8n_*` tools that talk to your instance (Public API, and — with `N8N_MCP_ACCESS_TOKEN` — the instance-level MCP)
- Installed via `npx n8n-mcp`
- Communicates over **stdio** transport
- Best for: building, editing, validating, and debugging workflows
- Repository: https://github.com/czlonkowski/n8n-mcp

**Key capabilities:**
- Search and inspect ~840 built-in nodes plus verified and unverified community nodes (do not hard-code the count)
- Validate node configurations against schemas
- Create, read, update, delete workflows (JSON-based)
- Deploy from the community template library
- Manage credentials (create, update, delete, list schemas)
- Audit instance security
- Manage data tables, rows and columns
- Auto-fix validation errors
- Run workflows without an external trigger (`n8n_test_workflow` with `prepare` / `pinned` / `direct`)
- Manage n8n Agents (`n8n_manage_agents`, Preview)

> `npx n8n-mcp` always pulls the latest release. For a reproducible setup pin it: `npx n8n-mcp@<version>` (find the current one with `npm view n8n-mcp version`).

### Native MCP (`n8n-native-mcp`)

Official MCP server built into n8n. Optimized for SDK-based workflow **creation**, publishing and Agents.

- **54 tools** on n8n 2.41 (the set depends on the n8n version): workflow builder, workflow management, executions and tests, versions, credentials (read-only), projects and folders, data tables, Agents
- Built into n8n (no separate install)
- Communicates over **HTTP** transport
- Best for: creating workflows from TypeScript SDK code, atomic edits, testing, publishing, building n8n Agents
- Needs n8n with instance-level MCP enabled — see the version table below

**Key capabilities:**
- Get the SDK reference, best practices per technique, and type definitions
- Search and discover nodes with discriminators
- Create workflows from TypeScript SDK code and validate it first
- Edit workflows with atomic operations (`update_workflow`)
- Execute (manual or production), test with pin data, read results
- Publish/unpublish/archive, browse and restore version history
- Search projects, folders and tags; manage data tables
- Build, test and publish first-class n8n Agents (Preview)

### Minimum n8n versions

| Capability | n8n |
|-----------|-----|
| Instance-level MCP | 2.2.0 |
| Builder tools (create and edit workflows) | 2.13.0 |
| Partial `update_workflow` (operations list) | 2.20.0 |
| Connect dialog, OAuth, `/publish` routes | 2.33.0 |
| Agents tools, renamed native tools, `n8n_test_workflow` `prepare`/`pinned`/`direct`, column actions | 2.34.0 |

Agents are **Preview**.

---

## Environment Variables

Set these at the **project level** (not plugin level). The plugin references them via `${VAR}` placeholders.

### For External MCP

| Variable | Description | How to Generate |
|----------|-------------|-----------------|
| `N8N_API_URL` | n8n instance URL — root (`https://your-n8n.example.com`) or ending in `/api/v1`; both work | Your n8n deployment URL |
| `N8N_API_KEY` | Public API key | n8n UI: Settings → n8n API → Create an API key |
| `N8N_MCP_ACCESS_TOKEN` | *Optional.* The instance-level MCP access token. A separate secret from `N8N_API_KEY`; it unlocks `n8n_test_workflow` (`prepare`/`pinned`/`direct`), `n8n_manage_agents`, `n8n_explore_node_resources`, `n8n_workflow_versions` with `source: "native"`, the column actions of `n8n_manage_datatable`, and the MCP fallback of `n8n_list_catalog`. The endpoint is derived from `N8N_API_URL`. | n8n UI: Settings → Instance-level MCP → Connect → **API key** tab (n8n 2.33+; earlier versions show the token on the MCP settings page) |

Optional extras: `N8N_CF_CLIENT_ID` / `N8N_CF_CLIENT_SECRET` (Cloudflare Access in front of n8n), `DISABLED_TOOLS` (comma-separated tool names to hide, for a read-only setup).

### For Native MCP

| Variable | Description | How to Generate |
|----------|-------------|-----------------|
| `N8N_NATIVE_MCP_URL` | Full MCP endpoint URL (e.g., `https://your-n8n.example.com/mcp-server/http`) | n8n UI: Settings → Instance-level MCP → Connect → **Server URL** |
| `N8N_MCP_TOKEN` | MCP access token (sent as a `Bearer` header) — the same kind of value as `N8N_MCP_ACCESS_TOKEN` | n8n UI: Settings → Instance-level MCP → Connect → **API key** tab |

MCP access must be enabled first: **Settings → Instance-level MCP → Enable MCP access** (instance owner or admin). Each workflow you want the client to run or edit must also be switched on (**Available in MCP**, only for published workflows with a webhook, form, schedule or chat trigger) — see the **n8n-native-mcp** skill.

### Setting Environment Variables

Store these in your shell profile or project-level `.env`:

```bash
export N8N_API_URL="https://your-n8n.example.com"
export N8N_NATIVE_MCP_URL="https://your-n8n.example.com/mcp-server/http"
export N8N_API_KEY="your-api-key-here"
export N8N_MCP_TOKEN="your-mcp-token-here"
export N8N_MCP_ACCESS_TOKEN="your-mcp-token-here"   # optional, see above
```

**Security note:** Never commit API keys or tokens to version control. Use environment variables or a secrets manager.

### OAuth instead of a token (native MCP)

The Connect dialog recommends **OAuth** over a pasted token. Keep the server name `n8n-native-mcp` so that the tool names in these skills (`mcp__n8n-native-mcp__...`) resolve:

```bash
claude mcp add --transport http n8n-native-mcp https://<n8n-host>/mcp-server/http
```

Then run `/mcp` in Claude Code, pick **n8n-native-mcp** and finish the sign-in in the browser. No `N8N_MCP_TOKEN` is needed in that case. (The OAuth login is an interactive step the user performs.)

---

## Project `.mcp.json` Configuration

Create or update `.mcp.json` in your project root.

### External MCP Only (stdio)

Use when you need workflow development tools — node search, validation, workflow CRUD, templates, credentials, audit.

```json
{
  "mcpServers": {
    "n8n-mcp-external": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "${N8N_API_URL}",
        "N8N_API_KEY": "${N8N_API_KEY}",
        "N8N_MCP_ACCESS_TOKEN": "${N8N_MCP_ACCESS_TOKEN:-}"
      }
    }
  }
}
```

`${N8N_MCP_ACCESS_TOKEN:-}` keeps the token optional: with it unset the server starts and only the token-gated tools answer `NOT_CONFIGURED`.

### Native MCP Only (HTTP)

Use when you need SDK-based workflow creation, testing, publishing and Agents.

```json
{
  "mcpServers": {
    "n8n-native-mcp": {
      "type": "http",
      "url": "${N8N_NATIVE_MCP_URL}",
      "headers": {
        "Authorization": "Bearer ${N8N_MCP_TOKEN}"
      }
    }
  }
}
```

### Combined Configuration (Both Servers)

Use when you need the full capability set — development tools from external plus SDK-based creation, testing and Agents from native.

```json
{
  "mcpServers": {
    "n8n-mcp-external": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "${N8N_API_URL}",
        "N8N_API_KEY": "${N8N_API_KEY}",
        "N8N_MCP_ACCESS_TOKEN": "${N8N_MCP_ACCESS_TOKEN:-}"
      }
    },
    "n8n-native-mcp": {
      "type": "http",
      "url": "${N8N_NATIVE_MCP_URL}",
      "headers": {
        "Authorization": "Bearer ${N8N_MCP_TOKEN}"
      }
    }
  }
}
```

---

## Verification Steps

After configuring `.mcp.json`, verify each server is operational.

### Verify External MCP

**Step 1: Health check**

Call `mcp__n8n-mcp-external__n8n_health_check`.

Expected: `status` is `healthy` (`degraded` means the instance answers but something is off; `error` means the URL or key is wrong). The response also carries `mcpVersion`, `supportedN8nVersion`, `versionCheck` (`current`, `latest`, `upToDate`, `updateCommand`), `features` and `performance`. `n8nVersion` is usually **absent** — n8n stopped exposing its version to API clients in 1.119.0 and the response says so in `n8nVersionNote`. That is not an error and not worth retrying; probe capabilities by calling the API instead of comparing versions. With `N8N_MCP_ACCESS_TOKEN` set, an `officialMcp` block reports whether the instance-level MCP is reachable.

If `status` is `error`, `N8N_API_URL` or `N8N_API_KEY` is wrong. `mode: "diagnostic"` adds debug detail.

**Step 2: Test node search**

Call `mcp__n8n-mcp-external__search_nodes` with `query: "webhook"`.

Expected: a list of matching nodes including `n8n-nodes-base.webhook`.

**Step 3: Test workflow listing**

Call `mcp__n8n-mcp-external__n8n_list_workflows`.

Expected: a list of existing workflows (may be empty on fresh instances).

### Verify Native MCP

**Step 1: Search workflows**

Call `mcp__n8n-native-mcp__search_workflows` with `limit: 1`.

Expected: a preview list (may be empty on fresh instances). A result or an empty list without errors means the connection and the token work. This call returns previews of **every** workflow the user can see, whether or not it is exposed to MCP.

**Step 2: Get SDK reference**

Call `mcp__n8n-native-mcp__get_workflow_sdk_reference` with `section: "rules"`.

Expected: the SDK rules. This confirms the builder tools are available (n8n 2.13+).

**Step 3: Search nodes**

Call `mcp__n8n-native-mcp__search_nodes` with `queries: ["webhook"]`.

Expected: node search results with IDs and discriminators.

### Quick Verification Checklist

| Check | Tool | Pass Condition |
|-------|------|----------------|
| External health | `n8n_health_check` | `status: "healthy"` |
| External nodes | `search_nodes` | Returns node results |
| External workflows | `n8n_list_workflows` | Returns list (no auth error) |
| Native workflows | `search_workflows` | Returns list (no auth error) |
| Native SDK | `get_workflow_sdk_reference` | Returns documentation |
| Native nodes | `search_nodes` | Returns results with discriminators |

---

## Available Tools by Server

### External MCP Tools (28)

| Tool | Purpose |
|------|---------|
| `tools_documentation` | Tool docs, AI agent guide (`topic: "ai_agents_guide"`), Code node guides |
| `search_nodes` | Find nodes by keyword |
| `get_node` | Get node details, docs, property search, versions |
| `validate_node` | Validate node configuration |
| `validate_workflow` | Validate a complete workflow JSON |
| `search_templates` | Search community templates |
| `get_template` | Get template details |
| `n8n_health_check` | Verify connection to the n8n instance |
| `n8n_create_workflow` | Create workflow from JSON |
| `n8n_get_workflow` | Get workflow by ID (`full`, `details`, `structure`, `minimal`, `active`, `filtered`) |
| `n8n_list_workflows` | List workflows |
| `n8n_update_full_workflow` | Replace the entire workflow |
| `n8n_update_partial_workflow` | Update specific nodes/connections (diff operations) |
| `n8n_delete_workflow` | Delete workflow |
| `n8n_validate_workflow` | Server-side validation of a deployed workflow |
| `n8n_autofix_workflow` | Auto-fix validation errors |
| `n8n_deploy_template` | Deploy template to the instance |
| `n8n_test_workflow` | Run a workflow (HTTP trigger, or `prepare`/`pinned`/`direct` via the instance MCP) |
| `n8n_executions` | Get, list and delete executions |
| `n8n_evaluations` | Evaluation test runs (read from n8n 2.30, run/cancel from 2.32) |
| `n8n_workflow_versions` | Version history, diff, rollback (`source: "local"` or `"native"`) |
| `n8n_manage_credentials` | CRUD and schema discovery for credentials |
| `n8n_manage_datatable` | Data tables, rows and (with the token) columns |
| `n8n_manage_folders` | Workflow folders (n8n 2.19+) |
| `n8n_manage_agents` | n8n Agents (needs `N8N_MCP_ACCESS_TOKEN`, n8n 2.34+, Preview) |
| `n8n_list_catalog` | Projects and tags |
| `n8n_explore_node_resources` | Resolve dropdown / resource-locator values with a real credential (needs the token) |
| `n8n_audit_instance` | Security audit |

### Native MCP Tools (54)

| Group | Tools |
|-------|-------|
| Builder | `get_workflow_sdk_reference`, `get_workflow_best_practices`, `search_nodes`, `get_node_types`, `validate_node_config`, `validate_workflow`, `create_workflow_from_code`, `update_workflow`, `explore_node_resources`, `list_n8n_gateway_services` |
| Management | `search_workflows`, `get_workflow_details`, `publish_workflow`, `unpublish_workflow`, `archive_workflow` |
| Executions and tests | `execute_workflow`, `get_workflow_execution`, `search_workflow_executions`, `prepare_workflow_pin_data`, `test_workflow` |
| Versions | `get_workflow_history`, `get_workflow_version`, `get_workflow_versions_diff`, `restore_workflow_version` |
| Credentials | `list_credentials` |
| Organisation | `search_projects`, `search_folders`, `create_folder`, `update_folder`, `move_workflows_to_folder`, `list_workflow_tags` |
| Data tables | `search_data_tables`, `create_data_table`, `rename_data_table`, `add_data_table_column`, `rename_data_table_column`, `delete_data_table_column`, `get_data_table_rows`, `add_data_table_rows` |
| Agents | `get_agent_builder_reference`, `discover_agent_assets`, `create_agent`, `get_agent`, `search_agents`, `mutate_agent`, `validate_agent`, `call_agent`, `publish_agent`, `unpublish_agent`, `revert_agent`, `list_agent_versions`, `delete_agent`, `update_agent_integration`, `verify_agent_mcp_server` |

---

## When to Use Which MCP

Choose the right server based on the task.

| Task | Recommended MCP | Reason |
|------|-----------------|--------|
| Search/discover nodes | External | Richer search with docs mode |
| Validate node config | External or Native | External: validation profiles; Native: `validate_node_config` |
| Create workflow (JSON) | External | Direct JSON structure |
| Create workflow (SDK code) | Native | TypeScript SDK with type safety |
| Edit workflow incrementally | Either | External `n8n_update_partial_workflow`, Native `update_workflow` operations |
| Deploy templates | External | Template library |
| Run/test a workflow | Both | Native `execute_workflow` / `test_workflow`; External `n8n_test_workflow` |
| Manage credentials | External | Full CRUD + schema discovery (Native only lists them) |
| Security audit | External | Built-in + custom deep scan |
| Publish/unpublish | Native (or External `activateWorkflow` / `deactivateWorkflow` operations) | Publish lifecycle |
| Version history | Either | Native: n8n's own history; External: local snapshots or `source: "native"` |
| Node type definitions | Native | TypeScript-level detail with discriminators |
| Projects, folders, tags | Native or External | Native search tools; External `n8n_manage_folders`, `n8n_list_catalog` |
| n8n Agents | Native (or External `n8n_manage_agents`) | Builder reference and mutation tools |

### Decision Flowchart

```
Need to BUILD a workflow?
├── From scratch with type safety → Native (SDK code)
├── From JSON structure → External (create_workflow)
└── From community template → External (deploy_template)

Need to EDIT a workflow?
├── Change specific nodes → Native (update_workflow) or External (update_partial)
├── Replace entire workflow → External (update_full)
└── Redesign from new SDK code → Native (create_workflow_from_code, as a new workflow)

Need to RUN a workflow?
├── Has a webhook/form/chat trigger → External (test_workflow) or Native (execute_workflow)
└── No external trigger → Native (prepare_workflow_pin_data + test_workflow, or execute_workflow manual)

Need to MANAGE the instance?
├── Credentials → External
├── Security audit → External
├── Data tables → Either
└── Projects/folders → Native or External

Need an AGENT (not a workflow)?
└── Native (get_agent_builder_reference → create_agent → mutate_agent → validate_agent → call_agent)
```

---

## Troubleshooting

For common connection issues:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "Connection refused" | n8n not running or wrong URL | Verify N8N_API_URL is correct and n8n is running |
| "401 Unauthorized" | Invalid API key or token | Regenerate the key in n8n Settings → n8n API (Public API) or Settings → Instance-level MCP → Connect (MCP) |
| "npx n8n-mcp not found" | Package not available | Run `npx n8n-mcp` manually to verify install |
| External tools timeout | n8n instance unreachable | Check network, firewall, VPN |
| Native MCP 404 | MCP not enabled in n8n | Settings → Instance-level MCP → Enable MCP access (owner or admin) |
| Native tool refused on a workflow | Workflow not "Available in MCP" or not published with an eligible trigger | Enable it for that workflow (see **n8n-native-mcp**) |
| External `NOT_CONFIGURED` | `N8N_MCP_ACCESS_TOKEN` missing | Set the token (Connect → API key) or skip the token-gated tools |
| "ECONNREFUSED" on localhost | Wrong port | Default n8n port is 5678; verify with `N8N_API_URL=http://localhost:5678` |
| Partial tool failures | API key lacks permissions | Create a new API key with full permissions |

For detailed troubleshooting procedures, refer to the **troubleshoot** skill.

---

## Setup Checklist

Use this checklist when setting up n8n MCP for a new project:

1. [ ] n8n instance is running and accessible (2.13+ for the native builder tools)
2. [ ] API key generated (for external MCP)
3. [ ] MCP enabled in Settings → Instance-level MCP, and an MCP token or OAuth login set up (for native MCP)
4. [ ] Environment variables set (`N8N_API_URL`, `N8N_API_KEY`, `N8N_NATIVE_MCP_URL`, `N8N_MCP_TOKEN`, optionally `N8N_MCP_ACCESS_TOKEN`)
5. [ ] `.mcp.json` created in project root with desired server(s)
6. [ ] External MCP health check passes
7. [ ] Native MCP `search_workflows` succeeds
8. [ ] Both servers return tool results without auth errors
9. [ ] Workflows the client must run or edit are switched on as **Available in MCP**

---

## Official n8n resources

- **n8n-io/skills** — the official n8n skill pack for the instance-level MCP server: https://github.com/n8n-io/skills
- **n8n docs MCP servers** (search the docs from your coding agent):
  ```bash
  claude mcp add --transport http n8n-docs https://docs.n8n.io/~gitbook/mcp
  ```
  A second endpoint (Kapa.ai, docs plus forum and blog, needs a browser sign-in) is listed on https://docs.n8n.io/connect/connect-to-n8n-docs-mcp-server