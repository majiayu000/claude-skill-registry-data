---
name: upwork-invitation-responder
description: Respond to an Upwork "Invitation to Interview" fast and well. Use when the user pastes a job invitation they received on Upwork and wants to accept it, decline it, or decline it while referring another freelancer. Triggers include "got an Upwork invite", "decline this invitation", "reply to this invite", "client invited me", "should I take this invitation". Drafts the reply; helps triage borderline invitations first. Companion to upwork-proposal-writer (which handles the full proposal after an accept).
---

# Upwork Invitation Responder

Invitations are not job applications. The client already handpicked this freelancer's profile and is asking for a proposal. That changes the reply's job: the credibility argument is half-won, speed and clarity do the rest. Method extracted from a Top Rated Plus freelancer's real invitation threads plus Upwork's published guidance.

## Inputs

1. **The invitation** (job post or invite message), pasted.
2. **The user's decision**: accept, decline, or unsure. If unsure, run the triage below first.
3. For accepts: one portfolio link matched to the job. For decline-with-referral: the referral's name and whether the user has already told them.

Profile shortcut: if a stored profile file exists (`upwork-profile.md` in the working directory or `~/.claude/`), read identity, niche, and links from it and ask only for what's missing or not stated concretely (a rate line that says "ask me" means ask).

## Rule zero: always respond, same day

Silence is the worst possible reply, and it is not private: the job's activity panel shows clients a counted "Unanswered invites" stat next to "Invites sent." An ignored invitation is a visible number on the client's screen. Every invitation gets an answer, even a two-line decline. If invitations arrive faster than the freelancer can handle, the fix is the profile availability setting ("Not Available"), never silence.

## Triage (when the user is unsure)

Three questions, thirty seconds:

1. **Would you do this work at your current rate?** If the answer needs a rate raise to become yes, it's a decline.
2. **Does your portfolio already prove this niche?** If proving fit requires explaining, the client picked the wrong person; decline or refer.
3. **Do you have capacity inside their timeline?** Busy-but-interested is still a decline (or a referral), never a slow maybe.

Two or three yeses: accept. Otherwise pick the decline move that fits.

Question 1 is a hard gate. If getting to yes needs a rate raise, it's a decline no matter how the other two land.

## Accept

Three or four sentences maximum. No sales copy: the client already chose this profile.

Shape: thank them for the invite, name the specific thing in their brief you'd start with (proves you read it), attach one matched portfolio link, close with one clarifying question or availability for a quick chat. If the client proposed a call, agree immediately and offer two time slots. The full proposal, when required, hands off to the upwork-proposal-writer skill.

Two mechanics worth knowing on accepts: Upwork's own UI states a video reply gets proposals noticed up to 31% more often (it costs extra Connects, so reserve it for invitations worth winning), and Uma now drafts invitation replies for everyone, which means a generic grateful reply is the baseline. Specificity about THEIR brief is what a handpicked freelancer's reply must add.

## Decline: three moves

All three share the same skeleton: **thank first, decline in the first sentence, give the real reason plainly, never apologize twice, never invent an excuse.** One or two sentences plus the closer.

**Move 1: decline and refer (the goodwill machine).** For good jobs you can't take. Thank them, say you're committed to other projects, refer a specific freelancer you can vouch for, and vouch in one line ("we've worked together; they have my full backing"). This converts a lost job into goodwill with the client AND a favor to a peer. Two rules: only refer someone whose work you'd stake your name on, and message the referred freelancer first so the handoff lands warm, not cold.

**Move 2: decline, not a fit.** For mismatched jobs. Thank them, say plainly the job isn't a fit for your skills, and leave the door open: "I hope we can work together on something closer to my lane." No fake busyness; clients respect an honest not-my-thing and remember it when the right job comes. Not a fit covers budget as well as skills. When the skills match but the budget can't reach your rate, say the job isn't a fit at this budget; never claim a skills mismatch that isn't true.

**Move 3: decline, at capacity.** For fine jobs at the wrong time. Thank them, say you're fully booked, keep the door open for future work. If they're worth staying visible to, invite them to reach out for the next project.

Upwork's decline flow also asks for a dropdown reason; tell the user which one matches the move (for example "Budget too low" or "Not a good fit").

## Voice rules (hard)

- One to two sentences per move plus the closer. An invitation decline is not an essay.
- Write like a person: contractions, plain words, warm but unapologetic.
- No em dashes. No "unfortunately" more than once. No "I'm honored."
- Never include contact information in the reply (platform policy).
- Never name-drop other clients or their projects in a decline.

## Sources and provenance

Method extracted from a Top Rated Plus freelancer's real invitation threads (design/dev niche); decline moves generalized from templates used across dozens of invitations. Official guidance:

- How To Reply to an Upwork Job Invitation: https://www.upwork.com/resources/job-invitation-reply

This skill is not affiliated with or endorsed by Upwork.
