---
model_tier: high
name: design-review
description: "When the user says \"review the design\", \"check the UI\", or wants a comprehensive UI/UX review. 7 phases: interaction, responsiveness, accessibility. Inventory via existing-ui-audit."
domain: quality
enforced_by:
  - "instruction-only: the Phase 4 sweep claims WCAG 2.1 AA and its criteria table is a deliberate SUBSET — depth is delegated to accessibility-auditor, which claims 2.2 AA and carries the resolver. No resolver checks this table against 2.1, so the claim is model-carried and the gap is recorded rather than implied."
workspaces:
  - engineering
packs:
  - engineering-base
---

# design-review

## When to use

> **Render-verification gate.** A UI verdict is gated on the
> [design-artifact verification checklist](../../../docs/contracts/design-artifact-verification.md#verification-checklist):
> where render capability exists, do not pass a design task without render
> evidence (checklist steps 1–5); where it is absent, scope the verdict to what
> was statically checked and say so — never "looks good" without evidence.

Use this skill when:
- Reviewing pull requests with UI changes
- Auditing frontend components for design quality
- Verifying responsive design across viewports
- Checking accessibility compliance (WCAG 2.1 AA)
- Testing interaction flows and user experience
- Conducting visual QA on new features

Do NOT use when:
- Creating new designs (use `fe-design` skill instead)
- Reviewing backend/API code only
- Quick syntax checks (use linters)

## Prerequisites

One of the following browser automation tools:
- **Playwright MCP** (recommended) — browser automation, screenshots, viewport testing
- **Chrome DevTools** — screenshot capture, performance analysis

A **live preview URL** is required for testing.

## Procedure: Design review

1. **Inspect the PR and preview** — Read the PR description, diff, and identify changed components/pages; read the probe artifact and run the appearance floor over the preview URL (Phase 0).
2. **Walk the interactions** — Run Phase 1; cover hover/focus/active/disabled, keyboard, loading, and form error states.
3. **Cover responsiveness, polish, a11y, robustness** — Run Phases 2–5 in order; record findings per phase.
4. **Audit code-health and content** — Run Phases 6–7; check tokens, dead styles, copy, console warnings.
5. **Verify and report** — Consolidate findings in the report structure; classify each as Blocker / High / Medium / Nit before posting.

### Phase 0: Preparation

- Read PR description and git diff.
- Identify changed components and affected pages.
- Navigate to preview URL.
- **Read the probe artifact** `agents/runtime/state/ui-conformance.json`
  (`ui_conformance_probe --target <file> --reference <file>`) — its per-dimension counters are the
  behavioral evidence Phases 1–2 report against. Absent is absent, never clean; a dimension the host
  could not exercise carries a not-applicable row with its reason rather than a zero.
- **Run the appearance floor** (§ Appearance verification) — mandatory on every review.

### Phase 1: Interaction

- Test user flows end-to-end.
- **Six interaction states — every interactive element asserts each one** (this
  is the single canonical states checklist; no other review phase repeats it):
  1. **default** — the resting state is a deliberate style, not the browser default.
  2. **hover** — pointer feedback present (and not the *only* affordance — see focus).
  3. **active** — pressed/engaged state visibly distinct from hover.
  4. **disabled** — visually unmistakable as non-interactive (a contrast dip alone
     that a user cannot read as "disabled" is a WCAG 1.4.1 failure — see `accessibility-auditor`).
  5. **focus** — a visible `:focus-visible` indicator (Q6 floor, `lint_design_quality`).
  6. **loading** — an explicit pending state (skeleton/spinner/disabled-submit), never a dead frozen control.
- **Transition timing** between these states follows the motion bands in
  [`fe-design`](../fe-design/SKILL.md) § Motion (micro-feedback ~100–200 ms;
  structural open/close ~200–500 ms) — the timing source of truth; do not restate
  a competing band set here. Every animated transition also carries a
  `prefers-reduced-motion` alternative (M5 / Q4).
- **Reduced motion is a presentation, not a suppression.** Check what the
  surface shows *instead of* the motion, not that a
  `prefers-reduced-motion` block exists — the block is greppable and says
  nothing. A reveal presents its content at the final state; a scrubbed
  sequence presents each beat at its resting state; only decoration is
  correctly removed. `animation: none` over a reveal leaves the content
  invisible. Verdict table:
  [`accessibility-auditor`](../accessibility-auditor/SKILL.md) § 2.
- Test keyboard navigation (Tab, Enter, Escape, Arrow keys).
- Verify form submission and error recovery.

### Phase 2: Responsiveness

Test at four viewports:

| Viewport | Width | Device |
|---|---|---|
| Desktop | 1440px | Standard monitor |
| Tablet | 768px | iPad |
| Mobile | 375px | iPhone SE |
| Floor | 320px | Narrowest supported — the asserted floor |

The 320px row is the floor [`fe-design`](../fe-design/SKILL.md) already asserts
("every layout must work on 320px width"). It is in this table because an
asserted floor outside the measured set is an assertion nobody checks; 375px
passing says nothing about 320px, which is where a two-column grid or a fixed
`min-width` actually breaks.

- **Read the probe artifact's `viewport_matrix` rows** — one per declared width, recording whether the
  layout property that should change at that breakpoint did. A not-applicable row is missing evidence, not a pass.
- **Run the appearance floor** (§ Appearance verification) at every one of the four widths.
- **Scroll-driven surface** — read the `scroll_evidence` artefact
  ([`references/verification-automation.md`](references/verification-automation.md)
  § Scroll evidence) and report every sample whose asserted `state` and
  `observed` disagree as a finding. An empty `samples` array is a recorded null,
  not a pass.
- Check layout shifts, overflow, and content reflow.
- Verify touch targets are at least 44x44px on mobile.

### Phase 3: Visual Polish

- **Typography:** Font sizes, weights, line heights, hierarchy.
- **Spacing:** Consistent margins, padding, alignment.
- **Colors:** Contrast ratios, brand consistency, dark mode.
- **Alignment:** Grid alignment, visual balance.
- **Icons:** Consistent size, style, and spacing.

### Phase 4: Accessibility (WCAG 2.1 AA)

| Criterion | Check |
|---|---|
| **1.1.1** | All images have meaningful alt text |
| **1.3.1** | Semantic HTML (headings, landmarks, lists) |
| **1.4.3** | Color contrast ≥ 4.5:1 (text), ≥ 3:1 (large text) |
| **1.4.11** | Non-text contrast ≥ 3:1 (UI components, borders) |
| **2.1.1** | All functionality available via keyboard |
| **2.4.3** | Focus order is logical and predictable |
| **2.4.7** | Focus indicator is visible |
| **3.3.1** | Error messages identify the field and describe the error |
| **3.3.2** | Labels and instructions for form inputs |
| **4.1.2** | ARIA roles, states, and properties are correct |

### Phase 5: Robustness

- **Empty states:** What happens with no data?
- **Error states:** What happens when things fail?
- **Content overflow:** Long text, many items, large numbers.
- **Loading states:** Skeleton screens, spinners, progressive loading.
- **Boundary values:** Min/max inputs, special characters.

### Phase 6: Code Health

- Component reuse — are existing components used where possible?
- Design tokens — are colors, spacing, fonts from the design system?
- CSS patterns — utility classes vs. custom CSS, consistency.
- Accessibility in code — semantic HTML, ARIA attributes.

### Phase 7: Content & Console

- Grammar and spelling in UI text.
- Consistent terminology and tone.
- No placeholder text left in production.
- Check browser console for JavaScript errors or warnings.

## Appearance verification — mandatory, and explicitly appearance-only

```
APPEARANCE VERIFICATION IS MANDATORY WHEREVER APPEARANCE CAN BE AFFECTED.
THE PROBE DEMOTES THE IMAGE FROM PRIMARY EVIDENCE — IT DOES NOT MOVE THE FLOOR.
AN IMAGE IS NEVER EVIDENCE FOR HOVER, FOCUS, KEYBOARD, BREAKPOINT OR JS BEHAVIOR.
AN UNRUN APPEARANCE CHECK IS REPORTED AS UNRUN, NEVER AS PASSED.
```

**Trigger — identical to the two capture steps it replaces**, not merely as broad: Phase 0
unconditionally, Phase 2 once per width. Only what the image is evidence *for* narrowed.
**Two jobs, and the older one comes first:** (1) presence and sanity — *"presence + sanity
check that nothing renders broken. Not pixel-perfect regression"* — no blank frame, no
collapsed or overlapping layout, no missing region, no unstyled flash; **no probe dimension
covers it**, because a computed style can be correct on a node nobody can see; (2) pixel
comparison against a baseline where one exists, element-scoped, dynamic content masked. No
render capability → scope the verdict and say so per the gate at the top of this skill;
degrading is reported, never a pass. What a clean render does *not* answer:
[`references/verification-automation.md`](references/verification-automation.md) § Appearance verification.

## Reviewer posture

**Approval is earned, not assumed. Default to flagging.**

A design review is a skeptic's pass. The default verdict for every element
is "this needs to justify itself" — not "this is probably fine." Approve
explicitly when you have examined the evidence and found it sound.

This posture prevents the failure of "nothing to report" reviews that miss
real issues because the reviewer defaulted to charitable assumptions.

## Subtraction-first remedial hierarchy

When a finding warrants a remediation recommendation, prefer in this order:

1. **Delete** — remove the element, animation, pattern, or copy entirely
2. **Reduce** — make it smaller, shorter, subtler, less frequent
3. **Fix the specific issue** — change easing, origin, duration, contrast, font
4. **Make it interruptible** (for motion) — switch to transition/spring
5. **Move to GPU** (for motion) — animate only transform/opacity
6. **Polish** — the lowest-leverage fix; only if the above don't apply

*"Delete the animation" is always the first option to consider, even before
suggesting a different easing curve.* The same applies to decorative elements,
excessive copy, and redundant UI chrome.

## Section index — load on demand

Load the reference file whose sections the review needs — never all of them by default:

- [`references/review-communication.md`](references/review-communication.md) — Before / After / Why output format · Communication principles · Report structure · Design Review Summary
- [`references/verification-automation.md`](references/verification-automation.md) — Visual QA with browser automation · Async-verifier pattern (keep the main context clean) · Appearance verification (what a clean render does not answer)

## Output format

1. Design review report following the Report structure section
2. Severity-rated findings (blocker, suggestion, nit)
3. Accessibility and responsive compliance summary

## Auto-trigger keywords

- design review
- UI review
- UX audit
- accessibility
- WCAG
- responsive

## Gotcha

- Don't review design without understanding the user's constraints (time, resources, scope).
- The model tends to suggest accessibility improvements that break the existing design system.
- "Best practice" is not always the right choice — sometimes "good enough" ships faster.

## Read the authority object — the review is scoped by it

Read the resolved `ui_authority`
([contract](../../../docs/contracts/ui-authority.md)) before reviewing. Three
fields change what a finding *means*:

- **`surface_mode`** sets the density, hierarchy and expressiveness a reviewer
  should expect. A dense `operate` screen is not "cramped" and a generous
  `persuade` hero is not "wasteful".
- **`change_intent`** decides whether a visual-world difference is a finding at
  all. Under `preserve` a palette or type-family delta is a **defect**; under
  `redesign` it is the point.
- **`reference_maturity`** decides whether a difference from the reference is a
  defect. A `wireframe` declares structure, so reproducing its gray boxes is
  over-fidelity, not fidelity.

```
QUALITY FLOORS DO NOT VARY BY SURFACE MODE.
THE Q1-Q6 FLOOR SET IS IDENTICAL IN ALL FOUR MODES.
```

Do not re-derive any of these fields here. This skill is a declared consumer of
that object, and the contract's consumer table names it.

## Fidelity proof — the chapter matrix

```
A 1:1 CLAIM IS PROVEN BY A COMMITTED MATRIX, NEVER BY A GREEN SUITE.
ONE ROW PER HANDOVER CHAPTER. ONE EVIDENCE KIND PER ROW. NO EMPTY CELL.
A BEHAVIOR TEST ANSWERS "DOES IT WORK", NOT "DOES IT MATCH".
```

This discharges [`design-fidelity`](../../rules/design-fidelity.md)'s proof
clause. It fires when a numbered handover is the spec — chapters like
`10-datenmodell-api.md` … `46-roadmap-achse-randtage.md`, each an abgegrenzter
contract. Such a handover is already a checklist; the failure it prevents is
reading it and never working it as one.

**Build the matrix from the handover's own numbering**, one row per chapter:

| Chapter | Claim it makes | Evidence | Status |

**Evidence is exactly one of four kinds**, and the row names which:

1. **Element-scoped screenshot baseline** — `toHaveScreenshot` on the component,
   not the page. Built into Playwright via pixelmatch, so no new dependency
   ([`playwright-testing`](../playwright-testing/SKILL.md)). Mask dynamic
   content (timestamps, running numbers, ids) or the baseline flakes on data
   rather than on design.
2. **`toHaveCSS` assertion on the value the chapter names** — the right kind
   when the chapter states a token, a spacing step or a color rather than a
   shape.
3. **Behavior spec with a sensitivity probe** — legitimate where the chapter
   describes an interaction. The probe is not optional: neutralise the
   mechanism, watch the spec go red, restore it. A spec never seen red has
   unknown sensitivity and is not evidence.
4. **Explicitly not implemented, with the reason** — a real row, not a gap. An
   honest `not implemented` is what makes the other three trustworthy.

**The matrix is committed**, not written into a reply. A matrix that lives in a
chat message dies with the session, which is the difference between a method and
an artifact — and the whole reason this section exists rather than a paragraph
telling a reviewer to be thorough.

**The staleness trap.** A new handover version ships and the baselines stay
pinned to the old one, so every screenshot row passes against a reference nobody
uses any more. Check the baseline timestamps against the handover's own
CHANGELOG before reading a green matrix as a pass.

**What the matrix does not do.** It records what was compared, never that the
comparison was honest — nothing in this tree reads a handover, so a row naming
evidence nobody took looks exactly like one naming evidence that was. The
control is that a reviewer can open it.

## Review independence — two passes, isolated, in this order

```
PASS A (JUDGEMENT) RUNS BEFORE PASS B (DETECTOR + RENDER), AND IN ISOLATION.
INLINE EXECUTION IS PERMITTED ONLY WHERE NO SPAWN PRIMITIVE EXISTS, AND THEN
LINE 1 READS `DEGRADED: single-context (<reason>)`.
THERE IS NO THIRD STATE.
```

**Pass A — judgement.** Read the surface and form a verdict without the
detector output and without the render artefact. Emit an assessment id.

**Pass B — detector plus render.** Run `lint_design_slop` and read the
`ui:render` manifest. Emit a second assessment id.

**Order is the whole point.** A judgement formed after reading a detector's
findings is anchored to them: the reviewer confirms the list instead of looking
at the surface. Running A first is what keeps B's findings additive rather than
directive — the same reason
[`evaluator-independence`](../../rules/evaluator-independence.md) forbids
pre-loading a verdict into a reviewer's prompt.

**When no spawn primitive exists** the two passes share one context, which
means A cannot be isolated from B. That is a real degradation and it is
reported, not hidden: line 1 of the output reads

```
DEGRADED: single-context (<reason>)
```

Output therefore carries **either** two assessment ids **or** that banner.
Neither present is not a third state — it is an unreported degradation, and it
is the failure this section exists to prevent.

## Anti-slop scan

Hybrid: a deterministic detector does the mechanical pattern-matching (zero
token cost, no catalog reload); you do the judgment it cannot. After the
structured review phases, add an explicit **Anti-Slop Check** section:

1. **Run the deterministic detector first** — it catches the pattern-detectable
   tells so you don't eyeball or re-derive them:
   ```
   npx tsx node_modules/@event4u/agent-config/src/scripts/lint_design_slop.ts --dir <consumer-ui-path> --json
   ```
   Each finding carries `rule` (e.g. `slop-v1-side-stripe`), `catalogId`
   (`V1`), `severity` (`P0`–`P3`), `file:line`, and a `message`. **Cite these
   verbatim** (rule-id + catalogId + file:line) — do not re-describe them from
   the prose catalog. Findings are *rebuttable presumptions*: a finding the
   consumer's `DESIGN.md` gate suppresses is already filtered out; a remaining
   finding means the project has not declared the pattern as intentional.
   `lint_design_slop` is **flags, never a block** (default exit 0; CI opts into
   failure via `--fail-on`).
2. **Judge what the detector cannot** — load
   [`docs/guidelines/design-antipatterns.md`](../../../docs/guidelines/design-antipatterns.md)
   for the tells that need structural/aesthetic judgment (e.g. T3 icon-tile
   stack, L2 three-identical-card grid, V2 glassmorphism intent). List any that
   appear, cite by entry ID, and check the override condition.
3. Run the AI-slop originality self-test on the overall aesthetic direction.
   Report the result (pass / flag / fail) with one sentence of evidence — this
   is the human judgment the detector deliberately does not make.
4. **Mark the findings a provided artifact already answers.** When the run is a
   port (`state.ui_design.provided_artifact` is set), a finding about a
   decision the artifact makes is correct about the pattern and wrong about the
   action. Keep it in the output, cite it as **"matches provided spec"**, and
   set `artifact_covered: true` on it — the polish gate drops those from the
   round-driving set, so an unmarked finding will send a round at the user's
   own design. The flag is scoped to decisions the artifact actually covers;
   anything it leaves open (a state it never showed) is generative work and
   keeps the full scan. Precedence + scope:
   [`design-fidelity-mechanics`](../../../docs/guidelines/design-fidelity-mechanics.md)
   § Provided-artifact precedence. Regression witness: `daf-slop-vs-provided`.

For the **objective quality floors** (WCAG contrast, font-size, line-length,
reduced-motion, heading hierarchy, focus indicator), do NOT eyeball them —
run the `accessibility-auditor` checklist (Q1–Q6 in the catalog) and cite its
verdict. The review owns the *subjective* anti-slop judgment (Visual /
Typography / Color / Layout taste); `accessibility-auditor` owns the
*objective* floors and the WCAG *audit method*. Cite, don't re-derive.

## Do NOT

- Do NOT skip accessibility testing — it's not optional.
- Do NOT report issues without evidence (screenshots, specific elements).
- Do NOT prescribe solutions — describe problems and impact.
- Do NOT block PRs on nitpicks.
- Do NOT test only at desktop resolution.
