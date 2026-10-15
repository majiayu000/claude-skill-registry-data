---
name: launch-campaigns
description: "Use when the user wants to build or launch campaigns: a new Meta sales campaign, ad set or ads; a Google Search campaign, ad group or RSAs; a Performance Max campaign or asset group; a TikTok launch; or duplicating a winning campaign, ad set or ad. Turns an approved brief and creative into a full campaign setup (structure, names, budgets, targeting, ads, links, tracking) that the user reviews and approves before anything goes live."
---

# Launch campaigns

Turn the approved brief into a campaign setup. GoMarble assembles the whole build: hierarchy, names, budgets, schedule, targeting, exclusions, placements, ads, copy, links and tracking. The user reviews it before the account changes.

## When to use

- "Launch a Meta campaign for our new bundle with these creatives."
- "Set up a Google Search campaign for these keywords."
- "Build a PMax campaign" / "Add an asset group."
- "Launch this video on TikTok."
- "Duplicate our best ad set into a new campaign with a new budget."

## Before you build

1. **Creative and brief.** Get the creative (upload, URL, existing ad, or Drive file) and the brief. If there's no creative, ask for it first.
2. **Account context.** `recall_memory` for naming conventions, UTM rules, targets and anything the brand never does. Apply the user's naming and tracking rules across the whole build.
3. **Currency.** Meta: `facebook_get_details_of_ad_account`. Google: `google_ads_get_currency`. TikTok: `tiktok_get_account_details`. Pass `currency_code` on every launch call. Budgets are in account currency (50 means $50).
4. **The platform's launch skill.** The launch tools' descriptions ask for GoMarble's master skill via `load_skill`. This plugin ships the same content: read it from the plugin (`meta-create-master-skill`, `google-ads-create-master-skill`, `tiktok-create-master-skill`) and don't call `load_skill`.

## Meta

Follow `meta-create-master-skill`, reading its `references/` at each step.
- One call to `facebook_propose_create_campaign_structure` creates the campaign, one ad set and all its ads. The objective is **Sales** (`OUTCOME_SALES`); other objectives aren't supported through the connector.
- Needed first: `facebook_list_pixels` (use the only pixel, or ask which), and the Page ID plus Instagram account ID for every ad (from `facebook_get_details_of_ad_account` → `account_structure`, `facebook_page_list` or `instagram_list_accounts`).
- Targeting: `facebook_search_targeting` for interests, and `facebook_list_custom_audiences` for custom and lookalike audiences (pass both id and name).
- Catalog / dynamic product ads: `facebook_list_product_catalogs`, then `facebook_list_product_sets`.
- Uploaded creative: analyze it first with `facebook_analyze_ad_creative_by_id_or_url` (`fastMode: true`) to write fitting copy.
- **Defaults:** campaign and ad set active, **ads paused**. To turn the ads on after review, make one `facebook_propose_update_ads` batch (each activation needs the ad's `thumbnail_url` from `facebook_list_ads`).
- **Duplicate a winner:** `facebook_propose_clone_campaign`, `facebook_propose_clone_adset` or `facebook_propose_clone_ad`. Clones are created paused. To change a clone's text, use `facebook_propose_clone_ad_creative` (Meta doesn't allow editing creative text in place).

## Google

Follow `google-ads-create-master-skill` and its `references/`.
- **Search:** one call to `google_ads_propose_create_campaign_structure` creates the campaign, one ad group and its RSAs, all or nothing. Campaign and ad group start enabled, **ads paused**. Research keywords first with `google_ads_keyword_discover` and `google_ads_keyword_metrics` (`google-ads-keywordplanner`); never estimate volume or CPC.
- **Performance Max:** `google_ads_propose_create_pmax_asset_group` (read `google-ads-create-master-skill` → `references/pmax.md`). Standard, non-retail PMax only. Needs 3–15 headlines, 1–5 long headlines, 2–5 descriptions, and landscape and square images. A new campaign also needs a business name and logo. Created paused.
- **Assets:** sitelinks, structured snippets and images with `google_ads_propose_create_asset`. Shared negative lists with `google_ads_propose_create_negative_keyword_list`.
- **Images from Google Drive:** `google_drive_search_files` finds files GoMarble can access. `google_drive_prepare_media_url` copies a private Drive image or video to a **public** GoMarble URL the ad platforms can fetch. Use it only when the user asked to use that file, and tell them it makes a public copy. `google_drive_upload_from_url` saves a file from a public URL into Drive, but only when the user explicitly asks. These built-in Drive tools need a Drive permission most AI app connections can't be granted yet; if one returns a 606 permission error, ask the user for a public link to the file (or to download and attach it) instead.

## TikTok (beta)

Follow `tiktok-create-master-skill` and its `references/`. The order is fixed: creative, then placement (it can't change later), then account scan, then propose.
- One call to `tiktok_propose_create_campaign_structure` creates the campaign, ad group and ads. **Everything starts disabled** unless enabled on purpose.
- Needed first: `tiktok_get_identities` (who the ad posts as), `tiktok_list_pixels` and `tiktok_list_custom_conversions` for conversion goals, `tiktok_search_targeting` for locations, `tiktok_search_interests` for interests, `tiktok_list_audiences` for custom audiences, and `tiktok_list_catalogs` for catalog or Shop launches.
- Media: `tiktok_upload_asset` uploads to the asset library, but it's a direct write that AI app connections can't make today; use media already in the account, or have the user upload it. Carousels need a `music_id` from `tiktok_get_music`.
- Duplicate a campaign: `tiktok_propose_copy_campaign` (the copy starts disabled).
- **TikTok launches can be prepared and validated, not applied, through the connector.** The TikTok tools are in a beta (accounts outside it don't see them), and the connector can't be granted TikTok write permission. For beta accounts, run the launch as a dry run to validate the whole build, then hand the user the complete spec to create in TikTok Ads Manager or the GoMarble web app.

## Microsoft Ads and LinkedIn

The connector can't create campaigns on these platforms. Plan the build (for Microsoft, keyword ideas from `bing_ads_keyword_ideas`) and give the user a ready-to-enter spec.

## Review and approval

1. Make the dry run (`mode: "dryrun"`, the default).
2. Show the whole build in one clear summary: structure, names, budgets, schedule, targeting, placements, each ad's copy, links and UTMs, and what starts paused.
3. Only after an explicit yes, call again with `mode: "live"`, the `account_id` and the approved `operation_ids`. Never go live without that yes in this conversation; GoMarble doesn't double-check for you.
4. Confirm what was created, with IDs, and what's still paused. Offer to turn the ads on as a separate approved change.

If a launch call fails twice, stop and explain. Don't loop through parameter guesses.

## After launch

Offer an agent that watches the new campaign through its learning phase (see `automate-with-agents`), or a budget pacing check (`shift-budget`).
