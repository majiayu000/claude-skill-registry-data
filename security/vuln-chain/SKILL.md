---
name: vuln-chain
description: Three-phase vulnerability chain analysis — parallel agents find individual weaknesses, then a synthesis step identifies which combinations escalate to critical impact. Inspired by Strix (usestrix/strix) "Graph of Agents" pentesting model.
origin: yana-ai — inspired by usestrix/strix (MIT)
license: MIT
version: 1.0.0
triggers:
  - /vuln-chain
  - vulnerability chain
  - vuln chain
  - chain analysis
  - pentest chain
  - chain vulnerabilities
  - security chain audit
---

# /vuln-chain

Three-phase security analysis that finds not just individual vulnerabilities — but **how they chain into critical impact**.

A single IDOR is medium severity. An IDOR + a missing rate limit + a leaked JWT = account takeover. That's what this skill finds.

## Usage

```
/vuln-chain                          → analyze current repo/codebase
/vuln-chain <path>                   → analyze specific directory or file
/vuln-chain <url>                    → analyze a web endpoint or API
/vuln-chain --quick                  → Phase 1 only (individual findings, no chain synthesis)
/vuln-chain --depth critical         → only report chains that reach critical severity
```

## When to Use

- Before merging a PR that touches auth, payments, or data access
- Auditing a new API surface you didn't write
- When individual scanners return "all clear" but something feels off
- After a dependency update in a security-sensitive path
- Preparing for a real penetration test engagement

## When NOT to Use

- Simple "does this code have XSS" — use `/code-review` or `security-reviewer` agent directly
- Production live exploit attempt — this is analysis only
- Static linting — use ESLint/Bandit instead

---

## Three Phases

### Phase 1 — Parallel Recon (4 agents in parallel)

Four specialized agents run simultaneously, each with a narrow lens:

| Agent | Focus | OWASP Coverage |
|-------|-------|----------------|
| **Surface Scout** | Entry points: routes, endpoints, inputs, file uploads | A1 Broken Access Control |
| **Auth Auditor** | Authentication & authorization: JWT, sessions, RBAC, OAuth flows | A2 Cryptographic Failures, A7 Auth Failures |
| **Data Flow Tracer** | How data moves: injection sinks, serialization, query building | A3 Injection, A8 Integrity Failures |
| **Config Inspector** | Environment, secrets, dependencies, headers, CORS, CSP | A5 Misconfiguration, A6 Vulnerable Components |

Each agent returns: `[finding_id, location, severity (Low/Med/High), description, evidence]`

### Phase 2 — Chain Synthesis (1 agent, reads all Phase 1 output)

The Chain Synthesizer receives all Phase 1 findings and answers:

> "Which of these findings, if combined, produce a higher-severity impact than any individual finding alone?"

It explicitly looks for:

```
Auth bypass + Data exposure       → Account takeover
SSRF + Cloud metadata endpoint    → Credential theft
IDOR + Mass assignment            → Privilege escalation
XSS + CSRF + Missing SameSite     → Session hijack
Insecure deserialization + RCE    → Full compromise
Path traversal + File write       → Backdoor installation
Open redirect + OAuth             → Token theft
```

Output per chain:
- **Chain path**: Finding A → Finding B → Impact
- **Combined severity**: what it becomes when chained
- **Exploitability**: how many steps an attacker needs
- **Proof-of-concept sketch**: what the attack would look like

### Phase 3 — Remediation Priority

Prioritized fix list sorted by:
1. Chains that reach Critical — fix before any deploy
2. Chains that reach High — fix this sprint
3. Individual High findings with no chain
4. Individual Medium/Low findings

Each fix includes: specific code location, recommended change, and a test to verify the fix.

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VULN CHAIN REPORT  ·  [target]  ·  [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHAINS FOUND: N critical / N high / N medium

── CHAIN #1  [CRITICAL] ──────────────────────────
  Path:   Finding #3 (IDOR) → Finding #7 (Mass assign) → Privilege escalation
  Impact: Any authenticated user can elevate to admin
  Steps:  2 (trivially exploitable)
  PoC:    PATCH /api/users/:id {"role":"admin"} with any valid session token
  Fix:    [file:line] Add ownership check before PATCH handler

── INDIVIDUAL FINDINGS ───────────────────────────
  #1 [High]   Missing rate limit on /api/auth/login  →  Brute force
  #2 [Medium] JWT HS256 with weak secret             →  Token forgery
  ...

── REMEDIATION QUEUE ─────────────────────────────
  BEFORE DEPLOY:  Chain #1, Chain #2
  THIS SPRINT:    Finding #1, #5
  BACKLOG:        Finding #2, #4, #8

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Execution Protocol

```
Step 1  Read target (codebase, URL, or path provided by user)
Step 2  Spawn 4 Phase 1 agents in PARALLEL — do not wait for one before starting others
Step 3  Collect all Phase 1 findings into a unified list
Step 4  Pass unified list to Chain Synthesizer (single agent, serial)
Step 5  Chain Synthesizer produces chain report + individual findings list
Step 6  Generate Remediation Queue sorted by combined severity
Step 7  Present full report in the output format above
```

**Never skip Phase 2 unless `--quick` flag is passed.** Individual findings without chain analysis miss the most critical compound risks.

---

## Anti-Fake-Pass Checks

```
❌ DO NOT report "no vulnerabilities found" without evidence from all 4 Phase 1 agents
❌ DO NOT mark a chain as Critical without stating the specific PoC attack path
❌ DO NOT list findings without file:line location references
❌ DO NOT skip Phase 2 chain synthesis (most important phase — where Strix's insight lives)
❌ DO NOT merge findings from different phases without labeling which phase found each
❌ DO NOT confuse "no chain" with "safe" — a single High finding still needs remediation
```

## Do NOT use for

- Writing actual exploits or malware (use authorized pentesting tools with explicit permission)
- Scanning systems you don't own (analysis only — on code/APIs you control)
- Replacing a real security audit for regulated industries (SOC 2, HIPAA, PCI DSS)
- See also: `security-reviewer` agent (per-file review), `agentshield-security-scanner` (pattern scanning)
