---
name: results-to-slides
description: Automate the grunt work of making research presentations — discovers experiments from git/output folders, collects images and metrics, and organizes them into slides. Creates a slide-by-slide script for user approval, then generates slide markdown and editable PPTX.
argument-hint: [start_date end_date]
---

# Results to Slides

Discover experiments, collect images/metrics, organize into slides. You provide the story —
this skill handles the grunt work. Output: slide markdown + editable PPTX.

## Core Rules

1. **State what was done and what the result was. Do not editorialize.** Never use:
   "breakthrough", "key insight", "importantly". Just experiment + number.
2. **Every slide MUST have a visual.** No text-only slides (except pure tables). If a concept
   has no experiment images, create a diagram. If no diagram makes sense, show dataset examples.
3. **Images first, text second.** Plan images for each slide BEFORE writing bullets. If you
   can't find an image for a slide, restructure or merge it.

---

## Parallel Execution

Maximize use of the Agent tool. Whenever you have 2+ independent tasks, launch parallel agents.

- **Phase 1**: Launch agents in parallel to read CLAUDE.md, README.md, memory files
- **Phase 2 (biggest win)**: Launch separate agents for git log, output folders, scripts, media
- **Phase 3**: Launch agents in parallel to read different experiment scripts and output folders
- **Phase 5+6**: Sequential (markdown must be written before converting)

---

## Important Paths

- Skill directory: `${CLAUDE_SKILL_DIR}`
- Converter: `${CLAUDE_SKILL_DIR}/md_to_pptx.py`
- Backgrounds: `${CLAUDE_SKILL_DIR}/backgrounds/`
- Theme CSS: `${CLAUDE_SKILL_DIR}/theme.css`
- Slide element reference: [slide_reference.md](slide_reference.md)

---

## Phase 0: Parse Arguments & Setup

The user provides: `/results-to-slides START_DATE END_DATE`

Arguments come as `$ARGUMENTS` containing two MMDD date strings (e.g., `0301 0308`).

**Parse the dates:**
- `$0` = start date (MMDD), `$1` = end date (MMDD)
- Infer year from system date. End date is INCLUSIVE (use end_date + 1 for `find` bounds)

**If no arguments provided**, use `AskUserQuestion`:
- header: "Date range"
- question: "What date range? Use MMDD MMDD format (e.g., 0301 0308)."
- options: ["Last week", "Last 2 weeks", "Last month"]

**Output directory**: `presentation/YYYY_MM_DD/` using the end date.

### Ask Presentation Preferences

Ask all preferences upfront before discovery, in a SINGLE AskUserQuestion call:

1. **Background theme**: "Light (Recommended)", "Warm", "Dark"
2. **Emphasis areas**: "What should the presentation emphasize? (e.g., dataset, model architecture,
   results comparison, failed approaches)" — free text, helps prioritize slide count allocation.

| Choice | Background file | `--theme` flag |
|--------|----------------|----------------|
| Light  | `slide_bg_light.png` | `light` |
| Warm   | `slide_bg_warm.png`  | `light` |
| Dark   | `slide_bg_dark.png`  | `dark`  |

Do NOT ask for slide count. Generate as many slides as the content needs — images drive the
count, not a preset number.

---

## Phase 1: Research Context Discovery

Scan project docs (CLAUDE.md, README.md, memory files, `docs/`) to understand:
- Research question and direction
- Key metrics and what "good" vs "bad" looks like
- Terminology, model names, dataset names, output folder conventions
- Prior results and baselines
- **Previous presentations** (check `presentation/` directory for prior slide decks to recap)

If no research goal found, use `AskUserQuestion`:
- header: "Research context"
- question: "Brief description of what this project does?"
- options: ["Let me describe it", "Use README description"]

Use this context internally for smart organization (grouping, filtering, prioritization).
Do NOT let it leak into slide text.

---

## Phase 2: Experiment Discovery

