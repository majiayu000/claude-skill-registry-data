---
name: tradecraft-attack-chain
description: >
  Orchestrate a full multi-stage kill chain — recon → initial access → privilege escalation →
  lateral movement → objective — with phase gates, per-phase playbooks, and operating
  discipline. Load on pentest tasks that span stages: "get from external to domain admin",
  "full internal pentest", "I have a webshell, route me to the objective", red-team exercise
  planning. Single-stage tasks go straight to their domain skill; bug bounty never uses this.
domain: tradecraft
type: methodology
stability: learning
modes: [pentest]
severity: high
mitre: [T1190, T1078, T1021, T1558]
tools: []
schema_version: 1
---

# Kill-chain orchestration

## When it applies
An authorized **pentest** (never bug bounty — persistence and lateral movement exceed program
scopes) whose objective spans stages: "external to domain admin", "full internal pentest",
"I have a webshell — what's the route", a red-team exercise. `tradecraft-attack-scenarios`
turns the objective into an ordered plan and `tradecraft-attack-path-mapping` models the
graph; this skill is the execution layer — phase gates, per-phase playbooks, and the
discipline that keeps a multi-day operation coherent. Single-stage tasks skip it and go
straight to their domain skill (`web-*`, `ad-*`, `cloud-*`).

## Why it works
Multi-stage engagements fail by drift, not by missing techniques. Re-planning at each phase
gate — what do I hold, what does it unlock, what's the cheapest next edge — reaches the
objective with least action and noise. The kill chain is a routing spine; each phase delegates
to the specialist skills that own the technique, and a blocked phase reroutes instead of
grinding.

## Method
> Full playbooks (web→DC, phishing→internal, proximity, cloud, AD CS) and the
> state→next-step decision matrix: [`cheatsheet.md`](cheatsheet.md).

0. **Gate: scope first.** Load `tradecraft-scope-roe`; confirm the signed scope in
   `engagements/<target>/scope.txt`. Persistence, EDR evasion, and log tampering need explicit
   written authorization — assumed only under a red-team RoE, never by default.
1. **Recon** (`recon-*`): subdomains → live hosts (`httpx`) → ports (`naabu`/`nmap`) → tech
   fingerprint (`nuclei -tags tech`). Prioritize test/dev/staging environments and newly
   deployed systems; mine leaks (`recon-github-code-leaks`) for cloud keys, connection
   strings, JWT secrets. **Gate: asset list + ranked candidate leads in `plan.md`.**
2. **Initial access** — highest-signal vector first: known-vuln components
   (`nuclei -severity critical,high`), the web classes (`web-sqli`, `web-ssti`,
   `web-file-upload`, `web-ssrf` → `cloud-imds-ssrf` for cloud creds), perimeter appliances
   (`network-appliance-attacks`), exposed services (`network-service-attacks`), or
   phishing/physical when the RoE includes them (`social-eng-*` — load
   `social-eng-methodology` first). **Gate: a foothold with proven command execution.**
3. **Privilege escalation** (`privesc-enumeration` before any exploit): Windows token abuse
   (`privesc-windows-tokens`), sudo/SUID (`privesc-linux-gtfobins`), cloud IAM
   (`cloud-iam-privesc`). **Gate: admin/SYSTEM/root, or a more powerful identity than before.**
4. **Lateral movement** — loot credentials (`privesc-enumeration`, mimikatz/secretsdump), then
   move: `ad-*` (Kerberoasting, delegation, DACL, ADCS), `network-ntlm-relay`, WinRM/SSH, and
   `network-pivoting-tunneling` for segmented networks. BloodHound drives the path
   (`tradecraft-attack-path-mapping`). **Gate: every hop is a validated edge, not an
   assumption.**
5. **Objective** — reach what the engagement exists to prove: domain admin, the data store,
   the crown-jewel system. Prove with the least data possible (anonymize any proof data).
   Implants/persistence only if the RoE authorizes them and a cleanup date is agreed.
6. **Close out** — remove every artifact you introduced (accounts, uploads, scheduled tasks,
   beacons, dropped tools, added SSH keys), restore what you changed, reconcile against your
   activity log. Then `reporting-evidence-review` → `reporting-pentest-report`.

Re-plan at every gate: a blocked phase routes back through `tradecraft-pivot-decisions` to the
next-best edge.

## Gotchas
- **Don't blast the whole chain with automation against a domain** — an unscoped scanner run
  is how engagements end careers. Work the asset list, phase by phase.
- **One failed technique ≠ blocked phase** — work the variation matrix (House rules) and the
  alternate edges before declaring a gate unpassable.
- **High-risk actions (DCSync, golden ticket, log tampering) need explicit RoE coverage** —
  if it isn't written down, don't do it; propose it to the client instead.
- **Honeypots**: an oddly open share or a too-tempting credential is a trap — verify before
  you use it.
- **Never touch availability or real user data** — no DoS, no mass exfiltration.
- Classic failure modes to avoid: mimikatz dumps left on disk, C2 on a threat-intel-burned
  domain, phishing that trips DLP because the gateway was never tested, lateral movement that
  springs a honeypot.

## Verify success
Every phase gate has a written pass/fail in `plan.md`; the path from first foothold to
objective is reproducible edge by edge; all introduced artifacts are removed and accounted
for; the evidence chain survives `reporting-evidence-review`.

## References
MITRE ATT&CK tactics; PTES; `tradecraft-attack-scenarios`, `tradecraft-attack-path-mapping`,
`tradecraft-complex-engagements`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
