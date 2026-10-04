---
name: superpowers-canary
description: >
  Post-deploy canary monitoring. Watches the live app for console errors,
  performance regressions, and page failures. Takes periodic screenshots,
  compares against pre-deploy baselines, and alerts on anomalies. Use when:
  "monitor deploy", "canary", "post-deploy check", "watch production",
  "verify deploy".
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
---

> **DEPRECATED** — use `/canary` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Canary — Post-Deploy Monitoring

**Purpose:** After a deployment, continuously monitor the live app for regressions
in console errors, performance, and page rendering.

**NOTE:** Requires browse daemon. If not available, use `/superpowers-qa-only`
for a one-shot report instead.

---

## Setup Check

```bash
~/.claude/skills/agent-browser/browse --version 2>/dev/null || \
  echo "BROWSE_NOT_FOUND"
```

If `BROWSE_NOT_FOUND`: Offer to install or use `/superpowers-qa-only`.

---

## Modes

| Mode | Flag | Use when |
|------|------|----------|
| **Baseline Capture** | `--baseline` | First run — establish the reference state |
| **Compare** | (default) | Subsequent runs — compare against baseline |
| **Quick** | `--quick` | 5-minute smoke test instead of continuous |

---

## Phase 1: Setup

### Parse args
```bash
URL="${1:-}"
MODE="${2:-compare}"
SLUG=$(echo "$URL" | sed 's|https\?://||' | cut -d'/' -f1 | cut -d':' -f1)
DATE=$(date +%Y%m%d-%H%M%S)
OUTDIR=~/.claude/.context/canary/$SLUG-$DATE
mkdir -p $OUTDIR/snapshots $OUTDIR/baselines
echo "URL: $URL"
echo "MODE: $MODE"
echo "OUTDIR: $OUTDIR"
```

### Detect base branch
```bash
gh pr view --json baseRefName -q .baseRefName 2>/dev/null || \
  gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || \
  echo "main"
```

---

## Phase 2: Baseline Capture (`--baseline` mode)

If `--baseline` flag is set:

1. **Discover pages:** Navigate the app, capture all primary routes
2. **Snapshot each page:** Full-page screenshot
3. **Capture console:** Check for errors/warnings on each page
4. **Measure performance:** Load time, render time for each page
5. **Save baseline:**
```bash
cat > $OUTDIR/baseline.json << 'EOF'
{
  "url": "{URL}",
  "captured": "{ISO date}",
  "pages": [
    { "path": "/", "screenshot": "snapshots/page-0.png", "load_time": N, "errors": N }
  ],
  "console_errors": [],
  "performance": { "avg_load_time": N }
}
EOF
cp $OUTDIR/baseline.json ~/.claude/.context/canary/baseline-$SLUG.json
echo "Baseline captured: ~/.claude/.context/canary/baseline-$SLUG.json"
```

Output: "Baseline captured. Run without --baseline to monitor against this baseline."

---

## Phase 3: Page Discovery

Discover pages to monitor:
```bash
~/.claude/skills/agent-browser/browse --navigate "$URL" 2>/dev/null | grep -o 'href="[^"]*"' | sed 's/href="//;s/"//' | grep -v "^#" | grep -v "^javascript" | head -20
```

Ask via AskUserQuestion:
> "Found N pages to monitor. Which should I include?
> - A) All discovered pages
> - B) Homepage + key user flows only
> - C) Specify pages manually"

---

## Phase 4: Pre-Deploy Snapshot (if no baseline exists)

If running without `--baseline` and no baseline exists:
1. Offer to capture baseline first via AskUserQuestion
2. If declined: run quick snapshot and note it as reference, not comparison

---

## Phase 5: Continuous Monitoring Loop

For each page in scope, every 60 seconds:

### Capture current state
1. Navigate to page
2. Full-page screenshot → `$OUTDIR/snapshots/{page}-{timestamp}.png`
3. Check console errors
4. Measure load time
5. Check for JS errors

### Compare against baseline
```bash
BASELINE=~/.claude/.context/canary/baseline-$SLUG.json
if [ -f "$BASELINE" ]; then
  # Load and compare
  echo "Comparing against baseline..."
else
  echo "No baseline — running in observation mode"
fi
```

### Alert rules
Alert if ANY of these persist for 2+ consecutive checks:
- **New console errors** — errors not in baseline
- **Page render change** — screenshot differs significantly
- **Load time regression** — >50% slower than baseline
- **Page fails to load** — HTTP error or blank page
- **JS errors** — uncaught exceptions

### Alert format
```
ALERT: {type}
Page: {URL}
Duration: {consecutive failures} checks
Expected: {baseline state}
Actual: {current state}
Evidence: snapshots/{page}-{timestamp}.png
```

Use AskUserQuestion for alerts:
> "ALERT: {description}. Options:
> - A) Continue monitoring
> - B) Stop monitoring
> - C) Page-specific focus (narrow to this page only)"

---

## Phase 6: Health Report

After monitoring ends (user stops or timeout), generate report:

```
CANARY REPORT
=============
URL: {URL}
Duration: {start} → {end}
Checks: N
Pages monitored: N

CONSOLE
=======
Errors found: N (baseline: N)
Warnings: N (baseline: N)
New errors: {list}

PERFORMANCE
===========
Avg load time: {N}ms (baseline: {N}ms)
Change: +{N}% / -{N}%
Slowest page: {path} @ {N}ms

PAGE RENDERS
============
{page}: OK / CHANGED / FAILED
...

ALERTS TRIGGERED
================
N total
{list}

VERDICT: [CLEAR / REGRESSION_DETECTED / CRITICAL]
```

---

## Phase 7: Baseline Update

After monitoring completes cleanly (no critical alerts):

Ask via AskUserQuestion:
> "Monitoring completed without critical regressions. Update the baseline with current state?
> - A) Yes — update baseline (recommended)
> - B) No — keep existing baseline"

If A:
```bash
cp $OUTDIR/baseline.json ~/.claude/.context/canary/baseline-$SLUG.json
echo "Baseline updated."
```

---

## Rules

- **Speed:** Start within 30 seconds of invocation
- **Alert on changes, not absolutes:** A page being slow in isolation isn't an alert — it being slower than baseline is
- **Screenshots as evidence:** Every alert needs visual proof
- **Transient tolerance:** Single-check anomalies are noise. Two+ consecutive = signal.
- **Baseline is king:** No baseline = observation mode only

---

## Monitoring Loop (Quick Mode)

If `--quick` flag:
```bash
# Run 5 checks, 30 seconds apart, then produce report
for i in $(seq 1 5); do
  echo "Check $i/5 at $(date)"
  # Run checks...
  sleep 30
done
```

---

## Completion Status

- **DONE** — Monitoring complete, report generated, no critical regressions
- **DONE_WITH_CONCERNS** — Monitoring complete with regressions detected
- **BLOCKED** — Browse daemon unavailable
- **NEEDS_CONTEXT** — No URL or baseline available
