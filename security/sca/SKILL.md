---
name: sca
description: "Expert routing agent for Software Composition Analysis (SCA). Covers open source vulnerability management, CVE/CVSS scoring, license compliance, SBOM generation, reachability analysis, and dependency update automation. Routes to Snyk OSS, Dependabot, Mend, and Black Duck. WHEN: \"SCA\", \"software composition analysis\", \"open source vulnerabilities\", \"dependency scanning\", \"CVE\", \"SBOM\", \"license compliance\", \"supply chain security\", \"transitive dependencies\", \"dependency updates\". Do NOT use for tool-specific questions -- use the `snyk-oss`, `dependabot`, `mend`, or `black-duck` skill."
license: MIT
---

# Software Composition Analysis (SCA)

This skill covers Software Composition Analysis — identifying and managing vulnerabilities and license risks in open-source and third-party dependencies.

## How to Approach Tasks

1. **Identify the tool** -- Read the relevant sibling skill when a tool is named.
2. **Identify the concern:**
   - **Vulnerability management** -- CVEs in dependencies, patch availability
   - **License compliance** -- Copyleft licenses, commercial restrictions
   - **SBOM** -- Software Bill of Materials generation and management
   - **Supply chain security** -- Package integrity, provenance, dependency confusion
   - **Automation** -- Auto-fix PRs, update management

## Tool Routing

| User mentions | Route to |
|---|---|
| Snyk, Snyk Open Source, Snyk OSS, snyk test | `snyk-oss` |
| Dependabot, dependabot.yml, GitHub security updates | `dependabot` |
| Mend, WhiteSource, Renovate, mend.io | `mend` |
| Black Duck, Synopsys, binary SCA, SOUP | `black-duck` |

## SCA Fundamentals

### Vulnerability Data Sources

SCA tools compare your dependencies against vulnerability databases:

| Database | Source | Notes |
|---|---|---|
| NVD (National Vulnerability Database) | NIST | Authoritative CVE database, US government |
| OSV (Open Source Vulnerabilities) | Google | Open, machine-readable, aggregates many sources |
| GitHub Advisory Database | GitHub | Includes private research, curated |
| Snyk Vulnerability DB | Snyk | Proprietary + curated, faster publication |
| OSS Index | Sonatype | Free lookup service |
| VulnDB | Risk Based Security | Commercial, broadest coverage |

**Coverage gaps:** NVD can lag weeks to months behind disclosure. Commercial databases (Snyk, Mend) publish vulnerabilities faster due to active research teams.

### CVSS Scoring

SCA tools use CVSS (Common Vulnerability Scoring System) to score severity:

**CVSS v3.1 Base Score components:**
- **Attack Vector (AV):** Network (highest risk) / Adjacent / Local / Physical
- **Attack Complexity (AC):** Low / High
- **Privileges Required (PR):** None / Low / High
- **User Interaction (UI):** None / Required
- **Scope (S):** Changed / Unchanged
- **Confidentiality (C):** High / Low / None
- **Integrity (I):** High / Low / None
- **Availability (A):** High / Low / None

**Score ranges:**
- Critical: 9.0-10.0
- High: 7.0-8.9
- Medium: 4.0-6.9
- Low: 0.1-3.9

**CVSS limitations:** Base score is context-free. Use Temporal score (exploit maturity, patch availability) and Environmental score (actual impact to your system) for prioritization.

### Transitive Dependencies

The majority of open-source vulnerabilities are in transitive (indirect) dependencies — packages your direct dependencies depend on.

```
Your app
├── express@4.18.0 (direct)
│   ├── path-to-regexp@0.1.7 ← Vulnerable (transitive)
│   └── body-parser@1.20.0
│       └── qs@6.10.0 ← Vulnerable (transitive)
└── lodash@4.17.21 (direct)
```

**Resolution strategies:**
1. **Upgrade direct dependency** (easiest) — if newer version of your direct dep ships a patched transitive dep
2. **Override transitive version** — `npm` resolutions field, `pip` direct pinning, Maven `dependencyManagement`
3. **Accept and track** — if no fixed version exists, document risk in SBOM

### License Compliance

Open-source licenses range from permissive to restrictive:

**Permissive (generally safe for commercial use):**
- MIT, BSD 2/3-Clause, Apache 2.0, ISC
- Requires: attribution in documentation

**Weak copyleft (file/component-level):**
- LGPL (v2, v3) — Dynamic linking typically permitted; static linking may trigger copyleft
- Mozilla MPL 2.0 — Copyleft only for modified files

**Strong copyleft (network use triggers):**
- GPL v2, GPL v3 — Distributing modified code requires opening source
- AGPL v3 — Using over a network may trigger open-source requirement (highest risk for SaaS)

