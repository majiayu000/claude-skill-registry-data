---
name: frontend
description: Design and build frontend UI -- HTML/CSS/JS, React, responsive.
version: 0.1.0
execution-mode: side_effecting
argument-hint: <task description>
category: dev-tools
status: candidate
---
# Frontend Design Skill

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=frontend] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

Build, refine, or scaffold frontend interfaces. Works across vanilla HTML/CSS/JS, React, and other frameworks detected in the project.

## Usage

```bash
[frontend] "Add a dark mode toggle to the dashboard"
[frontend] "Build a responsive card grid for agent status"
[frontend] "Scaffold a React component for the briefing viewer"
[frontend] "Review and improve the landing page layout"
```

## Task

$ARGUMENTS

## Execution

### 1. Detect project context
- Check for `package.json`, `tsconfig.json`, `vite.config.*`, `next.config.*` to identify framework
- Check for existing component patterns (naming, file structure, styling approach)
- Check for design tokens / CSS variables already in use
- If your organization project detected (`hummbl` in path), load brand tokens from `[brand-guidelines]` skill

### 2. Design approach
Before writing code, outline:
- **Layout**: How the UI is structured (grid, flex, sections)
- **Components**: What pieces are needed (new vs reuse existing)
- **Responsiveness**: Mobile-first breakpoints
- **Accessibility**: ARIA labels, keyboard nav, color contrast
- **Interactions**: Hover states, transitions, loading states

### 3. Implementation patterns

**Vanilla HTML/CSS/JS** (your site pattern):
- Single-file pages with `<style>` block using CSS custom properties
- CSS Grid/Flexbox for layout
- Vanilla JS for interactivity (no build step)
- CSP-compliant inline scripts

**React/Next.js**:
- Functional components with hooks
- CSS Modules, Tailwind, or styled-components (match existing project)
- TypeScript if `tsconfig.json` exists
- Follow existing component directory structure

### 4. Quality checks
- Validate HTML structure (semantic elements, heading hierarchy)
- Check color contrast (WCAG AA minimum)
- Test responsive behavior at 320px, 768px, 1024px, 1440px
- Verify no hardcoded colors -- use CSS variables or design tokens

## Design Principles

1. **Content-first**: Start with content hierarchy, then style
2. **Progressive enhancement**: Works without JS, enhanced with it
3. **Performance**: No unnecessary libraries, lazy-load images, minimize paint
4. **Consistency**: Match existing patterns in the project before introducing new ones
5. **Accessibility**: Keyboard navigable, screen reader friendly, sufficient contrast

## your organization Design Tokens

When working on your organization projects, use these tokens:

```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #141414;
  --bg-elevated: #1a1a1a;
  --text-primary: #e8e8e8;
  --text-secondary: #a0a0a0;
  --text-tertiary: #666;
  --accent-cyan: #00ff88;
  --accent-warm: #ff6b35;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-prominent: rgba(0, 255, 136, 0.3);
  --font-mono: "JetBrains Mono", "SF Mono", Consolas, monospace;
  --font-serif: "Crimson Pro", Georgia, serif;
}
```

## Figma Integration

If a Figma URL is provided, use the Figma MCP tools:
1. `get_design_context` with fileKey and nodeId extracted from URL
2. Adapt the returned code to the project's stack and conventions
3. Map Figma tokens to existing CSS variables

## Constraints

- Do NOT add new CSS frameworks without asking (e.g., don't add Tailwind to a vanilla project)
- Do NOT introduce build steps to projects that don't have them
- Match the existing code style (indentation, naming, file organization)
- Prefer CSS custom properties over hardcoded values
- All interactive elements must be keyboard accessible

## External References (Supplement)

- `ulpi-io/skills@frontend-design-ui-ux` — UI execution and review phrasing for frontend tasks.
- `ancoleman/ai-design-components@implementing-api-patterns` — concrete API-first frontend handoff patterns for UI/data boundary decisions.

## Skill Chains

### Mandatory

None — code generation; local file writes only (HTML/CSS/JS/React source files).

### Advisory

- `[brand-guidelines]` — load your organization design tokens for your organization projects before styling
- `[test-run]` — verify frontend changes don't break existing tests after implementation

## Authority

- **T1 (TRUSTED)**: May run (design, scaffold, build, refine frontend UI)
- **T2 (Active/High)**: May run (design, scaffold, build, refine frontend UI)
- **T3 (Medium)**: May run (design, scaffold, build, refine frontend UI)
- **T4 (Probationary)**: May run with operator notification (code generation — local file writes)
- **Operator**: Override any restriction
