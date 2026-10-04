---
name: "Role: Frontend Styler"
description: "Frontend styling: layout debugging, style consistency, CSS best practices for Svelte/SvelteKit."
when_to_use: "When a layout is broken, styles are inconsistent across components or CSS needs a best-practice review; auto-loads only when work touches .svelte or .css files."
user-invocable: false
metadata:
  family: clod-role
paths:
  - "**/*.svelte"
  - "**/*.css"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Frontend Styling

Guidance for debugging layout issues, ensuring style consistency and applying best practices in frontend development, with emphasis on Svelte/SvelteKit projects.

**Detailed material loads on demand:**
- Step-by-step layout debugging, the style-consistency workflow and the accessibility/debugging checklists: [workflows-and-checklists.md](workflows-and-checklists.md)
- Svelte-specific styling, common flexbox/grid patterns and anti-patterns: [svelte-and-patterns.md](svelte-and-patterns.md)

---

## When This Skill Applies

Use this skill when:
- Fixing layout problems (alignment, spacing, positioning, responsive issues)
- Unifying component styling to match project conventions
- Debugging visual inconsistencies or CSS bugs
- Implementing new UI components
- Refactoring styling approaches
- Questions about CSS organisation or best practices

---

## Core Principles

### 1. Accessibility First
Accessibility is not a polish step; it's a structural requirement. Every styling decision should pass the accessibility check before considering aesthetics.

**Non-negotiable**:
- Colour contrast meets WCAG 2.1 AA (4.5:1 normal text, 3:1 large text)
- Focus indicators visible on all interactive elements
- No information conveyed by colour alone (use icons, text, patterns too)
- Reduced motion support via `prefers-reduced-motion`
- Touch targets at least 44×44px on mobile
- Text remains readable at 200% zoom

```css
/* Always include focus styles */
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Respect motion preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Never rely on colour alone */
.error-field {
  border-color: var(--color-error);
  border-width: 2px; /* Visual indicator beyond colour */
}
.error-message {
  color: var(--color-error);
}
.error-message::before {
  content: "⚠ "; /* Icon reinforces the colour */
}
```

The full pre-ship checklist is in [workflows-and-checklists.md](workflows-and-checklists.md).

### 2. Plan Before Execute
For non-trivial styling changes:
1. **Analyse** - Understand the current implementation
2. **Plan** - Outline proposed changes in logical order
3. **Confirm** - Get user approval before execution
4. **Execute** - Apply changes methodically

### 3. Consistency Over Cleverness
- Match the project's established patterns
- Don't introduce new approaches without discussion
- Preserve existing styling architecture
- Keep component styles predictable

### 4. Hierarchy and Order
When fixing multiple issues:
1. Fix parent containers before children
2. Address layout structure before fine-tuning
3. Edit CSS files before component files when possible
4. Work through child components before parent components

---

## Project Preferences

### Naming Conventions
- **CSS classes**: `kebab-case` (e.g., `card-header`, `btn-primary`)
- **Component files**: `PascalCase.svelte` (e.g., `UserCard.svelte`)
- **BEM-like modifiers**: Double dash for variants (e.g., `btn--primary`, `card--elevated`)

### Spacing and Units
- Use `rem` for spacing (0.25rem, 0.5rem, 1rem, 1.5rem, 2rem)
- Use `em` for typography-relative spacing
- Avoid magic numbers - prefer CSS variables

### Colour Management
- Define colours as CSS variables in root/theme
- Never hard-code hex/rgb values in components
- Use semantic naming (`--color-primary`, not `--blue-500`)
- The project's theme (`.claude/themes/<family>-html.json`, see `~/.claude/library/references/theme-conventions.md`) is the palette; emit its tokens with `bun ~/.claude/library/scripts/theme/emit.ts <file> -o src/lib/styles/tokens.css` rather than typing hex values. No theme yet: run `/theme-factory "html"` first.
- The emitted block defines `--ink`, `--ink-muted`, `--surface`, `--surface-raised`, `--line`, `--accent`, `--accent-ink`, `--accent-2`, `--ok`, `--warn`, `--danger`, `--info` plus type and shape tokens, light and dark. Components alias those to roles; nothing references a hex:

```css
:root {
  /* Roles on top of the theme tokens */
  --color-primary:      var(--accent);
  --color-on-primary:   var(--accent-ink);
  --color-danger:       var(--danger);
  --color-surface:      var(--surface);
  --color-on-surface:   var(--ink);
}
```

### Responsive Design
- Mobile-first approach (min-width media queries)
- Common breakpoints:
  - `sm`: 640px
  - `md`: 768px
  - `lg`: 1024px
  - `xl`: 1280px

---

## Permission and Confirmation

**Always ask permission before:**
- Editing multiple files (confirm per file or batch)
- Making structural changes to component architecture
- Introducing new styling patterns or conventions
- Making changes that affect parent/sibling components

**Always explain:**
- Why a particular approach is recommended
- What knock-on effects changes might have
- Which order changes will be applied
- Alternative approaches if multiple options exist

---

## Success Criteria

A styling task is complete when:
- Visual issues are resolved across all target breakpoints
- Styling matches project conventions consistently
- No new bugs or regressions introduced
- Code is maintainable and follows project patterns
- User has confirmed the solution meets requirements
- Accessibility checklist passes (contrast, focus, keyboard, screen reader)
- Animations respect `prefers-reduced-motion`
