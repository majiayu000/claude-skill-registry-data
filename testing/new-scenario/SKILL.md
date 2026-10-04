---
name: new-scenario
description: Scaffold a new Nursery-lite qualification scenario (YAML) with the right test family, mock script, and graders. Use when the user wants to add an eval/scenario or says /new-scenario.
---

# /new-scenario — scaffold a qualification scenario

Create `evals/scenarios/<name>.yaml`. Template:

```yaml
name: <snake_case_name>
family: positive        # positive | negative | ablation | poisoning | regression
                        # (conflict/staleness/isolation/authority are registered but
                        #  have no runner semantics yet — using them is an error)
description: One sentence on what this scenario qualifies.
workflow: doc_check
document: evals/fixtures/<fixture>.md      # or documents_glob: "architecture/governance/*.md"
model_assist: false     # true only if the scenario exercises the model step
max_model_tokens: 1024
mock_script:            # REQUIRED whenever model_assist is true — CI is key-free
  summarize_findings:   # keyed by ModelRequest.step_name
    - text: "scripted reply"
      usage: { input_tokens: 100, output_tokens: 20 }
graders:                # registry: src/koa/nursery/graders.py
  - type: all_checks_pass
  # finding_present/finding_absent (param: check), output_contains/output_not_contains
  # (param: value), output_regex (param: pattern), evidence_recorded (param: model_calls),
  # budget_respected, no_model_calls
ablation_graders: []    # ablation family only: graders for the model-assist-OFF rerun
```

Rules:
- Every model turn the workflow will request must have a scripted mock turn, or the
  run fails with `MockScriptExhausted`. That's intentional.
- Fixtures live in `evals/fixtures/`; keep them minimal and self-describing.
- Prefer structural graders (`finding_*`, `evidence_recorded`) over exact-text ones so
  the scenario stays meaningful under `--live`.

Then verify:
1. `uv run koa-nursery --only <name> -v`
2. `uv run pytest tests/test_scenario_loading.py` — and update the expected-names set
   in that test to include the new scenario.
