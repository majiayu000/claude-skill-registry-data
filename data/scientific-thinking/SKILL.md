---
name: scientific-thinking
description: 'Forces hypothesis-driven scientific reasoning for complex problems. Use when debugging strange behavior, investigating root causes, designing architecture, performing complex refactoring, or when initial attempts have failed. Activates when facing problems that require systematic investigation rather than quick fixes.'
user-invocable: true
---

# Scientific Thinking Mode

**Workflow Reference**: See [Investigation Workflow](./../knowledge/workflow-diagrams/investigation-workflow.md) for the complete hypothesis-driven scientific method flow.

You are entering **Deep Reasoning Mode**. Activate this for: **Debugging**, **Architecture**, **Complex Refactoring**, or **Investigation**.

Do NOT use for trivial tasks (typo fixes, simple additions).

---

## 1. Observation

List ONLY factual observations (logs, errors, file contents, test output).

**No interpretations yet.**

```text
OBSERVED:
- [Exact error message]
- [File:line reference]
- [Actual behavior vs expected]
```

---

## 2. Hypothesis Formulation

- **H₀ (Null Hypothesis):** The system is working as intended; the issue is environmental, configuration, or user error.
- **Hₐ (Alternative Hypothesis):** The issue is caused by [Specific Cause in Code/Logic].

```text
H₀: [State null hypothesis]
Hₐ: [State alternative hypothesis with specific mechanism]
```

---

## 3. Prediction

"If Hₐ is true, then observing [Component X] will reveal [Y]."

```text
PREDICTION: If Hₐ, then [specific observable outcome]
```

---

## 4. Experiment Plan (Tree-of-Thought)

Design tests to falsify H₀. Multiple paths increase confidence.

```text
EXPERIMENT PLAN:
- Path A: Check [X]. Expected if Hₐ: [Y]. Expected if H₀: [Z].
- Path B: Check [W]. Expected if Hₐ: [Q]. Expected if H₀: [R].
```

---

## 5. Execution Control

Before running experiments:

- Are there confounding variables (caching, environment vars, stale state)?
- How will you isolate them?
- What is your rollback plan if experiments have side effects?

```text
CONFOUNDS:
- [List potential confounds]
- [Isolation method for each]
```

---

## 6. Execute and Record

**PROCEED:** Execute the Experiment Plan using available tools.

Record results factually:

```text
RESULTS:
- Path A result: [Actual observation]
- Path B result: [Actual observation]
```

---

## 7. Conclusion

Based on evidence:

- **Reject H₀** if predictions for Hₐ were confirmed
- **Fail to Reject H₀** if predictions were not confirmed (investigate further or revise hypothesis)

```text
CONCLUSION: [Reject H₀ / Fail to Reject H₀]
EVIDENCE: [Cite specific observations that support conclusion]
NEXT STEP: [Action based on conclusion]
```

---

## When to Use This Skill

| Situation                             | Use Scientific Thinking? |
| ------------------------------------- | ------------------------ |
| Bug with unknown cause                | YES                      |
| Architecture decision with trade-offs | YES                      |
| Refactoring with unclear scope        | YES                      |
| Strange/intermittent behavior         | YES                      |
| Simple typo fix                       | NO                       |
| Adding a straightforward feature      | NO                       |
| Following explicit instructions       | NO                       |
