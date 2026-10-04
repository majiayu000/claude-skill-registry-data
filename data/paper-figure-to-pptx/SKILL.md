---
name: paper-figure-to-pptx
description: Convert academic paper figures (architecture diagrams, system diagrams, timeline/pipeline diagrams, flowcharts, method overviews) into editable PowerPoint files where every box, text, formula, and arrow is a native PPT shape that can be double-clicked and edited. Use this skill whenever a user uploads or references a paper figure image and wants to recreate, edit, or adapt it in PowerPoint, even if they don't explicitly name the skill. Trigger phrases include 论文图转 PPT, 论文插图转可编辑 PPT, 学术论文架构图转 PPT, 论文图转 pptx, paper figure to editable powerpoint, image to editable pptx. NOT for pitch decks, marketing slides, AI-stylized illustrations, data/chart visualization, or generating figures from scratch without a reference image.
---

# Paper Figure to Editable PPT

## What This Skill Does

Convert a paper figure (JPG/PNG) into a native `.pptx` file where every element is editable in PowerPoint. Not a raster-to-vector trace, not an AI re-interpretation — a structured reconstruction using `python-pptx` so each box, text, formula, and arrow is an editable PPT shape.

## Realistic Expectations

Set these with the user upfront. "Perfect" reproduction is not achievable in one shot for any non-trivial figure, but close-to-faithful reconstruction with minor post-edits is very achievable.

- **What this skill produces reliably**: layout, text, arrows, regions, formulas with sub/superscripts, token sequences, labeled boxes.
- **What requires user post-editing in PPT**: complex domain icons (UAV, satellite, phone, database — use placeholders like `[UAV]` then swap with official SVGs), wavy lines (python-pptx has no wavy connector), perfect mathematical typesetting for complex formulas.
- **What user effort saves the most time**: providing a zoomed-in screenshot of each module after the block-plan is agreed (see Stage 2).

## The Five-Stage Workflow

Do not skip stages. Each stage exists because skipping it caused a rework in past runs.

### Stage 1: Structural Parse

List every element of the figure in a Markdown tree — top-level regions → sub-modules → internal elements → cross-region connections. Do not write code yet. Output the tree, then **stop and ask the user to confirm**. This forces alignment before investing in code.

Format:
```
**Region A: Top-level name**
- A1: Sub-module (x-position, fill color, border style)
  - Internal element 1 (text / formula / icon type)
  - Internal element 2
- A2: Next sub-module

**Cross-region connections**
- Element X in Region A → Element Y in Region B, arrow style
```

### Stage 2: Block Plan (conditional)

Decide the figure's complexity level along two axes — across the figure, and within each block:

**Across the figure**:
- **Simple** (single independent framework diagram, one algorithm flowchart, one system schematic) → draw on one slide, skip to Stage 3.
- **Complex** (multi-panel figure with several parallel sub-figures, timelines, and bottom legends — typical of journal Fig. 1 / Fig. 2) → propose 3–5 Module blocks. Boundaries follow the figure's own visual dividers (dashed lines, color bands, whitespace).

**Within each Module** (only consider this once blocks are identified):
- **Module fits on one slide** → proceed normally with one `moduleN.py` per Module.
- **Module is internally dense** (e.g., spans 4+ partitions with its own timeline, or packs ≥ 8 sub-components that would crowd a single slide) → split the Module itself into sub-Modules (1a, 1b, 1c). Each sub-Module is a separate slide/script (`module1a.py`, `module1b.py`, ...), independently built and reviewed in Stage 4. The user will layer them in PowerPoint during final assembly (see Stage 5 delivery notes). This pattern keeps the self-review cycle tight — a dense Module's bugs don't cascade across unrelated regions.

After the user confirms the block plan (and any sub-Module split), **strongly suggest they send a zoomed screenshot of each individual Module or sub-Module**. The thumbnail of a whole figure hides icon details, label fonts, and subtle colors that the full-image view cannot convey. This optional step dramatically improves fidelity.

### Stage 3: Proportion Estimate (advisory)

Estimate each Module's width:height ratio from the original. Three common patterns:

| Figure type | Approx ratio | Suggested slide height |
|---|---|---|
| Horizontal timeline band (TTFT/TPOT style) | 4:1 to 7:1 | 3.0–3.5 inches |
| Square-ish architecture diagram | close to 16:9 | nearly full slide |
| Ultra-wide legend/caption band | 7:1 to 10:1 | 1.5–1.8 inches |

