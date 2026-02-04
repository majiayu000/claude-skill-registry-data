---
name: mechinterp-overview
description: Quick "first look" overview of SAE features - top tokens, activation stats, weapons, families, sample contexts
---

# MechInterp Overview

Get a comprehensive first-look overview of an SAE feature before deep investigation. This skill provides a fast summary of key characteristics to help you decide what hypotheses to test.

## ⚠️ CRITICAL: Overview is NOT Findings

**The overview shows CORRELATIONS, not CAUSATION.** It is a starting point for generating hypotheses, NOT a source of conclusions.

| Overview Shows | What It Actually Means |
|----------------|------------------------|
| Top tokens (PageRank) | Tokens that CO-OCCUR with high activation (correlation) |
| Family breakdown | Which ability families appear in high-activation examples |
| Top weapons | Weapons present in high-activation examples |

**You CANNOT conclude from overview alone:**
- That a token "drives" or "causes" activation
- That the feature "detects" a specific ability
- That correlations are meaningful vs spurious

**To make conclusions, you MUST run experiments** (see mechinterp-investigator for deep dive basics).

## Purpose

The overview skill:
- Computes PageRank-weighted top tokens for a feature
- Shows activation statistics (mean, std, median, sparsity)
- Aggregates tokens by ability family
- Lists top weapons associated with the feature
- Provides sample high-activation contexts
- Checks for existing labels and ReLU floor issues

## When to Use

Use this skill when:
1. Starting to investigate a new feature
2. You want a quick summary before running experiments
3. Deciding which feature to label next
4. Checking if a feature has already been labeled

**DO NOT use overview results as final findings.** Always follow up with experiments.

## Output Information

| Section | Description |
|---------|-------------|
| Activation Stats | Mean, std, median, sparsity percentage, example count |
| Top Tokens | PageRank-weighted most important tokens (enhancers) |
| Bottom Tokens | Tokens suppressed in high-activation examples |
| Family Breakdown | Aggregated scores by ability family (SCU, SSU, etc.) |
| Top Weapons | Weapons with most examples for this feature |
| Sample Contexts | 3-5 high-activation example builds |
| Existing Label | Current label if one exists |
| ReLU Floor | Warning if feature is mostly zeros (>50%) |

### Sparsity Definition

**Sparsity = % of examples where feature activation is ZERO**

A high sparsity percentage means the feature fires RARELY (is selective):

| Sparsity | Meaning | Interpretation |
|----------|---------|----------------|
| 95%+ | Very sparse | Fires on only 5% of examples - very specific pattern |
| 80-95% | Moderately sparse | Good discriminative feature (fires on 5-20% of examples) |
| 50-80% | Dense | Fires often (20-50% of examples) - broad pattern |
| <50% | Very dense | Fires on majority of examples - may be baseline feature |

**Common confusion:** "89% sparsity" means "fires on 11% of examples" NOT "fires often."

Think of it as: **Sparsity = how empty/silent the feature usually is.**

**CRITICAL**: Always check the **Bottom Tokens** section! Tokens that rarely appear in high-activation examples reveal what the feature *avoids*, which is often more informative than what it detects.

## Usage

### Command Line

```bash
cd /root/dev/SplatNLP

# Basic overview (markdown output)
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 18712 \
    --model ultra

# JSON output for programmatic use
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 18712 \
    --model ultra \
    --format json

# More top tokens
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 18712 \
    --model ultra \
    --top-k 25

# Full model
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 5432 \
    --model full

# Verbose logging
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 18712 \
    --model ultra \
    --verbose
```

### Extended Analyses

Additional analysis flags provide deeper insights:

```bash
# Token enrichment (enhancers/suppressors)
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 6235 --model ultra --enrichment

# Activation region breakdown (anti-flanderization)
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 6235 --model ultra --regions

# Binary ability enrichment (main-only abilities)
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 6235 --model ultra --binary

# Sub/special weapon breakdown (kit analysis)
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 6235 --model ultra --kit

# All extended analyses at once
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 6235 --model ultra --all

# Customize high-activation threshold (default: 0.90 = top 10%)
poetry run python -m splatnlp.mechinterp.cli.overview_cli \
    --feature-id 6235 --model ultra --enrichment --high-percentile 0.95
```

### Extended Analysis Reference

| Flag | Purpose | Output |
|------|---------|--------|
| `--enrichment` | Token enrichment ratios | Suppressors (<0.8x) and enhancers (>1.2x) |
| `--regions` | Activation regions | Floor/Low/Core/High/Flanderization breakdown |
| `--binary` | Binary ability presence | Enrichment for main-only abilities (Comeback, Stealth Jump, etc.) |
| `--kit` | Sub/special breakdown | Which subs/specials appear in core region |
| `--all` | Enable all above | Combined output |
| `--kit-region` | Region for kit analysis | `core` (default), `high`, or `all` |
| `--high-percentile` | Threshold for "high" | Default: 0.90 (top 10%) |

