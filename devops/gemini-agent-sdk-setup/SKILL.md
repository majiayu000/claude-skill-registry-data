---
name: Gemini Agent SDK Setup
description: Integrate OpenAI Agent SDK with Google Gemini backend into FastAPI service using the official Google Gemini API via OpenAI compatibility layer.
---

# Gemini Agent SDK Setup

## Instructions

1. Generate the Agent SDK client initialization in app/services/agent/client.py:
   - Import OpenAI from openai package
   - Configure client with GEMINI_API_KEY
   - Set base_url to Google's Gemini OpenAI compatibility endpoint: "https://generativelanguage.googleapis.com/v1beta/openai/"
   - Ensure proper error handling and retry logic

2. Create agent configuration in app/services/agent/config.py:
   - Define model name constants (gemini-1.5-flash, gemini-2.5-flash)
   - Set up default parameters for agent calls
   - Include proper timeout and retry configurations

3. Implement tool registration system in app/services/tools/registry.py:
   - Create function to register tools with the agent
   - Define tool schemas following OpenAI Agent SDK specification
   - Include validation for tool inputs and outputs

4. Create utility functions for calling Gemini models in app/services/agent/utils.py:
   - Wrapper function for agent completion calls
   - Error handling and logging utilities
   - Response parsing and validation

5. Follow Context7 MCP conventions:
   - Only use Gemini models (no OpenAI inference)
   - Follow deterministic output formatting
   - Include proper error handling and logging

## Examples

Input: "Setup Gemini Agent SDK integration"
Output: Creates client.py with:
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def call_gemini_agent(messages, tools=None, model="gemini-1.5-flash"):
    """Call the Gemini agent with provided messages and tools."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            temperature=0.1
        )
        return response
    except Exception as e:
        # Handle errors appropriately
        raise e
```