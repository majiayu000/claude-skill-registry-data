---
name: skill-export
description: Export Claude skills. Use to generate documentation of all available Claude Skills.
allowed-tools: TodoWrite, Glob, Read, Bash(echo:*), Bash(cat:*), Bash(find:*), Bash(ls:*)
license: MIT
---

# Skill Export

Generate a comprehensive markdown catalog of all Claude skills available in the environment.

## Workflow

### Discover Skills from Three Sources

**Personal Skills**: `~/.claude/skills/*/SKILL.md`
- Scan all subdirectories for SKILL.md files

**Project Skills**: `.claude/skills/*/SKILL.md`
- Scan all subdirectories relative to current working directory

**Plugin Skills**: Requires careful multi-step discovery
1. Read `~/.claude/settings.json` to get enabled plugins (format: `plugin-name@marketplace-id`)
2. Parse each plugin ID into plugin name and marketplace ID
3. Look up marketplace location in `~/.claude/plugins/known_marketplaces.json`
4. Read `{marketplaceLocation}/.claude-plugin/marketplace.json` to get the marketplace manifest
5. Find the specific plugin by name in the manifest's `plugins` array
6. Only scan skills listed in that plugin's `skills` array (do not scan entire marketplace)
7. For each skill path, read `{marketplaceLocation}/{skillPath}/SKILL.md`

**Critical**: Plugin discovery must be scoped to enabled plugins. Do not scan all skills in a marketplace—only those listed in the specific enabled plugin's manifest entry.

### Extract and Format

For each SKILL.md file:
- Parse YAML frontmatter to extract `name` and `description`.
- Record location as absolute path to the skill directory (use `dirname()` of SKILL.md path)

**Critical:** Only read the YAML frontmatter, i.e., the top 5 lines, of SKILL.md files.

Generate markdown table:
```markdown
# Skills

Skills are additional instructions for specific scenarios. Given below is a list of name, description, and location of all available skills. 
If a skill is relevant to the task you're performing based on its description, read the SKILL.md file at the location of that skill for additional instructions.

| Name | Description | Location |
|------|-------------|----------|
| skill-name | Description text | /absolute/path/to/skill |

```

Formatting: escape pipe characters (`\|`), remove newlines from descriptions, sort by location type then name.

### Write Output

Write the output into a SKILLS.md file at the current working directory. Write the generated markdown into the file, and display summary to the user in chat.
