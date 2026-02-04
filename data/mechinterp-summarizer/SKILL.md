---
name: mechinterp-summarizer
description: Convert experiment results to Markdown research notes and optionally update research state with evidence
---

# MechInterp Summarizer

Convert experiment results into human-readable research notes and optionally link them as evidence to hypotheses in the research state.

## Purpose

The summarizer skill:
- Converts ExperimentResult JSON to Markdown notes
- Extracts key findings, tables, and diagnostics
- Appends notes to feature-specific research files
- Optionally updates research state with new evidence
- Synthesizes both enhancer and suppressor patterns for complete interpretation

## When to Use

Use this skill after:
1. The runner has completed an experiment
2. You want to document findings
3. You need to link evidence to hypotheses

## Usage

### Command Line

```bash
cd /root/dev/SplatNLP

# Basic: Generate note from result
poetry run python -m splatnlp.mechinterp.cli.summarizer_cli \
    --result-path /mnt/e/mechinterp_runs/results/20250607_142531__result.json

# With state update and evidence linking
poetry run python -m splatnlp.mechinterp.cli.summarizer_cli \
    --result-path /mnt/e/mechinterp_runs/results/20250607_142531__result.json \
    --update-state \
    --supports h001 h002 \
    --strength strong

# Print only (no file writes)
poetry run python -m splatnlp.mechinterp.cli.summarizer_cli \
    --result-path result.json \
    --output-only
```

### Programmatic

```python
from splatnlp.mechinterp.schemas import ExperimentResult
from splatnlp.mechinterp.cli.summarizer_cli import generate_note_from_result
from splatnlp.mechinterp.state import ResearchStateManager
from splatnlp.mechinterp.schemas.research_state import EvidenceStrength
from pathlib import Path

# Load result
result = ExperimentResult.model_validate_json(
    Path("/mnt/e/mechinterp_runs/results/20250607__result.json").read_text()
)

# Generate note
note = generate_note_from_result(result)
print(note)

# Update state with evidence
manager = ResearchStateManager(feature_id=18712, model_type="ultra")
evidence = manager.add_evidence_from_result(
    result=result,
    summary="SCU sweep shows threshold behavior at 41 AP",
    strength=EvidenceStrength.STRONG,
    supports=["h001"],
)
print(f"Added evidence: {evidence.id}")
```

## Output Format

### Research Notes

Notes are written to:
```
/mnt/e/mechinterp_runs/notes/feature_{id}_{model}.md
```

Example note content:

```markdown
## Family 1D Sweep
*Experiment: 20250607_142531*
*Duration: 45.3s*

### Key Findings
- Mean activation delta: **0.3500**
- Max delta: 0.5200
- Samples analyzed: 500
- Threshold Rung: 41

### rung_stats
*Activation statistics by special_charge_up AP rung*

| rung | label | mean_activation | std | n | delta_from_baseline |
|------|-------|-----------------|-----|---|---------------------|
| 0 | absent | 0.1234 | 0.05 | 200 | 0.0 |
| 3 | SCU_3 | 0.1500 | 0.06 | 50 | 0.0266 |
| 41 | SCU_41 | 0.4800 | 0.08 | 30 | 0.3566 |
| 57 | SCU_57 | 0.6400 | 0.10 | 20 | 0.5166 |

### Warnings
- ReLU floor detected in 5% of examples
```

### Evidence Linking

When using `--update-state`, creates an EvidenceItem:

```json
{
  "id": "e003",
  "experiment_id": "20250607_142531",
  "result_path": "/mnt/e/.../20250607_142531__result.json",
  "summary": "SCU sweep shows threshold behavior at 41 AP",
  "strength": "strong",
  "supports_hypotheses": ["h001"],
  "refutes_hypotheses": [],
  "key_metrics": {
    "threshold_rung": 41,
    "max_delta": 0.52
  }
}
```

## CLI Options

| Option | Description |
|--------|-------------|
| `--result-path` | Path to experiment result JSON (required) |
| `--feature-id` | Feature ID (auto-detected from result) |
| `--model-type` | Model type: full or ultra (default: ultra) |
| `--update-state` | Also update research state with evidence |
| `--supports` | Hypothesis IDs this evidence supports |
| `--refutes` | Hypothesis IDs this evidence refutes |
| `--strength` | Evidence strength: strong/moderate/weak |
| `--output-only` | Only print note, don't write files |

## Workflow Integration

Typical workflow:

1. **Run experiment**: Use mechinterp-runner to execute a spec
2. **Summarize**: Use this skill to generate notes
3. **Link evidence**: Use `--update-state` to connect to hypotheses
4. **Review**: Check updated state and notes
5. **Plan next**: Use mechinterp-next-step-planner for next experiment

```bash
# Full workflow example
poetry run python -m splatnlp.mechinterp.cli.runner_cli \
    --spec-path /mnt/e/mechinterp_runs/specs/scu_sweep.json

poetry run python -m splatnlp.mechinterp.cli.summarizer_cli \
    --result-path /mnt/e/mechinterp_runs/results/scu_sweep__result.json \
    --update-state \
    --supports h001 \
    --strength strong
```

## Evidence Synthesis Tips

When summarizing results, always consider:

1. **Enhancers + Suppressors**: A complete interpretation requires BOTH. If SCU is enhanced but death-perks (QR, SS, CB) are suppressed, the feature encodes "death-averse special builds", not just "SCU detector".

2. **Check ability semantics**: After identifying enhancers/suppressors, consult **mechinterp-ability-semantics** to validate interpretations against known semantic groupings.

3. **Token influence sweeps**: These provide the most complete picture of what a feature responds to and avoids. Prioritize summarizing both enhancers and suppressors tables.

## See Also

- **mechinterp-runner**: Execute experiments
- **mechinterp-state**: Manage research state
- **mechinterp-next-step-planner**: Plan next experiments
- **mechinterp-ability-semantics**: Ability semantic groupings for interpretation
- **mechinterp-investigator**: Full investigation workflow
