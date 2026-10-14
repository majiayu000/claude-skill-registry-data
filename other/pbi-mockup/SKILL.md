---
name: pbi-mockup
description: '[Project Management] Use when you need to generate an HTML mockup report from PBI and story artifacts.'
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Give stakeholders a clickable, self-narrating MVP prototype of every story's main-flow UI — by generating a self-contained interactive HTML mock-up file (one per PBI covering all stories) from finalized PBI/story artifacts, styled from the project's reference design docs, existing UI, components, and real domain entity data — before implementation begins, so layout/UX/flow/state gaps surface while changes are still cheap.

**Summary:**

- PRE-implementation preview tool, not a UI builder: run ONLY on finalized PBIs/stories (reviewed, gated); backend-only PBI with no UI sections → skip generation and tell the user; NEVER use for production UI, design specs, or scratch wireframes — why: it previews the wrong thing otherwise.
- **Main pipeline (run in order):** locate PBI/stories (1) → extract UI specs (2) → **[BLOCKING] plan demo flows into flow-specs + one todo each (2b)** → load design system (3) → **[BLOCKING] inventory existing UI + map connected flows (3b)** → load domain entities (3c) → generate the self-contained HTML prototype (4) → save beside the PBI (5) → report (6) → **[BLOCKING] fidelity validation (7)** → **[BLOCKING] demo-quality gate (8)**. The three BLOCKING gates (2b · 3b+7 · 8) must NEVER be skipped.
- Plan first, generate second: enumerate the PBI's main-story/MVP flows into flow-specs and create one todo per flow (Step 2b) BEFORE generating; sign off with a final Demo-Quality review gate (Step 8) auditing the generated prototype.
- Output is exactly ONE self-contained HTML file per PBI (all stories as tabs/sections), inline CSS/JS, no external deps except Google Fonts, saved alongside the PBI artifact as `{pbi-filename}-mockup.html`.
- The mock-up is a **scripted clickable prototype** — each main-story flow clicks through end-to-end ("click X → see Y → move to Z") with guided narration (▶ Play / ⏭ Next / ⏮ Prev / ↺ Reset / ⏏ Exit), an explanation panel, and a visible "⚠ Simulated" banner; interactivity is **scripted/simulated only** (canned transitions, illustrative data) — NEVER real auth, persistence, or backend.
- Fidelity is the whole point — the mock-up must LOOK like the existing app: load the canonical + matched per-app design-system docs (NEW→canonical, REFACTOR→per-app), read real shared/module components for layout patterns, and populate with real domain entity fields and realistic sample data, never Lorem ipsum.
- Render every defined component state (default/loading/empty/error) as toggleable, keep any accompanying prose/captions tech-agnostic (business terms, not framework/CSS class names) per the M1/M2 mandates, even though the rendered HTML may use real class names internally.

**Workflow:**

1. **Locate PBI Artifact** — find PBI + story files in `team-artifacts/pbis/`; read fully
2. **Extract UI Specs** — parse UI Layout/Wireframe, Components, States, Interaction Flow, Acceptance Criteria + priority/rank
   2b. **[BLOCKING] Plan the Demo Flows** — enumerate main-story/MVP flows, author one flow-spec per flow, task tracking one todo per flow BEFORE generating
3. **Load Design System** — baseline + matched per-app design tokens, colors, typography (NEW→canonical, REFACTOR→per-app)
   3b. **[BLOCKING] Inventory Existing UI + Map Connected Flows** — read real shared/module components + map entry/exit flows so the mock-up matches the current system
   3c. **Load Domain Entities** — entity fields, relationships, enums for realistic sample data
4. **Generate HTML** — one self-contained scripted clickable prototype + guided walkthrough matching the app's look and feel
5. **Save** — write `{pbi-filename}-mockup.html` beside the PBI artifact
6. **Report** — path, priority, stories, demo flows, components, states, fidelity + demo-quality verdicts
7. **[BLOCKING] Fidelity Validation** — mock-up matches inventoried UI (tokens/components/layout/connected flows); record PASS/FAIL
8. **[BLOCKING] Demo-Quality Review Gate** — every flow clicks end-to-end, no dead controls, narration + "⚠ Simulated" banner, offline, real data, iframe-safe; record PASS/FAIL

**Key Rules:**

- Ask AI to generate an **interactive HTML mock-up** for UI PBIs; do not stop at an ASCII-only or static mockup — every main-story flow is a scripted clickable prototype with guided narration.
- One HTML file per PBI (all stories shown as sections/tabs)
- Plan the demo flows (Step 2b) BEFORE generating; sign off with the Demo-Quality gate (Step 8) AFTER
- Interactivity is **scripted/simulated only** (canned transitions, illustrative data, "⚠ Simulated" banner) — NEVER real `fetch`/auth/persistence/backend; self-contained so it runs inside the deck's `<iframe srcdoc>`
- Self-contained: inline CSS/JS, no external dependencies except Google Fonts
- **Must resemble the project's current UI** — read existing component templates and page layouts
- Design must be based on project reference design docs: `docs/project-reference/design-system/README.md`, `docs/project-reference/design-system/design-system-canonical.md`, and the matched per-app design-system doc from `docs/project-config.json`
- Match project design system: colors, typography, spacing, BEM naming
- Use **real domain entity fields and realistic sample data** — not Lorem ipsum
- Include component states (default, loading, empty, error)
- Responsive layout with mobile/desktop preview
- Save in same directory as the PBI artifact
- **Tech-agnostic descriptive prose (M1/M2):** See `.claude/skills/shared/sdd-artifact-contract.md` → "AI-SDD Mandates (M1-M7)" for BLOCKING criteria. Any narrative, captions, annotations, generation notes, or component/state descriptions accompanying the mock-up describe components and states by business/observable terms (e.g., "status indicator", "record list", "loading placeholder"), NOT by framework component names or CSS class names. The rendered HTML itself may use real class names internally (that is implementation, not prose), but the human-readable descriptions stay tech-agnostic per `docs/project-reference/spec-principles.md` §3.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# PBI HTML Mockup Generator

