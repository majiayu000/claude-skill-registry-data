---
name: evidence-backed-content-brief
description: Turn a live AI Workstation Global Topic Radar topic into an evidence-aware, research-ready content brief using public Radar feed/source/history evidence and the host model's own reasoning. Use when the user wants to evaluate or select a current topic and plan its angle, audience, format, hook, verification, or research handoff. Do not use when the user already supplied complete material and only wants rewriting, scripting, summarization, translation, or generic title generation without a live-topic decision.
---

# Evidence-Backed Content Brief

Use this Skill when the user wants to turn a **current Radar topic** into a practical content plan.

The distributable public Skill must not spend AI Workstation server-side model quota. Its normal workflow uses live Radar facts plus the **current host model's own reasoning**.

## Host quality and cost contract

Before mapping user constraints to Radar filters, selecting a standalone topic, consuming an Opportunity handoff, or generating a brief, read and follow:

```text
references/quality-contract.md
```

Important consequences:

- content format/duration/language/audience/tone are post-query content constraints, not Radar platform/source filters unless the user names a supported Radar dimension;
- preserve an explicit subject/domain such as AI in the first bounded query;
- a valid current-task handoff must not trigger another broad selection pass;
- Radar facts and host editorial analysis must remain distinguishable;
- **the bundled/public Skill must not call server-side `/insight` or any other AI Workstation LLM-backed endpoint**.

## Public no-cost live contract

The bundled helper exposes only:

- `GET /api/v1/ai/topic-radar/feed`;
- `GET /api/v1/ai/topic-radar/sources` when source health matters;
- `GET /api/v1/ai/topic-radar/history?topic_id=...` when movement matters.

These endpoints provide current Radar evidence without asking AI Workstation to run a model for the Skill user.

Use the official `https://aiworkstation.cn` origin in the normal public Skill workflow. Use a custom `--base-url` or `AIWORKSTATION_TOPIC_RADAR_BASE_URL` only when the user explicitly asks to test a self-hosted/development Radar origin; identify that origin as non-official evidence in the result.

### Optional future Premium transport

A host may use a server-generated AI Workstation Topic Insight **only when all of the following are true**:

1. the host provides a native AI Workstation connection that is explicitly authenticated to the user's AI Workstation account;
2. the connection itself enforces the user's membership/quota/credits;
3. the user or host intentionally chooses that Premium capability;
4. the response is clearly treated as model-generated analysis, not independent evidence.

The bundled `scripts/topic_radar_client.py` does **not** contain Premium Insight support, credentials, shared API keys, or secret-management logic.

Never ask the user to paste a private AI Workstation API key into chat just to run this public Skill. Never embed a shared server key in the Skill package.

## Self-contained runtime

Resolve the bundled public helper relative to this `SKILL.md`:

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

Do not assume a repository-root helper, sibling checkout, or `../akaiagents` exists. A native host connection may call the same public no-cost contract directly.

The helper is transport-only: no crawler, score, persistence, topic matching, model backend, or Premium Insight is implemented inside the Skill.

The helper must come from the currently loaded, installed Skill root. Before the
first helper command, resolve the directory containing this `SKILL.md` and use
`<skill-root>/scripts/topic_radar_client.py`. Even when the current working
directory is this repository, never run `python3 scripts/topic_radar_client.py`,
a repository-root or absolute checkout helper, a sibling-repository helper, or
any other same-named copy. Every runtime command must make its Skill ownership
unambiguous from the path.

## Live topic evidence is mandatory

A brief about a **current** Radar topic must be anchored to one of:

1. a topic resolved from live Topic Radar data during the current task;
2. a valid current-task Topic Opportunity handoff; or
3. an equivalent current Topic Radar response explicitly supplied by the user/native host connection.

Do not search sibling repositories or local storage for a substitute when the live contract is unavailable. Never use old Radar snapshots, SQLite databases, fixtures, cached JSON exports, test captures, generated reports, logs, or persisted handoffs to establish that a topic is current.

If live feed evidence cannot be reached:

1. do not produce a current-topic verdict as if verified;
2. do not recover a topic from local files or model memory;
3. explain that live Radar evidence is unavailable in this execution environment;
4. offer a clearly labeled template/research plan instead.

## Choose the input mode

Use exactly one entry mode before generating the brief.

### Mode A — current-task Topic Opportunity handoff

If `creator-topic-opportunity-research` already selected the topic in the current task, accept the handoff defined by:

```text
references/handoff-contract.md
```

Expected schema:

```text
ati.topic-opportunity-handoff.v1
```

Accept it only when:

- the handoff was produced in this current task/session workflow;
- `topic_id` is non-empty and exactly equals `topic_snapshot.id`;
- `snapshot.generated_at`, `partial`, `stale`, and other material freshness fields are visible;
- `stale` is not true;
- `partial=true` does not remove evidence required for the requested claim;
- it is not a loaded cache, saved file, old log, prior-task artifact, or model-memory reconstruction.

When valid, **do not re-identify the topic from its title and do not run another candidate-selection feed pass**. Continue with the exact handed-off `topic_id`; call `/history` only when movement matters; then build the brief with the host model.

