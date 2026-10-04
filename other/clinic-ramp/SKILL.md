---
name: clinic-ramp
version: 1.0.0
description: Onboard a new clinic student onto a matter and the clinic's systems fast, with supervision and confidentiality from day one.
author: matrixx0070
tags: [legal-clinic, onboarding, supervision, confidentiality, docketing, first-tasks]
capabilities: []
---

## When to use
Use this when a new student joins the clinic or is assigned to a matter and needs to get productive quickly — what to read, who supervises them, the confidentiality rules, how docketing works, and a safe first task. It builds a shared, supervision-first starting point instead of ad hoc handoffs.

**Not for:** producing the actual work product once ramped (use clinic-memo, clinic-form-generation, or clinic-plain-language-letters), or authorizing a student to act on a matter without supervisor assignment (Rule 5.5).

## Method
1. Confirm the supervising attorney of record and the escalation path before the student touches the file. Every substantive step runs through the supervisor (Rule 5.5).
2. Brief confidentiality on day one: the student handles client information under Rule 1.6, does not discuss matters outside the clinic, and never puts client-identifying facts into external or GenAI tools (Rule 1.6; ABA Op. 512).
3. Give a read list: engagement/scope letter, matter file, key deadlines, and clinic procedures.
   **Decision point:** if the student has any personal or prior connection to the parties, run a conflicts check with the supervisor before granting access.
4. Walk the docketing system: where deadlines live, who enters them, and how a missed date is escalated (Rule 1.3).
5. Assign a bounded, reviewable first task with a clear due date and reviewer.
6. Set the check-in cadence and confirm the student knows they raise questions early rather than guess.

## Example
> New student joins the Nguyen housing matter. You name the supervising attorney and escalation path, cover Rule 1.6 and the no-client-data-in-GenAI rule, share the scope letter and file, walk the docket, run a quick conflicts check, and assign a first task: summarize the file facts for supervisor review by Friday.

## Pitfalls
- Granting file access before a conflicts check with the supervisor.
- Treating confidentiality as a later lesson instead of day-one (Rule 1.6).
- Letting a student act on the matter without supervisor assignment (Rule 5.5).
- Skipping the docketing walkthrough, risking a missed deadline (Rule 1.3).

## Output format
```
STUDENT: <name>   MATTER: <id>   START: <date>
SUPERVISING ATTORNEY: <name>   ESCALATION: <path>
CONFIDENTIALITY BRIEFED: yes (Rule 1.6; no client data in external/GenAI tools)
CONFLICTS CHECK: cleared/pending
READ LIST: <items>
DOCKETING: <system + who enters deadlines>
FIRST TASK: <bounded task> — due <date>, reviewer <name>
CHECK-IN CADENCE: <schedule>
```

## Reference
- ABA Formal Op. 512: confidentiality and competence duties when using GenAI in a clinic.
- Model Rules 1.3 (diligence/deadlines), 1.6 (confidentiality), 5.5 (supervised practice only).
- Clinic norm: supervising attorney assigned and confidentiality briefed before matter access.
