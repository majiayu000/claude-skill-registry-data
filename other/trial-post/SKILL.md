---
name: trial-post
description: "Posts finished, QA-passed reels as Instagram Trial Reels (shown to non-followers first, graduation stays a human tap) plus public TikToks through the Zernio MCP connector, with the safety rails that stop the classic mistakes: IG trials only via call_tool posts_create_post with trialParams (the simple posts_create tool publishes a normal FEED reel), trial proof checked in every response, spacing and daily caps, a duplicate-file guard, the right CTA ending per platform, the platform AI flag on avatar footage, and a STOP file on anything unexpected. Includes a scheduler adapter for other tools (Metricool, Buffer, Later, or any other scheduler). Use for 'post the trials', 'post this as a trial reel', 'send it to TikTok', 'schedule the reels'."
author: Johann (@johannships)
version: 1.0.0
---

# Trial post: Instagram Trial Reels + TikTok via Zernio

Step 5 of the pipeline: idea -> script -> record -> "the card is in" -> `edit-style` -> **trial-post** -> `reel-scorecard`.

Why trials: a Trial Reel is shown to people who do not follow you. Every hook gets tested on strangers first; only
winners are shared to your main feed (you tap "Share to everyone" in the Instagram app, there is no API for it).
Three hooks per idea = three trial reels = the scorecard tells you which hook wins.

## Requirements

- Claude Code with the Zernio MCP connector: `claude mcp add --transport http -s user zernio https://mcp.zernio.com/mcp`
  (sign in when asked). Instagram must be a professional account connected in Zernio; TikTok connected too.
- The connector has full access to every connected account (posting, DMs, comments, deletes). The rules below are
  the only guard: keep them, and never let a skill send DMs, comments, edits or deletes.
- `cp config.example.json config.json`, then fill `accounts` from Zernio `accounts_list` (one id per platform),
  your `timezone`, spacing and daily caps. Start low (3 to 5 a day per platform) and ramp.

## Before any post (per reel)

1. The edit passed every `edit-style` gate, including face-first, dead-air and join-envelope, on BOTH files:
   `final.mp4` (Instagram, comment-KEYWORD ending) and `final-bio.mp4` (TikTok, "link in my bio" ending).
2. Captions from `reel-captions` passed the checker. The Instagram caption carries the keyword CTA; the TikTok
   caption never says "comment" and does carry your bio line.
3. Every claim in the video was checked live today. A false or outdated line is cut, not posted.
4. Never an identical clone of something already posted. A new hook, a new edit, a genuinely different video.
   No fingerprint-evasion tricks (mirror flips of posted footage, speed or pitch nudges, noise): they read as spam
   and get accounts restricted.

## Post (one platform at a time)

1. **Upload.** `mcp__zernio__call_tool` name `media_get_media_presigned_url`, arguments
   `{"filename": "<short>.mp4", "content_type": "video/mp4", "size": <bytes>}`. Save the result. PUT the file to
   `uploadUrl` with `curl -X PUT -H "Content-Type: video/mp4" --data-binary @final.mp4 "<uploadUrl>"` (no auth
   header), then download `publicUrl` and compare sha256 with the local file. Mismatch = upload again.
2. **Build.** `python3 scripts/build_post.py --platform instagram --idea R6 --hook A --video final.mp4 --media-url <publicUrl> --caption CAPTION-IG.txt --now`
   (`--at 2026-11-02T18:05:00` for a slot, `--ai` for avatar or AI-generated footage). It refuses on a STOP file,
   a duplicate file, a spacing gap, a used-up cap, or a caption that breaks the rules, and prints the arguments.
3. **Call.** `mcp__zernio__call_tool` name `posts_create_post` with EXACTLY the printed arguments. Save the response.
4. **Verify.** `python3 scripts/verify_post.py --plan <plan> --response response.txt`. Exit 0 = recorded (Instagram:
   trial confirmed). Exit 4 = still publishing: wait a minute, `posts_get`, verify again. Exit 3 = STOP.
5. Repeat for TikTok with `final-bio.mp4` and the TikTok caption.

## THE TRAP (read twice)

| tool | what it does on Instagram | use it? |
|---|---|---|
| `call_tool` `posts_create_post` with `platformSpecificData.trialParams.graduationStrategy: "MANUAL"` | Trial Reel, non-followers, you graduate it | YES, the only way |
| `posts_create` (the simple tool) | no platformSpecificData: a NORMAL FEED reel to all followers | NEVER |
| `posts_publish_now`, `posts_cross_post`, `posts_bulk_upload_posts` | no trial params | NEVER for trials |
| `validate_post` | accepts a bogus trialParams value | not proof of anything |

`dry_run` exists for TikTok only; an Instagram dry run is rejected. So the proof of a trial is the create response:
the instagram target must show `trialParams.graduationStrategy: "MANUAL"` (and `isTrialReel: true` once listed).
Payload shapes and response examples: `references/zernio.md`.

## Stop rules (any one: stop the batch, tell the creator the same minute)

- An Instagram response without MANUAL trial proof, or with `SS_PERFORMANCE` (auto graduation).
- A failed status, no post id, or a create error.
- A trial-cap error ("maximum number of trial reels"), a TikTok `spam_risk` error, any account-status or
  recommendation-eligibility notice.
- A post still scheduled or publishing 30 minutes after its slot (over-cap posts can be held silently).

`verify_post.py` writes `$HOME/.trial-post/STOP` on the first three; `build_post.py` refuses until a human has looked
in the app and deleted the file. Never "fix" a post with an edit, delete or retry call.

## Never

X or LinkedIn from this skill, DMs, comments, deletes, edits, unpublishing, paid-partnership flags, collaborator tags,
a sponsor label burned into the video (disclosure goes in the caption), or posting to an account not in config.json.

## Other schedulers (adapter)

Not on Zernio, or also scheduling the main feed elsewhere? `references/scheduler-adapter.md` lists what any
scheduler must support (trial reels or not, the AI flag, per-platform captions, future-dated only) and a worked
example for Metricool. Fill the adapter section for your tool; keep every rule above.

## After posting

Hand the ledger (`$HOME/.trial-post/ledger.jsonl`) to `reel-scorecard` at 72 h. Graduation stays the creator's tap.
