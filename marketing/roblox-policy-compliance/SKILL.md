---
name: roblox-policy-compliance
description: Review Roblox platform policy and compliance risk. Use for Community Standards, advertising rules, Roblox Economy rules, paid random rewards or gacha odds disclosure, maturity and age labels, IP, privacy, off-platform links, scams, moderation risk, and pre-publish compliance checks.
---

# Roblox Policy Compliance

## Goal

Reduce moderation, takedown, trust, and legal risk. Roblox policies can change, so verify current official Roblox rules before final compliance advice.

## Source Rule

For policy-sensitive work, check official Roblox sources before giving final advice. Prefer:

- Roblox Community Standards.
- Roblox Creator Hub publishing, monetization, advertising, and promotion docs.
- Roblox Terms, privacy, subscription, advertising, and restricted content policies when relevant.

If current official sources cannot be checked, state that limitation clearly and treat the answer as a non-final risk review.

## High-Risk Areas

Review:

- Paid random items, loot boxes, gacha, pet eggs, drop tables, and odds disclosure.
- Developer products, subscriptions, game passes, and premium benefits.
- Advertising claims, sponsored content, branded content, and influencer disclosure.
- Maturity labels, age suitability, restricted content, horror, violence, gambling-like mechanics, and regulated goods.
- Off-platform links, Discord/social links, personal information, and privacy.
- Intellectual property, copied assets, music, logos, brands, and user-generated content.
- Scams, misleading content, fake rewards, fake scarcity, and impersonation.
- Trading, gifting, currency, and player-to-player value exchange.

## Compliance Review Workflow

1. Identify the feature, audience, monetization, data collected, and player value involved.
2. Check current official Roblox policy for each high-risk area.
3. Map concrete risks to specific game surfaces.
4. Recommend design or copy changes.
5. Add a pre-publish checklist item when the risk can recur.

## Output

Return:

- Policy areas checked.
- Risk level.
- Required or recommended changes.
- Unresolved policy questions.
- Official sources used.

## Next

Apply any required disclosures to the store page with `roblox-publishing-discovery`, and gate the build on the compliance checklist in `roblox-release-operations`.
