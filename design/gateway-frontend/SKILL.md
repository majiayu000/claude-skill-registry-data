---
name: gateway-frontend
description: Route frontend tasks to the right library skill. Detects React/Vue/CSS intent and returns specific skill file paths.
type: gateway
tier: core
domains: [frontend, ui, components]
trigger: "React, Vue, Angular, component, JSX, TSX, CSS, Tailwind, frontend, UI, browser, DOM, Next.js, anoa, visual, design check, screenshot, responsive"
---

## Purpose

You are the Frontend Gateway. Detect intent from the current task and return the exact library skill paths to load. Do NOT execute — only route.

## Intent Detection → Skill Routing

| Intent Keywords | Load Skill |
|---|---|
| `infinite loop`, `useEffect`, `hook loop`, `re-render loop` | `skills/library/frontend/debugging-react-hooks/SKILL.md` |
| `performance`, `render`, `memo`, `useMemo`, `useCallback`, `slow` | `skills/library/frontend/optimizing-react-performance/SKILL.md` |
| `state`, `zustand`, `redux`, `context api`, `global state` | `skills/library/frontend/state-management/SKILL.md` |
| `form`, `validation`, `zod`, `react-hook-form`, `yup` | `skills/library/frontend/form-handling/SKILL.md` |
| `routing`, `navigation`, `react-router`, `next/navigation` | `skills/library/frontend/client-side-routing/SKILL.md` |
| `animation`, `framer`, `transition`, `motion` | `skills/library/frontend/animations/SKILL.md` |
| `accessibility`, `a11y`, `aria`, `screen reader` | `skills/library/frontend/accessibility/SKILL.md` |
| `css`, `tailwind`, `styled-components`, `emotion` | `skills/library/frontend/styling-patterns/SKILL.md` |
| `ssr`, `ssg`, `next.js`, `hydration`, `server component` | `skills/library/frontend/ssr-patterns/SKILL.md` |
| `visual`, `design check`, `screenshot`, `responsive`, `contrast`, `browser validation`, `verify UI` | `skills/library/frontend/validating-visual-design/SKILL.md` |
| `browser`, `anoa`, `click`, `fill form`, `login flow`, `scrape`, `console errors`, `network requests` | `skills/core/anoa/SKILL.md` |
| `component`, `jsx`, `tsx`, `react` (general) | `skills/library/frontend/react-component-patterns/SKILL.md` |

## Output Format

```
GATEWAY_FRONTEND:
Domain: frontend
Skills to load:
  - [absolute/path/to/SKILL.md]

Instructions: Read the above skill files before proceeding with your task.
```
