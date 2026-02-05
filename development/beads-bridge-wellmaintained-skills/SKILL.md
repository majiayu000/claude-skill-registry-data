---
name: "beads-bridge"
description: "Use when tracking Beads epic status, syncing progress to GitHub/Shortcut, generating dependency diagrams, or monitoring multi-repo work. Bridges Beads issue tracking with project management tools."
version: "1.6.0"
author: "David Laing"
category: ["Development", "Project Management"]
tags: ["beads", "github", "shortcut", "project-management", "issue-tracking", "multi-repo", "progress-tracking"]
required_permissions:
  - "bash"
---

## Skill Overview

This skill bridges Beads (git-backed multi-repository issue tracker) with project management tools like GitHub Projects v2 and Shortcut. It enables teams working across multiple repositories to maintain a unified view of work while preserving detailed technical tracking in Beads.

**How Claude Uses This Skill:**

1. **Check if beads-bridge is installed:** Run `beads-bridge --version`
2. **If not found:** Show helpful error message directing user to installation instructions
3. **Execute commands:** Use `beads-bridge <command> <args>` via Bash tool
4. **Parse output:** Commands return JSON that can be presented to the user

**IMPORTANT:**
- The `beads-bridge` CLI must be installed and available in PATH
- Always run commands from the project root so CLI can find `.beads/` directory
- If `beads-bridge` command not found, instruct user to install it (see Installation section below)

### Key Capabilities

Works with both **GitHub Issues/Projects** and **Shortcut Stories**:

1. **Query Status** - Get aggregated progress across issues/stories and Beads epics
2. **Sync Progress** - Post progress updates from Beads to GitHub/Shortcut
3. **Generate Diagrams** - Create Mermaid dependency visualizations
4. **Detect Discoveries** - Identify newly discovered work during implementation
5. **Manage Mappings** - Create/query links between issues/stories and Beads epics
6. **Interactive Visualization** - Serve interactive web dashboard for beads exploration
7. **Decompose** - Convert issue/story task lists into Beads epics and tasks

### Use Cases

- **Tech Leads**: Monitor progress across 5+ repositories from a single GitHub Projects board
- **Product Managers**: Get accurate completion estimates based on actual dependency analysis
- **Engineering Teams**: Automatically propagate discovered work to project tracking
- **Stakeholders**: View real-time progress with auto-updating diagrams and metrics

## Installation

If `beads-bridge` is not found in PATH, provide this message to the user:

```
The beads-bridge CLI is not installed. Please install it first:

# Download and install the latest release:
curl -fsSL https://raw.githubusercontent.com/wellmaintained/skills/main/src/beads-bridge/scripts/install-beads-bridge.sh | bash

# Or install as Claude Code plugin (will install CLI automatically):
claude-code plugin install wellmaintained/skills/beads-bridge

After installation, beads-bridge should be available in your PATH.
```

## Command Usage

### Before Running Commands

Always verify beads-bridge is available:

```bash
beads-bridge --version
```

If this fails, show the installation message above and stop.

### Unified Commands

All commands should be run from the project root directory:

```bash
# Sync a bead to its external system (GitHub/Shortcut)
beads-bridge sync <bead-id>

# Decompose an external issue into Beads epics and tasks
beads-bridge decompose <ref>
# Examples:
beads-bridge decompose https://github.com/owner/repo/issues/123
beads-bridge decompose github:owner/repo#123
beads-bridge decompose shortcut:89216
```

### Interactive Visualization

```bash
# Serve interactive web dashboard for a bead
beads-bridge serve <bead-id>

# Example:
beads-bridge serve wms-123
```

