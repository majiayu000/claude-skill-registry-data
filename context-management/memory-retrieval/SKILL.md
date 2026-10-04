---
name: memory-retrieval
description: "Two-stage memory retrieval skill using semantic matching and utility filtering for higher-quality recall."
---

# Two-Stage Memory Retrieval

## Description
A high-quality memory retrieval skill based on MemRL paper (arXiv:2601.03192). Uses a two-stage process: semantic matching followed by utility filtering to solve the "stability-plasticity dilemma" in memory systems.

## Activation Keywords
- 记忆检索
- memory retrieval
- 查找知识
- find knowledge
- 搜索记忆
- search memory
- 两阶段检索
- two-stage retrieval
- 效用过滤
- utility filtering

## Recommended Model
- **sonnet4.5** (Recommended for semantic understanding and utility evaluation)

## Tools Used
- memory_search: Semantic search in MEMORY.md and memory/*.md
- memory_get: Retrieve specific memory snippets
- read: Read full memory files when needed
- write: Update memory with utility scores

## Usage Patterns

### Basic Retrieval
```
查找关于 [topic] 的知识
```

### With Context
```
检索记忆：[query]，上下文：[context]
```

### Utility-Based
```
查找最相关的 [topic] 知识，按效用排序
```

## Instructions for Agents

### Overview

The two-stage retrieval solves a fundamental problem in memory systems:

```
┌─────────────────────────────────────────────────────────┐
│           Two-Stage Memory Retrieval                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Stage 1: Semantic Matching                             │
│   ┌─────────────────────────────────────────────────┐   │
│   │  Query → memory_search → Relevant Results       │   │
│   │  (Broad search, semantic similarity)            │   │
│   └─────────────────────────────────────────────────┘   │
│                        ↓                                 │
│   Stage 2: Utility Filtering                            │
│   ┌─────────────────────────────────────────────────┐   │
│   │  Results → Utility Scoring → Filtered Results   │   │
│   │  (Quality check, usefulness rating)             │   │
│   └─────────────────────────────────────────────────┘   │
│                        ↓                                 │
│   High-Quality Memory Retrieval                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Stage 1: Semantic Matching

**Purpose:** Find all potentially relevant memories

**Process:**
1. **Construct Query**
   - Extract key concepts from user request
   - Generate multiple query variants
   - Include synonyms and related terms

2. **Execute Search**
   ```python
   # Use memory_search tool
   memory_search(
       query="search terms",
       maxResults=10,  # Get more results for filtering
       minScore=0.5    # Lower threshold for broad match
   )
   ```

3. **Collect Results**
   - Gather all matching snippets
   - Note file paths and line numbers
   - Preserve context around matches

**Output:** List of semantically relevant memory snippets

### Stage 2: Utility Filtering

**Purpose:** Filter and rank by practical usefulness

**Utility Scoring Formula:**
```
Utility = (Recency × 0.3) + (SuccessRate × 0.4) + (Relevance × 0.3)

Where:
- Recency: How recently was this memory used (0-1)
- SuccessRate: How often did it help solve problems (0-1)
- Relevance: How relevant to current context (0-1)
```

**Evaluation Criteria:**

| Factor | Weight | Measurement |
|--------|--------|-------------|
| Recency | 0.3 | Days since last use |
| Success Rate | 0.4 | Successful applications / Total uses |
| Relevance | 0.3 | Semantic similarity score |
| User Feedback | Bonus | Positive feedback adds +0.1 |

**Process:**
1. **Score Each Result**
   ```python
   def calculate_utility(result, current_context):
       recency = get_recency_score(result.last_used)
       success_rate = result.success_count / result.use_count
       relevance = calculate_relevance(result, current_context)
       
       utility = (recency * 0.3) + (success_rate * 0.4) + (relevance * 0.3)
       
       # Apply bonus for user feedback
       if result.has_positive_feedback:
           utility += 0.1
       
       return min(utility, 1.0)  # Cap at 1.0
   ```

2. **Filter Low-Utility Results**
   ```python
   # Default threshold
   UTILITY_THRESHOLD = 0.5
   
   filtered_results = [
       r for r in results
       if r.utility >= UTILITY_THRESHOLD
   ]
   ```

3. **Rank by Utility**
   ```python
   ranked_results = sorted(
       filtered_results,
       key=lambda r: r.utility,
       reverse=True
   )
   ```

**Output:** Ranked list of high-utility memory snippets

### Integration Pattern

```python
def two_stage_retrieval(query, context, max_results=5):
    """Two-stage memory retrieval with utility filtering."""
    
    # Stage 1: Semantic Matching
    semantic_results = memory_search(
        query=query,
        maxResults=max_results * 2,  # Get more for filtering
        minScore=0.5
    )
    
    # Stage 2: Utility Filtering
    scored_results = []
    for result in semantic_results:
        utility = calculate_utility(result, context)
        if utility >= UTILITY_THRESHOLD:
            scored_results.append({
                'content': result.content,
                'source': result.path,
                'utility': utility
            })
    
    # Rank and return
    ranked = sorted(scored_results, key=lambda r: r['utility'], reverse=True)
    return ranked[:max_results]
```

## Context Files

### ~/.openclaw/workspace/MEMORY.md
Long-term memory file with utility metadata.

### ~/.openclaw/workspace/memory/*.md
Daily memory files.

### ~/.openclaw/workspace/memory/utility-scores.json
Utility scores for memory entries (to be created).

```json
{
  "MEMORY.md#主动汇报约定": {
    "use_count": 5,
    "success_count": 4,
    "last_used": "2026-03-05T11:00:00Z",
    "utility": 0.85
  }
}
```

## Error Handling

### No Results Found
```
If Stage 1 returns no results:
  1. Broaden query terms
  2. Lower minScore threshold
  3. Search in related domains
  4. Report "No relevant memory found"
```

### All Results Filtered Out
```
If Stage 2 filters all results:
  1. Lower UTILITY_THRESHOLD temporarily
  2. Return best available result with warning
  3. Suggest creating new memory entry
```

### Utility Data Missing
```
If utility scores don't exist:
  1. Default to recency + relevance only
  2. Initialize utility tracking
  3. Track future uses for scoring
```

## Examples

### Example 1: Basic Retrieval

```
User: "查找关于股票分析的技能"

Agent Process:
1. Stage 1: Semantic Matching
   - Query: "股票分析 stock analysis skill"
   - Results: 5 matches found

2. Stage 2: Utility Filtering
   - Scoring each result:
     * stock-analysis SKILL.md: utility=0.9 (high success)
     * akshare usage: utility=0.75 (recent use)
     * old analysis notes: utility=0.4 (outdated)
   
   - Filtered: 2 results above threshold

3. Return ranked results:
   1. stock-analysis SKILL.md (utility: 0.9)
   2. akshare usage notes (utility: 0.75)

Agent: 找到 2 条相关记忆（按效用排序）：

**1. stock-analysis 技能** (效用: 0.9)
- 来源: knowledge/skills/external/stock-analysis.md
- 成功率: 90%, 最近使用: 今天

**2. AkShare 使用笔记** (效用: 0.75)
- 来源: knowledge/topics/optimization/api-stability.md
- 成功率: 75%, 最近使用: 昨天
```

### Example 2: Context-Aware Retrieval

```
User: "我需要处理 API 超时问题，查找相关知识"

Agent Process:
1. Stage 1: Semantic Matching
   - Query: "API timeout 超时处理 error handling"
   - Context: Current task is about API reliability
   - Results: 8 matches found

2. Stage 2: Utility Filtering
   - Context relevance scoring:
     * timeout-handling.md: relevance=0.95 (exact match)
     * api-stability.md: relevance=0.85 (related)
     * general error handling: relevance=0.5 (generic)
   
   - Combined utility:
     * timeout-handling.md: utility=0.92
     * api-stability.md: utility=0.78
     * general error: utility=0.45 (filtered out)

3. Return context-aware results:
   1. timeout-handling.md (utility: 0.92)
   2. api-stability.md (utility: 0.78)

Agent: 找到 2 条高相关记忆：

**1. 超时处理指南** (效用: 0.92)
- 高度相关当前任务
- 来源: knowledge/topics/optimization/timeout-handling.md

**2. API 稳定性方案** (效用: 0.78)
- 包含新浪财经备用 API
- 来源: TOOLS.md#api-数据源备份方案
```

## Best Practices

1. **Track Usage**: Record when memory entries are used
2. **Track Success**: Note if memory helped solve problems
3. **Periodic Cleanup**: Remove or archive low-utility memories
4. **Context Matters**: Always consider current task context
5. **Iterate Thresholds**: Adjust utility threshold based on results

## Limitations

- Requires utility tracking infrastructure
- Initial utility scores may be inaccurate
- Can filter out potentially useful but untested memories
- Requires regular maintenance of utility data

## Implementation Checklist

- [ ] Create utility-scores.json tracking file
- [ ] Implement utility calculation function
- [ ] Add usage tracking to memory access
- [ ] Add success/failure tracking
- [ ] Create periodic utility recalculation
- [ ] Add threshold configuration

## Resources

- **Source Paper**: https://arxiv.org/abs/2601.03192
- **MEMORY.md**: ~/.openclaw/workspace/MEMORY.md
- **Utility Tracking**: ~/.openclaw/workspace/memory/utility-scores.json

## Related Skills
- ice-review: Consolidate knowledge after tasks
- self-challenge: Test and validate memories
- skill-extractor: Extract patterns from memories

## Notes

- Two-stage retrieval significantly improves result quality
- The "stability-plasticity dilemma" refers to balancing old knowledge with new
- Utility scoring should be domain-aware for best results
- Consider user preferences in utility calculation
