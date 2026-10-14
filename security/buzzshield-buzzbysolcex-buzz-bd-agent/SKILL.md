---
name: buzzshield
description: >
  Crypto-native security scanner for Claude Code agent configurations.
  Scans for exposed private keys, insecure RPC endpoints, contract addresses
  in public repos, unprotected wallet operations, and agent config vulnerabilities.
  Extends AgentShield concept with 47 crypto-specific detection rules.
  Run via /security-scan command.
tags: [security, crypto, audit, scanner, agent, wallet]
---

# BuzzShield — Crypto Agent Security Scanner

> 47 crypto-specific rules. Scans CLAUDE.md, .env, hooks, agents, skills.
> Built on lessons from building a $0/day LLM cost production agent.

## When to Use

- Before deploying any crypto agent to production
- After adding new MCP servers or API keys
- Before hackathon submissions (catch leaks)
- As part of HSaaS security audit ($500 tier includes BuzzShield report)
- Periodic security hygiene check

## What It Scans

### 1. Secret Detection (14 patterns)

| Pattern                                    | What It Catches               |
| ------------------------------------------ | ----------------------------- |
| `0x[a-fA-F0-9]{64}`                        | Private keys (EVM)            |
| `[1-9A-HJ-NP-Za-km-z]{87,88}`              | Private keys (Solana)         |
| `sk-[a-zA-Z0-9]{48}`                       | API keys (Anthropic, OpenAI)  |
| `ghp_[a-zA-Z0-9]{36}`                      | GitHub personal access tokens |
| `xoxb-[0-9]{11}-[0-9]{13}-[a-zA-Z0-9]{24}` | Slack bot tokens              |
| `AKIA[0-9A-Z]{16}`                         | AWS access keys               |
| `fc-[a-f0-9]{32}`                          | Firecrawl API keys            |
| Mnemonic phrases                           | 12/24 word seed phrases       |
| `.env` in git                              | Uncommitted env files tracked |
| Hardcoded RPC URLs with API keys           | Alchemy, Infura, QuickNode    |
| `Bearer [a-zA-Z0-9._-]+`                   | Auth tokens in code           |
| Server IPs in public files                 | Infrastructure exposure       |
| OAuth client secrets                       | Google, GitHub OAuth          |
| Telegram bot tokens                        | Bot token patterns            |

### 2. Wallet Safety (9 patterns)

| Check                                          | Risk Level |
| ---------------------------------------------- | ---------- |
| Unprotected transfer_tokens calls              | CRITICAL   |
| Missing approval gate on swap operations       | CRITICAL   |
| Auto-approve at trust level 0                  | HIGH       |
| Wallet drain patterns (approve + transferFrom) | CRITICAL   |
| Missing amount limits on transactions          | HIGH       |
| Contract deployment without gas estimation     | MEDIUM     |
| Missing honeypot check before interaction      | HIGH       |
| Unverified contract addresses hardcoded        | MEDIUM     |
| Missing receipt/audit trail for transactions   | MEDIUM     |

### 3. Agent Config Review (12 patterns)

| Check                                              | Risk Level |
| -------------------------------------------------- | ---------- |
| `--dangerously-skip-permissions` without allowFrom | CRITICAL   |
| Missing requireMention in group configs            | HIGH       |
| Overly broad tool access in agent definitions      | MEDIUM     |
| MCP servers without rate limiting                  | MEDIUM     |
| Feature flags all TRUE (no safety gates)           | MEDIUM     |
| Missing trust gate on outreach operations          | HIGH       |
| Crons without maxRuns/expiresAt (infinite growth)  | HIGH       |
| Event handlers with side effects (recursive risk)  | MEDIUM     |
| Missing circuit breakers on mailbox                | HIGH       |
| Unvalidated task DAG dependencies (deadlock risk)  | MEDIUM     |
| server.js modifications without backup             | HIGH       |
| Gmail OAuth without CC enforcement                 | MEDIUM     |

### 4. Contract Security (7 patterns)

| Check                                        | Risk Level |
| -------------------------------------------- | ---------- |
| Deployer wallet used as contract owner       | CRITICAL   |
| EIP-7702 delegated wallet as owner           | CRITICAL   |
| Missing ownership transfer capability        | HIGH       |
| Unverified contract source on block explorer | MEDIUM     |
| Missing reentrancy guards                    | CRITICAL   |
| Unchecked external calls                     | HIGH       |
| Missing event emission on state changes      | MEDIUM     |

### 5. Infrastructure (5 patterns)

| Check                             | Risk Level |
| --------------------------------- | ---------- |
| Server IP in public content       | CRITICAL   |
| SSH keys in repository            | CRITICAL   |
| Docker socket exposed             | HIGH       |
| Missing fail2ban or rate limiting | MEDIUM     |
| Unencrypted database connections  | MEDIUM     |

## Output Format

### Terminal (default)

```
╔═══════════════════════════════════════╗
║  BUZZSHIELD SCAN REPORT — Grade: B+  ║
╚═══════════════════════════════════════╝

CRITICAL (0)  ✅ None found
HIGH     (2)  ⚠️
  → Missing honeypot check in /api/routes/swap.js:42
  → Cron job without expiresAt in /api/services/cron/jobs/token-scan.js:18
MEDIUM   (3)  ℹ️
  → Unverified contract address hardcoded in /api/lib/contracts.js:7
  → Feature flag WALLET_GUARD=false (governance disabled)
  → Missing rate limit on /api/score endpoint

Files scanned: 142
Rules checked: 47
Time: 2.3s
```

### JSON (CI/CD)

Exit code 2 on CRITICAL findings (build gate).

### Markdown (HSaaS reports)

Full report with remediation steps for each finding.

## Usage

### Via Claude Code

```
/security-scan                    # Quick scan
/security-scan --deep             # Include contract analysis
/security-scan --fix              # Auto-fix safe issues
/security-scan --report markdown  # Generate HSaaS report
```

### Via CLI

```bash
npx @buzzbd/shield scan
npx @buzzbd/shield scan --fix
npx @buzzbd/shield scan --format json
```

## How It Differs from AgentShield

| Feature         | AgentShield (ECC)    | BuzzShield (Buzz)               |
| --------------- | -------------------- | ------------------------------- |
| Focus           | Generic dev security | Crypto agent security           |
| Secret patterns | 14 generic           | 14 generic + 14 crypto-specific |
| Wallet checks   | None                 | 9 wallet safety rules           |
| Contract audit  | None                 | 7 smart contract patterns       |
| Trust system    | None                 | Trust gate verification         |
| On-chain        | None                 | Contract ownership checks       |
| Cost            | Free                 | Free (HSaaS report = $500)      |

## Architecture

BuzzShield runs entirely in Claude Code context — no external API calls.
It reads files via Bash/Grep/Glob tools and applies regex + heuristic rules.
Zero LLM cost for scanning. LLM used only for remediation suggestions.
