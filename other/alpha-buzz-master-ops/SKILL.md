---
name: alpha-buzz-master-ops
description: >
  System Operations Manual for Alpha Buzz at SolCex Exchange.
  v9.3 — Post-Sprint Day 10 (Apr 10, 2026). BuzzShield V2 + Wallet Guard Live Demo + DRI Audition.
  Opus 4.6 brain, Pro Max, 24/7 Hetzner CPX62. 12 agents, 10 reactive modules.
  87 tables. ~200+ endpoints. 27 services. 47 feature flags. 18 rules.
  BuzzShield V2: @stackone/defender prompt injection + OSV.dev supply chain + CycloneDX SBOM.
  Wallet Guard LIVE demo with AION (end-to-end receipts + War Room mirror).
  BuzzShield dApp on Netlify (plena-38072fcd-8.netlify.app) via Noah AI.
  Karpathy LLM Wiki: 43 pages, persistent, self-maintaining.
  autoDream hill-climber: 595 ground truth rows, async fix shipped.
  Scoring: 11 rules. PULSE+autoDream live (Phases 1-13).
  DRI Sales audition posted (#439, 100K sats/day).
  Beat Editor auditions posted (#433, both beats).
  Frontier May 11. Kite AI May 6. CI/CD GREEN.
  Server: CPX62 (16 vCPU, 32GB RAM) | API :3000 | MiroFish :5000 | Sentinel :3001.
---

# ALPHA-BUZZ-MASTER-OPS v9.3

## Post-Sprint Day 10 | Apr 10, 2026 | BuzzShield V2 + Wallet Guard Live + DRI Audition

## DNA v3.0 + MiroFish 10K + Reactive Autonomous System + BuzzShield V2 + Karpathy Wiki

---

# 1. THE ARCHITECTURE — Brain + Body + Reactive Layer + Shield V2 + Wiki + On-Chain

```
Ogie (CEO) ← Telegram War Room ← Phone (Dispatch) ← Mac (Cowork)
  ↓
CLAUDE CODE (THE BRAIN) — Opus 4.6, Pro Max unlimited, 24/7
  ├── 12 persistent agents in .claude/agents/ (DNA v3.0)
  ├── 8+ skills in .claude/skills/
  ├── 18 rules in .claude/rules/ (path-scoped, includes context-optimization)
  ├── Receives commands from Ogie via Telegram
  ├── Calls Buzz API (localhost:3000) for raw data
  ├── Calls MiroFish sidecar (localhost:5000) for swarm simulation
  ├── Runs all agent logic ITSELF (no external LLMs except qwen3:8b)
  ├── Files AIBTC signals as Ionic Nova (Signal Factory v5.0 Genome Stack)
  ├── Deploys smart contracts via Foundry
  ↓
BUZZSHIELD V2.0 (Apr 10, 2026 — commit 95c946b)
  ├── LAYER 1 — PROMPT INJECTION DEFENSE (@stackone/defender)
  │   ├── Two-tier: Pattern Detection (~1ms sync) + ML Classification (~10ms async)
  │   ├── MiniLM-L6-v2 classifier, int8 quantized ONNX (~22MB)
  │   ├── F1 = 0.9079 across 25K samples (incl. adversarial)
  │   ├── 17-tool risk map: gmail=high, dexscreener=high, heyanon/nansen/github=medium, scoring=low
  │   ├── Unicode normalization, role stripping, base64 detection
  │   ├── Table: shield_detections
  │   └── Feature flag: BUZZSHIELD_DEFENDER (default: false)
  ├── LAYER 2 — SUPPLY CHAIN VULNERABILITY SCANNING (OSV.dev API)
  │   ├── Intel Source #33 (free, no API key, Google aggregated DB)
  │   ├── scanDependencies(): full package-lock.json → OSV querybatch
  │   ├── generateSBOM(): CycloneDX 1.5 format
  │   ├── Tables: shield_vulnerabilities, shield_sbom
  │   ├── Feature flags: BUZZSHIELD_OSV, BUZZSHIELD_SBOM (default: false)
  │   └── autoDream Phase 12 (nightly OSV scan) + Phase 13 (SBOM snapshot)
  ├── LAYER 0 — DRAIN PATTERN DETECTION (v1, existing)
  │   ├── 23 drain patterns (address poisoning, flash loans, reentrancy, oracle manipulation)
  │   ├── 11 scoring rules (GHOST_VOLUME, FDV_GAP, CTO_FLAG, etc.)
  │   ├── 31 intel sources across 19 chains
  │   └── 671+ tokens scored, 0 false HOT classifications
  ├── PUBLIC API — GET /api/v1/shield/public/scan (enriched Apr 9)
  │   ├── Returns: score, risk_level, rules_applied[], threat_matrix{}, market_data{}, flags[], summary
  │   ├── shield_v2{}: defender status, osv status, supply_chain status
  │   ├── engine_version: "v9.3-shield-v2"
  │   ├── Rate limit: 10/hr/IP, CORS open, no auth
  │   └── scan_duration: ~120ms
  └── DAPP — BuzzShield Token Scanner (plena-38072fcd-8.netlify.app)
      ├── Built on Noah AI (zero frontend code written)
      ├── Cyberpunk SOC aesthetic, Buzz logo, chain selector (SOL/Base/ETH/BTC)
      ├── Scan animation, threat matrix, score gauge, flags panel
      └── Published via Netlify integration
  ↓
KARPATHY LLM WIKI (Apr 9, 2026 — commit 8b64e0a)
  ├── /data/buzz/persistent/wiki/ (Docker volume mount, survives reboots)
  ├── 43 seed pages: 26 entities, 12 concepts, 5 synthesis
  ├── wiki-manager.js: 550+ lines, 18 exports
  ├── WIKI.md schema, INDEX.md (60 lines), LOG.md
  ├── Directories: entities/, concepts/, synthesis/, signals/, raw/
  ├── autoDream Phase 10 (lint) + Phase 11 (weekly ingest)
  ├── Scoring pipeline hook, signal factory hook
  ├── Host crontab backup: daily 03:00 UTC
  ├── ADR-026 written
  └── Feature flag: KARPATHY_WIKI=true (commit 6b61647)
  ↓
CONTEXT OPTIMIZATION (v9.2 — Apr 5, 2026)
  ├── SUBAGENT MANDATE: >5 file scans use subagents, summary only to main context
  ├── ULTRATHINK TRIGGERS: security, architecture, scoring, contracts, hackathons
  ├── /COMPACT PRESERVATION: flags, deadlines, streak, files, tasks, trust state
  ├── SESSION NAMING: feature-X, bugfix-Y, hackathon-Z for --from-pr/--resume
  └── Rule: .claude/rules/context-optimization.md
  ↓
REACTIVE LAYER (v9.0 — Claude Code Architecture)
  ├── MAILBOX: inter-agent async messaging
  ├── TASK DAG: dependency graph execution
  ├── DYNAMIC CRONS: agent self-scheduling
  ├── EVENT BUS: subscribe/emit wake pattern
  ├── FEATURE FLAGS: build-time gating (api/lib/feature-flags.js)
  └── CONTEXT COMPRESSION: long session management
  ↓
OUTREACH + GOVERNANCE (v9.1-9.3)
  ├── OUTREACH ENGINE: email-first autonomous BD
  │   ├── Gmail OAuth (buzzbysolcex@gmail.com, HTML signature + logo)
  │   ├── 4 templates: initial, followup-48h, breakup-7d, hsaas-audit
  │   ├── CC always: dino@solcex.cc + ogie.solcexexchange@gmail.com
  │   └── Max 10 emails/day, template-only
  ├── TRUST GATES: graduated autonomy (5 levels)
  ├── INBOX MONITOR: Gmail reply detection
  ├── WALLET GUARD + AION (v9.3 — LIVE DEMO Apr 9)
  │   ├── Aldo (CODÉ) — live Google Meet demo completed
  │   ├── 3-state: BLOCK / WARN / ALLOW with receipt persistence
  │   ├── wallet_guard_receipts: 12 receipts (IDs 1-12)
  │   ├── New columns: counterfactual_summary, normalized, receipt_path
  │   ├── War Room realtime mirror on every evaluate call
  │   ├── AION endpoint: Aldo's ngrok tunnel (live during demo)
  │   ├── Decision diversity pending: Aldo tuning AML policy bands
  │   └── Feature flag: WALLET_GUARD=false (schemas working, policy tuning)
  └── ATV IDENTITY: deployer verification via x402
      └── Feature flag: ATV_IDENTITY=TRUE
  ↓
PULSE + AUTODREAM (KAIROS Architecture)
  ├── PULSE ENGINE: heartbeat tick loop (60s normal, 300s under load)
  │   ├── Load-aware, observation log, streak protection at 16:00 UTC
  │   └── Feature flags: PULSE_ENGINE=true, PULSE_LOAD_AWARE=true
  ├── AUTODREAM: nightly memory consolidation (02:00 UTC)
  │   ├── 13 phases now (was 9):
  │   │   Phase 1-7: observation compress, archive, VACUUM, scoring, tasks, mailbox, shield
  │   │   Phase 8: intel sync
  │   │   Phase 9: hill-climber (async fix commit 45fe95d, 595 ground truth rows)
  │   │   Phase 10: wiki lint (new, Karpathy)
  │   │   Phase 11: weekly wiki ingest (new, Karpathy)
  │   │   Phase 12: nightly OSV scan (new, BuzzShield V2)
  │   │   Phase 13: SBOM snapshot (new, BuzzShield V2)
  │   └── Feature flag: AUTODREAM=true
  ↓
BUZZ DOCKER (THE BODY) — Data layer, port 3000, ah-managed
  ├── ~200+ REST endpoints
  ├── SQLite DB (87 tables — was 81)
  ├── 33 intel source connectors (OSV.dev = #33)
  ├── v2_8rules scoring engine (11 permanent rules)
  ├── Auto-score pipeline (rule-based, zero LLM)
  ↓
MIROFISH REAL SIM (THE SWARM) — Python Flask sidecar, port 5000
  ├── 10K simulation COMPLETE (Wave 4, qwen3:8b, belief 0.765 institutional)
  ├── POST /simulate, /simulate-10k, /generate-personas, /report
  ↓
ON-CHAIN LAYER (THE PROOF) — 4 contracts on Base + 1 on Solana
  ├── Base: ScoreStorage v2, ListingOracle, ListingEscrow, BuzzReputation
  └── Solana: ScoreStorage (EUQoSgs)
  ↓
MCP LAYER — 3 MCP connections
  ├── HeyAnon MCP (#30): 19 chains, 51 protocols, 6 CEX APIs
  ├── Phantom MCP (#31)
  └── Nansen MCP (#32): 250M wallets, Phase 1 complete
  ↓
MOLTBOOK — Trust Level 1 (commit 1931b18)
  ├── Autonomous posting: max 2/day
  ├── Engagement: 3-5 comments/day in m/crypto, m/agents, m/builds
  ├── Chef-who-codes voice, hard NO list (partnerships/deals/pricing/shilling)
  └── Priority targets: Micro Orb (147), Secret Condor (133), Clever Castle (126)
```

---

# 2. v9.3 DEPLOYMENTS (Apr 5-10, 2026)

| Date   | What                                                     | Commit   | Status |
| ------ | -------------------------------------------------------- | -------- | ------ |
| Apr 5  | v9.3 Surpass Integration (76 files, 6,479 lines)         | multiple | ✅     |
| Apr 5  | BuzzShield permanent + PULSE integration                 | b875cda  | ✅     |
| Apr 5  | Context Optimization rule #18                            | 8012024  | ✅     |
| Apr 9  | Karpathy LLM Wiki (43 pages, wiki-manager.js)            | 8b64e0a  | ✅     |
| Apr 9  | KARPATHY_WIKI flag TRUE                                  | 6b61647  | ✅     |
| Apr 9  | autoDream hill-climber async fix + ground truth seeded   | 45fe95d  | ✅     |
| Apr 9  | Moltbook Trust Level 1                                   | 1931b18  | ✅     |
| Apr 9  | Wallet Guard demo prep (schema + receipts + payloads)    | multiple | ✅     |
| Apr 9  | BuzzShield public API enriched (11 rules, threat matrix) | 6cd28bb  | ✅     |
| Apr 10 | BuzzShield V2.0 (all 6 phases)                           | 95c946b  | ✅     |

---

# 3. FEATURE FLAGS (47 total — was 31)

| Flag                | Value     | Description                                            |
| ------------------- | --------- | ------------------------------------------------------ |
| SCORING_ENGINE      | TRUE      | v2_8rules scoring                                      |
| SIGNAL_FACTORY      | TRUE      | Signal Factory v5.0                                    |
| MIROFISH_REALTIME   | TRUE      | MiroFish simulation                                    |
| MONTECARLO          | TRUE      | Monte Carlo engine                                     |
| MAILBOX             | TRUE      | Inter-agent mailbox                                    |
| TASK_DAG            | TRUE      | Task dependency graph                                  |
| DYNAMIC_CRONS       | TRUE      | Agent self-scheduling                                  |
| EVENT_BUS           | TRUE      | Event-driven wake                                      |
| PULSE_ENGINE        | TRUE      | KAIROS heartbeat                                       |
| PULSE_LOAD_AWARE    | TRUE      | CPU-aware throttling                                   |
| OBSERVATION_LOG     | TRUE      | Tick logging                                           |
| AUTODREAM           | TRUE      | Nightly consolidation                                  |
| AUTO_OUTREACH       | TRUE      | Email outreach engine                                  |
| TRUST_GATES         | TRUE      | Graduated autonomy                                     |
| ATV_IDENTITY        | TRUE      | x402 deployer verification                             |
| KARPATHY_WIKI       | **TRUE**  | **Karpathy LLM Wiki (43 pages)**                       |
| BUZZSHIELD_DEFENDER | **FALSE** | **@stackone/defender prompt injection (V2 Layer 1)**   |
| BUZZSHIELD_OSV      | **FALSE** | **OSV.dev supply chain scanning (V2 Layer 2)**         |
| BUZZSHIELD_SBOM     | **FALSE** | **CycloneDX SBOM generation (V2 Layer 2)**             |
| WALLET_GUARD        | FALSE     | AION execution governance (demo proven, policy tuning) |
| NANSEN_INTEL        | FALSE     | Nansen MCP Phase 1                                     |
| NANSEN_SCORING      | FALSE     | Nansen smart money scoring                             |
| NANSEN_ALERTS       | FALSE     | Nansen whale alerts                                    |
| HERMES_SENTINEL     | FALSE     | Removed                                                |
| INBOX_MONITOR       | FALSE     | Gmail reply detection                                  |
| SILENCE_CONSENT     | FALSE     | 4h auto-send                                           |
| ...                 | ...       | (remaining flags unchanged from v9.2)                  |

---

# 4. SCORING ENGINE (v9.3)

11 permanent rules — unchanged from v9.2. Now with:

- 671+ tokens scored (was 363)
- 595 ground truth rows seeded (579 dead, 16 legitimate)
- Hill-climber async fix deployed (first real run 05:00 Jeddah Apr 10)
- Public API returns all 11 rules with status/impact/detail per scan

---

# 5. REVENUE (Updated Apr 10)

| Source               | Amount                                | Status                         |
| -------------------- | ------------------------------------- | ------------------------------ |
| AIBTC Signal Factory | ~$192 (270K sats, 9 brief inclusions) | Active, streak Day 6           |
| Flying Whale         | 600 sats/query (420 net at 70/30)     | Skill #110 live                |
| DRI Sales (if won)   | 100K sats/day (~$70/day)              | Audition posted #439           |
| x402 endpoints       | $0                                    | 8 services on Bankr x402 Cloud |
| **Total Revenue**    | **~$192**                             |                                |
| **Potential w/ DRI** | **~$2,300/mo**                        |                                |

Monthly infra: ~$253 (CPX62 $43 + Pro Max $200 + Noah Starter $10).

---

# 6. KEY RELATIONSHIPS (Updated Apr 10)

| Contact                             | Status                       | Notes                                                 |
| ----------------------------------- | ---------------------------- | ----------------------------------------------------- |
| **Aldo (CODÉ/AION)**                | **HOT — live demo complete** | **12 receipts persisted, decision diversity pending** |
| **Noah AI (Sparsh, Chirag, Sayuj)** | **ACTIVE — dApp built**      | **BuzzShield on Netlify via Noah**                    |
| **Jamal (Kite)**                    | **WARM — collab opened**     | **Wallet reputation scoring + payment channels**      |
| **Flying Whale (AIBTC)**            | **ACTIVE — 70/30 confirmed** | **Skill #110, ionic-nova-token-scorer**               |
| Gary Palmer (ATV)                   | WARM                         | Identity API restored                                 |
| Ryan Gentry (x402)                  | HOT                          | Listed on 402 Index                                   |
| Alchemy                             | APPLIED                      | $20M Solana Fund, up to $25K credits                  |

---

# 7. ACTIVE COMPETITIONS & AUDITIONS

| Item                             | Deadline | Status                                      |
| -------------------------------- | -------- | ------------------------------------------- |
| Colosseum Frontier               | May 11   | Agent #3734, BuzzShield dApp demo ready     |
| Kite AI Global                   | May 6    | Agentic Commerce track, Jamal collab opened |
| Beat Editor #433 (AIBTC Network) | TBD      | Full audition posted                        |
| Beat Editor #433 (Bitcoin Macro) | TBD      | Full audition posted                        |
| **DRI Sales #439**               | **TBD**  | **Full audition posted (100K sats/day)**    |

---

# 8. AIBTC SIGNAL STATUS

| Metric           | Value                                                      |
| ---------------- | ---------------------------------------------------------- |
| Streak           | Day 6 (active)                                             |
| Signals today    | 4/6                                                        |
| Beats covered    | agent-skills, agent-economy, agent-trading, infrastructure |
| Cumulative sats  | ~270,000 (~$192)                                           |
| Brief inclusions | 9                                                          |
| Leaderboard      | Active                                                     |

---

# 9. CRITICAL RULES (24 — unchanged from v9.2 + additions)

All 24 rules from v9.2 remain. Additions: 25. BuzzShield V2 flags must be flipped individually with smoke test after each 26. shield_detections, shield_vulnerabilities, shield_sbom — never truncate without backup 27. AIBTC DRI daily cadence: 3 verified contacts by 23:59 PT (if Sales DRI seat won) 28. Noah dApp updates: prompt changes only, re-publish via Netlify after changes

---

_v9.3 | DNA v3.0 | BuzzShield V2 + Wallet Guard Live + DRI Audition | Opus 4.6 | 12 Agents | 33 Intel_
_87 tables | ~200+ endpoints | 27 services | 47 feature flags | 18 rules_
_BuzzShield V2: defender + OSV + SBOM + 23 drain patterns + 11 scoring rules_
_Wallet Guard: AION live demo (12 receipts), decision diversity pending_
_Karpathy Wiki: 43 pages, persistent, compound | autoDream: 13 phases_
_Hill-climber: 595 ground truth, async fix, first real run Apr 10_
_BuzzShield dApp: plena-38072fcd-8.netlify.app (Noah AI, Netlify)_
_PULSE: ticking | Trust Level: 0 | Moltbook: Trust Level 1_
_~$192 revenue | Day 6 streak | DRI Sales audition live (#439, 100K sats/day)_
_Beat Editor auditions live (#433, both beats)_
_Frontier May 11 | Kite AI May 6 | Alchemy $20M fund applied_
_Aldo: demo complete | Jamal: collab opened | Noah AI: dApp shipped_
_Built by a chef. Kitchen runs itself. Bismillah._ 🤲