When a request combines Creator selection and Brief generation with both Skills
installed, consume the Creator checkpoint before reasoning. The checkpoint must
contain `ati.topic-opportunity-handoff.v1`, the exact `topic_id`,
`topic_snapshot.id == topic_id`, freshness fields, and
`evidence-backed-content-brief:host-reasoning`. Then emit the terminal research
brief. Do not repeat `feed` or another selection query merely to make Brief
runtime visible; the Creator's finalist evidence and history may be reused.

Refresh/re-resolve live evidence only when the handoff is stale, materially partial, identity-invalid, from another task, or the user explicitly asks for a fresh re-check.

### Mode B — user supplies a current topic ID or name

If the user supplies a topic ID, verify that it still exists in live Radar data unless the user also supplied the current Radar response containing that ID.

If the user supplies only a topic name:

1. query `/feed` with `q`;
2. choose the closest server-known topic only when identity is reasonably clear;
3. if materially different clusters match and the choice changes the brief, ask or explain which cluster you selected.

Feed topic cards expose the stable identifier as `id`. Preserve that exact value through history and the final brief.

### Mode C — Brief-only bounded selection

When the user asks this Skill to pick the best current topic and Creator Opportunity Research is unavailable:

1. run one bounded live `/feed` query;
2. preserve any explicit subject/domain constraint from the user in that first query;
3. reject literal substring collisions or other candidates that do not semantically match that domain; refine with supported domain terms when necessary instead of broadening to generic technology;
4. use a recent `max_age_hours` and normally no more than 5 candidates;
5. select at most one candidate using Radar-provided `opportunity_score`, `trend_stage`, freshness, evidence breadth, and user constraints;
6. never invent another ranking score;
7. do not query history for every candidate;
8. if no candidate is useful or evidence is too weak, say so instead of forcing a choice.

Do not map `短视频`, `2–3 分钟`, `中文`, audience, tone, or production style into Radar `platform`/`source` filters.

## Check freshness and evidence

Before producing the brief, inspect the parent live feed/handoff context:

- `generated_at`;
- `partial`;
- `stale`;
- `snapshot_age_seconds`;
- `refreshing`;
- topic `evidence`;
- topic `trend`;
- `source_status` when relevant.

If stale/partial is material, carry that caveat into the brief and refresh live evidence before making unsupported current-state claims.

Use `/history` only for a finalist when “why now” depends on acceleration, persistence, cooling, or recent rank/score movement. Do not call it for every candidate.

When `refreshing=true`, sequential requests may see a newer history point. Compare timestamps and identity rather than treating normal refresh movement as a contradiction.

## Build the brief with host reasoning

The current ChatGPT/Codex/agent model should transform the live Radar facts into an editorial plan. This is **host editorial analysis**, not server evidence.

Generate/adapt as needed:

- recommendation: make / conditional / watch;
- target audience and audience payoff;
- why now;
- one selected angle;
- hook and opening 3 seconds;
- viewer question, core conflict, promise;
- narrative beats for the requested duration;
- visual/material plan;
- research questions and search queries;
- preferred source types;
- `must_verify`;
- `avoid_claims`;
- known unknowns and risks.

Do not claim these editorial fields were measured by Radar. Statements such as “受众更大”, “更适合中国用户”, “更容易传播”, or “最值得做” are analysis/judgment unless directly supported by a current Radar field.

When the brief discusses audience, ordinary technology users, China-market fit, or distribution potential, state these unknowns explicitly in the final answer: Radar does not measure actual audience size, content/topic saturation, or future reach/virality. Label claims such as “适合中国用户” or “受众可能更广” as host editorial judgment, not Radar fact. Do not replace this disclosure with a generic statement that risks may exist.

If an explicitly authenticated Premium AI Workstation connection supplies Topic Insight, treat its creative fields as optional server model analysis: preserve its provenance, adapt it to the user's constraints, and do not present it as independently verified fact.

## Research-ready output

A strong final brief should contain:

### Topic / Radar facts

- title / stable topic ID;
- current stage and opportunity score;
- snapshot freshness;
- evidence breadth and source limitations;
- history movement when relevant.

### Editorial analysis

- recommendation;
- target audience and audience payoff;
- why the topic may work for the requested content goal;
- selected angle and why it was chosen.

### Opening and narrative

- hook / first 3 seconds;
- 2–3 minute or user-requested narrative beats;
- platform/format adaptation without pretending those are Radar filters.

### Research handoff

- research questions;
- search queries;
- preferred source types;
- `must_verify`;
- known unknowns.

### Claims boundary

Show `avoid_claims` explicitly. Do not bury them in a generic disclaimer.

### Visual plan

Distinguish must-have factual visuals from optional illustrative B-roll.

## Quality rules

- Never fabricate a current topic from model memory.
- Never use local/sibling snapshots, fixtures, databases, exports, logs, or old handoffs as current evidence.
- **Never call anonymous/public server `/insight` from this Skill.**
- Never embed or share a server credential in the Skill package.
- Never ask the user to paste a private credential into chat as a workaround.
- Never invent a fallback ranking score.
- Never force a candidate when evidence is too weak.
- Never reselect after a valid current-task handoff.
- Never confuse host editorial analysis with Radar facts.
- Never claim a video will perform because the Radar score/stage is high.
- Preserve `must_verify`, `avoid_claims`, unknowns, and evidence limitations.
- Prefer one executable, evidence-bounded brief over a generic brainstorm.
