---
name: ai-agent-frameworks
description: Expert guidance on building production-ready multi-agent AI systems using CrewAI, LangChain, AutoGen, and custom architectures. Use when building agent systems, selecting frameworks, designing multi-agent workflows, debugging agent behavior, or deploying agents to production.
---

# AI Agent Frameworks Skill

## When to Use This Skill

Invoke this skill when working with multi-agent AI systems, including:

- Selecting between CrewAI, LangChain, AutoGen, LangGraph, or custom agent architectures
- Designing multi-agent collaboration patterns
- Implementing agent workflows with proper observability
- Debugging stuck agents, infinite loops, or runaway costs
- Integrating agents with MCP servers and external tools
- Deploying agent systems to production
- Recognizing when agents add unnecessary complexity

## Framework Selection Decision Process

### Decision Tree

Start by determining if agents are truly needed:

**Question 1: Is multi-step reasoning or tool orchestration required?**
- If NO → Use a single LLM call or simple chain
- If YES → Continue

**Question 2: Does the workflow map to clear team roles (research, write, edit)?**
- If YES → Prefer **CrewAI** for its role-based simplicity
- If NO → Continue

**Question 3: Is RAG (Retrieval-Augmented Generation) central to the application?**
- If YES → Prefer **LangChain** for best-in-class RAG capabilities
- If NO → Continue

**Question 4: Do agents need conversational debate or consensus-reaching?**
- If YES → Consider **AutoGen** for conversation patterns
- If NO → Continue

**Question 5: Does the workflow require complex state machines with loops and branching?**
- If YES → Consider **LangGraph** for stateful control
- If NO → Continue

**Question 6: Are minimal dependencies and maximum control essential?**
- If YES → Build **custom** agent system
- If NO → Default to **LangChain** (most versatile)

### Quick Framework Comparison Reference

For detailed comparisons, refer to `references/framework-comparison.md`

- **CrewAI**: Best for role-based teams, sequential workflows, quick prototypes
- **LangChain**: Best for RAG, extensive integrations, production tooling (LangSmith)
- **AutoGen**: Best for conversational agents, code execution, research projects
- **LangGraph**: Best for complex stateful workflows requiring loops and retries
- **Custom**: Best for simple use cases, performance-critical systems, unique requirements

## Agent Architecture Patterns

### Single-Agent vs Multi-Agent Criteria

Use **single agent** when:
- Task is straightforward with clear steps
- No benefit from specialization
- Cost and complexity must be minimized

Use **multi-agent** when:
- Tasks benefit from specialized expertise (research vs writing vs review)
- Parallel execution would improve performance
- Different agents need different models or tools
- Workflow involves handoffs or collaboration

### Common Orchestration Patterns

**Sequential Pattern:**
```
Agent A → Agent B → Agent C
```
- Use when each step depends on previous output
- Examples: Research → Write → Edit → Publish

**Parallel Pattern:**
```
      → Agent A →
Input → Agent B → Merge → Output
      → Agent C →
```
- Use when tasks are independent and can run concurrently
- Examples: Parallel research from multiple sources

**Hierarchical Pattern:**
```
     Manager Agent
    /      |      \
Agent A  Agent B  Agent C
```
- Use when dynamic task allocation is needed
- Manager delegates and coordinates

**Conversational Pattern:**
```
Agent A ⟷ Agent B ⟷ Agent C
```
- Use for debate, consensus, or iterative refinement
- Common in AutoGen workflows

## Framework-Specific Guidance

### When Working with CrewAI

Refer to `references/crewai-patterns.md` for comprehensive patterns.

**Key principles:**
- Design agents with specific roles (not generic "helper")
- Keep 2-5 agents per workflow (avoid over-engineering)
- Use sequential process for predictable workflows
- Use hierarchical process when dynamic delegation is needed
- Set `max_iterations` to prevent runaway costs

**Common anti-pattern to avoid:**
```python
# ❌ Don't: Vague agents with overlapping responsibilities
agent = Agent(role="Helper", goal="Help with stuff")

# ✅ Do: Specific agents with clear boundaries
researcher = Agent(
    role="Technical Researcher",
    goal="Find accurate data on Python frameworks",
    tools=[search_tool, docs_tool]
)
```

### When Working with LangChain

Refer to `references/langchain-patterns.md` for comprehensive patterns.

**Key principles:**
- Always set `max_iterations` on AgentExecutor to prevent loops
- Use LCEL (`|` operator) for composing chains
- Enable LangSmith tracing in production
- Implement proper error handling with `handle_parsing_errors=True`
- Consider using GPT-3.5-turbo for simple agents to reduce costs

**RAG pattern (common use case):**
```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True
)
```