Use **relative-proportion scaling**: keep ratio relationships between Modules faithful to the original, allow absolute sizes to enlarge where content needs room. Users with explicit size requirements override this.

**Narrow-partition check**: for any partition narrower than ~1.5 inches (common in horizontal bands with 4+ columns), list each planned internal element (icons, labels, text). If an element's natural width exceeds the partition width, don't just shrink the font — the usual fix is to relocate the label to the upstream partition's whitespace where the incoming arrow enters this narrow partition. See Pitfall 11 for the decision logic. Catching this at Stage 3 avoids rebuilding the partition in Stage 4.

**Critical for merging**: define shared horizontal x-coordinate constants (e.g., `TTFT_X = 1.60`, `RED_LINE_X = 6.75`, `TPOT_X = 6.80`) at the top of every Module file. All Modules use the same constants so assembled output aligns automatically.

### Stage 4: Build + Self-Review (up to 3 rounds)

**Setup at the start of a new task** (do this once before writing any Module):
1. Copy `scripts/helpers.py` to your working directory (so `from helpers import *` works).
2. For each Module, copy `scripts/module_template.py` to your working directory as `module1.py`, `module2.py`, etc.
3. Also copy `scripts/assemble.py` to your working directory (it must live alongside the module files to auto-discover them).

For each Module:
1. Open `moduleN.py`, replace the example content inside `build_module(prs)` with real drawing code matching the structural parse.
2. Run `python moduleN.py` to generate a single-page pptx.
3. Convert to JPG for visual inspection:
   ```bash
   soffice --headless --convert-to pdf moduleN.pptx
   pdftoppm -jpeg -r 150 moduleN.pdf slide
   ```
4. Inspect `slide-1.jpg`. Fix obvious defects. **Maximum 3 rounds**; typically 2 converges. Do not make a pre-flight checklist — just look at the image and fix what looks wrong.

Common issues to catch: placeholder text leakage (`[wavy line]` visible in output), LaTeX source text displayed literally, decorative lines occluded by region fills, text overflow, misalignment. For known traps, read `references/pitfalls.md`.

### Stage 5: Deliver

Two artifacts:
1. **Each Module's individual `.pptx`** — for user to inspect blocks separately.
2. **A single combined multi-page `.pptx`** (one page per Module) — run `python assemble.py` from the working directory. Saves the user from manual copy-paste.

**If Stage 2 produced sub-Modules (1a/1b/1c) within a Module**, add a third artifact and a merge instruction in the delivery summary:
3. **Per-sub-Module `.pptx` files** (e.g., `module1a.pptx`, `module1b.pptx`, `module1c.pptx`) — each is a separate slide rendering one sub-region. The combined pptx will show them on consecutive pages.

Tell the user explicitly how to layer sub-Modules onto a single target page in PowerPoint:
1. Open the combined pptx, pick the page that should become the final canvas (usually the first sub-Module).
2. For each other sub-Module page: `Ctrl+A` to select all shapes → `Ctrl+C` to copy → go to the target page → `Ctrl+V`. The shapes paste at the same x/y coordinates, which is why shared x-constants (Rule 6) matter.
3. Delete the now-empty sub-Module pages.
4. Check layering: if a sub-Module's fills obscure another's content, right-click the covering shape → "Send to Back" / "Bring to Front" to fix order.

Without this instruction, users often try to recreate the layout manually and lose the coordinate alignment.

How to deliver depends on environment:
- **Claude.ai chat**: copy files to `/mnt/user-data/outputs/` and call the `present_files` tool.
- **Claude Code CLI**: files are already in the user's working directory; just confirm paths and next steps.

## Design Rules (Hard Rules — Violations Require Rework)

These rules emerged from actual reworks. Read `references/design_rules.md` for the full reasoning behind each rule.

