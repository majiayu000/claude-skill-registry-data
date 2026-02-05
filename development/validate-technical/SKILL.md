---
name: validate-technical
description: Technical validation of APIs and detection approaches. Use to verify registry APIs work and detection algorithms are viable.
---

# TECHNICAL VALIDATION — API & ALGORITHM VERIFICATION

> **Frequency**: Monthly or when APIs change
> **Purpose**: Ensure technical foundation is still valid
> **Action**: Verify APIs work, algorithms effective

---

## INVOCATION

```
/validate-technical          # Full validation
/validate-technical api      # API endpoints only
/validate-technical algo     # Algorithm effectiveness only
```

---

## VALIDATION PROTOCOL

### 1. Registry API Validation

#### PyPI API

```bash
# Test package metadata endpoint
curl -s "https://pypi.org/pypi/flask/json" | python -c "
import json, sys
data = json.load(sys.stdin)
print(f'Name: {data[\"info\"][\"name\"]}')
print(f'Version: {data[\"info\"][\"version\"]}')
print(f'Author: {data[\"info\"][\"author\"]}')
print(f'Downloads: Available via stats API')
print(f'Repository: {data[\"info\"].get(\"project_urls\", {}).get(\"Homepage\", \"N/A\")}')
print('STATUS: OK')
"

# Test non-existent package
curl -s -o /dev/null -w "%{http_code}" "https://pypi.org/pypi/definitely-not-real-pkg-xyz/json"
# Expected: 404

# Test rate limiting (make 10 rapid requests)
for i in {1..10}; do
  curl -s -o /dev/null -w "%{http_code} " "https://pypi.org/pypi/flask/json"
done
# Expected: All 200s (no rate limit for read-only)
```

#### npm Registry

```bash
# Test package metadata endpoint
curl -s "https://registry.npmjs.org/express" | python -c "
import json, sys
data = json.load(sys.stdin)
print(f'Name: {data[\"name\"]}')
print(f'Latest: {data[\"dist-tags\"][\"latest\"]}')
print(f'Repository: {data.get(\"repository\", {}).get(\"url\", \"N/A\")}')
print('STATUS: OK')
"

# Test non-existent package
curl -s -o /dev/null -w "%{http_code}" "https://registry.npmjs.org/definitely-not-real-pkg-xyz"
# Expected: 404
```

#### crates.io API

```bash
# Test package metadata endpoint
curl -s "https://crates.io/api/v1/crates/serde" -H "User-Agent: phantom-guard" | python -c "
import json, sys
data = json.load(sys.stdin)
crate = data['crate']
print(f'Name: {crate[\"name\"]}')
print(f'Downloads: {crate[\"downloads\"]}')
print(f'Repository: {crate.get(\"repository\", \"N/A\")}')
print('STATUS: OK')
"

# Test non-existent package
curl -s -o /dev/null -w "%{http_code}" "https://crates.io/api/v1/crates/definitely-not-real-xyz" -H "User-Agent: phantom-guard"
# Expected: 404
```

---

### 2. Detection Signal Validation

#### Signal: Package Age

```python
# Validate that new packages are detectable
from datetime import datetime, timedelta

# Test: Can we detect packages created recently?
# Known new package (find one from PyPI recently uploaded)
# Verify: created_date < 30 days ago = SUSPICIOUS

def test_package_age_signal():
    # Simulate package created yesterday
    created = datetime.now() - timedelta(days=1)
    assert is_suspicious_age(created) == True

    # Simulate package created 2 years ago
    created = datetime.now() - timedelta(days=730)
    assert is_suspicious_age(created) == False
```

#### Signal: Download Count

```python
# Validate download count thresholds
def test_download_signal():
    # Very low downloads = suspicious
    assert is_suspicious_downloads(10) == True
    assert is_suspicious_downloads(50) == True

    # High downloads = not suspicious
    assert is_suspicious_downloads(10000) == False
    assert is_suspicious_downloads(1000000) == False
```

#### Signal: Repository Link

```python
# Validate repository presence check
def test_repository_signal():
    # No repo = suspicious
    assert is_suspicious_no_repo(None) == True
    assert is_suspicious_no_repo("") == True

    # Has repo = not suspicious
    assert is_suspicious_no_repo("https://github.com/org/repo") == False
```

