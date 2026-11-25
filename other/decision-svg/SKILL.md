---
name: decision-svg
description: >
  Extract architectural decisions from an Obsidian note and render them as an
  inline SVG diagram — black background, white boxes and arrows, chronological
  top-down flow. Each box shows what was decided, what was rejected, and the
  meeting where the decision was locked. The SVG is embedded directly in the
  host note inside an [!info] callout: no external files, no plugins required.
  Use when asked to "create a decision diagram", "draw decisions as SVG",
  "make a decision map from this note", "visualise decisions inline", or
  invokes /decision-svg.
---

# Decision SVG Skill

Reads a markdown note, extracts architectural (or any domain) decisions,
and generates a self-contained inline SVG that lives 100% inside the host
note. No Excalidraw file, no Mermaid engine, no image attachment.

---

## When to Use

- User asks to "visualise decisions" in a note.
- User asks for a "decision map", "decision diagram", or "decision flow".
- User wants a diagram that is portable — no plugin required to view.
- Mermaid is producing boxes that are too narrow for the content.
- The note already has a `### Decision Map` section that needs refreshing.

---

## Output Contract

| Property | Value |
|---|---|
| Location | Inline in the host note, replacing or creating `### Decision Map` |
| Format | Raw `<svg>` HTML block inside an Obsidian `> [!info]` callout |
| Background | `#000000` (black) |
| Draw colour | `#ffffff` (white) — borders, text, arrows |
| Canvas width | `viewBox="0 0 1600 {H}"` with `width="100%"` — scales to container |
| Box width | 1500 px (`x=50` to `x=1550`) |
| Font | `Arial, sans-serif` embedded via `style` attribute |
| Flow direction | Top to bottom, chronological by decision date |

---

## Step 1 — Read the note

Read the full content of the target note. Identify:

1. **Decision items** — anything that records a resolved choice. Look for:
   - Sections titled `Decision`, `ADR`, `Decided`, `Resolved`, `Key Decisions`
   - Bullet points with `✓/YES/approved` vs `✗/NO/rejected` framing
   - Meeting summaries containing phrases like "confirmed", "agreed", "locked"
   - JIRA or Confluence links that describe approved work items

2. **Dates** — when each decision was made. Extract from:
   - Meeting backlinks (`[[2026.05.14.ArchitectureBacklogRefinement.Summary|...]]`)
   - Task completion dates (`✅ 2026-04-23`)
   - Explicit date ranges in prose

3. **Meeting references** — which meetings produced or confirmed each decision.
   Keep the display name short: `Apr 9 · Architecture Backlog Refinement`.

4. **A deadline or forcing function** — if the note has a hard date or milestone
   that all decisions feed into, capture it as the final box.

If the note has a `### Related Meetings` section or a narrative thread, use it
to confirm the chronological order.

---

## Step 2 — Structure the decisions

Build a Python list of sections in **chronological order** (earliest first):

```python
sections = [
    ("PROB", [                          # id, list of (text, bold, center)
        ("PROBLEM", True, False),       # (text, is_header, is_centered)
        ("One-line description of the problem being solved", False, False),
        ("Second problem dimension if needed", False, False),
    ]),
    ("D1", [
        ("DECISION 1 — NAME  ·  Date", True, False),   # header: bold, left
        ("NO: rejected option", False, False),
        ("YES: chosen option", False, False),
        ("    detail line indented with spaces", False, False),
        ("    another detail line", False, False),
        ("Decided: Meeting Name  /  Meeting Name 2", False, False),  # last line
    ]),
    # ... one entry per decision, D2 through DN ...
    ("DL", [
        ("DEADLINE OR MILESTONE — Date", True, True),  # centered
        ("Description line", False, True),
        ("Second line", False, True),
    ]),
]
```

**Rules for structuring:**
- First section is always `PROB` — the problem the decisions solve.
- Last section is always `DL` — the hard deadline or forcing function.
  If no explicit deadline exists, use a "Current State" summary box instead.
