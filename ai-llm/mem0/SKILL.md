---
name: mem0
description: Add persistent, intelligent memory to AI agents with Mem0 — add/search/update/delete memories per user/agent/session, supports vector + graph + key-value storage, integrates with LangChain, CrewAI, OpenAI Assistants, and any LLM.
triggers:
  - "mem0"
  - "mem0ai"
  - "memory layer ai agent"
  - "persistent agent memory"
  - "user memory ai"
  - "add memory agent"
  - "search memory"
  - "memory.add"
  - "memory.search"
  - "agent long term memory"
  - "personalized ai memory"
  - "cross session memory"
do_not_use_for:
  - Short-term conversation history — use LangChain ConversationBufferMemory instead
  - Vector search only — use pgvector or qdrant directly
  - State management within a single LangGraph run — use checkpointer instead
see_also:
  - langgraph
  - crewai
  - pydantic-ai
---

# Mem0 — Intelligent Memory Layer for AI Agents

**Source:** mem0ai/mem0 (Apache 2.0) — persistent, intelligent memory for AI applications

## Why Mem0

- Automatically extracts facts from conversations and stores them
- Semantically searches memories relevant to current context
- Deduplicates and updates conflicting memories
- Scoped by `user_id`, `agent_id`, `run_id` — flexible memory isolation
- Supports vector (default) + graph + key-value backends

## Install

```bash
pip install mem0ai
# Optional: graph memory
pip install mem0ai[graph]
```

## Quick Start (Managed Cloud)

```python
from mem0 import MemoryClient

client = MemoryClient(api_key="your-mem0-api-key")

# Add memories from a conversation
messages = [
    {"role": "user", "content": "I'm Alice and I love hiking."},
    {"role": "assistant", "content": "That's great! Do you have a favorite trail?"},
    {"role": "user", "content": "Yes, the Pacific Crest Trail is my favorite."},
]
client.add(messages, user_id="alice")

# Search memories
results = client.search("outdoor activities", user_id="alice")
for mem in results:
    print(mem["memory"])  # "User loves hiking" / "Favorite trail is PCT"

# Get all memories for a user
all_mems = client.get_all(user_id="alice")

# Update a memory
client.update(memory_id="mem-xxx", data="User loves hiking and cycling")

# Delete
client.delete(memory_id="mem-xxx")
client.delete_all(user_id="alice")
```

## Self-Hosted (Open Source)

```python
from mem0 import Memory

config = {
    "llm": {
        "provider": "anthropic",
        "config": {
            "model": "claude-sonnet-4-5",
            "api_key": "your-anthropic-key",
        },
    },
    "embedder": {
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "mem0_memories",
            "host": "localhost",
            "port": 6333,
        },
    },
}

memory = Memory.from_config(config)
```

## Memory Scoping

```python
from mem0 import Memory

m = Memory()

# User-scoped memory (persists across sessions)
m.add("User prefers dark mode", user_id="user-123")
m.add("User is a Python developer", user_id="user-123")

# Agent-scoped memory (shared across users for this agent)
m.add("This agent specializes in cooking recipes", agent_id="chef-bot")

# Session-scoped memory (single conversation)
m.add("User asked about pasta today", user_id="user-123", run_id="session-abc")

# Search within scope
results = m.search("coding preferences", user_id="user-123")
```

## Integration with AI Agents

```python
from mem0 import Memory
from anthropic import Anthropic

memory = Memory()
client = Anthropic()

def chat_with_memory(user_id: str, user_message: str) -> str:
    # 1. Search relevant memories
    relevant_memories = memory.search(user_message, user_id=user_id)
    mem_context = "\n".join(f"- {m['memory']}" for m in relevant_memories)

    # 2. Build prompt with memory context
    system = f"""You are a helpful assistant.
Relevant memories about this user:
{mem_context if mem_context else "No memories yet."}
"""

    # 3. Get LLM response
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    answer = response.content[0].text

    # 4. Extract and store new memories from this exchange
    memory.add(
        [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": answer},
        ],
        user_id=user_id,
    )

    return answer

# Usage
print(chat_with_memory("alice", "My name is Alice and I love hiking."))
print(chat_with_memory("alice", "What do you know about me?"))
```

## Graph Memory (Relationships)

```python
from mem0 import Memory

config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "password",
        },
    },
    "llm": {"provider": "anthropic", "config": {"model": "claude-sonnet-4-5"}},
    "version": "v1.1",  # required for graph memory
}

memory = Memory.from_config(config)

# Graph memory automatically extracts relationships
memory.add("Alice works at Anthropic and knows Bob", user_id="user-1")
memory.add("Bob is a senior engineer", user_id="user-1")

# Graph-aware search finds Alice→Anthropic→Bob relationships
results = memory.search("Who does Alice work with?", user_id="user-1")
```

## Async Support

```python
import asyncio
from mem0 import AsyncMemory

async def main():
    memory = AsyncMemory()

    await memory.add(
        [{"role": "user", "content": "I'm learning Rust"}],
        user_id="user-1",
    )

    results = await memory.search("programming languages", user_id="user-1")
    for m in results:
        print(m["memory"], m["score"])

    # Get all
    all_mems = await memory.get_all(user_id="user-1")

asyncio.run(main())
```

## Memory with Metadata & Filters

```python
from mem0 import Memory

m = Memory()

# Add with metadata
m.add(
    "User prefers vegetarian food",
    user_id="alice",
    metadata={"category": "preference", "source": "onboarding"},
)

# Search with filters
results = m.search(
    "food preferences",
    user_id="alice",
    filters={"metadata": {"category": "preference"}},
    limit=5,
)

# Get specific memory by ID
mem = m.get(memory_id="mem-xxx")
print(mem["memory"], mem["created_at"])
```

## CrewAI Integration

```python
from crewai import Agent
from mem0 import Memory

memory = Memory()

class MemoryAwareAgent:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory = memory

    def get_context(self, task: str) -> str:
        mems = self.memory.search(task, user_id=self.user_id)
        return "\n".join(f"- {m['memory']}" for m in mems)

    def save_interaction(self, messages: list):
        self.memory.add(messages, user_id=self.user_id)
```

## Memory Stats

```python
m = Memory()

# Get memory count for user
all_mems = m.get_all(user_id="alice")
print(f"Total memories: {len(all_mems)}")

# Memory history (updates over time)
history = m.history(memory_id="mem-xxx")
for event in history:
    print(event["event"], event["old_memory"], event["new_memory"])
```

## Anti-Fake-Pass Checks

- [ ] `memory.search()` returns list of dicts with `memory` and `score` keys — not plain strings
- [ ] `memory.add()` accepts either a string or a list of messages (conversation format)
- [ ] Scoping: must pass at least one of `user_id`, `agent_id`, or `run_id`
- [ ] Graph memory requires `"version": "v1.1"` in config
- [ ] Self-hosted requires vector store running (Qdrant/Chroma/pgvector) + LLM configured
- [ ] `AsyncMemory` for async contexts — `Memory` uses sync API only
- [ ] Memories are automatically deduplicated/merged — duplicate adds won't create duplicates