Generate visual HTML mockup reports from PBI and user story artifacts.

---

## When to Use

- After PBI and stories are finalized (reviewed, challenged, gated)
- Before moving to implementation planning or design spec
- When stakeholders need a visual preview of the feature
- As the final step in `workflow-idea-to-pbi` and similar workflows

**NOT for**: Implementing production UI (use `$feature-implement`), creating design specs (use `$design-spec`), or wireframing from scratch (use `$design-spec --mode=wireframe`).

---

## Quick Reference

### Input

| Source          | Path                                                    |
| --------------- | ------------------------------------------------------- |
| PBI artifact    | `team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md`            |
| Story artifacts | `team-artifacts/pbis/stories/{YYMMDD}-us-{pbi-slug}.md` |
| Explicit path   | User provides path as argument                          |

### Output

| Type        | Path                                           |
| ----------- | ---------------------------------------------- |
| HTML mockup | `{same-dir-as-pbi}/{pbi-filename}-mockup.html` |

### Related

- **Input from:** `$refine`, `$story`
- **Command:** `$pbi-mockup`
- **Next Step:** `$prioritize`, `$design-spec`, `$plan`

---

## Detailed Workflow

### Step 1: Locate PBI Artifact

1. If argument provided, use it as path
2. Otherwise, find most recent PBI: `Glob("team-artifacts/pbis/*-pbi-*.md")` sorted by modification time
3. Read the PBI artifact fully
4. Check for associated stories: `Glob("team-artifacts/pbis/stories/*-us-{pbi-slug}*.md")`
5. Read all story artifacts if found

### Step 2: Extract UI Specifications

From the PBI and story artifacts, extract:

| Section                            | What to Extract                                                                                                                                         |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `## UI Layout` / `## UI Wireframe` | ASCII wireframe, layout description                                                                                                                     |
| `### Components`                   | Component names, behaviors, tiers                                                                                                                       |
| `### States`                       | Default, Loading, Empty, Error states                                                                                                                   |
| `### Interaction Flow`             | User actions and system responses                                                                                                                       |
| `## Acceptance Criteria`           | GIVEN/WHEN/THEN scenarios for context                                                                                                                   |
| `## Description`                   | User role, capability, business value                                                                                                                   |
| frontmatter `priority` / `rank`    | PBI priority label + numeric rank — render in the header (Step 4). MANDATORY when present; the mockup MUST carry the same priority info as the backlog. |

If no UI sections exist (backend-only PBI), inform user and skip mockup generation:

> "This PBI has no UI sections (marked as backend-only). No mockup generated."

### Step 2b: [BLOCKING] Plan the Demo Flows (think → plan → many todos BEFORE generating)

> **[BLOCKING] Do NOT generate the mock-up until every main-story flow is planned as a flow-spec and a todo exists per flow.** The mock-up is a clickable, self-narrating prototype of the PBI's main user-story happy paths — plan the journeys first, generate second.

1. **Enumerate the main-story / MVP flows** — from `### Interaction Flow`, the `## Acceptance Criteria` GIVEN/WHEN/THEN scenarios, and each story's "As a / I want / So that". One flow per main user story (MVP happy path) — not every edge case.
2. **Author one flow-spec per flow** — fill the `references/interactive-demo.md` §1 schema: `id`, business-language `title`, `persona`, `trigger`, ordered `steps[]` where each step = `{ action: "user clicks/selects/types X", result: "screen/state Y appears", explain: "plain-language why" }`, and `endState`. The `explain`/`title` prose stays tech-agnostic (business terms, not class names) per M1/M2.
3. **task tracking one todo per flow** — so each journey is generated and later verified (Step 8) individually; add the Step 8 Demo-Quality review as the final todo.

> See `references/interactive-demo.md` §1 for the flow-spec schema + a worked example.

### Step 3: Load Design System Context

1. Read PBI `module` field from frontmatter
2. Load design system docs dynamically (project-config.json + glob fallback). The HTML mock-up design must be based on these project reference design docs:
    - **Mandatory baseline:** Read `docs/project-reference/design-system/README.md` and `docs/project-reference/design-system/design-system-canonical.md`
    - **Primary:** Read top-level `designSystem` in `docs/project-config.json`: use `designSystem.docsPath` + `designSystem.canonicalDoc`, then match the PBI/app context against `designSystem.appMappings[]` to select the per-app doc. Do NOT look for `designSystem` on module entries.
    - **Fallback:** `Glob("docs/project-reference/design-system/*.md")` → match module name against discovered file names (case-insensitive substring match)
    - **Default:** If no match found, use `docs/project-reference/design-system/README.md`
    - **Triage rule (NEW vs REFACTOR):** For NEW pages/components → load `designSystem.canonicalDoc` from top-level `project-config.json` (single source of truth for new code). For REFACTOR of existing screens → load the matched per-app doc via top-level `designSystem.appMappings` (current-state inventory).

3. Extract from design system docs (read enough of the canonical and matched per-app docs to apply the rules):
    - **Colors:** Primary, secondary, accent, background, text colors
    - **Typography:** Font families, sizes, weights
    - **Spacing:** Margin/padding scale
    - **Border radius:** Component roundness
    - **Shadows:** Elevation levels

4. Optionally read `docs/project-reference/scss-styling-guide.md` (first 100 lines) for BEM patterns

### Step 3b: [BLOCKING] Inventory Existing UI + Map Connected Flows (match current system UI)

> **[BLOCKING] Do NOT generate the mockup until this inventory + connected-flow map is done** (canonical: `SYNC:existing-ui-research`). The mockup must faithfully match the current UI system, not generic HTML.

The mockup should resemble the project's actual UI, not generic HTML. Discover existing components AND map the flows that connect to this screen:

