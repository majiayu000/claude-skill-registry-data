---
name: licensing-compliance
description: Audit project dependencies for license compliance, identify legal issues, verify compatibility between licenses, and generate compliance reports. Use when.
---

# Licensing Compliance Check

Audit project dependencies for license compliance, identify potential legal issues, ensure compatibility between licenses, and generate compliance reports for legal review. This skill helps prevent licensing violations that could result in legal liability.

## When to Use This Skill

Use this skill when you need to:

- Release open-source software publicly
- Meet corporate compliance requirements
- Add new dependencies to existing projects
- Prepare for legal review before distribution
- Conduct due diligence for mergers and acquisitions
- Contribute to projects with strict license policies
- Verify license compatibility with your project
- Generate NOTICE files for distribution

**Trigger phrases**: "license check", "license compliance", "legal review", "license audit", "GPL compatibility", "license report", "NOTICE file", "open source compliance"

## What This Skill Does

### Core Capabilities

- **License Inventory**: Catalog all dependency licenses
- **Compatibility Check**: Verify license compatibility
- **Risk Assessment**: Categorize licenses by risk level
- **Policy Enforcement**: Check against company license policy
- **Attribution Generation**: Create NOTICE files for distribution
- **CI/CD Integration**: Automate compliance checking
- **Compliance Reporting**: Generate detailed compliance reports

### License Categories

| Category | Risk Level | Examples | Typical Use |
|----------|------------|----------|-------------|
| Permissive | Low | MIT, BSD, Apache 2.0 | Commercial/Open Source |
| Weak Copyleft | Medium | LGPL, MPL, EPL | Dynamic linking only |
| Strong Copyleft | High | GPL, AGPL | Open source projects |
| Proprietary | Varies | Custom, Commercial | Requires negotiation |

## Prerequisites

- Access to project dependency manifests
- Understanding of common open-source licenses
- Company license policy (if applicable)
- Legal team contact (for complex cases)

## Instructions

### Step 1: Install License Scanning Tools

#### Python

```bash
# Install license checking tools
pip install pip-licenses          # Generate license list
pip install licensecheck          # Verify licenses
pip install license-expression    # Parse license expressions
pip install python-license-check  # Compliance checking

# Install enhanced tools
pip install pip-audit             # Security + license audit
pip install pipdeptree            # Dependency tree with licenses
```

#### JavaScript/TypeScript

```bash
# Install license checking tools
npm install -g license-checker    # Check licenses
npm install -g nlf                # Node License Finder
npm install -g legally            # Generate license reports
npm install -g license-report     # Detailed reports

# Install CI-friendly tools
npm install --save-dev license-checker-webpack-plugin
```

#### Java

```xml
<!-- Maven license plugin -->
<!-- Add to pom.xml: -->
<plugin>
  <groupId>org.codehaus.mojo</groupId>
  <artifactId>license-maven-plugin</artifactId>
  <version>2.2.0</version>
</plugin>
```

```bash
# Generate license report
mvn license:third-party-report
```

#### C#

```bash
# Using dotnet-project-licenses
dotnet tool install --global dotnet-project-licenses

dotnet-project-licenses -i . -o -u -f markdown > licenses.md
```

#### Go

```bash
# Install go-licenses
go install github.com/google/go-licenses@latest

# Generate license report
go-licenses report ./... --template=licenses.tpl > licenses.md

# Check specific license
go-licenses check ./...

# Save license files
go-licenses save ./... --save_path=licenses/
```

### Step 2: Generate License Inventory

#### Python

```bash
# Basic license list
pip-licenses --format=markdown --output-file=licenses.md

# Detailed JSON report
pip-licenses --format=json --with-urls --with-description > licenses.json

# Check specific formats
pip-licenses --format=csv --output-file=licenses.csv

# Example output:
# | Name          | Version | License                |
# |---------------|---------|------------------------|
# | requests      | 2.31.0  | Apache-2.0             |
# | numpy         | 1.24.0  | BSD-3-Clause           |
# | flask         | 3.0.0   | BSD-3-Clause           |
# | cryptography  | 41.0.0  | Apache-2.0 OR BSD-3-Clause |
```

#### JavaScript

```bash
# Generate license report
license-checker --json --out licenses.json

# Summary format
license-checker --summary

# CSV export
license-checker --csv --out licenses.csv

# Example output:
# ├─ express@4.18.2
# │  ├─ licenses: MIT
# │  ├─ repository: https://github.com/expressjs/express
# │  ├─ publisher: TJ Holowaychuk
# │  └─ licenseFile: node_modules/express/LICENSE
```

