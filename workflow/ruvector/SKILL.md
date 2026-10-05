---
name: ruvector
description: Use when generating and managing vector embeddings for semantic search
  and RAG retrieval across knowledge bases.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- infrastructure
- memory
- ruvector
- self-improvement
persona:
  name: Edo Liberty
  title: The Vector Search Expert - Master of Similarity Search
  expertise:
  - Vector Databases
  - Approximate Nearest Neighbors
  - Embeddings
  - Similarity Search
  philosophy: Similarity search powers the next generation of AI applications.
  credentials:
  - Founder of Pinecone
  - Former AWS AI Labs director
  - Published 50+ research papers
  principles:
  - Index for speed
  - Approximate is good enough
  - Scale to billions
  - Latency matters
version: 1.0.0
category: core
---

# RuVector Skill

> Self-learning vector database with Graph Neural Networks for autonomous AI memory

## Overview

RuVector is a distributed vector database that **learns from every query**. Unlike static vector databases, RuVector uses GNN (Graph Neural Network) layers to improve search results over time. It's perfect for building self-improving AI memory systems.


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
**Trigger phrases:**
- "Edo Liberty"
- "Generate and manage vector embeddings for semantic search and RAG retrieval acro"


Use this skill when you need:
- **Local vector storage** without external API dependencies
- **Self-improving memory** that gets smarter with usage
- **Graph queries** with Cypher syntax
- **Local LLM integration** for RAG without cloud APIs
- **Autonomous AI agents** that learn from interactions

## Key Features
- Automated workflow execution with error recovery
- Configurable parameters for different use cases
- Integration with existing tooling and pipelines
- Detailed logging and status reporting


### 🧠 Self-Learning Index
- GNN layers learn from every query
- Search results improve over time
- No manual index rebuilding needed

### 🔍 Graph Queries (Cypher)
```cypher
MATCH (a)-[:SIMILAR]->(b) WHERE a.name = "AI" RETURN b
```

### 💾 Local Embeddings
- Built-in ONNX embedding models
- No API calls needed
- Runs entirely offline

### ⚡ MCP Tools
- 213+ MCP tools for swarm management
- Memory integration
- GitHub automation

## Installation

```bash
# Quick start
npx ruvector

# Initialize self-learning hooks
npx @ruvector/cli hooks init

# Install optional GNN module
npx ruvector install gnn
```

## Usage Patterns
- Invoke the skill when the matching domain keywords appear
- Combine with related skills for end-to-end workflows
- Use verification steps to confirm successful execution
- Review output quality before finalizing results


### Basic Vector Storage
```javascript
const ruvector = require('ruvector');

// Create collection
await db.createCollection('memories', { dimension: 384 });

// Add embeddings
await db.insert('memories', {
  id: 'memory_1',
  vector: embedding,
  metadata: { context: 'user_preference', topic: 'coffee' }
});

// Search (improves over time!)
const results = await db.search('memories', queryEmbedding, { topK: 5 });
```

### Self-Learning Hook
```javascript
// Enable learning from queries
await db.hooks.enable('self-learning', {
  algorithm: 'q-learning',
  memorySize: 10000
});
```

### Local LLM Integration
```javascript
// Run LLMs locally
const { RuvLLM } = require('@ruvector/ruvllm');
const llm = new RuvLLM({ model: 'ruvltra-small' });

const response = await llm.chat('Explain vector databases');
```

## Integration with 1ai-skills

RuVector integrates perfectly with:
- `runtime-self-improvement` - Store learned patterns
- `ai-research-agent` - Long-term memory
- `skill-performance-monitor` - Track skill usage

## Files in This Skill

- `SKILL.md` - This file
- `references/` - Additional documentation

## See Also

- [RuVector GitHub](https://github.com/ruvnet/ruvector)
- [RuVector NPM](https://www.npmjs.com/package/ruvector)
- [Documentation](https://ruv.io)

## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
