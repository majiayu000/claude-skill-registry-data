---
name: auto-driver
description: >
  Orient before /auto starts. Loads the hypothesis JSON from
  lib/auto-detect.sh, surfaces one action line, dispatches when
  ambiguity is null, or asks one blocking question when it isn't.
  No verdict-tree enumeration, no workflow-picker prose. Hands off to
  lib/auto.sh (single plan) or lib/auto-spawn.py (multi-plan batch).
  Distinct from the `auto` skill (the loop driver): auto-driver runs
  BEFORE the run starts; `auto` takes over AFTER it's armed.
---

# auto-driver

One action line per branch. Dispatch. Do not narrate.

## Load the hypothesis

```
bash "${CLAUDE_PLUGIN_ROOT}/lib/auto-detect.sh"
```

If the detector yields no parseable envelope (empty/non-zero env hiccup), don't stall — treat as `raw`.

Returns one JSON object (`situation`, `summary`, `ambiguity`, `single_plan`, `multi_plan`, `in_flight`, `workspace`, `workspace_action`, `recommendation`, `plans`, `git`). The detector emits deterministic **facts** — it has no transcript access. **You** have the transcript: surface `summary`, then decide the route from `situation` + `ambiguity` + the `plans`/`git` facts. The conversation-vs-stale-plan call is YOURS, not the detector's (U4 — see below).

| situation         | ambiguity null → dispatch                                                    | ambiguity non-null → AskUserQuestion |
|-------------------|------------------------------------------------------------------------------|--------------------------------------|
| `in-flight`       | (FRESH run) `bash "${CLAUDE_PLUGIN_ROOT}/lib/auto-resume.sh" "continue <run-id>"` | (STALE run) options = resume vs start-fresh; on the resume option (carries `run_id`) → `auto-resume.sh "continue <run-id>"`; on "Start fresh" (`run_id` null) → treat as `raw` (ask what to work on) |
| `ambiguous-runs`  | (n/a — always ambiguous)                                                     | options = the in-flight run-ids; on answer, resume the chosen run |
| `reviewed-plan`   | if `single_plan.freshness` is `stale` and this session is about other live work, prefer conversation-context (below). Else run the **goal-aware pre-step**; if it does not reshape, load `auto-launch` (the launch chooser) via Skill: it gates on `driving_session_id` — self-driven silent-applies, interactive confirms — then dispatches `lib/auto.sh "<path> --workflow w"` | (n/a — single plan unambiguous)      |
| `multi-plan`      | If every `plans[].freshness` is `stale` and this session is about other live work, use conversation-context (below) and do NOT offer the stale plan actions; otherwise run the **goal-aware pre-step** first | options = the FRESH plans (`path` → `auto.sh "<path>"`); a "Fan out all N" option (`path` null → `auto-spawn.py fanout`) appears ONLY when the set is fresh. An all-stale set offers no plan actions — it routes to conversation-context |
| `raw`             | (n/a — always ambiguous)                                                     | open "what should we work on?"; on answer, route as freeform text (or conversation-context, below). Summary may include dirty-tree context (the `git` fact). |

**Conversation-context is driver-owned (U4).** The detector no longer emits a `conversation-context` situation — it can't sense the transcript. When the facts show no in-flight run and no LIVE plan to act on (`situation` = `raw`, or a `reviewed-plan`/`multi-plan` whose plans are all `freshness: stale`) AND this session is clearly about live work, DON'T act on the stale/absent plan: classify state → recommend (`lib/recommender.py`) → author goal → dispatch the entry workflow (pre-dispatch escalate if unsure). A FRESH plan (`freshness: fresh`) always wins over conversation.

## Goal-aware plan routing (pre-step)

For `reviewed-plan` / `multi-plan`, **interactive runs only** (`driving_session_id`
null — self-driven/headless runs skip this whole step, take the row above
unchanged). Recover THIS invocation's goal: the typed `/auto` intent or a session
`/goal`'s text (read only — never query/run/bind/clear it);
else infer from the session (advisory). Weight the plans (the fuzzy judgment is
yours → ordered matched paths), hand verdicts to the crisp router, run its `reason`
(map + guardrails: `driver-reference.md` §17; rubric `goal-plan-relevance-rubric.md`):

```
python "${CLAUDE_PLUGIN_ROOT}/lib/goal-route.py" \
  '{"authority":"<explicit|inferred|none>","matches":[<ordered matched paths>],
    "all_plans":[<multi_plan.paths>],"interactive":<driving_session_id is null>}'
```

Reason markers (§17): `explicit-suppress`, `inferred-re-rank`, `no-match-unchanged`, `no-goal-unchanged`.

**Argument-aware freeform**: a plan path → `auto-launch` → `auto.sh "<path> --workflow
w"`; else classify with `lib/verb-classify.py` → the `auto-launch` chooser —
freshest plan / `clear-intent-no-plan`→`a1`@plan / `/ce-plan`.

**Workspace / conversation-context / unknown** (§17): branch `workspace_action`; unknown → `raw`.

## Dispatch grammar (reference)

- Single plan: `bash lib/auto.sh "<plan-path> [auto] [--review-plan]
  [--backend ce|native] [--goal <text>] [--workflow <name>]"`
- Batch fanout: `python lib/auto-spawn.py fanout <plan> [<plan>...]
  [--intent "<text>"]` — the spawner owns worktrees/ports/sidecar +
  dispatch; the driver never shells out per sub-run.
- Resume: `bash lib/auto-resume.sh "<continue|abort|retry|skip>
  [<run-id>] [<step>]"`

Theory + edge cases (`docs/contracts/driver-reference.md`): prepare/execute, goal
binding, pulse/handoff/fan-out, exit reasons, goal-aware routing (§17) — load on demand.