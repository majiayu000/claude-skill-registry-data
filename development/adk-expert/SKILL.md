---
name: adk-expert
description: "Google ADK (Agent Development Kit) orchestration patterns — boundaries, agent composition, and tool seams. Trigger when designing or reviewing multi-agent systems built on ADK. Authoritative source: adk.dev."
---

# ADK Expert

> **ADK is a mental model for agent composition, not a framework to learn. The patterns transfer to any orchestration foundation.**

This skill covers how to think about agent boundaries, orchestration topology, and tool seams using Google ADK principles. It is not a tutorial on SDK methods — the official docs at [adk.dev](https://adk.dev) own that. This skill covers the architecture of agent systems.

## When to use

- Designing a multi-agent system on Google ADK
- Deciding where to draw agent boundaries
- Choosing between orchestration topologies (supervisor-worker vs peer-to-peer vs sequential)
- Reviewing an existing ADK-based system for structural problems
- Integrating MCP servers or external tools into an ADK agent graph

## Procedure

1. **Verify current ADK documentation** — before writing any agent topology or referencing API surface, fetch the latest docs from [adk.dev](https://adk.dev). ADK evolves; training data lags.

2. **Define agent responsibilities first** — each agent in the system must have:
   - A single, nameable responsibility
   - A defined input contract (what it receives)
   - A defined output contract (what it produces)
   - A declared set of tools it may use (no raw DB access; use bounded tool seams)

3. **Choose the orchestration topology**:

   | Topology | When to use | Trade-off |
   |---|---|---|
   | Supervisor → Worker | Audit trails required; routing logic is complex | Adds latency; supervisor is a bottleneck |
   | Sequential pipeline | Tasks are strictly ordered; each step feeds the next | Simple but no parallelism |
   | Parallel fan-out | Independent sub-tasks that merge at a synthesis step | Fast; coordination overhead at merge |
   | Peer-to-peer | Speed over governance; tasks are loosely coupled | Hard to audit; compliance risk |

4. **Design the tool seams** — tools are the boundary between an agent and the external world. Each tool should:
   - Have a typed schema (inputs and outputs)
   - Enforce the agent's permission scope (least-privilege)
   - Be independently testable
   - Return structured errors, not raw exceptions

5. **Plan for agent failure** — every agent in the graph must have a declared failure behaviour: retry, escalate to supervisor, return partial result, or halt. Unhandled agent failure silently corrupts downstream output.

6. **Add observability at the boundary** — log every agent invocation: agent name, input summary, output summary, latency, tool calls made. The agent graph is only debuggable if the boundary calls are visible.

7. **Run the Adversarial Gate** — before finalising the topology, invoke `adversarial-gate` on the design. Common failure modes: supervisor SPOF, context window overflow at the synthesis step, tool permission creep, silent agent loops.

## Outputs

- Agent topology diagram (C4 component or sequence diagram)
- Agent responsibility matrix: agent | input | output | tools | failure behaviour
- Tool schema definitions (typed inputs/outputs)
- ADR for topology choice (via `the-architect`)

## Guardrails

- **The agent graph is not self-documenting.** Name every agent, every tool, every edge. Implicit wiring creates invisible failure modes.
- **No raw database access from agents.** Agents call tools; tools call infrastructure. This boundary is the governance seam.
- **Context window is finite.** Design the graph so no single agent accumulates unbounded context. Summarise at synthesis points.
- **Verify API surface before writing code.** ADK API changes. Always ground against [adk.dev](https://adk.dev) before implementing.
