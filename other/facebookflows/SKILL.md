---
name: facebookFlows
description: "The Facebook part of flow: Facebook's recorded flows, their MCP tools (facebookFlow<Name> and facebookFlow<Name>Live), what each Facebook flow's steps must answer, Facebook's overlays and the profileSetup example. Read with its shared counterpart, skills/flow/SKILL.md (the flows guide), when recording or running a flow on Facebook."
---

# facebookFlows

How every flow is recorded, built and run (inspect, `log flow fromInspect`,
params, dry run, live run, the machine, confirming requests) is
`skills/flow/SKILL.md`. This is what only applies on Facebook.

## Tools

Each Facebook flow has its own MCP tool, `facebookFlow<Name>`, and a live
twin, `facebookFlow<Name>Live`, that runs it on Facebook with
`confirmLive: true` (`profileSetup` is `facebookFlowProfileSetup` and
`facebookFlowProfileSetupLive`; `facebookLanguageEnglish` is
`facebookFlowLanguageEnglish`). The CLI words stay `log flow run <name>`.

The flows recorded on Facebook (`src/browser/flow/definitions/`):
`deletePost`, `facebookLanguageEnglish`, `groupHeaderMenus`, `groupMembers`,
`groupPostComments`, `groupPostDialog`, `groupTabs`,
`marketplaceListingDelete`, `marketplaceListingPublish`,
`messengerPinCreate`, `postComment`, `profilePhotoPost`, `profilePost`,
`profileSetup`, and the five warm-up activities (`warmupCreateAccessCheck`,
`warmupFeedBrowse`, `warmupMarketplaceBrowse`, `warmupMessagesVisit`,
`warmupSellingVisit`; see `skills/facebookWarmup/SKILL.md`).

## What Facebook's flows check

- `marketplaceListingPublish` checks `buy_location`, the set-location
  answer's city, the create page's `marketplace_new_seller_can_post_item`
  and `sell_location` (so it stops before the form when the account may not
  post), and the listing id in the create answer (`noListingId`).
- `profileSetup`'s three saves check their mutations answered 2xx (no saved
  answers to read fields from yet).
- `deletePost`: `move_to_trash_story.success` true; `postComment`:
  `comment_create.feedback_comment_edge`; the posts:
  `story_create.story_id`.
- A plain endpoint `expect`: `/profile/picture/upload/` is
  `profilePictureUpload`.

## The profileSetup example

```bash
log inspect start --account <a> --url https://www.facebook.com/me --bypass --now
log inspect do click <ref> --live ...   # one step at a time
log inspect do stop

log flow fromInspect ~/.logCli/runs/inspect/<run> --name profileSetup \
  --rename text1=firstName --rename text2=lastName --rename file1=profilePhoto --rename file2=coverPhoto

log flow run profileSetup --account <a> --set firstName=Bethlehem --set lastName=Trash \
  --set profilePhoto=<path|url> --set coverPhoto=<path|url>
log flow run profileSetup --account <a> ... --live --bypass --now
```

Over MCP: `facebookFlowProfileSetup` with `account` and the params by name;
`facebookFlowProfileSetupLive` with `confirmLive: true`.

## Controls on Facebook

"Upload Photo" in a recording finds Facebook's "Upload photo": controls
match by role, then name (`skills/flow/SKILL.md`, Deterministic steps).

## Facebook's overlays

| Overlay | Page state | Checked by |
| --- | --- | --- |
| "To allow or block browser notifications from Facebook…" | `browserNotificationsNotice` | gone from the page (Escape sends no call) |
| "What happened" … "Ended on <date>" | `pastNoticeDialog` | `useAccountStatusClearEnrollmentEntryPointActionMutation` answers `data.xfb_ixt_gateway_clear_flow: true` |

A "What happened" with no "Ended on" is not cleared: it stays unknown, for
SubQ to read (rule 73).

Rebuild Facebook's request docs after a run: `log capture docs`.

## Saved flows

| Flow | Recorded | Does |
| --- | --- | --- |
| `profileSetup` | Lancaster, 2026-10-19; the picture steps checked on Exeter, 2026-10-24 | Profile picture, cover photo, name (13 steps). The picture steps wait on the dialog query, the upload and the set mutation, inside "Choose profile picture". The host runs only the parts Twenty has data for (`flowWithParams`). |
| `marketplaceListingDelete` | Bethlehem, 2026-10-23 | Delete one Marketplace listing from Selling: More options, Delete listing, Delete, then "No, haven't sold" on Facebook's survey (6 steps). The menu answer must name the listing id given, and so must the delete answer (`commerce_for_sale_item_delete.deleted_for_sale_item_id`). Run it through `log facebook listing remove`, which then sets the Twenty row REMOVED. |
