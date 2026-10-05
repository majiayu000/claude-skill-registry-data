---
name: event-tracking
displayName: Event Tracking
tagline: Set up and manage product event tracking with naming conventions and validation.
description: |
  Designs and implements product analytics event tracking plans. Defines
  event naming conventions, required properties, and validation rules.
  Creates tracking documentation, generates implementation code, and
  validates event data quality across platforms.
department:
  - Product
  - Engineering
  - Data & Analytics
use_cases:
  - Product Analytics
  - Event Tracking
  - Data Quality
tools_required:
  - Mixpanel MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Create a tracking plan for our checkout flow.
  Events: page views, button clicks, form submissions, and conversions.
exampleOutput: |
  Tracking Plan — Checkout Flow

  EVENTS
  1. checkout_started
     Properties: cart_value, item_count, source_page
     Trigger: User clicks "Checkout" button

  2. shipping_info_entered
     Properties: shipping_method, country, has_discount
     Trigger: User completes shipping form

  3. payment_method_selected
     Properties: method_type (card/paypal/apple_pay)
     Trigger: User selects payment option

  4. order_completed
     Properties: order_id, total_value, item_count, discount_amount
     Trigger: Payment confirmed

  5. checkout_abandoned
     Properties: last_step, cart_value, time_spent_seconds
     Trigger: User leaves without completing

  NAMING CONVENTION: snake_case, object_action format
  VALIDATION: All events require user_id and session_id
---

# Event Tracking

Set up and manage product event tracking with naming conventions and validation.

**Integrations:** Mixpanel

## When to Use

- The user wants to implement product analytics tracking
- Event naming conventions need standardization
- The user mentions "event tracking", "analytics events", or "tracking plan"

## Steps

### Step 1: Define Events

List all events to track with triggers and required properties.

### Step 2: Set Naming Convention

Establish consistent naming rules for events and properties.

### Step 3: Generate Implementation

Create tracking code or SDK configuration for each event.

### Step 4: Validate Data Quality

Set up validation rules and monitor event completeness.

## Output

Deliver:
- Tracking plan document
- Implementation code snippets
- Data validation rules
