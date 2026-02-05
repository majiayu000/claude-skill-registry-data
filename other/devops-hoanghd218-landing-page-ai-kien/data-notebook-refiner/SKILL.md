---
name: data-notebook-refiner
description: Standards for high-quality Jupyter Notebooks. Focuses on readability, reproducibility, and educational value.
---

# Notebook Refiner Standards

## Purpose
To ensure Jupyter Notebooks are not just "functioning code dumps" but **educational learning materials** and **reproducible assets**.

## Core Philosophy: "Readability & Reproducibility"
A notebook is a document meant to be read by humans, not just a script for machines.

## Refactoring Standards

### 1. Structure (Flow)
- **Imports**: All imports must be in the first cell.
- **Logical Flow**: Data Load → EDA → Preprocessing → Modeling → Evaluation.
- **Kernel Check**: Must specify required environment (e.g., `venv`, python version).

### 2. Code Quality (Refactor)
- **Naming**: Use descriptive names (`titanic_df`) over generic ones (`df`). Follow conventions (`X`, `y`, `model`).
- **Granularity**: One logical step per cell. Don't mix loading and training in one massive cell.
- **Output**: Suppress verbose logs (e.g., strict `fit()` output).

### 3. Documentation (Context)
**"Explain Why, Not What"**
- **Bad**: "This code splits the data." (Redundant)
- **Good**: "We use `stratify=y` to maintain class balance in the test set." (Insightful)
- **Headers**: Use clear Markdown headers (`#`, `##`) to navigate structure.

### 4. Verification (Reproducibility)
- **Restart & Run All**: The notebook must run from top to bottom without error after a kernel restart.
- **Visuals**: All plots must have Titles, Axis Labels, and Legends.
