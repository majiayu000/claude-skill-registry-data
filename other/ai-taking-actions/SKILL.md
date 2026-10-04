---
name: ai-taking-actions
description: Build AI that takes actions, calls APIs, and does things autonomously. Use when you need AI to call APIs, use tools, perform calculations, search the web and act on results, interact with databases, or do multi-step tasks. Also AI that does things not just talks, tool-using AI agent, AI calls external APIs, function calling with DSPy, build AI that books appointments, AI workflow automation, agent that searches and acts on results, AI that updates databases, autonomous AI agent, AI performs multi-step tasks, give LLM access to tools, agentic AI workflow, AI agent for DevOps, build AI assistant that takes actions, MCP tool integration with AI, AI that can browse and click, LLM with tool access.
---

# Build AI That Takes Actions

Guide the user through building AI that reasons and takes actions — calling APIs, using tools, and completing multi-step tasks. Uses DSPy's ReAct and CodeAct agent modules.

## Step 1: Understand the use case

Ask the user:
1. **What should the AI do?** (answer questions, call APIs, perform calculations, search, etc.)
2. **What tools does it need?** (calculator, search, database, APIs, file system, etc.)
3. **How many steps might it take?** (simple tool call vs. multi-step reasoning)

## Step 2: Define tools

Tools are Python functions with type hints and docstrings. DSPy uses these to tell the AI what's available:

```python
def search(query: str) -> str:
    """Search the web for information."""
    # Your search implementation
    return "search results..."

def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return dspy.PythonInterpreter().execute(expression)

def lookup_database(table: str, query: str) -> str:
    """Query the database for records matching the query."""
    # Your database logic
    return "query results..."
```

**Tool requirements:**
- Type hints on all parameters and return type
- Docstring explaining what the tool does
- Return a string (or something that converts to string)

## Step 3: Build the AI

### Choose your agent module

| | ReAct | CodeAct |
|---|---|---|
| **Best for** | General tool-calling (APIs, search, databases) | Tasks where writing code is more natural (math, data transforms) |
| **How it works** | Alternates thinking and tool calls | Writes and executes Python code with tool access |
| **Tool types** | Any callable, `dspy.Tool`, LangChain tools | Pure functions only (no callable objects or external deps) |
| **Default max_iters** | 20 | 5 |
| **Start here?** | Yes — most general-purpose | When the task is inherently code-centric |

### ReAct (Reasoning + Acting) — start here

The standard choice. Alternates between thinking and acting:

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

agent = dspy.ReAct(
    "question -> answer",
    tools=[search, calculate],
    max_iters=8,  # default is 20; lower for simple tasks to save cost
)

result = agent(question="What is the population of France divided by 3?")
print(result.answer)
```

### CodeAct — for code-heavy tasks

Writes and executes Python code. Only accepts **pure functions** as tools — no callable objects or undeclared dependencies:

```python
agent = dspy.CodeAct(
    "question -> answer",
    tools=[calculate],  # pure functions only
    max_iters=5,  # default is 5
)

result = agent(question="Calculate the compound interest on $1000 at 5% for 10 years")
print(result.answer)
```

### Custom AI with state

```python
class ResearchBot(dspy.Module):
    def __init__(self):
        self.agent = dspy.ReAct(
            "question, context -> answer",
            tools=[search, lookup_database],
            max_iters=8,
        )

    def forward(self, question):
        # Add initial context or pre-processing
        context = "Use search for general questions, database for specific records."
        return self.agent(question=question, context=context)
```

## Step 4: Test the quality

```python
def action_metric(example, prediction, trace=None):
    # Check if the final answer is correct
    return prediction.answer.strip().lower() == example.answer.strip().lower()

# For open-ended tasks, use an AI judge
class JudgeResult(dspy.Signature):
    """Judge if the AI's answer correctly addresses the question."""
    question: str = dspy.InputField()
    expected: str = dspy.InputField()
    actual: str = dspy.InputField()
    is_correct: bool = dspy.OutputField()

