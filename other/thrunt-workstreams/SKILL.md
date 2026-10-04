---
name: thrunt-workstreams
description: Manage parallel workstreams — list, create, switch, status, progress, complete, and resume
---


# /thrunt-workstreams

Manage parallel workstreams for concurrent milestone work.

## Usage

`/thrunt-workstreams [subcommand] [args]`

### Subcommands

| Command | Description |
|---------|-------------|
| `list` | List all workstreams with status |
| `create <name>` | Create a new workstream |
| `status <name>` | Detailed status for one workstream |
| `switch <name>` | Set active workstream |
| `progress` | Progress summary across all workstreams |
| `complete <name>` | Archive a completed workstream |
| `resume <name>` | Resume work in a workstream |

## Step 1: Parse Subcommand

Parse the user's input to determine which workstream operation to perform.
If no subcommand given, default to `list`.

## Step 2: Execute Operation

### list
Run: `node "$THRUNT_TOOLS" workstream list --raw --cwd "$CWD"`
Display the workstreams in a table format showing name, status, current phase, and progress.

### create
Run: `node "$THRUNT_TOOLS" workstream create <name> --raw --cwd "$CWD"`
After creation, display the new workstream path and suggest next steps:
- `/hunt-new-program --ws <name>` to set up the milestone

### status
Run: `node "$THRUNT_TOOLS" workstream status <name> --raw --cwd "$CWD"`
Display detailed phase breakdown and state information.

### switch
Run: `node "$THRUNT_TOOLS" workstream set <name> --raw --cwd "$CWD"`
Also set `THRUNT_WORKSTREAM` env var for the current session.

### progress
Run: `node "$THRUNT_TOOLS" workstream progress --raw --cwd "$CWD"`
Display a progress overview across all workstreams.

### complete
Run: `node "$THRUNT_TOOLS" workstream complete <name> --raw --cwd "$CWD"`
Archive the workstream to milestones/.

### resume
Set the workstream as active and suggest `/thrunt-resume-work --ws <name>`.

## Step 3: Display Results

Format the JSON output from thrunt-tools into a human-readable display.
Include the `${THRUNT_WS}` flag in any routing suggestions.
