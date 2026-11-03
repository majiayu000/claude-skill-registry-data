---
name: dm-revival
description: Grinds the creator's Instagram DM inbox in their real Chrome (Claude-in-Chrome MCP) to find lost leads, people who showed interest but the convo died, then visits each lead's profile and drafts a personalized re-engagement DM in the creator's voice. Sends in approved batches and keeps looping until the creator says stop. Use whenever the creator says grind my dms, dm revival, revive my dms, find lost leads, lost leads in my dms, dm outreach, follow up with my dms, re-engage leads, work my inbox, or dead leads.
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/dm-revival/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# DM Revival

Grind the Instagram inbox: find people who showed real interest and then went quiet, learn who they are from their profile, and re-open the conversation with a message that only fits them. This is warm follow-up inside existing threads, never cold outreach. Do not message any account that has no prior thread with the creator.

The end goal of every revived convo is the one offer in `backbone/offer.md` (name and current price live there, never hardcode them), but the re-opener itself never pitches. Its only job is to get a reply. The pitch happens later, in conversation, if they bite.

## Preflight

1. Load the Chrome tools in ONE ToolSearch call: `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__find,mcp__claude-in-chrome__form_input`
2. Use the real logged-in Chrome profile (Claude-in-Chrome), never Playwright or a fresh automation profile: the DM inbox only exists logged in.
3. Load the context files from the project root before classifying or drafting anything: `backbone/icp.md` (who counts as a lead), `backbone/offer.md` (what is sold, what is on the "What is NOT sold" list, what topics count as interest), and `voice-dna.md` (how the drafts sound). If `voice-dna.md` is still the "not built yet" stub, use the Voice/Tone one-liner in the root `CLAUDE.md` Creator Profile instead. Optional when present: `knowledge/*.md` for extra context on what the creator teaches.
4. Read the state log (see State below). It is status-aware: entries with status `sent` or `skipped` are done and get skipped; entries with status `drafted` are held drafts that get resurfaced at the start of this run (step 0 of the loop). Create the log if missing. Then run the cap preflight: count entries with `status: sent` whose `sent_at` falls on today's date (hard stop at 40, do not start a batch if it's already reached) and whose `sent_at` is within the last 60 minutes (about 15 per hour; if that's full, sweep and draft but hold sends until the window clears).
5. Navigate a tab to `https://www.instagram.com/direct/inbox/`. If reads come back empty or the page seems to silently not exist, that is the desktop-app symptom (Chrome MCP only works from terminal Claude Code). Stop and tell the creator to run this from the terminal.

## The grind loop

0. **Resurface held drafts first.** Before sweeping any new thread, take every log entry with status `drafted`. For each one, open its `thread_url` once and re-check for dead air: if the lead (or the creator) has messaged since the draft's `date`, flip the entry to `skipped` with reason `active` and move on. If it's still dead, put it in this run's FIRST checkpoint marked "held from <date>" with the stored draft text, not redrafted (a re-check, not a rewrite). The creator approves it, edits it, or declines it a second time (see checkpoint rules).

Then work the Primary tab top to bottom, scrolling the thread list to load more as you go. When Primary runs dry, do a second pass over the General tab and then the Requests tab the same way. If the inbox has no Primary/General split (personal account), work the single thread list top to bottom, then Requests. Those General and Requests threads are still existing inbound (someone messaged the creator first), so the no-cold-outreach rule holds. Nothing in Requests gets messaged unless it clears the same lost-lead bar. Match every thread against the log by `thread_url` (or by the username shown in the chat header once opened): the inbox list shows display names, so the URL is the reliable pre-open key. Skip anything already logged `sent` or `skipped`. For every other thread:

1. **Open the thread** and read the last 10 to 20 messages (scroll up a little if the tail is ambiguous). Note the username from the chat header and the thread URL (`/direct/t/<id>/`) so you can come back. If either the header username or the URL is already logged `sent` or `skipped`, close it and move on immediately.
2. **Classify it** (rules below). Skips get logged with a one-word reason and cost no further time.
3. **If it's a lost lead, profile-check them**: open `instagram.com/<username>` in a NEW tab, read bio + their 3 to 6 most recent posts (captions and pinned content tell you what they're about), then close that tab. New tab keeps the inbox scroll position; always close the tab you opened and don't touch the tab group.
4. **Draft the message** (craft rules below) and hold it. Do not type anything into the message box yet: Enter sends instantly on IG web, so the box only gets touched at send time.
5. **Checkpoint every 5 drafts** (or when the sweep runs dry): present the batch and wait for the creator.
6. **Send approved drafts**: re-run the cap count first (today's `sent` entries under 40, last hour's under 15, else hold). Then return to each thread URL, click the message box, type the final text as ONE line (an embedded newline sends the half-typed message on IG web), press Enter once. One send at a time with pacing. Log each result immediately after it sends (with `sent_at`), not at the end of the batch.
7. Keep sweeping. The loop only ends when the creator says stop, the whole inbox is processed, or a rail below trips.

### Batch checkpoint format

Numbered list (never bare "#N" refs), each entry: handle, one line of who they are and what the old convo was, then the draft in quotes.

The creator replies with things like "send all", "send 1 and 3", "2: swap the question for X", "drop 4", or "stop". Apply edits verbatim, send what's approved. Anything not approved the first time gets logged `drafted` (a held draft: the next run resurfaces it via step 0 after re-checking the thread). Anything the creator explicitly drops ("drop 4"), or that comes back as a held draft and still isn't approved (silence counts as a second decline), flips to `skipped` with reason `declined` and never resurfaces again.

