---
name: memory-design-patterns
description: Best practices for memory architecture design including user vs agent vs session memory patterns, vector vs graph memory tradeoffs, retention strategies, and performance optimization. Use when designing memory systems, architecting AI memory layers, choosing memory types, planning retention strategies, or when user mentions memory architecture, user memory, agent memory, session memory, memory patterns, vector storage, graph memory, or Mem0 architecture.
allowed-tools: Read, Write, Bash, Edit
---

# Memory Design Patterns

Production-ready memory architecture patterns for AI applications using Mem0. This skill provides comprehensive guidance on designing scalable, performant memory systems with proper isolation, retention strategies, and optimization techniques.

## Instructions

### Phase 1: Understand Memory Types

Mem0 provides three distinct memory scopes, each serving different purposes:

#### 1. User Memory (Persistent Preferences & Profile)
**Purpose**: Long-term personal preferences, profile data, and user characteristics that persist across all interactions.

**Use Cases**:
- User preferences (dietary restrictions, communication style, language preferences)
- Personal information (location, occupation, family details)
- Long-term goals and interests
- Historical context that should persist indefinitely

**Implementation**:
```python
# Add user-level memory
memory.add(
    "User prefers concise responses without technical jargon"
    user_id="customer_bob"
)

# Search user memories
user_context = memory.search(
    "communication style"
    user_id="customer_bob"
)
```

**Key Characteristics**:
- Persists indefinitely (or until explicitly deleted)
- Shared across all agents interacting with this user
- Should contain stable, long-term information
- Typically 10-50 memories per user

#### 2. Agent Memory (Agent-Specific Context)
**Purpose**: Agent-specific knowledge, behaviors, and learned patterns that apply across all users interacting with this agent.

**Use Cases**:
- Agent capabilities and limitations
- Domain-specific knowledge
- Learned behaviors and patterns
- Agent-specific instructions and protocols

**Implementation**:
```python
# Add agent-level memory
memory.add(
    "When handling refund requests, always check order date first"
    agent_id="support_agent_v2"
)

# Search agent memories
agent_context = memory.search(
    "refund process"
    agent_id="support_agent_v2"
)
```

**Key Characteristics**:
- Shared across all users interacting with this agent
- Contains agent-specific procedures and knowledge
- Moderate retention (days to months)
- Typically 50-200 memories per agent

#### 3. Session/Run Memory (Temporary Conversation Context)
**Purpose**: Ephemeral context specific to a single conversation or task session.

**Use Cases**:
- Current conversation topic
- Temporary task context
- Session-specific state
- Short-term working memory

**Implementation**:
```python
# Add session-level memory
memory.add(
    "Current issue: payment failed with error code 402"
    run_id="session_12345_20250115"
)

# Search session memories
session_context = memory.search(
    "current issue"
    run_id="session_12345_20250115"
)
```

**Key Characteristics**:
- Short-lived (minutes to hours)
- Isolated to specific conversation or task
- Should be cleaned up after session ends
- Typically 5-20 memories per session

### Phase 2: Choose Storage Backend (Vector vs Graph)

#### Vector Memory (Default)
**How It Works**: Embeddings stored in vector database, semantic similarity search using cosine distance.

**Strengths**:
- Fast semantic search
- Excellent for unstructured data
- Low setup complexity
- Works out-of-the-box with Mem0

**Weaknesses**:
- Cannot query relationships
- No explicit entity connections
- Limited reasoning about connections

**Best For**:
- Simple preference storage
- Document/chunk retrieval
- Semantic search use cases
- Quick prototyping

**Configuration**:
```python
from mem0 import Memory

# Default vector-only configuration
memory = Memory()
```

#### Graph Memory (Advanced)
**How It Works**: Entities and relationships stored in graph database (Neo4j/Memgraph), enables relationship traversal and complex queries.

**Strengths**:
- Explicit entity relationships
- Complex query capabilities
- Relationship reasoning
- Multi-hop traversal

**Weaknesses**:
- Requires graph database setup
- Higher infrastructure complexity
- Slower for pure semantic search
- More storage overhead

**Best For**:
- Multi-entity systems
- Relationship-heavy domains
- Complex reasoning requirements
- Enterprise knowledge graphs

**Configuration**:
```python
from mem0 import Memory
from mem0.configs.base import MemoryConfig

config = MemoryConfig(
    graph_store={
        "provider": "neo4j"
        "config": {
            "url": "bolt://localhost:7687"
            "username": "neo4j"
            "password": "password"
        }
    }
)
memory = Memory(config)
```

