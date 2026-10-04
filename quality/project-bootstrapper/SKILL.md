---
name: project-bootstrapper
description: Initialize or enhance projects with .claude configuration folders. Provides templates (minimal, hooks-demo, full-stack) for quick setup. Use when starting a new project, adding Claude Code configuration to an existing project, or setting up hooks and validation from scratch.
---

# Project Bootstrapper

Initialize projects with `.claude/` configuration folders using battle-tested templates. Transform any project into a Claude Code-powered workspace.

## When to Use

Use this skill when:

- Starting a new project
- Adding Claude Code configuration to existing project
- Setting up automatic validation (hooks)
- Need example command or skill structure
- Want proven .claude folder patterns

## Templates Available

### 1. Minimal Template

**Purpose:** Basic `.claude/` setup with project context

**Includes:**

- `settings.json` - Empty configuration ready to customize
- `CLAUDE.md` - Project context and instructions template

**Best for:**

- Simple projects
- Quick Claude Code enablement
- Projects that don't need validation

### 2. Hooks-Demo Template

**Purpose:** Self-validating project with example hooks

**Includes:**

- `settings.json` - Configured with PostToolUse and Stop hooks
- `CLAUDE.md` - Context with hook documentation
- `commands/build.md` - Example command with Stop hook
- `hooks/validators/ruff-validator.py` - Python linting validator
- `hooks/validators/template-validator.py` - Template validator you can customize

**Best for:**

- Projects needing automatic validation
- Learning hook patterns
- Python projects
- Quality-first workflows

### 3. Full-Stack Template

**Purpose:** Complete agentic setup for complex projects

**Includes:**

- Everything from hooks-demo
- Additional validators
- Example skills
- Example agents
- Comprehensive settings
- Full CLAUDE.md with architecture patterns

**Best for:**

- Large, complex projects
- Team projects
- Production codebases
- Full automation needs

## Workflow

### Bootstrap New Project

1. **Detect project type** (check for package.json, pyproject.toml, etc.)
2. **Ask user which template** (minimal, hooks-demo, full-stack)
3. **Copy template to `.claude/`**
4. **Customize CLAUDE.md** with detected project info
5. **Explain what was created**

### Add to Existing Project

1. **Check if `.claude/` already exists**
2. **If exists:**
   - Ask if user wants to merge or replace
   - Backup existing if replacing
3. **Copy template**
4. **Merge settings if needed**
5. **Update CLAUDE.md** with existing project details

### Customize Template

After installing:

1. **Review CLAUDE.md** - Add project-specific context
2. **Adjust settings.json** - Enable/disable features
3. **Customize validators** - Add project-specific checks
4. **Test hooks** - Trigger validation to verify setup

## Template Selection Guide

**Choose Minimal if:**

- Just want CLAUDE.md for project context
- Don't need automatic validation
- Exploring Claude Code
- Small/simple project

**Choose Hooks-Demo if:**

- Want self-correcting workflow
- Python project needing linting
- Learning hook patterns
- Medium-sized project

**Choose Full-Stack if:**

- Large/complex project
- Team environment
- Need comprehensive automation
- Production codebase

## Project Type Detection

The skill auto-detects project type by checking for:

**Python:**

- `pyproject.toml`
- `requirements.txt`
- `setup.py`

**JavaScript/TypeScript:**

- `package.json`
- `tsconfig.json`

**Rust:**

- `Cargo.toml`

**Go:**

- `go.mod`

**General:**

- `.git/` (git repository)
- `README.md`

Detection informs template customization and validator selection.

## Files Created

### Minimal Template

```
.claude/
├── settings.json           # Empty config
└── CLAUDE.md              # Project context template
```

### Hooks-Demo Template

```
.claude/
├── settings.json          # With PostToolUse and Stop hooks
├── CLAUDE.md             # Context + hook docs
├── commands/
│   └── build.md          # Example command with hooks
└── hooks/
    └── validators/
        ├── ruff-validator.py      # Python linter
        └── template-validator.py  # Customizable template
```

### Full-Stack Template

```
.claude/
├── settings.json         # Comprehensive config
├── CLAUDE.md            # Full documentation
├── commands/
│   ├── build.md
│   └── test.md
├── skills/
│   └── project-specific/
│       └── SKILL.md
├── agents/
│   └── specialized-agent.md
└── hooks/
    └── validators/
        ├── ruff-validator.py
        ├── manifest-validator.py
        └── custom-validator.py
```

## Examples

**User:** "Initialize this Python project with validation"

→ Detect: Python project (pyproject.toml found)
→ Recommend: hooks-demo template
→ Copy template to .claude/
→ Customize CLAUDE.md with project name and Python details
→ Result: Self-validating Python project

**User:** "Add .claude folder to this project"

→ Check: .claude/ doesn't exist
→ Ask: Which template? (minimal/hooks-demo/full-stack)
→ User chooses: hooks-demo
→ Copy template
→ Result: Project now has validation hooks

**User:** "Setup comprehensive Claude configuration"

→ Recommend: full-stack template
→ Copy template
→ Explain components: commands, skills, agents, hooks
→ Customize for project
→ Result: Fully automated development environment

## Template Customization

After installing a template, help user:

1. **Update CLAUDE.md:**
   - Project name and description
   - Tech stack details
   - Architecture notes
   - Common commands
   - Team conventions

2. **Configure settings.json:**
   - Model preferences
   - Tool permissions
   - Hook configuration
   - Custom paths

3. **Customize validators:**
   - Add project-specific checks
   - Remove irrelevant validators
   - Adjust validation rules

4. **Add commands:**
   - Common development tasks
   - Build/test/deploy workflows
   - Project-specific operations

## Best Practices

✓ Start with minimal, upgrade to hooks-demo/full-stack as needed
✓ Always customize CLAUDE.md with project-specific info
✓ Test validators after installation
✓ Review and adjust hooks for your workflow
✓ Document custom patterns in CLAUDE.md

## Reference

**Template location:** `@project-bootstrapper/templates/`
**Templates:** minimal/, hooks-demo/, full-stack/
**Target location:** `.claude/` (project root)

## Integration with Other Skills

**Works well with:**

- **hooks-mastery** - Learn to customize validators
- **skill-manager** - Install additional skills to project

**Workflow:**

1. Use project-bootstrapper to create .claude/
2. Use hooks-mastery to understand validators
3. Customize validators for project needs
4. Use skill-manager to add specialized skills
