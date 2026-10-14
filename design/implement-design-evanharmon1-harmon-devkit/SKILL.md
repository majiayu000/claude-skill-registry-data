---
name: implement-design
description: >-
  Implement a finished Claude Design in this code repo — the Claude Design → code handoff. Use
  whenever the user has a design from Claude Design (Anthropic's design canvas) to turn into real
  code: phrases like "I finished designing in Claude Design", "implement this design", "do the design
  handoff", "Handoff to Claude Code", "I exported the handoff bundle / tokens.css / a .tar.gz design",
  "turn this design into code", or "set up a design system from this design". Handles both a single
  feature AND establishing a new design system in a repo that has none. Targets React + Vite +
  Tailwind v4 + shadcn/ui (Astro 6 and TanStack Router fully supported). This is NOT session/context
  handoff between agent sessions — it is about implementing a visual/UX design in code. Trigger it
  even if the user doesn't say the word "skill".
---

# Implement Design (Claude Design → repo)

Turn a finished design from **Claude Design** (or a similar tool) into working, on-brand code in this
repo. The export is a **handoff bundle** — a `.tar.gz` or `.zip` from "Handoff to Claude Code" holding a
README, the design **chat transcript**, prototype HTML/JSX/CSS, a token file, and uploads. Identify it
by that **content shape, not the extension**: Claude Design's separate "Download as .zip" menu item is
a raw-assets export with no README/chats — if the archive lacks the shape, it's the wrong export
(`ingesting-the-bundle.md`). The format is an unstable research preview, not a standard, so **parse
defensively**: read what's actually present rather than assuming exact filenames or folders. That same defensiveness lets the skill absorb
Claude Design's format changes and adapt to other tools (e.g. Google Stitch). The prototype code is
**prototype-grade** (it often runs on in-browser Babel + UMD React); your job is to **port** it into
this repo's stack, not paste it in.

**Three modes — detect which one you're in (Phase 0) and route accordingly:**

- **`establish-design-system`** — the repo has no design system yet; bootstrap one from the bundle.
- **`evolve-design-system`** — the repo has a design system and the bundle deliberately changes it (new/changed/removed
  tokens or brand); reconcile and **version** the change.
- **`implement-feature`** — the repo has a design system and the bundle is a bounded feature; build it
  **consume-first**, honoring the design without clobbering the established system.

The core principle running through all three: **`src/styles/globals.css` is the canonical runtime token
source and `DESIGN.md` is the AI-facing statement of intent — the repo is the source of truth, and the
bundle is a _proposal_.** When they disagree, `globals.css` wins; **never overwrite it wholesale from a
bundle** — diff and apply deliberate changes only. The bundle stays in place until **the user has
reviewed the implementation and approved it**, and only then is it removed before merge. Never assume
your implementation is correct; the user decides whether it matches the intent.

## Definition of done

**Render this in the chat — don't just leave it buried in this file.** At the **start** of the run,
paste the checklist below into your reply. Re-post it with boxes ticked as you finish each phase, and at
every **gate** state in the chat whether it **PASSED**, with the **evidence** (the measured numbers, the
screenshots taken, the user's words). Do **not** declare the handoff done until every box is ticked **in
the chat** and all four gates show **PASS with evidence**. Keeping the criteria visible in the
conversation is how you and the user know nothing was skipped.

The four **gates** are blocking: you may not take the action a gate guards until it is green and you
have shown why in the chat.

Reconciliation

- [ ] Bundle ingested **defensively** (parse what's there; don't assume exact filenames): intent/README
      → chat transcript → markup → token file → assets, read for intent and **ported**, never pasted
      into `src/`
- [ ] **Mode detected** — `establish-design-system` / `evolve-design-system` / `implement-feature` (asked if ambiguous); framework +
      router detected; up-front questions asked
- [ ] Bundle tokens treated as a **proposal** — diffed against canonical `globals.css`, never
      overwritten wholesale; new tokens resolved (force-fit to existing, or deliberate extension)
- [ ] Tokens in `globals.css` are by **role** (not export name) — Tailwind v4, OKLCH, three-layer;
      `.dark` authored (brand hue held, neutrals inverted); `--tw-prose-*` mapped if prose is used
- [ ] `DESIGN.md` reconciled (not clobbered); a system change (`establish-design-system`/`evolve-design-system`, or a feature
      extension) carries a **DDR + SemVer bump**

Implementation

- [ ] shadcn/ui + Lucide (named imports) only; styled **exclusively** with semantic tokens (zero
      arbitrary hex / one-off color literals)
- [ ] States covered: default, empty, loading, error, disabled
- [ ] Responsive (mobile-first): holds at phone/tablet/desktop with no horizontal overflow
- [ ] `/brand` built/updated in the **same** change (scope chosen up front during intake)
- [ ] Assets placed (static → repo, user media → R2); fonts self-hosted OFL/Apache `.woff2`; favicons
      generated from the mark
- [ ] **Logos downloadable on `/brand`** — SVG + PNG size matrix (square mark 64–1024, lockup/wordmark
      400/800/1600 wide, full-color / reversed/white / single-color black, padded solid-bg avatar) + `logos.zip`,
      generated by `task brand:assets`; a missing mark flagged to the user, never silently skipped

Gates — post **PASS + evidence** in the chat before taking the guarded action

- [ ] **① Static contrast** (blocks implementation — Phase 2): `task lint:design` is green; every token
      pair meets WCAG AA (4.5:1 text, 3:1 large/UI) in **both** themes. _Evidence:_ the checker output.
- [ ] **② Licensing** (blocks commit — Phase 4): every font/icon/image cleared for commercial use; AI
      logos flagged; anything unclear stopped, not guessed. _Evidence:_ the per-asset license list.
- [ ] **③ Verification** (blocks sign-off — Phase 5): `task verify` green and the build compiles;
      **rendered** contrast measured as **numbers** (both themes, every text role incl. long-form
      prose); responsive at phone/tablet/desktop with no overflow; cross-browser on
      Chromium/Firefox/WebKit (incl. mobile Safari). _Evidence:_ the numbers + the screenshot matrix.
- [ ] **④ Sign-off** (blocks deletion & close-out — Phase 6): screenshots shown (both themes, all
      states, key breakpoints), deltas surfaced, user has **explicitly approved**. _Evidence:_ the
      user's approval in the chat — never inferred from a green build or your own confidence.

Close-out (only once gate ④ is green)

- [ ] Handoff bundle deleted (or a thin screenshot + intent note extracted first if states remain)
- [ ] `docs/architecture/design-language.md` and `/brand` updated; a system change recorded as a **DDR with a SemVer bump**
- [ ] Conventional Commit on a **feature branch**; PR opened for human review; hooks never bypassed
      (`--no-verify` prohibited); no direct merge to `main`

## Inputs & stack

- A handoff bundle, usually unpacked to `specs/handoff-<feature>/`. If you can't find one, ask
  the user where the export landed (or whether they've exported yet) before proceeding.
- The existing repo: `DESIGN.md` (root), `src/styles/globals.css`, `docs/architecture/design-language.md`, `Taskfile.yml`, and
  the project's `CLAUDE.md`.
- **Stack target:** TypeScript, React, Vite, pnpm, Tailwind CSS v4, shadcn/ui, Lucide, Cloudflare
  Pages/Workers. Named primary router **TanStack Router**; **React Router**/plain React and **Astro 6**
  fully supported. Favor **shadcn/ui** for components and **Lucide** for icons.

---

## Procedure

Work the phases in order, and **track them in the chat** (see "Definition of done"): post the checklist
up front, tick boxes as you go, and report each gate's PASS with evidence. Explanations of _why_ live in
the referenced files — read the reference when you reach its phase.

### Phase 0 — Ingest, detect & decide

All the up-front orientation happens here, before any building:

1. **Ingest (defensively).** Unpack the bundle and read it for intent — don't hard-code its layout; the
   format is an unstable preview and varies by tool. The common Claude Design shape is a `.tar.gz` or
   `.zip` with a README ("CODING AGENTS: READ THIS FIRST") → `chats/*.md` (the design conversation — the real
   intent) → the entry HTML → a token file (`tokens.css`/`site.css`) → components → `uploads/`. Read
   whatever is actually present in that spirit (intent/README → transcript → markup → tokens → assets),
   and adapt if a piece is named or shaped differently. The prototype code is prototype-grade — read it
   for structure and intent, then **port** it; don't paste markup into `src/`. Locate the bundle (often
   `specs/handoff-*/`); if you can't find it, ask where the export landed. (`ingesting-the-bundle.md`)
2. **Detect mode, framework & router.** **Mode** — `establish-design-system` (no design system: no real `:root` tokens
   in `globals.css` and no `/brand` route), `evolve-design-system` (a system exists and the bundle is
   token/brand-dominant, or intent says "update the design system"), or `implement-feature` (a system
   exists and the bundle is a page/feature, its tokens mostly a re-emission of the existing set). Judge
   from the bundle's content (tokens vs. screens), the chat intent, and the repo state; **if it's
   ambiguous, ask** (fold the question into the batch below) rather than guess — a wrong guess risks
   clobbering the system. **Framework + router** drive file placement: TanStack → `src/routes/brand.tsx`
   and `src/components/ui`; React Router/plain → a normal `/brand` route; Astro → `src/pages/brand.astro`
   with React **islands** for interactive specimens; any other framework maps the same three roles
   (global stylesheet import, component dir, route entry) — never block on an unrecognized router.
   `establish-design-system` runs Phase 1 next; `evolve-design-system`/`implement-feature` skip to Phase 2.
3. **Decide up front — one `AskUserQuestion` batch.** Now that you've read the intent and know the
   stack, ask **everything you'll need at once** (up to 4 questions) so Phases 1–5 run uninterrupted:
   the **`/brand` scope** (core guide → brand/press kit → collateral groups; `brand-page.md`), plus any
   **genuine ambiguity** the transcript left open (routes/pages in scope, a required font/icon set,
   dark mode if unclear). Only ask what you can't determine yourself. The **one** thing that can't be
   front-loaded is the Phase 6 **sign-off** — it approves the built result.

### Phase 1 — `establish-design-system`: greenfield bootstrap (only if no design system exists)

If detection found no design system, stand one up before reconciling: install and configure Tailwind v4
and shadcn for the detected framework, let `shadcn init` write the default three-layer `globals.css`,
scaffold the `/brand` route, `DESIGN.md`, and `docs/architecture/design-language.md`, copy `scripts/check-contrast.mjs`, and add
the design Taskfile tasks. **Normalize whatever the bundle emits** (often HSL or inline values) into the
canonical OKLCH three-layer form, and record a **DDR establishing the system at v1.0.0**. Assumes a
working frontend app already exists. Use `deliverables-checklist.md` to confirm the **full** token and
component set is covered, not just the brand colors. See `greenfield-bootstrap.md`. (An existing system
skips to Phase 2.)

### Phase 2 — Reconcile tokens — GATE: static contrast

The most error-prone step, and where the modes diverge — **the bundle's tokens are a proposal,
`globals.css` is truth.** Read `token-reconciliation.md` (and `evolving-the-system.md` for `evolve-design-system`):

- **`establish-design-system`** — write canonical tokens from the bundle: map by **role** into the shadcn three-layer
  OKLCH `globals.css`, author `.dark` by hand (hold brand hue, invert neutrals), map `--tw-prose-*` if
  prose is used.
- **`implement-feature` (consume-first)** — **diff** against canonical and map each value to the
  **existing** token (inline hex/oklch → `bg-primary`, `text-muted-foreground`, …); add **nothing** by
  default. A value with no close match is a **decision point**: force-fit to the nearest token, or
  extend the system additively with a DDR — never inline.
- **`evolve-design-system`** — a three-bucket diff (added/changed/removed), classified with **SemVer**, breaking
  changes handled by **aliasing + deprecating** (not deleting), recorded as a **DDR + version bump**.
  A **wholesale replacement** (new brand; every consumer rewritten in the same change) is still
  evolve _governance_ — major bump + DDR — executed with establish _mechanics_: write canonical
  tokens fresh; aliasing serves nobody when no consumer of the old tokens survives the change.

Reconcile `DESIGN.md` (don't clobber it). Then run `task lint:design` (`scripts/check-contrast.mjs`) and
fix every sub-AA pair — this static gate must be **green** before you implement. Numbers in
`accessibility-verification.md`.

### Phase 3 — Implement components, assets & `/brand`

Build the UI in the stack: shadcn-first (check for an existing component before building), port the
prototype JSX to typed components, Lucide **named** imports, and style **exclusively** with semantic
tokens — never arbitrary hex. Cover the states the bundle won't show: empty, loading, error, disabled.
Build **mobile-first and responsive** — Tailwind breakpoints, fluid layout, no fixed widths, `dvh`, and
container queries where apt. Place assets (static → repo, user media → R2), self-host OFL/Apache
`.woff2` fonts (mind the `@import` order), and generate the favicon set **and the downloadable logo
exports** — icons alone are not enough; every run ships grab-able logo files in the standard sizes
(Stripe/GitHub/LinkedIn/README/social). Build/maintain the living
`/brand` page to the **scope chosen during intake** (no need to ask again here). See
`components-and-states.md`, `responsive-and-cross-browser.md`, `assets-fonts-favicons.md`,
`brand-page.md`.

### Phase 4 — Licensing gate (blocks commit)

Every font, icon, and image must permit commercial use. Fonts OFL/Apache only; Lucide (ISC) is safe;
confirm image licenses ("free to download" ≠ commercial). Flag AI-generated logos: usually
trademark-able but **not** copyrightable — recommend human edits + a clearance search before they
become the brand. If any license is unclear, **stop and flag it** rather than guessing. See
`ethics-and-licensing.md`.

### Phase 5 — Verify — GATE: verification (contrast, responsive, cross-browser)

Run the gates (`task lint:design`, `check`, `verify` — create any that's missing; never `--no-verify`).
Build, run the app, and screenshot every view in **both light and dark**, for every state, **and across
key breakpoints (phone/tablet/desktop) and engines (Chromium/Firefox/WebKit incl. mobile Safari)** —
Playwright drives all three from one config; set it up if the repo lacks it (agent-browser is
Chromium-only and doesn't substitute) — see `responsive-and-cross-browser.md`. Then
measure **rendered** contrast on the running page (static tokens passing isn't enough — a runtime layer
like `.prose` can override them): computed colors, both themes, every text role incl. long-form prose,
reported as **numbers**. Fix and re-measure failures before showing the user. See
`verification-and-signoff.md`, `accessibility-verification.md`.

### Phase 6 — Sign-off gate (blocks deletion)

Do not assume the implementation is correct. Show the user the screenshots (both themes, all states)
and measured ratios, compare against the bundle's intent and surface every delta, then ask
**explicitly** whether it matches before anything is removed. Iterate and re-verify; **loop here until
the user explicitly approves.** The bundle stays fully in place through this step. See
`verification-and-signoff.md`.

### Phase 7 — Close out (only after approval)

Delete `specs/handoff-<feature>/` (or extract a thin screenshot + intent note first if states
remain), update `docs/architecture/design-language.md` and `/brand`, and record a **DDR (with a SemVer bump)** in `docs/decisions/`
for any design-system change — `establish-design-system` (v1.0.0), `evolve-design-system` (patch/minor/major), or a feature token
extension. Commit with Conventional Commits on a **feature branch** (direct
commits to `main` are blocked) and open a **PR** for human review — never merge to `main` directly. See
`verification-and-signoff.md`.

---

## Guardrails (apply throughout)

- **Port, don't paste.** The bundle is a prototype; re-implement it idiomatically in the stack.
- **Semantic tokens only.** Never arbitrary hex or one-off Tailwind color literals — they skip dark
  mode and the contrast gate.
- **`globals.css` wins over `DESIGN.md`** for runtime. If they drift, flag it.
- **The bundle is a proposal; the repo is truth.** Never overwrite `globals.css` wholesale from a
  bundle — diff against canonical and apply deliberate, approved changes only.
- **New tokens are a decision point.** Map to an existing token, or extend the system deliberately
  (additive, with a DDR) — never invent ad-hoc values inline.
- **Record system changes as a DDR with a SemVer bump** (`establish-design-system` = v1.0.0; `evolve-design-system` =
  patch/minor/major; a feature extension = minor).
- **`/brand` is a maintained route, not a doc.** Keep it synced with the tokens; never let it drift.
- **Get sign-off before deleting anything.** Approval is the user's decision, never inferred from a
  green build or your own confidence.
- **Don't bypass hooks** (`--no-verify` is prohibited).
- **Conventional Commits**; feature branch; PR for human review; no direct merges to `main`.

## Reference files

- **`ingesting-the-bundle.md`** — Phase 0: defensive, format-agnostic ingest; the common Claude Design
  anatomy; and the prototype→production port.
- **`token-reconciliation.md`** — Phase 2: the proposal-vs-canonical doctrine — `establish-design-system` writes
  canonical tokens by role; `implement-feature` diffs and maps to existing (the new-token decision
  point). shadcn three-layer OKLCH, `.dark`, and the `--tw-prose-*` mapping.
- **`evolving-the-system.md`** — Phase 2 (`evolve-design-system`): the token diff (added/changed/removed), SemVer
  classification, aliasing + deprecation, and the DDR/version record.
- **`greenfield-bootstrap.md`** — Phase 1 (`establish-design-system`): stand up Tailwind v4 + shadcn + `globals.css` +
  `/brand` + Taskfile, per framework.
- **`components-and-states.md`** — Phase 3: port the JSX, shadcn-first, Lucide, the full UI-state
  matrix.
- **`assets-fonts-favicons.md`** — Phase 3: asset placement, self-hosted fonts (+ the `@import` order
  rule), favicon generation.
- **`responsive-and-cross-browser.md`** — Phases 3 & 5: build mobile-first/responsive and verify across
  viewports and rendering engines with Playwright (Chromium/Firefox/WebKit, incl. mobile Safari).
- **`accessibility-verification.md`** — Phases 2 & 5: the dual (static + rendered) WCAG AA contrast
  gate.
- **`brand-page.md`** — Phase 3: the living `/brand` style guide, the runtime scope question, and the
  collateral tiers.
- **`ethics-and-licensing.md`** — Phase 4: the commercial-use gate, the AI-logo reality, and vendor
  lock-in.
- **`verification-and-signoff.md`** — Phases 5–7: the gates, the sign-off loop, cleanup, and commit +
  PR.
- **`deliverables-checklist.md`** — a completeness self-check for token, component, brand, asset, and
  collateral coverage; used in `establish-design-system`/`evolve-design-system` and when building
  `/brand`.

Bundled assets (the skill installs these into the target repo):

- **`assets/check-contrast.mjs`** — zero-dependency static WCAG-AA token-contrast checker (resolves
  `var()` chains, merges the `@theme`/`:root`/`.dark` cascade, **auto-discovers the `*-text` status
  roles** so the "status text on light" rule is enforced by default, and is alpha-aware: translucent
  foregrounds are composited before scoring, translucent backgrounds are flagged for the rendered
  check instead of passing on the opaque value); copy to `scripts/`.
- **`assets/check-off-palette.sh`** — the off-palette half of the static gate: fails on arbitrary color
  literals (`bg-[#…]`, gradient hex, legacy + modern color functions — rgba/hsla/hwb/lab/lch/oklch/
  `color()` — anywhere in a style value or SVG attr); copy to `scripts/` (`chmod +x`).
  With check-contrast.mjs it backs `task lint:design`.
- **`assets/measure-rendered-contrast.mjs`** — the rendered half of the gate: samples computed
  colors on real pages in both themes (parses Chromium's oklch/oklab serialization, composites
  alpha, and fails as UNSUPPORTED any sample over a gradient/image/pseudo-element ground it can't
  model); copy to `scripts/`, fill `SAMPLES`. Run by `task verify:contrast`.
- **`assets/ingest-design.sh`** — safe bundle extraction for `task ingest:design`: takes
  `BUNDLE`/`DEST` from the environment (no shell interpolation), selects tar vs unzip by validated
  extension, and rejects unsafe archive entries (absolute paths, `..` traversal, links) before
  extracting; copy to `scripts/` (`chmod +x`).
- **`assets/Taskfile.design.yml`** — design task snippets (`lint:design`, `ingest:design`,
  `verify:browsers`, `verify:contrast`) to merge into the repo's `Taskfile.yml`.
- **`assets/playwright.config.ts`** — the cross-browser config (baseURL + `build && preview` webServer +
  the Chromium/Firefox/WebKit + mobile Safari/Chrome matrix); copy to the repo root.
- **`assets/brand-screenshots.spec.ts`** — a parameterized Playwright sweep (route × theme × the
  config's engine/device matrix, chunking pages taller than the browser capture cap) plus a
  route × theme horizontal-overflow guard; fill in `ROUTES`, `baseURL`/`webServer`, and the theme
  mechanism. Run by `task verify:browsers`.

## Complements

This skill handles the _reconciliation and wiring_. It pairs well with the `frontend-design` skill
(anti-"AI-slop" aesthetic direction) during Phase 3. It does not depend on any third-party skill.
