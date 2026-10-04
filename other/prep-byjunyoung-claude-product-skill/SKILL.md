---
name: prep
description: Prepares a Figma design page before the real work — normalizing frame names to `[screen]-[state]`, creating and placing feature-level sections, and reading screen content to find missing cases (state variants, interaction results) and stub them as placeholder frames. Includes the absorb workflow that works around reparenting limits with local font files. It handles renumbering and handoff URLs; it does not verify or report violations — both status checks and completion checks belong to /fig:lint. Triggers - "/fig:prep", "tidy this page", "group these into sections", "stub the missing states", "프렙 해줘", "가이드대로 정리해줘", "빠진 케이스 채워줘".
allowed-tools: AskUserQuestion, Bash, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot, mcp__claude_ai_Notion__notion-fetch, mcp__plugin_figma_figma__whoami
---

# fig:prep — prepare the page (tidy, section, stub missing cases)

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install fig@byjunyoung`), rather than improvising what the scripts do.

Like *mise en place* in a kitchen: before the design work and the arrows, every ingredient — every frame — gets cut and put where it belongs.

Takes one page of a design file and (1) normalizes frame names to the convention, (2) groups them into feature-level sections and lays them out, and (3) reads what is actually on each screen to find missing cases and stub them as placeholder frames. A tidied page is only a third done — `/fig:draw` fills the stubs, then connecting the flow with `/fig:arrows` completes the set.

**Prerequisites**: always load the `figma:figma-use` skill before calling `use_figma`.

**Seat check before the first write** — call `whoami` once. Where every plan it lists carries `seat: View`, stop before any `use_figma` write and say so: the reading half of this skill runs on a View seat, the writing half needs an Edit seat on the file's plan, and no retry changes that. Where the seats are mixed, go ahead — and if the first write comes back as a permission error, report the seat table and stop rather than retrying.

## When to invoke

- "tidy this page to the convention", "fix the frame naming and sections"
- "stub the missing states as placeholders"
- Laying down the skeleton — sections plus placeholders — before designing a new domain's screens

## When NOT to invoke

- Creating or syncing flow arrows → `/fig:arrows`
- Checking for violations only, zero writes → `/fig:lint`
- Auditing and applying work into the canonical page → `/fig:sync`
- Designing the screens themselves → `/fig:draw`
- Just understanding the file structure → `/fig:read`

## Inputs

- `figma_url` (required): the page to tidy. Its name decides how strictly the rules apply
- `mode` (optional): run the tidy. Omitted, `/fig:lint` runs first to establish the current state and a plan is proposed from it

## Where the rules come from — the config file (same source as fig:lint and fig:sync)

The rules are set by **`figma-conventions.yaml`**, not by this document. No values are written here.

```
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --js <fileKey>
```

Sections read: `naming` (frame and section patterns, state suffixes, required states per screen type) · `layout` (spacing tokens, column grid, row bucket) · `section_style` · `placeholder_style` · `pages` (strictness, excluded sections, protected numbers).

- **Strictness comes from the target page's name.** A match in `pages.readonly` means refuse the work and say so. On `pages.free`, apply the minimum — frame naming — and leave sectioning and layout alone. Only `pages.strict` gets the full treatment
- A page matching none of the lists is **not promoted to strict; ask the user** — not knowing the convention and there being no convention are different things
- On an unfamiliar file with no config, run `/fig:setup` first to infer the conventions and draft one
- If the team keeps a written guide, point `guide_source` at it. **It is not fetched on every run** — it is an input absorbed once

## Core conventions (what the config sets, and what this skill knows)

The values live in the config. What follows is the judgement about **how to use them**.

| Item | Rule |
|---|---|
| Frame names | The `naming.frame` shape, e.g. `Login-Default`, `Login-ErrorModal`, `ProductList-Empty` |
| Section unit | **By feature** — domain × feature, uniformly. Never split by UI pattern (page versus modal) |
| One axis per page | Within a page, sections are split on one basis only. Splitting domain A by feature while leaving domain B whole is not allowed |
| Section names | The `naming.section` shape. Number order equals user-flow order |
| Section style | `section_style` verbatim. **Never change the color to mean something** — every section looks identical |
| Layout (within a section) | **Flow first**: row 1 is the happy path (entry screen → steps → completion feedback), left to right on the `layout.column_grid` pitch. Branch screens (modals, dialogs) and what follows them go on the row below their source, left to right, with an overlay's state variants directly beneath that overlay. State variants of full-page screens, and sibling-type screens, go in a **variant zone** at the bottom of the section, separated by `layout.section_gap_same_row`. A list screen's single-column state stack is itself a variant zone. **Continuous variant stacking (required): variants of one `[screen]` stack in one column with no gaps, and no other screen — a transition-result modal or dialog — is wedged between a parent and its variants.** When the variant slot (directly below the parent) collides with the branch-follow slot (the row below the source), **variants win and stay directly beneath, continuous**, and the branch-follow moves to the next column or row. The `[state]` dashed line is straight, so anything in between gets passed through (this pairs with the state chains in /fig:arrows). The goal is arrows that run short — horizontal for progress, vertical for branching. When layout fights the arrows, fix the layout |
| Layout (between sections) | **Domain rows**: sections of one domain across a single row, left to right in feature order; a new domain starts a new row below. Numbering is row-major. Row tops align. Gaps are `layout.section_gap_same_row` and `layout.domain_row_gap` |
| Never touched | Sections matching `pages.exclude_sections` and number bands in `pages.protected_numbers` are **left alone at every step** |

## Repeated common elements — a common page plus a Default annotation, not per-screen placeholders

States and elements that **repeat identically across many screens** — generic Empty, Error, Loading, a shared empty-result, a shared error, a shared toast or dialog — do not get a placeholder frame on every screen. Copying one pattern as many times as there are screens destroys the single source, and one change then means touching all of them. Instead, gather them:

1. **One canonical copy on a dedicated common page** — put a single set of those states on the page `naming.common_page_pattern` points at, prefixed with `naming.common_frame_prefix`. That is the single source for the repeated pattern. **Look for an existing reusable asset first** (a design system spinner or feedback component) and only build one when there is none.
2. **Each screen gets nothing — no placeholder and no annotation** — the common page existing is the reference. A screen that draws none of its own empty, error or loading uses the common one; that is the rule, and it does not need restating on every Default. Pinning the same "see the common page" note on every screen was tried and it buried the few pins that mattered under dozens of identical ones.
3. **If placeholders are already scattered, remove them and convert** — delete the common-natured placeholder frames built per screen, and tidy the `[state]` and `-->` arrows that pointed at what was deleted (reconnect broken flows with `/fig:arrows`). **Before deleting, confirm that screen has its own separate Default** so the only copy is never destroyed → preview → go.

**Deciding common versus screen-specific:** if the state repeats *identically across many screens*, it goes on the common page. If it is *that screen's own* empty message, its own error, its own interaction result, it stays a per-screen placeholder (step 4). When it is ambiguous, ask about scope — do not sweep screen-specific states into the common pile.

**The test is what is on screen, not what the state is called.** A state that still shows the screen's own furniture — its table with its own columns and no rows, its filters, its header — belongs to **that screen**, however generic the name sounds, and is drawn per screen. Only a state that replaces the page with a single message carrying nothing of the screen is common. A list's empty state is almost always the first kind; a session-expired page is the second. Reading `Empty`, `Loading`, `Error` as common on the strength of the name is the way this goes wrong, and it takes a whole class of screens out of the to-draw list at once. **A real screen that has already been designed is not a placeholder**, so it is neither deleted nor annotated, even if its name ends in `-Empty`; exclude it and say so.

Canonical state frames on the common page carry the same identifying style as placeholders (dashed border, `Placeholder —` / `TBD`). Once the design is filled in, updating that one place counts as updating every screen that references it.

## Constraint: local fonts and reparenting — the group+ungroup workaround (confirmed 2026-06-05)

If an existing frame contains text in a local font that is not synced to the cloud, `appendChild` and `insertChild` **cannot move it into a section** — the font fails to load and the whole script is rejected (atomically, so the file is unchanged). `loadFontAsync` also fails on local fonts.

**But `figma.group([frame], section)` → `figma.ungroup(group)` does not go through font validation.** Making a group as a child of the section drags the frame in with it; ungrouping leaves the frame a direct child of the section — no manual dragging needed. The `absorb()` helper does exactly this. Two cautions:

1. Decide the coordinate correction from **the parent before the group call** — if the frame is already a child of that section its coordinates are already relative, and subtracting unconditionally double-counts and throws it outside the section
2. If even group+ungroup fails in that environment, fall back: move the frame's coordinates over the section area, put it in `figma.currentPage.selection`, and ask the user once to "nudge the selected frame and the section will absorb it"

Newly created placeholders only use configured cloud fonts, so this constraint does not apply — **create them as children of the right section from the start.**

## Establishing the current state is `/fig:lint`

To see what is out of line before tidying, call `/fig:lint`. **Every check, every criterion, and all the audit code live there** — detection is separated from repair, and this skill only repairs.

The `[membership]`, `[bounds]`, `[frame overlap]`, `[section overlap]`, and `[naming]` entries in the lint report are this skill's work list. Carry them straight into the step 2 plan.

The criteria are not repeated here. Two copies drift apart at the first revision.

## Procedure

### 1. Collect the conventions and the inventory

- **Resolve the config** — settle this run's basis with `resolve-config.py --js <fileKey>`
- Decide strictness from the target page's name (stop and report on `pages.readonly`)
- Collect frame and section names, coordinates, and sizes with page-level `get_metadata`
- Identify each screen from its screenshot (batched five at a time, in parallel) — never guess from the name alone
- If sections already exist, read their fill and name pattern and follow them
- **Read how a finished page covers one screen.** Open a page that is already built and list its frames for a single screen — how many states it carries, which suffixes, whether a modal has its selected state drawn beside it, whether a completion toast exists, **what each frame's height is and what sits at its bottom edge**. **That is the house baseline for step 4, and it outranks the fallback table there.** A file where one screen carries a dozen frames and a file where it carries three are both internally right; the wrong answer is a page that does not match its own neighbours. Name the page it was read from in the report
- **A sibling page is where to look first, not the only place to look.** A file opened for one new domain often has no finished page in it — the siblings are placeholders or empty, and the baseline sits **in another file**: the product's main design file, the one this page was branched from, or whichever file the team's guide names. An empty sibling is not "no baseline", it is a baseline one hop away, and treating it as none is how a page ends up being the first thing in the product built its own way. Only when the search outside the file also comes up empty is the fallback table all there is — say which file and page were read, or that the search was made and found nothing

### 2. Propose the plan (preview required)

Present renames, section composition, and layout as a table:

```
| current name | → new name | section |
```

- When sections could reasonably be composed more than one way (merged versus split), offer the options
- Flag frames whose identity is uncertain with an explicit guessed label
- **Write nothing before the user's go**

### 3. Execute (split into steps)

Never all at once — verify after each step before the next:

1. **Rename** — font-independent, safe to do in bulk
2. **Create sections** — empty sections at the target position and size. Immediately after creation, send them to the bottom of z-order with `figma.currentPage.insertChild(0, s)` (otherwise a new section covers existing frames with a white background)
3. **Place frames** — move coordinates over the section area, on the layout grid. **Keep gaps uniform** using the spacing tokens (the same effect as Tidy Up)
4. **Absorb** — `figma.group([frame], section)` → `figma.ungroup()` (font-independent; see the Constraint section above). Confirm parent and relative coordinates from metadata afterwards
5. **Resize sections** — sections do not auto-resize. The `resizeSection()` helper handles it with `layout.section_resize_margin` padding. **Check for overlap with neighbours immediately after resizing** — if the stretched section's bottom or right invades the row below or beside it (most likely with a vertically long list-state stack), push the invaded section out by the row gap in `layout` and re-check. This is the most common accident when placeholders grow a section
6. **Renumber** — once the arrangement is settled, reassign `NN.` in bulk with `renumber()`. `pages.protected_numbers` are left as they are
7. **Reorder layers (optional)** — align layer panel order with canvas position (an `insertChild` reorder within one parent, so no font constraint). Not required by the convention, so skipped by default and done only on request

### 4. Detect missing cases → placeholders (preview required)

**First split common from specific** — a missing case that repeats identically across many screens (generic Empty, Error, Loading) does not get a per-screen placeholder; it follows the "repeated common elements" section above (common page plus a Default annotation). Only screen-specific cases get placeholders as below.

Check on two axes:

**(a) State variant checklist** — `naming.required_states` is the basis. Settle the screen type from the screen's content, then compare against that type's list. **A screen is usually more than one type — run every row that applies and take the union.** A list with an edit card that opens under the selected row is a list *and* a form, so it owes the list's empty and load-failure states *and* the form's validation and leave-confirmation ones; settling on the single type that fits best is how half the list goes missing. If the config has none, use the fallback below and note that in the report:

| Screen type | Expected states |
|---|---|
| List / browse | Default, Empty (zero rows), Loading, Error (load failure) |
| Input form (create / edit) | Default, Validation (required and format errors), save confirmation, leave confirmation (closing mid-edit) |
| Search / filter | No results |

Pick the placeholder's state suffix from `naming.states` — never invent one.

**(b) Interaction result screens** — read the actual UI elements from the screenshot and check whether the screen you land on after pressing them exists:

| Clue visible on screen | Case that must exist |
|---|---|
| Delete button or link | Delete confirmation dialog → completion feedback |
| A clickable row or card | The detail or edit screen it opens |
| Upload area | Upload failure / wrong format |
| A maximum-count notice | The over-limit state |

Present the missing list as a table, including which clue each was inferred from → placeholders are created after a go. **Where the policy is undecided, write `TBD (needs confirmation): …` into the placeholder's description** — never draw an invented behaviour as though it were settled.

**A placeholder is work owed, not work done.** Where the case is already settled — the spec describes it, or a sibling page has drawn the same thing — the stub stands in only until `/fig:draw` fills it, and the report says so in those words. Drawing the real screen is not this skill's job, which is exactly why the report has to hand the list on rather than close on it. A stub counted as coverage is worse than a gap, because a gap is still visible.

### 5. Verify and hand off

**The mandatory last action of this step — call `/fig:lint` (via the Skill tool).** Once writing is done (creating, duplicating, moving, placing), **always** call `/fig:lint` and get `STRUCT PASS` and `FLOW PASS` — unconditionally if clone or move was involved. Fix what it reports and call again; **never report completion without a PASS.**

No inline self-check audit lives here. Holding the same check in two places means one gets fixed and they drift — the verdict always comes from `/fig:lint` alone.

- **Never PASS on an isolated screenshot.** `node.screenshot()` and single-node captures render a frame on its own and **cannot catch a parent or canvas-position error** — the frame looks perfectly fine by itself. The first pass is `/fig:lint`'s measurements; the second is **a screenshot of the whole section node**, not an isolated frame. When clone or move was involved, this is almost always where the accident shows
- **State the coverage per screen, beside the PASS** — for each screen, which required states are drawn, which are stubbed, and which are still missing. **A `PASS` is structural and says nothing about coverage**: the required-state check is the one item `/fig:lint` deliberately leaves to judgement (its `✋`), so a page of one Default frame passes every check there is. Reporting the PASS on its own reads as "finished" for something nobody counted
- **Output the per-section handoff URLs** — `https://figma.com/design/{fileKey}/?node-id={section id with : replaced by -}`. This matches the "share section URLs for handoff, not individual frames" checklist
- End the output with: the list of guessed labels needing confirmation, the list of TBD policies, and what comes next — `/fig:draw` on each stub, then `/fig:arrows`, and `/fig:handoff` once the screens are drawn

