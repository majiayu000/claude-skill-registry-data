---
name: store
description: The merch store that members pay for with points.
---

# Store

Use it to manage products and orders.

## Flow

1. `store.products` and `store.orders` to see what is there.
2. `store.save_product` adds a product (name, price, stock) or changes one by id.
3. `store.update_orders` sets the status or the message to the buyer for up to 100 orders.

## Watch out

- Cancelling an order puts its items back in stock and refunds the points. A cancelled order stays cancelled.
- `store.delete_products` refuses a product that has orders.
