---
name: ui-design
description: '[Design] Use when a workflow step or the user asks for a UI design (create, describe) or a UI review: content fit, layouts, styling conventions, accessibility, async states. --mode={fast|good|explore|describe|screenshot|video|review}.'
disable-model-invocation: false
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
> **[BLOCKING] Mode routing — detect FIRST.** Explicit `--mode=review` selects the UI review (read-only findings over existing interfaces); explicit `--mode={fast|good|explore|describe|screenshot|video}` selects that design mode; no `--mode` is the default `fast` design (everything below, unchanged). An explicit mode always wins. `$ui-design --mode=review` is the former `/ui-review`: that slash command no longer exists, and the mode works called directly with no workflow. `--mode=review` REPLACES the design spine for the invocation — read `references/mode-review.md` in full before anything else (see [Mode Dispatch](#arguments--mode-dispatch)); the shared steps, design-intelligence search, lane and mode branches below do not run for it.

## Quick Summary

**Goal:** Create (or describe) a UI design using design-intelligence databases and subagents, dispatched by `--mode` (input carrier) × `--lane` (design lane); `--mode=review` instead reviews existing UI for content fit, supported-size layout, styling conventions, layering, accessibility and async states.

**Summary:**

- **Route:** parse `--mode={fast|good|explore|describe|screenshot|video|review}` and `--lane={product|marketing}`; default to `fast` × `product`. `review` replaces the design spine with `references/mode-review.md` (`--lane` does not apply).
- **Spine (BLOCKING order, every design mode — not `review`):** Journey Report (`UX-1`) → design authority read — principles, design system, existing UI (`UX-2`) → design-intelligence search (candidates only) → ingest visual evidence when applicable → low-fi structure walked against the journeys (`UX-7`) → design with `ui-ux-designer` (`DD-3` plan + `UI-*`/`DD-*`) → implement unless `describe` → validate by walking the journeys + traceability (`UX-8`) → report and seek approval.
- **Quality floor:** apply project tokens/components plus `UI-*`/`DD-*`/`CL-*`; design states, interaction feedback, declared scales, measured contrast, touch targets, responsive reflow, and subject-grounded copy before the happy path.
- **Ownership:** the design modes author the visual direction and implementation contract; `--mode=review` owns source findings and review evidence; the local index supplies candidates only.

> **Renamed:** folds the former `/design-fast`, `/design-good`, `/design-describe`, `/design-screenshot`, `/design-video` skills into the same-named value of `--mode={fast|good|explore|describe|screenshot|video}` — those names no longer resolve as slash commands; use `$ui-design --mode=…`.
>
> **Folded review:** the former `/ui-review` is `--mode=review` — that name no longer resolves as a slash command; use `$ui-design --mode=review [scope] [--report-only]`. Its full body lives in `references/mode-review.md`.
>
> **Absorbed lanes:** the former `frontend-design` (marketing/creative) and `interface-design` (product-UI) skills now fold into `--lane={marketing|product}` — those names no longer resolve as slash commands; use `$ui-design --lane=…`. Each lane's full body lives under `references/lane-{marketing,product}/lane-guide.md`.

**Mode dispatch:** `--mode={fast|good|explore|describe|screenshot|video|review}` — default `fast` when omitted.
**Lane dispatch:** `--lane={product|marketing}` — default `product` when omitted. Lane (the design tradition) is orthogonal to mode (the input carrier); any mode combines with any lane.

| Lane                  | Use for                                                                 | Full body |
| --------------------- | ----------------------------------------------------------------------- | --------- |
| `product` (default)   | dashboards, admin panels, SaaS apps, tools, settings, data interfaces   | `references/lane-product/lane-guide.md` |
| `marketing`           | landing pages, marketing sites, campaigns, distinctive creative pieces  | `references/lane-marketing/lane-guide.md` |

| Mode                  | Input carrier               | Output                                                       |
| --------------------- | --------------------------- | ----------------------------------------------------------- |
| `fast` (default)      | text brief                  | quick prototype implementation                              |
| `good`                | text brief                  | immersive, researched, higher-quality implementation        |
| `explore`             | text brief                  | 1–3 divergent drafts (count asked first) → user picks one → continues as `good` (Slide → deck builder) |
| `describe`            | screenshot / video          | super-detailed written description + implementation plan (NO code) |
| `screenshot`          | screenshot                  | design recreated from the image as functional code          |
| `video`               | video                       | design + interactions recreated from the video as functional code |
| `review`              | changed UI files / surfaces | read-only review report (findings, severity, fix guidance; fixes only via the validated fix loop, none under `--report-only`) — formerly `/ui-review` |

**Shared workflow (journey-first spine — BLOCKING order, every design mode; `review` runs its own reference instead):**

1. **Journey Report (`UX-1`)** — Analyze and REPORT the main user journeys BEFORE any other output (template: `.claude/docs/ux-journey-process.md` §4, depth per §10). Confirm an inferred primary actor, main job or success outcome with the user before generating.
2. **Design authority read (`UX-2`)** — Read the project's design principles/guidelines, the design system resolved from `docs/project-config.json` (`designSystem.canonicalDoc`, `tokenFiles`, `appMappings[]`) and the existing related UI (`SYNC:existing-ui-research`); record `Design authority read: <paths>` or `N/A — none configured (checked: <paths>)`.
3. **Research** — Run this skill's design-intelligence search, framed by the Journey Report; results are candidates only, never project authority.
4. **Ingest** — For visual modes (`describe`/`screenshot`/`video`), use `visual analysis tooling` to analyze the screenshot/video in super-detail.
5. **Low-fi structure (`UX-7`)** — Sketch flow and views (ASCII is enough) from the journey steps (`UX-3`) and per-decision-point priority (`UX-4`); walk the main journeys on it before any styling.
6. **Design** — Use `ui-ux-designer` subagent to layer the `DD-3` Design Plan and visual design (or, for `describe`, an implementation plan) on the validated structure, applying `UI-*`/`DD-*` and the selected lane's craft body.
7. **Implement** — Build as code following the selected lane guide: `references/lane-product/lane-guide.md` (product UIs) or `references/lane-marketing/lane-guide.md` (marketing/creative). Skipped in `describe` mode.
8. **Validate (`UX-8`)** — Cognitive walkthrough of every main journey on the produced design plus a traceability matrix (journey step → view → element → information tier → rule → states); fix every unserved step and orphan element before hand-off. Measure interaction cost per main journey (`UX-9`) and check wayfinding on every view (`UX-10`) (catalog §12).
9. **Report** — Close with the **UI/UX Gate Report** (`UX-11`, catalog §13): one row per gate (`UX-*`, applicable `UI-*`, `DD-*`, `CL-*` with at least the `CL-5` triage, UI copy), each `PASS` / `FAIL → fixed` / `N/A` with evidence; an unresolved `FAIL` blocks hand-off. Present to user for approval with the Journey Report, walkthrough result, matrix and Gate Report; update `./docs/design-guidelines.md` if needed.

**Key Rules:**

- Report the main user journeys (`UX-1`) first, then resolve the project's design principles, accepted design system and existing UI (`UX-2`); only then use this skill's local design-intelligence index as candidate input.
- Default to pure HTML/CSS/JS if the user doesn't specify a framework
- Use `visual analysis tooling` for generating AND reviewing real visual assets
- Use media processing tooling (RMBG) to remove backgrounds from generated assets when needed

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Arguments & Mode Dispatch

`$ui-design --mode={fast|good|explore|describe|screenshot|video|review} --lane={product|marketing} <brief | screenshot | video | review scope>`

- When `--mode` is omitted, default to `--mode=fast`.
- An explicit `--mode` always wins; `--mode=review` is never inferred from the brief and is never the default.
- When `--lane` is omitted, default to `--lane=product` (the dominant PBI/app use). Pick `marketing` for landing pages, campaigns, and distinctive creative pieces.
- `--mode` (input carrier) and `--lane` (design tradition) are orthogonal — e.g. `--mode=screenshot --lane=product` recreates a dashboard screenshot in the product-UI craft tradition.
- `$ARGUMENTS` carries the full input after the command. Interpret it per mode: `fast`/`good`/`explore` → a text design brief; `describe`/`screenshot` → a screenshot reference (path/URL/attachment); `video` → a video reference; `review` → the review scope (files, directories or surfaces; empty = all uncommitted UI changes) plus the optional `--report-only` flag.

### Lane selection (apply the chosen lane's craft body at stages 6-7)

- **`--lane=product` (default)** — product UIs: dashboards, admin panels, SaaS apps, tools. Domain-driven craft (intent → domain exploration → signature → layered surfaces/tokens). Full body: `references/lane-product/lane-guide.md`.
- **`--lane=marketing`** — marketing/creative: landing pages, campaigns, screenshot replication. Bold aesthetic direction (distinctive type, cohesive palette, atmosphere, motion). Full body: `references/lane-marketing/lane-guide.md`.

Do NOT inline the lane bodies here — read the matching `lane-guide.md` when the lane is selected.

## Required Skills (Priority Order)

1. **In-skill design-intelligence search/data** — Query `scripts/search.py` after the Journey Report (`UX-1`) and the design-authority/existing-UI read (`UX-2`); results are candidate input, not project authority.
2. **In-skill lane references** — `references/lane-{product|marketing}/lane-guide.md` (+ their reference files) own implementation, screenshot/video analysis, and design replication for the selected lane.
3. **In-skill explore references** — `references/explore/workflow.md` (+ `gate-files.md`, `brand-asset-protocol.md`) own the `--mode=explore` flow; read them only when that mode is selected.
4. **In-skill review reference** — `references/mode-review.md` owns `--mode=review`; read it only when that mode is selected.

**Ensure token efficiency while maintaining high quality.**

## Shared First Step (ALL design modes)

> **[BLOCKING] Step 0 — Journey Report (`UX-1`).** Before any wireframe, mockup, design plan, token table, search result or code, analyze and PRESENT the main user journeys, per `SYNC:ux-journey-gate` and the template in `.claude/docs/ux-journey-process.md` §4: frame · actors + job statements · 3–5 ranked main journeys with step tables (intent · decision/action · information needed · business rule · system response · failure → recovery) · derived design requirements · assumptions and open questions, each claim tagged `SOURCED (location)` or `INFERRED`. Depth scales with scope (§10), never to zero for a new or reshaped view. **Confirm an inferred primary actor, main job or success outcome with the user before generating.**
>
> **[BLOCKING] Step 0b — Design authority read + existing UI (`UX-2`).** Resolve from `docs/project-config.json` and its reference docs, then read the project's design principles/guidelines, the design system (`designSystem.canonicalDoc`, `tokenFiles`, `appMappings[]`), accepted design ADRs, and the existing related UI — inventory the screens and components already serving this feature/domain and map every connected flow that links to / embeds / navigates to-or-from it (`SYNC:existing-ui-research`). Record `Design authority read: <paths>` or `N/A — none configured (checked: <paths>)`. Adopt house patterns; never invent tokens or components the project already defines.
>
> Skip Steps 0 and 0b ONLY for work with no user-facing surface, stated explicitly.

**THEN**, after Steps 0 and 0b, run focused design-intelligence searches — framed by the Journey Report — to gather candidate input:

```bash
# Windows: py -3 · macOS/Linux: python3 (same arguments)
py -3 .claude/skills/ui-design/scripts/search.py "<product-type>" --domain product
py -3 .claude/skills/ui-design/scripts/search.py "<style-keywords>" --domain style
py -3 .claude/skills/ui-design/scripts/search.py "<mood>" --domain typography
py -3 .claude/skills/ui-design/scripts/search.py "<industry>" --domain color
```

## Design Intelligence Research Contract

The local index is a research aid owned by this skill. It supplies structured candidates; it never outranks the adopter project's accepted brief, design system, tokens, components, frontend conventions, or accessibility requirements.

1. **Frame the query.** Derive the product type, audience and job-to-be-done from the Journey Report (`UX-1`: frame, actors, job statements, main journeys), then add industry, desired style, platform, implementation stack, and constraints before searching.
2. **Search deliberately.** Query `product`, `style`, `typography`, and `color` first; add `landing`, `chart`, `ux`, `prompt`, and the relevant `--stack` query when the surface needs them. Use specific domain terms and more than one query when the brief has multiple concerns.
3. **Resolve and record authority.** Read `docs/project-config.json` and resolve `designSystem.canonicalDoc`, `tokenFiles`, and `appMappings[]` when present. Reconcile candidates against the accepted brief, existing-UI inventory, shared `UI-*`/`DD-*`/`CL-*` contracts, and the selected lane. Record why important candidates were selected or rejected; never invent tokens, components, breakpoints, or stack defaults when the project has not declared them.
4. **Keep implementation quality explicit.** Use the project's icon system or one consistent accessible SVG set; do not use emoji as UI icons; verify official brand marks. Define stable hover, focus, active, disabled, and loading feedback without layout shift, using the project's cursor and motion conventions.
5. **Design state coverage before the happy path.** Specify `Default`, `Loading`, `Disabled`, `Error`, `Empty`, and `Success` where applicable. Errors need human-readable recovery, empty states need a meaningful next action, in-flight actions must prevent duplicate submission, and successful actions need acknowledgment.
6. **Design for reachable reflow.** Use the project's content breakpoints. If none are declared, smoke-check 320, 768, 1024, and 1440 widths: rows reflow, grids collapse, non-reflow content has an intentional reachable scroll fallback, and nothing is clipped or unreachable. Surface any large refactor or new breakpoint as an explicit decision.

`--mode=review` remains the owner of source-level findings, evidence, severity, component ownership, and review procedure. This contract makes the same quality floor explicit while authoring a design; it does not duplicate or replace the review mode.

## UX Journey Contract (all design modes)

The journey-first gate (`UX-1`–`UX-11`, `SYNC:ux-journey-gate`; deep catalog `.claude/docs/ux-journey-process.md`) binds EVERY design mode (`--mode=review` applies it through its own reference) and runs BEFORE `UI-*`/`DD-*`/`CL-*`, because those judge a surface whose purpose it defines. Steps 0 and 0b above deliver `UX-1` and `UX-2`.

**Generative modes (`fast`, `good`, `explore`) — DERIVE the design from the journeys:**

1. **Views are journey steps (`UX-3`)** — every view hosts ≥1 main-journey step and names its primary task; every step lands on a view; the container fits the task (catalog §2 S5).
2. **Priority per decision point (`UX-4`)** — rank each item and action by need-at-the-decision × frequency × cost-of-missing into Primary · Secondary · On demand · Not here; ONE focal point and ONE primary action = the journey's next step (catalog §6).
3. **Rules become interaction (`UX-5`)** — map each business rule to the lightest treatment that prevents the error before one that reports it; design each step's failure → recovery (catalog §7).
4. **Low-fi before hi-fi (`UX-7`)** — walk the main journeys on the ASCII structure before layering the `DD-3` Design Plan.
5. **Walk before reporting (`UX-8`)** — cognitive walkthrough of every main journey plus the traceability matrix (catalog §9); an unserved step or orphan element is fixed before hand-off.
6. **Interaction cost and wayfinding (`UX-9`, `UX-10`)** — per main journey record steps · clicks · view changes · fields · decisions against the existing flow or spec, and cut what does not advance the job (every click confident — no "3-click rule"). Every view answers where am I / where can I go / how do I get back, with no dead ends. The primary tier sits in the first viewport (catalog §12).
7. **Check every UI/UX gate (`UX-11`)** — every mode's final walk step also runs items 5–6 and ends with the UI/UX Gate Report (catalog §13) before the report to the user; a gate missing from the report counts as not checked.

**Recreation modes (`describe`, `screenshot`, `video`) — INFER and REPORT:** the Journey Report names the journeys the observed UI serves (tagged `INFERRED` unless a spec or the user sources them); the walk RECORDS every violation it exposes (`UX-3`/`UX-4`/`UX-5`) — `describe` carries it into the implementation plan as a correction, `screenshot`/`video` fix it in the recreation and confirm with the user any fix that changes the visual match.

## Design Principles Contract (all design modes)

The 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`) carried as the `SYNC:ui-ux-design-principles` block below bind EVERY mode of this skill; `--mode=review` applies them as fail-conditions through its own reference. Project design-system docs OUTRANK them — surface a genuine conflict to the user with both sides, NEVER resolve it silently.

**Generative modes (`fast`, `good`, `explore`) — APPLY the clauses as an output contract on the design you produce:**

1. **States first.** Design and build the empty, loading and error state BEFORE the populated state (`UI-1.5`), and reserve space for anything that loads so nothing shifts in (`UI-9.3`).
2. **All 5 interaction states per interactive element** — default, hover, focus, active, disabled — plus loading where it applies (`UI-5.2`); keep a visible focus ring, restyled if it clashes but NEVER removed (`UI-5.5`).
3. **Declare the scales, never improvise them.** State the type scale as 6 named steps with no one-off sizes (`UI-2.5`), body 16px web / 17px mobile and never below 14px (`UI-2.2`), measure 45–75 characters (`UI-2.3`); and declare ONE spacing unit — 4px or 8px base, every gap a multiple of it (`UI-4.1`). Both declarations belong in the summary you report back at stage 9; an undeclared scale is an incomplete design, not a style choice.
4. **Contrast is measured, not eyeballed** — state the target AND the measured value: 4.5:1 text, 3:1 UI edges (`UI-3.1`); colour NEVER carries meaning alone — pair it with an icon, label or position (`UI-3.3`).
5. **Touch surfaces.** When the design covers a mobile/touch surface, hit targets are ≥44×44pt and 8px apart (`UI-8.1`) and primary actions sit in the bottom third where the thumb lives (`UI-8.2`). When it does not, state that explicitly so the §8 skip is auditable.

**Reporting modes (`describe`, and the analysis pass of `screenshot` / `video`) — REPORT against the clauses:** the super-detailed description MUST name which clauses the OBSERVED design SATISFIES and which it VIOLATES, cited by ID — e.g. type-scale drift (`UI-2.5`), contrast failure with the measured ratio (`UI-3.1`), undersized touch targets (`UI-8.1`), missing empty/loading/error states (`UI-1.5`), a removed focus ring (`UI-5.5`). A violation is RECORDED, never silently reproduced: `describe` carries it into the implementation plan as a correction; `screenshot` / `video` then apply the five generative obligations above so the recreation FIXES the violation rather than inheriting it — flag any correction that changes the visual match and confirm it with the user before shipping it.

## Mode Branches

### `--mode=review` — UI review (read-only; replaces the design spine)

**[BLOCKING] When `--mode=review`, read `references/mode-review.md` in full FIRST** and follow it as the whole invocation: Phase 0 load UI rules → scope and surfaces → blast radius → surface composition → surface UX pass → six UI categories plus the UI/UX principles and design-distinctiveness passes → report → why-review validation → validated fix loop (none under `--report-only`). It carries its own protocols inline; do not run the design-spine steps, the design-intelligence search or a lane for it. Workflow invocation (`--mode=review --report-only`) and standalone both run it.

### `--mode=fast` (default) — quick design

1. **Journey Report (`UX-1`) + design authority (`UX-2`)** — Steps 0 and 0b above; present the report and confirm an inferred primary actor/job/outcome before continuing (no question tool → record it `INFERRED — unconfirmed` and continue).
2. Run the shared design-intelligence searches above.
3. Use `ui-ux-designer` subagent to start the design process — brief it with the Journey Report and the `Design authority read:` paths; low-fi structure walked against the journeys first (`UX-7`).
4. If the user doesn't specify, create the design in pure HTML/CSS/JS.
5. **Walk the main journeys (`UX-8`)** on the built design with the traceability matrix; fix every unserved step and orphan element.
6. Report back with a brief summary of the changes, the walkthrough result and the UI/UX Gate Report (`UX-11`); ask the user to review and approve.
7. On approval, update `./docs/design-guidelines.md` if needed.

### `--mode=good` — immersive, high-quality design

Same spine as `fast`, raised to a higher quality bar (iterate on details):

1. **Journey Report (`UX-1`) + design authority (`UX-2`)** — Steps 0 and 0b above at full depth for the scope (catalog §10); present the report and confirm an inferred primary actor/job/outcome before continuing (no question tool → record it `INFERRED — unconfirmed` and continue).
2. Run comprehensive design-intelligence searches across the applicable domains.
3. Use `researcher` subagent to research design style, trends, fonts, colors, borders, spacing, elements' positions, etc.
4. Use `ui-ux-designer` subagent to implement the design step by step based on the Journey Report, the design authority and the research — low-fi structure walked against the journeys first (`UX-7`).
5. If the user doesn't specify, create the design in pure HTML/CSS/JS.
6. **Walk the main journeys (`UX-8`)** on the built design with the traceability matrix; fix every unserved step and orphan element.
7. Report back with a summary, the walkthrough result and the UI/UX Gate Report (`UX-11`); ask the user to review and approve.
8. On approval, update `./docs/design-guidelines.md` if needed.

- **ALWAYS REMEMBER you have the skills of a top-tier UI/UX Designer who won many awards on Dribbble, Behance, Awwwards, Mobbin, TheFWA.**
- Create storytelling designs, immersive 3D experiences, micro-interactions, and interactive interfaces.

### `--mode=explore` — 1–3 drafts, user picks, then `good`

Opt-in. Use when the visual direction is genuinely open and the user wants to choose it by looking. **Read `references/explore/workflow.md` first and follow its steps (Step 0 draft count, then 1–10), one task each.** First action: its Step 0 asks 3 / 2 / 1 drafts or skip (no question tool → ONE auto-selected draft). A picked Slide direction goes to a deck builder, not `good` (item 8).

1. **Journey Report (`UX-1`) + design authority (`UX-2`)** — Steps 0 and 0b above, produced ONCE before any seed and shared by all N drafts; confirm an inferred primary actor/job/outcome first (no question tool → record it `INFERRED — unconfirmed` and continue). The design-authority read also resolves **authority per axis** (colour · type · layout). A direction stated in the brief, or a project design system pinning all three axes → record it as `ADOPTED`, log the exemption, and run `--mode=good` instead. Partial pins → the drafts share the pinned axes and diverge only on the free ones.
2. **Ground before diverging** — fact-check named products/specs, ask once for reference designs the user likes or dislikes, run `references/explore/brand-asset-protocol.md` when a real brand is named, gather ONE shared content-imagery set (licensed, sources recorded) or labelled placeholders, answer the five form questions, fix the deliverable type and pixel canvas, write the `DD-3` Design Plan skeleton.
3. **N seeds (take the first N)** — a random style row from `node .claude/skills/ui-design/scripts/pick-style.cjs` (after changing the picker, run its tests: `node .claude/skills/ui-design/tests/pick-style.test.cjs`), the user's liked reference or a web-verified real-world reference, a studio persona described by traits only. Seeds are divergence seeds, never taste: each draft translates its seed into THIS subject (`DD-1`) and passes the `DD-3` generic test, or it is revised.
4. **Fan out** — N `ui-ux-designer` sub-agents in ONE message → `tmp/design/<run>/direction-{a,b,c}.html`; layout FREE → structurally different layout skeletons, layout ADOPTED → the pinned layout is shared and drafts diverge on the free axes only. Every draft serves the SAME main journeys and information-priority tiers (`UX-3`/`UX-4`) — drafts diverge on visual axes and layout skeleton, never on the journeys or the priority tier of content. No sub-agents → build serially; each later draft names what it avoided from the earlier ones.
5. **Render after all return** — per draft, `node .claude/skills/html-export/scripts/export.cjs --to=png --viewport=<canvas> --out=tmp/design/<run>/renders/<draft>/ <file>`; handle exits 0/4/3/1-2 per workflow step 8, re-render after the `DD-8` edit. NEVER run install commands.
6. **Present side by side, open every draft in the default browser, and ASK** — each draft with how it serves the primary journey; open each with `node .claude/scripts/open-report.cjs tmp/design/<run>/direction-<x>.html`, then, with 2–3 drafts, ask user tool with one option per draft and your evidence-backed `(Recommended)` draft first (explore step 9); one draft → no question (`Selection: USER — 1 option`, or `AUTO-SELECTED — no question tool (1 draft)` set at Step 0); drafts cannot be shown or the question tool errors → AUTO-SELECT the recommended draft; record why either way (explore step 9 fallback). Never pick for the user while they can be asked; never offer a text-only style choice; "continue" is not a pick.
7. **Record** the user's verbatim choice, or the `Selection:` line, in `tmp/design/<run>/direction-approved.md` (template: `references/explore/gate-files.md`), with the chosen draft's Design Plan tokens in its `## Design Plan tokens` section.
8. **Walk the main journeys (`UX-8`)** on the chosen draft with the traceability matrix, record the gaps in the `## Journey fixes (UX-8)` table of `run-notes.md` as inputs, then continue as `--mode=good` from the chosen draft — except a Slide deliverable: hand two files, `direction-approved.md` (carrying the tokens) and `run-notes.md`, to a deck builder instead (`$presentation-builder` for a general deck — command-only, so stop and tell the user to run it; `feature-presentation` for a feature review deck; explore step 10).

### `--mode=describe` — describe only (NO implementation)

Treat `$ARGUMENTS` as the screenshot/video to describe.

1. **Journey Report (`UX-1`) + design authority (`UX-2`)** — Steps 0 and 0b above: infer and report the journeys the observed UI serves (tagged `INFERRED` unless sourced), and read the project design authority the implementation must adopt.
2. Use `visual analysis tooling` to describe super-details of the screenshot/video so a developer can implement it easily.
    - Be specific about design style, every element, elements' positions, every interaction, every animation, every transition, every color, every border, every icon, every font style/size/weight, every spacing/padding/margin, every size/shape/texture/material/light/shadow/reflection/refraction/blur/glow/image, background transparency, etc.
    - **IMPORTANT:** Predict the font name (Google Fonts) and font size — don't just use Inter or Poppins.
3. Use `ui-ux-designer` subagent to create a design implementation **plan** following the progressive-disclosure structure so the result matches the screenshot/video:
    - Create a directory using the naming pattern from the `## Naming` section.
    - Save the overview access point at `plan.md`, keep it generic, under 80 lines, listing each phase with status/progress and links.
    - For each phase, add `phase-XX-phase-name.md` with sections (Context links, Overview with date/priority/statuses, Key Insights, Requirements, Architecture, Related code files, Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps).
4. **Walk the main journeys (`UX-8`)** on the observed UI with the traceability matrix; record every violation the walk exposes and carry it into the plan as a correction.
5. Report back with a summary of the plan, the Journey Report, the walkthrough findings and the UI/UX Gate Report (`UX-11`, recording the violations observed). **Do NOT implement.**

### `--mode=screenshot` — recreate from image as code

Treat `$ARGUMENTS` as the screenshot to recreate exactly.

1. **Journey Report (`UX-1`) + design authority (`UX-2`)** — Steps 0 and 0b above: infer and report the journeys the observed UI serves (tagged `INFERRED` unless sourced), and read the project design authority the recreation must adopt.
2. Use `visual analysis tooling` to describe super-details of the screenshot (design style, trends, fonts, colors, border, spacing, elements' positions, size, shape, texture, material, light, shadow, reflection, refraction, blur, glow, image, background transparency, transition, etc.).
    - **IMPORTANT:** Predict the font name (Google Fonts) and font size — don't just use Inter or Poppins.
3. Use `ui-ux-designer` subagent to create a design plan following the progressive-disclosure structure (as in `describe`) so the final result matches the screenshot. Keep every research markdown report concise (≤150 lines).
4. Implement the plan step by step.
5. If the user doesn't specify, create the design in pure HTML/CSS/JS.
6. **Walk the main journeys (`UX-8`)** on the recreation with the traceability matrix; fix every violation the walk exposes and confirm with the user any fix that changes the visual match.
7. Report back with a summary, the walkthrough result and the UI/UX Gate Report (`UX-11`); ask the user to review and approve.
8. On approval, update `./docs/design-guidelines.md` if needed.

- **ALWAYS REMEMBER you have the skills of a top-tier UI/UX Designer who won many awards on Dribbble, Behance, Awwwards, Mobbin, TheFWA.**
- Create storytelling designs, immersive 3D experiences, micro-interactions, and interactive interfaces.

### `--mode=video` — recreate from video as code

Treat `$ARGUMENTS` as the video to recreate exactly. Same as `--mode=screenshot`, but ingest a VIDEO and capture BOTH static layout AND interaction/animation/transition patterns.

1. **Journey Report (`UX-1`) + design authority (`UX-2`)** — Steps 0 and 0b above: infer and report the journeys the observed flow serves (the video's interaction sequence is direct evidence; tag `INFERRED` unless sourced), and read the project design authority the recreation must adopt.
2. Use `visual analysis tooling` to describe super-details of the video: every element, every interaction, every animation, every transition, every color, every font, every border, every spacing, every size/shape/texture/material/light/shadow/reflection/refraction/blur/glow/image, background transparency, etc.
    - **IMPORTANT:** Predict the font name (Google Fonts) and font size — don't just use Inter or Poppins.
3. Use `ui-ux-designer` subagent to create a design plan following the progressive-disclosure structure so the final result matches the video. Keep every research markdown report concise (≤150 lines).
4. Implement the plan step by step.
5. If the user doesn't specify, create the design in pure HTML/CSS/JS.
6. **Walk the main journeys (`UX-8`)** on the recreation with the traceability matrix; fix every violation the walk exposes and confirm with the user any fix that changes the visual match.
7. Report back with a summary, the walkthrough result and the UI/UX Gate Report (`UX-11`); ask the user to review and approve.
8. On approval, update `./docs/design-guidelines.md` if needed.

- **ALWAYS REMEMBER you have the skills of a top-tier UI/UX Designer who won many awards on Dribbble, Behance, Awwwards, Mobbin, TheFWA.**
- Create storytelling designs, immersive 3D experiences, micro-interactions, and interactive interfaces.

## Notes (all design modes)

- **Design system (canonical):** When implementing UI — HTML, CSS, or SCSS — read `docs/project-config.json` first, then resolve `designSystem.canonicalDoc`, `tokenFiles`, and `appMappings[]`. Read every configured authority before choosing tokens, component patterns, breakpoints, or BEM conventions. If the project has no configured authority, record `N/A` and follow the selected lane plus the shared UI/DD/CL contracts; never invent a canonical path or token vocabulary.
- Remember you have the capability to generate images, videos, edit images, etc. with `visual analysis tooling` skills. Use them to create the design and real assets.
- Always review, analyze, and double-check generated assets with `visual analysis tooling` skills to verify quality.
- Use media processing tooling (RMBG) to remove background from generated assets if needed (`good`/`screenshot`/`video`).
- Maintain and update `./docs/design-guidelines.md` docs if needed.

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

Think hard to plan & start working on these tasks follow the Orchestration Protocol, Core Responsibilities, Subagents Team and Development Rules. Parse `--mode` from the input (default `fast`; an explicit mode wins) and route to the matching branch above:
<tasks>$ARGUMENTS</tasks>

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `design-distinctiveness-gate` — Design identity gate DD-1 to DD-8: subject, design plan, generic test, restraint; designing, implementing or reviewing a visual surface → .claude/skills/shared/protocols/design-distinctiveness-gate.md
- `design-review-checklist` — Executable front-end design review protocol CL-1 to CL-6; reviewing, planning or building front-end work → .claude/skills/shared/protocols/design-review-checklist.md
- `existing-ui-research` — Study the existing UI before designing or specifying a screen; designing or specifying a new or updated screen → .claude/skills/shared/protocols/existing-ui-research.md
- `ui-copywriting` — User-visible strings are design content; writing or reviewing UI text → .claude/skills/shared/protocols/ui-copywriting.md
- `ui-ux-design-principles` — Forty usability and accessibility clauses, UI-1.1 to UI-9.4; designing, building or reviewing a user-facing interface → .claude/skills/shared/protocols/ui-ux-design-principles.md
- `ux-journey-gate` — Journey-first UX gate UX-1 to UX-11: report journeys, read the design authority, generate, then check every UI/UX gate; generating, specifying, planning, mocking up or reviewing a user-facing surface → .claude/skills/shared/protocols/ux-journey-gate.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:ui-ux-design-principles:reminder -->

Apply `UI-1.1`–`UI-9.4` only to applicable user-interface work. Resolve platform and project conventions first. Use WCAG 2.2 AA as the web accessibility baseline plus any stricter applicable legal/project requirement; non-web surfaces use the documented platform standard. Other web/mobile metrics and component tiers are defaults/examples only for matching surfaces. Skip N/A clauses and non-UI work explicitly. Project config, references, and accepted decisions govern; cite applicable findings by `UI-<clause>` + `file:line`.

<!-- /SYNC:ui-ux-design-principles:reminder -->

<!-- SYNC:design-distinctiveness-gate:reminder -->

- **MUST ATTENTION** apply the design distinctiveness gate (`DD-1`–`DD-8`) to any user-facing visual surface: ground it in the named subject/audience/job and confirm when the brief is silent (`DD-1`) · every choice carries a WHY, token names included (`DD-2`) · write a design plan (colour 4–6 named hex · type families+roles+scale · layout prose+ASCII+alignment · principles) then run the BLOCKING generic test and state what you revised BEFORE coding (`DD-3`) · audit every free axis against the T1–T5 tell catalog — cream+serif+`#D97757`, acid-on-black, broadsheet, the SaaS-card kit, template chrome (ALL-CAPS eyebrows, `A · B · C`, spaced-em-dash labels, `#0B0B0B`, mono data labels, trailing `→`) — a match is a missed decision, never a defect (`DD-4`) · 1–2 clearly distinct families, real scale, <80ch, no single-word headline accent / ALL-CAPS labels / redundant eyebrows (`DD-5`) · numbering only on real sequences; hero = the subject's most characteristic thing, not big-number+gradient (`DD-6`) · one orchestrated motion moment, never per-section entrances plus universal card hovers (`DD-7`) · spend boldness once, critique the BUILT page, remove one accessory (`DD-8`). The brief's stated direction OUTRANKS the tell catalog; project design-system docs OUTRANK these clauses — genuine conflicts go to the user, NEVER resolved silently. Cite findings as `DD-<clause>` + `file:line`. Skip ONLY for surfaces with no user-facing visuals, stated explicitly.

<!-- /SYNC:design-distinctiveness-gate:reminder -->

<!-- SYNC:ui-copywriting:reminder -->

- **MUST ATTENTION** treat user-visible words as design content: end-user vocabulary, not system vocabulary (notifications, not webhook config) · active-voice CTAs that say what happens ("Save changes", never "Submit") · ONE name per action across the whole flow (Publish → "Published") · errors explain what happened and how to fix it and NEVER apologize or stay vague, empty screens invite action · sentence case, plain verbs, no filler, one job per element · real subject-specific copy, never lorem — and read every string for TRUTH: one coherent story, not three products' content on one screen. Skip ONLY when no user-visible text changes, stated explicitly.

<!-- /SYNC:ui-copywriting:reminder -->

<!-- SYNC:design-review-checklist:reminder -->

- **MUST ATTENTION** when the change/plan/artifact has an applicable user-facing UI surface, READ `.claude/docs/design-review-checklist.md` and run it: `CL-1` establish context first (platform · user · task · metric · constraints · scope · artifacts — state missing context and its confidence impact) · `CL-2` evidence or nothing, cite a location per finding, NEVER invent a measurement (unmeasurable → `NOT VERIFIABLE`), tag `MEASURED`/`OBSERVED`/`HEURISTIC` · `CL-3` rank `P0`–`P4`, cap at top 10 by severity, NEVER pad, concrete fix on every `P0`/`P1` · `CL-4` sweep §A–§N plus §R over whole surfaces (changed files → affected views, composition reconstructed, render or `ENVIRONMENT-BLOCKED`), including surface load B12–B15, container fit E9–E11, §H by usage, Field Necessity Matrix for input, applying only relevant platform/product sections and the WCAG 2.2 AA web baseline plus any stricter applicable legal/project requirement, or the documented standard for other platforms · `CL-5` short on time → use the §P prompts · `CL-6` report in the §O shape · for source code, assess component ownership, base abstractions, reuse, and duplication using the project's documented taxonomy or observed boundaries. Project design-system docs and ADRs OUTRANK the checklist; report a defect ONCE across `UI-*`/`DD-*`/`CL-*`. For a plan, bind only applicable sections and states to acceptance criteria, and name each UI view's primary task, container, information priority, and creation-vs-deferred inputs; a plan review flags a UI phase that omits them. Skip when the work has no user-facing UI surface, and state why.

<!-- /SYNC:design-review-checklist:reminder -->


<!-- SYNC:ux-journey-gate:reminder -->

- **MUST ATTENTION** journey-first, BLOCKING order: REPORT the main user journeys (`UX-1`, evidence-tagged; confirm an inferred actor/job/outcome, or with no question tool record it `INFERRED — unconfirmed` and continue) → READ project design principles, design system, existing UI (`UX-2`) → generate → CHECK all gates. Checks: views = journey steps (`UX-3`) · important information first — one focal point, one primary action = next step, first viewport holds the primary tier (`UX-4`) · rules become prevention, states, recovery (`UX-5`) · the user's mental model (`UX-6`) · low-fi first (`UX-7`) · walkthrough + traceability, no unserved step or orphan (`UX-8`) · interaction cost per journey measured — steps, clicks, view changes, fields, decisions — every click confident, not a 3-click rule (`UX-9`) · wayfinding: where am I, where can I go, how do I get back, no dead ends (`UX-10`) · close with the **UI/UX Gate Report** covering `UX-*`, `UI-*`, `DD-*`, `CL-*` and UI copy — an unresolved `FAIL` blocks hand-off (`UX-11`). Catalog: `.claude/docs/ux-journey-process.md`. Skip ONLY with no user-facing surface, stated.

<!-- /SYNC:ux-journey-gate:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Create (or describe) a UI design using design-intelligence databases and subagents, dispatched by `--mode` (input carrier) × `--lane` (design lane); `--mode=review` reviews existing UI through `references/mode-review.md`.

**IMPORTANT MUST ATTENTION** route `--mode={fast|good|explore|describe|screenshot|video}` × `--lane={product|marketing}` (`--mode=review` → read `references/mode-review.md` in full first and follow it instead) → Journey Report (`UX-1`) → design authority/existing UI (`UX-2`) → query local design intelligence → ingest visual evidence when applicable → low-fi walked against journeys (`UX-7`) → design → implement unless `describe` → walk journeys + traceability (`UX-8`) → report and seek approval; project authority outranks candidates, `--mode=review` owns source review evidence.

**IMPORTANT MUST ATTENTION** journey-first order is BLOCKING in EVERY design mode: (1) present the Journey Report (`UX-1`) and confirm an inferred primary actor/job/outcome (no question tool → record it `INFERRED — unconfirmed` and continue) → (2) read and record the project's design principles, design system and existing UI, or `N/A` with the paths checked (`UX-2`) → (3) only then search, sketch, design or build; walk every main journey (`UX-8`), measure interaction cost and wayfinding (`UX-9`, `UX-10`) and close with the UI/UX Gate Report covering `UX-*`/`UI-*`/`DD-*`/`CL-*`/copy (`UX-11`) before reporting — why: a screen designed before its journey is known answers the brief's layout, not the user's job.

**MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**


- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting
- **MANDATORY IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
- **MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality
- **MANDATORY IMPORTANT MUST ATTENTION** apply the 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`) to every design: empty/loading/error states designed FIRST (`UI-1.5`), all 5 interaction states per interactive element (`UI-5.2`), type scale (6 named steps, `UI-2.5`) and spacing unit (4/8px base, `UI-4.1`) DECLARED not improvised, contrast measured and stated (4.5:1 text / 3:1 edges, `UI-3.1`), ≥44×44pt touch targets + bottom-third primaries on mobile surfaces (`UI-8.1`, `UI-8.2`); `fast`/`good`/`explore` APPLY them, `describe`/`screenshot`/`video` also REPORT by clause ID which the observed design satisfies or violates — project design-system docs outrank the clauses, conflicts go to the user

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.