### Programmatic

```python
from splatnlp.mechinterp.labeling import FeatureOverview, compute_overview
from splatnlp.mechinterp.skill_helpers import load_context

# Load context
ctx = load_context("ultra")

# Compute overview
overview = compute_overview(
    feature_id=18712,
    ctx=ctx,
    top_k_tokens=15,
    n_sample_contexts=5,
)

# Display markdown
print(overview.to_markdown())

# Access fields directly
print(f"Mean: {overview.activation_mean}")
print(f"Top token: {overview.top_tokens[0]}")
print(f"Main family: {max(overview.family_breakdown.items(), key=lambda x: x[1])}")
```

## Sample Output

```markdown
## Feature 18712 Overview (ultra)

### Activation Stats
- Mean: 0.5056
- Std: 0.5163
- Median: 0.3835
- Sparsity: 97.1%
- Examples: 108,163

### Top Tokens (PageRank)
1. `special_charge_up` (0.274)
2. `swim_speed_up` (0.099)
3. `ink_saver_sub` (0.084)
4. `stealth_jump` (0.049)
5. `run_speed_up` (0.048)

### Family Breakdown
- special_charge_up: 31.2%
- swim_speed_up: 11.2%
- ink_saver_sub: 9.6%

### Top Weapons
- weapon_id_5021: 28
- weapon_id_220: 28

### Bottom Tokens (Suppressors)
Tokens rarely present in high-activation examples:
1. `respawn_punisher` (high_rate_ratio=0.00) - Never in high activation
2. `special_saver` (high_rate_ratio=0.16) - 6x less common than baseline
3. `quick_respawn` (high_rate_ratio=0.47) - 2x less common than baseline

### Sample Contexts (High Activation)
1. [weapon_id_1111] special_charge_up_6, special_charge_up_57 (act=0.731)
2. [weapon_id_1111] special_charge_up_6, special_charge_up_51... (act=0.724)
```

## FeatureOverview Dataclass

```python
@dataclass
class FeatureOverview:
    feature_id: int
    model_type: str

    # Activation statistics
    activation_mean: float
    activation_std: float
    activation_median: float
    sparsity: float  # Percentage (0-100)
    n_examples: int

    # PageRank-weighted top tokens
    top_tokens: list[tuple[str, float]]

    # Bottom tokens (suppressors) - tokens excluded from high activation
    bottom_tokens: list[tuple[str, float]]  # (token, high_rate_ratio)

    # Detailed token influence statistics
    token_influences: list[TokenInfluence]

    # Aggregated by family
    family_breakdown: dict[str, float]

    # Weapon breakdown
    top_weapons: list[tuple[str, int]]

    # Sample high-activation contexts
    sample_contexts: list[SampleContext]

    # Diagnostic flags
    relu_floor_rate: float
    existing_label: str | None
```

## Performance

- Typical runtime: 30-60 seconds (dominated by PageRank computation)
- Loads activation data lazily from efficient database
- Caches context between calls in the same session

## Interpretation Tips

1. **High sparsity (>90%)**: Most inputs don't activate this feature. Look at what's special about the ones that do.

2. **ReLU floor warning**: If >50% of examples hit the ReLU floor, the feature may be hard to interpret or require special handling.

3. **Single dominant family**: If one family has >50% of the breakdown, the feature likely responds to that ability family.

4. **Multiple families**: If breakdown is spread across families, look for interactions or common contexts.

5. **Weapon concentration**: If a few weapons dominate, the feature may be weapon-specific rather than ability-specific.

## ⚠️ CRITICAL: Super-Stimuli Detection

**Don't only examine high activations - they may be "super-stimuli"!**

High activation examples can be exaggerated, "flanderized" versions of the true concept. The core region (25-75% of **effective max**) often reveals the actual feature meaning better than the flanderization zone (90%+ of effective max).

**Why "effective max"?** Activation distributions are heavy-tailed. Use `effective_max = 99.5th percentile of nonzero activations` to prevent single outliers from making your core region nearly empty.

### Warning Signs of Super-Stimuli

| Pattern | What It Means |
|---------|---------------|
| 90%+ activations only on 3-4 niche weapons | Flanderization zone = super-stimuli |
| Core region (25-75%) has diverse mainstream weapons | TRUE concept is in core region |
| One weapon spans ALL activation levels continuously | Feature is general, not weapon-specific |

### Activation Region Bins

Use these standard bins (as % of **effective max** = 99.5th percentile) to analyze feature behavior:

| Region | Range (% of effective max) | Typical Interpretation |
|--------|----------------------------|------------------------|
| Floor | ≤1% | Feature not activated |
| Low | 1-10% | Weak signal, early detection |
| Below Core | 10-25% | Emerging pattern |
| Core | 25-75% | **TRUE CONCEPT** (examine carefully!) |
| High | 75-90% | Strong expression |
| Flanderization Zone | 90%+ | Potential super-stimuli |

