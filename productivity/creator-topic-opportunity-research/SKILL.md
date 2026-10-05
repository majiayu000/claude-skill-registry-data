---
name: creator-topic-opportunity-research
description: Compare and prioritize live topic candidates for creator or editorial publishing decisions using AI Workstation Global Topic Radar. Use when the user is choosing what to research, cover, or publish based on acceleration, early-opportunity signals, freshness, platform or region differences, or cross-market timing.
---

# Creator Topic Opportunity Research

Use this Skill for **current topic discovery and trend interpretation** based on AI Workstation Global Topic Radar.

Do not use model memory as a substitute for live trend data.

## Host quality contract

Before mapping user constraints to Radar filters, making audience/editorial judgments, or composing into Brief, read and follow:

```text
references/quality-contract.md
```

The public Skill cost boundary is strict:

- bundled/public runtime may use only `feed`, `sources`, and `history`;
- do not call anonymous/public AI Workstation model-backed `/insight`;
- use the **current host model** for comparison and editorial reasoning;
- do not embed/share a server credential or ask the user to paste one into chat;
- server Topic Insight is optional Premium analysis only when a native authenticated AI Workstation connection explicitly provides it and enforces the user's membership/quota.

## Product boundary

Global Topic Radar already owns:

- public-source collection;
- normalization and clustering;
- `opportunity_score`;
- `trend_stage`;
- trend/history calculations;
- source health and stale-data handling.

This Skill owns intent interpretation, efficient querying, freshness/evidence checks, comparison, cross-market reasoning, and creator/editorial recommendations.

Never recreate a score from raw fields when Radar already supplies it.

## Live-data gate

Before claiming that a topic is current, rising, accelerating, new, or region/platform-specific, obtain a live Topic Radar response.

The public no-cost contract is:

- `GET /api/v1/ai/topic-radar/feed`
- `GET /api/v1/ai/topic-radar/sources`
- `GET /api/v1/ai/topic-radar/history?topic_id=...`

Use the official `https://aiworkstation.cn` origin in the normal public Skill workflow. Use a custom `--base-url` or `AIWORKSTATION_TOPIC_RADAR_BASE_URL` only when the user explicitly asks to test a self-hosted/development Radar origin; identify that origin as non-official evidence in the result.

### Self-contained runtime

Resolve the bundled helper relative to this `SKILL.md`:

```text
scripts/topic_radar_client.py
```

Invoke that Skill-local helper only with `python3`. Do not use `python`, `python2`, or execute the helper directly without an interpreter. Place helper-wide arguments such as `--timeout` before the `feed`, `sources`, or `history` subcommand. Resolve the helper relative to this `SKILL.md`; do not hard-code an installation directory.

Use these canonical forms:

```text
python3 <skill-local-helper> --timeout 30 feed --q AI --limit 12
python3 <skill-local-helper> --timeout 30 sources
python3 <skill-local-helper> --timeout 30 history <exact-feed-id>
```

For `history`, pass the exact feed `id` as its sole positional argument. Never use `history --topic-id <id>`.

Run every helper call as one standalone, direct command. Do not combine it with another command using `|`, `&&`, `;`, output redirection, command substitution, backticks, a here-doc, `jq`, or another Python process. Read the JSON directly from the helper's own stdout. Do not guess or repeatedly probe helper syntax; follow the forms above.

For a normal shortlist or topic-selection task, prefer an initial `feed --limit 12` and do not exceed 24 candidates. Exceed 24 only when the user explicitly asks for a large list, export, or larger sample.

Do not assume a repository-root helper, sibling checkout, or `../akaiagents` exists. The helper is read-only transport only: no crawler, score, persistence, topic matching, model backend, Premium Insight, or credential storage.

