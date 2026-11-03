---
name: minimalist-ui
description: "Use this skill whenever a user asks for a minimal, clean, simple, nerdy or terminal-inspired interface, monospace typography, ASCII, dashed borders, Gruvbox, Tokyo Night, Catppuccin, Nord, Rose Pine, Game of Life or another generative background, or says make it look good but not generic. Apply its textured-minimal aesthetic to any website or app. Skip it when the user specifies a different explicit style or brand system, or asks for conventional corporate or luxury design."
license: MIT
---

# Textured minimal

Few elements and little chrome, with each element carrying character. Keep content
clear and the interface useful; make restraint tactile rather than empty. This is
neither white-space-first corporate minimalism nor a terminal costume. Apply to any
real page or app: storefronts, docs, blogs, dashboards, forms, tools, community
pages, and personal sites among others. There is no default page structure.

## Scope and precedence

- Work only inside the current workspace and this skill's own folder. An empty
  workspace means build from `assets/starter.html`. If the user refers to a site
  not present in the workspace, ask them for its files.
- Preserve real content, routes, brand constraints, existing flows, and
  architecture. This skill decides look and feel; other applicable guidance may
  add non-style requirements such as real content, accessibility, and motion
  budgets.
- Teach decisions, not a page to clone. `assets/starter.html` is neutral
  placeholder content and a reference implementation of the output, not a required
  stack.
- Inspect the actual project before coding. Read its package manifest,
  configuration and source to identify the stack and styling system. Match its
  conventions; never add a framework, utility CSS system, or component library it
  does not already use.
- Before building, state the chosen composition archetype and dials together in one line:
  `ARCHETYPE: <name> / TEXTURE n / DENSITY n / MOTION n / VOICE nerd|neutral|professional`.
  Add `TYPE readable` when the body text is proportional. Choose one archetype per major page/view and never repeat an archetype within a project.

## Direction and dials

Set one focal point and one primary action per view. Choose composition around the
task, not a preset content sequence. Use monospace throughout (in the default `nerd` voice; see Voice and type), themed paper and
ink, one restrained accent, a strong dashed outer frame where it fits, dashed
accent underlines for section titles, `*` bullets, and muted `meta` lines. Give
buttons a dashed resting border and an inverted or subtly beveled hover. A
low-opacity cellular or generative canvas is optional; if present, show an
accessible pause control. A fixed footer bar can hold theme choice; floating
dashed utility controls are for a real, useful action. Add the opacity-plus-12px-
rise entrance once, and never make content depend on animation.

Dials run from 1 to 10; defaults are `TEXTURE 4 / DENSITY 5 / MOTION 3`. Texture
is visual ornament, density is content and control packing, motion is nonessential
movement. Pick values for the task and state them before implementation. Starting
points:

| Page type | Texture | Density | Motion |
| --- | ---: | ---: | ---: |
| Docs, articles, reading | 2 | 4 | 1 |
| Dashboards, data tools | 2 | 8 | 1 |
| Forms, checkout, settings | 3 | 5 | 1 |
| Storefronts, directories | 4 | 5 | 2 |
| Landing pages | 7 | 4 | 4 |
| Personal sites | 7 | 4 | 4 |

At low texture, keep the palette, type, and one clear dashed detail; omit glow and
default canvas on docs and dashboards. Higher texture means a few more deliberate
touches, not every effect at once. See `references/page-types.md` to calibrate by
task.

## Voice and type

Voice is a separate three-way setting (`data-voice` on `<html>`) that decides how
much terminal flavour the page keeps. The structure, themes, and UX rules never
change. Default is `nerd`, which is everything described above. `professional` is for
users who want this skill's structure and theming with less costume; a request for
conventional corporate design that never asks for this look still skips the skill.

