---
name: bioresearcher-plot-making
description: "Biomedical visualization router and plotting engine: classifies research data and produces publication-ready scientific figures (structural protein-binder complexes, conformational dynamics, literature method summaries, developmental case registers, and evidence tables). Use when asked to plot, visualize, graph, or chart biomedical data, PDB complexes, binding modes, literature searches, or translational safety cases."
license: Apache-2.0
compatibility: "Any Agent Skills harness with Python 3.10+ and uv; matplotlib, pymupdf, numpy, pillow, pymol (optional for 3D)"
metadata:
  version: "1.0.0"
  source: "bioresearcher-skills"
allowed-tools: Bash Read Write Edit Glob Grep
---

# Bioresearcher Plot-Making: Visual Dispatcher & Production Engine

This skill serves as the central router and quality assurance engine for
producing publication-grade scientific figures. It directs requests to
specialized domain plotting specifications, enforces declarative data
contracts, and verifies outputs against deterministic geometric QA gates.

## 1. Decision Matrix & Routing Table

Inspect the research request and input data to select the corresponding plot
type. Immediately load the detailed specification document using `Read`:

| Generalized Plot Type | Input Data & Research Context | Reference Specification |
| :--- | :--- | :--- |
| **`structural-biology_binder-visualization`** | PDB/mmCIF coordinates, structural conformer comparisons, RMSF trajectories, multi-ligand binding modes, residue contact matrices (BSA, H-bonds, salt bridges). | [Structural Biology Guide](references/structural-biology-binder-visualization.md) |
| **`literature-search_method-summary`** | Biomedical literature syntheses, translational risk pathways, developmental drug case registers (preclinical $\to$ approved), preclinical assay detection cascades, structured evidence tables. | [Literature Summary Guide](references/literature-search-method-summary.md) |
| **`qa-gates-and-gotchas`** | Multi-panel alignment troubleshooting, vector collision audit failures, minimum glyph size compliance, hard-earned gotchas. | [QA Gates and Gotchas Guide](references/qa-gates-and-gotchas.md) |

Do not generate plotting code without loading the corresponding reference guide.

## 2. Production Workflow

Follow this five-step workflow for all visualization requests:

### Step 1: Classify and Load Domain Specification

Identify the appropriate archetype from the Decision Matrix above. Load the
corresponding specification via `Read` (e.g. `Read references/structural-biology-binder-visualization.md`).

### Step 2: Ingest and Validate Declarative Data Contracts

Ensure input data conforms to the required schema before writing plotting code:
- **Structural Dynamics**: `conformer_rmsf.tsv` (`resnum`, `chain_role`, `domain`, `displacement_A`).
- **Interaction Matrix**: `binder_hotspot_matrix.tsv` (composite `<site>:<residue>` headers, triple-encoded cells `BSA_A2|HBOND|SALTBRIDGE`).
- **Case Register**: `literature_cases.tsv` (`entity_name`, `hazard_description`, `development_stage`, `status`, `pmids`).
- **Detection Cascade**: `assay_cascade.tsv` (`assay_name`, `readout`, `method_family`, `screening_stage`, `pmids`).
- **Evidence Matrix**: `evidence_table.tsv` (`citation`, `test_system`, `sample_matrix`, `analytical_method`, `readout`).

### Step 3: Verify uv Python Environment & Dependencies

Never rely on globally installed host packages. Ensure the project-local uv
environment is configured (via `bioresearcher-python-setup-uv`) with all
required visualization libraries:

```bash
./uv venv .venv
VIRTUAL_ENV="$(pwd)/.venv" ./uv pip install pymol-open-source matplotlib pymupdf numpy pillow biopython pandas
```

If `bioresearcher-python-setup-uv` already raced and exported `UV_INDEX_URL`, keep it exported — these installs inherit it automatically.

The `VIRTUAL_ENV` pin is mandatory: on hosts with an active conda/mamba environment (`CONDA_PREFIX`), bare `./uv pip install` silently targets the HOST environment instead of `./.venv`.

Never execute plotting scripts that write outputs to the workspace root:
- Create a dedicated target directory: `figures/<TARGET>/`.
- Place or generate data files directly inside `figures/<TARGET>/`.
- Ensure all Python scripts resolve relative paths via `Path(__file__).resolve().parent`.

### Step 4: Execute Deterministic Plotting Script

Run the figure generation script using the project-local interpreter:

```bash
./.venv/bin/python fig1.py
# Or for standalone PyMOL scripts:
# ./.venv/bin/pymol -cq render_script.py
```

### Step 5: Enforce Three-Layer Quality Assurance (QA)

Certify figures before delivery:
1. **Layer 1 (Static Source Preflight)**: Enforce standard typography (`font.family='sans-serif'`, base size 7 pt) and vector formats (`pdf.fonttype=42`, `svg.fonttype='none'`).
2. **Layer 2 (Deterministic Geometry Gates)**:
   - Run panel alignment gate (`audit_panel_alignment.py`): max deviation $\le 1.5\text{ pt}$.
   - Run vector collision audit (`audit_figure_collisions.py`): 0 FAIL.
   - Run font floor audit (`audit_pdf_text.py`): minimum glyph size $\ge 5.0\text{ pt}$.
3. **Layer 3 (Vision Model Semantic Review)**: Ask focused, single-question queries to verify biological topology and icon orientation.

## 3. Core Gotchas Summary

- **CWD Drift**: Relative save paths silently write to the process cwd; always verify outputs exist in the target directory with fresh timestamps.
- **Probe Render Trick**: Never render 3D text labels in PyMOL; extract 2D projection coordinates via a probe pass (`render_anchors.json`) and draw native vector text in Matplotlib.
- **Contact-Fragment Pruning**: Superimposing full macromolecules buries the receptor; prune ligands to residues within 8 Å plus 3-residue extension.
- **Dynamic Text Advance**: Use `right_edge()` taking `max(ink_bbox, advance_width)` to space inline text; character-count heuristics fail on proportional fonts.
- **Baseline Staggering**: Alternate column header baselines ($y=9.50$ vs $8.98$) to prevent PDF parsers from merging adjacent text runs.
- **Aspect Ratio Desync**: Panels sharing a row with `aspect='equal'` will letterbox and drift vertically unless physical aspect ratios match.
