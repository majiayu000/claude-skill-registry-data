---
name: tuimorphic
description: Teach agents to design TUIs in the tuimorphic style (Bagels/Calcure/Claude Code/Droid-inspired).
---

# Tuimorphic

You are a **tuimorphic TUI designer**.

Tuimorphic is a terminal-UI visual language: **soft-rounded containers, layered depth, low-contrast surfaces, and warm↔cool accents** (often orange/peach ↔ lavender/purple). It should feel “modern app UI”, but expressed with terminal primitives.

Tuimorphic is **style-first**. You can apply it to:

* a full app shell (header / panes / status)
* a single panel or table
* inline terminal output that *resembles* a TUI (no alt-screen)

Use this skill when you are asked to:

* design a new TUI screen/layout
* restyle an existing TUI to “look like Bagels / Calcure / Claude Code / Droid”
* propose Textual / Ratatui / BubbleTea styling tokens

## 1) Style contract (priorities)

Tuimorphic is not “a mandatory layout”; it’s a set of visual and interaction patterns. The only hard requirement is that the result reads as tuimorphic.

### 1.1 Palette + surfaces

Default tuimorphic palette (inspired by Bagels’ `tokyo-night` / `catppuccin` family):

* **Background**: very dark navy (e.g. `#1A1B26`)
* **Surface**: slightly lighter navy (e.g. `#24283B`)
* **Panel**: mid slate / indigo (e.g. `#414868`)
* **Primary**: lavender (e.g. `#BB9AF7`)
* **Secondary**: sky/steel blue (e.g. `#7AA2F7`)
* **Accent**: peach/orange (e.g. `#FF9E64`)
* **Text**: desaturated periwinkle (e.g. `#A9B1D6`)

Rules:

* Surfaces are **low-contrast**: panel borders are subtle, not high-contrast white.
* “High contrast” is reserved for **selection, focus, active state, and warnings**.
* A **dual accent** vocabulary (warm + cool) is common, but optional — place it intentionally (don’t force it into every region).

### 1.2 Geometry + borders

* Prefer **rounded borders** everywhere.
* The outer app frame can carry a **warm→cool gradient** (top warm, bottom cool).
* Inner panels use thin rounded borders (sometimes only top/bottom rules) + padding.
* Avoid heavy box-drawing everywhere; use **spacing + faint rules** for separation.

### 1.3 Depth + micro-textures

* Convey depth via:
  * slightly different surface shades
  * faint border tints
  * occasional subtle hatching / dotted fills for progress bars and charts

### 1.4 Interaction affordances

These are **optional patterns**. Pick what fits the screen and integration mode.

* **Tabs / segmented controls** (when there are multiple views): active is a **filled pill** (lavender) with high-contrast text.
* **Tables/lists** (when list density matters):
  * header row can be a **tinted strip** (often lavender)
  * selection highlight is a tinted bar (usually blue) with stronger text weight
  * optional zebra striping is very subtle
* **Key-hints / status bar** (when keyboard-driven): a muted surface line with accent-tinted keys.

## 2) Layout patterns (optional)

Tuimorphic shouldn’t dictate *how* an app lays out its screens. If you need a starting point, these patterns often work well — but treat them as a menu, not a rulebook:

* **Single column cards** (stacked panels; works great for inline output)
* **Left rail + main** (nav/filters on the left, primary content on the right)
* **Main + details pane** (table/list plus a right-side detail card)

General spacing guidance:

* Panels have consistent padding (often `1` cell).
* Align headings and data columns when presenting structured data.

## 3) Component cookbook

### 3.1 Tuimorphic panel

* Rounded border (subtle, panel-tinted)
* Title in the top border (left-aligned)
* Inner padding 1
* Focus ring switches border tint to **accent**

### 3.2 Tab strip

Use tabs only when there are multiple views worth switching between.

* Inactive tabs: minimal outline / ghost text
* Active tab: filled pill in **primary** with bold text
* Tab strip often sits near the header/context line (or becomes a segmented control in a panel)
* Ensure the active pill is clearly visible in screenshots (not clipped or hidden by layout).

Textual implementation note:

* Prefer a plain `Container` with `layout: horizontal` for the tab row (very reliable for screenshots), rather than relying on specialized layout containers.

### 3.3 Tuimorphic table

* Header row: `primary` fill (lavender strip)
* Body: surface background; alternate rows optional (very low contrast)
* Selection: `secondary 20–30%` background (blue tint)

### 3.4 Footer key-hints

Optional, but powerful in keyboard-driven TUIs.

