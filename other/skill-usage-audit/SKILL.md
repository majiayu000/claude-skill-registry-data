---
name: skill-usage-audit
user-invocable: true
description: Use when measuring whether a skill-concierge gate-threshold change helped real skill usage or adoption — "did the new gate values help", "skill usage impact after the change", "assess skill helpfulness", "audit skill usage post-deploy", "which telemetry is valid for skill-usage analysis". Stops the reflex of using the skill-invocation-ledger or treating offer→take as usage; routes to the transcript SKILL-FIRST trail instead.
argument-hint: "[--since <when>] [--until <when>]"
license: MIT
metadata:
  version: 0.2.1
---

# Skill Usage Audit

## Overview

Whether agents use the **right** skill is NOT the enforcer's offer→take. The invocation-ledger
measures **gate compliance** and is **INVALID for usage analysis** (operator-flagged). The real
signal lives in the **transcript store** — and most of it is the **SKILL-FIRST declaration trail**,
which no invocation counter records.

**Violating the letter here is violating the spirit:** "I'll just use the ledger, it has
invocations" is the exact failure this skill exists to stop.

## Pick the right source

| Source | Path | Measures | Use for |
|---|---|---|---|
| invocation-ledger | `~/.claude/skill-concierge/logs/skill-invocation-ledger.log` | gate compliance (offer→take; `auto`/`manual`/`search`) | gate firing only — **NOT usage** |
| skill-usage-tracker | transcripts → `~/.claude/audits/skill-usage-stats/` | usage frequency (Skill tool + `/slash`) | how often each skill actually ran |
| **SKILL-FIRST trail** | assistant text in `~/.claude/projects/**/*.jsonl` | agent KNEW + chose a skill (`USING`/`SEARCH`/`NO SKILL` declarations; `SKIPPING` before `0.52.0` — both read) | **the operator's metric** |

Inline SKILL-FIRST use (declare `USING: <skill>` → read its `SKILL.md` → execute) fires **no Skill
tool**, so the ledger AND the usage-tracker both miss it. The declaration trail is the proxy that
catches it; subagent/`Task` skill use is missed by all three.

## Run it

```bash
python3 scripts/audit_skill_usage.py --since "<ship/commit time, e.g. 2026-06-29 01:06:35>"
```

Outputs the scoped post-change counts (Skill-tool, `/slash`, and the `USING`/`SEARCH`/skip-ruling
trail, skips split into `NO SKILL:` and the old `SKIPPING`), self/meta sessions flagged, plus a **false-SKIPPING** rate — per turn, a skip ruling (`NO SKILL:`, or the older `SKIPPING`)
declared with NO same-turn `search_skills` call (the doctrine's hardest rule). A turn carrying the
enforcer's `SKILL-CHECK:` marker (`AUTHORIZED_SKIP_MARKER`, injected on the enforcer's five
authorized-skip legs — getaway, intent_skip, selfref, the harness-message lane (ADR-0054) and the
router's no-fit leg (ADR-0061) — see `hooks/scripts/enforcer.py`) is a **lawful, hook-pre-authorized
skip**: it is excluded from the false-skip count and tallied separately as `authorized_skip`, reported
alongside the false-skip figure so "false-SKIPPING" stays honestly defined. Since `0.52.0` the marker counts only from the enforcer's own output (`_enforcer_output`: a
UserPromptSubmit `hook_additional_context` attachment whose text starts with `SKILL-FIRST`,
`SKILL-CHECK:` or `CONSULT-ROUTE`) — never from the agent's own text, a tool result, a file echo, a
memory or instructions attachment, another hook or the session-start standing order, so a copied line
cannot authorize a skip (ADR-0062). The report adds an **enforcer-run turns only** line — the
same verdict over turns where the enforcer's offer, consult route or `SKILL-CHECK:` line reached the agent
before it ruled (Stop-hook feedback, subagent prompts, and short or slash prompts get no offer, though the
doctrine still binds the last two). Since `0.52.1` a line that arrives after the ruling — a queued
notification — neither authorizes the skip nor marks the turn enforcer-run (ADR-0063). Since `0.52.2`
the same holds for the search: a skip is search-backed only by a skill-search `search_skills` call made
before the ruling (rule 4).

