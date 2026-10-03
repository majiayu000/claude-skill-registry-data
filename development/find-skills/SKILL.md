---
name: find-skills
description: Discover available skills in the builtin library by keyword.
allowed-tools:
  - list_dir
  - read_file
  - bash
enabled: true
related-skills: [skill-creator]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Find Skills

This skill helps you discover skills available in Poirot's builtin library
and install user-contributed skills.

## When to Use (PROACTIVE — call before starting work)

Call this skill OR the `skill_search` tool when:

- User asks for ANY specialized task (not just "find a skill")
- You're about to start coding/research and haven't checked for relevant skills
- Keywords in user message match skill categories: frontend/chart/diagram/github/debug/tdd/...

### PROACTIVE CHECK (before starting work)

1. Identify task keywords (frontend, chart, github, debug, tdd, ...)
2. Call `skill_search("<keywords>")`
3. If matches found → read the SKILL.md → follow its workflow
4. If no matches → proceed with general capabilities

### Common keywords → skill categories

| Keyword | Likely skill |
|---|---|
| frontend / UI / React / Vue | frontend-design |
| chart / graph / visualization | chart-visualization |
| diagram / architecture | architecture-diagram |
| github / PR / code review | github-code-review / github-pr-workflow |
| debug / bug | systematic-debugging / python-debugpy |
| test / TDD | test-driven-development |
| plan / spike | plan / spike |
| simplify / refactor | simplify-code |

## Legacy When to Use (still valid)

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain

## Builtin skill library

Poirot ships a builtin library at:

```
poirot/backend/agents/skill/builtin_skills/
├── core/                    # meta-skills, loaded at agent startup
├── research/                # research & intelligence skills
├── software-development/    # coding & GitHub skills
├── creative/                # visualization & design skills
└── productivity/            # docs & office skills
```

Only `core/` skills are auto-loaded at startup (registered as active). Skills
under other categories are searchable but not auto-injected — use the
`skill_search` tool or `/skill search <query>` command to find and load them
on demand.

## How to find a skill

### Step 1: List categories

```bash
list_dir("poirot/backend/agents/skill/builtin_skills/")
```

### Step 2: Search by keyword

Use `bash` with `grep` to find skills whose name or description matches:

```bash
bash("grep -rl '<keyword>' poirot/backend/agents/skill/builtin_skills/ --include='SKILL.md'")
```

Or read a category directory and inspect each `SKILL.md` frontmatter:

```bash
list_dir("poirot/backend/agents/skill/builtin_skills/research/")
```

Then read a candidate:

```bash
read_file("poirot/backend/agents/skill/builtin_skills/research/deep-research/SKILL.md")
```

### Step 3: Activate a non-core skill

Non-core skills are not auto-loaded. To use one this turn:

1. Read its `SKILL.md` content
2. Follow its guidance for the current task
3. (Future: `/skill search <query>` will surface + inject matched skills
   automatically once the search tool is wired)

To permanently install a user skill from an external path:

```
/skill install <path> [name]
```

This copies it into `skills/` (user skill storage, gitignored) and re-discovers.

## Presenting options to the user

When you find relevant skills, present them with:

1. The skill name and what it does (from `description` frontmatter)
2. The category it lives in
3. Whether it needs explicit activation

Example:

```
I found a skill that might help. "deep-research" (research category) guides
multi-step web research with evidence cross-verification. It's not auto-loaded
— I'll follow its guidance for this task. Want me to proceed?
```

## When no skills are found

If no builtin skill matches:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using general capabilities
3. Suggest the user could create a new skill with `/skill install` or by
   authoring `skills/<name>/SKILL.md` (see the `skill-creator` skill)

## Common categories

| Category             | Example keywords                          |
| -------------------- | ----------------------------------------- |
| research             | arxiv, deep-research, literature, osint   |
| software-development | debug, github, pr, codebase, subagent     |
| creative             | chart, diagram, frontend, visualization   |
| productivity         | docs, ppt, documentation                  |
| core                 | plan, debugging, tdd, review, skill       |
