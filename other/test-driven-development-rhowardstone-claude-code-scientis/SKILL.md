---
name: test-driven-development
description: Use when implementing any feature, bugfix, experiment, or analysis - before writing implementation code or running experiments
---

# Validation-First Development

## Overview

Define success criteria first. Verify your validation catches problems. Then implement minimal solution.

**Core principle:** If you didn't verify your validation catches failures, you don't know if it validates the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**
- New features/experiments
- Bug fixes/anomaly investigations
- Refactoring/methodology improvements
- Behavior/hypothesis changes

**Exceptions (ask your human partner or RD):**
- Throwaway prototypes
- Generated code
- Configuration files
- Pure exploratory analysis (but then: throw away, restart with validation)

Thinking "skip validation-first just this once"? Stop. That's rationalization.

## The Iron Law

```
NO IMPLEMENTATION WITHOUT DEFINED VALIDATION CRITERIA FIRST
```

Write code/run experiments before defining success criteria? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing validation
- Don't look at it
- Delete means delete

Implement fresh from validation criteria. Period.

## Red-Green-Refactor (Hypothesis-Test-Improve)

### For Software: Classic TDD

```
RED    → Write failing test
GREEN  → Minimal code to pass
REFACTOR → Clean up, stay green
```

### For Research: Validation-First

```
DEFINE   → State expected outcome and validation criteria
VERIFY   → Confirm validation would catch failure
EXECUTE  → Minimal experiment/analysis to produce result
VALIDATE → Check result against criteria
IMPROVE  → Refine methodology, stay valid
```

---

## Software: Red-Green-Refactor

### RED - Write Failing Test

Write one minimal test showing what should happen.

**Good:**
```python
def test_retries_failed_operations_3_times():
    attempts = []
    def operation():
        attempts.append(1)
        if len(attempts) < 3:
            raise Exception('fail')
        return 'success'

    result = retry_operation(operation)

    assert result == 'success'
    assert len(attempts) == 3
```
Clear name, tests real behavior, one thing.

**Bad:**
```python
def test_retry_works():
    mock = Mock(side_effect=[Exception(), Exception(), 'success'])
    retry_operation(mock)
    assert mock.call_count == 3
```
Vague name, tests mock not code.

**Requirements:**
- One behavior
- Clear name
- Real code (no mocks unless unavoidable)

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
pytest tests/path/test.py::test_name -v
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### GREEN - Minimal Code

Write simplest code to pass the test. Nothing more.

Don't add features, refactor other code, or "improve" beyond the test.

### Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
pytest tests/path/test.py -v
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

### REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

---

## Research: Validation-First Development

### DEFINE - State Expected Outcome

Before running any experiment or analysis, explicitly state:

**Good:**
```markdown
## Expected Outcome
- Metric: Correlation between treatment and response
- Success: r > 0.3 with p < 0.05
- Failure: r < 0.1 or p > 0.1
- Anomaly: r > 0.9 (suspicious, check for confounds)
```

**Bad:**
```markdown
## Expected Outcome
- We expect to see an effect
- Results should be significant
```

**Requirements:**
- Specific measurable criteria
- Explicit success threshold
- Explicit failure/null criteria
- What would indicate problems (anomalies, data quality issues)

### VERIFY - Confirm Validation Works

**MANDATORY. Never skip.**

Before running your experiment, verify your validation criteria would catch problems:

1. **What would a null result look like?** (e.g., r ≈ 0, p > 0.5)
2. **What would a confounded result look like?** (e.g., perfect correlation due to batch effects)
3. **What would bad data look like?** (e.g., missing values, outliers, wrong format)

If you can't describe what failure looks like, your validation is worthless.

### EXECUTE - Minimal Experiment/Analysis

Run the simplest version that tests your hypothesis. Nothing more.

**Good:**
```python
# Minimal analysis
df = pd.read_csv("data.csv")
r, p = stats.pearsonr(df["treatment"], df["response"])
print(f"r={r:.3f}, p={p:.4f}")
```

**Bad:**
```python
# Over-engineered before knowing if basic approach works
class CorrelationAnalyzer:
    def __init__(self, config, logger, cache, ...):
        # YAGNI
```

Don't add features, optimize, or expand scope beyond the immediate test.

### VALIDATE - Check Against Criteria

**MANDATORY.**

Compare actual result to defined criteria:
- Does it meet success threshold?
- Does it fall in failure range?
- Are there any anomaly flags?

**Result meets criteria?** Proceed to improve.

**Result in failure range?** This is valid information. Document and report.

**Result triggers anomalies?** Investigate before trusting.

### IMPROVE - Refine Methodology

Only after validation passes:
- Improve statistical power
- Add additional checks
- Clean up code
- Expand scope

