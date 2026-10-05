---
name: skill-auditor
version: 1.0.0
description: Pre-install skill quality auditor. 10-point security and quality scan before installing any third-party skill.
---

# Skill Auditor — Quality Scanner & Curator

> **"装 skill 之前先审。市面 skill 质量参差，安全扫描是刚需。"**

## 10-Point Quality Scan

| # | Check | What It Detects |
|---|-------|-----------------|
| 1 | YAML validity | Broken/missing frontmatter |
| 2 | Description quality | Vague triggers, missing "when to use" |
| 3 | Token efficiency | Bloat >500 lines, redundant instructions |
| 4 | Prompt injection | Hidden commands in description or body |
| 5 | Dangerous commands | `rm -rf`, `.env` writes, `--force` patterns |
| 6 | Data exfiltration | Curl to unknown domains, file reads outside project |
| 7 | Obfuscated code | Base64 blobs, zero-width chars, homograph attacks |
| 8 | Dependency risk | References to unvetted MCP servers or scripts |
| 9 | Trigger accuracy | Does description match actual behavior? |
| 10 | Overlap detection | Duplicates existing installed skills? |

## Scoring

Each check: pass (1) or fail (0). Total: 0-10.

| Score | Verdict | Action |
|-------|---------|--------|
| 9-10 | Trusted | Safe to install |
| 7-8 | Caution | Install, monitor first 5 runs |
| 5-6 | Risky | Read source before installing |
| 0-4 | Blocked | Do not install |

## Skill Recommender

When user asks "which skill for X?":
1. `mcp__memory__search_nodes` → find similar past tasks
2. Scan installed skills for best match
3. If none → search skills.sh marketplace
4. Return top 3 with audit scores

## Curator Mode

Maintains a curated skill index (stored in memory.db via memory-lora):
- Installed skills with audit scores
- Duplicate/deprecated markers
- Recommendations per task type

## Before Install Checklist

- [ ] Audit score ≥7
- [ ] Not duplicate of installed skill
- [ ] Dependencies are trusted
- [ ] No prompt injection detected
- [ ] Description triggers are clear

## Trigger
- User runs `npx skills add` or `/plugin install`
- User browses marketplace ("which skill for X?")
- User asks "is this skill safe?"
- New skill detected in skills/ directory

## Lifecycle
- **Pre-install**: skill-auditor scans safety (this skill)
- **Post-use**: skill-judge evaluates effectiveness (complementary partner)
- **memory-lora**: 🔜 Audit scores stored as baseline for future comparisons
