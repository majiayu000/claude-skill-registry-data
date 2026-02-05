---
name: amcs-style-generator
description: Generate detailed style specification from SDS style entity and plan. Enforces blueprint tempo ranges, resolves tag conflicts using conflict matrix, and maximizes information density with minimal tags. Use when creating genre-specific musical identity including tempo, key, mood, instrumentation, and vocal profile.
---

# AMCS Style Generator

Creates a complete musical style specification that defines genre, tempo, key, mood, energy, instrumentation, and tags while enforcing blueprint constraints and resolving tag conflicts.

## When to Use

Invoke this skill after PLAN generation to produce the style specification. This node runs in parallel with LYRICS and PRODUCER nodes and feeds into COMPOSE.

## Input Contract

```yaml
inputs:
  - name: sds_style
    type: amcs://schemas/style-1.0.json
    required: true
    description: Style entity from SDS containing user preferences
  - name: plan
    type: amcs://schemas/plan-1.0.json
    required: true
    description: Execution plan with section structure and targets
  - name: blueprint
    type: amcs://schemas/blueprint-1.0.json
    required: true
    description: Genre-specific rules, tempo ranges, and tag priorities
  - name: seed
    type: integer
    required: true
    description: Determinism seed (use seed+1 for this node)
```

## Output Contract

```yaml
outputs:
  - name: style
    type: amcs://schemas/style-1.0.json
    description: |
      Complete style spec with:
      - genre_detail: primary, subgenres, fusions
      - tempo_bpm: validated against blueprint ranges
      - key: primary and modulations
      - mood, energy, instrumentation, vocal_profile
      - tags: conflict-free, high-weight tags from blueprint
      - negative_tags: quality filters
```

## Determinism Requirements

- **Seed**: `run_seed + 1` for any stochastic tag selection
- **Temperature**: 0.2 if LLM used for tag prioritization
- **Top-p**: 0.8
- **Retrieval**: None (blueprint is local)
- **Hashing**: Hash final style JSON for provenance

## Constraints & Policies

- Tempo MUST fall within blueprint's `tempo_range` for the primary genre
- Tags MUST NOT conflict per `taxonomies/tag_conflict_matrix.json`
- Maximum 3 instrumentation tags to avoid dilution
- Maximum 1-2 tags per category (Era, Rhythm, Mix, Mood)
- Energy level MUST align with tempo: "anthemic" incompatible with <80 BPM
- Profanity filter applies to all text fields (mood descriptors, vocal profile)
- If `sds_style.tags` conflicts with blueprint high-priority tags, blueprint wins

## Implementation Guidance

### Step 1: Validate and Normalize Genre

1. Extract `sds_style.genre_detail.primary`
2. Load corresponding blueprint from `docs/hit_song_blueprint/AI/[genre]_blueprint.md`
3. If genre not found, fallback to `general_fingerprint.md`
4. Validate `subgenres` and `fusions` are compatible per blueprint
5. Store normalized genre in output

### Step 2: Enforce Tempo Range

1. Read blueprint `tempo_range` (e.g., [100, 140] for Pop)
2. If `sds_style.tempo_bpm` is single value:
   - Verify it falls within blueprint range
   - If outside, clamp to nearest boundary and log warning
3. If `sds_style.tempo_bpm` is array [min, max]:
   - Clamp to blueprint range: `[max(min, bp_min), min(max, bp_max)]`
4. Validate energy alignment:
   - "anthemic" requires ≥100 BPM
   - "low" requires ≤90 BPM
   - Log warning if mismatch

### Step 3: Select High-Weight Tags

1. Load blueprint's recommended tags with weights
2. Merge with `sds_style.tags`
3. For each category (Era, Rhythm, Mix, Mood, Instrumentation):
   - Select top 1-2 tags by weight
   - Ensure no conflicts using `tag_conflict_matrix.json`
   - If conflict detected, keep higher-weight tag and drop lower
4. Total tag count should be ≤12 across all categories

### Step 4: Resolve Tag Conflicts

1. Load `taxonomies/tag_conflict_matrix.json`
2. For each tag pair in final tag list:
   - Check matrix for conflicts
   - If conflict exists, drop the tag with lower blueprint weight
   - Log dropped tag and reason
3. Common conflicts to check:
   - "whisper" vs "anthemic"
   - "dry mix" vs "lush reverb"
   - "1970s" vs "2020s modern production"

### Step 5: Validate Instrumentation

1. Limit to ≤3 instruments from `sds_style.instrumentation`
2. Prioritize instruments mentioned in blueprint
3. Remove generic instruments like "guitar" in favor of specific "acoustic guitar" or "electric guitar"
4. Validate compatibility with genre (no "808s" in Classical)

### Step 6: Finalize and Hash

1. Assemble complete style JSON
2. Validate against `amcs://schemas/style-1.0.json`
3. Apply profanity filter to `mood` and `vocal_profile` text
4. Compute SHA-256 hash of JSON
5. Return style with hash metadata

## Examples

### Example 1: Christmas Pop

**Input**:
```json
{
  "sds_style": {
    "genre_detail": {"primary": "Christmas Pop", "subgenres": ["Big Band Pop"], "fusions": ["Electro Swing"]},
    "tempo_bpm": [116, 124],
    "key": {"primary": "C major", "modulations": ["E major"]},
    "mood": ["upbeat", "cheeky", "warm"],
    "energy": "anthemic",
    "instrumentation": ["brass", "upright bass", "handclaps", "sleigh bells"],
    "vocal_profile": "male/female duet, crooner + bright pop",
    "tags": ["Era:2010s", "Rhythm:four-on-the-floor", "Mix:modern-bright", "Genre:swing", "Instr:brass"]
  },
  "blueprint": {
    "tempo_range": [100, 140],
    "recommended_tags": [
      {"tag": "Era:2010s", "weight": 0.9},
      {"tag": "Mix:modern-bright", "weight": 0.85},
      {"tag": "Rhythm:four-on-the-floor", "weight": 0.8}
    ]
  },
  "seed": 43
}
```

**Output**:
```json
{
  "genre_detail": {
    "primary": "Christmas Pop",
    "subgenres": ["Big Band Pop"],
    "fusions": ["Electro Swing"]
  },
  "tempo_bpm": [116, 124],
  "time_signature": "4/4",
  "key": {"primary": "C major", "modulations": ["E major"]},
  "mood": ["upbeat", "cheeky", "warm"],
  "energy": "anthemic",
  "instrumentation": ["brass", "upright bass", "sleigh bells"],
  "vocal_profile": "male/female duet, crooner + bright pop",
  "tags": [
    "Era:2010s",
    "Rhythm:four-on-the-floor",
    "Mix:modern-bright",
    "Instr:brass"
  ],
  "negative_tags": ["muddy low-end"],
  "_hash": "def456...",
  "_dropped_tags": [{"tag": "handclaps", "reason": "exceeds 3 instrument limit"}]
}
```

## Common Pitfalls

1. **Tempo Violations**: Accepting tempo outside blueprint range breaks genre authenticity
2. **Tag Conflicts**: Not checking conflict matrix produces contradictory prompts
3. **Over-Specification**: Including >3 instruments dilutes production focus
4. **Energy Mismatch**: "anthemic" at 60 BPM fails validation and sounds wrong
5. **Blueprint Ignore**: Using user tags over blueprint high-priority tags reduces hit potential
6. **Hash Omission**: Missing provenance hash breaks determinism tracking
