---
name: wlilo-design-system
description: "Use when you need the WLILO look (White Leather + Industrial Luxury Obsidian) across HTML, SVG, and jsgui3. Covers token schema, palette, and how to write back design learnings so other agents reuse them. Triggers: wlilo, white leather, industrial luxury, obsidian, design system, palette, theme tokens, diagram styling."
---

# Skill: WLILO Design System (White Leather + Industrial Luxury Obsidian)

## WLILO acronym

WLILO = **White Leather + Industrial Luxury Obsidian**.

## Scope

Use this Skill to:
- Apply WLILO consistently across **HTML/CSS**, **inline/build-time SVG**, and **jsgui3** controls.
- Convert “make it feel WLILO” into a small, repeatable **token set**.
- Improve repo memory: when you learn a reusable design rule, **write it back** (Skills/Patterns/Lessons).

Out of scope:
- Pixel-perfect design reviews (ask for screenshots / run capture scripts when needed)
- Large rebrands (create a dedicated design session)

## Inputs

- Target surface: `html`, `svg`, `jsgui3` (one or more)
- Embedding mode for SVG: `file/img` (build-time variants) vs `inline` (CSS variables possible)
- Constraints: contrast/readability, collision-free diagrams, performance (control counts)

## Procedure

### 0) Memory load + user-visible feedback (required)

1. Read:
   - `docs/guides/WLILO_STYLE_GUIDE.md`
2. If the task is SVG heavy, also read:
   - `docs/agi/skills/svg-theme-system/SKILL.md`
   - `docs/agi/skills/svg-collisions/SKILL.md`

Then emit a 1–2 line summary so the user can see what you loaded:
- `🧠 Memory pull (for this task) — Skills=wlilo-design-system, svg-theme-system | Sessions=<n> hits | Guides=WLILO_STYLE_GUIDE | I/O≈<in>→<out>`
- `Back to the task: <task description>`

### 1) Use a small token schema (don’t freestyle colors)

Recommended tokens (minimum viable):
- `--wlilo-bg` (leather)
- `--wlilo-panel` (obsidian)
- `--wlilo-border` (panel border)
- `--wlilo-text` / `--wlilo-text-muted`
- `--wlilo-accent-gold`
- `--wlilo-accent-blue` (optional CTA)

Reference palette values live in `docs/guides/WLILO_STYLE_GUIDE.md`.

### 2) Apply tokens per surface

**HTML/CSS (recommended default)**
- Define tokens in `:root` (or a theme scope class).
- Apply WLILO via semantic classes (panels, headers, separators) rather than per-element inline styles.

**SVG**
- If SVG is used via `<img>` / markdown: prefer **build-time variants** (one SVG per theme).
- If SVG is inlined: define CSS variables inside `<defs><style>` and reference via `fill="var(--wlilo-...)"`.

**jsgui3**
- Prefer classes + CSS over inline styles.
- Keep controls lean (avoid rendering 1000s of micro-controls for purely decorative chrome).

### 3) Validate

- SVG diagrams: `node tools/dev/svg-collisions.js <file> --strict`
- If UI code changed: run the smallest relevant `checks/*.check.js` and a focused Jest suite.

### 4) Write back (how Skills “get better”)

Skills don’t auto-improve; agents make them better by updating docs.

After finishing a WLILO-related task:
- If you discovered a reusable rule, append a short entry to:
  - `docs/agi/PATTERNS.md` (preferred) or `docs/agi/LESSONS.md`
- If you discovered a repeatable workflow, update this Skill (tight + SOP-focused).
- Capture evidence commands in the active session’s `WORKING_NOTES.md`.

## References

- WLILO style guide: `docs/guides/WLILO_STYLE_GUIDE.md`
- SVG theming: `docs/agi/skills/svg-theme-system/SKILL.md`
- SVG validation: `docs/agi/skills/svg-collisions/SKILL.md`
