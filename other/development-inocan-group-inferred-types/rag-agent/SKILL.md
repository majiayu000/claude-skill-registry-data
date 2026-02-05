---
name: rag-agent
description: Retrieval-Augmented Generation for project knowledge management using ChromaDB
---

# Rag Agent

## Purpose

Stores and retrieves project artifacts with semantic search capabilities

## When to Use This Skill

1. **Context Retrieval** - Get relevant info for LLMs
2. **Documentation Search** - Find relevant docs
3. **Prompt Management** - Store/retrieve prompts
4. **Code Examples** - Find similar implementations

## Responsibilities

1. **Store artifacts** - (prompts, code, docs) with embeddings
2. **Semantic search** - across project knowledge
3. **Context retrieval** - for LLM queries
4. **Version management** - for artifacts
5. **Integration with** - Knowledge Graph

## Integration with Pipeline

### Communication

**Receives:**

- Artifacts to store (prompts, docs, code)
- Search queries from other agents
- Context retrieval requests for LLMs


**Sends:**

- Relevant artifacts based on semantic similarity
- Context for LLM queries
- Search results with relevance scores


## Usage Examples

### Standalone Usage

```bash
python3 rag_agent.py \
  --operation store \
  --content-file prompt.txt \
  --collection prompts \
  --metadata '{"type": "developer_prompt", "version": "1.0"}'
```

### Programmatic Usage

```python
from rag_agent import RAGAgent

rag = RAGAgent(persist_directory="./rag_data")

# Store artifact
rag.store_artifact(
    content=prompt_text,
    collection_name="prompts",
    metadata={"type": "developer_prompt"}
)

# Retrieve context
results = rag.query(
    query_text="How to implement authentication?",
    collection_name="documentation",
    top_k=5
)

for doc in results:
    print(f"Relevance: {doc['score']:.2f}")
    print(f"Content: {doc['content'][:200]}...")
```

## Configuration

### Environment Variables

```bash
# Agent-specific configuration
ARTEMIS_RAG_AGENT_ENABLED=true
ARTEMIS_LLM_PROVIDER=openai
ARTEMIS_LLM_MODEL=gpt-4o
```

### Hydra Configuration (if applicable)

```yaml
rag_agent:
  enabled: true
  llm:
    provider: openai
    model: gpt-4o
```

## Best Practices

1. **Organize Collections** - Separate prompts, docs, code
2. **Rich Metadata** - Tag artifacts for better filtering
3. **Regular Cleanup** - Archive old/unused artifacts
4. **Monitor Size** - ChromaDB can grow large
5. **Backup Regularly** - Persist directory is critical

## Cost Considerations

Typical cost: $0.05-0.20 per operation depending on complexity

## Limitations

- Depends on LLM quality
- Context window limits
- May require multiple iterations

## References

- [Artemis Documentation](../README.md)
- [Agent Pattern](https://en.wikipedia.org/wiki/Software_agent)

---

**Version:** 1.0.0

**Maintained By:** Artemis Pipeline Team

**Last Updated:** October 24, 2025
