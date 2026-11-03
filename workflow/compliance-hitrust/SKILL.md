---
name: compliance-hitrust
description: Assess HITRUST CSF certification readiness — choose the e1, i1 or r2 assessment, score control domains, map existing ISO 27001, NIST and SOC 2 controls, and estimate the certification path. Use when a healthcare customer demands HITRUST and the user wants to assess which assessment to pursue and how far their own controls are from it.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# HITRUST CSF Assessment

Assess HITRUST Common Security Framework (CSF) certification readiness for "$ARGUMENTS". Determine assessment type, evaluate control domains, and identify the certification path.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-hitrust","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-hitrust","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-hitrust","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **Assessment type determination:**
   - **e1 (Essentials, 1-year)** — assess suitability for low-risk organizations (44 controls)
   - **i1 (Implemented, 1-year)** — assess suitability for moderate assurance needs (182 controls)
   - **r2 (Risk-based, 2-year)** — assess suitability for high assurance requirements (full control set)
   - Evaluate organization risk profile, regulatory requirements, and customer expectations
   - Document recommended assessment type with rationale

3. **Control domain assessment:**
   - **Access Control** — user access management, authentication, authorization, privileged access
   - **Human Resources Security** — screening, terms of employment, security awareness, termination
   - **Risk Management** — risk assessment methodology, risk treatment, risk acceptance criteria
   - **Security Policy** — information security policies, management direction, review cycle
   - **Asset Management** — asset inventory, acceptable use, information classification, media handling
   - **Communications and Operations Management** — operational procedures, change management, capacity, malware, backup, network security, media handling, exchange of information, monitoring
   - **Information Systems Acquisition, Development, Maintenance** — security requirements, secure development, test data, access control to source code
   - **Information Security Incident Management** — incident response, reporting, evidence collection
   - **Business Continuity Management** — BCM framework, BIA, BC plans, testing
   - **Compliance** — legal requirements, security reviews, audit controls
   - **Privacy Practices** — privacy program, notice, choice/consent, collection, use/retention/disposal
   - **Third-Party Assurance** — vendor risk management, third-party agreements, monitoring
   - Score each domain: 1 (policy), 2 (procedures), 3 (implemented), 4 (measured), 5 (managed)

4. **Control mapping from existing frameworks:**
   - Map existing ISO 27001 controls to HITRUST requirements
   - Map existing NIST CSF/800-53 controls to HITRUST requirements
   - Map existing SOC 2 controls to HITRUST requirements
   - Identify controls already satisfied by existing certifications
   - Identify gaps requiring additional HITRUST-specific implementation

5. **Certification path and timeline:**
   - Determine readiness timeline based on current maturity
   - Identify external assessor (authorized HITRUST assessor) requirements
   - Estimate assessment effort (internal preparation, external assessment)
   - Estimate budget (HITRUST licensing, assessor fees, remediation costs)
   - Define milestone timeline from current state to certification

6. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/hitrust.md` following the assessment template structure with:
   - **Assessment Type Recommendation** — e1/i1/r2 with rationale
   - **Control Domain Scoring** — maturity score per domain
   - **Framework Mapping** — existing controls mapped to HITRUST
   - **Gap Analysis** — controls requiring new implementation
   - **Certification Path** — timeline, assessor requirements, budget estimate
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The HITRUST CSF assessment written to `.singularskills/compliance/<project>/01-assess/hitrust.md`. Present a summary to the user highlighting:
- Recommended assessment type (e1/i1/r2)
- Overall control maturity score across domains
- Percentage of controls satisfied by existing framework certifications
- Top 3 gaps requiring remediation
- Estimated timeline to certification readiness

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-hitrust","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-hitrust
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
