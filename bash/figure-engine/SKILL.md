---
name: figure-engine
description: >
  Activate when the user needs to generate, refine, or evaluate academic figures,
  diagrams, or statistical plots. Uses PaperBanana to transform text descriptions
  or data files into publication-quality illustrations via direct Python API call.
  Fallback: matplotlib/seaborn.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Figure Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (figure-engine)
> **Input:** [brief description of the figure request]
> **Output:** [brief description of what was produced — e.g., "Generated methodology diagram (fig03_methodology.png), 3 iterations"]
> ```

# Figure Engine

## Core Principle
Academic papers need professional figures. This skill eliminates manual design work
by using PaperBanana to generate publication-quality diagrams and plots from text
descriptions or data files. Claude should produce ACTUAL FIGURES, not describe what
to draw.

> **Based on:** Zhu, D., Meng, R., Song, Y., Wei, X., Li, S., Pfister, T., & Yoon, J. (2026).
> *PaperBanana: Automating Academic Illustration for AI Scientists.* [arXiv:2601.23265](https://arxiv.org/abs/2601.23265).
> The pipeline uses a 5-agent, 2-phase architecture: Retriever → Planner → Stylist (Phase 1: planning),
> then Visualizer ↔ Critic iterative refinement (Phase 2: generation) with VLM-as-Judge evaluation.
> Official research repo: [`dwzhu-pku/PaperBanana`](https://github.com/dwzhu-pku/PaperBanana).

## Prerequisites

PaperBanana must be installed: `pip install paperbanana[mcp,google]`

A `GOOGLE_API_KEY` must be available via one of:
- Environment variable `GOOGLE_API_KEY`
- `.env` file in project root
- `~/.paperbanana.env`

Get a free key at https://aistudio.google.com/apikey

---

## Method Priority

### Priority Order:
1. **PRIMARY — Direct Python API** (via Bash → python3) — ALWAYS use this
2. **FALLBACK — matplotlib/seaborn** — If PaperBanana is not installed at all

> **Note:** The PaperBanana MCP server is NOT used. The MCP stdio transport is
> unreliable (timeouts, hangs, silent failures). Always use the direct Python API.

---

## Method 1: Direct Python API (PRIMARY — Always Use This)

The plugin ships a helper script `scripts/paperbanana_direct.py` that calls the
PaperBanana Python API directly via `asyncio.run()`, completely bypassing the
MCP stdio transport. It outputs JSON to stdout.

### Locating the Script

The script is at `scripts/paperbanana_direct.py` inside the plugin directory.
To find it reliably across any installation:

```bash
PB_SCRIPT="$(find ~/.claude/plugins -name paperbanana_direct.py -path '*/open-academic-paper-machine/*' 2>/dev/null | head -1)"
```

### Generate Diagram

For **short** source contexts (< 1000 chars), pass inline:

```bash
PB_SCRIPT="$(find ~/.claude/plugins -name paperbanana_direct.py -path '*/open-academic-paper-machine/*' 2>/dev/null | head -1)" && \
python3 "$PB_SCRIPT" diagram \
  --source-context "The research follows a three-stage SLR methodology..." \
  --caption "Figure 1: Systematic Literature Review Process" \
  --output-dir figures/ \
  --filename "fig_method_slr_process.png" \
  --iterations 3
```

For **long** source contexts, write to a temp file first to avoid shell escaping issues:

```bash
# Step 1: Write source context to temp file
cat > /tmp/pb_source_context.txt <<'CTXEOF'
[FULL METHODOLOGY TEXT / FRAMEWORK DESCRIPTION HERE — can be multiple paragraphs,
include all relevant details about components, relationships, and visual structure]
CTXEOF

# Step 2: Generate the figure
PB_SCRIPT="$(find ~/.claude/plugins -name paperbanana_direct.py -path '*/open-academic-paper-machine/*' 2>/dev/null | head -1)" && \
python3 "$PB_SCRIPT" diagram \
  --source-context "$(cat /tmp/pb_source_context.txt)" \
  --caption "Figure N: Descriptive Caption" \
  --output-dir figures/ \
  --filename "fig_section_description.png" \
  --iterations 3
```

### Generate Plot

```bash
PB_SCRIPT="$(find ~/.claude/plugins -name paperbanana_direct.py -path '*/open-academic-paper-machine/*' 2>/dev/null | head -1)" && \
python3 "$PB_SCRIPT" plot \
  --data '{"categories": ["2020","2021","2022","2023","2024"], "values": [12,25,48,89,156]}' \
  --caption "Bar chart showing exponential growth in AI adoption across financial services" \
  --output-dir figures/ \
  --filename "fig_results_adoption_growth.png" \
  --iterations 3
