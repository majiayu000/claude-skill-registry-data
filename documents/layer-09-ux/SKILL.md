---
name: LAYER_09_UX
description: Expert knowledge for UX Layer modeling in Documentation Robotics
triggers:
  [
    "UX",
    "user interface",
    "UI",
    "view",
    "component",
    "screen",
    "form",
    "user experience",
    "state machine",
  ]
version: 0.7.0
---

# UX Layer Skill

**Layer Number:** 09
**Specification:** Metadata Model Spec v0.7.0
**Purpose:** Defines user experience using Three-Tier Architecture, specifying views, components, state machines, and interactions.

---

## Layer Overview

The UX Layer captures **user experience design**:

- **VIEWS** - Routable screens/pages with layouts
- **COMPONENTS** - UI components (forms, tables, charts, cards)
- **STATE MACHINES** - Experience states and transitions
- **ACTIONS** - Interactive elements (buttons, links, voice commands)
- **VALIDATION** - Client-side validation rules
- **LAYOUTS** - Layout configurations (grid, flex, etc.)

This layer uses **Three-Tier Architecture** (v0.5.0+):

1. **Library Tier** - Reusable design system components
2. **Application Tier** - Application-wide configuration
3. **Experience Tier** - Experience-specific views and flows

**Central Entity:** The **View** (routable screen) is the core modeling unit.

---

## Entity Types

### Three-Tier Architecture (26 entities)

**Library Tier:**

- **UXLibrary** - Container for library components
- **LibraryComponent** - Reusable component (form-field, table, chart, card)
- **LibrarySubView** - Reusable component groupings
- **StatePattern** - Reusable state machine patterns
- **ActionPattern** - Reusable action definitions

**Application Tier:**

- **UXApplication** - Application-wide UX configuration

**Experience Tier:**

- **UXSpec** - Container for experience specification
- **View** - Routable screen/page
- **SubView** - Component grouping within view
- **ComponentInstance** - Instance of library component
- **ActionComponent** - Interactive element
- **ExperienceState** - State in state machine
- **StateAction** - Action during state lifecycle
- **StateTransition** - Transition between states
- **ValidationRule** - Client-side validation

---

## When to Use This Skill

Activate when the user:

- Mentions "UX", "UI", "view", "screen", "component", "form"
- Wants to define user interfaces or user experiences
- Asks about state machines, transitions, or user flows
- Needs to model screens, forms, or interactive elements
- Wants to link UX to navigation, APIs, or business processes

---

## Cross-Layer Relationships

**Outgoing (UX → Other Layers):**

- `motivation.*` → Motivation Layer (UX supports goals)
- `business.*` → Business Layer (UX realizes business processes)
- `api.*` → API Layer (API calls from components)
- `data.*` → Data Model Layer (form validation rules)
- `navigation.*` → Navigation Layer (routing to views)

**Incoming (Other Layers → UX):**

- Navigation Layer → UX (routes point to views)
- Business Layer → UX (business processes trigger UX flows)

---

## Design Best Practices

1. **Reusability** - Use library components for consistency
2. **State machines** - Model complex flows with states/transitions
3. **Validation** - Add client-side validation rules
4. **Accessibility** - Consider accessibility requirements
5. **Responsive** - Design for multiple screen sizes
6. **Performance** - Set performance targets (load time, interaction latency)
7. **Error handling** - Define error states and messages

---

## Common Commands

```bash
# Add view
dr add ux view --name "User Profile" --property route=/profile

# Add component instance
dr add ux component-instance --name "Profile Form"

# List views
dr list ux view

# Validate UX layer
dr validate --layer ux

# Export UX documentation
dr export --layer ux --format markdown
```

---

## Example: Login View

```yaml
id: ux.view.login
name: "Login View"
type: view
properties:
  route: /login
  layout:
    type: centered
    maxWidth: 400px
  components:
    - id: login-form
      componentRef: library.component.form-field
      dataBinding:
        source: api.operation.login
        submitAction: POST /api/auth/login
      fields:
        - name: email
          type: email
          required: true
          validation:
            - type: email-format
            - type: required
        - name: password
          type: password
          required: true
          validation:
            - type: min-length
              value: 8
  actions:
    - id: submit-button
      type: button
      label: "Login"
      action: submit-form
      target: login-form
    - id: forgot-password
      type: link
      label: "Forgot password?"
      navigation: /forgot-password
  states:
    - id: idle
      initial: true
      onEnter: []
    - id: submitting
      onEnter:
        - action: disable-form
        - action: show-spinner
    - id: success
      onEnter:
        - action: navigate
          target: /dashboard
    - id: error
      onEnter:
        - action: show-error
        - action: enable-form
  transitions:
    - from: idle
      to: submitting
      trigger: submit
    - from: submitting
      to: success
      trigger: success
    - from: submitting
      to: error
      trigger: failure
    - from: error
      to: idle
      trigger: retry
  motivation:
    supports-goals:
      - motivation.goal.user-authentication
  api:
    operationId: login
  navigation:
    route-ref: navigation.route.login
```

---

## Pitfalls to Avoid

- ❌ Not using library components (inconsistent UX)
- ❌ Missing validation rules (poor user experience)
- ❌ Complex state machines without documentation
- ❌ Not linking to API operations or navigation routes
- ❌ Missing error states and handling
- ❌ No performance targets defined
