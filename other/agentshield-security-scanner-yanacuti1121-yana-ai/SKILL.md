---
name: agentshield-security-scanner
description: AI agent configuration security scanner — 102 rules across secrets, permissions, hooks, MCP servers, and agent definitions. Detects hardcoded secrets, permission misconfigurations, hook injection, MCP vulnerabilities, and prompt injection. Use before deploying any Claude Code/AI agent configuration.
license: MIT
source: https://github.com/affaan-m/agentshield
---

# AgentShield Security Scanner

102-rule scanner for Claude Code agent configurations, MCP servers, hooks, and agent definitions. Built at Claude Code Hackathon (Feb 2026).

**Trigger phrases:** "scan agent config", "agentshield", "audit .claude/", "check MCP security", "hook injection", "agent permission audit", "secrets in config", "agent security scan"

---

## When to Use

- Before merging any changes to `.claude/settings.json`, hooks, or MCP config
- After importing skills or agents from external repos
- CI gate on every PR touching agent configuration
- Before deploying to production Claude Code environment

---

## 5 Detection Categories (102 rules total)

### 1. Secrets (10 rules)

Detects: Anthropic keys (`sk-ant-*`), OpenAI (`sk-proj-*`), GitHub (`ghp_*`), AWS (`AKIA*`), Stripe, JWT tokens, private keys, DB connection strings, base64-obfuscated credentials.

```bash
# False positive filtering: env var refs ${VAR}, markdown fences, example contexts
```

### 2. Permissions (10 rules)

Detects:
- Wildcard allows: `Bash(*)`, `Write(*)`, `Edit(*)`
- Dangerous bypasses: `dangerously-skip-permissions`, `--no-verify`
- Destructive git: `push --force`, `reset --hard`, `clean -f`
- Sensitive paths: `/etc/`, `~/.ssh/`, `~/.aws/`
- Missing deny list entirely

### 3. Hooks (34 rules)

**Injection patterns (CRITICAL):**
- Variable interpolation in attacker-controllable context: `${file|command|content|input}`
- Shell injection: `sh -c` with variable expansion
- curl/wget interpolation (data exfiltration)

**HIGH:** reverse shells, SSH key manipulation, credential store access, log tampering

**MEDIUM:** silent error suppression (`2>/dev/null`), 3+ chained shell commands, env var mutations

### 4. MCP Server Security (23 rules)

Risk levels:
- CRITICAL: Shell/command execution servers
- HIGH: Filesystem, browser automation, database servers
- MEDIUM: Messaging services (Slack, Discord, email)

Checks:
- `npx -y` (auto-install without review)
- Unrestricted filesystem paths (`/`, `~`)
- `PATH`, `LD_PRELOAD`, `NODE_OPTIONS` overrides
- Unversioned npm packages, git URL deps

### 5. Agent Definitions (25 rules)

- Unrestricted tool combos: Bash + Write + Read = full system access
- Prompt injection patterns: "ignore previous instructions", role reassignment, jailbreak framing
- Hidden instructions: zero-width Unicode, bidirectional text, base64 obfuscation
- Supply chain: URL-based instruction loading, unsigned skill imports

---

## CLI Usage

```bash
# Install
npm install -g ecc-agentshield

# Scan current project
agentshield scan .

# Output formats
agentshield scan . --format json        # machine-readable
agentshield scan . --format sarif       # GitHub Code Scanning
agentshield scan . --format html        # executive report
agentshield scan . --format markdown    # PR comment

# Auto-fix safe findings
agentshield scan . --fix

# Deep Opus analysis (3-agent attacker/defender/auditor pipeline)
agentshield scan . --opus

# Supply chain verification (MCP package provenance)
agentshield scan . --supply-chain

# Generate secure baseline config
agentshield init

# Continuous monitoring
agentshield watch .
```

---

## Output Format

```json
{
  "findings": [{
    "id": "HOOK-INJECT-001",
    "severity": "critical",
    "category": "hooks",
    "title": "Shell injection via variable interpolation",
    "file": ".claude/hooks/pre-commit.sh",
    "line": 12,
    "runtimeConfidence": "active-runtime",
    "fix": {
      "description": "Quote the variable",
      "before": "eval $INPUT",
      "after": "eval \"$INPUT\"",
      "auto": false
    }
  }],
  "score": 72,
  "grade": "C",
  "summary": { "critical": 1, "high": 2, "medium": 4, "low": 1 }
}
```

Score 0–100, grade A–F based on finding counts.

---

## GitHub Actions Integration

```yaml
- uses: affaan-m/agentshield@v1
  with:
    path: "."
    format: "sarif"
    fail-on-findings: "true"
  permissions:
    contents: read
    security-events: write
```

---

## YAMTAM Integration

agentshield complements strix-scan.sh:

| Tool | Target | When |
|------|--------|------|
| `strix-scan.sh --mode rules` | YAMTAM rule files (*.ts, *.py, *.sh) | Every commit |
| `strix-scan.sh --mode experts` | Source code vulnerability research | Pre-release |
| `agentshield scan .` | Claude Code config, hooks, MCP, agents | Before any config change |

---

## Anti-Fake-Pass

```
❌ Skipping scan "because it's just a config change"
❌ Trusting auto-fix blindly — review before applying
❌ Not running --supply-chain when adding new MCP servers
❌ Ignoring MEDIUM findings — hook chaining can escalate
❌ One-time scan instead of CI gate
```
