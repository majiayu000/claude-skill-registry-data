---
name: orbit-multi-plugin
description: Batch-test multiple WordPress plugins in parallel with CPU throttling. Run the full gauntlet against 5+ plugins simultaneously, each on its own wp-env site. Use when the user maintains a portfolio (e.g. The Plus Addons + example-plugin + example-plugin) and says "test all my plugins", "batch QA", "audit my whole portfolio".
---

# 🪐 orbit-multi-plugin — Parallel batch testing

For agencies / vendors with multiple plugins. Run the full audit against 5 plugins at once instead of 5 hours of sequential runs.

---

## Quick start

```bash
# Test every plugin in ~/plugins/
bash ~/Claude/orbit/scripts/batch-test.sh --plugins-dir ~/plugins/

# Specific list
bash scripts/batch-test.sh \
  --plugins ~/plugins/the-plus-addons,~/plugins/example-plugin,~/plugins/example-plugin \
  --parallel 3
```

Output: `reports-batch/<plugin>/` — one full report set per plugin.

---

## How it works

For each plugin in the list:
1. Pick an unused port (8881, 8882, 8883...)
2. Spin up its own wp-env site
3. Run `/orbit-gauntlet --mode <mode>` against it
4. Capture reports to `reports-batch/<slug>/`
5. Tear down on completion

Parallelism throttled by `--parallel N` (default 3). Higher = faster but pegs CPU.

---

## CPU throttling

Each parallel gauntlet uses ~1.5 CPU cores during AI audits, ~3 cores during Playwright. Set `--parallel` based on your machine:

| CPU cores | Recommended `--parallel` |
|---|---|
| 4 cores (M1 Air) | 1-2 |
| 8 cores (M2 Pro) | 3 |
| 12+ cores (M3 Max) | 4-5 |
| 16+ cores (workstation) | 6+ |

Above the recommendation = OOMs and zombie wp-env containers.

---

## Output structure

```
reports-batch/
├── the-plus-addons/
│   ├── qa-report-<timestamp>.md
│   ├── playwright-html/
│   ├── skill-audits/
│   └── ... (full report set)
├── example-plugin/
│   └── ...
├── example-plugin/
│   └── ...
└── batch-summary.html       ← top-level dashboard
```

`batch-summary.html` shows:
- Pass/fail per plugin
- Severity bar (cumulative)
- Click any plugin → drill into its individual reports

---

## Use cases

### Pre-release sanity for a portfolio
Before tagging weekly releases for 5 plugins, run batch-test. Catches regressions across the whole stack.

### After upgrading a shared dependency
You bumped Composer / npm packages used by all 5 plugins. Run batch-test to verify nothing broke.

### Customer support: "is the issue across plugins or specific?"
Run batch-test against staging plugin builds reproducing the customer's setup. The pattern (1 plugin fails, 4 pass) tells you it's plugin-specific. (5 fail, all pass) tells you it's environmental.

### CI matrix on big workstation
Run nightly cron, batch-test the whole portfolio, send Slack ping with summary URL.

---

## Configure per-plugin

Each plugin still has its own `qa.config.json` — batch-test reads them:

```bash
~/plugins/the-plus-addons/qa.config.json
~/plugins/example-plugin/qa.config.json
~/plugins/example-plugin/qa.config.json
```

If a plugin lacks `qa.config.json`, batch-test skips it with a warning. Run `/orbit-setup` for that plugin first.

---

## Resource hygiene

After a batch run:

```bash
# Stop all wp-env sites
docker ps --filter "name=wp-env" --format "{{.ID}}" | xargs docker stop

# Or per-plugin
( cd ~/plugins/the-plus-addons && wp-env stop )

# If anything's stuck
docker rm -f $(docker ps -aq --filter "name=wp-env")
```

`batch-test.sh` calls these on exit, but if you Ctrl+C mid-run, manual cleanup may be needed.

---

## Common failures

### "No port available"
All ports 8881-8899 are taken. Stop existing wp-env sites:
```bash
docker ps --filter "name=wp-env" -q | xargs docker stop
```

### "Out of memory" — Docker dies
Lower `--parallel`, or increase Docker Desktop memory limit (Preferences → Resources).

### "Reports overlap" — wrong plugin's data in another's report
Race condition in WP_TEST_URL. Make sure each gauntlet has its own port via `--port=$port` and `WP_TEST_URL=http://localhost:$port`.

### "Took 3 hours" — should have been faster
Check that `--parallel` actually parallelises. Look at `htop` mid-run — if only 1 CPU is hot, parallelism isn't working. Check that `&` is in the bash script and `wait` is at the end.

---

## CLI flags

```bash
bash scripts/batch-test.sh \
  --plugins-dir ~/plugins/ \           # Or --plugins p1,p2,p3
  --mode quick \                       # default: quick. Use full for releases.
  --parallel 3 \                       # default: 3
  --output reports-batch/ \             # default: reports-batch/
  --skip-on-no-config \                 # default: warn but continue
  --slack-webhook https://hooks.slack.com/...   # optional notification
```

---

## Slack / Discord notification

Add `--slack-webhook` and a summary lands in the channel:

```
🪐 Orbit batch test — 5 plugins, 4 passed, 1 failed (example-plugin: 2 critical)

Reports: https://reports.example.com/batch-2026-04-29/
```

---

## Pair with `/orbit-reports`

After batch-test, generate the per-plugin master index:

```bash
for plugin in reports-batch/*; do
  python3 ~/Claude/orbit/scripts/generate-reports-index.py \
    --reports-dir "$plugin" \
    --output "$plugin/index.html" \
    --title "$(basename "$plugin")"
done
```

Then `reports-batch/index.html` (the top-level summary) links to each.
