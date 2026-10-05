---
name: skill-security-auditor-v2
description: Hybrid security auditor for OpenClaw skills, Claude/Codex skills, and app repos. Use when installing a new skill, auditing a repo before use or deploy, reviewing custom scripts, checking for prompt injection, command execution, data exfiltration, dependency risk, secrets exposure, or privilege escalation. Use as the default gatekeeper before installing any third-party skill.
---

# Skill Security Auditor v2

Run a hybrid security audit before installing a skill or deploying code. Return a clear **PASS / WARN / FAIL** verdict with concrete findings and remediation.

## Use

### Audit a local path

```bash
python3 scripts/security_auditor_v2.py /path/to/target
```

### Audit a git repo

```bash
python3 scripts/security_auditor_v2.py https://github.com/org/repo
```

### JSON output

```bash
python3 scripts/security_auditor_v2.py /path/to/target --json
```

### Strict mode

```bash
python3 scripts/security_auditor_v2.py /path/to/target --strict
```

## What it checks

1. **Command execution risk**
   - shell execution
   - eval/exec
   - dynamic imports
   - `child_process` / subprocess misuse

2. **Prompt injection risk**
   - instruction override attempts
   - role hijacking
   - safety bypass language
   - hidden directives

3. **Data exfiltration risk**
   - outbound network writes
   - credential harvesting patterns
   - suspicious file access

4. **Privilege and persistence risk**
   - `sudo`
   - cron modification
   - shell/profile tampering
   - dangerous permissions

5. **Filesystem safety**
   - writes outside expected scope
   - destructive deletes
   - symlinks
   - hidden sensitive files

6. **Dependency and secret risk**
   - suspicious install-at-runtime behavior
   - unpinned deps
   - likely secrets/tokens in repo

7. **Optional deep scanners if installed**
   - Semgrep
   - Bandit
   - Gitleaks
   - Trivy

## Output contract

Always return:

- **PASS**: no meaningful issues found
- **WARN**: review required, but likely safe after inspection
- **FAIL**: unsafe to install/use as-is

For each finding include:
- severity
- category
- file and line when possible
- why it matters
- how to fix it

## Hard rules

- Treat third-party skills as untrusted until scanned
- Never auto-approve a FAIL result
- For WARN, explain why it is likely safe or why manual review is needed
- Distinguish **live executable risk** from **documentation/examples**
- Prefer fewer high-confidence findings over noisy output

## Optional deeper tools

If available on the machine, the script will automatically use:
- `semgrep`
- `bandit`
- `gitleaks`
- `trivy`

If missing, the script still works with the native scanner only.

## References

- Read `references/risk-model.md` when tuning findings or reviewing gray-area cases.
