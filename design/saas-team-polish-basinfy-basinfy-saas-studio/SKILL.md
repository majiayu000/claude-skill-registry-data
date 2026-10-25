---
name: saas-team-polish
description: "Orchestrate the polish team — performance-analyst, ui-motion-designer, frontend-engineer, qa-tester — Core Web Vitals, micro-interactions, loading states, and UI polish."
argument-hint: "[area or feature to polish] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-team-polish/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation`

Resolved above — use as-is; `--review` overrides `review_mode` for this run.

# Team Polish & Performance

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Orchestrate the specialized polish team to elevate software quality through Core Web Vitals optimization,
tasteful micro-animations, loading skeletons, accessible focus states, and responsive edge-case hardening.

**Argument check:** If no description is provided, output:
> "Usage: `/saas-team-polish [area or feature description] [--review full|lean|solo]` — Describe the area to polish (e.g. Dashboard load performance and skeletons, App shell responsive transitions, Data table hover states and keyboard navigation, Core Web Vitals pass)."

When this skill is invoked with a valid argument, orchestrate the team:

1. **Performance & Audit Phase**:
   - `performance-analyst`: Measure initial metrics (Lighthouse score, initial JS bundle size, Largest Contentful Paint, Cumulative Layout Shift)
   - Profile slow database queries or unmemoized React component re-renders

2. **Micro-Interactions & Loading States**:
   - `ui-motion-designer`: Design subtle, high-end motion (framer-motion or CSS transitions):
     - Route transitions (instant fade, no jarring flashes)
     - Skeleton loaders matching exact content layout
     - Button active/loading spinner states
     - Drawer slide-over and modal backdrop blur

3. **Frontend Implementation & Hardening**:
   - `frontend-engineer`:
     - Apply dynamic imports (`next/dynamic` / lazy loading) to heavy modules (charts, rich text editors)
     - Eliminate Cumulative Layout Shift (reserve image dimensions, avoid late-injected fonts)
     - Harden dark mode color contrast and focus rings (`focus-visible:ring-2`)

4. **Cross-Browser & Device Verification**:
   - `qa-tester`: Verify jank-free UI animations (fluid transitions without frame drops), mobile touch responsiveness, Safari rendering quirks, and reduced-motion fallback.

5. **Verdict**:
   - Output: **COMPLETE** — performance optimized and UI polished to enterprise standard.