Use ALL methods — each catches things the others miss.

### Git Log

```bash
git log --after="YYYY-MM-DD_START" --before="YYYY-MM-DD_END+1" --oneline --stat
```

Extract: commit messages (often contain results), files changed, dates.

### Output Folders

```bash
find . -maxdepth 2 -type d -newermt "YYYY-MM-DD_START" ! -newermt "YYYY-MM-DD_END+1" 2>/dev/null | sort
```

Also check: `outputs/`, `results/`, `experiments/`, `runs/`, `logs/`, `checkpoints/`.
Do NOT assume MMDD_ naming — use modification time as primary signal.

For each folder: list contents, look for metrics files (`metrics.json`, `*.pkl`, `scores.txt`,
`*.log`) and images (`*.png`, `*.jpg`, `*.gif`).

### Scripts

```bash
find . -name "*.py" -newermt "YYYY-MM-DD_START" ! -newermt "YYYY-MM-DD_END+1" 2>/dev/null | grep -v __pycache__ | sort
```

Also check `.sh` scripts. **Read the code** to understand what each experiment does — folder
names are opaque, scripts tell you everything.

### Media Selection — AGGRESSIVE

Collect FAR more images than you think you need. This is the most important discovery step.

1. Read experiment scripts for `plt.savefig(...)`, `Image.save(...)`, `cv2.imwrite(...)` calls
2. Look for naming patterns: `baseline.*`, `best_*.*`, `comparison.*`, `grid.*`, `eval*.*`
3. Also look for videos: `.mp4`, `.avi`, `.mov` — the converter embeds them as playable media
4. For comparison experiments: collect ALL images across ALL prompts/seeds
5. Grid sizing: 1 image → `cols-2`, 2 → `cols-2`, 3 → `cols-3`, 4 → `cols-4`

### Build Timeline

Cross-reference git commits ↔ output folders ↔ scripts. Build:
```
DATE | EXPERIMENT_NAME | SCRIPT | OUTPUT_FOLDER | KEY_RESULT | IMAGES
```

---

## Phase 2.5: Diagram Planning

For slides explaining concepts, pipelines, or architectures — create diagrams.

- Write as clean HTML/CSS, render to PNG with the diagram renderer:
  ```bash
  # One-time setup: cd /tmp && npm install puppeteer
  node ${CLAUDE_SKILL_DIR}/render_diagram.js input.html output.png [--width 1200] [--scale 2]
  ```
- Read the rendered PNG to verify readability before embedding.
- **Do NOT use matplotlib for diagrams** — only for actual data plots. HTML/CSS diagrams are
  far more readable in presentations.
- Save HTML files in the presentation directory for reuse.

---

## Phase 3: Organize Experiments into Slides

Order slides **chronologically** — the audience follows the story of discovery.

### Visual Budget Rule

Every slide in the outline must have one of: `[IMG]`, `[DIAGRAM]`, `[TABLE]`, `[DATASET]`.
If a slide has none, merge it into an adjacent slide or add a visual.

### Key Rules

- **Group** variations of the same idea into one slide with a comparison table
- **Filter** debug scripts, typos, one-off tests
- **Success/failure galleries**: minimum 5 success + 5 failure slides showing `cols-4` grids
  of baseline | method variants. Pick diverse examples — don't repeat the same prompt.
  Annotate failures: "(no change)", "(worse)", "(baseline better)".

### Per Slide

Each experiment slide contains:
1. What was done (factual description from script/commit)
2. What the result was (metrics from logs/files)
3. Visual evidence (images from output folder)

---

## Phase 4: Script Generation & User Review

Generate a structured outline:

