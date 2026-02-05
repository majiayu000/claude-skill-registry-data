---
name: mechinterp-runner
description: Execute mechanistic interpretability experiments from JSON specs - family sweeps, itemsets, interactions, minimal cores, validation
---

# MechInterp Runner

Execute experiment specifications for mechanistic interpretability analysis. This skill takes JSON spec files and runs the appropriate analysis, producing structured result files.

## Purpose

The runner skill:
- Loads experiment specs from JSON files
- Routes to the appropriate experiment runner
- Executes the analysis with constraint enforcement
- Produces structured JSON results with diagnostics

## When to Use

Use this skill after:
1. The planner has generated experiment specs
2. You have manually created an experiment spec
3. You need to re-run an experiment with different parameters

## Supported Experiment Types

| Type | Description |
|------|-------------|
| `family_1d_sweep` | Test one ability family across AP rungs |
| `family_2d_heatmap` | Test two families in a 2D grid (e.g., SCU × ISS) |
| `frequent_itemsets` | Mine co-occurring token patterns |
| `minimal_cores` | Find irreducible activating token sets |
| `pairwise_interactions` | Compute token-pair synergy/redundancy |
| `conditional_interactions` | How a third token modulates interactions |
| `split_half` | Validation: correlation across random splits |
| `shuffle_null` | Validation: null distribution via shuffling |
| `weapon_sweep` | ⚠️ CORRELATIONAL: Analyze activation by weapon (observational grouping) |
| `kit_sweep` | ⚠️ CORRELATIONAL: Analyze activation by sub/special weapon |

## Usage

### Subcommand Interface (Recommended)

Run experiments directly without writing JSON spec files:

```bash
cd /root/dev/SplatNLP

# 1D family sweep
poetry run python -m splatnlp.mechinterp.cli.runner_cli family-sweep \
    --feature-id 6235 --family quick_respawn --model ultra

# 2D heatmap
poetry run python -m splatnlp.mechinterp.cli.runner_cli heatmap \
    --feature-id 6235 --family-x special_charge_up --family-y quick_respawn

# Weapon sweep (correlational)
poetry run python -m splatnlp.mechinterp.cli.runner_cli weapon-sweep \
    --feature-id 6235 --model ultra --top-k 20

# Kit sweep (correlational)
poetry run python -m splatnlp.mechinterp.cli.runner_cli kit-sweep \
    --feature-id 6235 --model ultra --analyze-combinations

# Binary ability presence analysis
poetry run python -m splatnlp.mechinterp.cli.runner_cli binary \
    --feature-id 6235 --model ultra

# Core coverage analysis
poetry run python -m splatnlp.mechinterp.cli.runner_cli coverage \
    --feature-id 6235 --tokens comeback,stealth_jump,respawn_punisher

# Token influence analysis
poetry run python -m splatnlp.mechinterp.cli.runner_cli token-influence \
    --feature-id 6235 --model ultra
```

### Subcommand Reference

| Subcommand | Required Args | Optional Args |
|------------|---------------|---------------|
| `family-sweep` | `--feature-id`, `--family` | `--model`, `--rungs` |
| `heatmap` | `--feature-id`, `--family-x`, `--family-y` | `--model`, `--rungs-x`, `--rungs-y` |
| `weapon-sweep` | `--feature-id` | `--model`, `--top-k`, `--min-examples` |
| `kit-sweep` | `--feature-id` | `--model`, `--top-k`, `--analyze-combinations` |
| `binary` | `--feature-id` | `--model`, `--tokens` |
| `coverage` | `--feature-id` | `--model`, `--tokens`, `--threshold` |
| `token-influence` | `--feature-id` | `--model`, `--high-percentile` |

### JSON Spec Mode (Legacy/Advanced)

For complex experiments or batch processing, use JSON spec files:

