---
name: dark-factory-commands
description: "Common commands and CLI invocation reference for the Dark Factory DOT pipeline runner — running smoke and full gated pipelines, CXDB failure diagnosis with df-healer, pipeline graph visualization, and test suite execution."
---

# Dark Factory Common Commands

Use this skill when you need the standard command syntax for running Dark Factory pipelines, diagnosing CXDB execution logs with the Healer, rendering DOT pipeline graphs, or executing the test suite.

## When to use

- Running a smoke or sanity pipeline without LLM calls.
- Running a full gated pipeline with CXDB recording and Agent Orchestrator (AO).
- Clustering CXDB execution failures into a Healer diagnosis.
- Rendering `.dot` pipeline graphs to PNG for visual inspection.
- Running pytest against the test suite, specific test files, or individual test cases.

## Pipeline execution

### Smoke pipeline
Echo backend, no LLM calls:
```bash
dark-factory --pipeline pipelines/factory/hello.dot --goal "smoke test" --backend echo
```

### Full gated pipeline
Run the full gated pipeline with CXDB recording from the target repo cwd:
```bash
dark-factory \
  --pipeline pipelines/factory/gates.dot \
  --goal "<feature description>" \
  --backend ao \
  --ao-agent antigravity \
  --feature <feature_name> \
  --cxdb ~/.dark-factory/cxdb.sqlite
```

`gates.dot` declares `hello` as its default holdout feature; an explicit `--feature` value overrides that DOT default at runtime.

## Diagnosis and visualization

### Cluster CXDB failures into a Healer diagnosis
```bash
df-healer --cxdb ~/.dark-factory/cxdb.sqlite
```

### Visualize a pipeline graph
```bash
dot -Tpng pipelines/factory/gates.dot -o gates.png
```

## Testing

Run the full suite, a single file, or an individual test:
```bash
.venv/bin/python -m pytest tests/
.venv/bin/python -m pytest tests/test_engine.py -k green
.venv/bin/python -m pytest tests/test_gates.py::test_parse_verdict_pass_warn_fail
```

> **Legacy dev-only:** `.venv/bin/python -m runner ...` from `$DARK_FACTORY_HOME`.
