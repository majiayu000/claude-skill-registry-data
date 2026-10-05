---
name: review-skill
description: Inspect a skill's health using observation logs, eval results, and protocol analysis, then propose targeted amendments
version: 1.3.0
---

<Purpose>
Review Skill inspects a skill's health and proposes evidence-based amendments. It closes the feedback loop between skill execution and skill improvement:

opt-in host event → human-reviewed export → inspect → amend → evaluate

This skill implements the inspect and amend phases. Skills never write their
own observations. A host operator may opt in to privacy-minimized collection,
and a named human reviewer must export redacted events before this skill reads
them. Evaluation is handled separately by the eval harness.

**5-phase protocol:**
1. **Skill Profile** — Read the skill's agent prompt, SKILL.md, and CHANGELOG.md to understand current state
2. **Observation Analysis** — Read `observations/{skill}.yaml`, validate its review boundary, and identify category, severity, and outcome patterns
3. **Eval Correlation** — Cross-reference observations only with hash-verified results whose adjacent run-manifest-v1 is schema-valid and has `status: valid`
4. **Health Diagnosis** — Synthesize findings into a structured health report with severity-ranked issues
5. **Amendment Proposal** — For each diagnosed issue, propose a specific, minimal change to the skill prompt with predicted impact
</Purpose>

<Use_When>
- A reviewed observation export shows repeated failures or increasing severity
- A skill's eval scores have dropped or plateaued
- User feedback indicates a skill is missing obvious issues or producing false positives
- A model update has occurred and skill behavior may have shifted
- Periodic health check (quarterly or after significant codebase changes)
- Before shipping a new skill version, to identify pre-existing issues
</Use_When>

<Do_Not_Use_When>
- Building a new skill from scratch — use the skill templates and exemplars
- Running an evaluation — use test-builder to generate suites, eval harness to run them
- Reviewing eval suite quality — use test-critic
- Making a specific, known fix — just edit the skill directly following skill-iteration-workflow
</Do_Not_Use_When>

<Why_This_Exists>
Skills degrade silently. A skill that worked well 3 months ago can quietly start underperforming when:

- The codebase it reviews has evolved beyond its assumptions
- Model behavior has shifted after an update
- User tasks have drifted beyond the skill's training distribution
- A tool call pattern the skill relies on has changed

Without systematic inspection, these failures are invisible until someone manually notices worse output. Review Skill automates the inspection and proposes targeted fixes grounded in evidence — not guesswork.

This is the missing piece between "skills as static prompt files" and "skills as living system components."
</Why_This_Exists>

<Steps>
1. User invokes `/review-skill {skill-name}` or `/review-skill {skill-name} --focus {area}`
2. Delegate to review-skill agent with the skill name and optional focus area
3. Agent reads the skill's agent prompt, SKILL.md, CHANGELOG.md, and the reviewed `observations/{skill-name}.yaml` export if available
4. Before reading metrics, agent runs `python3 scripts/validate_review_evidence.py {result-artifact}`; only an artifact hash-listed by exactly one adjacent schema-valid run-manifest-v1 with `status: valid` is eligible
5. Agent produces a Health Report with diagnosed issues and proposed amendments
6. User reviews amendments and decides: apply, iterate, or dismiss

**Optional flags:**
- `--focus routing` — Focus on whether the skill triggers correctly
- `--focus instructions` — Focus on protocol steps and evidence requirements
- `--focus tools` — Focus on tool call patterns and environment assumptions
- `--focus calibration` — Focus on severity calibration and false positive rate
- `--since 2026-03-01` — Only analyze observations after this date
</Steps>

<Benchmark_Test_Info>
No benchmarks yet. Review Skill is a meta-skill that operates on other skills' observation data.

Expected validation approach:
- Create synthetic, privacy-minimized reviewed exports for 3-5 skills with known failure patterns
- Run review-skill on each and verify it identifies the planted patterns without accessing raw prompts or outputs
- Verify proposed amendments target the right protocol sections
- Measure false positive rate (amendments proposed for non-issues)
</Benchmark_Test_Info>