```bash
cd /root/dev/SplatNLP

# Run an experiment spec
poetry run python -m splatnlp.mechinterp.cli.runner_cli \
    --spec-path /mnt/e/mechinterp_runs/specs/20250607__f18712__family-1d-sweep.json

# With custom output directory
poetry run python -m splatnlp.mechinterp.cli.runner_cli \
    --spec-path my_spec.json \
    --output-dir ./my_results/

# Dry run (validate spec only)
poetry run python -m splatnlp.mechinterp.cli.runner_cli \
    --spec-path my_spec.json \
    --dry-run

# List available experiment types
poetry run python -m splatnlp.mechinterp.cli.runner_cli --list-types
```

### When to Use Subcommands vs JSON Specs

| Use Subcommands When | Use JSON Specs When |
|---------------------|---------------------|
| Quick one-off experiments | Batch processing multiple specs |
| Standard experiment configs | Custom dataset slices needed |
| Interactive investigation | Need to track experiment provenance |
| You want to avoid writing JSON | Complex constraint configurations |

### Programmatic

```python
from splatnlp.mechinterp.schemas import ExperimentSpec, ExperimentType
from splatnlp.mechinterp.experiments import get_runner_for_type
from splatnlp.mechinterp.skill_helpers import load_context

# Create spec
spec = ExperimentSpec(
    type=ExperimentType.FAMILY_1D_SWEEP,
    feature_id=18712,
    model_type="ultra",
    variables={"family": "special_charge_up"},
)

# Load context and run
ctx = load_context("ultra")
runner = get_runner_for_type(spec.type)
result = runner.run(spec, ctx)

# Check result
print(result.get_summary())
if result.success:
    print(f"Mean delta: {result.aggregates.mean_delta}")
```

## Spec File Format

```json
{
  "id": "20250607_142531",
  "type": "family_1d_sweep",
  "feature_id": 18712,
  "model_type": "ultra",
  "dataset_slice": {
    "percentile_min": 10.0,
    "percentile_max": 90.0,
    "sample_size": 500
  },
  "variables": {
    "family": "special_charge_up",
    "rungs": [3, 12, 29, 41, 57],
    "include_absent": true
  },
  "constraints": ["one_rung_per_family"],
  "outputs": {
    "aggregates": true,
    "tables": true,
    "diagnostics": true,
    "figures": false
  },
  "description": "Test SCU response across rungs",
  "parent_hypothesis": "h001"
}
```

## Result File Format

```json
{
  "spec_id": "20250607_142531",
  "spec_path": "20250607_142531__f18712__family-1d-sweep.json",
  "feature_id": 18712,
  "experiment_type": "family_1d_sweep",
  "aggregates": {
    "mean_delta": 0.35,
    "std_delta": 0.12,
    "n_samples": 500,
    "custom": {
      "threshold_rung": 41,
      "max_rung_delta": 0.52
    }
  },
  "tables": {
    "rung_deltas": {
      "name": "rung_deltas",
      "columns": ["rung", "mean_delta", "std_error", "n"],
      "rows": [
        {"rung": 3, "mean_delta": 0.05, "std_error": 0.02, "n": 100},
        {"rung": 12, "mean_delta": 0.12, "std_error": 0.03, "n": 100}
      ]
    }
  },
  "diagnostics": {
    "relu_floor_detected": false,
    "relu_floor_rate": 0.02,
    "n_contexts_tested": 500,
    "warnings": []
  },
  "success": true,
  "duration_seconds": 45.3
}
```

## File Locations

- **Specs**: `/mnt/e/mechinterp_runs/specs/`
- **Results**: `/mnt/e/mechinterp_runs/results/`
- **Figures**: `/mnt/e/mechinterp_runs/figures/`

## Constraint Enforcement

The runner enforces constraints specified in the spec:

- **one_rung_per_family**: Prevents invalid multi-rung builds
- **no_weapon_gating_if_relu_floor**: Warns/skips if base activation too low

Violations are logged in `diagnostics.constraint_violations` and `diagnostics.warnings`.

## Error Handling

If an experiment fails:
- `result.success` is `False`
- `result.error_message` contains the error
- Partial results may still be available in `aggregates`/`tables`

## Weapon Analysis Workflow: weapon_sweep → kit_sweep

