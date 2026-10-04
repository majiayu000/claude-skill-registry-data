---
name: codex-slides-structured-intake
description: Collect and persist structured presentation requirements for Codex Slides, including scenario choice, audience, page count, language, format, research mode, visual direction, source-file roles, and clarification checkpoints. Use when a new deck request is ambiguous or scenario-led.
---

# Codex Slides Structured Intake

The Codex Slides Browser owns the canonical intake form. Structured intake must
produce one durable project and one shared clarification state, not a separate
chat-only questionnaire.

## Flow

1. Call `open_codex_slides` without a project id and follow its
   `browserHandoff` to the home/create workspace.
2. When a workflow preset fits, call `list_scenarios`, then open the selected
   scenario deep link. Use product-owned defaults and source slots.
3. Submit the user's topic and available files in the Browser. Assign every
   uploaded file its scenario role; do not flatten datasets, source decks,
   brand assets, and visual references into one undifferentiated list.
4. Let the product create the durable project before clarification. Keep the
   clarification checkpoint visible and persist answers in project workflow
   state.
5. Ask only questions that materially change the result: audience, purpose,
   page count, language, aspect, research depth, evidence constraints, and
   visual direction. Use recommendations already present in the form.
6. Continue through outline and inspiration checkpoints in the same Browser
   project. Do not call the unattended `create_deck` path unless the user asked
   for a headless run.

If Browser submission is unavailable, use `start_project` as the deterministic
fallback, immediately follow its clarification handoff, and keep later choices
attached to that same project id. `get_onboarding_questions` may help formulate
the intake, but its output is not a second source of truth.

When a durable outline or render job is useful, call `start_project_run`, keep
its `runId`, and use `wait_project_run` or `cancel_project_run` without closing
the Browser workspace.
