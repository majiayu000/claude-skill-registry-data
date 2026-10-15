---
name: accounts-and-connections
description: "Use when the user wants to see, add, enable, remove or switch ad accounts and data sources in GoMarble: which accounts are connected, adding a new ad account, connecting a platform (Meta, Google, TikTok, LinkedIn, Microsoft Ads, GA4, Search Console, Shopify, Klaviyo, Snowflake, impact.com, Pages, Instagram), connecting other tools like HubSpot, Notion or BigQuery, connecting Slack for agents, switching a connection between read-only and read & write, fixing expired connections, or removing an account."
---

# Accounts and connections

Help the user see what's connected to GoMarble, add what's missing, and change or remove connections. Connecting and removing happen in the GoMarble web app, and the model guides the user there. No GoMarble tool connects, disconnects, disables or removes anything. The one exception is described under "Adding an ad account".

Connections belong to the team, and only **owners and admins** can connect, reconnect, switch or remove them. If the user is a member, tell them up front that an admin has to do it, so they don't hit an access error at the last step. For roles and access, see `access-and-permissions`.

## What's connected

Call the list tool for each platform. Each returns two things:
- **`configured_accounts`:** the accounts saved in GoMarble. These are the ones GoMarble works with, and for members only the ones granted to them.
- **The platform's own list:** everything the connection can see, including accounts not yet added to GoMarble.

| Platform | Tool |
|---|---|
| Meta Ads | `facebook_list_ad_accounts` |
| Google Ads | `google_ads_list_accounts` |
| TikTok Ads | `tiktok_list_ad_accounts` |
| LinkedIn Ads | `linkedin_list_ad_accounts` |
| Microsoft Ads | `bing_ads_list_accounts` |
| GA4 | `google_analytics_list_properties` |
| Search Console | `gsc_list_properties` |
| Shopify | `shopify_list_shops` |
| Klaviyo | `klaviyo_list_shops` |
| Facebook Pages / Instagram | `facebook_page_list`, `instagram_list_accounts` |
| impact.com | `impact_list_accounts` (an empty list means none connected, or none granted to this user) |

Summarize by platform: what's configured, what's visible but not added, and anything missing that the user expects.

## Adding an ad account

**The normal way:** an owner or admin opens **apps.gomarble.ai/settings/integrations**, opens the platform's connection, and picks the accounts to add.

**By using it:** when an owner or admin asks about a Meta, Google Ads, TikTok, LinkedIn or Microsoft Ads account that's visible but not yet configured, the first tool call on it **adds it to GoMarble automatically**. That uses one of the plan's ad-account slots, and counts the account's last-30-day spend against the plan's ad-spend limit. So before the first call on an account that isn't in `configured_accounts`, say this and confirm the user wants it added. If the plan limit is reached, the tool returns a 403; explain which limit was hit and stop. Don't share the `upgrade_url` (see `access-and-permissions`).

Members can't add accounts this way; their call is denied before it gets there. They need an admin to add the account and grant them access.

## Removing or disabling an account

- **There is no "disable".** An account is either configured or removed.
- **Remove:** an owner or admin opens Settings → Integrations → the account's row menu → **Delete account**. Before they do, warn them: this removes the account **for the whole team**, together with the reports, agents and dashboards built on it (including teammates'), and it can't be undone. It also frees the plan slot.
- **Stop syncing** (same row menu) stops dashboard syncing without deleting the account, with a choice to keep or delete the synced data.
- To stop one person from using an account without removing it, the admin sets their access to None in Team management instead.

The model can't remove accounts. Give the steps and the warning.

## Connecting a new data source

| Source | Where | Notes |
|---|---|---|
| Ad platforms, GA4, Search Console, Shopify, Klaviyo, Snowflake, impact.com, Facebook Pages, Instagram | **apps.gomarble.ai/settings/integrations** | Owner or admin. Sign in to the platform, then choose accounts where asked. |
| Other tools: CRMs, analytics, warehouses, project tools (HubSpot, Notion, PostHog, Mixpanel, BigQuery, Linear…) | **apps.gomarble.ai/settings/connectors** | Owner or admin, in the GoMarble web app. Connectors added there are used by GoMarble's own app and agents. Don't call `discover_connectors` from here, and don't promise that a newly added connector's tools will appear in this conversation. |
| Slack (for agent delivery) and Google Drive | **apps.gomarble.ai/settings/apps** | Slack needs a plan that includes it. For private channels, invite the GoMarble bot. |

From here, work only with the GoMarble tools this plugin's skills describe. Google Drive is one of them: its tools are named `gdrive-*` (for example `gdrive-search_files`) and appear once Drive is connected; the user may need to start a new conversation to see them.

A connection can't be completed from the chat. The user finishes sign-in in the browser.

## Switching read-only and read & write

Only Meta Ads, Google Ads and TikTok have this setting. Read-only connections can analyze but can't apply changes.

- An owner or admin opens Settings → Integrations → the account's row menu → **Read only** or **Read & Write**.
- Google Ads switches without signing in again. Meta and TikTok go through the platform's sign-in again.
- Downgrading a connection to read-only downgrades every account on it.
- For the model to apply changes, the AI app's connection also needs the write permission for that platform (`access-and-permissions`, scopes).

## Expired or broken connections

When a tool says a connection expired or has no access, relay the message and any link exactly. If the connection was added by someone else, only they (or an admin) can reconnect it.
