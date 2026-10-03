---
name: diagram-pdf
description: Generate standalone TikZ diagrams (pipelines, hierarchies, cycles, hub-and-spoke, thematic) compiled to PDF, with a mandatory independent audit agent that catches overlap and routing defects before delivery. Triggers on "create a diagram", "diagram this", "draw a diagram", "workflow diagram", "visualize this workflow", "process diagram", "org chart", "concept map", "thematic diagram", "diagram the themes", "map the themes", and "visualize key themes".
when_to_use: Use when the user wants a picture of a structure as its own deliverable, such as a workflow or process diagram, an org chart or other hierarchy, a cycle, a hub-and-spoke layout, or a concept map of the themes in some source material. The output is one diagram compiled to its own PDF, so use a slide skill instead when the picture is meant to be a figure inside a deck being generated.
allowed-tools: Bash(pdflatex*), Bash(mkdir*), Bash(ls*), Bash(cp*), Bash(mv*), Bash(rm*), Bash(cd*), Bash(which*), Read, Write, Edit, Glob, Grep, Agent
---

# Diagram Generation

Generate standalone TikZ diagrams rendered to PDF. Supports multiple layout types for workflows, hierarchies, cycles, hub-and-spoke relationships, and thematic maps. Uses a consistent color palette and typography defined in the diagram style guide.

## Input

The skill accepts two input modes:

1. **Free text description.** The user describes the structure, relationships, and elements to diagram. The skill determines the best layout type and generates the diagram.

2. **Auto-discovery from SKILL.md files.** The user points to a set of skill files or a skills directory. The skill reads trigger phrases, handoff points, inputs, outputs, and pipeline relationships to build a workflow diagram automatically. Ask: "Are you diagramming a skill workflow (I'll read the SKILL.md files) or describing something else?"

## Layout Types

### Pipeline

Vertical spine of sequential steps with optional side entries, user decision points, inputs, and outputs. Best for: skill workflows, process flows, multi-step procedures.

**Structure:** Linear sequence of steps at x=0, content boxes flanking each step (outputs left, inputs right), side entries positioned between steps at offset x-positions, connecting diagonally to the main spine.

### Hierarchy

Top-down tree with a root node and branching children. Best for: org charts, decision trees, taxonomies, classification schemes.

**Structure:** Root at top center, children distributed horizontally at each depth level, connected by downward arrows. Sibling spacing computed from the number of children and their widths.

### Cycle

Nodes arranged in a circular or polygonal pattern with directional arrows along the perimeter. Best for: feedback loops, iterative processes, circular dependencies.

**Structure:** Nodes placed at equal angular intervals around a center point. Radius computed from node count and sizes. Optional central label or annotation.

### Hub-and-Spoke

Central concept node with radiating connections to surrounding nodes. Best for: central concept with supporting elements, stakeholder maps, capability models.

**Structure:** Central node at origin, spoke nodes at consistent radius and equal angular spacing. Labels on spokes describe the relationship.

### Thematic

Central thesis node with surrounding theme clusters, each containing bullet-point sub-themes. Best for: visualizing a user-supplied set of themes and sub-themes with relationships between them.

**Structure:** Central thesis node, theme clusters positioned in a grid or radial arrangement. Each cluster has a colored header and a body with sub-theme bullets. Connections between related clusters shown with labeled arrows.

### Layout Complexity Classification

Diagrams are classified for generation purposes:

- **Simple layouts:** Hierarchy, hub-and-spoke, thematic, simple pipelines without feedback arrows. These proceed directly to full generation in a single pass (Step 3, single-pass mode).
- **Complex layouts:** Pipelines with feedback loops, cycles with cross-connections, or any layout requiring arrows that must route around multiple unrelated nodes. These require the two-phase generation process (Step 3, two-phase mode).

The independent audit agent (Step 5) runs regardless of layout complexity.

## Working Directory

Output files go in the current working directory by default. If the user specifies a different output folder, the skill writes there instead.

**Default layout (current working directory):**

