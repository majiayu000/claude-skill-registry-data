---
name: grading-claude-agents-md
description: Grades and improves CLAUDE.md (Claude Code) and AGENTS.md (Codex/OpenCode) configuration files. Use when asked to grade, score, evaluate, audit, review, improve, fix, optimize, or refactor agent config files. Triggers on 'grade my CLAUDE.md', 'score my AGENTS.md', 'is my CLAUDE.md too big', 'improve my agent config', 'fix my CLAUDE.md', 'optimize context usage', 'reduce tokens in CLAUDE.md', or 'audit my config files'. Automatically grades both files if present, generates improvement plan, and implements changes on approval.
---

# Grading CLAUDE.md and AGENTS.md

Grade agent configuration files, generate improvement plans, and implement fixes.

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. GRADE          2. PLAN           3. IMPLEMENT          │
│  ─────────         ─────────         ─────────────         │
│  Auto-detect       Show issues       Apply fixes           │
│  files → Score     with fixes →      on approval →         │
│  against rubric    prioritized       verify result         │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

1. **Detect config files**: Look for CLAUDE.md and/or AGENTS.md in project
2. **Grade each file**: Apply rubric from [references/rubric.md](references/rubric.md)
3. **Generate report**: Score card + prioritized issues + improvement plan
4. **On approval**: Implement changes using [references/improvement-patterns.md](references/improvement-patterns.md)
5. **Verify**: Re-grade to confirm improvements

## Grading Checklist

Copy and track progress:

```
Evaluation Progress:
- [ ] Step 1: Detect CLAUDE.md and AGENTS.md files
- [ ] Step 2: Measure size (lines, bytes, tokens)
- [ ] Step 3: Score Structure (25 pts)
- [ ] Step 4: Score Content Quality (25 pts)
- [ ] Step 5: Score PDA Implementation (25 pts)
- [ ] Step 6: Score Maintainability (25 pts)
- [ ] Step 7: Apply modifiers (±10 pts)
- [ ] Step 8: Generate report with grade
- [ ] Step 9: List improvements with priority
- [ ] Step 10: Ask: "Implement these improvements?"
```

## Score Summary

**Base:** Structure (25) + Content (25) + PDA (25) + Maintainability (25) = 100 pts
**Modifiers:** ±10 pts for bonuses/penalties
**Final:** Capped at 0-100

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Excellent, minimal changes needed |
| B | 80-89 | Good, minor improvements recommended |
| C | 70-79 | Adequate, notable issues to fix |
| D | 60-69 | Poor, significant refactoring needed |
| F | <60 | Critical, major overhaul required |

## Reference Files

| Reference | When to Read |
|-----------|--------------|
| [references/rubric.md](references/rubric.md) | Scoring all criteria |
| [references/improvement-patterns.md](references/improvement-patterns.md) | Implementing fixes |
| [references/size-guide.md](references/size-guide.md) | Understanding thresholds |

## Implementation Workflow

After grading, if user approves improvements:

1. **Backup**: Copy original to `CLAUDE.md.backup`
2. **Create structure**: Add subdirectory configs if needed
3. **Extract content**: Move sections to reference files
4. **Add TOC**: Generate table of contents for files >100 lines
5. **Update imports**: Add @imports for extracted content
6. **Validate**: Run size check on new structure
7. **Report**: Show before/after comparison

## What Gets Fixed Automatically

| Issue | Fix Applied |
|-------|-------------|
| File too large (>500 lines) | Split into subdirectory configs or docs/ |
| Missing TOC (>100 lines) | Generate and insert table of contents |
| No @imports for large sections | Extract to docs/*.md, add @imports |
| Style rules in config | Move to linter config, add pointer |
| Negative-only rules | Add "instead use X" alternatives |
| Duplicate content | Consolidate to single location |
| Monorepo without subdirs | Create package-level CLAUDE.md files |

## Output Format

Grade report structure:

```markdown
# Config Grade Report: [filename]

## Score: XX/100 (Grade: X)

| Pillar | Score | Max |
|--------|-------|-----|
| Structure | XX | 25 |
| Content Quality | XX | 25 |
| PDA Implementation | XX | 25 |
| Maintainability | XX | 25 |
| Modifiers | ±X | ±10 |

## Top Issues (prioritized)

1. **[Issue]**: [Description] → [Fix]
   Impact: +X pts if fixed

2. **[Issue]**: [Description] → [Fix]
   Impact: +X pts if fixed

## Recommended Actions

- [ ] Action 1
- [ ] Action 2
- [ ] Action 3

---
**Implement these improvements? (y/n)**
```

## When Not to Use

Do not use this skill for:
- Creating new skills (use skill-creator)
- General markdown editing
- README.md or documentation files
- System prompts or prompt engineering
- MCP server configuration
