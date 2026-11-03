---
name: skill-evals-trigger
description: Create trigger evals and run description optimization for a skill. Generates should-trigger/should-not-trigger queries, reviews with user, runs the optimization loop, and applies the best description to SKILL.md. Invoked by skill-creator after the skill is committed.
license: MIT
metadata:
  version: "1.1.3"
---

# Skill Evals Trigger

Creates trigger evals and runs the description optimization loop to improve how reliably a skill activates.

**Prerequisite:** SKILL.md must be committed before running this skill.

---

## Step 1 — Generate trigger eval queries

Create 20 eval queries — should-trigger and should-not-trigger:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Make queries realistic and concrete — include file paths, company names, casual speech, typos, varying lengths. Focus on edge cases. Avoid abstract requests like "Format this data."

**Should-trigger (8–10):** vary phrasing (formal and casual), include cases where the user doesn't name the skill but clearly needs it, and cases where this skill should win against a competing skill.

**Should-not-trigger (8–10):** near-misses only — queries sharing keywords but needing something different. Avoid obviously irrelevant negatives; the negative cases should be genuinely tricky.

---

## Step 2 — Review with user

1. Read the template from `<CORE>/../skills/interactive/.claude/skills/skill-creator/assets/eval_review.html`
2. Replace placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → the JSON array (no quotes — it's a JS variable assignment)
   - `__SKILL_NAME_PLACEHOLDER__` → the skill's name
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → the skill's current description
3. Write to `/tmp/eval_review_<skill-name>.html` and open: `open /tmp/eval_review_<skill-name>.html`
4. User edits queries, toggles should-trigger, clicks "Export Eval Set"
5. File downloads to `~/Downloads/eval_set.json` — check for the most recent version if duplicates exist

Wait for the user to confirm they're done reviewing before proceeding.

---

## Step 3 — Run the optimization loop

Save the confirmed eval set to `<skill-dir>/evals/trigger_eval.json`, then run in the background:

```bash
cd "${CLAUDE_PROJECT_DIR}/.claude"
python -m scripts.run_loop \
  --eval-set <skill-dir>/evals/trigger_eval.json \
  --skill-path <skill-dir> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Warn the user this takes a few minutes. Periodically tail the output with iteration and score updates.

---

## Step 4 — Apply the result

Take `best_description` from the JSON output. Update the `description` field in `<skill-dir>/SKILL.md` frontmatter.

Show the user before/after and report the scores. Return to skill-creator.
