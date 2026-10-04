---
name: new-skill
description: >
  Scaffold a new brooks-lint analysis skill so it passes `npm run validate` and
  `npm run evals` on the first try — generates skills/{name}/SKILL.md (with the
  mandatory "Do NOT trigger for:" clause and a Process section citing guide step
  ranges) plus skills/{name}/{name}-guide.md (sequentially numbered steps), then
  appends paired eval scenarios.
  Triggers when the maintainer asks to "add a new skill", "scaffold a skill", or
  "create a brooks-lint mode".
  Do NOT trigger for: editing an existing skill's content, adding a single eval to
  an existing skill, or authoring skills for some other plugin.
disable-model-invocation: true
---

# brooks-lint — New Skill Scaffold

Skill name comes from `$ARGUMENTS` (kebab-case, e.g. `brooks-security`). If empty,
ask for the name and a one-line purpose first.

Follow the repo's "Adding a New Skill" checklist exactly:

1. **Create `skills/{name}/SKILL.md`** with frontmatter — `name`, a `description`
   that ends with a `Do NOT trigger for:` clause (validate-enforced for shipped
   skills; omitting it causes false triggering), and a `Process` section of 3–6
   bullets that cite the guide's step ranges inline (e.g. `Scan risks (Steps 1–6 of
   the guide)`). Mirror the structure of an existing skill such as
   `skills/brooks-review/SKILL.md` (Setup → Process → Mode line).
2. **Create `skills/{name}/{name}-guide.md`** with sequentially numbered steps —
   no gaps, no duplicates. Sub-steps like `Step 2a` are allowed. The guide owns the
   detailed steps; the SKILL.md Process is just an orientation skeleton.
3. **Wire the framework.** The new SKILL.md Setup section must Read the relevant
   `_shared/` files (`common.md` for Iron Law + Report Template, plus
   `decay-risks.md` / `test-decay-risks.md` as applicable) — `_shared/` is NOT
   auto-loaded.
4. **Add eval coverage** to `evals/evals.json`: append with the next sequential
   `id` at least one happy-path scenario (with the relevant risk code in
   `expected_output`) and at least one false-positive scenario flagged
   `no_risk_codes: true`. Each scenario needs `id`, `name`, `prompt`,
   `expected_output`, `mode`, `files`.
5. **Validate.** `npm run validate` (structure + step continuity + Process-section
   presence) and `npm run evals` (eval schema). Fix until both pass.
6. **Local-test.** `cp -r skills/* ~/.claude/skills/brooks-lint/` (if you've
   symlinked `~/.claude/skills/brooks-lint` to the repo, skip this — edits are
   already live), trigger the new skill in a Claude session, verify the Iron Law
   output, then restore the marketplace copy: `/plugin marketplace update` →
   `/plugin install brooks-lint@brooks-lint-marketplace`.

Do NOT register a slash command by hand — short forms are auto-installed by the
session-start hook. Report the files created and the validate/evals results.
