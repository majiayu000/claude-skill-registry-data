---
name: skill-new
description: Scaffold a new SKILL.md with the enforced frontmatter and six-section template, then validate it with the skill linter.
disable-model-invocation: true
argument-hint: "/skill-new <kebab-case-name>"
allowed-tools: "Read, Write, Bash, AskUserQuestion"
sensitive: false
---

Meta-skill that creates new skills consistently. Produces a SKILL.md that passes `tools/lint-skills.py --strict` on first save, with placeholders that force the author to fill in the load-bearing parts.

## Overview

Hand-authored skills drift in shape. Some have argument hints, some do not. Some declare allowed tools, some do not. The 6-section template gets partially adopted. This skill removes the drift by scaffolding from a single source of truth and immediately validating the result.

## When to Use

- User says "new skill X", "scaffold skill", "create a slash command for X"
- A new repeatable workflow has emerged that justifies a slash command
- A retrospective surfaced a pattern that should become a skill

Do NOT use when:
- The behavior belongs in a rule, hook, or agent instead (consider first)
- The workflow is too project-specific to live in the global config
- An existing skill already covers the use case (extend it)

## Process

1. **Resolve name.** Accept a kebab-case identifier (e.g., `interview-me`). Reject names that already exist under [`skills/`](../). Reject names that conflict with an existing slash command vocabulary.
2. **Gather inputs.** Ask one question at a time, using `AskUserQuestion`:
   - Invocation. Pick model-invocation only when the agent must reach the skill on its own.
     - Model-invoked, the default: the description is loaded into every session and carries the trigger phrases plus positive routing such as "for X, use /y".
     - User-invoked: add `disable-model-invocation: true`. The description is one human-facing sentence for the `/` menu, with no trigger list, and costs zero context. Claude cannot run it through the Skill tool, so no other skill or rule may hand off to it.
   - Description matching that invocation choice, quoted when it contains `: `
   - Argument hint (example invocations)
   - Tool scope: which tools the skill pre-approves (`allowed-tools`) or which to deny (`disallowed-tools`)
   - Sensitive flag (`true` for destructive or privileged skills)
   - Scripts: does any step run a deterministic operation the agent would otherwise regenerate on every run, such as parsing, validating, or formatting? Ship it as a script in the skill folder and call it, rather than describing it in prose.
3. **Scaffold.** Create `skills/<name>/SKILL.md` with the frontmatter block and the six required headings. Each section gets a placeholder paragraph that names what belongs there. Every Process step ends on a checkable completion criterion, per Completion Criteria in [`standards/agent-instruction-files.md`](../../standards/agent-instruction-files.md).
4. **Validate.** Run `python3 tools/lint-skills.py --strict skills/<name>/SKILL.md`. Block return until the linter passes.
5. **Prove it bites.** For every linter, hook, or check the skill introduces, run it three times: on the clean tree it passes, with one planted violation it fails, and with the violation removed it passes again. Keep the output of all three runs as evidence.
6. **Register.** If a new on-demand rule trigger applies, add an entry to [`rules/index.yml`](../../rules/index.yml). If the skill should appear in the README skill table, update it.

## Common Rationalizations

- "I will copy from another skill instead": copying introduces drift. Scaffold from the template.
- "I will fill the sections in later": the linter blocks merging until the sections exist. Fill them now.
- "I will skip the linter, the file is fine": strict mode catches missing fields you forgot. Run it.
- "The description is good enough at 20 characters": short descriptions fail discovery. Aim for 50+.

## Red Flags

- About to commit a skill where `argument-hint` is empty or absent
- About to commit a skill with neither `allowed-tools` nor `disallowed-tools`
- About to commit a skill missing one of the six required sections
- About to invoke this skill for editing an existing SKILL.md
- About to scaffold a skill whose name collides with an existing one

## Verification

- `python3 tools/lint-skills.py --strict skills/<name>/SKILL.md` returns 0
- Every check the skill introduces passed clean, failed on a planted violation, and passed again once the violation was removed
- A user-invoked skill has `disable-model-invocation: true` and a one-sentence description; a model-invoked skill has trigger phrases and positive routing
- README skill table updated
- [`rules/index.yml`](../../rules/index.yml) updated if the skill is triggered on-demand by keywords
- Frontmatter `name` matches the directory name exactly
- All six required sections present with non-empty bodies