## Classifying: what counts as a lost lead

**Lost lead = interest signal + dead air.** Both required:

Interest signals (any one is enough):
- Asked about the offer, the price, or how to join (whatever `backbone/offer.md` sells)
- Asked how the creator built something, or any real question about what the creator teaches or sells (topics in `backbone/offer.md` + `backbone/icp.md`)
- Described their business or their bottleneck (matches the segments in `backbone/icp.md`)
- Substantive story reply that started an actual exchange (a lone emoji is not a signal)

Dead air: no message from either side in 3+ days, and the thread ended without a close. The creator leaving THEM on read counts double: those get drafted first, and the draft should quietly own the dropped ball.

**Skip (log the reason, move on):**
- Active threads (either side replied within 3 days)
- Current members or clients: if they mention already being inside the offer, they're fulfillment, not outreach
- Friends and personal convos
- Brand deal / collab / sponsorship inbound (different lane)
- Spam, bots, mass-sent pitches, pure fan messages with zero business context
- Group chats
- Anyone the log shows this skill already messaged (`sent`) or already closed out (`skipped`, including `declined`). Never double-send a revival message; if they didn't reply to the first one, that's an answer.

When a thread is genuinely ambiguous, draft it anyway and flag the doubt in the batch line. The creator arbitrates in the checkpoint, that's what it's for.

## Crafting the message

The draft must pass one test: could this exact message have been sent to anyone else? If yes, rewrite it. Personalization means one concrete detail from their profile plus the specific thing they originally wanted, welded together.

Rules:
- 1 to 3 sentences, under about 40 words. It's a DM, not an email.
- One paragraph, no line breaks. Enter sends on IG web, so a draft with a newline in it goes out half-typed.
- Write in the creator's voice per `voice-dna.md` at the project root (loaded in preflight; while it is still the stub, the Voice/Tone one-liner in the root `CLAUDE.md` is the fallback). Match the lead's register: if they write formal, ease off; matching them beats performing.
- Reference ONE specific, current thing from their profile, stated plainly. Observation, not flattery: "saw you're running the 6-week challenge again" works, "love your content!!" is banned.
- Tie back to what THEY asked or wanted in the old thread. That's the thread's reason to exist again.
- End with exactly one low-effort question. Easy to answer from a phone in one line.
- No links, no pitch, no mention of the offer in the re-opener, and nothing from the "What is NOT sold" list in `backbone/offer.md`.
- Banned: "just following up", "just checking in", "circling back", "hope you're well", any em dash, anything that smells like a sequence email.
- If the creator left them on read: open by owning it ("my bad, this got buried") before the re-engage. Never own it when they were the one who went quiet.

The examples below show the pattern (one profile detail + the thing they wanted + one easy question), not the topic or the register. Swap the topic for what they asked about in your niche, and take the register from `voice-dna.md`.

**Example, niche-neutral (they asked how you handle <the thing you teach>, profile shows a fitness coach mid-launch):**
> yo saw you're running the transformation challenge again, the check-in reels are clean. did you ever get <the thing they asked about> sorted or did it fall off the plate?

**Example, from an AI-automation creator (swap the topic for your niche) (asked price then ghosted, profile shows a realtor who just closed a listing):**
> congrats on the lakeview close man. still thinking about automating the listing content or did that fall off the plate?

**Bad (would get ignored, and deserves it):**
> Hey! Just following up on our conversation about the community. Let me know if you're still interested!

## State

Log lives at `outreach/dm-revival/log.json` relative to the project root (not inside this skill folder). One entry per handled thread:

```json
{
  "<username>": {
    "status": "sent | drafted | skipped",
    "reason": "lost-lead | active | member | friend | brand | spam | group | already-messaged | declined",
    "message": "final text if sent, draft text if drafted, empty if skipped",
    "thread_url": "/direct/t/<id>/",
    "date": "YYYY-MM-DD",
    "sent_at": "ISO 8601 timestamp with timezone (only when status is sent), e.g. 2026-08-17T14:32:05-04:00"
  }
}
```

Status semantics: `sent` and `skipped` are terminal (skip on every future run); `drafted` is a held draft that step 0 of the loop resurfaces once, after re-checking the thread. `declined` is the reason for a `skipped` entry the creator dropped or turned down twice. `sent_at` is what the cap preflight counts (today's sends against the 40/day hard stop, the last 60 minutes against the 15/hour pace); `date` is the day the entry was logged, whatever its status.

Check it before opening any thread, matching on `thread_url` (or header username once open). It's what makes the grind resumable across sessions and what guarantees nobody gets the same revival twice. Update it after every send and every skip, not in end-of-run batches: an interrupted session must not forget a message that already went out.

## Pacing and rails

These are replies inside existing threads, which Instagram tolerates far better than fresh outbound, but the account is the business. Protect it:

- 2 to 5 seconds between UI actions, and a longer beat between sends. Cap sends at about 15 per hour, hard stop at 40 in a day. Both caps are enforced from the log, not memory: before each batch, count `sent` entries by `sent_at` (today for the 40, last 60 minutes for the 15). The log spans sessions, so a fresh session inherits an earlier session's sends.
- Any "Try Again Later" banner, action-block warning, or send that visibly fails: stop everything immediately and tell the creator. Do not test the limit.
- If a send is interrupted or ambiguous, re-open the thread and check whether the message actually posted before even thinking about re-sending.
- Anything else weird twice in a row (layout shift breaking selectors, thread that won't load): stop and report, don't burn tokens retrying.

On stop (the creator's call or a rail): give the session tally in two lines, threads scanned / leads found / sent / skipped, and where the sweep left off.
