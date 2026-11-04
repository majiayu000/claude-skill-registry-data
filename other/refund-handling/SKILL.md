---
name: refund-handling
description: Handle refund requests and returns for WooCommerce orders with policy enforcement
category: woocommerce
display_name: Refund Handling
tools_required: [wc_get_order, wc_process_refund, wc_update_order_status]
always_on: false
---

# Refund Handling Skill

This skill enables the AI agent to process refund requests following store policies.

## When to Use This Skill

Activate when the customer mentions:
- Refund, returns, money back
- Order not as expected
- Wrong item received
- Damaged or defective product

## Instructions

### 1. Verify Order Details
- Request order number or email to look up the order
- Confirm the items being returned
- Check order date against refund policy window

### 2. Policy Checks
- Verify item is within return window (default: 30 days)
- Check if item category allows refunds
- Confirm item condition (unused, original packaging)

### 3. Process Refund
For approved refunds:
- Explain refund timeline (3-5 business days)
- Provide return shipping instructions if needed
- Update order status appropriately

For denied refunds:
- Explain reason politely
- Offer alternatives (exchange, store credit)
- Escalate to human if customer insists

### 4. Example Responses

**Approved Refund:**
> "I've processed your refund of $XX.XX for Order #XXXX. You should see the funds back in your account within 3-5 business days. Is there anything else I can help with?"

**Denied Refund:**
> "I understand your frustration. Unfortunately, this item is outside our 30-day return window. However, I can offer you a 15% discount on a replacement or store credit for the full amount. Would either of these options work for you?"

## Important Notes
- Always maintain a helpful, empathetic tone
- Document all refund decisions in order notes
- Escalate complex cases or large amounts to human support
