---
name: incident-response
description: >
  Guide defensive security incident handling on systems the user owns or is authorized to
  investigate: triage and scoping, evidence preservation in order of volatility, containment
  decisions, timeline building, eradication/recovery planning and post-incident review,
  aligned with NIST SP 800-61 Rev. 3 and RFC 3227. Use when the user suspects a compromise
  (unexpected logins, malware, leaked credentials, ransomware signs, data exposure) and needs
  a structured, evidence-safe plan. Not for operational outages without a security angle (use
  linux-troubleshooting or logging-observability), proactive hardening (use linux-hardening),
  threat modeling (threat-modeling), offensive testing, or attacking/retaliating against
  an adversary.
compatibility: >
  Agent Skills-compatible coding agents with shell access to systems the user is authorized
  to investigate. Procedures are platform-neutral; examples are Linux-oriented. Not legal advice.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "incident-response, forensics, security, nist-800-61, evidence, containment, dfir"
  topics: "security, operations"
---

# Incident Response (Defensive)

An incident is a situation where an event may have compromised confidentiality, integrity or availability. Your goals, in order: **protect people and critical systems, preserve evidence, understand scope, restore safely, learn**. The commonest failures are self-inflicted: rebooting the evidence away, "cleaning up" before understanding, or announcing conclusions the evidence does not support.

Framework: NIST SP 800-61 Rev. 3 (final April 2025; supersedes Rev. 2) positions incident response as part of risk management and maps to the CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover), replacing the older four-phase lifecycle in Rev. 2. RFC 3227 supplies the evidence-collection principles used below.

Boundaries: prevention and baselines are `linux-hardening`, `secrets-management`, `container-security`; log design is `logging-observability`; a plain outage is `linux-troubleshooting`; reviewing code for vulnerabilities is `security-code-review`. This skill is the live-incident layer.

## Non-negotiable rules

1. **Authorization and ownership first.** Only investigate systems the user owns or is explicitly authorized to examine; ask who the incident owner and approver are. Never access third-party systems, "hack back", contact the adversary, or probe attacker infrastructure.
2. **Read-only, minimum-footprint collection.** Every command you run on a suspect host changes it a little. Prefer collecting from outside (cloud audit logs, EDR, network telemetry, snapshots) over logging in. Do not install tools on the suspect host without approval.
3. **Containment and eradication change evidence; they need explicit user authorization.** Isolating a host, disabling accounts, revoking keys, killing processes, blocking IPs, reimaging, deleting files or rotating credentials are decisions for the incident owner. Present options with consequences and wait for a clear yes per action.
4. **Do not shut down or reboot early.** RFC 3227 warns that finishing collection before shutdown matters because attackers may alter shutdown scripts and volatile data is lost. Also avoid abruptly cutting network access without thought: it can trigger "dead man" behavior and loses live-connection evidence. Prefer controlled isolation (VLAN/security-group quarantine) the owner approves.
5. **Do not trust the suspect host's tools.** Binaries, libraries and logs on a compromised host can be altered. Use trusted static tools from read-only media, or analyze images and snapshots elsewhere.
6. **Never print, copy into chat, or exfiltrate secrets.** Do not read private keys, token files or password stores. When credentials are suspected exposed, record where and when, and recommend rotation; do not test them.
7. **Record everything as you go.** Timestamps in UTC, who/what/when, commands and hashes. Keep facts separate from hypotheses.
8. **Legal, privacy and disclosure duties are human decisions.** Raise regulators, customers, law enforcement and insurers with the owner and counsel; do not communicate externally on their behalf. Limit collection to what is justified (privacy).

## Workflow

### 1. Intake and triage (first 15 minutes, no changes)

Capture: what was observed, by whom, when (UTC), which assets, how it was detected, current business impact, whether the activity may be ongoing. Ask: is there immediate risk to safety or critical services? Classify severity with the user's own scheme and assign roles: incident lead, technical lead, communications, scribe. Open a single timeline document.

### 2. Preserve before you contain (when safe)

Order of volatility (RFC 3227), most to least volatile:

| Order | Data | Typical read-only source |
|---|---|---|
| 1 | CPU registers, cache | Not practically collectable |
| 2 | Routing/ARP tables, process table, kernel statistics, memory | Memory capture by approved tooling; `ps`, `ss`, `ip route` outputs recorded with timestamps |
| 3 | Temporary filesystems | `/tmp`, tmpfs snapshots |
| 4 | Disk | Block-level image or cloud volume snapshot, hashed |
| 5 | Remote logging and monitoring data | SIEM, cloud audit logs, proxy/DNS/flow logs, exported before retention rolls |
| 6 | Physical configuration, topology | Diagrams, cloud config |
| 7 | Archival media | Backups, kept intact |

