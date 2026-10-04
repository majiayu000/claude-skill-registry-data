---
name: sigil-scan
description: >
  Automated security auditing for AI agent code. Scans repos, packages, MCP
  servers, and installed skills for malicious patterns using eight-phase
  analysis: install hooks, dangerous code patterns, network exfiltration,
  credential access, obfuscation, provenance, prompt injection, and skill
  security. Use when: cloning repos, installing
  packages, reviewing MCP servers, auditing skills, scanning code before
  execution, or when asked to check if something is safe, audit code, scan
  for malware, review dependencies.
compatibility: Requires internet for initial setup only. All scanning is local and offline. Works on macOS (arm64/x64), Linux (x64), and WSL.
license: Apache-2.0
allowed-tools: Read Bash(bash:*)
metadata:
  author: nomarj
  version: "1.1.0"
  homepage: https://sigilsec.ai
---

# Sigil Security Scanner

Sigil provides eight-phase security analysis purpose-built for AI agent code. It detects install hooks, dangerous code patterns, network exfiltration, credential access, obfuscation, provenance issues, prompt injection attacks, and AI skill security threats.

All file paths in this document are relative to this skill's directory (the directory containing SKILL.md).

## When to Activate

Invoke this skill in ANY of these situations:

- Before cloning any repository with `git clone`
- Before installing any package with `pip install` or `npm install`
- When the user asks to "scan", "audit", "check", or "review" code
- When the user asks "is this safe?" or "is this malicious?"
- When reviewing MCP server configurations
- When the user mentions supply chain security, dependency auditing, or code safety
- When any unfamiliar repo, package, or skill is about to be used

## Setup

Before first use, verify the Sigil CLI binary is installed:

```bash
bash scripts/setup.sh
```

Parse the JSON stdout. On success: `{"installed": true, "version": "...", "path": "..."}`. On failure: `{"error": true, "message": "..."}`. If setup fails, present the error to the user and suggest manual installation: `brew install nomarj/tap/sigil`, `npm install -g @nomarj/sigil`, or `cargo install sigil-cli`.

## Core Scan

To scan any target, run:

```bash
bash scripts/scan.sh <target>
```

The `<target>` argument accepts:
- **Local path**: `/path/to/project` or `./src`
- **GitHub URL**: `https://github.com/owner/repo`
- **GitHub shorthand**: `owner/repo`
- **npm package**: `@scope/package` or `npm:package-name`
- **pip package**: `pip:package-name`
- **Any URL**: `https://example.com/file.py`

### Output Format

The script outputs a single JSON object to stdout:

```json
{
  "verdict": "HIGH RISK",
  "score": 37,
  "target": "github.com/someone/sketchy-mcp-server",
  "files_scanned": 142,
  "duration_ms": 85,
  "findings_count": 12,
  "phases": {
    "InstallHooks": { "findings": 2, "severity": "critical" },
    "CodePatterns": { "findings": 5, "severity": "high" },
    "NetworkExfil": { "findings": 1, "severity": "medium" },
    "Credentials": { "findings": 3, "severity": "high" },
    "Obfuscation": { "findings": 0, "severity": "clean" },
    "Provenance": { "findings": 1, "severity": "low" },
    "PromptInjection": { "findings": 0, "severity": "clean" },
    "SkillSecurity": { "findings": 0, "severity": "clean" }
  },
  "findings": [
    {
      "phase": "InstallHooks",
      "severity": "Critical",
      "weight": 10,
      "rule": "INSTALL-003",
      "file": "package.json",
      "line": 8,
      "snippet": "postinstall script detected: node malicious.js"
    }
  ]
}
```

### Interpreting Results

**Always present the verdict prominently to the user.**

| Verdict | Score | Action |
|---------|-------|--------|
| `LOW RISK` or `CLEAN` | 0-9 | Proceed. Note that low risk does not mean zero risk. Inform the user of the result. |
| `MEDIUM RISK` | 10-24 | Show findings to the user. Ask for explicit approval before proceeding with any installation or execution. |
| `HIGH RISK` | 25-49 | Show detailed findings. Recommend rejection. Do NOT proceed without explicit user approval. |
| `CRITICAL RISK` or `CRITICAL` | 50+ | Show all findings prominently. Strongly recommend rejection. Never auto-proceed. |

Verdict strings vary slightly between CLI versions (`CLEAN` vs `LOW RISK`, `CRITICAL` vs `CRITICAL RISK`) — treat the pairs as equivalent. A `CRITICAL` verdict can also occur below score 50: any Critical-severity finding in the InstallHooks phase escalates the verdict immediately, because install hooks execute before the user can review the code.

### Presenting Findings

When presenting findings to the user:
1. Group findings by phase (Install Hooks first — they are the most dangerous)
2. Show the severity, rule ID, file path with line number, and description for each finding
3. Highlight any `Critical` severity findings in the `InstallHooks` phase — these indicate code that runs automatically during installation
4. For reference on what each rule detects, read `references/PHASES.md`
5. For details on how scoring works, read `references/SCORING.md`

### Exit Codes

- `0`: LOW RISK / CLEAN (score 0-9)
- Non-zero: MEDIUM RISK or higher

## Environment Audit

To scan the developer's local environment for exposed credentials:

```bash
bash scripts/audit-env.sh
```

This checks:
- `.env` files in the current project for exposed API keys, secrets, and tokens
- Home directory credential files (`~/.aws/credentials`, `~/.ssh/id_rsa`, `~/.kube/config`, etc.) for insecure permissions
- Shell history files for accidentally leaked secrets
- Agent-accessible directories for credential files

Present all findings to the user. Flag any `critical` severity items prominently.

## Installed Skills Audit

To scan all installed skills across all agent directories:

```bash
bash scripts/audit-skills.sh
```

This enumerates skills in: `~/.agents/skills/`, `~/.claude/skills/`, `~/.cursor/skills/`, `~/.roo/skills/`, `~/.codex/skills/`, and other agent paths. Each skill is scanned and assigned a risk verdict.

Present the results as a summary table showing each skill's name, agent, verdict, and score. Highlight any skills with `HIGH RISK` or `CRITICAL RISK` verdicts.

## Report Generation

To format scan results as a readable markdown report:

```bash
bash scripts/scan.sh <target> | bash scripts/report.sh
```

Or from a saved JSON file:

```bash
bash scripts/report.sh results.json
```

## Important Behavioural Rules

1. **Never describe code as "safe" or "malicious" in definitive terms.** Use "low risk", "elevated risk", "flagged patterns", or "detected patterns" instead.
2. **Always present the risk verdict and score** before any other commentary.
3. **When a scan returns HIGH RISK or CRITICAL RISK**, always show the detailed findings. Never summarise away critical findings.
4. **For CRITICAL RISK findings in the InstallHooks phase**, explicitly warn the user that install-time code execution was detected — this means code runs automatically when the package is installed, before the user can review it.
5. **Wait for explicit user approval** before proceeding with installation or execution of any target rated MEDIUM RISK or higher.
6. **Include the disclaimer** at the end of scan result presentations: "Sigil provides risk assessments based on automated pattern detection. Risk assessments do not constitute a guarantee of security or a definitive determination of malicious intent."

## Troubleshooting

If you encounter issues, read `references/TROUBLESHOOTING.md` for common solutions.
