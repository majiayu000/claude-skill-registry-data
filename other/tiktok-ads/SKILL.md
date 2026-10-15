---
name: tiktok-ads
description: "Use for any TikTok Ads work that isn't a new launch: performance and creative reports, audience breakdowns, account balance and quotas, ad review status and rejections, change history, automated rules, Smart+ and Smart Creative campaigns, split tests, Reach & Frequency, offline events, and editing or copying TikTok campaigns, ad groups and ads. For new launches use launch-campaigns."
---

# TikTok Ads

Read, analyze and operate TikTok Ads through GoMarble. For new launches, use `launch-campaigns` (which follows `tiktok-create-master-skill`).

> **Beta, and no applied changes through the connector.** Tools marked (β) are part of a TikTok tools beta. Accounts outside the beta don't see them at all; if the user asks for something that needs one, say it's in GoMarble's TikTok beta (they can contact GoMarble support). **TikTok changes can't be applied through the connector today** — the connector can't be granted TikTok write permission. For accounts in the beta, the propose tools still work in dry-run mode, which validates the change; then give the user the exact edit to make in TikTok Ads Manager or the GoMarble web app.

## Setup and conventions

- Accounts: `tiktok_list_ad_accounts`. Details, currency and timezone: `tiktok_get_account_details`. Money is in the advertiser's currency, never micros; pass `currency_code` on changes.
- Business Centers: `tiktok_list_business_centers` (β) supplies the `bc_id` that finance and catalog tools need.
- Lists paginate. When a response says `has_more_pages`, call `tiktok_fetch_pagination` before totaling.
- Regular list tools don't return Smart+ campaigns. Use `tiktok_get_smart_plus` (β) for those.

## Reporting and analysis

| Question | Tool |
|---|---|
| Campaigns, ad groups, ads and their settings | `tiktok_get_campaigns`, `tiktok_get_adgroups`, `tiktok_get_ads` |
| Performance at any level (sync) | `tiktok_get_basic_report_enhanced`. Include a time dimension for revenue and ROAS metrics, and pick purchase metrics by destination (website, app or TikTok Shop). |
| Large or long-range reports | `tiktok_get_async_report` (β). If it says `still_processing`, call again with the `task_id`. |
| Age, gender, location and other audience segments | `tiktok_get_audience_report` |
| Spend and engagement per creative | `tiktok_get_creative_report` (β), and `tiktok_get_ad_creative_url` for the media itself |
| What changed in the account | `tiktok_get_change_log` (β). Async, at most 30 days per request. |
| Account balance, or active ad group quota | `tiktok_get_account_finance` (β): `BALANCE` needs `bc_id`; `QUOTA` needs the advertiser ID |
| Why ads were rejected, and how to fix them | `tiktok_get_ad_review_info` (β). Pass up to 100 ad IDs in one call. |
| Automated rules and their history | `tiktok_get_automated_rules` (β). Check before proposing budget or status changes so a rule doesn't undo them. Rules can only be created in TikTok Ads Manager. |
| Tracking setup | `tiktok_list_pixels` (β) and `tiktok_list_custom_conversions` (β). Offline event sets: `tiktok_get_offline_event_sets` (β). |
| Audiences and targeting | `tiktok_list_audiences` (β), `tiktok_search_targeting` (β, locations only), `tiktok_search_interests` (β) |
| Catalogs and TikTok Shop stores | `tiktok_list_catalogs` (β) |
| Identities, music | `tiktok_get_identities` (β), `tiktok_get_music` (β) |

Apply the same diagnosis discipline as other channels (`diagnose-performance`, `analyse-creative`): compare against the account's own baseline, and don't judge ad groups with too few conversions.

## Operations (β): prepare and validate

Use these to prepare a TikTok change and validate it as a dry run (`mode: "dryrun"`, the default). Show the user the validated change, then give them the exact steps to apply it in TikTok Ads Manager. A `mode: "live"` call returns a permission error (606) for AI app connections; don't retry it. TikTok has no platform-side validation, so review carefully.

| Change | Tool | Watch out for |
|---|---|---|
| Campaign name, budget, status | `tiktok_propose_update_campaigns` | Bids live on ad groups, not campaigns. |
| Ad group name, budget and bids, schedule, dayparting, targeting, audiences, status | `tiktok_propose_update_adgroups` | List fields replace the whole list. Placement, optimization goal, billing event and pixel can't change after creation. |
| Ad name, text, media, music, Spark post, identity, status | `tiktok_propose_update_ads` | Creative changes send the ad back to review. The CTA and landing page can't be changed. |
| Copy a campaign | `tiktok_propose_copy_campaign` | The copy starts disabled. |
| Smart+ campaigns: create, update, status, budget, copy | `tiktok_propose_manage_smart_plus` | Read first with `tiktok_get_smart_plus`. Budget updates take one ad group per proposal. Follow `tiktok-create-master-skill` → `references/smart-plus.md`. |
| Smart Creative (ACO) ads and materials | `tiktok_propose_manage_smart_creative` | Read first with `tiktok_get_smart_creative`. Send list fields complete. Keep the ad group paused while reviewing. |
| Split tests: create, reschedule, end | `tiktok_propose_manage_split_test` | **Creating a test overwrites both ad groups' budgets.** Ending is irreversible. Read results with `tiktok_get_split_test` at least 24 hours after the test ends. |
| Reach & Frequency campaigns and ad groups | `tiktok_propose_manage_reach_frequency` | Estimate first with `tiktok_get_reach_frequency`. **Approving an R&F ad group reserves real budget** and can't be paused; the only undo is cancelling the order. Say so before asking for approval. |
| Appeal a rejected ad, or create or update an offline event set | `tiktok_propose_manage_review_and_events` | An appeal is one-shot per rejection, so fix what `tiktok_get_ad_review_info` suggests first. |
| Upload a video or image to the asset library | `tiktok_upload_asset` | A direct write with no dry run, so it needs TikTok write permission and isn't available to AI app connections today. |

## Put it on a schedule

Offer a daily TikTok performance or creative fatigue agent (see `automate-with-agents`). Agents that make changes need a Meta or Google account in scope, so TikTok agents are read-only.
