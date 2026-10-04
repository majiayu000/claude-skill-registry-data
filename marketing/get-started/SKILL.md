---
name: get-started
description: >
  Set up a brand-new Marky account end to end, from your AI agent, in one sitting. Use this
  the first time someone connects Marky and has no business yet, or when they say "set me up",
  "get me started", "onboard me", or paste a prompt asking you to get their social media going.
  It creates their first workspace and brand kit from their website, walks them through
  connecting their first social account, learns from what they already post, and drafts their
  first few posts for approval — it never schedules anything without them saying go. Uses the
  marky-api, build-brand-kit, and plan-social-content skills for the actual work. For a full
  week of content once they're set up, see plan-social-content; for just the brand kit, see
  build-brand-kit.
---

# Get Started with Marky

This is the very first run for a new Marky account. The goal is to take someone from an empty
account to a handful of on-brand posts waiting for their approval — without making them touch
the onboarding wizard themselves. You do the setup; they just answer a couple of questions and
approve at the end.

**Read the `marky-api` skill first** for the `mk_live_` key, the base URL, and the MCP
connection. This skill drives Marky through the **MCP tools** and leans on two other skills for
the heavy lifting: `build-brand-kit` (workspace + brand) and `plan-social-content` (drafting).

**The approval gate is mandatory.** This flow ends at *drafts*, never at scheduled posts.
Publishing to someone's live accounts is brand-facing and irreversible-feeling; they review the
first batch and say go before anything is queued. Do not call `schedule_post` or `queue_post`
in this skill. Stop at `create_post` (which leaves a `NEW` draft) and hand off.

**Marky wants your feedback.** First-run is the most important flow to get right — if any step
breaks or confuses you, send Marky a note with the `submit_feedback` MCP tool. See the "Marky
wants your feedback" section in the `marky-api` skill.

## Before you start: are you connected?

Call `list_businesses`.

- **The call fails / you have no key or MCP connection** → you are not connected yet. Follow the
  install + connect steps in the `marky-api` skill (or the repo README), get the user signed in,
  then come back here.
- **The call returns one or more real businesses** → this account is already set up. This skill
  is for empty accounts; use `plan-social-content` or `suggest-topics` instead.
- **The call returns an empty list (or only a placeholder business)** → you're in the right
  place. Continue.

## Stage 1 — Create the workspace and brand kit

A good brand kit is what makes every future post sound and look like the business instead of
generic AI filler, so this comes first.

1. Ask the user for their website. One question: *"What's your website? I'll pull your logo,
   colors, and voice from it."* If they have no website, ask for their most active social
   profile — any page that carries their branding works.
2. **Run the `build-brand-kit` skill** with that URL. It visits the site, extracts the logo,
   colors, fonts, voice, and imagery style, shows the user the proposed kit, and — on their
   approval — creates the business and writes the brand profile via `update_business`.
3. If the user genuinely has no site or social presence, fall back to `create_business` with a
   name and a short description they give you, and set the voice from a couple of questions.

Note the `business_id` that comes back — every later step needs it.

## Stage 2 — Connect the first social account

Publishing can't work until at least one account is connected, and connecting is an
OAuth-per-platform step that only happens in the dashboard — there is no API for it. So you hand
the user a link and wait.

1. Tell the user which platforms Marky supports (Instagram, Facebook, LinkedIn, TikTok, X,
   Google Business, Pinterest, YouTube) and ask which one they want to start with. One is enough
   to get going; they can add more later.
2. Send them to their connect page:

   ```
   https://app.mymarky.ai/ws/BUSINESS_ID/business/profile
   ```

   (Replace `BUSINESS_ID` with the id from Stage 1.) Tell them: *"Open this, click the platform
   you picked, and approve the connection. Come back here when it's done."*
3. **Poll, don't guess.** Call `list_connected_social_accounts` for the business every 10–15
   seconds (or when they say they're done) until at least one account shows up with a `valid`
   status. Don't move on until you can see it — a confident "great, you're connected!" that turns
   out to be wrong is worse than waiting.

## Stage 3 — Learn from what they already post

If the account they connected has posting history, that's the richest possible signal for their
real voice and cadence — use it before you write anything.

1. `list_connected_social_accounts` gives you the connected integration(s). For one with
   history, pull their recent posts and stats:
   - `list_integration_posts` — what they've actually posted (topics, format, length, hashtags).
   - `get_integration_stats` — what landed (which posts got engagement).
2. Read for patterns, not just numbers: what subjects they cover, how long their captions run,
   how formal they are, whether they use emoji or hashtags, what their best post had in common.
   Fold this into the voice you'll draft in (and, if you keep a `writing-style.md` per the
   `plan-social-content` skill's storage rule, write it there so it compounds).
3. **Brand-new account with no history?** That's fine — skip this stage and lean on the brand
   kit's voice from Stage 1.

## Stage 4 — Draft the first few posts (for approval)

Now produce a small, strong first batch — enough to show the value, not a full month.

1. **Use the `plan-social-content` skill's drafting approach** to write 3–5 posts grounded in
   something real: the brand kit, the learnings from Stage 3, and a quick question or two about
   what's coming up for them (a launch, an offer, a seasonal moment). Quality over quantity —
   these are the posts that decide whether they trust Marky.
2. Create each one with `create_post`, which leaves it as a `NEW` draft in their queue. **Do not
   schedule.** No `schedule_post`, no `queue_post`, no `status: SCHEDULED`.
3. Show the user each draft — caption and, if you generated a graphic, the design — right in the
   conversation.

## Stage 5 — Hand off

You've done the setup; now it's their call.

1. Point them to their drafts to review, edit, and approve:

   ```
   https://app.mymarky.ai/ws/BUSINESS_ID/social-posts
   ```

2. Tell them plainly what you did and what's left: *"Your brand kit is set, [platform] is
   connected, and I've drafted 5 posts. Review them here — nothing publishes until you approve
   and schedule."*
3. Offer the obvious next steps:
   - "Schedule the ones you like — just tell me which and when."
   - "/plan-social-content for a full week. Ask me what's coming up first."
   - "Connect another platform and I'll post there too."
   - "/build-brand-kit again if the posts don't sound quite like you yet."

That's a complete first run: empty account → workspace → connected → learned → drafted →
approved. Everything after this is normal Marky use.
