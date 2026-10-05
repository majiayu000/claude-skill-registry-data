---
name: skill-discovery
description: Search all Claude Code skill/plugin marketplaces, curated collections, and GitHub for skills matching a use case. Compares findings to installed inventory, ranks by adoption, and handles install + symlink + agent wiring. Use PROACTIVELY when any agent is missing skills, when the user asks "find a skill for X", "is there a skill for Y", "search for Z", or when you notice a capability gap that an existing skill might fill. Also use when setting up a new specialist agent that needs domain skills.
user-invocable: true
argument-hint: <use-case-or-query>
---

# Skill Discovery

Search across all Claude Code skill sources, compare to what's installed, and install the best match — or identify gaps where a custom skill is needed.

## Quick Start

```bash
# Unified search across all sources (skills.sh + GitHub + SkillsMP)
uv run mde-py research skill-discover <query>

# JSON output for programmatic use
uv run mde-py research skill-discover <query> --json

# Via mise task
mise run mde:research:skill-discover -- <query>
```

## The Discovery Pipeline

```
1. INVENTORY — Check what's already installed locally
2. SEARCH — Query working sources (skills.sh, skillkit, GitHub)
3. COMPARE — Rank results by adoption and relevance
4. DECIDE — Install best match, or identify gap for custom skill
5. INSTALL — skills add + symlink + agent wiring
6. VERIFY — Confirm skill file exists and agent references it
```

## Step 1: Check Local Inventory First

Before searching externally, check what's already installed. This avoids duplicates and may reveal the skill already exists.

```bash
# Search installed project + user skills by keyword
find .claude/skills .agents/skills -name "SKILL.md" 2>/dev/null \
  | xargs grep -li "<query>" 2>/dev/null

# Count total installed skills
skillfish list 2>&1 | tail -3

# Search installed plugins
claude plugins list 2>&1 | grep -i "<query>"
```

## Step 2: Search External Sources

Run all agent-accessible tools in parallel, then guide the user for interactive/web tools.

### Agent-Accessible Search Tools (run these via Bash)

```bash
# 1. skills.sh — BEST source. 22K+ skills with install-count rankings.
#    Fastest, most reliable, has adoption metrics as quality signal.
skills find "<query>" 2>&1 | head -30

# 2. skillkit — 15K+ skills, cross-platform (13+ AI tools).
#    Slower (downloads 19MB on first run), but finds results skills.sh misses.
skillkit search "<query>" 2>&1 | head -30

# 3. GitHub code search — deepest, finds niche/personal skills.
#    Searches ALL public SKILL.md files on GitHub.
gh search code "<query>" --filename "SKILL.md" --limit 15 2>&1
```

### User-Interactive Search Tools (user runs these in their terminal)

These tools have interactive TUIs that require a real terminal. Ask the user to run them via the `!` prefix (which runs in their shell session):

```
# 4. skills-installer — 203+ results for popular queries, interactive TUI selector.
#    Searches all public GitHub skills via agentskills.io index.
! skills-installer search "<query>"

# 5. skill.fish browser — 31-33K skills, visual search.
#    User opens https://skill.fish in browser and searches there.
```

Tell the user: "I can search skills.sh, skillkit, and GitHub automatically, but skills-installer and skill.fish need your terminal. Run `! skills-installer search '<query>'` to search the agentskills.io index (203+ results for terraform, 33 for chezmoi)."

### API-Key-Required Sources (setup needed first)

```bash
# 6. SkillsMP API — 546K+ skills, largest catalog.
#    Requires API key: sign up at https://skillsmp.com/docs/api
#    Set SKILLSMP_API_KEY env var, then use skillsmp-mcp-lite MCP server.
curl -s -H "Authorization: Bearer $SKILLSMP_API_KEY" \
  "https://skillsmp.com/api/v1/skills/search?q=<query>" 2>&1 | head -50
```

### Skillfish (installer only, search broken upstream)

`skillfish search` returns empty results — the backend API at mcpmarket.com returns 403. But `skillfish add`, `skillfish list`, `skillfish install` (from skillfish.json manifest), and `skillfish bundle` all work. Use it for installing/managing, not searching.

```bash
# List all installed skills across all agents
skillfish list 2>&1 | tail -5

# Install a specific skill from a known repo
skillfish add <owner/repo/skill-name> 2>&1
```

### GitHub Collection Search (curated quality)

