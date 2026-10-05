---
name: qruiq-community-analyze
description: |
  Produce a comprehensive analysis report for a Reddit community — combines timing analysis
  (when high-upvote comments arrive) with optional critic-prompt training (what makes
  comments score well). Use when asked to "analyze community", "analyze subreddit",
  "research community", "社区分析", "分析 subreddit", or when someone wants to know how to
  do comment-ops on a specific Reddit community.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
  - TodoWrite
---

# qruiq-community-analyze

End-to-end Reddit community analysis for comment-ops planning. Given a single subreddit, orchestrates the two workflows in the `cowork` repo (`analysis-comment-timing` + `community-critic-prompt-train`) and synthesizes their output into a single comprehensive report.

## When to use

Trigger when the user asks anything like:
- "analyze r/xxx" / "分析 r/xxx"
- "how should I do comment-ops on r/xxx"
- "what's the golden window for r/xxx"
- "train a critic for r/xxx"
- "给我一份 r/xxx 的完整报告"
- Just a subreddit name or URL with intent to understand it

Do NOT trigger for generic "analyze Reddit" questions without a specific subreddit.

## Prerequisites

This skill depends on the `cowork` repo at `/Users/timmysun/Desktop/cowork`. It must have:
- `yarn build` passing
- Valid `TSKGONE_API_KEY`, `TSKGONE_API_SECRET`, `TSKGONE_FETCH_JSON_TASK_GROUP_ID` in `.env`
- Valid `ZENMUX_API_KEY` (for critic training step) in `.env`
- Both workflows registered in `src/workflows/registry.ts`: `analysis-comment-timing` and `community-critic-prompt-train`

If prerequisites are missing, tell the user and stop.

## Parameters

Collect before execution:

| Parameter | Required | Default | Description |
|---|---|---|---|
| `SUBREDDIT` | Yes | — | Target subreddit, with or without `r/` prefix (e.g. `r/wallstreetbets` or `singaporefi`) |
| `DEPTH` | No | `quick` | `quick` = timing only (~3 min, no LLM cost). `standard` = timing + single-seed critic (~35 min, moderate LLM cost). `deep` = timing + multi-seed critic with 3 seeds (~2 hours, high LLM cost). |
| `SEEDS` | No | `7,42,99` | Only used when `DEPTH=deep`. Seeds for multi-seed validation. |
| `MIN_POST_AGE_DAYS` | No | `3` | Override timing workflow's post-age filter. Increase for very fast-moving communities if stats look censored. |

If the user only gives a subreddit name, default to `DEPTH=standard` unless they say otherwise. Explicitly confirm depth and cost with one `AskUserQuestion` before running anything that calls LLMs.

## Steps

**Execute all steps directly, not as TODOs to the user. Use TodoWrite only for internal multi-step tracking.**

### 1. Verify prerequisites

```bash
cd /Users/timmysun/Desktop/cowork
test -f .env && grep -q TSKGONE_API_KEY .env && grep -q ZENMUX_API_KEY .env \
  && echo "env ok" || echo "env MISSING"
grep -q "analysis-comment-timing" src/workflows/registry.ts \
  && grep -q "community-critic-prompt-train" src/workflows/registry.ts \
  && echo "workflows ok" || echo "workflows MISSING"
```

If either check fails, stop and tell the user what's missing.

### 2. Confirm depth with the user (once, compact)

Use **one** `AskUserQuestion` call. Show the three options with cost/time estimates. Skip this step if the user already specified a depth in the initial request.

### 3. Run the timing workflow (always, for every depth)

```bash
cd /Users/timmysun/Desktop/cowork
yarn wf analysis-comment-timing -- --subreddit=<SUBREDDIT> --min-post-age-days=<MIN_POST_AGE_DAYS> 2>&1 \
  | grep -vE "PENDING|PROCESSING|Task [a-z0-9]+ \[fetchJson\] params" \
  > /tmp/qruiq-timing-<safe-subreddit>.log
```

Where `<safe-subreddit>` is the subreddit name lowercased with non-alphanumerics replaced by `_`.

**Expected duration:** 1-3 minutes. Fails fast if `SUBREDDIT` is wrong.

**Capture the log dir:** find the latest `logs/workflow/analysis-comment-timing_*` directory written during this run. Read its `output.json` for structured data and `output.md` for the generated markdown.

### 4. Run the critic workflow (if DEPTH != quick)

For `DEPTH=standard`:

```bash
yarn wf community-critic-prompt-train -- --subreddit=<SUBREDDIT> --seed=7 2>&1 \
  | grep -vE "PENDING|PROCESSING|Task [a-z0-9]+ \[fetchJson\] params" \
  > /tmp/qruiq-critic-<safe-subreddit>.log
```

For `DEPTH=deep`:

