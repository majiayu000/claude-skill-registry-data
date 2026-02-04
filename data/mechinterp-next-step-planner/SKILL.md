---
name: mechinterp-next-step-planner
description: Propose next mechanistic interpretability experiments based on research state, hypotheses, and existing evidence
---

# MechInterp Next-Step Planner

Analyze current research state and propose the next best experiments to run. Writes ExperimentSpec JSON files directly to the specs directory.

## Purpose

The planner skill:
- Analyzes current hypotheses and their evidence status
- Identifies gaps in understanding
- Proposes 2-3 experiments that would discriminate between hypotheses
- Writes ExperimentSpec JSON files ready for the runner

## When to Use

Use this skill when you need to:
- Decide what experiment to run next
- Find experiments that test uncertain hypotheses
- Generate specs after updating research state
- Plan a sequence of experiments

## Decision Heuristics

The planner considers:

1. **Hypothesis uncertainty**: Prioritize experiments for hypotheses with confidence near 0.5
2. **Evidence gaps**: Look for hypotheses with few evidence items
3. **Validation needs**: Suggest validation for high-confidence hypotheses (>0.7)
4. **ReLU floor avoidance**: Skip weapon experiments if activation is low
5. **Constraint compliance**: All specs enforce one-rung-per-family
6. **Suppressor detection**: Suggest token_influence_sweep when single-family features may have hidden suppressors

## Planning Workflow

### 1. Load Current State

```python
from splatnlp.mechinterp.state import ResearchStateManager

manager = ResearchStateManager(feature_id=18712, model_type="ultra")
print(manager.get_summary())
```

### 2. Analyze Evidence Gaps

Check which hypotheses need more testing:

```python
for h in manager.state.hypotheses:
    n_support = len(h.supporting_evidence)
    n_refute = len(h.refuting_evidence)
    print(f"{h.id}: conf={h.confidence:.0%}, support={n_support}, refute={n_refute}")

    if h.status == "proposed" and n_support == 0:
        print(f"  -> NEEDS TESTING")
    elif h.confidence > 0.7 and h.status == "supported":
        print(f"  -> NEEDS VALIDATION")
```

### 3. Generate Experiment Specs

Based on the analysis, create appropriate specs:

```python
from splatnlp.mechinterp.schemas import ExperimentSpec, ExperimentType
from splatnlp.mechinterp.state.io import get_spec_path, SPECS_DIR
import json
from datetime import datetime

# Example: Family sweep for untested hypothesis about SCU
spec = ExperimentSpec(
    id=datetime.now().strftime("%Y%m%d_%H%M%S"),
    type=ExperimentType.FAMILY_1D_SWEEP,
    feature_id=18712,
    model_type="ultra",
    variables={
        "family": "special_charge_up",
        "rungs": [3, 12, 29, 41, 57],
        "include_absent": True
    },
    dataset_slice={
        "percentile_min": 10.0,
        "percentile_max": 90.0,
        "sample_size": 500
    },
    description="Test SCU response to identify threshold rung",
    parent_hypothesis="h001",
    rationale="Hypothesis h001 claims SCU >= 41 AP triggers feature. "
              "This sweep will identify the exact threshold."
)

# Write spec to file
spec_path = SPECS_DIR / spec.to_filename()
spec_path.parent.mkdir(parents=True, exist_ok=True)
spec_path.write_text(spec.model_dump_json(indent=2))
print(f"Spec written to: {spec_path}")
```

### 4. Common Experiment Templates

#### For Family-Specific Hypotheses

```python
# "Feature responds to family X at high AP"
ExperimentSpec(
    type=ExperimentType.FAMILY_1D_SWEEP,
    feature_id=feature_id,
    model_type="ultra",
    variables={"family": "swim_speed_up"},
)
```

#### For Multi-Family Interactions

```python
# "SCU and ISS have synergistic effect"
ExperimentSpec(
    type=ExperimentType.FAMILY_2D_HEATMAP,
    feature_id=feature_id,
    model_type="ultra",
    variables={
        "family_x": "special_charge_up",
        "family_y": "ink_saver_sub"
    },
)
```

#### For Pattern Discovery

```python
# "Feature detects specific ability combinations"
ExperimentSpec(
    type=ExperimentType.FREQUENT_ITEMSETS,
    feature_id=feature_id,
    model_type="ultra",
    variables={
        "min_support": 0.05,
        "max_size": 4,
        "high_activation_pct": 10.0
    },
)
```

#### For Validation

```python
# Validate stable high-confidence hypothesis
ExperimentSpec(
    type=ExperimentType.SPLIT_HALF,
    feature_id=feature_id,
    model_type="ultra",
    variables={"n_splits": 10},
    parent_hypothesis="h001",
)
```

#### For Token Influence Analysis (Enhancers + Suppressors)

```python
# Identify both enhancing and suppressing tokens
# CRITICAL: Use this when you need to understand what a feature AVOIDS
ExperimentSpec(
    type=ExperimentType.TOKEN_INFLUENCE_SWEEP,
    feature_id=feature_id,
    model_type="ultra",
    variables={
        "min_samples": 50,
        "high_percentile": 0.995,  # Top 0.5%
        "collapse_families": True,
        "suppressor_threshold": 0.8,  # < 0.8 = suppressed
        "enhancer_threshold": 1.2,    # > 1.2 = enhanced
    },
    description="Identify enhancers and suppressors for complete interpretation",
)
```

## Planner Decision Tree

