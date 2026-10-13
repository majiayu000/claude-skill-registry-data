---
name: ui-redline
description: Diagnose an existing UI implementation (screenshot, code, or live URL) against an approved spec, identify mismatches, rank them by severity, prescribe exact fixes, and produce a copy-paste-ready refactor prompt that can be sent back to a code-generation step. Use this skill whenever the user has a built UI that doesn't match what they expected, says "this doesn't look right", "fix the layout", "review what was generated", or pastes a screenshot of an implementation. Always use it as the closing step of any build cycle when the result feels off — even if the user can't articulate exactly what's wrong, this skill names the mismatches and produces the fix.
status: stable
---

# UI Redline

Compares an implementation against a spec and produces three things: a list of mismatches with severity, exact fixes for each, and a refactor prompt to feed back into `ui-generate-code` (or any other code path). This is the loop-closer of the kit — without it, the spec and the build drift apart with no formal mechanism to reconcile them.

## When to use this skill

Use this skill when:
- The user has built (or had Claude build) a UI that doesn't match the spec or doesn't match their mental picture.
- The user pastes a screenshot and says "this looks off" / "fix this" / "what's wrong".
- A build was declared "done" but `ui-acceptance` failed several checks.

Do **not** use this skill when:
- No spec exists. Without a spec, "redlining" is just opinion-giving. Run `ui-brief` and `ui-blueprint` first.
- The user wants to redesign, not fix. Redesign is `ui-blueprint` again, not redline.

## Core principle

**A redline names the gap, doesn't dramatize it.** The output is dispassionate: "spec says X, implementation does Y, severity is Z, fix is this exact change." No hand-wringing, no "this is awful". The point is to produce actionable fixes, not to prosecute.

## Pre-flight check

Before drafting, confirm:

1. **A spec exists.** Brief, blueprint, component spec, system spec, or acceptance checklist. At least one. Without a spec, the redline has nothing to compare to.
2. **The implementation evidence is available.** This can be a screenshot, code snippet, live URL, or static source-code inspection report.
   **Preferred input:** Use the evidence report produced by `ui-inspector` (found at `redlines/inspector-report.md`) as the primary data source, supplemented by screenshots or code where helpful.
3. **The user knows what they're complaining about, or is genuinely unsure.** If they can articulate it ("the button is the wrong color, the spacing is too tight"), capture those as starting points. If they can't ("just looks weird"), proceed systematically through the spec.
4. **Determine the redline mode.** Choose one of the three modes below and declare it in the report header. The mode controls which verification status values are available.
5. **Choose evidence confidence level.** Prefer Playwright-backed inspector evidence when available for layout, responsive behavior, keyboard flow, modal or drawer behavior, and accessibility checks. If unavailable, continue with static evidence and clearly label the redline as partial.

If no spec exists, refuse and propose: "Let's recover a brief and blueprint quickly first — otherwise I'm just guessing what you wanted."

---

## Redline modes

Declare one mode at the top of the report. The mode determines how each mismatch finding is classified and what the overall report can reliably assert.

### Mode 1 — Live authenticated browser

Full browser access with a valid auth session. All states, dynamic behaviors, keyboard navigation, and network-triggered states can be tested directly.

Verification status values available: `verified live`, `cannot verify`.

### Mode 2 — Live unauthenticated smoke

Browser access but the target route redirects to login. Only pre-auth states (login page, redirect, public landing, error pages) can be verified live. Post-auth UI must be checked by static source-code analysis or deferred.

Verification status values available: `verified live`, `verified by static code`, `deferred — auth-gated`, `cannot verify`.

### Mode 3 — Static-code-assisted partial

No live browser access. All evidence is from source code, screenshots, or a static inspector report. Useful when the route is behind auth, an environment is unavailable, or the redline is being run in a headless context.

Verification status values available: `verified by static code`, `deferred — needs live DOM`, `cannot verify`.