1. Read `docs/project-reference/frontend-patterns-reference.md` (first 200 lines) — extract base component classes, common UI patterns, form patterns, table/grid patterns, dialog/modal patterns
2. Glob the project's shared component library (if exists):
    - `Glob("**/libs/*common*/**/*.component.ts")` or `Glob("**/shared/**/*.component.ts")` — discover reusable components (buttons, tables, forms, dialogs, filters, status badges)
    - Read 2-3 key component files to understand their HTML template structure and CSS class naming
3. Glob the module's own components (if PBI module detected):
    - Search for existing page components in the module to understand the current UI layout patterns
    - Read 1-2 existing page templates to capture the actual look and feel (sidebar layout, toolbar patterns, card grids, etc.)
4. Extract from discovered components:
    - **Layout patterns:** Sidebar + content, full-width, split-panel, tabbed
    - **Common components:** Table with pagination, filter bar, action buttons, status chips, breadcrumbs
    - **Form patterns:** Form groups, validation display, multi-step forms
    - **Navigation:** Tab bars, breadcrumbs, sidebar menus
5. **Map connected feature flows** — identify every existing feature/screen that links to, embeds, includes, or navigates to/from this new screen; note the entry/exit flows so the mockup fits the surrounding navigation, not just a standalone page.

> **Key principle:** Mimic existing system UI. If the project has a table with specific column patterns, use that pattern. If it has card-based layouts, use cards. The mockup should feel like it belongs in the existing application.

### Step 3c: Load Domain Entity Context

Use real domain entities and relationships for realistic mockup data:

1. Read `docs/project-reference/domain-entities-reference.md` (if exists) — extract entities, fields, relationships for the PBI's module
2. From the PBI artifact, extract referenced entities from `## Domain Context` section
3. Use entity field names and types to generate **realistic sample data** in the mockup:
    - Entity names → table column headers, form field labels
    - Entity relationships → navigation links, dropdowns, nested displays
    - Entity statuses/enums → status badges, filter options
    - Date fields → realistic date values
    - String fields → domain-appropriate sample text (customer names, invoice titles, etc.)

> **Key principle:** Sample data should use actual entity field names and realistic domain values — not "Lorem ipsum" or "Item 1, Item 2".

### Step 4: Generate HTML Mockup

Generate a **single self-contained HTML file** with the following structure:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Mockup: {PBI Title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
        <style>
            /* Design system tokens as CSS variables */
            /* Component styles matching project BEM conventions */
            /* Responsive breakpoints */
            /* Dark/light theme support */
        </style>
    </head>
    <body>
        <!-- PBI Header: title, description, metadata -->
        <!-- Navigation tabs (one per story) -->
        <!-- Story sections with mockup UI -->
        <!-- Component state toggles (default/loading/empty/error) -->
        <!-- Interactive prototype: screens/states + hotspots + demo control bar + explanation panel + "⚠ Simulated" banner -->
        <script>
            /* Tab navigation */
            /* State toggles */
            /* Theme toggle */
            /* Responsive preview toggle */
            /* Prototype engine: goTo(stateId) router + hotspots + simulated submit — see references/interactive-demo.md §2 */
            /* Guided walkthrough: ▶ Play ⏭ Next ⏮ Prev ↺ Reset ⏏ Exit — see references/interactive-demo.md §3 */
        </script>
    </body>
</html>
```

#### Interactive Prototype + Guided Walkthrough

The mock-up is a **scripted clickable prototype** of each planned flow (Step 2b), not a still image. For EVERY flow-spec, render the journey so a stakeholder can click through it and watch it narrate. Mechanics are delegated — do NOT inline the engine here:

1. **Screen/state router + hotspots** — render each flow's screens/states as DOM sections and wire clickable hotspots that `goTo` the next state (`references/interactive-demo.md §2`). Simulated submit → success toast → in-memory row insert; NO real `fetch`/persistence/backend.
2. **Demo controls + guided walkthrough** — a control bar (`▶ Play · ⏭ Next · ⏮ Prev · ↺ Reset · ⏏ Exit`) auto-/step-walks the flow, spotlighting the active hotspot (`references/interactive-demo.md §3`).
3. **Explanation panel + "⚠ Simulated" banner** — a persistent panel names the current flow + step (`n / total`) + the step's plain-language `explain`; a visible "⚠ Simulated — illustrative data, no real actions are performed" banner is the scope guard (`references/interactive-demo.md §4`).
4. **Affordances + a11y** — hotspots visibly highlighted (pulse/outline), disabled controls show a tooltip, demo never traps the user, `prefers-reduced-motion` respected (`references/interactive-demo.md §5`).

> **Scope guard:** interactivity is **scripted/simulated only** (canned transitions, illustrative data) — never real auth, persistence, or backend calls; self-contained so it runs inside the deck's `<iframe srcdoc>` sandbox (`references/interactive-demo.md §6`).

#### Design-Principles Build Constraints (real markup, not advice)

The 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`, the `SYNC:ui-ux-design-principles` block below) are BUILD CONSTRAINTS on the emitted HTML/CSS — the mock-up must actually DO these, not merely describe them. Project design-system tokens outrank the clause defaults; a genuine conflict goes to the user, NEVER resolved silently.

