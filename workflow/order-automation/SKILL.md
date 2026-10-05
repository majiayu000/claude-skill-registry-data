---
name: order-automation
displayName: Order Automation
tagline: Automate order processing, fulfillment, and status updates across your e-commerce stack.
description: |
  Automates the end-to-end order lifecycle from placement to delivery.
  Processes new orders, triggers fulfillment workflows, updates tracking
  information, and handles returns and refunds. Integrates with payment
  processors and shipping providers for seamless order management.
department:
  - E-commerce
  - Operations
use_cases:
  - Order Processing
  - Fulfillment Automation
  - E-commerce Operations
tools_required:
  - Shopify MCP
  - Stripe MCP
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
  Set up automated order processing for our Shopify store.
  Include fraud detection, fulfillment routing, and status notifications.
exampleOutput: |
  Order Automation — Shopify Store

  WORKFLOW
  1. New Order      -> Fraud check (Stripe Radar)
  2. Payment OK     -> Route to fulfillment center
  3. Shipped        -> Send tracking email + SMS
  4. Delivered      -> Request review after 3 days
  5. Return Request -> Auto-generate return label

  FRAUD RULES
  - Flag orders > $500 from new customers
  - Block mismatched billing/shipping countries
  - Review orders with >3 items of same SKU

  DAILY STATS
  Orders Processed:  142
  Auto-fulfilled:    128 (90%)
  Flagged for Review: 8
  Returns Initiated:  6
---

# Order Automation

Automate order processing, fulfillment, and status updates across your e-commerce stack.

**Integrations:** Shopify, Stripe

## When to Use

- The user wants to automate order processing workflows
- Manual order fulfillment is creating bottlenecks
- The user mentions "order automation", "fulfillment", or "order processing"

## Steps

### Step 1: Configure Order Flow

Define the order lifecycle stages and automation rules.

### Step 2: Set Up Fraud Detection

Configure fraud rules and review thresholds.

### Step 3: Automate Notifications

Set up customer notifications for each order stage.

## Output

Deliver:
- Order processing workflow configuration
- Fraud detection rules
- Customer notification templates
