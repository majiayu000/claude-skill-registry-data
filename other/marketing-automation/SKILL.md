---
name: marketing-automation
description: Marketing automation architect — build trigger→condition→action journeys, drip sequences, and lifecycle flows. Free-first n8n/Automatisch.
personas:
  - MARKETING
triggers:
  - journey
  - zapier
  - marketing automation
  - أتمتة تسويق
  - رحلة عميل
tech_stack:
  - websites/n8n-io_n8n
  - websites/automatisch_automatisch
  - websites/knadh_listmonk
  - websites/mautic_mautic

---
[SKILL] marketing-automation
[OBJ] Design and deploy automated customer journeys — trigger → condition → action — that nurture leads, onboard users, and recover churn without manual effort.

[RULES]
1. [REQ] Journey anatomy: Trigger (event) → Enrich → Condition (branch) → Action (message/task) → Wait → Loop/Exit. Model every flow as a state graph.
2. [CMD] Context7 IDs: `n8n-io/n8n` (node/trigger graph), `automatisch/automatisch` (Zapier alt, AGPL), `knadh/listmonk` (lists/campaigns), `mautic/mautic` (CampaignBundle state machine).
3. [REQ] Free-first engines: n8n (fair-code, self-host, internal use) or Automatisch (AGPL, self-host) default; Mautic for email journeys; Zapier/Make only as paid parity.
4. [REQ] Drip design: welcome (3-5 emails), nurture (value→proof→offer), abandoned-cart, re-engagement. Each email uses `copy-frameworks` (PAS/BAB).
5. [REQ] Idempotency + exits: every journey has an unsubscribe/opt-out path and a "do not contact" flag checked at each step (see `marketing-compliance`).
6. [REQ] Lifecycle stages: subscriber → lead → MQL → SQL → customer → advocate. Map which journey owns each transition.
7. [REQ] Error handling: failed step → retry + alert; dead-letter to human queue; never silently drop a customer.
8. [REQ] Arabic/RTL: Arabic-language journeys with RTL templates; respect local sending-time windows; mirror logic for ar/en audiences.
9. [REQ] Measurement: track open/click/convert per step; optimize the weakest node. Feed to `marketing-analytics`.
10. [REQ] Approval gate: any journey that sends messages requires explicit user approval before activation (kernel write-gate).

[PROHIBIT]
1. No automation that sends without an opt-out path.
2. No journey activated without user approval.
3. No infinite/non-terminating loops.
4. No logging of PII/payment data.
