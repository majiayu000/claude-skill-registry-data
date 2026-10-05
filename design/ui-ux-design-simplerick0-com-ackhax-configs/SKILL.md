---
name: ui-ux-design
description: Design user interfaces and experiences for web applications without requiring design tools. Use for wireframing in text/ASCII, defining user flows, creating component hierarchies, establishing design systems, planning responsive layouts, and making accessibility decisions.
---

# UI/UX Design

Design user interfaces and experiences using structured thinking and text-based artifacts.

## Design Process

1. **User flows** - Map the journey before screens
2. **Information architecture** - Organize content and navigation
3. **Wireframes** - Layout and hierarchy (low fidelity)
4. **Component inventory** - Identify reusable pieces
5. **Interaction patterns** - Define behaviors
6. **Visual design** - Apply styling (or use existing system)

## User Flow Mapping

### Flow Notation
```
[Start] → (Action) → [Screen] → <Decision> → [End]

Example: Password Reset
[Login Page]
    → (Click "Forgot Password")
    → [Email Input]
        → (Submit email)
        → <Email exists?>
            Yes → [Check Email Message] → (Click link) → [Reset Form] → [Success]
            No  → [Error: Email not found]
```

### Flow Documentation
```markdown
## Flow: User Registration

### Happy Path
1. Landing Page → Click "Sign Up"
2. Registration Form → Enter email, password
3. Email Verification → Click link in email
4. Profile Setup → Add name, avatar (optional)
5. Dashboard → Onboarding tour

### Error States
- Invalid email format → Inline validation
- Email already exists → Link to login
- Weak password → Requirements tooltip
- Verification expired → Resend option
```

## Wireframing (Text-Based)

### ASCII Wireframe
```
┌─────────────────────────────────────┐
│  Logo          [Search...]   [Login]│
├─────────────────────────────────────┤
│                                     │
│  ┌─────────┐  ┌─────────┐          │
│  │  Card   │  │  Card   │          │
│  │  -----  │  │  -----  │          │
│  │  text   │  │  text   │          │
│  └─────────┘  └─────────┘          │
│                                     │
│  ┌─────────┐  ┌─────────┐          │
│  │  Card   │  │  Card   │          │
│  └─────────┘  └─────────┘          │
│                                     │
├─────────────────────────────────────┤
│  Footer links        © 2024         │
└─────────────────────────────────────┘
```

### Component Specification
```markdown
## Component: User Card

### Layout
- Avatar (48x48, left)
- Name (bold, truncate at 20 chars)
- Role (muted text, below name)
- Actions menu (right, icon button)

### States
- Default: White background
- Hover: Light gray background
- Selected: Blue border
- Loading: Skeleton placeholder

### Responsive
- Desktop: Horizontal layout
- Mobile: Stack avatar above text
```

## Information Architecture

### Navigation Structure
```
Primary Nav (always visible)
├── Dashboard
├── Projects
│   ├── Active
│   ├── Archived
│   └── [Create New]
├── Team
└── Settings

Secondary Nav (contextual)
└── Project Detail
    ├── Overview
    ├── Tasks
    ├── Files
    └── Settings
```

### Content Hierarchy
```
Page: Project Dashboard
├── H1: Project Name
├── Meta: Status, Owner, Due Date
├── Section: Quick Actions
│   └── [New Task] [Upload] [Invite]
├── Section: Recent Activity
│   └── Activity feed (5 items)
├── Section: Tasks Overview
│   └── Kanban or list view
└── Section: Team
    └── Member avatars + invite
```

## Component Design System

### Core Components
```markdown
## Buttons
- Primary: Main actions (1 per screen)
- Secondary: Supporting actions
- Ghost: Tertiary/cancel actions
- Destructive: Delete/remove (red)

Sizes: sm (32px), md (40px), lg (48px)
States: default, hover, active, disabled, loading

## Form Inputs
- Text input (single line)
- Textarea (multi-line)
- Select (dropdown)
- Checkbox / Radio
- Toggle switch

All inputs need: label, placeholder, error state, disabled state

## Feedback
- Toast: Temporary, auto-dismiss (success, error, info)
- Alert: Persistent, in-page (warning, error)
- Modal: Blocking, requires action
- Empty state: No data illustration + CTA
```

### Spacing Scale
```
4px  - xs (tight elements)
8px  - sm (related items)
16px - md (default spacing)
24px - lg (section gaps)
32px - xl (major sections)
48px - 2xl (page sections)
```

## Responsive Design

### Breakpoints
```
Mobile:  < 640px   (single column)
Tablet:  640-1024px (2 columns)
Desktop: > 1024px  (full layout)
```

### Responsive Patterns
```markdown
## Navigation
- Desktop: Horizontal top bar
- Mobile: Hamburger → slide-out drawer

## Data Tables
- Desktop: Full table with columns
- Mobile: Card-based list, key info only

## Forms
- Desktop: 2-column where logical
- Mobile: Single column, full width inputs

## Images/Media
- Desktop: Grid layout
- Mobile: Single column, swipeable carousel
```

## Accessibility Essentials

### Must-Have
- [ ] Color contrast 4.5:1 minimum (text)
- [ ] Focus indicators visible
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Error messages announced
- [ ] Keyboard navigation works
- [ ] Touch targets 44x44px minimum

### Semantic Structure
```html
<!-- Use proper hierarchy -->
<header> - Site header
<nav>    - Navigation
<main>   - Primary content
<aside>  - Secondary content
<footer> - Site footer

<!-- Headings in order -->
<h1> → <h2> → <h3> (no skipping)
```

### ARIA When Needed
```html
<!-- Only when HTML semantics insufficient -->
<button aria-expanded="false">Menu</button>
<div role="alert">Error message</div>
<input aria-describedby="help-text">
```

## Design Handoff Format

```markdown
## Screen: [Name]

### Purpose
One sentence explaining what user accomplishes here.

### Layout
[ASCII wireframe or description]

### Components Used
- Header (sticky)
- Card (with hover state)
- Button (primary)
- Empty state

### Interactions
- Click card → Navigate to detail
- Hover card → Show quick actions
- Click delete → Confirm modal

### Data Requirements
- User list (paginated, 20/page)
- User object: id, name, email, avatar, role

### Edge Cases
- Empty: Show illustration + "Add first user" CTA
- Loading: Skeleton cards
- Error: Inline error with retry
```