### Step 3: Categorize Licenses by Risk

```python
# license_analyzer.py
"""Categorize licenses by compliance risk level."""
from typing import Dict, List
import json

class LicenseAnalyzer:
    """Analyze and categorize software licenses."""

    # License categories
    PERMISSIVE = {
        'MIT', 'BSD-2-Clause', 'BSD-3-Clause', 'Apache-2.0',
        'ISC', 'Unlicense', 'WTFPL', 'CC0-1.0'
    }

    WEAK_COPYLEFT = {
        'LGPL-2.1', 'LGPL-3.0', 'MPL-2.0', 'EPL-1.0', 'EPL-2.0',
        'CDDL-1.0', 'CDDL-1.1', 'CPL-1.0'
    }

    STRONG_COPYLEFT = {
        'GPL-2.0', 'GPL-3.0', 'AGPL-3.0', 'CC-BY-SA-4.0'
    }

    PROPRIETARY = {
        'Commercial', 'Proprietary', 'Custom', 'UNLICENSED'
    }

    def __init__(self, inventory_file: str):
        """Initialize with license inventory."""
        with open(inventory_file, 'r') as f:
            self.inventory = json.load(f)

    def categorize_licenses(self) -> Dict[str, List]:
        """Categorize all licenses by type."""
        categories = {
            'permissive': [],
            'weak_copyleft': [],
            'strong_copyleft': [],
            'proprietary': [],
            'unknown': [],
            'multiple': []
        }

        for package, info in self.inventory.items():
            license_str = info.get('licenses', 'UNKNOWN')

            # Handle multiple licenses (e.g., "Apache-2.0 OR MIT")
            if ' OR ' in license_str or ' AND ' in license_str:
                categories['multiple'].append({
                    'package': package,
                    'licenses': license_str,
                    'version': info.get('version')
                })
                continue

            # Categorize single license
            if license_str in self.PERMISSIVE:
                categories['permissive'].append(package)
            elif license_str in self.WEAK_COPYLEFT:
                categories['weak_copyleft'].append(package)
            elif license_str in self.STRONG_COPYLEFT:
                categories['strong_copyleft'].append(package)
            elif license_str in self.PROPRIETARY:
                categories['proprietary'].append(package)
            else:
                categories['unknown'].append({
                    'package': package,
                    'license': license_str
                })

        return categories

    def check_compatibility(self, project_license: str) -> Dict:
        """
        Check if dependencies are compatible with project license.

        Compatibility rules:
        - Permissive (MIT, BSD, Apache) can use anything except strong copyleft
        - Weak copyleft (LGPL, MPL) can use permissive and weak copyleft
        - Strong copyleft (GPL) can use everything (but makes project GPL)
        """
        categories = self.categorize_licenses()
        issues = []

        if project_license in self.PERMISSIVE:
            # Check for strong copyleft dependencies
            if categories['strong_copyleft']:
                issues.append({
                    'severity': 'HIGH',
                    'issue': 'Strong copyleft dependencies incompatible with permissive license',
                    'packages': categories['strong_copyleft'],
                    'recommendation': 'Remove GPL/AGPL dependencies or change project license'
                })

        elif project_license in self.WEAK_COPYLEFT:
            # Can use permissive and weak copyleft, not strong copyleft
            if categories['strong_copyleft']:
                issues.append({
                    'severity': 'HIGH',
                    'issue': 'Strong copyleft dependencies force GPL licensing',
                    'packages': categories['strong_copyleft'],
                    'recommendation': 'Remove or replace with LGPL alternatives'
                })

        # Check for unknown licenses
        if categories['unknown']:
            issues.append({
                'severity': 'MEDIUM',
                'issue': 'Dependencies with unknown licenses',
                'packages': categories['unknown'],
                'recommendation': 'Manually verify these licenses'
            })

        return {
            'compatible': len(issues) == 0 or all(i['severity'] == 'INFO' for i in issues),
            'issues': issues,
            'summary': {
                'permissive': len(categories['permissive']),
                'weak_copyleft': len(categories['weak_copyleft']),
                'strong_copyleft': len(categories['strong_copyleft']),
                'unknown': len(categories['unknown'])
            }
        }
```

### Step 4: Define Company License Policy

