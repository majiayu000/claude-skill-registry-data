---
name: write-command
description: Create effective Claude Code slash commands with proper YAML frontmatter and argument handling. Use when writing new slash commands, improving existing commands, or learning command best practices.
---

# Slash Command Creator

Create slash commands that users explicitly invoke with `/command-name`.

## Command vs Skill

| Aspect | Slash Command | Skill |
|--------|---------------|-------|
| Activation | Manual `/command` | Automatic (context) |
| Location | `.claude/commands/<name>.md` | `.claude/skills/<name>/SKILL.md` |
| Best for | On-demand actions | Recurring workflows |

## File Structure

```
.claude/
└── commands/
    ├── my-command.md
    └── subdir/
        └── nested-command.md
```

## Creation Process

### 1. Initialize

Run the init script to create proper structure:

```bash
python3 scripts/init_command.py <command-name>
```

Options:
- `--path`, `-p`: Output directory (default: `.claude/commands`)
- `--no-args`: Create without argument template

### 2. Edit the Command

Update the generated file with your instructions.

### 3. Test

Restart Claude Code, then run `/<command-name>`.

## Command Template

```markdown
---
name: command-name
description: Brief description of what this command does
arguments:
  - name: required_arg
    description: Something required
    required: true
  - name: optional_arg
    description: Something optional
    required: false
---

# Command Title

[What this command does]

## Process

### 1. [Step Name]
[Instructions with code examples]

### 2. [Step Name]
[Instructions]

## Example Usage

/command-name value1 value2
```

## YAML Frontmatter

### Required Fields

| Field | Format |
|-------|--------|
| `name` | lowercase, hyphens (must match filename) |
| `description` | Brief action description |

### Optional Fields

| Field | Description |
|-------|-------------|
| `arguments` | Array of argument definitions |
| `allowed-tools` | Pre-approved tools list |

## Arguments

Define arguments as array:

```yaml
arguments:
  - name: issue-id
    description: GitHub issue number
    required: true
  - name: branch
    description: Branch name (default: main)
    required: false
```

### Accessing Arguments

| Syntax | Usage |
|--------|-------|
| `$ARGUMENTS` | Entire input string |
| `$1`, `$2` | Positional parameters |

Example: `/deploy app prod` → `$1`=app, `$2`=prod

## Body Guidelines

**Do**:
- Use imperative form ("Run" not "You should run")
- Provide concrete code examples
- Break into numbered steps
- Show example usage

**Don't**:
- Include "When to use" (goes in description)
- Be vague about commands
- Make it too long

## Special Features

### Bash Execution
```markdown
!npm run build
!python scripts/process.py
```

### File References
```markdown
Review this:
@src/index.ts
```

## Validation Checklist

- [ ] Name matches filename (kebab-case)
- [ ] Description is clear and actionable
- [ ] Arguments have descriptions and required flags
- [ ] Body uses imperative form
- [ ] Includes example usage
