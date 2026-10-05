---
name: jupyter-python
description: >-
  Use for creating, reviewing, debugging, testing, or reproducing Python
  Jupyter notebooks and .ipynb artifacts, including kernel identity, execution
  order, hidden state, nbformat, nbclient execution, outputs, parameters,
  notebook-to-script boundaries, and privacy. Do not use for ordinary Python
  modules, Jupyter server administration, or data analysis with no notebook
  artifact.
argument-hint: "[notebook task, kernel/environment, inputs, outputs, and reproducibility]"
---

# Notebooks as executable documents

A notebook file stores cells, metadata, and possibly outputs. A kernel owns the
live Python process and mutable state. Saved output is evidence from a prior
execution, not proof that the current source runs in order.

## Workflow

1. Inspect notebook format version, kernelspec, language metadata, cell order,
   execution counts, imports, file paths, parameters, secrets, widgets, large
   outputs, and repository environment.
2. Choose the correct kernel from the project environment. Record interpreter
   and dependency versions; do not trust a familiar kernel display name.
3. Make dependencies and input paths explicit. Put reusable logic in imported
   modules with tests; keep the notebook for orchestration, explanation, and
   display.
4. Restart and execute all cells top-to-bottom in a clean process. Stop on the
   first unexpected error; do not use `allow_errors` to make a failing notebook
   appear successful.
5. Write the executed notebook to a separate artifact unless in-place mutation
   was explicitly requested. Inspect error outputs, execution counts, output
   size, and sensitive content.
6. Re-run from the same clean inputs and compare material artifacts. Persist
   scripts, data products, or reports separately when they are the canonical
   result.

## Invariants

- Out-of-order success is hidden-state failure. A clean top-to-bottom run is
  the minimum reproducibility test.
- A notebook kernel can outlive cell edits and deletions; restart before proof.
- Do not embed credentials, personal row data, or huge binary/base64 output.
- Set random seeds and control clocks/network inputs when reproducibility
  requires them, while documenting unavoidable nondeterminism.
- Parameter cells or a small configuration object are preferable to manual
  edits scattered through cells.

```python
import nbformat
from nbclient import NotebookClient

notebook = nbformat.read("analysis.ipynb", as_version=4)
client = NotebookClient(
    notebook,
    timeout=600,
    kernel_name="python3",
    resources={"metadata": {"path": "notebooks"}},
)
client.execute()
nbformat.write(notebook, "artifacts/analysis.executed.ipynb")
```

Read [state and structure](references/state.md), [execution and verification](references/execution.md),
and [module/report boundaries](references/boundaries.md).
