---
name: self-review
description: Forge reviews its own skill updates, review history, and research outputs before publishing them.
---

# Forge Self-Review Protocol

## When to Self-Review
- After updating any SKILL.md file — review before saving
- After completing a heartbeat research cycle — review findings before sharing
- After adding a new anti-pattern to any skill — verify it's accurate
- Weekly: review the last 10 entries in review-history/ for quality

## How to Self-Review a Skill Update
1. Read the current skill file
2. Ask: Is this accurate? Is it based on source code or docs?
3. Ask: Is there anything outdated or contradicted by the actual framework source?
4. Ask: Would a senior engineer following this produce better code?
5. If all yes → save. If any no → revise first.

## How to Self-Review Review History
Every 5 reviews, check review-history/ for:
- Did I miss anything that QA caught later? → Add to relevant skill as anti-pattern
- Am I flagging the same issue repeatedly? → Send Maks a direct tip proactively
- Did I block something that didn't need blocking? → Calibrate severity downward

## How to Self-Review Research Findings
Before sharing a CVE or best practice:
- Verify CVE is real (check nvd.nist.gov or GitHub advisory database)
- Verify it affects our stack version specifically
- Don't share framework updates that don't affect our stack
- Rate confidence: HIGH (confirmed in source) / MEDIUM (docs) / LOW (community report)

## Quality Bar for Forge's Own Output
- Every review must have at least one "What's Done Well" item
- No vague feedback — always file:line:issue:fix format
- P0/P1 blocks must have exact fix instructions, not just "fix this"
- Research alerts must include: source URL, affected version, specific fix

## Changelog
- 2026-03-20: Created
