---
name: compliance-gdpr
description: Assess EU GDPR compliance as a scored control-gap assessment — lawful basis, records of processing, DPIAs, data subject rights, transfers, DPO and breach readiness. Use when the user processes EU personal data and wants to see how their processing measures up to GDPR, area by area. Not for legal analysis or a DPA; see /legal-gdpr-compliance or /legal-data-processing-agreement.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# GDPR Assessment

Assess EU General Data Protection Regulation (GDPR) compliance for "$ARGUMENTS". Evaluate lawful basis, data mapping, data subject rights, international transfers, and breach readiness.

See also `/legal-gdpr-compliance` for the legal analysis of GDPR obligations — DPIA/DPO needs, data subject rights procedures and transfer mechanisms.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-gdpr","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-gdpr","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-gdpr","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **Lawful basis assessment (Art 6/9):**
   - Identify each processing activity and its claimed lawful basis
   - Assess validity of consent mechanisms (freely given, specific, informed, unambiguous)
   - Evaluate legitimate interest balancing tests where applicable
   - Review special category data processing (Art 9) and additional conditions
   - Document lawful basis per processing activity in a matrix

3. **Data mapping and records of processing (Art 30):**
   - Assess data inventory completeness (what personal data, categories of data subjects)
   - Map data flows (collection points, storage locations, processing systems, recipients)
   - Evaluate retention periods and deletion schedules
   - Review records of processing activities for controllers and processors
   - Identify gaps in data lineage documentation

4. **Data Protection Impact Assessment (Art 35):**
   - Identify high-risk processing requiring DPIA (profiling, large-scale monitoring, sensitive data)
   - Assess existing DPIAs for completeness and quality
   - Evaluate whether prior consultation with supervisory authority is required (Art 36)
   - Review DPIA methodology and risk scoring approach

5. **Data subject rights procedures:**
   - Assess processes for: access (Art 15), rectification (Art 16), erasure (Art 17), restriction (Art 18), portability (Art 20), objection (Art 21)
   - Evaluate response timelines (one month, extension procedures)
   - Review identity verification procedures for requests
   - Assess automated decision-making and profiling safeguards (Art 22)

6. **International transfers:**
   - Map all transfers outside the EEA
   - Assess transfer mechanisms: adequacy decisions, Standard Contractual Clauses (SCCs), Binding Corporate Rules (BCRs)
   - Evaluate Schrems II compliance (Transfer Impact Assessments, supplementary measures)
   - Review derogations relied upon (Art 49)

7. **DPO and governance:**
   - Assess whether DPO appointment is required (Art 37)
   - Evaluate DPO independence, resources, and reporting line
   - Review privacy by design and by default implementation (Art 25)

8. **Breach notification readiness:**
   - Assess breach detection capabilities
   - Evaluate notification procedures (72 hours to supervisory authority, without undue delay to data subjects)
   - Review breach severity assessment methodology
   - Check breach register maintenance

9. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/gdpr.md` following the assessment template structure with:
   - **Lawful Basis Matrix** — processing activity to legal basis mapping with validity assessment
   - **Data Mapping Assessment** — data inventory completeness and flow documentation
   - **DPIA Status** — high-risk processing identified and DPIA coverage
   - **Rights Procedures** — Compliant / Partial / Non-Compliant rating per right
   - **Transfer Mechanisms** — transfer map with mechanism and Schrems II compliance
   - **Governance** — DPO status, privacy by design maturity
   - **Breach Readiness** — detection, notification, and documentation capability
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The GDPR assessment written to `.singularskills/compliance/<project>/01-assess/gdpr.md`. Present a summary to the user highlighting:
- Overall compliance score across all assessment areas — score = (Compliant + 0.5 × Partial) ÷ applicable requirements (N/A excluded), as a percentage
- Lawful basis coverage and any unsupported processing activities
- Top 3 gaps requiring remediation
- International transfer risk areas

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-gdpr","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-gdpr
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
