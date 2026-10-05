---
name: excalidraw-diagram
description: Create Excalidraw diagram JSON files that make visual arguments. Use when the user wants to create, draw, sketch, or visualize any kind of diagram — flowcharts, system diagrams, architecture diagrams, technical diagrams, data flow diagrams, sequence diagrams, entity relationship diagrams, state machines, mind maps, org charts, network topologies, pipeline diagrams, decision trees, process flows, concept maps, wireframes, or any visual explanation of workflows, systems, relationships, or concepts.
---

# Excalidraw Diagram Creator

Generate `.excalidraw` JSON files that **argue visually**, not just display information.

**Setup:** If the user asks you to set up this skill (renderer, dependencies, etc.), see `README.md` for instructions.

## Customization

**All colors and brand-specific styles live in one file:** `references/color-palette.md`. Read it before generating any diagram and use it as the single source of truth for all color choices.

To produce diagrams in your own brand style, edit `color-palette.md`. Everything else in this file is universal design methodology and Excalidraw best practices.

---

## Core Philosophy

**Diagrams should ARGUE, not DISPLAY.**

A diagram is a visual argument that shows relationships, causality, and flow that words alone cannot express. The shape should BE the meaning.

**The Isomorphism Test**: If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test**: Could someone learn something concrete from this diagram, or does it just label boxes? A good diagram teaches — it shows actual formats, real event names, concrete examples.

---

## Depth Assessment (Do This First)

Before designing, determine what level of detail this diagram needs:

**Simple/Conceptual** — Use abstract shapes when explaining a mental model, the audience does not need technical specifics, or the concept IS the abstraction.

**Comprehensive/Technical** — Use concrete examples when diagramming a real system, the diagram will teach or explain, the audience needs to understand what things look like, or you are showing how multiple technologies integrate. For technical diagrams, you MUST include evidence artifacts (see below).

---

## Research Mandate (For Technical Diagrams)

**Before drawing anything technical, research the actual specifications.**

If you are diagramming a protocol, API, or framework:
1. Look up the actual JSON/data formats
2. Find the real event names, method names, or API endpoints
3. Understand how the pieces actually connect
4. Use real terminology, not generic placeholders

Bad: "Protocol" -> "Frontend"
Good: "AG-UI streams events (RUN_STARTED, STATE_DELTA)" -> "CopilotKit renders via createA2UIMessageRenderer()"

---

## Evidence Artifacts

Evidence artifacts are concrete examples that prove your diagram is accurate and help viewers learn. Include them in technical diagrams.

| Artifact Type | When to Use | How to Render |
|---------------|-------------|---------------|
| **Code snippets** | APIs, integrations | Dark rectangle + syntax-colored text (see color palette) |
| **Data/JSON examples** | Data formats, schemas | Dark rectangle + colored text |
| **Event/step sequences** | Protocols, workflows | Timeline pattern (line + dots + labels) |
| **UI mockups** | Showing actual output | Nested rectangles mimicking real UI |
| **Real input content** | Showing what goes IN | Rectangle with sample content visible |
| **API/method names** | Real function calls | Use actual names from docs, not placeholders |

The key principle: **show what things actually look like**, not just what they are called.

---

## Multi-Zoom Architecture

Comprehensive diagrams operate at multiple zoom levels simultaneously — like a map showing both country borders and street names.

**Level 1: Summary Flow** — Simplified overview of the full pipeline. Often at the top or bottom.

**Level 2: Section Boundaries** — Labeled regions grouping related components. Create visual "rooms" (e.g., Backend / Frontend, Setup / Execution / Cleanup).

**Level 3: Detail Inside Sections** — Evidence artifacts, code snippets, and concrete examples within each section. This is where educational value lives.

For comprehensive diagrams, aim to include all three levels.

| Bad (Displaying) | Good (Arguing) |
|------------------|----------------|
| 5 equal boxes with labels | Each concept has a shape mirroring its behavior |
| Card grid layout | Visual structure matches conceptual structure |
| Icons decorating text | Shapes that ARE the meaning |
| Everything in a box | Free-floating text with selective containers |

---

## Container vs. Free-Floating Text

**Not every piece of text needs a shape around it.** Default to free-floating text. Add containers only when they serve a purpose.