**Decision Matrix**:
| Use Case | Vector | Graph |
|----------|--------|-------|
| User preferences | ✅ Best | ⚠️ Overkill |
| Product recommendations | ✅ Best | ⚠️ Overkill |
| Customer support | ✅ Good | ✅ Better |
| Knowledge management | ⚠️ Limited | ✅ Best |
| Multi-tenant systems | ✅ Good | ✅ Best |
| Team collaboration | ⚠️ Limited | ✅ Best |

### Phase 3: Design Retention Strategy

Use the retention strategy template:
```bash
bash scripts/generate-retention-policy.sh <memory-type> <retention-days>
```

#### Retention Guidelines

**User Memory**:
- Retention: Indefinite (with user control)
- Cleanup: User-initiated deletion only
- Archival: After 1 year of inactivity
- GDPR: Must support right to deletion

**Agent Memory**:
- Retention: 90-180 days typical
- Cleanup: Automatic based on relevance score
- Versioning: Keep agent version history
- Deprecation: Clear old agent memories on major updates

**Session Memory**:
- Retention: 1-24 hours
- Cleanup: Automatic after session end
- Conversion: Promote important memories to user/agent level
- Storage: Consider in-memory for very short sessions

#### Retention Implementation

Run the retention analyzer:
```bash
bash scripts/analyze-retention.sh <user_id_or_agent_id>
```

This script:
1. Analyzes memory age and access patterns
2. Identifies stale memories
3. Suggests cleanup actions
4. Generates retention reports

### Phase 4: Implement Multi-Level Memory Pattern

**Pattern**: Combine all three memory types for comprehensive context.

**Template**: Use `templates/multi-level-memory-pattern.py`

**Architecture**:
```
Query Processing Flow:
1. Retrieve session context (immediate)
2. Retrieve user context (preferences)
3. Retrieve agent context (capabilities)
4. Merge contexts with priority weighting
5. Generate response with full context
```

**Priority Weighting**:
- Session: 40% weight (most relevant to current task)
- User: 35% weight (personalizes response)
- Agent: 25% weight (ensures consistent behavior)

**Implementation**:
```python
# Retrieve all context levels
session_memories = memory.search(query, run_id=run_id)
user_memories = memory.search(query, user_id=user_id)
agent_memories = memory.search(query, agent_id=agent_id)

# Weighted merge
context = merge_contexts(
    session=session_memories
    user=user_memories
    agent=agent_memories
    weights={"session": 0.4, "user": 0.35, "agent": 0.25}
)
```

### Phase 5: Optimize Performance

#### Vector Search Optimization

Run the performance analyzer:
```bash
bash scripts/analyze-memory-performance.sh <project_name>
```

**Optimization Techniques**:

1. **Limit Search Results**:
   ```python
   memories = memory.search(query, user_id=user_id, limit=5)
   ```
   - Default: 10 results
   - Recommended: 3-5 for chat, 10-20 for RAG

2. **Use Filters to Reduce Search Space**:
   ```python
   memories = memory.search(
       query
       filters={
           "AND": [
               {"user_id": "alex"}
               {"agent_id": "support_agent"}
           ]
       }
   )
   ```

3. **Cache Frequently Accessed Memories**:
   - Cache user preferences (rarely change)
   - Refresh cache every 5-10 minutes
   - Invalidate on explicit memory updates

4. **Batch Operations**:
   ```python
   # Add multiple memories in one call
   memory.add(messages, user_id=user_id)
   ```

#### Graph Query Optimization

For graph memory:
1. **Limit Traversal Depth**: Max 2-3 hops
2. **Index Key Properties**: user_id, agent_id, timestamps
3. **Use Relationship Filters**: Reduce unnecessary traversals
4. **Monitor Query Performance**: Track slow queries > 100ms

### Phase 6: Implement Cost Optimization

Run the cost analyzer:
```bash
bash scripts/analyze-memory-costs.sh <user_id> <date_range>
```

**Cost Optimization Strategies**:

1. **Deduplication**: Remove similar/redundant memories
   ```bash
   bash scripts/deduplicate-memories.sh <user_id>
   ```

2. **Archival**: Move old memories to cold storage
   - Active: Last 30 days (vector DB)
   - Archive: 30-180 days (compressed JSON)
   - Long-term: > 180 days (S3/cold storage)

3. **Compression**: Use shorter embeddings for less critical memories
   - Critical: 1536 dimensions (OpenAI large)
   - Standard: 768 dimensions (OpenAI small)
   - Archival: 384 dimensions (lightweight model)