```bash
yarn tsx src/workflows/community-critic-prompt-train/run-multi-seed.ts \
  --subreddit=<SUBREDDIT> --seeds=<SEEDS> 2>&1 \
  | grep -vE "PENDING|PROCESSING|Task [a-z0-9]+ \[fetchJson\] params" \
  > /tmp/qruiq-critic-multi-<safe-subreddit>.log
```

**Expected durations:** standard ~30-60 min, deep ~2-6 hours depending on seed count.

**Run in background.** The `run_in_background: true` option on Bash is required so the user sees progress. Tell the user: "Critic workflow runs in background; I will notify when it completes." Continue to Step 5 if data is sufficient without waiting. If the user is waiting for the final report, periodically check status via `BashOutput` or `ps aux`.

**Handle failure:** if `fetch-comments` fails with "not enough usable posts", the community is too small or the filters are too strict for it. In that case:
- Look at `output.json > fetch.dropReasons` from timing step to diagnose (`weak-label-separation` vs `too-few-comments` vs `negatives-not-downvoted`).
- Suggest to the user: widen `topN` (edit config) or relax `maxNegativeUpvote` — but do NOT auto-modify config unless user asks. Instead report the diagnosis and stop the critic step.
- Always still produce the timing report (Step 5) even if critic failed.

### 5. Extract structured data from both runs

Use the helper script `extract-metrics.mjs` co-located with this SKILL.md. It handles finding the latest log dir, parsing output.json, and flattening key fields. Run with the subreddit the user gave:

```bash
# Timing metrics (always)
node ~/.qruiq/skills/skills/qruiq-community-analyze/extract-metrics.mjs timing <SUBREDDIT>

# Critic metrics (standard mode)
node ~/.qruiq/skills/skills/qruiq-community-analyze/extract-metrics.mjs critic <SUBREDDIT>

# Multi-seed metrics (deep mode)
node ~/.qruiq/skills/skills/qruiq-community-analyze/extract-metrics.mjs critic-multi <SUBREDDIT>
```

