---
name: social-publishing
description: Manage drafts, media, schedules, and publishing in a connected Sync Socials workspace. Use when the user asks to save social content in Sync Socials, check its queue, edit its posts, or schedule or publish to its connected accounts.
---

# Sync Socials publishing

This plugin declares the hosted Sync Socials connector, which the user must
connect and authenticate in Claude before its tools can operate. Use the
available Sync Socials MCP tools. Tool names below may have a client-added
prefix; match the `syncsocials_` name. Discover the current tool schemas before
calling them. Do not register another MCP server or construct a REST or API-key
workaround when this connector is unavailable.

## Establish the workspace

Call `syncsocials_get_workspace` to check the workspace identity, timezone,
capabilities, and allowances. For targeted drafts, schedules, or publishing, call
`syncsocials_list_connections` and use only the returned connected account IDs.
Do not infer that a destination is available from its platform name. When more
than one account matches and the user has not selected one, ask them to choose.
Use `syncsocials_list_posts` to inspect the queue or locate a requested post.

Facebook publishing targets Facebook Pages, not personal profiles. Instagram
publishing requires a business or creator account linked to a Facebook Page and
an image or video; text-only Instagram posts are unsupported. Use each platform's
own returned account ID, including when Facebook and Instagram share a linked
Page. If a destination is missing or needs reauthorization, direct the user to
Sync Socials Connections to connect or reconnect, allow publishing, and select
the correct Page or linked Instagram account. Recheck the connection before
targeting it; app approval does not replace the customer's account consent.

TikTok takes image or video posts and needs the user's privacy level and posting
consent before scheduling or publishing, plus commercial-content disclosure when
applicable. YouTube requires one video asset and an explicit privacy choice.
LinkedIn targets personal profiles with text or image posts. Threads, Bluesky,
Telegram, Discord, and Slack accept the post types returned for each connection.

If the tools are absent or authentication fails, explain that a connected Sync
Socials workspace is required. In Chat or Cowork, direct the user to the plugin's
Connectors tab. In Claude Code, the tools come from a Sync Socials connector
connected in the user's Claude account: connect it in Claude first, then start a
new Claude Code session signed in with that account. Claude Code's own sign-in to
this plugin's server URL is not accepted. Use the setup guide for the supported
connection flow. Installing the plugin alone does not authenticate the workspace.
Do not claim that a directory listing or a working public sign-in flow exists
unless verified. Never request OAuth client secrets, access tokens, or social
passwords in conversation. Stop on missing access or quota errors and explain the
specific remedy returned by the service.

## X publishing

X requires active paid Growth; trials and unpaid review access do not qualify.
Before selecting X, read `syncsocials_get_workspace`: check `xUsage.enabled`,
`xUsage.eligible`, `xUsage.disabledReason`, `xUsage.workspace.budgetExhausted`,
and `postingCapabilities`. Use `syncsocials_list_connections` for the selected
account's ID, supported post types, and limitations. A connection or an `x` enum
value alone does not establish publishing access.

Default allowances are 50 publishing attempts per workspace per month, 10 per
day, and 3 link-post attempts per month. Each stable X account is also limited
to 30 attempts per month and 3 per day, shared across workspaces; reconnecting
does not reset them. Reserved failures count. Media can exhaust the included
usage budget before the post count is reached. Use returned usage and UTC reset
times; stop on allowance or budget errors rather than changing credentials.
Before a batch, compare each selected X destination and its final caption with
the remaining workspace, account, daily, and link allowances. Explain any blocked
portion before writing; do not silently remove links or alter approved content.
Scheduled deliveries check allowances again when they run; current availability
does not guarantee capacity at a future publication time.

The final X caption, including any destination override and hashtags, must fit
280 weighted characters. URLs and Unicode use X's weighted counting rules;
plain string length is insufficient. Use text, up to four photos, or one MP4
video of at most 140 seconds and 50 MiB after processing. GIFs, multi-post
threads, and DMs are unsupported. Keep `tags: []` when no hashtags are requested.

Do not automatically retry an ambiguous X publish result, including a timeout
that might have occurred after acceptance. Inspect the existing post and the
actual X destination before any retry; explain an unresolved outcome to the
user instead of creating a duplicate.

