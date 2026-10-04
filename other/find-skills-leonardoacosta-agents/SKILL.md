---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
source: ~/.agents/skills@2026-07-13
---


# Find Skills

The job here is **corpus-first**: check installed and repository-local skills before reaching
for the external `npx skills` marketplace. Recommending an external install without checking
the local corpus first risks shipping a duplicate of a skill already installed under a
different name.

## Step 1 — Search This Repo's Corpus First

Three lookup paths exist, ordered by precision: a hand-curated routing table, a generated
description index, then raw grep as the last resort.

MANDATORY: Read [references/search-precedence.md](references/search-precedence.md) before
running any search — it gives the exact command for each path and explains why a
`description`-field hit outranks a body-text hit.

If a real match exists, load it directly — `Skill({ skill: "<name>" })` — rather than
recommending an external install of something equivalent.

## Step 2 — External Marketplace (Only When the Corpus Has Nothing)

`npx skills` is the package manager for the wider agent-skills ecosystem. Reach for it only
after Step 1 comes up empty:

```bash
npx skills find [query]                              # search
npx skills add <owner/repo@skill> -a claude-code -y   # install — ALWAYS -a claude-code (rules/TOOLING.md; omitting it sprawls .agents/.crush/.goose dirs)
```

After install, run `/reload-skills` (CC v2.1.152+) to pick it up in the **current** session; on
older versions a freshly-installed skill stays invisible until restart.

MANDATORY: Read [references/evaluating-candidates.md](references/evaluating-candidates.md)
before recommending ANY skill — corpus hit or external install. It has the anti-patterns table
(never trust a README for freshness, never install a second skill over an existing owner, never
rank by star count alone) and the signals that separate a real match from a false positive
(auto-triggered vs explicit-only, metadata-only skills, duplicate-domain drift, `source:`
provenance dates).

## Step 3 — Nothing Found Anywhere

Say so plainly, offer to help with the task directly, and only suggest turning it into a real
skill if the need is recurring — new in-house skills belong under this repo's `skills/`
directory (see `extend-before-create`), not a personal `~/.agents/skills` fork that nothing else
in this repo can discover.

## References

- [references/search-precedence.md](references/search-precedence.md) — MANDATORY before any corpus search: the 3 lookup paths in precision order, with commands
- [references/evaluating-candidates.md](references/evaluating-candidates.md) — MANDATORY before recommending any skill (internal or external): anti-patterns table + candidate-judging signals
