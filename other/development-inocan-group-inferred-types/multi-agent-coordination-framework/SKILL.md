---
name: multi-agent-coordination-framework
description: Advanced multi-agent coordination for managing AI agent pods and human teams. Includes agent architectures, communication patterns (pub/sub, message queues), task distribution, consensus mechanisms, conflict resolution, agent specialization, collaborative problem-solving, shared state management, lifecycle management, and multi-agent observability. Supports LangGraph, AutoGen, CrewAI, and distributed systems patterns.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# Multi-Agent Coordination Framework

## Purpose

Managing multiple AI agents or human teams requires sophisticated coordination mechanisms. This Skill provides comprehensive capabilities for:

1. **Multi-Agent System Architectures** - Hub-spoke, peer-to-peer, hierarchical coordination
2. **Agent Communication Patterns** - Pub/sub, message queues, direct messaging, broadcast
3. **Task Distribution Algorithms** - Load balancing, capability-based routing, priority queues
4. **Consensus and Voting Mechanisms** - Agreement protocols, quorum-based decisions
5. **Conflict Resolution** - Handling disagreements, resource contention, priority conflicts
6. **Agent Specialization and Routing** - Role-based agents, skill matching, dynamic routing
7. **Collaborative Problem-Solving** - Multi-agent reasoning, distributed search, collective intelligence
8. **Shared State Management** - Distributed state, CRDTs, event sourcing
9. **Agent Lifecycle Management** - Registration, health checks, scaling, retirement
10. **Multi-Agent Debugging and Observability** - Distributed tracing, agent metrics, visualization

## When to Use This Skill

Use this skill when you need to:

- Build multi-agent AI systems with specialized agents
- Coordinate human teams with AI assistance
- Implement distributed problem-solving requiring multiple perspectives
- Design complex workflows requiring agent collaboration
- Create agent swarms for parallel processing
- Implement human-in-the-loop AI systems
- Orchestrate multi-model systems (GPT-4, Claude, local models)
- Build competitive agent systems (agents voting/competing)
- Design hierarchical agent organizations
- Create agent mesh networks for resilience
- Implement collaborative code review by multiple agents
- Build ensemble AI systems for improved accuracy

## Quick Start

### 1. Choose Your Architecture

Start by selecting the right architecture for your use case:

- **Hub-Spoke (Centralized)** - Simple coordinator routes tasks to specialized agents
  - Use when: Single point of coordination is acceptable, simple debugging needed
  - Example: Supervisor agent coordinating code review by specialized agents

- **Peer-to-Peer (Distributed)** - Agents communicate directly without central coordinator
  - Use when: High availability needed, no single point of failure tolerated
  - Example: Agent mesh for distributed data processing

- **Hierarchical (Tree)** - Multi-level supervision with delegation
  - Use when: Complex workflows, need clear responsibility hierarchy
  - Example: Engineering organization simulation with managers and workers

- **Mesh (Fully Connected)** - All agents can communicate with all others
  - Use when: Maximum resilience required, communication overhead acceptable
  - Example: Consensus-based decision systems

See [REFERENCE.md](./REFERENCE.md#architectures) for detailed architecture diagrams.

### 2. Select Your Framework

Choose the framework that matches your needs:

| Framework | Best For | Complexity | Key Strength |
|-----------|----------|------------|--------------|
| **LangGraph** | Complex workflows, state management | Medium | Graph-based coordination |
| **AutoGen** | Conversations, human-in-loop | Low | Easy multi-agent chat |
| **CrewAI** | Role-based teams | Low | Task delegation |
| **Custom** | Full control, unique requirements | High | Maximum flexibility |

See [KNOWLEDGE.md](./KNOWLEDGE.md#framework-comparison) for detailed comparison.

### 3. Implement Your First Multi-Agent System

**Example: Simple supervisor pattern with LangGraph**

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_agent: str

# Create specialized agents
def researcher(state):
    # Research logic
    return {"messages": ["Research complete"], "next_agent": "writer"}

def writer(state):
    # Writing logic
    return {"messages": ["Report written"], "next_agent": "FINISH"}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher)
workflow.add_node("writer", writer)
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)
workflow.set_entry_point("researcher")

app = workflow.compile()
result = app.invoke({"messages": [], "next_agent": "researcher"})
```

See [EXAMPLES.md](./EXAMPLES.md) for complete working examples.

### 4. Add Consensus Mechanism (Optional)

For critical decisions, implement voting:

```python
from multi_agent_coordination import ConsensusEngine, Vote, VoteType

