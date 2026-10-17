---
name: partner-and-advertiser-onboarding
description: Take a new client from a signed insertion order to first-campaign-ready as a gated, ordered onboarding sequence. Use when the user asks how to onboard a new advertiser, new client setup, an intake checklist, the kickoff, getting a client first-campaign-ready, or billing setup. Covers intake, partner and advertiser provisioning, Campaign Manager 360 link verification, billing and PO and currency and timezone confirmation, seat and data-partner provisioning, brand-safety floor inheritance, and the kickoff handshake.
---

# Partner and advertiser onboarding

The deliverable is a new client moved from a signed insertion order to first-campaign-ready, with every account, link, billing, access, and safety prerequisite confirmed before a single campaign is built. Onboarding is a gate, not a formality: a brand-safety floor that did not inherit, a currency or timezone set wrong, a Campaign Manager 360 link that never synced, or a billing profile chosen wrong all surface as mis-delivery, broken measurement, or a suspended account once spend starts, and unwinding them after launch is far more expensive than confirming them now.

This is the operational onboarding sequence shared across the team. For the account architecture and naming taxonomy this sequence stands up, see the `dv360-account-setup-and-taxonomy` skill. For the pre-launch QA that gates the first campaign at go-live, see the `dv360-launch-qa` skill. For the kickoff deck, intake summary, and client-facing artifacts, see the `client-deliverable-templates` skill.

## When to use this skill

- "Onboard a new advertiser" or "new client setup" or "set up a new account."
- "I need an intake checklist" or "what do we collect before we build anything?"
- "Run the kickoff" or "what happens at the kickoff handshake?"
- "Get this client first-campaign-ready" or "what is left before we can launch?"
- "Billing setup" or "confirm the billing profile, PO, currency, and timezone."

Boundary: this skill is the ordered onboarding sequence and its gates. The naming convention, role matrix, and governance defaults it applies are owned by `dv360-account-setup-and-taxonomy`. The line-by-line pre-launch sign-off for the first campaign is `dv360-launch-qa`. The kickoff deck and intake-summary templates are `client-deliverable-templates`. This skill sequences and gates the work; those skills own the depth at each step.

## Quick reference: the onboarding gates

Work top to bottom. Each gate must pass before the next, because a downstream step built on an unconfirmed upstream gate has to be redone.

| # | Gate | First-campaign-ready means |
| --- | --- | --- |
| 1 | Intake | Goals, KPIs, definition of success, brand-safety requirements, approval chain, and reporting cadence captured and confirmed with the client |
| 2 | Partner and advertiser setup | Partner mapped to the billing entity, advertiser created for the brand, named to the taxonomy |
| 3 | Campaign Manager 360 link | Floodlight configuration shared and the advertiser linked, sync confirmed |
| 4 | Billing, PO, currency, timezone | Correct billing profile selected, PO recorded, currency and timezone confirmed against the buy |
| 5 | Seat and data-partner provisioning | User seats granted at least privilege, data and measurement partners provisioned |
| 6 | Brand-safety floor inheritance | The exclusion floor is set and confirmed inherited onto the advertiser |
| 7 | Kickoff handshake | Roles, cadence, approvals, and the path to first campaign agreed with the client and the team |

Rule of thumb: nothing about a campaign is touched until gates 1 through 6 are confirmed and gate 7 has aligned the client and the team. The cheap-looking confirmations (currency, timezone, that the floor actually inherited) are exactly the ones that, if skipped, mis-deliver or break measurement silently once spend starts.

## Core process

