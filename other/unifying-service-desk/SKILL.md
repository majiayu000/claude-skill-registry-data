---
name: unifying-service-desk
description: >-
  Intelligent multi-tier IT support (L0-L4) with automatic escalation routing.
  Handles incident triage, troubleshooting, root cause analysis, and vendor
  coordination across 12 issue categories. Use when users report issues,
  troubleshooting any technical problem, performing diagnostics, analyzing
  incidents, or coordinating complex fixes. Always use this skill for any IT
  support request — even casual ones like my headset stopped working,
  can't connect to VPN, Teams is broken, computer is slow, printer
  won't work, locked out of my account, monitor not displaying, app
  keeps crashing, email won't sync, or new hire needs setup. Also
  triggers on incident, ticket, issue, error, outage, troubleshoot, diagnose,
  broken, not working, slow, down, help desk, service desk, support request,
  escalation.
  Do NOT trigger for Loxihart Technology Services / FreshService / Kaseya environments.
metadata:
  version: "1.1.0"
---

## Scope Lock

Generic IT support skill. Do NOT use when: the context is explicitly Loxihart Technology Services, Loxihart, FreshService, Kaseya, or [CLIENT].
For Loxihart-specific environments: use operating-loxihart-service-desk.

## Evals

### Should trigger
1. "My laptop is running really slow and freezing." (generic laptop issue, no MSP context)
2. "I can't connect to the VPN from home." (generic VPN / connectivity issue, no Loxihart context)
3. "My headset audio cut out on calls." (generic audio device issue, no Loxihart context)

### Should NOT trigger
1. "Draft a FreshService note for this ticket." (FreshService mentioned -> use operating-loxihart-service-desk)
2. "Triage this Kaseya alert for the [CLIENT]/Loxihart client." (Kaseya + Loxihart mentioned -> use operating-loxihart-service-desk)

<essential_principles>

These principles apply to EVERY support interaction regardless of tier or category.

1. One Step At A Time
Never dump a full troubleshooting sequence. Present one step, confirm the result, then decide the next action. The previous step's outcome determines the next step — not a predetermined script. This matters because skipping confirmation leads to wasted effort and misdiagnosis.

2. Prove Before You Escalate
Every tier boundary requires documented proof that the current tier's procedures were exhausted. "It didn't work" is not an escalation reason — "Steps 1-4 attempted, service restart returned error 0x80070005 (access denied), driver reinstall completed with no change, logs attached" is. This prevents ping-ponging between tiers and respects everyone's time.

3. Document As You Go
Ticket notes are written during troubleshooting, not after. Every step attempted, every result observed, every error code captured — logged in real time using the ticket-notes template. If a tech gets hit by a bus mid-ticket, the next person can pick up exactly where they left off.

4. Security Incidents Break All Rules
If at any point during triage or troubleshooting you identify a security incident (phishing, compromise, malware, unauthorized access), stop normal workflow immediately. Security incidents bypass tier routing and go to L2 minimum with IR procedures. Do not continue troubleshooting a "slow machine" if the root cause is cryptominer malware.

5. Root Cause Over Symptom Relief
Restarting a service fixes the symptom. Understanding why the service died prevents the next ticket. L0-L1 focus on symptom relief (get the user working). L2+ must pursue root cause. Both are valid — but never confuse one for the other.

</essential_principles>

<intake>

To route this correctly, determine three things:

**First — Who are you?**
- End user experiencing the issue → L0 self-service path
- Support tech working a ticket → Tech path (L1+)
- Engineer investigating a pattern → L2+ path

**Second — What's happening?**
Ask for a one-sentence description of the issue. Map it to one of the 12 categories.

**Third — How bad is it?**
Read `references/sla-priority-matrix.md` and classify P1-P5 based on impact and urgency.

These three inputs (role + category + priority) determine the starting tier.

</intake>

<routing>

**Priority-based overrides (these always win):**
- P1 (business-stopping, multiple users) → Start at `workflows/l2-advanced-diagnosis.md`, skip L0/L1
- Security incident (any priority) → Start at `workflows/l2-advanced-diagnosis.md` with IR track
- Recurring/systemic pattern → Start at `workflows/l3-engineering-escalation.md`

**Role + category routing:**

| Role | Priority | Starting Workflow |
|------|----------|-------------------|
| End user | P3-P5 | `workflows/l0-self-service.md` |
| End user | P2 | `workflows/l0-self-service.md` (fast-track to L1 if unresolved in 15 min) |
| End user | P1 | `workflows/l1-first-touch.md` (tech must engage immediately) |
| L1 tech | Any | `workflows/l1-first-touch.md` |
| L2+ engineer | Any | `workflows/l2-advanced-diagnosis.md` |

**Category → reference file mapping (load the relevant reference when entering a workflow):**

