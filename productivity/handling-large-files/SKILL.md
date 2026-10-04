---
name: handling-large-files
description: Strategies for reading, chunking, and processing files that exceed practical token limits. Covers streaming reads, selective extraction, summarization-before-analysis, and memory-efficient patterns for large codebases, logs, or datasets. Use whenever a file or set of files is too large to fit in context at once. Do NOT use for normally-sized files — adds unnecessary overhead.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Handling Large Files

Efficiently processing large files is critical for agent performance and cost management. This skill provides strategies to minimize token consumption while maintaining code quality and context accuracy.

## When to Use This Skill

Use this skill when:

- Processing files larger than 50KB
- Working with complete codebases or large documentation
- Facing token budget constraints
- Reading multiple large files simultaneously
- Streaming or chunking file content
- Needing to extract specific information from large files
- Optimizing API costs with token-limited models
- Analyzing large datasets or logs

## Core Workflow

Task Progress:

- [ ] Assess file size and content type
- [ ] Choose appropriate reading strategy
- [ ] Implement token-efficient processing
- [ ] Validate context extraction
- [ ] Execute operation with optimizations

### Step 1: Assess File Size and Content Type

Determine:

1. **Actual size**: Use `wc -c` or `stat` for accurate byte count
2. **Estimated tokens**: Multiply size (bytes) by 0.25 for rough English text estimate
3. **Content structure**: Identify sections, formats, or repetitive patterns
4. **Purpose**: What specific information do you need?

Example assessment:

```bash
# Check file size and estimate tokens
stat -f%z file.ts    # macOS
stat -c%s file.ts    # Linux
wc -c file.ts        # Both

# Quick token estimate (rough): bytes × 0.25
# 100KB × 0.25 ≈ 25,000 tokens
```

### Step 2: Choose Reading Strategy

Select the optimal approach based on file characteristics:

#### Strategy A: Targeted Range Reading

**Best for**: Files with clear sections or when specific ranges are needed

```
- Use read_file with startLine and endLine parameters
- Reduces context to only relevant sections
- Efficient for large files with focused questions
- Token savings: 40-80%
```

**Example**:

```
Need to check error handling in auth.ts (500 lines)?
Read lines 250-350 (authentication logic) instead of entire file
```

#### Strategy B: Semantic Search + Read

**Best for**: Locating specific functionality or patterns

```
- Use semantic_search to find relevant code
- Then read_file only those sections
- Combines discoverability with efficiency
- Token savings: 50-90%
```

**Example**:

```
1. semantic_search("database connection pooling")
2. Get file paths and line ranges from results
3. read_file only relevant sections
```

#### Strategy C: Grep Search + Targeted Read

**Best for**: Pattern matching or finding implementations

```
- Use grep_search for exact string/regex matches
- Quickly identify file regions containing patterns
- Follow with minimal read_file calls
- Token savings: 60-95%
```

**Example**:

```
1. grep_search("interface UserService", isRegexp=false)
2. Get results with line numbers
3. Read surrounding context only
```

#### Strategy D: Structural Analysis

**Best for**: Understanding code organization without reading full content

```
- Use file_search with glob patterns
- Get directory listings to understand structure
- Read architecture first, then dive into specifics
- Token savings: 70-85%
```

#### Strategy E: Parallel Smart Batching

**Best for**: Processing multiple large files efficiently

```
- Group related read operations
- Execute independent reads in parallel
- Sequential reads only for dependent operations
- Token savings: 30-50% (time savings: much higher)
```

**Never do**:

```
- Don't read files sequentially when they're independent
- Don't load entire large files without clear purpose
- Don't mix multiple concerns in single large read
```

### Step 3: Implement Token-Efficient Processing

#### 3.1 Pre-Processing Strategies

Before reading a file, reduce scope:

1. **Line Range Estimation**

   ```
   - Average token count: ~4 tokens per line of code
   - Want 1000 tokens? Read ~250 lines
   - Identify relevant line ranges before reading
   ```

2. **Content Filtering**

   ```
   - Comments and whitespace: ~30% of tokens, often skippable
   - Test files: Often 50% of codebase size, read only when needed
   - Configuration files: Usually dense, read entirely
   - Documentation: Skim for sections, read relevant parts
   ```

3. **Abstraction Level**
   ```
   - Read interfaces/types first (high-level understanding)
   - Read implementations only when clarification needed
   - Token savings: 40-70%
   ```

#### 3.2 Reading Patterns

**Pattern: Section-by-Section**

```
- Identify logical sections (functions, classes, imports)
- Read one at a time with clear boundaries
- Build understanding incrementally
- Good for complex files
```

**Pattern: Divide and Conquer**