**Mode 3 reports must be labelled "partial redline" in the frontmatter (`partial: true`) and in the report title.** A partial redline is valid and useful, but readers must know its limits.
If Playwright evidence is unavailable, explicitly describe the report as `static partial` and do not imply live verification.

---

## The severity scale

Use these four levels exactly. Do not invent more.

| Severity | Meaning | Examples |
|---|---|---|
| **Blocker** | Implementation violates a hard spec requirement; ship is blocked. | Required state missing (no error state); accessibility violation (no labels); primary action not present. |
| **Major** | Implementation diverges from spec in a way the user will notice. | Wrong color used; wrong layout density; missing hover state; wrong copy. |
| **Minor** | Divergence within tolerance but worth fixing. | Slight padding mismatch; non-token spacing value; redundant whitespace. |
| **Polish** | Aesthetic or refinement, not in spec but worth raising. | Icon stroke inconsistency; subtle alignment improvement. |

Polish items are noted but should not be presented as failures — they're opportunities. Only blockers and majors gate "ship".

## Workflow

### Step 1 — Inventory the spec sections in scope

List the spec sections that apply to this implementation. For example, for a built component:
- component-spec: §2 anatomy, §3 props, §4 states, §5 behavior, §7 a11y
- system: §2 spacing, §4–5 colors

These become the audit frame.

### Step 2 — Walk the spec, check the implementation evidence

For each section, compare what the spec says against what the implementation evidence shows. Use `redlines/inspector-report.md` as your source of truth for computed values.

For the inspector report:
- Compare computed values (colors, spacing, font sizes) against the design tokens in the spec.
- Check the DOM inventory for semantic completeness.
- Review accessibility findings for violations.
- Eyeball layout, hierarchy, color, spacing.
- Look for missing visual indicators (focus rings, hover states often invisible in static screenshots — note "cannot verify from screenshot" for those).

For code:
- Read the code against the spec line-by-line.
- Search for missing branches (e.g. component spec lists 8 states; code has 5 — find the missing 3).
- Search for hardcoded values that should reference tokens.

For live URLs:
- Inspect interactively. Test every keyboard shortcut. Test every state.

### Step 3 — Record each mismatch in the table

### Step 3 — Record each mismatch in the table

Use the redline table format. Each row: section, what spec says, what implementation does, severity, verification status, fix.

**Verification status values** (choose the one that matches the redline mode):

| Status | Meaning |
|---|---|
| `verified live` | Confirmed by direct browser interaction with an authenticated session (Mode 1 only). |
| `verified by static code` | Confirmed by reading source files — reliable but not browser-confirmed (Modes 2 and 3). |
| `deferred — auth-gated` | Cannot be checked without an authenticated session (Mode 2). |
| `deferred — needs live DOM` | Requires a running browser to verify (hover/focus states, runtime-injected styles, animations) (Mode 3). |
| `cannot verify` | Evidence is insufficient regardless of access level (e.g., a state that requires a specific data fixture not available). |

Deferred and cannot-verify rows must still appear in the table with their severity marked. Do not silently omit checks because they could not be verified — a deferred blocker is still a blocker.

### Step 4 — Prescribe exact fixes

For each row, the fix must be specific enough that a reasonably-instructed coder (or another AI) can execute it without ambiguity. "Make the spacing bigger" is not a fix. "Change padding from 8px to 16px (token: `space.4`) on the root container" is a fix.

### Step 5 — Generate the refactor prompt

The most valuable output is a single prompt the user can copy and paste into a fresh code-generation session, scoped to the specific changes. The prompt must:

- Reference the spec authoritatively ("per component-spec §4...").
- List every change in imperative form.
- State the severity ordering — blockers first.
- Not introduce any new design decisions — only fixes traceable to the spec.

### Step 6 — Confirm with the user

Show the redline. Ask: "Anything I've misread? Any severity you'd reclassify?" Iterate before delivering the refactor prompt.

## Output template

