---
name: skill-new
description: "Scaffold a new Clade skill end-to-end — interview for use cases and trigger phrases, generate SKILL.md + prompt.md with spec-validated frontmatter (bilingual triggers, NOT-for disambiguation), wire golden-set routing tests, and run the lint gate before committing"
when_to_use: "create a new skill, scaffold a skill, add a skill, write a new slash command, build a skill for X, 新建技能, 创建技能, 写个新技能 — NOT for hook generation (use /generate-hook), NOT for absorbing external skill repos (use /equip)"
user_invocable: true
argument-hint: '[skill-name or one-line description of what it should do]'
---

# Skill New

Scaffolds a new skill for the Clade skill registry (`configs/skills/`),
encoding the Agent Skills spec rules (agentskills.io) and Clade's own
conventions so every new skill is born consistent, discoverable, and tested.

## What it does

1. Checks the existing 127+ skills for overlap first (extend beats duplicate)
2. Interviews for the missing pieces: use cases, trigger phrases (EN + 中文),
   sibling disambiguation, invocability, arguments
3. Generates `SKILL.md` (discovery layer) + `prompt.md` (execution body)
   following the frontmatter hard rules enforced by `validate-skills.py`
4. Adds golden-set routing test cases to
   `orchestrator/tests/test_routing_eval.py` so triggering is CI-guarded
5. Runs the full validation gate: skill lint + routing eval
6. Commits via `committer` and reminds about `./install.sh` deploy

## Usage

```
/skill-new                          # full interview
/skill-new pdf-extract              # name known, interview the rest
/skill-new "summarize meeting notes into action items"
```

## Frontmatter hard rules (validated, don't fight them)

- `name` = directory name, kebab-case, no "claude"/"anthropic"
- `description` ≤ 1024 chars, single line, WHAT + key capabilities, no `<` `>`
- `when_to_use` carries trigger phrases users would actually type (EN + 中文),
  ending with `NOT for X (use /y)` clauses when siblings could confuse routing
- `SKILL.md` body under 500 lines (Agent Skills spec); execution detail lives
  in `prompt.md`, bulky reference material in `references/`
- No `README.md` inside the skill folder
