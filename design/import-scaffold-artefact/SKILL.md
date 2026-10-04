---
name: "Import: Scaffold from Artefact"
description: "Convert an exported Claude artefact (HTML or JSX) into a working Svelte 5 / SvelteKit 2 project"
when_to_use: "When a design or prototype exported from an Artifact (HTML or React/JSX) needs turning into a real, runnable project scaffold."
model: sonnet
effort: high
metadata:
  glyph: ᛊ
  family: import
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write", "Bash(bun:*)", "Bash(bunx:*)", "Bash(npm:*)", "Bash(git:*)", "Bash(mkdir:*)", "Bash(open:*)", "Bash(find:*)"]
argument-hint: '[artefact path (.html/.jsx, optional)] ["react" to opt into React/Next]'
---

Take a single-file artefact exported from Claude Chat or Cowork (an interactive HTML page or a JSX component) and grow it into a real, runnable project in Jason's default stack. Understand the artefact, interview for the decisions only a human can make, then port it: scaffold a project, translate the artefact into components or routes, and rewire its styling onto the project theme. A **full-project tail** (tests, git, docs, deploy) follows and is skippable.

Default target is **Svelte 5 (runes) / SvelteKit 2**. A JSX artefact becomes Svelte 5 components; an HTML artefact becomes a SvelteKit route. React/Next.js is an explicit opt-in. Nothing is scaffolded until the project config is approved.

**Announce at start:** "I'm using the Scaffold-from-Artefact skill. I'll read `{file}` first, then ask a few quick questions before building anything."

## Step 1: Interpret `$ARGUMENTS` and locate the artefact

- **A path is given and the file exists:** use it. Record its extension (`.html`, `.htm`, `.jsx`, `.tsx`, `.svelte`).
- **`react` (or `next`) appears in the arguments:** set the target stack to React/Next.js instead of the Svelte default. Note it and carry it into Step 3.
- **No path given:** search the likely export locations before asking. Run a read-only scan:
  ```bash
  find . ~/Downloads ~/Desktop -maxdepth 3 \
    \( -iname "*.jsx" -o -iname "*.tsx" -o -iname "*.html" \) \
    -not -path "*/node_modules/*" -mtime -7 2>/dev/null
  ```
  Present the candidates (most-recently-modified first) and ask which one. Do not guess if more than one plausible match exists.
- **Nothing found:** ask the user for the path and stop. Do not invent an artefact.

Confirm the resolved absolute path and the detected artefact type back to the user in one line before reading.

- [ ] Artefact file resolved to an absolute path that exists
- [ ] Artefact type detected (HTML vs JSX/TSX)
- [ ] Any stack opt-in from the arguments recorded

## Step 2: Read and understand the artefact

Read the whole file. Build an inventory before translating anything or asking any questions; a rushed port loses interactivity, and an uninformed interview asks questions the artefact already answers. Capture:

- **Structure:** the visible sections/components and how they nest. For a monolith, note the seams where it could decompose into components.
- **State and interactivity:** every piece of mutable state, what mutates it and every event handler. This is the part that must survive the port; static markup is easy, state is where ports break.
- **Data shapes:** the objects the artefact renders (arrays of items, config objects, form state). These become TypeScript interfaces in Step 6.
- **External dependencies:** CDN `<script>`/`<link>` tags (React UMD, Tailwind CDN, Babel standalone, charting libs, icon fonts), Google Fonts, inline `import` from `esm.sh`/`unpkg`. Each is a decision: replace with a bun dependency, keep as a CDN link or drop.
- **Styling:** inline `style=`, a `<style>` block, Tailwind utility classes or a CSS-in-JS object. Note every hardcoded colour (hex, `rgb()`, named) for Step 7.
- **Signs of a backend need:** does the artefact simulate fetching data, persist anything to `localStorage` or fake an API call? This informs the backend/database question in Step 3.
- **React-specific idioms** (JSX only): hooks in use (`useState`, `useEffect`, `useMemo`, `useRef`, `useContext`), portals, `dangerouslySetInnerHTML`, `children` composition, refs to DOM nodes, effect cleanup functions. Flag each one that will need care in Step 4.

