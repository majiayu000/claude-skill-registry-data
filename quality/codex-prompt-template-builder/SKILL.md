---
name: codex-prompt-template-builder
description: >
  Create, choose, adapt, and validate reusable Codex prompt templates that
  orchestrate skills, plugins, files, tools, and safety gates. Use when the
  user asks for massive prompts, prompt templates, reusable Codex prompts,
  plugin-orchestration prompts, marketplace prompt packs, or turning a prompt
  into a skill. Triggers: prompt template, reusable prompt, massive prompt,
  plugin stack prompt, prompt pack, turn this prompt into a skill. Skip when
  the user only needs a one-off short prompt with no reusable structure.
---

# Codex Prompt Template Builder

Goal: turn broad user intent into a reusable, safe, copy/paste Codex prompt
template with clear inputs, plugin/skill routing, workflow steps, validation,
and expected output.

## Workflow

1. Read `references/prompt-template-system.md`.
2. Inspect `prompt-templates/README.md` and choose the closest template.
3. If no template fits, create one new template with frontmatter and a concrete
   prompt body.
4. For public prompt packs, add or update color-coded plugin lanes in
   `PROMPT_GALLERY.md` or `prompt-templates/README.md`.
5. Keep the template reusable:
   - role and outcome
   - dynamic inputs/placeholders
   - plugins or skills to use
   - safety gates
   - execution steps
   - validation
   - final output format
6. For prompt packs, add the template to `prompt-templates/` and update the
   catalog only when discovery changes.
7. Run the template catalog validator.

## Template Frontmatter

Each template must include:

```yaml
---
name: lower-kebab-name
title: Human Readable Title
summary: One sentence outcome.
tags: comma, separated, keywords
plugins: comma, separated, plugins-or-skills
safety: Main safety gate or none
---
```

## Commands

```bash
python3 scripts/prompt_template_catalog.py --validate
python3 scripts/prompt_template_catalog.py --table
```

## References

- `references/prompt-template-system.md`
- `prompt-templates/README.md`
- Pair with `$skill-pack-factory` when creating a full prompt/skill pack.
- Pair with `$skill-quality-gate` before publishing templates as skills.

## Skip When

- The user only needs a tiny one-off prompt.
- The requested template would embed private credentials, account secrets, or
  hidden chain-of-thought instructions.
- The requested workflow mainly installs or runs untrusted code; use
  `$mcp-safety-review` or `$sandbox-source-intake` first.

## Validation

- The template has complete frontmatter and no placeholder secrets.
- The prompt states dynamic inputs, tools/skills/plugins, safety gates,
  workflow, verification, and output format.
- Public templates have clear color-coded plugin/capability lanes when useful.
- The prompt can be copied into Codex without requiring hidden repo context.
- `python3 scripts/prompt_template_catalog.py --validate` passes.
