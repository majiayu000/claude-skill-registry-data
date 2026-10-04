---
name: eos-new-usecase
description: Author a new dogfood use-case scenario — a committed, rotation-ready scenarios/<slug>.md file in the dogfood-agent catalog that both the automated persona loop and the hand-walk skills can run. Two modes — coverage (verify a shipped feature) and discovery (express a real goal the system may not support yet; walking it surfaces feature gaps as #missing findings). Use when the user says "new use case", "author a scenario", "add a dogfood scenario", "write a use case for <feature>", "what would I actually want to do here", "/eos-new-usecase", or right after shipping a feature that deserves automated dogfood coverage. NOT the walk-and-fix loop (use eos-usecase-audit — it delegates authoring here), NOT the report-only hand walk (use eos-ui-walk), NOT app scaffolding (use eos-new-app), NOT org-roleplay scenarios (use eos-orgs-run-scenario), NOT model-benchmark scenarios (use eos-model-bench-scenario-audit).
---

# EmptyOS New Use Case — author one scenario, verify it parses, commit it

This skill produces exactly one artifact: a scenario file at
`apps/extension/dev/dogfood-agent/scenarios/<slug>.md` conforming to the house
contract in `scenario-shape.md` (this skill's sibling file — the single source
of truth; `eos-usecase-audit` Phase 1 delegates to it). A scenario is dual-use
by construction: the automated dogfood-agent persona loop can run it on
rotation, and the audit/walk skills can hand-walk it.

Authoring only — no walking, no fixing, no report. If the user wants the flow
walked and findings fixed, that's `/eos-usecase-audit`.


## Prerequisites

The daemon on `:9000` must be reachable, because the scenario is validated against the
live app list at `GET /api/apps` — the endpoint the Inputs table below names. Probe
**that** route, not `/api/health`: `/api/health` is auth-exempt, so it answers 200 in
exactly the state where `/api/apps` returns `{"error":"unauthorized"}` and the real
dependency is unusable. In `network.mode = "private"` pass the bearer token from
`emptyos.toml`. If the app list is unreachable, say so and stop rather than authoring
a scenario against a guess — and never start or restart the daemon yourself
(`.claude/rules/daemon-handling.md`).

## Two modes — coverage AND discovery

A use case is not only a test of what exists; it is a statement of what the
user **wants to do**. Author in one of two modes (and say which in the final
message):

Record the mode in the scenario's frontmatter (`mode: coverage | discovery`)
— the audit's selection rule reads it, and a catalog whose discovery
scenarios are unfindable degrades back to coverage-only.

- **Coverage** — verify a shipped feature or guard a flow against regression.
  Grounded in what the system does today; `tier: feature` is the usual shape.
- **Discovery** — write the flow the user *genuinely wants*, from real life
  (a real evening, a real work task, a real errand), **without checking first
  whether the system supports every step**. Walking it is how feature gaps
  get found: a goal the walker can't complete becomes a `#missing` finding,
  which the audit routes to the fix queue or the gap registry. A catalog that
  only contains flows the system already passes is blind to gaps by
  construction — that failure is documented in `eos-usecase-audit` Phase 1.

**The cardinal authoring sin is sanding a goal down to what the system can
do.** If the natural version of the goal is "snap a receipt and have the
expense logged" and the system only has manual entry, write the natural
version — the fumble cap + `#missing` tag turn the shortfall into a recorded
gap instead of silent scope-shrink.

## Step 0 — Inputs (cheap reads)

| Input | Where | Tells you |
|---|---|---|
| Existing catalog | `apps/extension/dev/dogfood-agent/scenarios/*.md` (frontmatter: `expected_apps`, `surface`) | what's already covered — reuse check |
| App inventory | `GET http://127.0.0.1:9000/api/apps` (Bearer token from `emptyos.toml [network] auth_token`) | exact app ids for `expected_apps` |
| Walk coverage | `data/apps/dogfood-agent/ui-walks/coverage.json` | which apps have zero/stale credit |
| Recent churn | `git log --oneline --since="14 days ago"` | recently-shipped surfaces (coverage mode) |
| Gap registry | `{vault}/30_Resources/EmptyOS/gap-analysis/*.md` (open rows) | suspected thin areas worth a discovery scenario |
| **The user's real work** | `{vault}/10_Projects/` active project notes, open tasks, current job/engineering tracks | the highest-value discovery goals — what the user is *actually trying to accomplish this month*. A discovery scenario grounded in a live project beats an invented errand |

**The inventory maps `expected_apps`; it never constrains the flow.** In
discovery mode, write the goal first and only then map which apps it
*should* touch — an app id in `expected_apps` for a step the system can't do
yet is fine; that step is the gap being hunted.

**Daemon down → keep going.** Scenario files are static; authoring works
offline. Skip the API reads, take app ids from manifests, and note in the
final message that Step 4's live verify was skipped.

## Step 1 — Mini-grill (only if the brief is ambiguous)

If the user's brief already answers these, don't ask. Otherwise
AskUserQuestion for the gaps:

1. **The goal** — what does the user want to accomplish, as a real-life
   narrative? Start from the need, not from an app or feature. (One flow per
   scenario; a second flow is a second file.)
2. **Mode** — coverage (guard something shipped) or discovery (hunt gaps in
   how well the system serves this goal)?
3. **Surface** — `web` | `cli` | `bridge`?
4. **`expected_apps`** — which app ids *should* the flow touch? (Verify ids
   against the inventory — coverage credit and rotation deficit key off
   these.)
5. **Runtime** — can the automated persona loop run every step (`persona`),
   or does any step need human hands (`manual`)? Prefer restructuring toward
   `persona`/HTTP-checkable over `manual` (see scenario-shape.md § Rotation
   guard).
6. **Checks** — any deterministic acceptance probes worth pinning
   (`checks:` list)? (Coverage mode mostly; discovery goals often can't be
   pinned yet — that's expected.)
7. **Budget** — turn cap (default 15).

## Step 2 — Reuse before authoring

Grep the catalog's frontmatter for overlapping `expected_apps` + goals. If an
existing scenario already covers the flow, **extend it** (add goals / checks /
steps) instead of creating a near-duplicate — the rotation picker spreads
credit by scenario, and two files for one flow dilutes it. Only write a new
file when nothing covers the flow. Overlap is judged by **goal, not app id**:
an existing scenario touching the same apps for a different goal is not
coverage — a discovery scenario for a new goal is still worth its own file.

## Step 3 — Write `scenarios/<slug>.md`

Follow `scenario-shape.md` exactly: frontmatter schema, `{{DAEMON_URL}}` +
guardrails, hard turn cap restated in prose, 3-turn fumble cap,
`#bug`/`#missing`/`#confusing` tag vocabulary, `## Wrap`, no-source-dive rule,
log-file convention. Copy the nearest template (`tuesday-evening.md` web,
`cli-daily-driver.md` cli, `telegram-inbound.md` bridge) rather than writing
from a blank page. Slug = short-kebab-case of the flow, matching the existing
catalog's style.

## Step 4 — Verify it parses

`_scenarios()` re-globs disk per call, so no restart is needed:

```bash
curl -s -H "Authorization: Bearer <token>" \
  http://127.0.0.1:9000/dogfood-agent/api/scenarios
```

Confirm the new id appears with correctly-parsed `expected_apps`, `goals`,
`surface`, and `runtime` (a YAML slip fails soft to `{}` — empty
`expected_apps`/`goals` on your new entry means broken frontmatter, not a
clean pass). Daemon down → hand-check the frontmatter against
scenario-shape.md and say the live verify was skipped.

## Step 5 — Rotation guard + commit

- If `runtime: manual`: state explicitly that it must NOT be added to the
  scheduled rotation config (`[apps.dogfood-agent]` scenario rotation).
- Commit the scenario file by explicit pathspec (never `git add -A` —
  `.claude/rules/environment.md` § parallel-session staging). Scenario files
  ARE committed; nothing under `data/` is.

Final message: the file path, the parsed-meta verify result, the rotation
note, and (if relevant) a pointer that `/eos-usecase-audit` will pick it up
on its next run via the catalog.

## Cross-references

- `scenario-shape.md` (sibling file) — the house contract this skill authors to.
- `eos-usecase-audit` — the walk→fix→converge orchestrator; its Phase 1
  selection rule picks from the catalog this skill grows, and it invokes this
  skill for any new scenario.
- `eos-ui-walk` — hand-walk mechanics; the catalog is one of its use-case sources.
- `apps/extension/dev/dogfood-agent/app.py` — `_scenario_meta` / `_scenarios`
  (the fail-soft parser + per-call disk re-glob).
- `apps/extension/dev/dogfood-agent/scheduled.py` — the rotation deficit picker
  that runs `persona` scenarios automatically.
