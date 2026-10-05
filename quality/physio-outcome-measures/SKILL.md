---
name: physio-outcome-measures
description: "Select and compare physiotherapy PROMs, ClinROMs, performance tests, and diagnostic special tests using population-specific evidence. Use for test/ölçek selection, baseline or change measurement, reliability, validity, responsiveness, SEM, SDC/MDC, MIC/MCID, sensitivity, specificity, likelihood ratios, cutoff values, feasibility, Turkish adaptation, licensing, or reassessment. Keep measurement properties, diagnostic accuracy, and prognostic models on separate pathways."
---

# Physio Outcome Measures

## Mandatory first reads

Read [safety core](references/safety-core.md) and [measurement selection method](references/measurement-selection.md). Do not administer or recommend a performance/special test before checking medical stability, falls risk, environment, supervision, and stop criteria.

## Choose the pathway first

- **Measure status or change:** PROM, ClinROM, or performance test → COSMIN pathway.
- **Update probability of a target condition:** diagnostic special/index test → diagnostic-accuracy pathway.
- **Estimate a future outcome:** prognostic factor/model → prognostic-model pathway.

Do not combine these into one “validity score.” A special test modifies probability; it does not independently rule serious disease in or out.

## Selection workflow

1. **Define the construct precisely.** Replace broad labels such as “pain” with intensity, interference, catastrophizing, self-efficacy, activity limitation, or another intended construct.
2. **Define purpose.** Screening, diagnostic probability, discrimination, prognosis, baseline profile, change monitoring, goal attainment, or service evaluation.
3. **Match context.** Age/development, diagnosis, stage/severity, acute/chronic status, setting, language/culture, device, evaluator, delivery mode, and time/resource constraints.
4. **Check a core outcome set.** Use COMET/COSMIN recommendations when relevant; do not treat inclusion in a core set as proof that an instrument is adequate.
5. **Search current evidence.** Open systematic measurement reviews, original validation studies, official instrument documentation, language adaptation, license, and scoring rules. Verify discovery-database numbers in primary sources.
6. **Evaluate properties separately.** Content validity, structural validity, internal consistency, reliability, measurement error, construct/criterion/cross-cultural validity, and responsiveness.
7. **Evaluate interpretability.** Score direction, norms, floor/ceiling effects, MIC/MCID, SEM, and MDC/SDC. Attach every number to its population, version/language, follow-up, method, direction, and uncertainty.
8. **Evaluate feasibility and equity.** Time, burden, equipment, training, cost/license, permission, accessibility, cognition/communication, fatigue, safety, and repeatability.
9. **Choose the smallest sufficient set.** Cover patient priority, key function/participation, safety, and change detection without redundant measures.
10. **Create a standardized reassessment protocol.** Preserve instructions, speed condition, device/orthosis, assistance, environment, scoring, and time point.

## Diagnostic special tests

Extract protocol, threshold/positive rule, intended role, reference standard, patient spectrum, verification/blinding, flow/timing, and analysis bias. Report sensitivity, specificity, LR+/LR−, and 95% intervals. Calculate post-test probability only from a defensible pretest probability. Use a test cluster only when that exact combination and decision rule were validated.

Do not ask the user to self-administer a risky test to exclude an emergency.

## Numeric guardrails

- “Validated” is insufficient; name the property, population, and study quality.
- Correlation is not agreement/reliability. Report ICC/kappa type/model, interval, retest timing, and stability.
- Interpret alpha/omega only after adequate dimensionality evidence.
- Distinguish measurement SEM from standard error of the mean.
- MDC/SDC addresses measurement error; MIC/MCID addresses importance. Neither is universally transferable.
- A distribution-only threshold is not patient importance; prefer a credible anchor-based estimate when available.
- Do not invent a “validated Turkish form.” Verify translation, cross-cultural validity, version, and permission.

## Output

1. Measurement purpose and construct
2. Patient/setting/language match and missing critical data
3. Outcome-measure comparison table
4. Separate diagnostic-test table when applicable
5. `recommended`, `conditional`, `insufficient evidence`, or `not recommended`
6. Baseline and reassessment protocol
7. Safety, feasibility, accessibility, license, and uncertainty
8. Direct sources

