---
name: order-lookup
description: Look up and provide order status, tracking, and shipping information
category: woocommerce
display_name: Order Lookup
tools_required: [wc_get_order, wc_search_orders]
always_on: false
---

# Order Lookup Skill

This skill enables the AI agent to find and share order information with customers.

## When to Use This Skill

Activate when the customer asks about:
- Order status, where is my order
- Tracking number or shipping updates
- Delivery date or estimated arrival
- Order history or past purchases

## Instructions

### 1. Identify the Order
- Ask for order number (preferred)
- Or search by email address
- Verify customer identity if needed

### 2. Share Order Information
Provide relevant details based on status:

**Processing:**
> "Your order #XXXX is being prepared. It should ship within 1-2 business days."

**Shipped:**
> "Great news! Your order shipped on [date]. Here's your tracking number: [tracking]. Estimated delivery: [date]."

**Delivered:**
> "Your order was delivered on [date]. If you haven't received it, please check with neighbors or your building management."

**On Hold:**
> "Your order is on hold pending [reason]. [Action needed to resolve]."

### 3. Proactive Assistance
After providing status, offer:
- Tracking link if available
- Help with any issues
- Product care tips if delivered

## Handling Issues

### Order Not Found
- Double-check order number spelling
- Search by email if no order number
- Suggest checking spam folder for confirmation email

### Delayed Orders
- Apologize for the inconvenience
- Provide updated timeline if available
- Offer discount code for future purchase if significant delay

## Important Notes
- Never share order details without verification
- Use conversational, friendly language
- Offer order modification if still processing
