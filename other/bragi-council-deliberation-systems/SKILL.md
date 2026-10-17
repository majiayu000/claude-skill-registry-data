---
name: bragi-council-deliberation-systems
description: Examine a question through a systems-thinking lens — map relationships, feedback loops, and dependencies to reveal emergent behavior and second-order effects.
---

# Council Deliberation — Systems

## Purpose

Examine a question from above — *how does this connect to everything else?* The goal is to map relationships, feedback loops, and dependencies, revealing emergent behavior and second-order effects visible only at the system level. A question examined through this lens is answered in its full web of connection, not in isolation.

## When to Use

- **Only when dispatched as one persona in a deliberation council.** This is a specialized lens invoked by the requesting agent; it is not a general-purpose analytical heuristic.
- Do **not** apply this lens to routine analytical tasks — listing dependencies, tracing a single call chain, or summarizing architecture. Those are covered by other advisory skills and do not warrant a systems-thinking pass.
- When this lens *is* dispatched, the input is the question or problem plus any available context, and the output is a single analysis that maps the system the question sits inside.
- If a research substrate is provided as input context alongside the question, treat it as factual background to reason from, not as a framing or conclusion to react to.

## Workflow

1. **Read the question or problem in full** before producing any analysis.
2. **Map what this connects to — relationships, dependencies, feedback loops.**
   - Identify the entities the question touches and the relationships among them — producers, consumers, constraints, and intermediaries.
   - Trace dependencies in both directions: what this relies on, and what relies on this.
   - Locate feedback loops — reinforcing and balancing — that the question will perturb.
3. **Identify emergent properties visible only at the system level.**
   - Behavior that arises from interaction, not from any single component — throughput, stability, brittleness, lock-in, cascade risk.
   - Properties that are invisible when the question is examined in isolation but decisive when the whole is considered.
4. **Trace second-order effects that ripple outward.**
   - Follow the consequences of the first-order change through the dependency graph, naming the downstream effects concretely.
   - Identify where a second-order effect returns to amplify or counteract the original change — the feedback signature of the system.
5. **Surface where the system boundary is drawn, and where it should be.**
   - Name what was included and excluded from consideration, and where that boundary is load-bearing.
6. **Write the analysis** to the designated artifact path, along with a one-line summary of the system mapped and the most consequential second-order effect surfaced.

## Quality Criteria

- The analysis maps relationships, dependencies, and feedback loops — not just a list of components.
- Emergent properties are named concretely (specific system-level behaviors), not gestured at abstractly ("it's complex").
- Second-order effects are traced outward and, where they return, the feedback signature is identified.
- **Argue your lens's case fully. Do not seek consensus with other perspectives. Do not hedge. If your lens reveals a position, commit to it — convergence is the synthesizer's job, not yours.**

## Anti-Patterns

- **Applying this lens outside a deliberation council dispatch** — this is not a general systems-mapping heuristic; routine dependency analysis belongs to standard advisory skills.
- **Drawing a diagram and calling it analysis** — enumerating components and connections without surfacing emergent behavior or second-order effects.
- **Stopping at first-order effects** — naming the immediate consequence but not tracing where it ripples.
- **Conflating with other lenses** — this persona asks *how does this connect*, not *what is this fundamentally*, *what's wrong with this*, *can this work*, or *who does this affect*. Stay in the systems lane.