| Use a Container When... | Use Free-Floating Text When... |
|------------------------|-------------------------------|
| It is the focal point of a section | It is a label or description |
| Arrows need to connect to it | It describes something nearby |
| The shape carries meaning (decision diamond) | Typography alone creates hierarchy |
| It represents a distinct "thing" in the system | It is a title, subtitle, or annotation |

**The container test**: For each boxed element, ask "Would this work as free-floating text?" If yes, remove the container. Aim for <30% of text elements inside containers.

---

## Design Process (Do This BEFORE Generating JSON)

### Step 0: Assess Depth
Determine simple/conceptual vs. comprehensive/technical. If comprehensive, do research first.

### Step 1: Understand Deeply
For each concept, ask: What does it DO? What relationships exist? What is the core transformation? What would someone need to SEE to understand this?

### Step 2: Map Concepts to Patterns
Match each concept to the visual pattern that mirrors its behavior. See `references/visual-patterns.md` for the full pattern library and a concept-to-pattern quick reference table.

### Step 3: Ensure Variety
For multi-concept diagrams, each major concept must use a different visual pattern. No uniform cards or grids.

### Step 4: Sketch the Flow
Mentally trace how the eye moves through the diagram. There should be a clear visual story.

### Step 5: Generate JSON
Create the Excalidraw elements. For large diagrams, build section-by-section (see below).

### Step 6: Render & Validate (MANDATORY)
Run the render-view-fix loop until the diagram looks right. See the Render & Validate section below.

---

## Large / Comprehensive Diagram Strategy

**For comprehensive or technical diagrams, build the JSON one section at a time.** Do NOT generate the entire file in a single pass. Claude Code has a ~32,000 token output limit per response, and a comprehensive diagram easily exceeds that. Even for smaller diagrams, section-by-section produces better quality.

### The Section-by-Section Workflow

**Phase 1: Build each section**

1. **Create the base file** with the JSON wrapper (`type`, `version`, `appState`, `files`) and the first section of elements.
2. **Add one section per edit.** Each section gets its own dedicated pass — think carefully about layout, spacing, and connections to existing sections.
3. **Use descriptive string IDs** (e.g., `"trigger_rect"`, `"arrow_fan_left"`) so cross-section references are readable.
4. **Namespace seeds by section** (e.g., section 1 uses 100xxx, section 2 uses 200xxx) to avoid collisions.
5. **Update cross-section bindings** as you go. When a new element binds to an earlier one, edit the earlier element's `boundElements` array at the same time.

**Phase 2: Review the whole**

After all sections are in place, read through the complete JSON and check:
- Are cross-section arrows bound correctly on both ends?
- Is overall spacing balanced?
- Do all IDs and bindings reference elements that actually exist?

**Phase 3: Render & validate** — Run the render-view-fix loop.

### Section Planning

Plan sections around natural visual groupings. A typical split:
- **Section 1**: Entry point / trigger
- **Section 2**: First decision or routing
- **Section 3**: Main content (hero section — may be the largest)
- **Section 4-N**: Remaining phases, outputs

### What NOT to Do

- **Do not generate the entire diagram in one response.** You will hit the output token limit and produce truncated JSON.
- **Do not use a coding agent** to generate the JSON. The agent will lack context about this skill's rules.
- **Do not write a Python generator script.** The indirection makes debugging harder. Hand-crafted JSON with descriptive IDs is more maintainable.

---

## Shape Meaning

Choose shape based on what it represents — or use no shape at all:

| Concept Type | Shape | Why |
|--------------|-------|-----|
| Labels, descriptions, details | **none** (free-floating text) | Typography creates hierarchy |
| Section titles, annotations | **none** (free-floating text) | Font size/weight is enough |
| Markers on a timeline | small `ellipse` (10-20px) | Visual anchor, not container |
| Start, trigger, input | `ellipse` | Soft, origin-like |
| End, output, result | `ellipse` | Completion, destination |
| Decision, condition | `diamond` | Classic decision symbol |
| Process, action, step | `rectangle` | Contained action |
| Abstract state, context | overlapping `ellipse` | Fuzzy, cloud-like |
| Hierarchy node | lines + text (no boxes) | Structure through lines |

---

## Color as Meaning

Colors encode information, not decoration. Every color choice must come from `references/color-palette.md`.

