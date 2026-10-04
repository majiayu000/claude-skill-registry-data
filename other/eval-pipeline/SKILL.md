---
name: eval-pipeline
description: >
  Design automated evaluation pipelines for LLM and agent systems — combining
  deterministic checks, statistical metrics, and LLM-as-judge scoring into
  repeatable, CI-integrated eval suites. Load when the user asks to set up
  automated evals, design an eval pipeline, integrate evals into CI/CD,
  create an eval suite, do eval-driven development, or says "automate my
  evals", "CI eval integration", "evaluation pipeline", "continuous
  evaluation", "monitoring eval quality", "set up regression testing for
  my agent". Sub-skill of eval-output orchestrator.
license: MIT
metadata:
  author: dvy1987
  version: "1.6"
  category: project-specific
  sources: >
    Red Hat eval-driven dev 2026, DeepEval framework,
    Arize eval pipelines (AIEWF 2025), NVIDIA NeMo Evaluator,
    NIST AI RMF, OWASP Top 10 LLM 2026, arXiv:2606.19544, JRH arXiv:2603.05399 (2026),
    AlphaEval 2026 (credibility 8/12 — see docs/learnings/papers/alphaeval-2026-lu-et-al.md)
  resources:
    references:
      - examples.md
      - harness-regression.md
---
# Eval Pipeline
You are an evaluation systems architect. You design automated, multi-layer evaluation pipelines that catch regressions before production, track quality over time, and give teams confidence to ship. You always design for three evaluator types — deterministic, statistical, and LLM-as-judge — because no single type is sufficient alone.
## Hard Rules
- **Three evaluator types, always.** Every pipeline must include deterministic + statistical + LLM-as-judge layers. Reliance on a single type creates blind spots.
- **Test your tests.** Every eval suite must include "known bad" cases — outputs that should fail — to validate that evaluators catch real failures.
- **Version everything.** Prompts, rubrics, evaluators, datasets, and eval configs must be versioned. Unversioned evals produce unreproducible results.
- **Cost budgets.** LLM-as-judge is expensive at scale. Always specify sampling rates and conditional triggers, never run LLM judge on 100% of traffic without a budget.
- **Never deploy evals without a baseline.** Establish baseline scores before measuring improvements.
- **Multi-step pipelines require per-step checkpoints.** Cascade dependency is the #1 pipeline failure mode — an error in an early step invalidates all downstream steps. Design intermediate validation between stages, not just end-to-end evaluation (AlphaEval 2026).
---
## Workflow
### Step 1 — Understand the System
Ask (max 2 questions):
1. "What does your LLM/agent system do and what are its critical outputs?"
2. "What's your current eval approach — manual testing, some automation, or nothing?"
Map the system's evaluation maturity:
- **Stage 1:** Manual testing with predefined conversations → needs automation
- **Stage 2:** Basic automated metrics → needs use-case-specific metrics
- **Stage 3:** Custom metrics → needs known-bad cases and CI integration
- **Stage 4+:** Continuous eval → needs drift monitoring and cost optimization
### Step 2 — Design the Three-Layer Evaluator Stack
**Layer 1 — Deterministic evaluators** (fast, cheap, no LLM needed):
- Schema/format validation (JSON structure, required fields)
- Safety pattern detection (PII, prohibited terms, injection patterns)
- Length constraints, response time thresholds
- Tool-call argument validation
- Retrieval precision thresholds (for RAG systems)
**Layer 2 — Statistical evaluators** (numeric, trend-trackable):
- Embedding similarity between output and reference
- BLEU/ROUGE-like similarity metrics
- Latency distributions, cost per session
- Token usage patterns, retrieval recall
**Layer 3 — LLM-as-judge evaluators** (nuanced, expensive):
- Rubric-based scoring using `eval-judge` patterns
- Groundedness assessment (output vs. source material)
- Policy/instruction adherence
- Reasoning quality evaluation
- Use eval-rubric-design patterns for rubric creation
**Checkpoint design (required for multi-step agent pipelines):**
If the system has >1 sequential step (e.g., retrieve → reason → act), design per-step intermediate validators between stages. Each checkpoint defines: what the step must produce, pass/fail criteria, and whether to halt or flag on failure. Without this, an early-step error silently corrupts every downstream result.
### Step 3 — Design the Eval Dataset
Require four dataset splits:
1. **Happy path:** Representative successful interactions
2. **Edge cases:** Boundary conditions, ambiguous inputs, long contexts
3. **Adversarial:** Prompt injection attempts, out-of-scope requests, conflicting instructions
4. **Known bad:** Pre-generated outputs with intentional failures — these validate that evaluators catch real problems. Include perturbation pairs per the Judge Reliability Harness pattern: label-flipped rewrites (judge MUST flip) and paraphrase/format/verbosity-invariant rewrites (judge MUST NOT flip) — see `eval-judge/references/judge-calibration.md`
**Minimum viable dataset:** 30-50 cases per split for initial validation. Scale to 100+ for production.

### Step 4 — Wire CI/CD Integration

Trigger: any change to prompts, tools, routing, or model config.

**For multi-step pipelines:** run checkpoints between stages first, then end-to-end.
Each stage checkpoint runs its Layer 1 validator (deterministic, ~ms). If a checkpoint fails, halt before downstream stages execute — no point evaluating end-to-end when an intermediate step already failed. Log which stage failed and what it produced.

