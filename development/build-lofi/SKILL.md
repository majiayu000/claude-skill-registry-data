---
name: build-lofi
description: Use when a feature's screens and flows are drafted and the design phase needs a navigable wireframe — a multi-screen greyscale Astro prototype where buttons and links actually work, suitable for the design gate and moderated user testing. In the A-Team pipeline it is conducted by ateam-design and consumes design.md's ## Screens & flows section, writing the throwaway prototype to docs/features/<slug>/lofi/. Triggered standalone by "build the lo-fi", "scaffold the wireframe", "make the prototype clickable", or "let's user-test the flow". Subcommands: `regen <screen>` (surgical single-screen rebuild — also the REVISE mechanic at the design gate) and `debrief` (standalone-only post-user-test interview, staged as an input/ evidence batch). Do not use for ad-hoc design exploration without drafted screens, or for hi-fi production UI — that is downstream of spec.md and belongs to the dev phase.
metadata:
  version: 0.1.0
  owner: Design (implemented on their behalf; every design opinion traces to the upstream skill)
  provenance: ported 2026-08-11 from subvisual/harness skills/design/build-lofi @ 940c86631660. The greyscale discipline, engine mechanics (templates, sentinel, lint, regen idempotence, debrief walk) are preserved; adaptations — input is design.md's ## Screens & flows instead of docs/design/ia.md, output lands per-feature, JOURNEY.md derives from JTBDs in pipeline mode, the lint is hardened to token-vars-only, variants mount at runtime, and debrief notes become an evidence batch — are marked A-Team where they touch mechanics.
---

# build-lofi

Generate a navigable greyscale Astro wireframe at `docs/features/<slug>/lofi/`
from `design.md`'s stable `flow-contract` and readable Screens & flows section.
Preserves graph navigation and selected local interaction fidelity,
enforces no-color via a lint step, and supports two follow-up modes:

- `build-lofi regen <screen>` — regenerate one screen idempotently.
- `build-lofi debrief` — post-user-test interview (standalone-only), staged
  as an evidence batch.

The lofi is a **throwaway visual reference** (CONTRACT.md): never production
code, never shipped. Dev builds the real UI from `spec.md` against the design
system.

## Modes

- **Pipeline** — conducted by `ateam-design`. Never asks a question: the
  screen list is `design.md`'s `## Screens & flows` (the conductor guarantees
  it exists), mock state derives from the JTBDs, ambiguities become flags in
  the phase report instead of interactive prompts.
- **Standalone** — a human invoked it directly. The upstream interactive
  behavior applies: ambiguity prompts, staleness confirmation, the debrief
  interview.

## Input — stable flow contract

Read `design.md`'s top-level `flow-contract` JSON fence, compiled against the
actual `briefs/wireflow/board.json` using `<harness>/runner/PROTOTYPES.md`.
The contract carries the complete graph, stable node/page/edge IDs, conditions,
transitions, scenario and interaction fidelity. `## Screens & flows` remains the
human-readable description; arrow strings and display names are not identifiers.
Unknown or stale graph references stop generation before writing output.

## Fidelity — `run_brief.fidelity` calibrates depth

| fidelity | What gets built |
|---|---|
| `flows` | Skeleton screens: title, purpose, navigation links only. No mock content, no variants. |
| `lofi` (default) | Full mock content per screen + scale/palette variants mounted for comparison. |
| `hifi-direction` | The full lofi, with the **recommended palette variant preloaded as the default view** (the human asked to feel the visual direction; `?palette=default` returns to greyscale). |

## Default mode: generate

### 1. Read and validate

Compile authored `prototype.json` against the current wireflow and place the
returned contract in design.md. Generation validates those sources before writing;
run `prototype-cli.mjs validate` again after generation. Select interaction fidelity
explicitly: `navigation` keeps graph links; `interactive` exercises local fixture
validation, loading, failure and retry. This is independent of visual depth.

### 2. Staleness check

Validate the graph, design and generated contract hashes. A timestamp or sentinel
alone cannot establish currency. Regenerate stale contract data before review;
keep unrelated screens and accepted token files intact.

### 3. Flag ambiguities