**Commercial restrictions:**
- CC BY-NC — Non-commercial only
- Custom BUSL, SSPL — May restrict commercial use

**SCA license policy approach:**
1. Define an approved license list (MIT, Apache 2.0, BSD, ISC typically safe)
2. Define requires-legal-review list (LGPL, MPL)
3. Define blocked list (GPL, AGPL for proprietary software)
4. Configure SCA tool to fail CI on blocked licenses

### SBOM (Software Bill of Materials)

An SBOM is a machine-readable inventory of all software components in an application.

**Formats:**
- **SPDX (Software Package Data Exchange):** Linux Foundation standard, NIST recommended
- **CycloneDX:** OWASP standard, security-focused, widely supported
- **SWID Tags:** ISO standard, used in enterprise/government

**When SBOMs are required:**
- US Executive Order 14028 (2021): Federal agencies must require SBOMs from software vendors
- EU Cyber Resilience Act (2024+): Products with digital elements require SBOMs
- Medical devices (FDA guidance): SBOMs for medical device software
- Financial services: Increasing regulatory guidance

**Generating SBOMs:**

```bash
# CycloneDX for npm
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# CycloneDX for Maven
mvn org.cyclonedx:cyclonedx-maven-plugin:makeBom

# CycloneDX for Python
pip install cyclonedx-bom
cyclonedx-bom -r -o sbom.xml

# SPDX via syft (container + package scanning)
syft my-app:latest -o spdx-json > sbom.spdx.json
```

### Reachability Analysis

Standard SCA flags any CVE in any dependency you use. Reachability analysis asks: "Is the vulnerable code path actually invoked by your application?"

**Without reachability:** 200 total CVEs across all dependencies → 200 findings.

**With reachability:** 200 total CVEs → 15 reachable (your code actually calls the vulnerable function) → dramatically fewer actionable findings.

**Available in:** Snyk Open Source (for JavaScript, Java, Python), Semgrep Supply Chain, GitHub dependency review (for some ecosystems).

**Limitation:** Reachability requires static analysis of your code. It can still have false positives (paths that appear reachable but are guarded by runtime conditions).

### Supply Chain Security

**Dependency confusion attacks:**
- Attacker publishes malicious package with same name as internal package on public registry
- Build system pulls public package instead of internal one if not configured to prefer internal registry
- **Mitigation:** Use private registry with scope prefixes (`@company/`), configure `npm config set @company:registry https://internal-registry`, use lockfiles

**Typosquatting:**
- Malicious packages named similarly to popular packages (`lodash` → `1odash`)
- **Mitigation:** Verify exact package names; use SCA tools with typosquatting detection

**Compromised packages:**
- Legitimate packages taken over by malicious actors (event-stream, ua-parser-js incidents)
- **Mitigation:** Pin exact versions in lockfiles, monitor security advisories, evaluate package activity/maintainership before adoption

**Package integrity verification:**
```bash
# npm: enable package provenance verification
npm install --include=dev
# Check SIGSTORE signatures for packages with provenance

# pip: hash checking mode
pip install --require-hashes -r requirements.txt

# Maven: verify artifact checksums (done by default in secure repos)
```

### Remediation Prioritization

Not all CVEs need immediate action. Use a risk-based approach:

| Criteria | Weight | Assessment |
|---|---|---|
| CVSS score | High | Base + Temporal |
| Exploitability | Critical | Is there a public exploit? Is it weaponized? |
| Reachability | Critical | Is the vulnerable code path executed? |
| Fix available | High | Is there a patched version? |
| Upgrade effort | Medium | Major version change? Breaking changes? |
| Asset criticality | High | Production customer data vs. internal tool |

**Typical SLA guidelines:**
- Critical (CVSS 9+) + public exploit: 24-48 hours
- High (CVSS 7-9): 7 days
- Medium (CVSS 4-7): 30 days
- Low: Next sprint or dependency update cycle

### SCA in the Pipeline

**Developer workflow:**
1. `snyk test` / `npm audit` / `gradle dependencyCheckAnalyze` locally before commit
2. IDE plugins (Snyk, Mend Advise) for real-time alerts as dependencies are added

**CI pipeline:**
1. SCA scan on every PR (quick, 1-2 minutes)
2. Block merge on newly introduced exploitable CVEs
3. SCA scan on main branch merge (full report for security team)

**Dependency update automation:**
- Dependabot or Renovate runs daily/weekly
- Creates PRs for dependency updates
- Tests run on PR
- Auto-merge safe updates (patch versions, no security risk)
- Flag breaking changes (major versions) for manual review
