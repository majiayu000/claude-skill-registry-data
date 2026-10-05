---
name: creo-design-implement
description: >
  Execute design fixes from review reports with high-quality code modifications.
  Implements responsive design corrections, accessibility improvements, component
  consistency fixes, and visual polish. Trigger keywords: design implement, fix design,
  implement review, responsive fix, accessibility fix.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Design Implementation

Systematically execute implementation roadmaps created by creo-design-review. Works in iterative cycles, implementing fixes and verifying them through live browser testing until all design issues are resolved.

## Commands

| Command | Description |
|---------|-------------|
| `/creo design-implement <report-path>` | Execute fixes from a specific review report |
| `/creo design-implement auto` | Find the latest review report and implement fixes |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `dev_server_url` (default: `http://localhost:3000`), `ui_framework`, `ui_rules`, `reports_path`
3. Load project extension if it exists at `.claude/skills/creo-design-implement/creo-design-implement-{project_id}.md`. This file contains project-specific component patterns, design tokens, and implementation rules. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, use defaults or ask user

### Mobile-First Approach (Critical)

Check layout at sizes 375px, 768px, 1440px, 1920px. Start with 375px and work upward. For each viewport, make changes until the design is consistent and polished before moving to the next.

### Mobile Layout Requirements (Mandatory)

#### Mobile (375px) Critical Issues
- **Text Overflow**: Headers and text must not exceed screen boundaries
- **Button Sizes**: Buttons must fit in viewport and be accessible for tapping
- **Horizontal Scrolling**: There should never be horizontal scrolling
- **Touch Targets**: Minimum 44px for all clickable elements
- **Text Readability**: Fonts must be readable (minimum 14px on mobile)

#### Typography Responsive Rules
- H1: 2rem on mobile, 3rem on desktop
- H2: 1.5rem on mobile, 2.25rem on desktop
- Body: 0.875rem on mobile, 1rem on desktop
- Buttons: 0.875rem on mobile, 1rem on desktop

#### Spacing Mobile Rules
- Container Padding: minimum 16px on each side on mobile
- Section Spacing: 32px between sections on mobile
- Component Spacing: 16px between components on mobile

### Fix Process

1. Open the page on 375px viewport
2. Take a screenshot and analyze all problems
3. Fix all overflow problems, font sizes, button issues
4. Check that there is no horizontal scrolling
5. Take a control screenshot; if problems remain, return to step 3
6. Add a check to prevent infinite loops (max 5 iterations per viewport)
7. Only after this, move to the next viewport

### Phase 1: Roadmap Processing

- Import implementation roadmap from the design review report
- Track all roadmap tasks
- Prioritize: Blockers, High-Priority, Medium-Priority, Enhancements

### Phase 2: Implementation Strategy

- **Responsive Issues**: Apply mobile-first approach using framework breakpoints
- **Component Issues**: Ensure consistency with established patterns

### Phase 3: Iterative Implementation

Execute fixes in priority order with continuous verification:

1. **Implement Task** -- Apply code changes for current priority item
2. **Test via Browser** -- Navigate to affected pages, test functionality
3. **Document Completion** -- Mark task as done
4. **Move to Next Task** -- Continue until all roadmap items complete

### Phase 4: Continuous Verification

- Test every implementation immediately via browser tools
- Stop work if server not available -- inform user immediately
- Navigate to affected pages
- Test across breakpoints (375px, 768px, 1440px, 1920px)
- Capture evidence screenshots
- Verify compliance before moving to next task

### Technical Approach

#### Accessibility Fixes
- Add proper ARIA labels and roles
- Ensure keyboard navigation
- Implement focus management
- Fix color contrast issues
- Add semantic HTML structure

#### Component Consistency
- Follow established design patterns
- Apply design tokens from style guide
- Maintain consistent spacing
- Use proper component variants

#### Code Quality Standards
- Use TypeScript interfaces properly
- Apply consistent naming conventions
- Minimize code duplication
- Comment complex implementations
- Follow existing project patterns

### Implementation Priorities

1. **User Impact First**: Fix issues affecting real user workflows
2. **Accessibility Critical**: WCAG violations get immediate attention
3. **Mobile Experience**: Ensure excellent mobile-first experience
4. **Visual Polish**: Apply consistent styling and spacing

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/design-principles.md` | Design principles checklist |
| `references/responsive-rules.md` | Responsive breakpoint rules |

## Quality Gates

- Every fix must be verified with a screenshot at the relevant breakpoint
- No horizontal scrolling on any viewport
- Touch targets must be at least 44px
- Text must never overflow its container on mobile
- Maximum 5 iterations per viewport to prevent infinite loops
- All blockers must be resolved before moving to high-priority items
- Server must be running before any work begins
