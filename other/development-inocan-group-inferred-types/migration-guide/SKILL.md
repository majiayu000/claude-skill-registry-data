---
name: migration-guide
description: Migrate existing plugins to proper Claude Code format. Use when converting flat skill files, adding missing frontmatter, restructuring plugin directories, or upgrading plugin structure.
allowed-tools: Read, Write, Glob, Grep
---

# Plugin Migration Guide

This skill provides procedures for migrating plugins to the correct Claude Code format.

## Common Migration Scenarios

### 1. Flat Skills to Directory Format

**Before:**
```
skills/
├── my-skill.md
└── another-skill.md
```

**After:**
```
skills/
├── my-skill/
│   └── SKILL.md
└── another-skill/
    └── SKILL.md
```

**Migration Steps:**

1. For each `skills/*.md` file:
   ```bash
   # Create directory
   mkdir -p skills/skill-name

   # Move and rename
   mv skills/skill-name.md skills/skill-name/SKILL.md
   ```

2. Add frontmatter if missing:
   ```yaml
   ---
   name: skill-name
   description: [extracted from content or prompted]
   ---
   ```

### 2. Adding Missing Frontmatter

**Skills without frontmatter:**

Check if file starts with `---`. If not, add:

```yaml
---
name: [derive from filename, lowercase, hyphens]
description: [extract first paragraph or prompt user]
allowed-tools: [analyze content for tool usage]
---

[existing content]
```

**Agents without frontmatter:**

```yaml
---
name: [derive from filename]
description: [extract purpose from content]
tools: [analyze for tool references]
model: sonnet
---

[existing content]
```

### 3. Moving Directories to Plugin Root

**Issue:** Directories inside `.claude-plugin/`

**Before:**
```
.claude-plugin/
├── plugin.json
├── commands/
├── agents/
└── skills/
```

**After:**
```
.claude-plugin/
└── plugin.json
commands/
agents/
skills/
```

**Migration:**
```bash
# Move directories to root
mv .claude-plugin/commands ./commands
mv .claude-plugin/agents ./agents
mv .claude-plugin/skills ./skills
```

### 4. Removing Empty Directories

Check for and remove empty directories:

```bash
# Find empty directories
find . -type d -empty

# Remove specific empty dirs
rmdir agents/  # if empty
rmdir commands/  # if empty
```

## Frontmatter Extraction

### Extracting Description from Content

Look for description in order:
1. First line after `#` heading
2. First paragraph of content
3. File's first sentence

Example:
```markdown
# My Skill

This skill helps with X, Y, and Z.

## Instructions
...
```

Extract: "This skill helps with X, Y, and Z."

### Deriving Name from Filename

| Filename | Derived Name |
|----------|--------------|
| `my-skill.md` | `my-skill` |
| `MySkill.md` | `myskill` |
| `my_skill.md` | `my-skill` |
| `My Skill.md` | `my-skill` |

Rules:
1. Lowercase everything
2. Replace underscores/spaces with hyphens
3. Remove non-alphanumeric except hyphens
4. Ensure starts with letter

### Detecting Tool Usage

Scan content for tool references:

| Pattern | Tool |
|---------|------|
| "read file", "Read tool" | Read |
| "search", "grep", "find text" | Grep |
| "find files", "glob" | Glob |
| "run command", "bash", "execute" | Bash |
| "write", "create file" | Write |
| "edit", "modify" | Edit |

## Migration Checklist

### Pre-Migration
- [ ] Backup existing plugin
- [ ] List all files to migrate
- [ ] Identify content to extract

### During Migration
- [ ] Convert flat skills to directories
- [ ] Add frontmatter to all skills
- [ ] Add frontmatter to all agents
- [ ] Move directories to plugin root
- [ ] Remove empty directories
- [ ] Update plugin.json paths

### Post-Migration
- [ ] Run `/pb:validate` on migrated plugin
- [ ] Test all commands appear in `/help`
- [ ] Verify skills are discovered
- [ ] Check agents can be invoked
- [ ] Remove backup after verification

## Handling Edge Cases

### Skills with Reference Files

If skill has associated files:

**Before:**
```
skills/
├── api-reference.md
└── api-reference-data.json
```

**After:**
```
skills/
└── api-reference/
    ├── SKILL.md
    └── data.json
```

### Nested Command Directories

Preserve namespace structure:

**Before:**
```
commands/
└── git/
    ├── commit.md
    └── push.md
```

**After:** (no change needed - already correct)
```
commands/
└── git/
    ├── commit.md  → /git:commit
    └── push.md    → /git:push
```

### Multiple Content Files per Skill

Move all related files to skill directory:

```
skills/
└── complex-skill/
    ├── SKILL.md
    ├── reference.md
    ├── examples.md
    └── templates/
        └── template.json
```
