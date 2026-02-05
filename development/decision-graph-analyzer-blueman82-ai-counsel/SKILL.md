---
name: decision-graph-analyzer
description: Query and analyze the AI Counsel decision graph to find past deliberations, identify patterns, and debug memory issues
when_to_use: >
  Use this skill when you need to explore the decision graph memory system,
  find similar past deliberations, identify contradictions or evolution patterns,
  debug context injection issues, or analyze cache performance.
---

# Decision Graph Analyzer Skill

## Overview

The decision graph module (`decision_graph/`) stores completed deliberations and provides semantic similarity-based retrieval for context injection. This skill teaches you how to query, analyze, and troubleshoot the decision graph effectively.

## Core Components

### Storage Layer (`decision_graph/storage.py`)
- **DecisionGraphStorage**: SQLite3 backend with CRUD operations
- **Schema**: `decision_nodes`, `participant_stances`, `decision_similarities`
- **Indexes**: Optimized for timestamp (recency), question (duplicates), similarity (retrieval)
- **Connection**: Use `:memory:` for testing, file path for production

### Integration Layer (`decision_graph/integration.py`)
- **DecisionGraphIntegration**: High-level API facade
- **Methods**:
  - `store_deliberation(question, result)`: Save completed deliberation
  - `get_context_for_deliberation(question)`: Retrieve similar past decisions
  - `get_graph_stats()`: Get monitoring statistics
  - `health_check()`: Validate database integrity

### Retrieval Layer (`decision_graph/retrieval.py`)
- **DecisionRetriever**: Finds relevant decisions and formats context
- **Key Features**:
  - Two-tier caching (L1: query results, L2: embeddings)
  - Adaptive k (2-5 results based on database size)
  - Noise floor filtering (0.40 minimum similarity)
  - Tiered formatting (strong/moderate/brief)

### Maintenance Layer (`decision_graph/maintenance.py`)
- **DecisionGraphMaintenance**: Monitoring and health checks
- **Methods**:
  - `get_database_stats()`: Node/stance/similarity counts, DB size
  - `analyze_growth(days)`: Growth rate and projections
  - `health_check()`: Validate data integrity
  - `estimate_archival_benefit()`: Space savings simulation

## Common Query Patterns

### 1. Find Similar Decisions

**When**: You want to see what past deliberations are related to a new question.

```python
from decision_graph.integration import DecisionGraphIntegration
from decision_graph.storage import DecisionGraphStorage

# Initialize
storage = DecisionGraphStorage("decision_graph.db")
integration = DecisionGraphIntegration(storage)

# Get similar decisions with context
question = "Should we adopt TypeScript for the project?"
context = integration.get_context_for_deliberation(question)

if context:
    print("Found relevant past decisions:")
    print(context)
else:
    print("No similar past decisions found")
```

**Direct retrieval access**:
```python
from decision_graph.retrieval import DecisionRetriever

retriever = DecisionRetriever(storage)

# Get scored results (DecisionNode, similarity_score) tuples
scored_decisions = retriever.find_relevant_decisions(
    query_question="Should we adopt TypeScript?",
    threshold=0.7,  # Deprecated but kept for compatibility
    max_results=3   # Deprecated - uses adaptive k instead
)

for decision, score in scored_decisions:
    print(f"Score: {score:.2f}")
    print(f"Question: {decision.question}")
    print(f"Consensus: {decision.consensus}")
    print(f"Participants: {', '.join(decision.participants)}")
    print("---")
```

### 2. Inspect Database Statistics

**When**: Monitoring growth, checking health, or debugging performance.

```python
# Get comprehensive stats
stats = integration.get_graph_stats()
print(f"Total decisions: {stats['total_decisions']}")
print(f"Total stances: {stats['total_stances']}")
print(f"Total similarities: {stats['total_similarities']}")
print(f"Database size: {stats['db_size_mb']} MB")

# Analyze growth rate
from decision_graph.maintenance import DecisionGraphMaintenance
maintenance = DecisionGraphMaintenance(storage)

growth = maintenance.analyze_growth(days=30)
print(f"Decisions in last 30 days: {growth['decisions_in_period']}")
print(f"Average per day: {growth['avg_decisions_per_day']}")
print(f"Projected next 30 days: {growth['projected_decisions_30d']}")
```

