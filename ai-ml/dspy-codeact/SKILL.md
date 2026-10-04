---
name: dspy-codeact
description: Build agents that write and execute Python code using dspy.CodeAct. Use when the task requires computation, data transformation, or multi-step logic better expressed as code than tool calls or natural language - data analysis, precise calculations, file processing. Common scenarios - data analysis tasks where the agent writes pandas code, computation-heavy tasks where natural language reasoning fails, file processing automation, tasks requiring precise calculations, or building agents that manipulate data programmatically. Related - ai-taking-actions, dspy-react, dspy-program-of-thought. Also used for dspy.CodeAct, agent writes and runs Python code, code execution agent, data analysis agent, AI agent that writes code, computation with LLM agent, pandas automation with AI, agent that processes files, code-generating agent, execute Python in sandbox, when ReAct is not precise enough use code, programmatic problem solving agent.
---

# Build Agents That Write and Execute Code with dspy.CodeAct

Guide the user through building DSPy agents that solve problems by generating and running Python code, rather than calling tools through a fixed interface.

## Step 1 — Gather context

Ask the user before writing code:

1. **What task should the agent perform?** (e.g., data analysis, math computation, file processing, custom calculation) — this guides tool design and `max_iters` choice.
2. **Do you have existing Python functions to expose as tools, or do they need to be defined?** CodeAct requires plain functions with type hints and docstrings — not classes or lambdas.
3. **What LM provider are you using?** Any DSPy-supported provider works — OpenAI, Anthropic, local models, etc.
4. **Will you optimize the agent on training examples, or use it for one-off tasks?** Optimization with BootstrapFewShot significantly improves performance on repeated tasks.

## What is CodeAct

`dspy.CodeAct` is a DSPy module that creates agents which write Python code to accomplish tasks. Instead of selecting from a predefined set of tool calls (like ReAct), CodeAct generates executable code snippets that use provided tools as Python functions.

The agent works in a loop:

1. **Generate** -- the LM writes a Python code snippet using the available tools
2. **Execute** -- the code runs in a sandboxed interpreter
3. **Observe** -- the agent sees the output and decides whether the task is done
4. **Repeat** -- if not done, writes more code incorporating previous results

CodeAct inherits from both ReAct and ProgramOfThought, combining reasoning-and-acting with code generation.

## How CodeAct differs from ReAct

| | ReAct | CodeAct |
|---|---|---|
| **How it acts** | Calls tools by name with arguments | Writes Python code that calls tools |
| **Composition** | One tool call per step | Can chain multiple tool calls, use loops, variables, conditionals in a single step |
| **Data manipulation** | Limited to what tools return | Can transform, filter, aggregate data in code |
| **Best for** | Simple tool orchestration | Complex computation, data processing, multi-step logic |
| **Overhead** | Lower -- just picks a tool | Higher -- generates and executes code |

**Rule of thumb:** If your agent needs to do math, transform data, or chain several operations together, CodeAct is a better fit. If it just needs to look things up and combine results, ReAct is simpler.

## When to use CodeAct

Use CodeAct when the agent needs computation, data transformation, or multi-step logic — see the decision table at the bottom of this skill for scenario-by-scenario guidance.

Avoid CodeAct when:

- Simple tool calls are sufficient (use ReAct instead)
- You need tight control over exactly which tools are called and in what order
- The execution environment cannot support sandboxed code execution
- You need to use external libraries like numpy or pandas inside tools (CodeAct tools cannot import external libraries)

