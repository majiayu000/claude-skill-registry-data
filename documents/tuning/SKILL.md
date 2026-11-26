---
name: tuning
description: >-
  Reads the pack's own evidence (fire log, saved test runs), finds skills that never fire or keep failing, and proposes the smallest fix, applied only after the user's ok. Run by hand: /foma-skills:tuning.
license: Apache-2.0
disable-model-invocation: true
metadata:
  level: "meta"
  uses: ""
  agents: ""
  tokens: "584"
---

Finds which pack skills are not earning their place, from files already on disk, and fixes the worst few with the least spend. Evidence first and free; model work only for flagged skills.

## Steps
1. *Always.* Run `python3 "${CLAUDE_SKILL_DIR}/scripts/evidence.py" $ARGUMENTS` and read nothing else yet. It prints the mode (`repo` = the pack's own repository, `project` = anything else), fire counts, skills that never fired, and failing or flaky saved task runs (runs older than the skill's last edit are ignored and listed: rerun its smoke instead of judging it). Nothing flagged, or a log under 20 sessions and no failing runs: say so and stop.
2. Take at most 3 flagged skills, failing runs first. Read each one's description only; read a body only for a skill with a failing run, together with that run's reason.
3. Diagnose one cause per skill. Never fired: the description misses how the user words the task, or the skill is not needed here; ask for one prompt that should have fired it, do not guess. Failing or flaky run: the body lacks or ignores a line, or the test is wrong; say which. Fires on the wrong task: fix its "Not for" clause.
4. Propose the smallest fix per skill: one description edit (at most 250 characters), one body line, switch off, or delete. Show evidence and the exact diff. Never rewrite a skill whole; never loosen a test to make it pass.
5. Mode `repo`: after the ok, apply and check: `python3 scripts/trigger_test.py <skill> --set heldout`, plus `python3 scripts/task_test.py <skill> --variants skill --models sonnet --runs 1` only when the body changed. Log any changed test prompt or checklist in `docs/engineering/test-ledger.md`. Mode `project`: pack files cannot be edited (a plugin update overwrites them); offer to switch the skill off (the user's call), a CLAUDE.md line, or issue text for the pack's repository; test nothing.
6. Budget per run: 3 skills, 30 Haiku trigger prompts, 2 Sonnet smokes. Stop and ask before going over. Put the test batch's cost line in the report.

## Rules
- Never write without an ok per item.
- Never read all skill bodies or run the full test set.
- Never change a failed test prompt to a passing one; a replacement needs a ledger line and the standard as reason.
- Never add what a one-line CLAUDE.md rule already does.

## Report
- Skills examined, each: diagnosis, fix proposed, applied / declined.
- Spent: the cost line, or "no model runs".
- Not checked: <…>
