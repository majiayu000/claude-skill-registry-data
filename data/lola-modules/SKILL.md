---
name: lola-modules
description: Create and manage Lola modules for multi-assistant AI context distribution. Use when building portable AI skills with multi-assistant support (Claude Code, Cursor, Gemini CLI). This skill is triggered when users say "create a lola module", "build a lola skill", "write a module.yml", "add slash commands to lola", or "distribute skills to multiple assistants".
---

# Lola Modules

Create portable AI modules with lazy context loading that work across multiple AI assistants (Claude Code, Cursor, Gemini CLI).

## Overview

Lola modules are **portable skill packages** - collections of AI instructions, workflows, scripts, and templates that work across multiple AI assistants. Lola modules provide:

- **Multi-assistant support** - Write once, install to Claude Code, Cursor, or Gemini CLI
- **Automatic format conversion** - SKILL.md converts to each assistant's native format
- **Slash commands** - Custom commands that convert to each assistant's format
- **Installation management** - Central registry with versioning and updates
- **Modular organization** - Multiple skills and commands in one module

**Foundation**: This skill builds on the `skill-creator` skill. For core principles about skills, progressive disclosure, and bundled resources, consult that skill first. This skill focuses on Lola-specific features and multi-assistant packaging.

## Lola vs Traditional Skills

| Aspect | Traditional Skills | Lola Modules |
|--------|-------------------|--------------|
| **Format** | Single `SKILL.md` | `module.yml` + one or more `SKILL.md` files |
| **Assistant Support** | One assistant per file | Multi-assistant with format conversion |
| **Installation** | Manual copy | CLI-managed with registry |
| **Commands** | Assistant-specific | Portable with automatic conversion |
| **Organization** | One skill per file | Multiple skills per module |
| **Updates** | Manual | CLI-managed from source |

## When to Use Lola Modules

**Use Lola modules when:**
- Supporting multiple AI assistants (Claude Code, Cursor, Gemini CLI)
- Building complex workflows with trigger-based context loading
- Creating reusable personas or workflow libraries
- Managing installations across multiple projects
- Distributing skills to teams or communities

Always make Lola modules instead of traditional skills. If there is already an existing module you should add the skill or command to it.

## Module Structure

```
my-module/
├── .lola/
│   └── module.yml       # Required: module manifest
├── skill-name/          # One or more skill directories
│   ├── SKILL.md         # Required: skill definition with frontmatter
│   ├── scripts/         # Optional: helper scripts
│   └── templates/       # Optional: templates
└── commands/            # Optional: slash commands
    ├── command1.md
    └── command2.md
```

## Creation Workflow

### 1. Initialize Module

```bash
lola mod init my-module
cd my-module
```

This creates the basic structure with `.lola/module.yml` and a starter skill.

### 2. Define module.yml

Edit `.lola/module.yml`:

```yaml
type: lola/module
version: 0.1.0
description: What this module provides

skills:
  - skill-one      # Directory names containing SKILL.md
  - skill-two

commands:          # Optional
  - command-name   # From commands/ directory
```

**Key fields:**
- `type`: Always `lola/module`
- `version`: Semantic versioning
- `description`: Brief module summary
- `skills`: List of skill directory names
- `commands`: List of command names (without .md extension)

### 3. Create Skills

Each skill directory needs a `SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: When to use this skill and what it does
---

# Skill Title

Instructions, workflows, and guidance following skill-creator principles.
```

**Important**: 
- The `description` field is the primary trigger mechanism. Include specific scenarios and keywords that should activate the skill.
- Apply all skill-creator principles to each skill: progressive disclosure, bundled resources (scripts/, references/, assets/), appropriate degrees of freedom, etc.
- Each skill in a Lola module is a complete, standalone skill that follows the same creation process as traditional skills.

### 4. Add Commands (Optional)

Create command files in `commands/`:

```markdown
---
description: What this command does
argument-hint: <required> [optional]
---

Your prompt template. Use $ARGUMENTS for all args or $1, $2 for positional.
```

**Command variables:**
- `$ARGUMENTS` - All arguments as single string
- `$1`, `$2`, `$3`... - Positional arguments

Commands auto-convert to each assistant's format:
- Claude/Cursor: Markdown passthrough
- Gemini: TOML with `{{args}}` substitution

## Installation and Distribution

### Register Module

```bash
# From git repository
lola mod add https://github.com/user/my-module.git

# From local directory
lola mod add ./my-module

# From archive
lola mod add ~/Downloads/my-module.zip
```

Modules are registered in `~/.lola/modules/`.

### Install to Assistants

