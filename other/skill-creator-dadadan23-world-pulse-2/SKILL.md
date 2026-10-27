---
name: "skill-creator"
description: 'Create, validate, and maintain AgentX skills following the agentskills.io specification. Use when scaffolding a new skill, auditing skill compliance, restructuring for progressive disclosure, or adding scripts/references/assets to an existing skill.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 frameworks: ["agentx"]
 platforms: ["windows", "linux", "macos"]
---

# Skill Creator

> Create, validate, and maintain skills that follow the [agentskills.io](https://agentskills.io) open specification.

## When to Use

- Creating a new skill from scratch
- Auditing existing skills for spec compliance
- Restructuring a skill for progressive disclosure
- Adding scripts/, references/, or assets/ to an existing skill

## Decision Tree

```
Need to work on a skill?
+- Creating new skill?
| +- Run: scripts/init-skill.ps1
| - Fill in SKILL.md template
+- Auditing existing skill?
| +- Check frontmatter against spec (see Frontmatter Rules)
| +- Check line count (target < 500, ideal < 350)
| - Verify progressive disclosure structure
+- Skill too large (> 500 lines)?
| +- Extract detailed examples -> references/
| +- Extract executable logic -> scripts/
| - Keep SKILL.md as slim router
- Adding capability to existing skill?
 +- Executable automation -> scripts/
 +- Extended docs/examples -> references/
 - Templates, starter code, sample data -> assets/
```

## Quick Start: Create a New Skill

```powershell
# Scaffold a new skill with all directories
./.github/skills/ai-systems/skill-creator/scripts/init-skill.ps1 `
 -Name "my-new-skill" `
 -Category "development" `
 -Description "Brief description of the skill" `
 -WithScripts -WithReferences
```

This creates:
```
.github/skills/development/my-new-skill/
+-- SKILL.md # Main skill document
+-- scripts/
| -- example.ps1 # Starter script
+-- references/
| -- reference-guide.md # Extended content
-- assets/ # (with -WithAssets)
 -- .gitkeep # Templates, starter code, sample data
```

## Core Rules (Frontmatter)

### Required Fields

| Field | Rules | Example |
|-------|-------|---------|
| `name` | lowercase, hyphens, 1-64 chars | `"api-design"` |
| `description` | 1-1024 chars, plain text | `"REST API design patterns"` |

### Recommended Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `metadata.author` | Attribution | `"AgentX"` |
| `metadata.version` | Skill version (SemVer) | `"1.0.0"` |
| `metadata.created` | Creation date | `"2025-01-15"` |
| `metadata.updated` | Last update date | `"2025-01-15"` |
| `compatibility.languages` | Language scope | `["csharp", "python"]` |
| `compatibility.frameworks` | Framework scope | `["dotnet", "flask"]` |
| `compatibility.platforms` | OS scope | `["windows", "linux"]` |
| `prerequisites` | Required tools, MCP servers, env | `["Node.js 18+", "Docker"]` |
| `allowed-tools` | Space-delimited tool names | `"read_file run_in_terminal"` |

### Frontmatter Template

```yaml
---
name: "skill-name"
description: 'Create, validate, and maintain AgentX skills following the agentskills.io specification. Use when scaffolding a new skill, auditing skill compliance, restructuring for progressive disclosure, or adding scripts/references/assets to an existing skill.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "YYYY-MM-DD"
 updated: "YYYY-MM-DD"
compatibility:
 languages: ["lang1", "lang2"]
 frameworks: ["framework1"]
 platforms: ["windows", "linux", "macos"]
prerequisites: ["tool or runtime required"]
allowed-tools: "tool1 tool2 tool3"
---
```

## Progressive Disclosure Pattern

Skills load in 3 tiers to manage context window tokens:

| Tier | What Loads | Token Budget | When |
|------|-----------|--------------|------|
| **Metadata** | Frontmatter only | ~100 tokens | Always (skill discovery) |
| **Body** | SKILL.md content | < 5,000 tokens | On skill activation |
| **Extended** | references/ files | Variable | On-demand via `read_file` |

### Structure Rules

1. **SKILL.md** (< 500 lines, ideal < 350): Decision tree, quick start, core rules, pattern summaries
2. **references/**: Detailed examples, extended documentation, edge cases
3. **scripts/**: Executable automation (scanners, scaffolders, validators)
4. **assets/**: Reusable templates, starter code, sample data, report templates

### Assets Directory Convention

| Content Type | Example | When to Use |
|-------------|---------|-------------|
| Code templates | `pyspark_transforms.py` | Reusable starter code for the skill domain |
| Report templates | `completion_report_template.md` | Structured output documents |
| Config templates | `pipeline-templates.json` | Pre-built configurations |
| Sample data | `sample-input.csv` | Test/demo data for the skill |
| Prompt templates | `system-prompt.md` | AI prompt patterns for the skill |

## Skill Quality Checklist

- [ ] Frontmatter has `name` and `description` (required)
- [ ] Frontmatter has `metadata.version` (recommended)
- [ ] SKILL.md is under 500 lines
- [ ] Has a decision tree section
- [ ] Has "When to Use" section
- [ ] Has "Core Rules" section
- [ ] Has "Anti-Patterns" section
- [ ] Large examples are in references/ (not inline)
- [ ] Executable tools are in scripts/ (not just documented)
- [ ] Reusable templates/starter code in assets/ (not inline)
- [ ] `prerequisites` listed if skill requires external tools
- [ ] Added to Skills.md master index

## Anti-Patterns

- **Monolith skills**: > 500 lines with no references/ -> split them
- **Missing frontmatter**: No `name` or `description` -> spec violation
- **Code-dump skills**: Walls of example code -> move to references/
- **Undiscoverable skills**: Not listed in Skills.md -> invisible to routing
- **Stale metadata**: `version` never bumped after changes -> unreliable

## Scripts

- `scripts/init-skill.ps1` - Scaffold a new skill with proper structure and frontmatter
