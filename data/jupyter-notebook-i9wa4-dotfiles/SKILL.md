---
name: jupyter-notebook
description: Jupyter Notebook Expert Skill - Guide for notebook execution and Databricks kernel integration
---

# Jupyter Notebook Expert Skill

This skill provides a guide for Jupyter Notebook execution.

## 1. Databricks Jupyter Kernel

<https://github.com/i9wa4/jupyter-databricks-kernel>

```bash
# With uv
uv pip install jupyter-databricks-kernel
uv run python -m jupyter_databricks_kernel.install

# With pip
pip install jupyter-databricks-kernel
python -m jupyter_databricks_kernel.install
```

## 2. Default Execution Method

When instructed to execute an entire notebook, use this command:

```sh
uv run jupyter execute <notebook_path> --inplace --timeout=300
```

## 3. Execute with Databricks Kernel

When running notebook on Databricks cluster:

```sh
uv run jupyter execute <notebook_path> --inplace --kernel_name=databricks --timeout=300
```

Required environment variables:

- `DATABRICKS_HOST`: Databricks workspace URL
- `DATABRICKS_TOKEN`: Personal Access Token
- `DATABRICKS_CLUSTER_ID`: Cluster ID

## 4. Usage Examples

```bash
# Execute with local Python kernel
uv run jupyter execute /workspace/notebooks/sample.ipynb --inplace --timeout=300

# Execute with Databricks kernel
uv run jupyter execute /workspace/notebooks/databricks-sample.ipynb --inplace --kernel_name=databricks --timeout=300
```

## 5. Option Descriptions

- `--inplace`: Overwrite original file with execution results
- `--kernel_name=<name>`: Specify kernel to use (databricks, python3, etc.)
- `--timeout=<seconds>`: Set timeout in seconds (-1 for unlimited)
- `--startup_timeout=<seconds>`: Kernel startup timeout (default 60 seconds)
- `--allow-errors`: Continue execution to end even with errors

## 6. Notes

- Verify required environment variables are properly set before execution
- Adjust `--timeout` value for long-running cells
- If open in VS Code, verify file updates after execution
- For Databricks kernel, cluster startup takes 5-6 minutes if stopped

## 7. Reference Links

- jupyter-databricks-kernel: <https://github.com/i9wa4/jupyter-databricks-kernel>
- Jupyter nbclient: <https://nbclient.readthedocs.io/>
