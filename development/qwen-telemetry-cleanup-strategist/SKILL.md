---
name: qwen_telemetry_cleanup_strategist
description: Strategic planning for YouTube telemetry cleanup and archival
version: 1.0
author: 0102_wre_team
agents: [qwen]
dependencies: [gemma_telemetry_retention_detector]
domain: autonomous_operations
intent_type: DECISION
promotion_state: prototype
estimated_tokens: 200-500
execution_time_ms: 150-300
wsp_chain: [WSP_77, WSP_91, WSP_96, WSP_15]
---

# Qwen Telemetry Cleanup Strategist

**Purpose**: Strategic analysis and safe execution planning for YouTube DAE telemetry lifecycle management

**Architecture**: Phase 2 of Gemma→Qwen→0102 cleanup wardrobe pattern

## WSP Compliance

- **WSP 15**: Module Prioritization Scoring (MPS) for cleanup impact analysis
- **WSP 77**: Agent Coordination (receives Gemma classification, plans for 0102 execution)
- **WSP 91**: DAEMON Observability (cardiovascular telemetry health)
- **WSP 96**: WRE Skills Wardrobe (autonomous recursive improvement)

## Task Description

Analyze Gemma's retention classification and create a safe, prioritized cleanup execution plan with risk assessment and rollback strategy.

## Input Contract

Receives output from `gemma_telemetry_retention_detector`:

```json
{
  "gemma_scan": {
    "scan_timestamp": "2025-10-27T20:00:00Z",
    "total_records_scanned": 3719,
    "categories": {
      "keep_recent": {"count": 1200, "age_range_days": "0-30", "disk_mb": 45},
      "keep_training": {"count": 1500, "age_range_days": "30-90", "disk_mb": 95},
      "archive_candidate": {"count": 800, "age_range_days": "91-365", "disk_mb": 70},
      "purge_candidate": {"count": 219, "age_range_days": ">365", "disk_mb": 19}
    },
    "recommendation": "archive_and_vacuum",
    "estimated_reclaim_mb": 89
  },
  "execution_context": {
    "youtube_dae_active": false,
    "disk_usage_percent": 45,
    "last_cleanup": "2024-08-15T10:00:00Z"
  }
}
```

## Strategic Analysis Framework

### Step 1: Risk Assessment

**Analyze operational risk of cleanup**:

```python
risk_factors = {
    "youtube_dae_active": "HIGH" if active else "LOW",
    "concurrent_writes": "HIGH" if heartbeats_last_5min > 0 else "LOW",
    "data_age": "LOW" if all_records > 90_days else "MEDIUM",
    "disk_pressure": "HIGH" if disk_usage > 80 else "LOW"
}

overall_risk = calculate_mps_risk_score(risk_factors)
```

**WSP 15 MPS Scoring**:
```
Operational Risk Score =
  (youtube_dae_active ? 10 : 0) +
  (concurrent_writes ? 8 : 0) +
  (data_age_recent ? 6 : 0) +
  (disk_pressure ? 4 : 0)

Low Risk: 0-5 (proceed immediately)
Medium Risk: 6-12 (proceed with caution)
High Risk: 13+ (defer until safer window)
```

### Step 2: Retention Strategy Decision

**Analyze training value vs disk pressure**:

```python
training_value = {
    "keep_recent": 1.0,     # Critical - active monitoring
    "keep_training": 0.85,  # High - pattern learning
    "archive_candidate": 0.4, # Medium - historical reference
    "purge_candidate": 0.1   # Low - minimal value
}

# Apply MPS formula
mps_score = sum(
    count * training_value[category] * (1 - age_decay_factor)
    for category, count in gemma_scan["categories"].items()
)
```

**Decision Matrix**:

| Condition | Action | Reasoning |
|-----------|--------|-----------|
| Disk <50% + Training value HIGH | KEEP ALL | Training data more valuable than disk space |
| Disk >80% + Old records >1000 | ARCHIVE + VACUUM | Reclaim space urgently |
| YouTube DAE active | DEFER CLEANUP | Avoid interfering with live telemetry writes |
| Last cleanup >180 days | PROACTIVE CLEANUP | Prevent unbounded growth |

### Step 3: Execution Plan Generation

**Safe cleanup plan with rollback**:

