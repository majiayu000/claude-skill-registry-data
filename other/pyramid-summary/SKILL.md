---
name: pyramid-summary
description: Use this skill to rewrite a completed investment analysis in pyramid-principle form with conclusion first, core reasons, evidence, valuation, risks, gates, and action framework. Trigger when the user asks for clearer structure, executive summary, or symbol-based output.
---

# Pyramid Summary Skill

## Purpose

Present the final investment analysis using the pyramid principle.

This skill transforms detailed analysis into a conclusion-first, structured, decision-oriented format.

## Trigger Conditions

Activate when:

- A final investment analysis is generated
- User asks for clearer structure
- User asks for pyramid principle output
- User wants easier-to-understand investment conclusion
- User wants symbols such as ✅ ❌ ⚠️ ➡️ 📌 🔹 🔸 💡

## Inputs

- Final view
- Business quality
- Valuation result summary
- Reverse DCF result
- Risk analysis
- Execution gate checklist
- Investor action framework
- Data provenance table

## Output Rules

1. Start with conclusion.
2. Use 3-5 core reasons.
3. Separate fact, interpretation, and action.
4. Use symbol system consistently.
5. Keep L1 output compact.
6. Put detailed tables after the conclusion.
7. Show blocked modules explicitly.
8. Do not invent new analysis.
9. Do not expose step-by-step valuation calculations by default. Show only valuation range, margin of safety, key assumptions, sensitivity summary, and blocked/usable status.
10. Put formulas, model input tables, derived metric tables, and calculation traces only in an optional appendix when explicitly requested.

## Default Sections

```markdown
## 📌 Executive Conclusion
## 🧭 Decision Snapshot
## 🔹 Core Thesis
## 📊 Key Evidence
## 🧮 Valuation Summary
## ⚠️ Risks
## ✅ Execution Gate Checklist
## 🧭 Investor Action Framework
## 🔍 Data Provenance
```

## Symbol Guide

- ✅ supportive / passed
- ❌ negative / failed
- ⚠️ risk / uncertainty
- ➡️ action / implication
- 📌 key conclusion
- 🔹 main point
- 🔸 detail
- 💡 interpretation
- 🧮 valuation
- 📊 data
- 🔍 source
- 🧭 action framework
