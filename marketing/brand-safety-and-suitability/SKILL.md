---
name: brand-safety-and-suitability
description: Protect the brand and the spend across any DSP with pre-bid and post-bid verification, MFA avoidance, invalid-traffic and ad-fraud controls, suitability tiers, regulated-category rules, and supply-path transparency. Use when the user asks about brand safety, brand suitability, made for advertising, MFA, invalid traffic, ad fraud, GIVT vs SIVT, sellers.json, ads.txt, app-ads.txt, the SupplyChain object, supply path optimization or transparency, the GARM framework, or running regulated category ads (pharma, financial, alcohol, gambling, political, children and COPPA on CTV).
---

# Brand safety and suitability

Keep ads off content that damages the brand and out of inventory that wastes the spend, without paying twice for the same control. This skill is DSP-agnostic: it encodes the verification model, the quality thresholds, the regulated-category rules, and the supply-path signals an experienced trader applies on any platform. It owns the cross-platform lens and the open-standard mechanics (ads.txt, sellers.json, the SupplyChain object, the industry suitability framework).

For shared definitions (CPM, viewability, the MRC viewable standard, IVT terminology), see the `programmatic-foundations` skill. For where each control physically lives in DV360 and how to set advertiser-level floors, see the `dv360-frequency-and-brand-safety` skill. For consent, regional privacy law, and what identity signals you may use, see the `privacy-and-consent` skill.

## When to use this skill

Use when the user wants to:

- Decide between pre-bid avoidance and post-bid measurement, or audit whether they are paying for both on the same risk.
- Cut made-for-advertising (MFA) inventory or understand why so much spend leaks before it reaches a consumer.
- Reason about ad fraud and invalid traffic: general invalid traffic (GIVT) versus sophisticated invalid traffic (SIVT), and what filtration covers.
- Set suitability tiers or apply the industry brand-safety floor and suitability framework, including its post-2024 stewardship.
- Run a regulated category (pharmaceutical, financial, alcohol, gambling, political) or anything touching children and COPPA, especially on connected TV.
- Tighten the supply path: read ads.txt and app-ads.txt, verify sellers.json, require a SupplyChain object, or run supply-path optimization (SPO).

Boundary with sibling skills:

- For the DSP-specific control surface (digital content labels, sensitive categories, exclusion lists, Active View, where to set advertiser floors), use `dv360-frequency-and-brand-safety` or the matching platform skill. This skill owns the cross-platform model and open standards; that skill owns the click path.
- For consent, GDPR, the California privacy law, and identity-signal eligibility, hand off to `privacy-and-consent`.
- For inventory packaging and deal mechanics, use the platform inventory skill (for example `dv360-deals-and-inventory` or `ttd-inventory-and-deals`).

## Quick reference

| Goal | Control | Layer |
| --- | --- | --- |
| Never pay for objectionable or unsafe inventory | Pre-bid avoidance segment or native exclusion | Targeting, before the auction |
| Get an independent measured quality number | Post-bid verification tag | Measurement, after the impression |
| Cut arbitrage and low-attention junk | MFA avoidance: domain lists, attention or made-for-advertising filters | Pre-bid targeting plus exclusion lists |
| Remove bots and non-human traffic | IVT filtration (GIVT and SIVT) plus accredited third party | Mostly automatic; verify in reporting |
| Align inventory to brand tolerance | Suitability tier (floor plus dial) | Account-level floor, line-item dial |
| Keep a regulated category compliant | Geo and audience gating, certification, content rules | Campaign setup plus legal sign-off |
| Verify who is really selling the impression | ads.txt, app-ads.txt, sellers.json, SupplyChain object | Supply-path policy and SPO |

## Core process

1. **Separate the floor from the dial before touching settings.** Brand safety is the floor: content almost every advertiser rejects (illegal, hateful, graphic, fraudulent). Brand suitability is the dial: how much risk one brand tolerates relative to its tone. Set the safety floor once at the highest account level so it applies everywhere and cannot be loosened below, then tune suitability per campaign. Conflating the two leads to either reckless placement or needless reach loss.

2. **Choose pre-bid avoidance or post-bid measurement per risk, and never pay for both on the same control.** Pre-bid avoidance (an accredited segment or native exclusion in targeting) stops you bidding on inventory that fails the rule, so you never pay for the bad impression. Post-bid measurement (a verification tag) reports quality after delivery but does not prevent the buy. If you already enforce a category pre-bid, do not also pay a post-bid fee to measure that same category. Use pre-bid to control spend; use post-bid only to satisfy an independent-measurement contract or to monitor a risk you deliberately did not block.

