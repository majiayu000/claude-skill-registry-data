---
name: html-design-polish
description: 网页需要产品清晰度、信息层级、响应式或视觉系统美化、重设计或设计审计时使用。
---

# HTML设计美化

## Goal

Make the product purpose and primary user task clear before adding visual character. Build quality through hierarchy, proportion, spacing, material, and brand fit; do not reproduce a fixed palette, font, radius, layout, or component library.

## Scope and boundaries

Use for product pages, internal tools, navigation hubs, mobile web tools, design audits, redesigns, visual refinement, reference-image interpretation, and pages that feel generic, templated, or brand-incoherent.

Do not trigger by default for:

- Ordinary feature implementation with an already-decided design.
- A single CSS bug or mechanical responsive fix.
- Pure code refactoring.
- Exact pixel replication.
- Component work with no product, hierarchy, or visual judgment.
- Business research or content strategy without a web artifact.

In an existing project, preserve data, formulas, links, routes, states, business rules, and working behavior unless the brief explicitly changes them. Do not turn a focused tool into a landing page or dashboard merely to make it look more designed.

## Choose the execution mode

### Audit mode

Use when the user asks to analyze, assess, audit, evaluate, recommend, or explicitly says not to modify yet.

- Read the relevant project material and inspect the rendered page when possible.
- Produce a diagnosis at the requested depth.
- Do not edit code, generate implementation artifacts, or claim visual verification for changes that were not made.

### Execute mode

Use when the user asks to modify, redesign, optimize, implement, repair the design, or polish the page.

1. Diagnose internally.
2. Lock protected behavior and content.
3. Implement high-confidence, in-scope changes directly.
4. Run the page and verify rendered and business states.
5. Complete a second refinement pass.
6. Report at the task-appropriate detail level.

Do not stop after routine diagnosis to request approval. An unfamiliar project is not a blocker: inspect it, establish invariants, and proceed.

Stop only if a critical input is absent, the project cannot be inspected or run enough to act safely, the next action creates irreversible/material external risk, or the user must choose between materially different product directions.

## Operating sequence

Use this order. Do not start with colors, gradients, glass, or animation when an earlier layer fails.

1. Product model
2. User and core task
3. Information architecture
4. Interaction and responsive composition
5. Visual system
6. Browser and business verification

### 1. Product model

Classify the page before judging layout:

- Single-task tool
- Multi-step tool
- Dashboard
- Marketing landing page
- Navigation hub
- Content experience
- Other explicit model

Confirm that the current page model matches the actual product purpose. Diagnose these errors first:

- A single-task tool is made into a dashboard.
- An internal tool is made into a marketing landing page.
- A result-oriented tool leads with extensive explanation.
- A navigation hub is made into corporate promotion.
- Unsupported metrics, cases, testimonials, or social proof are invented.
- A reference image changes the product purpose instead of informing visual direction.

If the model is wrong, repair model and task sequence before visual polish.

### 2. User and core task

State, in one sentence each:

- Primary user and use context.
- Core task and desired outcome.
- What a first-time user must understand in one viewport.
- Primary action or result.
- Secondary tasks and their frequency.
- Protected data, formulas, links, routes, states, and business logic.
- Target viewports and relevant device orientation.
- Explicit scope and out-of-scope changes.

Ask:

- Can a new user say what this product is, who it serves, and what to do next?
- Is the highest-value outcome visible before internal taxonomy, long explanation, or secondary reporting?
- Does copy describe a concrete product task rather than generic slogans?
- Is status/availability truthful?

If these answers are unclear, solve this layer before styling.

### 3. Information architecture

List visible modules in order. Rank each by user value and frequency.

Check:

- Does the current order follow the user task rather than internal project structure?
- Does the first viewport jointly expose purpose, current context, outcome, and next action?
- Are primary, secondary, and supporting actions visibly different in weight?
- Does any selector, navigation, or dashboard occupy more space than the content it controls?
- Is a high-value result hidden behind long policy/process text?
- Can low-frequency details be grouped, collapsed, deferred, or hidden?

When several entries exist, group by user task and status. Do not flatten internal project names into equal cards. Promote the primary available action or result; make secondary entries quieter but discoverable.

### 4. Interaction and responsive composition

Treat mobile as a new composition and disclosure problem, not a reduced desktop layout.

For every responsive state decide:

- What remains visible first.
- What moves, collapses, or becomes on demand.
- How navigation/selection changes: row, segmented control, compact grid, list, drawer, or another explicit pattern.
- How long labels, values, units, and mixed-language text wrap.
- How selected, focus-visible, expanded, disabled, loading, error, empty, and long-content states render when present.

