---
name: buzz-bd-agent
description: >
  Buzz BD Agent operational skill for SolCex Exchange.
  v9.3 — Post-Sprint Day 10 (Apr 10, 2026). BuzzShield V2 + Wallet Guard Live + DRI Audition.
  BuzzShield V2: @stackone/defender prompt injection + OSV.dev supply chain + SBOM.
  BuzzShield dApp LIVE: plena-38072fcd-8.netlify.app (Noah AI + Netlify).
  Wallet Guard AION: 12 receipts persisted, end-to-end proven, decision diversity pending.
  Karpathy LLM Wiki: 43 pages, persistent, wiki-manager.js 550+ lines.
  autoDream: 13 phases (was 9), hill-climber async fix, 595 ground truth.
  Moltbook Trust Level 1 live. DRI Sales audition posted (#439, 100K sats/day).
  Beat Editor auditions posted (#433, both AIBTC Network + Bitcoin Macro).
  87 tables. ~200+ endpoints. 47 feature flags. 33 intel sources.
  CI/CD GREEN. 671+ tokens scored. ~270K sats revenue (~$192).
  Kite AI: Jamal collab opened. Alchemy $20M fund applied.
  Server: CPX62 (16 vCPU, 32GB RAM) | API :3000 | MiroFish :5000 | Sentinel :3001.
---

# Buzz BD Agent — Operational Skill v9.3

> Post-Sprint Day 10 | Apr 10, 2026 | BuzzShield V2 + Wallet Guard Live + DRI Audition
> Claude Code IS Buzz. Brain on Hetzner 24/7. Body on localhost:3000.
> v9.0: 6 reactive modules (mailbox, task-dag, dynamic-crons, event-bus, compression, feature-flags)
> v9.1: 4 outreach modules (outreach-engine, trust-gates, inbox-monitor, wallet-guard)
> v9.2: Context Optimization + Master Deploy (8 phases)
> v9.3: BuzzShield V2 (defender + OSV + SBOM) + Karpathy Wiki + dApp + Wallet Guard live demo
> v10.0: PULSE engine + autoDream (KAIROS architecture, 13 phases)
> For full system manual see: **ALPHA-BUZZ-MASTER-OPS**

---

## QUICK REFERENCE

| Field         | Value                                                          |
| ------------- | -------------------------------------------------------------- |
| Brain         | Claude Code Opus 4.6 (Pro Max unlimited, 24/7 tmux)            |
| Body          | Buzz Docker localhost:3000 (ah-managed)                        |
| Swarm         | MiroFish Real Sim localhost:5000 (Flask Python sidecar)        |
| Server        | Hetzner CPX62, 16 vCPU, 32GB RAM                               |
| Cost          | $43/mo server + ~$200/mo Pro Max + $10 Noah = ~$253/mo         |
| LLM burn      | **$0/day** (qwen3:8b local + Pro Max unlimited)                |
| Endpoints     | **~200+**                                                      |
| Tables        | **87** (was 81 — +3 shield V2, +2 wiki, +1 ground truth)       |
| Services      | **27** (was 21)                                                |
| Rules         | **18** in .claude/rules/                                       |
| Feature flags | **47** (was 31 — +3 shield V2, +1 wiki, +12 from v9.3 surpass) |
| Intel Sources | **33** (OSV.dev = #33)                                         |
| Agents        | 12 persistent in .claude/agents/ (DNA v3.0)                    |
| Pipeline      | **671+ tokens scored**, 0 HOT honest                           |
| Contracts     | 4 on Base + 1 on Solana                                        |
| Revenue       | ~$192 (270K sats AIBTC) + 600 sats/query (Flying Whale)        |
| dApp          | **plena-38072fcd-8.netlify.app** (BuzzShield Token Scanner)    |
| Wiki          | **43 pages** (26 entities, 12 concepts, 5 synthesis)           |

---

## WHAT'S NEW IN v9.3 (Apr 5-10, 2026)

### BuzzShield V2.0 (commit 95c946b)

- **Layer 1**: @stackone/defender prompt injection defense (F1=0.9079, two-tier ML)
- **Layer 2**: OSV.dev supply chain scanning (Intel Source #33, nightly via autoDream)
- **Layer 2b**: CycloneDX SBOM generation (npm sbom)
- 3 new tables: shield_detections, shield_vulnerabilities, shield_sbom
- 3 new flags: BUZZSHIELD_DEFENDER, BUZZSHIELD_OSV, BUZZSHIELD_SBOM
- 17-tool risk map: gmail=high, dexscreener=high, heyanon/nansen/github=medium
- Public API enriched: shield_v2{} in every scan response
- GET /shield/v2/status — standalone V2 layer status

### BuzzShield dApp (Netlify)

- **LIVE**: plena-38072fcd-8.netlify.app
- Built on Noah AI (zero frontend code written, prompt-engineered)
- Cyberpunk SOC aesthetic, Buzz logo, v9.3 badge
- Chain selector (Solana, Base, Ethereum, Bitcoin)
- Scan animation, threat matrix, score gauge, flags panel, share results
- Address validation, scan history
- Enriched API: rules_applied[], threat_matrix{}, market_data{}, flags[], summary
- scan_duration: ~120ms

### Karpathy LLM Wiki (commit 8b64e0a)

- 43 seed pages (26 entities, 12 concepts, 5 synthesis)
- wiki-manager.js: 550+ lines, 18 exports
- Persistent: /data/buzz/persistent/wiki/ (Docker volume, survives reboots)
- autoDream Phase 10 (lint) + Phase 11 (weekly ingest)
- Scoring pipeline hook, signal factory hook
- Host crontab backup daily 03:00 UTC
- Flag: KARPATHY_WIKI=true

### Wallet Guard AION — Live Demo Complete

- End-to-end: Buzz → AION → receipt → persist → War Room mirror
- 12 receipts persisted (IDs 1-12) with counterfactual_summary, normalized, receipt_path
- Decision diversity pending: all returned WARN (Aldo tuning AML policy bands)
- Aldo sending normalized_snapshot payloads for ALLOW/WARN/BLOCK split
- Demo recorded: front-end + back-end + screen capture

### autoDream Evolution

- Now 13 phases (was 9):
  - Phases 1-7: existing (compress, archive, VACUUM, scoring, tasks, mailbox, shield)
  - Phase 8: intel sync
  - Phase 9: hill-climber (async fix commit 45fe95d)
  - Phase 10: wiki lint (Karpathy)
  - Phase 11: weekly wiki ingest (Karpathy)
  - Phase 12: nightly OSV scan (BuzzShield V2)
  - Phase 13: SBOM snapshot (BuzzShield V2)
- 595 ground truth rows seeded (579 dead, 16 legitimate)
- First real hill-climb: 05:00 Jeddah Apr 10

### Moltbook Trust Level 1 (commit 1931b18)

- Autonomous posting: max 2/day
- Engagement: 3-5 comments/day
- Priority targets: Micro Orb (147), Secret Condor (133), Clever Castle (126)

### Signal Factory

- Streak Day 6, 4 signals filed Apr 9
- Cooldown fix identified: cron slots need 3-min buffer (patch queued)
- 30K sats earned overnight (brief inclusion, 9th total)
- Cumulative: ~270K sats (~$192)

---

## ACTIVE AUDITIONS & COMPETITIONS

| Item                        | Where     | Status                       | Revenue potential              |
| --------------------------- | --------- | ---------------------------- | ------------------------------ |
| **DRI Sales**               | #439      | **Audition posted**          | **100K sats/day (~$2,100/mo)** |
| Beat Editor (AIBTC Network) | #433      | Audition posted              | 175K sats/day                  |
| Beat Editor (Bitcoin Macro) | #433      | Audition posted              | 175K sats/day                  |
| Colosseum Frontier          | hackathon | Agent #3734, dApp demo ready | Prize pool                     |
| Kite AI Global              | hackathon | Jamal collab opened          | Prize pool                     |
| Alchemy Fund                | applied   | $20M Solana Fund             | Up to $25K credits             |

---

## KEY RELATIONSHIPS (Updated Apr 10)

| Contact                         | Status                   | Latest                                       |
| ------------------------------- | ------------------------ | -------------------------------------------- |
| Aldo (CODÉ/AION)                | **HOT — demo complete**  | 12 receipts, decision diversity pending      |
| Jamal (Kite)                    | **WARM — collab opened** | Wallet reputation scoring + payment channels |
| Noah AI (Sparsh, Chirag, Sayuj) | **ACTIVE — dApp built**  | BuzzShield on Netlify                        |
| Flying Whale                    | ACTIVE                   | 70/30 confirmed, Skill #110                  |
| Gary Palmer (ATV)               | WARM                     | Identity API restored                        |
| Ryan Gentry (x402)              | HOT                      | Listed on 402 Index                          |

---

## STANDING RULES

1. /scan = QUICK SCORE only (never triggers BD screening)
2. Only full dual-source pipeline (fundamentals ≥42 AND market ≥18) can classify HOT
3. All tweets → War Room (Claude Code Opus Brain) before posting
4. Trust Level 0 — no autonomous external posting without War Room approval
5. All outreach drafts → War Room first
6. NEVER reveal Hetzner IP — use domain names only
7. NEVER share listing fee/commission details publicly
8. Never rush Ogie to accept workarounds — keep going until he says stop
9. BuzzShield V2 flags flip individually with smoke test after each
10. DRI daily cadence: 3 verified contacts by 23:59 PT (if seat won)

---

_v9.3 | BuzzShield V2 + Wallet Guard Live + DRI Audition | 87 tables | 47 flags | 33 intel_
_dApp: plena-38072fcd-8.netlify.app | Wiki: 43 pages | autoDream: 13 phases_
_~$192 revenue | Day 6 streak | DRI Sales 100K sats/day audition live_
_Built by a chef. Kitchen runs itself. Bismillah._ 🤲
