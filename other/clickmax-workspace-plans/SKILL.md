---
name: clickmax-workspace-plans
description: Use when the user wants to inspect, compare, preview cancellation of, or cancel the workspace's own Clickmax SaaS subscription and billing plan.
---

## When this applies

Use this skill for the workspace's own Clickmax SaaS billing plan: inspect current plan/usage, compare upgrades, view invoice or plan transaction history, preview cancellation impact, cancel the current plan, or manage the cards the workspace pays Clickmax with.

Not this skill:

- customer subscriptions sold by the workspace -> `clickmax-seller-subscriptions`

## Key assumptions

- this surface is about the workspace as Clickmax customer
- usage metrics are current billing-period counts
- cancel preview should come before cancel execution when intent is exploratory
- cancelling does NOT take effect immediately: the plan enters a retention window and is only cancelled at `scheduledFor`, during which support can revert it. The window shrinks when a renewal charge is close, and disappears entirely when the charge is imminent (`executedImmediately: true`)
- there is no admin/cross-workspace cancel tool here — the cancel tool is scoped to the CALLING workspace's own plan only; there is no way to target another workspace's subscription from this skill

## Thought process

1. Confirm the user means the workspace's own Clickmax subscription, not customer subscriptions sold by that workspace.
2. Separate read-only questions from cancellation intent.
3. Cancel with `plans_cancel_current_plan` (structured `reason`, always the caller's own current plan). Preview first with `plans_cancel_preview` whenever the intent is still exploratory. Report the returned `scheduledFor` — never tell the user the plan is already cancelled.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__plans_user_summary`, `mcp__plugin_clickmax_clickmax__plans_user_metrics`, and `mcp__plugin_clickmax_clickmax__plans_invoice_summary` together for current plan overview, billing status, renewal context, and current billing-period usage.
- `mcp__plugin_clickmax_clickmax__plans_user_metrics` is the source for the workspace's current LIMITS: it returns, per resource, `used`, `limit`, and `remaining` (limit `-1`/empty = unlimited). Use it whenever the user asks about their plan usage/limits ("uso do plano", "quais meus limites", "quanto já usei") or wants to see where they stand across resources.
- Use `mcp__plugin_clickmax_clickmax__plans_upgrade_list` when the user wants higher-tier options or a comparison between the current plan and available upgrades.
- Use `mcp__plugin_clickmax_clickmax__plans_transaction_history` for past billing events, renewals, charges, and plan movements.
- Use `mcp__plugin_clickmax_clickmax__plans_pending_changes` to detect already-scheduled plan changes before suggesting or performing another change.
- Use `mcp__plugin_clickmax_clickmax__plans_cancel_preview` when the user is still evaluating cancellation impact, timing, expiration, or access loss — it takes NO input, it always previews the caller's own current plan.
- Cancel with `mcp__plugin_clickmax_clickmax__plans_cancel_current_plan` (requires a structured `reason`; `reasonDescription` is mandatory when the reason is `other`; `type` picks keep-account vs delete-account). Always targets the caller's own current plan, and only after the user clearly asked to cancel.
- After cancelling, state the effective date from `scheduledFor` and that the plan stays usable until then. Saying "cancelled" flat out is wrong while the window is open.
- Before any cancellation path, check pending changes so you do not stack a new mutation on top of an already-scheduled one.
- Manage the workspace's own SaaS-billing cards (the cards paying for THIS Clickmax plan, not a customer's checkout card — different domain, do not confuse with `clickmax-transaction-operations`/checkout buyers): `mcp__plugin_clickmax_clickmax__buyers_cards_list` to see saved cards, `mcp__plugin_clickmax_clickmax__buyers_card_set_default` to promote one (it decides which card Clickmax charges next and unsets the previous default — confirm the card with the user first), `mcp__plugin_clickmax_clickmax__buyers_purchases_list` to check active commitments before deleting a card, then `mcp__plugin_clickmax_clickmax__buyers_card_delete` only when removal is explicit.

## Report

- Open with the scope: current plan, usage, billing history, upgrade options, pending changes, or cancellation impact.
- Order the answer: current state -> relevant metrics/history -> next action options.
- When showing current usage/limits, render a `cx-limits` card — one `cx-row` per resource with `label` (friendly resource name), `value` = `used/limit` (e.g. `1/2`, or `1 / Ilimitado` for unlimited), and `pct` = the usage percentage (omit `pct` for unlimited). The card draws a usage bar per resource (green → amber → red as it fills) and a "% utilizado" readout. Use friendly names in the user's language (Funis, Páginas, Quizzes, Produtos, Leads, Automações, Área de membros, Projetos, Domínios, Assentos, Créditos, Envios de e-mail/SMS/WhatsApp…), never the raw metric key. List resources with a defined numeric limit first; you may omit purely unlimited ones if the list is long. When any resource is at its limit, add an upgrade `cx-cta action="open-page" path="/settings/plan"` beneath the card.
- For cancellation preview or cancellation result, state scheduled effects such as expiration timing or pending access changes when returned.
- Treat follow-up mutations as opt-in only unless the user explicitly asked to cancel.

## Warnings

- Do not use customer subscription tools here.
- The cancel tool is destructive and self-scoped to the caller's own workspace plan — there is no separate admin/cross-workspace variant to reach for.
- `buyers_card_delete` is destructive; check `buyers_purchases_list` first and confirm before deleting a card backing an active commitment.

## Anti-patterns

- Canceling without preview when the user is still evaluating options.
- Mixing workspace SaaS billing with seller revenue operations.
- Reaching for a `plans_admin_*` tool — it does not exist; the cancel tool already only affects the caller's own workspace.

---

Clickmax skill revision: `b8294822a4d6`
