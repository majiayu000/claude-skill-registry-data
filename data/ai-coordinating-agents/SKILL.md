---
name: ai-coordinating-agents
description: Build multiple AI agents that work together. Use when you need a supervisor agent that delegates to specialists, agent handoff, parallel research agents, support escalation (L1 to L2), content pipeline (writer + editor + fact-checker), or any multi-agent system. Also used for CrewAI alternative, AutoGen alternative, LangGraph multi-agent, agents that talk to each other, specialist agents with a supervisor, agents keep stepping on each other, build an AI team, route tasks to the right agent, when one agent is not enough, parallel agents for research.
---

# Build Multi-Agent Systems

Guide the user through building multiple AI agents that collaborate — a supervisor delegates tasks, specialists handle their domains, and results flow back. Uses DSPy for each agent's reasoning and LangGraph for orchestration, handoff, and parallel execution.

## Step 1: Identify the agents

Ask the user:
1. **What's the overall task?** (research a topic, handle support, create content, analyze data?)
2. **What specialist roles do you need?** (researcher, writer, reviewer, analyst, etc.)
3. **How do agents hand off work?** (supervisor routes, chain passes forward, parallel fan-out?)
4. **Do any agents need tools?** (search, database, APIs, code execution?)

### Common multi-agent patterns

| Pattern | How it works | Good for |
|---------|-------------|----------|
| **Supervisor** | Central agent routes tasks to specialists | Support triage, research coordination |
| **Chain** | Agent A → Agent B → Agent C in sequence | Content pipelines (write → edit → review) |
| **Parallel** | Multiple agents work simultaneously, merge results | Research (search multiple sources at once) |
| **Hierarchical** | Supervisor → sub-supervisors → specialists | Complex organizations with many agents |

## Step 2: Build each agent as a DSPy module

Each agent gets its own signature, reasoning strategy, and (optionally) tools.

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)
```

### Simple agent — just a DSPy module

```python
import dspy

class ResearchSummary(dspy.Signature):
    """Research the topic and provide a detailed summary with key findings."""
    topic: str = dspy.InputField()
    sources: list[str] = dspy.InputField(desc="Search results or documents to analyze")
    summary: str = dspy.OutputField(desc="Detailed research summary")
    key_findings: list[str] = dspy.OutputField(desc="Top 3-5 key findings")

class ResearchAgent(dspy.Module):
    def __init__(self, retriever):
        self.retriever = retriever
        self.analyze = dspy.ChainOfThought(ResearchSummary)

    def forward(self, topic):
        sources = self.retriever(topic).passages
        return self.analyze(topic=topic, sources=sources)
```

### Agent with tools — use ReAct

```python
def search_web(query: str) -> str:
    """Search the web for current information."""
    # your search implementation
    return results

def query_database(sql: str) -> str:
    """Query the analytics database."""
    # your database implementation
    return results

class DataAnalyst(dspy.Module):
    def __init__(self):
        self.agent = dspy.ReAct(
            "question, context -> analysis, recommendation",
            tools=[search_web, query_database],
            max_iters=5,
        )

    def forward(self, question, context=""):
        return self.agent(question=question, context=context)
```

### Agent with LangChain tools

Convert pre-built LangChain tools for use in DSPy agents:

```python
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = dspy.Tool.from_langchain(DuckDuckGoSearchRun())

class WebResearcher(dspy.Module):
    def __init__(self):
        self.agent = dspy.ReAct(
            "question -> findings",
            tools=[search_tool],
            max_iters=5,
        )

    def forward(self, question):
        return self.agent(question=question)
```

## Step 3: Add a supervisor (LangGraph)

The supervisor decides which agent to call next based on the current state.

### Define the shared state

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

class TeamState(TypedDict):
    task: str                                     # the overall task
    messages: Annotated[list[dict], operator.add]  # communication log
    current_agent: str                             # who's working now
    results: dict                                  # collected results from agents
    status: str                                    # "in_progress", "done", "needs_review"
```