#### Signal: Hallucination Patterns

```python
# Validate pattern matching
HALLUCINATION_PATTERNS = [
    r"flask[-_].*[-_]helper",
    r"django[-_].*[-_]utils",
    r".*[-_]common[-_].*",
    r"py[-_]?[a-z]+[-_]?client",
]

def test_hallucination_patterns():
    # Should match
    assert matches_hallucination_pattern("flask-redis-helper") == True
    assert matches_hallucination_pattern("django-auth-utils") == True

    # Should not match
    assert matches_hallucination_pattern("flask") == False
    assert matches_hallucination_pattern("requests") == False
```

---

### 3. Algorithm Effectiveness Testing

#### False Positive Rate

```python
# Test against TOP 1000 PyPI packages
# None should be flagged as suspicious

TOP_PACKAGES = ["requests", "flask", "django", "numpy", "pandas", ...]

def test_false_positive_rate():
    false_positives = 0
    for package in TOP_PACKAGES:
        result = validate_package(package)
        if result.risk_score > 0.5:
            false_positives += 1
            print(f"FALSE POSITIVE: {package} scored {result.risk_score}")

    rate = false_positives / len(TOP_PACKAGES)
    assert rate < 0.05, f"False positive rate {rate:.2%} exceeds 5% target"
```

#### True Positive Rate

```python
# Test against known suspicious patterns
# All should be flagged

SUSPICIOUS_PATTERNS = [
    "flask-redis-helper",  # Classic hallucination pattern
    "django-common-utils",  # Common pattern
    "py-aws-client",  # AI tends to generate these
]

def test_true_positive_rate():
    true_positives = 0
    for package in SUSPICIOUS_PATTERNS:
        result = validate_package(package)
        if result.risk_score > 0.5:
            true_positives += 1
        else:
            print(f"MISS: {package} scored {result.risk_score}")

    rate = true_positives / len(SUSPICIOUS_PATTERNS)
    assert rate > 0.95, f"True positive rate {rate:.2%} below 95% target"
```

---

## VALIDATION REPORT TEMPLATE

```markdown
# Technical Validation Report — YYYY-MM-DD

## API Status

### PyPI
- Metadata endpoint: ✅ Working
- 404 handling: ✅ Working
- Rate limiting: ✅ Not hit
- Response time: Xms average

### npm
- Metadata endpoint: ✅ Working
- 404 handling: ✅ Working
- Response time: Xms average

### crates.io
- Metadata endpoint: ✅ Working
- User-Agent required: ✅ Handled
- Response time: Xms average

---

## Detection Signals

| Signal | Status | Notes |
|:-------|:-------|:------|
| Package age | ✅ Working | Threshold: 30 days |
| Download count | ✅ Working | Threshold: 100 |
| Repository link | ✅ Working | Binary check |
| Hallucination patterns | ✅ Working | X patterns |

---

## Algorithm Performance

| Metric | Target | Measured | Status |
|:-------|:-------|:---------|:-------|
| False Positive Rate | <5% | X% | ✅/❌ |
| True Positive Rate | >95% | X% | ✅/❌ |
| Detection Latency | <200ms | Xms | ✅/❌ |

---

## Issues Found

### Critical
- [None]

### Warning
- [List any degraded signals]

### Info
- [List any observations]

---

## Recommendations

1. [Recommendation based on findings]
2. [Recommendation based on findings]

---

## Next Validation

Date: [Next month date]
```

---

## RESPONSE TO FAILURES

### API Endpoint Changed

```
1. Document the change
2. Update client code
3. Re-run validation
4. Update tests
```

### API Rate Limited

```
1. Implement backoff strategy
2. Add caching layer
3. Consider API key if available
4. Document rate limits
```

### Detection Accuracy Degraded

```
1. Analyze false positives/negatives
2. Adjust thresholds
3. Update pattern database
4. Re-validate with new settings
```

---

## TECHNICAL DEBT TRACKING

Record any technical issues:

```markdown
# .fortress/reports/technical/TECH_DEBT.md

| Date | Issue | Impact | Resolution |
|:-----|:------|:-------|:-----------|
| YYYY-MM-DD | [Issue] | [Impact] | [Status] |
```

---

*Technical Validation: Because assumptions rot faster than code.*
