---
name: meeting-classifier
description: "Classify a teacher's meeting-related request, then route it. Use whenever a teacher mentions a meeting or invite — faculty, grade-level/PLC, department, data, or emergency meetings; evaluation observations, post-observation debriefs, and interim walkthroughs; parent-teacher conferences; calls home about discipline or a medical issue; IEP and Section 504 meetings; MTSS; pre-planning, planning, post-planning; PD; safety training; special-event planning. It pieces the meeting together from context clues (email subject and body, the sender and their title, prior threads, call notes, and calendar invites) using whatever connectors are available, identifies the student and guardians, surfaces a student's medical action plan on file when relevant, attaches the IEP/504 required-meeting advisory, and recommends the right skill. Do NOT use it to author lessons, assessments, IEP/504 content, or letters (it routes to those skills); it never makes a determination about an individual student's plan, medical or legal."
---

# meeting-classifier

Classifies a teacher's meeting + what they want done about it, then **routes** to the right TOS skill —
**decision support, not a determination**. It classifies + routes (and produces a light prep brief); it
does **not** author the meeting artifacts (sibling skills do).

> **Read first — boundaries (`SECURITY_AND_SAFETY.md`).** This skill never makes a determination about
> an individual student's IEP/504, eligibility, medical, or legal status — it **escalates** those to a
> human/team. Medical/ePHI is **surfaced from the source on file (attributed; a signature is not required), never fabricated**
> (`references/student-data-policy.md`); real student data never enters a tracked/committed file.

## 1. Resolve context, connectors, and student first
- **Context** — resolve the teaching-context contract (`shared/context/`), including the `department`
  scope; carry it through the handoff.
- **Connectors** — read what's available (`shared/connectors/`): use whatever is connected, **degrade**
  to what you have permission for, and **converge** via alternate sources; never present a disabled
  connector as an active path; lower confidence on degraded paths.
- **Student** — when a meeting concerns a student, resolve the profile (`shared/students/`,
  identification mode name-by-default; SIS authoritative when connected). Surface guardian contacts for
  a call home, and a **medical action plan from the source on file** when the meeting/call is medical (safety-critical).

## 2. Follow the pipeline (`references/method.md`)
Within Generation the domain work is **classification**:
1. **Gather clues** from the available evidence per `references/evidence-model.md` (strong→weak:
   explicit statement, calendar event, sender title/role, attendee roles, subject/body, prior thread,
   transcript/notes, filename).
2. **Classify the meeting type** (one of the taxonomy in `references/meeting-taxonomy.md`).
3. **Classify the request intent** (prep, draft communication, summarize/minutes, identify attendees,
   schedule/triage, documentation/compliance, extract-only, or unknown).
4. **Attach advisories** — for `iep_meeting`/`section_504_meeting` attach the required-cadence advisory
   (an existing plan is reviewed on a legal cadence; `verify_on_source`; cite IDEA / Section 504); for a
   medical meeting, surface the action plan from the source on file and flag safety-critical.
5. **Decide honestly** — when two meeting types are materially plausible (e.g., annual-review vs interim
   observation) or sources conflict, emit a **minority report** via the resolver
   (`shared/context/sot_resolver.py`; policy `shared/context/minority-report.md`) instead of guessing;
   when evidence is too weak, return `unknown` and recommend `manual_review` / one clarifying question.

## 3. Route (don't author)
Use the routing table in `references/meeting-taxonomy.md` (parent contact → `family-communication`;
IEP/504 → `special-education-support` + escalate; MTSS → `intervention-mtss`; observations →
`professional-learning` or `school-administration`; planning → `curriculum-mapping`/`lesson-planner`).
Only recommend a skill that exists, or `manual_review`. The bundled `scripts/classify_meeting.py` gives a
fast first-pass label from compact clues; if it conflicts with stronger evidence, follow the evidence.

## 4. Artifacts
See `references/artifact-types.md` — a meeting classification record, a routing recommendation, and a
light prep brief / handoff packet (with guardian-contact info + a medical safety banner when relevant).
No full artifact authoring here.

## 5. Output: always emit the metadata block
End with the metadata block from `references/metadata-schema.md`, including the quality decision and
`human_review_required: true` — outputs are decision support, not final professional, medical, or legal
determinations. Placeholders only in any committed example; real student PII/ePHI stays in the storage
adapter (`shared/students/`), never committed.
