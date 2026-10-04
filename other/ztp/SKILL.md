---
name: ZTP
description: A mandatory security audit skill for validating new code, skills, and MCP servers against the SEP-2026 Zero Trust protocol.
---

# openclaw-security

## Description

This skill enforces the **SEP-2026 Security Protocol**. It provides tools to audit source code for malicious patterns, obfuscation, and unauthorized network capability. It is the **Gatekeeper**; no external code (Skills, MCP Servers, Python scripts) should be integrated without passing this audit.

## Usage

Use this skill whenever you need to:

1.  **Audit** a new Python file, Skill, or MCP Server before using or installing it.
2.  **Verify** the safety of a downloaded script.
3.  **Check** for supply chain attacks (typosquatting).

## Commands

### 1. Deep Audit (Source Code)

Run the **Shield Pro 2.0** static analyzer on a target directory or file.

```bash
python3 skills/openclawSecurity/scripts/shield_pro.py --target <path_to_scan> --format json
```

**Output:** A JSON report containing `CRITICAL`, `HIGH`, and `MEDIUM` findings.
**Action:**

- If `CRITICAL` or `HIGH` > 0: **REJECT** the code.
- If `MEDIUM` > 0: **HALT** and ask User for manual review.

### 2. Supply Chain Check

Check `requirements.txt` or `package.json` for typosquatting and version pinning issues.

```bash
python3 skills/openclawSecurity/scripts/shield_pro.py --target <path_to_requirements> --mode supply-chain
```

### 3. Layer 2: External Defense Arsenal (Recommended)

If available in the environment, the Agent MUST run these SOTA tools to augment Shield Pro's findings:

| Tool          | Purpose                                         | Command                                         |
| :------------ | :---------------------------------------------- | :---------------------------------------------- |
| **Bandit**    | Python Static Analysis (Common Vulnerabilities) | `bandit -r <target_dir> -f json`                |
| **Safety**    | Python Dependency Check (Known CVEs)            | `safety check -r requirements.txt --json`       |
| **NPM Audit** | Node.js Dependency Check                        | `npm audit --json` (in package dir)             |
| **Trivy**     | Filesystem/Container Scan (Secrets/Vulns)       | `trivy fs <target_dir> --format json`           |
| **Garak**     | LLM/Prompt Injection Testing                    | `garak --model_type <type> --model_name <name>` |

> **Note:** If a tool is missing, log a warning in the final report but proceed with `shield_pro` findings.

## Workflow: The SEP-2026 Gatekeeper Process

1.  **Acquire**: Download or locate the target code.
2.  **Isolate**: ensure the code is not executed.
3.  **Scan**: Run `shield_pro.py` on the target.
4.  **Evaluate**:
    - **Pass**: No Critical/High issues.
    - **Fail**: Any Critical/High issue found. Reporting potential Line of Code (LOC) and threat type.
5.  **Report**: Present the findings to the user.

## Principles

- **Zero Trust**: treat all input as malicious.
- **No Execution**: Never run the target code during the audit.
- **Paranoia**: False positives are better than missed malware.