Each command prints a JSON object to stdout. Parse the output to populate the report template. Exit codes:
- `0` — success, JSON on stdout
- `2` — no matching log dir (workflow failed or wasn't run yet)
- `3` — critic-multi mode but no `multi-seed-summary.json` (multi-seed runner wasn't used)

If the helper fails, fall back to reading `output.json` directly from the latest `logs/workflow/*` directory that matches the workflow name and subreddit.

### 6. Write the synthesized report

Write to: `/Users/timmysun/Desktop/cowork/logs/qruiq-community-analyze/<safe-subreddit>_<ISO-timestamp>.md`

Create the parent directory if it doesn't exist.

Follow the template in **Report structure** below. Keep the tone direct and evidence-based. Cite exact numbers from the JSON files.

### 7. Show the report to the user

Print the full report inline via stdout — do NOT just give them a file path. The user wants to see the content. At the bottom of the message, include:
- Absolute path to the saved report file
- Absolute path to the raw `output.json` files from both workflows (so they can dig deeper if they want)
- Absolute path to the `finalPrompt` as a standalone file (write it if you ran the critic step — see Step 8)

### 8. Save the trained critic prompt as a standalone file (if DEPTH != quick)

Write the final critic prompt as a plain text file to:
`/Users/timmysun/Desktop/cowork/logs/qruiq-community-analyze/<safe-subreddit>_critic-prompt.txt`

This lets the user `cat` it and copy-paste directly as a system prompt.

## Report structure

The synthesized markdown report must contain the following sections, in this order. Populate every field from actual data — never leave placeholders.

### Header

```
# r/<SUBREDDIT> — Comprehensive Community Analysis

**Analyzed:** <ISO date>
**Depth:** <quick | standard | deep>
**Workflows:** analysis-comment-timing[, community-critic-prompt-train]
```

### 1. Executive summary (3-5 bullets)

One-paragraph community character sketch + 3 hard recommendations, e.g.:
- Monitoring cadence (realtime / hourly / daily) — derived from golden window
- Content style dos/don'ts — derived from critic prompt learned rules (if standard/deep)
- Whether automation is feasible — derived from sample size + training signal

### 2. Timing analysis

Table from `timing_summary`:

| Metric | Value |
|---|---|
| Golden window (80% top) | `fmtDuration(goldenWindowSec)` |
| Median top-bucket age | `fmtDuration(medianTopBucketAgeSec)` |
| Median bottom-bucket age | `fmtDuration(medianBottomBucketAgeSec)` |
| Spearman(age, score) | `-0.xxx` |
| Posts analyzed | `totalPosts` |
| Comments analyzed | `totalComments` |

Then the full ASCII histogram from the timing report's `Distribution by age bucket` section (copy verbatim from `output.md`).

Then cumulative shares:
- Within 1h: `cumTopShareAt.1h * 100`%
- Within 6h: `cumTopShareAt.6h * 100`%
- Within 24h: `cumTopShareAt.24h * 100`%

### 3. Operational implications

Based on the golden window value, include ONE of these blocks:

- **< 30 min**: 必须实时监控. SLA 目标 `post → comment < (goldenWindowSec / 10)` 秒. Cron 轮询架构 structurally cannot win.
- **30 min - 3 h**: 小时级轮询足够. SLA post → comment < 30min.
- **3 h - 12 h**: 几小时一次 sweep. SLA post → comment < 1-2h.
- **> 12 h**: 日度 sweep. 内容质量比速度更重要.

### 4. Critic training results (if DEPTH != quick)

**Single-seed version** (standard):

| Metric | Baseline | Final | Δ |
|---|---|---|---|
| Classification accuracy | `xx.x%` | `xx.x%` | `+xx.xpp` |
| Mean positive fitScore | `x.xx` | `x.xx` | `+x.xx` |
| Mean negative fitScore | `x.xx` | `x.xx` | `+x.xx` |
| Score gap | `x.xx` | `x.xx` | `+x.xx` |
| Spearman (per-post avg) | `0.xxx` | `0.xxx` | `+0.xxx` |

Plus training summary:
- Total training posts: `training.totalPosts`
- Converged: `training.convergedCount / training.totalPosts` (`xx%`)
- Hard cases: `training.hardCases.length`

**Multi-seed version** (deep): render the per-seed table + multi-seed summary verdict from `multi-seed-summary.json`:

| seed | Kept | Baseline acc | Final acc | Δ acc | Δ Spearman |
...

And the final **VERDICT** line from the summary.

### 5. Learned critic prompt (if DEPTH != quick)

```
<full finalPrompt content from output.json>
```

Followed by 3-7 bullets extracted from the prompt highlighting the most distinctive rules (e.g., for WSB: "Could 50 others write this" test, small-position solidarity reverse signal, DD dismissal reward).

### 6. Hard cases (if DEPTH != quick and any exist)

For each hard case (post that didn't converge), list:
- Post title
- Iterations run
- Last misclassification pattern

Interpret: are they all the same type of post? If yes, note that as a labeling artifact to watch for.

### 7. Filter pipeline stats

Both workflows pass through filters. Report:

**Timing workflow**:
- Raw: `fetch.rawCount`
- Kept: `fetch.keptCount`
- Drop reasons breakdown

**Critic workflow** (if done):
- Raw: `fetch.rawCount`
- Kept: `fetch.keptCount`
- Drop reasons breakdown

If any reason dominates (>50% of drops), call it out with a suggested config tweak.

### 8. Pre-ship checklist (if DEPTH != quick)

Yes/no per item:
- Spearman Δ > 0 — `YES/NO`
- Convergence rate ≥ 70% — `YES/NO`
- Hard cases NOT all same post type — `YES/NO`
- Final prompt no internal contradictions — `REQUIRES MANUAL CHECK`
- Schema validation passed — `YES/NO`

Final recommendation: **SHIP** / **NEEDS MORE WORK** / **DO NOT SHIP** with one-sentence justification.

### 9. Reproducibility

```bash
# Timing
yarn wf analysis-comment-timing -- --subreddit=<SUBREDDIT>

# Critic (standard)
yarn wf community-critic-prompt-train -- --subreddit=<SUBREDDIT> --seed=7

# Critic (deep, multi-seed)
yarn tsx src/workflows/community-critic-prompt-train/run-multi-seed.ts \
  --subreddit=<SUBREDDIT> --seeds=7,42,99
```

## Helpers

### Duration formatter

```
< 60s       → "<X>s"
< 3600s     → "<X.X>m"
< 86400s    → "<X.X>h"
else        → "<X.X>d"
```

### Safe subreddit slugification

Input `r/wallstreetbets` → `wallstreetbets`
Input `r/Something.Weird` → `something_weird`

```bash
echo "<SUBREDDIT>" | sed 's|^r/||i' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g'
```

## Error handling

- **Timing workflow fails**: report the fetch/filter stats from the error log. Most common cause: subreddit doesn't exist or is private. Verify URL in the error and suggest the correct spelling.
- **Critic workflow fails with "not enough usable posts"**: explicitly tell user this community is below the size threshold, but still produce the timing report. Suggest `--min-post-age-days=1` to include newer posts if timing stats look fine.
- **Timing schema validation fails**: report as a bug and dump the validation errors; don't try to fix automatically.
- **Background critic run still active when user wants report**: produce the timing-only report immediately + a note that critic data will be appended when the background job completes. Then use `BashOutput` to monitor and issue a follow-up message when it's done.

## Output conventions

- Always save the full report to disk even if the user is waiting inline.
- Never commit changes; never modify `config/workflow.yaml` without explicit user approval.
- Always include the absolute path to the JSON artifacts in the final message so the user can explore.
- If you launched background jobs, list their task IDs so the user can kill them if needed.
