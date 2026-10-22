---
name: implement-design
description: Implement an updated design handoff in this repo - study what changed in design/ (DESIGN.md + mockups), commit the handoff, build the new or changed pages with the tailwind-design-system and vercel-react-best-practices skills, then verify the build against the mockups in a browser (Playwright or Claude in Chrome) at 390/834/1440 px in both themes, and commit the implementation. Use whenever the user says the design was updated, new pages or mockups were added, or asks to implement a page from design/.
---

# Implement a design update

The design handoff in `design/` is the source of truth (`.claude/rules/styling.md`). A design drop usually
changes `design/DESIGN.md`, adds `design/mockups/<page>/{light,dark}/*.dc.html` and touches the shared
header/footer links in every existing mockup. Work through the phases in order and keep the user posted.

## 1. Study the change

1. `git status --short design/` and `git diff design/DESIGN.md`: the new sections (`## N. <Page> (/route)`)
   are the spec. Read related older sections too (tokens §2, dark mapping §10) when the new one refers to them.
2. `git diff --stat design/mockups` then a sample diff of an existing mockup: often only nav links changed
   (e.g. a live-site URL became an internal route) and need the same change in `src/content/site.ts` `links`.
3. Render the mockups: `python3 scripts/render-mockups.py` (writes `.design-preview/`). If a new page needs
   fixed values for time-dependent holes, extend the script like the `home` case.
4. Read each new mockup at all three sizes (`awk '/<main/,/<\/main>/' <file>` keeps it short, and
   `grep -v '<path\|<svg'` drops icon noise) plus its `class Component` script: it holds the logic
   (filters, live status) and the sample data. Diff light vs dark to get the dark colours, then map every
   hex to an existing token in `src/styles/globals.css` (white cards in light → `raised` in dark, etc.).
5. Before coding, list for yourself: routes, data model changes (`src/content/types/<group>.ts`), pure logic for
   `src/lib/<group>/` (with tests), server vs client components (client only for "now", state or browser APIs),
   and anything the spec leaves open. Ask the user only about choices that change what you build.

## 2. Commit the design handoff

Commit the design changes on their own, before touching any code, with the **`commit`** skill. That keeps the
handoff separate from the implementation in the history.

- Stage only `design/` (`git add design/`); leave everything else unstaged.
- Use a `docs(design)` message naming the new or changed pages, e.g.
  `docs(design): add the Pořad bohoslužeb and Kontakty handoff`.
- This commit is docs-only, so the `commit` skill's build check does not apply to it.

## 3. Implement

Load the **`tailwind-design-system`** and **`vercel-react-best-practices`** skills (Skill tool) before
writing components, and follow the project rules (`.claude/rules/*.md`, loaded per path):

- Content stays in `src/content/`, behind `src/content/types/`; one data source per concept (e.g. the regular
  schedule feeds both the homepage and Pořad bohoslužeb). Update `.claude/rules/content-and-time.md` when
  the data model changes.
- Pure date/logic in `src/lib/<group>/*.ts` with Vitest tests (`.claude/rules/structure.md`) (Prague time, `pragueWeekday`, `useNow`/`useToday`
  for anything depending on "now"; client components get `renderedAt={BUILD_TIME}`).
- Components in `src/components/<group>/`, one per block, one markup for all breakpoints (`contents`,
  `order-*`, grid, `max-*`), tokens only (no hex, no arbitrary values; add a token in both themes if needed),
  `cva` for variants, `clsx` to join classes, no duplicate utilities for one property.
- Pages in `src/app/<route>/page.tsx` with `metadata`, `<SiteHeader currentHref=…>`, `<main id="obsah"
className="container-page …">`, `PageHeading`. Remember `output: "export"`: nothing that needs a server.
- JS-only controls get `data-js-only` plus `<noscript><style>[data-js-only]{display:none}</style></noscript>`.
- Update README.md (project layout), `.claude/rules/structure.md` if a new group appears, and
  `.claude/rules/design-check.md` (page list).

Known traps from earlier drops:

- Mockup links/buttons are `content-box`: `min-height: 52px` + `padding: 8px 0` is 68px tall, + a 2px
  border is 56px. Tailwind is `border-box`, so add padding/border to the min-height.
- The mockup renders use a fallback font when Google Fonts doesn't load, so their text runs wider;
  compare layout and spacing, not where lines wrap.
- Rules beat the mockup: never white text on green or orange (use `on-orange` / `on-green`), coloured text
  uses `*-ink`, arrows are `ArrowRightIcon` (Oxygen has no `→`) and a text link with one is `ArrowLink`, placeholders like `[foto]` / `[mapa]`
  become designed placeholders, `href="#"` needs a real URL.

## 4. Verify

1. `pnpm format && pnpm test && pnpm lint && pnpm exec tsc --noEmit && pnpm build`.
2. Serve both: `python3 -m http.server -d out 4173` and `python3 -m http.server -d .design-preview 4174`
   (background). Use the Playwright MCP tools (load them with ToolSearch) or Claude in Chrome.
3. Screenshot mockup and build per page at viewport widths **405, 849, 1455** (mockup width + ~15px),
   light and dark (`emulateMedia({ colorScheme: 'dark' })`), into the scratchpad, e.g. with
   `browser_run_code_unsafe`:
   ```js
   async (page) => {
     const dir = "<scratchpad>/shots",
       pages = [["<page>", "/<route>/"]];
     for (const [name, route] of pages)
       for (const [file, w] of [
         ["mobile-390", 405],
         ["tablet-834", 849],
         ["desktop-1440", 1455],
       ]) {
         await page.setViewportSize({ width: w, height: 900 });
         await page.goto(`http://localhost:4174/mockups/${name}/light/${file}.html`);
         await page.screenshot({ path: `${dir}/${name}-${file}-mock.png`, fullPage: true });
         await page.goto(`http://localhost:4173${route}`);
         await page.waitForTimeout(400);
         await page.screenshot({ path: `${dir}/${name}-${file}-build.png`, fullPage: true });
       }
   };
   ```
   Paste each pair side by side with PIL (mockup | build, scaled to ≤ 1800px tall) and Read the result;
   one composite per size is far cheaper than separate images.
4. Also check: no horizontal scroll (`document.documentElement.scrollWidth` equals the viewport width), the
   interactions (filters, copy buttons, live status), the page with JavaScript disabled (new browser context
   with `javaScriptEnabled: false`), and that pages sharing changed data (e.g. the homepage) still render.
5. Fix differences, rebuild and check again until the build matches.

## 5. Commit the implementation

Once everything in step 4 passes, commit the implementation with the **`commit`** skill. That skill runs the
full check again and validates the message with commitlint.

- Stage the code, tests and docs explicitly. Never stage `out/`, `.design-preview/`, `.playwright-mcp/` or
  screenshots.
- If the work has independent parts (e.g. a data-model change, each new page, docs or tooling), make one
  Conventional Commit per part, in an order where every commit still builds. Otherwise make a single
  `feat(<scope>)` commit.

Then report to the user: what was built, the data model changes, deliberate deviations from the mockup and
why, open questions for the parish (copy, URLs, photos), and the commits made.