| Voice | Pick it when | Type | Strokes | Motifs |
| --- | --- | --- | --- | --- |
| `nerd` | The user asks for nerdy, terminal, or hacker flavour, or for a personal or tool-for-developers page | Mono everywhere | Dashed frame, underline, controls | `*` bullets, `>` prompts, cursor, ASCII, canvas, stamps |
| `neutral` | General audiences, products, docs: keep the character, lose the costume | Mono headings and labels, sans body | Solid 2px frame and underlines; dashed controls stay as the signature | Dash bullets; no cursor, prompts, or ASCII |
| `professional` | Work tools, B2B, finance, health, or any audience that would read mono as a gimmick | Sans headings and body; mono only for small labels, keycaps, code | Solid hairline throughout; primary button has no offset shadow | Dot bullets; no canvas, ghost numerals, animated stamps, grain, or italic emphasis |

Voice also governs copy: `nerd` may be dry and in-joke friendly; `neutral` is plain and
specific; `professional` is direct and formal, with no jokes. In `neutral` and
`professional`, treat TEXTURE as at most 5 and 3 respectively. Type is its own
setting (`data-type`): `mono` or `readable`. `readable` keeps mono headings and
labels and sets body copy in the system sans, which widens the audience without
leaving the look. An explicit `data-type` always beats what a voice implies. Both
settings persist with the theme (see `references/themes.md`); `assets/head.js`
applies them before paint. For a standalone page, copy `assets/head.js`, `assets/tokens.css`, and `assets/base.css` into the project's public/static folder. Load `head.js` synchronously in `<head>` before the stylesheets, then link `tokens.css` first and `base.css` second. For generative backgrounds, also copy `assets/ambient.js` and `assets/ambient-mount.js` into the same folder and load `ambient-mount.js` with `<script type="module">`; serve the page over HTTP, not `file://`.

## Taste and visual decisions

- Keep body type comfortably readable, usually at least 16px with open line
  spacing. A reading measure near 45–75 characters is a useful start; data and
  controls may need more width.
- Establish hierarchy through size, weight, alignment, and grouping before adding
  boxes. Use regular spacing steps and align related labels, controls, and headings.
- Use flat themed surfaces. Dashed strokes signal emphasis; solid rules organize
  repeated data or fields. Do not outline every paragraph or control.
- Keep square corners as the baseline. Bevels belong on a pressable control or an
  intentional dialog, not every surface. Make hover geometry stable.
- Make the primary action obvious before hover. Secondary actions remain visible
  and understandable without decoration.
- Images, product photography, charts, and other media are welcome when real and
  useful. Reserve their dimensions; retain captions and meaningful detail.
- If a composition feels empty, restore content and hierarchy before adding
  ornament. If it feels like a terminal costume, remove prompts and fake system
  labels.
- Use one distinctive motif tied to the task. Prefer restraint over stacking the
  frame, canvas, CRT, animation, grain, and ASCII art in one view.
- Choose a hero grammar for the subject, rather than defaulting to an oversized
  headline or italic accent. When the content has numbers, categories, or a
  position, draw that real data as the focal motif before reaching for decoration.
  Colour a category only alongside a label, glyph, or outline.
  `references/craft.md` has hero grammar options and craft moves;
  `references/compositions.md` has page archetypes.

## Build in layers

1. **Design language:** use semantic design tokens as CSS custom properties and
   plain CSS component classes. Preserve the project's styling and component
   conventions by mapping the roles into them; do not replace an existing system.
2. **Ambient core:** when an ambient canvas is useful, use or adapt
   `assets/ambient.js`, a framework-free ES module. `create(canvas, options)`
   returns `start`, `stop`, `setMode`, `setPaused`, and `destroy`. Pass token
   colours. The module owns drawing, not application markup or theme persistence.
3. **Adapter:** detect the actual stack first, then read `references/stacks.md`
   for its short adapter recipe. The file includes all supported stacks; do not
   read it until detection is complete. Keep framework code thin and lifecycle-safe.

Theme choice and light/dark mode are separate. Apply saved theme and mode in a tiny
inline head script before paint, with system preference as the initial light/dark
setting. Persist safely; storage failure must not break the page. Canvas setup is
client-only; server and client markup must match. Reduced motion renders one static
ambient frame. Pause when the tab is hidden and on teardown. If there is no canvas,
use the CSS static fallback.

### Implementation sequence