### 3. Validate Database Health

**When**: Debugging issues, after schema changes, or periodic maintenance.

```python
# Run comprehensive health check
health = integration.health_check()

if health['healthy']:
    print(f"Database is healthy ({health['checks_passed']}/{health['checks_passed']} checks passed)")
else:
    print(f"Found {health['checks_failed']} issues:")
    for issue in health['issues']:
        print(f"  - {issue}")

    # View detailed results
    print("\nDetails:")
    for check, result in health['details'].items():
        print(f"  {check}: {result}")
```

Common issues detected:
- Orphaned participant stances (decision_id doesn't exist)
- Orphaned similarities (source_id or target_id missing)
- Future timestamps (data corruption)
- Missing required fields (incomplete data)
- Invalid similarity scores (not in 0.0-1.0 range)

### 4. Analyze Cache Performance

**When**: Debugging slow queries or optimizing cache configuration.

```python
# Get cache statistics
retriever = DecisionRetriever(storage, enable_cache=True)

# Run some queries first to populate cache
for question in test_questions:
    retriever.find_relevant_decisions(question)

# Check cache stats
cache_stats = retriever.get_cache_stats()
print(f"L1 query cache: {cache_stats['query_cache_size']} entries")
print(f"L1 hit rate: {cache_stats['query_hit_rate']:.1%}")
print(f"L2 embedding cache: {cache_stats['embedding_cache_size']} entries")
print(f"L2 hit rate: {cache_stats['embedding_hit_rate']:.1%}")

# Invalidate cache after adding new decisions
retriever.invalidate_cache()
```

**Expected performance**:
- L1 cache hit: <2μs (instant)
- L1 cache miss: <100ms (compute similarities)
- L2 cache hit: ~50% after warmup
- Target: 60%+ L1 hit rate for production workloads

### 5. Retrieve Specific Decisions

**When**: Debugging, inspection, or building custom queries.

```python
# Get a specific decision by ID
decision = storage.get_decision_node(decision_id="uuid-here")
if decision:
    print(f"Question: {decision.question}")
    print(f"Timestamp: {decision.timestamp}")
    print(f"Consensus: {decision.consensus}")
    print(f"Status: {decision.convergence_status}")

    # Get participant stances
    stances = storage.get_participant_stances(decision.id)
    for stance in stances:
        print(f"{stance.participant}: {stance.vote_option} ({stance.confidence:.0%})")
        print(f"  Rationale: {stance.rationale}")

# Get all recent decisions
recent_decisions = storage.get_all_decisions(limit=10, offset=0)
for decision in recent_decisions:
    print(f"{decision.timestamp}: {decision.question[:50]}...")

# Find similar decisions to a known decision
similar = storage.get_similar_decisions(
    decision_id="uuid-here",
    threshold=0.7,
    limit=5
)
for decision, score in similar:
    print(f"Score: {score:.2f} - {decision.question}")
```

### 6. Manual Similarity Computation

**When**: Testing similarity detection, calibrating thresholds, or debugging retrieval.

```python
from decision_graph.similarity import QuestionSimilarityDetector

detector = QuestionSimilarityDetector()

# Check backend being used
print(f"Backend: {detector.backend.__class__.__name__}")
# Outputs: SentenceTransformerBackend, TFIDFBackend, or JaccardBackend

# Compute similarity between two questions
score = detector.compute_similarity(
    "Should we use TypeScript?",
    "Should we adopt TypeScript for our project?"
)
print(f"Similarity: {score:.3f}")

# Find similar questions from candidates
candidates = [
    ("id1", "Should we use React or Vue?"),
    ("id2", "What database should we choose?"),
    ("id3", "Should we migrate to TypeScript?")
]

matches = detector.find_similar(
    query="Should we adopt TypeScript?",
    candidates=candidates,
    threshold=0.7
)

for match in matches:
    print(f"{match['id']}: {match['score']:.2f}")
```

## Similarity Score Interpretation

The decision graph uses semantic similarity scores (0.0-1.0) to determine relevance:

| Score Range | Tier | Meaning | Example |
|-------------|------|---------|---------|
| 0.90-1.00 | Duplicate | Near-identical questions | "Use TypeScript?" vs "Should we use TypeScript?" |
| 0.75-0.89 | Strong | Highly related topics | "Use TypeScript?" vs "Adopt TypeScript for backend?" |
| 0.60-0.74 | Moderate | Related but distinct | "Use TypeScript?" vs "What language for frontend?" |
| 0.40-0.59 | Brief | Tangentially related | "Use TypeScript?" vs "Choose a static analyzer" |
| 0.00-0.39 | Noise | Unrelated or spurious | "Use TypeScript?" vs "What database to use?" |

**Thresholds in use**:
- **Noise floor** (0.40): Minimum similarity to include in results
- **Default threshold** (0.70): Legacy retrieval threshold (deprecated)
- **Strong tier** (0.75): Full formatting with stances in context
- **Moderate tier** (0.60): Summary formatting without stances

**Adaptive k** (result count):
- Small DB (<100 decisions): k=5 (exploration phase)
- Medium DB (100-999): k=3 (balanced phase)
- Large DB (≥1000): k=2 (precision phase)

## Tiered Context Formatting

The decision graph uses budget-aware tiered formatting to control token usage:

### Strong Tier (≥0.75 similarity)
**Format**: Full details with participant stances (~500 tokens)
```
### Strong Match (similarity: 0.85): Should we use TypeScript?
**Date**: 2024-10-15T14:30:00
**Convergence Status**: converged
**Consensus**: Adopt TypeScript for type safety and tooling benefits
**Winning Option**: Option A: Adopt TypeScript
**Participants**: opus@claude, gpt-4@codex, gemini-pro@gemini

**Participant Positions**:
- **opus@claude**: Voted for 'Option A' (confidence: 90%) - Strong type system reduces bugs
- **gpt-4@codex**: Voted for 'Option A' (confidence: 85%) - Better IDE support
- **gemini-pro@gemini**: Voted for 'Option A' (confidence: 80%) - Easier refactoring
```

### Moderate Tier (0.60-0.74 similarity)
**Format**: Summary without stances (~200 tokens)
```
### Moderate Match (similarity: 0.68): What language for frontend?
**Consensus**: Use TypeScript for better type safety
**Result**: TypeScript
```

### Brief Tier (0.40-0.59 similarity)
**Format**: One-liner (~50 tokens)
```
- **Brief Match** (0.45): Choose static analysis tools → ESLint with TypeScript
```

**Token budget** (default: 2000 tokens):
- Allows ~2-3 strong decisions, or
- ~5-7 moderate decisions, or
- ~20-40 brief decisions
- Formatting stops when budget reached

## Troubleshooting

### Issue: No context retrieved for similar questions

**Symptoms**: `get_context_for_deliberation()` returns empty string

**Diagnosis**:
```python
# Check if decisions exist
stats = integration.get_graph_stats()
print(f"Total decisions: {stats['total_decisions']}")

# Try direct retrieval with lower threshold
retriever = DecisionRetriever(storage)
scored = retriever.find_relevant_decisions(
    query_question="Your question here",
    threshold=0.0  # See all results
)
print(f"Found {len(scored)} candidates above noise floor (0.40)")
for decision, score in scored[:5]:
    print(f"  {score:.3f}: {decision.question[:50]}...")
```

**Common causes**:
1. **Database empty**: No past deliberations stored
2. **Below noise floor**: All similarities <0.40 (unrelated questions)
3. **Cache stale**: Cache not invalidated after adding decisions
4. **Backend mismatch**: Using Jaccard (weak) instead of SentenceTransformer (strong)

**Fixes**:
```python
# 1. Check database
if stats['total_decisions'] == 0:
    print("No decisions in database - add some first")

# 2. Lower threshold temporarily for testing
context = retriever.get_enriched_context(question, threshold=0.5)

# 3. Invalidate cache
retriever.invalidate_cache()

# 4. Check backend
detector = QuestionSimilarityDetector()
print(f"Using backend: {detector.backend.__class__.__name__}")
# If Jaccard: install sentence-transformers for better results
```

### Issue: Slow queries (>1s latency)

**Symptoms**: `find_relevant_decisions()` takes >1 second

**Diagnosis**:
```python
import time

# Measure query latency
start = time.time()
scored = retriever.find_relevant_decisions("Test question")
latency_ms = (time.time() - start) * 1000
print(f"Query latency: {latency_ms:.1f}ms")

# Check cache stats
cache_stats = retriever.get_cache_stats()
print(f"L1 hit rate: {cache_stats['query_hit_rate']:.1%}")
print(f"L2 hit rate: {cache_stats['embedding_hit_rate']:.1%}")

# Check database size
stats = integration.get_graph_stats()
print(f"Total decisions: {stats['total_decisions']}")
```

**Common causes**:
1. **Cold cache**: First query always slow (computes similarities)
2. **Large database**: >1000 decisions increases compute time
3. **No cache**: Caching disabled in retriever
4. **Slow backend**: Jaccard or TF-IDF slower than SentenceTransformer

**Performance targets**:
- Cache hit: <2μs
- Cache miss (<100 decisions): <50ms
- Cache miss (100-999 decisions): <100ms
- Cache miss (≥1000 decisions): <200ms

**Fixes**:
```python
# 1. Warm up cache (run same query twice)
retriever.find_relevant_decisions(question)  # Cold (slow)
retriever.find_relevant_decisions(question)  # Warm (fast)

# 2. Enable caching if disabled
retriever = DecisionRetriever(storage, enable_cache=True)

# 3. Reduce query limit for large databases
all_decisions = storage.get_all_decisions(limit=100)  # Not 10000

# 4. Upgrade to SentenceTransformer backend
# pip install sentence-transformers
```

### Issue: Memory usage growing

**Symptoms**: Process memory increases over time

**Diagnosis**:
```python
# Check cache sizes
cache_stats = retriever.get_cache_stats()
print(f"L1 entries: {cache_stats['query_cache_size']} (max: 200)")
print(f"L2 entries: {cache_stats['embedding_cache_size']} (max: 500)")

# Check database size
stats = integration.get_graph_stats()
print(f"Database: {stats['db_size_mb']} MB")

# Estimate memory usage
# L1: ~5KB per entry = ~1MB for 200 entries
# L2: ~1KB per entry = ~500KB for 500 entries
# Total expected: ~1.5MB for cache + DB size
```

**Common causes**:
1. **Cache unbounded**: Using custom cache without size limits
2. **Database growth**: Normal, ~5KB per decision
3. **Embedding cache**: SentenceTransformer embeddings (768 floats each)

**Fixes**:
```python
# 1. Use bounded cache (default)
retriever = DecisionRetriever(storage, enable_cache=True)
# Auto-creates cache with maxsize=200 (L1) and maxsize=500 (L2)

# 2. Monitor database growth
maintenance = DecisionGraphMaintenance(storage)
growth = maintenance.analyze_growth(days=30)
print(f"Growth rate: {growth['avg_decisions_per_day']:.1f} decisions/day")

# 3. Consider archival at 5000+ decisions (Phase 2)
if stats['total_decisions'] > 5000:
    estimate = maintenance.estimate_archival_benefit()
    print(f"Archival would save ~{estimate['estimated_space_savings_mb']} MB")
```

### Issue: Context not helping convergence

**Symptoms**: Injected context doesn't improve deliberation quality

**Diagnosis**:
```python
# Check what context was injected
context = integration.get_context_for_deliberation(question)
print(f"Context length: {len(context)} chars (~{len(context)//4} tokens)")
print(context)

# Check tier distribution in logs (look for MEASUREMENT lines)
# Example: tier_distribution=(strong:1, moderate:0, brief:2)

# Verify similarity scores
scored = retriever.find_relevant_decisions(question)
for decision, score in scored:
    print(f"Score {score:.2f}: {decision.question[:40]}...")
    if score < 0.70:
        print(f"  WARNING: Low similarity, may not be helpful")
```

**Common causes**:
1. **Low similarity**: Scores 0.40-0.60 are tangentially related
2. **Brief tier dominance**: Most context in brief format (no stances)
3. **Token budget exhausted**: Only including 1-2 decisions
4. **Contradictory context**: Past decisions conflict with current question

**Calibration approach** (Phase 1.5):
- Log MEASUREMENT lines: question, scored_results, tier_distribution, tokens, db_size
- Analyze which tiers correlate with improved convergence
- Adjust tier boundaries in config (default: strong=0.75, moderate=0.60)
- Tune token budget (default: 2000)

## Configuration

Context injection can be configured in `config.yaml`:

```yaml
decision_graph:
  enabled: true
  db_path: "decision_graph.db"

  # Retrieval settings
  similarity_threshold: 0.7        # DEPRECATED - uses noise floor (0.40) instead
  max_context_decisions: 3         # DEPRECATED - uses adaptive k instead

  # Tiered formatting (NEW)
  tier_boundaries:
    strong: 0.75                   # Full details with stances
    moderate: 0.60                 # Summary without stances
    # brief: implicit (≥0.40 noise floor)

  context_token_budget: 2000       # Max tokens for context injection
```

**Tuning recommendations**:
- Start with defaults (strong=0.75, moderate=0.60, budget=2000)
- Collect MEASUREMENT logs over 50-100 deliberations
- Analyze tier distribution vs convergence improvement
- Adjust boundaries if needed (e.g., raise to 0.80/0.70 for stricter relevance)
- Increase budget if frequently hitting limit with strong matches

## Testing Queries

```python
# Minimal test: Store and retrieve
from decision_graph.integration import DecisionGraphIntegration
from decision_graph.storage import DecisionGraphStorage
from models.schema import DeliberationResult, Summary, ConvergenceInfo

storage = DecisionGraphStorage(":memory:")
integration = DecisionGraphIntegration(storage)

# Create mock result
result = DeliberationResult(
    participants=["opus@claude", "gpt-4@codex"],
    rounds_completed=2,
    summary=Summary(consensus="Test consensus"),
    convergence_info=ConvergenceInfo(status="converged"),
    full_debate=[],
    transcript_path="test.md"
)

# Store
decision_id = integration.store_deliberation("Should we use TypeScript?", result)
print(f"Stored: {decision_id}")

# Retrieve
context = integration.get_context_for_deliberation("Should we adopt TypeScript?")
print(f"Context retrieved: {len(context)} chars")
assert len(context) > 0, "Should find similar decision"
```

## Key Files Reference

- **Storage**: `decision_graph/storage.py` - SQLite CRUD operations
- **Schema**: `decision_graph/schema.py` - DecisionNode, ParticipantStance, DecisionSimilarity
- **Retrieval**: `decision_graph/retrieval.py` - DecisionRetriever with caching
- **Integration**: `decision_graph/integration.py` - High-level API facade
- **Similarity**: `decision_graph/similarity.py` - Semantic similarity detection
- **Cache**: `decision_graph/cache.py` - Two-tier LRU caching
- **Maintenance**: `decision_graph/maintenance.py` - Stats and health checks
- **Workers**: `decision_graph/workers.py` - Async background processing

## See Also

- **CLAUDE.md**: Decision Graph Memory Architecture section
- **Tests**: `tests/unit/test_decision_graph*.py` - Unit tests with examples
- **Integration tests**: `tests/integration/test_*memory*.py` - Full workflow tests
- **Performance tests**: `tests/integration/test_performance.py` - Latency benchmarks
