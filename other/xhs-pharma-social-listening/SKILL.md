---
name: xhs-pharma-social-listening
description: Run evidence-disciplined Xiaohongshu social listening for foreign pharma employee pain points. Use when the user asks to collect and analyze notes/comments about pharma companies, aliases, roles, compliance, medical affairs, or AI topics, then produce a cited and scored sampled-insight report. Includes independent-evidence counting, MediaCrawler batch collection, and CAPTCHA/461 fallback to Agent Reach/OpenCLI.
---

# XHS Pharma Social Listening

## Overview

Use this skill to run an end-to-end Xiaohongshu social listening workflow for foreign pharma employee pain points. The main agent owns orchestration, scoring, analysis, and final reporting. Delegate Xiaohongshu collection to a collector subagent when subagent tools are available. Use Agent Reach/OpenCLI for access checks, seed discovery, spot validation, and note-level fill-in. For large runs or when OpenCLI throughput is insufficient, prefer a batch crawler path, with MediaCrawler as the first candidate. See `references/batch-collection.md` before changing collection strategy.

## Workflow

1. Check platform access:
   - Run `agent-reach doctor --json`.
   - Confirm `xiaohongshu.status` is `ok` and active backend is OpenCLI or another working backend.
2. Select collection path:
   - Delegate Xiaohongshu information collection to a subagent when `multi_agent_v1.spawn_agent` or an equivalent subagent tool is available.
   - Keep one active XHS collection subagent per logged-in account/session unless the user explicitly asks for parallel collection; platform rate limits and captcha risk matter more than raw parallelism.
   - If the task is small or only needs validation, run `scripts/collect_xhs_pharma.py`.
   - If the user reports OpenCLI is slow, requests `>1000` items, or asks for recurring social listening, read `references/batch-collection.md` and run a MediaCrawler POC first.
   - For large runs, target at least 1,000 independent evidence items: deduplicated notes plus deduplicated comments. Report search rows, note-detail rows, and comment rows separately; a detail row enriches its note and is not another independent item.
   - Use a broad-first query matrix. Start with single company, alias, and pharma-specific role terms, then add paired precision probes. Do not run cross-industry work or pain terms as standalone searches, including `市场部`, `报销`, `背调`, `外企`, `裁员`, `离职`, `合规`, `薪资`, and `KPI`; these must be paired with a pharma context anchor from `references/query-matrix.md`.
   - Cover company names, blackwords/aliases, roles, pain terms, compliance terms, AI/medical affairs terms.
   - Do not narrow or abandon the broad-first query matrix merely because MediaCrawler returns CAPTCHA/461. First distinguish query semantics from backend execution risk. If Agent Reach/OpenCLI can still search/read the same query, treat the issue as MediaCrawler-path or session cooldown risk, not as evidence that the keyword strategy is invalid.
   - Before any MediaCrawler batch run after a prior CAPTCHA/461, run an Agent Reach/OpenCLI smoke on the same or adjacent keyword: `opencli xiaohongshu search "<query>" --limit 5 -f json`, then read one note and comments. If OpenCLI succeeds but MediaCrawler fails, switch the collection backend to Agent Reach/OpenCLI and cool down MediaCrawler; do not continue retrying MediaCrawler in the same turn.
3. Analyze:
   - Run `scripts/analyze_xhs_pharma.py` on the collection directory.
   - Produce `report.md`, `topic_scores.csv`, `evidence_notes.csv`, `evidence_comments.csv`, and `dataset_summary.json`.
4. Report carefully:
   - Treat output as sampled social listening, not platform-total statistics.
   - Mark unverified items: author identity, policy authenticity, company-specific generalization, and whether a pain point is industry-wide.

## Collection Commands

Default collection:

```bash
python <skill>/scripts/collect_xhs_pharma.py --output-dir ./xhs-pharma-run --target-items 1200 --max-queries 40 --search-limit 20 --max-notes 80 --comment-limit 30 --sleep 2.5
```

Resume a partial run:

```bash
python <skill>/scripts/collect_xhs_pharma.py --output-dir ./xhs-pharma-run --target-items 1200 --resume
```

Analyze a run:

```bash
python <skill>/scripts/analyze_xhs_pharma.py --input-dir ./xhs-pharma-run --output-dir ./xhs-pharma-report
```

## Subagent Collection

Use a collector subagent for Xiaohongshu collection. The main agent should continue with non-overlapping work such as query-matrix refinement, scoring review, schema mapping, and final report preparation.

Subagent model choice:

- Prefer the environment's current general-purpose tool-using model for collection because the task requires browser/tool handling, login/captcha observation, error judgment, and structured status reporting.
- A cheaper or faster model is acceptable only for narrow deterministic subtasks such as counting rows, converting files, schema validation, or running a known smoke command.
- Do not hardcode a model identifier in this skill. If model selection is unavailable or the available model list is unknown, omit the override and inherit the environment default.

Collector subagent prompt template:

```text
Use the xhs-pharma-social-listening skill. You own only Xiaohongshu data collection for this run.
Do not edit skill files or analysis scripts. Write outputs only under <output-dir>.
Run the selected collection path, capture command lines, elapsed time, item counts, errors, login/captcha observations, and sample raw links.
Return a concise status with: output directory, files produced, search rows, detail rows, comment rows, failures, and unverified assumptions.
```

