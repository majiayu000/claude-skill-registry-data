---
name: grey-haven-memory-systems
description: "Design and implement long-term memory systems for AI agents using vector stores, knowledge graphs, and hybrid approaches. Includes benchmarks and decision frameworks. Use when building persistent agent memory, implementing RAG, designing knowledge bases, or when user mentions 'memory', 'RAG', 'vector store', 'knowledge graph', 'long-term memory', 'retrieval', or 'embeddings'."
# v2.0.43: Skills to auto-load for memory work
skills:
  - grey-haven-data-modeling
  - grey-haven-code-style
# v2.0.74: Tools for memory system work
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Memory Systems Skill

Design and implement long-term memory systems for AI agents.

## The Context-Memory Spectrum

Memory exists on a spectrum from ephemeral to permanent:

```
Ephemeral ◄────────────────────────────────────► Permanent

Context Window    Short-term    Long-term    Knowledge
(disappears)      Cache         Memory       Base
                  (session)     (weeks)      (forever)
```

### When to Use What

| Memory Type | Duration | Use Case |
|-------------|----------|----------|
| Context window | Single turn | Immediate task context |
| Short-term cache | Session | Conversation history |
| Long-term memory | Weeks/months | User preferences, learnings |
| Knowledge base | Permanent | Facts, documentation, procedures |

## Memory Architecture Options

### 1. Vector RAG (Retrieval-Augmented Generation)

Store embeddings, retrieve by semantic similarity.

**Pros**:
- Simple to implement
- Works well for document retrieval
- Scales to millions of documents

**Cons**:
- No relationships between items
- Recency bias (older memories fade)
- Can retrieve irrelevant but similar content

**Best for**: Document search, FAQ systems, code search

### 2. Knowledge Graphs

Store entities and relationships explicitly.

**Pros**:
- Captures relationships
- Supports reasoning
- No similarity confusion

**Cons**:
- Complex to build and maintain
- Requires structured data
- More expensive queries

**Best for**: Domain modeling, reasoning tasks, complex queries

### 3. Temporal Knowledge Graphs

Knowledge graphs with time-based relationships.

**Pros**:
- Tracks how knowledge evolves
- Supports "as of" queries
- Captures causality

**Cons**:
- Most complex option
- Storage grows over time
- Query complexity

**Best for**: Historical analysis, change tracking, audit trails

### 4. Hybrid Approaches

Combine vector + graph for best of both:

```
Query ──▶ Vector Search ──▶ Top K candidates
              │
              ▼
          Graph Traversal ──▶ Related entities
              │
              ▼
          Re-ranking ──▶ Final results
```

## Performance Benchmarks

Research benchmarks for memory systems (2024 data):

| System | Recall@10 | Latency (P50) | Cost/Query |
|--------|-----------|---------------|------------|
| Zep | 94.8% | 45ms | $0.0001 |
| MemGPT | 93.4% | 120ms | $0.0003 |
| LangChain Memory | 87.2% | 80ms | $0.0002 |
| Simple RAG | 78.5% | 30ms | $0.00005 |

### Key Insights

1. **Zep** excels at conversation memory with entity extraction
2. **MemGPT** best for complex reasoning over memory
3. **Simple RAG** sufficient for most document retrieval
4. **Hybrid approaches** win for complex queries

## What's Included

### Examples (`examples/`)
- **Conversation memory** - Storing and retrieving chat history
- **Entity memory** - Tracking entities mentioned in conversations
- **Knowledge base integration** - Connecting to Grey Haven KB

### Reference Guides (`reference/`)
- **Architecture patterns** - When to use each memory type
- **Embedding strategies** - Chunking, models, dimensions
- **Grey Haven integration** - Using with knowledge-base agents

### Checklists (`checklists/`)
- **Memory system selection** - Choose the right architecture
- **Implementation checklist** - Before deploying memory

## Grey Haven Knowledge Base Agents

This skill complements the knowledge-base agents:

| Agent | Purpose |
|-------|---------|
| `memory-architect` | Design memory storage, semantic search |
| `knowledge-curator` | Create and organize knowledge entries |
| `ontology-builder` | Map relationships between entries |
| `kb-search-analyzer` | Search and synthesize from KB |
| `kb-entry-creator` | Create structured KB entries |
| `kb-validator` | Validate KB integrity |
| `kb-manifest-generator` | Generate KB indexes |
| `kb-ontology-mapper` | Visualize knowledge structure |

## Implementation Patterns

### Pattern 1: Conversation Memory

```python
class ConversationMemory:
    def __init__(self):
        self.short_term = []  # Last N messages
        self.long_term = VectorStore()  # Semantic search
        self.entities = EntityStore()  # Mentioned entities

    def add_message(self, message: str, role: str):
        # Short-term: sliding window
        self.short_term.append({"role": role, "content": message})
        if len(self.short_term) > 20:
            self.short_term.pop(0)

        # Long-term: embed and store
        self.long_term.add(message, metadata={"role": role})

        # Entity extraction
        entities = extract_entities(message)
        self.entities.update(entities)

    def retrieve(self, query: str, k: int = 5) -> list:
        # Combine short-term + relevant long-term
        recent = self.short_term[-5:]
        similar = self.long_term.search(query, k=k)
        entities = self.entities.get_relevant(query)

        return {
            "recent": recent,
            "similar": similar,
            "entities": entities
        }
```

### Pattern 2: Entity Memory

```python
class EntityMemory:
    def __init__(self):
        self.entities = {}  # entity_name -> EntityRecord
        self.relationships = []  # (entity1, relation, entity2)

    def update(self, entity: str, info: dict):
        if entity not in self.entities:
            self.entities[entity] = EntityRecord(entity)

        self.entities[entity].update(info)
        self.entities[entity].last_mentioned = now()

    def get_context(self, entity: str) -> str:
        if entity not in self.entities:
            return ""

        record = self.entities[entity]
        related = self.get_relationships(entity)

        return f"""
Entity: {entity}
Type: {record.type}
Properties: {record.properties}
Related: {related}
Last mentioned: {record.last_mentioned}
"""
```

### Pattern 3: Tiered Memory

```python
class TieredMemory:
    def __init__(self):
        self.hot = LRUCache(100)      # Frequent access
        self.warm = VectorStore()      # Semantic search
        self.cold = PersistentStore()  # Rarely accessed

    def get(self, key: str):
        # Check hot first
        if key in self.hot:
            return self.hot[key]

        # Then warm
        result = self.warm.get(key)
        if result:
            self.hot[key] = result  # Promote
            return result

        # Finally cold
        result = self.cold.get(key)
        if result:
            self.warm.add(key, result)  # Promote
            return result

        return None
```

## Use This Skill When

- Designing persistent memory for AI agents
- Implementing RAG systems
- Building knowledge management systems
- Choosing between vector vs graph approaches
- Optimizing memory retrieval performance
- Integrating with Grey Haven knowledge base

## Related Skills

- `context-management` - Managing context in workflows
- `data-modeling` - Designing memory data structures
- `llm-project-development` - Building LLM applications

## Quick Start

```bash
# Understand architecture options
cat reference/architecture-patterns.md

# See implementation examples
cat examples/conversation-memory.md

# Use selection checklist
cat checklists/memory-selection-checklist.md
```

---

**Skill Version**: 1.0
**Key Benchmark**: Zep 94.8% recall, 45ms latency
**Related Agents**: 8 knowledge-base agents
**Last Updated**: 2025-01-15
