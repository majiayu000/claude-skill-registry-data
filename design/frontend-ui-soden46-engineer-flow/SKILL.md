---
name: frontend-ui
description: Build and review user interfaces using framework-agnostic usability, accessibility, state, and rendering principles.
metadata:
  internal: true
---

# frontend-ui

Use this skill for UI components, forms, layouts, interaction behavior, responsive design, and accessibility.

## Principles

Keep UI state explicit.

Separate presentation from unrelated business or persistence logic where practical.

Forms should provide:

- clear labels
- validation feedback
- useful error states
- loading/submission state
- accessible interaction

Consider:

- keyboard usage
- focus management
- semantic structure
- screen readers
- responsive layouts
- empty states
- loading states
- error states

Avoid unnecessary rendering or state duplication.

Preserve user input where practical when recoverable errors occur.

Use the project's existing design system and component conventions.

### Browser-Driven UI Inspection

When the task involves visual UI work and a browser-capable tool is available, inspect the real rendered interface instead of relying only on source files.

Useful browser-capable tools may include:

- host browser tools
- browser MCP tools
- Playwright or Playwright MCP
- agent-browser
- compatible external browser or UI inspection skills

Do not hardcode a single browser tool as mandatory. Use the best available tool for the host and project.

If no browser-capable tool or runnable app is available, state that limitation and avoid claiming visual or runtime parity.

Inspect relevant:

- rendered layout and visual hierarchy
- DOM structure
- accessibility tree or semantic structure
- typography
- spacing
- color usage
- component density
- navigation structure
- loading, empty, error, hover, focus, and active states
- console errors
- network or asset failures when visible in the browser

### Reference-Driven UI Reconstruction

Use this workflow when the user provides a reference website, screenshot, design, or existing UI to emulate.

1. Open or inspect the reference with the best available browser-capable tool.
2. Capture the interface structure, layout, spacing rhythm, typography scale, color tokens, component patterns, navigation, responsive behavior, and interaction states.
3. Separate the reusable visual language from site-specific content, logos, proprietary media, brand assets, and exact copy.
4. Inspect the target project and its current design system, components, routes, backend contracts, and frontend stack.
5. Map the reference design into the target project's existing conventions instead of blindly cloning markup or adding an unrelated design system.
6. Implement the smallest coherent UI change that satisfies the task.
7. Re-open the local app and compare against the intended visual direction.
8. Iterate until the implemented UI is visually coherent across the required states and viewports.

Reference-driven reconstruction is not blind copying. Preserve user-provided or project-owned branding and content, and do not copy third-party logos, proprietary images, or exact text unless the user has supplied the asset or explicitly authorized that usage.

### Screenshot DOM Accessibility Tree

Use screenshots for visual evidence when layout, spacing, color, or responsive behavior matters.

Use DOM or accessibility-tree inspection when structure, semantics, labels, focus order, or assistive behavior matters.

Prefer the smallest useful evidence:

- full-page screenshots for overall composition
- element screenshots for component-level fixes
- DOM snapshots for structure
- accessibility snapshots for labels, roles, and focus behavior
- console logs for runtime UI errors

### Responsive Visual Verification

For responsive UI work, verify behavior at the viewports that matter for the product or task.

Check:

- text wrapping and overflow
- horizontal scrolling
- clipped controls
- touch target size
- sticky or fixed elements
- modal and dropdown fit
- table/list density
- navigation collapse behavior
- focus visibility
- loading, empty, and error states

Do not claim mobile, desktop, browser, screenshot, or visual parity unless it was actually inspected or tested.

### Implementation Boundaries

Detect the current frontend stack and component system from project evidence.

Preserve existing backend contracts, routes, forms, API payloads, authorization behavior, and state ownership.

Do not introduce a new UI framework, browser automation dependency, or visual testing stack unless it solves a clear project need and matches existing tooling or the user's request.

When durable regression coverage is needed, hand off stable browser-observed behavior to the `testing` capability or a compatible external browser/E2E testing skill.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.