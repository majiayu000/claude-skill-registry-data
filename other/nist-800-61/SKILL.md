---
name: nist-800-61
description: "Knowledge base from NIST SP 800-61 Rev. 3 (Incident Response Recommendations for Cybersecurity Risk Management). Use for CSF 2.0-aligned incident response life cycles, IR roles, Community Profile priorities for DE/RS/RC and preparation, playbooks, coordination, and continuous improvement. Covers 800-61r3 only; does not replace CSF 2.0 full text, SP 800-61r2 tactical playbooks, or sector-specific breach-notification law."
---

<!-- argument-hint: [topic, function, or chapter number] -->

# NIST SP 800-61 Rev. 3 — Incident Response for Cyber Risk Management
**Source**: NIST SP 800-61r3 (US Government work, public domain) | **Chapters**: 6

## When to use
Reach for this pack when designing or improving an incident response capability as part of cybersecurity risk management — especially if you are aligning IR to NIST CSF 2.0, migrating from the older SP 800-61r2 life cycle, building a Community Profile for cyber incident risk management, clarifying IR roles and authorities, or tightening coordination, communications, training, and lessons-learned loops.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about life-cycle models, CSF Functions in IR, roles, policies/playbooks, preparation profile, detect/respond/recover, or coordination/training.
- **With a chapter** — ask for `ch01` through `ch06`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### From handling guide to CRM integration
SP 800-61r3 supersedes r2. Tactical how-to content ages too fast for a single static SP, so r3 focuses on integrating IR across CSF 2.0 Functions and points to CPRT, the IR project page, and other resources for implementation depth.

### CSF-based IR life cycle
| Layer | Functions | IR role |
|-------|-----------|---------|
| Preparation foundation | Govern, Identify, Protect | Prevent, prepare, reduce impact, host many lessons sinks |
| Active IR | Detect, Respond, Recover | Discover, manage, contain, eradicate, restore, communicate |
| Continuous improvement | Identify → Improvement (ID.IM) | Capture lessons anytime; feed all Functions |

### Community Profile structure
- **Table 2 — Preparation & lessons learned**: GV/ID/PR + ID.IM with IR-relative priorities (often lower because not unique to active response).
- **Table 3 — Incident response**: DE/RS/RC with higher priorities and denser recommendations/considerations.
- Annotations: **R** recommendation, **C** consideration, **N** note; IDs like `DE.CM.R1`. Higher-level R/C/N inherit downward.

### Roles beyond the IR team
Leadership, handlers (staff/contract/on-demand), technology professionals, legal, public affairs, HR, physical security/facilities, asset owners, and third parties (MSSP, CSP, partners, law enforcement) all participate. Policy must pre-assign disruptive authorities.

### Policy and playbooks
Policies cover commitment, scope, definitions, roles/authorities, prioritization/severity, recovery initiation, and measures. Procedures and playbooks make common and emergency paths executable and trainable.

### Coordination and learning
Pre-arrange external contacts and sharing rules; train decision-makers as well as handlers; exercise; push findings through ID.IM into detections, safeguards, and governance.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-scope-shift-and-csf-integration.md) | Scope Shift and CSF Integration | r3 purpose, supersession of r2, Community Profile mechanics |
| [ch02](chapters/ch02-ir-lifecycle-model.md) | IR Life Cycle Model | Legacy vs CSF life cycle, Function roles, Table 1 mapping |
| [ch03](chapters/ch03-roles-policies-and-playbooks.md) | Roles, Policies, Playbooks | Multi-role model, policy elements, procedures/playbooks |
| [ch04](chapters/ch04-preparation-and-lessons-learned-profile.md) | Profile: Preparation & Lessons | Table 2 GV/ID/PR + ID.IM |
| [ch05](chapters/ch05-detect-respond-recover-profile.md) | Profile: Detect/Respond/Recover | Table 3 DE/RS/RC execution outcomes |
| [ch06](chapters/ch06-coordination-training-and-improvement.md) | Coordination, Training, Improvement | Comms, sharing, exercises, continuous improvement |

## Topic Index
- **Active IR layer (DE/RS/RC)** → ch02, ch05
- **Authorities to shut down / isolate** → ch03
- **Community Profile priorities (H/M/L)** → ch01, ch04, ch05
- **Continuous improvement / ID.IM** → ch02, ch04, ch06
- **Continuous monitoring** → ch05
- **Coordination with MSSP/CSP/partners** → ch03, ch06
- **CSF 2.0 Functions in IR** → ch02
- **Event vs incident definitions** → ch01, ch03
- **Incident declaration** → ch05
- **Legal and breach notification context** → ch03, ch04
- **Lessons learned timing** → ch02, ch06
- **Life cycle model (legacy r2)** → ch02
- **Media / public affairs** → ch03, ch06
- **Playbooks and procedures** → ch03
- **Policy elements for IR** → ch03
- **Preparation (GV/ID/PR)** → ch02, ch04
- **Recovery declaration / backup integrity** → ch05
- **Roles and responsibilities** → ch03
- **Supersession of SP 800-61r2** → ch01
- **Table 1 phase mapping** → ch02
- **Threat information sharing** → ch05, ch06
- **Training and exercises** → ch06

## Supporting Files
- [glossary.md](glossary.md) — IR / CSF terms used in 800-61r3
- [patterns.md](patterns.md) — implementation patterns with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, maps, tells & smells

---

## Scope & Limits
This pack covers NIST SP 800-61 Revision 3 (final 2025-04-03, DOI 10.6028/NIST.SP.800-61r3) — IR as cybersecurity risk management, the CSF-based life cycle, roles/policies, and the Community Profile structure — as synthesized reference notes. Actual page count from extraction metadata is **48**. It does **not** cover: full CSF 2.0 subcategory catalog detail (see nist-csf pack); SP 800-61r2 step-by-step tactical handling as an authoritative current guide; CISA playbooks verbatim; organization-specific legal breach-notification advice; or classified IR programs. US Government public domain work. No source-material download link is published.
