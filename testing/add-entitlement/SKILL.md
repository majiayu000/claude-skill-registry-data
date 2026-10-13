---
name: add-entitlement
description: Put a feature behind a paid plan, or give plans a new limit. Use when the user wants something available only on Pro, or a per-plan quota.
argument-hint: <entitlement>
---

# Add an entitlement

Plans and what they allow are in `packages/contracts/src/billing.ts`; Stripe holds the
prices. With billing off, every organization has everything (`unlimited`).
docs/files-and-billing.md, "Plans and entitlements", has the model.

1. **Declare it** in `Entitlements`, and set it in every plan in `plans` and in
   `unlimited` (`false`/`true` for a feature, a number or `null` for a limit). The
   `satisfies` clauses fail `check-types` until each has it.
2. **Enforce it** where the feature is used, in the API:
   `await this.billing.require(orgId, "<entitlement>")` (`BillingService`, apps/api),
   which throws `ENTITLEMENT_REQUIRED`. A limit is checked where the count grows, like
   `members` in `apps/api/src/auth/auth-plugins.ts`.
3. **Show it** in the clients from `billing.overview`: hide the feature or show
   `UpgradeHint` (`apps/web/src/modules/billing/components/upgrade-hint.tsx`), with its
   copy in every catalog.
4. **Test** in `apps/api/test/billing.integration.test.ts` (against the fake Stripe): a
   free organization gets `ENTITLEMENT_REQUIRED`, a paying one gets through, and with
   billing off everyone does.
5. Update the plans table in `docs/files-and-billing.md`.

## Done when

`bun run check-types`, `bun run test` and `bun run test:integration` pass, and the
`reviewer` agent reports nothing blocking.
