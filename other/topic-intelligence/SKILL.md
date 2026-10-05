---
name: topic-intelligence
description: Find and compare current creator or editorial topic candidates with AI Workstation Global Topic Radar, or build a research-ready brief for one supplied current topic. Use when the user needs a live-topic choice, a brief grounded in a current Radar card or a supplied topic name resolved against current Radar, or both in one workflow. Do not use for ordinary news or factual lookup, translation, rewriting, summarization, generic titles or ideas, platform-style advice, or complete supplied material that needs no current-topic decision.
---

# Topic Intelligence

Use one public Skill for current-topic selection and evidence-backed content
planning.

Before querying or reasoning, read `references/quality-contract.md`. Read
`references/selection-workflow.md` when selecting or comparing topics and
`references/brief-workflow.md` when the request includes a content brief.

## Choose exactly one mode

Infer the smallest mode that satisfies the request. Do not make the user choose a
mode name.

### Mode 1: selection only

Run one bounded live feed query, compare qualified candidates, and stop after the
requested shortlist or finalist. Do not add an unsolicited brief.

### Mode 2: brief for a supplied current topic

- Exact Radar ID/current card: preserve its identity and do not run feed to
  select again. Use `history <exact-feed-id>` only when movement matters. If an
  ID alone lacks enough facts, ask for the current card or explain the gap.
- Topic name without stable identity: run at most one bounded feed with
  `--q <supplied-topic-name> --lane raw` solely to resolve that same event.
  Accept only a clear semantic match, preserve its exact `id`, and never replace
  it with a more convenient topic.

### Mode 3: selection followed by brief

Run exactly one bounded selection feed, choose one finalist, preserve its exact
feed `id`, and build the brief from the same evidence. Do not run a second feed.
History is optional and finalist-only.

## Public runtime contract

The bundled helper may call only public no-cost `feed`, `sources`, and `history`
endpoints. The current host model performs comparison and editorial reasoning.
Resolve the helper from the loaded Skill root:

```text
scripts/topic_radar_client.py
```

Canonical commands:

```text
python3 <skill-local-helper> --timeout 30 feed --q AI --lane all --locale zh --market CN --max-age-hours 24 --limit 12
python3 <skill-local-helper> --timeout 30 sources
python3 <skill-local-helper> --timeout 30 history <exact-feed-id>
```

Requirements:

- use `python3`, never `python`, `python2`, or direct execution;
- every feed explicitly passes `--lane`, `--locale`, and `--market`; never rely on
  API defaults;
- place helper-wide options before the subcommand;
- pass the history ID as the sole positional argument;
- run each helper call as one standalone direct command;
- never combine it with pipes, `&&`, `;`, redirection, command substitution,
  backticks, a here-doc, `jq`, or another Python process;
- read JSON directly from stdout and never probe CLI syntax;
- never repeat a successful request to recover display-truncated output; use the
  returned JSON and mark unavailable fields unknown;
- never use a repository-root, sibling-repository, user-global, or copied helper;
- never use `--base-url` or an origin override in the official public workflow.

Ordinary selection starts with 12 candidates and never exceeds 24. Selection-only
and selection-followed-by-brief modes each use exactly one successful feed. For an
explicit large export only, paginate sequentially with identical filters and
`generated_at`, non-overlapping offsets, and a stop at `has_more=false`. Do not
merge pages from changed snapshots or retry completed pages.

## Explicit lane, language, and market

Infer `locale` from the answer language and `market` from the requested audience
or geography. With no explicit audience/market, use `zh` + `CN` for Chinese and
`en` + `GLOBAL_EN` for English.

- current/today's research-worthy topics: `lane=all` plus an explicit time window;
- strongest and sufficiently evidenced: `lane=curated`;
- accelerating/heating up: `lane=rising`;
- overseas-first/regional lead: `lane=market_lead`;
- early opportunity: `lane=early`;
- monitor but not ready: `lane=watch`;
- evergreen: `lane=evergreen`;
- web page “全部”/raw event pool: `lane=raw`;
- supplied-name resolution: `lane=raw` plus the exact name as `q`.