**⚠️ IMPORTANT: Both weapon_sweep and kit_sweep are CORRELATIONAL analyses.**

They show which weapons/kits are *associated* with high activation through observational grouping, NOT through counterfactual intervention. High activation for a weapon may be because:
- The weapon itself drives the feature
- Players of that weapon tend to use certain abilities
- The weapon's kit (sub/special) is the actual driver

Always cross-reference with ability analysis to distinguish weapon effects from ability effects.

When analyzing weapon-specific patterns, follow this workflow:

### Step 1: Run weapon_sweep

```json
{
  "type": "weapon_sweep",
  "feature_id": 18712,
  "model_type": "ultra",
  "variables": {"min_examples": 10, "top_k_weapons": 20}
}
```

**Check result diagnostics** for dominant weapon warning:
- If `diagnostics.warnings` contains "DOMINANT WEAPON", one weapon has >2x delta
- `aggregates.custom.dominant_weapon_detected` will be `true`
- `aggregates.custom.recommended_followup` will be `"kit_sweep"`

### Step 2: Run kit_sweep (if dominant weapon detected)

```json
{
  "type": "kit_sweep",
  "feature_id": 18712,
  "model_type": "ultra",
  "variables": {
    "min_examples": 10,
    "top_k": 10,
    "analyze_combinations": true
  }
}
```

**Output tables:**
- `sub_stats`: Activation statistics by sub weapon (mean, std, n, delta_from_global)
- `special_stats`: Activation statistics by special weapon
- `combo_stats`: (if analyze_combinations=true) Statistics by sub+special pairs

**Aggregates:**
- `top_sub`, `top_sub_mean`, `top_sub_delta`
- `top_special`, `top_special_mean`, `top_special_delta`

### Step 3: Cross-reference with splatoon3-meta

Use the **splatoon3-meta** skill to look up weapon kits:
- Read `.claude/skills/splatoon3-meta/references/weapons.md`
- Compare dominant weapon's kit with kit_sweep results
- Check if high-activation weapons share sub or special

### Example: Feature 18712

```
weapon_sweep results:
  - Octobrush Nouveau: +0.22 delta (DOMINANT - 2.4x second weapon)
  - Rapid Blaster: +0.09 delta

kit_sweep results:
  - Top special: Ink Storm (+0.18 delta)
  - Top sub: Squid Beakon (+0.08 delta)

splatoon3-meta lookup:
  - Octobrush Nouveau: Squid Beakon + Ink Storm

Conclusion: Feature encodes "Ink Storm spam builds" not "Octobrush Nouveau builds"
```

## Known Limitations

### Binary Tokens in family_2d_heatmap

**LIMITATION**: The `family_2d_heatmap` experiment type does NOT correctly handle binary abilities (comeback, stealth_jump, haunt, etc.).

The runner uses `parse_token()` which expects tokens in `family_name_AP` format (e.g., `swim_speed_up_21`), but binary abilities appear as just the token name without an AP suffix (e.g., `comeback` not `comeback_10`).

**Workaround**: Use manual 2D analysis code for binary abilities. See the Binary Ability Analysis Protocol in **mechinterp-investigator**.

### Future Enhancement: Stable Tokens

A useful enhancement would be adding "stable tokens" to sweep experiments - tokens that are held constant across all conditions in the sweep. This would allow testing questions like:

- "How does SCU affect activation *when Comeback is present*?"
- "How does ISM scale *on Stamper builds*?"

Proposed spec format:
```json
{
  "type": "family_1d_sweep",
  "variables": {
    "family": "special_charge_up",
    "stable_tokens": ["comeback", "stealth_jump"]  // Hold these constant
  }
}
```

This is not currently implemented.

## See Also

- **mechinterp-next-step-planner**: Generate experiment specs
- **mechinterp-state**: Track research progress
- **mechinterp-summarizer**: Convert results to notes
- **mechinterp-glossary-and-constraints**: Domain reference
- **splatoon3-meta**: Weapon kit lookups and meta knowledge
