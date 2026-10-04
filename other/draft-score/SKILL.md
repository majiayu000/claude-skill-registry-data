---
name: draft-score
description: Lightweight ContentShake AI self-check the /draft stage can call before saving. Returns just SEO + Quality scores (no full optimization) so the writer knows whether the draft is in winning territory before /quality-check runs. Fails soft when SEMRUSH_API_KEY is unset.
allowed-tools: Read, Write, Bash
---

# Draft Score Skill (ContentShake self-check)

Run a lightweight ContentShake AI score on the current draft so the writer / orchestrator knows whether the draft is already close to winning territory. Cheaper than the full `/optimize-content` pass — uses the `score` action of `contentshake_optimize.py` which doesn't return the term/topic recommendation lists.

This skill is **optional** in the pipeline. If the draft is already strong, it lets the orchestrator skip directly to `/quality-check` → `/verify-claims` and save a full `/optimize-content` pass for a future revision. If the draft scores poorly, it's an early warning that `/optimize-content` will need its full iteration budget.

## Input

`/draft-score {slug}`

Reads:
- `content-pipeline/5-drafts/{slug}.md` (or `6-drafts-cited/{slug}.md` if already cited)
- `content-pipeline/1-research/{slug}.md` (target keyword)

## Process

### Step 1 — Preflight

1. Confirm the draft exists. If not, exit with a clear error.
2. Read the target keyword from the research dossier's frontmatter (or fall back to the slug with hyphens replaced by spaces).
3. Check `SEMRUSH_API_KEY_CONTENTSHAKE` then `SEMRUSH_API_KEY_BLOG_AGENT` in env.

### Step 2 — Soft-fail when key is missing

If neither key is set:

1. Print to stdout:
   ```
   draft-score: SEMRUSH_API_KEY not set in env. Skipping ContentShake self-check.
                Load via `doppler run -- claude` or export the key. Pipeline continues.
   ```
2. Write a stub at `content-pipeline/optimization/{slug}-draft-score.json`:
   ```json
   {
     "skipped": true,
     "reason": "SEMRUSH_API_KEY not set",
     "_meta": {"slug": "{slug}", "action": "score"}
   }
   ```
3. Exit 0. **Same convention `/research` uses for missing OpenRouter** — never block the pipeline on a missing optional key.

### Step 3 — Call the script with --action=score

```bash
doppler run -- python .claude/skills/optimize-content/scripts/contentshake_optimize.py \
  --slug {slug} --keyword "{keyword}" --action score
```

The `score` action returns just `seo_score` and `quality_score` (plus `_meta`) — no term lists, no missing-topic analysis, no competitor coverage. Cheaper than `optimize` and counts as 1 unit against the same `BLOG_AGENT_CONTENTSHAKE_MONTHLY_CAP` budget tracked by `/optimize-content`.

### Step 4 — Persist the result

Save the script's stdout to `content-pipeline/optimization/{slug}-draft-score.json`. Increment the budget counter at `content-pipeline/optimization/api-budget.md` (shared with `/optimize-content`).

### Step 5 — Print the verdict

```
draft-score: SEO 7.2  Quality 8.1   verdict=NEEDS_OPTIMIZE
  → /optimize-content {slug} likely needed before publish
```

Verdict heuristic:

| Condition | Verdict | Implication for orchestrator |
|---|---|---|
| `seo_score ≥ 8 AND quality_score ≥ 8` | `WIN_LIKELY` | `/optimize-content` may be skippable — quality-check first, then decide |
| `seo_score ≥ 7 AND quality_score ≥ 7` | `BORDERLINE` | Run `/optimize-content` but expect 1–2 iterations to clear |
| Otherwise | `NEEDS_OPTIMIZE` | `/optimize-content` should run with full iteration budget |

## Output

- `content-pipeline/optimization/{slug}-draft-score.json` — the raw scoring response (or stub if skipped)
- One-line verdict to stdout

## Quality checklist

- [ ] Draft file exists and was readable
- [ ] Target keyword resolved from research dossier or slug
- [ ] Soft-fail path runs cleanly when `SEMRUSH_API_KEY` is unset (exits 0, writes stub)
- [ ] Result JSON persisted to `optimization/{slug}-draft-score.json`
- [ ] Verdict printed with the recommended next action

## When to call this skill

This skill is designed to be called from the `/draft` stage **after the draft is written but before `/quality-check`** — a "is this close to ready?" signal. It's also fine to call standalone:

- During iterative revisions, to see if a manual edit moved the score
- Before deciding whether to schedule `/optimize-content` (saves a full optimize pass when the draft is already strong)
- After `/update-draft` to see if the refresh moved scores in the right direction

## When NOT to call this skill

- When `/optimize-content` is about to run anyway — the full optimize pass produces scores AND recommendations, so the lightweight self-check is redundant and wastes a budget unit
- When the budget is at 100% — the script will exit cleanly but the call still gets recorded as attempted

## Why not just call `/optimize-content`

`/optimize-content` is a 5-iteration loop that mutates the draft. This skill is a **read-only** scoreback. Call this when you want to know "where do I stand?" without committing to the full optimization. Two distinct jobs.
