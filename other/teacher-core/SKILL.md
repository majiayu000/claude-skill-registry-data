---
name: teacher-core
description: "The Teacher Operating System hub for K-12 educators. Use this whenever a teacher, special-education teacher, interventionist, instructional coach, curriculum specialist, administrator, or district leader needs a standards-aligned, differentiated educational artifact — lesson and unit plans, assessments and rubrics, instructional slide decks, curriculum maps and pacing guides, IEP/504 supports and accommodations, MTSS/intervention plans, family communication, coaching/PD tools, or walkthrough/implementation resources. It classifies the request and routes it to the right TOS capability skill, runs the shared production pipeline, and applies the Quality Gates before anything is called final. Make sure to use this skill whenever the user mentions lessons, units, assessments, rubrics, standards alignment (CCSS/NGSS/state), differentiation/UDL, accommodations, IEPs, MTSS/RTI, pacing, or teaching materials, even if they don't name a specific document type. Do NOT use it for non-education tasks or general coding."
---

# Teacher Operating System — Core (hub)

`teacher-core` is the hub of the TOS skill ecosystem. It turns an educator's request into a
standards-aligned, differentiated, quality-gated artifact by routing to the right capability skill
and running one shared, governed pipeline.

## 1. Mission & boundaries
Produce nearly any K-12 educational artifact a teacher needs — well-aligned, differentiated, and
trustworthy. Every output is **decision support, not a final professional or legal determination**;
a qualified educator reviews and adapts it. Operate within educational, legal, and accessibility
constraints (`SECURITY_AND_SAFETY.md`). Never use real student data — placeholders only.

## 2. Who you're serving (personas)
Classroom Teacher · Special Education Teacher · Interventionist · Instructional Coach · Curriculum
Specialist · Administrator · District Leader. Persona sets sensible defaults; it never restricts what
can be requested. Details: `shared/personas/personas.md`.

## 3. The pipeline (always)
Follow `references/method.md`:
`Request → Routing → Protocol Enforcement → Generation → Validation → Quality Gates →
Approval/Certification → Release`.
- **Context resolution (first)** — resolve the teaching-context contract (`shared/context/`):
  state / district / school_type / program(s) / instructional_model / mandates / uploaded SOPs. Apply
  the school-type **exception rule-set** and **authority precedence**, and **carry the contract through
  every handoff** (overrides logged, never silent). Default to traditional-public Florida when
  unstated; log the assumption. School type governs standards applicability (home-ed/private contexts
  do not silently inherit the B.E.S.T./NGSSS mandate).
- **Routing** — classify persona × artifact × subject × grade band (× context), then dispatch (§4).
- **Protocol Enforcement** — log assumptions (`references/assumptions-protocol.md`), initialize the
  metadata block (`references/metadata-schema.md`), arm standards verification
  (`references/standards-verification.md`).
- **Generation** — `Analysis → Standards Alignment → Differentiation → Generation` (the capability
  skill owns this; standards from `shared/standards/`, supports from `shared/differentiation/`).
- **Validation → Quality Gates** — self-check against `references/quality-gates.md`, then the
  authoritative gate via `quality-review`. Resolve contradictions with
  `protocol-layer/conflict-protocol.md`; degrade honestly with `protocol-layer/failure-recovery.md`.

## 4. Routing & orchestration
Use `references/routing-map.md` (mirrors `ROUTING_MODEL.md`). Route a single request to the best-fit
skill. **Meeting-centered requests** (a meeting, invite, or calendar event) classify via
`meeting-classifier` first — it returns the meeting type, intent, IEP/504 advisories, subject
student/guardians, and the recommended owner skill, then route there. When a request bundles several artifacts (e.g., "a unit + its assessments + slides + a parent
letter"), **orchestrate a multi-skill workflow** per `references/workflows.md`: decompose → order →
share one standard/persona/grade-band + teaching-context contract across steps → gate each piece with `quality-review` →
assemble one coherent bundle. If the request is genuinely ambiguous, ask one clarifying question
rather than guess.

## 5. Standards, differentiation, quality (the shared engines)
- **Standards** — select + cite verifiable standards (CCSS/NGSS/state), framework + version; never
  fabricate (`shared/standards/`, `references/standards-verification.md`).
- **Differentiation** — UDL by default, plus tiering / EL / IEP supports (`shared/differentiation/`).
- **Quality** — the 9-dimension Quality Gates rubric; nothing is "Final" below 4.0 or with a critical
  failure (`references/quality-gates.md`; full spec `references/quality-gates.md`).

## 6. Output: always emit the metadata block
End every artifact with the metadata block from `references/metadata-schema.md`: artifact type,
persona, grade band, subject, standards set + cited codes, differentiation applied, the
teaching-context contract (district / school-type / mandates / SOPs; `shared/context/`), the quality
decision (per-dimension scores + composite), assumptions, and `human_review_required: true`.
