---
name: vkc-wizardkit
description: Build step-based wizard UIs (step UI, fixed bottom CTA with safe-area, localStorage draft save, runtime validation, submit event logging). Use for visa assessment, doc generation, admin queue inputs.
metadata:
  short-description: Wizard UI kit workflow
---

# VKC WizardKit

## When to use

- You need a multi-step form (visa precheck, document generation, lead intake, admin queue)

## Required UX contract

- Step indicator (current step / total)
- Fixed bottom CTA (primary action) with safe-area padding
- Draft persistence via `localStorage` (recover after refresh)
- Runtime validation before advancing or submitting
- Submission event logging (via `POST /api/events`)

## Implementation shape (recommended)

- UI: a template-level wrapper under `src/components/templates/**` (Wizard layout)
- Logic: a hook under `src/lib/hooks/**` (draft storage, step nav)
- API: submit via `src/repo/<domain>/**` + `src/app/api/**`

## Reference spec

- `.codex/skills/vkc-wizardkit/references/wizard-ui-spec.md`

