---
name: local-setup
description: Interactive setup workflow for running the Magnet MCP server locally (project-specific, magnet-app directory only). Use when user says "local setup", "run locally", "test locally", "configure MCP", or "set up local development".
---

# Local MCP Server Setup

This skill walks users through setting up the Magnet MCP server for local development and testing with their MCP client (Claude Code, Cursor, Claude Desktop).

**Important:** This setup configures the MCP server to talk to a **local Magnet instance** (localhost:3000), not production. The user must have the Magnet web app running locally.

## When to Use This Skill

Use this skill when the user requests:
- Setting up local development environment
- Running the MCP server locally
- Testing the MCP server before deploying
- Configuring their MCP client to use local version
- Troubleshooting local MCP connection issues

## Instructions

### Step 1: Check Prerequisites

Verify the development environment is ready:

```bash
# Check Node.js version (must be >= 22.2.0)
node --version

# Check pnpm is installed
pnpm --version

# Check if dependencies are installed
ls node_modules/.bin/tsc 2>/dev/null && echo "Dependencies installed" || echo "Need to install dependencies"
```

If dependencies are missing, install them:
```bash
pnpm install
```

### Step 2: Confirm Project-Specific Scope

**Important:** This setup configures the MCP server for the `magnet-app` project directory only. The MCP server will NOT be available when working in other directories.

Use AskUserQuestion to confirm the user understands:

Question: "This will configure the MCP server for your magnet-app project directory only. It will NOT be available globally in other projects. Do you understand and want to proceed?"
Options:
- "Yes, I understand it's project-specific" - Continue with setup
- "No, I need global setup" - Inform user that global setup requires manual configuration in ~/.claude/ and is not covered by this skill

If the user needs global setup, explain:
- Global MCP configuration is not officially supported by Claude Code
- They would need to manually configure ~/.claude/settings.json or use the plugins system
- Recommend using project-specific setup for most use cases

### Step 3: Verify Local Magnet Server is Running

Check that the local Magnet web app is running:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "Not running"
```

If it returns 200 (or redirects), the server is running. If not, inform the user they need to start the Magnet web app first before continuing.

### Step 4: Build the MCP Server Project

Build the TypeScript project:
```bash
pnpm build
```

Verify the build succeeded:
```bash
ls -la dist/index.js
```

### Step 5: Check for Existing Environment Configuration

Check if .env file exists with API key:
```bash
if [ -f .env ]; then
  echo ".env file exists"
  grep -q "MAGNET_API_KEY" .env && echo "API key configured" || echo "API key missing"
else
  echo "No .env file found"
fi
```

If no .env file, check .env.sample for template:
```bash
cat .env.sample 2>/dev/null
```

### Step 6: Gather API Key

Use AskUserQuestion to get the Magnet API key if not already configured. Since this is a local setup, the API key must come from the **local Magnet instance** (not production).

Question: "Do you have an API key from your local Magnet instance?"
Options:
- "Yes, I have one" - Prompt them to provide it
- "No, I need to get one" - Direct them to http://localhost:3000/settings to generate one from their local instance
- "Use existing .env file" - Read from existing .env if present

If they provide a key, store it:
```bash
echo "MAGNET_API_KEY=<their-key>" > .env
echo "MAGNET_WEB_API_BASE_URL=http://localhost:3000" >> .env
```

### Step 7: Detect MCP Client

Use AskUserQuestion to determine which MCP client they're using:

Question: "Which MCP client are you using?"
Options:
- "Claude Code" - Will configure `.mcp.json` file
- "Cursor" - Will configure ~/.cursor/mcp.json
- "Claude Desktop" - Will configure ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)

### Step 8: Find User's magnet-app Directory

**Important:** The default setup location should be the user's `magnet-app` repo, since that's where they'll be doing development work and need the MCP tools available.

```bash
# Common locations to check for magnet-app
ls -d ~/magnet-app 2>/dev/null || \
ls -d ~/Projects/magnet-app 2>/dev/null || \
ls -d ~/Code/magnet-app 2>/dev/null || \
echo "magnet-app not found in common locations"
```

If not found, ask:
Question: "Where is your magnet-app repository located?"

### Step 9: Check Existing MCP Configuration

**Claude Code uses `.mcp.json` files, NOT settings.json for MCP servers.** The settings.json schema does not support the `mcpServers` field.

```bash
# Check for existing .mcp.json in magnet-app
cat ~/magnet-app/.mcp.json 2>/dev/null || echo "No .mcp.json found"
```

**Cursor:**
```bash
cat ~/.cursor/mcp.json 2>/dev/null
```

**Claude Desktop (macOS):**
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json 2>/dev/null
```

### Step 10: Generate Configuration

Get the absolute path to the MCP server:
```bash
pwd  # Should be /path/to/magnet-mcp-server
```

Create the `.mcp.json` file structure. **Important:** This always points to the local Magnet API at localhost:3000.

