---
name: gemma_telemetry_retention_detector
description: Fast binary classification of YouTube telemetry records for retention strategy
version: 1.0
author: 0102_wre_team
agents: [gemma]
dependencies: []
domain: autonomous_operations
intent_type: BINARY_CLASSIFICATION
promotion_state: prototype
estimated_tokens: 50-100
execution_time_ms: 10-50
wsp_chain: [WSP_77, WSP_91, WSP_96]
---

# Gemma Telemetry Retention Detector

**Purpose**: Fast pattern matching to classify YouTube DAE heartbeat records for retention strategy

**Architecture**: Phase 1 of Gemma→Qwen→0102 cleanup wardrobe pattern

## WSP Compliance

- **WSP 77**: Agent Coordination (Gemma fast classification → Qwen strategy)
- **WSP 91**: DAEMON Observability (telemetry lifecycle management)
- **WSP 96**: WRE Skills Wardrobe (autonomous cleanup execution)

## Task Description

Scan `data/foundups.db::youtube_heartbeats` table and classify records into retention categories using fast binary pattern matching.

## Input Contract

```json
{
  "database_path": "data/foundups.db",
  "table": "youtube_heartbeats",
  "scan_limit": 1000,
  "current_timestamp": "2025-10-27T20:00:00Z"
}
```

## Classification Rules (Fast Binary Decisions)

### Rule 1: Recent Activity (KEEP)
- Age: < 30 days
- Pattern: High training value, operational visibility
- Binary decision: `category = "keep_recent"`

### Rule 2: Training Data (KEEP)
- Age: 30-90 days
- Pattern: Historical patterns for Gemma learning
- Binary decision: `category = "keep_training"`

### Rule 3: Archivable (ARCHIVE)
- Age: 91-365 days
- Pattern: Historical value but low operational need
- Binary decision: `category = "archive_candidate"`

### Rule 4: Purgeable (PURGE)
- Age: > 365 days
- Pattern: Minimal value, disk space reclamation
- Binary decision: `category = "purge_candidate"`

## Output Contract

```json
{
  "scan_timestamp": "2025-10-27T20:00:00Z",
  "total_records_scanned": 3719,
  "categories": {
    "keep_recent": {
      "count": 1200,
      "age_range_days": "0-30",
      "disk_mb": 45
    },
    "keep_training": {
      "count": 1500,
      "age_range_days": "30-90",
      "disk_mb": 95
    },
    "archive_candidate": {
      "count": 800,
      "age_range_days": "91-365",
      "disk_mb": 70
    },
    "purge_candidate": {
      "count": 219,
      "age_range_days": ">365",
      "disk_mb": 19
    }
  },
  "recommendation": "archive_and_vacuum",
  "estimated_reclaim_mb": 89,
  "confidence": 0.95
}
```

## Execution Logic (Gemma Implementation)

```python
from datetime import datetime, timedelta, timezone
import sqlite3

def classify_heartbeat_age(timestamp_iso: str, now: datetime) -> str:
    """Fast binary classification by age"""
    ts = datetime.fromisoformat(timestamp_iso.replace('Z', '+00:00'))
    age_days = (now - ts).days

    if age_days < 30:
        return "keep_recent"
    elif age_days < 91:
        return "keep_training"
    elif age_days < 366:
        return "archive_candidate"
    else:
        return "purge_candidate"

def scan_telemetry_retention(db_path: str) -> dict:
    """Gemma fast scan for retention categories"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all heartbeat timestamps
    cursor.execute("SELECT timestamp FROM youtube_heartbeats ORDER BY timestamp DESC")
    rows = cursor.fetchall()

    now = datetime.now(timezone.utc)
    categories = {
        "keep_recent": [],
        "keep_training": [],
        "archive_candidate": [],
        "purge_candidate": []
    }

    # Fast classification loop
    for (ts,) in rows:
        category = classify_heartbeat_age(ts, now)
        categories[category].append(ts)

    conn.close()

    # Generate output
    return {
        "scan_timestamp": now.isoformat(),
        "total_records_scanned": len(rows),
        "categories": {
            cat: {
                "count": len(records),
                "age_range_days": _get_age_range(cat),
                "disk_mb": len(records) * 0.06  # Rough estimate
            }
            for cat, records in categories.items()
        },
        "recommendation": "archive_and_vacuum" if len(categories["archive_candidate"]) > 500 else "no_action",
        "estimated_reclaim_mb": (len(categories["archive_candidate"]) + len(categories["purge_candidate"])) * 0.06,
        "confidence": 0.95
    }

def _get_age_range(category: str) -> str:
    ranges = {
        "keep_recent": "0-30",
        "keep_training": "30-90",
        "archive_candidate": "91-365",
        "purge_candidate": ">365"
    }
    return ranges[category]
```

## Performance Metrics

- **Scan speed**: 10,000 records/second (pure SQLite query)
- **Classification**: <1ms per record (simple age comparison)
- **Total execution**: <50ms for 3,719 records
- **Token cost**: 50-100 tokens (output generation only, no LLM inference)

## Pattern Memory Integration

Store execution results in `wre_core/recursive_improvement/metrics/telemetry_cleanup_metrics.jsonl`:

```json
{
  "skill": "gemma_telemetry_retention_detector",
  "timestamp": "2025-10-27T20:00:00Z",
  "execution_time_ms": 47,
  "records_scanned": 3719,
  "recommendation": "archive_and_vacuum",
  "estimated_reclaim_mb": 89,
  "pattern_fidelity": 0.95
}
```

## Next Phase

When `recommendation == "archive_and_vacuum"`, trigger:
- **Phase 2**: `qwen_telemetry_cleanup_strategist` - Strategic cleanup plan
- **Phase 3**: 0102 validation and execution

## Training Value

**Gemma learns**:
- Fast age-based classification patterns
- Binary decision thresholds (30/90/365 days)
- Disk usage estimation heuristics

**Pattern reuse**:
- Same logic applies to other telemetry tables
- Reusable for foundups_selenium telemetry
- Generic retention classifier for any time-series data
