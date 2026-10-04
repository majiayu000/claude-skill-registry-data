---
name: cognitive
description: Cognitive systems skill for reasoning, memory, and agent behavior; use when designing agent workflows or mental-model tooling.
---

# Skill: Cognitive

Domain: `agent` | Depth: `axiom`

## Capabilities
- Reasoning chains: chain-of-thought, tree-of-thought, self-consistency
- Working memory management: context window, sliding window, summarization
- Episodic memory: store and retrieve past experiences
- Semantic memory: vector-based concept retrieval (ChromaDB)
- Attention modeling: relevance scoring, salience weighting
- Meta-cognition: confidence estimation, uncertainty quantification
- Belief updating: Bayesian reasoning primitives
- Pattern recognition across dimensional records (Akashic field)

## Architecture
- Working memory: last N turns + auto-summarize on overflow
- Episodic memory: SQLite — timestamped facts and sessions
- Semantic memory: ChromaDB — vector similarity retrieval
- Akashic field: dimensional records — domain/depth/resonance retrieval

## Libraries
| Library   | Purpose |
|-----------|---------|
| torch     | Attention, embeddings |
| numpy     | Probability and belief arrays |
| scipy     | Statistical reasoning |
| chromadb  | Semantic memory backend |

## Module
`agents/skills/cognitive.py`

## Key Functions
- `chain_of_thought(problem, steps)` — structured reasoning scaffold
- `confidence(logits)` — softmax confidence from raw scores
- `bayesian_update(prior, likelihood, evidence)` — posterior belief
- `attention_score(query, keys)` — dot-product attention weights
- `summarize_context(turns, max_tokens)` — compress working memory
- `retrieve_relevant(concept, memory, n)` — semantic memory retrieval