```
┌─────────────────────────────────────────┐
│     Load Research State                 │
└────────────────┬────────────────────────┘
                 │
    ┌────────────▼────────────┐
    │  Any hypotheses?         │
    └────────────┬────────────┘
                 │
         No ◄────┴────► Yes
         │               │
         ▼               ▼
┌─────────────────┐ ┌─────────────────────────┐
│ Exploration     │ │ Any untested?           │
│ - PageRank      │ └────────────┬────────────┘
│ - Itemsets      │              │
│ - Family sweeps │      Yes ◄───┴───► No
└─────────────────┘       │              │
                          ▼              ▼
                 ┌─────────────┐ ┌─────────────────┐
                 │ Test most   │ │ Any uncertain?  │
                 │ uncertain   │ │ (conf ~0.5)     │
                 └─────────────┘ └────────┬────────┘
                                          │
                                  Yes ◄───┴───► No
                                   │             │
                                   ▼             ▼
                          ┌─────────────┐ ┌─────────────────┐
                          │ Discriminate│ │ Any high-conf   │
                          │ experiments │ │ need validation?│
                          └─────────────┘ └────────┬────────┘
                                                   │
                                           Yes ◄───┴───► No
                                            │             │
                                            ▼             ▼
                                   ┌─────────────┐ ┌───────────┐
                                   │ Validation  │ │ Research  │
                                   │ experiments │ │ complete! │
                                   └─────────────┘ └───────────┘
```

## Guardrails

The planner enforces these rules:

1. **One-rung-per-family**: All specs include this constraint
2. **ReLU floor check**: If state has pitfall "relu_floor_at_low_activation", avoid weapon sweeps
3. **Evidence diversification**: Prefer different experiment types than recently run
4. **Hypothesis coverage**: Ensure all active hypotheses have at least one pending experiment
5. **Suppressor check**: For single-family features, suggest token_influence_sweep to detect what the feature AVOIDS (critical for complete interpretation)
6. **Conditional sweep requirement**: After confirming primary driver with 1D sweep, ALWAYS suggest 2D heatmaps for secondary abilities (see below)

## ⚠️ CRITICAL: Conditional 2D Sweep Logic

**After a 1D sweep confirms a primary driver, 1D sweeps for other abilities are MISLEADING.**

### Why 1D Sweeps Fail for Secondary Abilities

When feature has strong primary driver (e.g., SCU):
- Most contexts have LOW primary → activation ≈ 0
- Secondary ability can't suppress zero
- 1D sweep averages across ALL contexts → delta ≈ 0
- **False conclusion**: "secondary has no effect"

### Planner Logic

```python
def suggest_next_experiments(state):
    # Check if primary driver is confirmed
    primary_confirmed = any(
        h.status == "supported" and h.confidence > 0.7
        for h in state.hypotheses
        if "primary" in h.tags or "monotonic" in h.tags
    )

    if primary_confirmed:
        primary_family = get_confirmed_primary(state)
        correlated_abilities = get_overview_top_tokens(state, top_k=10)

        # For EACH correlated ability, suggest 2D heatmap
        for ability in correlated_abilities:
            if ability != primary_family:
                suggest_2d_heatmap(
                    family_x=primary_family,
                    family_y=ability,
                    rationale=f"Test conditional effect of {ability} at each {primary_family} level"
                )

        # ALWAYS suggest death-mitigation battery
        for death_ability in ["quick_respawn", "special_saver", "comeback"]:
            if not already_tested(state, primary_family, death_ability):
                suggest_2d_heatmap(
                    family_x=primary_family,
                    family_y=death_ability,
                    rationale="Death-aversion test"
                )
```

### Template: Post-Primary Conditional Sweeps

After confirming primary driver `{PRIMARY}`, automatically suggest:

```json
// Batch 1: Death-mitigation (REQUIRED)
[
  {"type": "family_2d_heatmap", "variables": {"family_x": "{PRIMARY}", "family_y": "quick_respawn"}},
  {"type": "family_2d_heatmap", "variables": {"family_x": "{PRIMARY}", "family_y": "special_saver"}},
  {"type": "family_2d_heatmap", "variables": {"family_x": "{PRIMARY}", "family_y": "comeback"}}
]

// Batch 2: Top correlated from overview (if not already primary)
[
  {"type": "family_2d_heatmap", "variables": {"family_x": "{PRIMARY}", "family_y": "{SECONDARY_1}"}},
  {"type": "family_2d_heatmap", "variables": {"family_x": "{PRIMARY}", "family_y": "{SECONDARY_2}"}}
]

// Batch 3: Weapon interaction (optional)
[
  {"type": "weapon_sweep", "variables": {"condition_family": "{PRIMARY}", "condition_rung": 29}}
]
```

### Interpreting 2D Results

| 2D Result | Meaning | Label Update |
|-----------|---------|--------------|
| Y suppresses at high X | Anti-synergy | Add "{Y}-averse" |
| Y enhances at high X | Synergy | Add "{Y}-synergistic" |
| Y flat across X levels | Spurious correlation | Remove from label |
| No data at high X + high Y | Mutual exclusion | Note in label |

## Output Location

Specs are written to:
```
/mnt/e/mechinterp_runs/specs/{timestamp}__f{feature_id}__{type}.json
```

Example filenames:
- `20250607_142531__f18712__family-1d-sweep.json`
- `20250607_143022__f18712__frequent-itemsets.json`
- `20250607_143500__f18712__split-half.json`

## See Also

- **mechinterp-state**: Manage research state
- **mechinterp-runner**: Execute generated specs
- **mechinterp-glossary-and-constraints**: Domain rules
- **mechinterp-summarizer**: Process results
- **mechinterp-ability-semantics**: Ability semantic groupings for interpretation
- **mechinterp-investigator**: Full investigation workflow