**Key principles:**
- Each semantic purpose (start, end, decision, AI, error, etc.) has a specific fill/stroke pair
- Free-floating text uses color for hierarchy (titles, subtitles, details — each at a different level)
- Evidence artifacts use their own dark background + colored text scheme
- Always pair a darker stroke with a lighter fill for contrast

**Do not invent new colors.** If a concept does not fit an existing semantic category, use Primary/Neutral or Secondary.

---

## Modern Aesthetics

- **Roughness**: `roughness: 0` for clean/modern (default). `roughness: 1` for hand-drawn/informal.
- **Stroke width**: `1` for thin/elegant lines, `2` for standard shapes/arrows, `3` sparingly for emphasis.
- **Opacity**: Always `opacity: 100`. Use color, size, and stroke width for hierarchy instead of transparency.
- **Small markers**: Use 10-20px ellipses as timeline markers, bullet points, connection nodes, or visual anchors for free-floating text.

---

## Layout Principles

- **Hierarchy through scale**: Hero 300x150, Primary 180x90, Secondary 120x60, Small 60x40.
- **Whitespace = importance**: The most important element has the most empty space around it (200px+).
- **Flow direction**: Left-to-right or top-to-bottom for sequences, radial for hub-and-spoke.
- **Connections required**: Position alone does not show relationships. If A relates to B, there must be an arrow.

---

## Text Rules

**CRITICAL**: The JSON `text` property contains ONLY readable words.

```json
{
  "id": "myElement1",
  "text": "Start",
  "originalText": "Start"
}
```

Settings: `fontSize: 16`, `fontFamily: 3`, `textAlign: "center"`, `verticalAlign: "middle"`

---

## JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

## Element Templates

See `references/element-templates.md` for copy-paste JSON templates for each element type. Pull colors from `references/color-palette.md` based on each element's semantic purpose.

---

## Render & Validate (MANDATORY)

You cannot judge a diagram from JSON alone. After generating or editing the Excalidraw JSON, you MUST render it to PNG, view the image, and fix what you see — in a loop until it is right.

### How to Render

```bash
cd .claude/skills/excalidraw-diagram/references && uv run python render_excalidraw.py <path-to-file.excalidraw>
```

This outputs a PNG next to the `.excalidraw` file. Then use the **Read tool** on the PNG to view it.

### The Loop

**1. Render & View** — Run the render script, then Read the PNG.

**2. Audit against your original vision** — Compare the rendered result to what you designed. Ask:
- Does the visual structure match the conceptual structure you planned?
- Does each section use the intended pattern (fan-out, convergence, timeline, etc.)?
- Does the eye flow through the diagram in the designed order?
- Is the visual hierarchy correct — hero elements dominant, supporting elements smaller?
- For technical diagrams: are evidence artifacts readable and properly placed?

**3. Check for visual defects:**
- Text clipped by or overflowing its container
- Text or shapes overlapping other elements
- Arrows crossing through elements instead of routing around them
- Arrows landing on the wrong element or pointing into empty space
- Labels floating ambiguously (not clearly anchored to what they describe)
- Uneven spacing, unbalanced composition, text too small to read

**4. Fix** — Edit the JSON. Common fixes: widen containers for clipped text, adjust coordinates for spacing, add waypoints to arrow `points` arrays to route around elements, reposition labels closer to their subject.

**5. Re-render & re-view** — Run the render script again and Read the new PNG.

**6. Repeat** — Keep cycling until the diagram passes both the vision check and the defect check. Typically 2-4 iterations. Do not stop after one pass just because there are no critical bugs — if the composition could be better, improve it.

### When to Stop

The loop is done when:
- The rendered diagram matches the conceptual design from your planning steps
- No text is clipped, overlapping, or unreadable
- Arrows route cleanly and connect to the right elements
- Spacing is consistent and the composition is balanced
- You would be comfortable showing it to someone without caveats

### First-Time Setup
```bash
cd .claude/skills/excalidraw-diagram/references
uv sync
uv run playwright install chromium
```

---

## Quality Checklist

After completing the render-validate loop, run through `references/quality-checklist.md` for a final comprehensive check covering depth, evidence, conceptual integrity, container discipline, structural quality, technical correctness, and visual validation.