Test the actual minimum supported width, 375 px, 414 px, relevant tablet, and relevant landscape. Check for horizontal overflow, clipped controls, vertical character stacking, accidental multi-line clickable labels, loss of primary-task exposure, and touch-target failures.

Select columns from item count, task frequency, and label length. For example, a compact 3×2 grid can suit six navigation entries; it is not a global mobile rule.

### 5. Visual system

Use visual treatment to clarify purpose, hierarchy, state, and brand. Do not use it to hide structural weakness.

Inspect in this order when the page feels ordinary, heavy, generic, or “not premium”:

1. Task order and first viewport.
2. Container width and text measure.
3. Alignment and spacing rhythm.
4. Typography levels, numbers, labels, and line breaks.
5. Density and visual weight.
6. Asset quality and image crop.
7. Borders, cards, shadows, material, and motion.

Give every color, surface, border, icon, image, and animation a job: identity, hierarchy, state, grouping, affordance, depth, feedback, or explanation. Remove it if it has none.

Standardize repeated geometry and interaction behavior. Preserve meaningful product/brand differences such as logos and restrained product accents. “Unified” does not mean every item has identical color or prominence.

Use a supplied reference image to extract hierarchy, proportion, material, contrast, image role, and interaction tone. Adapt those decisions to the product; do not copy pixels or change product purpose. Keep critical text in HTML rather than generated imagery.

### Project icon generation (required)

For every named project, product, or service entry shown on the page, generate one corresponding primary icon with Image2 (`image_gen`). Do not substitute generic line icons, emoji, or a repeated placeholder as the primary project identifier.

- Generate each icon from its actual product/service function, name, and brand cues; use one distinct prompt per entry.
- Use Apple TV-style app-icon language: clean rounded-square silhouette, tactile dimensional form, centered recognizable symbol, controlled highlight/shadow, no black outer ring, no nested frames, no baked UI chrome.
- Keep the icon set structurally consistent: shared canvas, scale, corner treatment, depth, and lighting direction. Use restrained per-project color variation to aid recognition.
- Do not bake important text, product names, or tiny labels into icons. Keep names and status as HTML beside or below the asset.
- Inspect every generated result at its real card size. Regenerate individual failures instead of applying CSS effects to hide weak icon anatomy.
- Save approved assets inside the current project and reference local copies. Never leave a project-used icon only in generated-image storage.
- If the project already has an approved brand icon/logo, use it as the semantic reference; generate an Apple TV-style companion only when the user asked for the visual treatment or the existing asset cannot serve the entry.

## Decision rules

| Condition | Judge | Act |
|---|---|---|
| First viewport is unclear | Purpose, outcome, and next action are not visible together | Reorder/rewrite the first viewport before styling |
| A result tool starts with explanation | The result is delayed by low-frequency detail | Promote the result; collapse or defer explanation |
| Users choose among many entries | Frequency, grouping, status, and scan order | Group by task; give primary/available/secondary entries distinct weight |
| A selector dominates the page | Control uses more attention/space than controlled content | Replace default-expanded cards with compact choices; expand only where needed |
| The UI feels heavy | Nested frames, repeated labels, oversized cards, too many borders | Remove one structural layer at a time; retain only layers with a job |
| The page feels generic | Product could be swapped by changing logo/accent only | Increase product-specific task language, structure, and asset role |
| The page feels “not premium” | Hierarchy, proportion, spacing, type, density, or asset quality is weak | Correct those first; add effects only if they strengthen the direction |
| Strong material/style is requested | It supports brand but risks legibility | Build controlled layers; protect contrast, focus, and reduced motion |
| Reference image is supplied | DNA is useful but product differs | Adapt visual DNA, retain current product task and invariants |
| Visual-only change is requested | Behavior must remain unchanged | Lock invariants and exercise them before/after |
| Brand variants coexist | Uniformity may erase recognition | Standardize system rules; retain meaningful identity signals |
| Mobile is crowded | Desktop order/density no longer serves the task | Reorder, regroup, collapse, resize, and retest |

## Avoid these failure modes

- Effects, gradients, glass, or animation used to compensate for weak hierarchy.
- Nested frames around already distinctive logos or assets.
- Large fields of same-size, same-weight cards.
- Every section given an icon, pill, badge, gradient, and rounded container.
- Hero copy that sounds polished but does not explain the tool.
- A hidden or diluted primary action.
- Generic SaaS rhythm imposed on a focused workflow.
- Dashboard chrome imposed on an internal single-task tool.
- Desktop layout merely shrunk for mobile.
- Generated or invented metrics, testimonials, proof, or case studies.
- Important text embedded in generated images.
- Visual changes that silently alter formulas, policy data, links, state, or copy meaning.
- Declaring success from source inspection or one default screenshot alone.

