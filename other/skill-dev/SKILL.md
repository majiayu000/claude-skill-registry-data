---
name: skill-dev
description: |
  Develop or modify a Prismstack product skill. Ensures changes follow skill-craft-guide.
  Trigger: "edit skill X", "improve domain-plan", "add feature to skill-check", "skill-dev"
  Do NOT use when: editing a user's domain stack skills (that's the product /skill-edit)
user_invocable: true
---
<!-- Internal maintenance skill — edit this file directly -->

# /skill-dev: Develop Prismstack Product Skills

You are a Prismstack skill developer. You modify the 10 product skills with discipline, ensuring every change follows the methodology.

## Phase 0: Scope the Change

Parse `$ARGUMENTS` for the target skill and change description.

If not provided, ask:
1. Which skill? (one of the 10 product skills in `skills/*/SKILL.md`)
2. What change? (add feature, fix issue, refactor section, etc.)

Read the current SKILL.md for the target skill fully before making any change.

## Phase 1: Load Relevant Methodology

Based on the type of change, read the appropriate methodology file:

| Change Type              | Read This                                      |
|-------------------------|-------------------------------------------------|
| Structure / sections     | `skills/shared/methodology/skill-craft-guide.md` |
| Scoring / rubric         | `skills/shared/methodology/quality-standards.md`  |
| Artifact flow / wiring   | `skills/shared/methodology/system-wiring-guide.md`|
| Fix loop / triage        | `skills/shared/methodology/fix-loop-guide.md`     |
| Context / accumulation   | `skills/shared/methodology/context-accumulation-guide.md` |

If the change spans multiple areas, read all relevant files. Do not guess at methodology — read it.

## Phase 2: Make the Change

Rules for editing:
- **Minimal and surgical.** Change only what is needed. Do not rewrite surrounding sections.
- **Read before edit.** Always use Read tool on the file before using Edit tool. Never edit blind.
- **Preserve voice.** Match the existing tone and formatting of the skill.
- **No scope creep.** If you notice other issues while editing, note them but do not fix them now. One change per /skill-dev invocation.

Use the Edit tool (not Write) for modifications. Write is only for new files.

## Phase 3: Self-Check (Quick 15D)

After the edit, run a quick quality check on the modified skill:

1. Read `skills/shared/methodology/quality-standards.md` for the 15D rubric
2. Score the modified skill on all 15 dimensions (1-5 scale)
3. Compare to a rough pre-edit baseline (your reading from Phase 0)

Answer these questions:
- Did the target dimension improve? (If not, the change missed its goal.)
- Did any other dimension drop? (If so, the change introduced a regression.)
- Is the overall score at least 3.5 average? (If not, flag for additional work.)

Report the before/after comparison as a compact table.

## Phase 4: Run Install Test

```bash
bash test/install-test.sh
```

All tests must pass. If any fail:
1. Read the failure output
2. Identify whether the failure is caused by your change or pre-existing
3. If caused by your change, fix it and re-run
4. If pre-existing, note it but do not block on it

## Phase 5: Commit

If all checks pass, stage and commit:

```bash
git add skills/<skill-name>/SKILL.md
git commit -m "fix(skill-name): <concise description of change>"
```

Use conventional commit prefixes:
- `feat(skill-name):` — new capability added to the skill
- `fix(skill-name):` — bug or issue fixed
- `refactor(skill-name):` — restructured without behavior change
- `docs(skill-name):` — documentation or comment changes only

## Gotchas

- **Line count guard**: After editing, check `wc -l` on the SKILL.md. Product skills should stay under 200 lines. If over, consider splitting into `references/` files.
- **Do not rewrite the whole skill** when changing one section. Large diffs are hard to review and easy to break.
- **Shared methodology changes** require a different workflow. If the methodology itself is wrong, edit the methodology file directly — do not hack around it in a skill.
- **Test after every change.** Never commit without running install tests.
