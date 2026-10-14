---
name: ui-review
version: 2.0.0
description: '[Code Quality] Use when reviewing UI/frontend changes for long-content overflow, responsive multi-screen layout (flex-wrap / row-to-column on small devices), flex-vs-fixed sizing, z-index discipline, SCSS/BEM styling quality, and async UI states & feedback (loading indicator, error surface, empty state).'
execution-mode: subagent
context-budget: high
---

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Validate UI/frontend changes for the six visual-quality dimensions that break in production but slip past correctness review — long-content overflow & truncation, responsive multi-screen layout (flex-wrap / row-to-column so it stays usable on small devices), flex-grow vs fixed sizing, z-index scale discipline, SCSS/CSS/BEM styling quality, and async UI states & feedback (loading indicator, user-visible error surface, empty state, in-flight disable) — so frontend/UI changes survive real content, responsive layouts, layering, styling conventions, and the loading/error/empty branches before handoff.

**Default scope:** All uncommitted frontend changes (staged + unstaged) matching the frontend path and file-extension patterns declared by the project configuration/docs index. Override: specify files, directories, components, or full frontend codebase.

> **CONDITIONAL — SKIP when no frontend files in scope.** In workflow context this skill is SKIPPED when the diff has no files matching the project frontend path/extension patterns. If invoked standalone with no frontend changes → announce `"No frontend changes detected — ui-review skipped"` and report clean.

> **ROUTING BOUNDARY (read before starting):**
>
> - **`ui-review` (this skill)** — the project UI review gate. Purpose: find issues, assign severity, give project-specific fix guidance citing real reuse targets (sourced from the project reference docs). It complements `architecture-review`. In `workflow-review-changes` it runs in TWO places by design (keep both): (a) INTERNALLY as `changes-review`'s UI dimension (step 1), AND (b) as a DEDICATED conditional parallel-batch member (step 9, `ui-ux-designer` sub-agent). Both fire only when frontend files are in scope.
> - **`web-design-guidelines`** — a generic, standalone accessibility / UX checklist. Cross-read it for a11y depth (WCAG, focus order, ARIA, contrast); do NOT duplicate its content here.
> - **`ui-ux-designer`** — specialized UI/UX, accessibility, responsive layout, and design-token review/authoring sub-agent when the local agent catalog provides it.

> **MANDATORY MUST ATTENTION** Plan tasks to READ UI rules BEFORE reviewing:
>
> 1. Project styling rules doc — BEM convention, mixins, variables, responsive patterns **(READ FIRST — primary styling rules source; resolve via project config/docs index)**
> 2. Project design-system/token doc — design tokens, especially the **Z-Index & Layering** section
> 3. Project frontend architecture/patterns doc — base component classes, state/store, API service, lifecycle teardown rules shared with `architecture-review`
> 4. Project code-review rules doc — anti-patterns and conventions
>
> Not found → search: "scss styling", "design tokens", "frontend patterns". Rules come from docs — NOT general knowledge.

**Workflow:**

1. **Phase 0: Load UI Rules** — Resolve and read the four project UI/styling rule docs above
2. **Phase 1: Determine Scope** — Changed frontend files (default) or user-specified scope
3. **Phase 2: Blast Radius** — Run graph trace if graph.db exists
4. **Phase 3: UI Category Review** — Check each file against all 6 applicable categories
5. **Phase 4: Finalize** — Generate compliance report with PASS/BLOCKED/WARN verdicts
6. **Fix Loop: Validate → Fix → Full UI Re-Review** — validate findings first; after validated fixes, rerun the full UI review using the local sub-agent selection guide only when that protocol calls for agents

**Key Rules:**

- Write findings to `plans/reports/ui-review-{date}-{slug}.md`
- BLOCKED = must fix before merge | WARN = review and decide | PASS = compliant
- Every violation needs `file:line` proof + grep 3+ counterexamples before flagging
- Review is read-only until `/why-review --validate-findings` confirms findings; fixes may happen only in the validated fix loop or downstream plan/feature-implement, and every fix restarts a full UI review from Phase 0 with brand-new tasks.

## Your Mission

<task>
$ARGUMENTS
</task>

## First Principle — Easy to Change

> **The success metric of every coding decision is _future change cost_.**
> DRY, SRP, abstraction, design patterns, naming, layering, tests — every
> technique exists to serve one goal: **making the next change cheaper**.

When evaluating styling, a layout, a token, or a component, ask:
**does this make the next change cheaper or more expensive?**

- Reject "best practices" that raise change cost (hardcoded values forcing
  per-file edits, hand-rolled overflow handling, raw breakpoints,
  copy-pasted truncation CSS).
- Name the real enemies in findings: **magic values, duplicated styling
  knowledge, fixed sizing that fights the viewport, cross-system token
  mixing, z-index escalation wars**.
- A simpler layout that survives 320px and a 200-char value beats a
  pixel-perfect fixed layout that breaks on either.

Apply this lens **before** invoking any specific rule, pattern, or checklist
below — if a downstream rule would raise change cost, this principle wins.

---

## Review Mindset (NON-NEGOTIABLE)

Skeptical. Every claim needs traced proof, confidence >80%.

- NEVER flag a styling violation without reading the actual SCSS/template + tracing the rendered element
- Every finding MUST include `file:line` evidence
- Before flagging a pattern violation: grep 3+ existing examples — codebase convention wins
- Question: "Is this actually a violation, or an established exception (icon dimensions, fixed brand assets, genuinely fixed UI)?"

## Phase 0: Load UI Rules (MANDATORY FIRST) (MUST ATTENTION)

> **MUST ATTENTION:** Read project UI docs BEFORE reviewing. Rules come from docs, not general knowledge.

- read the project styling rules doc — extract BEM convention, mixin names, variable names, responsive breakpoint mixins, nesting limits
- read the project design-system/token doc — extract design tokens and the **Z-Index & Layering** section
- read the project frontend architecture/patterns doc — extract base component classes, store/effect patterns, API service base, lifecycle teardown pattern
- read the project code-review rules doc — extract frontend anti-patterns and review rules directly

> **CROSS-SYSTEM WARNING (carry through every category):** Do NOT mix token systems with incompatible root-size, namespace, or layer assumptions in one file. When flagging a fix, recommend whichever token system the file already imports/uses; never introduce another system unless the project docs explicitly require migration.

## Phase 1: Determine Scope

**Default (no override):** Review all uncommitted frontend changes.

```bash
git status          # List changed files
git diff            # Staged + unstaged changes
git diff --cached   # Staged only
```

- Collect file list to review
- Filter to files matching the project frontend path/extension patterns resolved from project config/docs
- If ZERO frontend files match → announce `"No frontend changes detected — ui-review skipped"` and report clean (honor the CONDITIONAL skip)

## Phase 2: Blast Radius (if graph.db exists)

- If `.code-graph/graph.db` exists: run graph trace on key changed component files
- Record: impacted file count, shared-component fan-out (a changed shared-library component affects every consumer app), risk level
- Prioritize review by highest-impact files first (shared library components > app-local components)
- Graph unavailable: note "Graph not available — skipping blast radius" and proceed

For each changed component/style file with downstream impact:

```bash
python .claude/scripts/code_graph trace <changed-file> --direction both --json
```

Use `--node-mode file` first (10-30x less noise), then `--node-mode function` for detail. Flag shared-component consumers impacted by a styling or layout change.

## Phase 3: UI Category Review

Create report: `plans/reports/ui-review-{date}-{slug}.md`

For EACH file in scope, evaluate against ALL applicable categories. Skip categories not applicable to the file type (e.g., a pure `.ts` store file skips overflow/sizing/z-index but still hits Category 5's architecture checks and Category 6's loading/error/empty-state wiring).

> **Apply the `Think:` reasoning prompt before each category — derive violations, do NOT recite checklists.**

---

### Category 1: Long-Content Overflow & Truncation — Severity: WARN (HIGH when a flex child truncates with no `min-width: 0`)

**Think:** Does every text container survive a 200-char value? Single-line or multi-line? Can the user still read the full value when it is truncated?

**Detection signals:**

- Hand-rolled `text-overflow: ellipsis` (with `white-space: nowrap` / `overflow: hidden` re-declared by hand) instead of the project mixin/directive
- A flex child that truncates but has **NO `min-width: 0`** — the flex-overflow trap: a flex item's default `min-width: auto` refuses to shrink below content width, so ellipsis never triggers
- Truncated text with **NO tooltip / `title`** to reveal the full value

**DECISION RULE the reviewer enforces:**

- Single-line labels / table cells / chips → ellipsis **+ tooltip-on-overflow**
- Multi-line prose / descriptions → wrap or `-webkit-line-clamp`

**Project fix guidance** (cite real reuse targets from the resolved styling rules doc):

- Prefer the project's documented overflow/ellipsis directive, component, or utility. It must expose the full value only when the element actually overflows and must handle the flex `min-width` trap.
- OR the project's documented truncate/text-ellipsis mixins or utility classes from the styling rules doc.
- Multi-line: use the project-documented clamp pattern.

**GOOD vs BAD:** a utility/token-driven truncation that exposes the full value on overflow (tooltip/`title`) is correct; a hand-rolled substring / width-math truncation, or truncated text with no tooltip, is the anti-pattern. Cite the styling rules doc for the project's reuse targets.

---

### Category 2: Responsive Multi-Screen via Flex — Severity: WARN (BLOCKED only when content is broken on a small screen — clipped, cut off, or unreachable)

**Think:** Is this usable at 320 / 768 / 1024 / 1440? Does the layout flex, wrap, and **reflow from row to column** on small screens? If it genuinely cannot reflow, does it at least stay _usable_ via a fixed `min-width`/`min-height` + `overflow: auto` scroll — or does content get clipped, cut off, or pushed out of reach?

**Small-screen usability — the minimum bar (canonical):**

- **Preferred:** reflow — `flex-wrap: wrap`, a `flex-direction: row → column` switch at the breakpoint, or a responsive grid that collapses to a single column.
- **Acceptable fallback:** when a layout genuinely can't reflow (dense tables, canvases, diagrams, wide data grids), a fixed `min-width`/`min-height` with `overflow: auto` is fine — **scrolling is OK, not a defect.** Do NOT flag a component BLOCKED merely because it scrolls.
- **Hard minimum (BLOCKED if violated):** on a small screen the UI is _usable_ and nothing is **broken** — no clipped, cut-off, or unreachable content/controls (e.g. a submit button pushed off-screen with no scroll path, text overlapping, a fixed row that overflows AND hides content instead of scrolling).
- **Escalation:** if making a surface small-screen-usable would need a refactor too large for the current change, STOP and **confirm scope with the user** before proceeding — note it as a finding, do not silently rewrite the layout.

**Detection signals:**

- Raw `@media (max-width: NNNpx)` / `(min-width: NNNpx)` in component SCSS that bypasses the breakpoint mixins
- A multi-child flex `row` with **NO `flex-wrap`**, **NO `flex-direction: column`** override, AND **no `overflow: auto`** escape → content is trapped and clips on a phone (BLOCKED); the same row WITH a scroll escape is at most WARN (prefer reflow)
- Multi-column CSS grid with fixed column counts / fixed track widths and no single-column collapse and no scroll container at small breakpoints
- Non-flex fixed layouts (absolute positioning, fixed px widths on containers) that cannot reflow AND cannot scroll → content lost off-screen
- Content clipped, overlapping, or a control pushed out of reach below ~360px with no scroll path (BLOCKED). Horizontal scroll _by itself_, with all content still reachable, is the acceptable fallback — not a finding.

**Project fix guidance:**

