---
name: investigate
description: >
  Deep, multi-lens codebase investigation with evidence-based proofing,
  cross-referencing, diagrams, and synthesis. Use when the user needs to
  understand how something works end-to-end, why it behaves the way it does,
  or what the implications of a design are. Trigger on: "investigate",
  "deep dive", "how does X work", "trace the flow of", "understand this
  system", "analyze this subsystem", "what's going on with", "explain end
  to end", "walk through the architecture", or any request that needs
  call-trace walking, multi-perspective analysis, and synthesized
  recommendations.
---

# Deep codebase investigation

A five-phase investigation workflow. Each phase builds on the last. The subject is whatever the user names: a feature, a subsystem, a pattern, a bug class, an architectural question.

## Arguments

```
/investigate <subject> [focus areas...]
```

The subject is mandatory. Focus areas are optional narrowing hints.

## Phase 1: Evidence gathering

Perform a deep, evidence-based investigation of the subject. Treat every claim as a hypothesis until the code confirms it.

### Method

- Dispatch specialist agents to examine the subject from different lenses. Pick agents that match the subject: architecture for structure, code-review for quality, security for risk, performance for hot paths, explore for discovery. Use at least two lenses. Launch independent agents in parallel.
- Walk call traces in both directions: callers and callees, all the way to the boundary (HTTP handler, background job entry, CLI command, test harness). Do not stop at the first caller.
- Read surrounding code, not just the target symbol. The function above and below, the sibling methods, the module's other exports all carry context.
- Keep scratch notes in `~/.claude/scratchpad/investigate-scratch.md`. Use this file however is useful: findings log, question queue, evidence table, contradictions list. Overwrite it each run.

### Standards

- Every finding must cite `file:line`.
- Distinguish **observed** (code says X) from **inferred** (X implies Y).
- Flag contradictions between code and comments, tests and implementation, or documentation and behavior.

## Phase 2: Cross-reference

Assess how the Phase 1 findings relate to each other.

- Build a relationship matrix: which findings share files, data structures, control flow, failure modes, or domain concepts.
- Identify clusters: findings that reinforce each other, and findings that contradict each other.
- Surface emergent patterns that no single lens caught alone.
- Note gaps: areas the evidence does not cover, questions still open.

Write the cross-reference into the scratch file.

## Phase 3: Diagrams

Create diagrams that make the system visible. Use `/ascii-design` for each diagram.

### Required diagrams

- **Flow diagram**: the primary control flow through the subject, with decision points and branches.
- **Data diagram**: the shape of data at each stage. Use dummy data that shows realistic structure, field names, types, and cardinality.

### Optional diagrams
*(include when the subject warrants them)*

- **Before/after**: when the investigation reveals an architectural shift, a migration path, or a proposed change.
- **Dependency diagram**: when the subject spans multiple services, modules, or packages.
- **State diagram**: when the subject involves a state machine or lifecycle.

Each diagram must label every node with the real file or module name.

## Phase 4: Synthesis

Read the full output from Phases 1 through 3 as a whole. This is a fresh pass, not a summary.

- For each section, draw conclusions informed by the other sections. A finding from the architecture lens may explain a pattern from the quality lens.
- Note new patterns that appear only when comparing sections.
- Identify the load-bearing decisions: the choices that, if changed, would cascade through the most findings.
- Draft recommendations grounded in the evidence. Each recommendation must:
  1. Name the finding or pattern it addresses.
  2. Cite the relevant `file:line` locations.
  3. Include a representative code snippet showing what the change looks like. Match the project's language, idioms, and conventions.
  4. State the tradeoff: what improves, what gets harder or more complex.

## Phase 5: Deliver

Present the final output to the user. Structure it as:

1. **Summary**: 2-3 sentences on what was investigated and the headline finding.
2. **Findings**: the evidence from Phase 1, organized by theme (not by agent or lens).
3. **Cross-references**: the Phase 2 relationship analysis, as a table or grouped bullets.
4. **Diagrams**: inline from Phase 3.
5. **Recommendations**: from Phase 4, ranked by impact. Lead with the highest-leverage change.

Clean up the scratch file after delivery.
