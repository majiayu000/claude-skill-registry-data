---
name: experiment-results-interpreter
description: "Interpret A/B test results in plain language and get a ship/rollback/extend recommendation with a stakeholder summary. Use when you have experiment results from any analytics tool and need a clear go/no-go decision. Triggers: 'interpret experiment results', 'read my A/B test results', 'should I ship this experiment', 'интерпретируй результаты эксперимента', 'помоги прочитать результаты A/B теста'."
version: 1.0.0
---

# Experiment Results Interpreter

This skill takes A/B test results — pasted from an analytics dashboard or described in plain text — and returns a plain-language significance assessment, a ship/rollback/extend recommendation with a documented rationale, and a ready-to-paste stakeholder summary. No statistics background or database access required.

**Input:**
- Test description: hypothesis, variant names, primary metric, test duration
- Results: pre-computed (p-value or confidence interval + lift) or raw numbers (visitors and conversions per variant)
- Optional: guardrail metrics (secondary metrics to protect)

**Output:**
- Test Summary, Results Interpretation, Recommendation with rationale, Draft Stakeholder Summary

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that the user has provided at minimum:
   - A primary metric (what was being measured)
   - At least one result value (conversion rate, lift, p-value, or raw visitor/conversion counts)

2. If the primary metric is missing: ask "What metric was this experiment measuring? (e.g., signup rate, checkout conversion, 7-day retention)"
   - Exception: if the user refers to "primary metric" or "main metric" without naming it but does provide result values (lift %, p-value, or counts) — proceed using "primary metric" as the metric name placeholder rather than blocking. Name it "primary metric" in the output.

3. If no results data at all: ask for one of:
   - p-value or confidence interval from their analytics tool
   - Control and treatment: visitors and conversions (to compute significance here)

4. If statistical data is present but no test description: proceed — infer variant names as "Control" and "Treatment" if not specified.

5. Do not ask more than one clarifying question at a time. Prioritise the most critical missing piece.

### Step 2: Parse Test Setup

Extract and structure the following from the user's input:

- **Test name / feature:** what feature or change was tested
- **Hypothesis:** what improvement was expected (infer if not stated)
- **Variants:** control vs. treatment(s) — names and what changed
- **Primary metric:** the single metric that determines success
- **Guardrail metrics:** secondary metrics that must not degrade (if provided)
- **Duration:** how long the test ran
- **Sample size:** visitors per variant (if provided)

If multiple primary metrics are mentioned: ask the user to designate one as the primary decision metric before proceeding.

### Step 3: Assess Statistical Significance

**If p-value is provided:**
- p < 0.05 → statistically significant
- 0.05 ≤ p < 0.10 → borderline (leaning significant but uncertain)
- p ≥ 0.10 → not statistically significant

**If confidence interval (CI) is provided:**
- CI does not include 0 (or 1 for ratios) → statistically significant
- CI barely excludes 0 → borderline
- CI includes 0 → not statistically significant

**If only raw counts are provided (visitors and conversions per variant):**
Use the two-proportion z-test formula to compute p-value:

1. p1 = conversions_control / visitors_control
2. p2 = conversions_treatment / visitors_treatment
3. p_pool = (conversions_control + conversions_treatment) / (visitors_control + visitors_treatment)
4. SE = sqrt(p_pool × (1 − p_pool) × (1/visitors_control + 1/visitors_treatment))
5. z = (p2 − p1) / SE
6. Interpret: |z| > 1.96 → significant (p < 0.05); |z| > 1.645 → borderline (p < 0.10)

Show the computed lift: ((p2 − p1) / p1) × 100% rounded to 1 decimal.

**Flag maturation risk:**
- If test ran fewer than 7 days: add a warning that weekly seasonality may not be captured, recommend extending regardless of significance result.

**Flag insufficient sample:**
- If fewer than 100 conversions per variant: note that results may be unreliable due to small sample; recommend extending.

### Step 4: Generate Recommendation

Apply this decision matrix:

| Significance | Direction | Guardrail | Recommendation |
|---|---|---|---|
| Significant | Positive lift | OK or not measured | **Ship** |
| Significant | Negative lift | Any | **Rollback** |
| Significant | Positive lift | Degraded | **Hold** — investigate guardrail conflict before shipping |
| Borderline | Any | OK | **Extend** — collect more data |
| Not significant | Any | Any | **Inconclusive** — do not ship |
| Insufficient sample | N/A | N/A | **Extend** — sample too small |
| Maturation risk | Any | Any | **Extend** — test ran less than 7 days |

Write the recommendation with exactly 3 bullet points explaining the rationale:
- What the data shows
- Why this recommendation follows from the data
- What the next concrete action is

### Step 5: Draft Stakeholder Summary

Write 3–4 sentences suitable for a Slack message or email update. Requirements:
- No p-values or statistical terms without plain-language explanation
- Include: what was tested, what the result was, what the recommendation is, and what happens next
- Use concrete numbers (lift %, sample size) — do not leave placeholder values blank
- Tone: factual and direct, not promotional

---

## Output Format

Respond with four clearly labelled sections:

```
## Test Summary
[Structured recap: test name/feature, hypothesis, variants, primary metric, duration, sample size]

## Results Interpretation
[Plain-language significance assessment with explanation. Show lift % and p-value/CI if available. Flag any maturation or sample size concerns.]

## Recommendation: [SHIP / ROLLBACK / EXTEND / HOLD / INCONCLUSIVE]
- [What the data shows]
- [Why this recommendation follows]
- [Next concrete action]

## Draft Stakeholder Summary
[3–4 sentences, copy-paste ready]
```

---

## Guardrails

- Do not make a Ship recommendation if guardrail metrics are degraded without flagging the conflict.
- Do not claim statistical significance without showing the basis (p-value, CI, or z-test computation).
- Do not skip the Stakeholder Summary even if the recommendation is Rollback or Inconclusive.
- If test results come from multiple tools with conflicting numbers: ask the user to clarify which source to treat as authoritative before proceeding.
- Never recommend a decision based on absolute numbers alone without normalising by sample size (conversion rates, not raw counts).