- Decision sections are `D1` through `DN` in date order.
- Each decision section's last body line starts with `Decided:` and names the
  meeting(s) where it was locked.
- Indent continuation lines with 5 spaces so they visually group under the
  YES/NO line above them.
- Keep each line under ~100 characters. At font-size 17 in Arial, that is
  approximately the width of the 1420 px text area.

---

## Step 3 — Generate the SVG

Use this exact Python generator. Paste it into a bash block and run it.
Capture the output to a variable, then insert it into the note.

```python
# SVG layout constants
W       = 1600   # canvas width
BX      = 50     # box left x
BW      = 1500   # box width
TX      = 85     # text left x  (35 px padding from box left)
CX      = 800    # arrow / deadline-text centre x
GAP     = 50     # vertical gap between boxes (arrow space)
LH      = 26     # line height in px (dy between tspan elements)
PAD_TOP = 42     # rect top → first line baseline
PAD_BOT = 28     # last line baseline → rect bottom
H_HDR   = 19     # header font size
H_BODY  = 17     # body font size

def box_height(n_lines):
    """Exact height for a box with n_lines of text."""
    return PAD_TOP + n_lines * LH + PAD_BOT

# ── PASTE YOUR sections LIST HERE ──────────────────────────────────────────

sections = [
    # ... your extracted decisions ...
]

# ── GENERATOR (do not modify below this line) ───────────────────────────────

title_y = 15
y = title_y + 55   # first box starts below the title

box_positions = []
for sid, lines in sections:
    h = box_height(len(lines))
    if sid == "DL":
        h += 10    # extra breathing room on the deadline box
    box_positions.append((sid, y, h, lines))
    y += h + GAP
total_h = y - GAP + 20

out = []
out.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'viewBox="0 0 {W} {total_h}" width="100%" '
    f'style="display:block;font-family:Arial,sans-serif">'
)
out.append(f'  <rect width="{W}" height="{total_h}" fill="#000"/>')
out.append(
    f'  <text x="{CX}" y="{title_y + 38}" fill="white" '
    f'font-size="22" font-weight="bold" text-anchor="middle">'
    f'DECISIONS — (chronological)</text>'   # ← customise title here
)

for i, (sid, by, bh, lines) in enumerate(box_positions):
    # Arrow from previous box
    if i > 0:
        prev_bottom = box_positions[i-1][1] + box_positions[i-1][2]
        ay1 = prev_bottom + 5
        ay2 = by - 8
        out.append(
            f'  <line x1="{CX}" y1="{ay1}" x2="{CX}" y2="{ay2}" '
            f'stroke="white" stroke-width="2"/>'
        )
        out.append(
            f'  <polygon points="{CX-7},{ay2} {CX+7},{ay2} {CX},{by}" '
            f'fill="white"/>'
        )

    sw = 3 if sid == "DL" else 2
    out.append(
        f'  <rect x="{BX}" y="{by}" width="{BW}" height="{bh}" '
        f'fill="none" stroke="white" stroke-width="{sw}" rx="10"/>'
    )

    first_y = by + PAD_TOP
    out.append('  <text fill="white">')
    for li, (txt, bold, center) in enumerate(lines):
        anchor = 'middle' if center else 'start'
        tx     = CX if center else TX
        fs     = H_HDR if bold else H_BODY
        fw     = 'bold' if bold else 'normal'
        if li == 0:
            out.append(
                f'    <tspan x="{tx}" y="{first_y}" '
                f'font-size="{fs}" font-weight="{fw}" '
                f'text-anchor="{anchor}">{txt}</tspan>'
            )
        else:
            out.append(
                f'    <tspan x="{tx}" dy="{LH}" '
                f'font-size="{fs}" font-weight="{fw}" '
                f'text-anchor="{anchor}">{txt}</tspan>'
            )
    out.append('  </text>')

out.append('</svg>')
print('\n'.join(out))
```

Run the script:

```bash
python3 /tmp/gen_decisions.py > /tmp/decisions.svg
```

Verify it is valid XML and check the total height:

