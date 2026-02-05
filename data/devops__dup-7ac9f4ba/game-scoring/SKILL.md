---
name: game-scoring
description: >-
  Use when working with candidate scoring, confidence calculation, softmax
  aggregation, or guess decision logic. Load for understanding how candidates
  are ranked, when the system decides to guess, and how semantic + geographic
  scores combine. Covers temperature tuning, entropy thresholds, and margin logic.
---

# Game Scoring

Scoring and confidence calculation patterns specific to this game.

> **Announce:** "I'm using game-scoring to understand scoring logic correctly."

## Scoring Pipeline Overview

```
Player Description
       ↓
   Embedding
       ↓
Semantic Similarity (per place)
       ↓
Geographic Filtering (include/exclude regions)
       ↓
Combined Score + Softmax
       ↓
Confidence Metrics (max_prob, margin, entropy)
       ↓
Decision: Ask Question or Guess?
```

## Semantic Similarity

Traits are matched via embedding similarity:

```sql
-- For each place, calculate trait similarity
WITH trait_similarities AS (
  SELECT 
    pt.place_id,
    1 - (te.embedding <=> v_description_embedding) AS similarity
  FROM place_traits pt
  JOIN embeddings te ON te.id = pt.embedding_id
)
```

## Softmax Aggregation

**NOT simple average.** Softmax lets top traits dominate:

```sql
-- Softmax-weighted average
WITH softmax_weights AS (
  SELECT 
    place_id,
    similarity,
    exp(similarity / v_temperature) AS exp_sim,
    SUM(exp(similarity / v_temperature)) OVER (PARTITION BY place_id) AS sum_exp
  FROM trait_similarities
)
SELECT 
  place_id,
  SUM((exp_sim / sum_exp) * similarity) AS aggregated_score
FROM softmax_weights
GROUP BY place_id;
```

**Temperature effect:**
- Low (0.1): Top traits dominate strongly
- High (1.0): All traits contribute more equally

## Confidence Metrics

Three metrics determine when to guess:

```sql
-- Calculate from candidate probabilities
SELECT
  MAX(probability) AS max_prob,           -- Top candidate confidence
  MAX(probability) - MAX(second_prob) AS margin,  -- Gap to #2
  -SUM(p * ln(p)) AS entropy              -- Spread of distribution
FROM candidates;
```

| Metric | High Value Means | When to Guess |
|--------|------------------|---------------|
| `max_prob` | Strong #1 candidate | > threshold (e.g., 0.7) |
| `margin` | Clear separation | > threshold (e.g., 0.3) |
| `entropy` | Spread out (uncertain) | < threshold (e.g., 1.0) |

## Guess Decision Logic

```sql
-- System guesses when confident
IF v_max_prob >= get_config_float('confidence.top_prob_threshold')
   AND v_margin >= get_config_float('confidence.margin_threshold')
   AND v_entropy <= get_config_float('confidence.entropy_threshold')
THEN
  -- Make a guess
  RETURN create_guess_turn(v_top_candidate);
ELSE
  -- Ask a question
  RETURN create_question_turn(v_best_question);
END IF;
```

## Score Combination

Semantic and geographic scores combine:

```sql
-- Final score = semantic * (1 + geographic_bonus)
SELECT
  place_id,
  semantic_score,
  geographic_bonus,  -- From region matching
  semantic_score * (1 + geographic_bonus) AS combined_score
FROM scored_candidates
ORDER BY combined_score DESC;
```

## Configuration Parameters

All thresholds come from `game_logic.config`:

```sql
-- Scoring
get_config_float('scoring.temperature', 0.5)
get_config_float('scoring.initial_candidate_threshold', 0.3)

-- Confidence
get_config_float('confidence.top_prob_threshold', 0.7)
get_config_float('confidence.margin_threshold', 0.3)
get_config_float('confidence.entropy_threshold', 1.5)

-- Question selection
get_config_float('questions.min_split_quality', 0.3)
```

## Question Selection

Questions are ranked by split quality:

```sql
-- Perfect split = 0.5 yes, 0.5 no → quality = 1.0
-- All yes or all no → quality = 0.5
split_quality = 1.0 - ABS(0.5 - yes_ratio)
```

Best question maximizes information gain.

## Answer Processing

Answers update candidate scores:

```sql
-- 'yes' answer for geographic question
-- Keep only candidates in the region
UPDATE candidates SET
  active = ST_Intersects(geom, region_geom)
WHERE session_id = v_session_id;

-- 'no' answer
-- Keep only candidates NOT in the region
UPDATE candidates SET
  active = NOT ST_Intersects(geom, region_geom)
WHERE session_id = v_session_id;

-- 'not_sure' answer
-- Apply uncertainty penalty
UPDATE candidates SET
  score = score * get_config_float('scoring.unsure_penalty', 0.9)
WHERE session_id = v_session_id;
```

## Anti-Patterns

### DON'T: Use Simple Average

```sql
-- WRONG: All traits equal weight
SELECT place_id, AVG(similarity) FROM trait_similarities

-- CORRECT: Softmax-weighted for categorical matching
SELECT place_id, SUM((exp_sim/sum_exp) * similarity)
```

### DON'T: Hardcode Thresholds

```sql
-- WRONG: Magic numbers
IF max_prob > 0.7 AND margin > 0.3 THEN

-- CORRECT: From config
IF max_prob > get_config_float('confidence.top_prob_threshold')
   AND margin > get_config_float('confidence.margin_threshold') THEN
```

### DON'T: Skip Entropy

```sql
-- WRONG: Only check max_prob
IF max_prob > 0.7 THEN guess()

-- CORRECT: Check all three metrics
-- High max_prob with high entropy = false confidence
IF max_prob > threshold 
   AND margin > threshold 
   AND entropy < threshold THEN guess()
```

## Debugging Scores

```sql
-- View current candidates with scores
SELECT 
  c.place_id,
  p.name,
  c.semantic_score,
  c.geographic_bonus,
  c.combined_score,
  c.probability
FROM session_candidates c
JOIN places p ON p.id = c.place_id
WHERE c.session_id = 'xxx'
ORDER BY c.probability DESC
LIMIT 10;
```

## References

See `references/scoring-queries.md` for debugging queries.
