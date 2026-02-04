---
name: dependency-vetting
description: |
  Vet new package dependencies before installation. Triggers when adding packages
  via pip, npm, yarn, or similar package managers. Checks for typosquatting,
  known vulnerabilities, low adoption (potential supply chain risk), and package
  metadata anomalies.

  Use when:
  - User asks to install a new package
  - pip install, npm install, yarn add commands detected
  - requirements.txt or package.json modifications
  - User asks "is this package safe?"

  Blocks: Typosquats, critical vulnerabilities
  Warns: Low adoption, suspicious metadata
allowed-tools: Bash, Read, WebFetch
model: haiku
---

# Dependency Vetting Skill

## Purpose

Prevent supply chain attacks by vetting packages before installation:
- Detect typosquatting (e.g., `reqeusts` instead of `requests`)
- Check for known vulnerabilities (CVEs)
- Verify package legitimacy (download counts, age, maintainer)
- Warn on low adoption or suspicious patterns

---

## When to Trigger

Auto-trigger when detecting:
- `pip install <package>`
- `pip3 install <package>`
- `npm install <package>`
- `yarn add <package>`
- Modifications to `requirements.txt`, `package.json`, `pyproject.toml`

---

## Vetting Protocol

### Step 1: Parse Package Name

```bash
# Extract package name and version from command
# Examples:
#   pip install requests==2.28.0  → requests, 2.28.0
#   npm install lodash@4.17.21    → lodash, 4.17.21
#   pip install -r requirements.txt → parse file
```

### Step 2: Typosquatting Check

**Popular packages to check against:**

Python:
```
requests, numpy, pandas, flask, django, fastapi, pydantic,
sqlalchemy, pytest, black, mypy, ruff, httpx, aiohttp,
beautifulsoup4, pillow, scipy, matplotlib, tensorflow, torch
```

JavaScript:
```
react, vue, angular, express, lodash, axios, moment,
webpack, babel, eslint, prettier, typescript, jest, mocha,
next, gatsby, tailwindcss, styled-components
```

**Typosquatting detection:**
```python
def is_typosquat(package_name: str, known_packages: list[str]) -> tuple[bool, str]:
    """Check if package name is suspiciously similar to a known package."""
    import difflib

    for known in known_packages:
        # Exact match is fine
        if package_name == known:
            return False, ""

        # Check similarity ratio
        ratio = difflib.SequenceMatcher(None, package_name, known).ratio()
        if ratio > 0.85 and package_name != known:
            return True, f"Suspiciously similar to '{known}' (similarity: {ratio:.0%})"

        # Common typosquatting patterns
        patterns = [
            package_name.replace('-', ''),      # request vs requests
            package_name.replace('_', '-'),     # python_dateutil
            package_name + 's',                 # request → requests
            package_name[:-1] if len(package_name) > 3 else package_name,  # requests → request
        ]
        if known in patterns:
            return True, f"Possible typosquat of '{known}'"

    return False, ""
```

### Step 3: Package Existence Verification

**Python (PyPI):**
```bash
# Check if package exists
pip index versions $PACKAGE_NAME 2>&1

# Or use API
curl -s "https://pypi.org/pypi/$PACKAGE_NAME/json" | jq '.info'
```

**JavaScript (npm):**
```bash
npm view $PACKAGE_NAME --json 2>&1
```

**If package doesn't exist:** BLOCK - likely typo or malicious attempt

### Step 4: Metadata Analysis

Extract and analyze:
```json
{
  "name": "package-name",
  "version": "1.2.3",
  "author": "author-name",
  "maintainers": ["maintainer1", "maintainer2"],
  "downloads_last_month": 1500000,
  "first_published": "2015-03-15",
  "last_updated": "2024-01-10",
  "repository_url": "https://github.com/org/repo",
  "license": "MIT"
}
```

**Red flags:**
- ⚠️ Package < 6 months old with low downloads
- ⚠️ No repository URL
- ⚠️ Author name similar to popular package author
- ⚠️ Recently changed maintainer
- ⚠️ No license specified
- ⚠️ Unusual install scripts

### Step 5: Vulnerability Check

**Python:**
```bash
# Using pip-audit
pip-audit --requirement requirements.txt

# Or check specific package
pip-audit $PACKAGE_NAME
```

**JavaScript:**
```bash
# Using npm audit
npm audit --json

# Or check specific package
npm audit $PACKAGE_NAME
```

**Severity levels:**
- **Critical:** Known RCE, SQL injection, etc. → BLOCK
- **High:** Serious vulnerabilities → WARN (require acknowledgment)
- **Medium/Low:** → WARN (inform user)

---

## Decision Matrix

| Condition | Action | Message |
|-----------|--------|---------|
| Typosquat detected | **BLOCK** | "Package '$name' appears to be a typosquat of '$real'. Did you mean '$real'?" |
| Package doesn't exist | **BLOCK** | "Package '$name' not found. Check spelling." |
| Critical vulnerability | **BLOCK** | "Package has critical vulnerability CVE-XXXX. Use alternative or pin older version." |
| High vulnerability | **WARN** | "Package has high-severity vulnerability. Proceed with caution?" |
| Low downloads (<1000/month) | **WARN** | "Package has very low adoption. Verify it's legitimate." |
| New package (<3 months) | **WARN** | "Package is very new. Verify maintainer reputation." |
| No repository | **WARN** | "Package has no linked repository. Cannot verify source." |
| Clean | **ALLOW** | "Package vetted: [summary of checks passed]" |

---

## Output Format

```json
{
  "package": "requests",
  "version": "2.28.0",
  "verdict": "ALLOW | WARN | BLOCK",
  "reason": "Brief explanation",

  "checks": {
    "typosquatting": {"passed": true, "details": null},
    "exists": {"passed": true, "details": "Found on PyPI"},
    "vulnerabilities": {"passed": true, "details": "No known CVEs"},
    "adoption": {"passed": true, "details": "51M downloads/month"},
    "age": {"passed": true, "details": "First published 2011-02-14"},
    "repository": {"passed": true, "details": "https://github.com/psf/requests"}
  },

  "recommendation": "Safe to install" | "Review warnings before proceeding" | "Do not install"
}
```

---

## Example Interactions

**Typosquat blocked:**
```
User: pip install reqeusts

Skill output:
⛔ BLOCKED: Package 'reqeusts' appears to be a typosquat of 'requests'

Did you mean: pip install requests

This is a common supply chain attack vector. The legitimate package
is 'requests' (with correct spelling).
```

**Low adoption warning:**
```
User: pip install obscure-tool-xyz

Skill output:
⚠️ WARNING: Package 'obscure-tool-xyz' has low adoption

- Downloads last month: 47
- First published: 2024-11-01 (2 months ago)
- No linked repository

This package has very limited community validation.
Proceed with installation? [yes/no]
```

**Critical vulnerability blocked:**
```
User: pip install vulnerable-lib==1.0.0

Skill output:
⛔ BLOCKED: Package has critical vulnerability

CVE-2024-12345: Remote Code Execution
Affected versions: < 1.2.0
Fixed in: 1.2.0

Recommendation: pip install vulnerable-lib>=1.2.0
```

---

## Remember

- **Block typosquats aggressively** - These are almost always malicious
- **Warn on low adoption** - But allow if user confirms
- **Check vulnerabilities** - Critical = block, High = warn
- **Provide alternatives** - When blocking, suggest the correct package
- **Log all decisions** - For audit trail
