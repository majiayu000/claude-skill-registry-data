---
name: mcp-skill-creator
description: Create skills that wrap MCP (Model Context Protocol) servers for use with mcp-skill-client. Use when user wants to create a new MCP-based skill, wrap an existing MCP server as a skill, or generate SKILL.md with tool documentation from an MCP server.
---

# MCP Skill Creator

Create skills that wrap MCP servers for browser automation, database access, API integrations, and more. Generated skills use `mcp-skill-client` to maintain persistent MCP sessions.

## Skill Structure

```
skill-name/
├── SKILL.md        # Skill instructions with tool documentation
├── config.json     # MCP server configuration
└── scripts/
    └── mcp         # Wrapper script for short commands
```

## Creating a Skill

### Step 1: Create skill directory and config.json

```bash
mkdir -p skill-name/scripts
```

Create `config.json`:
```json
{
  "name": "skill-name",
  "transport": "stdio",
  "command": "npx",
  "args": ["@org/mcp-package@version", "--option1", "--option2"],
  "env": {}
}
```

**Transport options:**
- `stdio`: Spawns MCP server as subprocess (most common)
- `http`: Connects to running MCP server at URL

### Step 2: Create wrapper script

Create `scripts/mcp` (executable):
```bash
#!/bin/bash
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SESSION="${MCP_SESSION:-default}"
exec npx github:runoshun/mcp-skill-client --config "$SKILL_DIR/config.json" --session "$SESSION" "$@"
```

Make it executable:
```bash
chmod +x scripts/mcp
```

### Step 3: Fetch Tool List

```bash
# Set session name (optional, defaults to "default")
export MCP_SESSION=dev

# Start daemon temporarily
./scripts/mcp start

# Get tool list (copy this output for SKILL.md)
./scripts/mcp tools

# Stop daemon
./scripts/mcp stop
```

### Step 4: Write SKILL.md

Use this template:

```markdown
---
name: skill-name
description: [What the skill does and when to use it]
---

# Skill Name

[Brief description of what this skill enables]

## Setup

Set session name (optional):
\`\`\`bash
export MCP_SESSION=myproject
\`\`\`

Start the MCP daemon:
\`\`\`bash
$SKILL_DIR/scripts/mcp start
\`\`\`

## Available Tools

[Document each tool from the tools list]

### tool_name
[Description from MCP server]

\`\`\`bash
$SKILL_DIR/scripts/mcp call tool_name param1=value
\`\`\`

## Cleanup

\`\`\`bash
$SKILL_DIR/scripts/mcp stop
\`\`\`
```

## Example: Playwright MCP Skill

### config.json

```json
{
  "name": "playwright-mcp",
  "transport": "stdio",
  "command": "npx",
  "args": ["@playwright/mcp@latest", "--headless", "--browser", "chromium", "--no-sandbox"]
}
```

### scripts/mcp

```bash
#!/bin/bash
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SESSION="${MCP_SESSION:-default}"
exec npx github:runoshun/mcp-skill-client --config "$SKILL_DIR/config.json" --session "$SESSION" "$@"
```

### SKILL.md (excerpt)

```markdown
---
name: playwright-mcp
description: Browser automation via Playwright MCP server. Navigate pages, click elements, fill forms, take screenshots. Use for web testing, scraping, or any browser automation task.
---

# Playwright MCP

Browser automation with persistent session via MCP.

## Setup

\`\`\`bash
export MCP_SESSION=myproject  # optional
$SKILL_DIR/scripts/mcp start
\`\`\`

## Tools

### browser_navigate
Navigate to a URL.
\`\`\`bash
$SKILL_DIR/scripts/mcp call browser_navigate url=https://example.com
\`\`\`

### browser_snapshot
Get accessibility snapshot with element refs.
\`\`\`bash
$SKILL_DIR/scripts/mcp call browser_snapshot
\`\`\`

### browser_click
Click an element by reference.
\`\`\`bash
$SKILL_DIR/scripts/mcp call browser_click element="Submit" ref=e12
\`\`\`
```

## Session Management

Sessions allow parallel usage from different projects:

```bash
# Project A
cd ~/project-a
export MCP_SESSION=project-a
./scripts/mcp start  # port auto-assigned (e.g., 8940)

# Project B (different terminal)
cd ~/project-b
export MCP_SESSION=project-b
./scripts/mcp start  # different port auto-assigned (e.g., 8941)
```

Session state is stored in `.<skill-name>/` in the current directory:
```
.skill-name/
├── sessions.json       # All session info
├── project-a/
│   ├── daemon.log
│   └── output/
└── project-b/
    ├── daemon.log
    └── output/
```

List all sessions:
```bash
./scripts/mcp sessions
```

## Tool Documentation Format

When documenting tools in SKILL.md:

1. **Tool name as heading** - Use `### tool_name`
2. **Brief description** - One line explaining what it does
3. **Example** - Show actual command with realistic values

## Templates

Copy templates from `assets/` directory:
- `assets/config.json` - MCP server configuration template
- `assets/SKILL.md.template` - SKILL.md template with placeholders
- `assets/mcp.sh` - Wrapper script template

## Tips

- **$SKILL_DIR**: Use this placeholder for skill directory path
- **MCP_SESSION**: Environment variable for session name (default: "default")
- **Session persistence**: Daemon maintains browser/connection state between calls
- **Error handling**: Check daemon status if tools fail (`$SKILL_DIR/scripts/mcp status`)
- **Parallel usage**: Each session gets auto-assigned port, no manual port management needed