Scan screens for vagueness: purpose under 4 words; generic name without
qualifier ("Dashboard", "Home", "Page", "Detail"); screen in 2+ flows with
different roles; same source flowing to 2+ destinations. For each, **explain
why it matters** — the lofi needs to know what's on the screen.

Standalone: ask, with the upstream (a) tell-me-the-content / (b)
split-the-screen options. Pipeline: resolve with the most conservative
reading, record each as an assumption (`research-plan.md`, `· [design
phase]`), and list them in the phase report. More than 3 ambiguous screens →
that's a **flag for the gate**: the screen draft needs sharpening.

### 4. Scaffold the Astro project (only if `lofi/` doesn't exist)

Copy from this skill's `templates/`: `package.json` (Astro + Tailwind v3),
`astro.config.mjs`, `tailwind.config.mjs` (greyscale baseline),
`src/layouts/Layout.astro` (carries the A-Team variant loader),
`src/components/Header.astro` + `Footer.astro`, `src/styles/tokens.css`
(greyscale baseline + brand fallback chain — replaced when `design-system`
materialises tokens), `lofi-lint.mjs`, `JOURNEY.md` and `LOFI.md`
placeholders. `prebuild` runs the lint.

### 5. Generate per-screen pages

For each screen, write `src/pages/<slug>.astro` (kebab-case of the name):

- `<h1>` = screen name; purpose as subtitle.
- Body: greyscale wireframe elements matching the purpose (boxes for content,
  gray rectangles for images, lists with placeholder rows) — calibrated by
  fidelity.
- Navigation uses stable graph edges, including branch conditions and retry
  loops. Run `prototype-cli.mjs generate` to create the shared `/flow` player and
  mapping manifest. Navigation fidelity leaves validation/recovery unverified;
  interactive fidelity uses the bounded local runtime and explicit scenario reset.
- Color discipline: use `white`/`black`/`gray-*`/`neutral-*` utilities or
  color roles whose Tailwind config value is bound to a CSS variable. The lint
  reads the generated target's `theme.colors` and `theme.extend.colors`, so
  declared roles such as `brand-500`, `success`, and target-specific nested
  roles remain valid without opening the vocabulary to Tailwind palette names.
  No raw or named CSS colors. Primary actions get `.cta` — greyscale by
  default, tinted only when a palette variant mounts (the fallback chain in
  `tokens.css`).

Mock data reads from `JOURNEY.md`, consistently — the same names, the same
counts, on every screen.

### 6. Write narrative documents

- `JOURNEY.md` — one paragraph: who the user is, what state they're in, the
  mock content scope. **Pipeline: derive it from the active JTBDs** the
  feature serves — jobs carry who/situation/trigger in their `## Context`;
  cite the job ids. Standalone with no jobs: ask one paragraph, then write.
- `LOFI.md` — per-screen invented-content summary (mock data, buttons, where
  each link goes).

### 7. Mount variants (fidelity ≥ lofi)

Visual variants are optional within the established project conventions. For a
declared high-risk interaction comparison, follow
`<harness>/runner/INTERACTION-ALTERNATIVES.md`: make two or three structurally
different flows using the same job, scenario, constraints, tokens and evidence
method. Preserve every option's flow IDs and receipts. Palette/scale changes
alone cannot satisfy the comparison. A routine correction retains the existing
interaction with a reason. Keep the selection provisional and target-user
usability unrun until separate evidence resolves its acceptance obligation.

Copy any `scale-variants/*.css` and `palette-variants/*.css` produced by
`design-system` into `lofi/public/scale-variants/` and
`lofi/public/palette-variants/`. The Layout loader mounts them at
`?scale=<name>` / `?palette=<name>` (sticky via localStorage;
`?palette=default` clears). `hifi-direction`: set the recommended palette as
the loader's preload default. List the comparison URLs in the phase report —
the gate reviews options by clicking, not by reading prose.

### 8. Touch the sentinel, lint, report