**Critical: Always limit iterations:**
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=10,  # REQUIRED
    max_execution_time=60,
    handle_parsing_errors=True
)
```

### When Working with AutoGen

Refer to `references/autogen-patterns.md` for comprehensive patterns.

**Key principles:**
- Always use Docker for code execution in production (`use_docker=True`)
- Set `max_round` on GroupChat to prevent infinite conversations
- Use `human_input_mode` appropriately (NEVER, TERMINATE, or ALWAYS)
- Keep group chats to 3-5 agents maximum
- Track token usage as conversations can be expensive

**Safe code execution:**
```python
user_proxy = UserProxyAgent(
    name="executor",
    code_execution_config={
        "use_docker": True,  # CRITICAL for production
        "timeout": 60
    }
)
```

### When Building Custom Agents

Refer to `references/custom-agent-guide.md` for complete implementations.

**Build custom when:**
- Single-purpose agent with minimal complexity
- Framework overhead is unjustified
- Need maximum performance control
- Learning exercise to understand agents deeply

**Minimal implementation pattern:**
1. Prompt template
2. LLM client with retry logic
3. Tool execution with error handling
4. Response parsing

**Production-ready custom agent includes:**
- Timeout protection
- Retry logic with exponential backoff
- Cost tracking
- Comprehensive logging
- Circuit breakers for external APIs

## Debugging Stuck or Looping Agents

### Detection Strategies

**Loop detection:**
- Track action history (last 3-5 actions)
- Alert when same action repeats consecutively
- Implement max_iterations as hard stop

**Stuck detection:**
- Set execution timeouts (30-60 seconds per agent)
- Monitor for agents waiting indefinitely
- Check for missing tool results

**Tools available:**
- Use `scripts/agent-debugger.py` to analyze trace files
- Examine span durations to identify bottlenecks
- Look for repeated patterns in execution logs

### Common Causes and Solutions

**Cause:** Agent keeps calling the same tool with same parameters
**Solution:** Improve prompt to guide agent away from repetition, implement action history in context

**Cause:** Agent waiting for tool that never completes
**Solution:** Add timeouts to all tool calls, implement circuit breakers

**Cause:** Agent confused about when to terminate
**Solution:** Clear termination conditions, explicit TERMINATE signals

## Tool Integration Best Practices

### MCP Server Integration

When integrating MCP servers with agent frameworks:

**With LangChain:**
```python
from langchain.tools import Tool

# Wrap MCP server function as LangChain tool
mcp_tool = Tool(
    name="mcp_server_query",
    func=mcp_server.query,
    description="Query the MCP server for data"
)

# Add to agent
agent = create_openai_functions_agent(llm, tools=[mcp_tool], prompt=prompt)
```

**With CrewAI:**
- Define MCP functions as @tool decorated functions
- Register with specific agents that need MCP access

**General principles:**
- Always handle MCP server errors gracefully (return error strings, not exceptions)
- Set timeouts on MCP calls (don't let agents hang)
- Log all MCP interactions for debugging

### Tool Error Handling Pattern

```python
@tool
def resilient_tool(query: str) -> str:
    """Tool with proper error handling"""
    try:
        result = external_api.call(query, timeout=10)
        return json.dumps(result)
    except TimeoutError:
        return "Error: Request timed out. Please try again."
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return f"Error: {str(e)}"
```

**Never let tools crash the agent** - always return strings, even for errors.

## Cost Optimization

### Estimation Before Building

Use `scripts/cost-estimator.py` to estimate costs before implementing:

```bash
python scripts/cost-estimator.py --config workflow.json --requests 1000 --optimize
```

### Optimization Strategies

**1. Use cheaper models for simple agents:**
- GPT-4 for complex reasoning (strategist, analyst)
- GPT-3.5-turbo for simple tasks (formatter, router)

**2. Limit iterations strictly:**
- Set `max_iterations` to 5-10 (not 50)
- Set `max_execution_time` to prevent runaway costs

**3. Cache repeated work:**
- Enable LLM response caching
- Store results of expensive operations
- Reuse research across similar queries

**4. Implement budgets:**
```python
cost_tracker = CostTracker()
if cost_tracker.total_cost > budget:
    raise BudgetExceededError()