### Example: Feature 9971

**Initial analysis (looking only at 90%+ activations):**
- Top weapons: Bloblobber, Glooga Deco, Range Blaster, Octobrush
- Conclusion: "SCU stacker on special-dependent weapons"

**After region analysis (examining core 25-75%):**
- Core region: Splattershot (115), Wellstring (65), Sploosh (57)
- Splattershot appears in EVERY region (29→125→83→115→61→19)
- True concept: "General offensive investment (death-averse)"
- Flanderization zone (90%+): "Super-stimuli" version on niche special-dependent weapons

**Key insight**: Label the core-region concept, not the flanderized extreme!

### Coverage Threshold Rule

**When overview shows a dominant token or weapon, CHECK CORE-REGION COVERAGE before treating it as the concept.**

A token can have high enrichment in the tail but be a **tail marker**, not the true concept.

| Metric | Interpretation |
|--------|----------------|
| >50% core coverage | **Primary concept** - safe to use in label |
| 30-50% core coverage | **Significant but not universal** - note in label, don't headline |
| <30% core coverage | **Tail marker / super-stimulus** - NOT the concept |

**Example (Feature 13934):**
```
Overview showed: respawn_punisher with 8.57x tail enrichment
BUT: RP only present in 12% of core-region examples

⚠️ Flag in overview: "respawn_punisher: high enrichment (8.57x) but <30% core coverage - may be tail marker, not core concept"
```

**When to flag:** If any token in top-10 has enrichment >3x but core coverage <30%, add a warning note.

6. **Weapon Outlier Detection**: If a single weapon has >2x the examples of the second weapon, this is a **weapon-dominated feature**:
   - Use **splatoon3-meta** skill to look up the weapon's kit (sub + special)
   - Check if other high-activation weapons share the same sub OR special
   - If they share kit components, the feature may encode kit behavior, not weapon behavior
   - Run **kit_sweep** experiment to analyze activation by sub/special

7. **Check suppressors**: Always examine bottom tokens! If death-mitigation abilities (QR, SS, CB) are suppressed, the feature encodes "death-averse" builds. See **mechinterp-ability-semantics** for semantic groupings.

8. **Enhancers + Suppressors together**: The combination tells the full story. A feature with SCU enhanced AND death-perks suppressed isn't just "SCU detector" - it's "death-averse special builds".

9. **"Weak activation" ≠ "unimportant feature"**: If all scaling effects are weak (max_delta < 0.03), don't immediately label as "weak feature". Check the feature's **decoder weights** to output tokens. Net influence = activation × decoder weight. A feature with low activation effects but high decoder weights may still strongly influence predictions.

## ⚠️ WARNING: Correlation ≠ Causation

**PageRank scores show correlation, NOT causation.** Tokens appearing in the overview may be:
- **True drivers**: Actually cause activation changes
- **Spurious correlations**: Just happen to co-occur with the true driver

### How to Distinguish

1. **Run 1D sweep** for top token (likely primary driver)
2. **If confirmed**, run **2D heatmaps** for other tokens:
   - `PRIMARY × SECONDARY` reveals if secondary has conditional effect
   - If secondary shows effect only at high primary → true interaction
   - If secondary shows NO effect at any primary level → spurious

### Example: Feature 18712

```
Overview showed: SCU (24%), Opening Gambit (17%), SSU (12%)

1D sweeps:
- SCU: strong effect (0.03→0.58) ✅ PRIMARY
- OG: delta ≈ 0 → appears to have no effect
- SSU: delta ≈ 0 → appears to have no effect

BUT WAIT! 1D sweeps for secondary abilities are MISLEADING.

2D heatmaps (SCU × OG, SCU × SSU):
- Both show NO conditional effect at any SCU level
- Conclusion: OG and SSU were SPURIOUS correlations

2D heatmaps (SCU × QR, SCU × SS):
- QR_12+ SUPPRESSES activation by 70-99% at high SCU!
- SS_12+ SUPPRESSES activation by 40-60%!
- Conclusion: Feature is DEATH-AVERSE (not visible in 1D)
```

**Always verify top overview tokens with conditional 2D testing!**

See **mechinterp-investigator** for the full Iterative Conditional Testing Protocol.

## See Also

- **mechinterp-labeler**: Manage labeling workflow and save labels
- **mechinterp-runner**: Run experiments to test hypotheses
- **mechinterp-next-step-planner**: Generate experiment specs based on overview
- **mechinterp-glossary-and-constraints**: Reference for token families and AP rungs
- **mechinterp-ability-semantics**: Ability semantic groupings (check AFTER forming hypotheses)
- **mechinterp-investigator**: Full investigation workflow
