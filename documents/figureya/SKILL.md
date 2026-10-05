---
name: figureya
description: "Use when the user asks for FigureYa templates, biomedical visualization templates, Rmd figure recipes, reusable omics or clinical plot workflows, PCA/ROC/GSEA/WGCNA/survival/CNV/ATAC/single-cell/mutation heatmap examples, or adapting local compressed FigureYa templates."
---

# FigureYa Content-Aware Template Skill

## Overview

FigureYa is a local atlas of biomedical visualization and analysis templates. This skill indexes the actual files inside fully extracted `FigureYa###*` template folders, not the nested ZIP files. Each record points directly to a real `Rmd`, `R`, `py`, `ipynb`, `sh`, `java`, or `md` file and includes content-derived purpose, method summary, packages, functions, input/output references, related docs, and inferred upstream/downstream workflow links when available.

Local source paths:

- Outer archive: `/home/h2048/temp/FigureYa-compressed-main.zip`
- Unpacked template ZIP directory: `/home/h2048/temp/FigureYa_unpacked_20260508/FigureYa-compressed-main`
- Extracted script directory: `/home/h2048/temp/FigureYa_templates_extracted_20260509`
- Script manifest: `figureya_manifest.csv`

## When to Use

Use this skill when the user needs a practical script for biomedical figures or analysis workflows, especially R Markdown workflows. Common triggers include PCA, ROC, GSEA, WGCNA, survival risk plots, Cox models, CNV, ATAC, ChIP-seq, methylation, immunotherapy, mutation signatures, heatmaps, Venn diagrams, Circos, lollipop plots, forest plots, and single-cell visualization templates.

For broad visualization advice, use this together with the Bizard skill. Use FigureYa when the user wants a concrete local template or reproducible Rmd-style recipe.

## Core Workflow

1. Search the script manifest first.
2. Pick 1-3 candidate records by matching the user's data type, analysis goal, expected figure style, `script_role`, `purpose`, and `method_summary`.
3. Prefer `script_role=tutorial` for runnable workflows, then inspect linked helpers, dependency scripts, and documentation via `upstream_scripts`, `downstream_scripts`, `related_docs`, and `install_dependencies_file`.
4. Inspect the selected `script_path` directly, plus companion `example_png`, `companion_html`, `input_references`, `output_references`, and `input_files_preview` paths.
5. Adapt the template to the user's actual data columns and environment.
6. Cite FigureYa if reusing its code or structure.

## Search Commands

From this skill directory:

```bash
python3 tools/search_figureya_templates.py figureya_manifest.csv "PCA dimension reduction" --limit 5
python3 tools/search_figureya_templates.py figureya_manifest.csv "survival risk cox" --limit 5
python3 tools/search_figureya_templates.py figureya_manifest.csv "single cell CNV" --limit 5
```

To rebuild the extracted template directory from the nested ZIP files:

```bash
python3 tools/extract_all_templates.py /home/h2048/temp/FigureYa_unpacked_20260508/FigureYa-compressed-main /home/h2048/temp/FigureYa_templates_extracted_20260509
```

To rebuild the content-aware manifest:

```bash
python3 tools/build_manifest.py /home/h2048/temp/FigureYa_templates_extracted_20260509 figureya_manifest.csv
```

## Manifest Columns

`figureya_manifest.csv` is content-level and includes:

- `template_id`, `template_name`, `template_dir`
- `script_role`, `script_kind`, `script_name`, `script_relpath`, `script_path`
- `title`, `requirement`, `purpose`, `method_summary`
- `packages`, `functions_defined`, `input_references`, `output_references`
- `chain_position`, `upstream_scripts`, `downstream_scripts`, `related_docs`
- `companion_html`, `example_png`
- `install_dependencies_file`
- `input_file_count`, `input_files_preview`
- `tags`

Use `tags` for rough filtering, but rely on `purpose`, `method_summary`, and the actual file contents before recommending or adapting code. Check `upstream_scripts` and `downstream_scripts` before reusing a step so hidden preprocessing or rendering stages are not missed.

## Safety and Quality Notes

- Do not install dependencies automatically. Read `install_dependencies.R` first and prefer the user's active R environment conventions.
- Do not copy large sample datasets into a project unless the user asks; prefer reading the selected script and adapting it to the user's data.
- Some templates are analysis workflows rather than pure plotting templates, so check whether they require external databases, Java tools, web services, or large reference data.
- Some automatically assigned tags are heuristic. Treat search results as candidates, not ground truth.
- Keep adaptations focused on the user's real input files and columns.

## Citation

Several templates include this citation request:

Xiaofan Lu, et al. (2025). FigureYa: A Standardized Visualization Framework for Enhancing Biomedical Data Interpretation and Research Efficiency. iMetaMed. https://doi.org/10.1002/imm3.70005
