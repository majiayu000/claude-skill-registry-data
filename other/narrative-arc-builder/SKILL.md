---
name: narrative-arc-builder
description: "Map raw project timelines, notes, research, and metrics into a five-stage evidence-backed narrative arc for a design case study. Use when a draft reads like a chronological task list, lacks tension or a turning point, makes the designer or product the hero, buries the pivotal decision, or needs a clear context-friction-complexity-breakthrough-impact structure."
---

# Narrative Arc Builder

Turn chronology into causal structure. Keep the user or operator as protagonist and the product, designer, and AI agent as supporting forces. This is a five-stage compression of Donna Lichaw's seven-part narrative arc (*The User's Journey*, Rosenfeld Media, 2016) — Exposition, Inciting Incident, Rising Action, Crisis, Climax/Resolution, Falling Action, End. Read `references/five-stage-arc.md` for the exact stage mapping.

## Workflow

1. Extract the protagonist, baseline, goal, inciting friction, constraints, evidence, alternatives, pivotal decision, changed state, and measured result.
2. Map only supported material into:
   1. Context and baseline
   2. Friction or inciting incident
   3. Rising complexity and trade-offs
   4. Systemic breakthrough or pivotal learning
   5. Quantifiable aftermath and remaining limits
3. Identify the climax as the moment value, risk reduction, or decisive learning became visible—not automatically the launch.
4. Place research and process steps where they changed a decision.
5. Preserve branches, failures, reversals, and unresolved evidence.
6. Draft section headings that reveal the argument when read alone.

Do not manufacture conflict, call a shipped feature a breakthrough without evidence, or force a positive ending. When impact is unknown, end with the strongest verified learning and the measurement plan.

## Output

Return a one-sentence thesis, the five-stage arc, a pivotal-decision statement, three evidence anchors, recommended headings, and unresolved gaps.

## Example

Input:

```text
Operators copied agent output directly until one incorrect batch affected 240 records.
We tested confirmation dialogs, full previews, and risk-tiered approvals. The risk-tiered
model cut routine review time while keeping destructive actions gated.
```

Expected outcome: an arc from fast but unbounded automation, through the 240-record incident and competing controls, to the risk-tiered approval decision and its measured review-time and safety evidence.
