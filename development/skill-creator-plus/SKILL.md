---
name: skill-creator-plus
description: Audits, creates and improves Agent Skills (folders with a SKILL.md) against Anthropic's skill authoring best practices, the Claude Code skills docs and the prompting guides for newer models such as Claude Fable 5 and Opus 5.5. Audit mode reports every rule as pass, fail or not applicable, with file and line evidence and a proposed fix, and changes nothing until the user approves. Use when the user asks to audit, review, check or score a skill or a folder of skills, to create a new skill or turn a repeated workflow into one, to improve, shorten, refactor or update an old skill for newer models, or to run the skill validator.
license: MIT
---

# Skill Creator Plus

Audits, builds and improves skills so Claude takes the same process on each run. A skill is a table of contents, not a manual: the description gets it chosen, SKILL.md says what to do, and detail waits in reference files until a step needs it.

## Rules for every mode

1. **Report before you change.** Start from evidence: the validator's output and a full read of the skill. In AUDIT, edit nothing until the user picks which findings to fix, because a skill change alters each future run and the user owns that call. A direct request to fix a named problem is already that approval.
2. **Absorb, don't layer.** Fold new guidance into the rule it refines and delete what it replaces. A good edit usually leaves the skill shorter. Write the reason, not the date, so a later editor can tell whether the rule still holds.
3. **Test before you delete.** Newer models often do better with fewer instructions, but only a with-skill and without-skill run proves a line is dead weight. Method: references/testing.md, "Test before you delete".
4. **The validator is the floor.** `scripts/validate_skill.py` checks what a script can check. The judgment rules in references/audit-checklist.md need a careful read.

## Pick the mode

| Mode | When | Output |
|---|---|---|
| AUDIT | A skill or a folder of skills should be checked, scored or improved | A findings report, then only the approved edits |
| NEW | No skill covers the job yet | A new skill folder that passes the validator and its test prompts |
| REFINE | A skill exists and new evidence arrived: a correction, a miss, a shipped result | The same skill, rewritten around the principle, usually shorter |

"Improve this skill" means AUDIT, then REFINE with the approved changes.

## AUDIT

Copy this checklist into the reply and tick it off:

```text
Audit progress:
- [ ] 1 Validator run on every skill in scope
- [ ] 2 Each skill read in full: SKILL.md, references, scripts
- [ ] 3 Every checklist rule marked pass, fail or N/A, with evidence
- [ ] 4 Report written
- [ ] 5 User chose which changes to apply
- [ ] 6 Approved changes applied
- [ ] 7 Validator re-run with no new errors or warnings
```

**Step 1. Run the validator.** `python3 scripts/validate_skill.py <skill-folder>` for one skill, or `--all <folder>` for a library; then audit in full the skills the user picks, by default the five with the most errors. Add `--json` to parse the results. Done when you have output for every skill in scope.

**Step 2. Read the skill.** All of it: SKILL.md, each reference file, each script. Done when you can name the skill's job, its branches and what every file is for.

**Step 3. Mark every rule.** Open references/audit-checklist.md. Script rules take the validator's result; read rules need evidence you can cite as file and line. Done when no rule is unmarked.

**Step 4. Write the report** in the format at the end of the checklist: the table with fails first, the changes ranked by impact, then anything that needs the user's decision. The worked example in examples/ shows the bar.

**Step 5. Stop and ask.** End the turn with the numbered changes. Edit nothing until the user picks.

**Step 6. Apply the approved changes** following REFINE. Before deleting instructions as too prescriptive (rule NM1), run the test in references/testing.md.

**Step 7. Re-run the validator.** If it shows a new error or warning, return to Step 6.

## NEW

```text
New skill progress:
- [ ] 1 Evidence: the task done once without a skill, gaps noted
- [ ] 2 Three test prompts and a no-skill baseline
- [ ] 3 Shape, invocation and freedom chosen
- [ ] 4 Folder scaffolded
- [ ] 5 Frontmatter and body written
- [ ] 6 Validator clean
- [ ] 7 Tests re-run in a fresh session
- [ ] 8 Audit checklist passed
```

1. **Evidence.** Do the task once with Claude and no skill, or read real past examples. Note what had to be explained. Done when you can list the gaps the skill must close.
2. **Tests first.** Write three prompts people would type and record the no-skill result (references/testing.md). Done when the baseline is written down.
3. **Shape.** Choose single file, bundle or router; who can invoke it; and the freedom for each step (references/authoring-guide.md). Done when each choice has a one-line reason.
4. **Scaffold.** Run `python3 scripts/init_skill.py <name> --path <skills-folder>`, adding `--refs`, `--scripts` or `--user-invoked` as needed. It creates the folder and validates it. Done when the folder exists.
5. **Write.** Description first, then the body: the most important rules at the top, a checklist with a go-back line for multi-step work, detail in linked files. Replace every `[FILL: ...]` placeholder. Done when nothing is left to fill.
6. **Validate.** Run the validator on the folder. Fix every error; fix or justify every warning. If an error remains, return to step 5.
7. **Re-test.** Run the test prompts in a fresh session with the skill on. If one fails, return to step 5.
8. **Audit.** Mark the checklist rules that need a read. Done when nothing fails.

## REFINE

1. **Name the evidence** in one line: what happened, what the user said, what shipped.
2. **Find the principle** that explains it. If you cannot name it, you are not ready to edit.
3. **Rewrite** every line the principle touches and delete lines it makes redundant. If a shipped result contradicts an older rule, the shipped result wins; tell the user.
4. **Check.** Run the validator. The file should not have grown; if it did, find what the new rule made redundant. If the validator shows a new error, return to step 3.

## Resources

- [references/audit-checklist.md](references/audit-checklist.md) - every rule with its ID, why it matters, how to check it and its source, plus the report format and the failure modes. Open in AUDIT step 3, and before calling any skill done.
- [references/authoring-guide.md](references/authoring-guide.md) - how to write each part: frontmatter fields, description, structure, degrees of freedom, workflows, scripts, hooks, newer models. Open in NEW steps 3 to 5 and in REFINE.
- [references/testing.md](references/testing.md) - evaluations, fresh-session baselines, Claude A and B, model sweeps, test before you delete. Open in NEW steps 2 and 7, and before cutting instructions.
- [examples/pdf-helper-report.md](examples/pdf-helper-report.md) - a finished audit report for the flawed sample skill in `examples/pdf-helper/`, built from the validator output in `examples/pdf-helper-validator-output.txt`. Open to see the bar for a report.
- `scripts/validate_skill.py` - run it, do not read it. `--help` lists the flags.
- `scripts/init_skill.py` - run it to scaffold a new skill.

Script paths are relative to this skill's folder (in Claude Code, `${CLAUDE_SKILL_DIR}`). Use `python3`, or `python` on Windows. Python 3.8 or newer, standard library only, nothing to install.
