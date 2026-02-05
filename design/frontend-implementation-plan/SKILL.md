---
name: frontend-implementation-plan
description: Create comprehensive, production-ready frontend implementation plans for any UI screen or feature. Use this skill when documenting how to build UI components, establishing design systems, planning component architecture, or creating technical specifications for frontend development. Works across frameworks (React, Vue, Angular, Svelte, etc.) and focuses on clear structure, reusable patterns, and maintainability.
---

# Frontend Implementation Plan

This skill teaches how to create comprehensive implementation plans for frontend features, screens, and components. It provides a framework-agnostic approach to documenting UI architecture, design specifications, and development guidelines.

## When to Use This Skill

- Planning implementation for new UI screens or features
- Documenting existing implementations for team reference
- Creating technical specifications for frontend work
- Establishing design system documentation
- Teaching implementation patterns to developers
- Preparing handoff documentation between design and development

## Core Principles

### 1. Structure Over Specifics

A good implementation plan follows a clear hierarchy:

```
Implementation Plan
├── Overview (What & Why)
├── Architecture (Component Hierarchy)
├── Design Specifications (Visual Standards)
├── Component Details (Props, States, Behavior)
├── Data Flow (API Integration, State Management)
├── User Interactions (Navigation, Events)
├── Quality Assurance (Testing, Accessibility, Performance)
└── Migration & Integration (How to Implement)
```

### 2. Framework-Agnostic Thinking

Document **what** needs to be built, not just **how** in a specific framework:

**Good** ✅:
```
Stats Card Component
- Displays: Icon, label, numeric value, optional trend
- States: Default, loading, hover, error
- Variants: Clickable vs. static
- Responsiveness: Stacks vertically on mobile
```

**Too Specific** ❌:
```
Create a React component using useState and useQuery...
```

### 3. Design System First

Define the design system before component details:

```
Typography Scale
├── Page Titles: 40px, semibold, tight tracking
├── Section Headers: 32px, semibold
├── Body Text: 16px, regular, relaxed tracking
└── Captions: 13px, light

Color Palette
├── Primary: Brand color for actions
├── Text Hierarchy: Primary → Secondary → Tertiary
├── Semantic Colors: Success, Warning, Error, Info
└── Neutrals: Backgrounds, borders, disabled states

Spacing System
├── Base Unit: 4px or 8px
├── Component Padding: 24px (large), 16px (medium), 8px (small)
├── Section Gaps: 48px (large), 32px (medium), 16px (small)
└── Layout Grid: Column count, gutter width
```

### 4. Component Documentation Pattern

For each component, document:

1. **Purpose** - What it displays, when to use it
2. **Anatomy** - Visual breakdown of parts
3. **Props/Configuration** - Input parameters
4. **States** - Loading, empty, error, success, disabled
5. **Variants** - Size, style, behavior variations
6. **Accessibility** - ARIA labels, keyboard navigation
7. **Examples** - Visual or code examples

### 5. State Management Clarity

Explicitly document all UI states:

**Loading State**:
- What: Skeleton/spinner while data fetches
- When: API call in progress
- Pattern: Show placeholder matching final layout

**Empty State**:
- What: Friendly message when no data
- When: Valid but empty data response
- Pattern: Icon + message + call-to-action

**Error State**:
- What: Error message with retry option
- When: API failure or invalid data
- Pattern: Error icon + explanation + retry button

**Success State**:
- What: Populated with real data
- When: Data loaded successfully
- Pattern: Full component render

## Implementation Plan Structure

### Section 1: Overview

```markdown
## 1. Overview

### Purpose
[What this feature/screen does and why it exists]

### User Goals
- [Primary user objective]
- [Secondary user objective]

### Key Features
- [Feature 1]
- [Feature 2]

### Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]
```

### Section 2: Architecture

```markdown
## 2. Architecture

### Component Hierarchy
```
Screen/Feature
├── Layout Components
│   ├── Header
│   ├── Sidebar (optional)
│   └── Footer
├── Feature Components
│   ├── Main Content Area
│   ├── Filter/Search Bar
│   └── Data Display Grid
└── Shared Components
    ├── Loading Skeleton
    ├── Empty State
    └── Error Boundary
```

### File Structure
```
/components
  /feature-name
    /FeatureMain.tsx (or .vue, .svelte, etc.)
    /FeatureHeader.tsx
    /FeatureCard.tsx
  /shared
    /Button.tsx
    /Input.tsx
/types
  /feature-name.ts
/hooks (or composables, stores)
  /useFeatureData.ts
```
```

### Section 3: Design Specifications

```markdown
## 3. Design Specifications

### Visual Hierarchy
- Primary elements: [Description + specs]
- Secondary elements: [Description + specs]
- Tertiary elements: [Description + specs]

### Typography
| Element | Size | Weight | Color | Line Height |
|---------|------|--------|-------|-------------|
| Page Title | 40px | Bold | Primary | 1.2 |
| Section Header | 24px | Semibold | Primary | 1.4 |
| Body Text | 16px | Regular | Secondary | 1.6 |

### Colors
| Use Case | Color Code | Usage |
|----------|------------|-------|
| Primary Action | #FF6B00 | Buttons, links |
| Text Primary | #1A1A1A | Main content |
| Text Secondary | #666666 | Descriptions |
| Border | #E5E5E5 | Dividers, outlines |

### Spacing & Layout
- Container: [Max width, padding]
- Grid: [Columns, gap]
- Component padding: [Internal spacing]
- Section margins: [Between major sections]

### Responsive Breakpoints
- Mobile: 0-767px (1 column)
- Tablet: 768-1023px (2 columns)
- Desktop: 1024px+ (3-4 columns)
```

