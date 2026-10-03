---
name: soc-triage-web
description: "Soc Triage Web."
domain: cybersecurity
---

|
| **High Likelihood (6-9)** | Medium | High | Critical |
| **Medium Likelihood (3-6)** | Low | Medium | High |
| **Low Likelihood (0-3)** | Note | Low | Medium |

## Triage Process

### Step 1: Categorize by OWASP Top 10

```python
OWASP_TOP_10_2021 = {
    "A01": "Broken Access Control",
    "A02": "Cryptographic Failures",
    "A03": "Injection",
    "A04": "Insecure Design",
    "A05": "Security Misconfiguration",
    "A06": "Vulnerable and Outdated Components",
    "A07": "Identification and Authentication Failures",
    "A08": "Software and Data Integrity Failures",
    "A09": "Security Logging and Monitoring Failures",
    "A10": "Server-Side Request Forgery",
}

CWE_TO_OWASP = {
    "CWE-79": "A03",   # XSS -> Injection
    "CWE-89": "A03",   # SQL Injection
    "CWE-78": "A03",   # OS Command Injection
    "CWE-352": "A01",  # CSRF -> Access Control
    "CWE-22": "A01",   # Path Traversal
    "CWE-200": "A02",  # Information Exposure
    "CWE-327": "A02",  # Weak Cryptography
    "CWE-287": "A07",  # Authentication Issues
    "CWE-918": "A10",  # SSRF
    "CWE-502": "A08",  # Deserialization
    "CWE-611": "A05",  # XXE -> Misconfiguration
}
```

### Step 2: Validate True vs False Positives

```python
def triage_finding(finding):
    """Classify finding as true_positive, false_positive, or needs_review."""
    fp_indicators = [
        "Content-Security-Policy header not set",  # Often informational
        "X-Content-Type-Options header missing",    # Low severity header
        "Cookie without SameSite attribute",        # Context dependent
    ]

    for indicator in fp_indicators:
        if indicator.lower() in finding.get("title", "").lower():
            if finding.get("severity", "").lower() in ("info", "low"):
                return "false_positive", "Common informational finding"

    # Check for confirmed exploitation evidence
    if finding.get("evidence") and finding.get("confidence", "").lower() == "certain":
        return "true_positive", "Scanner confirmed exploitation"

    # SAST findings need manual code review
    if finding.get("source") == "sast":
        if finding.get("cwe") in ["CWE-89", "CWE-78", "CWE-79"]:
            return "needs_review", "Injection finding requires manual code review"

    return "needs_review", "Requires manual validation"
```

### Step 3: Risk Score Calculation

```python
def calculate_risk_score(finding, app_context):
    """Calculate OWASP risk rating for a web application finding."""
    # Likelihood factors
    likelihood = {
        "skill_level": 6 if finding["cwe"] in ["CWE-89", "CWE-79"] else 4,
        "motive": 7,  # Financial gain
        "opportunity": 7 if finding.get("authenticated") == False else 4,
        "size": 9 if finding.get("internet_facing") else 4,
        "ease_of_discovery": 8 if finding.get("scanner_detected") else 5,
        "ease_of_exploit": 7 if finding.get("exploit_available") else 4,
        "awareness": 6,
        "intrusion_detection": 3 if app_context.get("waf_enabled") else 8,
    }

    # Impact factors
    impact = {
        "confidentiality": 9 if "data_exposure" in finding.get("tags", []) else 5,
        "integrity": 9 if finding["cwe"] in ["CWE-89", "CWE-78"] else 4,
        "availability": 7 if "dos" in finding.get("tags", []) else 2,
        "accountability": 3 if app_context.get("logging_enabled") else 7,
        "financial": 7 if app_context.get("processes_payments") else 3,
        "reputation": 6 if app_context.get("customer_facing") else 2,
        "compliance": 8 if app_context.get("pci_scope") else 3,
        "privacy": 9 if app_context.get("handles_pii") else 2,
    }

    likelihood_score = sum(likelihood.values()) / len(likelihood)
    impact_score = sum(impact.values()) / len(impact)
    risk_score = likelihood_score * impact_score

    if risk_score >= 42:
        risk_level = "Critical"
    elif risk_score >= 24:
        risk_level = "High"
    elif risk_score >= 12:
        risk_level = "Medium"
    elif risk_score >= 3:
        risk_level = "Low"
    else:
        risk_level = "Note"

    return {
        "likelihood_score": round(likelihood_score, 1),
        "impact_score": round(impact_score, 1),
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
    }
```

### Step 4: Generate Triage Report

```bash
# Process DAST/SAST results through triage pipeline
python3 scripts/process.py \
  --input zap_results.json \
  --format zap \
  --app-context app_config.json \
  --output triage_report.json
```

## Manual Validation Techniques

### SQL Injection Validation
```
# Test parameter with single quote
GET /search?q=test' HTTP/1.1

# Test with boolean-based payload
GET /search?q=test' AND 1=1-- HTTP/1.1
GET /search?q=test' AND 1=2-- HTTP/1.1

# Time-based verification
GET /search?q=test'; WAITFOR DELAY '0:0:5'-- HTTP/1.1
```

### XSS Validation
```
# Reflected XSS test
GET /search?q=<script>alert(document.domain)</script> HTTP/1.1

# Check if output is encoded
GET /search?q="><img src=x onerror=alert(1)> HTTP/1.1

# DOM-based XSS
GET /page#<img src=x onerror=alert(1)> HTTP/1.1
```

## References

- [OWASP Risk Rating Methodology](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)
- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [OWASP Testing Guide v4.2](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
