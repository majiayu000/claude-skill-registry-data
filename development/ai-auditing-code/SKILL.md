---
name: ai-auditing-code
description: Review DSPy code for correctness and best practices. Use when you want a code review of your DSPy program, need to check if your AI code follows best practices, want to find anti-patterns in your DSPy usage, or need a quality audit of your AI implementation. Also use for DSPy code review, is my DSPy code correct, review my AI code, best practices check, DSPy anti-patterns, code quality audit, am I using DSPy right, sanity check my AI code, peer review my DSPy program, does this follow DSPy conventions.
---

# Audit Your DSPy Code

**When NOT to use this skill:**

- Code is crashing or throwing errors -> use `/ai-fixing-errors` first
- Need to measure or improve accuracy -> use `/ai-improving-accuracy`
- Have not built anything yet -> use `/ai-kickoff` or `/ai-choosing-architecture`
- Want to learn a specific DSPy API -> use the matching `/dspy-*` skill

---

## Step 1: Ask 2 questions

Before reading any code, ask:

1. **Point me to the code** — which files contain your DSPy code?
2. **What are your concerns?** — general review, a specific worry, or a pre-launch check?

Do not proceed until you have answers to both.

---

## Step 2: Read the code

Read all DSPy-related files the user points you to. Build a mental model of:

- Signatures defined and their field names/types
- Modules defined and how they compose
- How `forward()` methods pass data between sub-modules
- Where data is loaded and how examples are constructed
- Whether a metric exists and how it is implemented
- Whether an optimizer is used and how it is called

---

## Step 3: Run the 7-category audit

For each category, check the items in [reference.md](reference.md). Mark each finding:

- **CRITICAL** — causes silent failures, wrong results, or data loss (e.g., missing `with_inputs()`, metric always returns `True`)
- **WARNING** — suboptimal but works (e.g., `Predict` where `ChainOfThought` would help, no error handling)
- **INFO** — style or convention suggestions (e.g., naming, file organization)

### Category 1: Signature Design

Check that field names are descriptive (not `output`, `result`, `text`), types are correct, complex outputs use Pydantic models, and ambiguous fields have a `desc=` argument.

### Category 2: Module Composition

Check that modules are registered in `__init__`, `forward()` passes sub-module outputs as typed fields (not strings), and there is no raw string manipulation of LM outputs.

### Category 3: Data Pipeline

Check that `with_inputs()` is called on every `dspy.Example`, a train/dev split exists, example field names match the signature, and data loading is reproducible (no random shuffles without a seed).

### Category 4: Metric Design

Check that the metric handles edge cases (empty strings, None), returns a `float` between 0 and 1 or a `bool`, accepts the `trace` parameter, and can be tested independently of the module.

### Category 5: Optimizer Usage

Check that the right optimizer is chosen for the dataset size, the trainset is large enough, the metric is passed correctly, and the optimized program is saved with `program.save()`.

### Category 6: Production Readiness

Check that LM calls are wrapped in error handling, timeouts are set, there is a fallback for LM failures, and costs have been estimated before deployment.

### Category 7: Anti-patterns

Check for f-string prompt construction instead of signatures, direct `lm()` calls instead of using modules, hardcoded prompt strings alongside DSPy code, and mixed raw API calls with DSPy modules.

---

## Step 4: Generate the findings report

After completing the audit, produce this report:

```
## DSPy Code Audit: [Project/Module Name]

### Summary
- X findings: Y critical, Z warnings, W info
- Overall assessment: [Ready for production / Needs fixes before production / Needs significant rework]

### Critical Findings
1. **[Category] — [Issue]**
   - File: path/to/file.py:line
   - Problem: ...
   - Fix: ...
   - Code:
     Before: <code>
     After:  <code>

### Warnings
1. **[Category] — [Issue]**
   - File: path/to/file.py:line
   - Problem: ...
   - Fix: ...

### Info
1. **[Category] — [Suggestion]**
   - ...

### Recommended Next Steps
1. Fix all critical findings
2. Address warnings in priority order
3. Run /ai-improving-accuracy to measure baseline quality after fixes
```

---

## Step 5: Offer to fix

After presenting the report, ask:

> "Would you like me to apply the critical and warning fixes directly to your code?"

If yes, make the fixes. Do not silently apply fixes during the audit itself.

---

## Gotchas

1. **Do not rewrite code during the audit.** Audit first, present findings, then fix on request. Silent refactoring while reviewing confuses users about what changed and why.

2. **Do not rate everything CRITICAL.** Reserve CRITICAL for things that cause silent failures, wrong results, or data loss. Suboptimal patterns are WARNING. Style issues are INFO.

3. **Do not audit accuracy instead of code.** This skill reviews code structure and patterns — not whether the AI produces correct answers. For accuracy measurement, send the user to `/ai-improving-accuracy`.

4. **Respect domain context.** A simple `Predict` module may be entirely correct for a simple task. Do not recommend `ChainOfThought` everywhere or assume complexity is always better.

5. **Do not suggest MIPROv2 for every finding.** Not every issue requires an optimizer-level fix. Many issues are plain code bugs that need to be corrected before any optimization makes sense.

---

## Additional resources

- Full 7-category checklist with code examples: [reference.md](reference.md)
- Worked audit examples (ticket classifier, RAG pipeline, content generator): [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Code is crashing?** Fix it first with `/ai-fixing-errors`
- **Measure accuracy after fixing** — see `/ai-improving-accuracy`
- **Plan your AI feature** — see `/ai-planning`
- **Pick the right DSPy pattern** — see `/ai-choosing-architecture`
- **Signature design patterns** — see `/dspy-signatures`
- **Module composition** — see `/dspy-modules`
- **Optimizer selection** — see `/dspy-optimizers`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
