---
name: ui-business-apps
description: "Applies owner priorities and original design skills to working dashboards, CRM, ERP and admin screens."
---

# Business Application UI Policy

Use this owner profile for working product screens. Preserve the original author
trees unchanged; this profile holds personal constraints and selection guidance,
not an extracted author design workflow.

## Author Selection

Select one primary provider and at most one support when it resolves a distinct
need. Read the provider's complete `SKILL.md` and required references from the
current-session catalog. Reviewed files and native plugins keep their own update
ownership; disk installation alone does not establish exposure.

| Task | Original provider |
| --- | --- |
| Dense working screens, application identity, design-system consistency | `interface.interface-design` |
| Specific UI pattern, chart, typography or stack research | `uipro.ui-ux-pro-max` |
| UX shape, critique, audit, polish or hardening | `impeccable.impeccable`, with the matching author reference and Operate mode |
| Analytics and visualization are the main deliverable | `build-web-data-visualization:data-visualization` |
| Frontend implementation | `build-web-apps:frontend-app-builder` |
| Existing shadcn composition or React/Next.js performance | The corresponding exposed `build-web-apps:shadcn` or `build-web-apps:react-best-practices` leaf |

Use native Product Design, Figma or Superdesign for an explicitly requested
workflow they support, including their prerequisites. Missing providers remain
unavailable until reviewed dependency or official plugin setup and host exposure
are established; do not replace them with a Bible summary.

Use UI UX Pro Max for targeted UX, chart or stack lookup against the actual
business brief. A generic product-category result or automatic CRM design-system
output is not an authority for a working application; keep the verified task,
table and data requirements as the source of truth.

## Owner Priorities

- Start from the actual role, task and product objects. Preserve an existing
  design system when it fits the requested scope. Do not invent screens,
  workflow steps, business metrics or access rights for visual completeness.
- Make relevant list, detail and edit tasks usable at the intended density.
  Include filters, saved views, bulk actions or drill-down only when the product
  requires them; do not add a generic dashboard card grid by default.
- Treat form validation, dirty state, save progress, failure and recovery as
  product behavior. Make permissions and unavailable actions understandable
  without claiming client UI enforces authorization.
- Keep KPI labels, units, periods, chart encoding and refresh/stale state tied
  to real data contracts. Label fixtures as demonstration data. Support the
  loading, empty and error states relevant to the actual task.
- Preserve readable density, keyboard and focus behavior, accessible semantics
  and responsive usability on the supported devices. Decoration must support
  scanning and task completion.

Use `templates/business-ui-brief.md` from the repository or installed Bible
`current/` snapshot when the brief needs durable product constraints; omit
irrelevant sections and record unknowns.
An existing screen or design system can provide visual direction without
generated images or a fresh approval step for every change.

## Scope And Evidence

Installing author files does not run launchers, hooks, setup or authentication.
Follow original runtime procedures only within the authorized UI task and host
execution boundary. Selecting a native design workflow does not authorize
uploading private customer data, creating external connections or publishing.

For Bible-managed Impeccable invocations, set `IMPECCABLE_NO_UPDATE_CHECK=1`.
Use `be skills check` and `be skills update` for reviewed author updates; do not
run `npx impeccable update` over a Bible-managed tree. Resolve author command
path placeholders, including Pro Max's `CLAUDE_PLUGIN_ROOT`, against the verified
provider installation returned by the route. Pro Max `--persist` or `--force`
applies only when the requested task calls for writing those project artifacts.

Choose `ui-qa` evidence for the requested slice: rendered supported layouts and
the affected list/form/navigation/data states. Preserve artifact pointers,
actual checks and unresolved gaps. Screenshots prove appearance; interaction
and data checks establish the relevant behavior. Reuse this route on same-task
follow-ups instead of rerouting or reloading unchanged instructions.