```

### Evaluate Diagram

```bash
PB_SCRIPT="$(find ~/.claude/plugins -name paperbanana_direct.py -path '*/open-academic-paper-machine/*' 2>/dev/null | head -1)" && \
python3 "$PB_SCRIPT" evaluate \
  --generated figures/fig_generated.png \
  --reference figures/fig_reference.png \
  --context "Original methodology text" \
  --caption "Figure caption"
```

### Reading the Output

The script prints JSON to stdout:
- Success: `{"status":"ok","image_path":"figures/fig_name.png","iterations":3,"metadata":{...}}`
- Error: `{"status":"error","message":"..."}`

On success, show the figure to the user using the Read tool on the PNG path.

### Timeout

PaperBanana generation takes 30-180 seconds (3 refinement iterations). Set a
generous Bash timeout of **300 seconds** (5 minutes) when calling the script.

---

## Method 2: Python matplotlib/seaborn (FALLBACK)

If PaperBanana is not installed at all, generate figures with Python directly:

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'figure.figsize': (10, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox_inches': 'tight',
})
```

For methodology diagrams without PaperBanana, use networkx or graphviz:
```python
import networkx as nx
# Build a directed graph and render with matplotlib
```

---

## When the User Says "Make Me a Figure" — What to Do

1. **Determine figure type**: diagram (methodology, framework, process) or plot (bar, line, scatter, etc.)
2. **Gather input**: text description for diagrams, data file for plots
3. **Generate using Direct Python API** (Method 1) — ALWAYS use this
4. **If Method 1 fails**: fall back to matplotlib/seaborn (Method 2)
5. **Save to figures/ directory** in the working folder
6. **Provide LaTeX include snippet** ready for copy-paste
7. **Show the generated figure** to the user using Read tool on the PNG

---

## Diagram Prompting Guide

Good source context for PaperBanana includes:
- **What the diagram shows**: "This figure illustrates the three-phase research design"
- **Key components**: "Phase 1: Literature Search, Phase 2: Screening, Phase 3: Analysis"
- **Relationships**: "Phase 1 feeds into Phase 2, which filters down to Phase 3"
- **Style hints**: "PRISMA-style flow diagram" or "layered architecture diagram"
- **Layout direction**: "left-to-right flow" or "top-to-bottom hierarchy"

The **communicative_intent** (caption) should describe WHAT the figure communicates,
not just what it contains. Good: "Three-pillar model showing how education, process
redesign, and encoded judgment sequentially build sovereign AI mastery." Bad: "Figure 1."

---

## Academic Figure Standards

### General Rules
- **Resolution:** Minimum 300 DPI for print
- **Width:** Match journal column width (single column ~8.5cm, double column ~17.5cm)
- **Font:** Serif fonts (Times, Computer Modern) matching paper body
- **Colors:** Use colorblind-friendly palettes (e.g., Okabe-Ito, viridis)
- **Labels:** All axes labeled with units, legend if multiple series
- **Caption:** Descriptive, can stand alone without reading the text

### LaTeX Integration
Always provide the complete figure environment:
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/FILENAME.png}
\caption{DESCRIPTIVE CAPTION}
\label{fig:SHORT_LABEL}
\end{figure}
```

For side-by-side figures:
```latex
\begin{figure}[htbp]
\centering
\begin{minipage}{0.48\textwidth}
  \centering
  \includegraphics[width=\linewidth]{figures/LEFT.png}
  \caption{Left caption}
  \label{fig:left}
\end{minipage}
\hfill
\begin{minipage}{0.48\textwidth}
  \centering
  \includegraphics[width=\linewidth]{figures/RIGHT.png}
  \caption{Right caption}
  \label{fig:right}
\end{minipage}
\end{figure}
```

### File Naming Convention
`fig_SECTION_DESCRIPTION.png`
- `fig_method_prisma_flow.png`
- `fig_results_adoption_by_year.png`
- `fig_framework_sociotechnical.png`

---

## Integration with Paper Machine

When used inside the `/write-paper` pipeline (Phase 4: Production), the figure-engine
should be called automatically for sections that need visual support:

| Section | Typical Figures |
|---------|----------------|
| Methodology | Research design overview, PRISMA flow, sampling diagram |
| Results | Distribution plots, frequency charts, concept maps |
| Discussion | Framework diagram, comparison matrix, implications model |

The writing-engine should reference generated figures with `\ref{fig:label}` in the text.
