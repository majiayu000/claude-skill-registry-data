---
name: arrows
description: Generates and re-syncs flow arrows and their labels on a Figma design page. Reproduces in code what Autoflow-style plugins do — edge-midpoint anchors, right-angle elbows, branch trunks, element anchors, line styles that carry meaning. Flow information is stored in the node name (`source --> target`), so the whole page re-syncs with one command after frames move. Triggers - "/fig:arrows", "draw the flow arrows", "connect these screens", "re-sync the arrows", "화살표 그려줘", "흐름 화살표 추가", "화살표 sync", "플로우 연결해줘".
allowed-tools: AskUserQuestion, Bash, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__whoami
---

# fig:arrows — draw and sync screen flow arrows

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install fig@byjunyoung`), rather than improvising what the scripts do.

Draws user flow between frames in a design file as arrow vectors with labels. Figma's magnetic connector (ConnectorNode) is FigJam-only, so in a design file these have to be plain vectors — this skill **stores the flow in the node name**, which makes re-syncing automatic even without magnetism.

**Prerequisites**: always load the `figma:figma-use` skill before calling `use_figma`.

**Seat check before the first write** — call `whoami` once. Where every plan it lists carries `seat: View`, stop before any `use_figma` write and say so: the reading half of this skill runs on a View seat, the writing half needs an Edit seat on the file's plan, and no retry changes that. Where the seats are mixed, go ahead — and if the first write comes back as a permission error, report the seat table and stop rather than retrying.

## When to invoke

- "draw the arrows for this section's flow", "arrow from A to B"
- "sync the arrows" after frames were rearranged
- Tidying flow on a page where hand-drawn arrows (from a Flow Chart plugin) are mixed in

## When NOT to invoke

- Auditing arrow geometry or coverage only, zero writes → `/fig:lint`
- An overview of flow across domains → `generate_diagram` into FigJam (the figma:figma-generate-diagram skill)
- Connections inside a FigJam file → creating ConnectorNodes directly is the right answer there

## Inputs

- `figma_url` (required): the page or section to draw or re-sync
- `mode` (optional): create / sync. Omitted, it decides from whether `-->` vectors already exist — a vector with the same name means switch to sync, not create

## Core conventions

| Item | Rule |
|---|---|
| Arrow name | `source frame --> target frame`, e.g. `Login-Default --> Login-ErrorModal` |
| Label name | `[label] source frame --> target frame` |
| What gets an arrow | **User-action transitions only** (a button press, selecting an item). Conditional variants (-Empty / -Loading / -Error) are not drawn as transition arrows — they belong to a branch box, or, when they are states of the same screen, to a `[state]` dashed grouping (see "State chains") |
| Label text | The trigger for the transition, e.g. "Save", "tap a comment". Based on the button name confirmed on screen; if it is a guess, say so |
| Parent | Created as a child of the source frame's section, so it travels with the section |
| State chain name | `[state] {upper frame} ~ {lower frame}` — a headless dashed line joining adjacent state variants of one screen. Not a transition, a grouping. See "State chains" |

The name *is* the data — sync works by parsing names alone, so anything that breaks the naming convention drops out of sync.

The authoritative list of state suffixes is `naming.states` in the config. Examples in this document are illustrative; the actual classification follows whatever frame names fig:prep assigned. Never invent a new suffix.

## The representative-screen rule — sibling variants do not each draw to a shared destination

**Do not over-draw. The main flow leaves from the representative screen only.** When **sibling variants** of one feature — parallel screen types, state variants grouped by `[state]` — all transition to **the same shared destination** (a common error, a completion toast, a shared dialog), draw it from **one representative screen** in that group, not from every variant.

- Not "every variant → shared destination" but "**one representative → shared destination**". Duplicating the `-->` per variant produces a fan of arrows converging on one point, which badly hurts handoff readability (raised by the user, 2026-06-09)
- The remaining siblings already appear in the flow through their `[state]` grouping, so **coverage is satisfied by that** — not drawing them to the shared destination does not make them orphans
- The "sharedness" of a shared destination is conveyed by its name, its placement in a dedicated column, and that one representative connection. That single connection also resolves its own orphan status
- The call: if the candidate sources are grouped together by `[state]` and head to the same destination → one representative only. Genuinely independent screens that happen to share a destination (real separate entry points) fall outside this rule — draw each

## Fan-out trunking — many branches from one source share one trunk

When one source screen branches to **three or more** destinations through **the same UI affordance** (a shortcut menu, a panel, a tab bar — one element), dragging a long line to each destination piles up parallel lines and crossings. Bundle them into a **shared trunk** instead.

- **Share the stem**: every branch leaves the same start point, **overlaps along the same stem** to near the destination group, and **splits only at the end**. The stem reads as a single line; the splits are short and near arrival. (The branch-trunk geometry, applied to the whole fan-out)
- **One label**: do not label each destination — put **one label naming the affordance on the stem**. Duplicating the label per branch stacks pills at every arrival point and makes a mess
- **Keep an arrow per destination**: sharing a stem does not merge the nodes. They stay `source --> each destination`, which keeps coverage intact and shows where each one goes
- **To shorten the stem, fix the layout**: gathering the destination group next to the source (the row below, typically) shortens it. When layout fights the arrows, fix the layout (pairs with fig:prep)

Where the representative-screen rule reduces the *converging* fan of "sibling variants → shared destination", this reduces the *diverging* fan of "one source → many destinations". Both exist to keep handoff readable.

## The result of a save-type action — only navigation is solid; same-screen results are states or dashed

One action like a form save or submit usually splits three ways: (1) success, which **navigates** to another screen, (2) validation failure, which stays on the screen as an inline error or toast, (3) processing failure, which stays as an error toast. The principle here is **"only a user action that changes screens gets an arrow; conditional variants do not."** The three are told apart visually:

- **Success (navigation)** → a **solid** `-->` arrow, e.g. labelled "Save", to the completion toast or list screen
- **A conditional result that stays on the screen** (-Validation, -Error and the like) → a `[state]` dashed grouping, not a transition. If it shares the `[screen]` name and column, group it there
- **When that conditional result is a shared screen** used by several flows (a common error) and so cannot attach to one column via `[state]` → one **dashed conditional arrow** (arrowhead kept) from the representative screen. Being demoted from solid marks it as a same-screen conditional result. This pairs with the representative-screen rule — one representative, not every variant

The hierarchy in short: **solid = screen change / dashed arrow = shared conditional result screen / dashed `[state]` grouping = state of the same screen.** (Decided by the user 2026-06-09 — validation and error are both "results that stay on the screen", so only success, the navigation, stays solid)

## Geometry rules (reproducing Autoflow / Overflow behaviour)

```
Start point: one per frame — the midpoint of the source edge.
             Several outgoing arrows all leave from that same point (branch trunk).
