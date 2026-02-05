---
name: ide
description: How to integrate Claude Code with VS Code and JetBrains IDEs. Use when user asks about IDE integration, VS Code extension, JetBrains plugin, or IDE setup.
---

# Claude Code IDE Integration

## VS Code Extension (Beta)

### Overview

Claude Code integrates with Visual Studio Code through a native extension, providing a dedicated sidebar panel with IDE-native features.

### Key Features

**Native IDE experience:**
- Dedicated sidebar panel accessed via the Spark icon
- Review Claude's proposed changes before accepting
- Auto-accept mode for automatic application of edits
- Inline diff viewing with expandable details

**Integration features:**
- File management through @-mentions and file picker attachment
- Model Context Protocol (MCP) server integration
- Conversation history access
- Multiple simultaneous sessions
- Support for most CLI slash commands

### Requirements & Installation

**Requirements:**
- VS Code 1.98.0 or higher
- Claude Code installed globally

**Installation:**
Download from the Visual Studio Code Extension Marketplace.

Search for "Claude Code" in VS Code Extensions panel.

### How to Use

1. Click the Spark icon to open the Claude Code panel
2. Drag the sidebar wider to see inline diffs
3. Click on diffs to expand for full details
4. Interact with Claude as you would in the terminal
5. Review and accept/reject changes

### Configuration

**Auto-accept mode:**
Enable to automatically apply Claude's edits without manual review.

**File attachments:**
Use @-mentions or the file picker to attach files to conversations.

**MCP servers:**
Configure MCP integrations for extended functionality.

### Third-Party Provider Support

The extension supports Amazon Bedrock and Google Vertex AI through environment variable configuration in VS Code settings:

**Settings (JSON):**
```json
{
  "claude-code.env": {
    "ANTHROPIC_API_KEY": "your-key",
    "AWS_REGION": "us-east-1",
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project"
  }
}
```

### Current Limitations

Features not yet implemented:
- Full MCP configuration
- Subagents setup
- Checkpoints
- Advanced shortcuts
- Tab completion

**Note:** These features are available in the terminal version.

### Legacy CLI Integration

For terminal-based users, the integration auto-installs when running `claude` from VS Code's integrated terminal.

**Features:**
- Selection context sharing
- Automatic diagnostic reporting
- Terminal-based interaction

## JetBrains Integration

### Overview

Claude Code integrates with JetBrains IDEs through a dedicated plugin, offering features like interactive diff viewing and automatic selection context sharing.

### Supported IDEs

The plugin works with:
- IntelliJ IDEA
- PyCharm
- Android Studio
- WebStorm
- PhpStorm
- GoLand

### Key Features

**Quick launch:**
- `Cmd+Esc` (Mac)
- `Ctrl+Esc` (Windows/Linux)

**Diff viewing:**
Code changes display directly in the IDE diff viewer

**Selection context:**
Current IDE selections automatically share with Claude Code

**File references:**
- `Cmd+Option+K` (Mac)
- `Alt+Ctrl+K` (Linux/Windows)

**Diagnostic sharing:**
IDE errors and diagnostics automatically sync with Claude

### Installation Methods

#### Marketplace Installation
1. Find the Claude Code plugin in the JetBrains marketplace
2. Install the plugin
3. **Restart your IDE completely**

#### Auto-Installation
The plugin may self-install when running `claude` in the integrated terminal.

**Important:** Requires full IDE restart to activate.

### Configuration

#### Claude Code Settings

1. Run `claude`
2. Enter `/config`
3. Set the diff tool to `auto` for automatic IDE detection

#### Plugin Settings

Go to: **Settings → Tools → Claude Code**

**Configuration options:**
- Specify custom Claude command paths
- Enable multi-line prompts with Option+Enter (macOS)
- Configure automatic updates

#### ESC Key Troubleshooting

If ESC doesn't interrupt operations:

**Option 1:**
Settings → Tools → Terminal → Uncheck "Move focus to the editor with Escape"

**Option 2:**
Delete the "Switch focus to Editor" shortcut

### Special Configurations

#### Remote Development

Install the plugin on the remote host:
Settings → Plugin (Host)

#### WSL Users

Set Claude command as:
```
wsl -d Ubuntu -- bash -lic "claude"
```

Replace `Ubuntu` with your distribution name.

### Troubleshooting

**Plugin not working:**
1. Run Claude from project root directory
2. Verify plugin is enabled in IDE settings
3. Completely restart the IDE (multiple times if needed)
4. Check that Claude Code is installed globally

**WSL-specific issues:**
Consult the dedicated troubleshooting guide in the Claude Code documentation.

**Diff viewer not showing:**
1. Verify `/config` has diff tool set to `auto`
2. Restart IDE
3. Check plugin version is up to date

### Security Note

When auto-edit is enabled, Claude Code may modify IDE configuration files. Consider using manual approval mode for edits when using JetBrains IDEs.

## Comparison: VS Code vs JetBrains

| Feature | VS Code | JetBrains |
|---------|---------|-----------|
| **UI Integration** | Sidebar panel | Terminal-based |
| **Diff Viewing** | Inline diffs | Native diff viewer |
| **File Attachment** | @-mentions, picker | Selection sharing |
| **Shortcuts** | Standard | Customizable |
| **MCP Support** | Yes (basic) | Via CLI |
| **Multi-session** | Yes | Via CLI |
| **Maturity** | Beta | Stable |

## Best Practices

### For VS Code

1. **Drag sidebar wider** to see diffs clearly
2. **Use @-mentions** for efficient file attachment
3. **Enable auto-accept** only after building trust
4. **Keep extension updated** for latest features
5. **Use MCP servers** for extended capabilities

### For JetBrains

1. **Set diff tool to auto** for seamless integration
2. **Use keyboard shortcuts** for quick access
3. **Run from project root** for proper context
4. **Share selections** for targeted help
5. **Completely restart IDE** after installation

### General

1. **Start with manual approval** before enabling auto-accept
2. **Use version control** to track Claude's changes
3. **Review diffs carefully** before accepting
4. **Configure permissions** appropriately
5. **Leverage IDE diagnostics** for better context
6. **Use subagents** for specialized tasks (CLI)
7. **Enable checkpointing** for easy rollback (CLI)

## Common Workflows

### VS Code: Feature Implementation

1. Open Claude Code sidebar
2. Describe feature requirements
3. Attach relevant files with @-mentions
4. Review proposed changes in inline diffs
5. Accept/reject individual changes
6. Test and iterate

### JetBrains: Bug Fixing

1. Select error in editor
2. Press `Cmd+Esc` to open Claude Code
3. Share selection context automatically
4. Describe the issue
5. Review fix in diff viewer
6. Accept and test

### Both: Code Review

1. Open files to review
2. Ask Claude to review for:
   - Security issues
   - Performance problems
   - Best practices violations
   - Code quality improvements
3. Review suggestions
4. Apply relevant fixes

## Future Enhancements

Both integrations are actively developed. Upcoming features may include:
- Enhanced MCP configuration (VS Code)
- Subagent support (VS Code)
- Checkpoint management (VS Code)
- Improved multi-session handling
- Advanced shortcuts and completions
