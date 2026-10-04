---
name: paper-repro-claim-map
description: Map an AI/ML paper into a reproducible claim-to-experiment ledger. Use when Codex needs to turn a paper PDF, HTML digest, arXiv/OpenReview page, appendix, or reproduction request into concrete claims, tables/figures, datasets, metrics, baselines, hyperparameters, seeds, compute needs, and minimal reproduction targets before sourcing code or running experiments.
---

# Paper Repro Claim Map

## Overview

Use this skill as the first execution step in a paper reproduction. It does not search for code, install dependencies, or run experiments. It creates the reproduction scope that downstream skills can lock, smoke test, and audit.

Read `references/patterns.md` when the paper is complex, missing details, or the user wants a rigorous reproduction checklist.

## Inputs

Accept any of:

- Paper PDF, structured HTML digest, Markdown notes, arXiv/OpenReview/proceedings URL, appendix, supplemental material, README, or user-selected tables/figures.
- Optional target scope such as "main result only", "Table 2 and Figure 4", "minimal smoke reproduction", "full benchmark", or "ablation only".

If the source is a raw PDF and no readable text is available, use `$paper-pdf-to-structured-html` or another PDF reader first.

## Workflow

1. Identify the paper version, title, venue, date, and artifact inputs used for mapping.
2. Extract claims from the abstract, introduction, contribution list, conclusion, and result sections.
3. Classify each claim:
   - `empirical_main`: primary result, SOTA claim, benchmark win, efficiency claim.
   - `empirical_support`: ablation, sensitivity, robustness, transfer, scaling, qualitative result.
   - `method_or_theory`: algorithmic, architectural, proof, complexity, or assumption claim.
   - `artifact`: dataset, model, code, benchmark, or tool release claim.
4. Link every reproducible claim to exact evidence:
   - paper section;
   - table, figure, equation, appendix, or supplementary file;
   - dataset and split;
   - metric direction and reported value;
   - baseline/comparator;
   - hyperparameters, seeds, statistical treatment, and compute if reported.
5. Select a minimal reproduction target before full reproduction:
   - Prefer the main experiment supporting the headline claim.
   - Prefer a cheap subset, pretrained checkpoint evaluation, or one small dataset when full training is expensive.
   - Preserve explicit exclusions and unresolved details.
6. Write a claim map artifact before moving to source locking.

## Output Contract

Create `claim_map.md` and, for structured runs, `claim_map.json`.

Required Markdown sections:

- `Paper Identity`
- `Reproduction Scope`
- `Claim Ledger`
- `Experiment Targets`
- `Missing or Ambiguous Details`
- `Recommended Minimal Reproduction`
- `Downstream Inputs`

Use this JSON shape when machine-readable output is useful:

```json
{
  "paper": {
    "title": "",
    "version": "",
    "source_url": "",
    "mapped_from": []
  },
  "scope": {
    "requested": "",
    "selected_minimal_target": "",
    "excluded_targets": []
  },
  "claims": [
    {
      "id": "C1",
      "type": "empirical_main",
      "claim": "",
      "paper_location": "",
      "evidence_artifacts": ["Table 1"],
      "experiment_ids": ["E1"],
      "status": "mapped"
    }
  ],
  "experiments": [
    {
      "id": "E1",
      "purpose": "",
      "dataset": "",
      "split": "",
      "metric": "",
      "reported_value": "",
      "baseline": "",
      "expected_command_or_entrypoint": "",
      "hyperparameters": {},
      "seeds_or_repeats": "",
      "compute": "",
      "reproduction_priority": "minimal"
    }
  ],
  "blockers": []
}
```

## Guardrails

- Do not infer an exact command, dataset version, or hyperparameter value unless the paper or accompanying artifact states it.
- Separate "paper reported" from "Codex inferred" fields.
- Do not mark a claim reproducible only because a table exists. It also needs a runnable target or a documented blocker.
- Keep the first target small enough for a smoke path unless the user explicitly asks for full-scale reproduction.

## Resources

- `references/patterns.md`: distilled practices from NeurIPS checklist guidance, ML reproducibility checklists, Papers with Code code completeness, and reproduction-agent patterns.
