---
name: auto-blog-loop
description: Autonomous run-loop for the blog pipeline. Picks the top unwritten keyword from the vetted queue, dispatches /blog-pipeline in autonomous mode, auto-publishes on success, quarantines persistent failures, and refreshes the keyword queue when empty. Cron-friendly. No human in the loop.
allowed-tools: Read, Write, Bash, Agent, Glob
---

# Auto Blog Loop (Master Orchestrator)

The autonomous entry point. Replaces the human as the decider for everything the pipeline currently asks: "which keyword?", "skip-or-regenerate?", "ship this draft?", "publish?".

## Invocation

```
/auto-blog-loop [--max N] [--update-mode] [--keyword "<override>"]
```

- `--max 3` (default) — articles per loop invocation. Cron runs once nightly with `--max 3`.
- `--update-mode` — refresh oldest stale article instead of writing new ones (see "Update mode" below).
- `--keyword "<phrase>"` — force pick a specific keyword (skips selector, useful for one-off catch-up runs).

## Why an Agent-dispatching loop, not inline forks

Same constraint as `/blog-pipeline` — Skill forks inherit context and hit `Prompt is too long` after compaction. Every stage of every article is dispatched as a fresh `general-purpose` Agent so the loop can run for hours without context pressure.

## Process (creation mode — default)

For each iteration up to `--max`:

1. **Pick the next keyword.** Run `python scripts/auto_keyword_selector.py`.
   - Exit 0 → JSON on stdout. Parse keyword, slug, priority_score, verdicts.
   - Exit 2 → queue empty/missing. Dispatch `/keyword-research-pipeline` (Agent), then re-run the selector. If still exit 2, log "no work, exit clean" and stop the loop.
   - Other exit → log error to `auto-blog-log.csv`, stop the loop.

2. **Append the audit row** (started_at, slug, keyword, source, verdicts) before dispatching the article. This way a crash mid-pipeline still leaves the audit log honest.

3. **Dispatch /blog-pipeline as an Agent** with env `BLOG_AGENT_AUTONOMOUS=1 UNATTENDED=1` (so the orchestrator inside picks the autonomous branch on every decision). Brief:

   ```
   You are the autonomous blog-pipeline runner for slug {slug}, keyword "{keyword}".
   Project root: {ROOT}. Brand: see brand-config.md.
   
   Run /blog-pipeline per .claude/skills/blog-pipeline/SKILL.md (read it first), with these env vars set:
   - BLOG_AGENT_AUTONOMOUS=1 (enables skip-resume, auto-revision, auto-format-for-publish)
   - UNATTENDED=1 (enables capture-visuals unattended mode)
   - BLOG_AGENT_AUTO_PUBLISH=1 (enables publishedAt=now in format-for-publish)
   - BLOG_AGENT_REVISION_BUDGET=2 (max revision passes on quality FAIL)
   
   The orchestrator's autonomous branch will: skip stages whose output exists, run stages 1-7 normally, run /quality-check, auto-revise on FAIL up to 2 times, run /verify-claims and /generate-visuals, fire /capture-visuals if Chrome MCP connected, render preview, then auto-run /format-for-publish --auto-publish.
   
   Return: final verdict (PASS/BORDERLINE-no-CRITICAL/QUARANTINED), final score, list of stages run with paths, public Strapi URL on auto-publish, any failures. Under 500 words.
   ```

