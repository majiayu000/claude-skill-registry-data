---
name: skill-builder
description: Author a new Claude Code skill the right way, from choosing the storage tier (project, shared library, or user-global) to scaffolding the SKILL.md, linking it across workspaces, and registering it for agents that do not auto-load skills, like Codex. Use when the user says "create a skill", "turn this workflow into a skill", "make this repeatable", or "new skill for".
---

# Skill Builder

The difference between a skill that fires reliably and one that never triggers is craft: a description written as a trigger matcher, absolute paths, explicit guardrails. This skill builds skills that work, and puts them where they belong.

## Step 1: Mine the workflow

The best skills come from a workflow that just happened. If the user is converting something they did this session, extract from THIS conversation: the exact steps, the paths touched, the mistakes made and corrected. Those corrections become the new skill's Rules section.

Pin down:

- **Name**: kebab-case, short, specific (`follow-up-radar`, not `helper-tool`). Check for collisions against every skill already installed in any tier.
- **Triggers**: the literal phrases the user would say. These go in the description, quoted.
- **Job**: one job. If the skill needs an "and also" clause, that is two skills.

## Step 2: Choose the storage tier

| The skill... | Tier | Location |
|---|---|---|
| Only makes sense in this project or workspace | Project | `<project>/.claude/skills/<name>/SKILL.md` |
| Useful across several workspaces | Shared library | One real folder in a central location, linked into each workspace's `.claude/skills/` |
| Generic personal utility, any folder | User-global | `~/.claude/skills/<name>/SKILL.md` |

For the shared library tier, create the real folder once and link it in per workspace:

- Windows (no admin rights needed): `New-Item -ItemType Junction -Path "<workspace>\.claude\skills\<name>" -Target "<library>\<name>"`
- macOS/Linux: `ln -s <library>/<name> <workspace>/.claude/skills/<name>`

An edit to the library folder then propagates to every workspace that links it.

## Step 3: Scaffold the SKILL.md

Always a folder with a `SKILL.md`, never a loose file. Frontmatter has exactly two keys:

```markdown
---
name: <name>
description: <What it does in one sentence. Then the trigger phrases, quoted, so the skill actually fires.>
---

# <Title>

One line: the outcome this skill produces.

## Step 1: ...
## Step 2: ...

## Rules
- The explicit never-do list: what it must not overwrite, delete, send, or invent.

## Output
What the user receives: files, report, chat summary.
```

Craft rules that matter:

- The description is the trigger matcher. Vague descriptions produce skills that never activate.
- Absolute paths for anything outside the current project, so the skill works regardless of where it runs.
- Personal data (emails, prices, client names) goes in an ask-once config file the skill loads at Step 0, never hardcoded, especially if the skill might ever be shared.
- Guardrails are explicit: "never overwrite", "report before acting", "drafts only, never send".

## Step 4: Register for agents that do not auto-load

Claude Code discovers `.claude/skills/` automatically. Codex and similar agents do not. If the workspace serves both, register the skill in the workspace's `AGENTS.md` as required reading: bold name, path, one line saying when it applies. Keep a short pointer in `CLAUDE.md` for load order. The `agents-md-writer` skill generates this contract if the workspace lacks one.

## Step 5: Verify

1. Confirm the skill appears in the available-skills list (fresh sessions pick it up on start).
2. Dry-run it once on throwaway input and delete the test output.
3. Review it with the `skill-reviewer` skill if it will be shared or installed elsewhere.

## Rules

- Never edit installed third-party skill bundles. New work goes in the three tiers above.
- Update rather than duplicate: if an existing skill has overlapping triggers, extend it.
- No em dashes in the skill file or its outputs.

## Output

A working skill folder in the right tier, linked and registered where needed, verified with a dry run.
