---
name: langchain
description: Build production-ready LLM applications with chains, agents, memory,
  tools, and RAG pipelines using the LangChain framework
version: 1.0.0
author: workspace-hub
category: ai-prompting
type: skill
trigger: manual
auto_execute: false
capabilities:
- chain_composition
- agent_orchestration
- memory_management
- tool_integration
- rag_pipelines
- vector_stores
- document_processing
- streaming_responses
tools:
- Read
- Write
- Bash
- Grep
tags:
- langchain
- llm
- chains
- agents
- rag
- embeddings
- vector-stores
- memory
- tools
platforms:
- python
related_skills:
- prompt-engineering
- dspy
- pandasai
scripts_exempt: true
---

# Langchain

## Quick Start

```bash
# Install LangChain ecosystem
pip install langchain langchain-openai langchain-community langchain-core

# Install vector store dependencies
pip install chromadb faiss-cpu

# Install document loaders
pip install unstructured pypdf docx2txt

# Set API key
export OPENAI_API_KEY="your-api-key"
```

## When to Use This Skill

**USE when:**
- Building complex LLM applications with multiple components
- Need agents that can use tools and make autonomous decisions
- Implementing RAG (Retrieval Augmented Generation) systems
- Integrating with various LLM providers (OpenAI, Anthropic, local models)
- Building chatbots with conversation memory
- Processing and querying document collections
- Need streaming responses for real-time applications
- Orchestrating multi-step reasoning workflows

**DON'T USE when:**
- Simple single-prompt LLM calls (use direct API)
- Optimizing prompts programmatically (use DSPy instead)
- Building UI-focused chat applications (use Streamlit/Gradio directly)
- Need minimal dependencies and maximum control
- Performance-critical applications requiring custom optimizations

## Prerequisites

```bash
# Core installation
pip install langchain>=0.2.0 langchain-openai>=0.1.0 langchain-core>=0.2.0

# For RAG applications
pip install chromadb>=0.4.0 faiss-cpu>=1.7.0

# For document processing
pip install unstructured>=0.10.0 pypdf>=3.0.0

# For web search and tools
pip install duckduckgo-search wikipedia arxiv

# Optional: Local LLMs
pip install langchain-community ollama

# Environment setup
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Complete Examples

### Example 1: Engineering Documentation Assistant

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from pathlib import Path

*See sub-skills for full details.*
### Example 2: Multi-Tool Research Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field
from typing import List, Optional
import json

*See sub-skills for full details.*

## Integration Patterns

### LangServe Deployment

```python
from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Create app
app = FastAPI(
    title="Engineering Assistant API",

*See sub-skills for full details.*
### LangSmith Tracing

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
os.environ["LANGCHAIN_PROJECT"] = "engineering-assistant"

# All chain invocations are now traced
chain = ChatPromptTemplate.from_template("{input}") | ChatOpenAI()
response = chain.invoke({"input": "Hello"})
```

## Resources

- **LangChain Documentation**: https://python.langchain.com/docs/
- **LangChain Expression Language**: https://python.langchain.com/docs/expression_language/
- **LangSmith**: https://smith.langchain.com/
- **LangServe**: https://python.langchain.com/docs/langserve/

---

## Version History

- **1.0.0** (2026-01-17): Initial release with chains, agents, memory, RAG, and streaming

## Sub-Skills

- [1. Basic Chain Composition](1-basic-chain-composition/SKILL.md)
- [2. Agent with Tools](2-agent-with-tools/SKILL.md)
- [3. Conversation Memory](3-conversation-memory/SKILL.md)
- [4. RAG (Retrieval Augmented Generation)](4-rag-retrieval-augmented-generation/SKILL.md)
- [5. Document Processing](5-document-processing/SKILL.md)
- [6. Streaming Responses](6-streaming-responses/SKILL.md)
- [1. Error Handling (+2)](1-error-handling/SKILL.md)
- [Rate Limit Errors (+2)](rate-limit-errors/SKILL.md)
