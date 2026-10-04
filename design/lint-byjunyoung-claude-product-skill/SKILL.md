---
name: lint
description: Audits a Figma design page read-only — frame membership and bounds, section overlap, naming, arrow geometry and entry direction and pass-through, coverage orphans, [state] dashed links, variants stacked on one another inside a component set, and component default residue carried over by duplication. Reports violations and writes nothing. Each one comes back graded blocking or warning, which is what decides whether a section can be handed to engineering. Rules come from figma-conventions.yaml and the audit code lives in one place under ${CLAUDE_PLUGIN_ROOT}/_common/scripts. It is the single gate that absorbs the checks fig:prep and fig:arrows would otherwise each carry, and it is called again right after those skills write. Triggers - "/fig:lint", "lint this page", "audit the design", "검증해줘", "규칙 위반 검사해줘", "피그마 검수", "화면 복제 후 검수".
allowed-tools: AskUserQuestion, Bash, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot, mcp__claude_ai_Notion__notion-fetch
---

# fig:lint — read-only structure and flow audit (violations only)

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install fig@byjunyoung`), rather than improvising what the scripts do.

Takes one design page and **audits structure (placement), flow (arrows), and component usage in a single pass**, reporting only violations. Detection is separated from repair, the way a design lint should be — this skill **only detects**; fig:prep fixes structure and fig:arrows fixes flow.

**Why it exists**: to keep verification logic in **one place behind one gate**. Whatever touched the canvas — prep, arrows, a duplicated form, a manual edit — running this one skill at the end covers all of it. When verification is scattered across the working skills you get a blind spot shaped like "I wasn't using that skill this time, so the audit never ran." Removing that blind spot is the reason it is separate.

**Prerequisites**: **zero writes.** `use_figma` is used only for **read-only scripts** that inspect node properties — `return` a report, never mutate a node. Load `figma:figma-use` before calling `use_figma`.

## When to invoke

- "lint this", "audit the design", "check for rule violations" — on its own
- **As the mandatory final gate for fig:prep and fig:arrows** — always confirm through this right after creating, duplicating, moving frames, or generating and syncing arrows
- **Always when clone or move was involved** — the main cause of page-level orphans and out-of-bounds frames, and an isolated screenshot will not catch either
- **Always right after building a screen by duplicating another** — component default residue carried over by the copy is caught by this audit alone; the eye keeps missing it

## When NOT to invoke

- Actually fixing, tidying, or stubbing placeholders → `/fig:prep`
- Drawing the screen a violation is about → `/fig:draw`
- Creating or syncing arrows → `/fig:arrows`
- Auditing token (variable) bindings → `/fig:tokens`
- Checking and applying work into the canonical page → `/fig:sync`
- Just understanding the structure → `/fig:read`

## Inputs

- `figma_url` (required): the page to audit. For several pages, split the calls per page and run them in parallel
- `scope` (optional): structure only / flow only / components only. Omitted, all three run
- `reference_page` (optional): an existing production page to derive component usage conventions from. Omitted, the page in the same file that uses the most of the same components is chosen

## Where the rules come from — the config file (same source as fig:prep and fig:sync)

Naming patterns, the state list, excluded sections, tolerances, and statistical thresholds all come from **`figma-conventions.yaml`**, which is the single source. No values are written into this document.

```
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --js <fileKey>
```

The layers merge bottom-up: bundled defaults → `~/.claude/figma-conventions.yaml` → `./figma-conventions.yaml`. If it ran on bundled defaults alone, **say so in the report**.

- **A `null` pattern means that check is skipped.** This is what keeps a file with no convention from having every frame reported — "not knowing the rule" and "breaking the rule" are different things
- On an unfamiliar file with no config at all, run `/fig:setup` first to infer the conventions and draft one
- If the team keeps a written guide, point `guide_source` at it. **It is not fetched on every run** — it is an input absorbed once to help fill the config

**Checked regardless of config**: frame membership, out-of-bounds frames, section overlap, variant stacking, library sibling overlap, arrow geometry, pass-through, orphans. Coordinates and parentage are geometry, not convention, so they hold true with or without a written rule.

## What it checks

### A. Structure (placement) — fig:prep's territory

| Item | Basis | Frequency |
|---|---|---|
| **Frame membership** | A screen frame's `parent.type === "SECTION"` on strict pages. **Sitting directly on the page means the absorb step was missed** — `clone()` and `createFrame` default their parent to currentPage, so anything not absorbed leaks out here | ★ high |
| **Out of bounds** | A frame outside its own section's bbox. Usually an absolute coordinate written where a section-relative one belongs — a frame that became page-level and shot off to a stray absolute position | ★ high |
| **Frame overlap** | Screen frames within one section whose bboxes intersect (excluding the deliberate adjacency of a variant stack) | medium |
| Section overlap | Section rectangles intersecting horizontally and vertically at once — an unambiguous violation. Usually a section stretched to fit a placeholder that then invades the row beside or below | medium |
| Naming violation | Mismatch against `naming.frame_pattern` / `naming.section_pattern` (skipped when `null`) | low |
| Ordering mismatch | A section's `NN.` number disagreeing with its position on the canvas (row-major) | low |
| Missing required state ✋ | Missing states per `[screen]` group against `naming.required_states` — **unless that state exists on the common page** (a screen that draws none of its own uses the common one) (see fig:prep, "repeated common elements") | low |
| Split state variants | Variants of one `[screen]` broken apart in a column by an unrelated frame wedged between parent and variant, so the `[state]` dashed line passes through it. Once the section has `[state]` chains, only the pairs a chain joins are judged; before that, variants are told by name | medium |
| **Variant stacking** | Variants of one component set whose bboxes intersect. A set with no auto-layout drops a new variant on the last one's coordinates, so several states render as a single component — nothing about it looks broken, the top variant draws fine and the rest are simply not visible | ★ high |
| Default layer names | Layers inside a screen still carrying Figma's own `Frame 427` / `Group 12` name. **Layers inside a component instance are excluded** — they belong to the library that made the component, cannot be renamed on this page, and are fixed in that file instead | low |
| Annotations | A screen carrying more than `annotations.max_per_screen` (default 2) Dev Mode pins, or the same pin text on `annotations.same_text_screens` (default 3) or more screens. The second is almost always clone residue — a pin that came along with a copied frame and reads as if written for it | medium |
| **Implicit variable mode** | A screen whose colours are bound to a collection with more than one mode (light/dark, brand A/B) while neither the screen, its section nor the page names a mode for it — so it renders in the collection default. The usual cause is a clone: a screen that looked right only because its old page or parent set the mode, landed where nothing does. Judged per screen, not against siblings, because a page whose screens were all cloned the same way has no sibling to disagree. Set the mode explicitly even where the default is wanted — an explicit default survives the next move | ★ high |
| **Clipped or overflowing content** | Inside a screen, a child cut by a clipping box that a component defines — a cell, a slot, a field (a button in a cell whose padding leaves it too little room). A frame the screen clips itself is not judged: that is how a scrolling list, a carousel track or a cropped image is drawn, and nothing on the node separates those from an accident, or a direct child hanging off the screen's own edge (a floating control placed past the bottom). Both usually arrive intact from the canonical screen being cloned, and neither moves any frame, so the placement checks pass. Only painted content counts — text, or anything with a visible fill or stroke — so an empty wrapper wider than its parent is not a cut. Measured on layout boxes, since render bounds come back already clipped and would hide the very cut being looked for | ★ high |
| Library sibling overlap | A set or component overlapping the one placed beside it in the same section. Frame overlap above looks at frames only, so a component page passes that check while its components bury each other — a set that gained a variant or a layout runs past the gap it was placed with | medium |

### B. Flow (arrows) — fig:arrows's territory

| Item | Basis |
|---|---|
| Transition arrow geometry | Start point within `arrows.audit.edge_tolerance` of the source edge / arrowhead within `arrows.audit.gap_range` of the target edge / **the final segment perpendicular to the target edge, so the head enters head-on** / no segment passing through an unrelated frame / both source and target frames exist (orphan) |
| Labels | The pill above its own arrow in z-order / clearing the arrowhead by more than `arrows.audit.label_clear` / not covering another arrow's segment |
| Coverage orphans | Every screen frame appears at least once in a `-->` or a `[state]` (zero orphans) |
| `[state]` dashed lines | Two vertices, vertical, no elbows / name order top to bottom / endpoints within `arrows.audit.edge_tolerance` of the source's bottom edge and the target's top edge / no other frame between them |

### C. Component usage (default residue) — fig:prep's territory

An instance that was newly placed or duplicated **carries the component's defaults with it.** A display toggle that is on in the library — an icon slot, a supplementary area, a caption — stays on even where that screen does not use it, and renders an empty slot with nothing in it. At zoomed-out scale it is barely visible, so eye inspection keeps letting it through. **This is caught by measurement alone.**

| Item | Basis | Frequency |
|---|---|---|
| **Boolean default deviation** | An instance's boolean property on the working page differing from **the convention that same component follows on existing production screens in the same file** | ★ high |
| Empty display toggle | Same axis — a slot, caption, or supplementary area switched on with nothing in it | medium |

The basis is not a written rule but **how the same file actually uses the component** — the same principle as preferring existing assets. A property whose value also varies across production screens is a per-use choice, not a violation, and is not reported; only properties overwhelmingly settled one way count as deviation. The thresholds are `component_audit.min_samples` and `dominance`.

### The ✋ mark — a check the script does not do

**Missing required state**, marked `✋` above, is not done by the audit script. Not because it can't be, but because **it shouldn't be** — which states are required depends on whether the screen is a list, a form, or a search, and that call requires reading the screen's content. Faking it with a regex produces "if the name contains 'list' it's a list screen", which only adds false positives.

So this item is **judged by the agent, in step 3.** Read the target screen as a screenshot, settle its type, compare against the matching list in `naming.required_states`, and write the missing states into the report separately. If the type is ambiguous, do not decide — record it as "type unclear". **The grade turns on exactly that**: a settled type makes a missing state blocking, an unclear one makes it a warning.

Keep **the script's violations and this judgement separate** in the report. They rest on different kinds of evidence.

## Severity — what blocks a handoff

Every violation carries one of two grades. **The grade never changes what is audited, only how it is reported** — every check still runs, and everything found is still listed.

- **blocking** — engineering reading the file as it stands would build the wrong thing. A screen that cannot be seen, a coordinate that left its section, a connection that points somewhere it does not go, a slot switched on with nothing in it
- **warning** — the file reads correctly and is merely untidy. Names, numbering, a few pixels of tolerance

The grade is read off the tag the script already emits, so it is a lookup and not a second judgement.

| In the output | Grade | Why |
|---|---|---|
| `[duplicate name]` | blocking | A name lookup catches only one of them, so nothing else in the run can be trusted — narrow and re-run before reading the rest |
| `[membership]` | blocking | Not in a section. Handoff marks status on sections, so the screen is not in the handover at all |
| `[bounds]` | blocking | The frame left its own section |
| `[frame overlap]` | blocking | Screens cover each other — the one behind is invisible |
| `[section overlap]` | blocking | Which section a frame belongs to becomes ambiguous |
| `[variant stack]` | blocking | Variants sit on one another and only the top one renders |
| `[library overlap]` | blocking | Components bury each other on a library page |
| `[clip]` | blocking | A control or label is cut off, or sits outside the screen — engineering reads the screen as it renders |
| `[mode]` | blocking | The screen renders in a mode nobody chose — bound colours flipped, anything hand-typed for the intended mode unreadable |
| `[split state]` | blocking | An unrelated frame is wedged in, so the state chain runs through it |
| `[arrow] … orphan` · `… passes through` | blocking | The source or target does not exist, or the line crosses an unrelated frame and reads as connecting to it |
| `[state] … orphan` · `… passes through` | blocking | The same two, on a state chain |
| `[coverage] orphan frame` | blocking | A screen nothing reaches — engineering cannot tell how the user gets there |
| `[default]` | blocking | The instance carries a library default this screen does not use, and it ships as an empty slot |
| Missing required state ✋, **type settled** | blocking | A state nobody designed is a state engineering invents |
| `[naming]` · `[order]` | warning | Reads correctly, filed untidily |
| `[layer name]` | warning | Reads fine to whoever drew it, and to nobody else |
| `[annotation]` | warning | Pins that pile up stop being read, and a copied pin states a decision nobody made for this screen |
| `[arrow]` · `[state]` geometry — edge offset, target gap, entry direction, elbows, name order | warning | The connection is right; the drawing is off |
| `[label]` — z-order, clearance, covering a line | warning | Legibility, not meaning |
| Missing required state ✋, **type unclear** | warning | Undecided is not the same as missing, and the report has to say which |

Three of these are close calls placed deliberately rather than obviously: `[section overlap]` (ambiguity, not invisibility), `[label] covers` (a label can be read against the wrong arrow), and `[arrow] arrowhead parallel` (the entry direction is wrong, the connection is not). If a file argues otherwise, move it and say so in the report.

**Who reads which.** `/fig:handoff` gates on blocking alone — how a file is filed is not a reason to withhold work engineering can build. `/fig:prep` and `/fig:arrows` call this skill right after writing and still need a full `PASS`: the person who would fix the warning is the one standing there.


## Procedure

1. **Settle the target page and resolve the config.** Take fileKey and page from the URL and get `CFG` via `resolve-config.py --js <fileKey>`. For several pages, split per page and **call in parallel** — one `setCurrentPageAsync` per script, per the figma-use rule.
2. **Run the read-only audits** — the scripts below (A structure / B flow / C components) and collect violations. Zero node changes. C is two stages: derive conventions from a reference page (C-1), then compare against the working page (C-2). Different pages, so different calls.
3. **Judge required states (✋) and do the second visual pass** — settle the screen type (list, form, search) from a screenshot and compare against `naming.required_states`. Then, if a violation is suspected or clone/move was involved, confirm with **a screenshot of the whole section node**, not an isolated frame. Isolated renders cannot catch parent or position errors, so they are never grounds for a PASS.
4. **Report** — violating nodes by category, a one-line reason each, its **grade** (see "Severity"), and **which skill fixes it** (structure → fig:prep, flow → fig:arrows). Blocking first, warnings beneath them, never interleaved. Close on a line of its own with both counts — `blocking: N · warning: N`. Zero of both is `PASS`. Zero blocking with warnings still open is `GATE PASS` — enough for /fig:handoff, not enough for fig:prep or fig:arrows.

## Running it

The audit code lives in `${CLAUDE_PLUGIN_ROOT}/_common/scripts/`. Snippets are not copied into this document — two copies means one gets fixed and they drift apart.

```
${CLAUDE_PLUGIN_ROOT}/_common/scripts/audit-struct.js       A. structure
${CLAUDE_PLUGIN_ROOT}/_common/scripts/audit-flow.js         B. flow
${CLAUDE_PLUGIN_ROOT}/_common/scripts/audit-component.js    C. components (MODE=collect / compare)
```

All three are called the same way.

1. Get the single `const CFG = {...};` line from `resolve-config.py --js <fileKey>`
2. Concatenate that line and the whole script, and hand it to `use_figma`. If the target page is not the first page, prepend one `setCurrentPageAsync` line (once per script)
3. The return value is either an array of violations or `STRUCT PASS` · `FLOW PASS` · `COMPONENT PASS`

For several pages, split the calls per page and **issue them in one message so they run in parallel**. One script never switches pages twice.

**C is two stages and its calls are split.** `MODE="collect"` derives STAT from the reference page; `MODE="compare"` checks the working page against it. If one reference page does not yield enough samples, take one form-heavy page and one list-heavy page and sum their STAT.

After editing a script, check its syntax with `scripts/lib/check.sh`. `use_figma` wraps scripts in an async function, so top-level `await` and `return` are both legal — a combination `node --check` alone cannot accept. check.sh wraps them the same way before checking.

## Constraints

- **Never substitute eye inspection for the component default check (C)** — empty icon slots and empty supplementary areas are invisible at zoomed-out scale. Always run C after building a screen by duplication, or after duplicating a field. Repairs go through fig:prep as a **"handle the first match, then re-query" while loop** — changing an instance property invalidates sibling handles
- **Grading never narrows the audit** — every check runs and everything found is reported whatever its grade. The grade tells the reader what to do, and only /fig:handoff acts on it
- **Zero writes** — `use_figma` is read-only (`return` only). Never create or change a node. Repairs go to fig:prep or fig:arrows behind their own go
- **Never PASS on an isolated screenshot alone** — measured metadata is the first pass, a whole-section screenshot the second. A frame rendered by itself cannot show a parent or canvas-position error
- Convention-dependent checks (naming and the like) are only decided when the config has a pattern. On `null`, skip the check; if it ran on bundled defaults, say so in the report
- **Excluded sections are treated three different ways** — dropped from the audit, dropped from coverage, but **kept as pass-through targets.** If a line actually crosses one, it is a broken line whether the section is excluded or not. The list is `pages.exclude_sections`
- Duplicate frame names make a name lookup return only one of them. Report `[duplicate name]` first, then narrow to a single section and re-run
- **States managed on a common page are not counted as per-screen omissions or orphans** (see fig:prep, "repeated common elements") — (1) a state present on the common page counts as covered for every screen that does not draw its own, (2) canonical state frames on a page matching `naming.common_page_pattern` are expected not to appear in per-screen flow, so they are dropped from coverage. If the setting is `null`, this exception does not apply
- **A pattern page is dropped from coverage the same way** — the page `naming.pattern_page_pattern` matches holds arrangements rather than screens (how a row is built, where a badge sits in it), and nobody navigates to one, so requiring its frames to appear in the flow would report each of them as an orphan. `/fig:draw` writes and reads that page. With the setting `null` the exception does not apply, and the page's sections come back as orphans — which is the signal to record it
- **File patterns in sections, the same as any other page.** Coverage collects frames from sections only, so a pattern sitting directly on the page escapes the exception above — and lands on `[membership]` instead, which the structure script applies to every page-level frame without reading page strictness. Neither is a reason to scatter patterns loose on the canvas: put them in a section, where the coverage exception is what carries them
- **The component check cannot see a pattern page under a shell offset.** `component_audit.body_offset` skips the nav column and top bar of a full screen, and a pattern frame is narrower than that offset, so every instance on it is skipped and the page reports `COMPONENT PASS` having examined nothing. The offset is dropped on a pattern page for that reason — a clean report there means the instances were read, not that there were none

## Notes

- fig:prep and fig:arrows contain no audit code. They call this skill as a gate right after writing, and handle only **the repair side** of what it finds
- This skill only answers "what is wrong". The reasoning for "why it should be placed or connected that way" lives in fig:prep, fig:arrows, and the comments in the config file
