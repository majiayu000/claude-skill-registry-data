---
name: technical-writing
description: Write technical design documents (design docs, specs, proposals). Use when creating design documents, technical specifications, project proposals, or similar structured technical content. Trigger on "design doc", "デザインドック", "設計書", "仕様書", "proposal".
---

# Technical Writing

## Workflow

1. **Context Gathering**: Understand the problem, stakeholders, constraints
2. **Structure Selection**: Choose appropriate template based on document type
3. **Data Collection**: Gather metrics, run queries, collect evidence
4. **Drafting**: Write section by section, starting with unknowns
5. **Verification**: Validate all data and queries are accurate

## Document Templates

See [references/templates.md](references/templates.md) for:

- Design Doc (問題解決型)
- Report Design (レポート設計型)

## Key Principles

### Data-Driven

- Include real data, not hypotheticals
- Show SQL queries with actual results
- Define measurable KPIs with baselines and targets

### Scope Clarity

- Explicit "スコープ外" section
- Document what you're NOT doing and why
- Prevents scope creep and sets expectations

### Problem First

- Start with the problem, not the solution
- Quantify the impact (件数, コスト, 時間)
- Make the "why" compelling before the "how"