```
SLIDE SCRIPT
============

Slide 1: Title
  Type: Title (lead)
  Heading: [Project Name — Weekly Update]
  Subtitle: [Date range, N experiments]
  Chips: [N slides], [date range], [key topics]
  Visual: [HERO_IMG]

Slide 2: [Experiment Name]
  Type: Content
  Heading: [What was done: key metric]
  Bullets:
    - [Configuration detail]
    - [Result metric]
  Visual: [IMG] path/to/image.png | [DIAGRAM] pipeline | [TABLE] | [DATASET]
  Grid: cols-[2/3/4]
```

Every slide MUST have a Visual field. Flag any slide without one.

### Review Mode

Use `AskUserQuestion`:
- header: "Review mode"
- question: "How would you like to review?"
- options: "Show each slide" (approve one at a time), "Show all slides" (feedback at once), "Skip review"

For per-slide review, use `AskUserQuestion` per slide with options: "Approve", "Edit", "Remove".

---

## Phase 5: Generate Slide Markdown

### Setup

```bash
mkdir -p presentation/YYYY_MM_DD
cp ${CLAUDE_SKILL_DIR}/theme.css presentation/YYYY_MM_DD/
cp ${CLAUDE_SKILL_DIR}/backgrounds/CHOSEN_BG.png presentation/YYYY_MM_DD/slide_bg.png
```

### Write Markdown

Write to `presentation/YYYY_MM_DD/slides.md`.

**Use ONLY elements from [slide_reference.md](slide_reference.md).** The PPTX converter only
understands those specific HTML elements.

**File header:**
```markdown
---
theme: notebook-status
paginate: true
size: 16:9
html: true
---
```

**Slide separator:** `---` on its own line.

### Style Rules

**Element order (strict, top to bottom):** heading → bullets (max 3, prefer 2) → table → images (always last).

**Banned elements on content slides:** chips, split layout, arch-box, stat cards, eyebrow,
decision card, timeline. Chips are ONLY allowed on the title (lead) slide.

**Do NOT generate:** next steps slides, takeaway slides, or any slide requiring editorial
interpretation.

**Headings:** factual label of experiment + result. "ResNet-50 on ImageNet: 76.1% Top-1"
not "ResNet-50 Is the Clear Winner".

**Bullets:** facts only. Max 3 per slide (prefer 2 — more space for images). Keep short.

**Table slides:** NO bullets. One context line above the table instead. Max 5 rows.

**Formatting:** `**bold**` for key numbers and method names. `` `code` `` for technical identifiers.

**Image captions:** terse identifiers, not sentences. Use `<strong>` for scores.

**Image paths:** relative to project root. Converter resolves via `--base-dir`.

**Title slide hero image:** The title slide can include a `cols-2` image grid below the chips.

**One visual concept per slide** — never mix grid types or have multiple unrelated sections.

**Image-to-claim consistency:** If a slide mentions a specific example, the images on that
slide MUST show that exact example. Verify image filenames match the described content.

**When uncertain about an experiment's purpose**, present observable facts and let the user
interpret. Do NOT guess intent.

---

## Phase 6: Convert to PPTX

```bash
python ${CLAUDE_SKILL_DIR}/md_to_pptx.py \
  --input presentation/YYYY_MM_DD/slides.md \
  --output presentation/YYYY_MM_DD/slides.pptx \
  --bg-image presentation/YYYY_MM_DD/slide_bg.png \
  --theme light \
  --base-dir .
```

Use `--theme dark` for dark background. Use `--theme light` for light and warm.

If `python-pptx` is missing: check conda/mamba environments, CLAUDE.md, or ask the user.

### Report

```
Presentation generated!

  Markdown: presentation/YYYY_MM_DD/slides.md
  PPTX:     presentation/YYYY_MM_DD/slides.pptx
  Slides:   [count]

Open in PowerPoint or LibreOffice Impress to edit further.
```

---

## Error Handling

- **No experiments found**: Suggest expanding date range
- **No images**: Generate text-only slides, note which could benefit from images
- **Missing python-pptx**: Report error, still deliver markdown
- **Background image missing**: Warn but continue — slides will have white background
- **Git not available**: Fall back to file modification times
