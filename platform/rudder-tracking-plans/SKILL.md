---
name: rudder-tracking-plans
description: Creates and manages tracking plans that validate events against schema contracts. Use when creating or managing tracking plans that define which events are allowed for a source
allowed-tools: "Bash(rudder-cli *), Read, Write, Edit"
---

# RudderStack Tracking Plans Management

This skill teaches how to assemble events into **tracking plans** - contracts that define which events a source can send and what properties each event must have.

## What is a Tracking Plan?

A tracking plan is a schema that:
- Defines **which events** are allowed from a source
- Specifies **required vs optional properties** for each event
- Enables **validation** at event ingestion time
- Provides **governance** over what data enters your warehouse

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     Source      │────▶│  Tracking Plan  │────▶│   Destination   │
│  (Web App SDK)  │     │   (Validator)   │     │   (Warehouse)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                        Validates events
                        against schema
```

## YAML Schema

### Basic Tracking Plan

```yaml
version: "rudder/v1"
kind: "tracking-plan"
metadata:
  name: "tracking-plans"
spec:
  name: "Web App Tracking Plan"
  description: "Events for the main e-commerce web application"
  events:
    - event: "urn:rudder:event/product-viewed"
    - event: "urn:rudder:event/product-added-to-cart"
    - event: "urn:rudder:event/order-completed"
```

### Tracking Plan with Rule Overrides

Override event-level rules at the tracking plan level:

```yaml
version: "rudder/v1"
kind: "tracking-plan"
metadata:
  name: "tracking-plans"
spec:
  name: "Mobile App Tracking Plan"
  description: "Events for iOS and Android apps"
  events:
    - event: "urn:rudder:event/product-viewed"
      rules:
        # Make session_id required for mobile (optional in event definition)
        - property: "urn:rudder:property/session_id"
          required: true
        # Make device_id required for mobile attribution
        - property: "urn:rudder:property/device_id"
          required: true
    - event: "urn:rudder:event/product-added-to-cart"
    - event: "urn:rudder:event/order-completed"
```

## Rule Precedence

When the same property appears at multiple levels:

```
1. Tracking Plan event rules  (highest priority)
2. Event-level rules          (default)
3. Property definitions       (validation config only)
```

**Example:** If `session_id` is optional in the event definition but required in the tracking plan, it's **required** for that tracking plan.

## Real-World Example

See `references/ecommerce-example.md` for a complete e-commerce example showing:
- Shared event catalog used by web, mobile, and kiosk apps
- Web App tracking plan (full funnel with page attribution)
- Mobile App tracking plan (device_id attribution)
- Kiosk tracking plan (limited event set)
- Environment-specific plans (production vs development)
- Gradual rollout patterns

## Governance Settings

When events violate the tracking plan:

```yaml
spec:
  name: "Strict Tracking Plan"
  governance:
    # Options: block, forward, log
    unplannedEvents: block      # Reject events not in plan
    violatingEvents: forward    # Forward violations with flag
```

| Setting | Behavior |
|---------|----------|
| `block` | Reject event entirely |
| `forward` | Forward event with violation metadata |
| `log` | Allow event, log violation for review |

## Directory Structure

```
tracking-plans/
├── web-app.yaml
├── mobile-app.yaml
├── kiosk.yaml
└── internal-tools.yaml
```

Each tracking plan in its own file for clear git history and code review.

## Workflow: Creating a New Tracking Plan

### Step 1: Identify the Source

What application/SDK will use this tracking plan?
- Web app (JavaScript SDK)
- Mobile app (iOS/Android SDK)
- Server-side (Node.js SDK)

### Step 2: List Required Events

Which events from your data catalog does this source need?

```
Web App needs:
✓ Product Viewed
✓ Product Added to Cart
✓ Order Completed
✗ App Opened (mobile only)
```

### Step 3: Determine Rule Overrides

For each event, what properties should be:
- **Required** for this source specifically?
- **Optional** even if required elsewhere?

### Step 4: Create the YAML

```yaml
version: "rudder/v1"
kind: "tracking-plan"
metadata:
  name: "tracking-plans"
spec:
  name: "Your Tracking Plan Name"
  description: "Clear description of what source uses this"
  events:
    - event: "urn:rudder:event/event-name"
      rules:
        - property: "urn:rudder:property/property-name"
          required: true
```

### Step 5: Validate and Apply

```bash
# Validate
rudder-cli validate -l ./

# Preview
rudder-cli apply --dry-run -l ./

# Apply
rudder-cli apply -l ./
```

### Step 6: Connect to Source

After applying, connect the tracking plan to your source:
- Via RudderStack UI: Sources → Select Source → Tracking Plan
- Via API: Update source configuration

## Common Patterns

### Pattern: Environment-Specific Plans

```yaml
# tracking-plans/web-app-production.yaml
spec:
  name: "Web App - Production"
  governance:
    unplannedEvents: block      # Strict in production
    violatingEvents: block

# tracking-plans/web-app-development.yaml
spec:
  name: "Web App - Development"
  governance:
    unplannedEvents: log        # Lenient in development
    violatingEvents: forward
```

### Pattern: Shared Base + Overrides

Create a comprehensive event catalog, then each tracking plan includes only what it needs:

```
Data Catalog: 50 events defined
├── Web App Plan: 30 events
├── Mobile Plan: 25 events
└── Kiosk Plan: 5 events
```

### Pattern: Gradual Rollout

Start permissive, tighten over time:

```yaml
# Phase 1: Log only
governance:
  unplannedEvents: log
  violatingEvents: log

# Phase 2: Forward violations
governance:
  unplannedEvents: forward
  violatingEvents: forward

# Phase 3: Block violations
governance:
  unplannedEvents: block
  violatingEvents: block
```

## Validation Commands

```bash
# Validate tracking plan references exist
rudder-cli validate -l ./

# Preview what will change
rudder-cli apply --dry-run -l ./

# Apply to workspace
rudder-cli apply -l ./
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Event URN not found | Referenced event doesn't exist | Create event in data catalog first |
| Property not in event | Adding property not defined on event | Add property to event rules first |
| Duplicate tracking plan name | Conflict in workspace | Use unique, descriptive names |
| Too strict too fast | Breaking production SDKs | Use `log` mode first, analyze, then tighten |

## Linking to Sources

After creating and applying a tracking plan:

1. **Get tracking plan ID** from workspace
2. **Update source** to use the tracking plan
3. **Test** by sending events and checking validation

Events from the source will now be validated against your tracking plan schema.