1. **Case/sub-figure labels**: vertical text stack outside the region, no card frame.
2. **Region outer frames**: dashed borders (`dash=True`), pale fills (C_PALE_BLUE not C_LIGHT_BLUE).
3. **Formulas and any text containing sub/superscripts**: always use `add_formula_tb()` with the parts list. Never put raw `T^{G2A}_{u→k}` in plain text — it renders literally. This applies not only to standalone formulas but to *any* line containing a token with sub/superscripts — captions, step annotations, legend text like "Process all ñ_u^in tokens in parallel" all need the formula path. See Pitfall 8 for examples.
4. **Critical decorative lines (red dashed lines, braces)**: draw LAST, after all regions. python-pptx z-order is insertion order; early lines get covered by later fills.
5. **Icons**: use `add_icon(slide, x, y, w, h, "[Type]")` for complex domain icons. Tell the user which to swap for official SVG icons (Cisco, AWS, Azure, GCP architecture icons, BioRender for biology, Flaticon/Noun Project general).
6. **Cross-Module coordinate alignment**: define the same x-coordinate constants at the top of every Module file.
7. **No wavy lines**: python-pptx cannot produce them. Draw straight lines and tell the user to replace them with PowerPoint's built-in wavy-line shape.

## Key Functions (from `scripts/helpers.py`)

Import all via `from helpers import *`:

| Function | Use case |
|---|---|
| `create_blank_slide(prs)` | Create 16:9 blank slide |
| `add_tb(...)` | Text box |
| `add_shape(...)` | Rectangle / rounded rectangle / oval / diamond |
| `add_arrow(...)` | Single-direction arrow |
| `add_bidir_arrow(...)` | Two-headed arrow (periodicity, range) |
| `add_line(...)` | Plain line, no arrowhead (for dashed refs, braces) |
| `add_formula_tb(slide, x, y, w, h, parts, ...)` | **Formula with real sub/superscripts**. `parts` is a list of `(text, style)` with style in `{'n', 'sup', 'sub'}`. |
| `add_hbrace(slide, x1, x2, y, ...)` | Horizontal brace (manual 4-line construction, avoids LEFT_BRACE rotation pitfall) |
| `add_icon(slide, x, y, w, h, label)` | `[Type]` placeholder with bold border |
| `add_token_row(...)` | Horizontal sequence of small boxes (e.g., LLM token stream) |
| `add_dashed_note_box(...)` | Gray dashed note box for small annotations |

All color constants: `C_BLUE`, `C_LIGHT_BLUE`, `C_PALE_BLUE`, `C_GREEN`, `C_PALE_GREEN`, `C_ORANGE`, `C_PALE_ORANGE`, `C_PURPLE`, `C_LIGHT_PURPLE`, `C_GRAY_TEXT`, `C_GRAY_BORDER`, `C_RED`, `C_BLACK`, `C_WHITE`, `C_NAVY`, `C_BROWN`, `C_YELLOW`. Use `C_PALE_*` for region fills, `C_LIGHT_*` for secondary elements.

## Environment-Specific Notes

### In Claude.ai Chat

- Work in `/home/claude/` (write module scripts there).
- After self-review passes, copy final `.pptx` files to `/mnt/user-data/outputs/`.
- Call `present_files` tool to surface them to the user.
- Always deliver both individual module pptx files AND the combined multi-page pptx.

### In Claude Code CLI

- Work directly in the user's project directory.
- Use the `Write` tool for module scripts, `Bash` for running them.
- Final pptx files end up in the user's directory — confirm paths with the user, don't move them.
- No `present_files` tool needed; user already has filesystem access.

## Further Reading (load on demand)

- `references/pitfalls.md` — 7 documented python-pptx traps with symptoms and fixes. Read when a visual defect appears that you don't immediately understand.
- `references/design_rules.md` — Extended reasoning for each design rule. Read when user pushes back on a rule or asks "why".
- `references/deployment.md` — How to install this skill to Claude.ai / Claude Code / API. Read only if the user asks about deployment.

## Minimum Delivery Checklist

- [ ] Individual `.pptx` for each Module (for spot-inspection).
- [ ] Combined multi-page `.pptx` (primary deliverable for user's editing workflow).
- [ ] Summary of known limitations: icon placeholders needing swap, wavy lines to redraw, formulas to re-typeset with PowerPoint's equation editor if user is picky.
- [ ] List of shared x-coordinate constants used (so user knows what to keep consistent if they modify).
- [ ] **If sub-Modules were produced**: the per-sub-Module files AND explicit layering instructions (select-all → copy → paste onto target page). Without this, users lose the alignment benefit of shared x-constants.