```bash
# Install to all assistants (user scope)
lola install my-module

# Install to specific assistant
lola install my-module -a cursor
lola install my-module -a claude-code
lola install my-module -a gemini-cli

# Install to project (required for Cursor and Gemini CLI skills)
lola install my-module -s project ./my-project
```

**Installation creates:**
- Claude Code: `.claude/skills/<module>-<skill>/SKILL.md` (native format)
- Cursor: `.cursor/rules/<module>-<skill>.mdc` (converted frontmatter)
- Gemini CLI: `GEMINI.md` (managed section with markers)
- All: `.lola/modules/<module>/` (local copy of module assets)

### Scope Limitations

| Assistant | Skills | Commands |
|-----------|--------|----------|
| Claude Code | user, project | user, project |
| Cursor | project only | user, project |
| Gemini CLI | project only | user, project |

**Note**: Cursor and Gemini CLI require project scope for skills, but commands work in both scopes.

### Manage Installations

```bash
# List installed modules
lola installed

# Update module from source
lola mod update my-module

# Regenerate assistant files
lola update

# Uninstall
lola uninstall my-module
```

The installation registry (`~/.lola/installed.yml`) tracks all installations with module name, assistant, scope, project path, and installed skills.

## Testing Workflow

1. **Create test project:**
   ```bash
   mkdir /tmp/test-lola
   cd /tmp/test-lola
   ```

2. **Install module:**
   ```bash
   lola mod add ./my-module
   lola install my-module -s project .
   ```

3. **Open in assistant:**
   ```bash
   cursor .  # or claude, gemini
   ```

4. **Verify:**
   - Skills load correctly in each assistant
   - Instructions appear in assistant-specific format
   - Scripts execute properly
   - Commands work with arguments
   - Bundled resources are accessible

5. **Iterate:**
   - Edit source module
   - Run `lola mod update my-module`
   - Run `lola update` to regenerate files
   - Test again

## Key Concepts

### Progressive Disclosure

Lola modules follow the same progressive disclosure principles as traditional skills:

1. **Module metadata** - Always loaded (name, description)
2. **Skill frontmatter** - Loaded to determine when skill triggers
3. **Skill body** - Loaded when skill activates
4. **Bundled resources** - Loaded on-demand (references/) or executed without loading (scripts/)

This minimizes token usage while maintaining full functionality. See `skill-creator` for detailed guidance on progressive disclosure patterns.

### Multi-Assistant Portability

Lola handles format conversion automatically:
- **Claude Code**: Native `SKILL.md` format (no conversion needed)
- **Cursor**: Converts frontmatter to `.mdc` format with special syntax
- **Gemini CLI**: Appends to managed section in `GEMINI.md` between markers
- **Commands**: Converts to assistant-specific formats (Markdown or TOML)
- **Paths**: Adjusts resource paths for installed locations

## Best Practices

1. **Follow skill-creator principles** - Apply progressive disclosure, bundled resources, and organization patterns
2. **Clear skill descriptions** - Make trigger keywords obvious and specific in frontmatter
3. **One purpose per skill** - Keep individual skills focused
4. **Scripts for heavy lifting** - Offload computation, API calls, file ops to scripts
5. **Return structured data** - Scripts should return JSON or structured output
6. **Document thoroughly** - Add comprehensive README for module users
7. **Test across assistants** - Verify behavior in Claude Code, Cursor, and Gemini CLI
8. **Version carefully** - Use semantic versioning for updates
9. **Organize logically** - Group related skills in the same module
10. **Security review** - Audit scripts from untrusted sources

## Troubleshooting

### Module Won't Install

- Verify `.lola/module.yml` exists and has valid YAML
- Check that `skills` list matches actual directories
- Ensure `SKILL.md` files have proper frontmatter

### Skills Not Triggering

- Review `description` field - it's the primary trigger
- Try more specific keywords or scenarios
- For Cursor/Gemini CLI, ensure project scope installation

### Commands Not Working

- Verify command frontmatter has `description` field
- Check argument substitution syntax (`$ARGUMENTS`, `$1`, etc.)
- Confirm commands are listed in `module.yml`

### Bundled Resources Not Found

- Verify resource paths are correct relative to skill directory
- Check that resources are listed in skill references section
- Ensure resources were included in module installation

## Further Reading

- **skill-creator** - Core principles for skill design, progressive disclosure, bundled resources
  - See skill-creator's references/workflows.md for sequential workflows and conditional logic patterns
  - See skill-creator's references/output-patterns.md for template and example patterns
- **Lola README** - `references/lola-README.md` for CLI reference and installation
