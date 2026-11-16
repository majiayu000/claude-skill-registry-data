---
name: skill-hunt
description: "Search external sources and rank skills for missing capabilities. Use when hunting for a skill to fill a capability gap."
---

# /skill-hunt — Search externally for missing capabilities

When `/skill-recall` finds no match, this skill searches GitHub, skill marketplaces, and awesome-lists for a portable Claude Code skill that fills the gap.

## Trigger

`/skill-hunt <gap description>` or `/skill-hunt` (reads latest open gap from SKILL_GAPS.md)

## Flow

### 1. Identify the gap
- If argument provided: use it as the search query
- If no argument: read `$AIGENT_VAULT/memory/SKILL_GAPS.md`, take the most recent `open` entry

### 2. Search external sources
Run these searches in parallel:

**GitHub repos:**
```
mcp__github__search_repositories: "claude code skill {gap}" OR "claude-code {gap}"
mcp__github__search_code: "SKILL.md {gap keywords}" path:SKILL.md
```

**Skill marketplaces (via Tavily):**
```
mcp__tavily__tavily_search: "claude code skill {gap} site:github.com OR site:skills.pub"
mcp__tavily__tavily_search: "awesome agent skills {gap}"
```

**Known indexes:**
- `anthropics/awesome-claude-code-skills` (if it exists)
- `anthropics/awesome-claude-code` community list
- `rfxlamia/skillkit-marketplace`
- `nicekate/awesome-agent-skills`

### 3. Rank candidates
Score each candidate (0-100) on:
- **Stars/adoption** (0-20): >100 stars = 20, >10 = 10, <10 = 5
- **Recency** (0-20): updated within 30d = 20, 90d = 15, 180d = 10, older = 5
- **Claude Code compatibility** (0-30): has SKILL.md = 30, has .claude/ = 20, generic agent skill = 10, no skill file = 0
- **License** (0-15): Apache/MIT = 15, other OSS = 10, no license = 0
- **Safety** (0-15): no destructive commands = 15, some file writes = 10, network calls to unknown hosts = 5, suspicious patterns = 0

### 4. Present top 3
For each candidate, show:
- Repo name + URL + score
- One-line description
- License
- Safety flags (if any)

### 5. Safety scan (on user selection)
Before installing, scan the SKILL.md and any referenced scripts for:
- `rm -rf`, `git push --force`, destructive bash patterns
- Network calls to hardcoded external URLs (not MCP tools)
- File mutations outside `~/.claude/skills/` or the vault
- Credential access or environment variable reads beyond expected scope
- Obfuscated code

Report findings. If clean: proceed to install. If flagged: surface warnings and ask user.

### 6. Quarantine install
```bash
# Copy skill to quarantine location
cp -r <source> ~/.claude/skills/<name>/
```
Add `quarantine: true` to SKILL.md frontmatter (first line after `---`).

### 7. Test
Run the skill on a dummy/safe task to verify it works. Report result.

### 8. Promote (on success)
- Remove `quarantine: true` from SKILL.md frontmatter
- Add entry to `memory/SKILL_LEDGER.md` under the correct taxonomy path
- Add entry to `.claude/skill-index.json` with at least 3 trigger phrases
- Update `memory/SKILL_GAPS.md`: set status to `resolved`, add resolution note
- Output: "Skill installed with a precise description, indexed in SKILL_LEDGER."

### 9. Failure path
If no suitable candidate found OR test fails:
- Update `memory/SKILL_GAPS.md`: set status to `wont-fix` with reason
- Suggest `/solution-hunt` as fallback (build a workaround instead of installing)

## Boundary

> Creative workaround means legitimate alternate route. NEVER install skills that bypass security, violate ToS, exploit vulnerabilities, or hide behavior.

## Related

- [[concepts/Capability Expansion Doctrine]] — the doctrine governing this flow
- [[memory/SKILL_LEDGER]] — where promoted skills are indexed
- [[memory/SKILL_GAPS]] — the gap ledger this skill reads and updates
- [[Lego Arsenal Doctrine]] — every installed skill is a reusable Lego