The helper must come from the currently loaded, installed Skill root. Before the
first helper command, resolve the directory containing this `SKILL.md` and use
`<skill-root>/scripts/topic_radar_client.py`. Even when the current working
directory is this repository, never run `python3 scripts/topic_radar_client.py`,
a repository-root or absolute checkout helper, a sibling-repository helper, or
any other same-named copy. Every runtime command must make its Skill ownership
unambiguous from the path.

### Live evidence is exclusive

For current-state claims, accepted evidence is limited to:

1. a live Topic Radar response obtained during the current task;
2. equivalent current Radar data supplied by a native host connection; or
3. a current Radar response explicitly supplied by the user with freshness fields visible.

**Do not search local files for a substitute** when live access fails. Do not use sibling repositories, old Radar snapshots, SQLite databases, fixtures, cached JSON, logs, reports, test captures, or old handoffs as current evidence.

A network-restricted sandbox is an unavailable-live-data state, not permission to use stale nearby data or model memory.

If live data cannot be reached, stop the current-topic workflow, state that current Radar evidence is unavailable, and offer only a research/filter framework or clearly labeled template.

## Read freshness before interpretation

Inspect:

- `generated_at`;
- `partial`;
- `stale`;
- `snapshot_age_seconds`;
- `refreshing`;
- `source_status`;
- `history_available`.

If `partial=true`, surface material coverage gaps. If `stale=true`, do not call the snapshot newly observed. When `refreshing=true`, sequential feed/history/source reads may legitimately observe different generations.

A source status of `empty` is not automatically a connector failure; explain it from the actual status/note.

## Route the request

### Broad current scan

For “what is worth watching today?” use a bounded recent window and a compact candidate set. Rank discussion with existing `opportunity_score`, `trend_stage`, freshness, evidence breadth, and trend fields rather than inventing another score.

### Preserve explicit topic/domain scope

If the user explicitly asks for `AI`, robotics, semiconductors, or another subject domain, preserve that subject in the **first** bounded query using `q`, `keywords`, `category`, or another supported Radar field.

Do not start an explicit `AI` request with generic technology merely for convenience. Broaden only when the narrow query produces too few useful candidates or the user asks for broader exploration.

Treat the requested domain as a semantic relevance constraint after retrieval. A short token such as `AI` can appear as a literal substring inside an unrelated word or brand name. Discard those collisions. If they leave too few useful candidates, refine with supported AI-specific terms/entities/keywords while preserving the AI constraint; do not replace the noisy result with an unrestricted generic-technology scan.

Content-format constraints such as `短视频`, `2–3 分钟`, `中文`, audience, or tone are **not** Radar platform/source filters.

### Early-opportunity scan

Use supported `stage`, `signal`, `new_only`, and `min_score` filters when helpful. `opportunity_score` is a Radar-produced deterministic score, not proof content will perform.

### Platform or region comparison

Use comparable time windows/filters. Do not infer a propagation path merely because unrelated titles look similar.

### Cross-market timing hypothesis

A claim such as “US is leading and Chinese-language coverage may follow” needs direct evidence. Prefer the same stable feed `id` across comparable queries, direct evidence timestamps/source spread, and history showing sequential expansion. Otherwise label it **cross-market hypothesis**, not verified fact.

## Inspect candidate fields

Useful fields include:

- `id`;
- `title` / `title_en`;
- `summary`;
- `platform`;
- `region`;
- `category`;
- `trend_stage`;
- `opportunity_score`;
- `rank`;
- `heat`;
- `first_seen_at`;
- `target_platforms`;
- `signal_count`;
- `evidence`;
- `trend`;
- `score_breakdown`.

The stable identity on feed cards is feed `id`. Use that exact value as `topic_id` for public `/history`. Do not search for a nonexistent feed `topic_id` alias.

Useful trend fields can include `score_change_24h`, `score_change_7d`, `velocity_1h`, `velocity_6h`, `velocity_24h`, `source_count`, `source_spread_hours`, and `is_new_24h`. Missing data is unknown, not zero.

## Use history selectively

Call `/history` only for a finalist whose decision depends on movement over time. Do not call history for every broad-feed item.