| Category Keywords | Reference File |
|-------------------|----------------|
| audio, headset, sound, microphone, speaker, Teams audio | `references/audio-headset.md` |
| network, VPN, Wi-Fi, internet, DNS, connectivity, proxy | `references/network-connectivity.md` |
| hardware, dock, monitor, display, USB, keyboard, mouse | `references/hardware-peripherals.md` |
| imaging, MDT, deployment, BIOS, boot, image | `references/imaging-deployment.md` |
| app, crash, Teams, Zoom, browser, Office, software | `references/software-applications.md` |
| password, MFA, locked out, access, permissions, SSO, license | `references/access-identity.md` |
| email, Outlook, calendar, mailbox, sync, Exchange | `references/email-calendar.md` |
| slow, performance, CPU, RAM, disk, startup, fan | `references/performance.md` |
| phishing, virus, malware, suspicious, compromise, security | `references/security-incidents.md` |
| new hire, onboarding, offboarding, provisioning, deactivate | `references/onboarding-offboarding.md` |
| printer, print, scan, print queue, scanning | `references/print-scan.md` |
| mobile, MDM, remote desktop, RDP, hotspot | `references/mobile-remote.md` |

If the issue spans multiple categories, pick the primary symptom category and note secondary categories for the tech.

**After determining the starting workflow, read it and follow it exactly.**

</routing>

<escalation_protocol>

All tier transitions use the shared escalation gate: `workflows/escalation-gate.md`

Read it before any handoff. It defines what must be documented, what artifacts to attach, and how to route.

</escalation_protocol>

<reference_index>

**Issue Categories** (in `references/`):
- audio-headset.md — Headset detection, auto-switch, mic, Teams/Zoom audio
- network-connectivity.md — VPN, DNS, DHCP, Wi-Fi, proxy, slow internet
- hardware-peripherals.md — Docking stations, monitors, USB, keyboards, mice
- imaging-deployment.md — MDT, driver injection, BIOS, boot failures
- software-applications.md — App crashes, Teams, Office, browsers, LOB apps
- access-identity.md — AD, MFA, SSO, passwords, licensing
- email-calendar.md — Outlook, Exchange, shared mailboxes, calendar sync
- performance.md — CPU, RAM, disk, startup, thermals
- security-incidents.md — Phishing, compromise, malware, IR procedures
- onboarding-offboarding.md — Provisioning, deprovisioning, asset lifecycle
- print-scan.md — Print queue, drivers, scan-to-email, network printers
- mobile-remote.md — MDM, RDP, hotspot, mobile email

**Cross-cutting references:**
- root-cause-patterns.md — Common failure signatures across all categories
- sla-priority-matrix.md — P1-P5 definitions, response/resolution targets

</reference_index>

<templates_index>

All in `templates/`:
- ticket-notes.md — Standardized ticket documentation (use during every interaction)
- escalation-handoff.md — Tier-to-tier handoff package
- rca-report.md — Post-incident root cause analysis
- known-error-entry.md — Entry for known error database

</templates_index>

<workflows_index>

| Workflow | Purpose |
|----------|---------|
| triage-and-classify.md | Symptom intake → category + severity → tier routing |
| l0-self-service.md | End-user guided resolution, no admin rights needed |
| l1-first-touch.md | Known fixes, scripts, remote tools, KB execution |
| l2-advanced-diagnosis.md | Log analysis, root cause diagnosis, config changes |
| l3-engineering-escalation.md | Vendor coordination, infra changes, fleet remediation |
| l4-architecture-review.md | Systemic patterns, design changes, preventive controls |
| escalation-gate.md | Shared escalation criteria + handoff checklist (all tiers) |

</workflows_index>

<scripts_index>

All in `scripts/` — executable PowerShell, run as-is:
- audio-service-restart.ps1 — Restart Windows Audio + Endpoint Builder + device rescan
- network-diag.ps1 — ipconfig, nslookup, ping, tracert, DNS flush
- print-spooler-fix.ps1 — Stop/start Print Spooler, clear queue
- disk-cleanup.ps1 — Temp files, Windows Update cache, reclaim space
- service-health-check.ps1 — Quick status sweep of critical Windows services
- user-profile-repair.ps1 — Rebuild Outlook profile, clear Teams/browser cache

</scripts_index>

<success_criteria>

A well-executed support interaction:
- Identified category and priority within the first 2 exchanges
- Routed to the correct starting tier without unnecessary steps
- Presented one troubleshooting step at a time with confirmation gates
- Documented every step attempted and every result observed
- Used the escalation gate checklist before any tier transition
- Resolved at the lowest possible tier
- Captured root cause (not just symptom relief) at L2+
- Left a ticket trail that any tech could pick up cold

</success_criteria>


---

## CLAIMS
<!-- [SOURCED] or [GENERATED] labels for assertions in this skill. None yet — footer added by audit fix pass. -->

## COUNTEREXAMPLE
<!-- Known cases where this skill should NOT activate or may produce wrong output -->

## CONTRADICTIONS
<!-- ! Conflicts with other skills or system prompts -->
