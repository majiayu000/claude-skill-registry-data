---
name: facilitating-ai-workshops
description: >
  Facilitates AI enablement workshops and consulting exercises that move
  stakeholders from abstract AI concepts to measurable business outcomes.
  Activates when running an AI workshop, facilitating AI adoption sessions,
  running consulting exercises, helping teams identify AI use cases, mapping
  AI to business KPIs, running a friction audit, building an AI risk matrix,
  outcome-first AI planning, AI readiness workshop, value stream mapping for
  AI, guardrail matrix, trade-off matrix, AI friction heatmap, reverse menu
  mapping, KPI-to-AI mapping, HITL architecture, workshop facilitation, AI
  strategy session, AI discovery exercise, stakeholder AI alignment, or any
  request to help a team figure out where and how to adopt AI.
version: "1.0.0"
---

<essential_principles>
## How This Skill Works

Three consulting exercises that move any audience from "we should do AI" to a prioritized, risk-mapped, KPI-anchored roadmap. Each exercise produces a concrete artifact. Outputs chain: Exercise 1 feeds Exercise 2 feeds Exercise 3.

### 1. Outcome Before Tool
No one names an AI tool until a KPI metric is on paper. This is the single most important rule across all three exercises. Enforce it.

### 2. Artifacts Over Discussion
Every exercise ends with a concrete, fillable artifact — not a summary, not bullet points. The Outcome Ledger, Friction Heatmap, and Trade-Off Balance Sheet are the deliverables.

### 3. Named Owners
Every HITL checkpoint requires a named human owner. "Human review" is not an owner. Push for a person.
</essential_principles>

<intake>
What do you want to run?

1. **Reverse Menu Mapping** — strategic alignment, KPI-to-AI mapping (leaders, PMs)
2. **AI Friction Audit** — bottleneck discovery, process workflow (ops, analysts)
3. **Guardrail & Trade-Off Matrix** — risk governance, HITL architecture (security, legal, platform eng)
4. **Full workshop** — all three in sequence, outputs chain
5. **Just the templates** — printable worksheets only, no facilitation

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "reverse menu", "outcome", "KPI", "backlog", "leaders" | `workflows/reverse-menu-mapping.md` |
| 2, "friction", "audit", "ops", "process", "heatmap", "bottleneck" | `workflows/friction-audit.md` |
| 3, "guardrail", "risk", "trade-off", "HITL", "security", "legal" | `workflows/guardrail-matrix.md` |
| 4, "full", "all three", "sequence", "complete", "whole" | `workflows/full-workshop.md` |
| 5, "template", "worksheet", "print", "just the" | Deliver `assets/workshop-templates.html` directly |
| Clear intent without menu selection | Route to matching workflow based on keywords above |

**After reading the workflow, follow it exactly.**
</routing>

<audience_calibration>
| Maturity Level | Starting Point | Pacing |
|---|---|---|
| Early-stage (AI = buzzword) | Exercise 1 | Slow — 60%+ of time on metric definition |
| Process-aware (ops-led) | Exercise 2 | Fast — they know their pain points |
| Governance-mature (risk-aware) | Exercise 3 | Fast — goes straight to architecture |
| Mixed room | Full workshop | ~45 min per exercise |
</audience_calibration>

<reference_index>
All templates and domain knowledge in `references/`:
- **exercises.md** — full exercise descriptions, facilitation notes, red flags to catch
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| reverse-menu-mapping.md | Run Exercise 1: KPI-first AI backlog |
| friction-audit.md | Run Exercise 2: Green/Red workflow timeline + heatmap |
| guardrail-matrix.md | Run Exercise 3: Trade-off balance sheet + HITL checkpoints |
| full-workshop.md | Run all three in sequence with chained outputs |
</workflows_index>
