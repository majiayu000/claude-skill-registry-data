---
name: research-brainstorm
description: Brainstorm follow-up research ideas from papers. Use when asked to generate research directions or ideas.
---

# Research Brainstorming

## When to use

- User says "what could we do next based on this paper?"
- User asks for research directions, follow-ups, or extensions
- User wants to identify gaps in existing work

## Workflow

1. **Understand the paper deeply** before brainstorming
   - What's the core contribution? What's actually new?
   - What assumptions does it rely on?
   - What did they NOT do, and why?
   - What are the stated limitations?

2. **Identify gaps from multiple angles**:
   - *Methodology*: can the approach be applied to different domains/modalities?
   - *Scale*: does it work at 10x/100x the tested scale?
   - *Assumptions*: what happens when key assumptions are relaxed?
   - *Combination*: can this be combined with orthogonal recent work?
   - *Failure modes*: where does the method break down?

3. **Generate 3-5 concrete research directions**, each with:
   - **One-line description**: specific and actionable
   - **Gap**: what's missing in the current work that this addresses
   - **Approach sketch**: 2-3 sentences on how you'd actually do it
   - **Feasibility**: easy (weeks, existing tools) / moderate (months, some new infrastructure) / hard (6+ months, fundamental challenges)
   - **Resources needed**: data, compute, specific expertise

4. **Quality bar**: every idea must be specific enough to start working on
   - Bad: "improve the model's performance"
   - Bad: "apply to other domains"
   - Good: "replace the cross-attention in the fusion module with a mixture-of-experts gate, since the current design scales quadratically with the number of modalities — test on the AudioSet + ImageNet joint benchmark"

5. **Prioritize** by the intersection of novelty and feasibility — the best ideas are those that are clearly doable and clearly haven't been done

## Formatting for Slack

- Number the ideas
- Bold the one-line description
- Keep feasibility assessments honest — don't oversell
- If an idea requires specific expertise the lab may not have, say so
