---
name: compliance-soc2
description: Assess SOC 2 readiness as a scored control-gap assessment — scope the Trust Services Criteria, test the Security and other in-scope criteria, and decide between Type I and Type II. Use when customers are asking for a SOC 2 report and the user wants to assess which criteria apply and where their controls fall short. Not for a policy and evidence prep plan; see /legal-soc2-prep.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# SOC 2 Assessment

Assess SOC 2 Type II readiness for "$ARGUMENTS". Evaluate control design and operating effectiveness across applicable trust services criteria, and determine Type I vs. Type II readiness.

See also `/legal-soc2-prep` for the policy set, control matrix and evidence collection plan to get audit-ready.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-soc2","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-soc2","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-soc2","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **Trust services criteria scoping:**
   - Security (CC series) — always in scope, mandatory for all SOC 2 engagements
   - Availability (A series) — assess applicability based on SLAs and uptime commitments
   - Processing Integrity (PI series) — assess applicability based on data processing accuracy requirements
   - Confidentiality (C series) — assess applicability based on confidential data handling
   - Privacy (P series) — assess applicability based on personal information processing
   - Document scoping decisions with rationale

3. **Security (Common Criteria) assessment:**
   - **CC1: Control Environment** — assess tone at top, organizational structure, security policies
   - **CC2: Communication and Information** — assess internal/external communication of security
   - **CC3: Risk Assessment** — assess risk identification, analysis, and management processes
   - **CC4: Monitoring Activities** — assess ongoing monitoring, logging, alerting
   - **CC5: Control Activities** — assess control design, implementation, and technology controls
   - **CC6: Logical and Physical Access** — assess access controls, authentication, MFA, physical security
   - **CC7: System Operations** — assess change management, incident detection, incident response
   - **CC8: Change Management** — assess change authorization, testing, deployment processes
   - **CC9: Risk Mitigation** — assess risk mitigation strategies, vendor management, insurance
   - Score each criterion: control designed effectively / operating effectively / gap

4. **Additional criteria assessment** (for each in-scope criterion):
   - Assess control design against AICPA points of focus
   - Evaluate evidence of operating effectiveness over the observation period
   - Identify controls with design gaps vs. operating gaps
   - Document compensating controls where applicable

5. **Type I vs. Type II readiness:**
   - Assess if controls are designed effectively (Type I ready)
   - Assess if controls have been operating effectively for 3-12 months (Type II ready)
   - Identify controls needing a burn-in period before Type II audit
   - Recommend observation period length

6. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/soc2.md` following the assessment template structure with:
   - **Scope Decision** — applicable trust services criteria with rationale
   - **Common Criteria Assessment** — CC1-CC9 detailed scoring
   - **Additional Criteria Assessment** — A/PI/C/P scoring (if in scope)
   - **Type I Readiness** — design effectiveness summary
   - **Type II Readiness** — operating effectiveness and burn-in status
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The SOC 2 assessment written to `.singularskills/compliance/<project>/01-assess/soc2.md`. Present a summary to the user highlighting:
- Trust services criteria in scope
- Type I vs. Type II readiness determination
- Overall readiness score — score = (operating effectively + 0.5 × designed effectively) ÷ applicable criteria, as a percentage (gap counts as 0)
- Top 3 gaps requiring remediation before audit

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-soc2","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-soc2
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
