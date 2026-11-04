---
name: refund-handling
description: Process customer refund and return requests according to store policy.
tools_required: [ecommerce_order_track, woo_order_manage]
always_on: false
---

# Refund Handling

## When to use this skill
- Customer asks about refunds or returns
- Customer wants to cancel an order
- Customer received damaged, wrong, or defective item
- Customer mentions return policy

## Before Processing
1. Verify order exists using `ecommerce_order_track`
2. Check order date against refund window
3. Determine refund type (full/partial/store credit)

## Refund Eligibility
Check these conditions:
- **Within 30 days of delivery**: Full refund eligible
- **30-60 days**: Store credit only
- **Over 60 days**: No refund (offer alternatives)
- **Sale items**: May have different policy (check references)

## Process Steps
1. Ask for order ID or email
2. Look up order and verify eligibility
3. Explain the applicable policy clearly
4. If eligible, process via `woo_order_manage`
5. Confirm refund details and timeline

## Communication Guidelines
- Always empathize first ("I understand this is frustrating...")
- Be clear about what's possible
- Offer alternatives when refund isn't possible
- Set realistic expectations for processing time

## Escalation Triggers
- Customer disputes the policy
- Complex case (multiple items, partial damage)
- Customer requests manager/supervisor
- Potential warranty claim

## Reference Documents
For detailed policies, load: [references/refund-policy.md]
