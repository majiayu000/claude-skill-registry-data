---
metadata:
  name: assess-quality
  class: toolboxes
  type: skill
  version: '1.0'
  schema_version: '1.0'
  freshness:
    status: active
    sync_count: 0
    last_synced_by: daemon
    last_synced: '2026-06-27T00:00:00'
credentials:
  maturity: "functional"
  description: "Assess outcomes and quality of executed steps against expected results."
  when_to_use: "Use this skill when the task involves assess quality"
  triggers: ["evaluate", "assess quality", "does it work", "test", "validate result", "review output", "qa"]
  inputs: ["execution output", "expected results", "success criteria", "context"]
  outputs: ["quality verdict", "score", "discrepancy list", "actionable feedback", "pass/fail gate"]
---

# Assess Quality

This skill allows the agent to rigorously evaluate the outcome of any executed step, comparing actual results against defined success criteria and producing a structured verdict with actionable feedback.

## Steps

1. **Establish success criteria.** Before evaluating, explicitly define what "good" looks like. If criteria are not provided, derive them from the goal context.
2. **Gather the output fresh.** Read or receive the actual execution output — do not evaluate from memory.
3. **Score against each criterion.** For each criterion, assign: ✅ Pass | ⚠️ Partial | ❌ Fail.
4. **List discrepancies.** For every Partial or Fail, describe exactly what is wrong and why it matters.
5. **Determine the overall verdict.** 
   - All Pass → **APPROVED** 
   - Any Partial (no Fail) → **CONDITIONAL** (list required fixes)
   - Any Fail → **REJECTED** (must be reworked before proceeding)
6. **Generate feedback.** For each non-Pass item, produce a specific, actionable fix instruction — not vague suggestions.
7. **Output** the full assessment.

## Output Format

```yaml
quality_assessment:
  subject: "<what was evaluated>"
  criteria_scores:
    - criterion: "<criterion name>"
      verdict: "pass | partial | fail"
      notes: "<observation>"
  overall_verdict: "APPROVED | CONDITIONAL | REJECTED"
  discrepancies:
    - item: "<what failed>"
      fix: "<specific action to resolve>"
  feedback_summary: "<one paragraph summary>"
```

## Notes
- Never emit APPROVED without checking every criterion.
- If success criteria are absent, generate them from context before scoring — never evaluate blindly.
- Pair with the `planning` toolbox to generate a remediation plan when verdict is REJECTED.
