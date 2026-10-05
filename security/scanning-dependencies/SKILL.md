---
name: scanning-dependencies
description: Scan project dependencies for vulnerabilities, license issues, and supply chain risks. Use when auditing third-party packages or before releases.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
  argument-hint: [project-root]
  stability: stable
  content-hash: sha256:a9ff14d899f3ffba809dd64536fd8a9f2cdd04ce72a99cfa9890a2fd06daf95f
---

# Dependency Vulnerability Scan

**Scope**: $ARGUMENTS

## When to Use

- Pre-release dependency audit
- Investigating CVE advisories
- License compliance review
- Supply chain risk assessment

## Workflow

1. **Detect language ecosystem** from manifest files
2. **Run appropriate scanner** (see tool matrix)
3. **Check license compliance** against project policy
4. **Identify outdated packages** with known upgrade paths
5. **Assess supply chain risk** indicators
6. **Report findings** in structured format

## Language Tool Matrix

| Ecosystem | Manifest | Lock File | Scanner Command |
|-----------|----------|-----------|-----------------|
| Node.js | `package.json` | `package-lock.json` | `npm audit --json` |
| Python | `pyproject.toml` / `requirements.txt` | `uv.lock` / `requirements.txt` | `uv run --with pip-audit pip-audit --skip-editable --format=json` (runs in the project env — bare `uvx pip-audit` audits only its own tool env) |
| Rust | `Cargo.toml` | `Cargo.lock` | `cargo audit --json` |
| Go | `go.mod` | `go.sum` | `govulncheck ./...` |

## Vulnerability Scan Checklist

- [ ] Run ecosystem-specific audit tool
- [ ] Cross-reference findings with NVD/GitHub Advisory Database
- [ ] Check transitive (indirect) dependencies
- [ ] Verify fix versions are available
- [ ] Confirm no yanked/deprecated packages in use

## License Compliance Checklist

- [ ] Identify all dependency licenses
- [ ] Flag copyleft licenses (GPL, AGPL) in non-copyleft projects
- [ ] Flag unknown or missing license declarations
- [ ] Check for license compatibility with project license
- [ ] Document any license exceptions

## Outdated Dependencies

- [ ] List packages with available major updates
- [ ] List packages with available security patches
- [ ] Identify unmaintained packages (no release in 12+ months)
- [ ] Check for deprecated packages with recommended replacements

## Supply Chain Risk Indicators

- [ ] Low download count or recent ownership transfer
- [ ] Typosquatting potential (similar names to popular packages)
- [ ] Install scripts that execute arbitrary code
- [ ] Excessive permission requests
- [ ] Single-maintainer packages for critical functionality

## Output Format

### Vulnerability Table

| # | Package | Version | CVE | Severity | Fix Version | Direct/Transitive |
|---|---------|---------|-----|----------|-------------|-------------------|
| 1 | `lodash` | 4.17.20 | CVE-2021-23337 | High | 4.17.21 | Direct |
| 2 | `py-yaml` | 5.4.0 | CVE-2020-14343 | Critical | 5.4.1 | Transitive |

### License Summary

| License | Count | Packages | Compatible |
|---------|-------|----------|------------|
| MIT | 42 | ... | Yes |
| GPL-3.0 | 1 | `foo-lib` | Review |

### Risk Summary

- **Critical CVEs**: count requiring immediate action
- **High CVEs**: count to address before release
- **License conflicts**: count needing review
- **Unmaintained**: count packages with no recent activity
