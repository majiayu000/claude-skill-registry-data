---
name: reporting-triage-communication
description: >
  Work productively with triagers after you submit — answer follow-ups, and handle duplicate,
  not-applicable, or severity disputes professionally. Load on "triage asked for more info",
  "they closed it as N/A", "dispute the severity/duplicate", or managing a report thread. Signals:
  a submitted report awaiting/receiving triage, a disagreement on outcome.
domain: reporting
type: reference
stability: learning
modes: [bugbounty]
severity: info
schema_version: 1
---

# Communicating with triage

## When it applies
The report is in and now it's a conversation. How you handle triage largely decides the outcome — a
valid bug can be closed over a bad thread, and a borderline one can be paid with a clear, calm one.

## Why it works
Triagers process a queue under time pressure and act on what's in front of them. A report that
reproduces from the steps alone, and follow-ups that answer the exact question with evidence, remove
every reason to close it — while professionalism keeps the relationship (and your reputation) intact.

## Method
1. **Pre-empt questions** in the report: exact requests/responses, account roles, a clean-session
   repro, and a crisp impact statement — most "need more info" rounds are avoidable.
2. **When asked for more**: give precisely what's requested (a fresh repro, a video, the missing
   header), not a wall of text. Re-confirm from a clean state.
3. **Duplicate**: ask politely for the dupe reference and compare — if yours is genuinely distinct
   (different root cause, endpoint, or a working chain where the original was theoretical), lay out
   the difference factually. If it's truly the same, accept it and move on.
4. **Not applicable / won't fix**: restate the *demonstrated* impact and, if needed, escalate the PoC
   to show real consequence (stay in scope). Don't argue theory — show it.
5. **Severity dispute**: bring the CVSS vector and the program's own scale (`reporting-cvss-scoring`),
   and justify the contested metric with what you proved.
6. **Escalate correctly**: use the platform's mediation/escalation path when stuck; keep it factual.

## Gotchas
- Never threaten public disclosure or go around the process — it voids safe harbor and burns you.
- Tone is leverage: rude threads get minimal effort; respectful, evidence-first threads get benefit
  of the doubt.
- Don't keep pushing a genuine dupe or a truly out-of-scope report — it costs goodwill you'll need later.

## Verify success
The thread moves toward resolution on the merits: your follow-ups answered the actual question with
evidence, and any dispute is argued from demonstrated impact and the program's own policy.

## References
Platform mediation/disclosure guidelines; the `reporting-bug-bounty-writeup`, `reporting-cvss-scoring`,
and `tradecraft-bugbounty-platforms` skills.
