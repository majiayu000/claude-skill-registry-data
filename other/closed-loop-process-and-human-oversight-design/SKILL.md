---
name: closed-loop-process-and-human-oversight-design
description: "Structures business processes as open or closed loops and decides the human's role (in-the-loop / on-the-loop / outside-the-loop) in each — a mental model for designing AI agents' areas of responsibility."
---

# Closed-Loop Process & Human Oversight Design

## Purpose

Help you see the business as a collection of processes, some of which are
"open loops" (executed, not learned from) and some of which could be
"closed loops" (executed, measured, automatically adjusted on the next
cycle). This skill provides the language and decision framework for
which processes are worth designing as closed loops, and where the
human needs to stay involved in decision-making — via a three-tier
in-the-loop/on-the-loop/outside-the-loop model.

## Based on

- The owner's AI-native Business Design workshop
  (the owner's own workshop), run 1–2 June 2026, Day 1 —
  Session 1 "AI as the operating system your company runs on": the open
  loop (Input → Execution → Output, no systematic feedback) vs. the
  closed loop (Input → Execution → Output → Feedback → Adjustment → back
  to Input); the core idea that "your company isn't one closed loop —
  it should be a set of closed loops," each run by agents and
  orchestrated together.
- The human-in-the-loop / human-on-the-loop / human-outside-the-loop
  three-way split on the level of human oversight in an AI process.
- Agent, orchestration, and tool/agent-registry concepts, as presented by
  the workshop.

## Method

1. **Choose a process to examine.** E.g. order processing, customer
   support, content production, quality assurance, sales tracking.
2. **Map the process as it currently stands.** Is it an open loop — Input
   → Execution → Output with no systematic feedback that would change
   the next cycle — or does it already have a partial feedback
   mechanism? Most companies, and most parts of most companies, run as
   open loops: learned information leaks away each cycle instead of
   improving the next one.
3. **Design the closed loop.** Add Feedback and Adjustment stages: Input
   → Execution → Output → Feedback → Adjustment → (back to Input). A
   closed loop is self-regulating — it watches its own output and
   adjusts its behavior to keep hitting the target.
4. **Give the loop a clear, measurable goal.** A closed loop only works
   if it knows what it needs to achieve and can measure progress toward
   it.
5. **Decide the human's position relative to the loop**, from three
   options:
   - **Human-in-the-loop** — a human reviews/approves every step before
     it proceeds. Highest control, slowest, suited to high-stakes or
     still-untested processes.
   - **Human-on-the-loop** — the process runs independently, a human
     monitors and can intervene when needed. A good middle ground once
     the loop has proven reliable.
   - **Human-outside-the-loop** — the process runs fully automatically
     with no human in any individual case. Fastest and most scalable,
     suited only for a trusted loop where the cost of error is low.
6. **Honestly assess whether the workflow is genuinely closed-loop
   shaped** before you set out to automate it: does it have a clear
   goal, machine-readable inputs, well-defined tools an agent can use,
   and a measurable success signal? If the work is mostly quiet human
   judgment without these, document the process manually first rather
   than trying to automate it directly.
7. **Once multiple loops have been designed:** record a tool/agent
   registry — which agents/tools are in use, what each does, and how work
   is routed to the right place. Think about orchestration: how the
   separate loops coordinate into a bigger, coherent whole.

## Gotchas

- Calling a process "closed loop" just because it has some occasional
  feedback is not the same as it having explicit Feedback and
  Adjustment stages that actually change the next cycle's behavior —
  step 2 notes most companies run as open loops where learned
  information leaks away each cycle, and it's easy to mistake ad hoc
  feedback for a real loop.
- Defaulting to human-outside-the-loop because it's fastest, without the
  loop having actually proven reliable, contradicts the method: that
  tier is suited only to a trusted loop where the cost of error is
  already known to be low, not to a newly designed one.
- Forcing a process into the closed-loop framework when it's mostly
  quiet human judgment without a clear goal, machine-readable inputs,
  well-defined tools, and a measurable success signal is exactly what
  step 6 warns against — document it manually first instead of
  automating it prematurely.
- This skill is the initial design choice, not the ongoing governance
  layer — once a loop is live with real usage data to calibrate
  against, the deeper model (confidence-score routing, override-rate
  diagnostics) lives in
  `../../../../human-ai-collaboration-design/skills/hitl-maturity-and-confidence-routing/SKILL.md`,
  not here.
- The goal is removing the *bottleneck* of human judgment only where
  it isn't genuinely needed — treating "closed loop" as a mandate to
  automate everything and remove judgment entirely is the opposite of
  what the method intends.

## What this skill does NOT do

- Does not recommend automating everything — the main message is the
  opposite: the goal is to remove the *bottleneck* of human judgment
  from the places where it isn't genuinely needed, not to remove
  judgment entirely from where it is needed.
- Does not assess a specific AI tool's technical feasibility — see
  `../ai-native-tool-stack-selection/SKILL.md` and
  `../../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md`.
- Does not replace a responsible-AI governance check for high-risk use
  cases — see
  `../../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md`
  and, if needed, separate EU AI Act regulatory expertise (not included
  in this skills pack).

## Continue from here

- Preceding/related skill in this pack:
  `../ai-native-opportunity-scan/SKILL.md` (the agentic-ness
  identification criterion that this skill deepens).
- Related skill in another pack:
  `../../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
  (the "Degree of Agenticness" stage),
  `../../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md`
- Related skill in another pack:
  `../../../../business-design-frameworks/skills/value-chain-mapping/SKILL.md`
  — a complementary way to structure the same business as a value chain
  rather than as processes.
- **Once a loop is live and needs deeper operational governance**, not
  just this initial design choice: `../../../../human-ai-collaboration-design/skills/hitl-maturity-and-confidence-routing/SKILL.md`
  — a four-level maturity model with confidence-score routing, a named
  accountable calibration owner, and override-rate diagnostics. This
  skill's simple in/on/outside-the-loop model is still the right starting
  point for an early-stage design decision; the linked skill is the
  deeper layer for once the process has real usage data to calibrate
  against.
- The pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/workshop-source.md` — source information
- `../../CLAUDE.md` — the pack's shared guardrails