```json
{
  "plan_id": "telemetry_cleanup_20251027_200000",
  "risk_assessment": {
    "overall_risk": "LOW",
    "mps_score": 6.2,
    "risk_factors": {
      "youtube_dae_active": "LOW",
      "concurrent_writes": "LOW",
      "data_age": "LOW",
      "disk_pressure": "LOW"
    }
  },
  "actions": [
    {
      "step": 1,
      "action": "export_archive_candidates",
      "target": "data/foundups.db::youtube_heartbeats",
      "filter": "timestamp < '2024-10-01T00:00:00Z'",
      "output": "data/telemetry_archive/youtube_heartbeats_2024_archive.jsonl",
      "estimated_records": 800,
      "estimated_size_mb": 70,
      "risk": "LOW",
      "rollback": "reimport from JSONL archive"
    },
    {
      "step": 2,
      "action": "delete_archived_records",
      "target": "data/foundups.db::youtube_heartbeats",
      "filter": "timestamp < '2024-10-01T00:00:00Z'",
      "estimated_records": 800,
      "risk": "MEDIUM",
      "safety_check": "verify archive file exists and is valid JSON"
    },
    {
      "step": 3,
      "action": "vacuum_database",
      "target": "data/foundups.db",
      "estimated_reclaim_mb": 70,
      "risk": "LOW",
      "note": "VACUUM reclaims disk space after DELETE"
    },
    {
      "step": 4,
      "action": "purge_old_records",
      "target": "data/foundups.db::youtube_heartbeats",
      "filter": "timestamp < '2023-10-27T00:00:00Z'",
      "estimated_records": 219,
      "estimated_reclaim_mb": 19,
      "risk": "LOW",
      "justification": "Records >1 year old have minimal training value"
    }
  ],
  "expected_outcomes": {
    "records_kept": 2700,
    "records_archived": 800,
    "records_purged": 219,
    "disk_reclaimed_mb": 89,
    "database_size_after_mb": 140
  },
  "rollback_strategy": {
    "archive_location": "data/telemetry_archive/youtube_heartbeats_2024_archive.jsonl",
    "reimport_command": "python scripts/reimport_telemetry_archive.py youtube_heartbeats_2024_archive.jsonl",
    "estimated_restore_time_minutes": 2
  },
  "execution_window": {
    "preferred": "YouTube DAE inactive",
    "defer_if": "heartbeats_last_5min > 0",
    "max_defer_hours": 24
  }
}
```

## Output Contract

```json
{
  "decision": "PROCEED_WITH_CLEANUP",
  "confidence": 0.92,
  "risk_assessment": {
    "overall_risk": "LOW",
    "mps_score": 6.2
  },
  "execution_plan": { ... },
  "reasoning": "Low operational risk (YouTube DAE inactive), disk usage healthy (45%), but proactive cleanup recommended (last cleanup 439 days ago). Archive 800 records (91-365 days old), purge 219 records (>365 days old), reclaim 89MB.",
  "alternatives_considered": [
    {
      "option": "KEEP_ALL",
      "pros": ["Maximize training data", "Zero risk"],
      "cons": ["Unbounded growth", "Database bloat"],
      "rejected_reason": "Last cleanup 439 days ago - proactive maintenance needed"
    },
    {
      "option": "PURGE_IMMEDIATELY",
      "pros": ["Maximum space reclaim"],
      "cons": ["Lose training data", "No rollback"],
      "rejected_reason": "Archive-first strategy safer and preserves training value"
    }
  ],
  "validation_required": true,
  "validation_criteria": [
    "0102 confirms archive export succeeded",
    "0102 verifies YouTube DAE inactive",
    "0102 approves risk assessment"
  ]
}
```

## Qwen Strategic Reasoning

**Training objectives**:

1. **Risk assessment accuracy** - Learn to identify unsafe cleanup windows
2. **MPS scoring calibration** - Balance training value vs disk pressure
3. **Execution ordering** - Safe sequence (export → verify → delete → vacuum)
4. **Rollback planning** - Always provide recovery path

**Pattern memory**:
- Store successful cleanup executions
- Track disk reclamation accuracy (estimated vs actual)
- Learn optimal cleanup intervals (prevent reactive cleanup)

## Integration with WRE

Qwen's decision triggers 0102 validation:

```python
if qwen_decision["decision"] == "PROCEED_WITH_CLEANUP":
    # Phase 3: 0102 validates and executes
    validation_result = wre_orchestrator.execute_skill(
        skill_name="0102_telemetry_cleanup_executor",
        input_context={
            "qwen_plan": qwen_decision["execution_plan"],
            "risk_assessment": qwen_decision["risk_assessment"]
        }
    )
```

## Performance Metrics

- **Strategic analysis**: 150-300ms (complex decision tree)
- **Token cost**: 200-500 tokens (LLM reasoning for risk assessment)
- **Pattern memory**: Store execution outcomes for recursive learning

## Next Phase

Trigger **Phase 3**: 0102 validation and safe execution with:
- Archive export verification
- Safe DELETE with WHERE clause validation
- VACUUM with lock management
- Rollback testing (optional dry-run)