## Save and edit drafts

- Default every create operation to `action: "draft"`. A request to draft,
  brainstorm, or prepare content does not authorize scheduling or publication.
- For ideas without destinations or media, use
  `syncsocials_create_content_draft`. It saves an untargeted text draft.
- For content tied to selected accounts or existing assets, use
  `syncsocials_create_post` with explicit `targets` and `mediaAssetIds`.
- `title` is the internal post name; `body` is the published caption. A title-only
  request leaves `body` empty. A request to write captions authorizes putting the
  requested copy in `body`. Use `tags: []` when the user requests no hashtags;
  omitted tags can be filled automatically by the server.
- Before editing, fetch the specific post with `syncsocials_get_post`. Use
  `syncsocials_update_post` with only the fields the user asked to change.
  Preserve its media, targets, timing, and privacy choices unless changing them
  is part of the request. If a named post is ambiguous, resolve it before writing.

## Use existing media and text concepts

Use `syncsocials_list_media` for existing images or videos. Import an existing
user-provided HTTPS media URL with `syncsocials_upload_media_from_url`, then use
the returned asset ID.

Hosted OAuth tools cannot read a file path on the user's computer. When you can
run shell commands where the file is, as in Claude Code or Cowork, upload it
directly. Call `syncsocials_create_media_upload` with its name, MIME type, and
exact size in bytes (from `wc -c`); images can be up to 25 MB and videos up to
250 MB. Run the returned `curlCommand` once, in one shell command that first
sets `FILE` to the local path (`FILE='/path/to/clip.mp4'; ...`). The upload
expires after 30 minutes. When curl exits successfully, call
`syncsocials_complete_media_upload` with the `uploadId` and use the returned
`mediaAssetIds`; repeating that call is safe. The command carries a one-time
upload token: never print, echo, or repeat it in replies or files. Where you
have no shell, as in Claude chat, or the upload cannot reach Sync Socials, ask
the user to upload the file to the Sync Socials media library; do not invent a
URL.

For Sync Socials campaign concepts, inspect `syncsocials_get_brand_profile`, then
use `syncsocials_generate_viral_concepts` when the user requests concepts. Select
the correct business if several exist. This operation creates text, can save a
brand profile, requires a configured workspace AI provider, and uses its
allowance. Show concepts for review before rendering one.

If the user requests an existing-media edit and the tool is available,
`syncsocials_produce_viral_video` assembles library clips or uploaded brand footage
with text and an existing soundtrack. Pass the approved concept object through
unchanged, choose only `library` or `remix`, and default to a draft. This connector
does not generate images, video footage, speech, or music through AI models.
Do not send media-generation prompt fields or switch authentication methods to
get around that restriction.

## Schedule, publish, and cancel

Only schedule or publish when the user explicitly requests that action. Resolve
the intended content, destination account IDs, and any required privacy,
commercial-content, or music declarations first. Do not invent consent or choose
an audience on the user's behalf. A clear request already containing these
details is sufficient; avoid asking the same question twice.

For scheduling, resolve the date and time in the workspace's IANA timezone unless
the user explicitly chooses another zone. Account for daylight saving. Clarify
an ambiguous or nonexistent local time before scheduling. Set `action: "schedule"`
and `scheduledFor` using an ISO timestamp with an explicit offset. For immediate
publication of an existing post, use `syncsocials_publish_post`.

Use `syncsocials_delete_post` only for the user's selected draft deletion or
cancellation of a scheduled post. It does not retract a post already published
on a social platform. Do not mass-delete or republish as a repair strategy.

## Verify and report

Read each mutation's result. Use `syncsocials_get_post` to verify the resulting
status and, after media processing, obtain its preview link. Queued publishing or
processing is still pending: do not call it published or ready until the returned
state confirms completion. If a write times out, inspect the queue or post before
retrying so that the action is not duplicated.

Report the post title and ID, resulting status, chosen accounts, and returned
preview or publishing link when available. For schedules, include the absolute
date and local time with its timezone, plus UTC. For failures, identify the
affected destination and the returned error without claiming the whole post
succeeded. Do not promise engagement or sales results.
