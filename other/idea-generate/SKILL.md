---
name: idea-generate
category: research-analysis
description: Helps users generate, refine, and stress-test ideas from loose topics. Use when user asks to brainstorm, find new ideas, or needs creative inspiration for a topic.
related-skills:
  - clarity-council
  - grill-me
loop-eligible: false
recurrence-hint: on-demand
compatibility: claude-code codex opencode
---

# Idea Generate

This skill guides the user through a process of **Divergence** (creating many options) and **Convergence** (refining the best ones).

## Quick Start
Provide one or more loose topics: *"I want some ideas for a new side project related to urban gardening and AI."*

## Workflows

### Phase 1: Divergence (Brainstorming)
The goal is to generate a high volume of diverse, raw ideas.

1. **Consult the Council**: Invoke `clarity-council` with a multi-persona set:
   - **The Visionary**: Focused on "blue sky" possibilities and radical innovation.
   - **The Skeptic**: Identifies potential failures and constraints early.
   - **The Pragmatist**: Focuses on feasibility, utility, and immediate application.
2. **Apply Frameworks**: Direct the council to use the frameworks in [REFERENCE.md](REFERENCE.md):
   - Use **First Principles** to strip away assumptions and find fundamental truths.
   - Use **SCAMPER** to iterate on existing concepts or twist them into something new.
3. **Present Raw List**: Output a simple list of ideas with a one-sentence summary for each.

### Phase 2: Selection & Filtering
Collaborate with the user to narrow down the list.

1. **User Feedback**: Ask the user which 2-3 ideas resonate most or if any specific "spark" should be pursued further.
2. **Preliminary Refinement**: Briefly flesh out the shortlisted ideas into basic concepts.

### Phase 3: Convergence (Stress-Testing)
Turn raw ideas into robust plans by attempting to break them.

1. **The Grill**: For each shortlisted idea, invoke `grill-me`.
2. **Iterative Hardening**: Use the grilling session to identify gaps, contradictions, or weaknesses.
3. **Final Polish**: Refine the idea based on the grill results until it reaches a state of high confidence.

## Guidelines
- **Start Simple**: Don't over-engineer the first batch of ideas. Focus on "hooks" and concepts.
- **Avoid Consensus Too Early**: Encourage the council members to disagree during Phase 1.
- **Embrace Friction**: Use `grill-me` not to discourage, but to harden the idea.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/idea-generate.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