### Build the supervisor

```python
class RouteTask(dspy.Signature):
    """Decide which specialist agent should handle the next step."""
    task: str = dspy.InputField(desc="The overall task")
    completed_work: str = dspy.InputField(desc="Work completed so far")
    available_agents: list[str] = dspy.InputField()
    next_agent: str = dspy.OutputField(desc="Which agent to call next")
    sub_task: str = dspy.OutputField(desc="Specific instruction for that agent")
    is_complete: bool = dspy.OutputField(desc="Whether the overall task is done")

supervisor_module = dspy.ChainOfThought(RouteTask)

def supervisor(state: TeamState) -> dict:
    completed = "\n".join(
        f"{k}: {v}" for k, v in state["results"].items()
    )
    result = supervisor_module(
        task=state["task"],
        completed_work=completed or "Nothing yet",
        available_agents=["researcher", "writer", "reviewer"],
    )

    if result.is_complete:
        return {"status": "done", "current_agent": "none"}

    return {
        "current_agent": result.next_agent,
        "messages": [{"role": "supervisor", "content": f"@{result.next_agent}: {result.sub_task}"}],
    }
```

### Wire up the agents as graph nodes

```python
researcher = ResearchAgent(retriever=my_retriever)
writer_module = dspy.ChainOfThought(WriteContent)
reviewer_module = dspy.ChainOfThought(ReviewContent)

def researcher_node(state: TeamState) -> dict:
    task_msg = state["messages"][-1]["content"]
    result = researcher(topic=task_msg)
    return {
        "results": {**state["results"], "research": result.summary},
        "messages": [{"role": "researcher", "content": result.summary}],
    }

def writer_node(state: TeamState) -> dict:
    result = writer_module(
        task=state["task"],
        research=state["results"].get("research", ""),
    )
    return {
        "results": {**state["results"], "draft": result.output},
        "messages": [{"role": "writer", "content": result.output}],
    }

def reviewer_node(state: TeamState) -> dict:
    result = reviewer_module(
        draft=state["results"].get("draft", ""),
        task=state["task"],
    )
    return {
        "results": {**state["results"], "review": result.feedback},
        "messages": [{"role": "reviewer", "content": result.feedback}],
    }
```

### Build the graph

```python
graph = StateGraph(TeamState)

# Add nodes
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)
graph.add_node("reviewer", reviewer_node)

# Supervisor decides who goes next
graph.add_edge(START, "supervisor")

def route_to_agent(state: TeamState) -> str:
    if state["status"] == "done":
        return "done"
    return state["current_agent"]

graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "researcher": "researcher",
        "writer": "writer",
        "reviewer": "reviewer",
        "done": END,
    },
)

# All agents report back to supervisor
graph.add_edge("researcher", "supervisor")
graph.add_edge("writer", "supervisor")
graph.add_edge("reviewer", "supervisor")

app = graph.compile()
```

### Run it

```python
result = app.invoke({
    "task": "Write a blog post about the benefits of remote work",
    "messages": [],
    "current_agent": "",
    "results": {},
    "status": "in_progress",
})
# Supervisor routes: researcher → writer → reviewer → done
print(result["results"]["draft"])
```

## Step 4: Agent handoff pattern

When one agent passes work directly to another (no supervisor).

### Shared context via state

```python
class HandoffState(TypedDict):
    task: str
    context: Annotated[list[str], operator.add]  # accumulated context
    output: str

def agent_a(state: HandoffState) -> dict:
    result = module_a(task=state["task"])
    return {"context": [f"Agent A found: {result.output}"]}

def agent_b(state: HandoffState) -> dict:
    full_context = "\n".join(state["context"])
    result = module_b(task=state["task"], context=full_context)
    return {"context": [f"Agent B added: {result.output}"]}

def agent_c(state: HandoffState) -> dict:
    full_context = "\n".join(state["context"])
    result = module_c(task=state["task"], context=full_context)
    return {"output": result.output}

graph = StateGraph(HandoffState)
graph.add_node("a", agent_a)
graph.add_node("b", agent_b)
graph.add_node("c", agent_c)
graph.add_edge(START, "a")
graph.add_edge("a", "b")
graph.add_edge("b", "c")
graph.add_edge("c", END)
```

