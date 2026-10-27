---
name: skill-eval
description: Optimize existing AI agent skills with a dual-loop workflow for activation tuning and execution quality. Use when improving a skill after initial creation, diagnosing false triggers or missed triggers, converting subjective output goals into binary assertions, building or refining eval.json test suites, or iteratively refining SKILL.md rules against repeatable checks with a final human review pass.
metadata: 
  author: arisng
  version: 0.3.0
---

# AI Skill Eval

> **DEPRECATED (2026-10-16)** — superseded by the [`waza-cli`](../waza-cli/SKILL.md) skill
> (microsoft/waza): readiness checks, eval scaffolding, quality scoring, and regression gating
> all run through waza now. This skill is kept for historical reference only — do not adopt it
> for new work.

Optimize an existing skill by separating two problems:

1. **Activation**: the skill fires on the right prompts.
2. **Execution**: the skill produces the right output after it fires.

Use `skill-creator` for first drafts. Use this skill to improve a skill that already exists.

## Decide the loop

1. If the problem is **when the skill fires**, run the activation loop.
2. If the problem is **what the skill produces**, run the execution loop.
3. If both are wrong, fix **activation first**, then execution.
4. Never optimize both layers in the same iteration.

## Load only the minimum working set

Read only:

- the target `SKILL.md`
- any references that materially affect output
- a small prompt set that should trigger
- a small prompt set that should not trigger
- a few representative success and failure outputs

Load these references only when needed:

- `references/assertion-playbook.md` to turn vague quality goals into binary checks
- `references/dual-loop-workflow.md` for the full sequence, guardrails, and loop diagram

Copy these assets into the target skill project when you need a starting point:

- `assets/activation-matrix-template.md`
- `assets/eval-template.json`
- `assets/continuous-eval-log-template.md`

## Run the activation loop

Keep the body fixed and change only the frontmatter `description`.

1. Copy `assets/activation-matrix-template.md` into the target skill project.
2. Add positive prompts that should trigger.
3. Add negative prompts that should not trigger.
4. Measure false positives and false negatives with the runtime's native trigger behavior or the best available prompt-set test. **Run the empirical audit**: `pwsh -NoProfile -File skills/skill-eval/scripts/Measure-ActivationAccuracy.ps1 -SkillDir <target>` to get a baseline accuracy score.
5. Tighten or broaden the description based on the observed failures.
6. **Re-run the activation audit** and use `Compare-AuditDelta.ps1` to verify accuracy improved. Keep the new description only if trigger accuracy improves.

### Activation rules

- Name concrete actions, artifacts, and situations instead of broad domains.
- Include nearby trigger phrases that should activate the skill.
- Mention confusing neighbor tasks when disambiguation matters.
- Prefer explicit verbs and file or workflow names over abstract labels.
- Keep execution rules out of the description.

## Run the execution loop

Keep the description fixed and change only execution guidance.

1. Copy `assets/eval-template.json` into `evals/eval.json` in the target skill project.
2. Convert output requirements into binary assertions only.
3. Move subjective quality checks into a human review section instead of pretending they are objective.
4. **Run the structural audit** before making changes: `pwsh -NoProfile -File skills/skill-eval/scripts/Test-SkillStructure.ps1 -SkillDir <target>`.
5. **Run the execution audit** to capture baseline: `pwsh -NoProfile -File skills/skill-eval/scripts/Invoke-EvalSuite.ps1 -SkillDir <target> -OutputSamplesDir <target>/evals/samples`.
6. Change one rule at a time in `SKILL.md` or a referenced file.
7. Re-run the eval suite after the change.
8. **Verify improvement**: `pwsh -NoProfile -File skills/skill-eval/scripts/Compare-AuditDelta.ps1 -BeforeReport before.json -AfterReport after.json`. Keep the change only if the score improves with no regressions.
9. Revert the change if the score drops or creates conflicting assertions.
10. If a human rejects a perfect-scoring output, log it and derive a new assertion candidate.

### Execution rules

- Prefer structural, formatting, and readability checks first.
- Pair upper-bound assertions with completeness checks so the loop cannot win by saying less.
- Keep the assertion set small and high-signal before expanding it.
- Stop adding checks when two assertions start fighting each other.
- Treat score plateaus as a sign to simplify the rule set or escalate to human review.

## Empirical audit

Every skill improvement claim must be backed by reproducible, measurable evidence — not agent intuition. The empirical audit enforces this through four deterministic scripts that accept any `-SkillDir` parameter.

