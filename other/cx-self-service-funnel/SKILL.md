---
name: cx-self-service-funnel
description: Use to analyse the help-centre funnel from search through article view to contact, find actionable drop-off, and align KB content to contact drivers. Trigger for "self-service funnel", "contact after viewing an article", "why doesn't the help centre deflect", KB deflection rate, search-to-contact conversion, or article effectiveness.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Self-service funnel analysis

Teams report **article views** and **ticket volume** as if one explains the other.
They do not. A customer can read three articles and still open a ticket — and that
sequence is usually a **self-service failure**, not success. The funnel you need is:

```
search (or land) → article view → [optional: in-article action] → contact (or exit)
```

Without instrumented steps and a **contact-after-view** flag, you are optimising
page traffic while contacts stay flat.

## Define the funnel steps

| Step | Event | Minimum fields |
| --- | --- | --- |
| **Enter** | Search submit or direct article land | `session_id`, `timestamp`, `query` or `article_id` |
| **View** | Article body rendered | `article_id`, `session_id` |
| **Engage** | Scroll depth, time on page, clicked CTA | optional but useful |
| **Resolve signal** | "Helpful" vote, flow completion, no contact in window | `session_id`, `customer_id` |
| **Contact** | Ticket/chat/call opened | `customer_id`, `timestamp`, `channel` |

**Contact-after-view (CAV)** — contact within a defined window (often 24–48h) after
an article view in the same session or for the same `customer_id`:

```
CAV rate = contacts after view / article views   (not "deflection")
```

High CAV on an article means **the article is associated with failure** — wrong
content, stale steps, missing prerequisite, or it describes a problem you cannot
self-resolve. That is the prioritised fix list, not "low views."

## Instrumentation requirements

If any of these are missing, state what you cannot conclude:

| Gap | Consequence |
| --- | --- |
| No search logging | Cannot diagnose findability vs content |
| Anonymous views only | Cannot link to tickets |
| Ticket opens not tied to identity | CAV is understated |
| Bot and KB on different sessions | Double-count or miss paths |
| No article version on view event | Stale fixes look ineffective |

Join keys: **`customer_id`** when logged in; **`session_id`** with careful TTL for
anonymous; never rely on email subject matching.

## Diagnose drop-off by stage

| Drop-off pattern | Likely cause | Action |
| --- | --- | --- |
| Search, no click | Findability, titles, synonyms | Query clustering, title rewrites |
| Click, immediate bounce | Wrong result ranked first | Snippet quality, intent routing |
| Long read, then CAV | Content wrong or incomplete | Rewrite against resolved tickets |
| High views, low CAV, high contacts elsewhere | Article fine; process blocks self-serve | Fix product or policy path |
| No search, direct land, CAV | Links from product/errors | In-app copy vs KB parity |
| Views falling, contacts flat | Traffic shifted to bot or phone | Cross-channel funnel |

## Match KB to contact drivers

Export top contact drivers (taxonomy or tags) and map each to:

1. **Primary article** — exists? accurate? last updated?
2. **CAV rate** and **view volume**
3. **Contained bot sessions** on same intent, if applicable

| Driver tier | KB priority |
| --- | --- |
| High volume + high CAV | Rewrite immediately |
| High volume + no article | Write net-new |
| Low volume + high CAV | Fix or delete misleading article |
| High views + low CAV | Candidate for promotion / in-app link |
| Stale + high views | Harmful — update before new content |

An article that ranks well in search but drives CAV **suppresses deflection** —
customers waste time before contacting anyway. That is worse than no article.

## Success metrics that are not vanity

| Metric | Use | Misuse |
| --- | --- | --- |
| **CAV rate by article** | Prioritise fixes | Sole deflection KPI |
| **Search success rate** | Findability | Ignoring content quality |
| **Contacts per 1k MAU** | Holistic self-service | Blaming support for product bugs |
| **Issue-level self-serve rate** | Requires identity + driver | Article views alone |

**True deflection** requires knowing whether the contact would have happened without
self-service — historical funnels only describe association. Holdouts and matched
pre/post at driver level are stronger when you need a causal claim.

## Traps

**"Helpful" votes.** Satisfied readers vote; angry readers contact. Votes skew
positive; CAV catches the rest.

**Publishing more articles.** Coverage without CAV analysis increases findability of
wrong answers.

**SEO traffic.** External hits inflate views; segment logged-in and in-app paths.

**Contact button on every page.** Makes CAV the rational choice; measure button
placement experiments.

## Present results to the user

1. **Funnel counts** — search → view → contact with conversion rates at each step;
   define the attribution window used.
2. **Top CAV articles** — volume, driver mapping, staleness, suggested fix type
   (rewrite, merge, deprecate, in-app only).
3. **Search gap list** — queries with no click or high click-then-CAV.
4. **Driver coverage table** — top N drivers vs KB asset and CAV rate.
5. **Instrumentation gaps** — what biases the funnel (identity, session, channel).
6. **Prioritised actions** — ordered by expected contact reduction, not page views.