4. **Smart Pruning**: Remove low-value memories
   - Score-based: Keep only high relevance scores
   - Access-based: Remove never-accessed memories
   - Importance-based: User/agent priority tagging

### Phase 7: Security and Isolation

#### Multi-Tenant Isolation

**Pattern**: Ensure complete data isolation between users/organizations.

**Implementation**:
```python
# Always scope by user_id or org_id
memories = memory.search(
    query
    filters={"user_id": current_user_id}
)

# Validate access before retrieval
if not user_has_access(user_id, requested_user_id):
    raise PermissionError("Access denied")
```

**Security Checklist**:
- ✅ Never allow cross-user memory access
- ✅ Validate all user_id parameters
- ✅ Implement org-level isolation for multi-tenant apps
- ✅ Audit memory access logs
- ✅ Encrypt sensitive memory content
- ✅ Support GDPR right to deletion

Run the security audit:
```bash
bash scripts/audit-memory-security.sh
```

## Decision Trees

### When to Use Each Memory Type

Use the decision helper:
```bash
bash scripts/suggest-memory-type.sh "<use_case_description>"
```

**Quick Reference**:
- User dietary preferences → User Memory
- Agent's SOP for task X → Agent Memory
- Current conversation topic → Session Memory
- Customer support ticket details → Session Memory (promote to User if resolved)
- System capabilities → Agent Memory
- User's birthday → User Memory

### Vector vs Graph Decision

Use the architecture advisor:
```bash
bash scripts/suggest-storage-architecture.sh "<project_description>"
```

**Decision Criteria**:
1. Need relationship traversal? → Graph
2. Pure semantic search? → Vector
3. < 10,000 memories total? → Vector
4. Complex entity relationships? → Graph
5. Team/org hierarchies? → Graph
6. Simple preference storage? → Vector

## Key Files

**Scripts** (all functional, not placeholders):
- `scripts/generate-retention-policy.sh` - Create retention policy configs
- `scripts/analyze-retention.sh` - Analyze memory age and access patterns
- `scripts/analyze-memory-performance.sh` - Performance profiling
- `scripts/analyze-memory-costs.sh` - Cost analysis and optimization suggestions
- `scripts/deduplicate-memories.sh` - Find and remove duplicate memories
- `scripts/audit-memory-security.sh` - Security compliance checking
- `scripts/suggest-memory-type.sh` - Interactive memory type advisor
- `scripts/suggest-storage-architecture.sh` - Architecture recommendation tool

**Templates**:
- `templates/multi-level-memory-pattern.py` - Complete implementation
- `templates/retention-policy.yaml` - Retention configuration
- `templates/vector-only-config.py` - Vector memory setup
- `templates/graph-memory-config.py` - Graph memory setup
- `templates/hybrid-architecture.py` - Vector + Graph combined
- `templates/cost-optimization-config.yaml` - Cost optimization settings

**Examples**:
- `examples/customer-support-memory-architecture.md` - Full implementation guide
- `examples/multi-agent-collaboration.md` - Shared memory patterns
- `examples/e-commerce-personalization.md` - Product recommendation memory
- `examples/healthcare-assistant.md` - HIPAA-compliant memory architecture

## Best Practices

1. **Start Simple**: Use vector-only with user + session memories
2. **Add Complexity as Needed**: Only introduce graph when relationships matter
3. **Monitor Performance**: Track memory retrieval times and costs
4. **Implement Retention Early**: Don't let memory grow unbounded
5. **Test Isolation**: Verify cross-user memory access is impossible
6. **Document Memory Schema**: Track what memories mean and when they're used
7. **Version Agent Memories**: Clear separation between agent versions
8. **Promote Important Memories**: Session → User when patterns emerge
9. **Use Metadata**: Tag memories with categories for better filtering
10. **Regular Audits**: Monthly review of memory growth and costs

## Troubleshooting

**Slow Memory Retrieval**:
- Reduce search limit
- Add more specific filters
- Check vector index performance
- Consider caching

**High Costs**:
- Run cost analyzer script
- Implement deduplication
- Review retention policy
- Archive old memories

**Poor Search Results**:
- Check embedding model quality
- Verify memory content is descriptive
- Use hybrid search (keyword + semantic)
- Add metadata for filtering

**Memory Leakage Between Users**:
- Audit security script immediately
- Review all memory queries for user_id filtering
- Check RLS policies if using custom backends
- Implement access logging

---

**Plugin**: mem0
**Version**: 1.0.0
**Last Updated**: 2025-10-27
