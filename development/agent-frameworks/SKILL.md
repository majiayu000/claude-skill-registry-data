---
name: agent-frameworks
description: AI agent development with LangChain, CrewAI, AutoGen, and tool integration patterns.
sasmp_version: "1.3.0"
bonded_agent: 06-ai-agents
bond_type: PRIMARY_BOND
---

# Agent Frameworks

Build autonomous AI agents with tools, planning, and multi-agent collaboration.

## Quick Start

### LangChain Agent
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub

# Define tools
def search(query: str) -> str:
    return f"Search results for: {query}"

def calculate(expression: str) -> str:
    return str(eval(expression))

tools = [
    Tool(name="Search", func=search, description="Search the web"),
    Tool(name="Calculator", func=calculate, description="Do math")
]

# Create agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)

# Execute
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = executor.invoke({"input": "What is 2+2 and who invented calculus?"})
```

### OpenAI Function Calling
```python
from openai import OpenAI
import json

client = OpenAI()

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather in a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
]

# Chat with tool use
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    # Execute the tool and continue conversation
```

## Framework Comparison

| Framework | Strengths | Best For |
|-----------|-----------|----------|
| LangChain | Comprehensive, many integrations | General agents |
| CrewAI | Multi-agent, role-based | Team simulations |
| AutoGen | Microsoft, conversational | Research |
| Semantic Kernel | C#/Python, enterprise | Microsoft stack |
| LlamaIndex | Data-focused | RAG agents |

## CrewAI Multi-Agent

```python
from crewai import Agent, Task, Crew, Process

# Define agents with roles
researcher = Agent(
    role='Senior Researcher',
    goal='Find comprehensive information on topics',
    backstory='Expert at gathering and synthesizing information',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)

writer = Agent(
    role='Technical Writer',
    goal='Create clear and engaging content',
    backstory='Experienced in explaining complex topics simply',
    verbose=True
)

# Define tasks
research_task = Task(
    description='Research the topic: {topic}',
    expected_output='Detailed research findings',
    agent=researcher
)

writing_task = Task(
    description='Write an article based on research',
    expected_output='Well-structured article',
    agent=writer
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff(inputs={'topic': 'AI Agents'})
```

## Tool Integration Patterns

### Custom Tool Definition
```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class SearchInput(BaseModel):
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, description="Max results")

class SearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for information"
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        # Implement search logic
        results = perform_search(query, max_results)
        return format_results(results)

    async def _arun(self, query: str, max_results: int = 5) -> str:
        # Async version
        results = await async_perform_search(query, max_results)
        return format_results(results)
```

### API Tool Wrapper
```python
import requests
from langchain.tools import tool

@tool
def api_call(endpoint: str, params: dict) -> str:
    """Make an API call to external service."""
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error: {str(e)}"
```

## Agent Patterns

### ReAct Pattern
```
Thought: I need to find information about X
Action: Search
Action Input: "X definition"
Observation: [search results]
Thought: Now I have the information, I can answer
Final Answer: X is...
```

### Plan-and-Execute
```python
from langchain.experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner
)

# Create planner and executor
planner = load_chat_planner(llm)
executor = load_agent_executor(llm, tools, verbose=True)

# Create agent
agent = PlanAndExecute(planner=planner, executor=executor)

result = agent.run("Create a report on AI trends")
# 1. Plans steps: research, analyze, write
# 2. Executes each step
# 3. Returns final result
```

### Reflection Pattern
```python
class ReflectiveAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.memory = []

    def act(self, task: str, max_iterations: int = 5) -> str:
        for i in range(max_iterations):
            # Act
            action = self._decide_action(task)
            result = self._execute_action(action)

            # Reflect
            reflection = self._reflect(task, action, result)
            self.memory.append({
                'action': action,
                'result': result,
                'reflection': reflection
            })

            # Check if done
            if self._is_complete(reflection):
                return self._synthesize_answer()

        return "Max iterations reached"

    def _reflect(self, task, action, result):
        prompt = f"""Task: {task}
Action taken: {action}
Result: {result}

Reflect on:
1. Was this action effective?
2. What did we learn?
3. What should we do next?"""

        return self.llm.generate(prompt)
```

## Memory Management

```python
from langchain.memory import ConversationBufferWindowMemory

# Short-term memory (last N turns)
memory = ConversationBufferWindowMemory(k=10, return_messages=True)

# With summary
from langchain.memory import ConversationSummaryBufferMemory
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=1000
)

# Entity memory
from langchain.memory import ConversationEntityMemory
memory = ConversationEntityMemory(llm=llm)
memory.save_context(
    {"input": "John works at Google"},
    {"output": "Got it, John works at Google"}
)
# memory.entity_store contains {"John": "works at Google"}
```

## Production Considerations

### Error Handling
```python
class RobustAgent:
    def execute_with_retry(self, task, max_retries=3):
        for attempt in range(max_retries):
            try:
                return self.agent.run(task)
            except ToolExecutionError as e:
                if attempt < max_retries - 1:
                    self.memory.add(f"Tool error: {e}, retrying...")
                    continue
                raise
            except LLMError as e:
                # Fallback to simpler approach
                return self.fallback_handler(task)
```

### Cost Control
```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = agent.run("Complex task")
    print(f"Total Cost: ${cb.total_cost}")
    print(f"Tokens Used: {cb.total_tokens}")

# Set budget limits
if cb.total_cost > MAX_COST:
    raise BudgetExceededError()
```

### Safety Guardrails
```python
FORBIDDEN_ACTIONS = ["delete", "drop", "rm -rf", "format"]

def safe_tool_filter(tool_input: str) -> bool:
    """Check if tool input is safe to execute."""
    for forbidden in FORBIDDEN_ACTIONS:
        if forbidden in tool_input.lower():
            return False
    return True

# Apply before tool execution
if not safe_tool_filter(action_input):
    return "Action blocked for safety reasons"
```

## Best Practices

1. **Start simple**: Single agent before multi-agent
2. **Limit tools**: 5-7 tools max for reliability
3. **Clear descriptions**: Tools need precise descriptions
4. **Error handling**: Graceful degradation on failures
5. **Cost monitoring**: Track token usage continuously
6. **Human-in-loop**: Confirm high-stakes actions

## Error Handling & Retry

```python
from tenacity import retry, stop_after_attempt

class RobustAgent:
    @retry(stop=stop_after_attempt(3))
    def execute_tool(self, tool_name, input_data):
        tool = self.tools[tool_name]
        return tool.run(input_data)

    def run_with_fallback(self, task):
        try:
            return self.agent.run(task)
        except Exception as e:
            return self.simple_llm_response(task)
```

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Infinite loop | No stop condition | Add max_iterations |
| Wrong tool choice | Poor descriptions | Improve tool docs |
| High cost | Many iterations | Set budget limits |

## Unit Test Template

```python
def test_agent_tool_execution():
    result = agent.run("Calculate 2+2")
    assert "4" in result
```
