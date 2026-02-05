---
name: building-skills-marketplace
description: Use when creating new Claude Code skills, setting up marketplace repositories, or packaging skills for distribution - complete workflow from skill creation to marketplace publication
---

# Building Skills & Marketplace

## Overview

Complete workflow for creating professional Claude Code skills and publishing them via marketplace, following superpowers pattern.

**Core principle:** Skills require testing BEFORE writing (RED-GREEN-REFACTOR). Marketplaces require two repositories (catalog + content).

## When to Use

Use this skill when:
- "Create a new skill" or "build a skill"
- "Set up marketplace" or "publish skills"
- "Package skill for distribution"
- "Add skill to marketplace"
- Refactoring existing skills to marketplace standards

## When NOT to Use

Don't use for:
- Using existing skills (that's different)
- General Claude Code questions
- Non-skill related tasks

## Quick Reference: Two-Repository Structure

| Repository | Purpose | Contains |
|------------|---------|----------|
| **Marketplace** | Plugin catalog | `.claude-plugin/marketplace.json`, README, LICENSE |
| **Skills** | Actual skills | `skills/`, `commands/`, manifest.json, docs |

**Installation flow:**
```bash
/plugin marketplace add owner/marketplace-repo
/plugin install plugin-name@marketplace-repo
```

## Essential Workflow: Create New Skill

### Step 1: Write Pressure Tests FIRST (RED Phase)

```bash
# Create test scenarios (3+ with multiple pressures)
# DO NOT write skill yet - watch agents fail first!

# Example pressures to combine:
# - Time pressure (production down)
# - Sunk cost (already invested effort)
# - Authority (senior dev requested)
# - Exhaustion (debugging for hours)
```

**Document baseline behavior** - capture agent quotes showing violations.

### Step 2: Write Minimal Skill (GREEN Phase)

**Structure:**
```
skills/[category]/[skill-name]/
├── SKILL.md                # <1000 words (ideally <500)
├── reference.md            # Heavy reference (unlimited)
├── examples.md             # Real workflows
├── troubleshooting.md      # Error diagnosis
└── TEST_RESULTS.md         # Required testing docs
```

**SKILL.md template:**
```markdown
---
name: skill-name
description: Use when [triggers/symptoms] - [what it does]
---

# Skill Name

## ⚠️ VERIFICATION REQUIRED (if platform-specific)
## Overview
## When to Use
## When NOT to Use
## Quick Reference
## Essential Patterns
## Common Mistakes
## Additional Resources
```

### Step 3: Test and Refactor (REFACTOR Phase)

```bash
# Run pressure tests WITH skill
# Identify new rationalizations
# Add explicit counters
# Re-test until bulletproof
```

### Step 4: Add Slash Command

**Create:** `commands/[skill-name].md`

```markdown
---
description: [Brief description for /help]
location: plugin
---

Use the [skill-name] skill to help with [task].
```

**Update manifest:**
```json
{
  "skills": [{
    "name": "skill-name",
    "path": "skills/category/skill-name",
    "command": "commands/skill-name.md"
  }]
}
```

## Essential Workflow: Create Marketplace

### Repository 1: Marketplace Catalog

**Structure:**
```
marketplace-repo/
├── .claude-plugin/
│   └── marketplace.json      # CRITICAL: Correct schema
├── README.md
├── LICENSE
└── .gitignore
```

**marketplace.json schema:**
```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "metadata": {
    "description": "Brief description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": {
        "source": "url",
        "url": "https://github.com/owner/skills-repo.git"
      },
      "description": "Max 125 chars description",
      "version": "1.0.0",
      "keywords": ["keyword1", "keyword2"],
      "strict": true
    }
  ]
}
```

### Repository 2: Skills Collection

**Structure:**
```
skills-repo/
├── .claude-plugin/
│   └── manifest.json
├── skills/
│   ├── TEMPLATE/
│   ├── deployment/
│   ├── infrastructure/
│   ├── development/
│   └── workflows/
├── commands/                 # IMPORTANT: Slash commands
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── RELEASE-NOTES.md
```

**manifest.json:**
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "marketplace": "owner/marketplace-repo",
  "skills_directory": "skills",
  "commands_directory": "commands",
  "skills": [
    {
      "name": "skill-name",
      "category": "deployment",
      "path": "skills/deployment/skill-name",
      "command": "commands/skill-name.md",
      "tested": true
    }
  ]
}
```

## Common Mistakes

**1. Wrong marketplace.json schema** - Must have `owner` object, `metadata` object, `source.url` not `repository`
**2. No slash commands** - Skills won't show in `/help` without commands/
**3. Testing after writing** - Violates TDD, leads to untested skills
**4. Over 1000 words** - Move heavy content to supporting files
**5. Missing verification** - Platform-specific skills need safeguards
**6. No TEST_RESULTS.md** - Required documentation missing
**7. No git tags** - Plugin system fetches tags, not main branch. MUST tag before users install
**8. Not restarting after install** - Slash commands only load at Claude Code startup
**9. Using `/plugin update` for versions** - Only works for NEW plugins, not version updates. Use uninstall/reinstall instead

## Critical Schema Requirements

### Marketplace Catalog Schema

**Required fields:**
- `name` - string
- `owner` - object with `name` and `email`
- `metadata` - object with `description` and `version`
- `plugins[]` - array of plugin objects

**Plugin object:**
- `name` - string
- `source` - object with `source: "url"` and `url`
- `description` - string (max 125 chars)
- `version` - semantic version
- `keywords` - array of strings
- `strict` - boolean

### Skills Plugin Manifest

**Required fields:**
- `name` - plugin name
- `version` - semantic version
- `skills_directory` - "skills"
- `commands_directory` - "commands"
- `marketplace` - "owner/marketplace-repo"
- `skills[]` - array with path and command

## Verification Checklist

**Before publishing:**
- [ ] Skill tested with 3+ pressure scenarios
- [ ] TEST_RESULTS.md with agent quotes exists
- [ ] Word count <1000 (check: `wc -w SKILL.md`)
- [ ] Slash command created in commands/
- [ ] manifest.json links skill to command
- [ ] marketplace.json has correct schema
- [ ] Both repos have LICENSE (MIT recommended)
- [ ] README has installation instructions
- [ ] **CRITICAL: Create git tags BEFORE users install:**
  ```bash
  # Skills repo
  git tag -a v1.0.0 -m "Description" && git push origin v1.0.0
  # Marketplace repo
  git tag -a v1.0.0 -m "Description" && git push origin v1.0.0
  ```
  **Why:** Plugin system fetches specific git tags, NOT main branch

## Installation Testing

**CRITICAL: Always test clean install with restart**

```bash
# 1. Uninstall for clean test
/plugin uninstall plugin-name

