---
name: jlcpcb-ordering
description: Use when preparing, checking, submitting, documenting, or troubleshooting JLCPCB/JiaLiChuang PCB orders from Gerber ZIPs, including China/global site workflows, desktop assistant handoff, Chrome CDP automation, private config, OSP/surface-finish limits, quality-compensation fees, courier defaults, and review-before-payment submission.
---

# JLCPCB Ordering

## Overview

Use this skill to turn a checked Gerber ZIP into a guarded JLC order workflow. Keep public repos clean: never commit recipient names, phone numbers, addresses, cookies, OTP/SMS codes, screenshots with private fields, wallet/payment data, or `~/.config/jlcpcb-order/private.json`.

## Safety Rules

- Treat submit/payment controls as real-world actions. Do not click final submit without explicit user intent, and never click recharge, wallet, or payment buttons unless the user explicitly asks.
- Stop if the order-check drawer shows `检测到您的订单还有`, `去填写`, `系统未检测到`, `余额不足`, `充值`, an OSP-size warning, or a paid `品质赔付费`.
- Submit only from a visible, clean order-check drawer. Do not use the whole page body as proof, because stale tabs and unselected option labels can create false positives.
- For bare PCBs, use `按标准合同常规处理`; do not select `元器件移植全额赔付`.
- Default China courier is `顺丰电商标快`; default shipping mode is `不同交期订单不一起发货`.

## AgenticApp Tooling

When working in AgenticApp, prefer the maintained CDP tool:

```bash
python3 agentic_tools/order_assistant.py --provider jlc --site china status
python3 agentic_tools/order_assistant.py --provider jlc --site china --allow-submit place path/to/gerber.zip
agentic_tools/jlcpcb_order_agent/scripts/launch_shared_chrome.sh
python3 -u agentic_tools/jlcpcb_order_agent/scripts/submit_board_order.py --config path/to/jlcpcb_order/order-settings.json --site china place
agentic_tools/jlcpcb_order_agent/scripts/quick_order_china.sh path/to/gerber.zip
agentic_tools/jlcpcb_order_agent/scripts/quick_order_global.sh path/to/gerber.zip
agentic_tools/jlcpcb_order_agent/scripts/quick_order_assistant.sh path/to/gerber.zip
```

Use `JLCPCB_ALLOW_SUBMIT=1` only after the check drawer is clean. Private state lives under `~/.config/jlcpcb-order/`: config, DOM snapshots, SQLite order database, and completion logs. The unified wrapper writes blocker handoff packets to `~/.config/manufacturing-order-assistant/packets/`.

For AgenticApp's paired manufacturing-order tools, also check `agentic_tools/ORDER_AUTOMATION.md`; Wenext 3D printing uses `agentic_tools/wenext_3d_order_agent/`.

For the official Linux desktop assistant, prefer the local installer:

```bash
agentic_tools/jlcpcb_order_agent/scripts/install_assistant_local.sh \
  ~/Downloads/JLCPcAssit-linux-x64-5.0.69.zip
```

It creates `~/.local/bin/jlc-assistant`; do not commit `~/.config/jlc-assistant`.

Start it through the detached, health-checked launcher rather than a foreground terminal:

```bash
agentic_tools/jlcpcb_order_agent/scripts/launch_assistant_local.sh --restart
```

## Workflow

1. Validate the board package first: KiCad DRC/ERC, Gerber ZIP, drill files, board size, and preview. Prefer `submit_board_order.py` when the repo has a public `jlcpcb_order/order-settings.json`.
2. Launch the shared logged-in Chrome profile through CDP; do not create throwaway browser profiles for ordering.
3. Upload Gerbers and fill conservative bare-PCB defaults: FR-4, correct layer count, explicit board size in centimeters when JLC misses it, low quantity, no SMT, no stencil, manual confirmation, standard compensation.
4. If OSP is rejected because any side is under `7 cm`, choose a supported finish such as lead-free HASL or stop for review.
5. If a matching legacy uploaded row already exists, use that row's `立即下单`/`pcbFileId` instead of uploading another copy. Avoid duplicate uploads unless the existing row is absent or invalid.
6. Run `检查订单`. If JLC opens `请选择本单是否需要SMT贴片`, choose `确定，不需要SMT`, then run `检查订单` again.
7. Clear all missing fields including board mark/customer-code fields. Select `确认订单方式` and `发货方式` by their field labels, not generic button text.
8. Record a private snapshot, then submit only to review/payment boundary when authorized.
9. After submit, prefer the `pcbPlaceSuccess` tab for database/log snapshots; stale order tabs can remain open.

Read `references/jlcpcb-ordering-runbook.md` for live DOM selectors, terms, and the China/global/assistant submission paths.
