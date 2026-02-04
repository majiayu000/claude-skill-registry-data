---
name: obsidian-project-documentation-assistant
description: Document technical projects in Obsidian vault. Use when the User mentions "document this", "close out", "wrap up", "update notes", "track progress", "where are we at", "what is the status", or discusses maintaining project documentation, experiment logs, asks for the state of the project, what next steps are, or work progress in Obsidian.
version: 2.1.0
allowed-tools: Read, Bash, AskUserQuestion, Task
---

# Obsidian Project Documentation Assistant

This skill helps maintain project documentation in an Obsidian vault while working with Claude Code. It automatically captures project progress and insights into structured, consistent notes.

**Architecture:** This skill acts as a lightweight launcher that detects project context, asks clarifying questions if needed, then launches an agent to handle the documentation work in the background.

## How This Works

### Situation 1: When a new working session is started

This skill:

1. Reads the AI Context file. (this should be a normal task already performed when a working session is started)
2. Reads the notes for this project if they exist to augement the context of what is happening with the project, the status, decisions made, and the next steps.
3. Welcomes the User back, asks how they're doing, and briefly inform them of what the next steps are for this new working session.

### Situation 2: When activated during a working session

This skill:

1. Loads configuration from `~/.claude/skills/obsidian-project-documentation-assistant/config.json`
2. Detects project context (name, area, type) from current directory
3. Asks the User for clarification if context is ambiguous
4. Launches a documentation agent with the detected context
5. The agent creates/updates notes, handles git operations, and returns results

### Situation 3: When a working session is about to end

This skill:

1. Offers to tie up the project documentation if the User has not already asked to do so.
2. Perform the steps in Situation 2 above.

## Tasks for Situation 1 and 2

### Step 1: Load Configuration

```bash
cat ~/.claude/skills/obsidian-project-assistant/config.json
```

Expected format:

```json
{
  "vault_path": "/path/to/ObsidianVault",
  "areas": ["Hardware", "Software", "Woodworking", "Music Synthesis"],
  "auto_commit": false,
  "auto_push": false,
  "git_enabled": true
}
```

If config doesn't exist, inform the User they need to reinstall the skill:

```bash
install install /path/to/vault
```

### Step 2: Quick Context Detection

#### Detect Project Name

Try these methods in order:

1. **From the User's message** - If the User explicitly mentions project name in their request
2. **From git repository**:

   ```bash
   git rev-parse --is-inside-work-tree 2>/dev/null && basename $(git rev-parse --show-toplevel)
   ```

   Transform kebab-case → Title Case (e.g., "obsidian-project-assistant" → "Obsidian Project Assistant")

3. **From directory name**:

   ```bash
   basename $(pwd)
   ```

If none of these work or result is generic (like "src", "build", "test"), refer to step 3 below.

#### Detect Project Area

Run quick file pattern checks:

```bash
# Check for Hardware indicators
if find . -maxdepth 2 -type f \( -name "*.ino" -o -name "*.cpp" -o -name "platformio.ini" \) 2>/dev/null | grep -q .; then
  echo "Hardware"
# Check for Software indicators
elif find . -maxdepth 2 -type f \( -name "package.json" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \) 2>/dev/null | grep -q .; then
  echo "Software"
# Check for Woodworking indicators
elif find . -maxdepth 2 -type f \( -name "*.stl" -o -name "*.blend" -o -name "*.f3d" \) 2>/dev/null | grep -q .; then
  echo "Woodworking"
# Check for Music Synthesis indicators
elif find . -maxdepth 2 -type f \( -name "*.pd" -o -name "*.maxpat" \) 2>/dev/null | grep -q .; then
  echo "Music Synthesis"
fi
```

If no clear match, refer to step 3 below.

#### Extract Description

Try to extract a brief description:

1. Check if README.md exists and read first paragraph
2. Check package.json for description field
3. Parse the User's message for description
4. See step 3 below if the previous steps fail.

### Step 3: Ask Clarifying Questions

If project_name is null OR area is null, use AskUserQuestion before launching agent:

**If project name is unclear:**

```text
Question: "What would you like to name this project?"
Options:
  - [Current directory name]
  - [Git repo name if available]
  - Other (custom input)
```

**If area is unclear:**

```text
Question: "What type of project is this?"
Options:
  - Hardware
  - Software
  - Woodworking
  - Music Synthesis
  - Other (custom input)
```

### Step 4: Launch Documentation Agent

Once you have all context, launch an `obsidian-project-documentation-manager` agent.

### Step 5: Report Results

When the agent completes, inform the User:

```text
✅ Project documented successfully!
📝 Updated: {path_to_note}
📋 Summary: {what_was_documented}
🔄 Git: {commit_status} {push_status}
```

## Error Handling

If errors occur:

- **Config missing**: Instruct the User to run installation
- **Vault not accessible**: Verify vault_path in config
- **Git operations fail**: Report error, but still create/update note
- **Template missing**: Use a basic template or ask the User to reinstall

## Important things to remember

- Use absolute paths for all file operations.
- Use the current date for all timestamp operations.
- Handle errors gracefully (missing templates, git failures, etc.).
- When refering to the User, use their name and not 'User'. If in any doubt of the User's pronouns, ask the User but always remember them.