```yaml
# license-policy.yml
# Company license compliance policy

project_license: MIT

allowed_licenses:
  # Permissive licenses - always allowed
  permissive:
    - MIT
    - BSD-2-Clause
    - BSD-3-Clause
    - Apache-2.0
    - ISC
    - Unlicense
    - CC0-1.0

  # Weak copyleft - allowed with conditions
  weak_copyleft:
    - LGPL-2.1
    - LGPL-3.0
    - MPL-2.0
    - EPL-2.0
    conditions: "Dynamic linking only, no modification of LGPL code"

denied_licenses:
  # Strong copyleft - not compatible with MIT
  - GPL-2.0
  - GPL-3.0
  - AGPL-3.0
  - CC-BY-SA-4.0
  # Proprietary/unclear licenses
  - Commercial
  - Proprietary
  - Custom
  - UNLICENSED

requires_review:
  # Licenses requiring legal review
  - Artistic-2.0
  - OFL-1.1
  - CC-BY-4.0
  - Zlib

exceptions:
  # Approved exceptions (with justification)
  - package: readline
    license: GPL-3.0
    justification: "Used only in development, not distributed"
    approved_by: "legal-team"
    approved_date: "2025-01-15"

notifications:
  # Who to notify for license issues
  legal_team: legal@company.com
  engineering: eng-leads@company.com
  compliance_officer: compliance@company.com
```

### Step 5: Automated Compliance Checking

```python
# check_compliance.py
"""Automated license compliance checking against policy."""
import json
import yaml
import sys
from typing import Dict, List

class ComplianceChecker:
    """Check licenses against company policy."""

    def __init__(self, policy_file: str, inventory_file: str):
        """Initialize checker with policy and inventory."""
        with open(policy_file, 'r') as f:
            self.policy = yaml.safe_load(f)

        with open(inventory_file, 'r') as f:
            self.inventory = json.load(f)

    def check_all_packages(self) -> Dict:
        """Check all packages against policy."""
        results = {
            'compliant': [],
            'violations': [],
            'requires_review': [],
            'exceptions': []
        }

        allowed = set(
            self.policy['allowed_licenses']['permissive'] +
            self.policy['allowed_licenses']['weak_copyleft']
        )
        denied = set(self.policy['denied_licenses'])
        review_required = set(self.policy['requires_review'])

        # Check for approved exceptions
        exceptions_map = {
            exc['package']: exc
            for exc in self.policy.get('exceptions', [])
        }

        for package, info in self.inventory.items():
            license_str = info.get('licenses', 'UNKNOWN')

            # Check if package has approved exception
            if package in exceptions_map:
                results['exceptions'].append({
                    'package': package,
                    'license': license_str,
                    'exception': exceptions_map[package]
                })
                continue

            # Check compliance
            if license_str in denied:
                results['violations'].append({
                    'package': package,
                    'version': info.get('version'),
                    'license': license_str,
                    'severity': 'HIGH',
                    'reason': 'Denied license used'
                })
            elif license_str in review_required:
                results['requires_review'].append({
                    'package': package,
                    'version': info.get('version'),
                    'license': license_str
                })
            elif license_str in allowed:
                results['compliant'].append(package)
            elif license_str == 'UNKNOWN':
                results['violations'].append({
                    'package': package,
                    'version': info.get('version'),
                    'license': license_str,
                    'severity': 'MEDIUM',
                    'reason': 'License not identified'
                })
            else:
                results['requires_review'].append({
                    'package': package,
                    'version': info.get('version'),
                    'license': license_str
                })

        return results

    def generate_report(self) -> str:
        """Generate compliance report."""
        results = self.check_all_packages()

        report = []
        report.append("="*60)
        report.append("LICENSE COMPLIANCE CHECK")
        report.append("="*60)
        report.append(f"\nProject License: {self.policy['project_license']}")
        report.append(f"Total Packages: {len(self.inventory)}")
        report.append(f"Compliant: {len(results['compliant'])}")
        report.append(f"Violations: {len(results['violations'])}")
        report.append(f"Requires Review: {len(results['requires_review'])}")
        report.append(f"Approved Exceptions: {len(results['exceptions'])}")

        if results['violations']:
            report.append("\n LICENSE VIOLATIONS:")
            for violation in results['violations']:
                report.append(f"\n  [{violation['severity']}] {violation['package']} v{violation['version']}")
                report.append(f"    License: {violation['license']}")
                report.append(f"    Reason: {violation['reason']}")

        if results['requires_review']:
            report.append("\n REQUIRES LEGAL REVIEW:")
            for item in results['requires_review']:
                report.append(f"  - {item['package']} v{item['version']} ({item['license']})")

        if results['exceptions']:
            report.append("\n APPROVED EXCEPTIONS:")
            for exc in results['exceptions']:
                report.append(f"  - {exc['package']} ({exc['license']})")
                report.append(f"    Justification: {exc['exception']['justification']}")

        # Compliance status
        if results['violations']:
            report.append("\n COMPLIANCE CHECK FAILED")
            report.append("\nAction Required:")
            report.append("1. Remove or replace packages with violations")
            report.append("2. Request exceptions from legal team")
            report.append(f"3. Contact: {self.policy['notifications']['legal_team']}")
        else:
            report.append("\n COMPLIANCE CHECK PASSED")

        return "\n".join(report)

    def fail_on_violations(self) -> bool:
        """Return True if there are violations (for CI/CD)."""
        results = self.check_all_packages()
        return len(results['violations']) > 0

# Usage
if __name__ == '__main__':
    checker = ComplianceChecker('license-policy.yml', 'licenses.json')
    print(checker.generate_report())

    # Exit with error code if violations found (for CI)
    if checker.fail_on_violations():
        sys.exit(1)
```