4. **Read the agent's report.**
   - **Success path** (verdict ∈ {PASS, BORDERLINE-no-CRITICAL} AND format-for-publish reported a Strapi URL):
     - Run `python scripts/auto_publish_check.py {slug}` to verify the public URL renders the right H1.
     - Update the audit row: `verdict`, `score`, `action=published`, `strapi_url`.
     - Continue to next iteration after a 60s cool-down.
   - **Quarantine path** (verdict=QUARANTINED, or auto-publish failure, or pipeline error):
     - Write `content-pipeline/9-needs-review/{slug}.md` with failure reason + last good stage if not already there.
     - Update audit row: `action=quarantined`, `error_reason`.
     - Continue to the next keyword (don't stop the loop on a single failure).

5. **After `--max` iterations OR queue exhausted:** print a tally and exit cleanly.

## Process (update mode)

`--update-mode`: refresh the oldest published article (lastUpdated < now - 12 months).

1. **Fetch Strapi inventory** via `.claude/skills/brand-reference/scripts/fetch_strapi_inventory.py`. Find articles with `lastUpdated < now - 12 months` (configurable via `BLOG_AGENT_REFRESH_AGE_DAYS`, default 365). Sort oldest-first.

2. For each candidate up to `--max`:
   - Skip if a `content-pipeline/9-needs-review/{slug}.md` already exists (quarantined; needs human first).
   - Dispatch `/update-pipeline <url>` Agent with `BLOG_AGENT_AUTONOMOUS=1` env. The orchestrator inside auto-skips audits scored "skip", auto-merges audits, dispatches `/format-for-publish {slug} --auto-publish --update` (PATCH on existing slug), runs `auto_publish_check.py`.
   - Same audit-row + quarantine handling as creation mode.

## Selector exit-2 handling (auto-refresh queue)

When the selector returns exit 2 (queue empty):

```
Dispatch /keyword-research-pipeline as a fresh Agent with env BLOG_AGENT_AUTONOMOUS=1.

Wait for completion. Re-run scripts/auto_keyword_selector.py.

If still exit 2 (the keyword pipeline produced no candidates — rare, usually means Semrush AI Toolkit / API quota exhausted or genuinely empty gap), log a "no work" entry to auto-blog-log.csv and stop the loop. Don't try to run keyword research twice in a row — wait for the next cron cycle.

If the keyword pipeline itself failed (exit non-zero), keep the previous keyword-queue.csv (if any) and try the selector once more. If selector still empty, stop cleanly.
```

The previous queue (if any) is the safety net: a failed keyword research run never erases what's already there.

## Audit log row format

`content-pipeline/audit/auto-blog-log.csv`:

```
slug,keyword,started_at,ended_at,verdict,score,action,error_reason,source,bid_verdict,aio_verdict,redteam_verdict,strapi_url
```

One row per article attempt. Action is one of `published`, `quarantined`, `update-published`, `update-quarantined`, `update-skipped` (no-update-needed marker), `keyword-pipeline-skip` (queue empty after refresh).

## Reporting (final tally)

```
✓ Auto-blog-loop complete (mode: creation | update)

Picked from queue:        N
Published live:           X (+ Strapi URLs)
Quarantined:              Y (see content-pipeline/9-needs-review/)
Update mode no-op:        Z (articles still fresh)
Keyword research re-run:  yes/no

Total runtime:            ~M minutes
Audit log:                content-pipeline/audit/auto-blog-log.csv
```

No "open in browser" or "review the preview" instructions — autonomous mode means done is done.

## Per-run cap and cool-down

- `--max N` caps articles per invocation (default 3).
- Between articles: 60s cool-down (rate-limit hygiene for Replicate / OpenRouter / Semrush).
- The keyword research re-run (when queue empty) does NOT count against the per-run cap — it's setup, not articles.

## Cron entry (production VPS)

```cron
# /etc/cron.d/blog-agent
# Nightly autonomous run, 3 articles per night
0 2 * * * ndong cd /opt/blog-agent && doppler run -- claude -p "/auto-blog-loop --max 3" --model claude-sonnet-4-6 >> /var/log/blog-agent.log 2>&1

# Weekly update-mode pass (Monday 4am, 1 article)
0 4 * * 1 ndong cd /opt/blog-agent && doppler run -- claude -p "/auto-blog-loop --update-mode --max 1" --model claude-sonnet-4-6 >> /var/log/blog-agent.log 2>&1
```

The `--model claude-sonnet-4-6` pin matches existing memory ("Claude-in-Chrome work always runs on Sonnet 4.6") and prevents cron drift to Opus.

## When the loop should NOT run

- Semrush AI Toolkit / API quota exhausted: Layer 1c logs to `cache/aio-toolkit-quota.log`. Skip until reset.
- Strapi unreachable: `auto_publish_check.py` will quarantine; a streak of consecutive quarantines = stop.
- Semrush MCP auth expired: Layer 2 will fail; keyword research pipeline halts cleanly.

The loop is designed to fail forward — one bad article doesn't stop the loop, but one structural failure does.

## Idempotency

- Pipeline status: stages whose outputs exist are skipped (resume-from-failure semantics).
- Quarantine: slugs in `9-needs-review/` are excluded from the selector — no infinite re-quarantine.
- Audit log: append-only.

## Cost expectations (per --max 3 nightly run)

- 3x /blog-pipeline: ~$2-5 in tokens + ~$0.15 Replicate (4 images avg) + ~$1 OpenRouter (deep research) ≈ $3-7
- Optional 1x /keyword-research-pipeline: ~$1.50
- Strapi/auto_publish_check: free
- Total: ~$3-9/night, ~$100-280/month

For comparison, a human content writer producing 3 articles/day at $100/article = $9k/month. Autonomous mode is ~3% of that cost.

## When to add a human checkpoint anyway

The loop is autonomous-by-default but writes everything to disk. Editors can spot-check `content-pipeline/audit/auto-blog-log.csv` and the published Strapi entries asynchronously. The pipeline doesn't *require* human review, but post-publish review remains valuable for calibration. Calibration changes go in:
- `bid-method.md` (if BID gates need tuning)
- `aio-cannibalization-rubric.md` (if AIO scoring drifts)
- `keyword-redteam` SKILL (if redteam over-keeps or over-drops)
- `quality-check` SKILL (if voice-baseline thresholds need adjusting)