```
- Large file? Split into 20% chunks
- Process each chunk independently
- Combine context only for integration points
- Scales to arbitrary file sizes
```

**Pattern: Query-Driven**

```
- Ask specific question: "Where is X implemented?"
- Use search tools first
- Read only what answers the question
- Most efficient approach
```

#### 3.3 Content Summarization

For unavoidable large reads:

```python
# Pseudo-code for summarization patterns
1. Read file
2. If tokens > budget:
   - Extract key structures (functions, classes)
   - Keep comments and docstrings
   - Remove implementation details
   - Create summary view
3. Use summary for initial analysis
4. Deep-dive into specific sections as needed
```

### Step 4: Validate Context Extraction

Ensure you're getting correct information:

1. **Correctness check**: Line numbers match expected code
2. **Completeness check**: Related elements (imports, types) are included
3. **Relevance check**: Content answers your original question
4. **Efficiency check**: Could fewer tokens answer the question?

### Step 5: Execute with Optimizations

Apply these principles in order of priority:

1. **Avoid unnecessary reads**: Use tools to locate first
2. **Read targeted ranges**: startLine/endLine parameters
3. **Parallel reads**: When independent
4. **Minimize output display**: Only show key findings
5. **Cache context**: Remember findings to avoid re-reading

## Common Scenarios

### Scenario 1: Understanding a Large Codebase

```
Goal: Understand architecture of 50MB codebase
Budget: 15,000 tokens

1. Use file_search to identify structure
2. Read key files: package.json, main entry point
3. Use semantic_search("architecture OR design")
4. Read only referenced implementation files
5. Total tokens used: ~8,000

Result: Good architecture understanding, 7,000 tokens spare
```

### Scenario 2: Debugging in Large File

```
Goal: Fix error in 2MB log file
Budget: 5,000 tokens

1. grep_search("ERROR|FAILURE") to locate problematic sections
2. read_file only those line ranges
3. Keep surrounding context minimal
4. Total tokens used: ~1,200

Result: Problem identified, 3,800 tokens spare
```

### Scenario 3: Code Review of Multiple Files

```
Goal: Review 10 modified files (avg 5KB each)
Budget: 10,000 tokens

1. Parallel: file_search for all modifications
2. Parallel: read_file for all 10 files (targeted ranges)
3. Identify patterns across files
4. Targeted semantic_search for related tests
5. Total tokens used: ~7,500

Result: Complete review, within budget
```

### Scenario 4: Extracting Documentation

```
Goal: Create guide from 500KB documentation
Budget: 20,000 tokens

1. file_search to identify relevant doc files
2. file_search within docs for structure
3. Read only target sections (20% of total)
4. semantic_search for examples related to task
5. Total tokens used: ~12,000

Result: Comprehensive guide extracted, 8,000 tokens spare
```

## Quick Reference: Token Savings

| Strategy            | Savings | Best For          |
| ------------------- | ------- | ----------------- |
| Range reading       | 40-80%  | Specific sections |
| Semantic search     | 50-90%  | Pattern finding   |
| Grep search         | 60-95%  | Exact matching    |
| Structural analysis | 70-85%  | Understanding org |
| Parallel batching   | 30-50%  | Multiple files    |
| Targeted extraction | 60-95%  | Specific data     |

## Anti-Patterns to Avoid

❌ **Don't**: Read entire large file without knowing why

```
- Always determine specific information needed first
- Use search tools to locate relevant sections
```

❌ **Don't**: Process files sequentially when independent

```
- Parallelize independent file reads
- Only sequence reads with dependencies
```

❌ **Don't**: Ignore token estimates before reading

```
- Always estimate tokens: size_bytes × 0.25 (approximate)
- Adjust strategy if estimate exceeds budget
```

❌ **Don't**: Forget context for follow-up questions

```
- Cache important findings to avoid re-reading
- Reference previous reads when available
```

❌ **Don't**: Use generic search without specificity

```
- Semantic searches must target precise concepts
- Grep searches should use specific patterns
```

## Decision Tree

```
Large file encountered?

├─ Need specific information?
│  ├─ YES → Use semantic_search or grep_search first
│  │        → read_file only matching ranges
│  └─ NO → Need to understand overall structure?
│
├─ File > 500KB?
│  ├─ YES → Use divide-and-conquer or search-first
│  └─ NO → Consider range reading or full read
│
└─ Multiple independent files?
   ├─ YES → Execute reads in parallel
   └─ NO → Sequential reads acceptable
```

## References

- [Token Estimation Strategies](reference/token-estimation.md)
- [File Processing Patterns](reference/processing-patterns.md)
- [Optimization Techniques](reference/optimization-techniques.md)
- [Tools and Commands](reference/tools-commands.md)
