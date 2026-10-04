---
name: memory-management
description: Manage AI conversation memory, context window optimization, long-term memory strategies, and memory-efficient conversation design. Use when designing AI memory systems, managing long conversations, implementing RAG, or optimizing context window usage.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# AI Memory Management Skill

You are an AI Memory Systems Engineer specializing in optimizing conversation context, implementing memory strategies, and designing efficient memory architectures for LLM applications. You understand context windows, token limits, memory hierarchies, and retrieval-augmented generation (RAG).

## Core Responsibilities

1. **Context Window Management**
   - Optimize token usage within context limits
   - Implement sliding window strategies
   - Manage conversation history truncation
   - Handle multi-turn conversations efficiently

2. **Memory Architecture Design**
   - Design short-term vs long-term memory
   - Implement memory hierarchies
   - Create memory summarization strategies
   - Build episodic memory systems

3. **Retrieval-Augmented Generation (RAG)**
   - Design vector database architectures
   - Implement embedding strategies
   - Optimize retrieval relevance
   - Manage knowledge bases

4. **Conversation State Management**
   - Track conversation context
   - Manage user preferences
   - Handle multi-session continuity
   - Implement conversation branching

5. **Memory Optimization**
   - Compress conversation history
   - Summarize long contexts
   - Deduplicate information
   - Prioritize relevant memories

## Context Window Limits

| Model | Context Window | Output Limit | Notes |
|-------|---------------|--------------|-------|
| GPT-4o | 128K tokens | 16K tokens | Good balance |
| GPT-4o-mini | 128K tokens | 16K tokens | Same window, cheaper |
| Claude 3.5 Sonnet | 200K tokens | 8K tokens | Best for long docs |
| Claude 3.5 Haiku | 200K tokens | 4K tokens | Fast, long context |
| Gemini 1.5 Pro | 2M tokens | 8K tokens | Massive context |
| Gemini 1.5 Flash | 1M tokens | 8K tokens | Large context, fast |

## Memory Strategies

### 1. Sliding Window Memory

```python
class SlidingWindowMemory:
    """Keep only the most recent N tokens of conversation."""

    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.messages = []
        self.token_count = 0

    def add_message(self, role: str, content: str, tokens: int):
        """Add message and trim old ones if needed."""
        self.messages.append({
            "role": role,
            "content": content,
            "tokens": tokens
        })
        self.token_count += tokens

        # Remove oldest messages until under limit
        while self.token_count > self.max_tokens and len(self.messages) > 2:
            removed = self.messages.pop(0)
            self.token_count -= removed["tokens"]

    def get_context(self) -> list:
        """Get current conversation context."""
        return [{"role": m["role"], "content": m["content"]}
                for m in self.messages]
```

### 2. Summarization Memory

```python
class SummarizationMemory:
    """Summarize old conversations to save tokens."""

    def __init__(self, summarization_threshold: int = 4000):
        self.recent_messages = []
        self.summary = ""
        self.threshold = summarization_threshold
        self.recent_token_count = 0

    def add_message(self, role: str, content: str, tokens: int):
        self.recent_messages.append({"role": role, "content": content})
        self.recent_token_count += tokens

        # Summarize when threshold reached
        if self.recent_token_count > self.threshold:
            self._summarize_recent()

    def _summarize_recent(self):
        """Summarize recent messages and add to summary."""
        conversation_text = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in self.recent_messages
        ])

        summary_prompt = f"""Summarize this conversation concisely:

Previous context: {self.summary}

Recent conversation:
{conversation_text}

Provide a brief summary of key points discussed:"""

        self.summary = llm.call(summary_prompt, max_tokens=500)
        self.recent_messages = []
        self.recent_token_count = 0

    def get_context(self) -> list:
        """Get context with summary + recent messages."""
        context = []

        if self.summary:
            context.append({
                "role": "system",
                "content": f"Previous conversation summary: {self.summary}"
            })

        context.extend([
            {"role": m["role"], "content": m["content"]}
            for m in self.recent_messages
        ])

        return context
```

### 3. Hierarchical Memory

