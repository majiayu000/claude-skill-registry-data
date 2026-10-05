---
name: cx-article-effectiveness
description: Use to measure which help articles actually resolve contacts versus merely being read, including contact-after-view and assisted resolution. Trigger for "are our help articles working", article view counts misleading, deflection measurement, contact after reading an article, self-service success metrics, KB ROI, or stopping AI agents from optimising for page views.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Measuring article effectiveness

View counts are the most dangerous metric in self-service. **A high-traffic article
that precedes a contact is a failure, not a success** — customers read it, did not
get what they needed, and wrote in anyway. Teams celebrate the traffic; the contact
rate tells the truth.

The question is not "did they read it?" It is **"did reading it remove the need to
contact?"**

## Views are not resolution

| Metric | What it actually measures | What it cannot tell you |
| --- | --- | --- |
| Page views | Exposure | Whether the problem was solved |
| Time on page | Engagement (ambiguous) | Whether they found the answer or gave up |
| Search clicks | Findability | Whether the destination helped |
| Helpful votes | Sentiment of readers who bother | Selection bias; no contact linkage |
| Deflection rate (platform) | Vendor-defined, often optimistic | Methodology varies; rarely auditable |

An article can have high views because it ranks well, because the title promises
something it does not deliver, because agents link it habitually, or because the bot
surfaces it before handoff. **None of those imply resolution.**

## Core effectiveness signals

Build analysis from conversation exports linked to article events. Exact event names
vary by platform; the logic does not.

**1. Contact-after-view (CAV).** Customer viewed article A, then opened a ticket on
the same topic within a defined window (typically 24–72 hours, same session where
possible). **CAV rate = contacts after view ÷ views.** High CAV means the article
is a waypoint to contact, not a substitute.

Segment CAV by:

- Channel of follow-up contact
- Topic / contact driver
- Whether the contact was resolved on first reply (article may have partially helped)
- New vs returning customer

**2. Assisted resolution.** Contact happened, but the agent's reply closely matches
the article — detected by phrase overlap, macro linkage, or explicit article URL in
the reply. The customer contacted; the article still did the work. **Without this
signal you over-penalise articles agents rely on silently.**

**3. No-contact resolution (true deflection).** Customer viewed the article; no
contact on that topic within the window. Hard to prove causation; treat as an upper
bound, not proof. Still useful for comparing articles on the same topic.

**4. Agent citation rate.** How often agents paste or link the article. High citation
+ high CAV = agents use it but customers still struggle alone — a findability or
clarity problem. High citation + low CAV = agent-assisted self-service; the article
works when a human frames it.

**5. Repeat contact on same topic.** Customer contacted, was told to read the
article, contacted again. The article failed twice.

## Ranking articles: useful vs harmful

| Pattern | Views | CAV | Interpretation |
| --- | --- | --- | --- |
| Workhorse | High | Low | Genuinely deflecting; protect and keep current |
| Leaky bucket | High | High | Priority rewrite or merge; actively wasting customers' time |
| Hidden gem | Low | Low | May prevent contacts you cannot attribute; check agent citation |
| Dead weight | Low | High | Wrong topic, wrong audience, or unfindable for the real question |
| Bot favourite | High (bot-surfaced) | High | AI/bot routing problem, not just content |

Sort findings by **estimated contact volume attributable to failure**, not by view
count. A leaky bucket on a high-volume driver beats a dead weight article every time.

## AI grounding and view-count misuse

Teams grounding AI agents in "top viewed" articles replicate the view-count mistake
at scale. An AI agent citing a high-CAV article **automates the path from unhelpful
content to confident wrong answers.**

Before prioritising articles for AI grounding:

1. Exclude high-CAV articles until rewritten.
2. Prefer articles with low CAV *or* high assisted resolution with agent-verified
   accuracy.
3. Never use views alone as a inclusion criterion.
4. Monitor **contact rate on conversations where the AI cited an article** — the
   article-level CAV equivalent for the bot channel.

A missing article produces escalation. **A wrong high-traffic article produces
automated misinformation.**

## Analysis procedure

1. **Export article events** — views, searches, clicks — with article ID and
   timestamp.
2. **Export conversations** — customer ID (or pseudonymous session), topic/driver,
   created_at, channel.
3. **Join on customer/session + time window** to compute CAV. State the window and
   match rate so the reader knows coverage.
4. **Compute assisted resolution** where agent replies are available.
5. **Read samples from the high-CAV head** — lexical matching and CAV both need
   human confirmation. The article may be fine but titled wrong; the contact may be
   a different sub-question.
6. **Compare before/after** for any article you rewrite — CAV should move, not just
   views.

If you cannot link views to contacts (anonymous help centre, no session stitching),
say so explicitly. **Report findability and content-quality findings from samples
instead of pretending CAV exists.**

## Traps

- **Attributing all post-view contacts to the article.** Customer may have read
  three pages; credit the last one cautiously or analyse path sequences.
- **Short CAV windows miss delayed contacts.** Refund questions contact three days
  later; tune window by topic.
- **Platform deflection numbers as ground truth.** Always show your methodology.
- **Penalising articles agents love.** Split customer-alone CAV from assisted paths.
- **Optimising titles for clicks.** Clickbait titles inflate views and CAV together.
- **Ignoring mobile vs web.** Different search behaviour; segment if sample size allows.

## Present results to the user

1. **Methodology summary** — join logic, time window, match rate, data gaps.
2. **Article ranking by failure impact** — high views × high CAV first, with volume
   estimate.
3. **Workhorse list** — low CAV articles worth protecting and keeping current.
4. **Assisted resolution findings** — articles that work with agent help but fail
   alone (rewrite for customer self-serve).
5. **AI grounding recommendations** — include/exclude/review lists with CAV evidence,
   not view rank.
6. **Sample tickets** for the top leaky buckets — concrete evidence for rewrites.
7. **Before/after baseline** if a measurement repeat is planned after content changes.