1. Identify the actual page purpose, audience, content, route, and main task.
2. Inspect the existing source, assets, styling system, and component conventions.
3. Choose a unique archetype for each major page/view, then set the dials, theme roles, content width, density, and one optional motif. State the archetype and dials together before building.
4. Write one sentence completing “This could only be this site because …” using a real, specific quality of its subject, audience, content, or data; use it to reject generic decoration and copy.
5. Build hierarchy and useful static content first; keep all real actions working.
6. Add at least one subject-driven interaction that lets people meaningfully explore, change, compare, or act on the site's actual material—not a generic decorative widget.
7. Finish empty, loading, error, success, and disabled states that the flow needs.
8. Add texture only after the core is clear; keep it removable and low-cost.
9. Check the narrow layout, keyboard path, supported themes, and relevant states.

## UX rules outrank style

- Every state is designed: empty, loading, error, success, disabled. Never fake a
  working action or success.
- Show form labels; put errors by the field and associate them accessibly. Keep
  keyboard order logical, focus visible, and Escape able to close dialogs.
- Meet 4.5:1 contrast for normal text, including muted and faint tokens on the
  page colour. Status is never conveyed by colour alone.
- Work at 390px; interactive targets are at least 40px; tables scroll in their own
  labelled container. Prevent layout shift and apply theme before paint.
- Below 560px, put every data table inside a wrapper with `overflow-x: auto`; the
  table scrolls within that wrapper instead of reflowing into clipped or shrunk
  cells. Keep a visible edge cue that more columns exist.
- Hero controls, toggles, and captions stay inside the hero's own background band at
  every width, including layered or exploded states. Grow the band to contain them;
  never let them spill onto the page behind it.
- Inputs, field borders, and monograms must clear their threshold on both light and
  dark themes, measured against the surface they actually sit on: 3:1 for large
  monogram text and for control borders, 4.5:1 for labels and values.
- Respect `prefers-reduced-motion`. Keep real content selectable and copyable. Do
  not invent testimonials, logos, statistics, or product facts; mark prototype
  content as placeholder.
- Keep decorative art out of accessible names. Give meaningful visualizations a
  text alternative and retain their important information in real text.
- Keep persistent controls clear of content, focus, form errors, and mobile safe
  areas. Do not make essential navigation depend on hover.

Avoid gradients, soft-shadow rounded cards, glassmorphism, emoji grids, fake logo
walls, mixed typefaces, animating everything, glow over long text, neon green on
black, and centring everything. Do not use command palettes or keyboard jump keys
as aesthetic furniture.

## Supporting files — progressive disclosure

Read only the material relevant to the work. Detect the stack before opening
`references/stacks.md`.

| File | Read when |
| --- | --- |
| `references/page-types.md` | Choosing composition and dials for a particular kind of page. |
| `references/themes.md` | Selecting or adding a theme, mapping roles, or checking contrast. |
| `references/craft.md` | Raising polish: hero grammars, headline scale, stat and bipolar data surfaces, segmented progress, category colour, tactile primary action, choice cards, share cards, copy voice. |
| `references/compositions.md` | Choosing a distinct page archetype before building; ensure major pages/views do not repeat one within a project. |
| `references/texture.md` | Considering the ambient canvas, ASCII, border language, micro-interactions, CRT, or Win98 details. |
| `references/components.md` | Implementing common controls, content patterns, tables, or component states. |
| `references/interaction-states.md` | Building forms, asynchronous feedback, menus, dialogs, keyboard behaviour, or motion. |
| `references/responsive-layout.md` | Choosing geometry, adapting dense views, or fixing responsive behaviour. |
| `references/stacks.md` | Only after identifying the project's stack and styling system; use its detection, mapping, and matching adapter recipe. |
| `assets/tokens.css` | Using the supplied role tokens or comparing the included palette definitions. |
| `assets/base.css` | Using the plain CSS component and base classes as an adaptable reference. |
| `assets/ambient.js` | Adding the framework-free ambient canvas core. |
| `assets/starter.html` | Workspace is empty, or a runnable neutral reference is useful. |


## Completion check

Use the real content and existing flows. Check theme contrast, keyboard focus and
dialog dismissal, reduced motion, hidden-tab pause, storage failure, long labels,
and 390px layout. Prefer a targeted build or test and a rendered review where
available. Report what was verified; say when visual or adapter testing was not
possible.
