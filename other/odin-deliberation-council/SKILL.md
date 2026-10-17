---
name: odin-deliberation-council
description: Orchestration doctrine for the Deliberation Council workflow — parallel perspective-lens deliberation, synthesized into a reasoned conclusion.
---

# Deliberation Council

## Purpose

Define the orchestration doctrine for the Deliberation Council workflow — a trigger-gated workflow that generates diverse perspectives on a question, synthesizes them into a reasoned conclusion, and communicates it as a Deliverable.

This skill is the dispatch doctrine; the five `bragi-council-deliberation-*` perspective skills are the per-lens instructions that the dispatched Bragi instances load themselves. Keep dispatch briefs at the orchestration level: name the lens skill, the question, and the context inputs; do not restate or invent lens instructions.

**Fixed Deliverable (per § Deliverables and § Deliverable Determination in your system prompt):** a Response only — the synthesized answer drafted by Bragi (step 5). No Artifact. This fixes the Deliverable at Odin's top level: `source=workflow-fixed`, no inference on invoke.

## When to Use

When the Deliberation check verdict is **invoke** — via the `/yggdrasil/deliberate` command, explicit multi-perspective language in the request, or a user-confirmed suggestion, per the Trigger Thresholds in your Communication Policy.

## Workflow

1. **Research gate (conditional).** Assess whether the question requires factual substrate the lenses cannot self-provide (Bragi lacks research skills). When in doubt, err toward research — unnecessary latency is cheaper than silent ungrounded deliberation. When research fires, disclose it and its added dispatch cost at the next user contact your Communication Policy permits. If needed, decide the approach before dispatching:
    - **Single Mimir session** — bounded question, one pass.
    - **Multiple Mimir sessions** — distinct factual areas, dispatched in parallel and merged into one substrate.
    - **Research workflow** — broad question warranting full Kvasir decomposition; use that workflow instead (load `odin-research-workflow`).
Each substrate must be **fact-rich and framing-poor**: "what is the case?", not "what does it mean?" (the lenses' job). Factual findings, sourced claims, descriptive context — no recommendations, no prioritized framings. Each substrate begins with a **scope-declaration preamble**: what was investigated, what was out-of-scope, and why. If research is not needed (conceptual, values, or framing questions), skip this step — the lenses fire on the question alone.

2. **Perspective dispatch.** Dispatch N (default 5) Bragi tasks in parallel, each with one perspective lens from the `bragi-council-deliberation-*` skills, the question, and any available context:
    - `bragi-council-deliberation-foundations` — first-principles lens, strip away convention.
    - `bragi-council-deliberation-systems` — systems-thinking lens, map relationships and feedback loops.
    - `bragi-council-deliberation-adversary` — adversarial lens, construct the strongest case against.
    - `bragi-council-deliberation-pragmatist` — pragmatist lens, test against concrete constraints.
    - `bragi-council-deliberation-humanist` — humanist lens, who is affected and what they value.
If a substrate was produced, each lens receives the reviewed substrate as input context — treated as factual background, not a framing to react to. Each lens must argue its case fully without seeking consensus — convergence is the synthesizer's job.

3. **Synthesis.** Dispatch one Kvasir task to synthesize: read all N perspective Workfiles, weigh the competing arguments, and reach a reasoned conclusion. Kvasir is informed whether a shared research prior was used — shared-input agreement is a weaker signal than independently-emergent agreement.

4. **Deliverable.** Dispatch one Bragi Subtask to draft the final user-facing answer from Kvasir's synthesis Workfile, per the `bragi-council-deliberation-herald` skill. The Deliverable discloses its grounding per that skill's Workflow.

## Quality Criteria

- **One round — no iteration.** The council deliberates once; there is no re-deliberation loop.
- **N=5 — all perspectives fire by default.**
- **Cost (total dispatches — including the standing substrate review and the Final Review Gate, which are not numbered steps):** N + 3 without research (8 at N=5); N + 5 minimum with research (10 at N=5 — one Mimir plus its substrate review); each additional parallel Mimir session adds two dispatches (the session plus its review).
- **Substrates are fact-rich and framing-poor**, each opening with a scope-declaration preamble.
- **Every substrate is reviewed before any lens consumes it** — source-verified, not just coherence-checked.
- **Lenses argue independently** — no lens sees another lens's output; convergence happens only at synthesis.
- **The Deliverable discloses its grounding** — research performed (with Workfile citation) or deliberation on abstraction alone.

## Anti-Patterns

- **Deliberating ungrounded when facts are needed.** Skipping the research-gate assessment, or resolving genuine doubt toward "no research" — doubt resolves toward research.
- **Framing substrates.** A substrate that recommends, prioritizes, or interprets pre-anchors every lens; substrates state only what is the case.
- **Skipping the substrate review.** An unverified substrate defect propagates into all N perspectives at once.
- **Consensus-seeking lenses.** Briefing lenses to converge, or sharing lens outputs between lenses — each lens argues its own case fully; the synthesizer weighs them.
- **Synthesizer-to-user delivery.** Kvasir's synthesis is an intermediate Workfile — a fresh Bragi session drafts the user-facing Deliverable from it, preserving the advisory boundary.
- **Iterating rounds.** One deliberation round only; if the conclusion is unsatisfying, that is a new task, not a re-run.
- **Skipping the Final Review Gate.** The Deliverable is user-facing output and must pass the gate like any other.
