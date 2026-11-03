---
name: compliance-pci-dss
description: Assess PCI DSS compliance — SAQ type and merchant level, cardholder data environment scope, the 12 requirements, and scope reduction options such as tokenization. Use when the user takes card payments and wants to assess their own SAQ type and PCI compliance or find ways to shrink their PCI scope.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: compliance
  phase: 1
  artifact: 01-assess/
---

# PCI DSS Assessment

Assess Payment Card Industry Data Security Standard (PCI DSS) compliance for "$ARGUMENTS". Determine SAQ type, assess the 12 requirements, and identify scope reduction opportunities.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"compliance-pci-dss","workflow":"compliance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess/","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the GRC Lifecycle workflow (`compliance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `compliance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"compliance-pci-dss","workflow":"compliance","phase":1,"project":"<project>","event":"refused","artifact":"01-assess/","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"compliance-pci-dss","workflow":"compliance","phase":1,"project":"<project>","event":"started","artifact":"01-assess/","note":""}`.

Read `.singularskills/compliance/<project>/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "<project>". Run `/compliance-regulatory-landscape <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `references/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `references/assessment-template.md` for output structure
   - Read `.singularskills/compliance/<project>/00-scope.md` for scope and control framework context

2. **SAQ type determination:**
   - Assess payment processing model and cardholder data flow
   - Determine applicable SAQ: A (card-not-present, fully outsourced), A-EP (e-commerce with partial outsourcing), B (imprint/standalone terminals), C (payment application connected to internet), D (all others), P2PE (validated P2PE merchants)
   - Evaluate merchant level (1-4) based on transaction volume
   - Document SAQ type and merchant level with rationale

3. **Scope assessment:**
   - Identify all systems that store, process, or transmit cardholder data (CHD)
   - Map the Cardholder Data Environment (CDE)
   - Identify connected-to and security-impacting systems
   - Assess network segmentation effectiveness
   - Document in-scope systems, applications, and network segments

4. **12 requirements assessment:**
   - **Req 1: Network security controls** — firewall/network security device configuration, CDE isolation
   - **Req 2: Secure configurations** — vendor default passwords removed, system hardening standards
   - **Req 3: Protect stored account data** — data retention policies, rendering PAN unreadable, key management
   - **Req 4: Encrypt transmission** — strong cryptography for CHD over open/public networks
   - **Req 5: Anti-malware** — malware protection on all systems, anti-malware mechanisms current
   - **Req 6: Secure development** — secure SDLC, patch management, web application security (WAF)
   - **Req 7: Restrict access** — need-to-know access control, access control systems
   - **Req 8: Identify users** — unique IDs, MFA for CDE access, strong authentication policies
   - **Req 9: Physical security** — physical access controls to CDE, visitor management, media security
   - **Req 10: Logging and monitoring** — audit trails, log review, time synchronization, SIEM
   - **Req 11: Security testing** — vulnerability scans (ASV quarterly), penetration testing, IDS/IPS, file integrity monitoring
   - **Req 12: Security policies** — information security policy, risk assessment, security awareness, incident response
   - Score each requirement: in place / in place with remediation / not in place / not applicable

5. **Scope reduction opportunities:**
   - Evaluate tokenization feasibility (replace CHD with tokens)
   - Assess Point-to-Point Encryption (P2PE) validated solutions
   - Review outsourcing options for payment processing
   - Evaluate network segmentation improvements
   - Identify quick wins for reducing in-scope systems

6. **Write the artifact** to `.singularskills/compliance/<project>/01-assess/pci-dss.md` following the assessment template structure with:
   - **SAQ Determination** — SAQ type and merchant level with rationale
   - **Scope Definition** — CDE map, in-scope systems, segmentation assessment
   - **12 Requirements Assessment** — scoring per requirement with sub-requirement detail
   - **Scope Reduction Opportunities** — tokenization, P2PE, outsourcing options
   - **ASV and Penetration Testing Status** — current scan and test coverage
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The PCI DSS assessment written to `.singularskills/compliance/<project>/01-assess/pci-dss.md`. Present a summary to the user highlighting:
- SAQ type and merchant level determination
- Overall compliance score across 12 requirements — score = (in place + in place with remediation) ÷ applicable requirements (not applicable excluded), as a percentage
- Scope reduction opportunities with estimated effort savings
- Top 3 gaps requiring remediation

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"compliance-pci-dss","workflow":"compliance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess/","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: compliance-pci-dss
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
