---
name: dependency-audit
description: Manually collect dependency vulnerability evidence for DegenExus release gates and security reviews.
disable-model-invocation: true
when_to_use: Invoke explicitly when dependencies or manifests change, when `/ship` needs release evidence, or when `security-auditor` requests shell-based CVE evidence.
---

# Dependency Audit

Run from the repository root when dependencies changed or release evidence requires a vulnerability scan.

## Commands

```bash
pip-audit -r requirements.txt
python -m pip list --outdated
```

The outdated-dependency command is optional unless freshness is in scope.

## Output contract

- Tool version when available.
- Exact command and result.
- Critical/High vulnerabilities with package, installed version, fixed version, owner, and remediation note.
- Environment limitations if tooling is unavailable.
- Handoff note for `security-auditor` when it lacks shell access.