### Conditional handoff

Route to different specialists based on intermediate results:

```python
def route_after_classify(state) -> str:
    if state["category"] == "billing":
        return "billing_specialist"
    elif state["category"] == "technical":
        return "tech_specialist"
    return "general_agent"

graph.add_conditional_edges("classifier", route_after_classify, {
    "billing_specialist": "billing",
    "tech_specialist": "tech",
    "general_agent": "general",
})
```

## Step 5: Parallel agents

Fan out to multiple agents simultaneously and merge results.

```python
from langgraph.constants import Send

class ParallelState(TypedDict):
    task: str
    subtasks: list[str]
    results: Annotated[list[dict], operator.add]
    final_output: str

def split_task(state: ParallelState) -> list:
    """Fan out subtasks to worker agents."""
    return [Send("worker", {"task": state["task"], "subtask": st}) for st in state["subtasks"]]

def worker(state: dict) -> dict:
    """Each worker handles one subtask."""
    worker_module = dspy.ChainOfThought("task, subtask -> result")
    result = worker_module(task=state["task"], subtask=state["subtask"])
    return {"results": [{"subtask": state["subtask"], "result": result.result}]}

def merge_results(state: ParallelState) -> dict:
    """Combine all worker results into a final output."""
    merger = dspy.ChainOfThought("task, partial_results -> final_output")
    partial = "\n".join(f"- {r['subtask']}: {r['result']}" for r in state["results"])
    result = merger(task=state["task"], partial_results=partial)
    return {"final_output": result.final_output}

graph = StateGraph(ParallelState)
graph.add_node("worker", worker)
graph.add_node("merge", merge_results)
graph.add_conditional_edges(START, split_task)
graph.add_edge("worker", "merge")
graph.add_edge("merge", END)
```

## Step 6: Human-in-the-loop

Pause before agents take critical actions.

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

# Interrupt before any agent that takes external actions
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_action", "send_email", "update_database"],
)

config = {"configurable": {"thread_id": "task-001"}}

# Run until interrupt
result = app.invoke(input_state, config)
# -> Pauses before "execute_action" node

# Human reviews the proposed action in result state
print(result["proposed_action"])

# If approved, resume from checkpoint
result = app.invoke(None, config)
```

## Step 7: Optimize the team

### Per-agent metrics

Optimize each agent's prompts independently first:

```python
def researcher_metric(example, prediction, trace=None):
    """Are the research findings relevant and complete?"""
    judge = dspy.Predict(JudgeResearch)
    return judge(topic=example.topic, findings=prediction.summary).is_good

optimizer = dspy.MIPROv2(metric=researcher_metric, auto="light")
optimized_researcher = optimizer.compile(researcher, trainset=research_trainset)
```

### End-to-end team metric

Then optimize all agents together with a team-level metric:

```python
def team_metric(example, prediction, trace=None):
    """Is the final output high quality?"""
    judge = dspy.Predict(JudgeOutput)
    return judge(
        task=example.task,
        expected=example.output,
        actual=prediction.final_output,
    ).is_good

# Create a module that wraps the full team
class TeamModule(dspy.Module):
    def __init__(self):
        self.supervisor = supervisor_module
        self.researcher = optimized_researcher
        self.writer = writer_module
        self.reviewer = reviewer_module

    def forward(self, task):
        # Run the LangGraph app
        result = app.invoke({"task": task, "messages": [], "current_agent": "", "results": {}, "status": "in_progress"})
        return dspy.Prediction(final_output=result["results"].get("draft", ""))

