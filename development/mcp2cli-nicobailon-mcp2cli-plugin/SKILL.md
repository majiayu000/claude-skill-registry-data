---
name: mcp2cli
description: Convert MCP servers into standalone Bash-invokable scripts. Use when user wants to make an MCP server usable as bash commands, convert MCP to CLI, or wrap MCP tools for agent use.
---

# mcp2cli

Convert any MCP server's tools into standalone Bash-invokable scripts.

## When to Use

- User wants to convert an MCP server to CLI tools
- User mentions making MCP tools "agent-ready" or turning an MCP into a "CLI tool"
- User wants to wrap an MCP server for direct invocation

## How to Execute

**Spawn a subagent** using the Task tool with `subagent_type: "general-purpose"`:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Convert MCP server to CLI tools"
- prompt: <see below>
```

### Subagent Prompt Template

```
Convert the MCP server "<package-name>" into standalone CLI tools.

## Step 1: Derive Names

Server name derivation:
- Remove @scope/ prefix (e.g., @anthropic-ai/pkg -> pkg)
- Remove @version suffix (e.g., pkg@1.0.0 -> pkg)
- Remove -mcp suffix (e.g., chrome-devtools-mcp -> chrome-devtools)
- Remove mcp- prefix (e.g., mcp-server-fetch -> server-fetch)

## Step 2: Fetch Package Description (in parallel with discovery)

Try to fetch a rich description to use in registration:

**For npm packages:**
```bash
curl -s "https://registry.npmjs.org/<package>" | jq -r '.readme // .description'
```
Extract the first paragraph after the title (skip badges/headings).

**For PyPI packages:**
```bash
curl -s "https://pypi.org/pypi/<package>/json" | jq -r '.info.description // .info.summary'
```
Extract the first paragraph after the title.

Use the first meaningful paragraph (>20 chars) or fall back to short description.

## Step 3: Discover Tools (Auto-Fallback)

**Try npm first:**
```bash
npx mcporter list --stdio "npx -y <package>@latest" --name <server> --schema --json
```

**If npm fails, try uvx (Python):**
```bash
npx mcporter list --stdio "uvx <package>" --name <server> --schema --json
```

Parse the JSON output. Extract all tools with their schemas.

## Step 4: Group Tools

Analyze discovered tools and group logically:
- Max 5-6 tools per wrapper
- Dedicated wrappers for complex/high-frequency tools
- Name files: <server>-<action>.js (lowercase, hyphenated)

## Step 5: Generate Wrapper Scripts

For each group, generate a Node.js ES module:

```javascript
#!/usr/bin/env node

import { execSync } from "child_process";

const MCP_CMD = "<mcp-command>";  // The command that worked (npx or uvx)
const SERVER = "<server-name>";

function callMcp(tool, params = {}) {
  const paramStr = Object.entries(params)
    .map(([k, v]) => `${k}:${JSON.stringify(v)}`)
    .join(" ");
  const cmd = `npx mcporter call --stdio "${MCP_CMD}" ${SERVER}.${tool} ${paramStr}`;
  try {
    return execSync(cmd, { encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"] });
  } catch (error) {
    throw new Error(error.stderr || error.message);
  }
}

const args = process.argv.slice(2);
if (args.includes("--help")) {
  console.log("Usage: <filename> [options]");
  console.log("");
  console.log("Options:");
  // List ALL parameters from the tool schema with descriptions
  process.exit(0);
}

// Parse --key value pairs
const params = {};
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith("--") && i + 1 < args.length) {
    const key = args[i].slice(2);
    const value = args[++i];
    try {
      params[key] = JSON.parse(value);
    } catch {
      params[key] = value;
    }
  }
}

try {
  const result = callMcp("<tool-name>", params);
  console.log(result);
} catch (error) {
  console.error("Error:", error.message);
  process.exit(1);
}
```

**Requirements:**
- ES modules (import, not require)
- --help showing ALL parameters with types and descriptions
- Handle complex params (arrays/objects) via --param '<json>'
- Errors to stderr, exit(1)

## Step 6: Write Output Files

```bash
mkdir -p ~/agent-tools/<server-name>
```

Create:
1. **package.json** - with "type": "module"
2. **README.md** - document all tools with usage examples (use symlink names without .js extension)
3. **Wrapper .js scripts** - one per tool group

Make executable and create symlinks for direct invocation:
```bash
chmod +x ~/agent-tools/<server-name>/*.js

# Use ~/agent-tools/bin if ~/agent-tools/ exists, otherwise ~/.local/bin
if [ -d ~/agent-tools ]; then
  BIN_DIR=~/agent-tools/bin
else
  BIN_DIR=~/.local/bin
fi
mkdir -p "$BIN_DIR"
for f in ~/agent-tools/<server-name>/*.js; do
  ln -sf "$f" "$BIN_DIR/$(basename "$f" .js)"
done
```
Note: Ensure the bin directory is in the user's PATH.

## Step 7: Register to CLAUDE.md

Append to ~/.claude/CLAUDE.md using the fetched description:

```markdown
### <Server Name>
<fetched description or fallback generic description>

Usage:
```bash
<server>-<tool1> --help
<server>-<tool2> --param "value"
<server>-<tool3> --url "https://example.com"
```

Full docs: `~/agent-tools/<server-name>/README.md`
```

Note: Replace `<server>-<tool>.js` with actual generated filenames in the registration.

## Report Back

- Package source: npm or PyPI (which succeeded)
- Description: what was fetched
- Tools discovered: count
- Wrappers generated: list of filenames
- Location: ~/agent-tools/<server-name>/
- Registration: confirmed in ~/.claude/CLAUDE.md
```

## Example Invocation

User: "Convert chrome-devtools-mcp to CLI tools"

Spawn Task with the full prompt above, substituting "chrome-devtools-mcp" for <package-name>.