This starts a local web server (typically at http://localhost:3000) showing:
- Interactive dependency graph
- Task status and progress
- Real-time updates via SSE
- Drag-and-drop canvas for exploring relationships

## Capability Implementation

When user requests a beads-bridge operation, use the corresponding CLI command:

### 1. Sync Progress

```bash
# Sync a bead by ID (uses external_ref from the bead)
beads-bridge sync <bead-id>

# Example:
beads-bridge sync wms-123

# Dry run to see what would be synced
beads-bridge sync wms-123 --dry-run
```

The sync command automatically:
- Reads the bead's `external_ref` field
- Detects the backend (GitHub or Shortcut)
- Generates a Mermaid dependency diagram
- Posts updates to the linked issue/story

Confirm to user that progress was synced successfully.

### 2. Decompose Issues

```bash
# Decompose using URL
beads-bridge decompose https://github.com/owner/repo/issues/123

# Decompose using shorthand format
beads-bridge decompose github:owner/repo#123
beads-bridge decompose shortcut:89216

# Decompose without posting confirmation comment
beads-bridge decompose github:owner/repo#123 --no-comment

# Decompose with custom priority for created beads
beads-bridge decompose github:owner/repo#123 --priority 1
```

The decompose command automatically:
- Detects the backend from the reference format
- Creates an epic with `external_ref` set
- Creates child tasks from the issue/story body

Confirm that task lists were decomposed into Beads epics and tasks.

### 3. Interactive Visualization

```bash
beads-bridge serve wms-123
```

Inform user that the server is starting and provide the URL to access the visualization.


## Error Handling

If `beads-bridge` command fails:

1. **Command not found**: Show installation instructions (see Installation section)
2. **Config file missing**: User needs to create `.beads-bridge/config.json` in project root
3. **Authentication errors**: User needs to run `beads-bridge auth` for GitHub/Shortcut
4. **Invalid arguments**: Check command syntax in this SKILL.md

Always provide helpful guidance based on the error message from the CLI.

## Best Practices

### For Product Managers

1. **Set external_ref early** - Link GitHub Issues or Shortcut stories when creating epics
2. **Review discoveries weekly** - Check `discover` output during standups
3. **Use interactive visualization** - Run `beads-bridge serve` for visual progress tracking

### For Tech Leads

1. **Keep diagrams current** - Run `sync` after major scope changes to update diagrams
2. **Track blockers actively** - Use `bd show <bead-id>` to check status
3. **Verify cross-repo deps** - Use `bd dep tree` to verify dependencies

### For Engineering Teams

1. **Use Beads for technical work** - Detailed tracking stays in repositories
2. **Let sync handle GitHub** - Don't manually update tracking issues
3. **Tag discoveries properly** - Beads issues with `discovered-from` relationships

## Troubleshooting

### CLI Not Found

```bash
# Check if beads-bridge is in PATH
which beads-bridge

# If not found, install it
curl -fsSL https://raw.githubusercontent.com/wellmaintained/skills/main/src/beads-bridge/scripts/install-beads-bridge.sh | bash
```

### Authentication Issues

```bash
# GitHub: Set up authentication
beads-bridge auth --backend github

# Shortcut: Set up authentication
beads-bridge auth --backend shortcut
```

### Config File Missing

Create `.beads-bridge/config.json` in your project root:

```json
{
  "repositories": {
    "repo-name": {
      "path": "/absolute/path/to/repository"
    }
  },
  "backend": "github",
  "githubRepository": "owner/repo"
}
```

See the beads-bridge documentation for complete configuration options.

## Output Format

All commands output JSON that can be parsed and presented to the user. Example:

```json
{
  "completionPercentage": 65,
  "totalTasks": 23,
  "completedTasks": 15,
  "epics": [
    {
      "id": "frontend-e42",
      "repository": "frontend",
      "status": "in_progress",
      "completion": 80
    }
  ]
}
```

Parse this JSON and present key information in a user-friendly format.

## Related Documentation

For detailed information:
- **Installation**: See src/beads-bridge/README.md
- **CLI Reference**: See src/beads-bridge/docs/CLI_REFERENCE.md
- **Configuration**: See src/beads-bridge/docs/CONFIGURATION.md
- **Troubleshooting**: See src/beads-bridge/docs/TROUBLESHOOTING.md
