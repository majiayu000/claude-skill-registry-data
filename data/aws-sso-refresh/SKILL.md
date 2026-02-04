---
name: aws-sso-refresh
description: Automatically refresh AWS SSO authentication tokens when encountering expiration errors. Use when AWS MCP tools fail due to expired SSO sessions.
---

# AWS SSO Token Refresh

You are an expert at handling AWS SSO authentication token expiration and refresh.

## When to Use This Skill

Activate this skill when you encounter AWS SSO token expiration errors, such as:

- "Token has expired and refresh failed"
- "Error when retrieving token from sso"
- "The SSO session associated with this profile has expired"
- "ExpiredTokenException"
- Any AWS MCP tool failures mentioning authentication or token issues

## How to Refresh

Use the `mcp__aws-sso__refresh_aws_sso_token` tool. It automatically:

1. Looks up the correct AWS profile from MCP config files
2. Initiates the SSO login flow
3. Opens a browser for authentication

### Option 1: Pass the Server Name (Recommended)

When an MCP tool fails, pass the server name to automatically find the correct profile:

```
mcp__aws-sso__refresh_aws_sso_token(server: "bedrock-kb")
```

The tool searches multiple MCP client configs (Claude Code, Claude Desktop, Cursor, VS Code, Gemini CLI, etc.) to find the `AWS_PROFILE` for that server.

### Option 2: Pass the Profile Directly

If you know the profile name:

```
mcp__aws-sso__refresh_aws_sso_token(profile: "MCPServerReadAccess")
```

**Note:** At least one of `server` or `profile` must be provided. The tool does not use a default profile to prevent unintended authentication actions.

## Workflow

When an AWS MCP operation fails due to expired tokens:

1. **Identify the failing MCP server**: Note which tool failed (e.g., `mcp__bedrock-kb__*` → server is `bedrock-kb`)

2. **Call the refresh tool** with the server name:
   ```
   mcp__aws-sso__refresh_aws_sso_token(server: "bedrock-kb")
   ```

3. **Inform the user**: "Your AWS SSO session has expired. Please complete the authentication in your browser."

4. **Wait for completion**: The tool will return success/failure status

5. **Retry the operation**: Once refreshed, retry the original AWS operation

## Example

**Tool `mcp__bedrock-kb__ListKnowledgeBases` fails:**

```
Error: Token has expired and refresh failed
```

**Response:**

```
mcp__aws-sso__refresh_aws_sso_token(server: "bedrock-kb")
```

**Result:**

```json
{
  "success": true,
  "profile": "MCPServerReadAccess",
  "profileSource": "mcp_config",
  "message": "Successfully refreshed SSO token for profile \"MCPServerReadAccess\"."
}
```

Then retry `ListKnowledgeBases`.

## Supported MCP Clients

The tool automatically searches these config locations:

| Client | Config Location |
|--------|-----------------|
| Claude Code | `.mcp.json` |
| Claude Desktop | Platform app support directory |
| Cursor | `.cursor/mcp.json` |
| VS Code | `.vscode/mcp.json` |
| Gemini CLI | `.gemini/settings.json` |
| Copilot CLI | `~/.copilot/mcp-config.json` |
| Amazon Q | `~/.aws/amazonq/mcp.json` |
| Cline | VS Code extension settings |

## Proactive Behavior

- Automatically detect token expiration errors
- Use the `server` parameter to find the correct profile automatically
- If profile lookup fails, **always ask the user** which profile to use before retrying
- Never call the tool without a `server` or `profile` parameter
- Keep the user informed about authentication status

## Important Notes

- SSO login opens a browser window - ensure user can access it
- Tokens typically expire after several hours
- Multiple MCP servers may share the same profile
- After refresh, all servers using that profile will work again
- The tool has a 2-minute timeout for browser authentication