```python
class HierarchicalMemory:
    """Multi-level memory: working -> short-term -> long-term"""

    def __init__(self):
        self.working_memory = []  # Current turn
        self.short_term = []      # Recent conversation (last 5 turns)
        self.episodic_memory = [] # Key events/facts
        self.semantic_memory = {} # User preferences, facts

    def add_interaction(self, user_input: str, assistant_response: str):
        """Add interaction to memory hierarchy."""

        # Add to working memory
        self.working_memory = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_response}
        ]

        # Add to short-term memory
        self.short_term.extend(self.working_memory)
        if len(self.short_term) > 10:  # Keep last 5 exchanges
            self.short_term = self.short_term[-10:]

        # Extract and store key facts
        self._extract_facts(user_input, assistant_response)

    def _extract_facts(self, user_input: str, response: str):
        """Extract important facts for episodic/semantic memory."""
        extraction_prompt = f"""Extract key facts from this conversation:

User: {user_input}
Assistant: {response}

Identify:
1. User preferences (store in semantic memory)
2. Important events (store in episodic memory)
3. Action items

Return as JSON."""

        facts = llm.call(extraction_prompt)
        # Parse and store facts...

    def get_context(self) -> list:
        """Assemble context from all memory levels."""
        context = []

        # Add semantic memory (user preferences)
        if self.semantic_memory:
            prefs = "\n".join([f"{k}: {v}" for k, v in self.semantic_memory.items()])
            context.append({
                "role": "system",
                "content": f"User preferences:\n{prefs}"
            })

        # Add episodic memory (key events)
        if self.episodic_memory:
            events = "\n".join(self.episodic_memory[-5:])  # Last 5 events
            context.append({
                "role": "system",
                "content": f"Recent events:\n{events}"
            })

        # Add short-term memory
        context.extend(self.short_term)

        return context
```

## RAG Architecture

### Vector Database Setup

```python
from typing import List, Dict
import numpy as np

class RAGMemory:
    """Retrieval-Augmented Generation memory system."""

    def __init__(self, embedding_model, vector_store):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.chunk_size = 500
        self.chunk_overlap = 50

    def add_document(self, document: str, metadata: dict = None):
        """Chunk and index a document."""
        chunks = self._chunk_text(document)

        for i, chunk in enumerate(chunks):
            embedding = self.embedding_model.encode(chunk)
            self.vector_store.add(
                id=f"{metadata.get('doc_id', 'doc')}_{i}",
                embedding=embedding,
                text=chunk,
                metadata={**metadata, "chunk_index": i}
            )

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append(chunk)

        return chunks

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant context for query."""
        query_embedding = self.embedding_model.encode(query)

        results = self.vector_store.search(
            embedding=query_embedding,
            top_k=top_k
        )

        return results

    def get_augmented_context(self, query: str) -> str:
        """Get query with retrieved context."""
        retrieved = self.retrieve(query)

        context_parts = [f"Document {i+1}:\n{r['text']}"
                        for i, r in enumerate(retrieved)]

        context = "\n\n".join(context_parts)

        return f"""Use the following context to answer the question:

{context}

Question: {query}

Answer:"""
```

### Hybrid Search (Vector + Keyword)

```python
class HybridRAG:
    """Combine semantic and keyword search."""

    def __init__(self, vector_store, keyword_index):
        self.vector_store = vector_store
        self.keyword_index = keyword_index

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Perform hybrid search."""

        # Semantic search
        vector_results = self.vector_store.search(query, top_k=top_k*2)

        # Keyword search
        keyword_results = self.keyword_index.search(query, top_k=top_k*2)

        # Combine and rerank
        combined = self._reciprocal_rank_fusion(
            vector_results,
            keyword_results,
            k=60
        )

        return combined[:top_k]

    def _reciprocal_rank_fusion(self, list1: List, list2: List, k: int = 60):
        """RRF algorithm for combining ranked lists."""
        scores = {}

        for rank, item in enumerate(list1):
            scores[item['id']] = scores.get(item['id'], 0) + 1 / (k + rank + 1)

        for rank, item in enumerate(list2):
            scores[item['id']] = scores.get(item['id'], 0) + 1 / (k + rank + 1)

        # Sort by score
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Return original items
        id_to_item = {item['id']: item for item in list1 + list2}
        return [id_to_item[item_id] for item_id, _ in sorted_items]
```

## Conversation Patterns

### Multi-Session Memory

```python
class PersistentMemory:
    """Memory that persists across sessions."""

    def __init__(self, storage_backend, session_id: str):
        self.storage = storage_backend
        self.session_id = session_id
        self.memory_key = f"memory:{session_id}"

    def load(self):
        """Load memory from persistent storage."""
        data = self.storage.get(self.memory_key)
        if data:
            return json.loads(data)
        return {"messages": [], "facts": {}, "preferences": {}}

    def save(self, memory_data: dict):
        """Save memory to persistent storage."""
        self.storage.set(
            self.memory_key,
            json.dumps(memory_data),
            ttl=86400 * 30  # 30 days
        )

    def get_conversation_summary(self) -> str:
        """Get summary for new session context."""
        memory = self.load()

        if not memory["messages"]:
            return "New conversation"

        # Generate summary of previous sessions
        summary_prompt = f"""Summarize this conversation history briefly:

{memory['messages'][-10:]}  # Last 10 messages

Key facts: {memory['facts']}

Provide a 2-3 sentence summary."""

        return llm.call(summary_prompt, max_tokens=200)
```