1. **Run intake before anything is provisioned.** Capture, in writing and confirmed back with the client: the business goals, the KPIs and the definition of success for each, the brand-safety requirements (suitability tier, categories and content to exclude, any blocked domains or apps), the approval chain (who approves creative, budget, and go-live), and the reporting cadence and format. Intake is the contract the rest of onboarding and every future campaign is measured against, so an ambiguous KPI or an unstated brand-safety requirement caught here is cheap and caught later is a mis-served campaign. Summarize intake using the `client-deliverable-templates` skill and get explicit sign-off.
2. **Map and create the partner and advertiser.** Map one partner to the billing and trading entity and create one advertiser per real-world brand, named to the convention before creation (renaming after reporting accrues breaks historical filters). Do not split one brand across advertisers for convenience, because audiences, brand controls, and conversion data do not move freely across advertisers and you will fragment measurement permanently. The partner-versus-advertiser map, the naming taxonomy, and what lives where are owned by `dv360-account-setup-and-taxonomy`.
3. **Verify the Campaign Manager 360 link.** Where conversions and creatives live in CM360, share the Floodlight configuration from the CM360 advertiser and use it to create or connect the DV360 advertiser, then confirm the link actually synced: audience lists and creatives appear on the DV360 side, allowing for sync lag. This link is effectively permanent once made, so confirm you are linking the right CM360 advertiser before connecting, not after. A campaign optimizing to conversions with a broken or wrong link learns nothing.
4. **Confirm billing, PO, currency, and timezone.** Select the correct billing profile for the advertiser (it carries the paying organization and the invoice currency), record the purchase order number, and confirm the currency and timezone match the buy and the client's billing intent. Choosing the wrong billing profile causes billing delays and raises suspension risk, and a wrong timezone starts or ends every flight a day off, so treat all four as load-bearing confirmations, not defaults to accept. The timezone set here is the advertiser's billing timezone that flights and reporting will key off.
5. **Provision seats and data partners on least privilege.** Grant each user the narrowest role at the narrowest scope that lets them do their job, preferring advertiser-scoped roles over partner-scoped admin, and reserve API-capable roles for the people and service accounts that drive automation. Provision the data and measurement partners the plan needs (audience data partners, verification and viewability vendors, measurement integrations) so they are live before the first campaign rather than bolted on mid-flight. The role-by-capability matrix and least-privilege patterns are owned by `dv360-account-setup-and-taxonomy`.
6. **Set and verify the brand-safety floor inheritance.** Set the exclusion floor at the advertiser (digital content labels, sensitive categories, blocked domains and apps, keyword exclusions, authorized-seller posture) per the intake brand-safety requirements, then positively confirm it is inherited and applied, rather than assuming the default cascaded. A floor that was specified but did not inherit is the silent failure that lets the first campaign serve against exactly the content the client told you to avoid. Per-campaign suitability tuning is `dv360-frequency-and-brand-safety`; here you are confirming the inherited floor exists.
7. **Run the kickoff handshake.** Align the client and the delivery team on roles and contacts, the reporting cadence and format, the approval chain for creative and go-live, and the concrete path to the first campaign (what is owed by whom and by when). The kickoff converts a provisioned account into a working engagement; skipping it leaves approvals and cadence unsaid, which stalls the first launch. Use the `client-deliverable-templates` skill for the kickoff artifact.

After gate 7, the client is first-campaign-ready. The first campaign is then built and taken through the full pre-launch sign-off in `dv360-launch-qa` before go-live; onboarding gets the account ready, launch QA gates the campaign.

## Decision rules and thresholds

- **Intake is signed off before provisioning starts.** Goals, KPIs and definition of success, brand-safety requirements, approval chain, and reporting cadence in writing and confirmed. Provisioning against unconfirmed intake gets redone.
- **One partner per billing entity, one advertiser per brand.** Separate billing means separate partners; one brand never spans advertisers, because brand controls, audiences, and conversion data do not move across advertisers.
- **The CM360 link is verified by sync, not by setup.** Confirm audiences and creatives actually appear on the DV360 side. Confirm the correct CM360 advertiser before linking, because the link does not come undone.
- **Billing profile, PO, currency, and timezone are all confirmed, never defaulted.** A wrong billing profile risks suspension; a wrong timezone shifts every flight. Confirm all four against the buy.
- **Access is least privilege from day one.** Narrowest role at narrowest scope, advertiser-scoped over partner admin, API roles only where automation runs.
- **The brand-safety floor is confirmed inherited, not assumed.** A specified floor that did not cascade lets the first campaign serve against excluded content. Positively verify inheritance.
- **The kickoff is a gate.** Roles, cadence, approvals, and the path to first campaign agreed with both sides before the first build begins.

## Reference material

This skill sequences and gates; the depth at each step lives in the linked skills, so reach for them at the matching gate:

- Gates 2 and 5, account map, naming taxonomy, and the role matrix: `dv360-account-setup-and-taxonomy`.
- The first campaign's pre-launch sign-off after onboarding completes: `dv360-launch-qa`.
- Gates 1 and 7, the intake summary and kickoff artifacts: `client-deliverable-templates`.
- Per-campaign brand suitability and frequency once the floor is set: `dv360-frequency-and-brand-safety`.

