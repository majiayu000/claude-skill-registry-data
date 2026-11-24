---
name: model-usage
description: "Summarize Hermes model usage windows by provider."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Usage, Cost, Quota, Models, DevOps]
    category: devops
---

# Model Usage Skill

Summarize Hermes model usage windows by provider: how much of each quota window is used, when it resets, and which window is closest to exhausted. The source is Hermes' own accounting in `agent/account_usage.py` (`fetch_account_usage`, `AccountUsageSnapshot`, `AccountUsageWindow`), not any third-party cost log.

## When to Use

- User asks how much usage is left, which model is closest to its limit, or when a window resets
- Before a long run, to check whether the current provider has headroom
- Comparing usage across providers (Codex, Anthropic, OpenRouter, Nous)
- Turning a `/usage` block or `hermes usage` output into a short summary

## Prerequisites

- Run commands with the `terminal` tool
- `hermes usage` is available on any Hermes host; in a session the same block comes from `/usage`
- Providers with a usage fetcher report windows (Codex, Anthropic, OpenRouter, Nous, plus provider plugins with a usage hook). A provider with no usage endpoint reports nothing; that is a gap in the provider, not a failure to summarize.

## How to Run

1. Fetch the snapshot with `terminal`: `hermes usage --json` for the configured provider, or `hermes usage --provider <slug> --json` for one provider.
2. Summarize with the bundled script (skill-relative path `scripts/model_usage.py`), or read the text block directly.
3. Report the most-used window first, with its reset time, and say which windows are account-scope vs model-scope.

## Quick Reference

```bash
hermes usage
hermes usage --provider codex
hermes usage --provider anthropic --json
hermes usage --json | python scripts/model_usage.py --mode current
hermes usage --provider codex --json > /tmp/codex-usage.json
python scripts/model_usage.py --input /tmp/codex-usage.json --mode all
```

`hermes usage --json` prints one JSON document: `provider`, `title`, `plan`, `fetched_at`, `windows` (each with `label`, `used_percent`, `resets_at`, `detail`), `details`, `unavailable_reason`. It exits 1 when nothing could be fetched: no credential configured, no usage endpoint, or the fetch failed.

## Procedure

1. Fetch fresh numbers. A snapshot older than about 15 minutes is stale: usage windows move in minutes, and the picker cache is at most one turn or one refresh interval behind. Re-run `hermes usage` instead of quoting an old block.
2. Read the windows. Each `AccountUsageWindow` carries a `label`, `used_percent`, `reset_at`, and `detail`, plus a scope:
   - `account` scope: exhausting this window exhausts the whole login.
   - `model` scope: the window caps only one model family and never implies the account itself is out of quota.
3. Summarize with the bundled script:
   - `--mode current`: the most-used window per provider (the one closest to exhausted).
   - `--mode all`: every window, most-used first.
   - `--format json` keeps the structured form for piping.
4. Present the summary: provider, plan, most-used window with percent used and reset time, then the remaining windows in descending use. State `fetched_at` so the reader knows how fresh the numbers are.
5. For several providers, fetch one JSON document per provider and pass them all to the script with repeated `--input` flags; the script groups by provider.

## Pitfalls

- Do not present a stale snapshot as live. If `fetched_at` is old, re-fetch before answering.
- A provider with no usage endpoint returns nothing. Say so plainly; do not invent a percentage.
- `used_percent` can be missing for a window (the provider did not report it). Report the window as unavailable, not as 0% used.
- Usage windows are quota gauges, not cost. Hermes has no per-model cost log; do not present percents as dollars.
- Do not reference any external cost-log tool: Hermes usage comes from `agent/account_usage.py` and `hermes usage`.

## Verification

- The summary's most-used window matches the top line of `hermes usage` run again immediately after.
- Every percent in the summary traces to a `used_percent` in the JSON document; every reset time traces to a `resets_at`.
- Re-running the fetch after a window resets shows the new window with a fresh `fetched_at`.