### Step 6: CI/CD Integration

#### GitHub Actions

```yaml
# .github/workflows/license-check.yml
name: License Compliance

on:
  pull_request:
    paths:
      - 'requirements.txt'
      - 'package.json'
      - 'pom.xml'
  schedule:
    - cron: '0 0 * * 0'  # Weekly check

jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install pip-licenses pyyaml
        pip install -r requirements.txt

    - name: Generate license report
      run: |
        pip-licenses --format=json --with-urls > licenses.json

    - name: Check compliance
      run: |
        python check_compliance.py

    - name: Upload license report
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: license-report
        path: |
          licenses.json
          compliance_report.json

    - name: Comment on PR
      if: failure() && github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: ' License compliance check failed. Please review the license report.'
          })
```

### Step 7: Generate License Notices

```python
# generate_notices.py
"""Generate license attribution notices for distribution."""
import json
from typing import Dict

class NoticeGenerator:
    """Generate third-party license notices."""

    def __init__(self, inventory_file: str):
        """Initialize with license inventory."""
        with open(inventory_file, 'r') as f:
            self.inventory = json.load(f)

    def generate_notice_file(self, output_file: str = 'NOTICE.txt'):
        """Generate NOTICE file for distribution."""
        lines = []

        lines.append("THIRD-PARTY SOFTWARE NOTICES AND INFORMATION")
        lines.append("=" * 60)
        lines.append("\nThis software incorporates components from the projects listed below.")
        lines.append("The original copyright notices and the licenses are provided below.\n")

        for package, info in sorted(self.inventory.items()):
            lines.append("\n" + "-" * 60)
            lines.append(f"Package: {package}")
            lines.append(f"Version: {info.get('version', 'unknown')}")
            lines.append(f"License: {info.get('licenses', 'UNKNOWN')}")

            if 'url' in info:
                lines.append(f"Homepage: {info['url']}")

            if 'licenseFile' in info:
                lines.append(f"\nLicense Text:")
                try:
                    with open(info['licenseFile'], 'r') as f:
                        license_text = f.read()
                        lines.append(license_text)
                except Exception as e:
                    lines.append(f"[License file could not be read: {e}]")

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"Generated {output_file}")
        print(f"  Included {len(self.inventory)} third-party components")

    def generate_html_attribution(self, output_file: str = 'licenses.html'):
        """Generate HTML page with license attributions."""
        html = [
            "<!DOCTYPE html>",
            "<html><head>",
            "<title>Third-Party Licenses</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 40px; }",
            "h1 { color: #333; }",
            ".package { margin: 20px 0; padding: 15px; border-left: 3px solid #007bff; background: #f8f9fa; }",
            ".package-name { font-size: 1.2em; font-weight: bold; }",
            "</style>",
            "</head><body>",
            "<h1>Third-Party Software Licenses</h1>"
        ]

        for package, info in sorted(self.inventory.items()):
            html.append(f'<div class="package">')
            html.append(f'  <div class="package-name">{package}</div>')
            html.append(f'  <div>Version: {info.get("version", "unknown")}</div>')
            html.append(f'  <div>License: {info.get("licenses", "UNKNOWN")}</div>')

            if 'url' in info:
                html.append(f'  <div>Homepage: <a href="{info["url"]}">{info["url"]}</a></div>')

            html.append('</div>')

        html.append("</body></html>")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html))

        print(f"Generated {output_file}")

# Usage
if __name__ == '__main__':
    generator = NoticeGenerator('licenses.json')
    generator.generate_notice_file('NOTICE.txt')
    generator.generate_html_attribution('licenses.html')
```

