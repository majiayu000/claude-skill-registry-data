---
name: compliance-lgpd
description: Assess compliance with Brazil's LGPD — the ten legal bases, data subject rights, the Encarregado (DPO), ANPD obligations and international transfers. Use when the user has users or customers in Brazil and wants to assess how their own processing measures up to LGPD, including where it differs from GDPR.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# LGPD Assessment

Assess Brazil Lei Geral de Protecao de Dados (LGPD) compliance for "$ARGUMENTS". Evaluate legal bases, data subject rights, DPO requirements, and ANPD obligations.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-lgpd","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-lgpd","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-lgpd","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **Legal bases assessment (10 bases):**
   - Map each processing activity to one of LGPD's 10 legal bases: consent, legal obligation, public administration, research, contract, exercise of rights, life protection, health protection, legitimate interest, credit protection
   - Assess consent mechanisms (free, informed, unambiguous, specific purpose)
   - Evaluate legitimate interest use and balancing report (LIA) where applicable
   - Review special categories of sensitive personal data and additional protections
   - Document legal basis per processing activity

3. **Data subject rights assessment:**
   - Assess procedures for each right: confirmation of processing, access, correction, anonymization/blocking/deletion of unnecessary data, portability, deletion of data processed with consent, information about shared entities, information about consent denial consequences, consent revocation
   - Evaluate response timelines and channel accessibility
   - Review identity verification procedures
   - Assess free-of-charge access requirements

4. **DPO (Encarregado) requirements:**
   - Assess whether DPO/Encarregado appointment is required
   - Evaluate DPO qualifications and independence
   - Review DPO contact information public availability
   - Assess DPO responsibilities and reporting structure

5. **ANPD registration and compliance:**
   - Assess ANPD registration requirements and status
   - Review records of processing activities
   - Evaluate incident notification procedures (reasonable timeframe to ANPD and data subjects)
   - Assess privacy impact report (RIPD / Relatorio de Impacto a Protecao de Dados Pessoais) requirements

6. **International transfers:**
   - Map all transfers outside Brazil
   - Assess transfer mechanisms: countries with adequate protection level, contractual clauses, BCRs, international cooperation, ANPD authorization
   - Evaluate adequacy of transfer safeguards
   - Review data localization requirements if applicable

7. **Security and governance:**
   - Assess technical and administrative security measures
   - Evaluate privacy by design implementation
   - Review data retention and deletion policies
   - Assess anonymization and pseudonymization practices

8. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/lgpd.md` following the assessment template structure with:
   - **Legal Basis Matrix** — processing activity to legal basis mapping
   - **Data Subject Rights** — Compliant / Partial / Non-Compliant rating per right
   - **DPO/Encarregado** — appointment status and compliance
   - **ANPD Compliance** — registration, records, incident notification
   - **RIPD Status** — privacy impact report coverage
   - **International Transfers** — transfer map and mechanism assessment
   - **Security Measures** — technical and administrative safeguard assessment
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The LGPD assessment written to `.singularskills/compliance/<project>/01-assess/lgpd.md`. Present a summary to the user highlighting:
- Overall LGPD compliance score — score = (Compliant + 0.5 × Partial) ÷ applicable requirements (N/A excluded), as a percentage
- Legal basis coverage across processing activities
- DPO and ANPD compliance status
- Top 3 gaps requiring remediation

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-lgpd","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-lgpd
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
