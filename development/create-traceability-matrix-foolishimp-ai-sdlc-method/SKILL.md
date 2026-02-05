---
name: create-traceability-matrix
description: Create traceability matrix mapping intents (INT-*) to requirements (REQ-*) and requirements to all downstream artifacts (design, code, tests, commits, runtime). Use to visualize and verify complete traceability.
allowed-tools: [Read, Write, Grep, Glob, Bash]
---

# create-traceability-matrix

**Skill Type**: Sensor/Reporter (Traceability Management)
**Purpose**: Create and maintain traceability matrix for impact analysis
**Prerequisites**: Requirements and intents exist

---

## Agent Instructions

You are creating a **traceability matrix** showing the complete lineage from intent → runtime.

**Matrix maps**:
- Intent (INT-*) → Requirements (REQ-*)
- Requirements (REQ-*) → Design, Code, Tests, Commits, Runtime

**Purpose**: Impact analysis, coverage verification, compliance auditing

---

## Matrix Structure

### Full Traceability Matrix

| INT-* | REQ-* | Design | Code | Tests | Commits | Runtime | Status |
|-------|-------|--------|------|-------|---------|---------|--------|
| INT-042 | <REQ-ID> | AuthService | login.py:23 | test_login.py:15 | 5 | Datadog ✅ | ✅ Complete |
| INT-042 | REQ-F-PORTAL-001 | PortalService | balance.py:12 | test_balance.py:8 | 3 | Datadog ✅ | ✅ Complete |
| INT-042 | REQ-F-PORTAL-002 | ProfileService | profile.py:45 | test_profile.py:22 | 2 | ❌ No metrics | ⚠️ Partial |
| INT-050 | REQ-NFR-PERF-001 | CacheLayer | cache.py:67 | test_cache.py:34 | 4 | Prometheus ✅ | ✅ Complete |

---

## Workflow

### Step 1: Collect Intent → Requirements Mapping

```bash
# Find all intents and their requirements
grep -rh "^# Intent:" docs/requirements/ | sort -u
grep -rh "^## REQ-" docs/requirements/ | sort -u
```

**Output format**:
```yaml
# docs/traceability/intent-to-requirements.yml

INT-042:
  title: "Customer self-service portal"
  date: "2025-11-20"
  status: "In Progress"
  requirements:
    - <REQ-ID>
    - <REQ-ID>
    - REQ-F-PORTAL-001
    - REQ-F-PORTAL-002
    - REQ-F-PORTAL-003
  count: 5
```

---

### Step 2: Collect Requirements → Design Mapping

```bash
# Find design documents mentioning requirements
grep -rn "REQ-" docs/design/ docs/adrs/
```

---

### Step 3: Collect Requirements → Code Mapping

```bash
# Find code implementing requirements
grep -rn "# Implements: REQ-" src/
```

---

### Step 4: Collect Requirements → Tests Mapping

```bash
# Find tests validating requirements
grep -rn "# Validates: REQ-" tests/ features/
```

---

### Step 5: Collect Requirements → Commits Mapping

```bash
# Find commits for each requirement
for req in $(grep -rho "REQ-[A-Z-]*-[0-9]*" docs/requirements/ | sort -u); do
  echo "$req:"
  git log --all --oneline --grep="$req"
done
```

---

### Step 6: Generate Matrix Document

**Create comprehensive matrix**:

```markdown
# Traceability Matrix

**Generated**: 2025-11-20 23:30:00
**Total Intents**: 12
**Total Requirements**: 42
**Coverage**: 86%

---

## Intent: INT-042 (Customer Self-Service Portal)

**Status**: 60% Complete (3/5 requirements implemented)

| REQ-* | Description | Design | Code | Tests | Commits | Runtime | Status |
|-------|-------------|--------|------|-------|---------|---------|--------|
| <REQ-ID> | User login | AuthService | ✅ login.py | ✅ test_login.py | ✅ 5 | ✅ Datadog | ✅ |
| <REQ-ID> | Password reset | EmailService | ✅ reset.py | ✅ test_reset.py | ✅ 3 | ⚠️ Partial | ⚠️ |
| REQ-F-PORTAL-001 | View balance | PortalService | ✅ balance.py | ✅ test_balance.py | ✅ 2 | ❌ None | ⚠️ |
| REQ-F-PORTAL-002 | Update profile | ProfileService | ❌ None | ❌ None | ❌ 0 | ❌ None | ❌ |
| REQ-F-PORTAL-003 | Download invoices | ❌ No design | ❌ None | ❌ None | ❌ 0 | ❌ None | ❌ |

**Summary**:
- Design: 80% (4/5)
- Code: 60% (3/5)
- Tests: 60% (3/5)
- Runtime: 40% (2/5)

---

## Intent: INT-050 (Performance Optimization)

**Status**: 100% Complete (2/2 requirements implemented)

| REQ-* | Description | Design | Code | Tests | Commits | Runtime | Status |
|-------|-------------|--------|------|-------|---------|---------|--------|
| REQ-NFR-PERF-001 | Login <500ms | CacheLayer | ✅ cache.py | ✅ test_cache.py | ✅ 4 | ✅ Prometheus | ✅ |
| REQ-NFR-PERF-002 | DB queries <100ms | QueryOptimizer | ✅ optimizer.py | ✅ test_optimizer.py | ✅ 3 | ✅ Datadog | ✅ |

**Summary**: All complete ✅
```

---

## Output Format

```
[TRACEABILITY MATRIX]

Generated: 2025-11-20 23:30:00

Total Intents: 12
Total Requirements: 42

Overall Coverage:
  Design: 95% (40/42) ✅
  Code: 86% (36/42) ⚠️
  Tests: 83% (35/42) ⚠️
  Commits: 86% (36/42) ⚠️
  Runtime: 24% (10/42) ❌

Coverage Gaps:

Requirements Without Code (6):
  - REQ-F-PROFILE-002
  - REQ-F-PORTAL-003
  - REQ-F-NOTIF-001
  - REQ-F-NOTIF-002
  - REQ-NFR-SCALE-001
  - REQ-DATA-LIN-001

Requirements Without Tests (7):
  - <REQ-ID> (has code, no tests)
  - REQ-F-CART-001 (has code, no tests)
  ... (5 more)

Requirements Without Runtime Telemetry (32):
  - Most requirements (needs telemetry setup)

Matrix Files Created:
  + docs/traceability/intent-to-requirements.yml
  + docs/traceability/requirements-matrix.md
  + docs/traceability/coverage-report.md

✅ Traceability Matrix Created!
```

---

## Notes

**Why traceability matrix?**
- **Impact analysis**: Know what breaks if requirement changes
- **Coverage verification**: Ensure all requirements implemented and tested
- **Compliance auditing**: Prove requirements → code → tests → runtime
- **Gap detection**: Find requirements without coverage

**Homeostasis Goal**:
```yaml
desired_state:
  traceability_complete: true
  all_stages_covered: true
  coverage_percentage: >= 80%
```

**"Excellence or nothing"** 🔥