## Implementation — the tidy helper preamble

Write scripts use `${CLAUDE_PLUGIN_ROOT}/_common/scripts/prep-ops.js` as a preamble. Concatenate the config line, the whole file, and the actual calls, then hand it to `use_figma`.

| Helper | What it does · caution |
|---|---|
| `createSection(name, x, y, w, h)` | Creates a section. **Sending it to the bottom of z-order is mandatory** — otherwise the new section covers existing frames with a white background |
| `absorb(jobs)` | group+ungroup absorption. Coordinate correction is decided from **the parent before the call** (prevents double subtraction) |
| `resizeSection(section, w, h)` | Resizes, then **returns the names of neighbouring sections it invaded**. An empty array means it is safe |
| `renumber()` | Reassigns `NN.` in canvas row-major order. Protected number bands are excluded |
| `placeholder(section, name, desc, w, h, x, y)` | Dashed-border placeholder. When the policy is undecided, put `TBD (needs confirmation)` in desc |
| `commonRef(frame, fileKey, pageId, label)` | Legacy — kept for older runs, no longer called. Screens do not carry a common-page note (see "Repeated common elements") |

## Constraints

- **Preview → go before writing** — renames/sections/layout (step 2) and the placeholder list (step 4) each need their own go
- Sections matching `pages.exclude_sections` are untouched at every step: rename, move, resize, placeholder
- No more than ten operations per call, verifying with metadata or screenshots between steps
- **`clone()` and `createFrame` default their parent to currentPage, not the original node's section.** To land inside a section you must absorb (group+ungroup) and then set coordinates — otherwise the node stays page-level, and section-relative coordinates written onto it are read as absolute and it shoots off somewhere else. **Right after duplicating or creating: confirm the parent (`f.parent.type === "SECTION"`), absorb, set coordinates, audit bounds** — that is one set. Never finish on an isolated screenshot alone (see step 5)
- A screenshot of an empty section does not render overlapping non-child frames (you get a white box) — verify absorption by querying the frame's parent instead
- Never write an unsourced policy into a placeholder as though it were settled — behaviour without evidence is all TBD

## Notes

- The detection tables in (a) and (b) are a starting point, not the whole of it — the real work is reading each screen and asking, for that screen, "if I press this, what should I see?"
- Frame coordinates change right after tidying, so if the page already had flow arrows, propose a `/fig:arrows` sync alongside
- A placeholder is only finished when the real design replaces it *and* the dashed border and "Placeholder —" text are removed — the name stays as it is
