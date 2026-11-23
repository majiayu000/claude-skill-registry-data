---
name: google-ads
displayName: "AdKit for Google Ads: Search, Performance Max, Display, Keywords and Reporting"
description: >
  Create, edit, and report on Google Ads from an AI agent through the AdKit MCP connector:
  Search and Performance Max campaigns, ad groups, ads, keywords, negative keywords, keyword
  research, search terms, and results. Every change is saved as a draft that the user approves
  before it goes live. Use when the user wants to run, change, or check Google Ads. Not for
  Google Ads strategy: use google-ads-strategy for that.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so/features/ads-mcp/google
triggers:
  - google ads
  - google ads mcp
  - google search ads
  - performance max
  - google ads keywords
  - negative keywords
  - search terms report
  - google ads report
  - google ads api
---

# Google Ads with AdKit

This skill tells you how to create, edit, and report on Google Ads through AdKit. It covers the steps. For what to build (keywords, structure, ad copy), read the `google-ads-strategy` skill.

## Connect AdKit

AdKit is one MCP connector for Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest ads.

- **Claude, ChatGPT, and most AI apps:** add a custom connector with the address `https://mcp.adkit.so`, then sign in.
- **Claude Code:** `claude mcp add --transport http adkit https://mcp.adkit.so`

For other AI apps, see how to set up the [AdKit MCP server for Google Ads](https://adkit.so/features/ads-mcp/google). If the AdKit tools are not available, tell the user how to connect. Then stop.

## What AdKit can do on Google Ads

| Entity           | Actions                                                                          |
| ---------------- | -------------------------------------------------------------------------------- |
| `campaigns`      | list, get, create, update, delete (Search, Display, Demand Gen, Performance Max) |
| `ad-groups`      | list, get, create, update, delete                                                |
| `ads`            | list, get, create, update, delete                                                |
| `keywords`       | list, get, create, update, delete, list-negatives, add-negative, remove-negative |
| `negative-list`  | create, list, get, delete, attach, detach (shared negative keyword lists)        |
| `assets`         | list, get, create, update, attach, detach (sitelinks, callouts, snippets, calls) |
| `asset-groups`   | list, get, create, update, delete (Performance Max)                              |
| `media`          | upload (images, and existing YouTube videos)                                     |
| `research`       | keywords (Keyword Planner ideas), topics, interests                              |
| `geo-locations`  | search (find location IDs by name)                                               |
| `conversions`    | list, get, create, update, delete, upload                                        |
| `change-history` | list (who changed what in the last 30 days)                                      |
| `results`        | list, search-terms, placements, keywords                                         |
| `accounts`       | list, available, connect, disconnect                                             |
| `drafts`         | get, publish (review your changes, then send them)                               |

## Steps

All calls go through `adkit_manage` with `platform: "google"`. Before a call you have not made in this session, read its fields with `adkit_help({ path: "manage google <entity> <action>" })`. Do not guess field names. In this skill, `campaigns` `create` means `entity: "campaigns"`, `action: "create"`.

1. **Project:** call `adkit_projects` and get the `projectId`. Every call needs it.
2. **Account:** call `adkit_status`. If no Google Ads account is connected, call `adkit_setup` with `platform: "google"` and give the user the link. After they sign in, use `accounts` `available`, then `accounts` `connect`.
3. **Build from the top down.** Each create saves a draft. For each level, do these steps before you start the next level:
   - Show the draft to the user (`drafts` `get`, or the link `https://app.adkit.so/manage/drafts?open=<draftId>`).
   - Wait for a yes. Then publish it with `drafts` `publish`.
   - Use the Google ID that the publish result returns as the parent of the next level. A draft ID never works as a parent ID.

   The levels, in order, for a Search campaign:
   1. **Keyword research:** `research` `keywords` for ideas. Choose keywords and match types with the user.
   2. **Campaign:** `campaigns` `create` with `campaignType: "search"`, a budget, a bid strategy, locations (`geo-locations` `search` finds cities and regions by name), and `status: "paused"`. A paused campaign spends nothing.
   3. **Ad group:** `ad-groups` `create` with the `campaignId`.
   4. **Keywords and ad:** `keywords` `create` and `ads` `create` (responsive search ad) with the `adGroupId`.
   5. **Negative keywords and assets:** `keywords` `add-negative`, then sitelinks and callouts with `assets` `create` and `assets` `attach`.

4. **Go live:** `campaigns` `update` with `status: "enabled"`. Publish that draft only after the user says yes. Then check with `ad-groups` `list` and `ads` `list` that the ad groups and ads are enabled too.
5. **Results:** `results` `list` with a `level` and a `period` or a date range (`from` and `to`). For Search, `results` `search-terms` shows what people typed. Use it to suggest new keywords and negatives.

## Google Ads rules

- **Performance Max:** create the campaign with its `assetGroups`. It has asset groups instead of ad groups and ads. Upload the images first.
- **Display (beta):** upload images, set targeting on the ad group, then create a `responsive_display` ad. A targeting update replaces the whole list, so send every item that should stay.
- **Demand Gen video:** register a video that is already on YouTube with `media` `upload`. AdKit cannot upload a video file to YouTube.
- **Manager accounts (MCC):** connecting an account under a manager also needs the `managerId`.
- **Ads:** updating or deleting an ad needs its `adGroupId`.
- **Conversions:** keep the account's existing conversion goals unless the user asks for a change. `conversions` `upload` (offline imports) runs immediately and saves no draft. First run it with `validateOnly: true`. Then ask the user. Run the real upload only after they say yes.
- **Before you retry a failed write,** read `change-history` so you do not create the same thing twice.
- List actions return settings only. Spend, clicks, conversions, and Quality Score come from `results`.
- Use AdKit field names (camelCase). The entities in the table above ignore raw Google Ads API field names.

## Anything else in the Google Ads API

For a Google Ads feature that AdKit does not cover (for example dynamic search ad targets or page feeds), use `entity: "platform-api-request"` with `action: "mutate"`. The action is always `mutate`, also for reads. AdKit sends the request to the Google Ads API as it is. The user must turn on Advanced Platform Access in AdKit's Agent Permissions.

- Check every resource and field in the [Google Ads API reference](https://developers.google.com/google-ads/api/reference/rpc).
- Read requests run immediately, with no draft. Writes save a draft, like any other change.
- After you use it, report the missing feature with `adkit_feedback`.

```json
{
  "projectId": "<projectId>",
  "entity": "platform-api-request",
  "action": "mutate",
  "data": {
    "platform": "google",
    "accountId": "<customerId>",
    "endpoint": "customers/<customerId>/googleAds:mutate",
    "payload": {
      "mutateOperations": [
        {
          "adGroupAdOperation": {
            "update": {
              "resource_name": "customers/<customerId>/adGroupAds/<adGroupId>~<adId>",
              "status": "PAUSED"
            },
            "update_mask": "status"
          }
        }
      ]
    },
    "description": "Pause one ad"
  }
}
```

## Other platforms

The same AdKit connector runs [Meta Ads](https://adkit.so/features/ads-mcp/meta), [TikTok Ads](https://adkit.so/features/ads-mcp/tiktok), [LinkedIn Ads](https://adkit.so/features/ads-mcp/linkedin), [Microsoft Ads](https://adkit.so/features/ads-mcp/microsoft), [Reddit Ads](https://adkit.so/features/ads-mcp/reddit), [X Ads](https://adkit.so/features/ads-mcp/x), and [Pinterest Ads](https://adkit.so/features/ads-mcp/pinterest) ads. Each platform has its own skill in this repo, for example `meta-ads` and `microsoft-ads`.
