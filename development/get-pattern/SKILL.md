---
name: "get-pattern"
description: "Retrieve APPLICATION patterns (architecture, procedures, conventions) from AgentDB skills table. Use BEFORE implementing to ensure consistency."
---

# Get Pattern - Retrieve Application Knowledge

## What This Skill Does

Retrieves established **application patterns** (architecture, procedures, conventions) for the Neural Data Platform using AgentDB's semantic skill search.

**Use this BEFORE implementing anything** to ensure you follow project standards.

---

## Quick Reference

```bash
# Search for patterns by description
agentdb skill search "domain adapter pattern" 5

# Fallback: search reflexion episodes for past experiences
agentdb reflexion retrieve "how to add a stream" --k 5 --only-successes

# View all stored patterns
agentdb db stats
```

---

## Primary Method: Skill Search

```bash
agentdb skill search "<query>" <k>
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `<query>` | What you're looking for (semantic search) |
| `<k>` | Number of results (default: 5) |

### Examples

```bash
# Find architecture patterns
agentdb skill search "domain adapter pattern" 5

# Find deployment procedures
agentdb skill search "deploy to raspberry pi" 3

# Find naming conventions
agentdb skill search "naming conventions streams fields" 3

# Find troubleshooting guides
agentdb skill search "mqtt data not appearing" 5
```

---

## Fallback Method: Reflexion Retrieve

If no skill patterns exist, search past experiences:

```bash
agentdb reflexion retrieve "<query>" --k 5 --only-successes --synthesize-context
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `<query>` | Task description to find similar work |
| `--k` | Number of results |
| `--only-successes` | Only successful episodes |
| `--min-reward` | Minimum success score (0-1) |
| `--synthesize-context` | Generate coherent summary |

### Examples

```bash
# Find successful similar work
agentdb reflexion retrieve "HTTP source implementation" \
  --k 5 \
  --only-successes \
  --min-reward 0.7

# Get synthesized context
agentdb reflexion retrieve "timescaledb schema" \
  --k 10 \
  --synthesize-context
```

---

## Pattern Categories

| Category | Example Queries |
|----------|-----------------|
| Architecture | "domain adapter pattern", "hexagonal architecture" |
| Data Flow | "ingestion pipeline", "bronze silver gold" |
| Development | "add new stream", "implement source trait" |
| Deployment | "docker deployment", "raspberry pi setup" |
| Troubleshooting | "mqtt not working", "parquet write errors" |
| Conventions | "naming conventions", "code organization" |

---

## Interpreting Results

Results from `skill search` include:

| Field | Meaning |
|-------|---------|
| `Name` | Pattern identifier |
| `Description` | The pattern content |
| `Success Rate` | How often this pattern succeeded (0-100%) |
| `Uses` | Number of times used |

**High-value patterns**: Success Rate > 80% AND Uses > 3

---

## Typical Workflow

```bash
# 1. Search for existing patterns
agentdb skill search "what I'm about to implement" 5

# 2. If found: Follow the pattern
# 3. If not found: Check reflexion for past experiences
agentdb reflexion retrieve "similar task" --k 5 --only-successes

# 4. After work: Record feedback
agentdb reflexion store "feature-id" "task" 0.9 true "Pattern worked well"

# 5. If you discovered something new: Save it
agentdb skill create "pattern-name" "description" "optional-details"
```

---

## CRITICAL: Record Pattern Usage

After using a pattern, **always use the `reflexion` skill** to record whether it helped:

```bash
# Pattern worked well
agentdb reflexion store "dp-004" \
  "Used domain-adapter pattern for new HTTP source" \
  1.0 true \
  "Pattern was complete - followed steps exactly, tests passed"

# Pattern needed fixes
agentdb reflexion store "dp-004" \
  "Used add-stream pattern but needed adjustment" \
  0.6 true \
  "Pattern missing retention field - should update via save-pattern"
```

Without feedback, the system can't learn which patterns work.

---

## If No Patterns Found

1. **Check pattern stats:**
   ```bash
   agentdb db stats
   ```

2. **Search reflexion episodes:**
   ```bash
   agentdb reflexion retrieve "your query" --k 10 --synthesize-context
   ```

3. **Check file-based documentation:**
   - `docs/architecture/` - Architecture documents
   - `docs/procedures/` - Step-by-step procedures
   - `product/features/*/architecture/` - Feature ADRs

4. **After implementing**, store the new pattern via `save-pattern`

---

## The Pattern Workflow

```
1. BEFORE work:  get-pattern  → Search for relevant patterns (THIS SKILL)
2. DURING work:  Apply the pattern, note what works/gaps
3. AFTER work:   reflexion    → Record if pattern helped (required)
                 save-pattern → Store NEW discoveries (if any)
                 learner      → Auto-discover patterns from episodes (periodic)
```

---

## Related Skills

- **`save-pattern`** - Store NEW patterns after discovering reusable approaches
- **`reflexion`** - Record feedback on pattern effectiveness (REQUIRED after using patterns)
- **`learner`** - Auto-discover patterns from successful episodes (user-invoked)

---

## What NOT to Use This For

| Don't Search For | Use Instead |
|------------------|-------------|
| Current swarm status | claude-flow swarm tools |
| Agent task state | claude-flow task tools |
| Working memory | claude-flow memory tools |
| Session context | claude-flow memory with TTL |

**Patterns are PERMANENT application knowledge, not transient swarm state.**