```

**5. Monitor costs in real-time:**
- Track token usage per agent
- Alert when costs approach thresholds
- Analyze cost breakdowns to identify expensive agents

## Production Deployment Considerations

Refer to `references/production-patterns.md` for deployment architectures and `references/observability-guide.md` for monitoring.

### Essential Production Patterns

**1. Async Task Queue (Recommended):**
- Use Celery + Redis for long-running workflows
- Return task ID immediately, poll for results
- Enables horizontal scaling

**2. Always Enable Observability:**
- Structured logging (JSON format)
- Distributed tracing (OpenTelemetry or LangSmith)
- Cost tracking per request
- Error monitoring (Sentry)

**3. Implement Fault Tolerance:**
- Retry with exponential backoff
- Circuit breakers for external APIs
- Graceful degradation (fallback to cheaper models)

**4. Security:**
- API authentication (JWT tokens)
- Rate limiting (10-100 requests/minute per user)
- Input validation (prevent prompt injection)
- Sandboxed code execution (Docker for AutoGen)

**5. Set Hard Limits:**
```python
LIMITS = {
    "max_iterations": 10,
    "max_execution_time": 60,  # seconds
    "max_cost_per_request": 1.0,  # USD
    "max_concurrent_agents": 5
}
```

## Anti-Patterns to Avoid

### ❌ Over-Engineering with Agents

**Problem:** Using multiple agents when a single LLM call would suffice

**Example:**
```python
# ❌ Overkill for simple task
agents = [InputParser(), Processor(), OutputFormatter()]
# Just to format text!
```

**Solution:** Start simple. One LLM call. Add agents only when truly beneficial.

### ❌ No Termination Conditions

**Problem:** Agents run forever or hit arbitrary iteration limits

**Solution:**
```python
# ✅ Always set termination conditions
max_iterations=10
is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "")
```

### ❌ Vague Agent Roles

**Problem:** Agents with unclear responsibilities cause overlap and confusion

**Solution:** Specific roles with clear boundaries. "Senior Python Developer" not "Helper".

### ❌ Ignoring Costs

**Problem:** Running expensive models without tracking or budgets

**Solution:** Track costs per request, set budgets, alert on anomalies

### ❌ No Observability

**Problem:** Can't debug when things go wrong

**Solution:** Implement logging, tracing, and metrics from day one

## When NOT to Use Agents

Recognize situations where agents add unnecessary complexity:

**Use a single LLM call instead of agents when:**
- Task is straightforward (translation, summarization, Q&A)
- No tool usage required
- Single-step reasoning suffices
- Cost and latency must be minimized

**Example decision:**
- "Translate this text" → Single LLM call
- "Research 10 sources and synthesize findings" → Multi-agent system

## Resource Reference Guide

This skill includes comprehensive reference materials. Load them as needed:

### Framework Comparisons
- **`references/framework-comparison.md`** - Detailed CrewAI vs LangChain vs AutoGen comparison with migration paths

### Framework-Specific Patterns
- **`references/crewai-patterns.md`** - Role design, task patterns, processes, production tips
- **`references/langchain-patterns.md`** - LCEL chains, RAG patterns, LangGraph workflows
- **`references/autogen-patterns.md`** - Conversational agents, group chats, code execution

### Advanced Topics
- **`references/custom-agent-guide.md`** - Building agents from scratch, minimal implementations
- **`references/observability-guide.md`** - Tracing, logging, metrics, debugging tools
- **`references/production-patterns.md`** - Deployment architectures, scaling, security, monitoring

### Helper Scripts
- **`scripts/cost-estimator.py`** - Estimate workflow costs before building
- **`scripts/agent-debugger.py`** - Analyze traces to identify loops and bottlenecks
- **`scripts/agent-system-template/`** - Boilerplate for new agent systems

## Getting Started Workflow

For new agent system development:

1. **Validate need for agents** - Can this be solved with a single LLM call?
2. **Choose framework** - Use decision tree above
3. **Estimate costs** - Run cost-estimator.py with expected workflow
4. **Implement with observability** - Enable logging/tracing from start
5. **Test for loops** - Use agent-debugger.py on traces
6. **Set hard limits** - max_iterations, budgets, timeouts
7. **Monitor in production** - Track costs, errors, performance

## Framework-Specific Quick References

### CrewAI Essentials
- Agents need: role, goal, backstory, tools
- Tasks need: description, expected_output, agent
- Processes: Sequential (linear) or Hierarchical (manager delegates)
- Limit: 2-5 agents per crew

### LangChain Essentials
- Always set max_iterations on AgentExecutor
- Use LCEL for chain composition: `prompt | model | parser`
- Enable LangSmith for production: `LANGCHAIN_TRACING_V2=true`
- RAG: Use RetrievalQA or ConversationalRetrievalChain

### AutoGen Essentials
- UserProxyAgent executes code, AssistantAgent generates it
- Always use Docker in production: `use_docker=True`
- GroupChat needs max_round limit
- Human input modes: NEVER (autonomous), TERMINATE (confirm end), ALWAYS (every step)

### LangGraph Essentials
- Define state, nodes (functions), and edges (transitions)
- Use conditional edges for branching logic
- Supports cycles (retries, loops)
- Requires StateGraph setup and compilation

## Summary

Multi-agent systems add complexity. Use this skill to:

✅ Make informed framework selections
✅ Design effective agent architectures
✅ Avoid common pitfalls (loops, runaway costs)
✅ Implement production-ready observability
✅ Recognize when agents are overkill

Prioritize simplicity. Start with the minimum viable agent system. Add complexity only when justified by concrete benefits.
