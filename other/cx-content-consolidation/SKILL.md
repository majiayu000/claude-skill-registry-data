---
name: cx-content-consolidation
description: Use to merge overlapping help articles without breaking search, bookmarks, or AI grounding — choosing a canonical page, setting redirects, and measuring post-merge impact. Trigger for "we have duplicate KB articles", consolidate help centre content, merge knowledge base articles, KB deduplication, article redirects, canonical help article, or overlapping docs confusing customers and search.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Consolidating overlapping articles

Duplicate articles are not harmless clutter. **Search splits rank between two mediocre
pages instead of one strong one**, agents bookmark the wrong version, macros link
to different URLs, and customers find contradictory steps. Consolidation fixes that —
but careless merges **404 bookmarks, break macros, and temporarily spike contacts**
while search reindexes.

The prize: **one canonical article per question, old URLs still resolve, and
measured proof contacts did not rise.**

## When to merge vs keep separate

| Situation | Action |
| --- | --- |
| Same question, overlapping answers, same audience | Merge |
| Same topic, different audiences (customer vs developer) | Keep separate; cross-link |
| Same topic, different products/plans | Separate with clear scoping in titles |
| One is subset of the other | Merge into superset; retire subset |
| Contradictory facts | Merge after policy owner picks truth — do not publish merge until resolved |
| High views on both, low CAV on both | Merge + rewrite — duplication may be the clarity problem |

Measure contact-after-view on candidates before merging. **Merging two leaky
buckets without rewrite gives one bigger leaky bucket.**

## Choosing the canonical article

Pick one survivor before writing merged prose:

| Factor | Weight |
| --- | --- |
| Lower contact-after-view rate | Strong signal it actually helps |
| Higher assisted + unassisted resolution | Proven answer |
| More complete / accurate content | Factual winner |
| Better URL slug and title match to customer language | Findability |
| More inbound links and macro references | Migration cost favours keeping it |
| Newer `updated_at` with verified facts | Currency |

When in doubt, **keep the URL that macros, AI grounding, and external sites already
use** — migration cost beats marginal content quality.

Document the decision: canonical ID, retired IDs, merge date, owner.

## Merge procedure

**1. Inventory references**

- Inbound links from other articles
- Macros, canned responses, bot flows
- AI grounding / RAG document lists
- External links (status pages, app deep links, marketing)
- Search analytics — top queries landing on each URL

**2. Draft merged content**

- Single outline — dedupe, do not concatenate.
- Lead with the answer customers need in the first two sentences.
- Fold unique edge cases from retirees into "When this doesn't apply."
- One set of steps; remove contradictory versions.
- Policy owner sign-off on any fact reconciliation.

**3. Publish canonical first**

- Update survivor in place or publish merged replacement at canonical URL.
- Do not delete retirees yet.

**4. Redirect retirees**

- HTTP 301 (or platform equivalent) from old URL to canonical **anchor** if the
  section moved (`/refunds#timeline`).
- If platform lacks redirects: stub page with prominent link, not blank 404.
- Keep redirects **indefinitely** — bookmarks die slowly.

**5. Update references**

- Fix internal links, macros, AI corpus in same change window.
- Export pre-change macro list; verify post-change with spot checks.

**6. Deprecate metadata**

- Mark retired IDs `superseded_by: canonical_id` in CMS.
- Hide from search index and customer nav; keep staff-visible during transition if
  needed.

## Search and findability after merge

- **Title and H2s** must include query terms from *both* old articles' top searches.
- Submit sitemap / reindex if your platform requires it.
- Monitor **search zero-results** and **top queries with no click** for two weeks.
- Synonyms customers used in old titles — add as keywords or subheadings, not silent
  loss.

Split traffic articles often each rank for different phrases. **Merged article must
cover both phrase sets** or search traffic drops despite better content.

## Measuring post-merge impact

Baseline **two weeks before** and compare **two–four weeks after** (allow reindex
time):

| Metric | Healthy merge | Problem signal |
| --- | --- | --- |
| Contact volume on driver | Flat or down | Up — merged page unclear |
| CAV on canonical | Down or flat | Up — rewrite failed |
| Search clicks to topic | Up or flat | Down — rank loss |
| Agent citations to one URL | Consolidated | Still split — references missed |
| Broken-link reports | Flat | Spike — redirects missing |

If contacts rise, read samples before reverting — often a missing subsection from a
retired page, fixable with one H2 add.

## Rollback plan

Before merge:

- Export full body and metadata of all articles.
- Snapshot macro definitions.
- Note redirect map.

If rollback needed: restore retiree, reverse redirects, restore macros. **Do not
delete source content for 90 days.**

## Traps

- **Concatenation merge.** Two 800-word articles become 1,600 words nobody reads.
- **Keeping both live "temporarily."** Permanent duplicate; pick a cutover date.
- **Redirect to homepage.** Worse than 404 for intent; send to canonical section.
- **Merging before contradiction resolved.** Agents lose trust in KB entirely.
- **Ignoring locale merges.** Consolidate per locale; do not redirect EN to FR.
- **Deleting without reference sweep.** Macros keep sending customers to dead URLs.

## Present results to the user

1. **Merge candidates** — duplicate clusters with merge/kill/keep recommendation.
2. **Canonical choice** — with rationale and retired URL list.
3. **Merged draft outline or full text** — policy-signed where needed.
4. **Redirect and reference change list** — macros, links, AI corpus.
5. **Cutover checklist** — order of operations and rollback snapshot steps.
6. **Measurement plan** — baseline metrics, review date, success thresholds.
