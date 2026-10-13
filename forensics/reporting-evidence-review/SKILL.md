---
name: reporting-evidence-review
description: >
  Pre-handoff audit of an engagement package — scope confirmed, every finding traceable to
  reproducible evidence, activity-log leads closed with rationale, artifact hashes intact.
  Load before writing the final report or handing a case to a teammate/client, on "is this
  ready to report", "review my engagement notes", QA of findings/ + notes.md. Signals:
  findings folder full, handoff, report QA, evidence chain, chain of custody.
domain: reporting
type: checklist
stability: learning
modes: [pentest, bugbounty, defense]
severity: info
mitre: []
tools: []
schema_version: 1
---

# Pre-handoff evidence review

## When it applies
The active work is done — findings drafted in `findings/`, `notes.md` complete, activity log
populated — and you're about to write the report (`reporting-pentest-report`,
`reporting-bug-bounty-writeup`) or hand the case to a teammate, client, or incident
stakeholder. This is a **read-only** audit of `engagements/<target>/`: it never touches the
target and never adds new testing. If a check fails, go back to the owning skill — don't patch
the report to hide the gap.

## Why it works
Reports get killed in review for the same few reasons: a finding with no reproducible proof, a
lead silently dropped, scope ambiguity, or an artifact that no longer matches its hash. A
structured pass over the package catches these while they're still cheap to fix and produces a
handoff another human can defend without you in the room.

## Method
Work the package top to bottom; every failure is a blocker until fixed or explicitly waived
with a written reason.

**1. Scope & readiness**
- [ ] `scope.txt` exists and every tested asset traces back to it (or to `roe.md` for bounty).
- [ ] Anything out of scope that was touched is disclosed, not buried.
- [ ] The objective from `plan.md` is answered, or the gap is stated.

**2. Evidence → finding traceability**
- [ ] Every `findings/*.md` has copy-pasteable repro steps and minimal proof of impact.
- [ ] Every finding cites its exact evidence (request, command + output, screenshot, artifact
      path) — and that evidence exists in the package.
- [ ] No orphaned evidence: each capture/log/screenshot is referenced by a finding or
      `notes.md`.
- [ ] Severity is defensible (`reporting-cvss-scoring`) and the finding survived false-positive
      checks (`reporting-triage-validation`).

**3. Lead & timeline coverage**
- [ ] Every lead in `.secskills/activity.jsonl` / `plan.md` has a terminal status — `confirmed`,
      `failed` (with variation-matrix rationale), `blocked`, or `skipped` (with why). No lead
      silently evaporates.
- [ ] `notes.md` timestamps let a reviewer reconstruct the order of operations; clock and
      timezone noted.
- [ ] Not-attempted surface is listed — what you didn't test and why (time, RoE, risk).

**4. Fixity (where artifacts matter — forensics, malware, captured data)**
- [ ] SHA-256 recorded for each acquired artifact at intake; re-hash now and compare. A
      mismatch is a hard failure — quarantine the copy, re-acquire or declare it.
- [ ] Chain of custody: who acquired what, when, with which command.

**5. Handoff**
- [ ] Save the review result (passes, failures, waivers) into the package — e.g.
      `findings/00-review.md` — so it ships with the report.
- [ ] Then run the report skill. A review result is not legal advice and doesn't replace your
      organization's evidence-handling procedures.

## Gotchas
- "It worked yesterday" is not evidence — capture it in the package or it doesn't exist.
- One-time observations (a state you could only see once) are allowed only with an explicit
  note of the limitation; don't dress them up as reproducible.
- Sanitize before handoff: third-party data, credentials, and internal paths in evidence need
  redaction with the reason noted.
- Don't fix gaps by editing findings to say less — go back and test, or mark the lead
  `blocked` honestly.
- Skipped hash verification needs a written reason ("no acquired artifacts — web-only
  engagement"), not silence.

## Verify success
A reviewer who was never on the engagement can start from `scope.txt`, follow any finding to
its evidence and reproduce it, see every lead's disposition, and confirm artifact integrity —
with the review record saved alongside the report.

## References
NIST SP 800-86 (forensic techniques in incident response); SWGDE best practices for forensic
acquisition and evidence archiving; `reporting-triage-validation`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