## License Compatibility Matrix

### Common License Compatibility

| Your License | MIT | BSD | Apache 2.0 | LGPL | GPL | AGPL |
|--------------|-----|-----|------------|------|-----|------|
| **MIT** | Yes | Yes | Yes | Yes* | No | No |
| **BSD** | Yes | Yes | Yes | Yes* | No | No |
| **Apache 2.0** | Yes | Yes | Yes | Yes* | No** | No |
| **LGPL** | Yes | Yes | Yes | Yes | No | No |
| **GPL** | Yes | Yes | Yes*** | Yes | Yes | No |
| **AGPL** | Yes | Yes | Yes*** | Yes | Yes | Yes |

**Notes**:
- *LGPL: Only via dynamic linking, not static linking
- **Apache 2.0 + GPL: Compatible with GPL 3.0, not GPL 2.0
- ***GPL can use Apache 2.0, but result must be GPL

### Actions for Incompatible Licenses

1. **Replace with Compatible Alternative**
   - Search for MIT/BSD/Apache licensed alternatives
   - Compare features and migration effort
   - Document migration plan

2. **Request Exception**
   - Document business justification
   - Get legal approval
   - Add to exceptions list with expiration

3. **Change Project License**
   - Evaluate impact on distribution
   - Get stakeholder approval
   - Update all license references

4. **Remove Functionality**
   - If dependency not critical
   - Implement alternative solution
   - Document removal reason

## Common Pitfalls and Solutions

### Pitfall 1: Ignoring Transitive Dependencies

**Problem**: Direct dependencies may be compliant, but their dependencies are not.

**Solution**: Always check entire dependency tree.

```bash
# Python
pipdeptree --json | python -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))"

# JavaScript
npm ls --all --json > deps-tree.json
```

### Pitfall 2: Assuming Compatibility

**Problem**: Developers assume all open-source licenses are compatible.

**Solution**: Use automated compatibility checking and maintain explicit policy.

### Pitfall 3: Missing Attribution

**Problem**: Using software without providing required attribution.

**Solution**: Generate and distribute NOTICE files with every release.

### Pitfall 4: Not Updating Regularly

**Problem**: License compliance checked once and forgotten.

**Solution**: Integrate into CI/CD and check on every dependency change.

## Quality Checklist

- [ ] All dependency licenses identified
- [ ] License compatibility verified with project license
- [ ] Company license policy defined and documented
- [ ] Automated compliance checking in CI/CD
- [ ] No high-risk violations present
- [ ] Unknown licenses manually reviewed
- [ ] NOTICE file generated for distribution
- [ ] HTML attribution page created (if web application)
- [ ] Legal team reviewed complex cases
- [ ] Exceptions documented with justification
- [ ] Regular audit schedule established

## Related Skills

- `dependency-security-audit` - Security vulnerability scanning
- `pre-commit-checklist` - Pre-commit validation
- `sbom-generation` - Software Bill of Materials

## Additional Resources

### License Databases
- [SPDX License List](https://spdx.org/licenses/)
- [ChooseALicense.com](https://choosealicense.com/)
- [TLDRLegal](https://tldrlegal.com/)

### Tools by Language
- **Python**: pip-licenses, licensecheck
- **JavaScript**: license-checker, licensee
- **Java**: license-maven-plugin
- **Go**: go-licenses
- **Multi-language**: FOSSology, ScanCode

### License Compatibility Resources
- [GPL Compatibility Matrix](https://www.gnu.org/licenses/gpl-faq.html#AllCompatibility)
- [Apache-GPLv3 Compatibility](https://www.apache.org/licenses/GPL-compatibility.html)
- [Open Source Initiative](https://opensource.org/licenses)

---

**Note**: This skill provides guidance but does not constitute legal advice. Consult with legal counsel for specific compliance questions.

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: SPDX License Standards, Open Source License Compliance Guidelines


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
