---
name: semantic-kernel
description: Use when microsoft Semantic Kernel — AI orchestration, plugins, planners,
  memory, prompt templates. Use when working with semantic kernel.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- infrastructure
- kernel
- memory
- self-improvement
- semantic
version: 1.0.0
category: core
---


## Overview

Semantic Kernel is Microsoft's SDK for building AI agents and orchestrating AI plugins. It integrates LLMs with native code, supports multiple languages (C#, Python, Java), and provides planners for automatic function chaining.

## Capabilities

- Create plugins with semantic (prompt) and native (code) functions
- Use planners to auto-select and chain functions
- Manage conversation memory and context
- Integrate with Azure OpenAI, OpenAI, and local models
- Build agents with tool use and multi-step reasoning
- Support RAG with vector stores and embeddings

## When to Use
**Trigger phrases:**
- "semantic kernel"
- "Microsoft Semantic Kernel — AI orchestration, plugins, planners, memory, prompt "


- Building AI agents in .NET/C#/Python enterprise environments
- Needing structured plugin architecture for AI capabilities
- Wanting planners to dynamically compose function chains
- Integrating with Microsoft/Azure ecosystem
- Building RAG applications with enterprise data

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Kernel Setup

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

kernel = sk.Kernel()

# Add AI service
kernel.add_service(
    OpenAIChatCompletion(
        service_id="chat",
        ai_model_id="gpt-4o",
        api_key="sk-...",
    )
)
```

### Semantic Function (Prompt Plugin)

```python
from semantic_kernel.functions import kernel_function

# Inline prompt
summarize = kernel.add_function(
    prompt="{{$input}}\n\nSummarize the above in 3 bullet points.",
    function_name="summarize",
    plugin_name="utils",
    description="Summarize text into bullet points",
)

result = await kernel.invoke(summarize, input="Long text here...")
```

### Native Function (Code Plugin)

```python
class MathPlugin:
    @kernel_function(description="Calculate the square root of a number")
    def square_root(self, number: str) -> str:
        import math
        return str(math.sqrt(float(number)))

    @kernel_function(description="Calculate compound interest")
    def compound_interest(self, principal: str, rate: str, time: str) -> str:
        p, r, t = float(principal), float(rate), float(time)
        amount = p * (1 + r/100) ** t
        return f"${amount:.2f}"

kernel.add_plugin(MathPlugin(), "math")
```

### Planner (Auto Function Selection)

```python
from semantic_kernel.planners import FunctionCallStepwisePlanner

planner = FunctionCallStepwisePlanner(
    service_id="chat",
    max_iterations=10,
)

result = await planner.invoke(
    kernel,
    question="What is the square root of 144 and what's the weather in Seattle?",
)
print(result.final_answer)
```

### Chat Agent with History

```python
from semantic_kernel.contents import ChatHistory

history = ChatHistory()
history.add_system_message("You are a helpful assistant with access to tools.")

while True:
    user_input = input("User: ")
    history.add_user_message(user_input)

    result = await kernel.invoke_prompt(
        function_name="chat",
        plugin_name="chat_plugin",
        chat_history=history,
    )

    history.add_assistant_message(str(result))
    print(f"Assistant: {result}")
```

### RAG with Memory

```python
from semantic_kernel.memory import SemanticTextMemory

memory = SemanticTextMemory(storage=VolatileMemoryStore(), embeddings=embedding_gen)

# Store information
await memory.save_information(collection="docs", id="doc1", text="Product supports SSO...")

# Search
results = await memory.search(collection="docs", query="How to enable SSO?")
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `@kernel_function` | Register code as callable tool |
| Semantic function (prompt) | LLM-powered text processing |
| `FunctionCallStepwisePlanner` | Auto-select tools for a question |
| `ChatHistory` | Multi-turn conversations |
| `SemanticTextMemory` | RAG with vector search |
| `kernel.invoke()` | Execute a specific function |
| `kernel.invoke_prompt()` | Run a prompt with variables |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `ServiceInvalidRequestError` | Invalid model or config | Check service_id and model name |
| Planner loop | No valid function found | Improve function descriptions |
| Token limit exceeded | Too many functions/context | Reduce plugins or summarize history |
| Embedding dimension mismatch | Wrong embedding model | Ensure consistent embedding config |

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |