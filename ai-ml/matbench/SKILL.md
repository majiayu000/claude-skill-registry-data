---
name: matbench
description: Python benchmark suite for materials science property prediction. Use when evaluating ML model performance on materials datasets, comparing algorithms, or accessing curated materials ML datasets.
metadata:
    skill-author: MindSpore Science Team
---

# Overview

Matbench is an ImageNet for materials science - a curated set of 13 machine learning benchmark tasks for evaluating property prediction methods. It provides standardized datasets, predefined splits, and a leaderboard for comparing model performance.

# Installation

## Via PyPI

```bash
pip install matbench
```

## Via GitHub

```bash
git clone https://github.com/materialsproject/matbench
pip install --user ./matbench
```

For development:
```bash
cd matbench
pip install -e . -r requirements.txt
```

**Requirements**: Python 3.8+ (Unix systems officially supported; Windows may work)

# When to Use This Skill

Use Matbench when you need to:

- **Benchmark new ML models** against standardized datasets
- Compare model architectures on materials property prediction
- Access **curated, clean datasets** for materials ML research
- Establish reproducible baselines for publications
- Evaluate generalization across property types (regression/classification)
- Test model performance across **composition vs. structure** inputs

**Consider alternatives when:**
- Need custom datasets not in Matbench (use matminer directly)
- Require larger datasets (>1M samples)
- Need time-series or non-equilibrium data

# Benchmark Tasks (13 Datasets)

## Regression Tasks

### Structure-Based Regression

| Dataset | Samples | Target | Unit | Description |
|---------|---------|--------|------|-------------|
| `matbench_dielectric` | 4,764 | refractive index (n) | unitless | Dielectric constant predictions for insulating materials |
| `matbench_jdft2d` | 636 | exfoliation energy | meV/atom | Energy to exfoliate 2D materials from bulk |
| `matbench_log_gvrh` | 10,987 | log₁₀ shear modulus | log₁₀(GPa) | Voigt-Reuss-Hill averaged shear modulus |
| `matbench_log_kvrh` | 10,987 | log₁₀ bulk modulus | log₁₀(GPa) | Voigt-Reuss-Hill averaged bulk modulus |
| `matbench_mp_e_form` | 132,752 | formation energy | eV/atom | DFT formation energy from Materials Project |
| `matbench_mp_gap` | 106,113 | PBE band gap | eV | DFT band gap from Materials Project |
| `matbench_perovskites` | 18,928 | formation energy | eV/unit cell | Formation energy of perovskite structures |
| `matbench_phonons` | 1,265 | last phonon DOS peak | cm⁻�?| Highest frequency phonon mode |

### Composition-Based Regression

| Dataset | Samples | Target | Unit | Description |
|---------|---------|--------|------|-------------|
| `matbench_expt_gap` | 4,604 | experimental band gap | eV | Experimentally measured band gaps |
| `matbench_steels` | 312 | yield strength | MPa | Yield strength of steel compositions |

## Classification Tasks

| Dataset | Type | Samples | Target | Description |
|---------|------|---------|--------|-------------|
| `matbench_expt_is_metal` | composition | 4,921 | is metal | Metal vs. non-metal classification from experiment |
| `matbench_mp_is_metal` | structure | 106,113 | is metal | Metal vs. non-metal from DFT calculations |
| `matbench_glass` | composition | 5,680 | glass forming ability | Whether composition forms metallic glass |

# Data Loading

## Load Single Dataset

```python
from matbench.data_ops import load

df = load("matbench_jdft2d")
print(df.head())
# Columns: structure (pymatgen Structure), exfoliation_en (target)
```

## Load via MatbenchBenchmark

```python
from matbench.bench import MatbenchBenchmark

mb = MatbenchBenchmark(autoload=False)
mb.load()  # Load all datasets into memory
```

## Access Individual Task

```python
from matbench.bench import MatbenchBenchmark

mb = MatbenchBenchmark()
task = mb.matbench_dielectric  # Access specific task

print(task.info)  # Dataset info
print(task.metadata)  # Task metadata
```

## Preset Subsets

```python
from matbench.bench import MatbenchBenchmark

# Load only structure-based tasks
mb_struct = MatbenchBenchmark.from_preset("matbench_v0.1", "structure")

# Load only composition-based tasks
mb_comp = MatbenchBenchmark.from_preset("matbench_v0.1", "composition")

# Load only regression tasks
mb_reg = MatbenchBenchmark.from_preset("matbench_v0.1", "regression")

# Load only classification tasks
mb_clf = MatbenchBenchmark.from_preset("matbench_v0.1", "classification")
```

# Evaluation Metrics

## Regression Metrics

- **MAE**: Mean Absolute Error
- **RMSE**: Root Mean Squared Error
- **MAPE**: Mean Absolute Percentage Error (masked for values near zero)
- **max_error**: Maximum residual error

## Classification Metrics

- **accuracy**: Classification accuracy
- **balanced_accuracy**: Balanced accuracy for imbalanced datasets
- **f1**: F1 score
- **rocauc**: Area under ROC curve

## Scoring Function

