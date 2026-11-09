---
name: ai-evaluation
description: Design and report reproducible AI evaluations against a deterministic baseline, quality thresholds and safety, latency and cost budgets. Use before selecting models or changing prompts, retrieval, tools or providers.
---

# AI evaluation

Status: Draft. Not yet verified in a documented practical example.

Input: capability, current baseline, data classification, constraints and authorized budget. Default to designing the evaluation, not executing it. Provider calls, data sharing and paid experiments require explicit authorization.

## Procedure

1. **Justify.** Compare AI with a deterministic implementation or manual workflow. Define the user outcome and critical failures. Recommend no AI if a simpler method meets the need more dependably.
2. **Dataset.** Build a proposed representative public or synthetic set covering typical, edge, adversarial and out-of-scope inputs. Version it, separate tuning from held-out evaluation, and record expected outputs or a scoring rubric. Do not import private notes or real user data.
3. **Protocol.** Pin model/provider version where possible, prompt, retrieval snapshot, tool contracts, settings and dataset revision. Define quality thresholds, safety gates, latency and cost limits, stopping rules, repeats and human review before running. Use an independent scoring pass and note judge-model bias where applicable.
4. **Safeguards.** Check prompt injection, tool-output trust, sensitive-data leakage, least privilege, structured-output validation and unavailable/ambiguous responses. Define deterministic fallback or human escalation. Never let an evaluated output execute a consequential action automatically.
5. **Compare.** Report per-case and aggregate results, failure severity, variation across repeats, latency distribution and actual usage cost. Separate provider claims, estimates and measurements. Re-evaluate after model, prompt, retrieval or tool changes and retain a rollback option.

## Output

| Candidate / version | Dataset / protocol | Quality and critical failures | Latency / cost | Evidence or not run | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Deterministic baseline | Synthetic task parsing set, revision pending | Not measured | Not measured | Proposed | Establish baseline first |

Include approval scope, unresolved risks and known evaluation limits. A small benchmark is not proof of production readiness. Keep raw outputs outside this public repository when their suitability is uncertain; do not publish sensitive logs or credentials.
