---
name: operator-panel
description: Maintain or extend the local operator panel, its backend endpoints, settings UX, logs, action wiring, and operator summaries for the paper-research workspace. Use when working in app/operator_panel.py, app/ui/*, or the panel launch flow, especially when productizing advisory decision support into a low-noise operator surface. Never use for public product UI or live trading controls.
---

# Operator Panel

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — **Layers 9–10** operator observability and reporting; console is **not** the whole product—see **`docs/IMPLEMENTATION_GAP.md`** for vision vs code.
- **`AGENTS.md`** — local-first; **paper** defaults; panel must not imply **live** trading or **L7** bypass.

## Purpose

Use this skill to keep the local operator panel coherent, safe, and useful as the main daily control surface for the paper-research system — advancing **Layers 9–10** (operational health, reporting, transparency) of the vision in `docs/FINAL_SYSTEM_VISION.md` without breaking **`AGENTS.md`** safety boundaries.

The panel is local-only and sits on top of existing safe workflows. It should expose status, runs, experiments, portfolio state, settings, and logs without inventing new runtime behavior.

It should increasingly feel like an operator console, not a debug page:
- fewer visible cards
- more table-first summaries
- stronger information hierarchy
- short, product-grade labels
- advisory decision support surfaced without raw JSON noise
- decision-support trends shown as compact journal-derived tables, not new card clutter

## Use When

Use this skill when:
- editing `app/operator_panel.py`
- editing `app/ui/*`
- changing panel actions, summaries, settings, or run history visibility
- wiring existing scripts or research flows into the panel
- surfacing `decision_support` fields such as fusion bias, edge, validation, pipeline stage, or supervisor state
- surfacing decision-support distributions, drift, or stability over time from journaled runs
- surfacing governance mode, bounded autonomous review traces, or manual approval history without adding card clutter
- adding compact manual governance controls such as bounded action select, note capture, defer/reject reason capture, and shared governance history visibility
- adding low-noise governance history filters or operational health trend rows that remain fully passive
- surfacing external context provider health or supervisor watch summaries as compact overview/analytics rows
- extending the Experiments view with governance comparison rows while keeping the layout table-first
- surfacing passive learning-readiness or AI-readiness summaries without turning the panel into a debug surface
- wiring shadow fallback insights into the panel when no dedicated shadow file exists yet

## Do Not Use When

Do not use this skill for:
- public-facing product UI work
- live trading controls
- strategy math, scorer math, or risk-policy changes
- unrelated CSS-only cleanup with no operator impact

## Safety Contract

- Keep the panel bound to local operation only.
- Never expose secrets in the UI, API responses, or logs.
- Keep destructive actions explicit and visibly labeled.
- Keep locked or non-editable safety fields clearly locked.
- Reuse existing safe execution paths instead of creating hidden alternates.
- Keep advisory decision support descriptive only; it must not imply a trade was approved automatically.
- Governance UI may expose manual review actions or bounded autonomous review traces, but it must never imply runtime mode switching, trade approval, or live enablement.
- Governance controls must stay bounded: they may record review actions and notes, but they must never trigger runtime mode changes or trading behavior changes.
- Learning-readiness and AI-readiness panels must remain audit-oriented summaries only; they must not imply runtime learning or AI enablement.

## Primary Workflow

1. Read `AGENTS.md`.
2. Inspect the touched panel endpoint, UI component, and related script or backend flow.
3. Preserve baseline operator actions before extending experiment or research visibility.
4. Keep summaries compact and operator-readable.
5. Verify changed actions still call existing safe behavior.
6. Prefer merging related fields into one decision-oriented surface instead of adding more card clutter.
7. Keep the visible UI one-language-at-a-time and avoid raw internal naming.

## Required Checks

- System status, active job, and recent results remain coherent.
- Baseline, experiment, and scoped-trial views remain clearly labeled.
- Settings save is explicit and secrets remain hidden.
- Reset or other destructive actions remain isolated in a danger zone.
- Panel changes do not break existing scripts or CLI flows.
- Decision-support fields remain human-readable and do not leak internal-only naming into the primary UI.
- Decision analytics remain table-first and trend-oriented rather than card-heavy.
- Governance mode, recommended action, final action, and decision source remain visible through one shared audit model.
- Operator-entered note/reason fields remain compact, optional, and traceable through the same shared history used by autonomous governance.
- History filters or trend summaries must stay passive, low-noise, and must not imply hidden governance actions.
- Provider-stack visibility remains summary-level and must not introduce raw debug payloads into the main screen.
- Shadow fallback, learning-readiness, and AI-readiness surfaces must remain compact and operator-readable even when the dedicated shadow file is missing.

## Expected Output

- `Panel Surface:` what changed in backend or UI.
- `Operator Workflow:` what can now be done from the panel.
- `Decision Hierarchy:` how the panel became easier to read quickly.
- `Safety Check:` local-only, secret-safe, paper-only confirmation.
