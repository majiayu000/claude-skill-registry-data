---
name: lior-code-to-figma
description: Lior Code to Figma™ by Lior Eli. Fixed rules for exporting any design, mock, flow or set of states from Claude into Figma using your own design system. Use whenever the user asks to put a design, screen, flow or states into Figma, "make mocks", "export to Figma", or hands over a ticket / spec / use-case list to design. Enforces design-system-only output (components, variables, text styles, icons, logos, spacing), one mock per use case, components built BEFORE mocks, one central master component, auto layout everywhere, and mocks placed inside the real product screen.
---

# Lior Code to Figma™

*Export designs from Claude into Figma, the way a senior product designer would.*
*Created by Lior Eli™*

These are standing rules, not suggestions. Follow them every time, in this order. If a rule cannot be met, say so explicitly in the final report instead of silently falling back.

**Tools:** Figma MCP (`use_figma`, `get_metadata`, `get_screenshot`, `get_libraries`, `search_design_system`, `get_figma_skill`). Always load the Figma `figma-use` skill first, plus `figma-generate-design` (composed screens) and `figma-generate-library` (components) when available.

**Your setup (fill in once, optional):** If you keep a project notes file (file key, page names, library names, key component names, screen size, content column width), read it before any Figma work. Otherwise ask the user for the Figma file link and discover the rest from the file.

## 0. Before touching the file

1. **Re-read the file.** Users rearrange pages and sections between turns. Never trust remembered ids or positions: run `get_metadata` and a read-only `use_figma` inventory first. Treat the user's current arrangement as authoritative. Never delete, move or overwrite their nodes; add new work in clear space inside a clearly named section.
2. **Collect the use cases** (section 2). Do not design before you have the list.
3. **Discover the design system** (section 1). Do not build before you know which components, variables and styles exist.

## 1. Always use the design system — no exceptions

Everything visible must come from the design system: **colors, typography, icons, logos/brand assets, spacing, radii, borders, shadows and components.**

- **Discovery order:** Code Connect / existing frames in the file → `get_libraries` → `search_design_system` (one intent per query: components, `variable`, `style`) → existing screens (inventory script: component keys, bound variable ids, text style ids). Search both the enabled libraries and the file's local variable collections (`getLocalVariableCollectionsAsync` returns only local ones; remote variables need `search_design_system` / `importVariableByKeyAsync`).
- **Colors / strokes / fills:** bind to semantic variables (e.g. `background`, `foreground`, `muted-foreground`, `border`, `muted`) with `setBoundVariableForPaint`. Never raw hex. Light and dark come from variable modes (`setExplicitVariableModeForCollection`), not duplicated colors.
- **Spacing / radius:** bind `itemSpacing`, paddings and corner radii to variables (e.g. `gap/*`, `radius/*`) when they exist.
- **Typography:** apply the library text styles (`textStyleId`); never set font or size by hand. Load the style's font before writing characters.
- **Icons and logos:** instantiate library icon/brand components. Never draw an icon from primitives, never paste an SVG when a library component exists. Swap icons through instance-swap, not by editing vectors. If the library truly lacks one: ask, or import the SVG once, make it a component, and flag it.
- **Components:** reuse existing ones (navigation, top bar, cards, buttons, inputs). Do not recreate something that exists. Do not detach instances. Override only via component properties, variants or text.
- If something is missing from the system, create it as a *local component bound to variables* and list it in the report as "new, needs a library home". Never ship hardcoded values.

## 2. Always design from the use cases

- **Source of truth for scope:** the prototype built in this conversation or codebase (its screens and states), a ticket (Jira, Linear, etc. — fetch it if a connector exists and read requirements, acceptance criteria and open questions), a spec/PRD, or the use cases written in the conversation. If several exist, use the union.
- Turn every requirement and acceptance criterion into an explicit **state list before designing**. Typical states: happy path, loading/in-progress, completed, collapsed/expanded, partial failure, retry/rate-limit, full failure, stopped/cancelled, empty, long-running, permissions/masked data, future-phase variants, history/reopen. Number them and show the list to the user in one short message if anything is ambiguous; otherwise proceed.
- **One mock per use case.** Never merge two states into one frame to save time. Each mock gets a number, a title and a one-to-two sentence note stating the rule it demonstrates.
- Trace each mock back to a requirement number in the report, and say which requirements have no mock and why.

## 3. Components first, one central master

Build in this order and do not skip a layer:

1. **Atoms** — the smallest reusable pieces (row, header, chip, badge, icon wrapper). Variants for states (e.g. Done / Running / Failed / Stopped), properties for text, booleans for optional parts, instance-swap for icons and logos.
2. **Composites** — groups of atoms with their own styling (card, timeline, panel, message bubble, input area). Use **slots** (`component.createSlot()`) for variable content so instances can be filled without detaching. Expose component properties for every text or toggle a mock changes.
3. **One central master** — the full product screen (e.g. `App / Shell`: navigation + top bar + main content slot + any persistent chrome). Every mock is an instance of this master. Changing the master changes every mock.
4. **Mocks** — contain only instances (plus slot content that is itself instances). No loose frames with fills, strokes or radius in a mock. Layout-only wrappers are allowed but must be auto layout.

**Test of success:** "Change the color of this icon / the border of this card / the radius of this element in one place, and every mock updates." If a visual property can only be changed by editing mocks one by one, the component layer is incomplete — fix it before delivering.

Place components in a dedicated, labelled section (`<Feature> · Master components`) with a README block and a label (name + purpose + slots/props) above each component. Keep pre-existing atoms where the user keeps them; reference them, do not duplicate.

## 4. Auto layout everywhere

