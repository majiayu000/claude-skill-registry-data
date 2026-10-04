---
name: preline-mcp
description: Add, integrate, or build Preline UI components and blocks into HTML files via the Preline MCP server. Use when the user mentions "preline", says "/preline", asks to add a UI component, or requests a Preline block (a ready-made page section) using Preline UI.
---

# Preline MCP

## Intent

Use this skill to integrate Preline UI components and blocks into HTML files via the Preline MCP server. The server exposes 6 tools that return integration-ready HTML, CSS, and JS.

Activate when:
- User says "preline", "add preline", "/preline", "use preline"
- User asks for a Tailwind CSS component from the Preline library
- User asks for a block (ready-made page section) or a starter page

## Defaults

- **Never guess slugs.** All section, component, and category identifiers are exact kebab-case strings. Always discover them via `components_list` or `blocks_categories` first.
- **One at a time.** Retrieve one component or block, integrate it fully, then move to the next.
- **Always read the target file** before inserting anything.
- Call `components_list({ section: "<inferred-slug>" })` when the component type is known - this keeps the response small. Omit section only when unsure.

## Decision: Component vs Block

| User says | Use |
|---|---|
| "component" / "components" | Component workflow |
| "block" / "blocks" (or "example" / "examples") | Block workflow |
| Ambiguous | Use judgment; blocks give more complete results |

## Clarifying Vague Requests

Ask the user to pick instead of guessing in either of these cases:

- **Abstract request.** Too abstract to confidently map onto one category/section, let alone one block/component - e.g. "give me something for a pricing page", "I need a nice form", "show me a dashboard example". Start at step 1 below.
- **Tied candidates.** The request is concrete enough to reach a single category/section, but `blocks_in_category` / `components_list({ section })` still leaves 2+ candidates whose titles + descriptions satisfy every criterion the request named about equally well (same layout/feature/style class), with nothing in the request to break the tie. Skip straight to step 3 below with just the tied candidates.

If exactly one candidate matches everything the request names ("a basic accordion", "the SaaS hero with tabs"), skip straight to the normal workflow - don't interrogate the user for things you can already resolve, and don't ask just to be safe when one option is clearly the best fit.

All clarifying questions and lists are in **English by default** - switch to the user's language only once they write to you in it.

**Blocks:**
1. **Ask which category fits.** Call `blocks_categories()` and present the relevant `mainSection / subSection / category` paths with their titles and descriptions - the catalog carries a one-line description for every category, so present it directly rather than inventing your own summary.
2. **Try to resolve in one round.** If the user's reply both names a category *and* describes the item distinctively enough to identify a single match (a specific layout, feature, or style), call `blocks_in_category` to confirm the exact ID and go straight to `single_block` - skip step 3 entirely.
3. **Otherwise, ask which block fits best.** Call `blocks_in_category({ mainSection, subSection, category })`, list the block titles + descriptions - or just the tied candidates, for the case above - and ask the user to pick the one closest to their needs.
4. **Fetch and integrate** the chosen block with `single_block`.

**Components - same shape, sections instead of categories:**
1. Ask which **section** fits (`components_list()` for the full list, or `components_list({ section })` once you can infer one).
2. If the reply names a section *and* describes the component distinctively enough → resolve directly via `single_component` (lean on `relative` metadata - see Smart Component Selection - to land on the right default/variant).
3. Otherwise list the components in that section (titles + descriptions, with `relative.category` groupings where present - or just the tied candidates, for the case above) and ask which fits best.
4. Fetch and integrate with `single_component`.

Keep each round to one focused question with a short, scannable list - that beats an open "what do you want?" and beats guessing a slug just to avoid asking.

## Composite & Layout Requests

When a request describes **more than a single component** - several pieces, a region, a full page, or an app shell - don't fetch ad-hoc. Plan the whole result first, then fetch and integrate one node at a time. The same steps apply to any shape: a dashboard, a settings page, a product page, a multi-step form, "a card/section/layout with X, Y and Z", etc.

1. **Lock cross-cutting constraints first.** Anything that applies to the whole result - class system (theme tokens vs utilities → `isUtilityBased` / `theme`), shared surfaces/colors, spacing/density, repeated element states - decide once, up front. Keep it identical across every later fetch and edit.
2. **Decompose into a tree:** containers → regions → leaf components. Write it down; each leaf is one fetch.
3. **Discover every node - route, then confirm.** Use [references/catalog-map.md](references/catalog-map.md) to route: an abstract intent (a whole page/region/shell) → the right `blocks_categories` branch (reuse a ready-made block as the skeleton when one fits); each named element → the right `components_list({ section })`. The map only tells you *where to look* - always confirm the exact slug against the tool output before inserting.
4. **Assemble outermost-first, one at a time.** The skeleton/outer container sets the shared surfaces and the script/init anchors; then fill inward region by region, integrating each fully (Integration Rules) before the next. Keep the returned classes, change **text only** - except the specific surfaces/colors/states the user asked to change. Apply every structural adaptation to the markup **before** writing it (see *Adapt before you write* in Integration Rules).
5. **Verify** the finished result against the request, element by element.

