---
name: devsecops-lookup
description: Looks up OWASP DevSecOps Guideline phases, security tools, and pipeline checks. Returns tool configurations, CWE mappings, and integration patterns for CI/CD security. Use when user asks about "DevSecOps", "SAST", "DAST", "SCA", "container security", "IaC security", "secret detection", "gitleaks", "semgrep", "trivy", "pipeline security", "シークレット検出", "静的解析", "動的解析", "コンテナセキュリティ", "セキュリティゲート".
---

# DevSecOps Guideline Lookup

Reference for OWASP DevSecOps Guideline phases, tools, and security checks.

## Pipeline Phases

| Phase | Activity | Key Tools |
|-------|----------|-----------|
| Develop | Pre-commit checks, Secret detection | Gitleaks, TruffleHog, pre-commit |
| Build | SAST, SCA, Container, IaC | Semgrep, Trivy, Hadolint, tfsec |
| Test | DAST, API Security, IAST | OWASP ZAP, Nuclei, Postman |
| Deploy | Security Gates, Config validation | Policy-as-code, Admission controllers |
| Operate | Monitoring, Vulnerability management | CNAPP, SIEM, Pentesting |

## Lookup Workflow

1. **Identify the Query Type**:
   - Pipeline phase (develop, build, test, deploy, operate)
   - Tool name (gitleaks, semgrep, trivy, etc.)
   - Security activity (SAST, SCA, DAST, etc.)
   - CWE reference

2. **Search the Indexes**:
   ```bash
   # Phase lookup
   cat ${CLAUDE_PLUGIN_ROOT}/skills/devsecops-lookup/pipeline-phases-index.json | jq '.phases["build"]'

   # Tool lookup
   cat ${CLAUDE_PLUGIN_ROOT}/skills/devsecops-lookup/tools-index.json | jq '.tools["semgrep"]'

   # Search by keyword
   cat ${CLAUDE_PLUGIN_ROOT}/skills/devsecops-lookup/tools-index.json | jq '[.tools | to_entries[] | select(.value.keywords | map(ascii_downcase) | any(contains("sast")))]'

   # CWE to phase mapping
   cat ${CLAUDE_PLUGIN_ROOT}/skills/devsecops-lookup/pipeline-phases-index.json | jq '[.phases | to_entries[] | select(.value.cwes | any(contains("CWE-798")))]'
   ```

3. **Return Results** with:
   - What it does (summary)
   - Installation command
   - Usage example
   - CI/CD integration pattern
   - Official references

## Response Format

```markdown
### [Tool/Activity Name]

**Phase**: [develop|build|test|deploy|operate]
**Category**: [secret-detection|sast|sca|container|iac|dast|misconfig]

**What It Does**:
[1-2 sentence summary]

**Installation**:
\`\`\`bash
[install command]
\`\`\`

**Basic Usage**:
\`\`\`bash
[usage command]
\`\`\`

**CI/CD Integration** (GitHub Actions):
\`\`\`yaml
[workflow snippet]
\`\`\`

**CWE Coverage**: [list of CWEs]

**References**:
- [Tool URL]
- [OWASP DevSecOps Guideline URL]
```

## Quick Reference: Tools by Phase

### Develop (Pre-commit)
| Tool | Purpose | Install |
|------|---------|---------|
| Gitleaks | Secret detection | `brew install gitleaks` |
| pre-commit | Hook management | `pip install pre-commit` |
| detect-secrets | Secret patterns | `pip install detect-secrets` |

### Build (CI)
| Tool | Purpose | Install |
|------|---------|---------|
| Semgrep | SAST | `pip install semgrep` |
| Trivy | SCA + Container | `brew install trivy` |
| Hadolint | Dockerfile lint | `brew install hadolint` |
| tfsec | Terraform security | `brew install tfsec` |
| Checkov | IaC security | `pip install checkov` |

### Test (CD/Staging)
| Tool | Purpose | Install |
|------|---------|---------|
| OWASP ZAP | DAST | Docker |
| Nuclei | Vulnerability scanner | `go install nuclei` |

## Index Coverage

### pipeline-phases-index.json
- All DevSecOps pipeline phases
- Activities per phase
- Recommended tools
- CWE mappings
- OWASP DevSecOps Guideline references

### tools-index.json
- 15+ security tools
- Installation commands
- Usage patterns
- CI/CD integration examples
- Output format specifications

## Example Queries

**User**: "How do I scan for secrets in CI?"
**You**: Look up `gitleaks` in tools-index.json

**User**: "What's the build phase?"
**You**: Look up `build` in pipeline-phases-index.json

**User**: "Terraform security scanning?"
**You**: Look up `tfsec` or `checkov` in tools-index.json

**User**: "CWE-798 prevention?"
**You**: Search for CWE-798 in phases, return secret detection tools

## External Resources

- [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)
- [OWASP DevSecOps Guideline (Japanese)](https://coky-t.gitbook.io/owasp-devsecops-guideline-ja/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [NIST SSDF](https://csrc.nist.gov/Projects/ssdf)
