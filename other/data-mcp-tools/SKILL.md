---
name: data-mcp-tools
category: tools
description: Use when tools from the jupyter, duckdb, dbt, mlflow, huggingface or postgres MCP servers appear in your tool list, or before reaching for one — what each is good for, what it can damage, and the CLI fallback when it is not connected
tech_stack: MLOps
source: original; informed by the datalayer jupyter-mcp-server, motherduckdb mcp-server-motherduck, dbt-labs dbt-mcp, MLflow MCP server, Hugging Face MCP and modelcontextprotocol server-postgres documentation (cited, not reproduced)
---
# Data MCP Tools

## Overview

TaskTrooper can connect optional MCP servers that make data work faster: a live Jupyter kernel, DuckDB, dbt, MLflow, Hugging Face search and Postgres. They are disabled by default; a person enables them in Settings → MCP servers. They are conveniences on top of the workspace, never a replacement for it: the repository's code and its test suite remain the deliverable and the evidence.

**Core principle:** a server is available only if its tools are in your tool list right now. If they are not, use the CLI equivalent and carry on — never stop a task, and never ask a person to install or enable a server mid-task.

## 1. Detecting availability

Look at your tool list. Tools from a server carry its id in the name — `mcp_duckdb_…` in TaskTrooper's own runtime, `mcp__duckdb__…` in a CLI runtime. Tool names differ between server versions; read the descriptions in your tool list rather than assuming a name from this skill. A server whose tools are absent is not connected for this run, whatever the repository's docs say.

## 2. The servers

| Server id | What it gives you | Use it for | Fallback without it |
|---|---|---|---|
| `jupyter` | read, insert, edit and execute cells in a running local JupyterLab | looking at data interactively, checking a notebook runs cell by cell | `uv run jupyter nbconvert --execute`, papermill, or a script |
| `duckdb` | SQL over Parquet/CSV/DuckDB files, in-memory by default | EDA, profiling (`SUMMARIZE`), reconciling a result two ways | `duckdb` CLI or `uv run python -c "import duckdb; ..."` |
| `dbt` | lineage, compile, list, show, test, run, build for the project | finding a model's parents and children, compiling SQL, running tests on the dev target | the `dbt` CLI with the same commands |
| `mlflow` | experiments, runs and registered models from the tracking server (ML tool set) | finding the current champion and its metrics to compare your candidate against | a short script with `mlflow.MlflowClient` |
| `huggingface` | model search on the Hub | finding a pretrained model and its exact revision | the Hub website docs or `huggingface_hub` in a script |
| `postgres` | read-only SQL against a configured Postgres | inspecting a source table's shape and row counts | `psql` with the repository's dev connection |

## 3. jupyter — the kernel runs whatever you send

- Executing a cell is exactly as powerful as run_terminal: it can delete files, call the network and write to databases. Apply the same care, and never send credentials into a cell.
- The kernel keeps state between calls. A result that depends on cells you ran earlier, out of order, is not reproducible — re-run from a fresh kernel before trusting it.
- Exploration in the kernel is fine; anything the deliverable needs moves into the package with tests (rule no-notebook-only-logic, notebook-to-module). A notebook edited through the server is still committed the repository's way (stripped outputs, jupytext pair or marimo file).
- The server talks to a JupyterLab a person started on this machine; it may have nothing to do with your task workspace. Check the notebook path and the kernel's working directory before reading results as evidence about your branch.

## 4. duckdb — fast SQL for EDA and result QA

- Point it at files in your workspace or `/tmp/tt-<task key>/`: `SELECT * FROM read_parquet('data/sample/*.parquet')`, `SUMMARIZE ...`, join-count checks (analytics-result-qa).
- Results come back capped (about 1,024 rows by default): aggregate and profile in SQL instead of pulling raw rows to read by eye.
- The default database is in-memory — tables you create disappear with the session. Anything a pipeline needs is written by code in the diff, not by a tool call.
- A DuckDB file or a MotherDuck (`md:`) connection may be configured instead: treat writes there like writes to a shared database — do not.

## 5. dbt — prefer read-only and dev-target commands

- Lineage, `list`, `compile`, `parse` and `show` read the project and are safe; use them to find what a change affects before editing (sql-analytics-and-dbt).
- `run` and `build` (and `test`, which queries the warehouse) execute against the warehouse with the credentials in `profiles.yml`. Use them only against a development target, never production, and only for the models your task touches (`--select fct_orders+`). A person may have disabled them for the server — then use the CLI on the dev target, or say they could not run.
- The tool result is evidence only for the target it ran on; name the target in your closing message.

## 6. mlflow — read to compare, never delete

- Use it to read experiments, runs and registered models: the champion's version and alias, its logged metrics, the data fingerprint and git SHA it was trained on. Compare your candidate against those numbers on the same data (model-training-and-evaluation).
- Never delete or rename runs, experiments, models or traces, and never move a registry alias: promotion is deploy-time work for a person (rule deploy-runbook-fields).
- Your own test and exercise runs log to a local store in `/tmp/tt-<task key>/`, not to the server behind this tool (experiment-tracking-and-reproducibility).

## 7. huggingface and postgres

- Hugging Face: search, then pin what you choose by commit revision in code (deep-learning-pytorch); check the model's license and whether it needs `trust_remote_code` before proposing it.
- Postgres: queries run read-only. Use them to learn a source's columns, types and row counts; never paste production rows into fixtures, commits or comments.

## 8. Evidence

A tool call is not a test. Whatever you learned through a server is either encoded in code with tests in the diff, or reported in your closing message as what you looked at (server, target, query). The hand-off gate runs the repository's checks (data-build-check); MCP results never replace them.

## Common Mistakes

- Waiting for, or asking for, a server that is not connected instead of using the CLI.
- Building the deliverable in the Jupyter kernel and never moving it into the package.
- Running `dbt build` through the server against the production target.
- Pulling thousands of rows through DuckDB to inspect by eye.
- Treating the shared MLflow server as a scratchpad for test runs.

## Red Flags

- A conclusion in your closing message that only exists in kernel state.
- A dbt or SQL tool call whose target you do not know.
- A delete, rename or alias change on a shared MLflow server.
- Production data copied from a tool result into a fixture.
