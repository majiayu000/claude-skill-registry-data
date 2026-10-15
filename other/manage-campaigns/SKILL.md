---
name: manage-campaigns
description: "Use when the user asks to change something in a live Meta or Google Ads account: pause or enable, rename, change a bid or bid strategy, edit targeting or schedule, update ad copy, URLs or tracking, add sitelinks or other assets, adjust device, location or ad-schedule modifiers, edit PMax asset groups, or run, end or apply an experiment. Picks the right GoMarble propose tool, shows the exact change, and applies it only after the user approves."
---

# Manage campaigns

Make any account change safely: the right tool, the exact edit, the user's yes, then the change. For budget moves use `shift-budget`, for exclusions and negatives `clean-wasted-spend`, and for new campaigns `launch-campaigns`. For TikTok changes see `tiktok-ads`.

## The flow for every change

1. **Read current state first.** Campaigns change often, so never propose from stale data.
2. **Check the rules.** Read `meta-guardrails` or `google-ads-guardrails`. For Google mutations, `google-ads-create-master-skill` is the master reference. For Meta changes, `meta-agent-operations`.
3. **Dry run.** Call the propose tool with one item per field change, so each can be approved on its own. Pass money in account currency with `currency_code`.
4. **Show the change.** For each item: the entity, current value, new value, and why. Warn when it matters: a bid strategy change resets learning; budget increases over 100% or cuts over 50%; daily vs lifetime budget; pausing stops delivery immediately.
5. **Apply only on an explicit yes.** Call the same tool with `mode: "live"`, the `account_id` and only the approved `operation_ids`. Don't resend the fields. GoMarble doesn't double-check that the user agreed, so that yes must come from the user in this conversation.
6. **Confirm** what changed. For Google, the live call runs Google's validation first; if it rejects, explain the error rather than retrying blindly.

## Meta Ads

| Change | Read first | Propose with |
|---|---|---|
| Campaign status, name, bid strategy, spend cap, budget, per-ad-set bid amounts | `facebook_get_campaign_details` | `facebook_propose_update_campaigns` |
| Ad set status, targeting, schedule, optimization goal, bid, frequency cap, attribution | `facebook_get_adset_details` | `facebook_propose_update_adsets`. Targeting is a **full replacement**: send the whole targeting spec. You can't switch between manual and Advantage+ placements. |
| Ad status, name, URL tags, tracking, destination or CTA | `facebook_list_ads` | `facebook_propose_update_ads`. Turning a paused ad on needs its `thumbnail_url`. Images and videos can't be swapped on an existing ad. |
| Creative name or status | `facebook_get_ad_creative_details` | `facebook_propose_update_ad_creatives` (name and status only) |
| Creative text | `facebook_get_ad_creative_details` | `facebook_propose_clone_ad_creative` with the new text. Meta doesn't allow editing text in place. |
| Duplicate a campaign, ad set or ad | | `facebook_propose_clone_campaign`, `facebook_propose_clone_adset`, `facebook_propose_clone_ad` (clones start paused) |

Before pausing, scaling or changing the optimization event on a sales campaign that optimizes for COMPLETE_REGISTRATION, read `meta-custom-event-interpretation`. Never pause the top-converting ad in an ad set.

## Google Ads

| Change | Propose with |
|---|---|
| Campaign status, name, dates, bid strategy and targets, networks, frequency caps, locations, languages, campaign negatives, content exclusions, conversion goals | `google_ads_propose_update_campaigns` (call `google_ads_get_currency` first) |
| Ad group status, name, CPC bids, keywords (add, pause, enable, change match type), audiences, topics, placements, Shopping listing groups | `google_ads_propose_update_adgroups`. Get criterion IDs with `google_ads_run_gaql` first. |
| Ad status, final URLs, tracking template, RSA headlines and descriptions | `google_ads_propose_update_ads`. RSA text replaces the whole list, so send every headline or description, not just the changed one. |
| New sitelinks, structured snippets, image assets | `google_ads_propose_create_asset` |
| Edit an asset or pause its link | `google_ads_propose_update_asset` (pausing is the soft delete) |
| Device, location or ad-schedule modifiers | `google_ads_propose_update_bid_modifiers` (0.1–10; 0 excludes a device; ad groups support device only) |
| PMax asset groups: status, URLs, audience signals, add or remove headlines, images, videos | `google_ads_propose_update_pmax_asset_group` (one item per asset group) |
| Start an experiment on a Search campaign | `google_ads_propose_create_experiment` (read `google-ads-create-master-skill` → `references/experiment.md`) |
| End, graduate or promote an experiment | `google_ads_propose_update_experiment` |

Keyword and bid work on Search follows `google-ads-search-execution`: never raise bids with Q4/Q5 search terms present, and never raise bids and budget together.

## Microsoft Ads and LinkedIn

The connector reads these platforms but can't change them. Give the user the exact change to make in their ads manager.

## When a change is refused

- **Needs a permission:** the tool returns a re-authorization link. Share it, and offer the recommendation in the meantime.
- **Plan limit reached:** explain which limit was hit and that the workspace owner manages the plan in GoMarble (plan details: gomarble.ai/pricing). Don't share upgrade or checkout links; offer the recommendation so the user can apply it in the ad platform.
- **Read-only connection or team permission:** say who can grant write access (the workspace owner, or Settings → Integrations in GoMarble).
- **Governance policy block:** say which limit applied. Don't try to work around it.
