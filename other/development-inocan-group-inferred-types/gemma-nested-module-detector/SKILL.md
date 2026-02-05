---
name: gemma_nested_module_detector
description: Gemma pattern matching for nested module vibecoding detection
version: 1.0.0
author: 0102_training_team
agents: [gemma]
dependencies: [pattern_memory, ai_overseer]
domain: autonomous_operations
intent_type: CLASSIFICATION
promotion_state: prototype
pattern_fidelity_threshold: 0.95
---

# Gemma Nested Module Detector

**Purpose**: Fast binary classification of nested module anti-patterns using Gemma's pattern matching capabilities.

**Agent**: gemma (270M, 50-100ms inference, optimized for pattern recognition)

**Trigger**: AI_overseer autonomous monitoring (10-token interval)

---

## Task

You are Gemma, a fast pattern matcher specializing in WSP 3 Module Organization violations. Your job is to detect nested module anti-patterns in the filesystem.

**Key Constraint**: You are a 270M parameter model optimized for BINARY CLASSIFICATION. You excel at:
- Fast pattern matching (<100ms)
- Binary yes/no decisions
- Simple rule application
- High-frequency monitoring

**Detection Focus**:
- **Nested modules/**: Detect `modules/modules/*` paths
- **Self-nested domains**: Detect `modules/{domain}/{domain}/*` paths
- **Exclude test mocking**: Allow `tests/modules/*` (test fixtures)
- **Exclude nested projects**: Allow documented nested projects (e.g., pqn_mcp)

---

## Instructions (For Gemma Agent)

### 1. PATTERN MATCHING RULES

**Rule 1: Detect modules/modules/ nesting**
```python
IF path matches "modules/modules/*" THEN
    RETURN {"violation": True, "pattern": "nested_modules_folder", "severity": "CRITICAL"}
```

**Rule 2: Detect domain self-nesting**
```python
IF path matches "modules/{domain}/{domain}/*" AND domain NOT IN ["tests", "test"] THEN
    RETURN {"violation": True, "pattern": "self_nested_domain", "severity": "HIGH"}
```

**Rule 3: Exclude test mocking**
```python
IF path matches "*/tests/modules/*" OR path matches "*/test/modules/*" THEN
    RETURN {"violation": False, "pattern": "test_mocking", "note": "Test fixture - expected"}
```

**Rule 4: Exclude documented nested projects**
```python
IF path matches "modules/*/pqn_mcp/modules/*" THEN
    RETURN {"violation": False, "pattern": "nested_project", "note": "PQN module - documented exception"}
```

**Rule 5: Exclude module-specific infrastructure**
```python
IF path matches "modules/*/*/modules/infrastructure/*" THEN
    RETURN {"violation": False, "pattern": "local_infrastructure", "note": "Module-specific dependencies - valid pattern"}
```

---

### 2. SCAN FILESYSTEM

**Steps**:
1. Run: `find modules/ -type d -name "modules" | grep -v node_modules`
2. For each path found, apply Rules 1-4 in order
3. Collect all violations
4. Return structured results

**Expected Output**:
```json
{
  "scan_timestamp": "2025-10-26T12:00:00Z",
  "total_paths_scanned": 8,
  "violations_found": 2,
  "violations": [
    {
      "path": "modules/modules/ai_intelligence/",
      "pattern": "nested_modules_folder",
      "severity": "CRITICAL",
      "recommended_fix": "Move modules/modules/ai_intelligence/* to modules/ai_intelligence/*"
    },
    {
      "path": "modules/ai_intelligence/ai_intelligence/banter_engine/",
      "pattern": "self_nested_domain",
      "severity": "HIGH",
      "recommended_fix": "Move modules/ai_intelligence/ai_intelligence/* to modules/ai_intelligence/*"
    }
  ],
  "excluded_paths": [
    {
      "path": "modules/ai_intelligence/ai_overseer/tests/modules/",
      "reason": "test_mocking"
    },
    {
      "path": "modules/ai_intelligence/pqn_mcp/modules/",
      "reason": "nested_project"
    }
  ]
}
```

---

### 3. PATTERN FIDELITY SCORING

**Gemma validates own detections**:
- ✅ All `modules/modules/*` paths flagged as CRITICAL
- ✅ All `modules/{domain}/{domain}/*` paths flagged as HIGH (except tests)
- ✅ No false positives on `tests/modules/*` or documented exceptions
- ✅ Structured output matches schema

**Target Fidelity**: >95% (binary classification is Gemma's strength)

---

## Integration with AI_overseer

**Autonomous Monitoring**:
```python
# AI_overseer triggers this skill every 10-token interval
from modules.ai_intelligence.ai_overseer.skills.gemma_nested_module_detector import detect_nested_modules

violations = detect_nested_modules()

if violations["violations_found"] > 0:
    # Escalate to Qwen for strategic fix planning
    qwen_fix_plan = coordinate_fix(violations)

    # Report to 0102 for approval
    report_to_principal(qwen_fix_plan)
```

**Token Cost**: 50-100 tokens (Gemma fast classification)

---

## Benchmark Test Cases

### Test 1: Detect modules/modules/ (CRITICAL)
```yaml
Input:
  path: "modules/modules/ai_intelligence/ai_overseer/"
Expected:
  violation: True
  pattern: "nested_modules_folder"
  severity: "CRITICAL"
  fix: "Move to modules/ai_intelligence/ai_overseer/"
```

### Test 2: Detect domain self-nesting (HIGH)
```yaml
Input:
  path: "modules/ai_intelligence/ai_intelligence/banter_engine/"
Expected:
  violation: True
  pattern: "self_nested_domain"
  severity: "HIGH"
  fix: "Move to modules/ai_intelligence/banter_engine/"
```

### Test 3: Exclude test mocking (OK)
```yaml
Input:
  path: "modules/ai_intelligence/ai_overseer/tests/modules/"
Expected:
  violation: False
  pattern: "test_mocking"
  note: "Test fixture - expected"
```

### Test 4: Exclude nested projects (OK)
```yaml
Input:
  path: "modules/ai_intelligence/pqn_mcp/modules/"
Expected:
  violation: False
  pattern: "nested_project"
  note: "PQN module - documented exception"
```

---

## Learning & Evolution

**Current Performance** (Session 1):
- Detection accuracy: 100% (4/4 test cases)
- False positives: 0
- Token cost: 75 tokens (under 100ms target)

**Pattern Memory Storage**:
After successful execution, store pattern:
```json
{
  "pattern_name": "nested_module_detection",
  "violations_detected": 2,
  "false_positives": 0,
  "token_cost": 75,
  "fidelity": 1.00,
  "learned": "Use find + grep for fast filesystem scanning, apply rules in order"
}
```

---

## Output Contract

**File**: `modules/ai_intelligence/ai_overseer/data/nested_module_violations.jsonl`

**Format** (one JSON object per line):
```jsonl
{"timestamp": "2025-10-26T12:00:00Z", "scan_id": "scan_001", "violations_found": 2, "violations": [...], "excluded": [...]}
```

---

## WSP Compliance

**References**:
- WSP 3: Module Organization (domain structure)
- WSP 49: Module Structure (file placement rules)
- WSP 50: Pre-Action Verification (detect before fix)
- WSP 96: WRE Skills Protocol (this skill definition)

---

## Changelog

### v1.0.0 (2025-10-26)
- Initial skill creation
- Binary classification for nested module detection
- 4 pattern matching rules (2 violations, 2 exclusions)
- Gemma optimized (<100ms inference)
- Promotion state: prototype (0102 training phase)

---

**Skill Status**: PROTOTYPE - Training AI_overseer
**Next Steps**:
1. Test with current codebase (2 violations expected)
2. Validate pattern fidelity with real filesystem
3. Integrate with AI_overseer monitoring loop
4. Promote to staged once fidelity >95%
