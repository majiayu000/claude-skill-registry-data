---
license: Apache-2.0
name: skill-logger
description: Logs and scores skill usage quality, tracking output effectiveness, user satisfaction signals, and improvement opportunities. Expert in skill analytics, quality metrics, feedback loops, and continuous improvement. Activate on "skill logging", "skill quality", "skill analytics", "skill scoring", "skill performance", "skill metrics", "track skill usage", "skill improvement". NOT for creating skills (use agent-creator), skill documentation (use skill-coach), or runtime debugging (use debugger skills).
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
category: Productivity & Meta
tags:
  - logging
  - analytics
  - metrics
  - quality
  - improvement
pairs-with:
  - skill: automatic-stateful-prompt-improver
    reason: Data for prompt optimization
  - skill: skill-coach
    reason: Quality tracking feeds coaching
---

# Skill Logger

Track, measure, and improve skill quality through systematic logging and scoring.

## Decision Points

### Skill Category → Logging Signals Priority

```
Skill Category Analysis:
├─ Code Generation Skills
│  ├─ IF output type = "code" → Priority: syntax_correctness, test_pass_rate, user_edits
│  ├─ IF includes tool calls → Track: tool_success_rate, retry_count
│  └─ ELSE → Standard completion signals
│
├─ Analysis/Advisory Skills  
│  ├─ IF output is recommendations → Priority: follow_up_rate, acceptance_rate
│  ├─ IF research-heavy → Track: source_quality, comprehensiveness
│  └─ ELSE → Focus on user_satisfaction, edit_ratio
│
├─ Creative/Content Skills
│  ├─ IF artistic output → Priority: user_acceptance, revision_requests
│  ├─ IF writing/documentation → Track: readability_score, user_edits
│  └─ ELSE → Standard quality metrics
│
└─ Meta/System Skills
   ├─ IF affects other skills → Priority: downstream_impact, system_health
   ├─ IF automation focused → Track: execution_success, error_recovery
   └─ ELSE → Completion rate, efficiency metrics
```

### Quality Signal Collection Strategy

```
Signal Availability Decision Tree:
├─ Real-time signals available?
│  ├─ YES → Collect: completion_rate, token_efficiency, tool_success
│  └─ NO → Skip to delayed collection
│
├─ User interaction possible?
│  ├─ YES → Request: thumbs_up/down, edit_ratio measurement
│  └─ NO → Infer from: retry_requests, follow_up_questions
│
├─ Output testable?
│  ├─ Code → Run: syntax_check, basic_execution
│  ├─ Data → Validate: format_compliance, completeness
│  └─ Text → Check: length_appropriateness, structure
│
└─ Delayed validation available?
   ├─ YES → Schedule: outcome_tracking, revert_detection
   └─ NO → Mark as: immediate_signals_only
```

### Scoring Model Selection

```
Based on skill usage context:
IF high_stakes_usage (production, important decisions):
   → Use strict scoring: require 90+ for "good", weight errors heavily
   
ELIF experimental_usage (testing, learning):
   → Use lenient scoring: 70+ acceptable, focus on learning signals
   
ELIF routine_usage (daily workflow):
   → Use balanced scoring: standard thresholds, efficiency emphasis
   
ELSE (unknown context):
   → Default to balanced scoring with conservative error handling
```

## Failure Modes

### Token Inflation Anti-Pattern
**Symptoms**: Skill produces unnecessarily verbose outputs, token usage 2x+ expected baseline
**Detection**: `IF tokens_output > baseline_tokens * 2.0 AND user_edit_ratio > 0.6`
**Diagnosis**: Skill optimizing for completeness over conciseness
**Fix**: Add explicit length constraints, example-based training on concise outputs

### Metric Drift Anti-Pattern  
**Symptoms**: Skill quality scores trending downward without apparent cause changes
**Detection**: `IF quality_trend_7d < -5 AND no_skill_changes AND stable_usage_pattern`
**Diagnosis**: External factors (user expectations, data changes) affecting relative performance
**Fix**: Recalibrate baselines, investigate environmental changes, update scoring criteria

### Feedback Lag Anti-Pattern
**Symptoms**: Quality scores don't reflect actual user satisfaction, delayed negative signals
**Detection**: `IF immediate_score > 80 AND delayed_satisfaction < 50 AND lag > 24hrs`
**Diagnosis**: Relying too heavily on completion metrics vs. outcome metrics
**Fix**: Implement delayed signal collection, weight outcome signals higher, add follow-up tracking