See [references/composite-layouts.md](references/composite-layouts.md) for the expanded method and worked illustrations.

## Workflow: Components

```
1. components_list({ section: "<slug>" })   → get valid component IDs
2. single_component({ section, component }) → get HTML/CSS/JS
3. Read target file
4. Integrate HTML, CSS, scripts, init (see Integration Rules)
5. Repeat from step 1 only after integration is complete
```

## Workflow: Blocks

```
1. blocks_categories()                                    → get hierarchy
2. blocks_in_category({ mainSection, subSection, category }) → get block IDs
3. single_block({ mainSection, subSection, category, block }) → get HTML/CSS/JS
4. Read target file
5. Integrate HTML, CSS, scripts, init (see Integration Rules)
6. Repeat from step 1 only after integration is complete
```

## Integration Rules

**HTML** - insert where the user needs it.

**CSS** (`<!-- CSS -->` section):
- MUST go inside `<head>`, immediately before `</head>`
- NEVER place in `<body>` or near `</body>`

**External scripts** (`<!-- Scripts -->` section):
- The `<!-- Scripts -->` label is a response section marker - NOT a location in the target file
- Placement algorithm: open target file, scan **upward** from `</body>`, skipping blank lines, comments, and non-structural tags (`</script>`, `</style>`, etc.)
- The **first structural closing tag** you reach (`</main>`, `</section>`, `</div>`, `</footer>`, `</article>`) is the anchor
- Insert `<script src>` tags after that anchor, ordered around the existing Preline core script - the loaded `<script src>` whose `src` contains `preline` (e.g. `…/preline/dist/index.js`; exact path varies by install):
  - scripts whose `src` does **not** contain `preline` (third-party libs: lodash, apexcharts, …) → **before** the Preline core script
  - scripts whose `src` **does** contain `preline` (Preline helpers, e.g. `hs-*-helpers.js`) → **after** the Preline core script
  - if no Preline core script exists yet, keep order: scripts without `preline`, then scripts with `preline`
  - inline init `<script>` always comes last, immediately before `</body>`

**Init** (`<!-- Init -->` section):
- Place immediately before `</body>`
- Wrap in `window.addEventListener('load', () => { ... })` unless the block already contains `<script>` tags

**Large responses (artifacts):** when a response is written to a temp scratch file, read it once with the Read tool (use offset/limit for big files), copy the needed blocks into the target, then delete the scratch file. Don't pull the whole artifact into context if you only need to place it.

**Adapt before you write.** When the request differs from the fetched markup - regions the user didn't ask for (breadcrumbs, demo menus, placeholder logos), different blocks or labels - produce the final markup in memory first, then write it into the target in ONE edit per region. Never insert fetched markup wholesale and refactor it with a chain of follow-up edits: every such edit re-transfers large markup, bloats context, and desyncs file state.

**Same token = same color.** Theme tokens (`bg-navbar`, `bg-sidebar`, `bg-layer`, …) are consistent across a theme - to give two surfaces the same color, give them the same token class. Never resolve tokens to raw colors by reading the project's CSS.

**Trust the returned markup - do not re-verify it.** The classes, structure, and `data-hs-*` attributes the MCP returns are valid Preline by construction. This is the single biggest time-sink to avoid. Do NOT:
- grep, parse, or scan the user's compiled CSS (e.g. `main.css`) to "confirm" a class exists or to resolve what color a design token produces - Preline classes resolve at the consumer's build step, so absence from any one stylesheet means nothing;
- write HTML/DOM/AST validators (Python `HTMLParser`, tag-balance checkers, etc.) - SVG and void elements trip naive parsers and produce false errors;
- re-read a placed artifact or re-open the edited file just to "double-check" the generated code.

Place the markup, change text only, move on. **Verify against the request** (is every element the user named present?), never by auditing the generated code or the project's CSS.

## Smart Component Selection

`components_list` may return a `relative` object per component:
- `isSectionDefault: true` - recommended default for the section; prefer when the request is vague
  - Exception: if the description says "multiple variants" and the user wants one, pick a single-variant component instead
- `category` - logical group (e.g. `"color-variants"`, `"states"`)
- `isCategoryDefault: true` - recommended default for its category; prefer when the request implies a style group

## Available Themes

`default` (blue) · `harvest` (amber) · `retro` (fuchsia) · `moon` (grayscale) · `ocean` (cyan) · `bubblegum` (pink) · `cashmere` (mauve) · `autumn` (orange) · `olive` (green)

Pass via `isUtilityBased: true, theme: "<name>"` on `single_component` or `single_block`.

## Key References

- [references/catalog-map.md](references/catalog-map.md) - routing map: block intent ontology (whole pages/shells) + all component sections grouped by purpose, JS-plugin marked. Open this to pick the right `section` / blocks branch before any discovery call.
- [references/composite-layouts.md](references/composite-layouts.md) - full method for multi-component / page / shell requests, with worked illustrations
- [references/mcp-tools-reference.md](references/mcp-tools-reference.md) - full parameter specs, placement algorithm detail, all 6 tools