1. **Build the empty, loading and error views FIRST (`UI-1.5`)** — author those three state panels BEFORE the populated one and wire each into the state toggle (Default | Loading | Empty | Error) so a stakeholder can click into them. A story panel rendering only the populated view is incomplete.
2. **Real focus rings (`UI-5.5`)** — every focusable control keeps a VISIBLE `:focus-visible` outline in the emitted CSS. `outline: none` with no replacement ring is a build defect; tab through each flow before the Step 8 gate.
3. **All 5 interaction states as real CSS (`UI-5.2`)** — `:hover`, `:focus-visible`, `:active`, `[disabled]` and the default rule exist for every button, link, input, tab and hotspot; disabled controls are visibly muted AND non-interactive, not merely unbound.
4. **Real 44×44pt touch targets (`UI-8.1`, `UI-8.2`)** — every tappable element carries a `min-width`/`min-height` of at least 44px (the hit area may exceed the visible icon) with ≥8px separation, in the responsive/mobile preview as well as desktop; primary actions sit in the bottom third of the mobile viewport.
5. **Reserved space for anything that loads (`UI-9.3`, `UI-9.1`)** — images, avatars, charts and skeletons carry explicit width/height or aspect-ratio so switching Default ↔ Loading NEVER shifts the layout; skeletons for known layouts, spinners only for unknown waits.
6. **Declared scales emitted as CSS variables (`UI-2.5`, `UI-4.1`)** — the type scale as 6 named custom properties and the spacing scale from ONE 4px or 8px base; every `font-size`, `padding`, `margin` and `gap` references a variable. Hard-coded one-off px values are a build defect.
7. **Measured contrast (`UI-3.1`, `UI-3.2`, `UI-3.3`)** — text ≥4.5:1 and UI edges/borders ≥3:1 against their ACTUAL backgrounds in BOTH themes, one accent with one job, and status chips / validation states pair colour with an icon or text label so colour never carries the meaning alone.
8. **Body type and measure (`UI-2.2`, `UI-2.3`)** — body text 16px (17px in the mobile preview) and never below 14px for readable content; prose columns constrained to a 45–75 character measure.
9. **Motion budget (`UI-5.4`)** — transitions 150–250ms ease-out, and the guided walkthrough honours `prefers-reduced-motion` (already required by the prototype a11y rule above).
10. **Forms (`UI-7.2`, `UI-7.3`, `UI-7.5`)** — visible labels on every input (placeholders are hints, NEVER labels); the error state shows the message beside its field with a fix instruction; simulated navigation between demo steps preserves entered values.

#### HTML Structure Requirements

1. **Header Section:**
    - PBI ID and title
    - Module badge
    - **Priority badge** — the PBI's priority label + numeric rank from frontmatter (e.g. "Priority: Must Have · Rank #2"). MANDATORY when the PBI carries `priority`/`rank`; the mockup MUST surface the same priority info as the backlog so stakeholders see it on the prototype itself. Omit only when the PBI genuinely has no priority assigned yet.
    - Story count summary
    - Generation date

2. **Navigation:**
    - Tab bar with one tab per story (or section per PBI acceptance criteria)
    - Active tab highlight using design system primary color

3. **Story Panels:**
    - Story title and description ("As a... I want... So that...")
    - Visual mockup of the UI described in wireframe/layout sections
    - Component placeholders with realistic sample data
    - State toggle buttons (Default | Loading | Empty | Error)

4. **Footer:**
    - "Generated from PBI {ID}" attribution
    - Link back to artifact path
    - Generation timestamp

#### Styling Rules

- Base every visual decision on the loaded project reference design docs; cite the docs used in the generation notes when reporting the mock-up.
- Use CSS custom properties (variables) from design system tokens
- Follow BEM naming: `mockup__header`, `mockup__nav`, `mockup__panel`
- Match the project's color palette, typography, and spacing
- Include both light and dark theme (toggle button in header)
- Responsive: mobile (< 768px) and desktop layout — mobile must stay usable: reflow where possible (stack rows, collapse grids to one column); where a block genuinely can't reflow (tables, wide grids) give it `overflow: auto` scroll rather than letting it clip; nothing broken or cut off
- Use realistic placeholder data (names, dates, numbers) — not "Lorem ipsum"

#### Component Rendering

Map wireframe components to HTML elements AND to their scripted demo interaction (the hotspot/transition that advances the flow — `references/interactive-demo.md §2`):

| Wireframe Component | HTML Rendering                             | Demo Interaction (scripted/simulated)                     |
| ------------------- | ------------------------------------------ | --------------------------------------------------------- |
| Table/Grid          | `<table>` with design system styles        | Row click → `goTo` detail screen/state                    |
| Form                | `<form>` with labeled inputs               | Submit → simulated success toast + in-memory row insert   |
| Button              | `<button>` with primary/secondary variants | Hotspot → advances the demo to the next screen/state      |
| Card                | `<div class="card">` with shadow           | Card click → `goTo` the card's detail screen/state        |
| List                | `<ul>` or data list                        | Item click → `goTo` selected-item screen/state            |
| Modal/Dialog        | Overlay `<div>` (toggleable)               | Trigger → open dialog state; confirm/cancel → `goTo` next |
| Tab panel           | Tab navigation with content panels         | Tab → switch panel (no nav away)                          |
| Search/Filter       | Input with icon                            | Apply → simulated filtered result state                   |
| Status badge        | `<span>` with color coding                 | Non-interactive (illustrative state indicator)            |
| Empty state         | Centered message with icon                 | Primary CTA → `goTo` the create/first-action screen/state |
| Loading state       | Skeleton placeholder or spinner            | Transient → auto-advances to the loaded screen/state      |
| Error state         | Error banner with message                  | Retry → `goTo` back to the prior screen/state             |

### Step 5: Save HTML File

- **Path:** Same directory as the PBI artifact
- **Name:** `{pbi-filename-without-ext}-mockup.html`
- Example: `team-artifacts/pbis/260324-pbi-goal-tracking-mockup.html`

### Step 6: Report to User

After generation, output:

```
Mockup generated: {path}
- PBI priority: {priority label} · Rank #{rank}  (or "not yet prioritized")
- Stories covered: {count}
- Demo flows: {count} ({flow titles})
- Components rendered: {list}
- States included: {default, loading, empty, error}
- Fidelity vs existing UI: PASS | FAIL
- Demo quality: PASS | FAIL

Open in browser to preview. Click highlighted hotspots or press ▶ Play to walk a flow. Use theme toggle for dark/light mode.
```

---

### Step 7: [BLOCKING] Fidelity Validation — Mockup Matches Existing UI

