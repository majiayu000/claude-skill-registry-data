---
name: pitch
description: Draft and refine pitch materials -- elevator pitch, one-pager, deck outline, demo script.
version: 0.1.0
execution-mode: advisory
argument-hint: "[elevator | one-pager | deck | demo | refine \"DRAFT\"]"
category: fleet-ops
status: candidate
---
# Pitch

Create and refine pitch materials for investors, partners, customers, or conferences.

## Execution

### 0. Repo hygiene check
Before creating any output file:
1. Identify the target directory (default: `outreach/`)
2. Check if the repo is public: `gh repo view --json isPrivate --jq .isPrivate`
3. If public, verify the target directory is in `.gitignore`
4. If NOT gitignored: add it before writing any files, or warn the user and ask for a different output path
5. Never write confidential content (pitch decks, partner briefs, financial models, outreach targets) to a tracked directory in a public repo

## Operations

### elevator
30-second elevator pitch:
```
For [TARGET CUSTOMER] who [PROBLEM],
[PRODUCT] is a [CATEGORY]
that [KEY BENEFIT].
Unlike [ALTERNATIVES],
we [DIFFERENTIATOR].
```

For your organization/GaaS:
```
For founders running AI agent fleets who need governance without bureaucracy,
your organization GaaS is a governance-as-a-service platform
that gives you Base120 mental models, delegation tokens, and cost controls out of the box.
Unlike building your own governance layer,
we've battle-tested ours across 11,000+ coordination bus messages with 5 agent types.
```

### one-pager
Single page covering:
- Problem (2 sentences)
- Solution (2 sentences)
- How it works (3 bullets)
- Traction (metrics)
- Team (1 line each)
- Ask (what you want)

### deck
Pitch deck outline (10-12 slides):
1. Title + tagline
2. Problem
3. Solution
4. Demo / How it works
5. Market size
6. Business model
7. Traction / Metrics
8. Competition
9. Team
10. Roadmap
11. Ask / Use of funds
12. Contact

### demo
Live demo script with:
- Setup (what to have running)
- Script (what to show, in what order)
- Talking points per screen
- Fallback (what to do if something breaks)
- Closer (end on strongest impression)

### refine
Take existing pitch material and improve it:
- Cut jargon (use `[cultural-adapt]`)
- Strengthen claims with evidence
- Sharpen the differentiator
- Make the ask specific

## Base120 Context
- Primary: **P8** (Narrative Framing)
- Related: **P5** (Empathy Mapping), **CO1** (Synergy), **SY16** (Ecosystem Strategy)