`raw` is the page's “全部”; API `all` is the candidate-lane union. Do not simulate
a lane with legacy `signal`/`trend_stage`, silently switch lanes, or force a topic
when the requested lane is empty.

## Live evidence gate

Current claims require a live Radar response obtained in this task, equivalent
current Radar data from a native host connection, or a current Radar response
explicitly supplied by the user. Never substitute model memory, sibling
repositories, snapshots, databases, fixtures, caches, logs, reports, exports, or
prior-task artifacts.

Inspect `generated_at`, `partial`, `stale`, `snapshot_age_seconds`, `refreshing`,
`source_status`, and topic evidence. Missing values are unknown, not zero. For
“current” or “today”, a supplied snapshot older than one hour or marked
`stale=true` cannot support a current acceleration claim.

Radar fields and evidence links are observations of what Radar returned, not
independent verification of external claims. Use links as research leads, prefer
primary sources, and place unresolved claims in `must_verify`.

## Selection invariants

- Preserve the user's domain in the first query and reject semantic substring
  collisions after retrieval.
- Treat duration, language, audience, tone, and format as editorial constraints,
  not source/platform filters.
- Read `editorial_lane(s)`, category/tags, `content_type`, `evidence_state`, the
  four component scores, classification/cluster confidence, rejection reasons,
  and `what_happened`/`why_worth_research`.
- Explain Radar's `trend_score`, `editorial_score`, `confidence_score`, and
  `market_fit_score` tradeoffs; never calculate a fifth host score.
- Count independent evidence by unique `independent_origin_id`, not collector,
  `source_id`, or display-name count.
- Use history for a finalist when a real rising/acceleration claim matters.
- Treat `market_lead` as a regional-lead observation, not proof of a measured
  domestic information gap.

For real-time selection, reject `marketing`, `routine_update`, and
`evergreen_advice` content unless explicitly requested. `unverified` is only a
research lead; `verified` is not independent external fact-checking.
`classification_confidence < 60` is normally not a finalist.
`cluster_confidence < 60` and non-empty `rejection_reasons` require disclosure.
By default, `watch`, `raw`, and `unverified` items cannot appear in
**recommendation** or become a Mode 3 finalist. They may be labeled as research
leads only. Unless the user explicitly asks to brief a research lead, report no
qualified recommendation and stop before the brief when no eligible finalist
remains.

## Output and brief invariants

Keep these layers visibly separate:

1. **Radar facts and evidence observations**;
2. **Radar deterministic editorial judgments**;
3. **Host editorial analysis**;
4. **recommendation**;
5. **unknowns / must_verify**.

Use all five headings even for a compact shortlist; never merge Radar fields and
host judgment into one candidate paragraph.

The first layer contains exact IDs, verbatim titles, timestamps, publishers,
canonical links, source roles/tiers, independent origins, source markets, history,
and factual limits. The second contains returned lanes, component scores,
evidence/confidence states, `why_worth_research`, and rejection reasons. End both
Radar layers before host comparison or recommendations. A **Radar title** or
**original title** label requires a verbatim copy.

For a brief, preserve one exact Radar `id` and include freshness, evidence/source
limitations, angle, audience payoff, hook, narrative beats, research questions,
preferred sources, `must_verify`, `avoid_claims`, unknowns, risks, and a
visual/material plan as relevant.

Radar's `editorial_score` and `market_fit_score` are deterministic estimates.
Radar does not measure actual audience size, topic/content saturation, real
user-demand volume, post-publication performance, future reach, or virality.
Audience and distribution conclusions remain host editorial judgments.

## Safety and cost boundary

- Never call anonymous/public `/insight` or another AI Workstation model-backed
  endpoint from the public Skill.
- Never embed a shared credential or ask the user to paste a private key.
- Optional Premium Topic Insight requires a native connection explicitly
  authenticated to the user's account and enforcing that user's quota; treat it
  as model analysis, not independent evidence.
- Never present any Radar score, target platform, or host judgment as a
  performance guarantee.