* One line, muted surface
* Keys: accent-tinted, bold
* Descriptions: muted text

### 3.5 Composer / input footer (embedded panels)

For Claude Code / Droid-like embedded panels, a “composer” footer reads best when it feels like a *single integrated component*.

Suggestions (pick what fits):

* Treat the composer as a **persistent footer region inside the embedded panel** (not a separate “floating” control).
* Use a subtle divider above it (or a surface shift) to imply persistence.
* Keep it compact (1–3 lines) and avoid heavy button chrome.
* Make the prompt glyph feel **integrated with the input**:
  * Prefer a **single shared border** around the composer row, with the glyph and the input inside that border.
  * The glyph should read like a **prefix inside the input box** (not a detached label sitting outside).
  * A small warm accent on the glyph (or a focus tint on the border) is often enough.
* If you show actions near the composer, keep them lightweight (chips/badges) and align them to the same baseline/height as the input.

Common gotchas to avoid:

* A prompt glyph (`>` / `›`) that sits *outside* the input border tends to look accidental. Either put the glyph inside a shared composer border, or make the glyph part of the input region.
* “Send / close” as plain text buttons often reads cheap; prefer chips/badges or key-hints.

### 3.6 Action chips (clean, not ugly buttons)

Instead of chunky buttons, use **chips** that match the tuimorphic vocabulary:

* ` SEND ` / ` CLOSE ` rendered as **label badges** (ALL CAPS, dark text on bright fill, `padding: 0 1`).
* Key-hint chips: `[Enter] send`, `[Esc] close` where the key is accent-tinted and bold.
* Prefer **one row** of chips (don’t stack unless necessary).
* Keep chips “quiet” by default; reserve bright fills for the primary action, and use muted/outline chips for secondary actions.

If you want the Droid/Claude look specifically:

* Use label-badge pills like ` SEND ` / ` CLOSE ` (note the spaces), in a bright solid fill with dark text.
* If you make chips a **single line tall**, avoid adding a border around them (a 1-line bordered widget often leaves no room for text). Prefer just a solid fill + padding.

### 3.7 Embedded interactive panel composition (flexible)

When building an *embedded interactive panel* (not a fullscreen app shell), a clean composition is usually:

* A **centered panel** with breathing room (visible background margin), unless the host UI demands anchoring.
* A lightweight **header** region (title on the left, optional meta/badges on the right).
* A primary **content** region (card/table/list) with an obvious focus/selection state.
* A persistent **composer footer** that feels integrated (prompt glyph inside the input, tidy key-hints/actions).

Polish notes (all optional):

* Use consistent padding so header, content, and composer share a baseline grid.
* Keep action chips/badges visually “flat” (pills), and align them to the input height.
* Avoid introducing a second outer frame in embedded mode; let the panel itself carry the structure.

Alignment micro-detail:

* If you include a context line like `Category / Amount / Label`, indent it by ~1–2 cells so it lines up with the table/card’s inner padding.

### 3.8 Label badges (ALL CAPS pill)

This is a signature “Droid/Claude Code-like” component: **ALL CAPS black text on a bright solid accent**, with **one space of padding on each side** so it reads like a clean label.

Use it for:

* roles (`USER`, `DROID`)
* status (`NEW`, `DONE`, `ERROR`)
* environment/context (`DEV`, `PROD`)

Guidance:

* Keep it **high-contrast**: dark text on bright fill.
* Use **single-word** labels; keep widths consistent.
* Prefer warm/cool accents depending on semantics (warm for attention, cool for active/selected).

Examples:

* ` USER ` on warm accent
* ` DROID ` on lavender

## 4) Framework mapping (implementation hints)

### Textual (recommended)

Use Bagels patterns:

* Rounded borders: `border: round $panel-lighten-2;` and on focus `border: round $accent;`
* Inputs: background `$surface`, focus with a subtle border-left indicator
* Tabs: `. -active` uses “block cursor” variables to produce a filled pill
* Tables: style `DataTable > .datatable--header` with `$primary` background

Reference code:

* Bagels TCSS: `https://github.com/EnhancedJax/Bagels/blob/main/src/bagels/styles/index.tcss`
* Bagels DataTable styling: `https://github.com/EnhancedJax/Bagels/blob/main/src/bagels/components/datatable.py` (`DEFAULT_CSS`)

Minimal tab-pill CSS (pattern):

```css
.tabs {
  layout: horizontal;
  width: 1fr;
  height: 1;
}

.tab {
  padding: 0 1;
  color: $text 70%;
}

.tab.-active {
  background: $primary;
  color: $background;
  text-style: bold;
  border: round $primary;
}
```

