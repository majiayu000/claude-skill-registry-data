---
name: case-study
description: "Route and produce evidence-backed product or design case studies from raw notes, research, screenshots, specifications, decision logs, architecture, metrics, and project artifacts. Use when the user invokes /case-study, asks to write, critique, structure, or polish a portfolio case study, needs to explain a complex design project, or needs an AI-agent case study covering autonomy, human oversight, telemetry, trust, latency, failures, and recovery."
---

# Case Study Dispatcher

Resolve the project, intended reader, available evidence, and requested format. Mark missing facts; never fill them with plausible fiction.

## Route

| Need | Load |
|---|---|
| Flat timeline or missing story | `narrative-arc-builder` |
| Screens without rationale | `extract-design-rationale` |
| Architecture shapes the experience | `system-architecture-translator` |
| Imprecise or inflated technical copy | `technical-microcopy-editor` |
| Dense, repetitive, slow-to-scan draft | `enforce-scannable-density` |
| AI agent or probabilistic system | `ai-agent-case-study` plus the applicable skills above |
| Complex multichannel or branching journey | `case-study-storytelling` and `case-study-story-map` |
| Deep stakeholder decision narrative | `case-study-design-decisions` |
| General long-form drafting and finishing | `case-study-writing` |

Load the smallest set that covers the evidence and requested deliverable. When the user asks for a complete build from raw artifacts, apply the automated pipeline below as one workflow, not as separate reports.

## Automated pipeline

```text
Raw logs / notes / code / research
  → narrative-arc-builder
  → system-architecture-translator (when architecture affects the experience)
  → extract-design-rationale
  → technical-microcopy-editor
  → enforce-scannable-density
  → quality gate
```

For an AI-agent case study, apply `ai-agent-case-study` across every stage. It governs autonomy, permission, observability, uncertainty, intervention, and recovery; it is not an extra standalone report.

## Evidence contract

Label every substantive claim:

- **Executed** — supported by a test, trace, artifact, or measured output.
- **Observed** — supported by research notes, usability observations, or recorded behavior.
- **Reported** — attributed to a stakeholder, participant, or project record.
- **Proposed** — a recommendation, hypothesis, future metric, or unverified narrative bridge.

Never convert a proposal into an outcome. Never invent research, metrics, quotes, responsibilities, constraints, alternatives, or impact. Use `[evidence needed: …]` where the story has a material gap.

## Workflow

1. Inventory source artifacts and create an evidence ledger.
2. State the protagonist, goal, inciting problem, constraints, pivotal decisions, delivered change, and measured result.
3. Select the smallest route above.
4. Build the narrative arc before drafting sections.
5. Translate consequential system behavior into visible states, controls, and recovery.
6. Extract the decision rationale and rejected alternatives.
7. For AI systems, document supervision and uncertainty before visual polish.
8. Run the accuracy, clarity, and brevity edit.
9. Enforce scannable density without deleting evidence.
10. Run the quality gate in `references/quality-gate.md`.
11. Deliver one clean case study plus a short unresolved-evidence list.

Use `assets/case-study-template.md` when creating a new Markdown artifact.

## Done

A case study is ready only when a skeptical reader can answer:

- What changed, for whom, and under what constraints?
- What did the designer actually own?
- Which decisions were difficult, what alternatives existed, and why were they chosen?
- What evidence supports the outcome?
- What remains unknown, limited, or confidential?
- For AI agents: where does autonomy stop, how does a human intervene, what is observable, and how does failure recover?
