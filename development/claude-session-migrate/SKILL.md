---
name: claude-session-migrate
description: Migrate Claude Code session storage when directories are moved or renamed. Use when user mentions moving folders, renaming directories, relocating projects, or needs to update Claude session paths after filesystem changes.
allowed-tools: Bash, Read, Glob
---

# Claude Session Migrate

This skill helps you migrate Claude Code session storage when you move or rename project directories.

## How It Works

Claude Code stores session data in `~/.claude/projects/` with directory paths encoded using hyphens instead of forward slashes. When you move a project to a new directory, the session data needs to be migrated to match the new path.

## Instructions

When a user has moved or renamed a directory:

1. **Determine the old and new directory paths**
   - Ask the user for the old directory path if not already mentioned
   - Use `pwd` to get the current directory path (new location)

2. **Convert paths to Claude's session folder format**
   - Replace forward slashes with hyphens
   - **Replace spaces with hyphens** (IMPORTANT: spaces become hyphens, not literal spaces)
   - Remove the leading slash
   - Add a leading hyphen
   - Example: `/home/user/project` becomes `-home-user-project`
   - Example: `/Users/kevin/My Project` becomes `-Users-kevin-My-Project`

3. **Check if the old session folder exists**
   ```bash
   ls ~/.claude/projects/-old-encoded-path
   ```

4. **Migrate the session folder**
   ```bash
   cd ~/.claude/projects/
   mv -- -old-encoded-path -new-encoded-path
   ```
   - Use `--` to handle paths with leading hyphens safely

5. **Confirm the migration**
   - Verify the new folder exists at `~/.claude/projects/-new-encoded-path`
   - Inform the user the session storage has been updated to match the new directory location

## Examples

### Example 1: Project Moved
```
Old path: /Users/kevin/dev/my-app
New path: /Users/kevin/projects/my-app

Old session: -Users-kevin-dev-my-app
New session: -Users-kevin-projects-my-app

Command:
cd ~/.claude/projects/ && mv -- -Users-kevin-dev-my-app -Users-kevin-projects-my-app
```

### Example 2: Renamed Directory
```
Old path: /home/user/old-name
New path: /home/user/new-name

Old session: -home-user-old-name
New session: -home-user-new-name

Command:
cd ~/.claude/projects/ && mv -- -home-user-old-name -home-user-new-name
```

### Example 3: Path with Spaces
```
Old path: /Users/kevin/Downloads
New path: /Users/kevin/Documents/My Project

Old session: -Users-kevin-Downloads
New session: -Users-kevin-Documents-My-Project  (NOTE: space becomes hyphen!)

Command:
cd ~/.claude/projects/ && mv -- -Users-kevin-Downloads -Users-kevin-Documents-My-Project
```

## Edge Cases

- **Session doesn't exist**: Inform the user no session was found at the old path
- **New session already exists**: Ask user if they want to merge or replace
- **Multiple sessions**: List available sessions and ask which one to migrate
- **Invalid paths**: Validate that paths look correct before migration
- **Paths with spaces**: Remember that spaces in directory names become hyphens in the encoded path. Double-check your encoding!

## Best Practices

- Always confirm the old and new paths with the user before migrating
- Show the encoded session folder names so the user understands the transformation
- Verify the migration was successful by checking that the new folder exists
