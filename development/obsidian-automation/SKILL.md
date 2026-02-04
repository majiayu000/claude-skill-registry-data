---
name: obsidian-automation
description: This skill should be used when working on Obsidian plugins, testing plugin changes, verifying plugin UI, debugging plugin behaviour, or running automated tests against Obsidian. Also triggers on "start Obsidian", "take Obsidian screenshot", "test plugin", "run plugin command", "execute in Obsidian", or any Obsidian automation task. Use proactively during plugin development to verify changes visually.
---

# Obsidian Automation Tools

Chrome DevTools Protocol tools for Obsidian plugin development and testing. These tools launch isolated Obsidian instances with CDP enabled, allowing automated control without interfering with the user's normal Obsidian usage.

## When to Use Proactively

**Use these tools without being asked when:**

- Implementing or modifying Obsidian plugin features - take screenshots to verify UI changes
- Debugging plugin behaviour - execute commands and inspect state
- Testing plugin with different vault configurations
- Verifying that plugin changes work as expected
- The user mentions something looks wrong in the plugin

**Do not wait for explicit requests.** If working on an Obsidian plugin, proactively start a test instance and take screenshots to verify work.

## Prerequisites

Run once to install dependencies:

```bash
cd ${CLAUDE_PLUGIN_ROOT} && npm install
```

## Available Tools

All tools are in `${CLAUDE_PLUGIN_ROOT}/scripts/`. Run from the plugin directory being developed (where `manifest.json` is located).

### Start Obsidian Instance

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-start.js --vault ~/path/to/vault
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-start.js --empty
```

Launch an isolated Obsidian instance with CDP enabled. The current directory's plugin (identified by `manifest.json`) is symlinked into the test vault and enabled.

**Options:**
- `--vault <path>` - Use an existing vault with test data
- `--empty` - Create a fresh empty vault in temp directory
- `--port <number>` - CDP port (default: 9223, auto-increments if busy)

**Output:** JSON with instance details:
```json
{
  "port": 9223,
  "vault": "/path/to/vault",
  "wsUrl": "ws://localhost:9223/devtools/page/...",
  "pluginId": "flow"
}
```

**Always capture the port** from the output for subsequent commands.

### Stop Obsidian Instance

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-stop.js --port 9223
```

Stop a running test instance and clean up temp directories. Safe to call even if no instance is running.

### Take Screenshot

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-screenshot.js --port 9223
```

Capture the Obsidian window and save to temp directory. Outputs the file path. **Use frequently** to verify UI changes.

### Execute JavaScript

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-eval.js --port 9223 'app.vault.getName()'
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-eval.js --port 9223 'app.workspace.activeLeaf?.view?.getViewType()'
```

Execute JavaScript in Obsidian's context. Access the full Obsidian API via the `app` global.

**Common expressions:**
- `app.vault.getName()` - Get vault name
- `app.vault.getFiles()` - List all files
- `app.workspace.activeLeaf` - Get active leaf
- `app.plugins.plugins` - Access loaded plugins
- `app.commands.commands` - List available commands

### Execute Command

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-command.js --port 9223 'flow:open-focus'
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-command.js --port 9223 --list
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-command.js --port 9223 --list | grep flow
```

Execute an Obsidian command by ID. Use `--list` to see all available commands.

## Typical Workflow

### Testing Against Existing Vault

```bash
# Start with test vault containing sample data
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-start.js --vault ~/Documents/flow-dev-vault/flow-dev
# Output: { "port": 9223, ... }

# Execute a plugin command
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-command.js --port 9223 'flow:open-focus'

# Verify visually
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-screenshot.js --port 9223

# Inspect state
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-eval.js --port 9223 'app.workspace.getLeavesOfType("flow-focus").length'

# Clean up
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-stop.js --port 9223
```

### Testing Against Empty Vault

```bash
# Start with fresh empty vault
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-start.js --empty
# Output: { "port": 9223, "vault": "/tmp/obsidian-vault-9223", ... }

# Test plugin behaviour with no data
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-command.js --port 9223 'flow:process-inbox'

# Verify empty state handling
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-screenshot.js --port 9223

# Clean up (also removes temp vault)
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-stop.js --port 9223
```

### Parallel Testing (Multiple Agents)

Each agent uses a different port:

```bash
# Agent 1
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-start.js --empty --port 9223

# Agent 2
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-start.js --empty --port 9224

# Agent 3 (port auto-increments if 9225 busy)
node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-start.js --empty --port 9225
```

## Error Handling

**"No manifest.json found"**
- Run from the Obsidian plugin directory containing `manifest.json`

**"Could not connect to CDP"**
- Start an instance first with `obsidian-start.js`
- Check the correct port is specified

**"Vault path does not exist"**
- Verify the `--vault` path is correct
- Use `--empty` for a fresh vault

**"No free port found"**
- Stop existing instances with `obsidian-stop.js`
- Specify a different port range

**Trust dialog blocking plugins**
- On first vault open, Obsidian shows "Do you trust the author of this vault?"
- Take a screenshot to check if this dialog is present
- Click the trust button via JS:
  ```bash
  node ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-eval.js --port 9223 \
    'Array.from(document.querySelectorAll("button")).find(b => b.textContent.includes("Trust"))?.click()'
  ```
- Wait a moment then verify plugin commands are available

## Architecture Notes

- Each test instance uses an isolated user-data-dir in `/tmp/obsidian-test-<port>/`
- Empty vaults are created in `/tmp/obsidian-vault-<port>/`
- The plugin from the current directory is symlinked (not copied) so changes reflect immediately after Obsidian reload
- CDP enables full control: screenshots, JS execution, DOM inspection
- Multiple instances can run simultaneously on different ports