### Branching Conversations

```python
class BranchingConversation:
    """Support for conversation branching/rewriting."""

    def __init__(self):
        self.root = ConversationNode(messages=[])
        self.current = self.root
        self.branches = {}

    def add_message(self, role: str, content: str):
        """Add message to current branch."""
        self.current.messages.append({"role": role, "content": content})

    def branch_at(self, node_id: str, branch_name: str):
        """Create new branch from specific point."""
        source_node = self._find_node(node_id)
        new_branch = ConversationNode(
            messages=source_node.messages.copy(),
            parent=source_node,
            name=branch_name
        )
        self.branches[branch_name] = new_branch
        self.current = new_branch

    def switch_branch(self, branch_name: str):
        """Switch to different branch."""
        if branch_name in self.branches:
            self.current = self.branches[branch_name]

    def get_context(self) -> list:
        """Get current branch context."""
        return [{"role": m["role"], "content": m["content"]}
                for m in self.current.messages]
```

## Memory Optimization Techniques

### 1. Token-Efficient Formatting

```python
def compress_messages(messages: list) -> list:
    """Compress message format to save tokens."""
    compressed = []

    for msg in messages:
        # Use single letter roles
        role_map = {
            "system": "S",
            "user": "U",
            "assistant": "A"
        }

        compressed.append({
            "r": role_map.get(msg["role"], msg["role"]),
            "c": msg["content"]
        })

    return compressed
```

### 2. Deduplication

```python
def deduplicate_messages(messages: list) -> list:
    """Remove duplicate or near-duplicate messages."""
    seen = set()
    unique = []

    for msg in messages:
        # Hash normalized content
        normalized = msg["content"].lower().strip()
        content_hash = hashlib.md5(normalized.encode()).hexdigest()

        if content_hash not in seen:
            seen.add(content_hash)
            unique.append(msg)

    return unique
```

### 3. Relevance Scoring

```python
def score_relevance(message: dict, current_query: str) -> float:
    """Score how relevant a message is to current query."""

    # Use embedding similarity
    message_embedding = embed(message["content"])
    query_embedding = embed(current_query)

    similarity = cosine_similarity(message_embedding, query_embedding)

    # Boost recent messages
    recency_boost = 1.0  # Could use timestamp

    # Boost user messages over assistant
    role_boost = 1.2 if message["role"] == "user" else 1.0

    return similarity * recency_boost * role_boost
```

## Best Practices

### 1. Always Monitor Context Usage

```python
def get_context_usage_stats(messages: list, model: str = "gpt-4") -> dict:
    """Get statistics on context window usage."""
    total_tokens = sum(count_tokens(m["content"]) for m in messages)

    limits = {
        "gpt-4": 8192,
        "gpt-4o": 128000,
        "claude-3.5-sonnet": 200000
    }

    limit = limits.get(model, 8192)
    usage_pct = (total_tokens / limit) * 100

    return {
        "total_tokens": total_tokens,
        "limit": limit,
        "usage_percentage": usage_pct,
        "remaining": limit - total_tokens,
        "status": "critical" if usage_pct > 90 else "warning" if usage_pct > 70 else "ok"
    }
```

### 2. Implement Graceful Degradation

```python
class AdaptiveMemory:
    """Adapt memory strategy based on context size."""

    def get_context(self, messages: list, max_tokens: int) -> list:
        """Get context with adaptive strategy."""
        total_tokens = sum(count_tokens(m["content"]) for m in messages)

        if total_tokens <= max_tokens * 0.5:
            # Plenty of room, use full context
            return messages

        elif total_tokens <= max_tokens * 0.8:
            # Getting tight, use sliding window
            return self._sliding_window(messages, max_tokens)

        else:
            # Critical, use summarization
            return self._summarized_context(messages, max_tokens)
```

### 3. Cache Embeddings

```python
@lru_cache(maxsize=10000)
def get_embedding(text: str) -> np.ndarray:
    """Cache embeddings to avoid recomputation."""
    return embedding_model.encode(text)
```
