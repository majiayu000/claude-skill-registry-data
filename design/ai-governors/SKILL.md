---
name: ai-governors
description: >-
  Use when designing or auditing AI product human-in-the-loop — write approval,
  proposal accept/reject, action confirm, spend caps, run detail, memory
  capture, or any AI action with irreversible blast radius. Trigger on
  confirmation UX, undo, cost-before-act, show-the-plan, citations, or keeping
  the owner in control.
---

# AI Governors — HITL product UX

Governors are **product patterns** that keep the owner in control while the
agent acts. Mechanism skills answer "is the gate sound?". This skill answers
"which oversight *shape* should the surface expose?".

Pattern catalog: [references/patterns.md](references/patterns.md).
Adapted from tommyjepsen/awesome-ux-skills `ai-governors`.

## When to use

- Write-approval queues, staged proposals, action confirm, spend UI, agent
  activity / runs, memory capture, voice speaker gates.
- Phrases like: confirm before act, undo, show cost, action plan, cite sources,
  draft then commit, pause the agent.
- **Not** for: low-level gate wiring audits, untrusted prompt framing, or
  workflow Send-and-Wait plumbing in isolation.

## Seam → pattern map

| Seam | Prefer | Hard rules |
|---|---|---|
| Staged writes / approvals | Verification + Memory + Footprints | Queue must drain; bind approval to exact bytes |
| Proposal accept/reject | Verification + Sample + Cost + Draft | Never auto-apply on model confidence alone |
| Action / code confirm | Action Plan + Verification + Cost | Confirm ahead of irreversible fire |
| Cloud / research spend | Cost Estimates (+ Draft for bakeoffs) | Unknown cost → visible, not "free" |
| Runs / agent activity | Shared Vision + Stream + Controls | Stop/cancel only if real control exists |
| Memory / fact capture | Memory (+ Verification when sensitive) | Secret scan before store |
| Research / web / vision | Citations + References | Untrusted framing; honest observer mode |
| Voice / mic gates | Controls + Verification | Partial API must not crash UI |

## Calibration (friction vs speed)

Match friction to **irreversibility × blast radius**:

1. **High** (money, outbound message, memory write, destructive tool) →
   Action Plan or Verification; no silent defaults that grant the act.
2. **Medium** (long research, multi-step run) → Shared Vision + Controls +
   Cost; Verification on the commit step.
3. **Low** (search, draft reply) → skip Verification; optional Citations.

Prompt fatigue is a defect: confirming every chat turn trains click-through.
Prefer one strong gate on the irreversible step.

## Design checklist

- [ ] Name the irreversible effect in the confirm copy.
- [ ] Approval bound to exact bytes / run id / proposal id — not vague intent.
- [ ] Cost or side-effect visible before commit when spend is non-trivial.
- [ ] Undo or compensating action stated when reversible; say so when not.
- [ ] Failure path does not skip the gate.
- [ ] Absent evidence ≠ consent.

## Anti-patterns

- Manifest that promises a capability the confirm gate still blocks.
- Staging then auto-applying "because the model was confident".
- Cost UI that meters one lane while another is silently free.
- A Stop control that only navigates away.
- Partial state payloads that crash the oversight UI.

## Output format

1. **Situation** — blast radius in one sentence.
2. **Patterns** — 1–3 from the catalog.
3. **Surface** — concrete UI / flag / API.
4. **Friction** — high / medium / low and why.

## Cross-references

- `ai-trust-builders` — disclosure beside oversight
- `ai-wayfinders` — first-run discoverability (does not replace HITL)
