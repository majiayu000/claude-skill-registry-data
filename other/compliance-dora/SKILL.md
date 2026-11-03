---
name: compliance-dora
description: Assess EU financial-sector ICT resilience under DORA, plus PSD2 strong customer authentication and MiFID II trading-system controls. Use when the user is an EU bank, insurer, payment or investment firm, or its ICT provider, and wants to assess how their own resilience program measures up to DORA.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# DORA / PSD2 / MiFID II Assessment

Assess Digital Operational Resilience Act (DORA), PSD2, and MiFID II compliance for "$ARGUMENTS". Evaluate ICT risk management, incident reporting, operational resilience testing, and third-party risk management.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-dora","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-dora","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-dora","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **DORA (Digital Operational Resilience Act) assessment:**
   - **ICT Risk Management Framework:**
     - Assess ICT risk management strategy and policies
     - Evaluate ICT asset inventory and dependency mapping
     - Review ICT risk identification, protection, detection, response, and recovery capabilities
     - Assess business impact analysis for ICT disruptions
     - Evaluate ICT change management and patch management
   - **Incident Reporting:**
     - Assess major ICT incident classification methodology
     - Evaluate reporting timelines: initial notification (within 4 hours of classification), intermediate report (within 72 hours), final report (within 1 month)
     - Review incident root cause analysis and post-incident review processes
     - Assess significant cyber threat voluntary reporting
   - **Digital Operational Resilience Testing:**
     - Assess basic testing program (vulnerability assessments, network security, gap analysis, software security, source code reviews, performance testing)
     - Evaluate Threat-Led Penetration Testing (TLPT) requirements for significant entities
     - Review testing frequency and scope adequacy
     - Assess use of qualified external testers
   - **Third-Party Risk Management:**
     - Assess register of all ICT third-party service providers
     - Evaluate contractual arrangements with ICT providers (SLA, audit rights, exit strategies)
     - Review concentration risk assessment for critical ICT providers
     - Assess oversight of critical third-party providers by European Supervisory Authorities
   - **Information Sharing:**
     - Assess participation in cyber threat information sharing arrangements
     - Evaluate information sharing agreements and mechanisms

3. **PSD2 (Payment Services Directive 2) assessment:**
   - Assess Strong Customer Authentication (SCA) implementation
   - Evaluate SCA exemptions application (low-value, trusted beneficiary, TRA)
   - Review secure communication standards for payment initiation and account information
   - Assess incident reporting to competent authority (major operational/security incidents)
   - Evaluate fraud monitoring and reporting mechanisms
   - Review API and third-party provider (TPP) access security

4. **MiFID II assessment:**
   - Assess algorithmic trading controls and circuit breakers
   - Evaluate business continuity arrangements for trading systems
   - Review record keeping requirements (communications, transactions, orders)
   - Assess IT governance and operational risk management
   - Evaluate outsourcing arrangements for critical/important functions
   - Review disaster recovery and system resilience

5. **ICT risk management maturity:**
   - Score overall ICT risk management maturity (initial, developing, defined, managed, optimized)
   - Identify areas where maturity falls below regulatory expectations
   - Compare maturity across DORA, PSD2, and MiFID II requirements
   - Prioritize maturity improvement areas by regulatory impact

6. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/dora.md` following the assessment template structure with:
   - **DORA ICT Risk Management** — framework maturity and gap assessment
   - **DORA Incident Reporting** — classification methodology and timeline readiness
   - **DORA Resilience Testing** — basic testing and TLPT readiness
   - **DORA Third-Party Risk** — provider register, contract assessment, concentration risk
   - **PSD2 Assessment** — SCA compliance, secure communication, incident reporting
   - **MiFID II Assessment** — algorithmic controls, BCP, record keeping
   - **ICT Maturity Score** — overall and per-domain maturity levels
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The DORA/PSD2/MiFID II assessment written to `.singularskills/compliance/<project>/01-assess/dora.md`. Present a summary to the user highlighting:
- Overall ICT risk management maturity level
- DORA readiness score across all five pillars — score = (Compliant + 0.5 × Partial) ÷ applicable requirements (N/A excluded), as a percentage
- PSD2 SCA compliance status
- Top 3 gaps requiring remediation

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-dora","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-dora
workflow: compliance
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```

End the artifact with this paragraph, verbatim:

> **Not legal or audit advice.** This artifact supports preparation for compliance work; certification, attestation and regulatory conclusions require a qualified auditor or counsel.
