---
name: meta
description: Guide for writing and improving Claude Code skills. Use when creating new skills, debugging why skills aren't activating, or improving skill descriptions and structure.
---

# Writing effective Claude Code skills

## Required structure

```
skill-name/
├── SKILL.md (required)
├── reference.md (optional)
├── scripts/ (optional)
└── templates/ (optional)
```

## SKILL.md frontmatter

```yaml
---
name: lowercase-with-hyphens
description: Explain WHAT it does AND WHEN to use it. Include trigger terms users would say.
allowed-tools: [Read, Write, Bash]  # optional: restrict permissions
---
```

## Critical best practices

1. **Keep skills focused** - one capability per skill
2. **Write specific descriptions** - include actual terms users would mention
3. **Test activation** - verify Claude invokes it when expected
4. **Use allowed-tools** - restrict permissions for security

## Description examples

❌ Bad: "Helps with data"
✅ Good: "Analyze Excel spreadsheets, generate pivot tables, create charts. Use when working with .xlsx files."

❌ Bad: "Manages configuration"
✅ Good: "Read and update YAML/JSON config files. Use when modifying settings, environment variables, or application configuration."

## Debugging checklist

If Claude doesn't use your skill:
- Description lacks trigger terms users would say
- YAML syntax errors (check `---` markers, indentation)
- Description not specific enough about WHEN to use it
- Wrong file path or permissions

### Finding and fixing frontmatter issues

**Check if frontmatter exists:**
```bash
# View first 10 lines of SKILL.md
head -10 ~/.claude/skills/*/SKILL.md
```

**Common frontmatter problems:**
1. **Missing frontmatter block** - File starts with `#` instead of `---`
   - Fix: Add YAML block at top of file
2. **Missing closing `---`** - Only one `---` marker
   - Fix: Ensure both opening and closing markers exist
3. **Missing required fields** - No `name:` or `description:`
   - Fix: Add both required fields
4. **Wrong indentation** - YAML is indentation-sensitive
   - Fix: Use 2 spaces, no tabs
5. **Missing description trigger terms** - Generic description
   - Fix: Add specific keywords users would say

**Validation script:**
```bash
# Check all skills for frontmatter
for skill in ~/.claude/skills/*/SKILL.md; do
  echo "=== $skill ==="
  if head -1 "$skill" | grep -q "^---$"; then
    echo "✓ Has frontmatter"
  else
    echo "✗ Missing frontmatter"
  fi
done
```

## Systematic skill debugging workflow

When debugging skills that aren't working:

1. **List all skills** - Verify skill exists
   ```bash
   ls -la ~/.claude/skills/
   ```

2. **Check frontmatter** - Validate YAML structure
   ```bash
   head -10 ~/.claude/skills/skill-name/SKILL.md
   ```

3. **Verify required fields** - Ensure name and description exist
   - `name:` must match directory name
   - `description:` must include trigger terms

4. **Test description specificity** - Does it explain WHEN to use?
   - Include file types, actions, or domain terms
   - Avoid generic phrases like "helps with" or "manages"

5. **Check allowed-tools** - If restricted, verify needed tools included
   ```yaml
   allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
   ```

6. **Review content** - Ensure instructions are clear and actionable

## Skills vs slash commands

**Use skills for:**
- Complex workflows with multiple files
- Automatic contextual invocation
- Comprehensive capabilities

**Use slash commands for:**
- Simple single prompts
- Manual explicit control
- Quick frequently-used operations