> **[BLOCKING] After the HTML is generated, validate it faithfully matches the existing UI inventoried in Step 3b before handing off.** Do NOT report the mockup as done until this validation records a result — a mockup that does not match the current system is not done.

Validate the produced mockup against the inventoried existing UI and record an explicit pass/fail:

1. **Design tokens** — colors, typography, spacing match the project design system (Step 3).
2. **Component patterns** — tables, forms, dialogs, status chips, and navigation reuse the existing component patterns (Step 3b), not generic HTML.
3. **Layout/structure** — the screen layout matches the existing pages of the related feature (sidebar / toolbar / card-grid conventions).
4. **Connected flows** — entry/exit navigation matches the connected feature flows mapped in Step 3b.

Record the outcome in the Step 6 report:

```
Fidelity vs existing UI: PASS | FAIL — tokens / components / layout / flows matched? If FAIL: what diverged + the fix.
```

If **FAIL**, revise the mockup to match the existing UI and re-validate before handoff.

---

### Step 8: [BLOCKING] Demo-Quality Review Gate

> **[BLOCKING] This is the final review todo (Step 2b created it).** After fidelity passes, audit the GENERATED interactive prototype's demo quality before handoff. Do NOT report the mock-up as done until this records a result — a prototype with a dead control or a flow that does not click through is not done. Full checklist: `references/interactive-demo.md §7`.

**First, confirm the result SATISFIES the PBI's intent** (not merely that it renders): every main user story in the PBI's `## Acceptance Criteria` / `### Interaction Flow` is represented by a flow-spec demo (coverage — no main story missing), AND each prototype faithfully demonstrates that story's intended behavior end-to-end. Then audit the produced prototype against every planned flow-spec and record an explicit pass/fail:

0. **Satisfies the PBI intent** — every main-story/MVP flow from the acceptance criteria is present and its demo conveys the intended behavior; if a story has no demo or the demo misrepresents it, this gate FAILS regardless of the items below.
1. **Every main-story flow clicks end-to-end** — each flow's `steps[]` reach its `endState` via real hotspots; no path dead-ends.
2. **No dead controls** — every button/hotspot advances the demo or is visibly disabled-with-tooltip.
3. **Narration present + tech-agnostic** — every step shows its plain-language `explain`; copy is business-language (M1/M2), not class names; the "⚠ Simulated — illustrative data, no real actions are performed" banner is visible on every flow.
4. **Opens offline standalone** — no external `<script src>`; Google Fonts CSS only; no JS console errors.
5. **Real domain data** — screens/rows use real entity field names + realistic values, never Lorem ipsum.
6. **iframe-safe** — works self-contained inside an `<iframe srcdoc>` sandbox (no parent-document or network dependency) so the deck can embed it.

Record the outcome in the Step 6 report:

```
Demo quality: PASS | FAIL — satisfies PBI intent (every main story demoed + faithful) / flows click end-to-end / no dead controls / narration tech-agnostic + banner / offline / real data / iframe-safe? If FAIL: what broke + the fix.
```

If **FAIL**, fix the prototype (re-author from the flow-spec — cheap) and re-audit before handoff.

---

## Mockup Quality Checklist

Before completing:

- [ ] HTML file is self-contained (opens correctly without a server)
- [ ] All stories from PBI are represented as sections/tabs
- [ ] Every main-story flow (Step 2b) is rendered as a scripted clickable prototype with guided narration
- [ ] Design is based on `design-system-canonical.md` plus the matched per-app design-system doc when available
- [ ] Design system colors and typography match the project
- [ ] Component states are toggleable (where defined in artifact)
- [ ] Responsive layout works for mobile and desktop — usable on small screens with nothing clipped/cut-off/unreachable (reflow preferred; `overflow: auto` scroll acceptable where a block can't reflow)
- [ ] Realistic placeholder data used (not Lorem ipsum)
- [ ] PBI metadata shown in header (ID, title, module, date)
- [ ] PBI priority shown in header (priority label + numeric rank from frontmatter) when the PBI is prioritized — the mockup carries the same priority info as the backlog
- [ ] File saved alongside the PBI artifact
- [ ] Fidelity validation (Step 7) recorded PASS — mockup matches existing UI tokens, components, layout, and connected flows
- [ ] Demo-Quality gate (Step 8) recorded PASS — every flow clicks end-to-end, no dead controls, narration + "⚠ Simulated" banner present, offline, iframe-safe
- [ ] Design-Principles build constraints hold — `UI-1.5` empty/loading/error panels BUILT and toggleable, `UI-5.5` visible focus ring on every focusable control, `UI-5.2` all 5 interaction states in real CSS, `UI-8.1`/`UI-8.2` real ≥44×44px touch targets 8px apart with bottom-third primaries in the mobile preview, `UI-9.3` reserved space so state switches never shift layout, `UI-2.5`/`UI-4.1` 6-step type scale + ONE 4/8px spacing unit emitted as CSS variables, `UI-3.1`/`UI-3.3` contrast measured 4.5:1 text / 3:1 edges in both themes and colour never the sole carrier of meaning

---

## Edge Cases

| Scenario                          | Handling                                                |
| --------------------------------- | ------------------------------------------------------- |
| Backend-only PBI (no UI sections) | Skip mockup, inform user                                |
| No stories yet (PBI only)         | Generate HTML mock-up from PBI's UI Layout section only |
| Multiple modules                  | Load primary module's design system                     |
| No design system docs             | Use sensible defaults (Inter font, neutral palette)     |
| Very large PBI (10+ stories)      | Group stories into categories, use collapsible sections |

---

## Anti-Patterns

| Anti-Pattern                                              | Correct Approach                                                                                                                           |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Production-quality CSS framework                          | Simple inline CSS matching design tokens                                                                                                   |
| External dependencies (CDN libs)                          | Self-contained except Google Fonts                                                                                                         |
| Pixel-perfect implementation                              | Approximate visual representation                                                                                                          |
| Real backend/business logic (auth, live API, persistence) | Scripted/simulated prototype interactivity only — clickable nav, simulated transitions, guided demo; NO real business logic or data writes |
| Dead / non-wired buttons                                  | Every control either advances the demo or is visibly disabled-with-tooltip                                                                 |
| Lorem ipsum placeholder text                              | Realistic domain-specific sample data                                                                                                      |

---

## Workflow Recommendation

> **MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS:** If you are NOT already in a workflow, you MUST ATTENTION use ask the user directly to ask the user. Do NOT judge task complexity or decide this is "simple enough to skip" — the user decides whether to use a workflow, not you:
>
> 1. **Activate `workflow-idea-to-pbi` workflow** (Recommended) — includes mockup as final step
> 2. **Execute `$pbi-mockup` directly** — run this skill standalone on an existing PBI

---

## Next Steps

**MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS** after completing this skill, you MUST ATTENTION use ask the user directly to present these options. Do NOT skip because the task seems "simple" or "obvious" — the user decides:

- **"$prioritize (Recommended)"** — Prioritize the PBI in the backlog
- **"$design-spec"** — Create detailed design specification from mockup
- **"$plan"** — Start implementation planning
- **"Skip, continue manually"** — user decides

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting.

> **Evidence Gate:** MANDATORY IMPORTANT MUST ATTENTION — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

<!-- SYNC:existing-ui-research -->

> **[BLOCKING] Understand the existing UI before you design or spec a new/updated screen.** Before producing any wireframe, mockup, screen design, or UI spec:
>
> 1. **Inventory existing related UI** — search the project for screens, pages, and components already serving this feature or its domain (consult design-system docs + the real component inventory).
> 2. **Map connected flows** — identify every feature that links to, embeds, includes, or navigates to/from the new screen; trace its entry and exit flows so the new screen fits them.
> 3. **Reuse before invent** — prefer existing components, patterns, and layout conventions; justify any new component against what already exists.
> 4. **Record findings** — note the matched existing screens/components + connected flows in the artifact so downstream design faithfully matches the current UI system.
>
> **Skip ONLY** when the feature is backend-only (no UI) — state that explicitly.

<!-- /SYNC:existing-ui-research -->

<!-- SYNC:ui-ux-design-principles -->

> **UI/UX Design Principles (Rev 1.0 — 40 clauses, web + mobile)** — the working rule set for ANY task that designs, plans, implements, or reviews a user interface. Applies to BOTH platforms unless a clause names one (§8 is mobile/touch). Cite clauses by ID: `UI-3.1`, `UI-8.2`.
>
> **Precedence:** project design-system / SCSS / frontend-pattern docs OUTRANK these clauses; these clauses outrank generic taste. A genuine conflict is SURFACED to the user with both sides — NEVER resolved silently. — why: the project's own recorded decision is the authority; these clauses are the default when it is silent.
>
> **1.0 Visual Hierarchy & Layout**
>
> - `UI-1.1` One focal point per screen. Two elements competing for first read → demote one.
> - `UI-1.2` Signal order: size → weight → colour → position. Use the cheapest signal that works before adding another.
> - `UI-1.3` Group by proximity, NEVER by border. Whitespace separates cleanly; boxes inside boxes do not.
> - `UI-1.4` Align to a shared edge. Every unexplained indent reads as an accident.
> - `UI-1.5` Design the empty, loading and error state FIRST. The full state is the easy one.
>
> **2.0 Typography**
>
> - `UI-2.1` Max 2 families, 3 weights each. More variety reads as inconsistency, not range.
> - `UI-2.2` Body text 16px web, 17px mobile. NEVER below 14px for anything a user must read.
> - `UI-2.3` Line length 45–75 characters. Constrain the measure, not the container.
> - `UI-2.4` Leading scales inversely with size: 1.5 body, 1.1–1.2 display.
> - `UI-2.5` Fixed type scale — 6 named steps shared with engineering. NEVER one-off sizes.
>
> **3.0 Colour & Contrast**
>
> - `UI-3.1` Contrast 4.5:1 text, 3:1 UI edges. Measure it — NEVER judge by eye on a bright screen.
> - `UI-3.2` One accent, one job. An accent that is everywhere points at nothing.
> - `UI-3.3` Colour NEVER carries meaning alone — pair it with an icon, label or position.
> - `UI-3.4` Dark mode is NOT inverted light mode. Lift surfaces to signal elevation; soften pure-white text.
>
> **4.0 Spacing & Grid**
>
> - `UI-4.1` One spacing unit, multiplied — 4px or 8px base; every gap a multiple of it.
> - `UI-4.2` Space belongs to the container, not the child. Use `gap`; reserve margins for exceptions.
> - `UI-4.3` Tighter inside, looser between — inner padding always smaller than the gap to the next group.
> - `UI-4.4` Breakpoints follow content, not devices. Break where the layout stops working.
>
> **5.0 Interaction & Feedback**
>
> - `UI-5.1` Every action gets a response under 100ms, even when the result takes longer.
> - `UI-5.2` Specify all 5 states — default, hover, focus, active, disabled — plus loading where it applies.
> - `UI-5.3` Prefer undo over confirmation. Confirm ONLY what cannot be reversed.
> - `UI-5.4` Motion clarifies cause and effect: 150–250ms, ease-out, honours reduced-motion.
> - `UI-5.5` Keep the visible focus ring. Restyle it if it clashes; NEVER remove it.
>
> **6.0 Navigation & IA**
>
> - `UI-6.1` Every screen answers: where am I, what's here, where next.
> - `UI-6.2` Max 5 top-level destinations. Depth beats a crowded first level.
> - `UI-6.3` Label by the user's word, not the internal one. Team vocabulary is not a taxonomy.
> - `UI-6.4` Every state deserves a URL or a back path. Deep links and hardware back must land somewhere sensible.
>
> **7.0 Forms & Input**
>
> - `UI-7.1` Ask for less. Every field needs a reason it exists today.
> - `UI-7.2` Labels stay visible. Placeholders are hints, NEVER labels.
> - `UI-7.3` Validate on blur, not on keystroke. Errors sit next to the field and say how to fix it.
> - `UI-7.4` Match keyboard to data type — correct input type, autocomplete and autocapitalise on every field.
> - `UI-7.5` NEVER lose entered data. Preserve input across errors, navigation and refresh.
>
> **8.0 Mobile & Touch** _(mobile/touch surfaces)_
>
> - `UI-8.1` Hit target ≥44×44pt, 8px apart. The target may exceed the visible icon.
> - `UI-8.2` Primary actions in the bottom third — that is where the thumb lives.
> - `UI-8.3` Gestures are shortcuts, NEVER the only route. Anything swipeable is also tappable.
> - `UI-8.4` Respect safe areas and the keyboard. Notch, home indicator and on-screen keyboard all steal space.
>
> **9.0 Speed & Perceived Speed**
>
> - `UI-9.1` Show structure before data — skeletons for known layouts, spinners only for unknown waits.
> - `UI-9.2` Assume success optimistically. Update UI first, reconcile after, roll back visibly on failure.
> - `UI-9.3` Reserve space for anything that loads. Images, ads and fonts must NEVER shift the layout.
> - `UI-9.4` Design for the slow connection. Offline, timeout and retry are states, NOT edge cases.
>
> **Apply by role** — the clauses are one set; what you DO with them depends on the task:
>
> | Role                                | Obligation                                                                                                                                                              |
> | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | DESIGN / PLAN a surface             | Clauses shape the artifact: empty/loading/error specified first (`UI-1.5`), all 5 states enumerated (`UI-5.2`), type scale + spacing unit declared (`UI-2.5`, `UI-4.1`) |
> | IMPLEMENT a component               | Pre-completion gate: states · tokens · contrast · focus ring · touch target · reserved space (`UI-5.2`, `UI-2.5`/`UI-4.1`, `UI-3.1`, `UI-5.5`, `UI-8.1`, `UI-9.3`)      |
> | REVIEW UI code or a design artifact | Each clause is a fail-condition; every finding cites `UI-<clause>` + `file:line` + severity. NEVER a tick-box sweep — one focused pass per section                      |
> | SCAN / document a UI system         | Record where the PROJECT deliberately deviates, so the overriding doc becomes the recorded authority                                                                    |
>
> **Skip ONLY** when the change has no user-facing surface (backend-only, tooling, docs) — state that explicitly so the skip is auditable, not an omission.

<!-- /SYNC:ui-ux-design-principles -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:ui-ux-design-principles:reminder -->

- **MUST ATTENTION** apply the 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`) to any user-facing surface: one focal point, proximity grouping, empty/loading/error designed FIRST (§1) · ≤2 families, 16px web / 17px mobile body, never <14px, 45–75ch, fixed 6-step scale (§2) · 4.5:1 text / 3:1 edges measured, one accent, colour never alone, dark mode ≠ inversion (§3) · one 4/8px unit, `gap` over margins, tighter-inside-looser-between, content-driven breakpoints (§4) · <100ms response, all 5 states, undo over confirm, 150–250ms ease-out honouring reduced-motion, visible focus ring (§5) · where-am-I/what's-here/where-next, ≤5 top-level destinations, user's words, URL or back path (§6) · fewer fields, visible labels, validate on blur, matched keyboard, NEVER lose input (§7) · ≥44×44pt targets 8px apart, bottom-third primaries, gestures never the only route, safe areas (§8) · structure before data, optimistic update with visible rollback, reserved space, slow-connection states (§9). Project design-system docs OUTRANK these clauses — a genuine conflict goes to the user, NEVER resolved silently. Cite every finding as `UI-<clause>` + `file:line`. Skip ONLY for changes with no user-facing surface, stated explicitly.

<!-- /SYNC:ui-ux-design-principles:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Give stakeholders a clickable, self-narrating MVP prototype of every story's main-flow UI — built from real domain data and the project's actual design system — before implementation begins, so layout/UX/flow/state gaps surface while changes are still cheap.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Critical Thinking:** MUST ATTENTION traced proof per claim, confidence >80% to act, NEVER guess.

**IMPORTANT MUST ATTENTION** run ONLY on finalized PBIs/stories (reviewed, challenged, gated); for a backend-only PBI with no UI sections, SKIP generation and tell the user — never fabricate UI — why: a mock-up of an unfinished or UI-less PBI previews the wrong thing.
**IMPORTANT MUST ATTENTION** run the FULL step pipeline in order — locate (1) → extract UI (2) → plan flows [BLOCKING] (2b) → load design system (3) → inventory existing UI [BLOCKING] (3b) → load domain entities (3c) → generate HTML (4) → save (5) → report (6) → fidelity validation [BLOCKING] (7) → demo-quality gate [BLOCKING] (8); NEVER skip the three BLOCKING gates (2b plan · 3b inventory + 7 fidelity · 8 demo-quality) — why: each guards a distinct failure (no plan → incomplete demo; no inventory/fidelity → generic-HTML mismatch; no demo-quality audit → dead controls ship).
**IMPORTANT MUST ATTENTION** PLAN the demo flows BEFORE generating — Step 2b enumerates the PBI's main-story/MVP flows into flow-specs and task trackings one todo per flow; Step 8 [BLOCKING] Demo-Quality gate signs off AFTER — why: think → plan → many todos → generate → final review is the discipline that makes the prototype complete and click-through-verified.
**IMPORTANT MUST ATTENTION** render each main-story flow as a **scripted clickable prototype** with guided narration (▶ Play · ⏭ Next · ⏮ Prev · ↺ Reset · ⏏ Exit), an explanation panel, and a visible "⚠ Simulated — illustrative data, no real actions are performed" banner; interactivity is **scripted/simulated only** (canned transitions) — NEVER real `fetch`/auth/persistence/backend; self-contained so it runs inside the deck's `<iframe srcdoc>` (mechanics: `references/interactive-demo.md §2–§4`) — why: a clickable prototype conveys behavior at the lowest cost, but a real backend breaks the offline preview-before-code purpose.
**IMPORTANT MUST ATTENTION** emit exactly ONE self-contained HTML file per PBI (all stories as tabs/sections), inline CSS/JS, no external deps except Google Fonts, saved as `{pbi-filename}-mockup.html` beside the PBI artifact — why: stakeholders open one file with no server, no build step.

**IMPORTANT MUST ATTENTION** the 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`) are BUILD CONSTRAINTS on the emitted HTML/CSS, not prose advice — build the empty/loading/error panels FIRST and make them toggleable (`UI-1.5`), emit all 5 interaction states as real CSS with a VISIBLE focus ring (`UI-5.2`, `UI-5.5`), real ≥44×44px touch targets 8px apart with bottom-third primaries in the mobile preview (`UI-8.1`, `UI-8.2`), reserved space so a state switch never shifts layout (`UI-9.3`), the 6-step type scale (`UI-2.5`) and ONE 4/8px spacing unit (`UI-4.1`) emitted as CSS variables with no one-off px values, and contrast MEASURED 4.5:1 text / 3:1 edges in both themes with colour never carrying meaning alone (`UI-3.1`, `UI-3.3`) — why: a mock-up that only describes these previews a quality the built UI will not have.

