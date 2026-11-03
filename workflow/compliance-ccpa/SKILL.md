---
name: compliance-ccpa
description: Assess CCPA/CPRA compliance — applicability thresholds, consumer rights, Do Not Sell or Share and GPC, service provider terms — as a scored control-gap assessment. Use when the user is subject to California privacy law and wants to assess how their own request handling, opt-outs and vendor terms measure up. Not for legal analysis of CCPA notices and contract terms; see /legal-ccpa-compliance.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# CCPA/CPRA Assessment

Assess California Consumer Privacy Act (CCPA) and California Privacy Rights Act (CPRA) compliance for "$ARGUMENTS". Evaluate consumer rights, opt-out mechanisms, data handling practices, and service provider agreements.

See also `/legal-ccpa-compliance` for the legal analysis of CCPA/CPRA notices, consumer-rights procedures and vendor contract terms.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-ccpa","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-ccpa","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-ccpa","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **Applicability threshold assessment:**
   - Assess annual gross revenue threshold ($25M+)
   - Evaluate personal information volume threshold (100,000+ consumers/households/devices)
   - Assess revenue derived from selling/sharing personal information (50%+ of revenue)
   - Determine if organization is a "business," "service provider," or "contractor"
   - Document applicability determination with rationale

3. **Consumer rights assessment:**
   - **Right to Know** — assess processes for disclosing categories and specific pieces of PI
   - **Right to Delete** — assess deletion request handling and exception application
   - **Right to Opt-Out of Sale/Sharing** — assess opt-out mechanisms and signal honoring
   - **Right to Correct** — assess correction request procedures
   - **Right to Limit Use of Sensitive PI** — assess sensitive PI identification and use limitation
   - Evaluate response timelines (45 days, 90-day extension)
   - Review identity verification procedures (reasonable security)
   - Assess authorized agent request handling

4. **Notice and transparency:**
   - Assess notice at collection (categories of PI, purposes, retention periods)
   - Evaluate "Do Not Sell or Share My Personal Information" link placement and functionality
   - Review financial incentive disclosures and opt-in consent
   - Assess privacy policy CCPA/CPRA-specific disclosures
   - Evaluate Global Privacy Control (GPC) signal recognition

5. **Service provider and contractor agreements:**
   - Review service provider agreements for required CCPA provisions
   - Assess contractor agreements and additional restrictions
   - Evaluate third-party data sharing agreements
   - Review subcontractor flow-down requirements
   - Assess due diligence procedures for downstream recipients

6. **Employee and B2B data obligations:**
   - Assess employee personal information handling (full CCPA rights apply)
   - Evaluate B2B contact personal information obligations
   - Review HR privacy notices and employee rights procedures

7. **Data retention and minimization:**
   - Assess data retention schedules per category of PI
   - Evaluate data minimization practices (collection limited to what is necessary)
   - Review purpose limitation compliance

8. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/ccpa.md` following the assessment template structure with:
   - **Applicability Determination** — threshold analysis and entity classification
   - **Consumer Rights Readiness** — Compliant / Partial / Non-Compliant rating per right with process maturity
   - **Notice and Transparency** — collection notice, opt-out link, privacy policy status
   - **Service Provider Framework** — agreement coverage and adequacy
   - **Employee/B2B Data** — HR and B2B compliance status
   - **Data Retention** — schedule completeness and minimization practices
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The CCPA/CPRA assessment written to `.singularskills/compliance/<project>/01-assess/ccpa.md`. Present a summary to the user highlighting:
- Applicability determination and entity classification
- Consumer rights readiness across all six rights
- Overall compliance score — score = (Compliant + 0.5 × Partial) ÷ applicable requirements (N/A excluded), as a percentage
- Top 3 gaps requiring remediation

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-ccpa","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-ccpa
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
