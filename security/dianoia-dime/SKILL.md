---
name: dianoia-dime
description: "After a paper release, build quick-start cards, one-click launchers, interactive figures and claim notebooks."
invocation: discipline
operad_source_colours: ["Paper", "Proof"]
operad_target_colour: "Diagram"
operad_arity: 2
operad_residual: "unknown"
---

# dianoia-dime

## Internal Receipt Ceiling

DIME mints no authority. Its public artifacts should explain evidence scope in ordinary reader language, not house receipt vocabulary.

## 1. Governance & Council Allocation

- **Governing Council:** **Dianoia** (`procurator_dc` — Media, Narrative Strategy & Public Engagement)
- **Peer Truth Auditor:** **Aletheia** (`procurator_ac` — Content Verification & Evidence Bounds)
- **Adversarial Gatekeeper:** **Thanatos Anti-DIME** (`thanatos-anti-dime` — Security, Defense & Anti-Slop Firewall)

---

## 2. The 3-Second Cognitive Engagement Ladder

When executed during `/rip-papers` (after `/paper-release`), DIME constructs the 3-tier cognitive ladder inside the paper directory:

```text
[Tier 1: 0–3 Seconds] Instant Visual Hook & 1-Line Verification
│  ├── public_export/fig*.png             # High-res publication-quality PNG figures
│  └── 1-Line Shell Command                # Copy-paste zero-dependency verification command
│
▼
[Tier 2: 3–30 Seconds] Dual Interactive Notebook Suite
│  ├── public_export/run_notebook.bat     # 1-Click launcher -> jupyter_notebooks/001_reviewer_*.ipynb
│  ├── public_export/run_notebook.sh      # POSIX launcher -> uv --with jupyter,ipywidgets,numpy,matplotlib
│  ├── public_export/run_refutation.bat   # 1-Click launcher -> jupyter_notebooks/002_refutation_sandbox.ipynb
│  ├── public_export/run_refutation.sh     # POSIX launcher -> uv --with jupyter,ipywidgets,numpy,matplotlib
│  ├── jupyter_notebooks/001_reviewer_*.ipynb       # Claim-by-claim interactive review notebook
│  └── jupyter_notebooks/002_refutation_sandbox.ipynb # Interactive falsification & boundary breaker notebook
│
▼
[Tier 3: 30+ Seconds] O(1) Structured Deep-Dive
   ├── docs/000_quick_start.md             # 1-Page Executive Summary & Quick-Start Card
   └── docs/claim_code_map.yaml            # Mechanized Claim-to-Code Mapping Registry
```

---

## 3. Mandatory DIME Deliverables & Dual Notebook Architecture

**Rebuild on every `/rip-papers` Stage 4.1 invocation** — do not skip if artifacts already exist.

1. **`docs/000_quick_start.md`:** 1-page executive summary, thesis statement, closed-form formulas, 1-line verification commands, launcher pointers to `001_reviewer_*.ipynb` and `002_refutation_sandbox.ipynb`, and top claim shortcuts.
2. **`docs/claim_code_map.yaml`:** Machine-readable YAML mapping every Claim ID -> Code Function -> Test File -> Notebook Cell -> Lean 4 Theorem.
3. **`code/generate_figures.py` or `*_lib/` figure helpers & `public_export/fig*.png`:** Publication-quality figures visualizing defects, bounds, and observer gaps.
4. **1-Click Launchers (`public_export/`):**
   - `run_notebook.bat` / `run_notebook.sh`: Opens `jupyter_notebooks/001_reviewer_*.ipynb` by default.
   - `run_refutation.bat` / `run_refutation.sh`: Opens `jupyter_notebooks/002_refutation_sandbox.ipynb` by default.
   - Both `cd` to paper package root and run via `uv run --with jupyter --with ipywidgets --with numpy --with matplotlib`.
5. **Notebook 1 — `jupyter_notebooks/001_reviewer_<topic>.ipynb` (Claim-by-Claim Interactive Walkthrough):**
   - **Claim Prose & Math Cell:** Displays exact claim statement, LaTeX equations, and Lean 4 formalization status.
   - **Production Code Import Cell:** Direct imports from package `code/` library (no manuscript-only duplicate math).
   - **Interactive Widget Cell:** `ipywidgets` continuous sliders/knobs (`FloatSlider`, `Dropdown`, `ToggleButton`) with live output refresh and `HAS_WIDGETS` static fallback.
   - **Embedded Test Verification Cell:** Programmatically executes corresponding Examiner pytest assertions (`pytest.main(["code/tests/...", "-k", "test_claim"])`) and displays live test results.
   - **Lean 4 Bijection Link:** Points to corresponding Lean 4 theorem signature.
6. **Notebook 2 — `jupyter_notebooks/002_refutation_sandbox.ipynb` (Interactive Falsification & Adversarial Sandbox):**
   - **Hypothesis Breaker Cells:** Allows reviewers to test parameter choices beyond validity boundaries, off-manifold points, uncontractive maps, and non-linear gauges.
   - **Live Refusal & Residual Visualizer:** Displays explicit `ReverseTriangleCertificate(accepted=False)` or residual threshold violations (`tripped = residual > 1e-12`).
   - **Mutation Audit Harness:** Lets reviewers toggle code mutations and confirm test suite failure detection.
   - **Evidence Scope Cell:** States what the notebook verifies, what it does not verify, and the relevant nonclaim boundaries in ordinary public language. Do not include `AuthorityEffect`, `Authority Effect`, `authority_effect`, or role-receipt vocabulary in public notebooks.

---

## 4. Stage 4.1 Acceptance Checklist (Blocking for DIME Green)

```text
[ ] run_notebook.bat and run_notebook.sh exist and resolve 001_reviewer_*.ipynb
[ ] run_refutation.bat and run_refutation.sh exist and resolve 002_refutation_sandbox.ipynb
[ ] all launchers pass --with ipywidgets to uv
[ ] 001_reviewer_*.ipynb contains claim-by-claim walkthrough, code imports, widgets, and pytest cells
[ ] 002_refutation_sandbox.ipynb contains hypothesis breaker cells, countermodels, and refusal visualizers
[ ] docs/000_quick_start.md links both launchers and notebooks
```

---

## 5. Constraint & Safeguard

DIME **never** exaggerates findings, invents hype, masks errors, or adds defensive boilerplate where a concise evidence-scope note is enough. All DIME artifacts are subject to mandatory adversarial audit by **`thanatos-anti-dime`** before publication.

## Mandatory De-Linting & Encoding Cleanliness (`RULE_MARKDOWN_DELINTING_001`)

Every file created or modified during the execution of this skill MUST be de-linted prior to turn completion. Run `/techne-docs-lint-hunter-killer` or `npx markdownlint-cli --fix` to verify **0 linter errors and 0 linter warnings**, and ensure no CP437/Windows-1252 Mojibake character artifacts remain (`RULE_UTF8_MOJIBAKE_CLEANLINESS_001`).
