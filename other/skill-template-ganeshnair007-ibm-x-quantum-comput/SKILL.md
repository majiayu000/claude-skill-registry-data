---
name: skill-template
description: Copy-paste scaffold for creating a new Antigravity Agent Skill. Use when you want to author a skill folder that follows the official SKILL.md format.
---

# Skill Template

Replace this file's frontmatter and body with your own skill. Keep the structure below.

## When to use this skill

- List 2-4 concrete situations where the agent should activate this skill.
- Include keywords a user would naturally type ("deploy", "review PR", "generate tests").

## How to use it

1. Step-by-step instructions the agent should follow.
2. Conventions and constraints (naming, formatting, tools to prefer).
3. What "done" looks like — a verifiable end state.

## Decision tree (optional, for complex skills)

- If situation A → do X.
- If situation B → do Y.
- If unsure → ask the user / choose the safe default.

## Notes for authors (delete this section)

- `description` in the frontmatter is **required** — it's the only thing the agent sees before deciding to activate. Write it in third person with matchable keywords.
- `name` is optional; it defaults to the folder name. Lowercase, hyphens.
- Keep one skill = one job. Split "do everything" skills.
- Optional companion folders: `scripts/`, `examples/`, `resources/`.

---

Part of [awesome-antigravity-skills](https://github.com/LichAmnesia/awesome-antigravity-skills). Browse more Agent Skills at [orangebot.ai/skills](https://orangebot.ai/skills).
