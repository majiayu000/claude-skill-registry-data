---
name: project-design
description: Design and implement interfaces in this Next.js starter. Use when adding or redesigning pages, features, navigation, forms, tables, dashboards, or interaction flows, and when reviewing visual hierarchy or usability. Follow the existing design system and connect the interface to real behavior. Backend-only changes do not need this skill.
---

# Project Design

Build interfaces around the work someone needs to do. Give the main task a clear hierarchy, make progress and recovery understandable, and carry the design through to working components.

## Establish the scope

Read `AGENTS.md`, the affected routes and components, `components.json`, `app/globals.css`, and any existing design specification. Inspect the running interface when available. Check the working tree and preserve unrelated work.

Use the request and project to identify the user, task, primary action, data, and constraints. Ask only for missing information that materially changes the implementation; otherwise state the useful assumption and proceed. A small component change needs a small plan.

Match the requested depth:

| Request | Work |
| --- | --- |
| Build a feature or screen | Design the flow and implement the behavior within the requested scope. |
| Redesign | Recompose the affected interface while preserving its data and behavior unless the request changes them. |
| Restyle | Adjust the visual system while keeping the layout and behavior. |
| Polish | Fix concrete hierarchy, spacing, state, and interaction defects in place. |
| Audit or review | Report actionable findings with source locations and browser evidence; leave files unchanged unless fixes were requested. |

For a redesign, read [references/redesign-and-review.md](references/redesign-and-review.md) before editing. Do not turn a button fix into a screen redesign or an audit into an implementation.

## Choose the layout from the task

For substantial work, read [references/interface-direction.md](references/interface-direction.md). Briefly name the primary working surface, the most important action, the states involved, and the files likely to change. Continue within the authorized scope without a separate design-approval ritual.

In this starter, the transaction list, classification decisions, and workflow progress are useful product material. A screen for working with them should expose those objects directly. Choose tables for comparing rows, a list and detail view for investigating one item, and inline disclosure for supporting information. Use a chart when it answers a quantitative question that the underlying table makes difficult.

Keep the current shell, fonts, semantic tokens, component vocabulary, and spacing rhythm unless the requested change calls for a new visual direction. For a new direction, compare a few distinct approaches when useful, choose one from the task and content, and implement it consistently. New screens should still belong to the same product.

## Implement the complete interaction

Read [references/states-and-data.md](references/states-and-data.md) for forms, asynchronous work, tables, or data visualizations. Build a working vertical slice early: input, validation, action, actual response, and recovery. Specify applicable empty, loading, error, review, and completion states alongside the populated view.

Use the existing integration skills as needed:

| Concern | Guidance |
| --- | --- |
| Component selection, variants, forms, overlays | `skills/shadcn/SKILL.md`; inspect installed primitives before adding any. Use Bun equivalents for its CLI examples. |
| New reusable component contracts | `skills/building-components/SKILL.md`. |
| Routes, server/client boundaries, data access | `skills/next-best-practices/SKILL.md`, `skills/nextjs/SKILL.md`, and the relevant installed docs in `node_modules/next/dist/docs/`. |
| React composition and performance | `skills/vercel-composition-patterns/SKILL.md`, `skills/vercel-react-best-practices/SKILL.md`. |
| AI interface components | `skills/ai-elements/SKILL.md` when the feature needs them. |
| Classification or durable progress | The relevant TypeSafe and Workflow skills and installed package docs. |
| Browser and end-to-end verification | `skills/web-design-guidelines/SKILL.md`, `skills/verification/SKILL.md`. |

Project constraints take precedence over generic examples:

- Use Node.js 24 and Bun for dependency and script commands. Preserve the pinned stack.
- Use existing semantic color and typography tokens. Add a needed token in the existing theme rather than creating a parallel theme or stylesheet system.
- Application and transaction components reject arbitrary Tailwind values and inline styles. Prefer component variants and the project's utility scale.
- Let shadcn primitives own focus management, keyboard interaction, and overlays. Preserve accessible names, visible focus, and reduced-motion behavior.
- Keep provider credentials server-side. Preserve the existing demo access-token flow without logging or persisting its value. Keep example data synthetic and label synthetic previews; they must never claim to be live results.
- Render queued, rules, Jev, classified, review, and failed states from actual workflow events. Account for replayed events and preserve uncertain decisions.
- Keep existing access controls, input limits, and retention boundaries. New storage or outbound behavior requires the authorization and retention model described in `AGENTS.md`.

## Verify the result

For changed behavior, update the relevant tests and run `bun run test`, `bun run lint`, and `bun run typecheck`. Run `bun run lint:design` for UI changes, `bun run build` for the changes required by `AGENTS.md`, and `bun run build:eve` if the agent changed.

Review the actual affected routes through their dev server at narrow and wide viewports. Check keyboard operation, the primary task, relevant states, and error recovery. For classification changes, use synthetic CSV import and selection, actual row progress, uncertain decisions, and stream-failure recovery. A static preview does not prove that a request or workflow succeeded.

For substantial visual work, use the review procedure in [references/redesign-and-review.md](references/redesign-and-review.md). Fix concrete regressions and verify again when those fixes warrant it. Report what changed, what was tested, and any unverified behavior. If credentials are missing, name only the required variable and finish the checks that can run without it.
