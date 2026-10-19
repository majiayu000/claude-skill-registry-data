---
name: skill-authoring-evals
description: "Write, validate and evaluate Agent Skills against the open standard: description design that triggers reliably, progressive disclosure, front-matter validation, and eval-driven iteration with_skill/without_skill baselines. Use when an agent must author a skill, audit an existing one for standard compliance, or measure whether a skill fires on the prompts it should; not for writing ordinary documentation."
compatibility: Agent Skills standard (agentskills.io); Claude Code, Codex, Cursor, Gemini CLI, VS Code/Copilot
license: MIT
---
# Skill Authoring and Evaluation

Trigger: author a new Agent Skill, audit an existing one, or measure whether a skill
fires when it should.

## When to use
- Writing a new skill folder with SKILL.md.
- Auditing a skill for standard compliance before shipping.
- A skill that loads but produces poor output — you need the eval loop to find out.
- Comparing two skill versions to decide which to keep.

## When not to use
- Writing ordinary documentation or README files.
- Tuning a model's weights or prompt for a single task — use the task-specific skill instead.

## Procedure (numbered — follow in order)
1. **Design the description first.** It is the trigger. State what the skill does AND the
   concrete symptoms that should load it. Use imperative phrasing ("Use this skill when…"),
   focus on user intent not implementation, and err on the side of being pushy. Hard cap:
   1024 characters.
2. **Name the folder and the `name` field identically.** Slug, lowercase-hyphenated,
   1–64 characters, no leading/trailing hyphen, no `--`. A mismatch means the skill never
   registers — this is the most common silent failure.
3. **Apply progressive disclosure.** Startup loads name + description only; activation
   loads the body (recommended under 5,000 tokens, SKILL.md under 500 lines); references
   and scripts load on demand. Push long material into `references/` linked one level deep.
4. **Validate front matter.** `name` and `description` present; `description` <=1024 chars;
   SKILL.md <=500 lines; every `references/` link well-formed; scripts deterministic and
   runnable offline. Treat `allowed-tools` as optional metadata, never a hard failure
   when absent.
5. **Write trigger eval queries.** Two labelled sets: prompts that SHOULD fire the skill
   and prompts that should NOT. Keep them realistic — real users mention file paths,
   column names and personal context. Use a train/validation split to avoid overfitting the
   description to your own phrasing.
6. **Run the eval loop.** Each test case runs twice: once with the skill, once without.
   This gives the baseline you compare against. Record outputs, timing and assertion
   results in `iteration-N/<eval>/with_skill/` and `without_skill/`, aggregated in
   `benchmark.json`.
7. **Grade outputs, then iterate.** Rewrite the weakest section, re-run evals, re-validate.
   Never ship a skill whose evals were not run.

## Decision tables
- **Description phrasing**: imperative ("Use this skill when…") -> good; declarative
  ("This skill does…") -> rewrite. User intent -> good; implementation detail -> rewrite.
- **Trigger verdict**: should-fire prompt fires -> correct; should-fire prompt does not
  fire -> description too narrow, widen it. Should-not-fire prompt fires -> description too
  broad, narrow it.
- **Validation severity**: missing `name`/`description` -> hard fail; description over
  1024 -> hard fail; SKILL.md over 500 lines -> hard fail; broken `references/` link ->
  hard fail; missing `allowed-tools` -> warn only.

## Near-miss triggers (stop and re-check before proceeding)
- Folder name and `name` field disagree -> the skill never registers; fix before anything
  else.
- Description over 1024 characters -> trim and front-load the trigger phrases.
- All eval prompts are the agent's own phrasing -> you have overfit; recruit fresh prompts.
- Only with_skill runs recorded -> you have no baseline; a skill that does nothing looks
  identical to a skill that works.

## Pitfalls from research
- P1: A well-written skill that never registers because the folder name and `name` field
  disagree.
- P2: A description so vague it never fires, or so broad it fires on everything.
- P3: Evals with no without_skill baseline — you cannot tell if the skill helped.
- P4: Overfitting the description to the eval set so it passes but fails in the wild.
- P5: Shipping a skill whose evals were never run.
- P6: Computing precision as tn/(tn+fp) instead of tp/(tp+fp) — the denominator is the
  number of *fired* cases, not the number of correct negatives. `scripts/eval_metrics.py`
  implements the right formula.
- P7: A firing log that omits a case id — the missing case counts as a miss, so a sparse
  log can make a good skill look bad. Every case must have a firing record.

## Verification checklist
- [ ] Folder name == `name` field, slug form, <=64 chars.
- [ ] `description` <=1024 chars, imperative, states what + when.
- [ ] SKILL.md <=500 lines, body under ~5,000 tokens.
- [ ] Long material moved to `references/`, linked one level deep.
- [ ] Every `references/` link resolves.
- [ ] Scripts deterministic, runnable offline, machine-readable to stdout.
- [ ] `evals.json` passes `scripts/evals_check.py` (unique ids, prompts, should_fire, expected_output).
- [ ] Every case carries a `split` field (`train`/`val`) — verified by `scripts/eval_metrics.py split`.
- [ ] Every case has both `with_skill/` and `without_skill/` output — verified by `scripts/eval_metrics.py delta` (zero identical-to-baseline cases).
- [ ] Trigger evals: should-fire and should-not-fire sets, with a train/validation split.
- [ ] Each eval run has with_skill and without_skill outputs.
- [ ] Weakest section identified and rewritten.

## Worked examples

Full good/bad cases with detection signals live in `references/examples.md`.
The four that matter most for *this* skill:

- **Good trigger vs bad summary.** A description that names concrete symptoms fires;
  "This skill helps with X" never does. Detection: the skill loads on the symptom
  prompt and skips the summary prompt.
- **Name/folder agreement.** `my-skill` vs `name: other` means the skill never
  registers. Detection: `validate_skill.py` prints
  `FAIL: name field 'other' != folder name 'my-skill'` and exits 1.
- **Body size.** 600 lines fails `validate_skill.py` at the 500-line cap. Detection:
  `FAIL: SKILL.md over 500 lines (600)`. Split into `references/`.
- **Baseline presence.** Without `without_skill/` runs you cannot tell whether the
  skill did anything at all. Detection: `scripts/eval_metrics.py delta` reports a
  zero output-delta case as a miss.

## Related skills
- (none — this is the meta-skill: it authors and evaluates the other skills and depends on nothing in this set.)

## References
- procedures: references/procedures.md
- front-matter rules: references/front-matter-rules.md
- trigger evals: references/trigger-evals.md
- worked examples: references/examples.md
- eval schema: references/eval-schema.md
- DESIGN: references/DESIGN.md
- EVALS: references/EVALS.md
- SOURCES: references/SOURCES.md
