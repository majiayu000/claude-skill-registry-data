---
name: roi-calculator-building
description: Build AI implementation ROI models for B2B enterprise sales. Use when creating ROI calculators, building business cases for AI adoption, estimating cost savings from automation, projecting revenue impact of AI features, or preparing financial justification for AI projects. Also triggers on ROI analysis, business case, cost-benefit analysis, payback period, total cost of ownership, AI investment justification, or value engineering. Even if someone says "prove the ROI of this AI project" or "build a business case" — use this skill.
allowed-tools: "Bash, Read, Write, Glob"
metadata:
  version: "1.0.0"
---

# ROI Calculator Building

Build defensible ROI models for AI/ML implementations targeting B2B enterprise clients.

<intake>

**When to use:** Building financial justification for AI projects, creating client-facing ROI calculators, estimating automation cost savings, or preparing business cases for executive approval.

| User Says | Route To |
|-----------|----------|
| "Build an ROI calculator" / "prove the value" / "business case" | `workflows/build-roi-model.md` |
| "What metrics" / "how to measure" / "KPIs" | `references/roi-frameworks.md` |
| "Template" / "starting point" / "spreadsheet model" | `assets/roi-model-template.md` |

</intake>

<quality_gates>

ROI model is complete when:

- [ ] Current state costs documented (labor, tools, error rates, cycle time)
- [ ] Future state projections modeled (with AI implementation)
- [ ] Implementation costs captured (licensing, integration, training, maintenance)
- [ ] Payback period calculated (months to break even)
- [ ] 3-year TCO comparison produced (current vs. AI-augmented)
- [ ] Sensitivity analysis included (optimistic, expected, conservative)
- [ ] Assumptions explicitly stated and defensible
- [ ] Non-financial benefits listed (quality, speed, scalability, employee satisfaction)

</quality_gates>

<reference_index>

| Workflow | Purpose | When to Read |
|----------|---------|--------------|
| `workflows/build-roi-model.md` | Step-by-step: current state → future state → costs → payback → sensitivity | Building any ROI calculator |

| Reference | Purpose | When to Read |
|-----------|---------|--------------|
| `references/roi-frameworks.md` | ROI metrics by use case, benchmark data, common pitfalls | Selecting the right metrics and avoiding overclaiming |

| Asset | Purpose | When to Use |
|-------|---------|-------------|
| `assets/roi-model-template.md` | Reusable ROI model structure with formulas and example values | Starting any new ROI calculator |

</reference_index>

<quick_reference>

**Example:** "Build a business case for automating our claims processing with AI" — follow `workflows/build-roi-model.md`, produce 3-year TCO comparison with payback period.

**Core ROI formula:**
```
ROI = (Net Benefits - Total Costs) / Total Costs × 100
Payback Period = Total Investment / Annual Net Benefits
3-Year NPV = Σ (Net Benefits_year / (1 + discount_rate)^year) - Initial Investment
```

**Environment note:** Configure financial parameters (discount rate, tax rate, growth assumptions) via environment variables when integrating ROI models into automated reporting pipelines.

</quick_reference>
