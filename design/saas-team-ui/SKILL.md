---
name: saas-team-ui
description: "Orchestrate the UI team through the complete frontend pipeline — ux-designer, design-system-director, frontend-engineer, qa-tester — UX spec, design tokens, responsive components, and visual testing."
argument-hint: "[UI feature description] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-team-ui/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation`

Resolved above — use as-is; `--review` overrides `review_mode` for this run.

# Team UI Pipeline

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Orchestrate the UI design and frontend engineering team from user experience specification
through design token alignment, responsive component development, and visual validation.

**Argument check:** If no description is provided, output:
> "Usage: `/saas-team-ui [UI feature description] [--review full|lean|solo]` — Describe the screen, view, or UI pattern you want to build (e.g. Analytics dashboard with interactive charts, Multi-step onboarding modal, Team member permissions table, App shell and global navigation)."

When this skill is invoked with a valid argument, orchestrate the team:

1. **UX Specification**:
   - `ux-designer`: Author UX specification (`design/ux/[feature]-spec.md`)
   - Specify layout zones, user interaction map, edge cases (empty states, loading, errors), and WCAG 2.2 accessibility checklist

2. **Design Tokens & Visual Design**:
   - `design-system-director`: Align component with `design/ui/design-tokens.md`
   - Specify typography classes, semantic color tokens, padding/gap tokens, and responsive breakpoints

3. **Frontend Implementation**:
   - `frontend-engineer`: Build accessible React/Vue components (using Tailwind CSS, Radix UI / shadcn/ui primitives):
     - Ensure semantic HTML (`<nav>`, `<main>`, `<dialog>`, `<button>`)
     - Implement keyboard accessibility (Tab order, Enter/Space, Escape to close)
     - Bind component state to backend API queries/mutations

4. **Visual & Accessibility Testing**:
   - `qa-tester`: Verify WCAG contrast ratios (minimum 4.5:1), responsive layout from 320px to 2560px, and keyboard operability.

5. **Verdict**:
   - Output: **COMPLETE** — UI feature specified, styled, implemented, and validated.
