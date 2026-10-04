---
name: wenext-3d-ordering
description: Use when preparing, checking, submitting-to-payment, documenting, or troubleshooting Wenext / 未来工场 3D-print orders from STL, STP, or STEP files, including global and China site workflows, Chrome CDP automation, cart/checkout delayed loads, invoice 普票 setup, private config, and cashier/payment-boundary stops.
---

# Wenext 3D Ordering

## Overview

Use this skill to turn STL/STP/STEP files into a guarded Wenext 3D-print order workflow. Keep public repos clean: never commit recipient names, phone numbers, addresses, cookies, OTP/SMS codes, payment screenshots, browser profiles, or `~/.config/wenext-3d-order/private.json`.

## Safety Rules

- Treat submit/payment controls as real-world actions. Submit only when the user intends to place the order.
- Stop at `checkout/payment` or `cashier?orderId=...`; do not click `Payment Link`, `PayPal`, `发起支付`, recharge, wallet, or QR-payment buttons unless the user explicitly asks for payment.
- If cart or checkout shows `暂无产品`, wait for product rows before continuing.
- If login/binding overlays appear, stop and ask the user to finish login in the same Chrome profile.

## AgenticApp Tooling

When working in AgenticApp, prefer the maintained CDP tool:

```bash
python3 agentic_tools/order_assistant.py --provider wenext --site china status
python3 agentic_tools/order_assistant.py --provider wenext --site china --allow-submit place
agentic_tools/wenext_3d_order_agent/scripts/quick_order_global.sh upload --navigate
agentic_tools/wenext_3d_order_agent/scripts/quick_order_china.sh upload --navigate
agentic_tools/wenext_3d_order_agent/scripts/quick_order_china.sh china-flow --allow-submit
```

Private state lives under `~/.config/wenext-3d-order/`: config, DOM snapshots, SQLite order database, and submission logs. The unified wrapper writes blocker handoff packets to `~/.config/manufacturing-order-assistant/packets/`.

## China Flow

Use the verified path:

```text
upload files -> wait quote rows -> 加入购物车 -> header cart -> wait rows -> 去结账 -> wait checkout rows -> invoice -> 提交订单 -> cashier
```

For `数电普票`, use `invoice.type: "数电普票"` or `"pupiao"` in private config, with `invoice.title` and `invoice.email`. The working fallback is personal 普票, not company 普票, unless tax number data is available.

## Global Flow

The global site uses the English checkout path:

```text
upload files -> address confirm -> Apply shipping -> Check Out -> Submit Order -> checkout/payment
```

Stop at the payment page and record a private snapshot.