```
./
├── <name>-diagram.pdf           (final deliverable)
└── diagram-build/
    ├── diagram.tex
    ├── diagram.pdf
    └── diagram.log
```

**With an explicit output folder:**

```
<output-folder>/
├── <name>-diagram.pdf
└── diagram-build/
    ├── diagram.tex
    ├── diagram.pdf
    └── diagram.log
```

The `.tex` source remains in the build subfolder so the user can edit and recompile without re-invoking the skill.

Name the final diagram descriptively (e.g., `case-workflow-diagram.pdf`, `ai-themes-diagram.pdf`).

## Step 0: Verify LaTeX Installation

Check that `pdflatex` is available:

```bash
which pdflatex
```

If not found, inform the user: "pdflatex is not installed. Install a TeX distribution: MacTeX on macOS (`brew install --cask mactex-no-gui`), TeX Live on Linux (`sudo apt install texlive-full`), or MiKTeX on Windows (https://miktex.org/download)."

## Step 1: Determine Layout and Content

### Free Text Input

1. Ask the user what they want to diagram if not already clear.
2. Identify the best layout type based on the description. If ambiguous, propose a layout and ask for confirmation.
3. Parse the description into elements: nodes, connections, labels, groupings.

### Auto-Discovery (Skill Workflows)

1. Read the specified SKILL.md files.
2. Extract from each: skill name, description, triggers, input requirements, output deliverables, handoff prompts to other skills.
3. Build a directed graph of skill relationships (which skill hands off to which).
4. Identify the pipeline spine (longest path), side entries (skills that feed into mid-pipeline steps), and optional branches.
5. Present the discovered structure to the user for confirmation before rendering.

## Step 2: Read Style Guide

Read the diagram style guide and apply all color definitions, node styles, arrow styles, typography, and spacing constants. Do not deviate from the style guide unless the user explicitly requests a modification.

**Default path:** If this skill was installed alongside the `style-guides/diagram-pdf/` folder from the same repo, the style guide lives at `style-guides/diagram-pdf/style-guide.md`. If the user installed it elsewhere, read from their chosen path. The skill cannot proceed without the style guide loaded.

## Step 3: Generate .tex

### Determine Generation Mode

Before generating, classify the diagram per the Layout Complexity Classification above:

- **Single-pass mode:** No feedback arrows, no complex routing. Proceed to "Algorithmic Positioning" and "Content Generation" below, then directly to Step 4.
- **Two-phase mode:** Feedback loops or arrows that must route around unrelated nodes. Proceed to "Phase 1: Static Elements with Coordinate Extraction" below.

### Algorithmic Positioning

Compute element positions based on the layout type. These rules apply to both single-pass and two-phase modes.

**Pipeline layout positioning:**

1. Place main spine nodes at x=0, starting at y=-2.5, with 2.2cm vertical spacing between consecutive steps. Add 1.8cm for each milestone/decision point between steps.
2. Place output nodes at x=-3.6, same y as their pipeline step, anchor=east.
3. Place input nodes at x=3.6, same y as their pipeline step, anchor=west.
4. **Paired node yshift:** When two nodes flank a spine node, use `yshift=16pt` for the upper and `yshift=-16pt` for the lower. The corresponding arrow yshifts from the spine node should be `yshift=6pt` / `yshift=-6pt`.
5. Identify clear vertical zones: y-ranges between pipeline steps where no content boxes exist.
6. Place side entries at the appropriate horizontal offset (left: x=-8.5, right: x=10.5) at y-positions within clear zones, NOT at the same y as any pipeline step.
7. Route side entry arrows to target pipeline steps using `north west` (left entries) or `north east` (right entries) anchors, creating diagonal paths through clear space.
8. Verify: for each side entry arrow, compute the arrow's y-coordinate at the x-positions of all content boxes it crosses. Confirm the arrow clears the top/bottom edges of every unrelated content box by at least 0.1cm. If not, shift the side entry further from the pipeline step.

**Hierarchy layout positioning:**

