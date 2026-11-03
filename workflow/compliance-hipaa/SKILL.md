---
name: compliance-hipaa
description: Assess HIPAA compliance — covered entity or business associate status, the Privacy Rule, Security Rule safeguards, the Breach Notification Rule and BAA coverage. Use when the user handles patient health data for US healthcare customers and wants to assess how their own safeguards and BAAs measure up to HIPAA.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# HIPAA Assessment

Assess Health Insurance Portability and Accountability Act (HIPAA) compliance for "$ARGUMENTS". Evaluate Privacy Rule, Security Rule, Breach Notification Rule, and Business Associate Agreement coverage.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-hipaa","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-hipaa","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-hipaa","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **Entity classification:**
   - Determine if covered entity (health plan, healthcare clearinghouse, healthcare provider with electronic transactions)
   - Determine if business associate (handles PHI on behalf of covered entity)
   - Assess hybrid entity considerations
   - Document entity classification with rationale

3. **Privacy Rule assessment:**
   - Assess permitted uses and disclosures of Protected Health Information (PHI)
   - Evaluate minimum necessary standard implementation
   - Review individual rights: access, amendment, accounting of disclosures, restriction requests, confidential communications, right to receive notice of privacy practices
   - Assess Notice of Privacy Practices (NPP) content and distribution
   - Evaluate authorizations for uses/disclosures not otherwise permitted
   - Review de-identification methods (safe harbor vs expert determination)
   - Assess marketing and fundraising communication compliance

4. **Security Rule assessment:**
   - **Administrative safeguards:** security management process (risk analysis, risk management, sanction policy, information system activity review), assigned security responsibility, workforce security, information access management, security awareness training, security incident procedures, contingency plan, evaluation
   - **Physical safeguards:** facility access controls, workstation use, workstation security, device and media controls
   - **Technical safeguards:** access control (unique user ID, emergency access, automatic logoff, encryption), audit controls, integrity controls (mechanism to authenticate ePHI), person/entity authentication, transmission security (integrity controls, encryption)
   - Classify each safeguard as required vs addressable
   - Score each safeguard: implemented / partially implemented / not implemented

5. **Breach Notification Rule assessment:**
   - Assess breach risk assessment methodology (four-factor test)
   - Evaluate individual notification procedures (within 60 days of discovery)
   - Assess HHS/OCR notification procedures (within 60 days for breaches affecting 500+ individuals, annual log for smaller breaches)
   - Review media notification requirements (500+ in a state/jurisdiction)
   - Evaluate breach documentation and investigation processes

6. **Business Associate Agreements (BAAs):**
   - Inventory all business associates handling PHI
   - Assess BAA coverage (all BAs have current, compliant agreements)
   - Review BAA terms for required provisions
   - Evaluate BA monitoring and compliance verification procedures
   - Assess subcontractor BAA flow-down requirements

7. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/hipaa.md` following the assessment template structure with:
   - **Entity Classification** — covered entity, business associate, or hybrid determination
   - **Privacy Rule Assessment** — use/disclosure controls, individual rights, NPP status
   - **Security Rule Assessment** — administrative, physical, technical safeguard scoring
   - **Breach Notification Readiness** — risk assessment methodology, notification procedures
   - **BAA Inventory** — coverage assessment and agreement adequacy
   - **Risk Analysis** — overall risk posture and highest-risk areas
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The HIPAA assessment written to `.singularskills/compliance/<project>/01-assess/hipaa.md`. Present a summary to the user highlighting:
- Entity classification determination
- Privacy Rule, Security Rule, and Breach Notification readiness scores — per rule, score = (implemented + 0.5 × partially implemented) ÷ applicable safeguards or requirements, as a percentage, using implemented / partially implemented (Security Rule safeguards) or Compliant / Partial (other items)
- BAA coverage percentage
- Top 3 gaps requiring remediation

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-hipaa","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-hipaa
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