### Section 4: Component Specifications

For each major component:

```markdown
## Component: [Name]

### Purpose
[What it does, when it's used]

### Anatomy
```
┌─────────────────────────────┐
│ Icon    Title       Badge   │
│                             │
│ Supporting text             │
│ ━━━━━━━━━━ Progress: 75%   │
│                             │
│         [Action Button]     │
└─────────────────────────────┘
```

### Configuration/Props
```typescript
interface ComponentProps {
  title: string
  description?: string
  progress: number (0-100)
  status: 'active' | 'pending' | 'complete'
  onAction: () => void
}
```

### States
1. **Default**: Normal display
2. **Hover**: Subtle highlight, cursor pointer
3. **Loading**: Show skeleton
4. **Disabled**: Grayed out, no interaction
5. **Error**: Red border, error icon

### Variants
- **Size**: Small (compact), Medium (default), Large (featured)
- **Type**: Clickable (with onClick), Display-only

### Accessibility
- [ ] ARIA label on interactive elements
- [ ] Keyboard navigation (Tab, Enter, Space)
- [ ] Focus visible indicator
- [ ] Screen reader announcements

### Example
[Screenshot/mockup or code example]
```

### Section 5: Data Flow

```markdown
## 5. Data Flow

### Data Sources
- API: `GET /api/resource` → Returns `Resource[]`
- Local Storage: Cached user preferences
- URL Parameters: Filter/sort state

### State Management
```
Global State (Store/Context)
├── User session data
└── App-wide settings

Component State (Local)
├── Form inputs
├── UI toggles (modals, dropdowns)
└── Temporary filters

Server State (Query library)
├── Fetched data from API
├── Loading/error states
└── Cache management
```

### API Integration
```
Fetch Pattern:
1. Component mounts → Trigger API call
2. Show loading state
3. On success → Update UI with data
4. On error → Show error state with retry

Endpoints Needed:
- GET /api/items → List items
- POST /api/items → Create item
- PATCH /api/items/:id → Update item
- DELETE /api/items/:id → Remove item
```
```

### Section 6: User Interactions

```markdown
## 6. User Interactions

### Navigation Flow
```
Entry Point → Screen A → Action → Screen B
         ↓                    ↓
    Alternative Path    Alternative Outcome
```

### Interaction Map
| Element | Trigger | Action | Result |
|---------|---------|--------|--------|
| Filter dropdown | Click/Select | Update filtered view | Re-render list |
| Search input | Type (debounced) | Filter items | Update results |
| Action button | Click | Navigate/Submit | Go to detail page |
| Sort icon | Click | Toggle sort order | Reorder items |

### Keyboard Shortcuts (if applicable)
- `Tab`: Navigate between focusable elements
- `Enter/Space`: Activate focused button
- `Esc`: Close modal/dropdown
- `Ctrl+F`: Focus search (optional)
```

### Section 7: Quality Assurance

```markdown
## 7. Quality Assurance

### Testing Checklist
**Visual States**:
- [ ] Loading state displays correctly
- [ ] Empty state shows appropriate message
- [ ] Error state includes retry option
- [ ] Success state renders data properly

**Responsive Design**:
- [ ] Mobile (375px): Single column, readable
- [ ] Tablet (768px): Optimized layout
- [ ] Desktop (1024px+): Full feature set

**Interactions**:
- [ ] All buttons clickable and responsive
- [ ] Forms validate correctly
- [ ] Navigation works as expected
- [ ] Filters apply properly

### Accessibility Audit
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Focus indicators visible
- [ ] Color contrast ≥ 4.5:1 (WCAG AA)
- [ ] Keyboard navigation functional
- [ ] Screen reader compatible

### Performance Targets
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s
- [ ] No layout shifts (CLS < 0.1)
- [ ] Images optimized/lazy loaded
- [ ] Large lists virtualized (if >100 items)

### Browser Support
- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)
```

### Section 8: Implementation Guide

```markdown
## 8. Implementation Guide

### Phase 1: Foundation
1. Set up component files and structure
2. Define TypeScript types/interfaces
3. Implement design tokens (colors, spacing, typography)
4. Create base components (Button, Input, Card)

### Phase 2: Core Features
1. Build main screen layout
2. Implement data fetching/state management
3. Create feature-specific components
4. Wire up user interactions

### Phase 3: States & Edge Cases
1. Add loading skeletons
2. Implement empty states
3. Handle error scenarios
4. Add form validation

### Phase 4: Polish & Optimization
1. Add animations/transitions
2. Optimize performance
3. Test accessibility
4. Cross-browser testing

### Migration Notes (if updating existing code)
- **Breaking Changes**: [List any breaking changes]
- **Backwards Compatibility**: [How to maintain during transition]
- **Rollout Strategy**: [Phased or all-at-once deployment]
```