Edge choice: decided by the target's relative position — to the right means
             right edge → left edge; below means bottom edge → top edge.
Path:        shortest, bending only when it must —
             a straight line when the cross-axis coordinates match, otherwise
             a right-angle elbow (start → trunk runs out by arrows.trunk →
             branches vertically → enters the target edge).
Avoidance:   if a straight or elbow path crosses another frame's area, detour
             over the top or bottom edge (a U shape). Decided by testing each
             segment of the path against frame rectangles.
End point:   the midpoint of the target edge, leaving arrows.head_gap before the head.
Entry:       the final segment is perpendicular to the target edge, so the head
             enters the frame head-on. Vertical edges (left, right) are entered
             horizontally; horizontal edges (top, bottom) vertically.
             When detouring above or below, target the midpoint of the top or
             bottom edge (vertical entry) rather than the left or right edge —
             dropping vertically onto a left edge leaves the head parallel to
             the edge, pointing at empty space beside it. The distance is right,
             so a numeric check passes and only the direction is wrong
             (confirmed 2026-06-16).
Labels:      built as a background pill placed over the line, the background
             hiding the line. Never covering the arrowhead —
             straight lines and single elbows: the middle of the vertical branch;
             branch trunks and corridors (several branches sharing one line):
             always on each one's own final segment before arrival
             (arrows.label.offset_from_target). Lining them up along the shared
             line makes a pill background cover another branch's line or corner
             and leaves it unclear which arrow the label belongs to
             (confirmed 2026-06-05).
z-order:     a pill always sits above its own arrow and any arrow crossing it —
             build every arrow first, then append the pills. Get this wrong and
             lines run through the label text.
