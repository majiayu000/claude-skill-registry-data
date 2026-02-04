---
name: LAYER_10_NAVIGATION
description: Expert knowledge for Navigation Layer modeling in Documentation Robotics
triggers:
  ["navigation", "routing", "route", "flow", "navigation guard", "redirect", "navigation flow"]
version: 0.7.0
---

# Navigation Layer Skill

**Layer Number:** 10
**Specification:** Metadata Model Spec v0.7.0
**Purpose:** Defines multi-modal navigation flows, routes, guards, and transitions between views.

---

## Layer Overview

The Navigation Layer captures **navigation and routing**:

- **ROUTES** - URL paths to views
- **GUARDS** - Authorization checks before navigation
- **FLOWS** - Multi-step navigation flows
- **TRANSITIONS** - Navigation between routes
- **REDIRECTS** - Conditional redirects
- **CONTEXT** - Navigation context variables
- **TRACKING** - Analytics and process tracking

This layer uses **Multi-Modal Navigation** supporting web, mobile, voice, and other modalities.

**Central Entity:** The **Route** (URL path to view) is the core modeling unit.

---

## Entity Types

### Core Navigation Entities (10 entities)

| Entity Type              | Description                                |
| ------------------------ | ------------------------------------------ |
| **Route**                | URL path mapped to view                    |
| **NavigationGuard**      | Authorization/validation before navigation |
| **NavigationFlow**       | Multi-step navigation sequence             |
| **NavigationTransition** | Transition between routes                  |
| **FlowStep**             | Step in navigation flow                    |
| **ContextVariable**      | Navigation context data                    |
| **DataMapping**          | Data passing between routes                |
| **NotificationAction**   | Navigation-triggered notifications         |
| **ProcessTracking**      | Business process tracking                  |
| **FlowAnalytics**        | Navigation analytics                       |

---

## When to Use This Skill

Activate when the user:

- Mentions "navigation", "routing", "routes", "flows"
- Wants to define URL paths or route guards
- Asks about multi-step flows or navigation transitions
- Needs to model navigation between screens
- Wants to link navigation to UX views or business processes

---

## Cross-Layer Relationships

**Outgoing (Navigation → Other Layers):**

- `view-ref` → UX Layer (which view does this route show?)
- `business.realizes-process` → Business Layer (what process does this flow realize?)
- `security.required-roles` → Security Layer (authorization requirements)
- `apm.flow-metrics` → APM Layer (navigation analytics)

**Incoming (Other Layers → Navigation):**

- UX Layer → Navigation (views reference routes)
- Business Layer → Navigation (processes trigger flows)

---

## Design Best Practices

1. **Guards** - Add navigation guards for protected routes
2. **Context** - Pass necessary context between routes
3. **Analytics** - Track navigation flows for insights
4. **Error handling** - Define fallback routes for errors
5. **Deep linking** - Support deep linking for all routes
6. **SEO** - Consider SEO requirements for public routes
7. **Performance** - Lazy-load routes when appropriate

---

## Common Commands

```bash
# Add route
dr add navigation route --name "User Profile Route" --property path=/profile/:id

# Add navigation guard
dr add navigation navigation-guard --name "Auth Guard"

# Add navigation flow
dr add navigation navigation-flow --name "Checkout Flow"

# List routes
dr list navigation route

# Validate navigation layer
dr validate --layer navigation

# Export navigation map
dr export --layer navigation --format mermaid
```

---

## Example: Protected Profile Route

```yaml
id: navigation.route.user-profile
name: "User Profile Route"
type: route
properties:
  path: /profile/:userId
  view-ref: ux.view.user-profile
  guards:
    - navigation.guard.authentication
    - navigation.guard.profile-ownership
  parameters:
    - name: userId
      type: string
      format: uuid
      required: true
  meta:
    title: "User Profile"
    requiresAuth: true
    allowedRoles:
      - user
      - admin
  contextVariables:
    - name: currentUserId
      source: auth.user.id
  dataMapping:
    - source: route.params.userId
      target: view.data.userId
  security:
    required-roles:
      - security.role.authenticated-user
  business:
    realizes-process: business.process.profile-management
  apm:
    flow-metrics:
      - apm.metric.profile-view-count
      - apm.metric.profile-load-time
```

---

## Example: Multi-Step Checkout Flow

```yaml
id: navigation.flow.checkout
name: "Checkout Flow"
type: navigation-flow
properties:
  steps:
    - id: cart-review
      route: /checkout/cart
      view: ux.view.cart-review
      onNext: validate-cart
    - id: shipping-address
      route: /checkout/shipping
      view: ux.view.shipping-form
      onNext: validate-address
    - id: payment
      route: /checkout/payment
      view: ux.view.payment-form
      onNext: validate-payment
    - id: confirmation
      route: /checkout/confirm
      view: ux.view.order-confirmation
      final: true
  transitions:
    - from: cart-review
      to: shipping-address
      trigger: next-button
      guard: cart-not-empty
    - from: shipping-address
      to: payment
      trigger: next-button
      guard: valid-address
    - from: payment
      to: confirmation
      trigger: submit
      guard: payment-successful
  context:
    - cartId
    - selectedAddress
    - paymentMethod
  analytics:
    trackStepCompletion: true
    trackAbandonmentRate: true
  business:
    realizes-process: business.process.checkout
```

---

## Pitfalls to Avoid

- ❌ Missing authentication guards on protected routes
- ❌ Not validating route parameters
- ❌ Complex flows without clear step definitions
- ❌ Not tracking navigation analytics
- ❌ Missing cross-layer links to UX views
- ❌ No error/fallback routes defined
