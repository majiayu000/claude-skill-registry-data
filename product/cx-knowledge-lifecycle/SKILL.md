---
name: cx-knowledge-lifecycle
description: Use to assign ownership, set review cadence, and deprecate support content without breaking self-service or AI grounding. Trigger for "who owns this article", "our KB is out of date", orphan articles, annual review calendar nobody follows, deprecating help content, knowledge governance, or preventing stale articles from quietly harming customers.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Knowledge lifecycle governance

Most knowledge bases rot through **calendar review nobody completes**, not through
neglect. An article gets a yearly "review due" date, the reminder fires, someone
clicks through unchanged, and the system records it as current. Meanwhile the
product changed six months ago and the article customers actually read — because
search surfaces it — is wrong.

The prize is not a tidy review log. It is **articles that stay correct under the
load they carry**, with a clear owner when they drift, and a deprecation path that
does not 404 customers mid-journey.

## The failure modes

| Symptom | Fault |
| --- | --- |
| Articles have no named owner | Nobody is accountable when policy changes |
| Review is calendar-only | High-traffic stale content waits for a date |
| "Reviewed" means opened, not verified | False confidence; worse than no review |
| Orphan articles after reorg | Owner left; content drifts with no alerts |
| Deprecated articles deleted or 404'd | Broken links, search gaps, angry customers |
| Low-traffic articles reviewed first | Effort spent where harm is lowest |

## Assign ownership before cadence

Every published article needs **one accountable owner** — a role or team, not a
person's name alone. The owner is responsible for factual currency when the
underlying policy, product or process changes, not for prose polish.

| Owner type | Owns |
| --- | --- |
| Product / policy team | What is true — fees, eligibility, timelines |
| Support ops / KB lead | Structure, findability, deprecation, metadata |
| Localisation lead | Translation currency when source changes |

Orphan detection: articles whose owner role no longer exists, whose owner field is
blank, or whose owner has not logged in since the article was last materially edited.
**Orphans are the highest-risk stale content** — nobody receives the alert when the
topic changes.

## Review triggered by usage and staleness, not calendar alone

Calendar review is a backstop, not the engine. Prioritise review when **both** are
true:

1. **Staleness signal** — `updated_at` older than the last known change on that
   topic, or older than a topic-specific threshold (refund policy: 90 days; a
   feature overview: tied to release cadence).
2. **Usage signal** — views, search impressions, agent citations, AI grounding
   frequency, or contact-after-view rate above baseline.

A stale article nobody reads is housekeeping. **A stale article customers and agents
hit constantly is an incident waiting to happen** — treat it like one.

Suggested priority tiers:

| Tier | Trigger | Action |
| --- | --- | --- |
| P0 | High usage + confirmed policy/product change | Verify within days; unpublish if wrong |
| P1 | High usage + stale by age or drift signal | Full factual review |
| P2 | Medium usage + stale | Review on next sprint |
| P3 | Low usage + stale | Deprecate or merge candidate; do not spend a full review |

Low-traffic content does not need the same cadence as head articles. **Equal
calendar review for every article is how teams burn out and miss the ones that
matter.**

## What "review" means

A review is not opening the page. It is:

1. **Verify every factual claim** against current policy, product behaviour and links.
2. **Check findability** — do titles and headings use the words customers search?
3. **Check duplication** — does another article answer the same question differently?
4. **Record what changed** — `updated_at` must move only when content or metadata
   materially changed, not when someone clicked approve.

If nothing changed, say so explicitly in the review log. That is valid — but
distinguish "verified unchanged" from "nobody looked."

## Deprecation without 404ing customers

Never delete a published article customers may bookmark, that search indexes, or
that external sites link to. Deprecation is a **controlled wind-down**:

1. **Mark status** — deprecated, superseded, or archived (use your platform's
   equivalent; do not leave it looking live).
2. **Choose canonical successor** — one article, not three overlapping replacements.
3. **Redirect or prominent banner** — old URL resolves to the successor, or shows
   "This article is outdated — see [link]" above the fold.
4. **Update internal references** — macros, AI grounding lists, agent shortcuts,
   onboarding docs. Deprecation that only changes the help centre leaves agents
   citing the old page.
5. **Retain for audit** — keep the old body accessible to staff even if hidden from
   customers.
6. **Measure after 30–60 days** — contact rate on the topic, search failures for old
   terms, broken-link reports.

Hard deletion is only for drafts, duplicates never published, or content that was
factually harmful and has no legitimate reason to exist.

## Governance rhythm

| Activity | Cadence |
| --- | --- |
| Orphan scan | Monthly |
| P0/P1 review queue | Weekly |
| Owner accountability check | Quarterly — can each owner name their top 5 articles? |
| Calendar backstop for long-tail | Annual, P3 only |
| Post-incident KB check | Within 48h of any policy or product change that affects customers |

Tie KB updates to **change management**, not documentation sprints. When policy
changes, the article owner is in the same Slack thread as the announcement — not
discovering it from a customer ticket three weeks later.

## Traps

- **Review completion rate as a KPI.** Teams game it; wrong articles get marked
  reviewed.
- **Equal ownership of the whole KB.** "Support owns the KB" means nobody owns
  anything.
- **Deprecating without checking AI and macro references.** The article vanishes from
  the help centre but still grounds answers.
- **Assuming low views means safe to delete.** Unused in conversation matching is not
  the same as unused in reality — check views and agent citations first.
- **Publishing a replacement before redirecting the old URL.** You now have two
  live answers and split traffic.

## Present results to the user

1. **Orphan and unowned article list**, with usage tier attached.
2. **Priority review queue** — usage × staleness ranked, not alphabetical.
3. **Proposed ownership map** — role per article or section, with gaps named.
4. **Review policy** — tier definitions, triggers, and what "done" means.
5. **Deprecation candidates** — with successor, redirect plan and reference check
   list (macros, AI, internal wiki).
6. **Governance calendar** — what runs weekly, monthly, quarterly; tied to change
   management not documentation theatre.