## Best Practices

### Documentation Quality

1. **Be Specific**: Use exact values (not "large padding" but "24px padding")
2. **Include Visuals**: Diagrams, mockups, or ASCII art for clarity
3. **Reference Real Examples**: Link to similar implementations
4. **Version Control**: Date the document, note which version of design/product

### Design System Documentation

1. **Single Source of Truth**: One place for all design tokens
2. **Live Examples**: Show components in action, not just specs
3. **Usage Guidelines**: When to use each component variant
4. **Don't Use**: Anti-patterns and what to avoid

### Component Documentation

1. **Atomic Design**: Document from smallest (atoms) to largest (pages)
2. **Props Over Implementation**: Focus on interface, not internals
3. **State Exhaustiveness**: Document every possible state
4. **Edge Cases**: List unusual scenarios and how to handle them

### Maintenance

1. **Keep It Updated**: Mark outdated sections clearly
2. **Link to Code**: Connect docs to actual implementation
3. **Review Process**: Docs updated whenever design/requirements change
4. **Feedback Loop**: Developers flag unclear documentation

## Common Patterns

### Grid/List Views

```markdown
### Grid Layout Pattern
- Container: Responsive grid
- Items: Uniform card components
- Empty Slots: Show placeholder or hide
- Loading: Skeleton items matching card layout
- Pagination: Load more button or infinite scroll
```

### Filter/Search Pattern

```markdown
### Filter System
- Filters: Dropdowns for categorical data
- Search: Text input with debounce (300ms)
- Sort: Dropdown or clickable headers
- Clear: Reset all filters button
- URL State: Persist filters in URL params
```

### Modal/Dialog Pattern

```markdown
### Modal Behavior
- Trigger: Button or link
- Backdrop: Dim page, close on click
- Focus Trap: Tab cycles within modal
- Close: X button, Esc key, backdrop click
- Scroll: Lock body scroll, scroll within modal
```

### Form Pattern

```markdown
### Form Structure
- Fields: Clear labels, helpful placeholders
- Validation: Real-time + on submit
- Errors: Inline messages, field highlighting
- Submit: Disabled during processing, success feedback
- Autosave: Optional, with save indicator
```

## Framework Examples

While this skill is framework-agnostic, here are translation hints:

### State Management
- **React**: useState, useReducer, Context, Redux, Zustand
- **Vue**: ref, reactive, provide/inject, Pinia
- **Angular**: Services, RxJS
- **Svelte**: Stores

### Data Fetching
- **React**: TanStack Query, SWR, Apollo
- **Vue**: VueQuery, composables
- **Angular**: HttpClient + Services
- **Svelte**: Stores + async/await

### Styling Approaches
- **Utility CSS**: Tailwind, UnoCSS
- **CSS-in-JS**: styled-components, Emotion
- **CSS Modules**: Scoped styles per component
- **Atomic CSS**: shadcn/ui, Radix, Headless UI

## Checklist for Complete Plans

Before finalizing an implementation plan, verify:

- [ ] **Overview**: Purpose and goals clearly stated
- [ ] **Architecture**: Component hierarchy diagram included
- [ ] **Design Specs**: Typography, colors, spacing defined
- [ ] **Components**: Each major component documented
- [ ] **Data Flow**: API endpoints and state management specified
- [ ] **Interactions**: User flows and navigation mapped
- [ ] **States**: Loading, empty, error, success all covered
- [ ] **Accessibility**: WCAG compliance checklist included
- [ ] **Testing**: Test scenarios and acceptance criteria listed
- [ ] **Performance**: Optimization targets defined
- [ ] **Responsive**: Mobile, tablet, desktop specs provided
- [ ] **Implementation**: Step-by-step guide or phases outlined

## Anti-Patterns to Avoid

❌ **Vague Specifications**: "Make it look nice" → ✅ "24px padding, #E5E5E5 border"

❌ **Framework Lock-in**: "Use React hooks" → ✅ "Manage component-level state"

❌ **Missing States**: Only documenting happy path → ✅ Document all states

❌ **No Accessibility**: Forgetting keyboard/screen readers → ✅ Include a11y checklist

❌ **Overly Technical**: Focus on code syntax → ✅ Focus on behavior and UX

❌ **Static Documentation**: No updates after creation → ✅ Living document

❌ **No Examples**: All text, no visuals → ✅ Include diagrams, mockups, code samples

## Additional Resources

### Documentation Tools
- **Diagrams**: Mermaid, Excalidraw, Figma
- **Component Catalogs**: Storybook, Histoire, Ladle
- **Design Systems**: Figma, Sketch, Adobe XD
- **API Docs**: OpenAPI/Swagger, GraphQL schema

### Inspiration Sources
- Component libraries' documentation (Material UI, Ant Design, shadcn/ui)
- Design system libraries (IBM Carbon, Atlassian Design System)
- Open source project READMEs
- Technical RFCs and ADRs (Architecture Decision Records)
