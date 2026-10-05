---
name: mindmap-summary
description: Use this skill to compress a completed investment analysis into a mind-map-friendly summary. Trigger when the user asks for a mind map, Mermaid mindmap, ASCII tree, visual structure, or compact executive summary of an existing report.
---

# Mind Map Summary Skill

## Purpose

Convert the final investment analysis into a compact mind-map-friendly representation.

## Trigger Conditions

Activate when:

- A stock analysis is completed
- A final report is generated
- User asks for a visual / structured summary
- User wants a mind-map-like output
- A quick executive summary is needed

## Inputs

- Final view
- Company snapshot
- Business quality assessment
- Valuation outputs
- Reverse DCF result or blocker
- Risk analysis
- Execution gate checklist
- Investor action framework
- Monitoring points

## Output Formats

Produce at least one of:

1. Nested bullet mind map
2. ASCII tree
3. Mermaid mindmap block

Preferred default:

- Markdown nested bullets for universal compatibility
- Mermaid block as optional extra

## Hard Rule

The mind map must not invent new conclusions.
It must compress the existing analysis only.

If a module is blocked in the main report, the mind map must show it as blocked.

## Output Template

```markdown
## Mind Map Summary

- [Company / Ticker]
  - Company Snapshot
  - Final View
  - Business Quality
  - Valuation
  - Reverse DCF / Expectations
  - Risks
  - Execution Gates
  - Investor Action Framework
  - Monitoring Points
```
