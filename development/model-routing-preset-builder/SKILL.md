---
name: model-routing-preset-builder
description: "Use when the operator explicitly wants to customise the native Codex model-capability-router policy."
---

# Native Routing Policy Builder

Read the installed `model-capability-router` as the single baseline. It
recommends GPT-6.1 Sol Medium for coordination, GPT-6 Astra Low with XHigh
reserved for exceptional reasoning, and GPT-6 Luna High/XHigh/Max. These are
policy recommendations; they do not establish or change the actual home
configuration. Preserve an explicit native effort selection, including Sol
Low; Medium is the shared recommendation, not a forced configuration change.
Do not revive retired schema-3 presets, mandatory coordinator topology or
resolver scripts.

1. Read the operator's requested changes and current native model/effort
   availability for each relevant channel. Preserve explicit selections.
2. Change only the requested profile choices or task boundaries. Keep task
   ownership, permissions, proof and compute selection separate.
3. For this operator, use the recommended palette above when the exact native
   channel supports it. Luna Max is available when justified, not an Ultra mode
   or a new paid route. Current GPT-6.1 capability, API pricing and benchmark
   evidence is in the router's `references/gpt61-sol-20260929.md`; historical GPT-6
   evidence remains in `references/gpt6-20260922.md`. Token prices and benchmark
   costs do not prove lower cost per completed Codex outcome.
4. Author changes in the normal TheAngrySkills source repository when requested
   as a durable shared policy. Do not create a competing Workbench install.
5. Validate identifiers and effort support against the current channel; check
   that the policy has no mandatory ladder, task creation or selected-main
   override, and adds no speculative cache retention, keepalive prompts or
   polling loops. Report unavailable options rather than inventing support.
6. Install published changes with `npx skills` from the normal source and verify
   canonical paths and lockfile provenance for each authorised host/profile.

Return the chosen profiles, actual source/version, validation evidence and
remaining gaps. Do not add topology machinery or modify native permissions.
