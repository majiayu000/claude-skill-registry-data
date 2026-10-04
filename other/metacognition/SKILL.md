---
name: metacognition
description: Self-reflection engine for AI agents. Extracts patterns from session transcripts into a weighted graph with Hebbian learning and time decay. Compiles a token-budgeted lens of active self-knowledge.
metadata: {"openclaw":{"requires":{"bins":["python3"]},"writablePaths":["memory/metacognition.json","scripts/metacognition-lens.md"],"readablePaths":["memory/"],"env":{"EMBEDDINGS_URL":"optional, localhost-only embeddings endpoint (defaults to http://localhost:4821/v1/embeddings, remote URLs rejected at startup)","WORKSPACE":"optional, workspace root path"},"security":"localhost-only network (EMBEDDINGS_URL validated to 127.0.0.1/localhost/::1 at import time, remote URLs disable embeddings entirely), no curl/subprocess — uses Python stdlib urllib only, extract command limited to 1MB file reads","homepage":"https://github.com/meimakes/metacognition","author":"Mei Park (@meimakes)"}}
---

# Metacognition Skill

A self-reflection engine for AI agents. Extracts patterns from session transcripts into a weighted graph with Hebbian learning and time decay.

## What It Does

- Maintains a store of categorized insights (perceptions, overrides, protections, self-observations, decisions, curiosities)
- Uses Hebbian reinforcement: repeated insights get stronger, unused ones decay
- Builds a graph of connections between related insights
- Finds clusters of related knowledge that may represent higher-level principles
- Compiles a "metacognition lens" — a token-budgeted summary of active self-knowledge

## Setup

1. Place `metacognition.py` in your workspace `scripts/` directory
2. The script stores data in `memory/metacognition.json` (relative to workspace)
3. The compiled lens outputs to `scripts/metacognition-lens.md`
4. Optionally configure a local embeddings endpoint for semantic similarity (falls back to string matching)

## Cron Integration

Set up a cron job to run periodically (e.g., every 4 hours):

```
METACOGNITION INTEGRATION. You are the self-reflection engine.

1. Run `cd <WORKSPACE> && python3 scripts/metacognition.py decay` to prune weak entries.

2. Use sessions_list + sessions_history to read the main session's recent conversation.

3. Analyze the conversation for DEEPER patterns:
   - PATTERNS: Am I repeating the same kind of mistake? What does that reveal?
   - ANTICIPATION: What did the human need that I could have predicted?
   - RELATIONSHIP: What did I learn about how the user communicates or what they value?
   - CONFIDENCE: Where was I certain and wrong? Where was I uncertain but right?
   - GROWTH: What's a higher-level principle behind today's specific events?

4. For each genuine insight (1-3, quality over quantity), add it:
   `python3 scripts/metacognition.py add <type> "<insight>"`
   Types: perceptions, overrides, protections, self-observations, decisions, curiosities
   Write insights as PRINCIPLES, not incident reports.

5. Run `python3 scripts/metacognition.py reweave` to build graph connections.

6. Run `python3 scripts/metacognition.py compile` to rebuild the lens.

7. Report only if something genuinely interesting was extracted.
```

## CLI Commands

```
python3 metacognition.py add <type> <text>       # Add or merge an entry
python3 metacognition.py list [type]              # List entries
python3 metacognition.py feedback <id> <pos|neg>  # Reinforce or weaken
python3 metacognition.py decay                    # Apply time-based decay
python3 metacognition.py compile                  # Compile the lens
python3 metacognition.py extract <path>           # Extract from a daily note
python3 metacognition.py resolve <id>             # Mark curiosity resolved
python3 metacognition.py reweave                  # Build graph connections
python3 metacognition.py graph                    # Show graph stats
python3 metacognition.py integrate                # Full cycle
```

## Configuration

Key constants in the script:

| Constant | Default | Description |
|----------|---------|-------------|
| `HALF_LIFE_DAYS` | 7.0 | How quickly unreinforced entries decay |
| `STRENGTH_CAP` | 3.0 | Maximum strength an entry can reach |
| `LENS_TOKEN_BUDGET` | 500 | Token budget for compiled lens |
| `EMBEDDING_SIM_THRESHOLD` | 0.85 | Similarity threshold for merging (embeddings) |
| `FALLBACK_SIM_THRESHOLD` | 0.72 | Similarity threshold for merging (string matching) |
| `EDGE_SIM_THRESHOLD` | 0.35 | Threshold for creating graph edges |

## Entry Types

- **perceptions** — Things learned from experience
- **overrides** — Corrections to previous beliefs
- **protections** — Rules to prevent known failure modes
- **self-observations** — Patterns in own behavior
- **decisions** — Policy decisions for future behavior
- **curiosities** — Open questions with lifecycle (born → active → evolving → resolved)