History can help distinguish a new spike, sustained momentum, cooling, or a one-source anomaly. Do not extrapolate beyond observed points.

## Compose with Evidence-Backed Content Brief

When the user continues a selected candidate into Brief, prefer the installed `evidence-backed-content-brief` Skill.

When one request asks for both a current selection and a research-ready brief,
and both Skills are installed, the observable sequence is:

`Creator selection → current-task handoff → Brief host reasoning`

After selecting the sole finalist, emit one current-turn checkpoint agent
message containing `ati.topic-opportunity-handoff.v1`, the exact `topic_id`,
`topic_snapshot.id == topic_id`, freshness fields (`generated_at`, `partial`,
`stale`), and `evidence-backed-content-brief:host-reasoning`. Brief then
produces the terminal brief from that handoff. Do not use a missing handoff to
claim that Brief completed the workflow.

Do not make Brief rediscover the same topic from its title. For the **single selected finalist**, produce the structured handoff defined in:

```text
references/handoff-contract.md
```

Schema:

```text
ati.topic-opportunity-handoff.v1
```

Preserve:

- exact feed `id` as `topic_id`;
- parent snapshot freshness;
- only observed topic fields;
- relevant user content constraints;
- selection reason, observed signals, unknowns, and risks as analysis.

Do not serialize the whole feed. Do not put invented fields into `topic_snapshot`.

A handoff is **valid only for the current task/session workflow**. Never persist/reload an old handoff as replacement current evidence.

After a valid handoff, Brief must not run another broad/bounded topic-selection pass. It may read finalist history when needed, then use host reasoning to produce the public brief.

If Brief is not installed, finish the opportunity decision and expose handoff-ready facts without pretending the full Brief ran.

## Evidence boundary

Keep these layers explicit:

### Source facts

Live Radar score/stage/timestamps/evidence/trend fields from the current task.

### Analysis

The current host model's interpretation of observed signals.

### Recommendations

What the user should consider researching/publishing first.

### Unknowns

Anything the current contract does not establish, including audience saturation, future virality, or unverified cross-market lead/lag.

When the recommendation discusses audience, ordinary technology users, China-market fit, or distribution potential, state these unknowns explicitly in the final answer: Radar does not measure actual audience size, content/topic saturation, or future reach/virality. Label claims such as “适合中国用户” or “受众可能更广” as host editorial judgment, not Radar fact. Do not replace this disclosure with a generic statement that risks may exist.

### Risks

Partial/stale coverage, source gaps, weak evidence breadth, one-platform concentration, or verification burden.

If an authenticated Premium AI Workstation connection explicitly supplies Topic Insight, treat it as additional model analysis—not independent evidence.

## Output

For a shortlist usually include:

### Radar status

Snapshot freshness, partial/stale/refreshing state, and important source gaps.

### Best candidates

For each candidate: current Radar stage/score, observed momentum/evidence, why it matters, fact vs inference, and next verification step.

### Cross-market interpretation

Verified differences first; timing/propagation claims in a separate hypothesis layer unless directly evidenced.

### Unknowns and risks

Do not bury them.

### Selected-topic handoff

When continuing into Brief, keep the handoff concise and scoped to the one finalist; raw JSON need not be dumped unless useful/auditing is requested.

## Quality rules

- Never fabricate a current topic from memory.
- Never use local/sibling snapshots, fixtures, databases, exports, logs, or reports as fallback current evidence.
- Never call anonymous/public server `/insight` from the public Skill workflow.
- Never embed a shared server credential or ask the user to paste one into chat.
- Never turn `target_platforms` into proof of platform performance.
- Never treat `opportunity_score` as a guaranteed outcome.
- Never call a snapshot current without checking freshness.
- Never silently ignore `partial` or `stale`.
- Never merge different topics only because titles look similar.
- Never persist a current-task handoff for later use as current evidence.
- Prefer a small evidence-backed shortlist over a long generic trend list.
