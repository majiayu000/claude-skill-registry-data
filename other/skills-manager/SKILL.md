---
name: skills-manager
description: Import, normalize, and maintain skills from various sources into the centralized TeamDay skills library. Use when updating the skill library, importing new skills from awesome-agent-skills, or syncing with upstream providers.
allowed-tools: Bash, Read, Write, WebFetch, WebSearch
---

# Skills Manager

Maintain the centralized TeamDay skills library by importing skills from various sources.

## Working Directory

**Work in the current repository** (TeamDay-AI/agents)

This skill expects to be run from the root of the agents repo:
```
.
├── skills/
│   ├── anthropic/      # submodule
│   ├── huggingface/    # submodule
│   ├── community/      # imported skills go here
│   └── teamday/        # our skills
├── agents/
└── plugins/
```

Verify you're in the right place:
```bash
git remote -v  # should show TeamDay-AI/agents
```

## Overview

This skill helps you:
1. Discover skills from awesome-agent-skills and other registries
2. Import skills from various repos (handling different structures)
3. Normalize them into our `skills/` directory structure
4. Commit and push updates to TeamDay-AI/agents

## Repository Structure

```
TeamDay-AI/agents/
├── skills/
│   ├── anthropic/           # git submodule → anthropics/skills
│   ├── huggingface/         # git submodule → huggingface/skills
│   ├── community/           # normalized community skills
│   │   ├── csv-summarizer/
│   │   ├── d3-visualization/
│   │   └── ...
│   └── teamday/             # our own skills
│       └── skills-manager/  # this skill
```

## Workflow

### 1. Discover New Skills

Fetch the awesome-agent-skills registry:
```bash
curl -s https://raw.githubusercontent.com/heilcheng/awesome-agent-skills/main/README.md
```

Parse the README to extract:
- Skill name
- Description
- Source repository URL
- Path within repo (if specified)

### 2. Import a Skill

For each skill to import:

1. **Determine structure** - Check if repo has:
   - `skills/{name}/SKILL.md` (standard)
   - `SKILL.md` at root (single skill repo)
   - Custom structure (needs manual mapping)

2. **Download skill files**:
   ```bash
   # Clone sparse checkout for specific skill
   git clone --depth 1 --filter=blob:none --sparse <repo>
   cd <repo>
   git sparse-checkout set <skill-path>
   ```

   Or use GitHub API:
   ```bash
   curl -L https://api.github.com/repos/{owner}/{repo}/contents/{path}
   ```

3. **Normalize structure**:
   - Ensure SKILL.md has required frontmatter (name, description)
   - Copy to `skills/community/{skill-name}/`
   - Include LICENSE if available

4. **Validate**:
   - Check SKILL.md has valid YAML frontmatter
   - Verify scripts have correct paths
   - Test any relative imports

### 3. Add Provider Submodules

For major providers (anthropic, huggingface), use submodules:
```bash
git submodule add https://github.com/{org}/skills.git skills/{provider}
```

### 4. Update Existing Skills

For submodules:
```bash
git submodule update --remote skills/anthropic
git submodule update --remote skills/huggingface
```

For community skills, re-import from source.

### 5. Commit and Push

```bash
git add -A
git commit -m "feat(skills): import {skill-name} from {source}"
git push origin main
```

## Skill Sources

### Primary Registries
- https://github.com/heilcheng/awesome-agent-skills (community index)
- https://github.com/anthropics/skills (official Anthropic)
- https://github.com/huggingface/skills (HuggingFace)

### Known Community Skills

| Skill | Source | Structure |
|-------|--------|-----------|
| csv-summarizer | coffeefuelbump/csv-data-summarizer-claude-skill | root SKILL.md |
| d3-visualization | chrisvoncsefalvay/claude-d3js-skill | root SKILL.md |
| playwright | lackeyjb/playwright-skill | root SKILL.md |
| aws-skills | zxkane/aws-skills | skills/ dir |
| epub-converter | smerchek/claude-epub-skill | root SKILL.md |

## Import Instructions

When importing a skill:

1. **Check the source repo structure**
   - Read the README
   - Look for SKILL.md location
   - Identify dependencies (scripts, assets)

2. **Handle edge cases**
   - Missing frontmatter → Add based on README
   - Different naming → Normalize to kebab-case
   - Relative paths in scripts → Update paths

3. **Preserve attribution**
   - Keep original LICENSE
   - Add source URL to SKILL.md frontmatter: `source: https://github.com/...`
   - Credit original author

## Example: Import a New Skill

```
User: Import the D3 visualization skill

Agent:
1. Fetch https://github.com/chrisvoncsefalvay/claude-d3js-skill
2. Check structure → found SKILL.md at root
3. Read SKILL.md → has valid frontmatter
4. Copy to skills/community/d3-visualization/
5. Verify scripts work
6. Commit: "feat(skills): import d3-visualization from chrisvoncsefalvay"
7. Push to main
```

## Maintenance Tasks

### Weekly: Check for Updates
- Pull latest awesome-agent-skills
- Compare with our imports
- Flag new skills for review

### Monthly: Full Sync
- Update all submodules
- Re-import community skills
- Remove deprecated skills
- Update README with current inventory

## Notes

- Always test skills before committing
- Some skills may need adaptation for our environment
- Keep community skills in `skills/community/` separate from provider submodules
- Document any modifications made during import