## Basic usage

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# Define tools as pure functions with type hints and docstrings
def factorial(n: int) -> int:
    """Calculate the factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Create the CodeAct agent
agent = dspy.CodeAct(
    "question -> answer",
    tools=[factorial, fibonacci],
    max_iters=5,
)

result = agent(question="What is the factorial of 10 plus the 15th Fibonacci number?")
print(result.answer)
```

## Constructor parameters

```python
dspy.CodeAct(
    signature,          # str or dspy.Signature -- defines input/output fields
    tools,              # list[callable] -- pure functions the agent can call in code
    max_iters=5,        # int -- max generate-execute cycles before stopping
    interpreter=None,   # PythonInterpreter or None -- custom interpreter (creates one if None)
)
```

### Parameter details

- **`signature`** -- same as any DSPy module. Defines what the agent receives and what it should produce.
- **`tools`** -- a list of Python functions. Must be **pure functions** (not callable objects or class instances). All dependencies must be self-contained within each function -- tools cannot import external libraries or reference outside state.
- **`max_iters`** -- safety limit on how many code-generation-and-execution cycles the agent runs. Default is 5. Increase for complex multi-step tasks, decrease for simple ones.
- **`interpreter`** -- optionally pass a pre-configured `dspy.PythonInterpreter`. If `None`, CodeAct creates a fresh one. The interpreter runs code in a sandboxed Deno-based environment.

## Tool requirements

CodeAct is strict about what tools it accepts:

```python
# OK -- pure function
def search(query: str) -> str:
    """Search for information."""
    return "results..."

# OK -- function with multiple parameters
def lookup(table: str, key: str) -> str:
    """Look up a value in a table."""
    return "value..."

# NOT OK -- callable object (will be rejected)
class MyTool:
    def __call__(self, query: str) -> str:
        return "results..."

# NOT OK -- tool that imports external libraries
def analyze(data: str) -> str:
    """Analyze data."""
    import pandas as pd  # This will fail in the sandbox
    return str(pd.read_csv(data))
```

**Rules for tools:**

1. Must be plain functions (not callable objects, not class methods, not lambdas)
2. Must have type hints and a docstring
3. Cannot import external libraries (numpy, pandas, requests, etc.) inside the function body
4. All logic must be self-contained -- no references to external classes or global state
5. Dependencies must be explicitly passed as tools if the agent needs them

## Code execution environment

CodeAct runs generated code in a **sandboxed Deno-based Python interpreter**, not your system's Python. This means:

- **Isolation** -- code cannot access your filesystem, network, or environment variables
- **No external imports** -- standard library only within generated code; no pip packages
- **Tool access** -- the agent calls your tool functions, which execute in your normal Python environment. Only the glue code between tool calls runs in the sandbox.
- **State persistence** -- variables persist across iterations within a single agent call, so the agent can build up results incrementally

The sandbox provides security boundaries, but your tool functions themselves run in your normal Python process. If a tool accesses a database or API, that access is real.

## Safety considerations

1. **Tool functions are the trust boundary.** The sandbox constrains the generated glue code, but tool functions execute with full privileges. Keep tool functions minimal and validate their inputs.

2. **Set `max_iters` appropriately.** A runaway agent burns tokens. Start with `max_iters=5` and increase only if you see the agent running out of steps on legitimate tasks.

3. **Validate outputs.** Use `dspy.Refine` as a wrapper to check that the agent's answer meets your requirements via a reward function.

4. **Don't expose dangerous operations as tools.** If you pass a tool that deletes files or sends emails, the agent can and will call it. Only expose tools you're comfortable with the agent using autonomously.

```python
class SafeCodeAgent(dspy.Module):
    def __init__(self, tools):
        self.agent = dspy.CodeAct(
            "task -> result",
            tools=tools,
            max_iters=5,
        )

    def forward(self, task):
        return self.agent(task=task)

def non_empty_reward(args, pred):
    if len(pred.result.strip()) > 0:
        return 1.0
    return 0.0  # Agent must produce a non-empty result

validated_agent = dspy.Refine(
    module=SafeCodeAgent(tools=[]),
    N=3,
    reward_fn=non_empty_reward,
    threshold=1.0,
)
```

## Using CodeAct inside a custom module

Wrap CodeAct in a `dspy.Module` to add pre-processing, post-processing, or combine it with other DSPy modules:

```python
class AnalysisAgent(dspy.Module):
    def __init__(self):
        self.planner = dspy.ChainOfThought("task -> plan")
        self.executor = dspy.CodeAct(
            "task, plan -> result",
            tools=[compute_stats, format_table],
            max_iters=8,
        )
        self.summarize = dspy.ChainOfThought("task, result -> summary")

    def forward(self, task):
        plan = self.planner(task=task)
        execution = self.executor(task=task, plan=plan.plan)
        return self.summarize(task=task, result=execution.result)
```

## Optimizing CodeAct agents

CodeAct agents are optimizable like any DSPy module:

```python
def task_metric(example, prediction, trace=None):
    return prediction.answer.strip() == example.answer.strip()

# BootstrapFewShot works well -- the agent learns from successful code traces
optimizer = dspy.BootstrapFewShot(metric=task_metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(agent, trainset=trainset)

# MIPROv2 can also tune the instructions for code generation
optimizer = dspy.MIPROv2(metric=task_metric, auto="medium")
optimized = optimizer.compile(agent, trainset=trainset)

# Save and load
optimized.save("optimized_codeact.json")
```

## Verify the agent works

After building, run a concrete test and inspect the generated code:

```python
result = agent(question="What is the factorial of 10 plus the 15th Fibonacci number?")
print(result.answer)       # should be a computed number, not vague prose
dspy.inspect_history(n=1)  # see the code the agent generated and executed
```

If the agent produces reasoning text instead of executing code, check that all tools have type hints and docstrings — these are required for the agent to understand how to call them.

## When to use CodeAct vs ReAct

| Scenario | Use |
|---|---|
| Look up facts and combine them | ReAct |
| Calculate, aggregate, or transform data | **CodeAct** |
| Simple API calls (weather, stock price) | ReAct |
| Multi-step data processing pipeline | **CodeAct** |
| Tasks where approach varies per input | **CodeAct** |
| Quick prototype with many tools | ReAct |
| Math-heavy or logic-heavy problems | **CodeAct** |
| Tasks needing external libraries in tools | ReAct (more flexible tool format) |

## Gotchas

- **Claude passes callable objects or class methods as tools.** CodeAct only accepts plain functions — not callable objects (`__call__`), not bound methods, not lambdas. If you need to wrap state, define a closure that captures the state and pass the inner function.
- **Claude writes tool functions that import external libraries.** Tools execute in your Python process, but the glue code between tool calls runs in the Deno sandbox which has no pip packages. If the LM-generated code tries to `import pandas` between tool calls, it fails. Move all library usage inside the tool function itself, not in the generated code.
- **Claude forgets to pass dependent functions as tools.** If tool A calls helper function B internally, B runs fine (it executes in your Python process). But if the agent needs to call B directly in generated code, B must be in the `tools` list. Claude often defines helper functions but forgets to register them.
- **Claude uses CodeAct for simple lookup tasks where ReAct is better.** CodeAct adds overhead — code generation, sandbox execution, iteration. For tasks that just call one or two tools and combine results, ReAct is simpler and faster. Reserve CodeAct for computation, data transformation, and multi-step logic.
- **Claude sets `max_iters` too low for complex tasks.** The default `max_iters=5` is fine for simple computation, but data analysis tasks that fetch multiple sources and process results often need 8-10 iterations. Watch for "max iterations reached" and increase accordingly.

## Additional resources

- [CodeAct API docs](https://dspy.ai/api/modules/CodeAct/)
- [reference.md](reference.md) — constructor parameters, tool requirements, execution model
- [examples.md](examples.md) — data analysis, file processing, math agents, optimization

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **ReAct** for simpler tool-calling agents -- see `/dspy-react` and `/ai-taking-actions`
- **ProgramOfThought** for code-based single-shot reasoning without a tool loop -- see `/dspy-program-of-thought`
- **Tools** and tool patterns -- see `/ai-taking-actions`
- **Multi-agent coordination** -- see `/ai-coordinating-agents`
- **Modules** for composing CodeAct with other modules -- see `/dspy-modules`
- **Signatures** for defining agent inputs/outputs -- see `/dspy-signatures`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
