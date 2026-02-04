---
name: amcs-plan-generator
description: Generate execution plan from Song Design Spec (SDS). Extracts section structure, calculates target metrics, and produces ordered work objectives for downstream workflow nodes. Use when processing SDS to determine song arrangement, section ordering, target word counts, and evaluation criteria.
---

# AMCS Plan Generator

Transforms a Song Design Spec (SDS) into a deterministic execution plan that guides all downstream workflow nodes.

## When to Use

Invoke this skill as the first node in the AMCS workflow when processing a new SDS. The plan establishes section order, target metrics, and evaluation criteria that inform Style, Lyrics, and Producer nodes.

## Input Contract

```yaml
inputs:
  - name: sds
    type: amcs://schemas/sds-1.0.json
    required: true
    description: Complete Song Design Spec containing all entity specs and constraints
  - name: seed
    type: integer
    required: true
    description: Determinism seed for this run
```

## Output Contract

```yaml
outputs:
  - name: plan
    type: amcs://schemas/plan-1.0.json
    description: |
      Execution plan containing:
      - section_order: Array of section names in performance order
      - target_word_counts: Per-section word count targets
      - evaluation_targets: Rubric thresholds from blueprint
      - work_objectives: Ordered list of tasks for downstream nodes
```

## Determinism Requirements

- **Seed**: Use run seed directly (no RNG calls in this node)
- **Temperature**: N/A (no LLM generation required)
- **Top-p**: N/A
- **Retrieval**: None
- **Hashing**: Hash the complete plan output for provenance tracking

## Constraints & Policies

- Section order MUST include at least one "Chorus" section
- Total target word count MUST respect `sds.constraints.max_lines` converted to approximate words (avg 6 words/line)
- Section requirements from `sds.lyrics.constraints.section_requirements` MUST be preserved
- If hook strategy is "lyrical" or "chant", require at least 2 chorus sections
- Duration targets MUST sum to within ±30 seconds of `sds.constraints.duration_sec`
- All blueprint-specified evaluation thresholds MUST be included in `evaluation_targets`

## Implementation Guidance

### Step 1: Extract Section Structure

1. Read `sds.lyrics.section_order` to get the base section sequence
2. Validate that at least one "Chorus" exists; if not, return error
3. If `sds.lyrics.hook_strategy` is "lyrical" or "chant", verify ≥2 chorus sections
4. Copy section order to `plan.section_order`

### Step 2: Calculate Target Metrics

1. For each section in `section_order`:
   - Check `sds.lyrics.constraints.section_requirements[section]` for min/max lines
   - Convert lines to approximate word counts (6 words/line avg)
   - Store in `plan.target_word_counts[section]`

2. Validate total:
   - Sum all section word counts
   - Verify ≤ `sds.constraints.max_lines * 6` words
   - If exceeded, proportionally reduce section targets

3. Duration targets:
   - If `sds.producer_notes.section_meta` contains `target_duration_sec`, copy to plan
   - Verify sum matches `sds.constraints.duration_sec` (±30s tolerance)

### Step 3: Define Evaluation Targets

1. Load blueprint for `sds.style.genre_detail.primary`
2. Extract rubric thresholds:
   - `hook_density`: minimum acceptable score
   - `singability`: minimum acceptable score
   - `rhyme_tightness`: minimum acceptable score
   - `section_completeness`: minimum acceptable score
   - `profanity_score`: maximum acceptable score (0 if `explicit=false`)
   - `total`: minimum composite score

3. Store in `plan.evaluation_targets`

### Step 4: Create Work Objectives

Generate ordered list of objectives for downstream nodes:

```json
{
  "work_objectives": [
    {
      "node": "STYLE",
      "objective": "Generate style spec with tempo [min-max], key [primary], mood [list], enforcing blueprint tempo ranges and tag conflict matrix",
      "dependencies": []
    },
    {
      "node": "LYRICS",
      "objective": "Produce lyrics for sections [list], enforcing rhyme scheme [scheme], meter [meter], hook strategy [strategy]",
      "dependencies": ["STYLE"]
    },
    {
      "node": "PRODUCER",
      "objective": "Create production notes with [N] hooks, structure [structure], section tags from plan",
      "dependencies": ["STYLE"]
    },
    {
      "node": "COMPOSE",
      "objective": "Merge artifacts into render-ready prompt respecting [engine] character limits",
      "dependencies": ["STYLE", "LYRICS", "PRODUCER"]
    }
  ]
}
```

### Step 5: Validate and Return

1. Validate plan against `amcs://schemas/plan-1.0.json`
2. Compute SHA-256 hash of plan JSON
3. Return plan with hash in metadata

## Examples

### Example 1: Christmas Pop Song

**Input**:
```json
{
  "sds": {
    "style": {"genre_detail": {"primary": "Christmas Pop"}},
    "lyrics": {
      "section_order": ["Intro", "Verse", "PreChorus", "Chorus", "Verse", "Chorus", "Bridge", "Chorus"],
      "hook_strategy": "chant",
      "constraints": {
        "max_lines": 120,
        "section_requirements": {
          "Chorus": {"min_lines": 6, "max_lines": 10}
        }
      }
    },
    "producer_notes": {
      "hooks": 2,
      "section_meta": {
        "Intro": {"target_duration_sec": 10},
        "Chorus": {"target_duration_sec": 25}
      }
    },
    "constraints": {"duration_sec": 180, "max_lines": 120}
  },
  "seed": 42
}
```

**Output**:
```json
{
  "section_order": ["Intro", "Verse", "PreChorus", "Chorus", "Verse", "Chorus", "Bridge", "Chorus"],
  "target_word_counts": {
    "Intro": 30,
    "Verse": 96,
    "PreChorus": 60,
    "Chorus": 54,
    "Bridge": 72
  },
  "evaluation_targets": {
    "hook_density": 0.7,
    "singability": 0.8,
    "rhyme_tightness": 0.75,
    "section_completeness": 0.9,
    "profanity_score": 0.0,
    "total": 0.8
  },
  "work_objectives": [
    {"node": "STYLE", "objective": "Generate Christmas Pop style with anthemic energy, brass instrumentation", "dependencies": []},
    {"node": "LYRICS", "objective": "Produce chant-heavy lyrics with AABB rhyme scheme across 8 sections", "dependencies": ["STYLE"]},
    {"node": "PRODUCER", "objective": "Create production notes with 2 hooks, lush mix, section-specific tags", "dependencies": ["STYLE"]},
    {"node": "COMPOSE", "objective": "Merge into Suno-compatible prompt under 5000 chars", "dependencies": ["STYLE", "LYRICS", "PRODUCER"]}
  ],
  "_hash": "abc123..."
}
```

## Common Pitfalls

1. **Missing Chorus**: Failing to validate chorus presence causes downstream validation failures
2. **Word Count Overflow**: Not checking total against `max_lines` leads to truncated lyrics
3. **Duration Mismatch**: Ignoring `target_duration_sec` sum validation causes rendering issues
4. **Blueprint Mismatch**: Using wrong blueprint for genre results in inappropriate thresholds
5. **Determinism Loss**: Introducing any randomness breaks reproducibility guarantee
