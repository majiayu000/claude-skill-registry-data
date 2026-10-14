---
name: ground-delegation
description: Strategic delegation. When to lead, delegate, or collaborate.
---

# Skill: Delegation

> "A senior engineer knows when to code, when to delegate, and when to collaborate."

## When

1. **At blueprint creation**: Assess each task and assign Owner (`self`, `sub-agent`, or `team`).
2. **Before each task**: Re-assess. Context may have changed.

## Mechanism First

The epigraph says "when to code" — but that is not a delegation choice. `ground-mechanism` decides
the executor **kind** (code or model). This skill decides the executor **context** (self, sub-agent,
team).

Ask mechanism first. If the answer is code, there is nobody to delegate to.

## The Primitives

| Primitive      | Communication    | Best For                                          |
|----------------|------------------|---------------------------------------------------|
| **Self**       | —                | Judgment-heavy, context-dependent, architectural  |
| **Sub-agent**  | Reports back only | Bounded, mechanical, verifiable                  |
| **Agent team** | Peer-to-peer     | Research, competing hypotheses, cross-layer work  |

## The Criteria

### Sub-agent — all four must be true:

| Criterion        | Question                                                   |
|------------------|------------------------------------------------------------|
| **Bounded**      | Can you specify input and expected output in one sentence? |
| **Context-free** | Does it NOT require knowledge of other in-flight tasks?    |
| **Mechanical**   | Is the approach obvious once started?                      |
| **Verifiable**   | Can success be checked without judgment?                   |

All yes → `sub-agent`. Any no → check if `team` fits.

### Agent team — when the work needs dialogue:

| Signal                       | Example                                           |
|------------------------------|---------------------------------------------------|
| **Competing hypotheses**     | Investigate the root cause in parallel             |
| **Cross-layer coordination** | Frontend, backend, and tests move together         |
| **Research with challenge**  | Findings should be questioned, not just collected  |
| **Peer review**              | Multiple lenses on the same artifact               |

If none → `self`.

## Deeper

| | |
|---|---|
| [authority](authority.md) | privilege attenuation, and the authority gradient |
| [briefings](briefings.md) | what a sub-agent is told, and what a team is told |
| [running](running.md) | the workflow, and running in parallel |
| [examples](examples.md) | delegations that worked, and one that did not |

## The Anti-Patterns

- **Over-delegating**: Spawning agents for trivial single-file changes.
- **Under-delegating**: Drowning in mechanical work instead of leading.
- **Vague briefs**: No clear success criteria.
- **Fire and forget**: Not reviewing output before committing.
- **Scope inflation**: Broader access than the task requires.
- **Blind obedience**: Executing flawed briefs without questioning. The `Challenge` line prevents this.
- **File collisions**: Two teammates, same file. Split the work.
