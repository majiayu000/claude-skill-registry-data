---
name: gaia-tm-inspect
description: >
  Use this skill when the user wants to understand why a named Gaia skill has a particular
  star rank, what its Trust Magnitude (TM) score is, which evidence rows are contributing
  (or dead), how far it is from the next grade, or what evidence to add to move the needle.
  Also use when asked for a full leaderboard of all named skills ranked by TM.
  Triggers: "why does X have 3 stars", "what's the TM for X", "inspect TM",
  "explain the score for X", "what evidence would rank up X", "show leaderboard",
  "rank all skills by TM", "what's dragging down X's score", "dead evidence rows",
  "how close is X to grade A/S".
version: "1.1.0"
genericSkillRef: registry-inspection
---

# /gaia-tm-inspect

Breaks down the Trust Magnitude (TM) score for any named Gaia skill, or produces a full ranked leaderboard. TM is the composite evidence score that gates star promotions — understanding it tells you exactly why a skill is ranked where it is and what would change that.

## Two Modes

### Inspect Mode — single skill deep-dive

```
/gaia-tm-inspect <skillId>
```

`<skillId>` is the `contributor/name` path (e.g. `garrytan/gstack`, `mattpocock/grill-me`, `obra/superpowers`).

**Output includes:**

- Each evidence row with the full score chain:
  `base magnitude → × type weight → × freshness → × mothership/creator/engagement → × inheritMultiplier → × plateau → final score`
- Dead rows (score = 0.0) and why (missing views, stars below threshold, deranked verifier, etc.)
- Fusion-recipe summary if `suiteComponents` is present: component count, graded origins, Fusion Score (informational, 0 TM)
- Total TM, overall grade, and exact points to the next grade threshold
- Most efficient evidence type to add for the next TM jump

### Leaderboard Mode — all skills ranked

```
/gaia-tm-inspect --leaderboard
```

Full ranked table grouped by grade band:

| Band | TM Threshold |
|---|---|
| S | >= 250 |
| A | >= 100 |
| B | >= 50 |
| C | >= 20 |
| Ungraded | < 20 |

Columns: Rank, Skill ID, TM, Grade, Level, Contributor.

## How to Run It

```bash
# Inspect a single skill
GAIA_OPERATOR_OVERRIDE=1 python scripts/inspectTrustMagnitude.py --skill <skillId>

# Full leaderboard
GAIA_OPERATOR_OVERRIDE=1 python scripts/inspectTrustMagnitude.py --leaderboard
```

The script loads named skills from `registry/named/`, resolves fusion recipes from `registry/nodes/`, and calls `explainTrustMagnitude()` in `src/gaia_cli/trustMagnitude.py`.

## Agent Instructions

**For `/gaia-tm-inspect <skillId>`:**

1. Run the inspect command for the requested skill.
2. Present a concise table of evidence rows: type, source, and final score. Group live rows above dead rows.
3. Call out dead rows and explain the specific reason each one contributes 0 (e.g. "social-signal: 820 views — below 1k floor").
4. State the next-grade gap plainly: "needs X more TM to reach grade Y (currently Z)".
5. Recommend the single highest-impact evidence type to add, with reasoning (e.g. "one peer-review with 3 reviewers adds ~90 TM — more than doubling current score").

**For `/gaia-tm-inspect --leaderboard`:**

1. Run the leaderboard command.
2. Present the output grouped by grade band.
3. Flag any skills with many evidence rows but low TM — dead rows are likely culprits worth a follow-up inspect.

## Trust Magnitude Formula Reference

```
artifact_score = magnitude × type_weight × freshness × mothership × creator × engagement
TM = Σ(artifact_scores), with social-signal capped at 80 across all rows
```

### Per-type magnitude formulas

| Type | Magnitude Formula | Weight | Cap |
|---|---|---|---|
| fusion-recipe | — (never scores) | 0 | 0 |
| github-stars-own | min(175.0, 35.0 × log10(stars/10)) (stars > 10) | 1.0 | 175 |
| proxy-containment | (externalStars/1000)×0.8 (min 10k stars) | 1.0 | 160 |
| verifier-attestation | 30 × verifiers | 1.5 | — |
| benchmark-result | percentile (field required — omitting it scores 0) | 1.4 | 100 |
| arxiv | citations / 5 | 1.0 | 100 |
| peer-review | 25 × reviewers | 1.2 | — |
| repo-own | commits/200 + contributors²×2 | 0.6 | 60 |
| self-attestation | 10 | 0.5 | 10 |
| social-signal | log10(views)×8 (min 1k views) | 1.0 | 80 (sum cap) |

> **fusion-recipe scores 0 TM.** Under Yggdrasil III, structure is reported by a separate,
> informational scalar — **Fusion Score** — never by Trust Magnitude. Over `N` distinct
> non-variant nodes in the resolved structural closure:
> `FS = 0` when `N = 0`; `FS = 20 × N` when `1 ≤ N ≤ 10`; `FS = 200 + 20 × √(N − 10)` when `N > 10`.
> Fusion Score gates no star, no rank, and no Trust Grade. Whenever you report one, also state
> that published TM fell for suites and fusions because this row went to 0 TM — **no evidence
> row, star count, or rank was edited** (META.md §2.1e).

### Grade thresholds

| Grade | TM Floor | Additional Gates |
|---|---|---|
| S | 250 | distinctTypes >= 3 AND independent witness (`benchmark-result`, `verifier-attestation`, or Grade A `peer-review`) |
| A | 100 | — |
| B | 50 | — |
| C | 20 | — |
| Ungraded | < 20 | — |

### Common dead-row causes to watch for

- `social-signal` with views < 1000 → scores 0 regardless of type weight
- Suite component shared repository evidence is capped at 50.0 TM per component across `github-stars-own` and `repo-own` (#1705).
- `github-stars-own` and `repo-own` pointing to the same URL → deduped; only the higher score counts
- `benchmark-result` missing `percentile` field → magnitude = 0
- Large suite with `github-stars-own` at the repo root → per-skill contribution tiny due to `/ skill_count_in_repo` divisor; use `social-signal` or `peer-review` instead
