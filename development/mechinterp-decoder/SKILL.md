---
name: mechinterp-decoder
description: Analyze SAE decoder weights - output influence, feature importance, and decoder similarity
---

# MechInterp Decoder

Analyze SAE features through their decoder weights. This skill answers: **"What does this feature RECOMMEND?"** rather than "What activates this feature?"

## Purpose

Decoder analysis provides a complementary perspective to activation analysis:

| Analysis Type | Question Answered |
|---------------|-------------------|
| **Activation** (overview, sweeps) | "What inputs activate this feature?" |
| **Decoder** (this skill) | "What outputs does this feature promote?" |

For **diffuse or heterogeneous features** where activation analysis shows multiple modes, decoder analysis often reveals the unifying concept.

## When to Use

Use this skill when:

1. **Activation analysis is inconclusive** - Multiple modes or no clear pattern
2. **Feature appears heterogeneous** - Different builds activate it for different reasons
3. **Looking for "what does it recommend"** - Shift from inputs to outputs
4. **Checking AP level preferences** - Does feature prefer low-AP (_3, _6) vs high-AP (_57)?
5. **Finding similar features** - Cluster features by decoder similarity

## Commands

### Output Influence

Show what tokens a feature promotes (positive contribution) or suppresses (negative contribution):

```bash
cd /root/dev/SplatNLP

# Basic output influence
poetry run python -m splatnlp.mechinterp.cli.decoder_cli output-influence \
    --feature-id 13934 \
    --model ultra

# JSON output
poetry run python -m splatnlp.mechinterp.cli.decoder_cli output-influence \
    --feature-id 13934 \
    --model ultra \
    --format json

# More tokens
poetry run python -m splatnlp.mechinterp.cli.decoder_cli output-influence \
    --feature-id 13934 \
    --model ultra \
    --top-k 25
```

**Sample Output:**
```markdown
## Feature 13934 Output Influence (ultra)

### Tokens This Feature PROMOTES

| Token | Contribution | Family | AP Level |
|-------|--------------|--------|----------|
| respawn_punisher | +0.232 | respawn_punisher | binary |
| comeback | +0.159 | comeback | binary |
| quick_super_jump_6 | +0.155 | quick_super_jump | 6 |
| intensify_action_3 | +0.140 | intensify_action | 3 |
| ink_saver_main_6 | +0.128 | ink_saver_main | 6 |

### Tokens This Feature SUPPRESSES

| Token | Contribution | Family | AP Level |
|-------|--------------|--------|----------|
| run_speed_up_57 | -0.301 | run_speed_up | 57 |
| quick_respawn_57 | -0.247 | quick_respawn | 57 |
| swim_speed_up_57 | -0.209 | swim_speed_up | 57 |

### Interpretation
- **Top promoted**: respawn_punisher (+0.232)
- **Top suppressed**: run_speed_up_57 (-0.301)
- **Pattern**: Promotes low-AP tokens, suppresses high-AP stacking
```

### Weight Percentile

Check how important a feature is by its decoder weight magnitude:

```bash
poetry run python -m splatnlp.mechinterp.cli.decoder_cli weight-percentile \
    --feature-id 13934 \
    --model ultra
```

**Sample Output:**
```markdown
## Feature 13934 Decoder Weight (ultra)

- **Magnitude**: 2.3456
- **Percentile**: 78.5%
- **Total features**: 24576
```

**Interpretation:**
- High percentile (>90%): Feature has strong output influence
- Low percentile (<10%): Feature has weak output influence
- Note: Low-magnitude features may still be important for specific tokens

### Similar Features (by Decoder)

Find features with similar decoder patterns (what they recommend):

```bash
poetry run python -m splatnlp.mechinterp.cli.decoder_cli similar \
    --feature-id 13934 \
    --model ultra \
    --top-k 10
```

**Sample Output:**
```markdown
## Features Similar to 13934 (ultra)

| Feature ID | Cosine Similarity |
|------------|-------------------|
| 13892 | 0.9234 |
| 14501 | 0.8876 |
| 12044 | 0.8521 |
```

## Experiment Runner

For programmatic use or integration with runner_cli:

```bash
# Create spec file
cat > decoder_spec.json << 'EOF'
{
  "type": "decoder_output_analysis",
  "feature_id": 13934,
  "model_type": "ultra",
  "variables": {
    "top_k_promoted": 15,
    "top_k_suppressed": 15,
    "group_by_family": true,
    "include_ap_level": true
  }
}
EOF

# Run via runner CLI
poetry run python -m splatnlp.mechinterp.cli.runner_cli \
    --spec-path decoder_spec.json
```

## Interpretation Guide

### AP Level Patterns

| Pattern | Meaning |
|---------|---------|
| Promotes _3, _6; Suppresses _51, _57 | "Use balanced spread, not stacking" |
| Promotes _57; Suppresses low AP | "Heavy stacking is the goal" |
| Promotes binary (RP, CB, OG) | "These specific abilities are key" |
| Mixed AP levels promoted | "Ability presence matters, not amount" |

### Common Feature Types

| Output Pattern | Feature Type |
|----------------|--------------|
| Single family promoted | Family detector (e.g., SCU detector) |
| Low-AP promoted, high-AP suppressed | "Balanced utility recommendation" |
| Binary abilities promoted | "Build style marker" (aggressive, defensive) |
| Death perks promoted (QR, SS, CB) | "Death-tolerant" archetype |
| Death perks suppressed | "Death-averse" archetype |

## Integration with Investigation Workflow

Decoder analysis fits into the investigation workflow as follows:

```
1. Overview (mechinterp-overview)
   ↓
2. Hypothesis formation
   ↓
3. 1D Sweeps (mechinterp-runner)
   ↓
4. Core Coverage Check ← NEW: Catch tail markers
   ↓
5. If diffuse/heterogeneous:
   → Decoder Output Analysis ← THIS SKILL
   ↓
6. Label formulation
```

## Example: Feature 13934 (from investigation log)

**Problem**: Activation analysis showed two opposite modes (RP anchor vs Zombie builds).

**Solution**: Decoder analysis revealed unifying pattern:

```
PROMOTES: low-AP utility (_3, _6 tokens)
SUPPRESSES: heavy stacking (_51, _57 tokens)

→ Feature recommends "balanced utility spread" regardless of death strategy
```

**Key Insight**: Different builds (RP vs Zombie) activate the feature because they share a NEED (balanced utility), not a BUILD pattern.

## See Also

- **mechinterp-overview**: Initial feature assessment
- **mechinterp-runner**: Run experiments (including core_coverage_analysis, decoder_output_analysis)
- **mechinterp-investigator**: Full investigation workflow
- **mechinterp-labeler**: Save labels after investigation
