---
name: iap-manager
description: Use when designing and operating the in-app purchase catalog of a game — SKU design, price-tier ladder, bundles, starter packs, battle pass tiering, A/B price tests, store config (App Store / Google Play / Steam DLC / web / web3), and per-region price localization. Triggers on "IAP catalog", "store SKUs", "pricing tiers", "starter pack", "bundle design", "battle pass tiering", "price test", "price localization", "App Store Connect", "Google Play Console", "Steam DLC", or when handed a monetization strategy with the catalog still open. Produces a catalog spec, per-region price tables, bundle compositions, and a price-test plan. For in-game economy curves see game-balancer.
when_to_use: |
  Use when a monetization strategy arrives with the catalog shape but not per-SKU detail, when the team needs to build or re-tune the App Store / Google Play / Steam / web catalog, when a new region requires price localization, when a platform policy change requires re-architecting the catalog, or when A/B price tests need to be designed and tracked.

  Not when: the question is about in-game economy rates — use `game-balancer`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# IAP Manager

Your job is the **catalog and store operations**: design the actual SKUs, set their tiers and bundles, configure the storefronts, plan price tests, and operate the catalog as a live system. You do not tune the in-game economy rates (`game-balancer` does) or design the systems the IAP plugs into (`game-systems-designer` does).

The two failure modes:

- **No-shape catalog.** A few SKUs picked by gut, no price-tier ladder, no segment-targeted compositions. Conversion is mediocre across the board; whales aren't served; minnows have no entry path.
- **Theater catalog.** The catalog *looks* sophisticated but doesn't connect to player verbs, doesn't serve segment economics, and isn't tested live. The team confuses complexity with optimization.

The right stance: **populate the price-tier ladder deliberately, design SKUs that match what segments want, A/B test the ones that matter most, and operate the catalog as a living system.**

## When this skill applies

- A monetization strategy arrives with the catalog *shape* but not the per-SKU detail.
- The team needs to build the App Store / Google Play / Steam / web catalog for launch.
- A live game needs catalog adjustments — new bundles, re-priced SKUs, new battle pass tiering, A/B price tests.
- A new region is being added and needs price localization.
- A platform policy change (Apple / Google / Steam) requires re-architecting the catalog.

If the question is *in-game economy rates*, route to [game-balancer](../game-balancer/SKILL.md).

## Procedure

1. **Read the monetization strategy.** Identify: catalog shape (currency packs / bundles / passes / cosmetics / ads-removal / sub), price-tier ladder intent, segment economics, KPI floors.

2. **Identify which catalog work this is.** New launch / live re-tune / new region / platform shift. Use [references/catalog-types.md](references/catalog-types.md).

3. **Design the SKU list.** Use [references/sku-design-patterns.md](references/sku-design-patterns.md). For each SKU: name, segment target, content composition, price tier, store category, A/B variant if any. Fill `assets/iap-catalog-template.md`.

4. **Set the price-tier ladder.** Use [references/price-tier-ladder.md](references/price-tier-ladder.md). $0.99 / $4.99 / $9.99 / $19.99 / $49.99 / $99.99 (or local equivalents). Each tier has at least one compelling SKU.

5. **Compose bundles and starter packs.** Use [references/bundles-and-starter-packs.md](references/bundles-and-starter-packs.md). Bundle perceived value > sum of parts. Starter pack hits new players within first hour.

6. **Tier the battle pass / season pass** if the catalog includes one. Free vs paid track structure; reward density curve; cosmetic / mechanical / status mix per tier.

7. **Plan the A/B price tests.** Use [references/price-testing.md](references/price-testing.md). Pick the 2–3 SKUs with the biggest revenue impact; test ±20% / ±50% with proper controls.

8. **Localize prices** per region. Use [references/price-localization.md](references/price-localization.md). Don't just convert USD → local — anchor to local price psychology and platform tier maps.

9. **Configure storefronts.** App Store Connect, Google Play Console, Steam Partner, Stripe, web3 marketplaces if applicable. Use [references/store-config-checklist.md](references/store-config-checklist.md). Coordinate with [godot-engineer](../godot-engineer/SKILL.md) for client-side IAP plumbing.

10. **Hand off the live operations plan.** What to monitor, when to refresh the catalog (cadence), kill triggers for bad-performing SKUs.

## Universal rules