For high-quality skills from known collections, search their repos directly:

```bash
for repo in wshobson/agents VoltAgent/awesome-claude-code-subagents \
  affaan-m/everything-claude-code ComposioHQ/awesome-claude-skills \
  anthropics/skills BehiSecc/awesome-claude-skills \
  travisvn/awesome-claude-skills; do
  echo "=== $repo ==="
  gh api "repos/$repo/git/trees/main" --jq '.tree[].path' 2>/dev/null \
    | grep -i "<query>" | head -5
done
```

## Step 3: Compare and Rank

Build a comparison table from all search results:

| Skill | Source | Installs/Stars | Already Installed? | Author |
|-------|--------|---------------|-------------------|--------|
| name | skills.sh / GitHub | count | YES/NO | ecosystem fit? |

**Ranking criteria (in priority order):**
1. **Relevance** — Does it actually solve the use case? Read the SKILL.md content.
2. **Adoption** — Install count from skills.sh is the best quality signal
3. **Ecosystem fit** — Same author as other installed skills? (terrylica has both chezmoi + mise)
4. **Recency** — When was it last updated?
5. **Not a duplicate** — Check it isn't already installed under a different name

## Step 4: Decide

**A. Strong match found** → Install (Step 5)

**B. Partial match** → Install best available + note gaps for a custom companion skill

**C. No match** → Report: "No existing skill covers this. Closest are [X, Y]. Recommend creating a custom skill covering [gaps]."

## Step 5: Install

```bash
# Install from skills.sh
skills add <owner/repo> --skill <name> --yes 2>&1

# Verify it landed in .agents/skills/
ls .agents/skills/<name>/SKILL.md 2>/dev/null

# Symlink to .claude/skills/ if not auto-linked
if [ ! -e ".claude/skills/<name>" ]; then
  ln -s "../../.agents/skills/<name>" ".claude/skills/<name>"
fi
echo "Symlink: $(ls -la .claude/skills/<name>)"
```

### Wire to Agent (if target agent specified)

```bash
# Read current skills field
grep "^skills:" .claude/agents/<agent-name>.md

# Add the new skill to the YAML list (edit the frontmatter)
# Example: skills: [existing-skill] → skills: [existing-skill, new-skill]
```

## Step 6: Verify

```bash
# 1. Skill file exists
head -5 .claude/skills/<name>/SKILL.md

# 2. Agent references it (if wired)
grep "^skills:" .claude/agents/<agent-name>.md

# 3. Skill resolves through symlink
test -f ".claude/skills/<name>/SKILL.md" && echo "RESOLVES" || echo "BROKEN SYMLINK"
```

## High-Adoption Skill Authors

Track these authors — they produce consistently popular, quality skills:

| Author | Ecosystem | Top Skills (installs) |
|--------|----------|----------------------|
| terrylica/cc-skills | DevOps + dotfiles (20 plugins) | mise-tasks (114), chezmoi-workflows (85) |
| samhvw8/dotfiles | mise specialist | mise-expert (98) |
| bobmatnyc/claude-mpm-skills | Package management | homebrew-formula-maintenance (84) |
| hashicorp/agent-skills | Terraform (official) | terraform-style-guide (2K), terraform-test (1.2K) |
| github/awesome-copilot | Azure/cloud | terraform-azurerm (7.3K) |

## Web Marketplaces (manual search only)

These have large catalogs but no working CLI. Use a browser or MCP when available:

| Marketplace | URL | Catalog Size |
|------------|-----|-------------|
| SkillsMP | https://skillsmp.com | 546K+ (API key required) |
| LobeHub | https://lobehub.com/skills | 229K+ |
| Skill.Fish | https://skill.fish | 31-33K |
| awesomeclaude.ai | https://awesomeclaude.ai/awesome-claude-skills | Curated directory |
| ClawHub | https://clawhub.ai | NEW, vector search |

For the full source registry with URLs, sizes, and search commands, see `references/sources.md`.

## Project-Specific Policies

- **Library-first**: Always search before building custom skills
- **Mise-first**: If a skill needs a CLI tool, install via mise not npm -g
- **Chezmoi pipeline**: Tool installs flow through chezmoi templates
- **Source catalog**: Log every URL discovered to `docs/research/source-catalog.md`
- **Provenance**: Write findings to `docs/research/trail/findings/finding-<slug>.yaml`
