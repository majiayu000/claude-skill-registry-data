---
name: Caddy Audit
description: Quarterly skill that walks the skill-index against the actual SKILL.md files on disk, reports drift (skills indexed that no longer exist, skills on disk that aren't enrolled, skills whose descriptions have changed since enrollment). Hardens the auto-enrollment pipeline against silent rot.
---

# Caddy Audit

Auto-enrollment makes adding skills easy. Easy adds without periodic audits accumulate drift. `/caddy-audit` is the quarterly hygiene pass that keeps the skill index honest.

## When to use

- Quarterly — once per ~90 days
- After bulk skill changes (importing skills from another principal, refactoring skills folder structure)
- When `/caddy-explain` shows surprising results that suggest the index doesn't match reality
- Triggered by Caddy on prompts like: "/caddy-audit", "audit caddy", "skill index drift", "is the skill index correct", "verify skill catalog", "skill drift check"

## How to execute

### Step 1 — Read the skill index

Load `.claude/skill-index.json` into memory. Each entry has at minimum: `name`, `triggers`, `why`.

### Step 2 — Walk the skills folder

List every `SKILL.md` file in `skills/<name>/SKILL.md` and any project-scope `.claude/skills/<name>.md`. For each, parse the YAML frontmatter for `name` and `description`.

### Step 3 — Cross-reference

For each skill in the index, check:
- **Does the corresponding SKILL.md exist?** If not → INDEX-ORPHAN (in index, not on disk)
- **Does the SKILL.md frontmatter match what was indexed?** Specifically:
  - The skill `name` matches
  - The skill `description` is consistent with the indexed `why` (the indexed why is usually a tighter summary; flag if they're contradictory)

For each SKILL.md file on disk, check:
- **Is it in the index?** If not → DISK-ORPHAN (on disk, not indexed)

### Step 4 — Optional: trigger freshness check

If the skill files store original triggers in their frontmatter (not all do), compare to the indexed triggers. If the SKILL.md has been edited since enrollment AND its trigger frontmatter has diverged from the index, flag as TRIGGER-STALE.

This step is best-effort; not all skills carry trigger frontmatter, and that's fine.

### Step 5 — Output the audit report

```
🔍 Caddy Audit ({date})

Index: {N} entries. Disk: {M} SKILL.md files.

✅ HEALTHY — {K} skills are correctly indexed and on disk.

⚠️ INDEX-ORPHANS ({count}) — in index, no matching SKILL.md:
   - /skill-a — last seen at skills/skill-a/SKILL.md (deleted? renamed?)
   - /skill-b — never had a file?

⚠️ DISK-ORPHANS ({count}) — SKILL.md exists, not in index:
   - skills/new-thing/SKILL.md — run /caddy-enroll skills/new-thing/SKILL.md
   - skills/experimental/SKILL.md — never enrolled

⚠️ TRIGGER-STALE ({count}, best-effort) — SKILL.md frontmatter diverges from index:
   - /skill-c — SKILL.md has 12 triggers, index has 8

Recommended actions:
1. {1-3 specific commands the principal should run to remediate}
```

### Step 6 — Optionally, write the report to the vault

If the principal wants longitudinal data:

```bash
# Save to vault/memory/AUDITS/caddy-{YYYY-MM-DD}.md
```

This becomes a track record over time of how clean the catalog stays. Patterns surface — "we always have 3-5 disk orphans because /skills-builder doesn't always run /caddy-enroll" — which informs whether the auto-enrollment pipeline needs hardening.

## What this skill should NEVER do

- **Auto-fix without asking.** Removing an INDEX-ORPHAN means deleting an entry from `skill-index.json`. The principal should approve that — even if "obvious," the entry might exist for a reason (e.g., a planned skill not yet implemented).
- **Auto-enroll DISK-ORPHANS.** Same reason. The principal might have a half-built skill that they don't want in the index yet.
- **Edit SKILL.md frontmatter.** TRIGGER-STALE means the index drifted; the fix is to re-run `/caddy-enroll` for the affected skill. The skill file is canonical.

## Why this skill exists

Auto-enrollment plus the natural rate of skill experimentation produces drift. Without periodic auditing, the index slowly diverges from reality:

- Old skills get deleted but stay in the index → Caddy emits hints for non-existent skills (errors when invoked)
- New skills get added without enrollment → Caddy can't see them (toolbox compounds without compounding)
- Skill descriptions get refined but enrollment isn't refreshed → Caddy emits stale `why` lines

The 200ms latency budget means Caddy can't afford to do this checking on every invocation. Hence the quarterly audit pattern.

## Connects to

- [[Caddy]] — the system this skill audits
- `/caddy-enroll` — the skill that adds a SKILL.md to the index (this audit's complement)
- `/caddy-explain` — the inspector for individual scoring decisions
- [[The Self-Management Layer]] — `/caddy-audit` is a member; this is the maintenance loop for the catalog itself