```json
{
  "mcpServers": {
    "magnet-local": {
      "command": "node",
      "args": ["/absolute/path/to/magnet-mcp-server/dist/index.js"],
      "env": {
        "MAGNET_API_KEY": "<api-key-here>",
        "MAGNET_WEB_API_BASE_URL": "http://localhost:3000"
      }
    }
  }
}
```

For development (rebuilds before running):
```json
{
  "mcpServers": {
    "magnet-local": {
      "command": "pnpm",
      "args": ["--dir", "/absolute/path/to/magnet-mcp-server", "dev"],
      "env": {
        "MAGNET_API_KEY": "<api-key-here>",
        "MAGNET_WEB_API_BASE_URL": "http://localhost:3000"
      }
    }
  }
}
```

### Step 11: Create .mcp.json in magnet-app

Create the `.mcp.json` file in the user's magnet-app directory (the default location).

Ask user:
Question: "How should the local server be named?"
Options:
- "magnet-local (recommended)" - Keeps production config separate
- "magnet (replace production)" - Replaces any existing magnet configuration

**Important:** The `.mcp.json` file is project-specific. It only makes the MCP server available when working in that directory.

### Step 12: Add .mcp.json to .gitignore

**Critical:** The `.mcp.json` file contains the API key and must NOT be committed to git.

Check and update `.gitignore` in the magnet-app directory:
```bash
grep -E "^\.mcp\.json$" ~/magnet-app/.gitignore 2>/dev/null || echo ".mcp.json" >> ~/magnet-app/.gitignore
```

### Step 13: Verify Setup

After updating the configuration, provide next steps:

1. **Restart the MCP client** to load the new configuration
2. **Verify the server loads** by checking available tools
3. **Test a simple command** like listing issues

For Claude Code:
```
Run /mcp to verify the magnet-local server is connected and shows its tools
```

### Step 14: Troubleshooting

If the server doesn't connect, check:

1. **Local Magnet Server**: Ensure the Magnet web app is running at localhost:3000
2. **API Key**: Ensure MAGNET_API_KEY is valid and from your **local** Magnet instance
3. **Path**: Verify the absolute path to dist/index.js is correct
4. **Build**: Make sure `pnpm build` completed successfully
5. **Node version**: Confirm Node.js >= 22.2.0

Common errors:
- "MAGNET_API_KEY is not set" - API key missing or not being passed
- "Cannot find module" - Build not complete or wrong path
- "Connection refused" - Either MCP server crashed OR local Magnet server not running
- 401/403 errors - API key is invalid or from wrong environment (production vs local)

## Examples

### Example 1: First-Time Setup

User: "I want to test the MCP server locally"

Actions:
1. Check Node.js version and pnpm
2. Run `pnpm install` if needed
3. Run `pnpm build`
4. Confirm local Magnet server is running at localhost:3000
5. Ask for API key from local Magnet instance, save to `.env` with `MAGNET_WEB_API_BASE_URL`
6. Detect they're using Claude Code
7. Find their magnet-app directory
8. Create `.mcp.json` in magnet-app with magnet-local config (including localhost:3000 URL)
9. Add `.mcp.json` to magnet-app's `.gitignore`
10. Instruct to restart Claude Code in magnet-app directory

### Example 2: Switching from Production to Local

User: "I need to test my changes before deploying"

Actions:
1. Verify build is current (`pnpm build`)
2. Confirm local Magnet server is running at localhost:3000
3. Check existing `.mcp.json` in magnet-app
4. Add magnet-local config alongside existing magnet config (with localhost:3000 URL)
5. Remind them to get an API key from local instance if they don't have one
6. Explain they can switch between production and local by using different server names

### Example 3: Troubleshooting Connection

User: "The local MCP server isn't working"

Actions:
1. Verify local Magnet server is running at localhost:3000
2. Check if dist/index.js exists
3. Verify Node.js version
4. Test running server directly: `MAGNET_WEB_API_BASE_URL=http://localhost:3000 MAGNET_API_KEY=xxx node dist/index.js`
5. Check API key is from **local** Magnet instance (not production)
6. Verify `.mcp.json` has `MAGNET_WEB_API_BASE_URL` set to `http://localhost:3000`
7. Verify `.mcp.json` has correct absolute path to dist/index.js
8. Confirm user restarted Claude Code after config changes

## Notes

- **NOT A GLOBAL SETUP** - This configures the MCP server for the magnet-app project directory only. It will NOT be available in other projects.
- **This skill configures for local development** - it always points to localhost:3000, not production
- **Local Magnet server must be running** - the user needs the Magnet web app running locally
- **API key must be from local instance** - production API keys won't work with local server
- **Claude Code uses `.mcp.json` files** - NOT `settings.json` for MCP servers
- **`.mcp.json` is project-specific** - it only works when Claude Code is running in that directory
- Always use absolute paths in MCP configuration
- The "magnet-local" name helps distinguish from production
- Restart Claude Code after configuration changes
- Use `pnpm dev` for development builds (rebuilds before running)
- **Always add `.mcp.json` to `.gitignore`** - it contains the API key
- The `.env` file in magnet-mcp-server is also gitignored and safe for storing API keys
