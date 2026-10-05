---
name: rudder-environment-check
description: Checks RudderStack tool prerequisites and reports status. Use when checking prerequisites, setup status, what tools are missing, or before running RudderStack workflows for the first time
allowed-tools: "Bash(which, curl, rudder-cli *, terraform *), Read"
---

# RudderStack Environment Check

Quick diagnostic that checks all RudderStack tool prerequisites and provides actionable guidance.

## When to Use

- Before starting with RudderStack workflows
- When troubleshooting "command not found" errors
- To verify your development environment is ready

## Check Process

Run these checks in sequence:

### 1. Check rudder-cli

```bash
# Check if installed
which rudder-cli

# If installed, check authentication
rudder-cli workspace info
```

### 2. Check Terraform (if using terraform workflows)

```bash
# Check if installed
which terraform

# If installed, check version
terraform version

# Check if provider is configured (run in project directory)
terraform providers
```

### 3. Check MCP Server Connectivity

```bash
# Check if hosted MCP server is reachable
curl -s -o /dev/null -w "%{http_code}" https://mcp.rudderstack.com/health
```

## Output Format

Present results as a status table:

```
RudderStack Environment Check
─────────────────────────────────────────────────────
Tool                    Status      Action
─────────────────────────────────────────────────────
rudder-cli              ✓ Ready
  └─ authenticated      ✓ Ready     Workspace: <name>
terraform               ✗ Missing   Run: /rudder-terraform-setup
  └─ provider           ─ Skipped   (terraform required first)
mcp.rudderstack.com     ✓ Reachable
─────────────────────────────────────────────────────
```

## Status Indicators

| Status | Meaning |
|--------|---------|
| ✓ Ready | Tool installed and configured |
| ✗ Missing | Tool not found, needs installation |
| ─ Skipped | Dependency not met, check parent first |
| ⚠ Issue | Tool found but configuration problem |

## Next Steps by Status

| Tool Missing | Action |
|--------------|--------|
| rudder-cli | Run `/rudder-cli-setup` or ask "help me install rudder-cli" |
| terraform | Run `/rudder-terraform-setup` or ask "help me setup terraform for rudderstack" |
| MCP unreachable | Run `/rudder-mcp-setup` or check network connectivity |

## Credential Security

- This skill only checks tool availability and authentication status
- Never logs or displays access tokens
- Workspace info shows only workspace name/ID, not credentials
