---
name: triage-issue
description: Investigate a bug, regression, or failing test without immediately implementing a fix. Use when the task is to reproduce an issue, isolate the failure surface, identify likely root cause, and recommend next actions.
allowed-tools: [Read, Grep, Glob, Bash, git]
---

# Triage Issue

Use this skill when the immediate goal is diagnosis, not implementation.

---

## Rules

- Reproduce before theorising whenever feasible
- Prefer the narrowest failing case available
- Separate confirmed facts from hypotheses
- Do not edit code unless the user explicitly asks to move from triage into fixing
- End with a concrete recommendation for next action

---

## Step 1 — Define the Symptom

Establish:

- Expected behavior
- Actual behavior
- Trigger conditions
- Scope of impact

If a failing test, stack trace, or error text exists, use it as the primary entry point.

---

## Step 2 — Reproduce and Narrow

Prefer one or more of:

```bash
rg -n "<error text|symbol|route|function>"
```

```bash
<targeted test or build command>
```

```bash
git diff --stat
```

Determine:

- Whether the failure is reproducible
- Which component owns the failing behavior
- Whether the issue appears new, pre-existing, or caused by recent changes

---

## Step 3 — Form the Diagnosis

Summarise:

- Confirmed failure surface
- Most likely root cause
- Confidence level
- Unknowns still blocking a definitive conclusion

If multiple causes remain plausible, rank them instead of forcing certainty.

---

## Output

Return:

- Reproduction status
- Suspected root cause
- Evidence
- Affected files or modules
- Recommended next step

---

## Done Criteria

The triage is complete only when:

- The symptom was scoped clearly
- Reproduction was attempted when feasible
- The likely root cause was narrowed to a concrete area
- The final response separates evidence from speculation
