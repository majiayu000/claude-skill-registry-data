---
name: insight-skill-generator
version: 0.1.0
description: Use PROACTIVELY when working with projects that have docs/lessons-learned/ directories to transform Claude Code explanatory insights into reusable, production-ready skills. Analyzes insight files, clusters related content, and generates interactive skills following Anthropic's standards.
---

# Insight-to-Skill Generator

## Overview

This skill transforms insights from the `extract-explanatory-insights` hook into production-ready Claude Code skills. It discovers insight files, clusters related insights using smart similarity analysis, and guides you through interactive skill creation.

**Key Capabilities**:
- Automatic discovery and parsing of insight files from `docs/lessons-learned/`
- **Deduplication** to remove duplicate entries from extraction hook bugs
- **Quality filtering** to keep only actionable, skill-worthy insights
- Smart clustering using keyword similarity, category matching, and temporal proximity
- Interactive skill design with customizable patterns (phase-based, mode-based, validation)
- Flexible installation (project-specific or global)

## When to Use This Skill

**Trigger Phrases**:
- "create skill from insights"
- "generate skill from lessons learned"
- "turn my insights into a skill"
- "convert docs/lessons-learned to skill"

**Use PROACTIVELY when**:
- User mentions they have accumulated insights in a project
- You notice `docs/lessons-learned/` directory with multiple insights
- User asks how to reuse knowledge from previous sessions
- User wants to create a skill but has raw insights as source material

**NOT for**:
- Creating skills from scratch (use skill-creator instead)
- Creating sub-agents (use sub-agent-creator instead)
- User has no insights or lessons-learned directory
- User wants to create MCP servers (use mcp-server-creator instead)

## Response Style

**Interactive and Educational**: Guide users through each decision point with clear explanations of trade-offs. Provide insights about why certain patterns work better for different insight types.

## Quick Decision Matrix

| User Request | Action | Reference |
|--------------|--------|-----------|
| "create skill from insights" | Full workflow | Start at Phase 1 |
| "show me insight clusters" | Clustering only | `workflow/phase-2-clustering.md` |
| "design skill structure" | Design phase | `workflow/phase-3-design.md` |
| "install generated skill" | Installation | `workflow/phase-5-installation.md` |

## Workflow Overview

### Phase 1: Insight Discovery and Parsing
Locate, read, **deduplicate**, and **quality-filter** insights from lessons-learned directory.
→ **Details**: `workflow/phase-1-discovery.md`

### Phase 2: Smart Clustering
Group related insights using similarity analysis to identify skill candidates.
→ **Details**: `workflow/phase-2-clustering.md`

### Phase 3: Interactive Skill Design
Design skill structure with user customization (name, pattern, complexity).
→ **Details**: `workflow/phase-3-design.md`

### Phase 4: Skill Generation
Create all skill files following the approved design.
→ **Details**: `workflow/phase-4-generation.md`

### Phase 5: Installation and Testing
Install the skill and provide testing guidance.
→ **Details**: `workflow/phase-5-installation.md`

## Quality Thresholds

**Minimum quality score: 4** (out of 9 possible)

Score calculation:
- Has actionable items (checklists, steps): +3
- Has code examples: +2
- Has numbered steps: +2
- Word count > 200: +1
- Has warnings/notes: +1

**Skip insights that are**:
- Basic explanatory notes without actionable steps
- Simple definitions or concept explanations
- Single-paragraph observations

**Keep insights that have**:
- Actionable workflows (numbered steps, checklists)
- Decision frameworks (trade-offs, when to use X vs Y)
- Code patterns with explanation of WHY
- Troubleshooting guides with solutions

## File Naming Convention

Files MUST follow: `YYYY-MM-DD-descriptive-slug.md`
- ✅ `2025-11-21-jwt-refresh-token-pattern.md`
- ✅ `2025-11-20-vitest-mocking-best-practices.md`
- ❌ `2025-11-21.md` (missing description)

## Important Reminders

- **Deduplicate first**: Extraction hook may create 7-8 duplicates per file - always deduplicate
- **Quality over quantity**: Not every insight should become a skill (minimum score: 4)
- **Descriptive filenames**: Use `YYYY-MM-DD-topic-slug.md` format
- **Avoid skill duplication**: Check existing skills before generating
- **User confirmation**: Always get user approval before writing files to disk
- **Pattern selection matters**: Wrong pattern makes skill confusing. When in doubt, use phase-based
- **Test before sharing**: Always test trigger phrases work as expected

## Limitations

- Requires `docs/lessons-learned/` directory with insight files
- Insight quality determines output quality (garbage in, garbage out)
- Cannot modify existing skills (generates new ones only)
- Clustering algorithm may need threshold tuning for different domains

## Reference Materials

| Resource | Purpose |
|----------|---------|
| `workflow/*.md` | Detailed phase instructions |
| `reference/troubleshooting.md` | Common issues and fixes |
| `data/clustering-config.yaml` | Similarity rules and thresholds |
| `data/skill-templates-map.yaml` | Insight-to-skill pattern mappings |
| `data/quality-checklist.md` | Validation criteria |
| `templates/*.md.j2` | Generation templates |
| `examples/` | Sample outputs |

## Success Criteria

- [ ] Insights discovered and parsed from lessons-learned
- [ ] Clusters formed with user approval
- [ ] Skill design approved (name, pattern, structure)
- [ ] All files generated and validated
- [ ] Skill installed in chosen location
- [ ] Trigger phrases tested and working

---

**Version**: 0.2.0
**Author**: Connor
**Integration**: extract-explanatory-insights hook