- Preferred: the project documented responsive-flex mixins/utilities; add `flex-wrap: wrap` and/or the documented `row → column` breakpoint switch so the layout stacks vertically on small screens
- Fallback (when reflow isn't feasible): give the container a sensible `min-width`/`min-height` and `overflow: auto` so everything stays reachable by scroll
- Breakpoints from the project breakpoint tokens — NEVER inline pixel breakpoints
- Large layout refactor required → surface it as a finding and confirm with the user; don't bundle a big responsive rewrite into an unrelated change

**Anti-patterns:** raw `@media` pixel breakpoints that bypass the project's breakpoint mixins; a `flex-direction: row` with no wrap, no column fallback, AND no scroll escape so content clips; and non-flex fixed grids that neither reflow nor scroll. Cite the styling rules doc for documented offenders; grep the changeset for the same patterns.

---

### Category 3: Flex-Grow vs Fixed Width/Height (prefer min/max) — Severity: WARN

**Think:** Must this size be fixed, or can it grow/shrink with content + viewport?

**Detection signals:**

- Fixed `width:` / `height:` in px (≥ ~3 digits) on containers / cards / forms / dialogs

**Project fix guidance:**

- Prefer `flex: 1` / `flex-grow` + `max-width` / `min-width` caps, and `min-width: 0` on truncating flex children
- The project flex-container mixin/utility documented in the styling rules doc
- Reserve fixed px for icons / borders / genuinely fixed UI

**Anti-patterns:** large fixed `width:` / `height:` in px on containers / cards / forms / dialogs (e.g. `width: 964px`, `height: 772px`) that should flex with content + viewport. Cite the styling rules doc for documented offenders.

---

### Category 4: Z-Index Scale Discipline — Severity: BLOCKED (HARD GATE)

**Think:** Which layer does this surface belong to (base / raised / dropdown / sticky / modal / toast)?

**Detection signals:**

- Raw numeric `z-index` (literal value instead of a token)
- **ANY `z-index` with `!important` → BLOCKED** (an escalation war that the next dev will only beat with a bigger literal)

**Project fix guidance — use tokens:**

- The project documented z-index layer tokens
- Existing legacy/framework token systems only when the current file already uses that system
- The semantic layer variables declared canonical by the project design-system doc

Cross-reference the project design-system **Z-Index & Layering** map. The chosen token MUST match the surface's semantic layer.

**GOOD vs BAD:** a `z-index` set from a semantic token / layer scale is correct; a raw literal (e.g. `z-index: 99999`, `z-index: 10000`) or `z-index: N !important` is the anti-pattern. Cite the design-system and styling docs for the project's token scale and documented offenders.

---

### Category 5: SCSS/CSS Best Practices & BEM — Severity: WARN (BLOCKED on `!important`, chained BEM modifiers)

**Think:** Does this stylesheet read cleanly, follow BEM, and use tokens — or does it hardcode, over-nest, and chain modifiers?

> **SCSS/BEM rules (canonical):** BEM classes on ALL template elements (`block__element--modifier`). No magic numbers — use variables / design tokens. Max 3 nesting levels.

**Detection signals:**

- Nesting > 3 levels
- Hardcoded hex colors (should use CSS vars / design tokens)
- `px` where `rem` is expected
- Chained BEM modifiers (`.block__element.--modifier`) — `.--mod` MUST be a separate class, NEVER chained → BLOCKED
- Template elements missing BEM classes
- `!important` → BLOCKED

Apply fixes per the resolved project styling rules doc.

**Frontend architecture checks (OWNED JOINTLY WITH `architecture-review` Category 8 — reference, do not drift):**

> These checks are lifted from `architecture-review` Category 8 so the two skills stay synchronized. They are **owned jointly**; when one changes, update both. They apply to the `.ts` files in scope:

- Components MUST extend the project-documented base component/form/store component classes (BLOCKED)
- State MUST use the project-documented store/effect pattern — NEVER ad hoc local state when the project provides a canonical store pattern (BLOCKED)
- API services MUST extend the project-documented API service base — NEVER raw HTTP clients when the project provides a service abstraction (BLOCKED)
- All subscriptions MUST use the project's auto-teardown operator — NEVER manual unsubscribe (BLOCKED)
- All template elements MUST have BEM classes (WARN)
- Logic in lowest layer: Model > Service > Component (WARN)

---

### Category 6: Async UI States & Feedback — Loading / Error / Empty / Disabled — Severity: BLOCKED (HARD GATE when an async fetch or mutation renders NO loading indicator OR NO user-visible error surface)

> **This is the fundamental UI-resilience gate.** A screen whose happy path renders perfectly but shows a frozen blank while loading, fails silently on error, or shows nothing when empty is a broken user experience. Every async or interactive surface MUST answer three questions for the user: _what do I see while it's working, when it fails, and when there's nothing?_

**Think:** For EACH async operation the file performs (data fetch, form submit, mutation, navigation-triggered load, subscription), trace what the user actually sees in the in-flight, failure, and zero-result branches — not just the success branch. If any of those three branches renders a blank/frozen screen or nothing at all, that is the finding.

**The essential states every async/interactive surface MUST handle** (canonical vocabulary — shared verbatim with `design-spec` "Component States Checklist": Default / Loading / Disabled / Error / Empty / Success):

- **Loading** — every in-flight async request MUST render a loading indicator (spinner / skeleton / progress bar), NEVER a frozen or blank screen. Lists/tables → skeleton rows; buttons → in-button spinner + disabled.
- **Error** — every operation that can fail (network, validation, server error) MUST surface a human-readable error to the user WITH a recovery/retry path where sensible. NEVER a silent failure, a swallowed `catch`, or a raw stack trace / raw error object rendered to the user.
- **Empty** — every collection / list / table view MUST render a meaningful empty state (message + optional CTA) when it has zero items, NOT a blank area.
- **Disabled / in-flight guard** — submit/action controls MUST disable (or show busy) while their request is in-flight, to prevent double-submission.
- **Success** — a completed mutation SHOULD give confirmation feedback (toast / inline / visibly updated data).

**Detection signals:**

- An async call (fetch / HTTP / `subscribe` / awaited mutation) whose template binds NO loading flag (`isLoading` / `pending` / `loading$` / skeleton) → **BLOCKED**
- A `.catch` / `try-catch` / error callback that logs or swallows the error but renders NO user-visible error surface → **BLOCKED**
- A raw error shown to the user (stack trace, raw JSON, unmapped exception) → WARN
- A list/table rendered from a collection with NO empty-state branch (`@empty`, `*ngIf="!items.length"`, `items.length === 0 ? …`) → WARN (BLOCKED when the collection is the screen's primary content)
- A submit handler that does NOT disable its trigger while in-flight (double-submit risk) → WARN (BLOCKED for payment / create / irreversible actions)

> **Check for centralized handling BEFORE flagging BLOCKED (avoid false positives):** many apps satisfy loading/error at the app level — a route-level progress bar, an HTTP interceptor that shows a global spinner/toast, an error boundary, or a base component that renders loading/error for all its children. If such a mechanism demonstrably covers this surface, the local component is compliant — grep for the shared mechanism (per this skill's "grep 3+ counterexamples / established exception" rule) and downgrade or drop the finding. Flag BLOCKED only when NO layer — local or global — gives the user a loading indicator / error surface.

**Project fix guidance** (cite real reuse targets from the resolved frontend/patterns + design-system docs):

- Prefer the project's documented loading component / skeleton / spinner and the documented error-banner / empty-state components or patterns — NEVER hand-roll one-off state UI when a canonical one exists.
- Bind loading / error / empty off the store / view-model / API-service state per the project's documented state pattern — state belongs in the lowest layer (Model > Service > Component), not improvised in the template.

**GOOD vs BAD:** a fetch bound to `isLoading` → skeleton, `error` → inline retry banner, and empty → placeholder is correct; a fetch that renders ONLY the populated happy path (blank while loading, nothing on error, blank when empty) is the anti-pattern. Cite the frontend-patterns and design-system docs for the project's reuse targets.

> **Note vs Category 5's Bug-Detection "Error Handling":** the shared Bug Detection protocol checks that `catch` scope is correct and exceptions are not swallowed at the _code_ level; Category 6 checks that the failure/loading/empty branch produces a _user-visible_ state at the _UI_ level. Both must pass — a correctly-caught error that renders nothing still fails Category 6.

---

## Phase 3B: UI/UX Design Principles Pass (9 dimensions)

The 40 clauses of `SYNC:ui-ux-design-principles` (full body inlined below in this skill) bind this skill in the **REVIEW** role: every clause is a fail-condition, not a suggestion. Run them as **NINE focused passes over the whole scope — one dimension at a time, in order.** A single simultaneous sweep of all nine is what degrades clause review into tick-boxing; serial attention is the mechanism, not a formatting preference.

**Per pass:** answer the `Think:` prompt from first principles FIRST — _what would make this dimension fail on THIS surface?_ — then hunt the violation that reasoning predicts. A pass that produced no reasoning produced no review: record the reasoning, never a tick.

**Every finding:** `UI-<clause>` + `file:line` + severity from the Phase 4 rubric already in force (**BLOCKED** must fix before merge · **WARN** review and decide · **PASS** compliant; a WARN escalates to BLOCKED under the escalation rule stated there). This pass introduces NO new severity scale.

**Precedence (MUST ATTENTION):** the project styling / design-system / frontend-pattern docs loaded in Phase 0 **OUTRANK** these clauses; the clauses outrank generic taste. Where a project doc states its own value (type scale, spacing unit, breakpoints, token contrast pairs), the PROJECT value is the rule and the clause is satisfied by following it. A genuine conflict is SURFACED to the user via `AskUserQuestion` with both sides — NEVER resolved silently.

| #   | Dimension                 | Clauses           | `Think:`                                                                                                                                                                                                                                                                                                                                           |
| --- | ------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Visual Hierarchy & Layout | `UI-1.1`-`UI-1.5` | Which element does a first-time user's eye land on, and is it the one this screen exists for? Which groups are held together by whitespace, and which by a border added because the whitespace was wrong? Are the empty, loading and error states designed at all — or only the full state?                                                        |
| 2   | Typography                | `UI-2.1`-`UI-2.5` | Trace every family/size/weight declaration in scope back to the project type scale — which are one-off literals? At the widest breakpoint, how many characters per line does body text actually reach, and does any text a user must read fall below 14px?                                                                                         |
| 3   | Colour & Contrast         | `UI-3.1`-`UI-3.4` | For each foreground/background pair that actually renders, what is the COMPUTED ratio (measured — never judged by eye)? What does a user who cannot perceive the accent hue see instead? In dark mode, is elevation signalled by lifted surfaces or by an inversion?                                                                               |
| 4   | Spacing & Grid            | `UI-4.1`-`UI-4.4` | Is every gap a multiple of the project base unit, or are there arbitrary values? Does spacing come from the container (`gap`) or from margins scattered across children? Is inner padding smaller than the gap to the next group? Do breakpoints break where the layout fails, or where a device is named?                                         |
| 5   | Interaction & Feedback    | `UI-5.1`-`UI-5.5` | For each interactive element: what changes visually within 100ms of the press? Which of the five states (default/hover/focus/active/disabled) is unstyled? Is the focus ring still visible after restyling? Could undo replace this confirmation? Does motion honour reduced-motion?                                                               |
| 6   | Navigation & IA           | `UI-6.1`-`UI-6.4` | Landing on this screen cold: where am I, what's here, where next? How many top-level destinations exist? Are labels the user's words or the team's internal vocabulary? Does this state have a URL or back path, and where does hardware back land?                                                                                                |
| 7   | Forms & Input             | `UI-7.1`-`UI-7.5` | Field by field: what breaks if this field is removed today? Is its label still visible once filled? When does validation fire, and does the message say how to fix it? Does the keyboard/autocomplete match the data type? What happens to typed data on validation error, navigation away, and refresh?                                           |
| 8   | Mobile & Touch            | `UI-8.1`-`UI-8.4` | At a touch viewport: measure each tappable element's HIT BOX (not the icon) and the gap to its neighbours; where do primary actions sit relative to the thumb; is anything reachable ONLY by gesture; what do notch, home indicator and the on-screen keyboard cover? _(Mobile/touch surfaces only — when the scope has none, say so explicitly.)_ |
| 9   | Speed & Perceived Speed   | `UI-9.1`-`UI-9.4` | For everything that loads: what occupies its space before data arrives, and does the layout shift when it lands? Is the optimistic path rolled back VISIBLY on failure? On a slow or offline connection, what does the user see — a designed state or a hang?                                                                                      |

**No double-counting.** Several clauses overlap Categories 1-6 (`UI-1.5`/`UI-5.2`/`UI-9.1` overlap Category 6's async-state gate; `UI-2.3` overlaps Category 1's content handling; `UI-4.1` overlaps Category 5's magic-number rule; `UI-4.4` overlaps Category 2's responsive bar). Where they meet, emit **ONE** finding carrying BOTH citations (e.g. `Category 6` + `UI-5.2`) at the HIGHER of the two severities — never two findings for one defect, and never a downgrade because "the other category already covers it".

**Skip rule.** This pass runs whenever any frontend file is in scope. Skip an individual dimension ONLY when the scope contains no surface it can apply to (`UI-8.*` with no touch surface, `UI-7.*` with no input) — name the skipped dimensions and the reason, so a skip is auditable rather than an omission.

---

## Phase 4: Finalize — UI Compliance Report

Update report with final sections:

### Verdict Scoring

| Verdict     | Condition                                       |
| ----------- | ----------------------------------------------- |
| **BLOCKED** | 1+ BLOCKED findings — must fix before merge     |
| **WARN**    | 0 BLOCKED, 1+ WARN findings — review and decide |
| **PASS**    | 0 BLOCKED, 0 WARN — UI compliant                |

> **Severity vocabulary (single source of truth).** Category headers and this verdict table use `BLOCKED` / `WARN` / `PASS`. The fresh sub-agent (Phase 5 and Round 2) emits `Critical / High / Medium / Low` + `PASS / FAIL` from the shared review-protocol template. Reconcile the two with this mapping — do NOT treat them as separate scales:
>
> | This skill | Sub-agent (Round 2)      | Merge gate            |
> | ---------- | ------------------------ | --------------------- |
> | BLOCKED    | Critical / High → FAIL   | Must fix before merge |
> | WARN       | Medium / Low → WARN/INFO | Review and decide     |
> | PASS       | (no findings) → PASS     | Merge-clear           |
>
> A category's **"(HIGH when …)"** note is NOT a separate tier — it means that WARN **escalates to BLOCKED** when the stated condition holds (i.e., the finding is a real rendered bug, not a latent risk).

### Report Structure

```markdown
# UI Review Report — {date}

## Scope

- Files reviewed: {count}
- Components / apps affected: {list}
- Blast radius: {summary from Phase 2}

## Verdict: {PASS | WARN | BLOCKED}

## BLOCKED Findings (Must Fix)

### {Category}: {description}

- **File:** {path}:{line}
- **Rule:** {rule from project UI doc}
- **Evidence:** {what was found}
- **Fix:** {reuse target to use — directive / mixin / token}

## WARN Findings (Review)

### {Category}: {description}

- **File:** {path}:{line}
- **Rule:** {rule from project UI doc}
- **Evidence:** {what was found}
- **Recommendation:** {suggested action}

## PASS Categories

- {list of categories that passed with no findings}

## UI Health Summary

- Long-content Overflow & Truncation: {PASS/WARN/BLOCKED}
- Responsive Multi-Screen (flex-wrap / row→column, usable on small devices): {PASS/WARN/BLOCKED}
- Flex-Grow vs Fixed Sizing: {PASS/WARN/BLOCKED}
- Z-Index Scale Discipline: {PASS/WARN/BLOCKED}
- SCSS/CSS Best Practices & BEM: {PASS/WARN/BLOCKED}
- Async UI States & Feedback (loading / error / empty / disabled): {PASS/WARN/BLOCKED}
- Frontend Architecture (joint w/ architecture-review): {PASS/WARN/BLOCKED/N/A}
```

---

## Systematic Review Protocol (10+ changed frontend files)

1. **Categorize** — Group files by app / shared-library / component concern
2. **Parallel Sub-Agents** — Launch one UI/UX-specialized sub-agent per group with the UI-category checklist
3. **Synchronize** — Collect findings, cross-reference shared-component consumers and cross-system token mixing
4. **Consolidate** — Single holistic report with per-category verdicts

---

## Phase 5: Why-Review Findings Validation Gate (MANDATORY when findings exist)

> **Purpose:** Adversarial validation of own findings BEFORE handoff. Catches over-flagged Highs, false positives, and severity inflation at the source rather than letting them propagate downstream.

**Trigger:** Any finding produced (Critical, High, Medium, OR Low). Skip ONLY when the report's verdict is unconditional PASS with literally zero findings.

**Protocol:**

1. Read own finalized report from `plans/reports/ui-review-{date}-{slug}.md` (the exact path written in Phase 3 — NOT `{skill}-…`)
2. Invoke `/why-review --validate-findings plans/reports/ui-review-{date}-{slug}.md`
3. Read the validation verdict path returned by why-review, expected as `plans/reports/why-review-validate-{date}.md`
4. **If why-review demotes/removes any finding:** UPDATE own finalized report with revised severities, remove false positives, and add a `## Why-Review Validation Notes` section citing what changed and why
5. **If why-review confirms all findings:** Append `## Why-Review Validation` line to own report stating "All N findings re-validated against actual code; no severity changes."
6. **If the report changed after validation:** re-run this validation gate, maximum 2 validation passes, until the report's remaining findings are validated or zero findings remain.

**Skip conditions (record explicit reason if skipping):**

- Verdict is unconditional PASS with zero findings → log "Skipped — no findings to validate"
- Why-review skill itself is the active context (avoid recursion)

**Why this exists:** AI sub-agent reports inherit confirmation bias — the orchestrator absorbs severity claims as ground truth. The 2026-05-09 review incident produced 5 Highs; adversarial validation demoted 3 of them. Codify this as standard practice.

---

## Phase 6: Validated Fix + Full UI Re-Review Loop (MANDATORY when validated findings remain)

**Trigger:** Phase 5 returns CLEAN/validated and the UI review report still has one or more findings that must be fixed.

**Protocol:**

1. Create a fresh fix-cycle task list before editing. Do not reuse the review tasks.
2. Fix only findings that survived `/why-review --validate-findings`; route broader or cross-cutting fixes through the parent `/plan` + `/feature-implement` flow when this skill is running inside a workflow.
3. Run targeted verification for the fixed UI files and any affected consumers.
4. Re-invoke `/ui-review` from Phase 0 over the full current UI scope, not only the fixed files.
5. The re-run MUST create brand-new review tasks, reload the UI docs, determine scope again, rerun blast radius where applicable, and review every changed UI file from the start.
6. Repeat validate → fix → full UI re-review until a complete pass has zero findings.
7. If the same validated blocker repeats across 2 full invocations with no progress, stop and ask the user for a decision.

**Non-negotiable rules:**

- Never fix a finding before `/why-review --validate-findings` validates it.
- Never mark UI review clean after a targeted fix check only; the clean verdict must come from a full Phase 0 restart.
- Never review only fixed files during the recursive pass; analyze all UI files in scope again.
- Never reuse old todo/task items for the recursive review pass.

---

## Workflow Recommendation

> **MANDATORY — NO EXCEPTIONS:** If NOT already in a workflow, MUST use `AskUserQuestion` to ask user. Do NOT judge task complexity or decide "simple enough to skip" — user decides, not you:
>
> 1. **Activate `workflow-review-changes` workflow** (Recommended) — run the canonical workflow from `.claude/workflows.json`; it runs UI review in TWO places by design (keep both) — internally as `/changes-review`'s UI dimension AND as a dedicated conditional parallel-batch reviewer (step 9) — alongside findings validation, the other parallel reviewers, `code-simplifier` self-review, fix-plan cycle, full re-review restart, docs, and handoff.
> 2. **Execute `/ui-review` directly** — run this skill standalone

---

## Next Steps

**MANDATORY — NO EXCEPTIONS:** After completing, use `AskUserQuestion` to present:

- **"/code-simplifier" (Recommended)** — Simplify and refine the styling/component code
- **"/web-design-guidelines"** — Generic accessibility / UX checklist for a11y depth
- **"Skip, continue manually"** — user decides

## AI Agent Integrity Gate (NON-NEGOTIABLE)

Before reporting ANY work done:

1. **Grep every removed name.** Extraction/rename/delete → grep confirms 0 dangling refs across ALL file types (SCSS `@use`, template class refs, TS imports)
2. **Ask WHY before changing.** Existing values intentional until proven otherwise — a fixed `width` may be a genuinely fixed UI element; no "fix" without traced rationale
3. **Verify ALL outputs.** One compiled stylesheet ≠ all consumers — a shared-component style change affects every consuming app
4. **Evaluate pattern fit.** Copying a nearby mixin/token? Verify the file imports/uses the SAME token system and does not mix incompatible project token systems
5. **New artifact = wired artifact.** Created a class/mixin? Prove it is imported, referenced in the template, and reachable

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting. Simple tasks: ask user whether to skip.

<!-- OVERRIDE:fresh-context-review -->

> **Fresh Context Re-Review** — Eliminate orchestrator confirmation bias after fixes by restarting the full review with isolated sub-agents where applicable.
>
> **Why:** The main agent knows what it (or `/feature-implement`) just fixed and rationalizes findings accordingly. A fresh sub-agent has ZERO memory, re-reads from scratch, and catches what the main agent dismissed. Sub-agent bias is mitigated by (1) fresh context, (2) verbatim protocol injection, (3) main agent not filtering the report.
>
> **When:** ONLY after a validated-finding fix cycle, or when the user/workflow explicitly requests an independent high-risk UI synthesis pass. A review pass that finds issues triggers validation first; it does NOT trigger a fresh-context pass over the same findings before validation/fix.
>
> **How:**
>
> 1. Start a NEW full review invocation/task breakdown; when that protocol calls for agents, spawn a NEW `Agent` tool call — use the UI/UX-specialized subagent_type from the local sub-agent selection guide
> 2. Inject ALL required review protocols VERBATIM into the prompt — see `SYNC:review-protocol-injection` for the full list and template. Never reference protocols by file path; AI compliance drops behind file-read indirection (see `SYNC:shared-protocol-duplication-policy`)
> 3. Sub-agent re-reads ALL target files from scratch via its own tool calls — never pass file contents inline in the prompt
> 4. Sub-agent writes structured report to `plans/reports/{review-type}-round{N}-{date}.md`
> 5. Main agent reads the report, integrates findings into its own report, DOES NOT override or filter
>
> **Rules:**
>
> - NEVER reuse a sub-agent across rounds — every iteration that uses sub-agents spawns a NEW `Agent` call
> - NEVER fix unvalidated findings; validate first using the caller's validation gate
> - NEVER skip the full review restart after a validated fix cycle — every fix invalidates the prior verdict
> - Continue until a complete full review pass has zero findings; if the same blocker repeats across 2 full invocations with no progress, escalate via `AskUserQuestion`
> - Track iteration count in conversation context (session-scoped, no persistent files)

<!-- /OVERRIDE:fresh-context-review -->

## Sub-Agent Type Override

> **MANDATORY:** UI reviews spawn the UI/UX-specialized sub-agent defined by the local sub-agent selection guide.
> Keep `subagent_type: "ui-ux-designer"` in the canonical template below when that agent type exists in the local catalog.
> **Rationale:** The shared sub-agent selection guide routes frontend UI/UX, accessibility, responsive layout, and design-token work to the UI/UX specialization. Do not fall back to a generic code-reviewer catch-all unless the local catalog lacks a UI/UX reviewer.

<!-- OVERRIDE:review-protocol-injection -->

> **Review Protocol Injection** — Every fresh sub-agent review prompt MUST embed 11 protocol blocks VERBATIM. The template below has ALL 11 bodies already expanded inline. Copy the template wholesale into the Agent call's `prompt` field at runtime, replacing only the `{placeholders}` in Task / Round / Reference Docs / Target Files / Output sections with context-specific values. Do NOT touch the embedded protocol sections.
>
> **Why inline expansion:** Placeholder markers would force file-read indirection at runtime. AI compliance drops significantly behind indirection (see `SYNC:shared-protocol-duplication-policy`). Therefore the template carries all 11 protocol bodies pre-embedded.

### Subagent Type Selection

- `ui-ux-designer` — default for UI reviews when the local agent catalog provides it
- `code-reviewer` — fallback only when the local catalog lacks a UI/UX-specialized reviewer

### Canonical Agent Call Template (Copy Verbatim)

```
Agent({
  description: "Fresh Round {N} UI review",
  subagent_type: "ui-ux-designer",
  prompt: `
## Task
{review-specific task — e.g., "Review all uncommitted frontend changes for UI quality: long-content overflow, responsive layout (flex-wrap / row→column, usable on small devices), flex-vs-fixed sizing, z-index discipline, SCSS/BEM, and async UI states & feedback (loading indicator, user-visible error surface, empty state, in-flight disable)" | "Review SCSS/template files under {path}"}

## Round
Round {N}. You have ZERO memory of prior rounds. Re-read all target files from scratch via your own tool calls. Do NOT trust anything from the main agent beyond this prompt.

## Protocols (follow VERBATIM — these are non-negotiable)

### Spec ↔ Tests ↔ Code Triangulation
DO THIS FIRST — before any per-protocol check below. The review target is the WHOLE PACKAGE, not the diff alone: load the behavior's spec (§3 ACs / §4 BRs / §8 TCs), its tests, and the changed code TOGETHER, and reason about their mutual consistency BEFORE judging any one in isolation.
1. Locate all three faces: the Feature Spec section(s) governing the changed behavior, the tests that guard it, and the production code that implements it. A missing face is itself a finding (SPEC-GAP / TEST-GAP / DEAD-SPEC).
2. Triangulate pairwise — every disagreement is a finding; classify which face is wrong:
   - code vs spec: behavior the code does that no §3/§4/§8 rule describes → CODE-EXTRA or SPEC-STALE; a [HARD] §4 rule or §5 invariant with no enforcing code path → CODE-WRONG.
   - tests vs spec: a §8 TC with no test, or a test asserting behavior no TC/rule names → TEST-GAP or SPEC-SILENT.
   - tests vs code: a changed code path with no covering test → TEST-GAP; a test that still passes against a deliberately broken invariant → WEAK-TEST (apply the mutation thinking in Bug Detection).
3. Hidden-rule capture: any invariant the code enforces but the spec never states (SPEC-SILENT) MUST be surfaced as a finding to add into §3/§4/§8 AND guarded with a test — the enrichment loop, never a silent pass.
4. Only after the three faces agree — or every disagreement is logged as a finding — proceed to the per-protocol checks below; when enrichment adds spec/test content, re-review the package against the enriched spec.
NEVER mark review PASS while any spec/test/code face disagrees without a logged finding. The diff is the entry point; the package is the unit of judgment.

### Evidence-Based Reasoning
Speculation is FORBIDDEN. Every claim needs proof.
1. Cite file:line, grep results, or framework docs for EVERY claim
2. Declare confidence: >80% act freely, 60-80% verify first, <60% DO NOT recommend
3. Cross-service validation required for architectural changes
4. "I don't have enough evidence" is valid and expected output
BLOCKED until: Evidence file path (file:line) provided; Grep search performed; 3+ similar patterns found; Confidence level stated.
Forbidden without proof: "obviously", "I think", "should be", "probably", "this is because".
If incomplete → output: "Insufficient evidence. Verified: [...]. Not verified: [...]."

### Bug Detection
MUST check categories 1-4 for EVERY review. Never skip.
1. Null Safety: Can params/returns be null? Are they guarded? Optional chaining gaps? .find() returns checked?
2. Boundary Conditions: Off-by-one (< vs <=)? Empty collections handled? Zero/negative values? Max limits?
3. Error Handling: Try-catch scope correct? Silent swallowed exceptions? Error types specific? Cleanup in finally?
4. Resource Management: Connections/streams closed? Subscriptions unsubscribed on destroy? Timers cleared? Memory bounded?
5. Concurrency (if async): Missing await? Race conditions on shared state? Stale closures? Retry storms?
6. Stack-Specific: Check the configured language/runtime pitfalls and framework-specific failure modes discovered from local code.
Classify: CRITICAL (crash/corrupt) → FAIL | HIGH (incorrect behavior) → FAIL | MEDIUM (edge case) → WARN | LOW (defensive) → INFO.

### Design Patterns Quality
Priority checks for every code change:
1. DRY via OOP: Same-suffix classes (*Entity, *Dto, *Service) MUST share base class. 3+ similar patterns → extract to shared abstraction.
2. Right Responsibility: Logic in LOWEST layer (Entity > Domain Service > Application Service > Controller). Never business logic in controllers.
3. SOLID: Single responsibility (one reason to change). Open-closed (extend, don't modify). Liskov (subtypes substitutable). Interface segregation (small interfaces). Dependency inversion (depend on abstractions).
4. After extraction/move/rename: Grep ENTIRE scope for dangling references. Zero tolerance.
5. YAGNI gate: NEVER recommend patterns unless 3+ occurrences exist. Don't extract for hypothetical future use.
Anti-patterns to flag: God Object, Copy-Paste inheritance, Circular Dependency, Leaky Abstraction.

### Logic & Intention Review
Verify WHAT code does matches WHY it was changed.
1. Change Intention Check: Every changed file MUST serve the stated purpose. Flag unrelated changes as scope creep.
2. Happy Path Trace: Walk through one complete success scenario through changed code.
3. Error Path Trace: Walk through one failure/edge case scenario through changed code.
4. Acceptance Mapping: If plan context available, map every acceptance criterion to a code change.
5. Tests Verify Intent: For test/spec changes, verify tests name the protected business rule or invariant and would fail if that intent breaks.
6. Migration Test Exclusion: Do not write tests for migration code. Schema/data migrations are one-time execution paths, not core application logic.
NEVER mark review PASS without completing both traces (happy + error path).

### Test Spec Verification
Map changed code to test specifications.
1. Identify the project's test/spec format from existing docs, test-case files, BDD feature files, or spec folders.
2. Every changed code path MUST map to a corresponding test case/spec (or flag as "needs test case").
3. New functions/endpoints/handlers → flag for test spec creation.
4. Migration files are excluded from test/spec creation; schema/data migrations are one-time execution paths, not core application logic.
5. If spec evidence fields exist, verify they point to actual code (file:line, not stale references).
6. Verify each meaningful test case names the business intent/invariant; flag behavior-only cases that only mirror implementation details.
7. Auth/data changes → verify corresponding authorization and data-state test cases exist.
8. If no specs exist for a changed path → log the gap and recommend the project's test-spec workflow.
NEVER skip test mapping. Untested code paths are the #1 source of production bugs.

### Behavioral Delta Matrix
MANDATORY for any bugfix review. Produce input-state × pre-fix × post-fix × delta table BEFORE writing verdict.
- Minimum 3 rows; include at least one row OUTSIDE the original bug report.
- Any "REGRESSION" delta → review returns FAIL until a preservation test is added.
- Narrative descriptions do NOT substitute for the matrix.
Example rows (external-record sync fix):
| Input                 | Pre-fix | Post-fix                  | Delta      |
| --------------------- | ------- | ------------------------- | ---------- |
| Record exists (valid) | Reused  | Always recreated → orphan | REGRESSION |
| Record missing (404)  | Error   | Recreated                 | Fixed      |

### Fix-Layer Accountability
NEVER fix at the crash site. Trace the full flow, fix at the owning layer. The crash site is a SYMPTOM, not the cause.
MANDATORY before ANY fix:
1. Trace full data flow — Map the complete path from data origin to crash site across ALL layers (storage → backend → API → frontend → UI). Identify where bad state ENTERS, not where it CRASHES.
2. Identify the invariant owner — Which layer's contract guarantees this value is valid? Fix at the LOWEST layer that owns the invariant, not the highest layer that consumes it.
3. One fix, maximum protection — If fix requires touching 3+ files with defensive checks, you are at the wrong layer — go lower.
4. Verify no bypass paths — Confirm all data flows through the fix point. Check for direct construction skipping factories, clone/spread without re-validation, raw data not wrapped in domain models, mutations outside the model layer.
BLOCKED until: Full data flow traced (origin → crash); Invariant owner identified with file:line evidence; All access sites audited (grep count); Fix layer justified (lowest layer that protects most consumers).
Anti-patterns (REJECT): "Fix it where it crashes" (crash site ≠ cause site, trace upstream); "Add defensive checks at every consumer" (scattered defense = wrong layer); "Both fix is safer" (pick ONE authoritative layer).

### Rationalization Prevention
AI skips steps via these evasions. Recognize and reject:
- "Too simple for a plan" → Simple + wrong assumptions = wasted time. Plan anyway.
- "I'll test after" → RED before GREEN. Write/verify test first.
- "Already searched" → Show grep evidence with file:line. No proof = no search.
- "Just do it" → Still need TaskCreate. Skip depth, never skip tracking.
- "Just a small fix" → Small fix in wrong location cascades. Verify file:line first.
- "Code is self-explanatory" → Future readers need evidence trail. Document anyway.
- "Combine steps to save time" → Combined steps dilute focus. Each step has distinct purpose.

### Graph-Assisted Investigation
MANDATORY when .code-graph/graph.db exists.
HARD-GATE: MUST run at least ONE graph command on key files before concluding any investigation.
Pattern: Grep finds files → trace --direction both reveals full system flow → Grep verifies details.
- Investigation/Scout: trace --direction both on 2-3 entry files
- Fix/Debug: callers_of on buggy function + tests_for
- Feature/Enhancement: connections on files to be modified
- Code Review: tests_for on changed functions
- Blast Radius: trace --direction downstream
CLI: python .claude/scripts/code_graph {command} --json. Use --node-mode file first (10-30x less noise), then --node-mode function for detail.

### Understand Code First
HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
1. Search 3+ similar patterns (grep/glob) — cite file:line evidence.
2. Read existing files in target area — understand structure, base classes, conventions.
3. Run python .claude/scripts/code_graph trace <file> --direction both --json when .code-graph/graph.db exists.
4. Map dependencies via connections or callers_of — know what depends on your target.
5. Write investigation to .ai/workspace/analysis/ for non-trivial tasks (3+ files).
6. Re-read analysis file before implementing — never work from memory alone.
7. NEVER invent new patterns when existing ones work — match exactly or document deviation.
BLOCKED until: Read target files; Grep 3+ patterns; Graph trace (if graph.db exists); Assumptions verified with evidence.

## Reference Docs (READ before reviewing)
- {resolved project styling rules doc}
- {resolved project design-system/token doc, especially Z-Index & Layering}
- {resolved project frontend architecture/patterns doc}
- {resolved project code-review rules doc}

## Target Files
{explicit file list OR "run git diff and filter by the project frontend path/extension patterns"}

## Output
Write a structured report to plans/reports/ui-review-round{N}-{date}.md with sections:
- Status: PASS | FAIL
- Issue Count: {number}
- Critical Issues (with file:line evidence)
- High Priority Issues (with file:line evidence)
- Medium / Low Issues
- Cross-cutting findings (cross-system token mixing, shared-component fan-out)

Return the report path and status to the main agent.
Every finding MUST have file:line evidence. Speculation is forbidden.
`
})
```

### Rules

- DO copy the template wholesale — including all 11 embedded protocol sections
- DO replace only the `{placeholders}` in Task / Round / Reference Docs / Target Files / Output sections with context-specific content
- DO keep the UI/UX-specialized `subagent_type` for UI reviews when the local catalog provides it (see Sub-Agent Type Override above)
- DO NOT paraphrase, summarize, or skip any protocol section
- DO NOT pass file contents inline — the sub-agent reads via its own tool calls so it has a fresh context
- DO NOT reference protocols by file path or tag name — the bodies are already embedded above
- DO NOT introduce placeholder markers for the protocols — they must stay literally expanded

<!-- /OVERRIDE:review-protocol-injection -->

> **Critical Purpose:** UI quality — no content overflow without escape, no broken responsive layouts (rows that never wrap or stack on small devices), no fixed sizing fighting the viewport, no z-index escalation wars, no styling/BEM drift, and no async surface that leaves the user staring at a frozen blank while loading, a silent failure on error, or a blank area when empty.

> **External Memory:** Complex/lengthy work → write findings to `plans/reports/`. Prevents context loss, serves as deliverable.

> **Evidence Gate:** MANDATORY — every finding requires `file:line` proof + confidence percentage (>80% act, <80% verify first).

<!-- OVERRIDE-NOTE:fresh-context-review -->

> **`fresh-context-review` is intentionally OVERRIDE-only in this skill** — see the `OVERRIDE:fresh-context-review` block above (it uses the UI/UX-specialized `ui-ux-designer` subagent_type, NOT the generic `code-reviewer`). The generic `SYNC:fresh-context-review` copy is deliberately omitted here so the two cannot drift into a `code-reviewer` vs `ui-ux-designer` contradiction. This mirrors how `OVERRIDE:review-protocol-injection` is handled (override-only, no generic SYNC copy). **Do NOT re-add the generic `SYNC:fresh-context-review` block** — the `sync-inline-versions.md` propagation only updates existing `SYNC:` markers, so omission is stable.

> **`ui-ux-design-principles` is deliberately NOT inside the `OVERRIDE:review-protocol-injection` template.** That template's protocol region MUST stay substance-identical to canonical `SYNC:review-protocol-injection` across all three OVERRIDE carriers (`integration-test-review`, `architecture-review`, `ui-review`) — `sync-carrier-parity.test.cjs` pins it, precisely because those copies silently drifted once before. Adding a 12th protocol here fails that guard. The dispatched reviewer still receives the 40 clauses: this skill's fresh-eyes sub-agent is `ui-ux-designer`, and `.claude/agents/ui-ux-designer.md` carries `SYNC:ui-ux-design-principles` in its own definition. **Do NOT add the clauses to the injection template** — route them through the specialist agent instead. — why: a shared template that also feeds security and integration reviewers is the wrong layer for UI-only clauses.

<!-- /OVERRIDE-NOTE:fresh-context-review -->

> **Complexity Prevention (UI-scoped)** — measure code by cost of change: one UI change should map to one code change. The full backend-OOP treatise (anemic models, primitive obsession, value objects, repo leakage) does not apply to UI review and is intentionally not carried here. UI-relevant essence: (1) **extract repeated component lifecycle** — 3+ forms/list views reimplementing loading/dirty/submit/pagination → base component / hook / composable / mixin; (2) **keep derivations, formatting, and validation off the template** — move them onto the model / store / view-model / API service, not inline in the component. For deeper OOP/DRY structural review of any backend the UI calls, defer to `/changes-review` / `/architecture-review`.

<!-- SYNC:graph-assisted-investigation -->

> **Graph-Assisted Investigation** — MANDATORY when `.code-graph/graph.db` exists.
>
> **HARD-GATE:** MUST ATTENTION run at least ONE graph command on key files before concluding any investigation.
>
> **Pattern:** Grep finds files → `trace --direction both` reveals full system flow → Grep verifies details
>
> | Task                | Minimum Graph Action                         |
> | ------------------- | -------------------------------------------- |
> | Investigation/Scout | `trace --direction both` on 2-3 entry files  |
> | Fix/Debug           | `callers_of` on buggy function + `tests_for` |
> | Feature/Enhancement | `connections` on files to be modified        |
> | Code Review         | `tests_for` on changed functions             |
> | Blast Radius        | `trace --direction downstream`               |
>
> **CLI:** `python .claude/scripts/code_graph {command} --json`. Use `--node-mode file` first (10-30x less noise), then `--node-mode function` for detail.

<!-- /SYNC:graph-assisted-investigation -->

<!-- SYNC:nested-task-creation -->

> **Nested Task Expansion Contract** — For workflow-step invocation, the `[Workflow] ...` row is only a parent container; the child skill still creates visible phase tasks.
>
> 1. Call `TaskList` first. If a matching active parent workflow row exists, set `nested=true` and record `parentTaskId`; otherwise run standalone.
> 2. Create one task per declared phase before phase work. When nested, prefix subjects `[N.M] $skill-name — phase`.
> 3. When nested, link the parent with `TaskUpdate(parentTaskId, addBlockedBy: [childIds])`.
> 4. Orchestrators must pre-expand a child skill's phase list and link the workflow row before invoking that child skill or sub-agent.
> 5. Mark exactly one child `in_progress` before work and `completed` immediately after evidence is written.
> 6. Complete the parent only after all child tasks are completed or explicitly cancelled with reason.
>
> **Blocked until:** `TaskList` done, child phases created, parent linked when nested, first child marked `in_progress`.

<!-- /SYNC:nested-task-creation -->

<!-- SYNC:project-reference-docs-guide -->

> **Project Reference Docs Gate** — Run after task-tracking bootstrap and before target/source file reads, grep, edits, or analysis. Project docs override generic framework assumptions.
>
> 1. Identify scope: file types, domain area, and operation.
> 2. **Read `docs/project-config.json` first — the project's machine-readable map.** It is the single source of truth for THIS repo (modules/paths, framework + search keywords, test/E2E/integration run-commands, design system, architecture rules, workflow patterns); ground exact paths, run-commands, and conventions on it **before investigating, planning, or coding** — never assume framework defaults (`CLAUDE.md` + reference docs are derived from it). If it — or the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any required reference doc — is missing or stale, auto-run `/project-init` or the narrow route (`/project-config`, `/docs-init`, `/scan-all`, `/scan --target=<key>`, `/claude-md-init`) first; if Codex mirrors or `AGENTS.md` are stale, ask the user to run `/sync-codex` (never auto-run it).
> 3. Required docs by trigger: always `docs/project-reference/lessons.md`; doc lookup `docs-index-reference.md`; review `code-review-rules.md`; backend/CQRS/API `backend-patterns-reference.md`; domain/entity `domain-entities-reference.md`; frontend/UI `frontend-patterns-reference.md`; styles/design `scss-styling-guide.md` + `design-system/design-system-canonical.md`; integration tests `integration-test-reference.md`; E2E `e2e-test-reference.md`; feature docs/specs `feature-spec-reference.md` + `spec-system-reference.md` + `spec-principles.md`; behavior/public-contract/spec-test-code sync `workflow-spec-test-code-cycle-reference.md`; derived spec index/ERD/reimplementation guides `spec-system-reference.md` + source Feature Specs under `docs/specs/`; architecture/new area `project-structure-reference.md`.
> 4. Read every required doc, then before target work state: `Reference docs read: ... | Not applicable: ...`.
>
> **Ready when:** scope evaluated, `docs/project-config.json` consulted, required docs checked/read or setup route completed, `lessons.md` confirmed, citation emitted.

<!-- /SYNC:project-reference-docs-guide -->

<!-- SYNC:task-tracking-external-report -->

> **Task Tracking & External Report Persistence** — Bootstrap this before execution; then run project-reference doc prefetch before target/source work.
>
> 1. Create a small task breakdown before target file reads, grep, edits, or analysis. On context loss, inspect the current task list first.
> 2. Mark one task `in_progress` before work and `completed` immediately after evidence; never batch transitions.
> 3. For plan/review work, create `plans/reports/{skill}-{YYMMDD}-{HHmm}-{slug}.md` before first finding.
> 4. Append findings after each file/section/decision and synthesize from the report file at the end.
> 5. Final output cites `Full report: plans/reports/{filename}`.
>
> **Blocked until:** task breakdown exists, report path declared for plan/review work, first finding persisted before the next finding.

<!-- /SYNC:task-tracking-external-report -->

<!-- SYNC:subagent-return-contract -->

> **Sub-Agent Return Contract** — When this skill spawns a sub-agent, the sub-agent MUST return ONLY this structure. Main agent reads only this summary — NEVER requests full sub-agent output inline.
>
> ```markdown
> ## Sub-Agent Result: [skill-name]
>
> Status: ✅ PASS | ⚠️ PARTIAL | ❌ FAIL
> Confidence: [0-100]%
>
> ### Findings (Critical/High only — max 10 bullets)
>
> - [severity] [file:line] [finding]
>
> ### Actions Taken
>
> - [file changed] [what changed]
>
> ### Blockers (if any)
>
> - [blocker description]
>
> Full report: plans/reports/[skill-name]-[date]-[slug].md
> ```
>
> Main agent reads `Full report` file ONLY when: (a) resolving a specific blocker, or (b) building a fix plan.
> Sub-agent writes full report incrementally (per SYNC:incremental-persistence) — not held in memory.
>
> **Context budget** — the return payload is a SUMMARY, not a transcript: ≤10 finding bullets, no raw file contents / full diffs / verbatim logs inline, no re-pasted source. Everything beyond the summary lives in the `Full report` on disk. A sub-agent that would exceed the summary shape MUST write the detail to its report and return only the pointer — the orchestrator's context is the scarce resource the whole map-reduce protects.

<!-- /SYNC:subagent-return-contract -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:sequential-thinking-protocol -->

> **Sequential Thinking Protocol** — Structured multi-step reasoning for complex/ambiguous work. Use when planning, reviewing, debugging, or refining ideas where one-shot reasoning is unsafe.
>
> **Trigger when:** complex problem decomposition · adaptive plans needing revision · analysis with course correction · unclear/emerging scope · multi-step solutions · hypothesis-driven debugging · cross-cutting trade-off evaluation.
>
> **Format (explicit mode — visible thought trail):**
>
> 1. `Thought N/M: [aspect]` — one aspect per thought, state assumptions/uncertainty
> 2. `Thought N/M [REVISION of Thought K]: ...` — when prior reasoning invalidated; state Original / Why revised / Impact
> 3. `Thought N/M [BRANCH A from Thought K]: ...` — explore alternative; converge with decision rationale
> 4. `Thought N/M [HYPOTHESIS]: ...` then `[VERIFICATION]: ...` — test before acting
> 5. `Thought N/N [FINAL]` — only when verified, all critical aspects addressed, confidence >80%
>
> **Mandatory closers:** Confidence % stated · Assumptions listed · Open questions surfaced · Next action concrete.
>
> **Stop conditions:** confidence <80% on any critical decision → escalate via AskUserQuestion · ≥3 revisions on same thought → re-frame the problem · branch count >3 → split into sub-task.
>
> **Implicit mode:** apply methodology internally without visible markers when adding markers would clutter the response (routine work where reasoning aids accuracy).
>
> **Deep-dive:** see `/sequential-thinking` skill (`.claude/skills/sequential-thinking/SKILL.md`) for worked examples (API design, debugging, architecture), advanced techniques (spiral refinement, hypothesis testing, convergence), and meta-strategies (uncertainty handling, revision cascades).

<!-- /SYNC:sequential-thinking-protocol -->

<!-- SYNC:evidence-based-reasoning -->

> **Evidence-Based Reasoning** — Speculation is FORBIDDEN. Every claim needs proof.
>
> 1. Cite `file:line`, grep results, or framework docs for EVERY claim
> 2. Declare confidence: >80% act freely, 60-80% verify first, <60% DO NOT recommend
> 3. Cross-service validation required for architectural changes
> 4. "I don't have enough evidence" is valid and expected output
>
> **BLOCKED until:** `- [ ]` Evidence file path (`file:line`) `- [ ]` Grep search performed `- [ ]` 3+ similar patterns found `- [ ]` Confidence level stated
>
> **Forbidden without proof:** "obviously", "I think", "should be", "probably", "this is because"
> **If incomplete →** output: `"Insufficient evidence. Verified: [...]. Not verified: [...]."`

<!-- /SYNC:evidence-based-reasoning -->

<!-- SYNC:design-patterns-quality -->

> **Design Patterns Quality** — Priority checks for every code change:
>
> 1. **DRY via OOP:** Identify classes/modules with the same purpose, naming pattern, or lifecycle. Apply your knowledge of the project's language/framework to determine the idiomatic abstraction (base class, mixin, trait, protocol, decorator). 3+ similar patterns → extract to shared abstraction.
> 2. **Right Responsibility:** Logic in LOWEST layer (Entity > Domain Service > Application Service > Controller). Never business logic in controllers.
> 3. **SOLID:** Single responsibility (one reason to change). Open-closed (extend, don't modify). Liskov (subtypes substitutable). Interface segregation (small interfaces). Dependency inversion (depend on abstractions).
> 4. **After extraction/move/rename:** Grep ENTIRE scope for dangling references. Zero tolerance.
> 5. **YAGNI gate:** NEVER recommend patterns unless 3+ occurrences exist. Don't extract for hypothetical future use.
>
> **Anti-patterns to flag:** God Object, Copy-Paste inheritance, Circular Dependency, Leaky Abstraction.
>
> **Serial Attention for Design Quality** — Scan one quality dimension at a time (serial passes), not all concerns at once. — why: split attention misses violations that single-focus passes catch.
>
> 1. **Identify applicable dimensions** — Based on the code's language, domain, and patterns, determine which quality dimensions apply: DRY, SOLID principles (SRP/OCP/LSP/ISP/DIP), OOP idioms, cohesion/coupling, GRASP, Law of Demeter, CQRS invariants, etc. Your list is NOT fixed — derive from what the code actually does.
> 2. **One focused pass per dimension** — Dedicate single-focus attention to EACH dimension in sequence. Do NOT mix concerns across passes.
> 3. **Threshold: 3+ similar patterns = MANDATORY extraction** — Not optional suggestion. Flag as mandatory structural fix requiring action.
> 4. **2+ violations of same kind = structural finding** — Report as "pattern problem" needing architectural resolution, not a list of individual instances.

<!-- /SYNC:design-patterns-quality -->

<!-- SYNC:double-round-trip-review -->

> **Validated-Finding Fix + Full Re-Review Loop** — Re-review is triggered by a validated finding fix cycle, not by a round number. Review purpose: `review → validate findings → fix validated findings → full re-review` until a complete review pass clears the round's exit bar (see **Severity floor** below). **A clean review ENDS the loop — no further rounds required.**
>
> _aka **Self-Review Convergence Loop**._ The name is historical — there is **NO 2-round cap**; "double-round-trip" only means a validated-finding fix cycle forces at least one fresh re-review. It runs until a clean pass, bounded by the **3-round ceiling** below.
>
> **Round cap — 3 rounds MAX (a ceiling, NEVER a target).** A clean pass ENDS the loop immediately at ANY round — round 1 included; the cap never obliges you to keep spinning. Hitting round 3 with blocking findings still open (severity floor applied) → **STOP and escalate via `AskUserQuestion`** with the still-open findings listed; NEVER emit a silent "good enough" PASS on cap exhaustion, and NEVER let the cap substitute for the clean-review requirement. The 2-repeated-no-progress blocker rule stays an EARLIER exit — escalate at whichever trips first.
>
> **Severity floor — from round 3, LOW stops blocking.** The exit bar tightens by round, so the loop converges on consequence instead of spinning on polish:

> Define one predicate everywhere: `blocking_findings(round, findings)` returns all validated findings in rounds 1–2 and only validated CRITICAL/HIGH/MEDIUM findings in round 3+. A binary gate (test-green, security must-fix, required artifact) is exempt only when its owning invariant explicitly says so.
>
> | Round | Exit bar — loop ENDS when the fresh full review has…                      | Must be fixed to continue      |
> | ----- | ------------------------------------------------------------------------- | ------------------------------ |
> | 1-2   | zero validated findings at ANY severity                                   | CRITICAL · HIGH · MEDIUM · LOW |
> | 3+    | zero validated CRITICAL / HIGH / MEDIUM findings — **LOW-only is a PASS** | CRITICAL · HIGH · MEDIUM only  |
>
> From round 3 onward LOW findings are **NOT required to be fixed**: a round whose validated findings are ALL LOW **ENDS the loop immediately** — do not open another round for them. Severity tiers are `SYNC:severity-rubric` (CRITICAL block-merge · HIGH must-fix · MEDIUM should-fix · LOW nice-to-fix); rounds 1-2 are unchanged, so an easy LOW still gets fixed early when it is cheap.
>
> **Severity-floor rules:**
>
> - **Never silently drop a deferred LOW.** Every unfixed LOW is listed in the final report under `## Deferred LOW Findings (severity floor, round ≥3)` with file, line, and description, so the owner can schedule it. Dropping it from the report is a protocol violation, not a clean pass.
> - **Never re-tier a finding to trigger the exit.** Downgrading a real CRITICAL/HIGH/MEDIUM to LOW so the loop can end is a FALSE PASS. Severity is set by consequence per `SYNC:severity-rubric` before the round bar is applied — never after, and never with the exit in view. — why: a floor that can be reached by relabeling is not a floor.
> - **The floor bounds the loop, not the standard.** It ends _iteration_; it never authorizes shipping a known CRITICAL/HIGH/MEDIUM, and it never lowers the finding-survival bar that admits a finding in the first place.
> - **The floor never applies to a hard gate.** Test-green gates (a suite must actually pass), security must-fix gates, and any gate whose criterion is binary rather than severity-rated are unaffected — a failing test is a failure, not a LOW finding.
>
> **Universal scope (any new output/judgment):** any newly produced output or judgment gets **≥1 self-review**; any **new judgment** gets **≥1 `/why-review --validate-findings` pass**; anything flagged to re-check is re-checked **≥1 time** — before that output is treated as final. This loop is the default convergence contract for ANY work-producing skill, not review skills only.
>
> **Routing invariant (author-facing):** a skill that validates findings MUST route them through `/why-review --validate-findings` (the terminal validator) — NEVER fork an inline finding-validation. Routing through why-review is what makes the finding-survival bar and this loop apply; the `verify-review-validate-coverage` sensor enforces this exact route mechanically.
>
> **Round 1:** Main-session review. Read target files, build understanding, note issues. Output findings + verdict (PASS / FAIL).
>
> **Decision after Round 1:**
>
> - **No issues found (PASS, zero findings)** → review ENDS. Do NOT spawn a fresh sub-agent for confirmation.
> - **`blocking_findings(round, findings)` is non-empty** → run the active review skill's findings-validation gate first; for review skills the default gate is `/why-review --validate-findings <report-path>`. Fix only validated findings, then restart the full review protocol from the beginning with a fresh task breakdown.
>
> **Fresh full re-review after every fix cycle:** Re-run the whole review protocol over the current full target. When sub-agents are part of that protocol, spawn NEW `Agent` calls — never reuse prior agents. Reviewers re-read ALL files from scratch with ZERO memory of prior rounds. See `SYNC:fresh-context-review` for the spawn mechanism and `SYNC:review-protocol-injection` for the canonical Agent prompt template. Each fresh full review must catch:
>
> - Cross-cutting concerns missed in the prior round
> - Interaction bugs between changed files
> - Convention drift (new code vs existing patterns)
> - Missing pieces that should exist but don't
> - Subtle edge cases the prior round rationalized away
> - Regressions introduced by the fixes themselves
>
> **Loop termination:** After each full re-review, repeat the same decision against **that round's exit bar**: bar cleared → END; blocking findings remain → validate findings → fix → restart from the first review phase. Rounds 1-2 clear on zero findings at any severity; **from round 3 the bar is zero CRITICAL/HIGH/MEDIUM, so a LOW-only round ENDS the loop** (deferred LOWs go in the report). Capped at **3 rounds**. Escalate via `AskUserQuestion` at whichever comes first: the same validated finding repeats for 2 full invocations with no progress · a fix requires product/owner input · round 3 completes with CRITICAL/HIGH/MEDIUM still open. NEVER loop past 3 rounds, and NEVER convert cap exhaustion into a PASS.
>
> **Rules:**
>
> - A clean Round 1 ENDS the review — no mandatory Round 2
> - From round 3 on, a round whose validated findings are ALL LOW ENDS the loop — never open round N+1 to fix LOW alone; list those LOWs as deferred instead
> - NEVER re-tier a CRITICAL/HIGH/MEDIUM down to LOW to reach the round-3 exit — severity is assigned by consequence before the bar is applied
> - NEVER fix unvalidated findings; validate first using the caller's validation gate
> - Every surviving finding must additionally clear the **finding-survival bar** defined in why-review's Findings Validation Routine (a deliberately higher bar than the generic act-gate — "keep this finding?" is a stricter question than "act on this evidence?"); a finding below the bar is demoted or dropped, not kept
> - NEVER skip the full re-review after a fix cycle (every fix invalidates the prior verdict)
> - NEVER reuse a sub-agent across rounds — every iteration that uses sub-agents spawns NEW Agent calls
> - Main agent READS sub-agent reports but MUST NOT filter, reinterpret, or override findings
> - The 3-round cap NEVER replaces the clean-review requirement — it bounds runaway looping, it does not authorize shipping an un-clean review; a clean pass ends the loop early at any round, and cap exhaustion escalates rather than passes
> - Enforce the round cap of 3 alongside the 2 repeated-no-progress blocker rule; both are escalation triggers, neither is a completion criterion
> - Track recursive invocation count and repeated blockers in conversation context (session-scoped)
> - Final verdict must incorporate ALL rounds executed
>
> **Report must include `## Round N Findings (Fresh Sub-Agent)` for every round N≥2 that was executed, plus `## Deferred LOW Findings (severity floor, round ≥3)` whenever the loop ended on the round-3+ bar with LOWs still open.**

<!-- /SYNC:double-round-trip-review -->

<!-- SYNC:source-test-drift-check -->

> **Source/test drift check.** For coding, fix, debug, investigation, test, or review work: when source behavior changes, inspect affected unit/integration/E2E tests and decide from evidence whether tests should change to match intended behavior or the source change is an unintended bug to fix. Do not write tests for migration code; schema/data migrations are one-time execution paths, not core application logic.

<!-- /SYNC:source-test-drift-check -->

<!-- SYNC:understand-code-first -->

> **Understand Code First** — HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
>
> 1. Search 3+ similar patterns (`grep`/`glob`) — cite `file:line` evidence
> 2. Read existing files in target area — understand structure, base classes, conventions
> 3. Run `python .claude/scripts/code_graph trace <file> --direction both --json` when `.code-graph/graph.db` exists
> 4. Map dependencies via `connections` or `callers_of` — know what depends on your target
> 5. Write investigation to `.ai/workspace/analysis/` for non-trivial tasks (3+ files)
> 6. Re-read analysis file before implementing — never work from memory alone. — why: long context drifts from the file; the file is ground truth
> 7. NEVER invent new patterns when existing ones work — match exactly or document deviation. — why: divergent patterns fragment the codebase and slow every future reader
>
> **BLOCKED until:** `- [ ]` Read target files `- [ ]` Grep 3+ patterns `- [ ]` Graph trace (if graph.db exists) `- [ ]` Assumptions verified with evidence

<!-- /SYNC:understand-code-first -->

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

<!-- SYNC:systematic-review-batching -->

> **Systematic Review Batching (map-reduce)** — When a changeset is large, do NOT review files one-by-one. Partition into size-capped batches, fire one specialized sub-agent per batch in parallel, then reduce. This bounds EVERY context — each batch agent AND the orchestrator — so coverage stays complete as file count grows.
>
> **Trigger ladder (one ordered escalation — not competing thresholds):**
>
> 1. **< 10 changed files** → sequential per-file review (default; no batching).
> 2. **≥ 10 changed files** → switch to systematic parallel mode. Announce: `"Detected {N} changed files. Switching to systematic parallel review protocol."` Then: categorize → size-capped batches → flat consolidation.
> 3. **categories > 6 OR files > 40** → additionally insert the hierarchical synthesis tier (below). Everything from rung 2 still applies.
>
> **Step 1 — Categorize.** Group changed files into logical categories derived from the project's actual structure (not forced). Category is the _concern axis_; orient with these examples, derive what fits the repository:
>
> | Category Type       | Example Groupings                                                     |
> | ------------------- | --------------------------------------------------------------------- |
> | Agent/Tooling       | AI scripts, hooks, skill definitions, workflow configs, linting rules |
> | Root config/docs    | Root README, project config, CI/CD pipeline configs                   |
> | Reference docs      | Architecture docs, patterns references, setup guides                  |
> | Feature/domain docs | Business feature documentation, spec files, ADRs                      |
> | Backend logic       | Service/handler/controller source (infer from project structure)      |
> | Frontend logic      | UI component/state/API source (infer from project structure)          |
> | Data/Schema         | Migrations, schema files, seed data                                   |
> | Tests               | Unit, integration, E2E test files                                     |
> | Infrastructure      | Docker, k8s, CI/CD, cloud manifests                                   |
>
> **Step 2 — Size-capped batches.** One sub-agent per batch of **≤8 files OR ≤2000 diff-lines**, whichever hits first. Category stays the concern axis, but any category exceeding a cap splits into multiple size-capped batches (30 backend files → 4 batches). Size caps — not category caps — make "many files" safe: a category cap alone lets one giant category blow a single agent's context.
>
> **Step 2a — Sub-agent type per batch** (match the batch's dominant concern):
>
> - Code logic (any stack) → `code-reviewer`
> - Security-sensitive changes → `security-auditor`
> - Performance-critical paths → `performance-optimizer`
> - Docs, plans, specs, configs, infra → `general-purpose`
>
> Each batch sub-agent receives: its full file list; `SYNC:category-review-thinking` as its primary thinking model — derive each category's concerns from first principles, NOT a fixed checklist (if the consuming skill does not carry that block, apply category-first thinking directly); project reference docs relevant to its concern (discover via `*patterns*`, `*conventions*`, `*style-guide*`); cross-reference verification instructions (counts, tables, links). All batch agents run in parallel and write findings to `plans/reports/` (per `SYNC:task-tracking-external-report`); reducers read from disk, never from memory.
>
> **Step 3 — Reduce.**
>
> - **Flat reduction (rung 2, ≤6 categories AND ≤40 files):** the orchestrator collects each batch report, cross-references counts/tables/contracts ACROSS batches, detects gaps visible only across categories (feature in code but missing from docs; new API endpoint with no client call), and consolidates into one categorized holistic report.
> - **Hierarchical reduction (rung 3, > 6 categories OR > 40 files):** insert a mid-tier — each concern gets ONE synthesizer agent that reads only its own batch reports and emits a single concern-synthesis. The orchestrator reads the **concern-syntheses (~5)**, never the raw batch reports — keeping the reducer's context O(#concerns), not O(#files).
>     - **Cross-concern interaction pass (mandatory at rung 3 — closes the synthesis-tier blind spot):** concern-siloed synthesis can drop an interaction spanning two concerns AND two batches (tainted source in data-layer/batch 7 → sink in api/batch 3). So: (a) each concern-synthesizer MUST emit an explicit **"cross-concern interaction candidates"** list — entities/symbols/contracts it touched that plausibly bind to another concern (shared DTOs, event names, table/collection names, exported symbols); (b) the orchestrator MUST run the Step-3 cross-reference/gap step **over those candidate lists across all concern-syntheses**, not only within a batch, before concluding. Without this pass the tier trades completeness for context-bounding on exactly the large diffs it targets.
>
> **Step 4 — Holistic assessment.** With all findings combined, judge: overall coherence as a unified intent; cross-category sync (docs match code? contracts match callers?); risk areas where categories interact; missing doc/spec updates for changed artifacts.
>
> **No silent truncation.** If any cap forces sampling or a batch is dropped for budget, ANNOUNCE the dropped/sampled scope explicitly — bounded coverage must never read as complete coverage.

<!-- /SYNC:systematic-review-batching -->

<!-- SYNC:severity-rubric -->

> **Severity Rubric** — Classify every finding by consequence, not by how easy it is to fix. One scale across all reviews so a "High" means the same thing everywhere.
>
> | Severity | Action      | Definition                                                                |
> | -------- | ----------- | ------------------------------------------------------------------------- |
> | CRITICAL | Block merge | Silent runtime failure, data corruption, validation bypass, security hole |
> | HIGH     | Must fix    | Incorrect behavior, invariant gap, architectural violation                |
> | MEDIUM   | Should fix  | Design debt, maintainability, likely future bug                           |
> | LOW      | Nice to fix | Convention, documentation, minor clarity                                  |
>
> **Score-based skills** map their numeric scale onto these tiers — do not invent a parallel vocabulary:
>
> - **0-2 criterion scoring** (e.g. production-readiness-review): `0` = CRITICAL/HIGH (criterion unmet, blocks production readiness), `1` = MEDIUM (partial, should fix), `2` = pass (no finding).
> - **Two-axis scoring** (e.g. performance-review, impact × likelihood): map the resulting cell to the nearest tier — high-impact + high-likelihood → CRITICAL/HIGH; low-impact OR low-likelihood → MEDIUM/LOW.
>
> A finding's tier drives the gate: CRITICAL/HIGH must be resolved or explicitly accepted by the owner before PASS; MEDIUM/LOW may ship with a tracked follow-up.

<!-- /SYNC:severity-rubric -->

<!-- SYNC:category-review-thinking -->

> **Category Review Thinking** — A thinking framework for reviewing any category of changed files. NOT a fixed checklist — derive concerns from domain knowledge; the examples are starting points only. Your knowledge of the category exceeds any list here — trust it.
>
> **Step 1 — Understand the category's role.** What is this category responsible for in the overall system? What invariants must it uphold? What are its consumer contracts (who depends on it, what do they expect)?
>
> **Step 2 — Read project conventions for this category.** Search for reference docs, style guides, ADRs, or READMEs specific to this area. Grep 3+ existing similar files — extract naming conventions, structural patterns, shared base classes. If no docs exist, derive conventions empirically from existing code.
>
> **Step 3 — Derive concerns from first principles.** Apply all that are relevant; expand beyond this list based on the actual category:
>
> - **Correctness:** Does the logic match the intent? Trace happy path AND error path.
> - **Boundary contracts:** Are interfaces/APIs/events/protocols honored? No implicit coupling introduced?
> - **Project conventions:** Does new code follow the patterns found in Step 2? Evidence-confirmed, not assumed.
> - **Security:** Auth enforced at every entry point? Input validated at boundaries? No secrets in the diff?
> - **Performance:** Unbounded operations? N+1 patterns? Blocking calls in async context? Unindexed queries?
> - **Maintainability:** DRY? Single responsibility? Complexity within reason? Names reveal intent?
> - **Test coverage:** Are the changed paths covered by tests? Are existing tests still valid after the change?
> - **Documentation:** Do related docs, specs, or READMEs reflect the changes?
>
> **Step 4 — Create sub-tasks and execute.** For each identified concern: create a `TaskCreate` sub-task, work through it with `file:line` evidence, mark done. No findings without proof.
>
> **Illustrative concern examples by category type** (not exhaustive — trust your knowledge beyond this):
>
> - _Server-side logic:_ handler/service structure conventions, validation layer placement, side-effect isolation, cross-service boundary enforcement, data-access layer separation, error propagation strategy
> - _Client-side logic:_ component lifecycle management, resource cleanup (subscriptions, listeners, timers), state management patterns, API integration layer separation, reactive stream composition
> - _Data/Schema:_ migration reversibility (rollback script), lock impact on table volume, backfill idempotency, index coverage for query patterns, deployment ordering
> - _Configuration:_ present in ALL environments? No secrets in diff? App fails fast if config missing (not silently null)? Documented in setup guide?
> - _Infrastructure:_ dev/prod parity? No hardcoded dev values (localhost, debug flags)? Pinned image/dependency versions? CI/CD secret requirements documented?
> - _Styles/Assets:_ follows project naming conventions? Uses design variables/tokens (no hardcoded magic values)? Correct scope (no global side effects from component styles)?
> - _Documentation:_ accurate? Links valid? Examples still match current code/behavior? Covers new scenarios?
> - _Tests:_ assertions verify specific outcomes (not just "no exception")? Idempotent (repeatable N times)? Covers edge cases, not just happy path?
> - _Security artifacts:_ all code paths reach the gate? Negative tests exist (unauthorized denied)? Both enforcement AND display control updated?
> - _Build/Tooling:_ rule changes apply consistently? No exceptions that silently swallow violations? Impact on CI runtime documented?

<!-- /SYNC:category-review-thinking -->

<!-- SYNC:goal-contract-satisfaction-loop -->

> **Goal Contract Satisfaction Loop** — Persist the user goal in an external file, execute against it, and loop review/fix until every saved required criterion passes or a blocker escalates. Bounded closed loop — NEVER open-ended autonomous exploration.
>
> 1. **Resolve the active goal** (in order): active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create a new Goal Contract from the current user request (template: `.claude/templates/goal-contract-template.md`).
> 2. **Required sections:** Original Request, Purpose, Success Criteria (checkboxes; mark required vs optional), Constraints, Evidence Required, Iteration Log, Goal Satisfaction matrix.
> 3. **Before work:** read the active goal and map planned work to saved success criteria — execution serves the saved criteria, never chat memory alone.
> 4. **After execution/verification:** append an Iteration Log entry — result, evidence references (`file:line`, command output, report path), remaining gaps.
> 5. **Review gate:** emit a Goal Satisfaction matrix — `| Success Criterion | Evidence | Status |` with PASS/FAIL/BLOCKED. Overall PASS requires every required criterion PASS.
> 6. **Loop rule (retry):** required criterion FAIL → validate the gap is real → fix → re-review only the affected criteria. Stop cleanly when all required criteria PASS.
> 7. **Escalation rule (stop):** two consecutive iterations with no criterion progressing, or a blocker needing user input → mark the criterion BLOCKED with a user-facing reason and escalate. NEVER loop indefinitely.
> 8. **Skip rule:** tiny conversational tasks may skip the goal file ONLY with a recorded one-line reason. User-accepted gate skips are recorded in the goal file with reason and scope.
> 9. **Security:** NEVER store secrets, tokens, credentials, or private customer data in goal files — store evidence references and redact sensitive values.
>
> **Blocked until:** active goal resolved (or skip reason recorded) · saved success criteria read before edits · iteration evidence appended after execution · Goal Satisfaction matrix emitted before any PASS verdict.

<!-- /SYNC:goal-contract-satisfaction-loop -->

<!-- SYNC:trade-off-interrogation-gate -->

> **Trade-Off Interrogation Gate** — ALWAYS ask these THREE questions before ANY verdict, score, finding, or recommendation — about the thing under review AND about every recommendation YOU make. — why: naming a benefit without its price is an endorsement, not a review; the costliest trade-offs are the ones nobody wrote down.
>
> 1. **Is there any trade-off?** Name what it SACRIFICES. "None" / "pure win" is an unfinished analysis, NOT an answer — to claim none, state which dimensions you checked and why each is unaffected: future change cost · complexity · performance/latency · memory/cost · coupling · reversibility · migration burden · operational load · blast radius · security posture · testability · team skill/ramp · delivery time · UX.
> 2. **Is it worth it?** Weigh gain against sacrifice EXPLICITLY — what is gained (with a metric) · what it costs · WHO pays · WHEN it comes due — then emit **WORTH IT / NOT WORTH IT / UNCLEAR**. "Better" with no metric and no cost FAILS this question. NOT WORTH IT → withdraw or replace the recommendation, never keep it as-is.
> 3. **Is the trade-off material enough to CONFIRM WITH THE USER?** A material trade-off is the user's call, never yours. **MATERIAL** when ANY holds: irreversible / one-way door (data migration, public contract, storage format, vendor lock-in) · cost shifted onto someone else (another team, ops/on-call, future maintainer, end user) · one quality attribute traded for another (correctness↔speed, security↔convenience, latency↔cost, simplicity↔flexibility) · a boundary crossed (client↔server tier, service contract, event contract, shared library) · a high-consequence path (auth, money, data integrity, breaking change, High/Medium residual risk) · the worth-it verdict is UNCLEAR.
>
> **MATERIAL → STOP and confirm via `AskUserQuestion` BEFORE the verdict stands** — state the trade-off, both options, what each sacrifices, and your recommendation. **NOT material →** record it inline with a one-line justification and proceed.
>
> **Non-asking execution contexts — ESCALATE BY HANDOFF, never by silence.** `AskUserQuestion` reaches only the main interactive agent: a sub-agent cannot ask the user, and a terminal/verdict-only mode asks nothing by design. When you are running in such a context, the obligation is **redirected, never waived** — do ALL of: (a) complete questions 1 and 2 normally; (b) decide materiality and record it in the Trade-Off Assessment row with `confirmed? = NO — cannot ask from this context`; (c) **name the unconfirmed MATERIAL trade-off explicitly in your returned summary/verdict so the CALLER (or parent orchestrator) escalates it via `AskUserQuestion` on your behalf** — a material trade-off mentioned only inside a report file on disk is NOT a handoff; (d) do not emit an unqualified PASS — mark the verdict as carrying an unconfirmed material trade-off, so the caller's gate stays closed until the user answers. The caller inherits the escalation duty the moment it reads your return.
>
> This carve-out is about **reachability, not convenience**: it applies ONLY where the tool genuinely cannot reach the user (spawned sub-agent, terminal validate/verdict-only mode, non-interactive/headless run). It is NEVER a licence to skip the question, to self-approve a one-way door, or to downgrade materiality because asking is inconvenient — if you CAN ask, you MUST ask.
>
> **Emit a Trade-Off Assessment row** per reviewed decision and per recommendation: `| decision | sacrifices | gain (metric) | who pays, when | WORTH IT/NOT/UNCLEAR | material? | confirmed? |`.
>
> **BLOCKED until:** trade-off named (or dimensions-checked justification given) · worth-it verdict emitted · materiality decided · every MATERIAL trade-off either confirmed with the user OR — in a non-asking context — handed off in the returned verdict for the caller to confirm. A MATERIAL trade-off that is neither confirmed nor handed off can NEVER be PASS, and NEVER gets buried as a Low-severity note.
>
> **NEVER** answer "no trade-off" without checking · decide a material trade-off silently on the user's behalf · let convergence/delivery pressure authorize walking through a one-way door · bundle several material trade-offs into one vague "proceed?".

<!-- /SYNC:trade-off-interrogation-gate -->

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

<!-- SYNC:evidence-based-reasoning:reminder -->

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim. Confidence >80% to act, <60% = do NOT recommend.

<!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:design-patterns-quality:reminder -->

**IMPORTANT MUST ATTENTION** check DRY via OOP, right responsibility layer, SOLID. Grep for dangling refs after moves.

<!-- /SYNC:design-patterns-quality:reminder -->

<!-- SYNC:graph-assisted-investigation:reminder -->

**IMPORTANT MUST ATTENTION** run at least ONE graph command on key files when graph.db exists. Pattern: grep → trace → verify.

<!-- /SYNC:graph-assisted-investigation:reminder -->

<!-- SYNC:source-test-drift-check:reminder -->

**IMPORTANT MUST ATTENTION** when source behavior changes, inspect affected tests; decide from evidence whether tests update to match intent or the source change is an unintended bug.

<!-- /SYNC:source-test-drift-check:reminder -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code BEFORE any modification. Run graph trace when graph.db exists.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:subagent-return-contract:reminder -->

**IMPORTANT MUST ATTENTION** every spawned sub-agent returns report path + status + severity counts; appends findings per-file (never batched); main agent integrates verbatim, never filters.

<!-- /SYNC:subagent-return-contract:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** apply sequential-thinking — multi-step Thought N/M, REVISION/BRANCH/HYPOTHESIS markers, confidence % closer; see `/sequential-thinking` skill.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:task-tracking-external-report:reminder -->

- **MANDATORY** Bootstrap task tracking before target work; transition one task at a time.
- **MANDATORY** Persist plan/review findings to `plans/reports/` incrementally and synthesize from disk.

<!-- /SYNC:task-tracking-external-report:reminder -->

<!-- SYNC:project-reference-docs-guide:reminder -->

- **MANDATORY** Before investigating, planning, or coding, read `docs/project-config.json` (the project map: modules/paths, run-commands, conventions, architecture/workflow rules) + the required project-reference docs, and cite `Reference docs read: ...`.
- **MANDATORY** Always include `lessons.md`; project config + conventions override generic framework defaults.
- **MANDATORY** If project config, root instruction files, or any required reference doc is missing or stale, auto-run `/project-init` or the narrow lower-level route before ordinary project-specific work.

<!-- /SYNC:project-reference-docs-guide:reminder -->

<!-- SYNC:nested-task-creation:reminder -->

- **MANDATORY** Parent workflow rows do not replace child phase tracking; expand phases and link the parent when nested.
- **MANDATORY** Orchestrators pre-expand child skill phases before invocation; use `[N.M] $skill-name — phase` prefixes and one-`in_progress` discipline.

<!-- /SYNC:nested-task-creation:reminder -->

<!-- SYNC:systematic-review-batching:reminder -->

- **MANDATORY** Large changeset → batch by size cap (≤8 files OR ≤2000 diff-lines), one parallel sub-agent per batch; never review many files one-by-one.
- **MANDATORY** > 6 categories OR > 40 files → add the hierarchical synthesis tier; each concern-synthesizer emits cross-concern interaction candidates and the orchestrator runs the cross-concern pass before concluding.

<!-- /SYNC:systematic-review-batching:reminder -->

<!-- SYNC:severity-rubric:reminder -->

- **MANDATORY** Classify findings Critical/High/Medium/Low by consequence; Critical/High block PASS until fixed or owner-accepted.
- **MANDATORY** Score-based skills (sre 0-2, perf two-axis) map onto the same four tiers — no parallel severity vocabulary.

<!-- /SYNC:severity-rubric:reminder -->

<!-- SYNC:category-review-thinking:reminder -->

- **MANDATORY** Derive review categories from file language + directory semantics + change nature; create a sub-task per category.
- **MANDATORY** Derive each category's concerns from first principles with `file:line` evidence — never a fixed checklist.

<!-- /SYNC:category-review-thinking:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:double-round-trip-review:reminder -->

- **MANDATORY IMPORTANT MUST ATTENTION** execute the review loop (aka **Self-Review Convergence Loop**): review → validate findings → fix validated findings → full re-review. A complete review pass with zero findings ENDS the review. Any newly produced output/judgment gets ≥1 self-review; any new judgment gets ≥1 `/why-review --validate-findings` pass before it is treated as final.
- **MANDATORY** apply the **severity floor**: rounds 1-2 exit on zero findings at any severity; **from round 3 the bar is zero CRITICAL/HIGH/MEDIUM — LOW findings are no longer required to be fixed, so a LOW-only round ENDS the loop.** List every deferred LOW in the report; NEVER re-tier a real CRITICAL/HIGH/MEDIUM down to LOW to reach the exit, and NEVER apply the floor to a binary gate (test-green, security must-fix).
- **MANDATORY** enforce the **round cap of 3 — a ceiling, NEVER a target**: a clean pass ends the loop immediately at any round (round 1 included), and round 3 completing with CRITICAL/HIGH/MEDIUM still open → **STOP & escalate via `AskUserQuestion`**, never a silent PASS. The 2-repeated-no-progress blocker rule is an earlier exit — escalate at whichever trips first. NEVER loop open-ended.

<!-- /SYNC:double-round-trip-review:reminder -->

<!-- SYNC:goal-contract-satisfaction-loop:reminder -->

- **MANDATORY** Resolve the active Goal Contract BEFORE work (active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create from current request) and read saved success criteria before editing.
- **MANDATORY** Append iteration evidence after execution; emit a Goal Satisfaction matrix (PASS/FAIL/BLOCKED) before reporting PASS; loop on validated FAIL; escalate repeated no-progress or blockers. NEVER store secrets in goal files.

<!-- /SYNC:goal-contract-satisfaction-loop:reminder -->

<!-- SYNC:trade-off-interrogation-gate:reminder -->

- **MANDATORY MUST ATTENTION ALWAYS ASK THE 3 TRADE-OFF QUESTIONS** — on the thing under review AND on every recommendation you make: (1) **is there any trade-off?** name what it SACRIFICES (change cost · complexity · perf · coupling · reversibility · migration · ops load · blast radius · security · testability · delivery time · UX) — "none"/"pure win" is an unfinished analysis, so state the dimensions checked; (2) **is it worth it?** gain (with a metric) vs cost, WHO pays, WHEN → emit **WORTH IT / NOT WORTH IT / UNCLEAR**; NOT WORTH IT → withdraw or replace it; (3) **is it material enough to confirm with the user?** irreversible/one-way door · cost shifted onto another team/ops/maintainer/user · one quality attribute traded for another · a tier/service/event/library boundary crossed · auth/money/data-integrity/breaking-change/High-or-Medium-risk path · verdict UNCLEAR → **STOP and confirm via `AskUserQuestion` BEFORE the verdict**.
- **MANDATORY** A MATERIAL trade-off with no user confirmation can NEVER be PASS; NEVER bury one as a Low-severity note, NEVER decide it silently, and NEVER let delivery or convergence pressure authorize a one-way door. — why: an un-walked-back one-way door is the user's call to make, not the reviewer's.
- **MANDATORY — non-asking contexts escalate BY HANDOFF, never by silence.** `AskUserQuestion` reaches only the main interactive agent: a sub-agent cannot ask the user, and a terminal/verdict-only mode asks nothing by design. There the duty is REDIRECTED, not waived — still name the trade-off, still decide materiality, record `confirmed? = NO — cannot ask from this context`, **state the unconfirmed MATERIAL trade-off in your RETURNED verdict/summary so the CALLER escalates it** (a note only in an on-disk report is not a handoff), and never emit an unqualified PASS. Applies ONLY where the user is genuinely unreachable (spawned sub-agent, terminal validate mode, headless run) — if you CAN ask, you MUST ask.

<!-- /SYNC:trade-off-interrogation-gate:reminder -->

<!-- SYNC:parallel-subagent-dispatch -->

> **Parallel Sub-Agent Dispatch** — Plan parallelism the moment a task breakdown exists, BEFORE executing it — running provably independent tasks sequentially wastes wall-clock. Applies to every multi-step job: workflow steps, planning, batch updates, investigation, research, scans, reviews, doc sync. **Plan execution is metadata-gated, NEVER default-parallel** — fan-out follows ONLY what the plan declares (`PAR`/`SEQ` tags + per-phase write set); an untagged plan runs sequentially — why: a derived write set cannot see cascade or generated writes.
>
> 1. **Tag every task `PAR` or `SEQ`.** `PAR` = inputs exclude every pending task's output AND write set disjoint from every other `PAR`. Else `SEQ` — MUST ATTENTION name the dependency forcing it.
> 2. **Group `PAR` into waves.** No edge between members. Two writers of one file NEVER share a wave. Read-only work (search, investigation, review, research) parallelizes freely.
> 3. **Declare before dispatch:** `Parallel plan: wave 1 = [...] · wave 2 = [...] · SEQ = [...] (reason)`.
> 4. **Spawn each wave in ONE message** — every `Agent` call in one response, NEVER dripped per turn. Route each task to its specialist (`.claude/skills/shared/sub-agent-selection-guide.md`); NEVER `code-reviewer` as catch-all.
> 5. **Brief each sub-agent self-contained:** goal · scope + owned files · reference docs · return contract (summary + `Full report:` path, per SYNC:subagent-return-contract) · incremental persistence to `plans/reports/` (per SYNC:incremental-persistence).
> 6. **Barrier per wave.** Advance ONLY after EVERY member returns (a skipped conditional counts as returned). Merge, mark each task completed/skipped, THEN dispatch the next wave. Mutating steps wait for the barrier.
> 7. **One level deep.** A dispatched sub-agent executes its own brief; further fan-out stays the orchestrator's job unless that agent's `.claude/agents/*.md` definition authorizes it.
>
> **NEVER parallelize:** tasks sharing a write target · a task consuming a pending task's output · trivial single-file work (dispatch overhead > gain) · an order a skill or workflow explicitly fixes · gates awaiting user approval.
>
> **Blocked until:** MUST ATTENTION every task tagged PAR/SEQ with a named reason per SEQ · waves declared + write-set disjointness checked · each wave spawned in ONE message · barrier honored before the next wave.

<!-- /SYNC:parallel-subagent-dispatch -->

<!-- SYNC:parallel-subagent-dispatch:reminder -->

- **MANDATORY** After planning tasks, tag each PAR/SEQ and spawn every PAR wave as parallel sub-agents in ONE message — default parallel for workflows, batch updates, investigation, research, reviews; plan execution fans out ONLY on what the plan declares.
- **MANDATORY** Disjoint write sets per wave · all-return barrier before the next wave · specialist routing · sub-agents NEVER fan out further unless their own agent definition authorizes it.

<!-- /SYNC:parallel-subagent-dispatch:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

<!-- SYNC:ui-ux-design-principles:reminder -->

- **MUST ATTENTION** apply the 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`) to any user-facing surface: one focal point, proximity grouping, empty/loading/error designed FIRST (§1) · ≤2 families, 16px web / 17px mobile body, never <14px, 45–75ch, fixed 6-step scale (§2) · 4.5:1 text / 3:1 edges measured, one accent, colour never alone, dark mode ≠ inversion (§3) · one 4/8px unit, `gap` over margins, tighter-inside-looser-between, content-driven breakpoints (§4) · <100ms response, all 5 states, undo over confirm, 150–250ms ease-out honouring reduced-motion, visible focus ring (§5) · where-am-I/what's-here/where-next, ≤5 top-level destinations, user's words, URL or back path (§6) · fewer fields, visible labels, validate on blur, matched keyboard, NEVER lose input (§7) · ≥44×44pt targets 8px apart, bottom-third primaries, gestures never the only route, safe areas (§8) · structure before data, optimistic update with visible rollback, reserved space, slow-connection states (§9). Project design-system docs OUTRANK these clauses — a genuine conflict goes to the user, NEVER resolved silently. Cite every finding as `UI-<clause>` + `file:line`. Skip ONLY for changes with no user-facing surface, stated explicitly.

<!-- /SYNC:ui-ux-design-principles:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Ensure frontend/UI changes survive real content, responsive layouts, layering, and styling conventions before handoff.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries — MUST ATTENTION honor each canonical body above):**

- **Graph-Assisted Investigation:** Run graph command on key files first.
- **Nested Task Creation:** Expand child phases; link parent when nested.
- **Project Reference Docs Guide:** Read project docs before reviewing.
- **Task Tracking External Report:** Track tasks; persist findings incrementally.
- **Subagent Return Contract:** Sub-agent returns summary plus report path.
- **Critical Thinking Mindset:** Traced proof per claim; never guess.
- **Sequential Thinking Protocol:** Multi-step reasoning; state confidence closer.
- **Evidence-Based Reasoning:** Cite `file:line`; >80% to act.
- **Design Patterns Quality:** DRY, layered responsibility, SOLID; grep dangling.
- **Double Round-Trip Review:** Validate, fix, full re-review until clean.
- **Source-Test Drift Check:** Source changes; inspect affected tests.
- **Understand Code First:** Read code, grep 3+, before changing.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Systematic Review Batching:** Large changeset; parallel size-capped batches.
- **Severity Rubric:** Classify by consequence; NEVER pass Critical/High.
- **Category Review Thinking:** Derive concerns first-principles, never fixed checklist.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**MUST ATTENTION** break work into small tasks using `TaskCreate` BEFORE starting
**MUST ATTENTION** resolve and read project UI/styling docs BEFORE reviewing — rules come from docs, not general knowledge
**MUST ATTENTION** SKIP this skill when no files match the project frontend path/extension patterns
**MUST ATTENTION** every violation requires `file:line` proof — NEVER speculate
**MUST ATTENTION** grep 3+ counterexamples before flagging any pattern violation
**MUST ATTENTION** `z-index` with `!important` and chained BEM modifiers are HARD-GATE BLOCKED
**MUST ATTENTION** NEVER mix incompatible project token systems in one file — recommend whichever system the file already imports/uses
**MUST ATTENTION** after validated UI fixes, rerun the full UI review; when that protocol uses a fresh reviewer, use the UI/UX-specialized sub-agent from the local sub-agent selection guide
**MUST ATTENTION** run at least ONE graph command on key files when graph.db exists
**MUST ATTENTION** NEVER fix code — review and report only
**MUST ATTENTION** apply `Think:` reasoning prompt before checking each category — derive violations, don't recite checklists
**MUST ATTENTION** run the Phase 3B UI/UX Design Principles pass — all 40 clauses (`UI-1.1`-`UI-9.4`) as NINE focused passes, one dimension at a time; every finding cites `UI-<clause>` + `file:line` + BLOCKED/WARN severity, and project design-system docs OUTRANK the clauses (genuine conflict → `AskUserQuestion`, NEVER resolved silently)
**MUST ATTENTION** use `AskUserQuestion` to present next steps after completing review

**Anti-Rationalization:**

| Evasion                                   | Rebuttal                                                                                |
| ----------------------------------------- | --------------------------------------------------------------------------------------- |
| "Too simple for a UI review"              | Simple templates still overflow on a 200-char value. Apply all 6 categories.            |
| "Already read the docs"                   | Show the extracted rule (mixin name, token name) — no recall = no read.                 |
| "Just flag obvious z-index literals"      | Gray areas matter most. Trace the surface's semantic layer before recommending a token. |
| "Fixed width is fine, it looks right"     | Looks right at 1440px ≠ usable at 320px. Apply the flex/min-max decision rule.          |
| "web-design-guidelines already covers UI" | That is a11y/UX, not the project styling gate. Different scope — do both.               |

---

> **Closing reminder — Easy to Change is the success metric.** Every finding,
> token, mixin, and layout must answer one question: _does this make the next
> change cheaper or more expensive?_ If it doesn't reduce future change cost,
> reject it. Magic values, duplicated styling knowledge, fixed sizing that
> fights the viewport, cross-system token mixing, and z-index escalation wars
> are the real enemies — call them out by name.