### Audit pillars

| Pillar | Script | What it checks |
|--------|--------|---------------|
| Structural integrity | `Test-SkillStructure.ps1` | SKILL.md frontmatter, eval.json schema, assertion sanity |
| Execution quality | `Invoke-EvalSuite.ps1` | Binary assertions produce deterministic pass/fail scores |
| Activation accuracy | `Measure-ActivationAccuracy.ps1` | False positive/negative rates from activation matrix |
| Improvement delta | `Compare-AuditDelta.ps1` | Before/after reports show improvement, no regressions |

### Script invocation

All scripts are located at `skills/skill-eval/scripts/` and accept `-SkillDir <path>` as their primary parameter. They output JSON to stdout and use exit codes to signal results.

```
# Structural audit
pwsh -NoProfile -File skills/skill-eval/scripts/Test-SkillStructure.ps1 -SkillDir <target>

# Execution quality audit
pwsh -NoProfile -File skills/skill-eval/scripts/Invoke-EvalSuite.ps1 -SkillDir <target> -OutputSamplesDir <target>/evals/samples

# Expression syntax validation (dry-run, no output files needed)
pwsh -NoProfile -File skills/skill-eval/scripts/Invoke-EvalSuite.ps1 -SkillDir <target> -ExpressionSyntaxOnly

# Activation accuracy audit
pwsh -NoProfile -File skills/skill-eval/scripts/Measure-ActivationAccuracy.ps1 -SkillDir <target>

# Improvement delta verification
pwsh -NoProfile -File skills/skill-eval/scripts/Compare-AuditDelta.ps1 -BeforeReport before.json -AfterReport after.json
```

### Exit code semantics

| Exit code | Meaning |
|-----------|---------|
| 0 | Audit passed — structure valid, scores improved, or accuracy meets threshold |
| 1 | Audit failed — non-compliant structure, regressions detected, or accuracy below threshold |
| 2 | Invalid input — bad path, malformed files, or type mismatch |

### Mandatory gate rule

No rule change is accepted without passing the empirical audit. A change that does not improve at least one metric without regressing others is reverted.

### End-to-end audit session

```
# 1. Validate structure
pwsh -NoProfile -File skills/skill-eval/scripts/Test-SkillStructure.ps1 -SkillDir skills/my-skill
# → exit 0, report: { compliant: true, errors: [], warnings: [] }

# 2. Get baseline execution score
pwsh -NoProfile -File skills/skill-eval/scripts/Invoke-EvalSuite.ps1 -SkillDir skills/my-skill -OutputSamplesDir skills/my-skill/evals/samples
# → exit 0, report: { pass_rate: 0.73, score: "8/11" }
# Save as before.json for later comparison.

# 3. Make one rule change in SKILL.md, re-generate outputs

# 4. Re-run eval suite
pwsh -NoProfile -File skills/skill-eval/scripts/Invoke-EvalSuite.ps1 -SkillDir skills/my-skill -OutputSamplesDir skills/my-skill/evals/samples > after.json

# 5. Verify improvement
pwsh -NoProfile -File skills/skill-eval/scripts/Compare-AuditDelta.ps1 -BeforeReport before.json -AfterReport after.json
# → exit 0 if improved, exit 1 if regressed
```

### Adopting this toolkit for any skill

1. Place `evals/eval.json` in the skill root (follow `assets/eval-template.json` schema).
2. Place `activation-matrix.md` in the skill root (follow `assets/activation-matrix-template.md` schema).
3. Create `evals/samples/<case-id>.md` with representative output samples.
4. Run the scripts with `-SkillDir <path>` — they auto-discover files by convention.

### Supported `passes_when` expressions

See `references/assertion-playbook.md` for the full expression grammar. Common patterns:

- `word_count < N` / `word_count > N` / `word_count == N`
- `paragraph_count <= N` / `heading_count >= N`
- `contains("text")` / `not_contains("text")`
- `matches_regex("pattern")` / `section_present("heading")`
- `sentence_count <= N` / `no_sentence_exceeds(N)`
- `json_valid == true`
- `heading_order("H1","H2")`

### Limitations

- Evaluators are designed for prose/documentation output. Code-generation skills may need additional evaluators (e.g., `compiles == true`) as a future extension.
- Sentence splitting is approximate (splits on `.!?` + whitespace).
- `Measure-ActivationAccuracy.ps1` is a metrics computer — filling the `Actual Trigger` column is a manual step.