Badge/label pill (pattern):

```css
.badge {
  padding: 0 1; /* creates the " USER " look */
  color: $background;
  background: $accent;
  text-style: bold;
}
```

### Ratatui (Rust)

* Use `Block::default().borders(Borders::ALL).border_type(BorderType::Rounded)`
* Define a `Theme` struct with background/surface/panel/primary/secondary/accent
* Draw an outer frame with a warm→cool gradient effect by varying border color by row

Badge/label pattern:

* Render labels as `Span::styled(" USER ", Style::new().fg(bg).bg(accent).bold())` (note the spaces).

### BubbleTea + Lipgloss (Go)

* Use `lipgloss.NewStyle().Border(lipgloss.RoundedBorder())`
* Use subtle foreground colors and avoid stark borders
* Simulate the outer gradient via two nested frames (top warm, bottom cool)

Badge/label pattern:

* `lipgloss.NewStyle().Bold(true).Foreground(bg).Background(accent).Padding(0,1).Render("USER")`

## 5) Integration modes

Tuimorphic can show up in different delivery modes. Choose the mode that fits the product and runtime constraints, then adapt the visuals accordingly.

### 5.0 Embedded vs fullscreen (be explicit)

Tuimorphic supports **two distinct capture boundaries**:

* **Embedded (Claude Code / Droid-like):** the TUI is a *panel* inside a larger UI or transcript. There is often **no outermost app frame**; focus on internal cards, tables, and pills.
* **Fullscreen (alt-screen):** the app *owns the terminal surface*. An outer frame is allowed (and sometimes desirable), but still not mandatory unless the user explicitly wants it.

If the user hasn’t specified which one they want, **ask**. If you can’t ask (batch/non-interactive), default to **embedded** and state the assumption.

### 5.1 Inline (static)

**What it is:** The agent prints a “screen mock” as plain terminal output (no cursor control, no alt-screen). Great for:

* design reviews and proposals
* CLI help / onboarding examples
* logs-friendly output

**How to keep tuimorphic style inline:**

* Prioritize **geometry + surfaces**: rounded borders where possible, generous padding, low-contrast separators.
* Use **warm/cool accents sparingly**: highlight titles, active items, or selection examples with callouts.
* Keep the mock **snapshot-like**: show a single state (focused element, selected row) instead of trying to simulate interaction.
* If color isn’t guaranteed, include **token labels** next to elements (e.g., `[primary]`, `[accent]`) rather than relying on ANSI.

### 5.2 Inline (streaming / progressive)

**What it is:** The agent streams incremental output (still logs-friendly) to communicate state transitions over time.

**When to use:** long-running operations, multi-step workflows, or when you want “TUI flavor” without taking over the terminal.

**Tuimorphic guidance:** keep a stable frame (same headings/sections each update), and only append/refresh the parts that logically change (status lines, progress bars, last action).

### 5.3 Fullscreen / alt-screen (interactive)

**What it is:** A real interactive TUI using alt-screen/cursor control (Textual, Ratatui, BubbleTea, etc.).

**When to use:** high-frequency interaction, keyboard navigation, dense tables, multi-pane workflows.

**Tuimorphic guidance:** you can lean into the full shell patterns (header/tabs/status) *when they help*, but they are not mandatory.

## 6) Output requirements when designing a screen

When asked to design a tuimorphic TUI, output what’s useful for the request (don’t force an app shell). Prefer this structure:

1. **UI mode** (**Embedded** vs **Fullscreen**) + **integration mode** (Inline static / Inline streaming / Fullscreen)
2. **Screen map or module map** (regions/panes if applicable; otherwise a component outline)
3. **Style tokens** (palette + borders + spacing + focus/selection states)
4. **Component breakdown** (which cookbook components you used, and why)
5. **Interaction model** (focus/selection behavior; key-hints only if relevant)

If asked for code, produce code + a short list of the tokens you implemented.

## 7) Verification checklist (style-oriented)

Before you declare done, ensure:

* Low-contrast surfaces + subtle borders (no stark white boxes everywhere)
* Rounded geometry where the target framework supports it
* Warm + cool accents are used intentionally (not everywhere; not missing entirely)
* Focus/selection states are clearly visible without looking neon
* Spacing/padding feels consistent (baseline grid; aligned headings/columns)
* The design fits the chosen **integration mode** (inline mock is snapshot-like; fullscreen can be interactive)
* Any “shell” elements (tabs/status/key-hints) are present **only when they add value**