For large query matrices, shard by keyword groups only when the user explicitly asks for parallel collection. Give each collector a disjoint output directory and keep per-process crawler concurrency conservative.

## Output Standard

Every final report must include:

- Monitoring scope and sample counts.
- Query matrix summary.
- Collection limits and failure counts.
- Topic ranking table with score breakdown.
- For each topic: discussion direction, heat, repetition, author/source proximity, evidence quality, representative raw links, comment evidence, and unverified assumptions.
- Methodology appendix explaining scoring and why the result is not exhaustive.

## Scoring Model

Score each pain-topic cluster on a 0-100 scale:

```text
score =
  heat 20
  + repetition 20
  + source_proximity 15
  + comment_validation 15
  + specificity 15
  + negative_intensity 10
  + confidence 5
```

Do not include trend-spike scoring unless the run has comparable historical windows.

## Batch Collection

OpenCLI is sufficient when it can collect more than 1,000 independent evidence items with acceptable failure rates. If collection stalls, returns frequent login/captcha errors, or cannot meet the independent-evidence target, switch to batch-collection evaluation:

- `NanmiCoder/MediaCrawler`: first candidate for batch runs; supports Xiaohongshu keyword search, note detail, first-level comments, optional second-level comments, CDP/local Chrome mode, and JSONL/SQLite/Excel storage. License is non-commercial learning only.
- `JoeanAmier/XHS-Downloader`: use as link extraction or single-work metadata helper, not as the primary comment social-listening collector unless comment support is separately verified.
- `chenningling/Redbook-Search-Comment-MCP2.0`: can search/read notes/comments, but includes comment-posting tools; only use read-only functions after code audit.
- `yangsijie666/xiaohongshu-crawler`: Playwright stealth crawler with JSON/Excel and comments; lower maturity, use only for sandbox POC.

Prefer MediaCrawler for recurring or larger research runs after a small POC verifies login, output schema, and rate-limit behavior. Keep Agent Reach for spot checks against raw links and for filling missing note pages.

## CAPTCHA / 461 Handling

When MediaCrawler logs `CAPTCHA appeared`, `Verifytype`, or HTTP `461`:

1. Stop the MediaCrawler run immediately and record the keyword, shard, timestamp, output counts, and stderr path.
2. Do not keep retrying MediaCrawler, lower concurrency repeatedly, or change the query matrix as the first reaction.
3. Run an Agent Reach/OpenCLI control query with the same or nearby keyword:
   - `opencli xiaohongshu search "<query>" --limit 5 -f json`
   - Read one returned note with `opencli xiaohongshu note <url> -f json`
   - Read comments with `opencli xiaohongshu comments <url> --limit 5 -f json`
4. Interpret the result:
   - If OpenCLI succeeds, MediaCrawler search/API path is the likely blocked path; use Agent Reach/OpenCLI for slow but stable collection and wait 12-24 hours before retrying MediaCrawler.
   - If OpenCLI also fails or shows a platform challenge, treat it as account/browser/session-level risk and pause all automated collection.
5. Mark the root cause as unverified unless separate evidence isolates account, IP, device fingerprint, keyword semantics, or crawler request signature.

The 2026-07-05 local run established this pattern: MediaCrawler hit 461 on both `辉瑞` and low-frequency `RWE 药企`, in CDP and standard modes, while Agent Reach/OpenCLI successfully searched `RWE 药企` and read note comments. Treat this as evidence to preserve the broad query matrix and adjust backend/execution strategy instead.

## Frequency Block / Cooldown Handling

When Xiaohongshu or the browser page shows `Requests too frequent. Try again later.`, `访问过于频繁`, `请求过于频繁`, `操作频繁`, or an equivalent frequency block:

1. Stop all Xiaohongshu collection immediately, including OpenCLI, MediaCrawler, xhs-cli, and any subagent collector.
2. Do not run smoke tests, retries, refreshes, query changes, or alternative crawler backends during the cooldown window.
3. Write a cooldown marker named `xhs_cooldown_until.json` in the workspace, with `observed_at`, `cooldown_until`, `reason`, and source evidence. Use at least 3 hours unless the user explicitly sets a longer pause.
4. Before any future XHS collection, check the marker and refuse to collect until `cooldown_until` has passed.
5. Interpret the root cause cautiously. A frequency block confirms platform-side request throttling for the current browser/account/session path; it does not by itself prove whether the primary trigger was query semantics, total request volume, request cadence, concurrent browser tabs, IP/device fingerprint, OpenCLI adapter behavior, or earlier MediaCrawler activity.

For repeated OpenCLI `Detached while handling command` errors during an XHS batch, treat it as a warning signal. If it appears in a rising cluster together with browser instability or user-observed frequency-block pages, stop collection and apply the same 2-3 hour minimum cooldown. Mark this link as a candidate hypothesis unless the block page is directly observed.

## Evidence Discipline

When evidence is insufficient, do not present a definitive cause or solution. Report only:

- known facts from collected notes/comments,
- candidate hypotheses,
- validation paths,
- temporary mitigations if the user explicitly asks for action.

Clearly label all unverified conclusions.
