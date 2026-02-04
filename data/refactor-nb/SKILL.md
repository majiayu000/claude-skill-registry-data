---
name: refactor_nb
description: Jupyter Notebook (.ipynb) 内のコード要素を一括置換・リファクタリングする
---

# `refactor_notebooks` Skill

This skill is for programmatically analyzing Jupyter Notebook (.ipynb) files and performing batch replacement or modification of specific import patterns or code blocks.

## Instructions

1.  **Analyze Notebook Structure**:
    *   Load `.ipynb` files as JSON using Python and iterate through the `cells` list.
    *   Verify if the `cell_type` of each cell is `code`.

2.  **Filter and Match**:
    *   Join the `source` field (list format) into a string and use regular expressions or keyword matching to identify target cells.
    *   Target specific import statements (e.g., `from gwexpy.noise import asd`), function calls, or targeted comments.

3.  **Implement Transformation**:
    *   Create a transformation script to rewrite the `source` list of the cells in memory.
    *   The updated source must be in list format (each element as a string ending with a newline).

4.  **Write and Verify**:
    *   Save the file using `json.dump`, maintaining an indent of 1 (a `gwexpy` convention) and specifying `ensure_ascii=False`.
    *   Verify that the resulting notebook is valid JSON and that the intended changes have been applied using `view_file` or similar.

## Usage Guidelines

*   When modifying multiple notebooks across a directory, create a loop script that collects `.ipynb` files using `glob` or similar.
*   For complex refactoring, adopt a workflow of saving the logic as a temporary `.py` script, executing it via `run_command`, and then deleting the script.