1. Root node at (0, 0).
2. Children at y = parent_y - 2.5cm.
3. Horizontal spacing: distribute children evenly across the available width. Minimum 1.0cm gap between sibling nodes.
4. If a level has too many children to fit (> 6), split into two rows at that level.
5. Connect parent to children with downward arrows.

**Cycle layout positioning:**

1. Compute radius: `r = max(1.5, n_nodes * 0.8)` cm where n_nodes is the number of cycle elements.
2. Place node i at angle `90 - i * (360/n_nodes)` degrees (starting from top, going clockwise).
3. Draw arrows along the cycle edges using `bend left` or explicit arc paths.
4. Optional central label at (0, 0).

**Hub-and-spoke positioning:**

1. Central node at (0, 0).
2. Spoke nodes at radius 4.0cm, evenly spaced by angle.
3. Arrows from center to each spoke, labeled on the connection.

**Thematic layout positioning:**

1. Thesis node at (0, 0) using `thesisnode` style.
2. Theme clusters arranged in a grid: 2-3 columns, rows as needed.
3. Each cluster is a stacked pair: `themeheader` node on top, `themebody` node below (anchored to header's south).
4. Grid spacing: 5.0cm horizontal between cluster centers, 4.0cm vertical between rows.
5. Center the grid around the thesis node, with the thesis above the grid or in the center with clusters around it.
6. Draw relationship arrows between related clusters using `arrowside` style with labels.

### Content Generation

1. Write the complete .tex file with all color definitions, style definitions, and positioned nodes.
2. Include a descriptive title and subtitle.
3. Include a legend appropriate to the layout type.
4. Use `\\` for line breaks within nodes, `\textbf{}` for emphasis, `\textit{}` for titles.
5. Escape special LaTeX characters in all user-provided text: `&` → `\&`, `%` → `\%`, `_` → `\_`, `#` → `\#`, `$` → `\$`, `>` → `$>$`, `<` → `$<$`.

### Two-Phase Generation (Complex Routing)

For diagrams classified as complex, generate in two phases. Do NOT attempt to place feedback arrows by guessing coordinates.

#### Phase 1: Static Elements with Coordinate Extraction

Generate the .tex with all static elements but NO feedback arrows:

1. All spine/core nodes, input/output nodes, skill/context nodes, downstream nodes.
2. All simple arrows (spine connections, input/output connections).
3. Legend, title, subtitle.
4. A coordinate extraction block appended before `\end{tikzpicture}`:

```latex
\makeatletter
\foreach \nodename in {node1, node2, node3, ...} {
  \pgfpointanchor{\nodename}{north east}
  \typeout{BBOX:\nodename:ne:\the\pgf@x:\the\pgf@y}
  \pgfpointanchor{\nodename}{south west}
  \typeout{BBOX:\nodename:sw:\the\pgf@x:\the\pgf@y}
}
\makeatother
```

The node list must include every named node. Include a comment `% ── NO FEEDBACK ARROWS IN PHASE 1 ──` where feedback arrows will go.

Save as `diagram-phase1.tex` in the build directory.

#### Phase 1: Compile and Parse

```bash
cd "<build-directory>" && pdflatex -interaction=nonstopmode -jobname=diagram-phase1_tmp diagram-phase1.tex
```

Parse `BBOX:` lines from the log. Each line: `BBOX:<name>:<ne|sw>:<x in pt>:<y in pt>`. Convert pt to cm by dividing by 28.45274. Record the bounding box of every node as (west, east, south, north) in cm.

#### Phase 2: Compute Safe Routes

From the bounding boxes:

1. **Right corridor x** = max(all node east edges) + 0.5cm
2. **Left corridor x** = min(all node west edges) - 0.5cm
3. **Top waypoint y** = max(all node north edges) + 0.5cm (but below the subtitle)

Feedback arrows use only horizontal and vertical segments with `rounded corners=8pt`. Standard patterns:

**Right-side feedback** (output east to spine north):
```latex
\draw[arrowfeed, rounded corners=8pt]
  let \p1 = (source.east) in
  (\p1) -- (RIGHT_CORRIDOR, \y1) -- (RIGHT_CORRIDOR, TOP_Y) -- (0, TOP_Y) -- (target.north);
```

**Left-side feedback** (spine west to output west):
```latex
\draw[arrowfeed, rounded corners=8pt]
  let \p1 = (source.west), \p2 = (target.west) in
  (\p1) -- (LEFT_CORRIDOR, \y1) -- (LEFT_CORRIDOR, \y2) -- (\p2);
```

The `let` syntax ensures arrow start/end y-coordinates track actual node positions. Corridor x-values and top y are hardcoded from Phase 1 measurements.

**Label placement:** Position labels adjacent to the vertical corridor segment. Use absolute coordinates at y-values verified clear of all elements by checking against bounding boxes. Use `anchor=west` for right-side labels, `anchor=east` for left-side labels.

**Document the corridors** in a comment block above the feedback arrows:
```latex
% Right route corridor: x = <value>cm (clears <node> + 0.5cm)
% Left route corridor:  x = <value>cm (clears <node> + 0.5cm)
```

#### Phase 2: Assemble Final .tex

1. Copy the Phase 1 .tex.
2. Remove the coordinate extraction block.
3. Insert the feedback arrows and labels.
4. Save as the final diagram name (e.g., `diagram.tex`).
5. Proceed to Step 4.

## Step 4: Compile

Compile the final .tex (single-pass output for simple layouts, or Phase 2 assembled output for complex layouts):

```bash
cd "<build-directory>" && pdflatex -interaction=nonstopmode diagram.tex
```

If compiling into a cloud-synced directory (Dropbox, iCloud Drive, OneDrive), compile to a temporary jobname first to avoid sync-lock collisions, then copy the result:

```bash
pdflatex -interaction=nonstopmode -jobname=diagram_tmp diagram.tex
cp diagram_tmp.pdf diagram.pdf
```

Check for errors in the log. If compilation fails, fix the .tex source and recompile. Do not proceed to the audit with a failed compilation.

## Step 5: Independent Quality Audit

After the final diagram compiles cleanly, hand the compiled PDF and .tex source to an **independent audit agent** using the Agent tool. This audit is mandatory for ALL diagrams regardless of layout complexity.

### Why an Independent Agent

The generating agent cannot reliably audit its own output. It sees what it intended, not what rendered. Testing confirmed that paired-node overlap defects (yshift spacing too tight) went undetected across multiple self-audit rounds but were immediately caught by an independent agent performing coordinate arithmetic.

### Audit Agent Invocation

Launch the audit agent with the Agent tool. The prompt must instruct it to:

1. Read the audit checklist at `audit-checklist.md` (shipped alongside this skill, in the same directory).
2. Read the diagram style guide (the file used in Step 2).
3. Read the compiled PDF.
4. Read the .tex source.
5. Apply every checklist item to the diagram.
6. Report defects with specific node names, coordinates, bounding box arithmetic, and proposed fixes.

The audit agent must have NO knowledge of what defects were previously found, what generation approach was used, or what iterations occurred. It receives only the rendered output and source.

### Audit Convergence Limit

Maximum 3 audit rounds. If defects persist after 3 rounds, present the diagram to the user with remaining findings noted.

## Step 6: Fix, Re-Audit, and Present

1. Fix ALL defects reported by the audit agent.
2. Recompile.
3. Re-invoke the audit agent on the fixed output. The re-audit is a fresh Agent invocation with no memory of previous findings.
4. If the re-audit finds new defects, fix and repeat (up to the convergence limit).
5. When the audit returns zero defects (or the limit is reached), copy the final PDF to the output folder.
6. Read the PDF and present it to the user for review.

If the user requests changes after delivery, edit the .tex source, recompile, and run the audit agent again before presenting. Every compilation that changes element positions must go through the audit.

## Output

- **Primary deliverable:** `<descriptive-name>-diagram.pdf` in the output folder (current working directory by default, or user-specified).
- **Build artifacts:** `.tex`, `.pdf`, `.log`, `.aux` in `<output-folder>/diagram-build/`.
- The `.tex` source is the editable artifact. Users can return to modify the diagram by editing the `.tex` and recompiling.
