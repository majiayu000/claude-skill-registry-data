---
name: code-audit
description: "Use for authorized source-code security review and SAST workflows including Semgrep, CodeQL patterns, dangerous API hunting, and fix verification."
version: 1.0.0
license: MIT
metadata:
  package: unleash-skills
  author: NetVar1337/unleash
  category: reverse-skill
  upstream: https://github.com/zhaoxuya520/reverse-skill
---

> Bundled with Unleash skills pack. Upstream: https://github.com/zhaoxuya520/reverse-skill

# Source Code Security Audit

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read `../field-journal/precedent-pentest.md` or the code-audit authorization
2. `NOW`: confirm you have **source/repo access** (binary without source → switch to an RE skill)
3. `NOW`: clarify the language stack and scope (directories/services/PR diff)
4. `NEXT`: tool-index; semgrep etc.
5. `ACT`: threat-model sketch → automated scanning → manual verification

## Applicable Scenarios

- White-box auditing, PR/differential security review
- SAST with Semgrep / CodeQL / Bandit / gosec etc.
- Dangerous APIs, injection points, missing authz, crypto misuse
- Division of labor with `supply-chain-security/`: this skill focuses on **first-party code logic**; supply chain focuses on dependencies and pipelines

## Workflow

### 1. Scope and Threat Model

```text
□ Trust boundaries: user input, files, deserialization, SSRF, authz middleware
□ High-value assets: authentication, payments, admin panels, key handling
```

### 2. Automated Scanning

```bash
semgrep --config auto .
# or a project rule pack
semgrep --config p/owasp-top-ten .
```

### 3. Manual Verification (MUST)

```text
□ Every SAST hit: reachability? exploitability? false positive?
□ Authz: IDOR/broken access control, missing checks, broken multi-tenant isolation
□ Injection: SQL/command/template/LDAP
□ Crypto: hardcoded keys, ECB, custom crypto
```

### 4. Deliverables

```text
Finding: location + data flow + PoC + fix recommendation
Optional ATT&CK / CWE identifiers
```

## Toolchain

| Tool | Language/scenario |
|------|-----------|
| Semgrep | Fast multi-language rules |
| CodeQL | Deep data flow (GitHub) |
| Bandit | Python |
| gosec / staticcheck | Go |
| SpotBugs / FindSecBugs | Java |

## References

- `references/sast-review-checklist.md`
- `../supply-chain-security/` `../api-security/` `../llm-security/` (agent code)

## Routing Context

**Upstream**: MASTER R26  
**Role**: `ops/role-map.md` cae  
**Downstream**: dependency vulnerabilities → supply-chain; runtime validation → pentest-tools

## Task Completion Self-Check

- [ ] Manually verified rather than just pasting scanner output?
- [ ] Fix recommendations included?
- [ ] Confined to the authorized repo scope?
- [ ] Checklist?
