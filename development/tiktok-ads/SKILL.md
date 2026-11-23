---
name: tiktok-ads
displayName: "AdKit for TikTok Ads: Campaigns, Ad Groups, Video Ads, Spark Ads and Reporting"
description: >
  Create, edit, and report on TikTok ads from an AI agent through the AdKit MCP connector:
  campaigns, ad groups, video ads, Spark Ads, media upload, and results. Every change is saved
  as a draft that the user approves before it goes live. Use when the user wants to run,
  change, or check TikTok ads. Not for TikTok ad strategy or creative advice.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so/features/ads-mcp/tiktok
triggers:
  - tiktok ads
  - tiktok ads mcp
  - tiktok ads manager
  - tiktok campaign
  - tiktok ad group
  - spark ads
  - tiktok ads report
  - tiktok ads api
---

# TikTok Ads with AdKit

This skill tells you how to create, edit, and report on TikTok ads through AdKit. It covers the steps, not the strategy.

## Connect AdKit

AdKit is one MCP connector for Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest ads.

- **Claude, ChatGPT, and most AI apps:** add a custom connector with the address `https://mcp.adkit.so`, then sign in.
- **Claude Code:** `claude mcp add --transport http adkit https://mcp.adkit.so`

For other AI apps, see how to set up the [AdKit MCP server for TikTok Ads](https://adkit.so/features/ads-mcp/tiktok). If the AdKit tools are not available, tell the user how to connect. Then stop.

## What AdKit can do on TikTok

| Entity       | Actions                                                          |
| ------------ | ---------------------------------------------------------------- |
| `campaigns`  | list, get, create, update                                        |
| `ad-groups`  | list, get, create, update                                        |
| `ads`        | list, get, create, update (video ads and Spark Ads)              |
| `media`      | list (Asset Library videos), upload                              |
| `lead-forms` | list (existing Instant Forms; create them in TikTok Ads Manager) |
| `results`    | list (account, campaign, ad group, or ad level)                  |
| `accounts`   | list, available, connect, disconnect, update, profiles, pixels   |
| `drafts`     | get, publish (review your changes, then send them)               |

AdKit cannot delete TikTok campaigns, ad groups, or ads. Pause them instead with `status: "paused"`.

## Steps

All calls go through `adkit_manage` with `platform: "tiktok"`. Before a call you have not made in this session, read its fields with `adkit_help({ path: "manage tiktok <entity> <action>" })`. Do not guess field names. In this skill, `campaigns` `create` means `entity: "campaigns"`, `action: "create"`.

1. **Project:** call `adkit_projects` and get the `projectId`. Every call needs it.
2. **Account:** call `adkit_status`. If no TikTok account is connected, call `adkit_setup` with `platform: "tiktok"` and give the user the link. After they sign in, use `accounts` `available`, then `accounts` `connect`.
3. **Build from the top down.** Each create saves a draft. For each level, do these steps before you start the next level:
   - Show the draft to the user (`drafts` `get`, or the link `https://app.adkit.so/manage/drafts?open=<draftId>`).
   - Wait for a yes. Then publish it with `drafts` `publish`.
   - Use the TikTok ID that the publish result returns as the parent of the next level. A draft ID never works as a parent ID.

   The levels, in order:
   1. **Campaign:** `campaigns` `create` with a name, an objective, a budget, and `status: "paused"`. A paused campaign spends nothing.
   2. **Ad group:** `ad-groups` `create` with the `campaignId`, a budget, bidding, and an optimization goal.
   3. **Video:** `media` `upload` from a public URL, or `media` `list` to pick a video that is already in the TikTok Asset Library. For a local file: call `adkit_manage` with `entity: "media"` and `action: "request_upload_url"` (no platform). It returns an upload URL. Send the file to that URL with `PUT`. Then call `media` `upload` with `source: "temporary_upload"`.
   4. **Ad:** `ads` `create` with the `adGroupId` and the creative.

4. **Go live:** `campaigns` `update` with `status: "active"`. Publish that draft only after the user says yes. Then check with `ad-groups` `list` and `ads` `list` that the ad groups and ads are active too.
5. **Results:** `results` `list` with a `level` and a date range (`from` and `to`).

## TikTok rules

- TikTok calls ad accounts "advertisers". AdKit calls them accounts.
- Ads are video only. Upload the video before you create the ad. AdKit picks the cover image.
- To promote an existing organic TikTok post as a Spark Ad, pass `existingPostId` instead of a video.
- Conversion ad groups need a pixel. Set a default pixel on the account (`accounts` `update` with `defaultPixelId`) or pass `conversion.pixelId`.
- App campaigns need an app that is already registered in TikTok, and ad group operating system targeting (iOS or Android) that matches the app store.
- Use AdKit field names (camelCase). The entities in the table above ignore raw TikTok API field names.

## Anything else in the TikTok API

For a TikTok feature that AdKit does not cover, use `entity: "platform-api-request"` with `action: "mutate"`. The action is always `mutate`, also for reads. AdKit sends the request to the TikTok Marketing API v1.3 as it is. The user must turn on Advanced Platform Access in AdKit's Agent Permissions.

- Check every path, field, and value in the [TikTok API reference](https://business-api.tiktok.com/portal/docs/campaign-management-api-reference/v1.3).
- Read requests run immediately, with no draft. Writes save a draft, like any other change.
- After you use it, report the missing feature with `adkit_feedback`.

```json
{
  "projectId": "<projectId>",
  "entity": "platform-api-request",
  "action": "mutate",
  "data": {
    "platform": "tiktok",
    "accountId": "<advertiserId>",
    "endpoint": "campaign/get/",
    "method": "GET",
    "payload": { "advertiser_id": "<advertiserId>" },
    "description": "List TikTok campaigns"
  }
}
```

## Other platforms

The same AdKit connector runs [Meta Ads](https://adkit.so/features/ads-mcp/meta), [Google Ads](https://adkit.so/features/ads-mcp/google), [LinkedIn Ads](https://adkit.so/features/ads-mcp/linkedin), [Microsoft Ads](https://adkit.so/features/ads-mcp/microsoft), [Reddit Ads](https://adkit.so/features/ads-mcp/reddit), [X Ads](https://adkit.so/features/ads-mcp/x), and [Pinterest Ads](https://adkit.so/features/ads-mcp/pinterest) ads. Each platform has its own skill in this repo, for example `meta-ads` and `google-ads`.