Produce a short written inventory (components, state, deps, backend signals, React idioms found) and show it before the interview.

- [ ] Every stateful behaviour catalogued
- [ ] Every external dependency listed with a keep/replace/drop decision proposed
- [ ] Backend/persistence signals noted
- [ ] React-specific idioms flagged (JSX case)
- [ ] Hardcoded colours collected for the styling step

## Step 3: Interview for the project-shaping decisions

Some decisions are the user's to make, not yours to assume. Run a short structured interview, adapting the round discipline of the `roadmap-create-interview` skill: ask **2–4 questions per round**, never dump a long list at once, acknowledge briefly (don't repeat answers verbatim), and end each round with *"Anything else, or shall I write up the config?"*. This is a conversation, not a form.

Skip any question the arguments or the Step 2 inventory already answers (don't ask about a backend if the artefact is clearly static; don't ask the stack if `react` was passed).

**Decisions to capture:**

- **Project name.**
- **Target stack:** default Svelte 5 / SvelteKit 2; React/Next.js only on explicit opt-in. Recommend based on the detected artefact type.
- **Backend/database needed?** Informs SvelteKit server routes (`+page.server.ts`) vs a static site. If yes, which paradigm per Jason's stack: PostgreSQL/Supabase (relational), Neo4j (graph), MongoDB (object), or none.
- **Auth needed?**
- **Deployment target:** Vercel / Deno Deploy / GitHub Pages. Recommend one based on whether a server is needed (GitHub Pages only suits a fully static build).
- **Which tail parts** (Step 9) the user wants: tests, git, docs, deploy, any combination or none.

For closed choices (deployment target, stack, backend paradigm), use the `AskUserQuestion` tool with your recommendation listed first. Keep open-ended threads (project name, auth specifics) conversational.

**Synthesise a short config proposal** once the interview is done, e.g.:

```text
Project: {name}
Stack: Svelte 5 / SvelteKit 2
Backend: none (static)
Auth: none
Deploy: Vercel
Tail: tests + git, skip docs/deploy config for now
```

Get explicit approval before scaffolding. Nothing is built until the user signs off; treat this the same as the interview skill treats "nothing is written to the roadmap until approved".

- [ ] All undetermined decisions covered in 2-4-question rounds, none dumped at once
- [ ] Closed choices used `AskUserQuestion` with a recommendation
- [ ] Config proposal shown and approved before Step 4 begins

## Step 4: Announce the translation

State the artefact→stack mapping from the approved config:

- **JSX artefact → Svelte 5 components.** One `.svelte` component per React component; a monolith decomposes in Step 6.
- **HTML artefact → a SvelteKit route.** Markup goes into `+page.svelte`; page-load data (if any) into `+page.ts` or `+page.server.ts` if a backend was chosen.
- **React opt-in:** mirror the artefact's own framework: JSX stays React components, HTML becomes a Next.js/Vite React page. Skip the rune mapping below but keep the styling and tail steps.

**React idiom → Svelte 5 rune mapping:** read `~/.claude/library/references/react-to-svelte5.md` and state the mappings actually used by this artefact (plus the gotchas it lists that apply: effect cleanup timing, synchronous context, portals, ref-as-box).

- [ ] Every React idiom in the artefact has a named Svelte target (or a flagged manual port)

## Step 5: Scaffold the project skeleton

Choose the scaffold from the artefact type and approved stack:

- **HTML → SvelteKit 2:** `bun create svelte@latest {name}` (Skeleton project, TypeScript, add Vitest when the tail includes tests). Verify the current scaffold command via context7/docs rather than guessing; `sv create` has superseded `create svelte` in some tooling versions.
- **JSX (few components, no routing) → plain Svelte + Vite:** `bun create vite@latest {name} --template svelte-ts`.
- **React opt-in:** `bun create vite@latest {name} --template react-ts`, or `bunx create-next-app@latest` if the artefact implies routing/SSR.