def judge_metric(example, prediction, trace=None):
    judge = dspy.Predict(JudgeResult)
    result = judge(
        question=example.question,
        expected=example.answer,
        actual=prediction.answer,
    )
    return result.is_correct
```

## Step 5: Improve accuracy

```python
# Optimize the AI's reasoning prompts
optimizer = dspy.BootstrapFewShot(metric=action_metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(agent, trainset=trainset)
```

For action-taking AI, `MIPROv2` often works better since it can optimize the reasoning instructions:

```python
optimizer = dspy.MIPROv2(metric=action_metric, auto="medium")
optimized = optimizer.compile(agent, trainset=trainset)
```

Typical improvement: BootstrapFewShot raises task success from ~55% to ~75%; MIPROv2 can reach ~85%+ by tuning the reasoning instructions themselves.

## Using LangChain tools

LangChain has 100+ pre-built tools (search engines, Wikipedia, SQL databases, web scrapers, etc.). Convert any of them to DSPy tools with one line:

```python
import dspy
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Convert LangChain tools to DSPy tools
search = dspy.Tool.from_langchain(DuckDuckGoSearchRun())
wikipedia = dspy.Tool.from_langchain(WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()))

# Use in any DSPy agent
agent = dspy.ReAct(
    "question -> answer",
    tools=[search, wikipedia],
    max_iters=5,
)
```

**When to use LangChain tools vs writing your own:**

| Use LangChain tools when... | Write your own when... |
|------------------------------|------------------------|
| There's an existing tool for it (search, Wikipedia, SQL) | You need custom business logic |
| You want quick prototyping | You need tight error handling |
| The tool wraps a standard API | You're wrapping an internal API |

Install the tools you need:

```bash
pip install langchain-community  # DuckDuckGo, Wikipedia, requests, etc.
```

For more LangChain tools, see the [LangChain community tools docs](https://python.langchain.com/docs/integrations/tools/).

## When NOT to use agents

- **Single-step tasks** — if the AI just needs to answer a question or classify text, use `dspy.Predict` or `dspy.ChainOfThought` instead. Agents add overhead (multiple LM calls per request).
- **Deterministic workflows** — if the steps are always the same, write the code yourself and use DSPy modules for the LM-powered steps only. Agents shine when the path depends on intermediate results.
- **Cost-sensitive applications** — each ReAct iteration is a separate LM call. A 5-step agent costs roughly 5x a single Predict call. Consider whether the task justifies this.

## Gotchas

- **Claude sets `max_iters=5` for ReAct but the default is 20.** The API default of 20 is generous — for most tasks, 5-10 iterations suffice. Set it explicitly to control cost, but do not assume 5 is the framework default.
- **CodeAct only accepts pure functions as tools.** Passing callable objects, class instances, or functions with undeclared dependencies will fail silently or error. If your tool has external deps, use ReAct instead.
- **Claude forgets to call `dspy.configure(lm=lm)` before creating agents.** The agent will fail at runtime with confusing errors if no LM is configured. Always configure the LM before instantiating any module.
- **Tool docstrings are the AI's only guidance on when to call each tool.** Vague docstrings like "do stuff" cause the agent to misroute. Write docstrings that describe what the tool does and when to use it, as if explaining to a colleague.
- **Claude wraps tool return values in complex objects instead of strings.** DSPy agents expect tools to return strings (or values that convert cleanly to strings). Returning dicts, lists, or custom objects can cause the agent to misinterpret results.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Multiple agents working together** — see `/ai-coordinating-agents`
- **Measure and improve accuracy** — see `/ai-improving-accuracy`
- **ReAct and CodeAct module details** — see `/dspy-react` or `/dspy-code-act` (if available)
- **Signatures for defining agent I/O** — see `/dspy-signatures`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For API signatures (ReAct, CodeAct, Tool, PythonInterpreter), see [reference.md](reference.md)
- For worked examples (calculator, search, APIs), see [examples.md](examples.md)
