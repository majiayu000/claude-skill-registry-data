---
name: cli-ninja-tools
description: CLI power tools for AI-assisted development. Use when (1) needing recommendations for CLI tools to install, (2) processing JSON/YAML data with jq/yq, (3) searching code with ripgrep or ast-grep, (4) documenting a CLI tool or multi-tool recipe you've discovered, (5) wanting to learn CLI patterns for data pipelines, or (6) setting up a new project and want CLI recommendations. Supports three modes - init (project scan), document (capture new recipes), and recommend (codebase analysis).
---

# CLI Ninja Tools

Transform terminal workflows with modern CLI utilities optimized for AI-assisted development.

## Content Organization

### CLI References (`clis/`)
Per-tool documentation with progressive disclosure:
- **[clis/_index.md](clis/_index.md)** - Tier 1/2/3 tool index
- **clis/{tool}/quick.md** - Essential patterns (~50 lines, always safe to load)
- **clis/{tool}/reference.md** - Full documentation (load on demand)

### Recipes (`recipes/`)
Multi-CLI combinations (2+ tools) for specific use cases:
- **[recipes/_index.md](recipes/_index.md)** - Recipe category index
- **recipes/{category}/*.md** - Individual recipes (30-80 lines each)

Categories: github, data-processing, code-analysis, devops, media

## Three Operational Modes

### Mode A: Init Integration
**When**: Setting up new project, after `/init`
**Purpose**: Scan project, recommend relevant CLI patterns

1. Run `python scripts/scan.py` to detect CLIs in project configs
2. Run `python scripts/discover.py --missing` to find missing Tier 1 tools
3. Recommend patterns from `recipes/` matching detected workflows
4. Optionally add "## CLI Tricks" section to CLAUDE.md

### Mode B: Documentation Helper
**When**: User discovers useful CLI pattern or recipe
**Purpose**: Help capture terse, high-quality documentation

For single CLI:
1. Run `{cli} --help`, optionally WebSearch for docs
2. Generate `clis/{cli}/quick.md` following template
3. Offer to save to skill or project CLAUDE.md

For recipe (multi-CLI):
1. User provides command pipeline
2. Decompose each component, explain data flow
3. Generate recipe following `recipes/TEMPLATE.md`
4. Validate with `python scripts/validate.py`

### Mode C: Codebase CLI Recommendations
**When**: User explicitly asks for CLI recommendations
**Purpose**: Analyze codebase patterns, recommend tools

1. Run `python scripts/discover.py` for current tool state
2. Run `python scripts/scan.py` for project patterns
3. Correlate with skill repertoire
4. Generate prioritized recommendations with install commands

## Quick Start

### Check Available Tools
```bash
python scripts/discover.py              # Full report
python scripts/discover.py --tier 1     # Essentials only
python scripts/discover.py --missing    # What to install
```

### Essential Tools (Tier 1)
| Tool | Check | Purpose |
|------|-------|---------|
| jq | `jq --version` | JSON processing |
| ripgrep | `rg --version` | Fast code search |
| fd | `fd --version` | File finder |
| bat | `bat --version` | Cat with syntax |
| ast-grep | `sg --version` | AST refactoring |

```bash
# Quick check all Tier 1
for cmd in jq rg fd bat sg; do command -v $cmd &>/dev/null && echo "OK $cmd" || echo "MISSING $cmd"; done
```

### Quick Install
```bash
# macOS
brew install jq ripgrep fd bat ast-grep

# Ubuntu/Debian
sudo apt install jq ripgrep fd-find bat
cargo install ast-grep --locked

# Windows (Scoop)
scoop install jq ripgrep fd bat ast-grep
```

## Most Common Patterns

### jq (JSON)
```bash
jq '.data[].name' response.json                    # Extract field
jq '.items[] | select(.active)' data.json          # Filter
jq -r '.users[] | [.id, .name] | @csv' users.json  # To CSV
jq -s '.[0] * .[1]' base.json override.json        # Merge
```

### ripgrep (Search)
```bash
rg 'TODO|FIXME' -A 2 --type py                     # With context
rg 'pattern' --json | jq 'select(.type=="match")' # Structured output
rg -l 'deprecated' | xargs sd -i 'old' 'new'       # Search & replace
```

### gh + jq (GitHub)
```bash
gh issue view 123 --json body --jq '.body'         # Inline jq
gh pr view 123 --json files --jq '.files[].path'   # PR files
gh issue list --json number,title --jq '.[].title' # List issues
```

## Loading Strategy

When user asks about CLI tools:
1. Start with this SKILL.md (overview)
2. Load `clis/{tool}/quick.md` for specific tool questions
3. Load `clis/{tool}/reference.md` only for advanced usage
4. Load `recipes/{category}/*.md` for multi-tool workflows

## Extending This Skill

### Add Personal Recipes
Create `~/.claude/skills/cli-ninja-local/`:
```
cli-ninja-local/
├── SKILL.md        # References this skill
├── recipes/        # Personal recipes
└── clis/           # Personal CLI docs
```

### Contributing Back
1. Create recipe following `recipes/TEMPLATE.md`
2. Validate: `python scripts/validate.py your-recipe.md`
3. PR to mem8-plugin

See [recipes/CONTRIBUTING.md](recipes/CONTRIBUTING.md) for details.

## Reference Documentation

- **[clis/_index.md](clis/_index.md)** - All CLI tools by tier
- **[recipes/_index.md](recipes/_index.md)** - All recipes by category
- **[references/top-100-cli-tools.md](references/top-100-cli-tools.md)** - Comprehensive tool list
- **[references/install-guides.md](references/install-guides.md)** - Platform-specific installation