## Implementation workflow for Execute mode

### Establish invariants

Before editing, identify and protect:

- Business data, formulas, and result calculations.
- URLs, routes, product names, availability, and feature flags.
- Existing interactions and keyboard behavior.
- Accessibility requirements and reduced-motion behavior.
- Required root/production parity, if applicable.
- Explicitly out-of-scope modules or files.

Create or run the smallest useful checks for these invariants. A visual improvement that breaks a business rule is a regression.

### Make structural changes first

Change page order, grouping, disclosure, navigation, or CTA weight only when product model, task sequence, or hierarchy requires it. Otherwise patch locally.

After structure changes, verify protected behavior before visual polish. If the task is still unclear with colors/effects mentally removed, continue structural work.

### Build the system

Reuse sound existing tokens. When creating new rules, define named roles for typography, spacing, surface, border, focus, status, motion, and brand accents. Avoid per-element visual improvisation.

Use containers for repeated entities, state, interaction, or meaningful grouping. Use icons for navigation, status, or rapid recognition; do not attach them automatically to every heading or row.

For project/service entry cards, run the required Image2 icon-generation pass before final card polish. Generate first, place real assets, then tune crop, vessel, contrast, and spacing around the approved icons. Do not judge the card system from placeholder icons.

### Implement responsive behavior

Design mobile deliberately:

1. Choose the first-visible information.
2. Set the mobile order.
3. Choose collapsed/expanded defaults.
4. Select a compact navigation or selector form.
5. Add safe wrapping and minimum-width behavior.
6. Test long labels, values, units, and mixed-language strings.
7. Add landscape-height rules when the usage context requires them.

### Verify and refine

Run the actual page. At each target viewport, record:

- Whether the core task is visible and understandable.
- Horizontal overflow and clipping.
- Typography, wrapping, alignment, and image crop.
- Selected, focus, expanded, long-content, error/loading/empty states when present.
- Console errors and asset loading.
- Relevant business outputs and interactions.

Compare the same state before and after. Then perform a second refinement pass for line breaks, spacing, content width, same-weight residue, focus/selected treatment, numeric alignment, image contrast, and reduced motion.

## Audit template

Use this structure in Audit mode or as internal notes in Execute mode.

### Context

- Product model:
- Primary user/context:
- Core task and first-viewport outcome:
- Protected behavior:
- Target states/viewports:
- Scope and exclusions:

### Ranked diagnosis

1. Product model:
2. User and core task:
3. Information architecture:
4. Interaction and responsive composition:
5. Visual system and brand fit:
6. Browser/business verification gaps:

### Direction

- What should become dominant:
- What should become quieter, grouped, collapsed, or deferred:
- Brand/reference decisions to retain:
- Effects deliberately excluded:
- Invariants to protect:
- Evidence required to accept the result:

## Acceptance checklist

- [ ] Product model matches product purpose.
- [ ] User, core task, and first-viewport outcome are explicit.
- [ ] Product/IA issues were resolved before visual polish.
- [ ] Primary and secondary actions have distinct weight.
- [ ] Protected behavior and content invariants still pass.
- [ ] Visual choices serve task, brand, state, or reference evidence.
- [ ] Each visible project/service entry has an approved, project-specific Image2 icon in the Apple TV-style family.
- [ ] No unnecessary decorative nesting or equal-card field remains.
- [ ] Mobile was recomposed where needed, not only scaled down.
- [ ] Target desktop/mobile/tablet/landscape states were rendered.
- [ ] Overflow, wrapping, focus, selected, collapsed/expanded, and relevant business states were checked.
- [ ] Before/after comparison proves clearer task use, not only different styling.
- [ ] A second refinement pass is complete.

## Output contract

Choose output depth from task scale. Do not create a full design report for a small targeted refinement.

### Small targeted refinement

Return only:

1. Core issue
2. Changes made
3. Browser verification
4. Remaining issues

### Full redesign or audit

Return, in order:

1. Product and task summary
2. Ranked diagnosis: product model, information architecture, interaction/responsive, visual system
3. Protected invariants and project-specific constraints
4. Chosen direction and rejected alternatives with reasons
5. Files and states changed, or proposed changes in Audit mode
6. Browser verification matrix and before/after findings
7. Remaining risks or evidence gaps

Never present a contextual palette, font, radius, card form, or layout as a universal rule.