# 2. Install from marketplace
/plugin install plugin-name@marketplace-repo

# 3. RESTART Claude Code (slash commands load at startup)
exit
claude

# 4. Verify installation
/help  # Should show ALL slash commands
ls ~/.claude/plugins/cache/plugin-name/  # Check files installed
cat ~/.claude/plugins/cache/plugin-name/.claude-plugin/manifest.json  # Check version
```

**Installation path:** `~/.claude/plugins/cache/[plugin-name]/` (NOT `~/.claude/skills/`)

**Version updates:** `/plugin update` only checks for NEW plugins. To get version updates:
```bash
/plugin uninstall plugin-name
/plugin install plugin-name@marketplace  # Fetches latest git tag
exit && claude  # Restart for slash commands
```

## Best Practices

- **Test with RED-GREEN-REFACTOR** - No exceptions
- **Create slash commands** - All skills need `/command` for discoverability
- **Follow schema exactly** - marketplace.json must match superpowers pattern
- **Version everything** - Git tag releases (v1.0.0, v1.0.1, etc.)
- **Document testing** - TEST_RESULTS.md is mandatory
- **Two repos** - Catalog (marketplace) + Content (skills)

## Additional Resources

**Templates:**
- See skills/TEMPLATE/ for skill template
- See marketplace schema above for catalog template

**Examples:**
- Railway skill: Tested, verified, with slash command
- Superpowers: github.com/obra/superpowers-marketplace

**Testing:**
- superpowers:writing-skills - TDD methodology
- superpowers:testing-skills-with-subagents - Pressure testing

---

**Remember:**
- Skills require testing FIRST (RED-GREEN-REFACTOR)
- Marketplaces require TWO repositories (catalog + content)
- Slash commands are MANDATORY for `/help` visibility
- Git tags are MANDATORY before users install (plugin system fetches tags, not main)
- Restart Claude Code required for slash commands to appear
- `/plugin update` doesn't update versions - use uninstall/reinstall
