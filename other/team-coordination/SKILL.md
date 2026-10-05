---
name: team-coordination
description: "Coordinate agent teams for adversarial review (paired skeptic/verifier per facet, disposition-only challenge round, mechanical consolidation with confidence) or parallel implementation (5-6 non-overlapping tasks per teammate). Enforces independent analysis before shared conclusions. Reference only (`disable-model-invocation: true`); loaded only when `agentTeams: true` in settings."
allowed-tools: Bash, Read, TaskCreate, TaskList, TaskUpdate
agent: general-purpose
disable-model-invocation: true
---

# Team Coordination

## Contract

Independent analysis before shared conclusions: teammates who see each other's findings are contaminated reviewers. Applies only when `agentTeams: true` and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set; `commands/review.md` Path A applies it, using the tables in `references/paired-review-protocol.md` verbatim. Returns consolidated P1/P2/P3 findings, each carrying a confidence and a disposition from the controlled set `consensus|validated|refined|kept|unchallenged`. The only permitted skip is the documented per-facet fallback to single-reviewer Path B; a paired-protocol failure never blocks a review.

## When to Spawn Teams

| Scenario | Decision |
|----------|----------|
| Review with 3+ facets | Spawn: independent analysis enables the adversarial protocol |
| Large feature (>5 acceptance criteria, independent modules) | Suggest: parallel implementation across modules |
| Debugging with competing hypotheses | Spawn: one hypothesis per teammate |
| Small feature (<3 criteria) or sequential dependencies | Single session |

## Task Sizing

5-6 tasks per teammate, each completable without coordination and carrying its own acceptance criteria. Overlapping file sets go to the same teammate.

## Adversarial Review Protocol

Each facet runs as a **paired reviewer**: a skeptic ("assume the diff is broken until proven otherwise") and a verifier ("assume correct; look for missed edge cases and unenforced invariants"), dispatched in parallel with no view of each other. The default 6-facet topology is 12 invocations: 5 `Agent(...)` pairs plus 2 `Skill(holdout-validation)` lens calls.

1. **Independent analysis.** Both variants return P1/P2/P3 findings with `file:line` citations. No challenge information in this phase.
2. **Share.** The lead indexes findings by facet. No LLM call. Holdout findings are indexed for consensus matching only.
3. **Challenge (disposition-only).** Each variant labels the other's findings `AGREE`, `DISAGREE: <reason>`, or `REFINE: priority= category=` WITHOUT re-reading the diff. Holdout-validation is excluded by design: it is objective claim-verification, so `DISAGREE` has no meaning there.
4. **Synthesize.** The lead applies the consolidation table mechanically: both raised independently (same facet, file, lines ±2, priority ±1) → HIGH `consensus`; AGREE → HIGH `validated`; REFINE → MEDIUM `refined`; DISAGREE → LOW `kept`; timeout/error → MEDIUM `unchallenged`; both DISAGREE → dropped and journaled under `## Dropped after challenge`. The lead never adjudicates.
5. **Emit.** Finding tables carry a trailing `_(confidence · disposition)_` suffix; the `FLOW_REVIEW_CYCLE` marker carries the 7-field rows per `references/finding-ledger-parser.md`.

Cost: about 23 LLM calls per review (12 + 10 challenge + 1 consolidation), roughly 3.8× the single-session baseline; opt-in.

Bias rules: no reading of another reviewer's findings before producing your own (anchoring); HIGH-confidence-on-everything is a smell (groupthink); no third-agent judge (central-judge bias).

## Fallback Semantics

Per facet, never blocking the review: `agentTeams: false` → Path B; env var unset → stderr WARN and Path B; one variant fails to spawn or times out (`timeouts.teammateTimeout`, default 300s) → use the responding variant, mark its findings `unchallenged`; both fail → re-dispatch that facet on Path B; challenge round fails → include findings as `unchallenged`. The full matrix is in `references/paired-review-protocol.md`.

## Teammate Health

Timeout: collect partial results and mark the facet "incomplete review", else "not reviewed". Crash: log, fall back to single-session for that facet, note it in the summary. Idle: `nudge-idle-teammate.sh` sends "check task list for unclaimed tasks" after 60s (stderr, exit 0).

## Implementation Team Protocol

The lead creates the dependency-ordered task list, assigns non-overlapping file groups, monitors via TaskList, and runs final verification after all teammates complete. Teammates claim, implement, commit, and mark tasks complete.

## Single-Session Fallback

When teams are disabled or spawning fails: sequential `Agent` dispatch (parallel where independent), main-thread coordination, no adversarial protocol. The calling command owns the fallback; this skill supplies team-specific knowledge only.