### Grade Inflation Anti-Pattern
**Symptoms**: Most skills scoring 85+ but users reporting quality issues
**Detection**: `IF avg_skill_score > 85 AND user_complaints > baseline AND edit_ratio > 0.4`
**Diagnosis**: Scoring criteria too lenient, missing key quality dimensions
**Fix**: Tighten scoring thresholds, add user satisfaction weight, implement comparative scoring

### Signal Noise Anti-Pattern
**Symptoms**: Quality scores fluctuating wildly, no clear improvement signal
**Detection**: `IF score_variance > 20 AND no_clear_trend AND random_pattern`
**Diagnosis**: Collecting too many weak signals, insufficient signal filtering
**Fix**: Focus on top 3-5 signals per skill category, implement signal confidence weighting

## Worked Examples

### End-to-End: Code Generation Quality Regression

**Scenario**: The `api-architect` skill's quality score dropped from 89 to 67 over 3 days.

**Step 1 - Detect Regression**
```bash
# Query recent performance
SELECT skill_name, AVG(quality_score) as avg_score, COUNT(*) as uses
FROM skill_invocations 
WHERE skill_name = 'api-architect' 
  AND timestamp > datetime('now', '-7 days')
GROUP BY DATE(timestamp)
ORDER BY timestamp DESC;

# Result shows: 89→78→71→67 trend with stable usage (12-15 daily uses)
```

**Step 2 - Diagnose Cause**
```sql
-- Check error patterns
SELECT errors_json, COUNT(*) 
FROM skill_invocations 
WHERE skill_name = 'api-architect' 
  AND quality_score < 70
  AND timestamp > datetime('now', '-3 days');

-- Result: 8 instances of "Missing import statements" error
-- This is NEW - wasn't appearing before
```

**Step 3 - Analyze Specific Failures**
```python
# Examine failed invocations
failed_cases = get_low_score_invocations('api-architect', days=3)
for case in failed_cases:
    if 'import' in case.errors:
        # Pattern: Generated code missing required imports
        # User edit ratio: 0.7 (high - users adding imports)
        # Tool success rate: normal (tools work, output incomplete)
```

**Step 4 - Root Cause**
The skill was recently updated to use a more concise code style, but the import detection logic wasn't updated to handle the new patterns.

**Step 5 - Fix Implementation**
```python
# Add import detection rule to skill
IMPORT_PATTERNS = [
    r'from \w+',
    r'import \w+',
    r'require\(',
    r'#include'
]

def ensure_imports_present(code):
    # Check for usage of external functions/classes
    # Automatically add missing imports
```

**Step 6 - Validate Fix**
Monitor for 48 hours:
- Quality score recovery: 67→79→86
- Error rate: 35%→8%→2%  
- User edit ratio: 0.7→0.3→0.1

**Expert Insight**: The novice approach would be to just re-calibrate the scoring threshold. The expert approach recognizes that a sudden quality drop with stable usage indicates a systematic issue requiring root cause analysis and targeted fixes.

## Quality Gates

- [ ] Logging infrastructure captures all required signals for skill category
- [ ] Quality score calculation includes both immediate and delayed feedback
- [ ] Baseline performance metrics established for trending analysis
- [ ] Alert thresholds configured for quality drops >15% and error spikes >2x
- [ ] Anti-pattern detection rules active for token inflation and metric drift
- [ ] Quality data feeds into skill improvement recommendations
- [ ] User feedback collection mechanism functioning (>60% response rate)
- [ ] Data retention policy implemented (detailed logs 30 days, aggregates 1 year)
- [ ] Privacy compliance verified (no sensitive data in permanent logs)
- [ ] Integration points active with skill-coach and prompt-improver skills

## NOT-FOR Boundaries

**Do NOT use skill-logger for:**
- Creating new skills → Use `agent-creator` instead
- Writing skill documentation → Use `skill-coach` instead  
- Runtime debugging or error diagnosis → Use `debugger` or `error-analyst` skills
- General application logging → Use `devops-automator` for system logs
- User behavior analytics → Use dedicated analytics tools
- Real-time monitoring dashboards → Use `system-monitor` skill

**Delegate when:**
- Quality issues require skill redesign → Hand off to `skill-coach`
- Patterns suggest new skill needed → Escalate to `agent-creator`
- Performance problems are infrastructure-related → Route to `devops-automator`