optimizer = dspy.MIPROv2(metric=team_metric, auto="medium")
optimized_team = optimizer.compile(TeamModule(), trainset=team_trainset)
```

### Verify improvement

Run a small held-out test set through both graphs to confirm the optimization helped before deploying:

```python
from dspy.evaluate import Evaluate
evaluator = Evaluate(devset=test_examples, metric=team_metric, num_threads=2)
baseline_score = evaluator(TeamModule())
optimized_score = evaluator(optimized_team)
print(f"Baseline: {baseline_score:.1%}  →  Optimized: {optimized_score:.1%}")
# Per-agent optimization alone typically lifts team output quality 15-30%.
# Team-level optimization on top adds another 5-15%.
# If the gap is under 5%, the team metric may not be discriminating enough.
```

## When NOT to use multi-agent

Multi-agent adds orchestration complexity. Consider simpler alternatives first:

- **One agent can do the job** — if your task needs tools but not multiple specialists, use a single `dspy.ReAct` agent (see `/ai-taking-actions`). A single agent with 5 tools is simpler than 3 agents with 2 tools each.
- **Fixed pipeline with no routing** — if agents always run in the same order (write → edit → review) with no conditional branching, a plain DSPy pipeline module is simpler than LangGraph (see `/ai-building-pipelines`).
- **You are over-specializing** — if each "agent" is just a single `dspy.Predict` call with no tools or state, you do not need agents. Use a multi-step DSPy module instead.

Use multi-agent when you genuinely need dynamic routing (supervisor decides who goes next), parallel execution (fan-out to multiple specialists), or human-in-the-loop checkpoints between steps.

## Gotchas

- **Claude puts orchestration logic inside DSPy modules.** Routing decisions, agent selection, and state transitions belong in LangGraph (conditional edges, `route_to_agent`). DSPy modules should only handle the reasoning each agent does — classify, research, write, review. If `forward()` contains `if agent == "writer"` branching, move that logic to LangGraph edges.
- **Claude creates one giant shared state with every field.** Each agent only needs a few fields from the state. A bloated `TypedDict` with 15+ fields makes the graph hard to debug and wastes context. Keep the shared state minimal — `task`, `messages`, `results`, `status` — and let agents pass specifics through the `results` dict.
- **Claude forgets to cap supervisor iterations.** Without a limit, the supervisor can loop forever — routing researcher → writer → reviewer → researcher indefinitely. Add a `max_steps` counter to the state and a check in the supervisor that forces `is_complete = True` after N iterations (typically 5-10).
- **Claude optimizes the full team before individual agents.** Multi-agent optimization is expensive and hard to debug. Always optimize each agent independently first (with per-agent metrics), then freeze the good ones and optimize the team end-to-end. This bottom-up approach is faster and produces better results.
- **Claude uses `dspy.Parallel` when it should use LangGraph `Send()`.** `dspy.Parallel` is for independent LM calls within a single module. For parallel agents with different roles, tools, and state, use LangGraph's `Send()` pattern — it gives you proper state management, error handling, and the ability to interrupt individual agents.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Single agent with tools** — start here instead of multi-agent if one agent suffices -- see `/ai-taking-actions`
- **Stateless pipelines** — when agents always run in the same order without routing -- see `/ai-building-pipelines`
- **Conversational agents** — if agents need to hold multi-turn conversations -- see `/ai-building-chatbots`
- **Measure and improve agents** — evaluate and optimize your multi-agent system -- see `/ai-improving-accuracy`
- **ReAct agents** — the DSPy module powering tool-using agents -- see `/dspy-react`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples (research team, support escalation), see [examples.md](examples.md)
- For API signatures (dspy.ReAct, dspy.Refine, LangGraph StateGraph, Send), see [reference.md](reference.md)
- [LangGraph documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
