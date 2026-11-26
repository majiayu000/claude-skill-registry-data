---
name: agent-orchestration-lord
description: Lord skill for multi-agent orchestration — pattern selection (orchestrator-worker, supervisor-router, hierarchical, peer-to-peer), A2A communication, task decomposition, and failure handling.
triggers:
  - agent orchestration lord
  - multi-agent
  - orchestration
  - orchestrator worker
  - supervisor router
  - agent coordination
  - تنسيق الوكلاء
  - توجيه الوكلاء
personas:
  - ARCH
  - ML
  - DEV
  - API
tech_stack: []
lord: true

---

# Agent Orchestration Lord

[OBJ] Design multi-agent systems with correct orchestration patterns, communication protocols, failure handling, and observability — avoiding god-orchestrators and tight coupling.

## Problem

Multi-agent systems promise parallelism and specialization but deliver chaos without discipline: agents talk past each other, the orchestrator becomes a bottleneck, shared mutable state causes race conditions, and a single agent failure cascades to system-wide breakdown. The orchestration layer is the most critical and most abused component.

## Rules

1. [REQ] **Orchestration pattern selection.** Choose based on task structure: orchestrator-worker (fan-out/fan-in, independent subtasks), supervisor-router (classify + delegate, dynamic routing), hierarchical (multi-level delegation, complex orgs), peer-to-peer (collaborative, no central authority). Document the rationale.
2. [REQ] **Agent communication via A2A.** Use the Agent-to-Agent (A2A) protocol for inter-agent communication. A2A defines agent cards, task lifecycle, and streaming. Do not invent ad-hoc message formats. Fallback to ACP (Agent Communication Protocol) for simpler setups.
3. [REQ] **MCP for tool sharing.** Agents share tools via MCP servers, not via direct code imports. Each agent connects to the MCP servers it needs. No agent has direct code-level access to another agent's tools.
4. [REQ] **Task decomposition.** Decompose tasks until each subtask is: (a) independently executable by one agent, (b) has clear input/output contract, (c) has a defined success criteria. No subtask should require another agent's internal state to proceed.
5. [REQ] **Parallel vs sequential.** Run independent subtasks in parallel. Run dependent subtasks sequentially. The orchestrator MUST know the dependency graph — no implicit dependencies. Parallel execution requires the subtasks to be truly independent (no shared mutable state).
6. [REQ] **Result aggregation.** Define the aggregation strategy upfront: merge (combine partial results), select (pick best result), vote (majority/weighted), synthesize (LLM combines into new output). No "let the orchestrator figure it out" — aggregation is a defined step.
7. [REQ] **Conflict resolution.** When agents produce conflicting results, resolve via: confidence scores (pick highest), domain authority (specialist wins), human escalation (irreconcilable), or re-delegation (ask a third agent). Document the resolution policy per task type.
8. [REQ] **Agent specialization.** Each agent has ONE primary capability. A "generalist" agent is an anti-pattern — it becomes a god-agent. Specialize: research agent, code agent, review agent, test agent. The orchestrator composes; agents do not generalize.
9. [REQ] **Context isolation.** Each agent operates in its own context window. Do not share full conversation history between agents — share only the task input and output contract. Prevents context overflow and cross-contamination of reasoning.
10. [REQ] **Shared memory patterns.** When agents need shared state, use an external store (Redis, vector DB, key-value store) with explicit read/write APIs. No shared in-memory variables between agents. Version all shared state for conflict resolution.
11. [REQ] **HITL gates in orchestration.** Insert human-in-the-loop gates at: high-stakes decisions (deploy, delete, spend), low-confidence results (agent confidence < threshold), and policy-sensitive actions (data access, external comms). The orchestrator pauses and waits for approval.
12. [REQ] **Failure handling — circuit breaker.** If an agent fails N consecutive times, trip the circuit breaker: stop sending tasks to that agent, alert, and either retry with a fallback agent or fail the workflow. No infinite retries on a broken agent.
13. [REQ] **Failure handling — fallback.** Define a fallback agent or fallback behavior for each agent role. If the primary agent fails, the fallback takes over. If no fallback exists, the orchestrator escalates to human.
14. [REQ] **Failure handling — retry.** Retry failed agent calls with exponential backoff. Max retries configurable per agent. Non-retryable errors (auth, validation) do not retry. Retryable errors (timeout, 5xx) retry up to the limit.
15. [REQ] **Cost optimization.** Track per-agent cost (tokens, API calls, time). Route tasks to the cheapest capable agent. Do not use a GPT-4-class agent for a task a GPT-4o-mini-class agent can handle. Cost dashboard per orchestration run.
16. [REQ] **Observability — tracing and spans.** Every orchestration run produces a trace. Each agent call is a span with: agent ID, task, input summary, output summary, duration, cost, status. Use OpenTelemetry + OpenInference for span attributes.
17. [REQ] **Testing multi-agent systems.** Test by: (a) unit test each agent in isolation, (b) integration test the orchestration graph with mocked agents, (c) chaos test by killing one agent mid-run and verifying fallback/recovery. No multi-agent system ships without a chaos test.
18. [PROHIBIT] God-orchestrator (one agent does everything), tight coupling (agents import each other's code), and shared mutable state between agents — these three guarantee production failure.

## References

- A2A Protocol: https://a2a-protocol.org
- Agent Communication Protocol (ACP)
- LangGraph: https://langchain-ai.github.io/langgraph
- CrewAI: https://crewai.com
- MS Agent Framework: https://github.com/microsoft/agent-framework
- Google ADK: https://google.github.io/adk-docs
- Mastra: https://mastra.ai