```

### Element anchor mode (Overflow's hotspot approach)

When the user names the trigger element ("start from the Save button"), the start point matches **that element's cross-axis coordinate** instead of the edge midpoint:

1. Find the element inside the source frame by name or text
2. Take the element centre's absolute coordinate and leave the source edge at that y (or x)
3. Other arrows on the same frame keep the edge midpoint; only the anchored one is the exception

The arrow then lines up with where the interaction actually is on screen, which reads better in handoff. If the element is not found, do not guess — fall back to the edge midpoint and report it.

### Line style by flow meaning (Autoflow's path types)

| Flow type | Style | How to ask for it |
|---|---|---|
| Default / happy path | solid | the default |
| Conditional / secondary | dashed (`arrows.dash_conditional`) | "make it conditional", "dashed" |
| Round trip (bidirectional) | heads at both ends (both vertices ARROW_EQUILATERAL) | "bidirectional" |

Colour stays at the single `arrows.color`. Flow type is carried by solid versus dashed and by the heads, not by colour — bringing colour in mixes the signal with section style and state marking. If asked to distinguish by colour, say this first, then proceed.

When two arrows join the same pair of frames (A→B and B→A, or a duplicate transition), offset them by `arrows.parallel_offset` so they do not overlap.

Style precedence: **if the page already has arrows, read their stroke — colour, weight, dash — and follow it.** The `arrows` config values are used only when there are none; colour, weight, heads, label font, and pill padding all live there.

Be careful raising the label font size. Arrows between adjacent frames are only about as long as the trunk, so a bigger pill covers the arrowhead (dropped 28px → 20px on 2026-06-05). MCP cannot load local fonts, so keep the label font a cloud font.

## Procedure — creating

### 1. Understand the target

- Read metadata for the target section or frames (`get_metadata`, or a read-only use_figma script)
- Collect frame names, coordinates, sizes. Confirm button names from screenshots — that is the evidence for label text
- **Collect existing `-->` vectors first and check for duplicates.** If an arrow with the name you are about to create already exists, drop it from the create list; if it exists but is misplaced, switch to sync rather than create — two vectors with the same name make every later sync regenerate both and tangle
- **Use only coordinates read live, immediately before writing.** Never compute from coordinates remembered from earlier in the conversation — the user may have rearranged the canvas since. Do the coordinate work inside the write script, reading node coordinates through the `find()` helper

### 2. Propose the flow list (preview required)

Infer the transitions from screen content and present them as a table:

```
| # | name (source --> target) | label (inferred) | style |
```

- Mark inferred labels as inferred. Note that conditional variant frames were excluded
- **Write nothing before the user's go**

### 3. Create

- Decide straight / elbow / detour → create the vectors
- Create the label pills, loading the label font first
- Ten or fewer per call; split beyond that

### 4. Verify

Do not finish on an eyeballed screenshot — small misalignments are invisible at zoomed-out scale. Right after creating or syncing, **call `/fig:lint` and get a `FLOW PASS`.** What is checked and at what tolerance all lives there: geometry, entry direction, pass-through, orphans, labels. The same check is not kept in two places.

One thing this skill knows on its own — **element-anchored arrows are exempt from the edge-midpoint check.** They deliberately leave the midpoint to match the trigger element, so it is not a violation. When lint reports a midpoint deviation, first check whether that arrow is element-anchored.

**Label violation repair, in escalating order** — move and re-audit, repeating until PASS (established 2026-06-05):

1. To the middle of a segment **only that arrow uses** (its branch descent or corridor descent)
2. If there is no exclusive segment, to **the first corner** (the end of the horizontal segment leaving the source)
3. If the first corner is shared too, **split the source edge** — reroute the corridor arrow of a congested trunk out of another edge (the top, say) so its vertical line becomes exclusive
4. If the arrow is too short (under about 150px), **float the label 40–50px above the line** — clear of the line and the head, still visibly attached
5. Only as a last resort, shrink the label font

After the audit passes, use a screenshot (cropped and zoomed if needed) to check only the visual matters, label position among them. Fix and re-audit anything it turns up.

## Procedure — sync (re-syncing after rearrangement)

1. Collect what to sync from the page or section — VECTORs containing `-->` (transitions) and `[state]` VECTORs containing `~` (state chains). Transitions follow steps 2–6 below; `[state]` follows the "State chains" section
2. Parse the name as `source --> target` and find the frames by name on the same page
3. When both exist: recompute by the geometry rules, delete the old vector and recreate it, **preserving the existing stroke style, dashPattern, and whether it was bidirectional**. Reposition the label pill too, and **raise it above the regenerated arrow in z-order again** — the new vector lands on top of the old pill, so re-append it
4. When either is missing (renamed or deleted): **do not repair it — report it as an orphan** and let the user decide
5. Hand-drawn or hand-edited arrows are sync targets too if their names fit the convention. Say so before overwriting
6. **Run the audit** (as in Verify) — sync is only reported complete at zero violations

**Cross-section arrows break when the canvas is rearranged** — they are children of the source section, so they follow that one, and if the target section moves separately the head ends up pointing at empty space. (Arrows within one section survive, because relative coordinates are preserved.) When there are signs the user moved a section — the audit showing hundreds of px of arrival gap — propose a sync first. Label pills are repositioned along with their arrows.

## State chains (a grouping, not a transition)

A secondary marking, separate from transition arrows, that **groups the state variants of one screen**. Conditional variants (-Empty, -Loading, -Error) are not user-action transitions and get no arrow, but sometimes you want to show "these are states of one screen". This is the light alternative to a branch box.

- **`[state]` chain** — a **headless** dashed line joining adjacent state variants that share a `[screen]` name and are **stacked vertically in one column**, from the upper frame's bottom-edge midpoint to the lower frame's top-edge midpoint. One strand per adjacent pair, in stack order. Named `[state] {upper} ~ {lower}`. A child of the source frame's section.
  - **Adjacent means touching vertically in the same column** — there must be no other frame in that column between the two. The dashed line is straight, so a transition-result frame wedged in between (a modal, a dialog, a toast) gets passed through, and the line reads as pointing at that frame instead (confirmed 2026-06-08: a delete dialog sitting between an edit modal and its validation variant). Do not draw it straight in that case — see Selection below.

**Selection** — chains join **only variants vertically adjacent in the same column**. The test is not "are there multiple columns" but "**does it cross a column**" — several parallel columns by type are fine as long as each is vertically adjacent within itself (the same basis lint uses for coverage), while **a variant that sits in a different column cannot be joined by a straight `[state]`, so do not draw it — report it.** (Connect it once the layout gathers them into one column; never force it.) **Even in the same column, if another frame sits between the two variants** — a transition result placed between a parent screen and its variant — the straight dashed line would pass through it, so **do not draw it; report it as a layout problem.** Never work around it with an elbow. The real fix is fig:prep's layout rule: variants of one `[screen]` stack **continuously** directly below the parent, and transition results move to the next column or row. Fix the layout and the dashed line is a clean straight line again. Colour stays the same single colour as transitions.

Creating and syncing both go through the `stateLink(section, from, to)` helper (see Implementation).

**Sync** (for the `[state]` collected in sync step 1):
- `[state]` VECTOR: parse the name on ` ~ ` → find both frames → if both exist, delete and recreate via `stateLink` (**preserving dashPattern**); if either is missing, **do not repair — report as an orphan**.

**The audit is `/fig:lint`'s job** — it checks endpoint positions, orphans, non-vertical elbows, and pass-through. What this skill knows is **what to do when something is found**.

- **On a pass-through, delete that vector and report a layout problem.** Do not force the straight line or work around it with an elbow — the real fix is fig:prep's layout (variants stacked continuously below the parent)
- **On a non-vertical or elbowed line**, recreate it as a vertical straight line in one column, or, if the variants are horizontally separated, gather the layout into one column first and then connect. Elbow leftovers curl over their own from and to and slip past the pass-through check, which is why they are caught separately (2026-06-09: a `Set~Single` elbow cutting across the target frame)
- **On a reversed name order**, correct the name to `[state] {upper} ~ {lower}`. Left flipped, `stateLink` tangles on a negative length

The rest is a plain vertical line, so a screenshot is enough for visual checking.

## Connection coverage (every frame connected at least once)

**The principle: every screen frame must appear at least once in a transition arrow (`-->`) or a state chain (`[state]`).** A frame connected to nothing reads in handoff as "a screen left out of the flow" — validation and error variants go missing most often. **Always run this right after creating or syncing, and include the orphan count in the report.**

**Detection is the `[coverage]` item in `/fig:lint`.** Frames in excluded sections (templates, archives) are not required to connect — they are reference material, and staying out of the flow is correct for them.

**Handling** — connect orphans according to their nature (preview → go):

- **State variants** (-Validation, -Error, -Empty, -Loading, sharing a `[screen]` name) → join to their siblings with a `[state]` dashed line. Multiple columns by type are fine — a vertical dashed line within each column if each is a vertical stack, an elbowed one if the columns are apart. **Do not dismiss them as "multi-column, so dashed doesn't fit"** — usually they can be joined vertically within a column. **But if another frame (a transition result) sits between a parent and its variant even in the same column**, the straight line would pass through it, so do not connect — report a layout problem, move the variants into a continuous stack below the parent with fig:prep, then connect.
- **Transition result screens** (modals, dialogs, toasts, dropdowns) → a `-->` transition arrow triggered by the user action. But **when several sibling variants lead to the same result, only from the representative screen** (see the representative-screen rule) — not from every variant.
- **A frame that already appears in a `[state]` is not an orphan** — do not add a `-->` to a shared destination just to raise the connection count. The goal is zero orphans, not maximum connections.

**Done means zero orphans.** (While not over-connecting — read this together with the representative-screen rule.)

## Implementation — the build preamble

Create and sync scripts use `${CLAUDE_PLUGIN_ROOT}/_common/scripts/arrow-build.js` as a preamble. Every style and geometry constant comes from the config, so **no numbers are written into this document.**

```
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --js <fileKey>
```

Concatenate that one line, the whole of `arrow-build.js`, and the actual calls, then hand it to `use_figma`.

| Helper | What it does |
|---|---|
| `find(section, name)` | Reads frame coordinates live. **Never compute coordinates outside and pass them in** — the canvas may have changed since |
| `arrow(parent, name, pts, opts)` | Creates from a vertex array. Two points is a straight line, three or more a right-angle elbow. `opts.dashed`, `opts.bidirectional` |
| `straight` · `trunkElbow` · `detour` | The three path patterns. The helper applies the naming rules |
| `pill(section, arrowName, text, cx, cy)` | The label. Call it **after every arrow is built** so z-order comes out right |
| `stateLink(section, from, to)` | The headless vertical dashed `[state]` line |
| `hits(section, pts, exclude)` | Names of frames a path crosses. Judge with `straight` first; if it hits something, escalate to `trunkElbow` or `detour` |

**Finding an anchor element** — search for the trigger element by name or text. `query()` selectors accept **ASCII only**, so non-ASCII keywords have to go through `findAll`.

```js
const kw = "Save";
const trigger = sourceFrame.findAll(n =>
  ["TEXT", "FRAME", "INSTANCE"].includes(n.type) &&
  ((n.type === "TEXT" && n.characters.includes(kw)) || n.name.includes(kw)))[0];
