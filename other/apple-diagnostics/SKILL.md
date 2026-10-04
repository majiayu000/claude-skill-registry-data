---
name: apple-diagnostics
description: Forensic, read-only-by-default diagnosis of Apple ecosystem issues from a Mac. Use when investigating macOS, iPhone/iPad, Watch, Apple TV, HomePod, AirPods, iCloud, Continuity, HomeKit, Matter, power, panic, storage, networking, security, or peripheral problems that require log analysis, timeline reconstruction, ranked hypotheses, safe remediation planning, and rollback-aware change control.
---

# Apple Diagnostics

Use this skill for opaque Apple system issues where the user needs expert diagnosis rather than guesswork.

This skill is Apple ecosystem-wide, but assumes the active execution environment is a Mac. For non-Mac devices, diagnose from Mac-side evidence, user-provided exports, or user-guided capture steps.

## Default Mode

This skill is forensic and advisory by default.

Do not change system state unless:
- you explain the suspected cause clearly
- you explain the proposed fix and why it may help
- you explain the risks and rollback implications
- the user explicitly approves

Before any approved change:
- record the pre-change state
- create backups or exports when feasible
- record rollback steps before acting

Never perform destructive actions casually. If one is truly necessary, explain why safer options are insufficient and get explicit approval first.

## Output Format

Use a dual-layer response unless the user asks otherwise.

Layer 1: Simple Summary
- plain-English explanation
- likely cause
- confidence
- safest next steps

Layer 2: Technical Appendix
- evidence used
- commands run
- timeline
- ranked hypotheses
- contradictions and unknowns
- escalation criteria

## Investigation Workflow

1. Establish the timeline.
2. Identify the failure boundary.
3. Gather the smallest relevant evidence set.
4. Correlate adjacent subsystems.
5. Rank likely causes.
6. Rule out obvious false leads.
7. Recommend safe next steps.
8. If a fix is proposed, switch into approval and rollback mode before changing anything.

Always distinguish:
- symptom
- trigger
- mechanism
- aftermath

Do not confuse post-crash activity with the pre-crash cause.

## Required Case Logging

Create a separate case folder at the start of each investigation using:
- `Investigations/YYYY.MM.DD-HH.MM.SS-case-name/`

Maintain at least:
- `case.md`
- `summary.md`
- `timeline.md`
- `hypotheses.md`
- `actions.md`
- `approvals.md`
- `rollback.md`
- `environment.md`

Use subdirectories when applicable:
- `evidence/`
- `exports/`
- `backups/`
- `rollback/`
- `attachments/`

The case record must capture:
- symptoms
- environment
- evidence
- reasoning
- conclusions
- confidence
- proposed actions
- user approvals or denials
- actions taken
- rollback state

Before any approved state change, record the pre-change state and rollback plan first.

For detailed logging structure and templates, read:
- `references/case-logging.md`
- `references/file-templates.md`

## Choose The Right Reference

Read only the references needed for the case:

- Panic, crash, watchdog, sleep panic:
  `references/panic-analysis.md`

- Sleep, wake, hibernation, battery, thermal:
  `references/power-sleep.md`

- APFS, cryptex, updates, storage, boot, install state:
  `references/storage-apfs.md`

- Wi-Fi, VPN, DNS, reachability, Continuity, Home discovery:
  `references/networking.md`

- MDM, persistence, TCC, trust, certificates, suspicious behavior:
  `references/security.md`

- HomeKit, Matter, hubs, Thread, accessory reachability:
  `references/homekit-matter.md`

- Broad evidence collection and escalation method:
  `references/evidence-workflow.md`

## Evidence Sources

Use the smallest useful set first, then widen if needed:
- panic and crash reports
- unified logs
- `pmset`
- `ioreg`
- `system_profiler`
- install history
- launch items and background items
- network state
- APFS and storage state
- account and sync indicators
- user-provided exports, screenshots, and repro steps

Prefer primary evidence over assumption.

## Web Research

Use live web research when it materially improves accuracy, especially for:
- current Apple builds and release notes
- known bugs
- firmware correlations
- support bulletins
- CVEs
- vendor docs for Apple-adjacent peripherals and Matter accessories

Prefer Apple and other primary sources first. Include dates when discussing current versions or known issues.

## Specialist Modes

This skill supports these specialist modes:
- panic and crash
- power, sleep, and thermal
- storage, APFS, and install state
- networking and connectivity
- peripherals and buses
- security and persistence
- Apple ecosystem and HomeKit/Matter

Switch modes based on the actual failure boundary, not just the user's wording.

## What Good Work Looks Like

Good analysis:
- is evidence-driven
- is explicit about uncertainty
- ranks causes instead of pretending certainty
- explains findings in plain English first
- avoids unnecessary fixes
- creates rollback-aware plans when changes are needed

Bad analysis:
- blames whatever appears in a log without correlation
- claims certainty without evidence
- changes settings before diagnosis
- proposes destructive resets without backups or approval