- Every container with related children uses auto layout (`figma.createAutoLayout()` / `layoutMode`). No absolute x/y inside a design (only top-level nodes on the canvas and sections).
- Set `layoutSizingHorizontal/Vertical` (FIXED / HUG / FILL) **after** `appendChild`; call `resize()` **before** setting sizing modes. Wrapping text: `textAutoResize = "HEIGHT"` + FILL.
- FILL for content that should stretch, HUG for content-sized, FIXED only for true fixed sizes (the screen frame, a fixed content column).
- Page-level layout (wrappers of screens, header + screen stacks) is also auto layout.

## 5. Mocks sit inside the real product screen

- Never show a component floating on a blank frame. Use the product's real screen (the master shell) with its navigation, top bar and content area, filled with realistic content from the ticket (real names, counts, durations) — no lorem ipsum.
- Chrome state must match the use case (e.g. while running → stop button; idle → primary action).
- After filling a slot, resize the screen instance to the product's screen size — instances can collapse to near-zero height until resized. Make taller screens when content exceeds the viewport; never let content hide behind fixed UI.
- Provide light mode by default; provide dark by setting the explicit variable mode on the screen (do not rebuild).

## 6. File organization

- One section per ticket/feature: `<Feature> · <Title> · full flows`. Inside, a single auto-layout `Screens` frame with one wrapper per mock: `[Header instance] + [Shell instance]`.
- Name everything: `N · State name` for wrappers; components as `Group / Name`; slots with meaningful names (`content`, `rows`, `steps`).
- Position new top-level nodes away from existing content (never at 0,0 on top of something). Return created ids from every call.
- Do not leave temp or probe nodes. Remove them in the same script.

## 7. Figma Plugin API lessons (learned the hard way)

- A failing script rolls back everything; fix and retry the whole call. Return ids and counts from every write.
- Load fonts (`loadFontAsync`) for every text you touch, including nodes you only set `textAutoResize` on.
- `figma.currentPage` can't be assigned: call `await figma.setCurrentPageAsync(page)` at the start of every call. Instances may reference components on other pages of the same file.
- `createComponentFromNode(node.clone())` converts an existing styled frame (keeping bound variables) into a component. `combineAsVariants([a, b], parent)`, then rename variants: `State=Idle`, `State=Running`.
- Slots: `comp.createSlot()` appends at the component root; relocate with `parentFrame.appendChild(slot)`; set `layoutMode`, `itemSpacing`, then `layoutSizingHorizontal = "FILL"`. In instances: `inst.findAll(n => n.type === "SLOT" && n.name === "x")[0].appendChild(node)`. Existing instances can be *moved* into a slot and keep their overrides.
- Component properties: `addComponentProperty(name, "TEXT" | "BOOLEAN", default)` and bind with `node.componentPropertyReferences = { characters | visible: key }`. On instances: `setProperties({ [key]: value })`; keys carry a `#id` suffix, so look them up by prefix.
- A nested instance's variant is set on the nested instance itself: `shell.findOne(n => n.name === "Footer").setProperties({ State: "Running" })`.
- Components placed in an auto-layout board need `layoutSizingHorizontal = "FIXED"` and `layoutSizingVertical = "HUG"`, otherwise they stretch or collapse.
- Section size is manual: `section.resizeWithoutConstraints(w, h)` after the board settles; move sections so they don't overlap.
- `findAllWithCriteria` may return nothing on pages that are not fully loaded; use `findAll` with a predicate or load the page first.
- An empty auto-layout spacer is 100px tall unless you set FIXED height 1. Mock wrappers must be HUG height (FIXED crops the screen). `parent.children.indexOf(node)` can return -1 inside instance slots; use `findIndex` by id.

## 8. Icons, logos and states

- **Neutral UI icons** use one consistent muted color variable and stroke weight in every mock. Only brand logos keep their colors, and status icons keep status colors (warning, error, success). Bake the color into the component (a variant per icon kind) — never rely on a tint override on a swapped icon, because instance-swap resets overrides.
- **Swapped logos:** instance-swap resets size overrides. Put swappable logos in a fixed-size wrapper and make the logo FILL/FILL. If a library logo doesn't scale, wrap it in a local component whose child instance uses SCALE constraints. Verify each brand logo visually.
- **Loading states** follow the design system's pattern. If the product has a defined in-progress indicator, use it everywhere; don't invent spinners.
- **Atoms must exist before mocks reference them.** Before every edit, check that main components still resolve (`getMainComponentAsync` not null). Deleted main components leave detached frames named like the component: remove them and rebuild. Never delete or rebuild a component the user may be using without saying so.
- **Matching a reference video or screenshot:** extract frames with `ffmpeg` (e.g. 1.5 fps, full resolution crop) and sample pixel colors to match colors and sizes one to one.

## 9. Verify before reporting

1. Take one composition screenshot of the section, then screenshots of any screen with long content. Check for clipping, overlap, content hidden behind fixed UI, wrong variants, leftover placeholder text, wrong fonts.
2. Run an audit script over the mocks and report the counts (all should be 0):
   - non-instance frames with fills or strokes inside mocks
   - text nodes without a text style
   - fills/strokes not bound to variables
   - absolutely positioned children inside mocks
   - leftover temp/probe nodes
3. Confirm every use case from the list has a mock.

## 10. Report (short)

State: the list of use cases ↔ mocks; which components are existing vs new (and where new ones live); anything hardcoded or missing from the design system (should be none); anything intentionally not done. No claims you did not verify.

---

**Lior Code to Figma™** · Created by **Lior Eli™**
© 2026 Lior Eli. Free to use, share and adapt with attribution — please keep this credit when sharing.
