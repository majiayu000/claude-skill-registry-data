---
name: Skill Audit
description: List every installed skill, when it was last invoked, how often, and whether the description still matches the trigger patterns the principal actually uses. Flags dead skills for retirement and frequently-needed-but-missing capabilities for skill creation. Pairs with Caddy.
---

# Skill Audit

Auditing the skill catalog itself. As the install grows from 5 skills to 50, the catalog goes from "I remember every skill" to "I have no idea what's in here." This skill makes the catalog legible to its owner.

## When to use

- Once a quarter — hygiene pass
- When Caddy starts surfacing the wrong skill repeatedly (signals a trigger-pattern mismatch)
- When a new feature feels like it should be a skill but you can't remember if you already built one
- After importing a skill bundle from another principal (e.g., from a public aigent-OS release)
- When considering retiring a project area and want to know which skills go with it

## What it produces

A markdown report with four sections:

### Section 1 — All skills, sorted by last invocation

```
| Skill | Last used | Total invocations (90d) | Description |
|---|---|---|---|
| /open | today | 47 | Start session, load vault context |
| /close | today | 47 | End session, commit memory |
| /caddy-enroll | 5 days ago | 12 | Add a skill to Caddy index |
| /skill-name | 23 days ago | 3 | Example skill entry |
| /old-experiment | 89 days ago | 1 | DEAD — flagged for retirement |
```

### Section 2 — Dead skills (last used >60 days, <3 total invocations)

These are candidates for retirement. List with:
- Skill name + path
- Last-used date
- Total invocations
- Recommendation: keep / archive / delete

### Section 3 — Caddy mismatch detection

For each skill, compare the trigger keywords in `.claude/skill-index.json` against the actual prompt patterns that preceded each invocation. Flag mismatches:

```
⚠️ /channel-audit
   Triggers: "channel status", "YPP progress", "kill a channel"
   Actual prompts that led to invocation: "how are channels doing", "performance check", "review channels"
   Suggested triggers to ADD: "performance check", "review channels", "how are channels doing"
```

### Section 4 — Capability gaps

Heuristic: scan recent prompts (last 30 days) where Caddy fired no hint and the principal manually invoked Read/Bash/Grep instead of a skill. Cluster by keywords. If a cluster has 3+ instances, flag as a capability gap.

```
🆕 Possible missing skill: "weekly metrics rollup"
   Inferred from prompts: "weekly metrics", "this week's numbers", "rollup the week"
   Manual tools used: 4 Bash calls per occurrence
   Suggestion: codify as /weekly-rollup skill via /skills-builder
```

## How to execute

1. Read the skill index and skill folder
2. Pull session logs / invocation history (location depends on install — check `vault/daily/`, `~/.claude/projects/`, hook output logs)
3. For each skill: count last 90 days of invocations, last invocation date
4. Build the four sections above
5. Output as markdown
6. Optionally: write report to `vault/memory/SKILL_AUDIT_<YYYY-MM-DD>.md` for trend tracking

## Why this skill exists

The Caddy pattern only works if the catalog stays useful. Skills accumulate faster than they're retired. Trigger patterns drift from the principal's actual phrasing. Capability gaps go unnoticed for months. Skill audit is the corrective loop.

## Anti-patterns this prevents

- Caddy surfacing dead skills that nobody has used in 6 months (noise)
- Caddy missing skills the principal needs because the trigger keywords don't match how they actually phrase things
- Re-building a skill that already exists (catalog isn't legible to the owner)
- Frequently-manual workflows that should be skills but never get codified