## Templates and examples

Worked onboarding for a new direct advertiser, "ACME", running its own buy through an agency trading desk:

- **Gate 1, intake.** Goal: drive online sales. KPI: cost per order at or below the target, with revenue and ROAS as the definition of success; awareness reach as a secondary read. Brand safety: standard suitability tier, exclude news and user-generated content categories, block a named competitor-adjacent domain list. Approvals: client marketing lead approves creative and go-live; trading desk approves budget pacing. Reporting: weekly pacing snapshot, monthly business review. Signed off by the client in writing.
- **Gate 2, setup.** One partner for the trading desk's billing entity; one advertiser "ACME" named to the taxonomy (Brand | Market | ... ). Not split across two advertisers despite ACME running two markets, to keep measurement whole.
- **Gate 3, CM360 link.** ACME's conversions live in CM360; the Floodlight configuration is shared and the DV360 advertiser connected, then confirmed by seeing ACME's creatives and audience lists appear on the DV360 side after sync.
- **Gate 4, billing.** Billing profile selected with ACME's paying organization and USD currency; PO number recorded; timezone confirmed as ACME's billing timezone so flights key off the right day.
- **Gate 5, access and partners.** Trading desk traders get advertiser-scoped standard access; the analyst gets reporting only; the automation service account is scoped to ACME alone with an API-capable role. Verification vendor and audience data partner provisioned.
- **Gate 6, floor.** Exclusion floor set per intake and confirmed inherited onto the ACME advertiser, verified by inspecting the advertiser's brand controls rather than assuming the cascade.
- **Gate 7, kickoff.** Client and team align on the weekly and monthly cadence, the creative and go-live approval path, contacts on both sides, and that the first prospecting campaign is owed for build next, to be signed off through launch QA before it goes live.

## Common pitfalls

- **Provisioning before intake is confirmed.** Building an account against vague goals or unstated brand-safety requirements bakes in rework. Sign off intake first.
- **Splitting one brand across advertisers for convenience.** Audiences, brand controls, and conversion data do not move across advertisers, so this fragments measurement permanently. One brand, one advertiser.
- **Treating the CM360 link as done at setup.** Confirm the sync landed (creatives and audiences visible on the DV360 side) and that you linked the right CM360 advertiser, because the link is permanent.
- **Accepting billing, currency, or timezone as defaults.** A wrong billing profile risks suspension and a wrong timezone shifts every flight. Confirm all four against the buy.
- **Over-granting access to move fast.** Partner-scoped admin handed out for convenience violates least privilege. Scope to the advertiser and reserve API roles for automation.
- **Assuming the brand-safety floor inherited.** A specified floor that did not cascade is invisible until the first campaign serves against excluded content. Positively verify inheritance.
- **Skipping the kickoff.** An account can be fully provisioned and still stall at first launch because approvals and cadence were never agreed. Run the handshake before the first build.

## Sources

- Partners in Display & Video 360, Display & Video 360 Help: https://support.google.com/displayvideo/answer/7622449 (as of June 2026)
- Advertisers in Display & Video 360, Display & Video 360 Help: https://support.google.com/displayvideo/answer/2696883 (as of June 2026)
- Connect a Campaign Manager 360 advertiser to Display & Video 360, Display & Video 360 Help: https://support.google.com/displayvideo/answer/3155819 (as of June 2026)
- About Floodlight and Floodlight activities, Display & Video 360 Help: https://support.google.com/displayvideo/answer/3027419 (as of June 2026)
- Create a new billing profile, Display & Video 360 Help: https://support.google.com/displayvideo/answer/14984923 (as of June 2026)
- Select a billing profile for a new advertiser, Display & Video 360 Help: https://support.google.com/displayvideo/answer/14985648 (as of June 2026)
- Manage users in Display & Video 360, Display & Video 360 Help: https://support.google.com/displayvideo/answer/2723011 (as of June 2026)
- View and edit brand controls for your advertiser, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9179543 (as of June 2026)
- Brand suitability, Display & Video 360 Help: https://support.google.com/displayvideo/answer/3032915 (as of June 2026)