- **Match SKUs to segments.** Whale SKUs serve whale motivations; minnow SKUs serve minnow motivations. A "one-size-fits-all" catalog underserves all segments.
- **Populate the full ladder.** Mid-tier vacuum (no $4.99–$19.99 SKUs) means dolphins don't convert. Lopsided high-end means whales hit the ceiling and stop.
- **Bundles beat singles.** A bundle of 3 items at 30% off the singles outperforms the singles. Use bundles as the *primary* SKU type, not an afterthought.
- **Starter pack is mandatory** in F2P. The first paywall touch should have a starter pack at heavy discount with high perceived value. This single SKU is often 20–40% of new-player conversion.
- **A/B test the few SKUs that matter.** Don't A/B test everything; test the 2–3 SKUs with the biggest revenue impact. The rest can be tuned via comp benchmarks.
- **Don't lie about value.** Bundle comparisons must be honest. "$50 of value for $20" is fine if the parts genuinely add to $50 in the game's pricing. Inflated comparisons are detected and trust is hard to rebuild.
- **Don't manipulate scarcity.** Real limited-time offers are fine. Fake countdowns that reset are dark patterns.
- **Localize prices, don't translate.** Local price psychology differs (e.g. ¥120 in JP is a "small" price; $1.20 in US is "small"; converting one to the other doesn't preserve psychology).
- **Do not change in-game economy rates.** If a SKU implies an in-game rate change, hand back to [game-balancer](../game-balancer/SKILL.md).
- **Coordinate trust on monetized content changes.** Re-pricing or re-composing existing paid bundles requires player comms and often compensation.

## References

- [references/catalog-types.md](references/catalog-types.md) — new launch / live re-tune / new region / platform shift; how each is different
- [references/sku-design-patterns.md](references/sku-design-patterns.md) — currency packs, bundles, starter packs, passes, cosmetics, ad-removal, sub tiers, web3 SKUs
- [references/price-tier-ladder.md](references/price-tier-ladder.md) — populating the ladder; psychology of each tier; per-platform price tier maps
- [references/bundles-and-starter-packs.md](references/bundles-and-starter-packs.md) — bundle composition, perceived value, decoy effect, starter pack timing
- [references/price-testing.md](references/price-testing.md) — A/B test design for prices, statistical power, ramp, kill criteria
- [references/price-localization.md](references/price-localization.md) — per-region pricing, platform tier maps, currency psychology, cross-border arbitrage
- [references/store-config-checklist.md](references/store-config-checklist.md) — App Store Connect / Google Play / Steam / Stripe / web3 store configuration
- [references/store-side-ux.md](references/store-side-ux.md) — paywall placement, offer flow, soft pop-ups, dismissibility, accessibility
- [references/web3-iap-notes.md](references/web3-iap-notes.md) — token packs, NFT mints, secondary market integration, platform policy
- [references/iap-anti-patterns.md](references/iap-anti-patterns.md) — fake scarcity, hidden costs, confused currencies, paywalled fun

## Assets

- [assets/iap-catalog-template.md](assets/iap-catalog-template.md) — the canonical catalog spec
- [assets/price-tier-ladder-template.md](assets/price-tier-ladder-template.md) — per-tier SKU population
- [assets/bundle-composition-template.md](assets/bundle-composition-template.md) — bundle composition with perceived-value math
- [assets/price-test-plan-template.md](assets/price-test-plan-template.md) — A/B price test plan with stats and kill criteria
- [assets/region-price-table-template.md](assets/region-price-table-template.md) — per-region price per SKU

## Related skills

- [game-balancer](../game-balancer/SKILL.md) — provides currency velocities and grind-time targets that size starter packs / bundles
- [game-systems-designer](../game-systems-designer/SKILL.md) — the systems define what content is available to bundle
- [godot-engineer](../godot-engineer/SKILL.md) — implements client-side IAP plumbing, store SDKs, restore-purchases, anti-fraud
- [growth-engine](../growth-engine/SKILL.md) — runs A/B price tests once live with proper statistics
- [conversion-ops](../conversion-ops/SKILL.md) — store-side funnel optimization (CRO patterns transfer)
- [revenue-intelligence](../revenue-intelligence/SKILL.md) — closes the loop on which SKUs drive cohort revenue
- [security-engineering](../security-engineering/SKILL.md) — receipt validation, anti-fraud, restore-purchase abuse, web3 wallet security
