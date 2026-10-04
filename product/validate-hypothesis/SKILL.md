---
name: validate-hypothesis
description: Turn a product assumption into a testable hypothesis and validation plan covering the riskiest assumption, cheapest test, success and kill criteria set in advance, A/B sample size, and a results readout. Use before investing in a feature or when a team disagrees about what users want.
---

# Validate a Hypothesis

Find the belief the plan depends on most, then design the cheapest test that could prove it wrong, with the pass/fail line drawn before any data arrives.

## Reasoning Framework

Most product bets fail on an untested assumption, not on execution. Writing the hypothesis and the kill criteria before the test prevents motivated reasoning afterward, when everyone wants the result to mean yes. The cheapest test that can change your mind wins. Experiment math (sample size, duration, significance) is deterministic, so `scripts/experiment_calc.py` does it instead of the model.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Hypothesis card | Markdown (template below) | Team |
| Validation plan | Method, criteria, sample, timeline, owner | Team, stakeholders |
| Results readout | Results against the pre-set criteria, and the decision | Team, leadership |

## When to Use

- Before committing engineering time to an idea
- The team disagrees about what users want or how they will behave
- A prioritization input (confidence) is low and matters
- Planning an A/B test and you need the sample size and duration

## When NOT to Use

- Open-ended discovery with no specific belief yet: use `question-storming` or `create-user-interview`
- Choosing among many validated options: use `prioritize-features`

## Inputs

1. **The belief or idea**, in the user's words.
2. **The decision it informs**: what we do differently if it's true versus false.
3. **Target users** and how to reach them.
4. **Existing evidence**: data, feedback, research.
5. **Resources**: time, traffic, budget, and who can run the test.
6. **Baseline metrics**, for quantitative tests (for example the current conversion rate).

## Steps

1. **List the assumptions** behind the idea across four risks: value (will they want it?), usability (can they use it?), feasibility (can we build it?), and viability (does it work for the business?).
2. **Pick the riskiest**: highest impact if wrong and least evidence. Test that one first.
3. **Write the hypothesis card:**
   > We believe **[change]** for **[users]** will result in **[outcome]** because **[evidence]**.
   > We're right if **[signal]** reaches **[threshold]** within **[time]**.
   > We stop if **[signal]** is below **[kill threshold]**.
4. **Choose the cheapest method that can disprove it**, going up this ladder only as needed: existing data or desk research → customer interviews (`create-user-interview`) → fake door or painted door → concierge or Wizard of Oz → prototype usability test → A/B test or holdout. Qualitative methods answer why and whether; quantitative methods answer how much.
5. **Set criteria and the decision rule now**: persevere, pivot, or stop. Qualitative criteria must be countable too (for example "at least 6 of 8 participants describe this problem unprompted, from the last month").
6. **Size quantitative tests (script):**
   ```bash
   python3 scripts/experiment_calc.py sample-size --baseline 0.12 --mde 10% --daily-traffic 4000
   python3 scripts/experiment_calc.py sample-size-mean --sd 42 --mde 5
   ```
   If the duration is impractical, detect a bigger effect, pick a more sensitive metric, or switch to a qualitative method. Add one or two guardrail metrics.
7. **Plan logistics**: owner, dates, participants or traffic, instrumentation, and ethics (consent, and fake doors that tell the truth: "coming soon", no charge).
8. **Read out the results** against the pre-set criteria:
   ```bash
   python3 scripts/experiment_calc.py significance --control 120/1000 --variant 150/1000
   ```
   State the decision, what you learned, and the next riskiest assumption. Inconclusive is a valid result. Report it as inconclusive.

## Readout Template

```markdown
# Readout: [Hypothesis]
**Test:** [method], [dates], [n] · **Criteria set on:** [date]
**Result:** [metric] = [value] vs threshold [x] → [met / not met / inconclusive]
**Decision:** [persevere / pivot / stop], because [..]
**Learned:** [..] · **Next assumption to test:** [..]
```

## Examples

- "I think admins want scheduled exports." Riskiest assumption: they export on a regular cadence today. Test: 8 interviews plus a fake-door "Schedule" button with an honest "coming soon" message. Pass line: 5% click-through and at least 5 of 8 interviewees describe a weekly export.
- "Will the new onboarding checklist lift activation from 12%?" Size the A/B test for a 10% relative lift: about 12,000 users per variant, roughly a week at 4,000 eligible users a day, so run a full week. Set a support-ticket guardrail.

## Guardrails

- Criteria before data. Never move the threshold after seeing results.
- No peeking: fix the sample size in advance; stopping when p first dips below alpha inflates false positives.
- Correlation in existing data is not causation. Say which you have.
- Small qualitative studies are directional. Report "5 of 8", not "63%".
- Keep participant personal data out of plans and readouts.
- A disproved hypothesis is a successful test. It saved the build.

## Related Skills

- `create-user-interview` and `analyze-user-interview`: qualitative tests
- `analyze-user-feedback`: existing evidence
- `prioritize-features`: feeds confidence back into the ranking
- `decision-brief`: present the persevere, pivot, or stop decision
- `library/lenny-podcast/lenny-problem-definition/SKILL.md` and `library/lenny-podcast/lenny-usability-testing/SKILL.md`: deeper playbooks