consensus = ConsensusEngine(agents=["agent_1", "agent_2", "agent_3"])

votes = [
    Vote("agent_1", VoteType.YES, 0.9, "High confidence"),
    Vote("agent_2", VoteType.YES, 0.8, "Agree"),
    Vote("agent_3", VoteType.NO, 0.7, "Concerns exist"),
]

result = consensus.simple_majority(votes)
# Returns: {"result": "PASS", "yes": 2, "no": 1, "percentage": 66.7}
```

See [PATTERNS.md](./PATTERNS.md#pattern-4-consensus-voting) for full consensus patterns.

## Implementation Patterns

This skill provides 6 battle-tested patterns:

### Pattern 1: LangGraph Multi-Agent with Supervisor
**When to use**: Complex workflows with state persistence and conditional routing
**Complexity**: Medium
**Key features**: Graph-based coordination, state management, cycle prevention

[View Pattern Details](./PATTERNS.md#pattern-1-langgraph-supervisor) | [View Code Example](./EXAMPLES.md#example-1-langgraph-supervisor)

### Pattern 2: AutoGen Multi-Agent Conversation
**When to use**: Conversational agents, human-in-the-loop, group chat scenarios
**Complexity**: Low
**Key features**: Natural conversation flow, easy human interaction, code execution

[View Pattern Details](./PATTERNS.md#pattern-2-autogen-conversation) | [View Code Example](./EXAMPLES.md#example-2-autogen-conversation)

### Pattern 3: CrewAI Role-Based Teams
**When to use**: Clear role assignments, task delegation, sequential workflows
**Complexity**: Low
**Key features**: Role specialization, task dependencies, built-in tools

[View Pattern Details](./PATTERNS.md#pattern-3-crewai-teams) | [View Code Example](./EXAMPLES.md#example-3-crewai-teams)

### Pattern 4: Consensus and Voting Mechanisms
**When to use**: Critical decisions, multiple agent perspectives, conflict resolution
**Complexity**: Medium
**Key features**: Multiple voting types, weighted decisions, quorum support

[View Pattern Details](./PATTERNS.md#pattern-4-consensus-voting) | [View Code Example](./EXAMPLES.md#example-4-consensus-voting)

### Pattern 5: Shared State with Event Sourcing
**When to use**: Distributed state, audit trail needed, state replay required
**Complexity**: High
**Key features**: Immutable events, state reconstruction, time-travel debugging

[View Pattern Details](./PATTERNS.md#pattern-5-event-sourcing) | [View Code Example](./EXAMPLES.md#example-5-event-sourcing)

### Pattern 6: Agent Lifecycle Management
**When to use**: Dynamic agent pools, health monitoring, auto-scaling needed
**Complexity**: High
**Key features**: Health checks, registration, auto-scaling, metrics

[View Pattern Details](./PATTERNS.md#pattern-6-lifecycle-management) | [View Code Example](./EXAMPLES.md#example-6-lifecycle-management)

## Top Gotchas

### 1. Coordination Overhead
**Problem**: Too much agent communication slows everything down
**Solution**: Batch communications, use async patterns, minimize chatter
**Detection**: Monitor message count and latency between agents

### 2. Agent Deadlock
**Problem**: Agents waiting for each other in circular dependency
**Solution**: Timeout on all waits, detect cycles, use coordinator to break deadlocks
**Detection**: Trace agent state transitions, look for circular waits

### 3. State Inconsistency
**Problem**: Agents have different views of shared state
**Solution**: Event sourcing, CRDTs, eventual consistency, versioning
**Detection**: Compare agent state snapshots, look for divergence

[View All 10 Gotchas](./GOTCHAS.md) - Detailed troubleshooting guide

## Communication Patterns

### Synchronous (Request-Response)
Direct agent-to-agent communication with immediate response.
```
Agent A ──request──► Agent B
Agent A ◄─response── Agent B
```

### Asynchronous (Message Queue)
Fire-and-forget messaging via queue.
```
Agent A ──msg──► Queue ──msg──► Agent B
```

### Pub/Sub (Broadcast)
One-to-many broadcasting to subscribers.
```
Publisher ──event──► Topic ──┬──► Subscriber 1
                             ├──► Subscriber 2
                             └──► Subscriber 3