**IMPORTANT MUST ATTENTION** render the PBI's priority in the header (priority label + numeric rank from frontmatter) whenever the PBI is prioritized — why: the mockup is a stakeholder-facing prototype and MUST carry the same priority info as the backlog, not just the title; downstream `feature-presentation` reuses it.

**MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting; add a final review todo to verify quality.
**MANDATORY IMPORTANT MUST ATTENTION** validate route/next-step decisions with the user by asking the user directly — never auto-decide complexity for the user.

**Domain rules this skill must not skip:**

**IMPORTANT MUST ATTENTION** fidelity is the whole point — the mock-up must LOOK like the existing app: load the mandatory baseline + matched per-app design-system docs (NEW→`designSystem.canonicalDoc`, REFACTOR→matched `designSystem.appMappings` per-app doc), read real shared/module components for layout patterns — why: a generic-HTML mock-up previews a system that does not exist.
**IMPORTANT MUST ATTENTION** populate with real domain entity field names and realistic sample data — NEVER Lorem ipsum or "Item 1, Item 2" — why: fake data hides the real layout/overflow/state gaps the preview exists to surface.
**IMPORTANT MUST ATTENTION** render every defined component state (default/loading/empty/error) as a toggleable view — why: stakeholders must see how the UI degrades, not only the happy path.
**IMPORTANT MUST ATTENTION** keep all accompanying prose/captions/notes tech-agnostic (business/observable terms, NOT framework or CSS class names) per the M1/M2 mandates in `.claude/skills/shared/sdd-artifact-contract.md`; the rendered HTML MAY use real class names internally (implementation, not prose) — why: tech-coupled descriptions break the spec-principles §3 contract while the rendered markup stays free to be concrete.
**IMPORTANT MUST ATTENTION** read design-system docs, existing components, and domain-entities reference (`docs/project-reference/*`) BEFORE generating — grep/read 2-3 real components first — why: skipping the read produces a mock-up that looks nothing like the app.

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim/finding (confidence >80% to act, <80% verify first) — NEVER speculate about entity fields, design tokens, or component patterns without reading the source — why: hallucinated fields and class names produce a misleading preview.