Write the timestamp to `.lofi-generated`. Run `node lofi-lint.mjs` — any hit
fails with file + line + rule (`lofi/no-raw-color`, `lofi/no-named-color`, or
`lofi/no-color-utility`); fix the leak, never bypass. Typography roles come
from the canonical scale plus the target's configured `fontSize` keys. For
ambiguous arbitrary utilities, length/position values are allowed only in the
corresponding utility family, while colors must resolve through `var(--token)`.
Fractions on layout utilities remain legal. Report: path, screen count,
ambiguities resolved (and how), variant URLs, dev command
(`cd docs/features/<slug>/lofi && npm install && npm run dev`).

## Regen mode: `build-lofi regen <screen> [with <instruction>]`

1. Resolve the stable page/node ID in the current flow contract; error if unknown.
2. Rewrite ONLY `src/pages/<slug>.astro` — not layouts, not other screens,
   not styles.
3. Incorporate the instruction if given; otherwise regenerate from the
   current `design.md` + `JOURNEY.md`.
4. Update that screen's entry in `LOFI.md`; touch the sentinel; lint.

**This is the design gate's REVISE mechanic**: the conductor maps the
human's revision notes to per-screen regens instead of rebuilding the world.
Layout-level changes warrant a full regenerate — say so rather than
stretching regen past its contract.

## Debrief mode: `build-lofi debrief` — standalone only

A post-user-test interview: definitionally a human moment, invoked
deliberately after a session. Never runs in pipeline mode.

1. **Confirm context**, one at a time: session date (default today), tester
   name/handle, which flow(s) were tested.
2. **Walk the template**, one section at a time — flow validity (end-to-end?
   where did they pause, backtrack, quit?) · per-screen friction (confused,
   expected, did instead) · screen-draft changes proposed (add/remove/rename/
   re-purpose) · regen requests (with instruction) · open questions for the
   next test.
3. **Stage the notes as evidence** (A-Team adaptation): write the session as
   a new batch `docs/product/input/<YYYY-MM-DD>-lofi-debrief-<slug>/session.md`
   — append-only, one batch per session, never edited after. User-test
   findings are demand-side evidence: `research-synthesis` digests them, jobs
   cite them, `confidence:` moves when a test validates or breaks a job.
4. **Offer inline regens** (all / pick / skip); skipped ones stay recorded in
   the batch. Proposed screen-draft changes route to `design.md`'s owner —
   never auto-edit `design.md` from a debrief.

## Common mistakes

- **Color slipping in.** Use the greyscale baseline or a token-bound target
  role; no raw literals, CSS color names, or undeclared palette utilities. The
  lint catches nested forms such as `ring-offset-red-500`; respect the failure.
- **Overstating fidelity.** Navigation sketches only follow graph links.
  Interactive mode may use local form/state transitions and deterministic
  fixtures, but never production persistence or real backend requests. Use the
  shared runtime; do not create an application framework for a prototype.
- **Mock data drift.** The same persona, the same three projects, on every
  screen. `JOURNEY.md` is the source.
- **Skipping ambiguity handling.** Generic screen names produce vague
  wireframes. Standalone asks; pipeline records and flags — neither ignores.
- **Touching multiple files in regen mode.** Regen Cart → `cart.astro` and
  `LOFI.md` only.
- **Forgetting the sentinel.** Every successful generate/regen touches
  `.lofi-generated`; staleness detection depends on it.
- **Treating the lofi as deliverable UI.** It is a throwaway reference; the
  production UI comes from `spec.md` + the design system, built by dev.

## Red flags — STOP

- `## Screens & flows` validates broken (orphan flow references). Refuse and
  report; the draft gets fixed first.
- More than 3 ambiguous screens. Pipeline: flag for the gate. Standalone:
  push back — the screen draft needs sharpening.
- Anyone asks for color in the lofi's default render. Decline. Greyscale
  enforces flow-validity testing; color lives behind `?palette=`.
- Debrief without a session having happened. Ask: "was there a session, or
  are you starting one?" Don't fabricate notes.
- Lint fails and you're tempted to bypass it. Don't. Fix the leakage.

## Scenario evidence

Follow `<harness>/runner/PROTOTYPES.md` for compile/generate/validate/assess commands.
Keep the full graph and its IDs in design, generated flow data and spec. Build
and inspect the actual prototype in a browser. Save scenario receipts and assess
them: navigation-only validation/recovery stays unverified. Prototype observation
never substitutes for production behavior or pending human studies.
