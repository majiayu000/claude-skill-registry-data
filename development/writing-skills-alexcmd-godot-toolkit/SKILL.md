---
name: writing-skills
description: Create new godot:* skills — use when adding a new skill to the godot plugin.
---

# Godot Writing Skills

## File Location

```
${CLAUDE_SKILL_DIR}/../<skill-name>/SKILL.md
```

## Required Frontmatter

```markdown
---
name: <skill-name>
description: <one line — "use when X" format>
---
```

## Description Quality

The `description` field is what Claude uses to auto-trigger the skill. It must:
- Use "use when X" format
- Name specific Godot concepts (GDScript, scene, signal, AgentBridge, shader)
- Be specific enough not to false-trigger on non-Godot tasks

Good: `"Write Godot shader code — use when creating spatial, canvas_item, or particle shaders."`
Bad: `"Use when writing code"` (too broad)

## Content Structure

**Domain skills** (coder, shader, ui, etc.):
1. One-sentence purpose
2. Rules or patterns (with GDScript/GLSL code examples)
3. AgentBridge usage examples where relevant
4. Context7 footer if API lookups are likely

**Process skills** (brainstorming, debugging, etc.):
1. One-sentence purpose
2. Hard gate (if applicable)
3. Numbered checklist
4. AgentBridge checkpoint pattern

## Self-Contained Rule

No skill may reference another plugin's skills. All content must be usable without external dependencies.

## After Creating

Restart Claude Code to reload the plugin and pick up the new skill.
Verify with: `claude plugin list` → confirm `godot` appears with updated skill count.