```

See [REFERENCE.md](./REFERENCE.md#communication-patterns) for detailed patterns.

## Best Practices

### DO's

1. **Start Simple** - Begin with single agent, add multi-agent only when needed
2. **Clear Contracts** - Define explicit communication protocols between agents
3. **Timeout Everything** - All agent interactions should have timeouts
4. **Monitor Conversations** - Log all agent-to-agent communications
5. **Use Voting** - For critical decisions, use consensus mechanisms
6. **Specialize Agents** - Each agent should have clear, focused responsibility
7. **Handle Failures** - Expect agents to fail, implement graceful degradation
8. **Version Protocols** - Use versioned message formats for compatibility
9. **Test in Isolation** - Test each agent independently before integration
10. **Implement Observability** - Trace multi-agent interactions for debugging

### DON'Ts

1. **Don't Create Agent Explosion** - Resist urge to create too many agents
2. **Don't Share Mutable State** - Use message passing, not shared memory
3. **Don't Ignore Deadlocks** - Test for circular dependencies
4. **Don't Skip Health Checks** - Monitor agent health continuously
5. **Don't Hardcode Routing** - Use dynamic agent discovery and routing
6. **Don't Trust All Agents** - Validate agent responses, especially in open systems
7. **Don't Forget Cleanup** - Properly shutdown and cleanup agent resources
8. **Don't Over-Engineer** - Simple coordination often beats complex protocols

## Documentation Structure

This skill uses progressive disclosure - start here and drill down as needed:

- **[KNOWLEDGE.md](./KNOWLEDGE.md)** - Framework deep-dives, theory, research, protocols
- **[PATTERNS.md](./PATTERNS.md)** - Implementation pattern details, architecture guidance
- **[EXAMPLES.md](./EXAMPLES.md)** - Complete, runnable code examples for all patterns
- **[GOTCHAS.md](./GOTCHAS.md)** - All 10 common pitfalls with detailed solutions
- **[REFERENCE.md](./REFERENCE.md)** - Architecture diagrams, API reference, feature matrix

## Production Deployment Checklist

Before deploying multi-agent systems:

- [ ] Define agent roles and responsibilities
- [ ] Design communication protocols (sync vs async)
- [ ] Implement agent registration and discovery
- [ ] Set up health monitoring and alerts
- [ ] Configure timeouts for all operations
- [ ] Implement consensus mechanisms for critical decisions
- [ ] Set up distributed tracing (trace ID propagation)
- [ ] Add circuit breakers for agent-to-agent calls
- [ ] Implement agent authentication/authorization
- [ ] Configure resource limits (CPU, memory, concurrency)
- [ ] Set up dead letter queues for failed messages
- [ ] Implement agent versioning and compatibility
- [ ] Add metrics and dashboards for agent performance
- [ ] Test failure scenarios (agent crashes, network partition)
- [ ] Document agent handoff protocols
- [ ] Implement graceful shutdown procedures

## Related Skills

- `orchestration-coordination-framework` - General orchestration patterns
- `evaluation-reporting-framework` - Evaluating multi-agent performance
- `mcp-integration-toolkit` - Agent communication via MCP
- `ai-evaluation-suite` - Testing agent interactions
- `architecture-evaluation-framework` - System architecture assessment

## Quick Reference

### Key Concepts
- **Agent**: Autonomous entity that can perceive, decide, and act
- **Coordinator**: Agent that orchestrates other agents
- **Consensus**: Agreement mechanism among multiple agents
- **State**: Shared or distributed data accessed by agents
- **Handoff**: Transfer of control from one agent to another

### Framework URLs
- [LangGraph Docs](https://python.langchain.com/docs/langgraph)
- [AutoGen Docs](https://microsoft.github.io/autogen/)
- [CrewAI Docs](https://docs.crewai.com/)
- [FIPA Standards](http://www.fipa.org/)

### Common Tasks
- **Create supervisor agent**: See [Example 1](./EXAMPLES.md#example-1-langgraph-supervisor)
- **Implement voting**: See [Example 4](./EXAMPLES.md#example-4-consensus-voting)
- **Manage shared state**: See [Example 5](./EXAMPLES.md#example-5-event-sourcing)
- **Auto-scale agents**: See [Example 6](./EXAMPLES.md#example-6-lifecycle-management)
- **Debug agent interactions**: See [GOTCHAS.md](./GOTCHAS.md#debugging-strategies)
