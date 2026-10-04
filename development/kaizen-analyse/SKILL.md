---
name: kaizen-analyse
description: Pick a Kaizen method (Gemba/VSM/Muda) for a target.
argument-hint: target (code, workflow, inefficiency)
allowed-tools: Read, Grep, Glob
---

# Smart Analysis

Selects and applies one of the three Kaizen *observation* methods below (Gemba / VSM / Muda).

## Method Selection Logic

**Gemba Walk** — analyzing code implementation, doc-vs-reality gaps, unfamiliar codebase areas
**Value Stream Mapping** — workflows, pipelines, bottlenecks, handoffs, cycle time
**Muda (Waste Analysis)** — over-engineering, duplication, technical debt, resource waste

If the target is not an observation task, hand off instead of forcing a fit:

| The target is | Use |
|---------------|-----|
| A problem needing a full writeup (background → countermeasures → follow-up) | `kaizen-analyse-problem` (A3) |
| A causal question — "why does this happen?" | `kaizen-analyse-problem/root-cause-methods.md` (Five Whys, Fishbone) |
| A change you want to test and measure | `kaizen-plan-do-check-act` |
| A bug, test failure, or unexpected behavior | `systematic-debugging` |

## Steps
Select the method (or hand off per the table), explain why it fits, execute it, then present findings as actionable recommendations.

## Method 1: Gemba Walk

"Go and see" the actual code to understand reality vs. assumptions.

1. **Define scope**: What code area to explore
2. **State assumptions**: What you think it does
3. **Observe reality**: Read actual code
4. **Document findings**: Entry points, actual data flow, surprises, hidden dependencies, undocumented behavior
5. **Identify gaps**: Documentation vs. reality
6. **Recommend**: Update docs, refactor, or accept

## Method 2: Value Stream Mapping

1. **Identify start and end**: Where process begins and ends
2. **Map all steps**: Including waiting/handoff time
3. **Measure each step**: Processing time, waiting time, owner
4. **Calculate metrics**: Total lead time, value-add vs. waste, % efficiency
5. **Identify bottlenecks**: Longest steps, most waiting
6. **Design future state**: Optimized flow
7. **Plan improvements**: How to get there

## Method 3: Muda (Waste Analysis)

### The 7 Wastes (Applied to Software)
1. **Overproduction**: Unused features, premature abstraction, unnecessary complexity
2. **Waiting**: Slow builds, review delays, blocked dependencies
3. **Transportation**: Unnecessary data transformations, redundant API layers
4. **Over-processing**: Redundant validation, excessive logging, over-normalized data
5. **Inventory**: Unmerged branches, half-finished features, untriaged bugs
6. **Motion**: Context switching, manual deployments, repetitive tasks
7. **Defects**: Production bugs, flaky tests, technical debt, incomplete features

Scope the area, examine each waste type for concrete instances, quantify impact (time, complexity, cost), prioritize by impact, then propose elimination strategies.