```python
from matbench.data_ops import score_array

scores = score_array(y_true, y_pred, task_type="regression")
# Returns: {"mae": 0.123, "rmse": 0.456, "mape": 0.789, "max_error": 1.23}
```

# Benchmark Workflow

## Basic Benchmark Loop

```python
from matbench.bench import MatbenchBenchmark

mb = MatbenchBenchmark(autoload=False, subset=["matbench_dielectric"])

for task in mb.tasks:
    task.load()
    for fold in task.folds:
        train_inputs, train_outputs = task.get_train_and_val_data(fold)
        test_inputs = task.get_test_data(fold, include_target=False)

        # Your model training here
        predictions = your_model(train_inputs, train_outputs, test_inputs)

        # Record predictions
        task.record(fold, predictions)

# Validate and get scores
mb.validate()
print(mb.scores)
```

## Complete Example with Dummy Model

```python
import numpy as np
from matbench.bench import MatbenchBenchmark

mb = MatbenchBenchmark(autoload=False)

for task in mb.tasks:
    task.load()
    for fold in task.folds:
        train_X, train_y = task.get_train_and_val_data(fold)
        test_X = task.get_test_data(fold, include_target=False)

        # Dummy model: predict mean of training targets
        mean_pred = np.mean(train_y)
        predictions = [mean_pred] * len(test_X)

        task.record(fold, predictions)

# Check validity
if mb.is_valid:
    print("Benchmark complete and valid!")
    for task in mb.tasks:
        print(f"{task.dataset_name}: MAE = {task.scores.mae.mean:.4f}")
```

## Record with Uncertainty (Regression Only)

```python
# Using standard deviation
task.record(fold, predictions, std=std_devs)

# Using confidence intervals
task.record(fold, predictions, ci=[(lower, upper) for ...])
```

## Save and Load Results

```python
# Save benchmark results
mb.to_file("my_benchmark_results.json")

# Load previous results
from matbench.bench import MatbenchBenchmark
mb = MatbenchBenchmark.from_file("my_benchmark_results.json")
```

# Best Practices

## Benchmark Protocol
- Always use predefined splits (5-fold cross-validation)
- Never tune hyperparameters on test data
- Record all 5 folds for each task
- Report mean and std of metrics across folds

## Model Development
- Start with simple baselines (dummy regressor/classifier)
- Compare against AutoMatminer reference
- Test on multiple tasks, not just one
- Consider computational cost for large datasets

## Data Handling
- Use `task.get_train_and_val_data(fold)` for training data
- Use `task.get_test_data(fold, include_target=False)` for test inputs
- Never access test targets directly

## Reporting Results
- Include model metadata with submissions
- Provide code for reproducibility
- Compare against leaderboard entries

# Troubleshooting

## Common Issues

### Memory issues with large datasets
- Load one task at a time: `MatbenchBenchmark(autoload=False)`
- Use generators instead of loading all data
- Process folds sequentially

### Invalid benchmark results
- Ensure all 5 folds are recorded
- Check predictions match test set size
- Verify no data leakage between folds

### Slow loading
- Cache downloaded datasets locally
- Use `autoload=False` and load selectively

### Structure parsing errors
- Update pymatgen version
- Check structure validity before processing

# Contributing New Models

1. Run benchmark on all 13 datasets using 5-fold cross-validation
2. Record all predictions using `task.record(fold, predictions)`
3. Validate benchmark with `mb.validate()`
4. Save results: `mb.to_file("results.json")`
5. Submit to leaderboard at https://matbench.materialsproject.org

## Requirements for Submission

- Use predefined train/test splits (no data leakage)
- No hyperparameter tuning on test data
- Include model metadata via `mb.add_metadata({...})`
- All 5 folds recorded for each task

```python
mb.add_metadata({
    "model_name": "MyModel",
    "model_version": "1.0",
    "authors": ["Your Name"],
    "paper": "https://arxiv.org/...",
    "github": "https://github.com/...",
})
```

# Leaderboard

- Main leaderboard: https://matbench.materialsproject.org
- Per-task leaderboards: https://matbench.materialsproject.org/Leaderboards%20Per-Task/matbench_v0.1_matbench_dielectric/
- Full benchmark data: https://matbench.materialsproject.org/Full%20Benchmark%20Data/matbench_v0.1_automatminer_expressv2020/

# Reference Algorithm

AutoMatminer is the baseline reference algorithm. Results available at the leaderboard link above.

# Citation

```bibtex
@article{dunn2020benchmarking,
  title={Benchmarking materials property prediction methods: The Matbench test set and Automatminer reference algorithm},
  author={Dunn, Andrew and Wang, Qi and Ganose, Alex and Dopp, Daniel and Jain, Anubhav},
  journal={npj Computational Materials},
  volume={6},
  number={1},
  pages={138},
  year={2020},
  publisher={Nature Publishing Group},
  doi={10.1038/s41524-020-00406-3}
}
```

# Resources

- GitHub: https://github.com/materialsproject/matbench
- Leaderboard: https://matbench.materialsproject.org
- Documentation: https://matbench.readthedocs.io
- Paper: Dunn et al., npj Comput. Mater. 6, 138 (2020)
