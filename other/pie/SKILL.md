---
name: pie
description: PIE command center. Entry point for all pricing intelligence operations. Runs /pie-measure by default, or dispatches to sub-skills based on intent. Use when user says "PIE", "pricing", or wants a pricing dashboard view.
---

# PIE Command Center

The umbrella skill. When invoked without qualifier, shows the full PIE
dashboard. With qualifiers, dispatches to the appropriate sub-skill.

## Usage

```
/pie              -> Full dashboard (measure + alert status + next action)
/pie measure      -> /pie-measure (quick snapshot)
/pie ratchet      -> /pie-ratchet (improve)
/pie accuracy     -> /pie-accuracy (validate)
/pie forecast     -> /pie-forecast (Layer 2)
/pie alert        -> /pie-alert (check for problems)
/pie census       -> /pie-census (expand manifest)
/pie simulate     -> /pie-simulate (full nationwide regeneration)
/pie fix          -> /pie-fix (repair worst violation)
/pie status       -> One-line summary for other skills to consume
/pie roadmap      -> Where we are on the national vision phases
```

## Default Behavior (no qualifier)

Run the full dashboard:

### 1. Health Check (< 5s)

```
PIE HEALTH [timestamp]
━━━━━━━━━━━━━━━━━━━━━
Pi: ● reachable (last sync: 2h ago)
PG: ● connected
Alerts: 0 active
```

### 2. Key Metrics (from /pie-measure)

```
COVERAGE
  Census:     70,234 ingredients
  Covered:    61.2% (42,983 / 70,234)
  Real:       24.8% | Synthetic: 36.4%
  Naked:      27,251 (no price at all)

QUALITY
  States:     31/50
  Fresh (7d): 41.3%
  Stale:      8,442 past threshold
  Accuracy:   unmeasured (run /pie accuracy)

INTELLIGENCE (Layer 2)
  Status:     LOCKED (need >80% coverage)
  Volatility: not built
  Seasonal:   not built
  Trends:     not built
```

### 3. Next Best Action

Based on current state, recommend what to run next:

```
RECOMMENDED ACTION: /pie-ratchet
  Reason: 27,251 naked ingredients (highest ROI: normalization mapping)
  Expected impact: +2-5% coverage per cycle
```

### 4. Progress Toward Vision

```
NATIONAL VISION PROGRESS
  Phase 0 (Foundation): IN PROGRESS
  Gate to Phase 1: coverage > 80% (currently 61.2%)
  Estimated: ~3 months at current ratchet rate

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [████████████░░░░░░░░░░░░░░░░] 61%
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## /pie roadmap

Show phased execution status:

```
PIE NATIONAL ROADMAP
━━━━━━━━━━━━━━━━━━━━

Phase 0: Foundation          [IN PROGRESS]
  ✓ 10-tier resolution chain built
  ✓ 150K+ stores from OSM
  ✓ Pi sync pipeline operational
  ✓ Census infrastructure built
  ○ Coverage > 80%
  ○ Accuracy measured and > 75%
  ○ All 50 states with data

Phase 1: Intelligence        [LOCKED]
  ○ Volatility scores computed
  ○ Seasonal calendars built
  ○ Trend detection active
  ○ Cost forecasting live
  ○ Forecast accuracy > 70%

Phase 2: API Alpha           [LOCKED]
  ○ Public API endpoints
  ○ Rate limiting
  ○ 100 external users

Phase 3: Scale               [LOCKED]
  ○ Pro tier monetization
  ○ Receipt OCR passive signals
  ○ 1000+ users
  ○ Serving 50K+ queries/day

Phase 4: Network Effect      [LOCKED]
  ○ Revenue-positive
  ○ Regional density flywheel
  ○ Enterprise tier
```

## /pie status (one-liner for other skills)

Output a single line consumable by `/morning`, `/status`, etc:

```
PIE: 61.2% covered (24.8% real), 31 states, 41% fresh. 27K naked. Phase 0. Next: /pie-ratchet.
```

## Skill Relationships

This skill does NOT duplicate other PIE skills. It:

- Calls `/pie-measure` for data (doesn't re-query)
- Reads `/pie-alert` log for active alerts (doesn't re-detect)
- Reads ratchet log for last action (doesn't re-compute ROI)
- Provides the "what should I do next?" decision layer

## Key Files

- Operational runbook: `docs/specs/pie-operational-runbook.md`
- National vision: `docs/specs/pie-national-vision.md`
- PIE Laws: `docs/specs/pie-laws.md`
- Ratchet log: `docs/pie-ratchet-log.md`
- Accuracy log: `docs/pie-accuracy-log.md`
- Alert log: `docs/pie-alert-log.md`
- All PIE skills: `.claude/skills/pie-*`
