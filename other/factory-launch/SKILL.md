---
name: factory-launch
description: Launch the factory's control plane — scaffold and fill FACTORY-ORDERS (weekly mandate + hard budget), STANDING-ORDERS (autonomous-program authority), HEARTBEAT (weekly pulse), and write lifecycle gates for every registered product. A deliberate one-time ritual (re-run to audit); invoke as /factory-launch, not auto-triggered.
---

# /factory-launch — set up the factory's control plane

The moment Hamzaish goes from "a repo with skills" to "a running factory": bounded
unattended work, a formal authority model, and numeric kill gates. Everything here is
operator-local (`.local` files, gitignored) — this is YOUR control plane, not the repo's.

## Preconditions

- `bun run setup` has been run (it scaffolds the three `.local` files from the `.example`
  templates at the repo root; re-run it if they're missing — it never overwrites).

## The walkthrough (one step at a time; confirm before moving on)

1. **FACTORY-ORDERS.local.md — the mandate.** Open it with the operator. Fill:
   - the Mandate section: 1–3 lines, each naming a product + the gate it's chasing this week;
   - the Budget section: the weekly dollar cap for ALL unattended work (suggest $25–50 to
     start — the cap is a feature, not a limitation: scarcity forces scoping).
   Explain: unattended sessions read this file FIRST and refuse work outside it.

2. **STANDING-ORDERS.local.md — the authority table.** Read the three programs
   (overnight-build, gtm-draft, heartbeat) aloud in summary. Confirm the operator accepts
   the iron law: *agents research and draft; the operator publishes, sends, pays.* Any
   scope widening is their explicit, dated edit — never yours.

3. **HEARTBEAT.local.md — the pulse.** Confirm the weekly cadence (default: Monday, before
   the operator's pulse block). Offer to schedule it (cron/scheduled task) or leave it
   manual (`run the HEARTBEAT checklist` in a fresh session).

4. **Gates for every registered product.** Run `bun run check-gates`. For each registered
   product flagged `NO GATES ✗`, write the `gates` block into its `product.config.json`
   with the operator — states-and-dates, channel-matched (see the gate ladder in
   FACTORY-ORDERS.example.md's pointer, or default: validation +4w · launch +30d ·
   traction +90d · pmf +6mo). Dates are absolute (YYYY-MM-DD). The operator sets the
   states; you propose channel-matched defaults. WIP caps to confirm while you're here:
   1 active build · 2 active GTM · rest autopilot.

5. **Verify.** `bun run check-gates` exits 0 and the dashboard shows every registered
   product with a next gate. `bun test ./scripts/control-plane-templates.test.ts` passes.
   Show the operator the dashboard. Done = both green, mandate + cap filled.

## Completion criteria (checkable — no "looks done")

- [ ] All three `.local` control-plane files exist, mandate + weekly cap filled (non-placeholder)
- [ ] `bun run check-gates` → exit 0 (every registered product has a valid gates block)
- [ ] Operator has confirmed the iron law and the WIP caps out loud

## Anti-patterns

- Filling the mandate/budget FOR the operator with invented numbers — the whole point is
  their precommitment, not yours.
- Writing gates a product can't measure (name the metric's source: Stripe, PostHog, GSC).
- Treating this as config to rush through — it's the factory's constitution; 20 minutes
  done honestly beats 5 minutes done cosmetically.
