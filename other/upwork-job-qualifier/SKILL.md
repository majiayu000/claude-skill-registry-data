---
name: upwork-job-qualifier
description: Decide whether an Upwork job post is worth applying to before spending Connects. Use when the user pastes an Upwork job post (or invitation) and wants a verdict (apply, skip, or apply with caution). Triggers include "is this job worth it", "should I apply", "check this job post", "is this client legit", "worth my Connects", "red flags in this job". Screens for scams, bad-client patterns, and dressed-up low-tier work, then weighs the Connects economics. Companion to upwork-proposal-writer (after an apply verdict) and upwork-invitation-responder (after a skip verdict on an invitation).
---

# Upwork Job Qualifier

Every proposal costs Connects, and the platform's own AI will never tell a freelancer to keep their money: application volume is the platform's revenue. This skill's whole job is the advice that structurally cannot come from inside: **when not to apply.** Method extracted from a Top Rated Plus freelancer's real invitation ledger and vetting decisions, plus Upwork's own published scam and client-screening guidance.

## Inputs

1. **The job post**, pasted in full.
2. **The "About the client" panel**, pasted: payment verified or not, total spent, number of hires, average hourly rate paid, hire rate, member-since date, and the category the job is filed under. This panel decides more verdicts than the job text does. If the user didn't paste it, ask for it before ruling.
3. The user's rate and niche, so the math below has a reference point.

Profile shortcut: if a stored profile file exists (`upwork-profile.md` in the working directory or `~/.claude/`), read rate and niche from it and ask only for what's missing or not stated concretely (a rate line that says "ask me" means ask).

## Instant skips (any one of these ends the evaluation)

- Any request to pay a fee, buy anything, do unpaid test work, or accept payment outside Upwork.
- Pressure to move communication off-platform before a contract exists.
- Requests for personal information beyond a normal work discussion.
- Payment not verified AND no spend history, on a job promising premium rates.
- A post with no scope, no budget signal, and careless writing throughout. Vague titles with empty descriptions are the fake-post signature.

## The client-history cross-check (the highest-value move)

Job titles are marketing. The client's history is data. Run the math:

- **Spend per hire:** total spent divided by hires. A "specialist" job from a client averaging under $100 per hire is a low-tier gig wearing a nice title.
- **Average hourly rate paid vs the user's rate.** A client who has paid $8/hr across twelve hires will not pay $80/hr for hire thirteen.
- **Category coherence:** a premium-sounding title filed under General Virtual Assistance, with data-entry skill tags, is telling the truth in the metadata and lying in the title. Trust the metadata.
- **On invitations: the personalized note carries no signal.** Invite notes are often templated. The client's posting history is the signal; the flattery is not.

Worked example (anonymized, from the method author's real ledger): a "$20 Shopify CRO Specialist" invitation looked plausible until the panel showed roughly $48 spend per hire, a $7.59 average hourly rate paid, and a General Virtual Assistance category history. Verdict: data-entry-tier work in a specialist costume. Declined, with a reply, because unanswered invitations are a visible stat.

## Soft flags (two or more means apply-with-caution or skip)

- "I promise you'll get a 5-star review" or any review offered as payment.
- Price pressure before scope discussion ("can you cut me a deal").
- "The last freelancer was terrible" used as leverage. That story usually has two sides, and the next chapter stars the user.
- A chaotic, unstructured brief where requirements arrive as a stream of consciousness.
- Rushed hiring with no questions asked. Clients who hire in an hour churn just as fast.
- Job posted more than ~48 hours ago with many proposals already: a weaker use of Connects regardless of quality, since early proposals capture the client's attention.
- Fixed-price with a large scope and no visible budget number: flag it, that combination is where scope creep lives.

## Positive signals

- Payment verified, real spend history, and an average paid rate within reach of the user's rate.
- Scope, deliverables, and budget stated plainly. Clients who write clear briefs run clear projects.
- The client's past jobs live in the same category as this one, at consistent rates.
- Posted recently, moderate proposal count: the window where a strong proposal actually gets read.

## Connects economics (the money math)

- Connects cost real money (~$0.15 each purchased; a limited free monthly allotment otherwise, more with Freelancer Plus). Every application is a purchase decision.
- Boosting is an auction: winning bids commonly run 10-20 Connects for a top-4 slot, roughly 17% more likely to be seen, with first place historically converting around twice as often. **Boost only strong-fit jobs from verified high-quality clients.** Boosting a weak fit is paying extra to lose faster.
- Decision rule: the worse the client-history math, the lower the acceptable Connects spend. A job that fails the cross-check is worth zero Connects, however good the title feels.

## When the user has no track record yet

The math above assumes a freelancer with a position to protect. Someone with no reviews and no badge is running a different calculation, and pretending otherwise gives them advice built for a situation they are not in. What changes:

- **Winnability enters the verdict, not just worth.** A job can pass every client-history check and still be a poor use of Connects for a beginner, because clients who filter on Job Success Score or badge tier will never see the proposal. Weigh that in, and prefer jobs where the client has few or no prior hires: they are less likely to be filtering on credentials that a beginner does not have yet.
- **Scope small on purpose.** A first contract that finishes cleanly and earns a genuine review is worth more than a larger one that stalls. Favor tight, well-defined jobs over ambitious ones, for now.
- **Scam screening matters more here, not less.** New freelancers are targeted precisely because they are eager and have nothing to lose by taking a risk. Every instant skip above stays absolute at this stage. This is the one part of the method that does not soften for beginners.
- **The rate-gap rule loosens slightly, and only deliberately.** A client paying below the user's target rate is normally a skip. At zero reviews it can be a considered tradeoff for the first two or three contracts, if the scope is small and the client history is clean. Name it as a tradeoff with an endpoint, never as a habit.

Honesty note: this method was extracted from an established freelancer's ledger. The beginner adjustments above are reasoned from the same evidence rather than lived at that stage, and the verdict should say so when it leans on them.

## Verdict format

No client panel, no verdict. If the About the Client panel wasn't pasted, reply with a HOLD: list what the post alone shows, flag any risks, and request the panel (payment verified, total spent, hires, average rate paid, member since). Never rule APPLY or SKIP on job text alone.

One short paragraph: **APPLY / SKIP / APPLY WITH CAUTION**, the top two or three reasons in plain language, and the next step. On APPLY, hand off to upwork-proposal-writer. On SKIP for an invitation, hand off to upwork-invitation-responder, because silence is a visible stat and a graceful decline is free. On CAUTION, name exactly what to verify before spending (usually one clarifying question to the client).

## Voice rules (hard)

- Verdict first, reasons second, no hedging paragraphs.
- No em dashes. Plain words, contractions fine.
- Never shame the user's pipeline; a thin month makes bad jobs look better, so state the math and let it argue.

## Sources and provenance

Method from a Top Rated Plus freelancer's real invitation ledger (40 invitations, 2022-2026) and documented vetting decisions. Official guidance:

- How To Spot Fake Job Posts: https://www.upwork.com/resources/spotting-fake-job-posts
- Upwork Scams To Watch For: https://www.upwork.com/resources/upwork-scams
- Client Red Flags: https://www.upwork.com/resources/client-red-flags
- Why Are My Proposals Not Being Viewed: https://www.upwork.com/resources/why-are-my-proposals-not-being-viewed
- How To Boost a Proposal: https://www.upwork.com/resources/how-to-boost-proposal
- Third-party: Evan Fisher's worst-clients breakdown (YouTube).

This skill is not affiliated with or endorsed by Upwork.