Package manager: **bun** (Jason's tiebreak: bun > deno > npm/pnpm). Use `bun install`, `bun add`, `bun run`.

**TypeScript strict** is mandatory. Ensure `tsconfig.json` has `"strict": true` (SvelteKit's default already does; verify). Encode Jason's TS standards as you write code: interfaces over types for object shapes, no `any` (use `unknown`), explicit return types on exported functions, discriminated unions where the data warrants.

**File naming and indentation:**
- `.ts`/`.js`/`.json`: kebab-case (`colour-utils.ts`).
- `.svelte`/`.tsx`/`.jsx`: PascalCase (`FilterBar.svelte`).
- **Tabs, not spaces.** Write files with tabs; when editing, preserve exact tab characters and use the Edit tool (never sed/awk).

Expected layout (SvelteKit):
```
src/
  routes/
    +page.svelte        # ported page
    +page.ts            # load data, if any
    +page.server.ts      # only if the interview chose a backend
  lib/
    components/         # PascalCase .svelte components
    types.ts             # data-shape interfaces
    styles/
      tokens.css          # emitted theme tokens + semantic aliases (Step 7)
tests/
  fixtures/             # named-export fixtures (tail)
docs/
  adrs/                 # 001-*.md (tail)
```

If the interview chose a backend/database, note where it wires in but do not build the data layer unless asked; that is out of scope for the port itself.

- [ ] Scaffold created with bun and the right template
- [ ] `tsconfig` strict verified
- [ ] Directory layout matches the stack and approved config

## Step 6: Port the artefact into components/routes

Translate the inventory from Step 2 into real source files.

- **Decompose the monolith.** Split by the seams noted in Step 2: one component per cohesive UI region (a `FilterBar`, a `Card`, a `Chart`). Keep components small; lift shared state to the parent or a `lib` rune module (`.svelte.ts`).
- **Types first.** Write the data-shape interfaces into `src/lib/types.ts` before the components, and import them where the data flows. Explicit `interface` per object shape, `unknown` over `any`.
- **Translate state and handlers** per the Step 4 mapping. Port interactivity behaviour-for-behaviour; do not silently drop a handler because it is awkward.
- **Replace external deps** per the Step 2 decisions: swap CDN libs for bun dependencies (`bun add`), keep Google Fonts as links, remove React/Babel-standalone CDN tags entirely (the framework now provides them).
- **Preserve the markup structure** so the ported page is visually recognisable before restyling.
- Leave styling hardcoded for now; Step 7 rewires it. Wire up structure and behaviour here.

- [ ] Monolith decomposed into named components in their real files
- [ ] Data shapes declared once as interfaces and imported
- [ ] Every stateful behaviour from Step 2 reproduced
- [ ] External deps resolved (added, kept or removed)
- [ ] No `any`; exported functions have explicit return types

## Step 7: Rewire styling onto the project theme

Replace every hardcoded colour from Step 2 with semantic aliases backed by the project's `html` theme. **Read `~/.claude/library/references/theme-conventions.md` first.** If `.claude/themes/` has no `html` target, run `/theme-factory "html"` before this step, seeding it from the artefact's own colours (Step 2's inventory is the seed): the artefact's approved look becomes the theme rather than being replaced by one.

This step's job is preserving the *source artefact's own design* in the new codebase, not imposing a different aesthetic on top of one the user already approved. `~/.claude/library/references/artefact-conventions.md` is a useful cross-check for masthead structure, typography-pairing logic and the honesty/status-marking rule if the ported app is *itself* a reference/status-style artefact (e.g. a dashboard), but it never overrides what Step 6 already preserved from the artefact's own markup and voice.

1. **Emit the tokens:** `bun ~/.claude/library/scripts/theme/emit.ts .claude/themes/<family>-html.json -o src/lib/styles/tokens.css`. Import it once at the app root. The emitted block already carries light and dark variants and the theme-switch contract, but not a control: add the masthead light/system/dark toggle from `artefact-conventions.md`'s theming section (verbatim HTML/CSS/JS) if the ported app didn't already have an equivalent. This is a behavioural requirement, not an aesthetic one, so it applies even though this step otherwise preserves the source app's own design rather than artefact-conventions' full look.
2. **Define role aliases** in the same `tokens.css`, on top of the theme tokens:
   ```css
   :root {
     --color-primary:      var(--accent);
     --color-on-primary:   var(--accent-ink);
     --color-surface:      var(--surface);
     --color-text:         var(--ink);
     --color-danger:       var(--danger);
   }
   ```
3. **Replace hardcoded colours in components with the role aliases only.** Components never reference a hex or a theme token by another name; they reference `--color-primary` etc. This is the non-negotiable rule.
4. **Contrast is the theme's job:** every pair in the theme's `contrast` table is verified by `validate.ts`. If a component needs a pair the table lacks, add the pair to the theme and re-validate rather than eyeballing it.
5. Token names are ours (`--ink`, `--surface`); the `color` spelling in role aliases follows the CSS convention and is acceptable; British spelling everywhere else.

- [ ] `tokens.css` emitted from the project theme and imported once
- [ ] Role alias layer defined in `tokens.css`
- [ ] Zero hardcoded colours left in components
- [ ] Zero raw theme-token references in components (role aliases only)
- [ ] Every fg/bg pair used appears in the theme's verified `contrast` table
- [ ] Light/system/dark toggle present and reachable (the ported app's own if it had one, otherwise the masthead control from `artefact-conventions.md`)

## Step 8: Verify it runs (core output)

The port is not done until the page runs and the interactivity works end-to-end. This step is part of the **core**, not the skippable tail.

```bash
bun run dev
```
Then load the served URL (`Bash(open:*)` the localhost address, or drive it with the browser tools) and check:

- The page renders and is visually recognisable versus the original artefact.
- **Every interaction from the Step 2 inventory works:** click each handler, toggle each piece of state, exercise each list/filter. Interactivity parity is the acceptance test.
- No console errors; TypeScript is clean (`bun run check` on SvelteKit).

Report what runs and any behaviour that did not survive the port (with the reason), before touching the tail.

- [ ] `bun run dev` serves without errors
- [ ] Every catalogued interaction verified live
- [ ] `bun run check` / typecheck clean

## Step 9: Full-project tail (only the parts chosen in Step 3)

Run only the tail parts the user selected during the interview. Each sub-section stands alone.

**9a. Vitest test stub + fixtures**
- Vitest is the default (natural for Svelte/Bun). Add a `module-name.test.ts` alongside one critical module (prefer an integration test on a critical path over exhaustive units).
- Fixtures as named exports in `tests/fixtures/<module>.ts`, imported with `import * as fixtures from '../fixtures/<module>'`.
- Ship a real, passing stub test (e.g. render a ported component, assert one interaction) so the harness is proven, not just present.

**9b. Git init and first commit**
```bash
# .gitignore BEFORE the first git add: never commit secrets, node_modules, or build output.
git init
git add . && git commit -m "chore: scaffold project from Claude artefact"
```
Confirm `.gitignore` covers `node_modules`, build output, and any `.env` before that first `git add`. No hook symlinks; there is no bootstrap template this skill depends on.

**9c. ADR + README from Jason's templates**
- Read `~/.claude/library/templates/ADR.md` and write `docs/adrs/001-initial-tech-stack.md` recording the stack choice and the artefact-to-Svelte translation rationale. Follow the template's exact section order; do not invent a format.
- For the README, read `~/.claude/library/templates/readme-root.md` and emit a `README.md` from it.

**9d. Deploy config**
- Configure only the target chosen in Step 3: **Vercel** (`@sveltejs/adapter-vercel` or auto), **Deno Deploy** (`adapter-deno` / static), **GitHub Pages** (`@sveltejs/adapter-static` + base path). Install and set the one adapter; do not scaffold config for targets not chosen.

- [ ] Only the tail parts chosen in Step 3 ran
- [ ] `.gitignore` covers node_modules / build / .env before first commit
- [ ] Conventional-commit first commit (`chore:`)
- [ ] ADR + README generated from the library templates (not invented)
- [ ] Deploy adapter matches the interviewed target, nothing else configured

## Step 10: Report

Summarise: artefact source path; approved config (stack, backend, auth, deploy); component/route layout; interactions verified; which tail parts ran; anything that did not survive the port (with reasons). Surface any flagged React idiom that needed a manual workaround inline so the user sees it without opening files.

## Quick Reference

| Stage | Rule |
|-------|------|
| Locate | Resolve an existing absolute path; scan `~/Downloads`/`~/Desktop`/cwd before asking |
| Understand | Full inventory (state, deps, colours, backend signals) before the interview |
| Interview | 2-4 questions per round; closed choices via `AskUserQuestion`; propose config, get approval before building |
| Target | Svelte 5 / SvelteKit 2 by default; React/Next only on explicit opt-in |
| JSX → | Svelte 5 components (`$state`/`$effect`/`$derived`/`$props`) |
| HTML → | SvelteKit route (`+page.svelte` / `+page.ts`) |
| Package mgr | bun (tiebreak: bun > deno > npm/pnpm) |
| Types | `interface` per shape, `unknown` over `any`, explicit return types |
| Naming | `.ts/.json` kebab-case; `.svelte/.tsx` PascalCase; tabs, Edit tool only |
| Colour | project theme (`.claude/themes/<family>-html.json`); role aliases only in components; read `theme-conventions.md` |
| Contrast | pairs from the theme's verified `contrast` table; new pairs go into the theme |
| Verify | `bun run dev` + drive every interaction; core, not tail |
| Tail | Only the parts chosen in the interview: tests / git / docs / deploy |

## Common Mistakes

- **Dumping all interview questions at once.** 2-4 per round; it should read as a conversation, not a form.
- **Scaffolding before the config is approved.** The interview's proposal needs a sign-off first, same as the roadmap interviewer never writes before approval.
- **Porting markup but dropping interactivity.** The state and handlers are the point; catalogue them in Step 2 and verify each live in Step 8.
- **`useEffect` → `$effect` without checking cleanup.** Teardown timing differs; verify the cleanup fires on the right change.
- **Turning a `useRef` mutable box into `$state`.** A ref-as-box is intentionally non-reactive; keep it a plain `let`.
- **Referencing theme tokens or hexes directly in components.** Always go through the role alias layer.
- **Guessing colour hexes.** Colours come from the theme file; a missing one is a `/theme-factory` update.
- **Spaces instead of tabs, or sed/awk edits.** Tabs only; Edit tool only.
- **Running tail parts the user didn't choose.** The interview decides the tail; don't add scope back in.
- **Inventing a README format.** Use `readme-root.md`; use `ADR.md` for the ADR.
- **Guessing the scaffold command.** Verify the current `create svelte`/`sv create` invocation against docs before running.

## Red Flags

**Never:**

- Commit secrets, `.env` or `node_modules` (set `.gitignore` before the first `git add`).
- Leave a hardcoded colour or a direct RC-var reference in a component.
- Use `any`, spaces for indentation, or sed/awk to edit files.
- Ship the port without running it and driving every interaction.
- Silently drop an interaction because it was awkward to translate; flag it.
- Scaffold before the project config is proposed and approved.
- Run tail parts beyond what the interview selected.
- Use em dashes in body prose, US spelling or "not X but Y" couplets.

**Always:**

- Understand the artefact fully before asking a single interview question.
- Ask in small rounds; end each round offering to write up the config.
- Announce the artefact-to-stack translation before writing code.
- Default to Svelte 5 / SvelteKit 2; treat React/Next as an explicit opt-in.
- Declare data shapes once as interfaces and import them.
- Route all component colours through semantic aliases; read the reference doc.
- Verify with `bun run dev` and live interaction before the tail.
- Generate the ADR and README from the library templates.
