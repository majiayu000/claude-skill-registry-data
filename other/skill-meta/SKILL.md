---
name: skill-meta
description: >-
  Meta-skills about the skills layer itself: creating new skills (scaffold +
  evals), validating and scoring skill quality, the authoring spec
  (frontmatter, folder structure, the unified router shape, checklists),
  installing community skills, the local MCP-ecosystem map, and plugin bundles.
  Use when the task is about skills themselves — "create a skill", "test this
  skill", "install a community skill", "audit skill quality".
---

# skill-meta — skills-about-skills

> Home branch in Memora: `root/skill/skill-meta`. The layer's law is `AGENTS.md`
> plus the Memora nodes under `root/skill/<name>` — every skill's own branch is
> its record, so there is no separate constitution file to consult.

## Choosing a part

| Situation | Part |
|---|---|
| Create a new skill from scratch, with evals and benchmarking | `parts/skill-creator/` (328K — read the sections you need) |
| Validate / score / grade a skill (structure, scripts, quality tiers) | `parts/skill-tester/` (302K — sectioned) |
| The authoring spec: frontmatter, structure, router shape, quality checklist | `parts/skill-authoring/` |
| Install or update a community skill from a local folder or archive | `parts/skill-installer/` |
| Local MCP ecosystem map (BrowseMCP, SearchMCP) | `parts/skill-hub/` |
| Scaffold a plugin bundle with versioned manifest + trust review | `parts/plugin-creator/` |

## Rules

- **One router shape.** Every top-level router carries the same four blocks —
  frontmatter trigger, `Choosing a part`, `Rules`, `Related` — as specified in
  `parts/skill-authoring/` §3. Quality is the body's content, not an extra
  layout.
- **Every router names two things in `Rules`**: the forks that go to
  `ask_questions`, and the skill's own Memora branch (`root/skill/<name>`) that
  it reads and appends to.
- **Creating a skill starts with the intake rule** in `parts/skill-authoring/`
  §0 (repeatability, no coverage in `skills/`, a place not a pile) —
  those parts are the how, not the whether.
- **After creating or editing a skill**: check it against
  `parts/skill-authoring/` §1–3 and run the skill-tester validation if scripts
  are involved. `_scripts/audit_skills_format.py` was retired on 2026-10-17, so
  the check is the spec plus reading the file.
- **Triggers must survive**: a description that does not match the body never
  fires — the August translation incident. Write descriptions in English, in
  the third person, with the words a real request would use.
- Skills live in `skills/`, are synced to Freebuff account-skills by
  `_scripts/sync_skills.py`; archives never delete.

## Related

`planning`, `review` (`verify`), `dev` (`using-superpowers`), `memory`.
