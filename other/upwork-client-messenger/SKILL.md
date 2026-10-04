---
name: upwork-client-messenger
description: Draft mid-contract messages to a freelance client on Upwork or similar platforms. Use when the user needs to deliver delay news, push back on scope creep, raise their rate, end a contract gracefully, or ask for a review. Triggers include "reply to my client", "tell the client it's delayed", "client keeps adding scope", "raise my rate", "end this contract", "ask for a review", "client is ghosting". Input is the situation plus the relevant thread context, pasted. Drafts in the voice of a working professional peer, never a permission-seeker.
---

# Upwork Client Messenger

Mid-contract messages decide whether a contract ends in a review and a referral or in silence. Method extracted from a Top Rated Plus freelancer's real client threads across long and short engagements, plus published guidance. The through-line: state facts plainly, never litigate, and let structure do the negotiating.

## Inputs

1. **The situation** (which of the five below).
2. **Thread context**, pasted: what was agreed, what changed, the client's last few messages.
3. **Engagement type: long-term relationship or short transactional contract.** Several moves below fork on this; ask if unclear. If it isn't stated and can't be inferred, ask once and draft both closings so the user isn't blocked on your question.

Profile shortcut: if a stored profile file exists (`upwork-profile.md` in the working directory or `~/.claude/`), read identity and rate context from it and ask only for what's missing or not stated concretely (a rate line that says "ask me" means ask).

## Voice (hard, applies to all five)

Professional peer, warm and short. Contractions, plain words, no em dashes. **Banned: permission-seeking and apology stacking.** "Can I possibly ask if maybe" is the junior register; the working register states facts and asks one clear question. One apology maximum when apologizing is warranted, then move to the plan.

## 1. Delay news

Lead with the revised date in the first line; never bury it under context. Then, in order: what is already done (specifics build trust), the honest ETA with its hedge stated plainly ("aiming for Thursday, can't fully lock it yet"), and a promise to flag the moment it's ready. No over-promising to soften the moment; a slipped second deadline costs more than a conservative first one.

When the delay is the client's, zero pushback: well wishes, confirm no rush. Holding a client to a date they slipped buys nothing and spends goodwill.

## 2. Scope creep (the fork that matters most)

First, classify with the repeated-game rule:
- **First small extra ask from a good long-term client:** do it, and name it as a courtesy in the same message ("happy to include this one; it sits outside our original scope, so flagging it"). The boundary is set without a confrontation.
- **Large ask, any client:** always bill, framed forward: "Let me scope that properly and send you a number." Never a flat no; the counter-offer form ("I can get it to you by Friday instead, will that work?") declines the terms while accepting the relationship.
- **Chronic pattern of free-work asks:** stop litigating individual asks; price the pattern into the next engagement's rate.

Then draft by engagement type:
- **Long engagement: quantify, never litigate.** Separate the quick fixes from the heavy scope, give estimates with caveats for what's outside your control, name the cumulative overage factually (count the change requests, name two examples that fell outside the brief), and close with a relationship check-in ("are you happy with how this has been going?") instead of a demand. Stated facts plus an open question reliably invites the client to propose the paid phase themselves, which lands better than any invoice argument.
- **Short transactional contract: name the number.** "We haven't talked about pricing for the extended scope; for these pages I'd add [amount]." Direct works fine when there's no long relationship to choreograph. If they counter reasonably, accept and move on.

When a large ask lands on a short transactional contract, timing follows the large-ask rule: give the number on the spot only if you can estimate it confidently, otherwise commit to a date for it. Naming the number never means guessing it.

## 3. Rate increase

Honest note first: this is the least-scripted move in the method, because no full playbook survives contact with real clients. What holds:

- **Never open from a weak position or with the number.** Open with alignment: a short call or message "to align on scope and what's next before we formalize."
- **Cite tenure and delivered volume** as the factual base ("over the past six months I've shipped X, Y, Z for you").
- **Mirror the client's own words.** Quote back what they've said about the work, then let them elaborate before the ask lands. Their praise, restated by them, is the strongest argument available.
- **Pair the ask with a reciprocal offer** (priority availability, expanded scope) so it reads as a next chapter, not a toll.
- **Wait for a green-light mood.** Timing beats phrasing; a rate ask during a fire costs the relationship points that the best wording cannot buy back.

## 4. Ending a contract

Before any message: verify the deliverables against the original brief, so the close opens from "everything agreed is delivered."

The message: warm, short, states the condition plainly ("looks like the task list is complete on my side"), proposes closing, and treats the close as a continuity moment: interest in future work, openness to referrals. **Ask the client to be the one who closes the contract**, because the review prompt fires reliably on their side, not yours. No soft ultimatums ("I'll close it myself eventually"); that register reads as a threat shrunk to fit politeness.

## 5. Review ask

One line, low pressure, bundled with a completion message, never standalone: "All done, let me know if there's anything else I can help with. And if you don't mind, a review would mean a lot." If the client is new to the platform, add the mechanics in one sentence, and fold in the contract-close ask from move 4, since the close is what triggers their review prompt.

## Privacy rule (hard)

Drafts never reference other clients by name, other projects' details, or specific rates from other engagements. Each thread is a sealed room.

## Sources and provenance

Method extracted from a Top Rated Plus freelancer's real client threads (2025-2026, long and short engagements), with the two-tier scope approach and the delay pattern taken from documented exchanges that resolved well. Published guidance:

- How To Avoid Scope Creep: https://www.upwork.com/resources/how-to-avoid-scope-creep
- What To Do Before a Contract Closes: https://www.upwork.com/resources/what-to-do-before-contract-closes
- When To Renegotiate: https://www.upwork.com/resources/renegotiate
- Third-party: the repeated-game client framework (Squareblack Blueprint); Nick Saraev on review mechanics.

This skill is not affiliated with or endorsed by Upwork.
