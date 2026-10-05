---
name: dify-workflow
description: Use when dify AI workflow platform — LLM apps, knowledge bases, agents,
  workflow orchestration, API deployment. Use when working with dify workflow.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- ai-agent
- api
- dify
- infrastructure
- memory
- self-improvement
- workflow
version: 1.0.0
category: core
---


## Overview

Dify is an open-source platform for building LLM applications with a visual workflow builder. It supports chatbots, agents, text generators, and complex workflows with knowledge bases, tools, and conditional logic.

## Capabilities

- Build LLM apps visually (chatbot, agent, text generator, workflow)
- Create and manage knowledge bases with document upload
- Design workflows with nodes: LLM, knowledge retrieval, code, HTTP, conditional
- Deploy apps via API, embed, or shareable link
- Manage prompts, variables, and conversation memory
- Integrate with OpenAI, Azure, local models via Ollama

## When to Use
**Trigger phrases:**
- "dify workflow"
- "Dify AI workflow platform — LLM apps, knowledge bases, agents, workflow orchestr"


- Building LLM applications without coding
- Needing visual workflow design for AI pipelines
- Wanting knowledge base RAG without infrastructure setup
- Prototyping AI features quickly
- Deploying AI apps as APIs

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


### App Types

| Type | Use Case |
|------|----------|
| **Chatbot** | Multi-turn conversation with memory |
| **Agent** | Tool-using autonomous assistant |
| **Text Generator** | Single input → output transformation |
| **Workflow** | Complex multi-step pipeline |

### Workflow Node Design

```
Start → Knowledge Retrieval → LLM → Conditional → HTTP Request → End
                                    ↓
                              Code Processing → End
```

### API Deployment

```bash
# Get API endpoint from Dify dashboard
# POST /v1/chat-messages
curl -X POST 'https://api.dify.ai/v1/chat-messages' \
  -H 'Authorization: Bearer {api_key}' \
  -H 'Content-Type: application/json' \
  -d '{
    "inputs": {},
    "query": "What is our return policy?",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "user-123"
  }'
```

### Knowledge Base Setup

```python
# Via API
import requests

# Upload document
files = {'file': open('company_docs.pdf', 'rb')}
response = requests.post(
    'https://api.dify.ai/v1/datasets/{dataset_id}/documents',
    headers={'Authorization': 'Bearer {api_key}'},
    files=files,
)

# Create knowledge base
response = requests.post(
    'https://api.dify.ai/v1/datasets',
    headers={'Authorization': 'Bearer {api_key}'},
    json={
        'name': 'Company Knowledge',
        'indexing_technique': 'high_quality',  # or 'economy'
    },
)
```

### Workflow Variables

```yaml
# Input variables
user_query: string
user_language: string

# System variables
conversation_id: string
user_id: string

# Output variables
answer: string
sources: array
confidence: number
```

### Self-Hosted Deployment

```bash
# Docker
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker-compose up -d

# Access at http://localhost:3000
```

### Integration Patterns

```python
# Python SDK
from dify_client import DifyClient

client = DifyClient(api_key="app-xxx")

# Chat
response = client.chat_messages(
    query="Hello",
    user="user-123",
    conversation_id="",
)

# Completion
response = client.completion_messages(
    inputs={"text": "Summarize this..."},
    user="user-123",
)
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| Knowledge Retrieval node | RAG over uploaded documents |
| LLM node | Generate text with prompts |
| Code node | Custom Python/JS logic |
| HTTP node | Call external APIs |
| Conditional node | Branch based on variables |
| Variable Aggregator | Merge outputs from branches |
| Template Transform | Format output with Jinja2 |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Knowledge retrieval empty | No documents indexed | Upload and process documents |
| Token limit exceeded | Prompt + context too long | Reduce knowledge retrieval count |
| Workflow timeout | Long-running HTTP/code node | Increase timeout or optimize |
| Model not available | API key or model config issue | Check model provider settings |

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