// Compute the exit position on the source edge from trigger.absoluteBoundingBox.
// If it isn't found, don't guess — fall back to the edge midpoint and report it.
```

The numeric audit is not here — `audit-flow` under `/fig:lint` is the single source. Calling it right after creating or syncing and getting a `FLOW PASS` is the completion condition.

## Constraints

- **The mandatory last action before completion — call `/fig:lint` (via the Skill tool).** Once arrows are created or synced, **always** call it and get `STRUCT PASS` and `FLOW PASS` (frame membership and bounds come along with the flow). This skill has no audit code — every verdict comes from there. Fix what it reports and call again; **never report completion without a PASS**
- **Preview → go before writing** (the flow list table). For sync, report how many will change first
- Never call ConnectorNode or createConnector in a design file (FigJam only; it errors)
- Newly created vectors, text, and pills use only the configured label font, so the local-font constraint does not apply. **Put a node in the right section at creation time** rather than reparenting an existing arrow
- Broken leftovers whose names contain `-->` but which sit near (0,0) with no target frame are excluded from sync and reported as orphans
- If a label pill overlaps an arrowhead or another label, move it along the line to clear

## Notes

- These routing rules are a Plugin API simplification of Autoflow (shortest path, bending only when needed, obstacle avoidance, line style per path type) and Overflow (element and hotspot anchors, label backgrounds, independent styling)
- The `arrows` defaults are set against `layout.reference_frame_width`. On a file at a different scale, adjust proportionally — trunk, head gap, and pill padding have to move together
- A labelled branch row needs at least `arrows.trunk_to_target_min` between the trunk and arrival. Leaving it equal to the trunk length makes the space between trunk and arrowhead too narrow for the label to physically fit — this pairs with fig:prep's layout tokens
- Flow within one domain belongs in design-file arrows; flow that crosses domains belongs in FigJam
- If a genuine magnetic connector is required, the options are moving to FigJam or manually using a Superconnector-type plugin that draws FigJam connectors into a design file — outside what the API can automate