3. **Cut MFA early, because it passes viewability and brand-safety checks while wasting budget.** Made-for-advertising sites are built to arbitrage cheap traffic into ad-dense pages. They often clear viewability and safety filters yet deliver almost no attention or outcome. The ANA programmatic transparency study found MFA was a large share of impressions (about 15% in its 2023 baseline). Filter MFA with a domain exclusion list, an MFA or attention signal from an accredited vendor, and supply-path discipline. Watch for a campaign that looks healthy on viewability but flat on outcomes; that pattern is the MFA tell.

4. **Treat invalid traffic as filtered by default, then verify the number.** General invalid traffic (GIVT) is known bots, crawlers, and data-center traffic removed by routine filtration lists. Sophisticated invalid traffic (SIVT) is harder: hijacked devices, falsified or spoofed inventory, bot nets that mimic humans, and requires behavioral analysis. Major DSPs and SSPs filter both pre-bid (never bought) and post-serve (credited back). You confirm filtration in reporting; you add an accredited third-party measurement only when a client requires an independent IVT figure. Pre-bid SIVT detection is never perfect, so pair it with supply-path hygiene that removes the spoofable inventory in the first place.

5. **Set the suitability tier with the industry framework, and know who stewards it now.** The industry has long used a shared brand-safety floor plus a suitability framework that grades sensitive content (for example adult, arms, crime, death or injury, hate speech, terrorism, and similar categories) into avoid, low, medium, and high suitability. The Global Alliance for Responsible Media (GARM), which authored that framework under the World Federation of Advertisers, was discontinued in August 2024. The framework definitions live on inside vendor products and buyer-specific policies; the WFA noted its tools had supported brand owners in building their own bespoke frameworks. There is no single named successor body. Treat the GARM tiers as a still-useful common vocabulary, but pin the actual enforced definitions to your verification vendor and the IAB Tech Lab Content Taxonomy rather than to a live GARM standard. Verify any current-state claim before asserting it.

6. **Gate regulated categories before launch, with legal sign-off, not as an afterthought.** Pharmaceutical, financial, alcohol, gambling, and political advertising carry platform policies and jurisdiction-specific law. Children's advertising adds COPPA. Apply geo and audience gating, age controls, required certifications or pre-clearance, and the platform's category policy at setup, and route the creative and targeting through legal or compliance review. See Decision rules for the per-category checklist.

7. **Tighten the supply path so you buy from the real seller.** Require authorized paths only: ads.txt for web and app-ads.txt for apps declare which sellers a publisher authorizes; sellers.json plus the OpenRTB SupplyChain object let you trace every intermediary on a bid request back to the publisher. Run supply-path optimization (SPO) to prefer the shortest authorized path to each publisher, which cuts fees, removes resold and spoofed inventory, and starves MFA and fraud of demand. See Decision rules for the pass and fail conditions.

## Decision rules and thresholds

- **Floor everywhere, dial per campaign.** Put the universal safety exclusions at the top account level. Tune suitability tier by campaign tone: a family brand sits near avoid or low tolerance; an edgy brand can accept medium. Never loosen the floor at a lower level expecting it to take effect; account-level floors bind downward.

- **One pre-bid source per risk category.** Layering a native exclusion, a DoubleVerify segment, and an IAS segment on the same risk wastes fees and over-filters into under-delivery. Pick one accredited pre-bid control per risk; add post-bid only for independent measurement.

- **MFA filter posture.** Default to excluding known MFA domains and enabling an accredited MFA or made-for-advertising avoidance segment on performance and most awareness buys. Relax only for a specific tactic where cheap reach is explicitly acceptable and outcomes are not the KPI.

- **IVT escalation.** If post-serve IVT credits or third-party SIVT readings rise above the low single-digit percentages typical of clean supply, stop scaling, pull the offending domains, sellers, and deal IDs, and shift budget toward shorter authorized paths. Do not simply re-target; remove the source.

- **Regulated-category checklist (apply the ones that fit, with legal sign-off):**
  - **Pharmaceutical:** prescription-drug rules vary by country; many markets restrict or ban direct-to-consumer promotion. Gate by geo, require fair-balance or safety information where mandated, and confirm platform certification where required.
  - **Financial:** licensing and disclosure requirements; gate offers by jurisdiction and confirm regulated-entity status before serving.
  - **Alcohol:** age-gate the audience, restrict geos that prohibit it, and meet minimum-age-audience-composition standards where platforms require them.
  - **Gambling:** allowed only in licensed jurisdictions; require the operator license, age-gate, and exclude prohibited regions and self-excluded users.
  - **Political:** identity and authorization verification, paid-for disclosure, and a public ad record where required; blackout windows and registration vary by jurisdiction.
  - **Children and COPPA on CTV:** if the audience or content is directed to children under 13, COPPA applies. The FTC rule (amended in 2025) requires verifiable parental consent before collecting a child's personal information and separate consent to disclose it to third parties for targeted advertising, expands personal information to include biometric and government identifiers, and limits data retention. On connected TV, treat child-directed inventory as no behavioral targeting and no personal-data collection: contextual only. When in doubt about whether content is child-directed, treat it as if it is.