Decision point: **volatile capture vs speed of containment.** If active data theft or destruction is occurring and the owner prefers to contain now, record that the volatile data was sacrificed and why. If the system is virtual or cloud, a snapshot (memory-inclusive if the platform supports it) captures much with little interaction. Hash every artifact (e.g. SHA-256), store copies read-only, note who handled them and when (chain of custody).

### 3. Scope with hypotheses

State each hypothesis and the evidence that would confirm or refute it (for example: "attacker used a stolen API key" predicts calls from unfamiliar IPs in cloud audit logs using that key id). Look for: initial access, persistence (new accounts, keys, scheduled tasks, services, startup items), privilege escalation, lateral movement, data access/exfiltration, and defense evasion (log tampering). Pivot on indicators across the estate, but treat IOCs as leads, not proof. Assume more than one host is affected until evidence says otherwise. Check log integrity and clock skew before trusting timestamps.

### 4. Contain (needs authorization)

Offer ranked options with side effects, for example: network-quarantine a host (preserves state, stops lateral movement), disable or rotate a specific credential (may break integrations), block an indicator at egress, revoke sessions. Prefer reversible, narrow actions first. Verify each action worked via an independent signal, and log it in the timeline.

### 5. Eradicate and recover (needs authorization)

Remove attacker access to *all* footholds found, not the first one. For a host with unknown persistence, rebuilding from a known-good image is safer than "cleaning". Rotate credentials in dependency order after access paths are closed (otherwise the attacker captures the new secrets), including any tokens exposed on compromised hosts. Restore from backups verified to predate compromise; monitor closely with enhanced detections for a defined period before declaring recovery.

### 6. Communicate

Short, factual status updates on a fixed cadence: known, unknown, next steps, decisions needed. Avoid speculation and attribution ("nation-state") without evidence. Use out-of-band channels if the primary communication systems may be compromised.

### 7. Post-incident review

Blameless review within days: timeline, root cause, detection gap, what slowed response, corrective actions with owners and dates, detection and hardening updates, and whether runbooks need change. Feed outcomes back to governance and risk processes (the Rev. 3 emphasis).

## Worked example: suspicious SSH logins on a Linux server

1. Intake: user reports logins for `deploy` from an unfamiliar country at 02:10 UTC. Confirm authorization; ask whether the host is production and whether data theft is suspected.
2. Preserve: ask the cloud owner to take a volume snapshot and, if available, a memory-inclusive snapshot; export authentication logs and cloud audit logs off-host; hash exports. No login to the host yet.
3. Hypotheses: (a) stolen key for `deploy`, (b) password guessing success, (c) legitimate VPN egress. Evidence for (c): matches the user's travel or VPN provider IP. Evidence for (a): same key fingerprint used earlier from known IPs. Compare with the exported logs; do not read key files on the host.
4. Containment options offered: remove that key from `authorized_keys` (narrow, reversible; requires approved host access or the cloud console), network-quarantine the host (broader), or leave monitoring in place while collecting. User chooses; the action and time are logged.
5. Scope: search estate-wide for the same key fingerprint and source IPs; check for new keys/cron/systemd units on the host from the snapshot mounted read-only elsewhere.
6. Recover: rebuild or rotate as approved; rotate the exposed key and any credentials available to `deploy`. Review.

## Anti-patterns

- Rebooting, "running antivirus", or deleting malware before imaging.
- Working directly on the original disk instead of a copy.
- Rotating credentials before closing access paths, tipping off or empowering the intruder.
- Declaring "contained" without verification, or "root cause found" from one data source.
- Hunting from the compromised host with its own binaries.
- Pasting logs with credentials or personal data into tickets and chat.
- Letting one engineer improvise on production without a scribe.

## Verification checklist

- [ ] Authorization and incident owner documented.
- [ ] Timeline in UTC with facts vs hypotheses separated.
- [ ] Evidence collected in volatility order where feasible, hashed, and access-logged.
- [ ] Every containment/eradication action was explicitly approved and logged.
- [ ] No secrets read or disclosed; credential exposure noted for rotation.
- [ ] Scope question answered: initial access, persistence, lateral movement, data impact (or marked unknown).
- [ ] Post-incident actions have owners and dates.

## References

- [references/evidence-and-timeline.md](references/evidence-and-timeline.md): evidence log and timeline templates, read-only collection notes.
- [references/scenarios.md](references/scenarios.md): scenarios.
- [references/sources.md](references/sources.md): sources and provenance.
