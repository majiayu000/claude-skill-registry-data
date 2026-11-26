---
name: flawless-ui-ux
description: Create, redesign, refine, or review web, native mobile, and desktop interfaces with product-specific visual design and usable interactions.
---

# Flawless UI/UX

Turn a product task into a deliberate interface, then inspect what the implementation actually does. The useful output is a screen people can understand and operate, with visual character appropriate to its content. An unfamiliar font, a different palette, fewer cards, or a clean automated report is not proof of improvement.

Use the requested platform and stack, preserving appropriate navigation, input, and accessibility conventions. Examples do not prescribe a sector, device, or aesthetic.

## Establish the intervention

Inspect the target, neighboring components, real content and available assets. Identify the visitor's main task, the requested change, and the facts, behavior and visual decisions that must survive. Recover existing product/design documents using [project context](references/project-context.md) when continuity matters. A short brief permits confident choices; it does not authorize invented product claims.

Distinguish the surface's job: a public page explains an offer and a next action; an operational screen supports repeated tasks and comparison; a reading surface supports comprehension; a collection lets the work lead. These jobs guide decisions, not prescribed styles. One product can contain all four. Native and desktop applications also owe users their platform's navigation, input and accessibility conventions.

- **Create:** establish information priorities and composition, inheriting an existing system where it is authoritative. Read [Direction](references/direction.md), then the craft and product references relevant to the actual surface.
- **Redesign:** replace authorized visual decisions while retaining product truth and functioning behavior. Read Direction and [Calibration](references/calibration.md); explicitly distinguish preserved facts from replaceable presentation.
- **Refine:** diagnose the weak relationship before editing. Read Calibration for a broad refinement and the reference owning the affected decision. Preserve identity and everything outside scope. A local contrast correction needs Color, not an entire direction workshop.
- **Review:** use [Review](references/review.md). Report evidence and corrections without editing, installing dependencies, formatting, or mutating live state. Planning delivers a proposal, not an implementation.

For broad work, form a concrete working hypothesis before editing: which information should lead, what currently prevents it, and what change should improve the task. Keep it in working notes rather than inventing a user-facing slogan. An observed defect can justify a direct correction. Ask only when an unresolved fact materially changes identity, scope, integration, or the promised outcome.

Use the requested stack and existing reliable primitives. Do not replace working controls merely to make the transformation visible. Preserve copy in visual-only work and presentation in copy-only work. Do not manufacture network, loading or failure states for an operation that is synchronous and local.

## Load the knowledge that changes the decision

Read the owning reference before making that kind of decision. This is selective routing, not a demand to read the whole library. Reuse material already loaded. A broad refinement normally needs Calibration plus the affected craft/product guidance; creation needs Direction plus the guidance for the main content and interaction. When a problem spans areas, resolve the underlying structure before polishing its symptoms.

| Question | Reference |
|---|---|
| Which information and action belong on this surface? | [Product structure](references/structure.md) |
| What craft decision needs deeper treatment? | [Craft](references/craft.md), routing to [Typography](references/typography.md), [Layout](references/layout.md) and [Color](references/color.md) |
| How should records and comparisons survive small screens? | [Tables](references/tables.md) and [Charts](references/charts.md) |
| How should inputs, errors and recovery work? | [Forms](references/forms.md) and [States](references/states.md) |
| How should controls, feedback, keyboard access, and states behave? | [Interaction](references/interaction.md) |
| What should the words say, and in whose voice? | [Copy](references/copy.md) |
| What should change in a broad visual refinement? | [Calibration](references/calibration.md) |
| Which recurring patterns need inspection? | [Contextual prevention](references/anti-slop.md) |
| Would a worked composition clarify the design? | The relevant [design study](references/design-studies.md) |
| Is a critique or deeper diagnosis needed? | [Review](references/review.md) |
| Should motion exist, and how should it behave? | [Motion](references/motion.md) |
| What makes this surface slow or unstable? | [Performance](references/performance.md) |
| Which platform conventions govern this implementation? | [iOS](references/ios.md), [Android](references/android.md), or [Desktop](references/desktop.md) |

References contain decision criteria and original worked examples, not compulsory styles. The examples' names, numbers, palettes and page structures are illustrative. Adapt the relationship that helps; do not copy a fictional business into the user's product. The bundled web examples are small executable studies, not a component framework to install into every project.

## Execute and compare

For new surfaces and broad redesigns, consider three genuinely different organizations of the content as Direction describes. Keep that exploration internal unless concepts are requested. Once the direction is settled, carry it through the lower regions and meaningful states. A hero that looks finished above an unrelated stack of template sections is incomplete.

For refinement, select the smallest intervention that resolves the diagnosis. Change grouping or information order when those are the cause; do not compensate with a larger heading or a new accent. Keep a useful baseline capture when rendering is available and compare matching content, state and width. Preserve useful density and expression. If the current interface already meets the task, do not invent a defect to justify changes.

For data interfaces, verify the semantic relationships as well as presentation: units, periods, signs, missing values, aggregate scope and state changes. Inspect the task at mobile width before deciding that an inner scroll container is sufficient. For a public page, verify that its offer and next action are understandable without invented social proof. For reading and collections, check the route into, through and back out of the material.

## Verify the implementation, not the intention

Observe the primary task at representative sizes and states with the available tools. Separate source inspection, rendered inspection, interaction and project checks: they support different claims. A screenshot cannot prove keyboard operation; a build cannot prove visual hierarchy. Review copy and icons in source even if rendering is unavailable.

Before delivering creation or redesign, perform the [final pattern pass](references/anti-slop.md#final-pass). During refinement apply its affected checks. Do not reduce expression, remove useful affordances, or rewrite protected text to reach a zero-pattern count.

When the CLI can cover the target, read [Executable inspection](references/inspection.md) and use an available runner. Resolve the installed executable, known checkout or package runner rather than assuming it is on PATH. Keep the project and server pairing explicit. Inspect evidence and incomplete coverage, correct authorized issues, and verify the same scope. An absent target is not a successful repair.

Inspect the captured result yourself. Exercise affected controls with keyboard and pointer/touch where applicable; measure relevant contrast against actual backgrounds and check content extremes and resizing. Run meaningful project checks. Native behavior requires platform tools, not a web scan. If a tool is unavailable, continue useful work and label the unobserved behavior instead of asserting a pass.

Finish when the requested change is complete and material in-scope issues are resolved, or identify the concrete remaining limit. Report the result, the important decisions, checks actually performed and unresolved risks. Do not claim an aesthetic score, full accessibility conformance, a measured speedup or a superiority result that the evidence does not establish. No automatic hooks, live visual editor or shader library is part of this skill.
