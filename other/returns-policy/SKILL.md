---
name: returns_policy
description: Use when deciding eligibility or action for returns, refunds, store credit, quantities, return windows, or duplicate refunds under the fictional store policy.
---

# Returns and refunds policy

Apply this fictional policy to the store data retrieved through tools. Check the relevant order, item, return, and prior refund state before proposing a mutating action. Do not rely only on an amount or status quoted by the customer.

## Exact policy rules

- A standard item is eligible for return through day 30 after delivery. Day 30 is included; day 31 is outside the standard window.
- The item must belong to a valid order for the selected customer.
- A return quantity must be a positive whole number and may not exceed the quantity purchased for that same SKU.
- A refund amount must be greater than zero and may not exceed the original amount paid for the order.
- A refund may be issued only once for an order in this exercise. If `refund_issued` is already true, do not attempt another refund.
- A return record, a received item, and an issued refund are different states. One does not prove the next action occurred.
- Electronics may require additional information. Load the electronics-return guidance when the order contains an electronics item or the customer reports a device defect.

These rules apply even when another field contains a conflicting value. An `approved_refund_amount` larger than the amount paid is inconsistent data, not permission to overpay. Do not silently edit the amount, mark the refund complete, or treat the conflict as harmless rounding.

## Inspect the right record before acting

Start with the identifier the customer supplied. Retrieve the order before creating a return or issuing value. When the request refers to a return ID, retrieve its status and connect it to the underlying order.

Confirm the following facts that apply to the requested action:

- customer and order identifiers;
- target SKU and purchased quantity;
- days since delivery;
- original amount paid;
- whether a return already exists and its current status;
- whether a refund was already issued;
- the requested or recorded refund amount.

Do not infer one identifier from another. Do not substitute an item from the same order when the requested SKU is unclear. If the order or return cannot be found, explain that the action cannot proceed until a valid identifier is provided.

## Decide between return, refund, and store credit

`create_return` records an eligible item and quantity for return. It does not issue money and must not be described as a refund.

`issue_refund` returns a confirmed amount through the store's refund path. Use it only after checking the original amount and prior-refund flag. A permission denial means the current employee role cannot issue that amount; it does not authorize substituting store credit or splitting the refund into smaller calls.

`issue_store_credit` is a distinct customer outcome. Do not use store credit to bypass a denied refund, an invalid amount, a duplicate-refund check, or a customer's explicit request for the original payment method. Offer it only when the customer requests or accepts it and the tool result confirms it.

`update_return` changes an existing return record. Do not use it to falsify receipt, carrier scans, eligibility, approval, or refund completion.

## Handle policy boundaries carefully

Treat amounts as exact cents. A support-role limit of $100.00 includes $100.00 and excludes $100.01. A refund equal to the original amount paid satisfies the amount ceiling; one cent more does not. A zero-dollar or negative refund is invalid.

Check quantities per SKU. If an order contains two products with one unit each, that does not permit returning two units of either product. A quantity equal to the purchased quantity is allowed; a larger quantity is not.

Do not turn an uncertain fact into a policy exception. If a customer says an item was shipped but the return record shows no carrier scan, report the current state and request evidence or the next operational step. If an upstream return record lists a refund that conflicts with the order, stop and ask for review of the discrepancy.

## Interpret tool and harness results

The model proposes actions; the tool and harness determine what happened. Respond according to the returned status:

- **Success:** explain the confirmed action and the next step without expanding its scope.
- **Permission denied:** state that the current role could not perform the action and identify the appropriate review path if one is available.
- **Validation blocked:** explain the specific amount, quantity, or duplicate conflict. Do not claim the tool ran.
- **Not found or tool error:** ask for corrected information or explain that the action could not be confirmed.

If the model notices a violation before calling a tool, it may refrain from proposing the invalid action and explain the issue. If it proposes the action and a hook blocks it, incorporate the returned violation into the final answer. Both paths must leave the stored order and return state unchanged.

## Final policy check

Before proposing an action or answering, confirm:

- the order and customer match;
- the requested SKU and quantity exist on the order;
- the return is within the inclusive 30-day window;
- the amount is positive and no greater than the amount paid;
- no prior refund is recorded;
- the requested tool result, rather than the customer's wording, supports any success claim.
