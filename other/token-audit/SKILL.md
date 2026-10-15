---
name: token-audit
description: Audit a repository for token waste — find redundant context files, measure baseline, recommend optimizations
---

# Token Audit — Repository Context Optimization

## Purpose
When Pantheon is installed in a new repository, run this skill to audit and optimize all AI context files for token efficiency.

## Step 1: Discover Context Files

Scan the repository for ALL files that contribute to AI context:

```bash
# Auto-loaded files (every invocation)
AGENTS.md
CLAUDE.md
.gemini/AGENTS.md
.github/copilot-instructions.md
.github/instructions/*.md
.claude/CLAUDE.md
.cursor/rules/*.mdc
.windsurfrules
.kilocode/rules/*.md
.clinerules
.opencode/agents/*.agent.md

# Memory bank
docs/memory-bank/*.md
docs/adr/*.md

# Skills (lazy-load)
.github/skills/*/SKILL.md
.claude/skills/*/SKILL.md
.opencode/skills/*/SKILL.md
```

## Step 2: Build Redundancy Map

Read all discovered files and map what information appears where:

| Information | Found in files | Lines duplicated |
|---|---|---|
| Tech stack | AGENTS.md, 00-overview.md, copilot-instructions.md | ~15 |
| Run commands | AGENTS.md, 03-tech-context.md, commands.md | ~10 |
| Agent roles | AGENTS.md, copilot-instructions.md, zeus.agent.md | ~20 |
| CI/CD rules | AGENTS.md, copilot-instructions.md, .github/workflows | ~12 |
| Coding standards | copilot-instructions.md, instructions/*.md | ~25 |

## Step 3: Measure Baseline

Count lines and estimate tokens:

```bash
# Auto-loaded context (every invocation)
wc -l AGENTS.md .github/copilot-instructions.md /memories/repo/*.md 2>/dev/null

# On-demand context (read by agents)
wc -l docs/memory-bank/*.md 2>/dev/null

# Skills (lazy-load)
find .github/skills .claude/skills .opencode/skills -name "SKILL.md" 2>/dev/null | xargs wc -l 2>/dev/null

# Agent definitions
wc -l .github/agents/*.agent.md .opencode/agents/*.agent.md .claude/agents/*.agent.md 2>/dev/null
```

Estimate: **1 line ≈ 4 tokens** (markdown average)

## Step 4: Identify Red Flags

Check for content that should NOT be auto-loaded. Use specific patterns, not generic keywords:

- [ ] Wave delivery tables: `Wave 1:`, `Wave 2:`, `## Wave`, `wave-by-wave` (NOT "DAG Waves" pattern)
- [ ] Delivery history: `delivered:`, `what was delivered`, `delivery history`, `delivery log`
- [ ] Progress metrics: `[0-9]+% complete`, `commit count`, `commits: [0-9]` (NOT in progress-log.md)
- [ ] Last-updated dates: `**Last Updated**:`, `<!-- last.updated:` (git has this)
- [ ] Cleanup logs: `deleted X lines of dead code`, `legacy cleanup`, `cleaned up X`
- [ ] Duplicated tech stack: same phrase in >3 files (use long phrases, not single words)
- [ ] Files exceeding line limits: AGENTS.md >80, memory-bank >100
- [ ] Empty or near-empty files that waste discovery overhead

**Skip files where the keyword is expected:**
- `progress-log.md` → skip "progress" checks
- `active-context.md` → skip "wave" checks (may reference wave patterns legitimately)
- Architecture docs → skip "DAG Waves" (it's a pattern name, not historical content)

## Step 5: Recommendations

Generate a structured report:

### Immediate Actions (high impact)
1. **Consolidate duplicated files** — merge files with >50% content overlap
2. **Remove historical content** — move delivery logs, wave tables to git/issues
3. **Compress verbose sections** — convert prose to tables (40-60% token savings)
4. **Delete derivable content** — router lists, entity tables that exist in code

### Structural Changes (medium impact)
5. **Create lazy-load skills** — move operational procedures from auto-loaded files to skills/
6. **Set up memory bank** — 3 files max: project.md, active-context.md, progress-log.md
7. **Shorten descriptions** — agent/command/skill descriptions under 100 chars

### Ongoing (maintenance)
8. **Set line limits** — AGENTS.md < 80, memory-bank files < 100
9. **Re-audit after major changes** — run this skill quarterly or after big features

## Step 6: Apply Optimizations

If user approves, execute:

1. Merge redundant files
2. Delete historical content
3. Compress verbose sections (prose → tables)
4. Create skills for heavy operational content
5. Set up optimized memory bank structure
6. Update cross-references

## Output Format

```
## Token Audit Report

### Baseline
- Auto-loaded: X lines (~Y tokens)
- On-demand: X lines (~Y tokens)
- Skills: N files, X lines total
- Agents: N files, X lines total
- **Total baseline: ~Y tokens per invocation**

### Redundancy
- X instances of duplicated content found
- Estimated waste: ~Y tokens per invocation

### Red Flags
- X files with historical content
- X files with derivable content (exists in code)
- X files exceeding line limits

### Recommended Actions
1. [action] — saves ~Y tokens
2. [action] — saves ~Y tokens
...

### Projected After Optimization
- Auto-loaded: X lines (~Y tokens) — **Z% reduction**
```