**Anti-Rationalization:**

| Evasion                                           | Rebuttal                                                                                                                                                                   |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "PBI looks ready, skip the gated/finalized check" | Run only on reviewed-and-gated PBIs. An unfinished PBI previews the wrong thing.                                                                                           |
| "A static mockup is faster than a clickable one"  | Static conveys layout only, not behavior — the user asked for an MVP demo. Render each flow as a scripted clickable prototype (regenerated from the §1 flow-spec — cheap). |
| "Skip the flow planning, just generate"           | Step 2b (flow-specs + one todo per flow) is BLOCKING; planning the journeys first is what makes the prototype complete and click-through-verifiable.                       |
| "Wire it to a real endpoint so it feels real"     | Interactivity is scripted/simulated only — canned transitions, illustrative data, "⚠ Simulated" banner. NO real `fetch`/auth/persistence/backend.                          |
| "Lorem ipsum is faster"                           | Fake data hides real overflow/state gaps. Use real entity field names + realistic values.                                                                                  |
| "Generic clean HTML is good enough"               | Fidelity is the point — read design-system docs + 2-3 real components, mimic the actual UI.                                                                                |
| "Class names in the notes are fine"               | Prose stays tech-agnostic (M1/M2). Real class names live in the rendered HTML, not captions.                                                                               |
| "Only need the default state"                     | Render every defined state (default/loading/empty/error) as toggleable.                                                                                                    |
| "Already know the entity fields"                  | Show `file:line` from the domain-entities reference. No proof = no read.                                                                                                   |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.

**IMPORTANT MUST ATTENTION Goal:** clickable, self-narrating MVP prototype of every story's main-flow UI from real domain data + the actual design system, BEFORE implementation — so flow/UX/state gaps surface while cheap.
**IMPORTANT MUST ATTENTION** PLAN flows first (Step 2b flow-specs + one todo per flow), then the Demo-Quality gate signs off (Step 8); each flow is a scripted clickable prototype with guided narration + "⚠ Simulated" banner — interactivity scripted/simulated only, NEVER real backend.
**IMPORTANT MUST ATTENTION** ONE self-contained HTML per PBI (Google Fonts only), real domain data not Lorem ipsum, every component state toggleable, prose tech-agnostic (M1/M2).
**IMPORTANT MUST ATTENTION** read design-system docs + real components + domain-entities reference first; cite `file:line` (>80% confidence) — NEVER guess fields or tokens.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