- **Supply-path pass and fail conditions.**
  - **Pass:** the seller appears in the publisher's ads.txt or app-ads.txt for the domain or bundle; the seller's sellers.json entry resolves and matches the seller ID on the bid request; the SupplyChain object is complete (`complete: 1`) with every node named.
  - **Fail (drop or deprioritize):** seller absent from ads.txt or app-ads.txt for that property; sellers.json entry missing or mismatched; an incomplete SupplyChain object; or more intermediaries than the shortest authorized path you already have to that publisher. Prefer the direct or shortest authorized path under SPO.

## Reference material

This skill is self-contained. For platform-specific exclusion mechanics and where controls live, read the `dv360-frequency-and-brand-safety` skill (or the matching platform skill). For consent and identity-signal eligibility, read `privacy-and-consent`.

## Templates and examples

**Performance buy, open web.** Account-level safety floor excludes the universal categories. Suitability tier set to low for a mainstream retail brand. One accredited pre-bid avoidance segment for the brand's named risks. MFA exclusion list plus an MFA avoidance segment on. SPO set to prefer direct and shortest authorized paths; drop any seller failing the ads.txt or sellers.json check. No post-bid tag, because nothing here requires an independent measured number.

**Premium video with a mandated vendor.** Suitability tier set to the stricter medium-minus for an automotive brand near sensitive news. The client-mandated DoubleVerify or IAS pre-bid segment carries the named categories. A post-bid verification tag runs only because the contract requires an independent measured figure, not to re-block what the pre-bid segment already blocks. Require complete SupplyChain objects and authorized-only paths.

**Regulated alcohol campaign, two markets.** Age-gated audience and minimum-age composition where the platform enforces it. Geos that prohibit alcohol advertising excluded. Creative and targeting cleared by legal before launch. Standard safety floor plus suitability set to avoid adjacency with content depicting minors or excess. Authorized-only supply paths.

**Child-directed CTV app inventory.** Contextual targeting only, no audience segments, no behavioral data, no personal-data collection from the device. Confirm the app or content is handled as child-directed under COPPA and that any data flow has verifiable parental consent upstream. If consent cannot be confirmed, do not run behavioral; keep it contextual.

## Common pitfalls

- Paying for pre-bid avoidance and post-bid measurement on the same risk category. Pick pre-bid to control spend; add post-bid only for an independent number.
- Judging a campaign healthy on viewability while outcomes stay flat. That is the MFA and low-attention pattern; check the domain list and add MFA avoidance.
- Treating GARM as a live standard. The body was discontinued in August 2024; the tier vocabulary survives, but pin enforced definitions to your vendor and the IAB Content Taxonomy, and verify current state before asserting it.
- Assuming IVT filtration is total. SIVT detection is imperfect; remove spoofable supply via ads.txt, sellers.json, and SPO rather than relying on filtration alone.
- Stacking redundant third-party segments on top of native exclusions, over-filtering into under-delivery.
- Bolting regulated-category controls on after launch. Gate by geo, age, and certification at setup with legal sign-off; political and gambling especially carry hard legal lines.
- Buying unauthorized or long resold paths. Require ads.txt or app-ads.txt authorization and a complete SupplyChain object, and prefer the shortest authorized path.
- Running behavioral targeting on child-directed CTV. Under COPPA, keep child-directed inventory contextual unless verifiable parental consent is confirmed.

## Sources

- WFA discontinues GARM: https://wfanet.org/knowledge/item/2024/08/09/wfa-discontinues-garm (as of June 2026)
- GARM at the World Federation of Advertisers: https://wfanet.org/leadership/garm (as of June 2026)
- IAB Tech Lab Content Taxonomy: https://iabtechlab.com/standards/content-taxonomy/ (as of June 2026)
- IAB Tech Lab ads.txt and app-ads.txt: https://iabtechlab.com/ads-txt/ (as of June 2026)
- IAB Tech Lab sellers.json and SupplyChain object: https://iabtechlab.com/sellers-json/ (as of June 2026)
- ANA Programmatic Media Supply Chain Transparency Study: https://www.ana.net/miccontent/show/id/rr-2023-12-ana-programmatic-media-supply-chain-transparency-study (as of June 2026)
- FTC Children's Online Privacy Protection Rule (COPPA): https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa (as of June 2026)
- FTC finalizes changes to the Children's Privacy Rule (2025 amendments): https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-finalizes-changes-childrens-privacy-rule-limiting-companies-ability-monetize-kids-data (as of June 2026)
