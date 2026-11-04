---
name: order-management
description: Complete WooCommerce order management. Process orders, handle fulfillment, manage refunds, and track order lifecycle.
tools_required: [woo_order_track, woo_order_manage, woo_customers, email]
always_on: false
group: woocommerce
order: 8
requires: [shopping-assistant]
suggests: [refund-handling, shipping-configurator]
---

# Order Management

Complete WooCommerce order processing and fulfillment management.

## When to Use This Skill

- Processing new orders
- Updating order status
- Managing fulfillment
- Handling customer inquiries
- Processing refunds
- Tracking order history

## Core Capabilities

### Order Processing
- View orders with `woo_order_track`
- Update status with `woo_order_manage`
- Add order notes
- Modify orders

### Fulfillment
- Pick/pack workflow
- Shipping label generation
- Tracking number entry
- Delivery confirmation

### Customer Communication
- Order confirmations via `email`
- Status update notifications
- Shipping notifications
- Delivery follow-up

## Order Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| Pending | Awaiting payment | Wait or follow up |
| Processing | Payment received | Fulfill order |
| On Hold | Needs review | Investigate |
| Completed | Fulfilled | Archive |
| Cancelled | Cancelled | Refund if paid |
| Refunded | Fully refunded | Closed |
| Failed | Payment failed | Contact customer |

## Order Workflow

### Standard Order Flow

```
1. New Order → Pending Payment
2. Payment Received → Processing
3. Items Picked → (internal)
4. Items Packed → (internal)
5. Shipped → Completed
6. Delivered → (confirmed)
```

### Order Processing Steps

1. **Review Order**
   - Check items and quantities
   - Verify shipping address
   - Note special instructions
   - Check payment status

2. **Prepare Fulfillment**
   - Print packing slip
   - Pick items from inventory
   - Quality check
   - Pack securely

3. **Ship**
   - Generate shipping label
   - Add tracking number
   - Update status to Shipped
   - Send notification

4. **Complete**
   - Mark as Completed
   - Archive order
   - Request review (optional)

### Handling Issues

**Address Problems:**
1. Contact customer immediately
2. Hold order until confirmed
3. Update address
4. Document in notes

**Stock Issues:**
1. Check inventory
2. Contact customer with options
3. Partial fulfillment or wait
4. Document decision

**Payment Issues:**
1. Verify payment status
2. Contact customer if pending
3. Wait or cancel as appropriate
4. Document attempts

## Order Notes

### Internal Notes (Staff Only)
```
- Issue: Customer requested gift wrapping
- Action: Added tissue paper, no receipt
- Staff: John, 2024-01-15
```

### Customer Notes (Visible)
```
Your order has shipped!
Tracking: [number]
Expected delivery: [date]
```

## Bulk Operations

### Bulk Status Update
- Select multiple orders
- Choose new status
- Apply to all
- Notifications sent automatically

### Bulk Export
- Select date range
- Choose fields
- Export to CSV
- Use for reporting

### Bulk Print
- Packing slips
- Invoices
- Shipping labels
- Pick lists

## Communication Templates

### Order Received
```
Subject: Order #[number] Received

Hi [name],

Thank you for your order!

Order #: [number]
Items: [list]
Total: [amount]

We'll notify you when it ships.

Thanks!
[Store]
```

### Order Shipped
```
Subject: Order #[number] Shipped!

Hi [name],

Great news - your order is on the way!

Tracking: [number]
Carrier: [carrier]
Expected: [date]

Track your package: [link]

Thanks for shopping with us!
[Store]
```

### Delivery Follow-up
```
Subject: How was your order?

Hi [name],

Your order should have arrived by now.

We'd love to hear your feedback!
[Review link]

Any issues? Just reply to this email.

Thanks!
[Store]
```

## Best Practices

1. **Process quickly** - Same/next business day
2. **Communicate proactively** - Updates before they ask
3. **Document everything** - Notes save time later
4. **Quality check** - Verify before shipping
5. **Personalize** - Add thank you notes
6. **Follow up** - Request reviews
7. **Handle issues fast** - Happy customers forgive

## Metrics to Track

| Metric | Target | Description |
|--------|--------|-------------|
| Processing Time | <24 hrs | Order to ship |
| Fulfillment Rate | 99%+ | Orders fulfilled correctly |
| On-Time Delivery | 95%+ | Arrived by estimate |
| Return Rate | <5% | Returned orders |
| Customer Satisfaction | 4.5+ | Rating/reviews |

## Troubleshooting

### Order Stuck in Processing
- Check inventory
- Verify address
- Look for payment issues
- Review notes for blocks

### Customer Didn't Receive
- Verify tracking shows delivered
- Check address accuracy
- Contact carrier
- Offer replacement/refund

### Duplicate Order
- Compare orders carefully
- Contact customer to confirm
- Cancel duplicate
- Refund if charged twice