The report also counts **continuations** (rule 3; ADR-0064, ADR-0065; epoch-watch W28): every
`USING: <name> (continuing …)` — `(continued …)`, `(continuation …)` and several names included — per
turn: whether the turn loads the skill (the Skill tool or skill-search's `get_skill`, before or after the
line), whether the session used it before this turn (a load, a `USING:` line or the user's slash command,
before the `--since` window too), and how many **work turns** ago it was last used (more than 5 is
flagged as likelier new work). A work turn is a prompt that hands the agent work: typed text, a relayed
chat message, pasted content, a slash command with arguments, or a typed prompt stored as a list of text
and image blocks. Stop-hook feedback, notifications, scheduled tasks, cross-session messages,
local-command output, session builtins (`/compact`, `/plugin`, `/model` …) and compaction summaries do
not count (since `0.52.4`, by prompt shape since `0.52.5`). Since `0.52.6` the harness's own record
fields decide first: an `origin.kind` other than `human`, a `system` prompt, or a `promptSource: sdk`
prompt from a program entrypoint (`sdk-…`) is not work — including the few a person typed through an
SDK app, a recorded trade-off (ADR-0071) — and neither is a team runner's inbox relay or scaffolding
(`## New Messages`, `## Team Governance`, `## Turn Context`, `Team: "…"`) or a bot scheduler's message
(`Meanwhile, Heartbeat check` and three siblings). A "turn" for the verdicts is every string-content user
record plus a list-form prompt that hands over work: a notification's or a message's content is a task
under the standing order (rule 4), so its turn is scored. A list-form harness record, and a program's
prompt in either form (a `system` or program-SDK prompt whose text would be work from a person), open a
turn whose skip rulings are never scored (since `0.52.8`; string-form programs since ADR-0073); a
continuation in such a turn still counts. The report adds the verdicts on turns a work prompt opened, as
its own line: the headline is mostly harness-message turns. A record line the store
wrote twice is read once, and a skip ruling a resumed session copied into its file counts once (the
session's own file wins; ADR-0073). Files are read in sorted order; a resumed session usually rewrites the copied
records' session id, so that order decides which copy of a continuation counts (when a copy keeps the
original id, the session's own file wins). A note that negates the continuation word itself ("(not
continuing x)", "(not actually continuing)", "(instead of continuing x)") or names a new task is a fresh
ruling; a justification elsewhere in the note ("same task, no new search — continuing", "(no need for a
new task)", "(won't stop continuing)") still reads; the bare `USING <name> (continuing)` reads in
capitals. A later name after a comma or `+` reads only as one word ("then study"), a skill this session
already used, or a hyphenated installed skill ("+ ak-git for the commit"): "then run the tests" is prose
even where a skill is named `run`. The installed-skill catalogue skips test fixtures and marketplace
copies (ADR-0073). Name forms of one skill
match loosely (`plugin:name` and `name`, or one name ending in `-<the other>`), which can join two
different skills whose names nest (`ssh-doctor`, `tk-servers-ssh-doctor`); a slash command counts as
earlier use only from the user's own prompt, not from a tool result that quotes one. The listing shows
local time, sorted, with self/meta sessions marked. Counts are shown for all sessions and for organic ones (self/meta excluded);
`--continuations` lists each one (session id prefix, time, skill) for hand review. A queued user prompt
splits a turn, so a re-read after it is missed. The `SEARCH` declaration count is display-only and
includes bare title-case prose lines ("Search …"); the raw-line pre-filter is case-sensitive, so a
lower- or title-case ruling that carries none of its tokens is not read. The verdicts come from tool
calls. Since `0.49.0`
([ADR-0059](../../docs/adr/0059-harness-complete-offer-isolation-echo-everywhere.md) §5), a `USING:`
retracted by a same-reply re-rule (the doctrine's `USING:`/`SEARCH:` line ending
`(re-rule: <old>)`, fired after `skill_exclusions.py` echoes a loaded skill's own "not for" lines
back) is moved out of the uptake counts into a separate `re-rules` tally, so a switched-away-from
skill no longer inflates uptake. Run `--help` for flags; `--selftest` pins the false-SKIPPING
verdict logic, including the authorized-skip case.

## Scope to reduce noise (post-change)

- **Window** to events at/after the ship/commit time (not calendar "since I deployed").
- **Drop fallback-band** offers (embed/Qdrant down — the gate never ran; not its decision).
- **Drop self/meta sessions** — work *on* the audited project itself (dogfooding/verification) is
  the agent testing the gate, not organic usage.
- **Canonicalize names** before any offered-vs-invoked join (`ck:journal` ≡ `journal`); raw
  set-intersection silently undercounts namespaced-vs-bare.
- **Gate the verdict on VOLUME, not calendar time** — need ~50–100+ organic offered turns before a
  few-point change clears noise.

## Right metric, not the trap

- Report **absolute coverage** (right skill surfaced-and-used ÷ applicable turns), NOT conditional
  offer→take: raising a floor fires fewer offers and **mechanically inflates** conditional
  conversion even if real routing drops.
- **Suppression cost is unobservable post-change** (a suppressed offer is never shown → never
  taken). Estimate it ONLY via a **backtest over history**: which taken offers would the new floor
  have blocked? (On the live ledger: taken offers score LOWER than dodged — cosine is
  anti-correlated with adoption.)

## Tuning thresholds (optimal values)

- Sweep candidate floors through the **real enforcer fns** (`_embed`/`_retrieve`/`_is_imperative`/
  `_intent_conversational`) over a labeled corpus — never reimplement the gate.
- **Held-out only:** `prompt_intent` is built from the same corpus, so `_intent_conversational`
  classifies in-sample (~73% noise-catch vs ~53% held-out). Build a temp collection on a train
  split (`SKILL_PROMPT_INTENT_COLLECTION=...heldout`), evaluate on the test split, delete it.
- Frame as **volume vs adoption**: a higher floor suppresses more (volume) but cuts the
  better-converting low-cosine offers (adoption). Re-confirm on the live ledger before recommending.
- Worked example: `skill-concierge/plans/reports/impact-analysis-260629-1020-*.md`.

> **v0.10.0 caveat (multi-vector, ADR-0012).** The "cosine anti-correlated with adoption /
> taken offers score LOWER than dodged" findings above were measured on the SINGLE-vector index.
> Multi-vector MAX-pool roughly doubled positive↔negative separation, so the cosine↔adoption
> relationship must be **re-measured on post-v0.10.0 traffic** before reuse — do not carry the old
> anti-correlation forward as fact. The methodology (held-out sweeps, absolute coverage, drop
> self/meta, gate on volume) is unchanged.

## Common mistakes (from baseline failures)

| Rationalization | Reality |
|---|---|
| "The ledger records invocations, so it's the source." | Ledger = gate compliance; operator flagged it INVALID for usage. Use transcripts. |
| "offer→take = how often the right skill is used." | Conditional on the gate firing; misses inline SKILL-FIRST use entirely. |
| "Post-change window is enough to judge." | Usually thin + dogfood-contaminated. Gate on organic volume; drop self/meta. |
| "Sweep the corpus through the intent gate as-is." | The intent corpus self-scores in-sample. Held-out split only. |
| "Compare pre vs post conversion." | Denominator shifts (the floor changes who is offered). Use within-population replay / absolute coverage. |
| "Offered `ck:journal` ≠ invoked `journal` → not used." | Canonicalize names before joining. |

## Red flags — STOP

- Reaching for `skill-invocation-ledger.log` to answer a **usage** question.
- Leading with offer→take / "accept rate".
- Reporting a post-change number without dropping self/meta sessions or checking volume.
- Sweeping the live `prompt_intent` collection in-sample.