```markdown
---
spec_type: redline
spec_id: <slug>-redline-<n>
based_on:
  - component-<slug>  # or whichever spec(s)
  - system-<slug>
implementation_source: <screenshot path | code snippet | URL>
redline_mode: <"live authenticated" | "live unauthenticated" | "static partial">
partial: <true | false>  # true when redline_mode is "static partial"
created: <YYYY-MM-DD>
status: draft
---

# Redline: <component or screen name><br>_(partial — static-code-assisted)_ <!-- include this suffix only when partial: true -->

## 0. Summary

| Severity | Count |
|---|---|
| Blocker | N |
| Major | N |
| Minor | N |
| Polish | N |

**Recommendation:** <ship | block on fixes | needs partial rework>

## 1. Mismatches

| # | Section | Spec says | Implementation does | Severity | Verification | Fix |
|---|---|---|---|---|---|---|
| 1 | component §4 (Disabled state) | "border `border-muted`, background `surface-disabled`, text `text-muted`, cursor `not-allowed`" | Disabled state has the same color as default; no cursor change | **Blocker** | verified live | Add `disabled:bg-surface-disabled disabled:text-text-muted disabled:cursor-not-allowed` to the className list. |
| 2 | component §4 (Loading state) | "spinner replaces icon while loading; click blocked" | No loading state implemented at all | **Blocker** | verified by static code | Add `loading?: boolean` prop. Render `<Spinner />` in place of icon when `loading=true`. Wire `disabled={disabled \|\| loading}`. |
| 3 | component §7 (a11y) | "error linked to input via `aria-describedby`" | `aria-describedby` is missing | **Blocker** | verified by static code | Add `aria-describedby={error ? \`${id}-error\` : undefined}` to the input. |
| 4 | system §2 (Spacing) | "all spacing uses tokens from `space.*`" | `padding: 13px` (literal value) | **Major** | verified by static code | Replace `13px` with `padding-3` (12px, token `space.3`) — closest token, slight visual diff acceptable. |
| 5 | component §4 (Focus-visible) | "2px focus ring at `focus-ring-color`, offset 2px" | Focus ring is browser default (1px outline) | **Major** | deferred — needs live DOM | Add `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring focus-visible:ring-offset-2`. |
| 6 | component §1 (Label) | Button label is "Save profile" | Implementation says "Submit" | **Major** | verified by static code | Change button text to "Save profile". |
| 7 | system §6 (Border radius) | Cards use `radius.md` (8px) | Cards use 6px | **Minor** | verified by static code | Change `border-radius: 6px` → `radius-md` (8px). |
| 8 | (not in spec) | — | Icon stroke is 2px, system convention seems to be 1.5px elsewhere | **Polish** | verified by static code | If the system spec adds an `icon.stroke` token, switch to it. |

## 2. Fix order
Apply blockers first, majors second, minors when convenient, polish later.

1. **Blockers (3):** Disabled state styling; Loading state implementation; aria-describedby on input.
2. **Majors (3):** Spacing token compliance; Focus-visible ring; Button label microcopy.
3. **Minors (1):** Border radius adjustment.
4. **Polish (1):** Icon stroke consistency (defer).

## 3. Refactor prompt

Copy and paste the block below into a fresh `ui-generate-code` session (or any code-gen step), along with the original component spec.

````
Refactor the existing implementation of <ComponentName> to fix the issues below. Do not introduce any design decisions not listed here. Reference component-spec-<slug> for token names and behaviors.

Blockers (must fix):
1. Implement the disabled state per component §4: add classes `disabled:bg-surface-disabled disabled:text-text-muted disabled:cursor-not-allowed`.
2. Implement the loading state per component §4: add prop `loading?: boolean`; when true, replace the leading icon with `<Spinner />` and disable interaction by combining `disabled={disabled || loading}`.
3. Implement the a11y error linkage per component §7: add `aria-describedby={error ? \`${id}-error\` : undefined}` to the input element. Ensure the error text element has `id={\`${id}-error\`}`.

Majors (should fix):
4. Replace `padding: 13px` with the system token `space.3` (12px). Per system §2, no inline literal spacing values are allowed.
5. Replace browser-default outline with the focus-visible ring per component §7: add `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring focus-visible:ring-offset-2`.
6. Change the button label from "Submit" to "Save profile" per component §1.

Minors:
7. Change `border-radius: 6px` to the `radius.md` token (8px) per system §6.

Do not change anything else. Do not add features. Do not refactor working code. Output the updated file with comments mapping each change to its number above.
````

## 4. What I could not verify from this input

This section is **required** for partial redlines. List items that cannot be verified without live browser access or runtime evidence:

- <Things you couldn't tell from the inputs you had — e.g. "Cannot verify hover state from a static screenshot.">
- <Things that would require live DOM — e.g. "Cannot verify focus-visible color at runtime.">
- <Suggestion to provide more — e.g. "Please share a live URL or video to verify hover and focus states.">

**Required for static/partial redlines:** For each item listed, include a recommended next verification mode (e.g., "run in live authenticated browser", "inspect at runtime", "test with screen reader").

## 5. Open questions
- <Numbered>
```

## Examples

### Example 1 — screenshot-only redline

User pastes a screenshot of a settings form. Spec is the component spec for it.

What the redline can detect from a screenshot:
- ✅ Layout, hierarchy, density, color, copy.
- ✅ Visible state — usually default state.
- ❌ Hover, focus, error, loading states (not visible in static).
- ❌ Keyboard behavior, screen reader announcements.

The redline notes what it could see, and explicitly lists what it could not. The "What I could not verify" section becomes important here.

### Example 2 — code-only redline

User pastes the React file. Spec is the component spec.

What the redline can detect from code:
- ✅ Every state branch (existence and structure).
- ✅ ARIA attributes and event handlers.
- ✅ Token usage vs. literal values.
- ❌ How it actually looks (unless you can mentally execute the styles).

### Example 3 — code + screenshot together

This is the ideal input — together they cover both visual and structural mismatches.

## Rules that prevent hallucinated diagnoses

1. **Never criticize something the spec didn't define.** If the spec is silent, the implementation can't be wrong. At most, raise it as an open question or a polish item.
2. **Never invent severity.** Use the four-level scale exactly. Don't escalate aesthetics to blocker.
3. **Never write a fix that isn't a code change.** "Make it more aesthetic" isn't a fix. Every fix is a concrete edit.
4. **Never add criteria to the refactor prompt that weren't in the redline table.** The prompt must be derivable line-by-line from the table.
5. **Never make the refactor prompt a re-design.** The prompt is bounded by the spec — it doesn't introduce new requirements.
6. **Don't redline what you can't see.** If the user gave a screenshot, don't claim the keyboard shortcut is broken — you can't verify that from a still image. Move it to "could not verify".

## Acceptance criteria for this skill's output

A redline produced by this skill is acceptable only if every one of these is true:

- [ ] Frontmatter links to at least one upstream spec.
- [ ] Implementation source is identified (screenshot / code / URL).
- [ ] Redline mode is declared in the frontmatter (`redline_mode`) and in the report header.
- [ ] If mode is "static partial", `partial: true` is set in frontmatter and the report title carries the _(partial — static-code-assisted)_ suffix.
- [ ] Summary table shows counts at each severity.
- [ ] Every mismatch row has all seven columns filled (#, section, spec says, impl does, severity, verification status, fix).
- [ ] Every fix is specific enough to be executed without further questions.
- [ ] A refactor prompt is included, and every line of it traces to a row in the mismatch table.
- [ ] The "could not verify" section is present (even if empty, to make the limits of the analysis explicit).
- [ ] No mismatch is graded above its evidence — if you can't see it, you can't blocker it. Deferred items may carry an estimated severity but must be labeled `deferred` in the verification column.

If any check fails, revise before delivering.