```bash
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('/tmp/decisions.svg')
root = tree.getroot()
vb = root.get('viewBox', '')
print(f'Valid XML ✓   viewBox: {vb}')
rects  = [e for e in root.iter('{http://www.w3.org/2000/svg}rect')]
arrows = [e for e in root.iter('{http://www.w3.org/2000/svg}line')]
print(f'Boxes: {len(rects)-1}   Arrows: {len(arrows)}')   # -1 for background rect
"
```

---

## Step 4 — Embed in the note

Find or create the `### Decision Map` section in the host note.

Replace whatever is currently inside it with this structure:

```markdown
### Decision Map

> [!info] {Topic} — Decision Map
> {One sentence describing what decisions the diagram covers and the date range.}

{SVG BLOCK — paste the full <svg>...</svg> output here, NOT in a code fence}

```

**Critical:** the SVG must be raw HTML, not inside a fenced code block.
Obsidian renders raw HTML in reading mode and live preview.
A fenced code block will show the raw XML text instead.

The `[!info]` callout provides the human-readable description.
The SVG sits immediately below the callout (outside the `>` prefix) so
Obsidian renders it at full width without the callout's left border clipping it.

---

## Tuning Guide

### Font too small?

Increase `H_HDR` and `H_BODY`. Also increase `LH` by the same proportion
and re-run the generator. `box_height()` will automatically grow all boxes.

| Use case | H_HDR | H_BODY | LH |
|---|---|---|---|
| Dense reference diagram | 17 | 15 | 22 |
| Default (balanced) | 19 | 17 | 26 |
| Presentation / large monitor | 22 | 20 | 30 |

### Boxes too narrow?

Increase `W` and `BW` together. Keep `BX = (W - BW) / 2` so boxes stay centred.
Update `CX = W / 2` for arrows and centred text.

| Setting | W | BW | BX | CX |
|---|---|---|---|---|
| Default | 1600 | 1500 | 50 | 800 |
| Double-wide | 2400 | 2300 | 50 | 1200 |
| Ultra-wide | 3200 | 3100 | 50 | 1600 |

### Lines too long to fit?

Split long lines in the `sections` list. Each element in the list is one
rendered line. Indent continuation lines manually with spaces:

```python
("YES: TypeORM direct queries against shared Aurora cluster", False, False),
("     cross-schema SQL JOINs · 25–48x latency", False, False),
```

### No hard deadline?

Replace the `DL` section with a `STATUS` section showing current state:

```python
("STATUS", [
    ("CURRENT STATE  ·  {Date}", True, True),
    ("In progress: {item}", False, True),
    ("Blocked on: {item}", False, True),
]),
```

---

## Line Length Guide

At `font-size=17, font-family=Arial`, one character ≈ 9.5 px average.
The text area is `BW - (TX - BX) - 35 = 1500 - 35 - 35 = 1430 px`.

Maximum safe line length: **~150 characters**.

Lines over 150 characters will overflow the box. When in doubt, split.

---

## Reference Implementation

The canonical example is in:

```
00.Tasks/Topics/NewGen/Performance/_Database.Refactor.md
```

Section `### Decision Map`. It covers 6 architectural decisions (Mar–Jun 2026)
for the Aurora cluster consolidation initiative, generated from meeting
summaries in `02.Meetings/summaries/`.

The Python generator that produced it is the exact script in Step 3.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| SVG inside a fenced code block | Remove the triple-backtick wrapper — raw HTML only |
| `dy` accumulates across `<text>` elements | Each `<text>` element resets. One `<text>` per box. |
| Chronological order wrong | Sort `sections` by the date in each decision's header line |
| Text baseline clipped at top | Increase `PAD_TOP`; the first `y` must exceed the rect's `y` |
| Arrow tip touching wrong box | Arrow `ay2 = next_box_y - 8`; polygon tip `= next_box_y` |
| Center-aligned tspan ignores `x` | Set `x` explicitly on every centered `<tspan>`, not just the parent `<text>` |
