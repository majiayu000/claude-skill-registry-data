---
name: compliance-nis2
description: Assess NIS2 Directive compliance — essential or important entity classification, the ten Article 21 risk management measures, 24 and 72 hour incident reporting, and supply chain security. Use when the user operates in or serves critical EU sectors and wants to assess their entity classification and how their own security measures meet NIS2.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# NIS2 Assessment

Assess compliance with the NIS2 Directive (EU 2022/2555) for "$ARGUMENTS". Classify the entity, evaluate the 10 minimum security measures, assess incident reporting readiness, and score supply chain security.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-nis2","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-nis2","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-nis2","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **Entity classification:**
   - Determine if the entity is "essential" or "important" under NIS2 Article 3
   - Assess sector classification (Annex I high-criticality vs. Annex II other critical sectors)
   - Determine size thresholds (medium: 50+ employees or EUR 10M+ turnover; large: 250+ or EUR 50M+)
   - Document classification rationale and implications for obligations

3. **Assess 10 minimum measures (Article 21):**
   - **Risk analysis and information system security policies** — assess policy existence, scope, review cadence
   - **Incident handling** — assess detection, response, and recovery capabilities
   - **Business continuity and crisis management** — assess BCP, DR plans, backup management
   - **Supply chain security** — assess vendor risk management, contractual security requirements
   - **Network and information systems security** — assess acquisition, development, vulnerability handling
   - **Vulnerability disclosure** — assess coordinated vulnerability disclosure policies
   - **Cybersecurity risk management effectiveness** — assess measurement and evaluation practices
   - **Cryptography and encryption** — assess encryption policies and implementation
   - **Human resources security** — assess security awareness, training, access control policies
   - **Access control and asset management** — assess identity management, MFA, asset inventory
   - Score each measure: Compliant / Partially Compliant / Non-Compliant with evidence

4. **Incident reporting readiness (Article 23):**
   - Assess capability to issue early warning within 24 hours of awareness
   - Assess capability to submit incident notification within 72 hours
   - Assess capability to deliver final report within 1 month
   - Evaluate CSIRT communication channels and procedures
   - Test reporting workflow against scenario

5. **Supply chain security (Article 22):**
   - Assess critical supplier identification and risk assessment
   - Evaluate contractual security requirements with suppliers
   - Assess supply chain incident notification procedures
   - Review supplier audit and monitoring practices

6. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/nis2.md` following the assessment template structure with:
   - **Entity Classification** — essential vs. important, sector, size, obligations
   - **Minimum Measures Assessment** — detailed scoring of all 10 measures
   - **Incident Reporting Readiness** — 24hr/72hr/1mo capability assessment
   - **Supply Chain Security** — supplier risk management maturity
   - **Overall Compliance Score** — score = (Compliant + 0.5 × Partially Compliant) ÷ the 10 minimum security measures, as a percentage; show it with a heatmap
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The NIS2 assessment written to `.singularskills/compliance/<project>/01-assess/nis2.md`. Present a summary to the user highlighting:
- Entity classification result
- Overall compliance score
- Top 3 gaps requiring remediation
- Incident reporting readiness status

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-nis2","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-nis2
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
