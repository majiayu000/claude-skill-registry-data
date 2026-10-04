---
name: run-rag-evaluation
description: Automatically run RAG evaluations using the local framework and output a benchmark report.
---

# Run RAG Evaluation

This skill allows the agent to execute evaluation pipelines in the Advance RAG Research framework.

## Instructions

1.  **Identify Configuration:** Check if the user has provided a path to an evaluation dataset (JSON) or a configuration file. If not, prompt the user or look for standard paths like `datasets/eval_data.json`.
2.  **Execute Command:** Run the evaluation CLI command from the root of the workspace:
    ```bash
    rag-framework evaluate --dataset <path-to-dataset>
    ```
3.  **Parse Results:** Extract the evaluation metrics (Context Precision, Recall, etc.) from the terminal output.
4.  **Report Generation:** If requested, format the output as a Markdown table or save it to a CSV file in the `results/` directory for historical tracking.

## References
- The CLI tool is built using Typer.
- Core logic is in `src/rag_framework/evaluators/basic_evaluator.py`.