Keep validation passing. Don't change hypothesis after seeing data.

---

## Why Order Matters

**"I'll add validation after to verify it works"**

Validation added after passes immediately. Passing immediately proves nothing:
- Might validate wrong thing
- Might validate implementation artifacts, not real effects
- Might miss edge cases you forgot
- You never saw it catch a problem

Validation-first forces you to see it fail, proving it actually validates something.

**"I already manually checked the results"**

Manual checking is ad-hoc. You think you checked everything but:
- No record of what you checked
- Can't re-run when data changes
- Easy to forget checks under pressure
- "It looked right" ≠ systematic validation

Defined criteria are systematic. They check the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:
- Delete and redo with validation-first (X more hours, high confidence)
- Keep it and add validation after (30 min, low confidence, likely problems)

The "waste" is keeping results you can't trust.

**"This is exploratory, validation doesn't apply"**

Exploratory is fine. But:
- Treat exploratory as throwaway
- When you find something interesting, STOP
- Define validation criteria for the finding
- Re-run with validation-first to confirm

"I explored, found X, and reported X" without validation is unreliable.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to validate" | Simple things break. Validation takes 30 seconds. |
| "I'll validate after" | Validation passing immediately proves nothing. |
| "Already manually checked" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified results is technical debt. |
| "This is exploratory" | Fine. Throw away exploration, restart with validation-first for anything you report. |
| "Validation hard = unclear requirements" | Listen to difficulty. Hard to validate = requirements unclear. |
| "Validation will slow me down" | Validation-first faster than debugging bad results. |
| "I already know this works" | If you know, validation takes 30 seconds. If you're wrong, validation saves you. |

## Red Flags - STOP and Start Over

- Implementation before validation criteria defined
- Validation added after implementation
- Validation passes immediately without ever failing
- Can't explain what failure would look like
- Validation added "later"
- Rationalizing "just this once"
- "I already manually checked it"
- "Validation after achieves the same purpose"
- "Keep as reference" or "adapt existing code/results"
- "Already spent X hours, deleting is wasteful"
- "This is different because..."

**All of these mean: Delete implementation. Start over with validation-first.**

## Example: Bug Fix (Software)

**Bug:** Empty email accepted

**RED**
```python
def test_rejects_empty_email():
    result = submit_form({"email": ""})
    assert result["error"] == "Email required"
```

**Verify RED**
```bash
$ pytest test_form.py::test_rejects_empty_email -v
FAIL: expected 'Email required', got None
```

**GREEN**
```python
def submit_form(data):
    if not data.get("email", "").strip():
        return {"error": "Email required"}
    # ...
```

**Verify GREEN**
```bash
$ pytest test_form.py -v
PASS
```

## Example: Analysis (Research)

**Question:** Is gene X expression correlated with treatment response?

**DEFINE**
```markdown
## Expected Outcome
- Metric: Spearman correlation between gene X expression and response score
- Success: rho > 0.3, p < 0.05, n > 30
- Failure: |rho| < 0.1 or p > 0.1
- Anomaly: rho > 0.9 (check for technical artifacts)
```

**VERIFY**
- Null result: rho ≈ 0 with high p-value (validates we can detect no effect)
- Bad data: Missing values in response score (validates we check data quality)
- Confound: Perfect correlation with batch (validates we check for artifacts)

**EXECUTE**
```python
df = pd.read_csv("expression_data.csv")
rho, p = stats.spearmanr(df["geneX"], df["response"])
n = len(df)
print(f"rho={rho:.3f}, p={p:.4f}, n={n}")
```

**VALIDATE**
- Result: rho=0.42, p=0.003, n=45
- Meets success criteria? Yes (rho > 0.3, p < 0.05, n > 30)
- Anomaly flags? No (rho not suspiciously high)

**IMPROVE**
- Add confidence intervals
- Check for outliers
- Visualize relationship

## Verification Checklist

Before marking work complete:

**Software:**
- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)

**Research:**
- [ ] Defined explicit success/failure criteria before executing
- [ ] Verified validation would catch known failure modes
- [ ] Executed minimal analysis/experiment
- [ ] Compared result to defined criteria
- [ ] Documented outcome (success, failure, or anomaly)
- [ ] Did NOT change criteria after seeing results

Can't check all boxes? You skipped validation-first. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to validate | Write wished-for outcome. Ask RD or human partner. |
| Validation too complicated | Requirements too complicated. Simplify question. |
| Must mock/simulate everything | System too coupled. Isolate component under test. |
| Setup huge | Extract helpers. Still complex? Simplify design. |

## Final Rule

```
Implementation/results → validation criteria existed and were verified first
Otherwise → not validation-first development
```

No exceptions without your human partner's (or RD's) permission.