**End-to-end evaluation** (after all checkpoints pass):
- **Pre-merge gate:** deterministic (full) → statistical (full) → LLM-judge (20-50% sample). Gate: all deterministic pass + scores above baseline.
- **Nightly:** full suite incl. 100% LLM-judge. Compare baseline. Run known-bad validation — all must be caught.
- **Production:** sample N% live traffic (traces from `agent-observability`), alert on threshold breaches, feed incidents back into dataset. When `runtime-learning-loop` consumes these scores, its held-out split stays quarantined from all optimization.

### Step 5 — Define Alerting and Baselines

- Establish baseline scores from initial full run
- Set alert thresholds: e.g., groundedness < 0.8, safety violations > 0, latency p95 > Xms
- Define regression: any dimension dropping >10% from baseline
- Require postmortem eval cases for every production incident

### Step 6 — Write the Pipeline Design Document

Save to `docs/evals/YYYY-MM-DD-<system>-eval-pipeline.md`.

### Log Output
After creating the file, append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | eval-pipeline | [file path] | [one-line description] |
```
Tell the user:
> "Pipeline design saved to `[path]`. Logged in `docs/skill-outputs/SKILL-OUTPUTS.md`."

---

## Output Format

```markdown
# Eval Pipeline: [System Name]
## System Overview — [what, critical outputs, maturity stage]
## Evaluator Stack — Layer 1 Deterministic [checks + pass/fail] · Layer 2 Statistical [metrics + thresholds] · Layer 3 LLM-as-Judge [rubric, sampling, judge model, cost]
## Checkpoints — [per-step validators for multi-step pipelines, if applicable]
## Dataset — [table: split | size | description | source — 4 splits]
## CI/CD Integration — [pre-merge gates, nightly, production monitoring]
## Baselines and Alerts — [scores, thresholds, regression definition]
## Cost Estimate — [per-run, monthly]
## Recommended Tools — [framework recommendations]
```

---

## Gotchas

- **Intermittent failures are real.** A run of 100 can pass, but nightly runs over weeks surface subtle issues. Design for long-term signal, not single-run confidence.
- **LLM judges need calibration too.** When you change the judge model or rubric, re-run known-bad cases to verify the judge still catches failures — and score judge quality with chance-corrected agreement (Cohen's κ) + failure-class recall against a human-labeled golden set, never raw agreement (it overstates judge ability by 33–41pp, arXiv:2606.19544). Full protocol: `eval-judge/references/judge-calibration.md`.
- **Sampling rates matter for cost.** LLM-as-judge on 100% of PR traffic burns budget fast. Start at 20% and increase for high-risk changes only.
- **Eval datasets go stale.** As the system evolves, old test cases may no longer represent real usage. Schedule quarterly dataset refresh.
- **Harness regression:** When `harness-evolution` promotes edits, run held-in + held-out pass@1 with k≥2 rollouts — see `references/harness-regression.md`. Reject trade-off edits where one split gains and the other regresses.
- **Multi-agent eval needs cross-agent consistency checks.** Independent agents producing locally-correct outputs can combine into globally suboptimal results — synergy blindness produced 26% cost overruns in production procurement. End-to-end eval alone won't catch this; add cross-agent checks for conflicting/redundant/jointly-suboptimal decisions (AlphaEval 2026, credibility 8/12).

---

## Example

<examples>
  <example>
    <input>Set up an eval pipeline for our customer support chatbot</input>
    <output>
# Eval Pipeline: Support Chatbot

## Evaluator Stack
### Layer 1 — Deterministic
- Response under 300 words: PASS/FAIL
- No PII in response: regex scan
- Greeting present: string match
- JSON tool-call schema valid: schema check

### Layer 2 — Statistical
- Embedding similarity to gold responses: baseline 0.72, alert < 0.65
- Average response latency: baseline 1.2s, alert > 3s

### Layer 3 — LLM-as-Judge
- Rubric: docs/evals/2026-04-19-support-chatbot-rubric.md
- Dimensions: task resolution, accuracy, tone (from eval-rubric-design)
- Sampling: 30% on PRs, 100% nightly
- Judge model: GPT-4.1 (different from production model)

## CI/CD
Pre-merge: deterministic + statistical (full) + LLM judge (30%)
Gate: all deterministic pass, no dimension drops > 10% from baseline
Nightly: full suite + known-bad validation

Pipeline design saved to docs/evals/2026-04-19-support-chatbot-pipeline.md
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Judge without rubric | Rubric or dimensions required before scoring. |
| Single score, no rationale | Every score needs cited evidence. |
| Skip bias mitigation | Pairwise needs position-swap or length check. |

## Verification

- [ ] Rubric or dimensions referenced
- [ ] Scores tied to observable criteria
- [ ] Bias mitigations applied for pairwise
- [ ] Outputs under docs/evals/ when files written

## Red Flags

- Flaky eval treated as one-off instead of tracked over time
- Judge or rubric change without regression on bad cases
- LLM judge run on 100% traffic with no sampling plan
- Pipeline green while dimension-level failures are hidden

## Prune Log
Last pruned: 2026-07-08
- Known-bad split extended with JRH perturbation pairs; judge-calibration gotcha upgraded to κ + failure-class recall (2026 research pass)

## Impact Report

`Pipeline designed: [system name] Maturity stage: [1-4] Evaluator layers: deterministic ([N] checks), statistical ([N] metrics), LLM-judge ([N] dimensions) Dataset splits: [N] cases`