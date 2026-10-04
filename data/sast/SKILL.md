---
name: sast
description: "Expert routing agent for Static Application Security Testing (SAST). Covers code scanning fundamentals, taint analysis, CI/CD integration patterns, and quality gate design. Routes to SonarQube, Checkmarx, Semgrep, Snyk Code, and Veracode. WHEN: \"SAST\", \"static analysis\", \"code scanning\", \"taint analysis\", \"security hotspot\", \"false positive tuning\", \"CI security gate\", \"IDE security plugin\", \"custom security rules\". Do NOT use for tool-specific questions -- use the `sonarqube`, `checkmarx`, `semgrep`, `snyk-code`, or `veracode` skill."
license: MIT
---

# Static Application Security Testing (SAST)

This skill covers Static Application Security Testing — analyzing source code, bytecode, or binaries for security vulnerabilities without executing the application. It provides both the theory and practical implementation of SAST across the major tools.

## How to Approach Tasks

1. **Identify the tool** -- Read the relevant sibling skill when a tool is named.
2. **Understand the goal** -- Finding vulnerabilities? Reducing false positives? CI/CD integration? Custom rules?
3. **Apply SAST-appropriate reasoning** -- SAST has inherent false positive rates; balance thoroughness vs. developer friction.
4. **Integrate with context** -- SAST findings mean more when mapped to OWASP Top 10 / CWE IDs and linked to remediation guidance.

## Tool Routing

| User mentions | Route to |
|---|---|
| SonarQube, SonarCloud, SonarLint, quality gate, quality profile | `sonarqube` |
| Checkmarx, CxOne, CxQL, KICS | `checkmarx` |
| Semgrep, semgrep rule, semgrep pattern, metavariable | `semgrep` |
| Snyk Code, DeepCode, Snyk SAST | `snyk-code` |
| Veracode, pipeline scan, policy scan, binary analysis | `veracode` |

## SAST Fundamentals

### How SAST Works

SAST tools parse source code into an intermediate representation (typically an AST — Abstract Syntax Tree) then apply analysis techniques:

**Pattern matching:** Regular expressions or AST patterns. Fast, low false-negative rate for known patterns, but high false-positive potential. Used by Semgrep.

**Taint analysis (data flow):** Tracks user-controlled data ("taint") from sources (HTTP parameters, file reads) through the program to sinks (SQL queries, shell execution, HTML output). Finds injection vulnerabilities. Used by all enterprise SAST tools.

**Control flow analysis:** Understands how code execution can reach a particular point. Used to determine reachability and reduce false positives.

**Type inference:** Understands variable types even in dynamically typed languages to reduce false positives.

**Inter-procedural analysis:** Tracks taint across function/method call boundaries. Computationally expensive but necessary for real application code.

### Source and Sink Taxonomy

**Sources** (user-controlled input):
- HTTP request parameters, headers, cookies, body
- File system reads of user-supplied paths
- Database reads of user-supplied data
- Environment variables in some contexts
- IPC / message queue data

**Sinks** (dangerous operations):
- SQL query construction → SQL injection
- Shell command execution → OS command injection
- HTML output rendering → XSS
- File path operations → path traversal
- URL fetching → SSRF
- Deserialization → insecure deserialization
- Log writing → log injection

**Sanitizers** (functions that break the taint chain):
- Parameterized queries / prepared statements
- Output encoding (HTML, URL, JavaScript)
- Input validation against allowlist
- Path canonicalization and allowlist check

### False Positive Management

SAST tools have inherent false positive rates. Enterprise tools (Checkmarx, Veracode) typically see 30-50% FP rates without tuning. Semgrep community rules can be higher.

**Tuning strategies:**
1. **Suppression annotations:** Mark false positives inline with tool-specific comments (`// NOSONAR`, `# nosec`, `// nosemgrep`)
2. **Path exclusions:** Exclude test files, generated code, vendor directories
3. **Custom rule tuning:** Narrow rule patterns to reduce noise
4. **Sanitizer registration:** Tell the tool which custom functions sanitize input
5. **Severity thresholds:** Gate CI on Critical/High only; Medium/Low as informational

**False positive vs. false negative tradeoff:**
- Security-focused: prefer fewer false negatives (miss fewer real issues), tolerate more false positives
- Developer-experience-focused: prefer fewer false positives, tolerate some missed issues
- Practical balance: tune to <20% FP rate for gated findings, keep informational findings for review

### CI/CD Integration Patterns

**PR/MR scanning (incremental):**
- Scan only changed files or new code
- Annotate the PR/MR with findings on the diff
- Block merge only on newly introduced findings (not pre-existing)
- Tools: SonarQube PR decoration, Semgrep `--baseline-commit`, Snyk Code PR checks

**Full scan (scheduled or release):**
- Complete codebase analysis
- Compare to baseline, track trends
- Input to security backlog
- Tools: all enterprise tools support full scan mode

**Quality gate pattern:**
```
PR opened
  → SAST scan (incremental, 2-5 min target)
  → Findings annotated on PR diff
  → Gate: any new Critical or High? → Block merge
  → Developer sees finding inline, fixes in same PR
  → Re-scan, gate passes
  → Merge allowed
```

### Language Coverage Considerations

| Category | Generally Well-Supported | Limited Support |
|---|---|---|
| Web backend | Java, C#, Python, JavaScript/TypeScript, PHP, Ruby, Go | Rust (improving), Kotlin (improving) |
| Mobile | Swift, Kotlin, Java Android | React Native, Flutter |
| Infrastructure | Terraform, CloudFormation, Kubernetes YAML | Pulumi, CDK |
| Compiled | C/C++, C# | Assembly, COBOL |

Check specific tool for language support before deployment — depth varies significantly (e.g., Java taint analysis is far more mature than Go taint analysis across most tools).

### SAST in the Security Program

**Maturity levels:**
- Level 1: Run SAST, review results manually, no gates
- Level 2: SAST in CI, gate on Critical, results tracked in backlog
- Level 3: SAST in IDE + CI + scheduled full scans, gated by severity, custom rules for org-specific patterns, metrics dashboarded
- Level 4: SAST integrated with threat model, custom rules per business logic, SLA-driven remediation, developer security champions

**Integration with other tools:**
- SAST + SCA: SAST finds code vulnerabilities, SCA finds library vulnerabilities. Both needed.
- SAST + DAST: SAST finds code paths, DAST validates runtime exploitability. Combine to reduce false positives.
- SAST + WAF: SAST finds XSS in code, WAF blocks XSS payloads at runtime. Not redundant — defense in depth.
