---
name: bash-helper

description: Understand natural language descriptions and generate bash commands for macOS/Linux with explanation.
---

# Bash Helper Skill

Understand natural language descriptions and generate bash commands for macOS/Linux.

## Usage

Invoke with: `/bash-helper <description>`

Example: `/bash-helper find all python files larger than 1MB`

## Instructions

When this skill is invoked:

1. **Parse the user's description**

   - Understand what the user wants to accomplish
   - Identify the platform (macOS or Linux) from the environment

2. **Generate the command**

   - Create the appropriate bash command
   - Consider platform-specific differences (e.g., `sed -i` on Linux vs `sed -i ''` on macOS)
   - Use modern alternatives when available (e.g., `fd` instead of `find`, `rg` instead of `grep`)

3. **Explain the command**

   - Break down each part of the command
   - Explain flags and options used
   - Note any potential side effects or risks

4. **Ask for confirmation**

   - Display the command clearly
   - Wait for user to confirm before execution
   - Allow user to modify the command if needed

5. **Execute and show results**

   - Run the command after confirmation
   - Display the output
   - Handle errors gracefully

## Common Command Categories

### File Operations

- Find files by name, size, date, type
- Copy, move, rename files
- Change permissions
- Create/delete directories

### Text Processing

- Search text in files (grep/rg)
- Replace text (sed)
- Extract columns (awk/cut)
- Sort and filter

### System Information

- Disk usage (df, du)
- Process management (ps, kill, top)
- Network info (netstat, lsof)
- System resources (free, uptime)

### Archive Operations

- Create/extract tar, zip, gz
- Compress/decompress files

### Network Operations

- Download files (curl, wget)
- Check connectivity (ping, traceroute)
- Port scanning (netcat)

## Example Interaction

```
User: /bash-helper find all files modified in the last 24 hours

Assistant: I will find files modified in the last 24 hours.

**Command:**
```bash
find . -type f -mtime -1
```

**Explanation:**
- `find .` - search in current directory
- `-type f` - only files (not directories)
- `-mtime -1` - modified within last 1 day (24 hours)

**Alternative using fd (if installed):**
```bash
fd --type f --changed-within 24h
```

Proceed with execution? [Y/n]
```

## Platform Differences

| Command | macOS | Linux |
|---------|-------|-------|
| `sed -i` | `sed -i ''` | `sed -i` |
| `date` | BSD date | GNU date |
| `xargs` | May need `-I{}` | `-i` or `-I{}` |
| `stat` | Different flags | Different flags |

## Safety Notes

- Commands with destructive potential (rm, mv, chmod -R) require explicit confirmation
- Always show what will be affected before executing
- For recursive operations, show a preview first
- Suggest using `-n` or `--dry-run` flags when available
